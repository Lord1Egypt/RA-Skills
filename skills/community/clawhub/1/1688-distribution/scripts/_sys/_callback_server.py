#!/usr/bin/env python3
"""
本地 AK 获取回调服务器

端点：
  GET  /callback      — 接收 1688 授权页面回调
  GET  /healthCheck   — 健康检查
  POST /api/save-ak   — 保存 AK
  POST /api/shutdown   — 通知关闭
"""
from __future__ import annotations

import json
import logging
import os
import socket
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

from scripts._sys._const import (
    CALLBACK_HOST,
    CALLBACK_BIND_ADDRESS,
    CALLBACK_PORT_START,
    CALLBACK_PORT_RETRIES,
)

logger = logging.getLogger(__name__)

ERROR_HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>获取失败</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
display:flex;justify-content:center;align-items:center;min-height:100vh;background:#fef2f2}
.card{text-align:center;padding:3rem 2.5rem;border-radius:1rem;background:#fff;
box-shadow:0 4px 24px rgba(0,0,0,.08);max-width:480px;width:90%}
.icon{font-size:3rem;margin-bottom:1rem}
h1{color:#dc2626;font-size:1.5rem;margin-bottom:0.75rem}
p{color:#666;line-height:1.6;margin-bottom:0.5rem}
.error-code{font-family:monospace;background:#fee2e2;color:#991b1b;
padding:0.25rem 0.5rem;border-radius:0.25rem;font-size:0.875rem}
.footer{margin-top:1.5rem;font-size:0.75rem;color:#999}
</style></head>
<body><div class="card">
<div class="icon">&#10008;</div>
<h1>获取失败</h1>
<p>{error_message}</p>
<p class="error-code">{error_code}</p>
<div class="footer">此页面仅运行在您的本地设备上 (localhost)</div>
</div></body></html>"""


class _FastBindMixin:
    """跳过 HTTPServer.server_bind() 中的 socket.getfqdn() 调用。
    默认实现对绑定地址做反向 DNS 查询，在某些网络环境下会超时 5 秒。"""
    def server_bind(self):
        import socketserver
        socketserver.TCPServer.server_bind(self)
        host, port = self.server_address[:2]
        self.server_name = socket.gethostname()
        self.server_port = port


class _ThreadingHTTPServer(_FastBindMixin, ThreadingMixIn, HTTPServer):
    """支持并发请求的 HTTP 服务器（IPv4）"""
    allow_reuse_address = True
    daemon_threads = True


class _ThreadingHTTPServerIPv6(_FastBindMixin, ThreadingMixIn, HTTPServer):
    """支持并发请求的 HTTP 服务器（IPv6）"""
    address_family = socket.AF_INET6
    allow_reuse_address = True
    daemon_threads = True


class AKCallbackServer:
    """仅处理 AK 获取的本地回调服务器"""

    def __init__(self, state: str) -> None:
        self._state = state
        self._port: int = CALLBACK_PORT_START
        self._server: HTTPServer | None = None
        self._server_ipv6: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._thread_ipv6: threading.Thread | None = None
        self._done_event = threading.Event()
        self._success = False
        self._result: dict = {}

    @property
    def port(self) -> int:
        return self._port

    @property
    def success(self) -> bool:
        return self._success

    @property
    def result(self) -> dict:
        return self._result

    def start(self) -> None:
        handler = self._create_handler()
        port = self._bind_port(handler)
        self._port = port

        if sys.platform == "win32":
            self._start_windows(handler, port)
        else:
            self._start_unix(handler, port)

        logger.info("回调服务器启动在 http://%s:%d", CALLBACK_HOST, self._port)

    def _bind_port(self, handler) -> int:
        """尝试从 CALLBACK_PORT_START 开始依次绑定，返回成功绑定的端口号。"""
        for attempt in range(CALLBACK_PORT_RETRIES):
            port = CALLBACK_PORT_START + attempt
            try:
                self._server = _ThreadingHTTPServer((CALLBACK_BIND_ADDRESS, port), handler)
                return port
            except OSError:
                if attempt == CALLBACK_PORT_RETRIES - 1:
                    raise OSError(f"无法绑定端口 {CALLBACK_PORT_START}-{port}")
                logger.warning("端口 %d 被占用，尝试 %d", port, port + 1)
        raise OSError("端口绑定失败")  # unreachable，满足类型检查

    def _start_windows(self, handler, port: int) -> None:
        """Windows：IPv4（127.0.0.1）+ IPv6（::1）分开监听。"""
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=False, name="ak-callback-server-ipv4",
        )
        self._thread.start()
        logger.debug("Windows: IPv4 回调服务器启动在 http://127.0.0.1:%d", port)

        logger.debug("Windows: 尝试同时启动 IPv6 回调服务器（::1:%d）", port)
        try:
            self._server_ipv6 = _ThreadingHTTPServerIPv6(("::1", port), handler)
            self._thread_ipv6 = threading.Thread(
                target=self._server_ipv6.serve_forever,
                daemon=False, name="ak-callback-server-ipv6",
            )
            self._thread_ipv6.start()
            logger.debug("Windows: IPv6 回调服务器启动在 http://[::1]:%d", port)
        except OSError as e:
            logger.warning("Windows: IPv6 回调服务器启动失败: %s", e)

    def _start_unix(self, handler, port: int) -> None:
        """Linux/macOS：单 AF_INET6 dual-stack socket，IPV6_V6ONLY=0 同时接受 IPv4/IPv6。"""
        self._server.server_close()
        self._server = _ThreadingHTTPServerIPv6(("::", port), handler, bind_and_activate=False)
        self._server.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        self._server.server_bind()
        self._server.server_activate()
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=False, name="ak-callback-server",
        )
        self._thread.start()
        logger.debug("Unix: dual-stack 回调服务器启动在 [::]:%d（同时接受 IPv4/IPv6）", port)

    def wait(self, timeout: int = 300) -> bool:
        return self._done_event.wait(timeout=timeout)

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server = None
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
        if self._server_ipv6:
            self._server_ipv6.shutdown()
            self._server_ipv6 = None
        if self._thread_ipv6:
            self._thread_ipv6.join(timeout=5)
            self._thread_ipv6 = None

    def _save_ak(self, ak: str) -> dict:
        from scripts.capabilities.configure.service import validate_ak, configure_ak
        is_valid, error_msg = validate_ak(ak)
        if not is_valid:
            return {"success": False, "error": "AK_INVALID", "error_description": error_msg}
        success, _ = configure_ak(ak)
        if success:
            return {"success": True, "ak": ak}
        return {"success": False, "error": "AK_SAVE_FAILED",
                "error_description": "AK 保存失败，请检查文件权限"}

    def _create_handler(self) -> type:
        server_ref = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path == "/callback":
                    self._handle_callback(parsed)
                elif parsed.path == "/healthCheck":
                    self._handle_health_check()
                else:
                    self.send_error(404)

            def _handle_health_check(self):
                logger.info("healthCheck from %s:%s", self.client_address[0], self.client_address[1])
                body = b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                parsed = urlparse(self.path)
                if parsed.path == "/api/save-ak":
                    self._handle_save_ak()
                elif parsed.path == "/api/shutdown":
                    self._handle_shutdown()
                else:
                    self.send_error(404)

            def _handle_callback(self, parsed):
                params = parse_qs(parsed.query)

                if "error" in params:
                    error = params["error"][0]
                    desc = params.get("error_description", ["用户拒绝了操作"])[0]
                    html = ERROR_HTML.replace("{error_message}", desc).replace("{error_code}", error)
                    self._send_html(200, html)
                    server_ref._result = {"success": False, "error": error, "error_description": desc}
                    server_ref._done_event.set()
                    return

                received_state = params.get("state", [None])[0]
                if received_state != server_ref._state:
                    html = ERROR_HTML.replace(
                        "{error_message}", "安全校验失败 (state 不匹配)，可能存在 CSRF 攻击。"
                    ).replace("{error_code}", "STATE_MISMATCH")
                    self._send_html(400, html)
                    return

                code = params.get("code", [None])[0]
                if not code:
                    html = ERROR_HTML.replace(
                        "{error_message}", "回调中缺少 AK 数据"
                    ).replace("{error_code}", "MISSING_CODE")
                    self._send_html(400, html)
                    return

                # 返回 HTML 页面，JS 自动 POST AK 到 /api/save-ak
                port = server_ref._port
                code_json = json.dumps(code)
                html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>1688 AK 设置</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;display:flex;justify-content:center;
align-items:center;min-height:100vh;background:#f8f9fa}}
.card{{background:#fff;border-radius:1rem;padding:2.5rem 2rem;
box-shadow:0 4px 24px rgba(0,0,0,.06);max-width:520px;width:92%;text-align:center}}
.spinner{{width:48px;height:48px;border:4px solid #e5e7eb;border-top-color:#FF6A00;
border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 1rem}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.title{{font-size:1.25rem;font-weight:600;color:#333}}
</style></head><body><div class="card">
<div class="spinner"></div><div class="title">正在保存 AK...</div>
</div>
<script>
(function(){{
const AK={code_json};
fetch("http://localhost:{port}/api/save-ak",{{method:"POST",
headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{ak:AK}})}})
.then(r=>r.json()).then(d=>{{
document.querySelector(".card").innerHTML=d.success?
'<div style="font-size:3rem;color:#16a34a">&#10004;</div><div class="title" style="color:#16a34a">AK 设置成功！</div><p style="color:#666;margin-top:1rem">您可以关闭此页面。</p>':
'<div style="font-size:3rem;color:#dc2626">&#10008;</div><div class="title" style="color:#dc2626">设置失败</div><p style="color:#666;margin-top:1rem">'+d.error_description+'</p>';
fetch("http://localhost:{port}/api/shutdown",{{method:"POST"}}).catch(()=>{{}});
}}).catch(err=>{{document.querySelector(".card").innerHTML='<div>连接失败: '+err.message+'</div>';}});
}})();
</script></body></html>"""
                self._send_html(200, html)

            def _handle_save_ak(self):
                origin = self.headers.get("Origin", "")
                allowed = f"http://localhost:{server_ref._port}"
                allowed2 = f"http://127.0.0.1:{server_ref._port}"
                if origin and origin not in (allowed, allowed2):
                    self._send_json(403, {"success": False, "error": "CORS_DENIED"})
                    return

                content_length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}
                ak = body.get("ak", "")

                if not ak:
                    self._send_json(400, {"success": False, "error": "MISSING_AK",
                                          "error_description": "AK 不能为空"})
                    return

                result = server_ref._save_ak(ak)
                server_ref._result = result
                if result.get("success"):
                    server_ref._success = True

                self._send_json(200, result, cors_origin=origin or allowed)
                if result.get("success"):
                    threading.Thread(target=lambda: server_ref._done_event.set(),
                                     daemon=True).start()

            def _handle_shutdown(self):
                allowed = f"http://localhost:{server_ref._port}"
                self._send_json(200, {"success": True}, cors_origin=allowed)
                threading.Thread(target=lambda: server_ref._done_event.set(),
                                 daemon=True).start()

            def _send_html(self, status: int, html: str):
                encoded = html.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(encoded)

            def _send_json(self, status: int, data: dict, cors_origin: str = ""):
                encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.send_header("Cache-Control", "no-store")
                if cors_origin:
                    self.send_header("Access-Control-Allow-Origin", cors_origin)
                    self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()
                self.wfile.write(encoded)

            def do_OPTIONS(self):
                allowed = f"http://localhost:{server_ref._port}"
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", allowed)
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def log_message(self, fmt, *args):
                logger.debug(fmt, *args)

        return Handler
