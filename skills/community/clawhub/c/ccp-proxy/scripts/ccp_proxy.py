#!/usr/bin/env python3
"""
CCP 本地反向代理服务（可移植版）
将本地 OpenAI 兼容接口转发到 https://ptest.cmccsim.com/ccp/v1
服务以守护进程方式常驻运行，不随会话关闭。

用法:
  python3 ccp_proxy.py start             # 启动服务（幂等，已在运行则跳过）
  python3 ccp_proxy.py status            # 查看运行状态
  python3 ccp_proxy.py stop              # 停止服务
  python3 ccp_proxy.py test              # 连通性测试（key 自动从 models.json 读取）
  python3 ccp_proxy.py test sk-xxx [model]   # 用指定 key（和模型）测试
  python3 ccp_proxy.py configure sk-xxx [model-id]  # 将模型（指向本地代理）写入 ~/.workbuddy/models.json，模型默认 qwen-3.5
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error

PORT = 8257
UPSTREAM = "https://ptest.cmccsim.com/ccp/v1"
MODELS_JSON = os.path.expanduser("~/.workbuddy/models.json")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(BASE_DIR, ".ccp_proxy.pid")
LOG_FILE = os.path.join(BASE_DIR, "ccp_proxy.log")
SERVER_FILE = os.path.join(BASE_DIR, "_server.py")

SERVER_CODE = r'''
# === 常驻代理服务（由 ccp_proxy.py 拉起，勿直接运行本段） ===
import http.server
import socketserver
import urllib.request
import urllib.error
import json

PORT = 8257
UPSTREAM = "https://ptest.cmccsim.com/ccp/v1"

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _proxy(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None
        # 本地 /v1/xxx 剥掉 /v1 前缀后拼到上游（上游 base 已含 /ccp/v1）
        path = self.path
        if path == "/v1":
            path = "/"
        elif path.startswith("/v1/"):
            path = path[3:]
        url = UPSTREAM + path

        req = urllib.request.Request(url, data=body, method=self.command)
        for h in ("Authorization", "Content-Type", "Accept", "User-Agent"):
            if self.headers.get(h):
                req.add_header(h, self.headers[h])

        try:
            resp = urllib.request.urlopen(req, timeout=600)
        except urllib.error.HTTPError as e:
            resp = e
        except Exception as e:
            payload = json.dumps({"error": {"message": str(e)}}).encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self.send_response(resp.status if hasattr(resp, "status") else resp.code)
        ct = resp.headers.get("Content-Type", "application/json")
        self.send_header("Content-Type", ct)
        self.send_header("Access-Control-Allow-Origin", "*")
        is_stream = "text/event-stream" in ct
        if is_stream:
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            # 流式转发：逐块读取并按 chunked 编码写出
            try:
                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(("%x\r\n" % len(chunk)).encode() + chunk + b"\r\n")
                    self.wfile.flush()
                self.wfile.write(b"0\r\n\r\n")
            except Exception:
                pass
        else:
            data = resp.read()
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    do_GET = _proxy
    do_POST = _proxy
    do_DELETE = _proxy
    do_PUT = _proxy
    do_OPTIONS = _proxy

    def log_message(self, fmt, *args):
        pass  # 静默访问日志，避免磁盘膨胀

class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == "__main__":
    print("ccp-proxy listening on 127.0.0.1:%d -> %s" % (PORT, UPSTREAM), flush=True)
    Server(("127.0.0.1", PORT), ProxyHandler).serve_forever()
'''

def make_model_entry(model_id, key):
    return {
        "id": model_id,
        "name": f"{model_id} (Local Proxy)",
        "vendor": "CMCC CCP",
        "url": f"http://127.0.0.1:{PORT}/v1/chat/completions",
        "apiKey": key,
        "supportsToolCall": True,
        "supportsImages": False,
        "supportsReasoning": False,
    }


def port_in_use():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def read_pid():
    try:
        with open(PID_FILE) as f:
            return int(f.read().strip())
    except Exception:
        return None


def get_configured_key():
    try:
        with open(MODELS_JSON) as f:
            for m in json.load(f):
                if m.get("id") == "qwen-3.5":
                    return m.get("apiKey")
    except Exception:
        pass
    return None


def cmd_start():
    if port_in_use():
        pid = read_pid()
        if pid and pid_alive(pid):
            print(f"[OK] 服务已在运行 PID={pid}，端口 {PORT}，无需重复启动")
        else:
            print(f"[WARN] 端口 {PORT} 被其他进程占用，请先 stop 或更换端口")
        return
    with open(SERVER_FILE, "w") as f:
        f.write(SERVER_CODE)
    with open(LOG_FILE, "a") as lf:
        proc = subprocess.Popen(
            [sys.executable, SERVER_FILE],
            stdout=lf, stderr=lf,
            start_new_session=True,  # 脱离会话，父进程退出后继续运行
        )
    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))
    for _ in range(30):
        if port_in_use():
            print(f"[OK] 服务已启动 PID={proc.pid}")
            print(f"     本地地址: http://127.0.0.1:{PORT}/v1/chat/completions")
            print(f"     上游: {UPSTREAM}")
            print(f"     日志: {LOG_FILE}")
            return
        time.sleep(0.2)
    print(f"[FAIL] 端口 {PORT} 未就绪，请查看日志: tail -20 {LOG_FILE}")


def cmd_status():
    pid = read_pid()
    running = bool(pid and pid_alive(pid) and port_in_use())
    if running:
        print(f"[RUNNING] PID={pid} 端口={PORT} 上游={UPSTREAM}")
    else:
        print("[STOPPED] 服务未运行")


def cmd_stop():
    pid = read_pid()
    if pid and pid_alive(pid):
        os.kill(pid, 15)
        for _ in range(20):
            if not pid_alive(pid):
                break
            time.sleep(0.1)
        if pid_alive(pid):
            os.kill(pid, 9)
        print(f"[OK] 已停止 PID={pid}")
    else:
        print("[INFO] 服务未在运行")
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def cmd_test():
    args = sys.argv[2:]
    key = None
    model = "qwen-3.5"
    for a in args:
        if a.startswith("sk-"):
            key = a
        elif a and not a.startswith("-"):
            model = a
    if not key:
        key = get_configured_key()
    if not key:
        print("[FAIL] 未提供 key 且 models.json 中未配置 qwen-3.5。用法: ccp_proxy.py test sk-xxx [model]")
        return
    url = f"http://127.0.0.1:{PORT}/v1/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 8,
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            head = resp.read(300).decode(errors="replace")
            print(f"[OK] HTTP {resp.status}，代理链路通畅，响应片段: {head[:200]}")
    except urllib.error.HTTPError as e:
        print(f"[WARN] 上游返回 HTTP {e.code}（代理本身工作正常，可能是上游或 key 问题）: {e.read(200).decode(errors='replace')}")
    except Exception as e:
        print(f"[FAIL] 代理不可达: {e}")


def cmd_configure(key=None, model=None):
    args = sys.argv[2:]
    key = key or next((a for a in args if a.startswith("sk-")), "")
    model = model or next((a for a in args if not a.startswith("sk-") and not a.startswith("-")), "")
    if not key.startswith("sk-"):
        print("[FAIL] 请提供有效的 API Key：python3 ccp_proxy.py configure sk-xxx [model-id]")
        return
    if not model:
        model = "qwen-3.5"
    try:
        with open(MODELS_JSON) as f:
            models = json.load(f)
    except FileNotFoundError:
        models = []
    except json.JSONDecodeError:
        print("[FAIL] models.json 已存在但不是合法 JSON，请手工检查后再试")
        return
    models = [m for m in models if m.get("id") != model]
    entry = make_model_entry(model, key)
    models.append(entry)
    with open(MODELS_JSON, "w") as f:
        json.dump(models, f, ensure_ascii=False, indent=2)
    print(f"[OK] 已写入 {MODELS_JSON}")
    print(f"     {model} -> http://127.0.0.1:{PORT}/v1/chat/completions")
    print(f"     重启 WorkBuddy 后在模型选择器中切换到 {model} (Local Proxy)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    {"start": cmd_start, "status": cmd_status, "stop": cmd_stop,
     "test": cmd_test, "configure": cmd_configure}.get(cmd, cmd_status)()
