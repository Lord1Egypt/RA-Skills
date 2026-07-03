#!/usr/bin/env python3
"""
MCP Streamable HTTP 客户端
通过 Streamable HTTP 方式调用 MCP 服务
支持会话初始化与保持、嵌套响应解析
"""

import sys
import os
import json
import argparse
import uuid
import urllib.request
import urllib.error

# =============================================================================
# Windows 控制台 UTF-8 编码修复（必须在任何 print 输出之前执行）
# =============================================================================
if sys.platform == 'win32':
    import ctypes
    import msvcrt

    # 方法1：切换控制台代码页到 UTF-8 (65001)
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)   # 设置控制台输出代码页为 UTF-8
        kernel32.SetConsoleCP(65001)         # 设置控制台输入代码页为 UTF-8
    except Exception:
        pass

    # 方法2：设置 MSVC 运行时以 UTF-8 模式处理文件 I/O
    try:
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)  # 二进制模式，避免 CR/LF 转换
        msvcrt.setmode(sys.stderr.fileno(), os.O_BINARY)
    except Exception:
        pass

    # 方法3：将 PYTHONIOENCODING 强制为 UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    # 方法4：重新配置 stdout/stderr 为 UTF-8 无 BOM
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        # 如果 reconfigure 失败，降级处理：替换 write 方法
        class _Utf8Writer:
            def __init__(self, file_obj):
                self._file = file_obj
            def write(self, s):
                if isinstance(s, bytes):
                    s = s.decode('utf-8', errors='replace')
                self._file.write(s)
                self._file.flush()
            def __getattr__(self, name):
                return getattr(self._file, name)
        sys.stdout = _Utf8Writer(sys.stdout)
        sys.stderr = _Utf8Writer(sys.stderr)

    # 方法5：打印 BOM 让部分 Windows 终端识别 UTF-8（可选，注释掉避免干扰 JSON 输出）
    # sys.stdout.write('\ufeff')

    # 方法6：调用前切换到 UTF-8 代码页（通过启动参数也行，这里用环境变量兜底）
    # 已在方法3中通过 PYTHONIOENCODING 覆盖

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "skill-config.json")
SESSION_FILE = os.path.join(SCRIPT_DIR, ".mcp_session_id")


def load_config():
    """从 skill-config.json 读取配置"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_stoken():
    """从 skill-config.json 读取 sToken"""
    return load_config().get("sToken", "")


def load_server_url():
    """从 skill-config.json 读取 mcpServerUrl"""
    return load_config().get("mcpServerUrl", "")


def build_jsonrpc(method, params=None, req_id=None):
    """构建 JSON-RPC 2.0 请求体"""
    if req_id is None:
        req_id = str(uuid.uuid4())[:8]
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
    }
    if params is not None:
        payload["params"] = params
    return payload


def read_sse_response(resp):
    """
    从 SSE 流式响应中逐行读取，直到获得第一条完整 JSON 消息。
    不等待连接关闭（EOF），避免超时。
    """
    json_body = None
    while True:
        line = resp.readline().decode("utf-8", errors="replace")
        if not line:
            break
        line = line.strip()
        if line.startswith("data:"):
            data_part = line[5:].strip()
            if data_part and data_part.startswith("{"):
                json_body = data_part
                break
    return json_body or ""


def send_request(url, payload, stoken, session_id=None):
    """
    发送 HTTP 请求。
    返回 (body_text, new_session_id)
    body_text 是已解析 SSE 后的 JSON 字符串。
    """
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if stoken:
        headers["sToken"] = stoken
    if session_id:
        headers["Mcp-Session-Id"] = session_id

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            new_sid = resp.headers.get("Mcp-Session-Id")
            content_type = resp.headers.get("Content-Type", "")

            if "text/event-stream" in content_type:
                body = read_sse_response(resp)
                return body, new_sid
            else:
                raw_body = resp.read().decode("utf-8")
                return raw_body, new_sid
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(json.dumps({"error": f"HTTP {e.code}: {e.reason}", "detail": error_body}),
              file=sys.stderr, flush=True)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": str(e.reason)}), file=sys.stderr, flush=True)
        sys.exit(1)


def _save_session_id(session_id):
    """保存 session ID 到本地文件"""
    if session_id:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            f.write(session_id)


def _load_session_id():
    """从本地文件读取 session ID"""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            sid = f.read().strip()
            if sid:
                return sid
    return None


def _clear_session_id():
    """清除本地 session ID 文件"""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except OSError:
            pass


def ensure_session(url, stoken):
    """确保存在有效 session，返回 session_id"""
    session_id = _load_session_id()
    if session_id:
        payload = build_jsonrpc("tools/list")
        try:
            body, new_sid = send_request(url, payload, stoken, session_id)
            resp = json.loads(body)
            if "result" in resp:
                if new_sid:
                    _save_session_id(new_sid)
                    return new_sid
                return session_id
            _clear_session_id()
        except (SystemExit, json.JSONDecodeError):
            _clear_session_id()

    # 初始化新 session
    _clear_session_id()
    init_payload = build_jsonrpc("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "sjzl-ai-okc-client", "version": "1.0.0"}
    })
    body, new_sid = send_request(url, init_payload, stoken)
    if new_sid:
        _save_session_id(new_sid)
        init_notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        send_request(url, init_notif, stoken, new_sid)
        return new_sid
    return None


def unwrap_mcp_response(raw_result):
    """
    解析 MCP 工具调用的嵌套响应。
    MCP 返回格式: {"result": {"content": [{"type": "text", "text": "..."}]}, ...}
    提取内层 text 并解析为 JSON。
    """
    if not isinstance(raw_result, dict):
        return raw_result
    content_list = raw_result.get("content", [])
    if content_list and isinstance(content_list[0], dict) and "text" in content_list[0]:
        text_content = content_list[0]["text"]
        if raw_result.get("isError"):
            return {"code": 500, "msg": text_content, "result": None}
        try:
            return json.loads(text_content)
        except json.JSONDecodeError:
            return {"code": 200, "msg": "", "result": text_content}
    return raw_result


def resolve_server_url(arg_url):
    """优先使用 --server-url 参数，否则读取 skill-config.json"""
    if arg_url:
        url = arg_url
        if not url.endswith("/"):
            url += "/"
        return url
    url = load_server_url()
    if not url:
        print(json.dumps({"error": "未配置 mcpServerUrl，请在 skill-config.json 中设置或通过 --server-url 参数传入"}),
              file=sys.stderr, flush=True)
        sys.exit(1)
    if not url.endswith("/"):
        url += "/"
    return url


def cmd_list(args):
    """列出 MCP 服务可用工具"""
    url = resolve_server_url(args.server_url)
    stoken = load_stoken()
    session_id = ensure_session(url, stoken)
    payload = build_jsonrpc("tools/list")
    body, new_sid = send_request(url, payload, stoken, session_id)
    if new_sid:
        _save_session_id(new_sid)
    print(body, flush=True)


def cmd_call(args):
    """调用 MCP 工具"""
    url = resolve_server_url(args.server_url)
    stoken = load_stoken()
    session_id = ensure_session(url, stoken)

    tool_name = args.tool_name
    params = {}
    if args.params_file:
        with open(args.params_file, "r", encoding="utf-8") as f:
            params = json.load(f)
    elif args.params:
        params_str = args.params
        # 支持 @file.json 语法，避免 PowerShell 转义问题
        if params_str.startswith("@") and len(params_str) > 1:
            with open(params_str[1:], "r", encoding="utf-8") as f:
                params = json.load(f)
        else:
            params = json.loads(params_str)

    payload = build_jsonrpc("tools/call", {
        "name": tool_name,
        "arguments": params,
    })
    body, new_sid = send_request(url, payload, stoken, session_id)
    if new_sid:
        _save_session_id(new_sid)
    print(body, flush=True)


def main():
    parser = argparse.ArgumentParser(description="MCP Streamable HTTP Client")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    list_parser = subparsers.add_parser("list", help="列出可用工具")
    list_parser.add_argument("--server-url", dest="server_url", default=None,
                             help="MCP 服务地址（可选，默认读取 skill-config.json）")

    call_parser = subparsers.add_parser("call", help="调用工具")
    call_parser.add_argument("tool_name", help="工具名称")
    call_parser.add_argument("--server-url", dest="server_url", default=None,
                             help="MCP 服务地址（可选，默认读取 skill-config.json）")
    call_parser.add_argument("--params", help="JSON 格式参数", default=None)
    call_parser.add_argument("--params-file", dest="params_file", help="JSON 参数文件路径", default=None)

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "call":
        cmd_call(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
