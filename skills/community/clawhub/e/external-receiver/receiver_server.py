#!/usr/bin/env python3
"""
External Receiver HTTP Server
接收外部文件 / 消息 → 转发到 OpenClaw 会话

用法：
    python3 receiver_server.py [--port 8080] [--host 0.0.0.0] [--secret KEY]
"""

import os
import sys
import json
import cgi
import traceback
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs

# ─── 配置 ───────────────────────────────────────
RECEIVER_HOST = os.getenv("RECEIVER_HOST", "0.0.0.0")
RECEIVER_PORT = int(os.getenv("RECEIVER_PORT", "8080"))
RECEIVER_DIR = Path(os.getenv("RECEIVER_DIR",
    os.path.join(os.path.dirname(__file__), "../received")))
RECEIVER_SECRET = os.getenv("RECEIVER_SECRET", "")  # 可选密钥

RECEIVER_DIR.mkdir(parents=True, exist_ok=True)

# ─── 日志 ───────────────────────────────────────
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# ─── OpenClaw 消息推送 ──────────────────────────
def push_to_openclaw(text: str):
    """
    把消息/文件通知写入队列文件，OpenClaw Agent 会在下次心跳时读取并显示。
    同时尝试通过 gateway WebSocket 推送（如果可用）。
    """
    queue_file = Path.home() / ".openclaw" / "workspace" / "received" / "message_queue.jsonl"
    queue_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "time": datetime.now().isoformat(),
        "text": text,
    }
    queue_file.append_text(json.dumps(entry, ensure_ascii=False) + "\n")
    log(f"消息已写入队列: {queue_file}")

    # 同时尝试 WebSocket 推送（gateway websocket）
    _try_ws_push(text)


def _try_ws_push(text: str):
    """
    尝试通过 WebSocket 向 OpenClaw gateway 推送消息
    （如果 websocket-client 库可用）
    """
    try:
        import urllib.request, urllib.error
        import json as _json

        # 读取 gateway 配置
        cfg_path = Path.home() / ".openclaw" / "openclaw.json"
        if not cfg_path.exists():
            return
        cfg = _json.loads(cfg_path.read_text())
        gateway_cfg = cfg.get("gateway", {})
        token = gateway_cfg.get("auth", {}).get("token", "")
        port = gateway_cfg.get("port", 18789)

        # gateway 的 WebSocket URL
        ws_url = f"ws://127.0.0.1:{port}"

        payload = _json.dumps({
            "jsonrpc": "2.0",
            "method": "sessions.send",
            "params": {
                "text": text,
            },
            "id": 1
        }).encode("utf-8")

        # 尝试 WS 连接（不阻塞主线程，超时 2s）
        import threading
        def _ws_thread():
            try:
                import websocket
                ws = websocket.create_connection(ws_url, timeout=2,
                    header=[f"Authorization: Bearer {token}"] if token else [])
                ws.send(payload)
                ws.close()
                log("WebSocket 推送成功")
            except Exception:
                pass  # 静默失败，回退到文件队列

        t = threading.Thread(target=_ws_thread, daemon=True)
        t.start()
        t.join(timeout=3)

    except ImportError:
        # websocket-client 未安装，跳过
        pass
    except Exception as e:
        log(f"WS 推送尝试失败: {e}")


# ─── 通知构建 ───────────────────────────────────
def build_file_notif(filename: str, size: int, path: str) -> str:
    size_str = f"{size:,}B" if size < 1024 else f"{size/1024:.1f}KB" if size < 1048576 else f"{size/1048576:.1f}MB"
    return (
        f"📎 收到外部文件\n"
        f"文件名: `{filename}`\n"
        f"大小: {size_str}\n"
        f"路径: `{path}`\n"
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


def build_message_notif(text: str, source: str = "外部") -> str:
    return (
        f"📥 收到外部消息 ({source})\n"
        f"内容: {text}\n"
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )


# ─── HTTP Handler ────────────────────────────────
class ReceiverHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        log(f"{self.address_string()} - {format % args}")

    # ── 安全检查 ──────────────────────────────
    def _check_secret(self) -> bool:
        if not RECEIVER_SECRET:
            return True
        auth = self.headers.get("Authorization", "")
        return auth == f"Bearer {RECEIVER_SECRET}"

    def _json_response(self, data: dict, status=200):
        body = json.dumps(data, ensure_ascii=False)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _ok(self, **kwargs):
        self._json_response({"ok": True, **kwargs})

    def _error(self, msg: str, status=400):
        self._json_response({"ok": False, "error": msg}, status)

    # ── GET / ─────────────────────────────────
    def do_GET(self):
        if self.path == "/health":
            self._ok(status="running", time=datetime.now().isoformat())
            return

        if self.path.startswith("/download/"):
            filename = os.path.basename(self.path[10:])
            filepath = RECEIVER_DIR / filename
            if not filepath.is_file():
                self._error("文件不存在", 404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
            return

        # 状态页
        files = list(RECEIVER_DIR.iterdir())
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>External Receiver</title></head>
<body>
<h1>🌐 External Receiver</h1>
<p>状态: ✅ 运行中</p>
<p>时间: {datetime.now().isoformat()}</p>
<p>文件数: {len(files)}</p>
<p>端口: {RECEIVER_PORT}</p>
<h2>最近文件</h2><ul>
{"".join(f'<li><a href="/download/{f.name}">{f.name}</a> ({f.stat().st_size}B)</li>' for f in files[:10])}
</ul>
<h2>Endpoints</h2>
<ul>
<li>GET/POST /upload - 上传文件</li>
<li>POST /message - 发送文本</li>
<li>POST /webhook - JSON Webhook</li>
</ul>
</body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    # ── POST /upload ───────────────────────────
    def do_POST(self):
        if not self._check_secret():
            self._error("未授权", 401)
            return

        if self.path == "/upload":
            self._handle_upload()
        elif self.path == "/message":
            self._handle_message()
        elif self.path == "/webhook":
            self._handle_webhook()
        else:
            self._error("未知路径", 404)

    def _handle_upload(self):
        try:
            content_type = self.headers.get("Content-Type", "")
            if "multipart/form-data" not in content_type:
                self._error("需要 multipart/form-data")
                return

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={"REQUEST_METHOD": "POST"}
            )

            if "file" not in form:
                self._error("未找到文件字段 'file'")
                return

            file_item = form["file"]
            if not file_item.filename:
                self._error("文件名为空")
                return

            filename = os.path.basename(file_item.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = f"{timestamp}_{filename}"
            filepath = RECEIVER_DIR / safe_name

            data = file_item.file.read()
            filepath.write_bytes(data)
            size = len(data)

            log(f"收到文件: {filename} -> {safe_name} ({size}B)")

            # 推送到 OpenClaw
            notif = build_file_notif(filename, size, str(filepath))
            push_to_openclaw(notif)

            self._ok(filename=safe_name, size=size, path=str(filepath))

        except Exception as e:
            log(f"上传出错: {e}\n{traceback.format_exc()}")
            self._error(str(e), 500)

    def _handle_message(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")

            # 支持 form-encoded 和 JSON
            content_type = self.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = json.loads(body)
                text = data.get("text", data.get("message", ""))
            else:
                text = parse_qs(body).get("text", [parse_qs(body).get("message", [""])[0]])[0]

            if not text:
                self._error("text 为空")
                return

            log(f"收到消息: {text[:100]}")
            notif = build_message_notif(text, "外部")
            push_to_openclaw(notif)

            self._ok(message=text[:100])

        except Exception as e:
            log(f"消息处理出错: {e}\n{traceback.format_exc()}")
            self._error(str(e), 500)

    def _handle_webhook(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)

            log(f"收到 Webhook: {str(data)[:200]}")

            # 格式化输出
            lines = ["📡 收到 Webhook\n"]
            for k, v in data.items():
                lines.append(f"**{k}**: {v}")

            text = "\n".join(lines)
            push_to_openclaw(text)

            self._ok(data=data)

        except json.JSONDecodeError:
            self._error("Invalid JSON")
        except Exception as e:
            log(f"Webhook 处理出错: {e}\n{traceback.format_exc()}")
            self._error(str(e), 500)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()


# ─── 主程序 ────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(description="External Receiver HTTP Server")
    parser.add_argument("--host", default=RECEIVER_HOST, help="监听地址")
    parser.add_argument("--port", type=int, default=RECEIVER_PORT, help="监听端口")
    parser.add_argument("--secret", default=RECEIVER_SECRET, help="访问密钥")
    parser.add_argument("--dir", default=str(RECEIVER_DIR), help="文件存储目录")
    args = parser.parse_args()

    global RECEIVER_SECRET, RECEIVER_DIR
    if args.secret:
        RECEIVER_SECRET = args.secret
    if args.dir:
        RECEIVER_DIR = Path(args.dir)
    RECEIVER_DIR.mkdir(parents=True, exist_ok=True)

    addr = (args.host, args.port)
    server = HTTPServer(addr, ReceiverHandler)

    log(f"")
    log(f"🌐 External Receiver 启动")
    log(f"   监听: http://{args.host}:{args.port}")
    log(f"   文件目录: {RECEIVER_DIR}")
    if RECEIVER_SECRET:
        log(f"   密钥: ✅ 已设置")
    else:
        log(f"   密钥: ❌ 未设置（建议生产环境设置 --secret）")
    log(f"")
    log(f"端点:")
    log(f"  GET  /              状态页")
    log(f"  GET  /health        健康检查")
    log(f"  POST /upload        上传文件 (multipart/form-data, 字段名 'file')")
    log(f"  POST /message       发送文本 (form: text=xxx 或 JSON: {{'text':'xxx'}})")
    log(f"  POST /webhook       JSON Webhook")
    log(f"")
    log(f"按 Ctrl+C 停止")
    log(f"-" * 40)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("停止服务")
        server.shutdown()


if __name__ == "__main__":
    main()
