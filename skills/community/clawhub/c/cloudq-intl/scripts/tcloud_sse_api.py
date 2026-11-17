#!/usr/bin/env python3
"""
腾讯云智能顾问 CloudQ SSE 流式调用脚本

通过 TC3-HMAC-SHA256 签名调用 CloudQ 对话接口。
国际站仅支持 AK/SK 环境变量鉴权，统一使用 CloudQChatCompletions 接口。

支持同步（SSE 流式）和异步两种对话模式：
    - 同步（Async=false，默认）：SSE 流式返回，连接保持到对话结束
    - 异步（Async=true）：立即返回 accepted 帧，通过 DescribeCloudQAsyncTask 轮询结果

接口固定参数：
    service:  advisor
    host:     advisor.ai.tencentcloudapi.com
    action:   CloudQChatCompletions
    version:  2020-07-21

请求格式：
    {"SessionID":"<uuid>","Question":"...","Source":"<platform>","Async":false}
    异步模式: {"SessionID":"<uuid>","Question":"...","Source":"<platform>","Async":true}

响应格式（SSE 大驼峰字段）：
    event:<chat_id>
    data:{"SessionId":"...","ChatId":"...","Event":"content","Content":"...","IsFinal":false}

    异步 accepted 帧：
    event: accepted
    data:{"ChatId":"<异步任务ID>","SessionId":"<会话ID>","Content":"任务已受理..."}

纯 Python 标准库实现，无外部依赖。

会话管理：
    SessionID 必填模式：
    - 调用方在首次调用前通过 Python 生成 UUID：python3 -c "import uuid; print(uuid.uuid4())"
    - 每次调用必须通过 --session-id 传入
    - 同一会话使用相同 session_id，新会话生成新 UUID
    - 不同会话使用不同 session_id，支持多会话并行

用法 (命令行):
    # 同步模式（默认）
    python3 tcloud_sse_api.py <question> --source <platform> --session-id <uuid>
    # 异步模式
    python3 tcloud_sse_api.py <question> --source <platform> --session-id <uuid> --async

示例:
    python3 tcloud_sse_api.py '列出架构图' --source codebuddy --session-id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    python3 tcloud_sse_api.py '详细说说' --source codebuddy --session-id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

兼容旧用法（仍支持位置参数传入 session_id，但不推荐）:
    python3 tcloud_sse_api.py '列出架构图' <session_id> [source]

作为模块导入:
    from tcloud_sse_api import call_sse_api, generate_session_id
    session_id = generate_session_id()
    result = call_sse_api(
        question="列出架构图",
        session_id=session_id,
        on_event=lambda e: print(e["data"].get("Content", ""), end="", flush=True),
    )
    # result["data"]["session_id"] 可用于后续调用

鉴权方式:
    环境变量 AK/SK（国际站唯一支持方式）
        TENCENTCLOUD_SECRET_ID  - 腾讯云 SecretId
        TENCENTCLOUD_SECRET_KEY - 腾讯云 SecretKey
        TENCENTCLOUD_TOKEN      - 临时密钥 Token（可选）

输出格式（统一 JSON）:
    成功: {"success": true, "action": "...", "data": {...}, "requestId": "..."}
    失败: {"success": false, "action": "...", "error": {...}, "requestId": "..."}
"""

import hashlib
import hmac
import json
import os
import ssl
import sys
import time
import uuid
from datetime import datetime, timezone
import urllib.request
from urllib.request import Request
from urllib.error import URLError, HTTPError

from i18n import T

# ---------------------------------------------------------------------------
# 固定参数
# ---------------------------------------------------------------------------
SERVICE = "advisor"
HOST = "advisor.ai.tencentcloudapi.com"
ACTION = "CloudQChatCompletions"             # 统一接口（国际站 AK/SK）
ACTION_CANCEL_CHAT = "CancelCloudQChat"      # 取消同步 SSE 编排
VERSION = "2020-07-21"


# ---------------------------------------------------------------------------
# 会话管理
# ---------------------------------------------------------------------------


def generate_session_id() -> str:
    """
    生成新的 SessionID（UUID v4）。

    Returns:
        str: UUID v4 格式的 SessionID
    """
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# 内部工具函数
# ---------------------------------------------------------------------------

def _get_ssl_context():
    """获取 SSL 上下文，兼容各平台 CA 证书差异"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        # certifi 不可用时降级到系统默认 CA（Windows/Linux 系统 CA 通常可用）
        return ssl.create_default_context()


def _sign_tc3(key: bytes, msg: str) -> bytes:
    """TC3 HMAC-SHA256 签名辅助函数"""
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _make_error(action: str, code: str, message: str, request_id: str = "") -> dict:
    """构造统一错误结果"""
    return {
        "success": False,
        "action": action,
        "error": {"code": code, "message": message},
        "requestId": request_id,
    }


def _make_success(action: str, data: dict, request_id: str) -> dict:
    """构造统一成功结果"""
    return {
        "success": True,
        "action": action,
        "data": data,
        "requestId": request_id,
    }


# ---------------------------------------------------------------------------
# SSE 行解析
# ---------------------------------------------------------------------------

def parse_sse_line(line: str):
    """
    解析单行 SSE 数据。

    Returns:
        dict | None:
            - id 行:               {"type": "id", "value": "..."}
            - event 行:            {"event": "<value>"}
            - data 行(JSON 有效):  {"event": "data", "data": {...}}
            - data 行(JSON 无效):  {"event": "data", "raw": "..."}
            - 空行/注释行:          None
    """
    if not line or line.startswith(":"):
        return None

    if line.startswith("id:"):
        return {"type": "id", "value": line[3:].strip()}

    if line.startswith("data:"):
        payload = line[5:].lstrip()
        try:
            return {"event": "data", "data": json.loads(payload)}
        except (json.JSONDecodeError, ValueError):
            return {"event": "data", "raw": payload}

    if line.startswith("event:"):
        value = line[6:].strip()
        return {"event": value}

    return None


# ---------------------------------------------------------------------------
# SSE 流式 API 调用
# ---------------------------------------------------------------------------

def call_sse_api(question: str, session_id: str,
                 secret_id: str = None, secret_key: str = None,
                 token: str = None, region: str = "ap-singapore",
                 source: str = "", on_event=None,
                 async_mode: bool = True) -> dict:
    """
    调用 CloudQ SSE 流式 API（统一使用 CloudQChatCompletions）。

    默认异步模式：立即返回 accepted 帧，连接关闭，
    后续通过 DescribeCloudQAsyncTask 轮询结果。
    设置 async_mode=False 可切回同步 SSE 流式模式（不推荐，客户端有 60s 超时风险）。

    Args:
        question:   用户问题
        session_id: 会话 ID（同一对话必须保持不变）
        secret_id:  SecretId，不传则自动获取
        secret_key: SecretKey，不传则自动获取
        token:      临时密钥 Token，不传则自动获取
        region:     地域字符串，国际站固定 ap-singapore
        source:     调用来源平台标识（不区分大小写），如 codebuddy、openclaw 等
        on_event:   回调函数（异步模式下 accepted 帧后即返回，回调不会被调用）
        async_mode: 是否异步模式，默认 True（推荐，避免客户端超时）

    Returns:
        dict: 统一格式的结果字典
            data 含 chat_id, session_id, content, is_accepted
    """
    # ---- 凭证获取（国际站仅 AK/SK 环境变量）----
    if secret_id and secret_key:
        # 显式传入凭证
        token = token or os.environ.get("TENCENTCLOUD_TOKEN", "")
    else:
        # 通过 credential_manager 统一获取
        try:
            from credential_manager import get_credential, CredentialNotFoundError
            cred = get_credential()
            secret_id = cred["secretId"]
            secret_key = cred["secretKey"]
            token = cred.get("token", "")
        except ImportError:
            # credential_manager 不可用，回退到环境变量
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
            token = os.environ.get("TENCENTCLOUD_TOKEN", "")
        except CredentialNotFoundError:
            return _make_error(
                ACTION, "NeedAuth",
                T("未找到凭证，请配置 AK/SK 环境变量。")
            )
        except Exception as e:
            return _make_error(
                ACTION, "NeedAuth", str(e)
            )

    if not secret_id or not secret_key:
        return _make_error(
            ACTION, "MissingCredentials",
            T("未配置凭证。请配置 AK/SK 环境变量。\n"
              "密钥获取: https://console.tencentcloud.com/cam/capi")
        )

    # 统一使用 CloudQChatCompletions 接口
    action = ACTION

    payload = {"Question": question, "SessionID": session_id}
    if async_mode:
        payload["Async"] = True
    # Source 字段统一发送
    if source:
        payload["Source"] = source
    payload_str = json.dumps(payload, separators=(",", ":"))

    # ---- TC3-HMAC-SHA256 签名 ----
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    hashed_payload = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    canonical_request = (
        f"POST\n/\n\n"
        f"content-type:application/json\n"
        f"host:{HOST}\n"
        f"x-tc-action:{action.lower()}\n\n"
        f"content-type;host;x-tc-action\n"
        f"{hashed_payload}"
    )

    credential_scope = f"{date}/{SERVICE}/tc3_request"
    hashed_cr = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_cr}"

    secret_date = _sign_tc3(f"TC3{secret_key}".encode("utf-8"), date)
    secret_service = _sign_tc3(secret_date, SERVICE)
    secret_signing = _sign_tc3(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    authorization = (
        f"{algorithm} "
        f"Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders=content-type;host;x-tc-action, "
        f"Signature={signature}"
    )

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Host": HOST,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": VERSION,
        "X-TC-Region": region,
    }
    if token:
        headers["X-TC-Token"] = token

    req = Request(
        f"https://{HOST}", data=payload_str.encode("utf-8"),
        headers=headers, method="POST",
    )

    # ---- 发送请求并解析 SSE 流 ----
    try:
        ctx = _get_ssl_context()
        resp = urllib.request.urlopen(req, context=ctx, timeout=1200)
    except HTTPError as e:
        return _handle_http_error(e, action)
    except URLError as e:
        return _make_error(
            action, "NetworkError",
            T("网络连接失败，请检查网络和域名 {host} 是否可达: {reason}",
              host=HOST, reason=e.reason)
        )
    except Exception as e:
        return _make_error(action, "NetworkError", T("请求异常: {error}", error=e))

    # 检查响应类型：腾讯云 API 可能返回 HTTP 200 + JSON 错误体（非 SSE 流）
    content_type = resp.headers.get("Content-Type", "")
    if "text/event-stream" not in content_type:
        return _handle_non_sse_response(resp, action)

    return _parse_sse_stream(resp, on_event, action, session_id, async_mode)


def _parse_sse_stream(resp, on_event, action: str,
                      session_id: str = "", async_mode: bool = True) -> dict:
    """
    解析 CloudQ SSE 流并构建结果。

    响应字段为大驼峰：Content, IsFinal, ChatId, SessionId, Event, Error
    输出统一为小写字段名的结果 dict。

    SSE 流中可能包含错误事件（如权限不足），Error 字段格式：
      {"Code": "UnauthorizedOperation", "Message": "..."}

    异步模式（async_mode=True）：
      解析 Event="accepted" 的 data 帧，提取 ChatID + SessionID 后立即返回。
    """
    content_parts = []
    last_event_data = {}
    request_id = ""

    for raw_line in resp:
        line = raw_line.decode("utf-8").rstrip("\r\n")

        parsed = parse_sse_line(line)
        if parsed is None:
            continue

        if parsed.get("event") != "data":
            continue

        data = parsed.get("data")
        if not isinstance(data, dict):
            continue

        # ---- 异步模式：处理 Event="accepted" 帧 ----
        if async_mode and data.get("Event") == "accepted":
            chat_id = data.get("ChatId", "")
            resp_session_id = data.get("SessionId", session_id)
            content = data.get("Content", "")
            return _make_success(action, {
                "chat_id": chat_id,
                "session_id": resp_session_id,
                "content": content,
                "is_accepted": True,
            }, chat_id)

        if not request_id:
            request_id = data.get("ChatId", "")

        # 检查 SSE 流中的错误事件
        error_info = data.get("Error")
        if isinstance(error_info, dict) and error_info.get("Code"):
            return _make_error(
                action, error_info.get("Code", "Unknown"),
                error_info.get("Message", T("未知错误")),
                request_id,
            )

        if on_event:
            on_event(parsed)

        content = data.get("Content", "")
        if content:
            content_parts.append(content)
        last_event_data = data

        # IsFinal=True 表示后端已推送完毕，主动断开不再等待
        if data.get("IsFinal") is True:
            break

    raw_content = "".join(content_parts)
    # 国际站：无免密登录机制（中文站专属功能），后端内容原样输出、不做任何替换/追加
    processed = raw_content

    merged = {
        "session_id": session_id,
        "content": processed,
        "is_final": last_event_data.get("IsFinal", True),
    }

    return _make_success(action, merged, request_id)




def _handle_http_error(e: HTTPError, action: str) -> dict:
    """处理 HTTP 错误响应"""
    try:
        body = e.read().decode("utf-8")
        data = json.loads(body)
        response = data.get("Response", {})
        error = response.get("Error", {})
        if error:
            return _make_error(
                action, error.get("Code", "HTTPError"),
                error.get("Message", f"HTTP {e.code}"),
                response.get("RequestId", ""),
            )
    except Exception:
        pass
    return _make_error(
        action, "HTTPError",
        T("HTTP 请求失败 (状态码 {code}): {reason}", code=e.code, reason=e.reason)
    )


def _handle_non_sse_response(resp, action: str) -> dict:
    """处理非 SSE 响应（HTTP 200 但 Content-Type 非 event-stream，通常是 JSON 错误体）"""
    try:
        body = resp.read().decode("utf-8")
        data = json.loads(body)
        response = data.get("Response", {})
        error = response.get("Error", {})
        if error:
            return _make_error(
                action, error.get("Code", "Unknown"),
                error.get("Message", T("未知错误")),
                response.get("RequestId", ""),
            )
        # 非错误但也非 SSE，返回原始数据
        return _make_success(action, response, response.get("RequestId", ""))
    except (json.JSONDecodeError, ValueError):
        return _make_error(
            action, "InvalidResponse",
            T("接口返回非 SSE 格式且无法解析为 JSON: {body}", body=body[:200])
        )
    except Exception as e:
        return _make_error(action, "InvalidResponse", T("解析响应失败: {error}", error=e))


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def _output_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _parse_args(args: list) -> dict:
    """解析命令行参数，支持 --source / --session-id 标志位。

    Returns:
        dict: {
            "question": str,
            "session_id": str | None,  # 传入时非 None
            "source": str,
        }
    """
    if not args:
        return {}

    result = {
        "question": "",
        "session_id": None,
        "source": "",
    }

    # 第一个非标志位参数为 question
    positional = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--source":
            if i + 1 < len(args):
                result["source"] = args[i + 1]
                i += 1
        elif arg.startswith("--source="):
            result["source"] = arg[len("--source="):]
        elif arg == "--session-id":
            if i + 1 < len(args):
                result["session_id"] = args[i + 1]
                i += 1
        elif arg.startswith("--session-id="):
            result["session_id"] = arg[len("--session-id="):]
        elif not result["question"]:
            result["question"] = arg
            positional.append(arg)
        else:
            positional.append(arg)
        i += 1

    # 兼容旧用法：位置参数第2个为 session_id，第3个为 source
    if len(positional) >= 2:
        result["session_id"] = positional[1] if positional[1] else None
    if len(positional) >= 3 and not result["source"]:
        result["source"] = positional[2]

    return result


def main():
    """命令行入口：python3 tcloud_sse_api.py <question> --source <platform> --session-id <uuid>"""
    # 锁定 stdout/stderr 为 UTF-8
    import io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parsed = _parse_args(sys.argv[1:])
    if not parsed or not parsed.get("question"):
        usage = T(
            "用法: python3 tcloud_sse_api.py <question> --source <platform> "
            "--session-id <uuid>"
        )
        print(_output_json(_make_error(ACTION, "MissingParameter", usage)))
        sys.exit(1)

    question = parsed["question"]
    source = parsed["source"]

    # ---- SessionID ----
    if not parsed["session_id"]:
        print(_output_json(_make_error(
            ACTION, "MissingParameter",
            T("缺少必填参数 --session-id。"
              "请通过 SID=$(python3 -c 'import uuid;print(uuid.uuid4())') 生成后传入。")
        )))
        sys.exit(1)
    session_id = parsed["session_id"]

    # 回显 session_id 到 stderr，供调用方追问时复用
    print(f"[session] {session_id}", file=sys.stderr, flush=True)

    result = call_sse_api(question, session_id, source=source)

    print(_output_json(result))
    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
