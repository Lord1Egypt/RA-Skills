#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aholo 3D Reconstruction Skill — International (OpenAPI v1, global gateway)

Flow (Aholo Open Platform global site, gateway https://api.aholo3d.com, world APIs under /global prefix):
1) GET /global/world/v1/asset/token
2) OUS direct / multipart upload (/ous/api/* has no /global prefix; globalDomain often https://ous-sg.kujiale.com)
3) POST /global/world/v1/reconstructions or /global/world/v1/generations
4) GET /global/world/v1/{worldId}
"""

import hashlib
import json
import mimetypes
import os
import re
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


SITE_CONFIG = {
    "base_url": "https://api-beta.aholo3d.com",
    "token_base_url": "https://api.aholo3d.com",
    "path_prefix": "/global",
    "viewer_url_template": "https://studio.aholo3d.com/3dgs-model/{world_id}",
    "api_keys_url": "https://labs.aholo3d.com/api-keys",
    "skill_script_path": ".cursor/skills/aholo-3dgs-reconstruction-global/aholo_reconstruct.py",
}


def _world_api_paths(path_prefix: str) -> Dict[str, str]:
    return {
        "upload_token": f"{path_prefix}/world/v1/asset/token",
        "reconstructions": f"{path_prefix}/world/v1/reconstructions",
        "generations": f"{path_prefix}/world/v1/generations",
        "world_detail": f"{path_prefix}/world/v1/{{worldId}}",
    }


_CFG = SITE_CONFIG
_PATHS = _world_api_paths(_CFG["path_prefix"])
PATH_UPLOAD_TOKEN = _PATHS["upload_token"]
PATH_RECONSTRUCTIONS = _PATHS["reconstructions"]
PATH_GENERATIONS = _PATHS["generations"]
PATH_WORLD_DETAIL = _PATHS["world_detail"]

HEADER_X_SOURCE = "x-source"
X_SOURCE_VALUE_SKILLS = "skills"

WORLD_TERMINAL_STATUS = {"SUCCEEDED", "FAILED", "CANCELED", "TIMEOUT", "REJECTED"}
WORLD_STATUS_DESC = {
    "PENDING": "Queued",
    "WAITING": "Waiting",
    "RUNNING": "Running",
    "SUCCEEDED": "Succeeded",
    "FAILED": "Failed",
    "CANCELED": "Canceled",
    "TIMEOUT": "Timed out",
    "REJECTED": "Rejected",
    "PREPROCESSING": "Preprocessing",
}


@contextmanager
def step_timer(step_name: str):
    start = time.time()
    print(f"[start] {step_name}")
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"[done] {step_name} | elapsed: {elapsed:.2f}s")


def _is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def _auth_hint(error_msg: str, code: Optional[str] = None) -> str:
    text = f"{error_msg} {code or ''}".lower()
    if any(x in text for x in ["auth", "authorization", "401", "403", "appkey", "api key", "apikey"]):
        return "Check that `AHOLO_API_KEY` is correct and the `Authorization` header is the raw API Key (no Bearer prefix)."
    return ""


def _format_hint(error_msg: str) -> str:
    msg = error_msg.lower()
    if "format" in msg or "h.264" in msg or "codec" in msg:
        return "Ensure the video is standard MP4 with H.264 encoding; use ffprobe to inspect and ffmpeg to transcode if needed."
    return ""


class AholoClient:
    BASE_URL = SITE_CONFIG["base_url"]
    TOKEN_BASE_URL = SITE_CONFIG["token_base_url"]

    @staticmethod
    def _is_open_api_error(payload: Any) -> bool:
        return isinstance(payload, dict) and "status" in payload and "message" in payload

    @staticmethod
    def _open_api_error_message(payload: Dict[str, Any], default: str = "Unknown error") -> str:
        msg = str(payload.get("message") or default)
        details = payload.get("details") or {}
        meta = details.get("metaData") or {}
        biz_code = meta.get("bizCode")
        if biz_code:
            msg = f"{msg} (bizCode={biz_code})"
        return msg

    @staticmethod
    def _open_api_biz_code(payload: Dict[str, Any]) -> Optional[str]:
        details = payload.get("details") or {}
        meta = details.get("metaData") or {}
        biz = meta.get("bizCode")
        return str(biz) if biz is not None else None

    def _parse_open_api_json(self, resp: requests.Response) -> Any:
        """Parse Open Platform JSON; tolerate UTF-8 BOM, leading/trailing whitespace, trailing junk after valid JSON."""
        text = (resp.text or "").strip().lstrip("\ufeff")
        if not text:
            raise ValueError("Empty response body")
        try:
            decoder = json.JSONDecoder()
            obj, end = decoder.raw_decode(text)
            return obj
        except json.JSONDecodeError:
            # Expected success body is {"worldId": "..."}; some gateways may return bare worldId text.
            if re.fullmatch(r"[A-Za-z0-9_-]{4,200}", text):
                return text
            raise ValueError("Failed to parse response: not valid JSON and body is not a recognizable worldId") from None

    @staticmethod
    def _world_id_from_create_payload(payload: Any) -> Optional[str]:
        """Extract worldId from create success response (WorldAsyncOperation JSON or legacy bare text)."""
        if isinstance(payload, str):
            s = payload.strip()
            return s if s else None
        if isinstance(payload, dict):
            for k in ("worldId", "data", "id"):
                v = payload.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
        return None

    def _check_open_api_response(self, resp: requests.Response, payload: Any) -> Optional[Dict[str, Any]]:
        if resp.status_code < 400 and not self._is_open_api_error(payload):
            return None
        if not isinstance(payload, dict):
            payload = {"message": resp.text or f"HTTP {resp.status_code}"}
        msg = self._open_api_error_message(payload)
        biz_code = self._open_api_biz_code(payload)
        hint = _auth_hint(msg, biz_code or str(payload.get("code")))
        return {
            "success": False,
            "error": msg + (f"\nSuggestion: {hint}" if hint else ""),
            "code": payload.get("code", resp.status_code),
        }

    def __init__(self, api_key: str):
        self.api_key = api_key
        skip_verify = str(os.environ.get("AHOLO_INSECURE_SKIP_VERIFY", "")).strip().lower()
        force_verify = str(os.environ.get("AHOLO_FORCE_SSL_VERIFY", "")).strip().lower()
        if force_verify in {"1", "true", "yes", "on"}:
            self.verify_ssl = True
        elif skip_verify in {"0", "false", "no", "off"}:
            self.verify_ssl = True
        else:
            # Skip TLS verification by default (corporate/self-signed certs).
            self.verify_ssl = False
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.ous_token: Optional[str] = None
        self.global_domain: Optional[str] = None
        self.block_size: int = 1024 * 1024
        # Create session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    @staticmethod
    def _ok(result: Dict[str, Any]) -> bool:
        """OUS V2 responses use c/m/d envelope."""
        return str(result.get("c")) == "0"

    @staticmethod
    def _api_error(result: Dict[str, Any], default: str = "Unknown error") -> str:
        """OUS V2 error message."""
        return str(result.get("m") or default)

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": self.api_key, "Content-Type": "application/json"}

    def _create_task_headers(self) -> Dict[str, str]:
        """Create reconstruction/generation: x-source=skills → platform OPEN_API_SKILL."""
        headers = self._auth_headers()
        headers[HEADER_X_SOURCE] = X_SOURCE_VALUE_SKILLS
        return headers

    def _ous_headers(self) -> Dict[str, str]:
        if not self.ous_token:
            return {}
        return {"ous-token-v2": self.ous_token}

    def get_upload_token(self) -> Dict[str, Any]:
        url = f"{self.TOKEN_BASE_URL}{PATH_UPLOAD_TOKEN}"
        with step_timer("fetch upload token"):
            try:
                resp = self.session.get(url, headers=self._auth_headers(), timeout=30, verify=self.verify_ssl)
                payload = self._parse_open_api_json(resp)
                err = self._check_open_api_response(resp, payload)
                if err:
                    return err

                data = payload if isinstance(payload, dict) else {}
                self.ous_token = data.get("ousToken")
                self.global_domain = data.get("globalDomain")
                self.block_size = int(data.get("blockSize") or self.block_size)
                if not self.ous_token or not self.global_domain:
                    return {"success": False, "error": "Upload token response missing ousToken or globalDomain."}

                return {
                    "success": True,
                    "ousToken": self.ous_token,
                    "globalDomain": self.global_domain,
                    "blockSize": self.block_size,
                }
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Request failed: {e}"}
            except (TypeError, ValueError) as e:
                return {"success": False, "error": str(e)}

    @staticmethod
    def _calculate_md5(file_path: str) -> str:
        h = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _poll_upload_until_ready(
        self, timeout_seconds: int = 120, interval_seconds: float = 0.5
    ) -> Dict[str, Any]:
        if not self.global_domain or not self.ous_token:
            return {"success": False, "error": "Missing upload credentials; cannot poll upload status."}

        url = f"{self.global_domain}/ous/api/v2/upload/status"
        deadline = time.time() + timeout_seconds

        while time.time() < deadline:
            try:
                resp = self.session.get(url, headers=self._ous_headers(), timeout=30, verify=self.verify_ssl)
                resp.raise_for_status()
                result = resp.json()
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Failed to query upload status: {e}"}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"Failed to parse upload status JSON: {e}"}

            if not self._ok(result):
                return {"success": False, "error": f"Failed to query upload status: {self._api_error(result)}"}

            data = result.get("d") or {}
            status = data.get("status")
            if status == 5:
                return {"success": True, "url": data.get("url"), "uploadStatus": status}
            if status in (6, 8):
                return {
                    "success": False,
                    "error": f"Upload failed, status={status} errorCode={data.get('errorCode')} errorMsg={data.get('errorMsg')}",
                }
            time.sleep(max(0.2, interval_seconds))

        return {"success": False, "error": f"Upload status poll timed out ({timeout_seconds}s)"}

    def _upload_file_single(self, file_path: str) -> Dict[str, Any]:
        if not self.global_domain:
            return {"success": False, "error": "Missing globalDomain."}

        path = Path(file_path)
        md5_value = self._calculate_md5(file_path)
        mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        url = f"{self.global_domain}/ous/api/v2/single/upload"

        with step_timer(f"single-file upload: {path.name}"):
            try:
                with open(file_path, "rb") as f:
                    resp = self.session.post(
                        url,
                        headers=self._ous_headers(),
                        data={"md5": md5_value},
                        files={"file": (path.name, f, mime_type)},
                        timeout=600,
                        verify=self.verify_ssl,
                    )
                resp.raise_for_status()
                result = resp.json()
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Single-file upload failed: {e}", "originalPath": file_path}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"Failed to parse upload response JSON: {e}", "originalPath": file_path}

        if not self._ok(result):
            msg = self._api_error(result)
            hint = _format_hint(msg) or _auth_hint(msg, result.get("c"))
            return {
                "success": False,
                "error": f"Single-file upload failed: {msg}" + (f"\nSuggestion: {hint}" if hint else ""),
                "originalPath": file_path,
            }

        poll_result = self._poll_upload_until_ready()
        poll_result["originalPath"] = file_path
        return poll_result

    def _upload_file_block(self, file_path: str) -> Dict[str, Any]:
        if not self.global_domain:
            return {"success": False, "error": "Missing globalDomain."}

        path = Path(file_path)
        file_size = path.stat().st_size
        md5_value = self._calculate_md5(file_path)
        block_size = max(1, self.block_size)
        total_blocks = (file_size + block_size - 1) // block_size
        init_url = f"{self.global_domain}/ous/api/v2/block/upload/init"

        with step_timer(f"multipart upload: {path.name}"):
            try:
                init_resp = self.session.post(
                    init_url,
                    headers=self._ous_headers(),
                    json={"md5": md5_value, "blocks": total_blocks, "size": file_size, "name": path.name},
                    timeout=30,
                    verify=self.verify_ssl,
                )
                init_resp.raise_for_status()
                init_result = init_resp.json()
                if not self._ok(init_result) and "md5" in str(self._api_error(init_result)).lower():
                    # Beta compatibility: some gateways expect multipart init params in query string.
                    init_resp = self.session.post(
                        init_url,
                        headers=self._ous_headers(),
                        params={"md5": md5_value, "blocks": total_blocks, "size": file_size, "name": path.name},
                        timeout=30,
                        verify=self.verify_ssl,
                    )
                    init_resp.raise_for_status()
                    init_result = init_resp.json()
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Multipart init failed: {e}", "originalPath": file_path}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"Failed to parse multipart init response: {e}", "originalPath": file_path}

        if not self._ok(init_result):
            msg = self._api_error(init_result)
            hint = _format_hint(msg) or _auth_hint(msg, init_result.get("c"))
            return {
                "success": False,
                "error": f"Multipart init failed: {msg}" + (f"\nSuggestion: {hint}" if hint else ""),
                "originalPath": file_path,
            }

        init_data = init_result.get("d") or {}
        deduplicated = bool(init_data.get("deduplicated"))
        if not deduplicated:
            part_url = f"{self.global_domain}/ous/api/v2/block/upload/part"
            mime_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
            try:
                with open(file_path, "rb") as f:
                    for block in range(1, total_blocks + 1):
                        chunk = f.read(block_size)
                        if not chunk:
                            break
                        resp = self.session.post(
                            part_url,
                            headers=self._ous_headers(),
                            data={"block": block},
                            files={"file": (f"{path.name}.part{block}", chunk, mime_type)},
                            timeout=600,
                            verify=self.verify_ssl,
                        )
                        resp.raise_for_status()
                        result = resp.json()
                        if not self._ok(result):
                            return {
                                "success": False,
                                "error": f"Multipart upload failed (block={block}): {self._api_error(result)}",
                                "originalPath": file_path,
                            }
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Multipart upload failed: {e}", "originalPath": file_path}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"Failed to parse multipart upload response: {e}", "originalPath": file_path}

        poll_result = self._poll_upload_until_ready()
        poll_result["originalPath"] = file_path
        return poll_result

    def upload_file(self, file_path: str) -> Dict[str, Any]:
        p = Path(file_path)
        if not p.exists():
            return {"success": False, "error": f"File not found: {file_path}"}

        # Single-file upload: fetch a fresh token before each upload (tokens are one-time)
        if p.stat().st_size <= self.block_size:
            token_result = self.get_upload_token()
            if not token_result.get("success"):
                return token_result
            return self._upload_file_single(file_path)

        # Multipart upload: multiple steps share one token
        if not self.ous_token or not self.global_domain:
            token_result = self.get_upload_token()
            if not token_result.get("success"):
                return token_result
        return self._upload_file_block(file_path)

    def upload_paths(self, paths: List[str], input_label: str = "asset") -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        local_paths = [x for x in paths if not _is_url(x)]
        if local_paths:
            token_result = self.get_upload_token()
            if not token_result.get("success"):
                return [{"success": False, "error": token_result.get("error"), "originalPath": p} for p in paths]

        for item in paths:
            if _is_url(item):
                print(f"Using existing URL (skip upload): {item}")
                results.append({"success": True, "url": item, "originalPath": item, "isUrl": True})
            else:
                print(f"Uploading {input_label}: {item}")
                up = self.upload_file(item)
                if up.get("success"):
                    print(f"{input_label} upload succeeded: {item}")
                else:
                    print(f"{input_label} upload failed: {item} - {up.get('error')}")
                results.append(up)
        return results

    def create_reconstruction(
        self,
        project_name: Optional[str],
        scene: str,
        resources: List[Dict[str, Any]],
        task_quality: str = "high",
        cover: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{PATH_RECONSTRUCTIONS}"
        body: Dict[str, Any] = {
            "scene": scene,
            "taskQuality": task_quality,
            "resources": resources,
        }
        if project_name:
            body["name"] = project_name
        if cover:
            body["cover"] = cover
        with step_timer("create reconstruction task"):
            try:
                resp = self.session.post(
                    url, headers=self._create_task_headers(), json=body, timeout=60, verify=self.verify_ssl
                )
                payload = self._parse_open_api_json(resp)
                err = self._check_open_api_response(resp, payload)
                if err:
                    return err
                world_id = self._world_id_from_create_payload(payload)
                if not world_id:
                    return {"success": False, "error": "Create succeeded but no worldId was returned."}
                return {"success": True, "worldId": world_id}
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Request failed: {e}"}
            except ValueError as e:
                return {"success": False, "error": str(e)}

    def create_generation(
        self,
        project_name: Optional[str],
        prompt: Optional[str],
        resources: List[Dict[str, Any]],
        cover: Optional[str] = None,
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{PATH_GENERATIONS}"
        body: Dict[str, Any] = {}
        if project_name:
            body["name"] = project_name
        if prompt:
            body["prompt"] = prompt
        if resources:
            body["resources"] = resources
        if cover:
            body["cover"] = cover
        with step_timer("create generation task"):
            try:
                resp = self.session.post(
                    url, headers=self._create_task_headers(), json=body, timeout=60, verify=self.verify_ssl
                )
                payload = self._parse_open_api_json(resp)
                err = self._check_open_api_response(resp, payload)
                if err:
                    return err
                world_id = self._world_id_from_create_payload(payload)
                if not world_id:
                    return {"success": False, "error": "Create succeeded but no worldId was returned."}
                return {"success": True, "worldId": world_id}
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Request failed: {e}"}
            except ValueError as e:
                return {"success": False, "error": str(e)}

    def get_project_info(self, world_id: str) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{PATH_WORLD_DETAIL.format(worldId=world_id)}"
        with step_timer(f"query task status: {world_id}"):
            try:
                resp = self.session.get(url, headers=self._auth_headers(), timeout=30, verify=self.verify_ssl)
                payload = self._parse_open_api_json(resp)
                err = self._check_open_api_response(resp, payload)
                if err:
                    err["isTerminal"] = True
                    return err
                data = payload if isinstance(payload, dict) else {}
                status = data.get("status")
                is_terminal = status in WORLD_TERMINAL_STATUS
                is_success = status == "SUCCEEDED"
                urls = (((data.get("assets") or {}).get("splats") or {}).get("urls") or {})
                return {
                    "success": True,
                    "worldId": data.get("worldId") or world_id,
                    "task": {
                        "status": status,
                        "statusDesc": WORLD_STATUS_DESC.get(status, status or "Unknown"),
                        "isTerminal": is_terminal,
                        "isSuccess": is_success,
                    },
                    "result": {
                        "plyPath": urls.get("plyPath"),
                        "spzPath": urls.get("spzPath"),
                        "sogPath": urls.get("sogPath"),
                    },
                    "isTerminal": is_terminal,
                }
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": f"Request failed: {e}", "isTerminal": False}
            except json.JSONDecodeError as e:
                return {"success": False, "error": f"JSON parse error: {e}", "isTerminal": False}

    def poll_project_until_terminal(self, world_id: str, interval_seconds: int = 60, timeout_seconds: int = 14400) -> Dict[str, Any]:
        start = time.time()
        attempts = 0
        history: List[Dict[str, Any]] = []

        while True:
            attempts += 1
            result = self.get_project_info(world_id)
            now = int(time.time())

            if result.get("success"):
                task = result.get("task") or {}
                history.append({"ts": now, "status": task.get("status")})
                print(f"[poll #{attempts}] status={task.get('status')} ({task.get('statusDesc')})")
                if task.get("isTerminal"):
                    result["pollMeta"] = {
                        "attempts": attempts,
                        "elapsedSeconds": int(time.time() - start),
                        "intervalSeconds": interval_seconds,
                        "recentHistory": history[-5:],
                    }
                    return result
            else:
                history.append({"ts": now, "error": result.get("error")})
                print(f"[poll #{attempts}] query failed: {result.get('error')}")

            elapsed = int(time.time() - start)
            if elapsed >= timeout_seconds:
                return {
                    "success": False,
                    "worldId": world_id,
                    "error": f"Poll timed out ({timeout_seconds}s). Retry later with status/poll.",
                    "isTerminal": True,
                    "pollMeta": {
                        "attempts": attempts,
                        "elapsedSeconds": elapsed,
                        "intervalSeconds": interval_seconds,
                        "recentHistory": history[-5:],
                    },
                }
            time.sleep(max(1, interval_seconds))


def format_create_result(
    result: Dict[str, Any],
    skill_script_path: Optional[str] = None,
) -> str:
    if not result.get("success"):
        return "## Task creation failed\n\n" + f"**Error:** {result.get('error', 'Unknown error')}"
    world_id = result.get("worldId")
    cfg = SITE_CONFIG
    script_path = skill_script_path or cfg["skill_script_path"]
    viewer_url = cfg["viewer_url_template"].format(world_id=world_id)
    lines = [
        "## Task created successfully",
        "",
        f"**World ID (worldId):** `{world_id}`",
        f"**Viewer URL:** {viewer_url}",
        "",
        "Next, run `poll`:",
        "```bash",
        f"python3 {script_path} '{{\"action\":\"poll\",\"worldId\":\"{world_id}\",\"intervalSeconds\":60,\"timeoutSeconds\":14400}}'",
        "```",
    ]
    return "\n".join(lines)


def format_status_result(result: Dict[str, Any], world_id: str) -> str:
    if not result.get("success"):
        return "\n".join(
            ["## Status query failed", "", f"**World ID:** `{world_id}`", f"**Error:** {result.get('error', 'Unknown error')}"]
        )

    task = result.get("task") or {}
    status = task.get("status")
    is_terminal = task.get("isTerminal")
    is_success = task.get("isSuccess")
    title = "## Task completed — success" if is_terminal and is_success else f"## Task status: {task.get('statusDesc')}"
    lines = [
        title,
        "",
        f"**World ID:** `{result.get('worldId')}`",
        f"**Status:** `{status}`",
        f"**Terminal:** {is_terminal}",
    ]

    if is_terminal and is_success:
        data = result.get("result") or {}
        lines.extend(
            [
                "",
                "### Result files",
                "",
                f"- **PLY:** {data.get('plyPath') or 'none'}",
                f"- **SPZ:** {data.get('spzPath') or 'none'}",
                f"- **SOG:** {data.get('sogPath') or 'none'}",
            ]
        )

    if is_terminal:
        lines.extend(["", "*Task finished; polling stopped.*"])
    return "\n".join(lines)


def format_poll_result(result: Dict[str, Any], world_id: str) -> str:
    lines = ["## Poll result", ""]
    meta = result.get("pollMeta") or {}
    lines.extend(
        [
            f"**World ID:** `{world_id}`",
            f"**Poll attempts:** {meta.get('attempts', 0)}",
            f"**Elapsed (s):** {meta.get('elapsedSeconds', 0)}",
            f"**Interval (s):** {meta.get('intervalSeconds', 0)}",
            "",
        ]
    )
    if result.get("success"):
        lines.append(format_status_result(result, world_id))
    else:
        lines.extend(["## Poll failed", "", f"**Error:** {result.get('error', 'Unknown error')}"])
    return "\n".join(lines)


def parse_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return default


def main() -> None:
    if len(sys.argv) < 2:
        print("## Usage")
        print("")
        print("Actions: create | create-reconstruction | create-generation | status | poll")
        print("Environment variable: `AHOLO_API_KEY`")
        print("")
        print("Reconstruction parameters:")
        print("  - `videoPaths`: video files (1-3)")
        print("  - `imagePaths`: image files (at least 20)")
        print("  - `imageDir`: image directory (scans all images; use imagePaths OR imageDir)")
        print("  - `scene`: `model` or `space`")
        print("  - `taskQuality`: `low` | `normal` | `high`")
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print("## JSON parse error\n")
        print(f"**Details:** {e}")
        sys.exit(1)

    api_key = os.environ.get("AHOLO_API_KEY", "").strip()
    if not api_key:
        print("## Missing environment variable\n")
        print("Set `AHOLO_API_KEY` (Aholo Open Platform API Key) in your environment.")
        print(f"If you do not have an API Key yet, create one at {SITE_CONFIG['api_keys_url']}")
        print("")
        print("After configuring, **reply \"continue\" in Cursor** or restate your 3D task; the agent will run the script.")
        print("Without API Key, **do not repeatedly run this script**, especially create actions.")
        sys.exit(1)

    client = AholoClient(api_key=api_key)
    action = params.get("action", "create")
    forbid_create = parse_bool(params.get("forbidCreate"), False)
    create_actions = {"create", "create-reconstruction", "create-generation"}
    if forbid_create and action in create_actions:
        print("## Blocked: create not allowed\n")
        print("Request has `forbidCreate=true`; use `status` or `poll` instead.")
        sys.exit(1)

    if action in create_actions:
        workflow = params.get("workflow", "reconstruction")
        if action == "create-reconstruction":
            workflow = "reconstruction"
        elif action == "create-generation":
            workflow = "generation"
        workflow = str(workflow).strip().lower()
        if workflow not in {"reconstruction", "generation"}:
            print("## Invalid workflow\n")
            print("`workflow` must be `reconstruction` or `generation`.")
            sys.exit(1)

        project_name_raw = params.get("projectName")
        if project_name_raw is None:
            project_name: Optional[str] = None
        else:
            project_name = str(project_name_raw).strip() or None

        print("## Create Aholo 3DGS task\n")
        if project_name:
            print(f"Project name: {project_name}")
        else:
            print("Project name: (not set; server default)")

        cover_url = params.get("cover")
        cover_path = params.get("coverPath")
        if cover_path:
            print("### Step 1: Upload cover (optional)")
            cover_up = client.upload_file(cover_path)
            if not cover_up.get("success"):
                print("\n## Cover upload failed")
                print(f"**Error:** {cover_up.get('error')}")
                sys.exit(1)
            cover_url = cover_up.get("url")

        if workflow == "reconstruction":
            scene = params.get("scene")
            task_quality = params.get("taskQuality")
            if not scene or scene not in {"model", "space"}:
                print("## Missing or invalid parameter: scene\n")
                print("`scene` must be `model` (object) or `space` (environment).")
                sys.exit(1)
            if not task_quality or task_quality not in {"low", "normal", "high"}:
                print("## Missing or invalid parameter: taskQuality\n")
                print("`taskQuality` must be `low`, `normal`, or `high`.")
                sys.exit(1)

            video_paths = params.get("videoPaths") or []
            image_paths = params.get("imagePaths") or []
            image_dir = params.get("imageDir")

            # imageDir: scan directory for images
            if image_dir:
                if image_paths:
                    print("## Parameter conflict\n")
                    print("Use either `imageDir` (directory) or `imagePaths` (file list), not both.")
                    sys.exit(1)
                if not os.path.isdir(image_dir):
                    print("## Directory not found\n")
                    print(f"`imageDir` does not exist: `{image_dir}`")
                    sys.exit(1)
                valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.gif')
                image_paths = [
                    os.path.join(image_dir, f)
                    for f in os.listdir(image_dir)
                    if f.lower().endswith(valid_ext)
                ]
                image_paths.sort()
                print(f"### Scanned {len(image_paths)} images from directory")

            if video_paths and image_paths:
                print("## Parameter conflict\n")
                print("Reconstruction requires either `videoPaths` OR `imagePaths`/`imageDir`.")
                sys.exit(1)
            if not video_paths and not image_paths:
                print("## Missing input\n")
                print("Reconstruction requires `videoPaths`, `imagePaths`, or `imageDir`.")
                sys.exit(1)
            if video_paths and (len(video_paths) < 1 or len(video_paths) > 3):
                print("## Invalid video count\n")
                print("`videoPaths` must contain 1-3 items.")
                sys.exit(1)
            if image_paths and len(image_paths) < 20:
                print("## Not enough images\n")
                print(f"`imagePaths` needs at least 20 images; found {len(image_paths)}.")
                sys.exit(1)

            resources: List[Dict[str, Any]] = []
            if video_paths:
                print("### Step 1: Upload videos")
                uploads = client.upload_paths(video_paths, "video")
                successful = [x for x in uploads if x.get("success")]
                if not successful:
                    print("\n## Upload failed")
                    for r in uploads:
                        print(f"- `{r.get('originalPath')}`: {r.get('error')}")
                    sys.exit(1)
                resources.extend([{"url": x.get("url"), "type": "video"} for x in successful])
            if image_paths:
                print("### Step 1: Upload images")
                uploads = client.upload_paths(image_paths, "image")
                successful = [x for x in uploads if x.get("success")]
                if not successful:
                    print("\n## Upload failed")
                    for r in uploads:
                        print(f"- `{r.get('originalPath')}`: {r.get('error')}")
                    sys.exit(1)
                resources.extend([{"url": x.get("url"), "type": "image"} for x in successful])

            print("\n### Step 2: Create reconstruction")
            create_result = client.create_reconstruction(
                project_name=project_name,
                scene=scene,
                resources=resources,
                task_quality=task_quality,
                cover=cover_url,
            )
        else:
            image_paths = params.get("imagePaths") or []
            prompt = params.get("prompt")
            if len(image_paths) > 1:
                print("## Invalid image count\n")
                print("Generation (spatial gen) allows at most 1 image in `imagePaths`.")
                sys.exit(1)
            if not image_paths and not prompt:
                print("## Missing input\n")
                print("Generation requires at least one of `imagePaths` or `prompt`.")
                sys.exit(1)
            if params.get("videoPaths"):
                print("## Invalid parameter\n")
                print("Generation does not support `videoPaths`; use `imagePaths`.")
                sys.exit(1)

            resources: List[Dict[str, Any]] = []
            if image_paths:
                print("### Step 1: Upload image")
                uploads = client.upload_paths(image_paths, "image")
                successful = [x for x in uploads if x.get("success")]
                if not successful:
                    print("\n## Upload failed")
                    for r in uploads:
                        print(f"- `{r.get('originalPath')}`: {r.get('error')}")
                    sys.exit(1)
                resources.extend([{"url": x.get("url"), "type": "image"} for x in successful])

            print("\n### Step 2: Create generation (spatial gen)")
            create_result = client.create_generation(
                project_name=project_name,
                prompt=prompt,
                resources=resources,
                cover=cover_url,
            )

        if not create_result.get("success"):
            print("\n## Task creation failed")
            print(f"**Error:** {create_result.get('error')}")
            sys.exit(1)
        print("\n" + format_create_result(create_result))
        return

    if action == "status":
        world_id = params.get("worldId")
        if not world_id:
            print("## Missing required parameter\n")
            print("- **worldId**: world task ID")
            sys.exit(1)
        result = client.get_project_info(world_id)
        print(format_status_result(result, world_id))
        return

    if action == "poll":
        world_id = params.get("worldId")
        if not world_id:
            print("## Missing required parameter\n")
            print("- **worldId**: world task ID")
            sys.exit(1)
        interval_seconds = int(params.get("intervalSeconds", 60))
        timeout_seconds = int(params.get("timeoutSeconds", 14400))
        if interval_seconds <= 0:
            interval_seconds = 60
        if timeout_seconds <= 0:
            timeout_seconds = 14400
        result = client.poll_project_until_terminal(
            world_id=world_id,
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
        )
        print(format_poll_result(result, world_id))
        return

    print("## Invalid action\n")
    print(
        f"**action** must be `create`, `create-reconstruction`, `create-generation`, `status`, or `poll`; got: `{action}`"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
