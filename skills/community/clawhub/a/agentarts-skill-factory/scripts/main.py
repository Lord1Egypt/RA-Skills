#!/usr/bin/env python3
"""AgentArts Skill Factory - Generate a standard Skill from AgentArts workflow params."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# SKILL.md template
# ============================================================

SKILL_MD_TEMPLATE = '''\
---
name: {name}
description: {description}
triggers:
{triggers_yaml}
---

# {title}

{user_identity_section}{greeting_section}\
## 固定接口

- Base URL: `{base_url}`
- Path: `{path}`
- 固定版本：`?endpoint=Latest`

## 触发条件

出现以下意图时优先使用本技能：

{trigger_conditions}

## 行为规则

{behavior_rules}

## 权限错误处理

当云端工作流返回以下类型的错误时，**直接将原始信息返回给用户**，不进行重试或网络分析：

### 识别条件

返回内容包含以下关键词之一：

- "没有权限" / "无权限" / "权限不足"
- "无权访问" / "access denied" / "permission denied"
- "unauthorized" / "forbidden"
- "您没有" + "权限"

### 处理方式

1. **直接返回原始信息**：将云端返回的原始错误信息原样展示给用户
2. **禁止重试**：不进行任何形式的反复尝试或重试
3. **禁止网络分析**：不分析网络原因、不提示网络问题
4. **简洁提示**：仅说明这是权限问题，建议用户联系管理员

### 示例输出

```
Warning: 权限不足
云端返回：[原始错误信息]
建议：请联系系统管理员确认您的访问权限。
```

## 鉴权

- API Key 通过环境变量 `AGENTARTS_API_KEY` 传入，或使用 `--api-key` 参数指定
- 已内置默认值，可直接使用（敏感信息，注意不要泄露 SKILL.md）

## 输入参数

- `--query`：业务查询指令
- `--command`：自然语言指令（支持直接触发调用）
- `--session-id`：{session_id_desc}

## 示例

```bash
python scripts/invoke_agentarts.py --command "{example_command}" --session-id "{session_id}"
```
'''


# ============================================================
# invoke_agentarts.py template
# ============================================================

INVOKE_PY_TEMPLATE = '''\
#!/usr/bin/env python3

"""Huawei AgentArts workflow simple invoker."""


from __future__ import annotations


import argparse

import json

import os

import re

import secrets

import sys

import socket

import ssl

from urllib import error, parse, request

from typing import Any, Dict, Optional



try:

    import requests

except ImportError:

    requests = None



# ==================== 配置项 ====================

DEFAULT_BASE_URL = "{base_url}"

DEFAULT_PATH = "{path}"

DEFAULT_AGENTARTS_API_KEY = os.environ.get("AGENTARTS_API_KEY", "{api_key}")

DEFAULT_SESSION_ID = "{session_id}"



NUMBER_PATTERN = re.compile(r"[-+]?\\d+(?:\\.\\d+)?")



CURRENT_VALUE_KEYS = (

    "current", "currentvalue", "current_value", "value",

    "temperature", "temp", "\\u5f53\\u524d\\u503c", "\\u5f53\\u524d\\u6e29\\u5ea6", "\\u6e29\\u5ea6", "\\u6570\\u503c"

)

RANGE_KEYS = ("normalrange", "normal_range", "range", "expectedrange", "threshold", "\\u6b63\\u5e38\\u8303\\u56f4", "\\u9608\\u503c\\u8303\\u56f4")

MIN_KEYS = ("min", "minimum", "minvalue", "normalmin", "\\u6b63\\u5e38\\u4e0b\\u9650", "\\u4e0b\\u9650")

MAX_KEYS = ("max", "maximum", "maxvalue", "normalmax", "\\u6b63\\u5e38\\u4e0a\\u9650", "\\u4e0a\\u9650")

# ================================================



if hasattr(sys.stdout, "reconfigure"):

    sys.stdout.reconfigure(line_buffering=True)

if hasattr(sys.stderr, "reconfigure"):

    sys.stderr.reconfigure(line_buffering=True)




def mask_key(value: str) -> str:

    if len(value) <= 8:

        return "*" * len(value)

    return f"{{value[:4]}}...{{value[-4:]}}"




def format_bearer_token(value: str) -> str:

    if value.lower().startswith("bearer "):

        return value

    return f"Bearer {{value}}"




class SimpleResponse:

    def __init__(self, status_code: int, headers: Dict[str, str], content: bytes):

        self.status_code = status_code

        self.headers = headers

        self.content = content

        self.text = content.decode("utf-8", errors="replace")



    @property

    def ok(self) -> bool:

        return 200 <= self.status_code < 300




def _resolve_ip_direct(host: str, port: int = 443) -> Optional[str]:

    try:

        infos = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)

        if infos:

            return infos[0][4][0]

    except Exception:

        pass

    return None




def _send_via_ip_direct(

    host: str, path: str, headers: Dict[str, str], data: bytes, timeout: int

) -> SimpleResponse:

    ip = _resolve_ip_direct(host)

    if not ip:

        raise ConnectionError(f"Cannot resolve {{host}}")



    ctx = ssl.create_default_context()
    print("[fallback] WARNING: SSL verification disabled for IP-direct connection")

    ctx.check_hostname = False

    ctx.verify_mode = ssl.CERT_NONE



    sock = socket.create_connection((ip, 443), timeout=timeout)

    ssock = ctx.wrap_socket(sock, server_hostname=ip)



    if "Host" not in headers and "host" not in headers:

        headers["Host"] = host



    request_line = f"POST {{path}} HTTP/1.1\\r\\n"

    header_lines = "".join(f"{{k}}: {{v}}\\r\\n" for k, v in headers.items())

    body = f"{{request_line}}{{header_lines}}Content-Length: {{len(data)}}\\r\\nConnection: close\\r\\n\\r\\n"

    ssock.sendall(body.encode("utf-8") + data)



    response_data = b""

    while True:

        chunk = ssock.recv(8192)

        if not chunk:

            break

        response_data += chunk

    ssock.close()



    text = response_data.decode("utf-8", errors="replace")

    header_end = text.find("\\r\\n\\r\\n")

    if header_end == -1:

        return SimpleResponse(0, {{}}, response_data)



    header_section = text[:header_end]

    body_content = response_data[header_end + 4:]

    status_line = header_section.split("\\r\\n")[0]

    status_code = int(status_line.split(" ", 2)[1]) if " " in status_line else 0



    resp_headers: Dict[str, str] = {{}}

    for line in header_section.split("\\r\\n")[1:]:

        if ":" in line:

            k, v = line.split(":", 1)

            resp_headers[k.strip()] = v.strip()



    return SimpleResponse(status_code, resp_headers, body_content)




def send_post_request(url: str, headers: Dict[str, str], data: bytes, timeout: int) -> SimpleResponse:

    try:

        if requests is not None:

            response = requests.request("POST", url, headers=headers, data=data, timeout=timeout)

            return SimpleResponse(response.status_code, dict(response.headers), response.content)



        req = request.Request(url, data=data, headers=headers, method="POST")

        with request.urlopen(req, timeout=timeout) as resp:

            return SimpleResponse(resp.status, dict(resp.headers), resp.read())



    except error.HTTPError as exc:

        return SimpleResponse(exc.code, dict(exc.headers), exc.read())

    except (ConnectionResetError, ConnectionError, OSError) as exc:

        parsed = parse.urlparse(url)

        host = parsed.hostname or ""

        path = parsed.path

        if parsed.query:

            path = f"{{path}}?{{parsed.query}}"

        if host:

            print(f"[fallback] SSL reset detected, trying IP-direct connection to {{host}}...")

            return _send_via_ip_direct(host, path, headers, data, timeout)

        raise




def generate_session_id() -> str:

    return f"s-{{secrets.token_hex(12)}}"




def build_url(base_url: str, path: str) -> str:

    base = base_url.rstrip("/")

    full_path = path if path.startswith("/") else f"/{{path}}"

    query = parse.urlencode({{"endpoint": "Latest"}})

    return f"{{base}}{{full_path}}?{{query}}"




def parse_json_or_text(text: str) -> Any:

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        return text




def parse_sse_events(raw_bytes: bytes) -> list[Any]:

    text = raw_bytes.decode("utf-8", errors="replace")

    events: list[Any] = []

    for line in text.splitlines():

        if not line.startswith("data:"):

            continue

        payload = line[5:].strip()

        if payload:

            events.append(parse_json_or_text(payload))

    return events




def looks_like_sse(text: str) -> bool:

    return text.lstrip().startswith("data:")




def extract_result(response: SimpleResponse) -> Any:

    content_type = response.headers.get("Content-Type", "")

    if "text/event-stream" in content_type or looks_like_sse(response.text):

        return parse_sse_events(response.content)

    return parse_json_or_text(response.text)




def resolve_query(query: Optional[str], command: Optional[str]) -> str:

    if query and query.strip():

        return query.strip()

    if not command or not command.strip():

        raise ValueError("query or command is required")

    return command.strip()




def extract_first_number(value: Any) -> Optional[float]:

    if value is None:

        return None

    if isinstance(value, (int, float)):

        return float(value)

    text = str(value).strip()

    match = NUMBER_PATTERN.search(text)

    if not match:

        return None

    try:

        return float(match.group(0))

    except ValueError:

        return None




def parse_range_value(value: Any) -> tuple[Optional[float], Optional[float], str]:

    display = str(value).strip() if value is not None else ""

    if isinstance(value, (list, tuple)) and len(value) >= 2:

        low = extract_first_number(value[0])

        high = extract_first_number(value[1])

        if low and high:

            return min(low, high), max(low, high), display

    if isinstance(value, dict):

        low = extract_first_number(value.get("min") or value.get("low"))

        high = extract_first_number(value.get("max") or value.get("high"))

        if low and high:

            return min(low, high), max(low, high), display

    normalized = display.replace("\\uff5e", "-").replace("~", "-").replace("\\u81f3", "-")

    numbers = NUMBER_PATTERN.findall(normalized)

    if len(numbers) >= 2:

        try:

            first, second = float(numbers[0]), float(numbers[1])

            return min(first, second), max(first, second), display

        except ValueError:

            pass

    return None, None, display




def pick_value_case_insensitive(node: Dict[str, Any], keys: tuple[str, ...]) -> Any:

    lowered = {{k.lower(): k for k in node.keys()}}

    for key in keys:

        if key in lowered:

            return node.get(lowered[key])

    return None




def detect_out_of_range_items(result: Any) -> list[Dict[str, str]]:

    findings: list[Dict[str, str]] = []



    def visit(node: Any, hint: str = "\\u5de1\\u68c0\\u6307\\u6807"):

        if isinstance(node, dict):

            metric = str(

                node.get("metric") or node.get("name") or node.get("\\u6307\\u6807") or hint

            ).strip() or "\\u5de1\\u68c0\\u6307\\u6807"

            current_raw = pick_value_case_insensitive(node, CURRENT_VALUE_KEYS)

            range_raw = pick_value_case_insensitive(node, RANGE_KEYS)

            min_raw = pick_value_case_insensitive(node, MIN_KEYS)

            max_raw = pick_value_case_insensitive(node, MAX_KEYS)



            current_val = extract_first_number(current_raw)

            low, high, range_disp = None, None, ""



            if range_raw:

                low, high, range_disp = parse_range_value(range_raw)

            if (low is None or high is None) and min_raw and max_raw:

                low = extract_first_number(min_raw)

                high = extract_first_number(max_raw)



            if current_val is not None and low is not None and high is not None:

                if not (low <= current_val <= high):

                    findings.append({{

                        "metric": metric,

                        "current": str(current_raw).strip(),

                        "normal_range": range_disp or f"{{low}}~{{high}}"

                    }})

            for v in node.values():

                visit(v, metric)

        elif isinstance(node, list):

            for item in node:

                visit(item, hint)



    visit(result)

    dedup = {{}}

    for item in findings:

        key = f"{{item['metric']}}|{{item['current']}}"

        dedup[key] = item

    return list(dedup.values())




def print_result(result: Any) -> None:

    if isinstance(result, (dict, list)):

        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:

        print(result)




# 权限错误关键词

PERMISSION_ERROR_KEYWORDS = [

    "\\u6ca1\\u6709\\u6743\\u9650", "\\u65e0\\u6743\\u9650", "\\u6743\\u9650\\u4e0d\\u8db3",

    "\\u65e0\\u6743\\u8bbf\\u95ee", "access denied", "permission denied",

    "unauthorized", "forbidden",

]




def check_permission_error(result: Any) -> Optional[str]:

    """\\u68c0\\u67e5\\u8fd4\\u56de\\u7ed3\\u679c\\u4e2d\\u662f\\u5426\\u5305\\u542b\\u6743\\u9650\\u9519\\u8bef\\u4fe1\\u606f\\u3002\\u8fd4\\u56de\\u539f\\u59cb\\u9519\\u8bef\\u4fe1\\u606f\\uff0c\\u5426\\u5219\\u8fd4\\u56de None\\u3002"""

    text = ""

    if isinstance(result, str):

        text = result

    elif isinstance(result, (dict, list)):

        text = json.dumps(result, ensure_ascii=False)

    else:

        text = str(result)



    text_lower = text.lower()

    for keyword in PERMISSION_ERROR_KEYWORDS:

        if keyword.lower() in text_lower:

            return text



    if "\\u60a8\\u6ca1\\u6709" in text and "\\u6743\\u9650" in text:

        return text



    return None




def invoke(

    url: str,

    authorization_token: str,

    session_id: str,

    query: str,

    timeout: int

) -> int:

    payload = json.dumps({{"inputs": {{"query": query}}}}, ensure_ascii=False).encode("utf-8")

    headers = {{

        "Content-Type": "application/json",

        "Authorization": authorization_token,

        "x-hw-agentarts-session-id": session_id,

    }}



    print(f"[request] POST {{url}}")

    print(f"[request] SessionID: {{session_id}}")

    print(f"[request] API-Key: {{mask_key(authorization_token)}}")



    try:

        response = send_post_request(url=url, headers=headers, data=payload, timeout=timeout)

        print(f"\\n[response] Status: {{response.status_code}}")

        result = extract_result(response)

        print("\\n===== \\u5de5\\u4f5c\\u6d41\\u8fd4\\u56de\\u7ed3\\u679c =====")

        print_result(result)



        # 检测超范围指标

        if response.ok:

            out_items = detect_out_of_range_items(result)

            if out_items:

                print("\\n===== \\u68c0\\u6d4b\\u5230\\u8d85\\u8303\\u56f4\\u6307\\u6807 =====")

                for it in out_items:

                    print(f"- {{it['metric']}} | \\u5f53\\u524d: {{it['current']}} | \\u6b63\\u5e38\\u8303\\u56f4: {{it['normal_range']}}")



        # 检测权限错误

        perm_err = check_permission_error(result)

        if perm_err:

            print(f"\\nWarning: \\u6743\\u9650\\u4e0d\\u8db3")

            print(f"\\u4e91\\u7aef\\u8fd4\\u56de\\uff1a{{perm_err}}")

            print(f"\\u5efa\\u8bae\\uff1a\\u8bf7\\u8054\\u7cfb\\u7cfb\\u7edf\\u7ba1\\u7406\\u5458\\u786e\\u8ba4\\u60a8\\u7684\\u8bbf\\u95ee\\u6743\\u9650\\u3002")



        return 0



    except Exception as exc:

        print(f"\\n[error] \\u8c03\\u7528\\u5f02\\u5e38: {{exc}}", file=sys.stderr)

        return 1




def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Simplified AgentArts Workflow Invoker")

    parser.add_argument("--query", help="\\u4e1a\\u52a1\\u67e5\\u8be2\\u6307\\u4ee4")

    parser.add_argument("--command", help="\\u81ea\\u7136\\u8bed\\u8a00\\u6307\\u4ee4")

    parser.add_argument("--api-key", help="AgentArts \\u9274\\u6743Key")

    parser.add_argument("--session-id", help="\\u81ea\\u5b9a\\u4e49\\u4f1a\\u8bddID")


    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="\\u7f51\\u5173\\u5730\\u5740")

    parser.add_argument("--path", default=DEFAULT_PATH, help="\\u8c03\\u7528\\u8def\\u5f84")

    parser.add_argument("--timeout", type=int, default=60, help="\\u8d85\\u65f6\\u65f6\\u95f4(\\u79d2)")

    return parser.parse_args()




def main() -> int:

    args = parse_args()

    try:

        query = resolve_query(args.query, args.command)

    except ValueError as e:

        print(f"[error] {{e}}", file=sys.stderr)

        return 2



    session_id = args.session_id or DEFAULT_SESSION_ID or generate_session_id()

    url = build_url(args.base_url, args.path)

    token = format_bearer_token(args.api_key or DEFAULT_AGENTARTS_API_KEY)



    return invoke(

        url=url,

        authorization_token=token,

        session_id=session_id,

        query=query,

        timeout=args.timeout

    )




if __name__ == "__main__":

    raise SystemExit(main())
'''


# ============================================================
# Generator logic
# ============================================================

DEFAULT_BEHAVIOR_RULES = """\
- 第一次调用 API 时：

  - **只输出云端工作流返回的结果**

  - **不自动执行后续分析**

  - **不自动生成报告或 PPT**

  - 提示用户可以继续追问更详细内容


- 如果用户需要进一步分析：

  - 需要用户明确要求（如"分析原因"、"请专家分析"等）
"""


def _generate_session_id() -> str:
    return f"s-{secrets.token_hex(8)}"[:32]


def generate_skill(config: Dict[str, Any], output_dir: Optional[str] = None) -> str:
    """Generate a complete AgentArts Skill directory.

    Args:
        config: Dict with keys: name, description, triggers, base_url, path,
                session_id, behavior_first_call, title
        output_dir: Parent directory for the generated skill folder.
                    Defaults to the script's parent parent (skills root).

    Returns:
        Path to the generated skill directory.
    """
    # --- Validate required fields ---
    required = ["name", "description", "triggers", "base_url", "path", "api_key"]
    missing = [f for f in required if config.get(f) is None]
    if missing:
        raise ValueError(f"Missing required config fields: {missing}")

    name = config["name"]
    description = config["description"]
    triggers = config["triggers"]
    if isinstance(triggers, str):
        triggers = [t.strip() for t in triggers.split(",") if t.strip()]

    base_url = config["base_url"]
    path = config["path"]
    api_key = config["api_key"]

    # --- Optional fields with defaults ---
    user_identity = config.get("user_identity", "")
    greeting = config.get("greeting", "")
    session_id = config.get("session_id", "") or _generate_session_id()
    behavior_rules = config.get("behavior_first_call", DEFAULT_BEHAVIOR_RULES)
    title = config.get("title", f"{name} Workflow API Skill")

    # --- Determine output directory ---
    if output_dir:
        skill_dir = Path(output_dir) / name
    else:
        # Default: current working directory / name
        skill_dir = Path.cwd() / name

    scripts_dir = skill_dir / "scripts"

    # --- Generate SKILL.md ---
    triggers_yaml = "\n".join(f"  - {t}" for t in triggers)
    trigger_conditions = "\n".join(f"- {t}" for t in triggers)

    user_identity_section = f"用户身份：{user_identity}。\n\n" if user_identity else ""
    greeting_section = f"固定助手开场白（写死）：\n\n- `{greeting}`\n\n" if greeting else ""

    session_id_desc = f"默认'{session_id}'" if session_id else "自动生成"

    # Pick first trigger as example command
    example_command = triggers[0] if triggers else "帮我查询"

    skill_md = SKILL_MD_TEMPLATE.format(
        name=name,
        description=description,
        triggers_yaml=triggers_yaml,
        title=title,
        user_identity_section=user_identity_section,
        greeting_section=greeting_section,
        base_url=base_url,
        path=path,
        trigger_conditions=trigger_conditions,
        behavior_rules=behavior_rules,
        api_key=api_key,
        session_id_desc=session_id_desc,
        session_id=session_id,
        example_command=example_command,
    )

    # --- Generate invoke_agentarts.py ---
    invoke_py = INVOKE_PY_TEMPLATE.format(
        base_url=base_url,
        path=path,
        api_key=api_key,
        session_id=session_id,
    )

    # --- Write files ---
    scripts_dir.mkdir(parents=True, exist_ok=True)

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md, encoding="utf-8")

    invoke_py_path = scripts_dir / "invoke_agentarts.py"
    invoke_py_path.write_text(invoke_py, encoding="utf-8")

    # --- Summary ---
    print(f"[generated] Skill directory: {skill_dir}")
    print(f"[generated] SKILL.md: {skill_md_path}")
    print(f"[generated] invoke_agentarts.py: {invoke_py_path}")
    print(f"\n[summary]")
    print(f"  name: {name}")
    print(f"  base_url: {base_url}")
    print(f"  path: {path}")
    print(f"  api_key: {api_key[:4]}...{api_key[-4:]}")
    print(f"  session_id: {session_id}")
    print(f"  triggers: {triggers}")

    return str(skill_dir)


# ============================================================
# CLI entry point
# ============================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AgentArts Skill Factory - Generate a Skill from workflow params"
    )
    parser.add_argument(
        "--config",
        help="JSON config string or path to JSON file",
    )
    parser.add_argument(
        "--output-dir",
        help="Parent directory for the generated skill folder",
    )
    # Individual params (alternative to --config)
    parser.add_argument("--name", help="Skill name")
    parser.add_argument("--description", help="Skill description")
    parser.add_argument("--triggers", help="Comma-separated trigger phrases")
    parser.add_argument("--base-url", help="AgentArts gateway URL")
    parser.add_argument("--path", help="API path")
    parser.add_argument("--api-key", help="Bearer token")
    parser.add_argument("--session-id", help="Default session ID")
    parser.add_argument("--user-identity", help="Target user identity")
    parser.add_argument("--greeting", help="Fixed greeting message")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Build config from --config or individual args
    if args.config:
        config_path = Path(args.config)
        if config_path.is_file():
            config = json.loads(config_path.read_text(encoding="utf-8"))
        else:
            config = json.loads(args.config)
    else:
        config = {}
        if args.name:
            config["name"] = args.name
        if args.description:
            config["description"] = args.description
        if args.triggers:
            config["triggers"] = args.triggers
        if args.base_url:
            config["base_url"] = args.base_url
        if args.path:
            config["path"] = args.path
        if args.api_key:
            config["api_key"] = args.api_key
        if args.session_id:
            config["session_id"] = args.session_id
        if args.user_identity:
            config["user_identity"] = args.user_identity
        if args.greeting:
            config["greeting"] = args.greeting

    try:
        skill_dir = generate_skill(config, output_dir=args.output_dir)
        print(f"\n[success] Skill generated at: {skill_dir}")
        return 0
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[error] Generation failed: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
