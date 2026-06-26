"""High-level client for BeautyPlus AI SDK."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from urllib.parse import urlencode

import requests

from sdk.core import api
from sdk.auth.signer import Signer, HeaderHost
from sdk.core.config import (
    WAPI_ENDPOINT,
    USER_AGENT,
    VERSION,
    url_download_max_bytes,
    url_download_connect_timeout,
    url_download_read_timeout,
)


def _wapi_meta_code_value(meta_code: Any) -> int:
    """Normalize meta.code for comparisons (int)."""
    if meta_code is None:
        return 0
    if meta_code == 0 or meta_code == "0":
        return 0
    try:
        return int(meta_code)
    except (TypeError, ValueError):
        return -1


class WapiApiError(RuntimeError):
    """HTTP 200 but WAPI meta.code != 0.

    Full server payload is in ``raw``; ``str(exception)`` is intentionally short
    so errors copied to logs or JSON stdout do not leak response bodies.
    """

    def __init__(self, code: int, msg: str, raw: Dict, *, original_code=None):
        self.code = code
        self.original_code = original_code if original_code is not None else code
        self.msg = msg or "Request failed"
        self.raw = raw if isinstance(raw, dict) else {}
        super().__init__(f"[{self.original_code}] {self.msg}")


class ConsumeDeniedError(WapiApiError):
    """Non-zero meta from POST /skill/consume.json (quota / permission)."""


class WapiClient:
    """Signed HTTP client for the skill WAPI gateway."""

    def __init__(self, ak: str, sk: str, endpoint: str = WAPI_ENDPOINT):
        self.ak = ak
        self.sk = sk
        self.endpoint = endpoint

    def request(self, path: str, method: str = "GET", body: Optional[Dict] = None) -> Dict:
        """Send a signed request to WAPI."""
        base = self.endpoint
        if not base.startswith(("http://", "https://")):
            base = f"https://{base}"
        uri = f"{base}{path}"
        signer = Signer(self.ak, self.sk)
        headers = {"User-Agent": USER_AGENT}
        body_str = json.dumps(body) if body else ""
        if body:
            headers["Content-Type"] = "application/json"

        signed_request = signer.sign(uri, method, headers, body_str)
        resp = requests.Session().send(signed_request, timeout=10)

        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code} from WAPI {path}")

        data = resp.json()
        meta = data.get("meta") or {}
        if _wapi_meta_code_value(meta.get("code", 0)) != 0:
            msg = meta.get("msg", "Request failed")
            raise WapiApiError(
                _wapi_meta_code_value(meta.get("code", 0)), msg, data, original_code=meta.get("code")
            )

        return data.get("response", {})


class SkillClient:
    """
    High-level client: remote config, quota consume, upload, and task run.

    Example::
        client = SkillClient()
        client.fetch_config()
        result = client.run_task("sod", "/path/to/image.jpg")
    """

    def __init__(
        self,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        region: str = "cn-north-4",
        oss_region: Optional[str] = None,
        auto_fetch_config: bool = True,
    ):
        """
        :param ak: Access Key (default: env ``BP_AK``)
        :param sk: Secret Key (default: env ``BP_SK``)
        :param region: API region, default cn-north-4
        :param oss_region: Optional OSS region override
        :param auto_fetch_config: If True, fetch remote config on init
        """
        self.ak = ak or os.environ.get("BP_AK")
        self.sk = sk or os.environ.get("BP_SK")

        if not self.ak or not self.sk:
            raise ValueError("AK and SK are required via arguments or BP_AK / BP_SK")

        self.wapi = WapiClient(self.ak, self.sk)
        self.api = api.AiApi(self.ak, self.sk, region, oss_region)

        if auto_fetch_config:
            self.fetch_config()

        self._pipeline_trace: list = []

    def fetch_config(self, gid=None, version=None):
        """
        Fetch skill config from wapi and refresh local SDK settings.

        :param gid: Optional group id (uses cached gid if omitted)
        :param version: Client version string (default from config.VERSION)
        """
        if version is None:
            version = VERSION

        if not gid:
            cached_gid = self._get_cached_gid()
            if cached_gid:
                gid = cached_gid

        try:
            response = self.wapi.request(
                "/skill/config.json",
                method="POST",
                body={"gid": gid or "", "version": version or ""}
            )
        except RuntimeError as e:
            raise RuntimeError(
                "Failed to fetch skill config (check network, AK/SK, and server). "
                "Detail: " + str(e)
            ) from e

        if response.get("gid"):
            self._cache_gid(response["gid"])

        if response.get("need_update"):
            message = response.get("update_message", "A newer version is available; please update.")
            print(f"[config update] {message}")

        self._update_config_from_response(response)
        return response

    def _get_cached_gid(self):
        """Load gid from local disk cache."""
        cache_file = os.path.expanduser("~/.cache/beautyplus/gid.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("gid")
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def _cache_gid(self, gid):
        """Persist gid to local disk cache."""
        cache_file = os.path.expanduser("~/.cache/beautyplus/gid.json")
        try:
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"gid": gid}, f, ensure_ascii=False, indent=2)
        except IOError:
            pass

    def _update_config_from_response(self, response):
        """Apply algorithm block from config response (regions and token policy only)."""

        if "algorithm" not in response:
            return

        algo = response["algorithm"]
        token_cfg_changed = False

        if "regions" in algo:
            self.api._config["regions"].update(algo["regions"])
            if self.api.region in algo["regions"]:
                self.api.EndPoint = algo["regions"][self.api.region]

        if "token_policy_type" in algo:
            token_cfg_changed = token_cfg_changed or (
                self.api._config.get("token_policy_type") != algo["token_policy_type"]
            )
            self.api._config["token_policy_type"] = algo["token_policy_type"]

        if "token_policy_types" in algo:
            token_cfg_changed = token_cfg_changed or (
                self.api._config.get("token_policy_types") != algo["token_policy_types"]
            )
            self.api._config["token_policy_types"] = algo["token_policy_types"]

        if "token_policy_app" in algo:
            token_cfg_changed = token_cfg_changed or (
                self.api._config.get("token_policy_app") != algo["token_policy_app"]
            )
            self.api._config["token_policy_app"] = algo["token_policy_app"]
        else:
            token_cfg_changed = token_cfg_changed or (
                self.api._config.get("token_policy_app") is not None
            )
            self.api._config["token_policy_app"] = None

        if token_cfg_changed:
            # Ensure next request re-fetches strategies with latest token policy settings.
            self.api.aiStrategy = None
            self.api.storageStrategy = None
            self.api.strategyLoadTime = 0

    def _consume_permission(self, url, task):
        """Call quota/consume API before running a task."""
        gid = self._get_cached_gid()

        try:
            return self.wapi.request(
                "/skill/consume.json",
                method="POST",
                body={"url": url, "task": task, "gid": gid or ""}
            )
        except WapiApiError as e:
            raise ConsumeDeniedError(
                e.code, e.msg, e.raw, original_code=e.original_code
            ) from e

    @staticmethod
    def _preview_media_ref(url) -> str:
        if url is None:
            return ""
        if isinstance(url, str):
            return api.safe_url_preview(url)
        if isinstance(url, dict):
            u = url.get("url") or url.get("uri")
            if u:
                return api.safe_url_preview(str(u))
        try:
            return api.safe_url_preview(json.dumps(url, ensure_ascii=False), max_len=80)
        except (TypeError, ValueError):
            return "<non-serializable>"

    def _fetch_http_input_to_tempfile(self, url: str) -> Tuple[str, int]:
        """Stream-download URL to a temp file (bounded size). Caller must unlink path."""
        preview = api.safe_url_preview(url)
        conn_t = url_download_connect_timeout()
        read_t = url_download_read_timeout()
        max_b = url_download_max_bytes()
        headers = {"User-Agent": USER_AGENT}

        try:
            with requests.get(
                url,
                stream=True,
                timeout=(conn_t, read_t),
                headers=headers,
            ) as resp:
                try:
                    resp.raise_for_status()
                except requests.HTTPError as e:
                    code = getattr(resp, "status_code", "?")
                    raise RuntimeError(
                        f"Input URL HTTP {code} (url={preview}). "
                        "Signed URLs may be expired; shell may have broken the URL at '&' without quotes."
                    ) from e

                fd, path = tempfile.mkstemp(prefix="openclaw_in_", suffix=".bin")
                total = 0
                try:
                    with os.fdopen(fd, "wb") as out:
                        for chunk in resp.iter_content(chunk_size=65536):
                            if not chunk:
                                continue
                            total += len(chunk)
                            if total > max_b:
                                raise RuntimeError(
                                    f"Input URL download exceeds max bytes ({max_b}); url={preview}. "
                                    "Set MT_AI_URL_MAX_BYTES to raise the cap or use a smaller file."
                                )
                            out.write(chunk)
                except Exception:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
                    raise

                if total == 0:
                    try:
                        os.unlink(path)
                    except OSError:
                        pass
                    raise RuntimeError(f"Input URL returned empty body (url={preview}).")

                return path, total
        except requests.Timeout as e:
            raise RuntimeError(
                f"Input URL download timed out (url={preview}). "
                f"Try MT_AI_URL_READ_TIMEOUT (read={read_t}s, connect={conn_t}s) or "
                f"`beautyplus_ai.py resolve-input --url ...` then pass local --input. Detail: {e}"
            ) from e
        except requests.RequestException as e:
            raise RuntimeError(f"Input URL download failed (url={preview}): {e}") from e

    def run_task(
        self,
        task_name: str,
        image_path: str,
        params: Optional[Dict] = None,
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> Dict:
        """
        Upload media (or use remote URL) and run the named algorithm task.

        :param task_name: Task effect key (sent to /skill/consume.json; server returns invoke_spec)
        :param image_path: Local path or http(s) URL
        :param params: Optional invoke params merged over preset defaults
        :param on_async_submitted: Optional ``callable(task_id: str)`` invoked once
            after the server accepts an async job (status 9) and before status polling.
        """
        self._pipeline_trace = []

        if isinstance(image_path, str) and image_path.startswith(("http://", "https://")):
            preview = api.safe_url_preview(image_path)
            api._progress_log(f"input: download from URL (GET {preview})")
            tmp_path, n = self._fetch_http_input_to_tempfile(image_path)
            try:
                api._progress_log(f"input: download done ({n} bytes) → OSS upload (PutObject)")
                self._pipeline_trace.append(
                    {"step": "download_input", "from_url": preview, "bytes": n}
                )
                url = self.api.getFileUrl(tmp_path, upload_source=image_path)
                self._pipeline_trace.append(
                    {"step": "upload_input", "via": "oss_put_object", "bytes": n}
                )
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
        else:
            ip = image_path
            sz = None
            if isinstance(ip, str) and os.path.isfile(ip):
                sz = os.path.getsize(ip)
                api._progress_log(
                    f"input: local file → OSS upload ({os.path.basename(ip)}, {sz} bytes)"
                )
            else:
                api._progress_log("input: local path → OSS upload (PutObject)")
            url = self.api.getFileUrl(image_path, upload_source=image_path)
            self._pipeline_trace.append(
                {
                    "step": "upload_input",
                    "via": "oss_put_object",
                    "path": os.path.basename(ip) if isinstance(ip, str) else str(ip),
                    "bytes": sz,
                }
            )

        if url is None:
            raise RuntimeError("Upload failed")

        ref = self._preview_media_ref(url)
        self._pipeline_trace.append({"step": "media_url_ready", "input_media": ref})
        api._progress_log(f"quota: POST /skill/consume.json task={task_name!r}")
        consume_info = self._consume_permission(url, task_name)
        context = consume_info.get("context", "") if consume_info else ""
        api._progress_log("quota: consume OK → submit algorithm job")

        self._pipeline_trace.append({"step": "consume_quota", "task": task_name})
        self._pipeline_trace.append(
            {"step": "submit_algorithm", "invoke_preset": task_name}
        )

        invoke_spec = consume_info.get("invoke_spec") if isinstance(consume_info, dict) else None
        if not invoke_spec:
            raise RuntimeError(
                f"consume.json did not return invoke_spec for task {task_name!r}. "
                "Check server configuration."
            )
        return self.api.invoke_task_with_spec(
            invoke_spec, url, params, context, on_async_submitted=on_async_submitted
        )

    def poll_task_status(self, task_id: str) -> Dict:
        """
        Resume status polling for an existing async task.

        :param task_id: Full task id string from ``data.result.id`` or failure payload
        :return: Same shapes as ``run_task`` (success dict with ``output_urls``, or
            failure dicts with ``skill_status`` / ``error``).
        """
        tid = (task_id or "").strip()
        if not tid:
            raise ValueError("task_id is required")
        self._pipeline_trace = [
            {
                "step": "resume_poll",
                "description": "No input download, OSS upload, or consume; algorithm status GET only",
                "task_id": tid,
            }
        ]
        api._progress_log(
            "query-task: resume polling only (no input download / OSS upload / consume)"
        )
        policy = self.api.getAiStrategy()
        if not policy:
            raise RuntimeError(
                "Failed to load AI token policy (check network, AK/SK, and fetch_config)."
            )
        return self.api.status(tid, policy)
