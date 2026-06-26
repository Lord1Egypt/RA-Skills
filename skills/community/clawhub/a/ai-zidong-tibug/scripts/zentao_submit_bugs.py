#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate ZenTao bugs from normalized bug entries and submit each one automatically.

Usage:
  python3 scripts/zentao_submit_bugs.py --input ./bugs.json --product-id 786
  python3 scripts/zentao_submit_bugs.py --input ./bugs.json --product-id 786 --module-map ./references/module-map.json

Security:
  - Do not hardcode credentials in this script.
  - Use env vars or CLI args for HTTP_USER / HTTP_PASS / ZENTAO_USER / ZENTAO_PASS.

Input formats:
  1) JSON array: [ {...}, {...} ]
  2) JSON object: {"bugs": [ {...}, {...} ]}
  3) JSONL: one JSON object per line

Expected bug fields (Chinese or English keys both supported):
  - 标题 / title
  - 指派人 / assignee / assignedTo
  - 步骤 / steps (list or string)
  - 期望 / expectation
  - 影响版本 / affectedVersion
  - 严重级别 / severity (S1~S4 or 1~4)
  - 优先级 / priority / pri (P1~P4 or 1~4)
  - 图片/附件 / attachments (list or string)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.auth import HTTPBasicAuth


# -------------------------
# Helpers
# -------------------------

def env_bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def pick(raw: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
    return default


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def parse_level(value: Any, prefix: str, default: int) -> int:
    if value is None or value == "":
        return default

    if isinstance(value, (int, float)):
        n = int(value)
        return n if 1 <= n <= 4 else default

    s = str(value).strip().upper()
    if s.startswith(prefix):
        s = s[len(prefix) :].strip()

    m = re.search(r"([1-4])", s)
    if not m:
        return default

    n = int(m.group(1))
    return n if 1 <= n <= 4 else default


def split_text_list(value: Any) -> List[str]:
    if value is None:
        return []

    if isinstance(value, list):
        result: List[str] = []
        for item in value:
            item_str = str(item).strip()
            if item_str:
                result.append(item_str)
        return result

    text = str(value).strip()
    if not text:
        return []

    # Split by common delimiters but keep URLs intact as much as possible.
    parts = re.split(r"[\n\r]+|[;；,，]", text)
    return [p.strip() for p in parts if p.strip()]


def normalize_steps(value: Any) -> List[str]:
    steps = split_text_list(value)

    normalized: List[str] = []
    for step in steps:
        # strip leading numbering like "1.", "1、"
        step = re.sub(r"^\s*\d+\s*[\.、]\s*", "", step).strip()
        if step:
            normalized.append(step)

    if not normalized:
        normalized = [
            "进入目标页面。",
            "执行触发操作。",
            "观察页面行为。",
            "实际结果待补充。",
        ]

    return normalized


def normalize_attachments(value: Any) -> List[str]:
    items = split_text_list(value)
    result: List[str] = []
    for item in items:
        if "待补充" in item:
            continue
        result.append(item)
    return result


def build_steps_html(
    steps: List[str], expectation: str, affected_version: str, attachment_links: List[Tuple[str, str]]
) -> str:
    parts: List[str] = []

    for idx, step in enumerate(steps, 1):
        parts.append(f"<p>{idx}. {escape(step)}</p>")

    parts.append("<p>&nbsp;</p>")
    parts.append(f"<p><strong>期望：</strong> {escape(expectation)}</p>")

    if affected_version:
        parts.append(f"<p><strong>影响版本：</strong> {escape(affected_version)}</p>")

    if attachment_links:
        parts.append("<p><strong>图片/附件：</strong></p>")
        for label, url in attachment_links:
            parts.append(
                f"<p><a href=\"{escape(url, quote=True)}\" target=\"_blank\">{escape(label)}</a></p>"
            )

    return "".join(parts)


def extract_file_extension(path: str, fallback: str = "jpg") -> str:
    ext = Path(path).suffix.lower().lstrip(".")
    return ext if ext else fallback


def extract_module_segment_from_title(title: str) -> str:
    """Extract module/page segment from title like: [安卓]（社区-详情页）..."""
    if not title:
        return ""
    m = re.search(r"（([^）]+)）", title)
    return m.group(1).strip() if m else ""


def load_module_map(module_map_path: Optional[Path]) -> Dict[str, Any]:
    """Load module mapping JSON. Returns normalized shape.

    Example:
    {
      "defaultModuleId": 0,
      "rules": [
        {"contains": "社区-社区详情页", "moduleId": 123},
        {"match": "^短视频-", "moduleId": 456},
        {"keywords": ["直播", "收藏主播"], "moduleId": 789}
      ]
    }
    """
    normalized = {
        "defaultModuleId": 0,
        "rules": [],
        "source": str(module_map_path) if module_map_path else None,
    }

    if not module_map_path:
        return normalized

    if not module_map_path.exists() or not module_map_path.is_file():
        return normalized

    try:
        data = json.loads(module_map_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"模块映射文件解析失败: {module_map_path} | {exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"模块映射文件格式错误: {module_map_path}（应为 JSON 对象）")

    rules = data.get("rules", [])
    if rules is None:
        rules = []

    if not isinstance(rules, list):
        raise RuntimeError(f"模块映射文件格式错误: rules 必须是数组（{module_map_path}）")

    normalized["defaultModuleId"] = parse_int(data.get("defaultModuleId", 0), 0)

    clean_rules: List[Dict[str, Any]] = []
    for idx, rule in enumerate(rules, 1):
        if not isinstance(rule, dict):
            continue
        module_id = parse_int(rule.get("moduleId", 0), 0)
        if module_id <= 0:
            continue
        clean_rules.append(
            {
                "name": str(rule.get("name", f"rule-{idx}")).strip() or f"rule-{idx}",
                "moduleId": module_id,
                "equals": str(rule.get("equals", "")).strip(),
                "contains": str(rule.get("contains", "")).strip(),
                "match": str(rule.get("match", "")).strip(),
                "keywords": [str(x).strip() for x in rule.get("keywords", []) if str(x).strip()]
                if isinstance(rule.get("keywords"), list)
                else [],
            }
        )

    normalized["rules"] = clean_rules
    return normalized


def resolve_module_id(
    explicit_module_id: int,
    title: str,
    module_map: Dict[str, Any],
) -> Tuple[int, str, Optional[str]]:
    """Resolve module id with precedence: explicit > map rule > map default > 0."""
    if explicit_module_id > 0:
        return explicit_module_id, "input", None

    title = title or ""
    module_segment = extract_module_segment_from_title(title)
    candidates = [module_segment, title]

    rules: List[Dict[str, Any]] = module_map.get("rules", []) if isinstance(module_map, dict) else []
    for rule in rules:
        rule_name = str(rule.get("name") or "rule")
        module_id = parse_int(rule.get("moduleId", 0), 0)
        if module_id <= 0:
            continue

        equals = str(rule.get("equals", "")).strip()
        contains = str(rule.get("contains", "")).strip()
        match = str(rule.get("match", "")).strip()
        keywords = rule.get("keywords", []) if isinstance(rule.get("keywords"), list) else []

        for candidate in candidates:
            if not candidate:
                continue

            if equals and candidate == equals:
                return module_id, "map-rule", rule_name

            if contains and contains in candidate:
                return module_id, "map-rule", rule_name

            if match:
                try:
                    if re.search(match, candidate):
                        return module_id, "map-rule", rule_name
                except re.error:
                    # ignore bad regex rule
                    pass

            if keywords and all(k in candidate for k in keywords):
                return module_id, "map-rule", rule_name

    default_module_id = parse_int(module_map.get("defaultModuleId", 0), 0) if isinstance(module_map, dict) else 0
    if default_module_id > 0:
        return default_module_id, "map-default", None

    return 0, "none", None


def require_credentials_for_submission(args: argparse.Namespace) -> None:
    """Enforce secure credential input for real submissions."""
    if args.dry_run:
        return

    missing: List[str] = []
    if not str(args.http_user or "").strip():
        missing.append("HTTP_USER / --http-user")
    if not str(args.http_pass or "").strip():
        missing.append("HTTP_PASS / --http-pass")
    if not str(args.zentao_user or "").strip():
        missing.append("ZENTAO_USER / --zentao-user")
    if not str(args.zentao_pass or "").strip():
        missing.append("ZENTAO_PASS / --zentao-pass")

    if missing:
        raise RuntimeError(
            "缺少提交凭据，请通过环境变量或参数传入：" + "，".join(missing)
        )


def md5_hex(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def run_with_retry(
    fn,
    *,
    attempts: int,
    op_name: str,
    base_delay: float = 0.6,
):
    attempts = max(1, int(attempts))
    last_error: Optional[Exception] = None
    for i in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if i >= attempts:
                break
            time.sleep(min(5.0, base_delay * (2 ** (i - 1))))
    raise RuntimeError(f"{op_name} 失败（已重试 {attempts} 次）: {last_error}")


class ZenTaoWebSession:
    """Legacy web session client used for strong attachment binding (files[])."""

    def __init__(self, cfg: "ZenTaoConfig"):
        self.cfg = cfg
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(cfg.http_user, cfg.http_pass)
        self._logged_in = False

    def _headers(self, referer: str) -> Dict[str, str]:
        return {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": referer,
            "Accept": "application/json,text/plain,*/*",
        }

    def ensure_login(self) -> None:
        if self._logged_in:
            return

        login_page = f"{self.cfg.base_url}/index.php?m=user&f=login&referer=Lw=="
        self.session.get(login_page, timeout=30, verify=self.cfg.verify_ssl)

        random_resp = self.session.get(
            f"{self.cfg.base_url}/index.php?m=user&f=refreshRandom",
            timeout=30,
            verify=self.cfg.verify_ssl,
        )
        rand = random_resp.text.strip().strip('"')
        if not rand:
            raise RuntimeError("获取禅道登录随机串失败")

        encrypted = md5_hex(md5_hex(self.cfg.zentao_pass) + rand)

        payload = {
            "account": self.cfg.zentao_user,
            "password": encrypted,
            "passwordStrength": "3",
            "referer": "/",
            "verifyRand": rand,
            "keepLogin": "1",
            "captcha": "",
        }

        resp = self.session.post(
            f"{self.cfg.base_url}/index.php?m=user&f=login",
            data=payload,
            headers=self._headers(login_page),
            timeout=30,
            verify=self.cfg.verify_ssl,
        )

        text = resp.text.strip()
        try:
            data = json.loads(text)
        except Exception as exc:
            raise RuntimeError(f"禅道Web登录返回异常: {text[:200]}") from exc

        if data.get("result") != "success":
            raise RuntimeError(f"禅道Web登录失败: {data}")

        # quick verify that session can access index
        index_resp = self.session.get(
            f"{self.cfg.base_url}/index.php?m=my&f=index",
            timeout=30,
            verify=self.cfg.verify_ssl,
            allow_redirects=False,
        )
        if index_resp.status_code in (301, 302) and "m=user&f=login" in str(index_resp.headers.get("Location", "")):
            raise RuntimeError("禅道Web登录校验失败，仍跳转登录页")

        self._logged_in = True

    def create_bug_with_files(
        self,
        *,
        bug: Dict[str, Any],
        steps_html: str,
        local_attachments: List[str],
    ) -> int:
        self.ensure_login()

        product_id = int(bug["product_id"])
        create_url = f"{self.cfg.base_url}/index.php?m=bug&f=create&productID={product_id}&t=json"

        form: List[Tuple[str, str]] = [
            ("product", str(product_id)),
            ("module", str(int(bug.get("module_id", 0) or 0))),
            ("execution", str(int(bug.get("execution_id", 0) or 0))),
            ("project", str(int(bug.get("project_id", 0) or 0))),
            ("type", str(bug.get("bug_type", "codeerror") or "codeerror")),
            ("pri", str(int(bug.get("priority", 3) or 3))),
            ("severity", str(int(bug.get("severity", 3) or 3))),
            ("title", str(bug.get("title", "") or "")),
            ("steps", steps_html),
            ("keywords", ""),
            ("os", ""),
            ("browser", ""),
            ("deadline", ""),
        ]

        for build in bug.get("opened_builds", []):
            form.append(("openedBuild[]", str(build)))

        assignee = str(bug.get("assignee", "")).strip()
        if assignee and assignee not in {"待分配", "待补充"}:
            form.append(("assignedTo", assignee))

        files_payload: List[Tuple[str, Tuple[str, Any, str]]] = []
        file_handles: List[Any] = []
        try:
            for path_str in local_attachments:
                path = Path(path_str).expanduser()
                if not path.exists() or not path.is_file():
                    continue
                mime_type, _ = mimetypes.guess_type(str(path))
                mime_type = mime_type or "application/octet-stream"
                fh = path.open("rb")
                file_handles.append(fh)
                files_payload.append(("files[]", (path.name, fh, mime_type)))

            resp = self.session.post(
                create_url,
                data=form,
                files=files_payload if files_payload else None,
                headers=self._headers(create_url),
                timeout=60,
                verify=self.cfg.verify_ssl,
            )
        finally:
            for fh in file_handles:
                try:
                    fh.close()
                except Exception:
                    pass

        text = resp.text.strip()
        try:
            data = json.loads(text)
        except Exception as exc:
            raise RuntimeError(f"禅道Web创建缺陷返回异常: {text[:300]}") from exc

        if data.get("result") != "success":
            raise RuntimeError(f"禅道Web创建缺陷失败: {data}")

        bug_id = data.get("id")
        if not bug_id:
            raise RuntimeError(f"禅道Web创建缺陷未返回ID: {data}")

        return int(bug_id)


# -------------------------
# ZenTao API client
# -------------------------

@dataclass
class ZenTaoConfig:
    base_url: str
    http_user: str
    http_pass: str
    zentao_user: str
    zentao_pass: str
    state_path: Path
    verify_ssl: bool


class ZenTaoClient:
    def __init__(self, cfg: ZenTaoConfig):
        self.cfg = cfg
        self.auth = HTTPBasicAuth(cfg.http_user, cfg.http_pass)
        self.token: Optional[str] = None

    def _api_url(self, path: str) -> str:
        return f"{self.cfg.base_url}/api.php/v1{path}"

    def load_state(self) -> None:
        if not self.cfg.state_path.exists():
            return
        try:
            data = json.loads(self.cfg.state_path.read_text(encoding="utf-8"))
            token = data.get("token")
            if token:
                self.token = token
        except Exception:
            pass

    def save_state(self) -> None:
        if not self.token:
            return
        self.cfg.state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "formatVersion": 2,
            "provider": "zentao-v1-token",
            "zentaoUrl": self.cfg.base_url,
            "token": self.token,
            "account": self.cfg.zentao_user,
            "savedAt": datetime.now(timezone.utc).isoformat(),
        }
        self.cfg.state_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def login(self) -> str:
        if not self.cfg.http_user or not self.cfg.http_pass:
            raise RuntimeError("登录失败：缺少 HTTP_USER/HTTP_PASS")
        if not self.cfg.zentao_user or not self.cfg.zentao_pass:
            raise RuntimeError("登录失败：缺少 ZENTAO_USER/ZENTAO_PASS")

        payload = {"account": self.cfg.zentao_user, "password": self.cfg.zentao_pass}
        response = requests.post(
            self._api_url("/tokens"),
            auth=self.auth,
            json=payload,
            timeout=30,
            verify=self.cfg.verify_ssl,
        )
        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"Token login failed: HTTP {response.status_code} | {response.text[:300]}"
            )

        data = response.json()
        token = data.get("token")
        if not token:
            raise RuntimeError(f"Token missing in login response: {data}")

        self.token = token
        self.save_state()
        return token

    def ensure_token(self, force_refresh: bool = False) -> None:
        if force_refresh:
            self.login()
            return

        if not self.token:
            self.load_state()

        if not self.token:
            self.login()
            return

        # Validate current token quickly.
        check = requests.get(
            self._api_url("/user"),
            auth=self.auth,
            headers={"Token": self.token},
            timeout=20,
            verify=self.cfg.verify_ssl,
        )
        if check.status_code == 401:
            self.login()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        retry_on_unauthorized: bool = True,
        **kwargs: Any,
    ) -> requests.Response:
        self.ensure_token()

        req_headers = {"Token": self.token or ""}
        if headers:
            req_headers.update(headers)

        response = requests.request(
            method,
            self._api_url(path),
            auth=self.auth,
            headers=req_headers,
            timeout=30,
            verify=self.cfg.verify_ssl,
            **kwargs,
        )

        if response.status_code == 401 and retry_on_unauthorized:
            self.login()
            req_headers["Token"] = self.token or ""
            response = requests.request(
                method,
                self._api_url(path),
                auth=self.auth,
                headers=req_headers,
                timeout=30,
                verify=self.cfg.verify_ssl,
                **kwargs,
            )

        return response


# -------------------------
# Core submit flow
# -------------------------

def load_bug_items(input_path: Path) -> List[Dict[str, Any]]:
    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if input_path.suffix.lower() == ".jsonl":
        items: List[Dict[str, Any]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
        return items

    data = json.loads(text)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if isinstance(data.get("bugs"), list):
            return data["bugs"]
        return [data]

    raise ValueError("Unsupported input format, expected JSON object/list or JSONL")


def normalize_bug(raw: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    title = str(pick(raw, ["标题", "title", "bugTitle"], "")).strip()
    assignee = str(pick(raw, ["指派人", "assignee", "assignedTo"], "")).strip()

    steps = normalize_steps(pick(raw, ["步骤", "steps"], []))
    expectation = str(pick(raw, ["期望", "expectation", "expected"], "")).strip()
    affected_version = str(
        pick(raw, ["影响版本", "affectedVersion", "version"], defaults["affected_version"])
    ).strip()

    severity = parse_level(
        pick(raw, ["严重级别", "severity"], defaults["severity"]), "S", defaults["severity"]
    )
    priority = parse_level(
        pick(raw, ["优先级", "priority", "pri"], defaults["priority"]),
        "P",
        defaults["priority"],
    )

    attachments = normalize_attachments(
        pick(raw, ["图片/附件", "附件", "attachments", "images"], [])
    )

    product_id = parse_int(pick(raw, ["产品ID", "product", "productId"], defaults["product_id"]))
    module_id = parse_int(pick(raw, ["模块ID", "module", "moduleId"], defaults["module_id"]))
    project_id = parse_int(pick(raw, ["项目ID", "project", "projectId"], defaults["project_id"]))
    execution_id = parse_int(
        pick(raw, ["执行ID", "execution", "executionId"], defaults["execution_id"])
    )

    opened_build = pick(raw, ["构建版本", "openedBuild", "build"], defaults["opened_build"])
    if isinstance(opened_build, str):
        opened_builds = [x.strip() for x in re.split(r"[,，;；]", opened_build) if x.strip()]
        if not opened_builds:
            opened_builds = [defaults["opened_build"]]
    elif isinstance(opened_build, list):
        opened_builds = [str(x).strip() for x in opened_build if str(x).strip()]
        if not opened_builds:
            opened_builds = [defaults["opened_build"]]
    else:
        opened_builds = [defaults["opened_build"]]

    bug_type = str(pick(raw, ["缺陷类型", "type"], defaults["bug_type"]))

    if not expectation:
        expectation = "应符合需求文档与UI原型预期。"

    if not assignee:
        assignee = defaults["assignee"]

    return {
        "title": title,
        "assignee": assignee,
        "steps": steps,
        "expectation": expectation,
        "affected_version": affected_version,
        "severity": severity,
        "priority": priority,
        "attachments": attachments,
        "product_id": product_id,
        "module_id": module_id,
        "project_id": project_id,
        "execution_id": execution_id,
        "opened_builds": opened_builds,
        "bug_type": bug_type,
    }


def upload_attachment(
    client: ZenTaoClient,
    bug_id: int,
    file_path: str,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "source": file_path,
        "status": "failed",
        "fileId": None,
        "url": None,
        "error": None,
    }

    path = Path(file_path).expanduser()
    if not path.exists() or not path.is_file():
        result["error"] = "附件文件不存在"
        return result

    mime_type, _ = mimetypes.guess_type(str(path))
    mime_type = mime_type or "application/octet-stream"

    try:
        with path.open("rb") as f:
            response = client.request(
                "POST",
                "/files",
                data={"objectType": "bug", "objectID": str(bug_id)},
                files={"imgFile": (path.name, f, mime_type)},
            )

        if response.status_code != 200:
            result["error"] = f"上传失败 HTTP {response.status_code}: {response.text[:200]}"
            return result

        data = response.json()
        if data.get("status") != "success":
            result["error"] = f"上传失败: {data}"
            return result

        file_id = data.get("id") or data.get("data", {}).get("id")
        ext = extract_file_extension(path.name)
        file_url = (
            f"{client.cfg.base_url}/index.php?m=file&f=read&t={ext}&fileID={file_id}"
            if file_id
            else (data.get("url") or "")
        )

        result.update(
            {
                "status": "success",
                "fileId": file_id,
                "url": file_url,
            }
        )
        return result
    except Exception as exc:
        result["error"] = str(exc)
        return result


def find_existing_bug_by_title(
    client: ZenTaoClient,
    *,
    product_id: int,
    title: str,
    limit: int = 200,
) -> Optional[Dict[str, Any]]:
    if not title:
        return None

    response = client.request(
        "GET",
        "/bugs",
        params={"product": product_id, "limit": max(1, min(int(limit), 500)), "orderBy": "id_desc"},
    )
    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except Exception:
        return None

    bugs = data.get("bugs", []) if isinstance(data, dict) else []
    for bug in bugs:
        if not isinstance(bug, dict):
            continue
        if str(bug.get("title", "")).strip() == title.strip():
            return bug

    return None


def submit_bugs(args: argparse.Namespace) -> Dict[str, Any]:
    cfg = ZenTaoConfig(
        base_url=normalize_base_url(args.zentao_url),
        http_user=args.http_user,
        http_pass=args.http_pass,
        zentao_user=args.zentao_user,
        zentao_pass=args.zentao_pass,
        state_path=Path(args.state_path).expanduser().resolve(),
        verify_ssl=args.verify_ssl,
    )
    client = ZenTaoClient(cfg)
    web_client = ZenTaoWebSession(cfg)

    input_path = Path(args.input).expanduser().resolve()
    bug_items = load_bug_items(input_path)

    defaults = {
        "product_id": args.product_id,
        "module_id": args.module_id,
        "project_id": args.project_id,
        "execution_id": args.execution_id,
        "opened_build": args.opened_build,
        "bug_type": args.bug_type,
        "severity": args.default_severity,
        "priority": args.default_priority,
        "affected_version": args.default_affected_version,
        "assignee": args.default_assignee,
    }

    module_map_path = Path(args.module_map).expanduser().resolve() if args.module_map else None
    module_map = load_module_map(module_map_path)

    if not args.dry_run:
        client.ensure_token(force_refresh=args.force_refresh_token)

    results: List[Dict[str, Any]] = []

    for idx, raw in enumerate(bug_items, 1):
        row_result: Dict[str, Any] = {
            "index": idx,
            "status": "failed",
            "title": None,
            "bugId": None,
            "bugLink": None,
            "moduleId": 0,
            "moduleSource": "none",
            "moduleRule": None,
            "createMethod": None,
            "duplicateOf": None,
            "error": None,
            "uploads": [],
        }

        try:
            bug = normalize_bug(raw, defaults)
            row_result["title"] = bug["title"]

            resolved_module_id, module_source, module_rule = resolve_module_id(
                explicit_module_id=bug["module_id"],
                title=bug["title"],
                module_map=module_map,
            )
            bug["module_id"] = resolved_module_id
            row_result["moduleId"] = resolved_module_id
            row_result["moduleSource"] = module_source
            row_result["moduleRule"] = module_rule

            if not bug["title"]:
                raise ValueError("标题为空，无法提交")
            if not bug["product_id"]:
                raise ValueError("缺少 product_id（产品ID）")

            attachment_links: List[Tuple[str, str]] = []
            # Keep external links as-is (already accessible URLs)
            for a in bug["attachments"]:
                if re.match(r"^https?://", a, flags=re.I):
                    attachment_links.append((Path(a).name or a, a))

            local_attachments = [
                a for a in bug["attachments"] if not re.match(r"^https?://", a, flags=re.I)
            ]

            steps_html = build_steps_html(
                steps=bug["steps"],
                expectation=bug["expectation"],
                affected_version=bug["affected_version"],
                attachment_links=attachment_links,
            )

            payload: Dict[str, Any] = {
                "product": bug["product_id"],
                "title": bug["title"],
                "openedBuild": bug["opened_builds"],
                "severity": bug["severity"],
                "pri": bug["priority"],
                "type": bug["bug_type"],
                "steps": steps_html,
            }

            if bug["module_id"] > 0:
                payload["module"] = bug["module_id"]
            if bug["project_id"] > 0:
                payload["project"] = bug["project_id"]
            if bug["execution_id"] > 0:
                payload["execution"] = bug["execution_id"]
            if bug["assignee"] and bug["assignee"] not in {"待分配", "待补充"}:
                payload["assignedTo"] = bug["assignee"]

            if args.create_mode == "legacy":
                use_legacy_strong = True
            elif args.create_mode == "api":
                use_legacy_strong = False
            else:
                use_legacy_strong = args.attachment_mode == "strong" and len(local_attachments) > 0

            if args.dry_run:
                row_result["status"] = "dry-run"
                row_result["createMethod"] = "legacy-web" if use_legacy_strong else "api-v1"
                row_result["payloadPreview"] = payload
                results.append(row_result)
                continue

            # Dedupe by title + product before submitting.
            if args.dedupe:
                existing_bug = run_with_retry(
                    lambda: find_existing_bug_by_title(
                        client,
                        product_id=int(bug["product_id"]),
                        title=str(bug["title"]),
                        limit=args.dedupe_limit,
                    ),
                    attempts=args.retry_attempts,
                    op_name="去重检查",
                )
                if existing_bug:
                    existing_id = parse_int(existing_bug.get("id"), 0)
                    row_result["status"] = "duplicate"
                    row_result["bugId"] = existing_id if existing_id > 0 else None
                    row_result["bugLink"] = (
                        f"{cfg.base_url}/index.php?m=bug&f=view&bugID={existing_id}"
                        if existing_id > 0
                        else None
                    )
                    row_result["duplicateOf"] = existing_bug
                    row_result["createMethod"] = "dedupe-skip"
                    results.append(row_result)
                    continue

            if use_legacy_strong:
                bug_id = run_with_retry(
                    lambda: web_client.create_bug_with_files(
                        bug=bug,
                        steps_html=steps_html,
                        local_attachments=local_attachments,
                    ),
                    attempts=args.retry_attempts,
                    op_name="禅道Web提单",
                )

                row_result["createMethod"] = "legacy-web"
                row_result["bugId"] = bug_id
                row_result["bugLink"] = f"{cfg.base_url}/index.php?m=bug&f=view&bugID={bug_id}"

                # Pull attached files from bug detail for explicit upload report.
                detail_resp = run_with_retry(
                    lambda: client.request("GET", f"/bugs/{bug_id}"),
                    attempts=args.retry_attempts,
                    op_name="读取缺陷详情",
                )
                if detail_resp.status_code == 200:
                    try:
                        detail_json = detail_resp.json()
                        files_obj = detail_json.get("files", {})
                        if isinstance(files_obj, dict):
                            for _, file_meta in files_obj.items():
                                if not isinstance(file_meta, dict):
                                    continue
                                row_result["uploads"].append(
                                    {
                                        "source": file_meta.get("title") or file_meta.get("name") or "",
                                        "status": "success",
                                        "fileId": file_meta.get("id"),
                                        "url": file_meta.get("url"),
                                        "error": None,
                                    }
                                )
                    except Exception:
                        pass
            else:
                def _create_v1_bug() -> int:
                    create_resp = client.request(
                        "POST",
                        "/bugs",
                        headers={"Content-Type": "application/json"},
                        json=payload,
                    )
                    if create_resp.status_code != 200:
                        raise RuntimeError(
                            f"创建失败 HTTP {create_resp.status_code}: {create_resp.text[:300]}"
                        )
                    create_json = create_resp.json()
                    if create_json.get("status") != "success":
                        raise RuntimeError(f"创建失败: {create_json}")
                    return int(create_json.get("id"))

                bug_id = run_with_retry(
                    _create_v1_bug,
                    attempts=args.retry_attempts,
                    op_name="API提单",
                )

                row_result["createMethod"] = "api-v1"
                row_result["bugId"] = bug_id
                row_result["bugLink"] = f"{cfg.base_url}/index.php?m=bug&f=view&bugID={bug_id}"

                # Upload local attachments (best effort) and append links into steps.
                uploaded_links: List[Tuple[str, str]] = []
                if local_attachments:
                    for attachment in local_attachments:
                        up = run_with_retry(
                            lambda a=attachment: upload_attachment(client, bug_id, a),
                            attempts=args.retry_attempts,
                            op_name=f"上传附件:{Path(attachment).name}",
                        )
                        row_result["uploads"].append(up)
                        if up.get("status") == "success" and up.get("url"):
                            uploaded_links.append((Path(attachment).name, str(up["url"])))

                # If we got uploaded links, append them into bug steps for direct traceability.
                if uploaded_links:
                    merged_links = attachment_links + uploaded_links
                    updated_steps = build_steps_html(
                        steps=bug["steps"],
                        expectation=bug["expectation"],
                        affected_version=bug["affected_version"],
                        attachment_links=merged_links,
                    )

                    def _update_steps() -> requests.Response:
                        return client.request(
                            "PUT",
                            f"/bugs/{bug_id}",
                            headers={"Content-Type": "application/json"},
                            json={"steps": updated_steps},
                        )

                    update_resp = run_with_retry(
                        _update_steps,
                        attempts=args.retry_attempts,
                        op_name="附件链接回填",
                    )
                    if update_resp.status_code != 200:
                        row_result["uploads"].append(
                            {
                                "status": "failed",
                                "error": f"附件链接回填失败 HTTP {update_resp.status_code}: {update_resp.text[:200]}",
                            }
                        )

            row_result["status"] = "success"
            results.append(row_result)

        except Exception as exc:
            row_result["error"] = str(exc)
            results.append(row_result)

    total = len(results)
    success = len([x for x in results if x["status"] == "success"])
    failed = len([x for x in results if x["status"] == "failed"])
    dry_run = len([x for x in results if x["status"] == "dry-run"])
    duplicate = len([x for x in results if x["status"] == "duplicate"])

    summary = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "input": str(input_path),
        "moduleMap": {
            "path": str(module_map_path) if module_map_path else None,
            "defaultModuleId": module_map.get("defaultModuleId", 0),
            "rules": len(module_map.get("rules", [])),
        },
        "createMode": args.create_mode,
        "attachmentMode": args.attachment_mode,
        "dedupe": bool(args.dedupe),
        "retryAttempts": int(args.retry_attempts),
        "total": total,
        "success": success,
        "failed": failed,
        "duplicate": duplicate,
        "dryRun": dry_run,
        "results": results,
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 提交完成：总计 {total} 条，成功 {success} 条，重复跳过 {duplicate} 条，失败 {failed} 条")
    print(f"📄 结果文件：{output_path}")

    return summary


# -------------------------
# CLI
# -------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Submit normalized bugs to ZenTao automatically")
    parser.add_argument("--input", required=True, help="JSON/JSONL bug input file")
    parser.add_argument(
        "--output",
        default="./playwright/.auth/zentao-submit-result.json",
        help="submission result JSON path",
    )

    parser.add_argument("--zentao-url", default=os.getenv("ZENTAO_URL", "https://pm.jsyyds.com/"))
    parser.add_argument("--http-user", default=os.getenv("HTTP_USER", ""))
    parser.add_argument("--http-pass", default=os.getenv("HTTP_PASS", ""))
    parser.add_argument("--zentao-user", default=os.getenv("ZENTAO_USER", ""))
    parser.add_argument("--zentao-pass", default=os.getenv("ZENTAO_PASS", ""))
    parser.add_argument(
        "--state-path",
        default=os.getenv("STORAGE_STATE_PATH", "./playwright/.auth/zentao-storageState.json"),
    )
    parser.add_argument(
        "--module-map",
        default=os.getenv("ZENTAO_MODULE_MAP", ""),
        help="optional module mapping json path",
    )

    parser.add_argument("--product-id", type=int, default=parse_int(os.getenv("ZENTAO_PRODUCT_ID", "0"), 0))
    parser.add_argument("--module-id", type=int, default=parse_int(os.getenv("ZENTAO_MODULE_ID", "0"), 0))
    parser.add_argument("--project-id", type=int, default=parse_int(os.getenv("ZENTAO_PROJECT_ID", "0"), 0))
    parser.add_argument(
        "--execution-id", type=int, default=parse_int(os.getenv("ZENTAO_EXECUTION_ID", "0"), 0)
    )
    parser.add_argument("--opened-build", default=os.getenv("ZENTAO_OPENED_BUILD", "trunk"))
    parser.add_argument("--bug-type", default=os.getenv("ZENTAO_BUG_TYPE", "codeerror"))

    parser.add_argument("--default-severity", type=int, default=parse_int(os.getenv("DEFAULT_SEVERITY", "3"), 3))
    parser.add_argument("--default-priority", type=int, default=parse_int(os.getenv("DEFAULT_PRIORITY", "3"), 3))
    parser.add_argument(
        "--default-affected-version",
        default=os.getenv("DEFAULT_AFFECTED_VERSION", "待补充"),
    )
    parser.add_argument("--default-assignee", default=os.getenv("DEFAULT_ASSIGNEE", "孙晓晨"))

    parser.add_argument("--dry-run", action="store_true", help="Only preview payloads, do not submit")
    parser.add_argument("--force-refresh-token", action="store_true")
    parser.add_argument(
        "--create-mode",
        choices=["auto", "api", "legacy"],
        default=os.getenv("ZENTAO_CREATE_MODE", "auto"),
        help="auto: attachments use legacy, otherwise api; api: force v1 api; legacy: force legacy web create",
    )
    parser.add_argument(
        "--attachment-mode",
        choices=["strong", "api-link"],
        default=os.getenv("ZENTAO_ATTACHMENT_MODE", "strong"),
        help="strong: files[] strong binding via legacy create; api-link: v1 upload + link backfill",
    )
    parser.add_argument(
        "--dedupe",
        action=argparse.BooleanOptionalAction,
        default=env_bool("ZENTAO_DEDUPE", "true"),
        help="skip submit when same title already exists under same product",
    )
    parser.add_argument(
        "--dedupe-limit",
        type=int,
        default=parse_int(os.getenv("ZENTAO_DEDUPE_LIMIT", "200"), 200),
        help="max records scanned for dedupe in product scope",
    )
    parser.add_argument(
        "--retry-attempts",
        type=int,
        default=parse_int(os.getenv("ZENTAO_RETRY_ATTEMPTS", "3"), 3),
        help="retry attempts for network/submit/upload operations",
    )
    parser.add_argument(
        "--verify-ssl",
        type=lambda x: str(x).strip().lower() in {"1", "true", "yes", "on"},
        default=env_bool("VERIFY_SSL", "true"),
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    require_credentials_for_submission(args)

    summary = submit_bugs(args)
    if summary["failed"] > 0 and not args.dry_run:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
