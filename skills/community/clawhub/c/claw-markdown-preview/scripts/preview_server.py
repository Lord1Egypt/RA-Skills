#!/usr/bin/env python3
"""启动本地 HTTP 服务，为 Markdown 预览页面提供静态文件服务。

支持：
- 动态读取文件内容（热更新）
- 心跳检测（页面关闭后自动停止服务）
"""

import argparse
import hashlib
import http.server
import json
import mimetypes
import os
import sys
import threading
import time
import uuid as uuid_mod
import webbrowser
from urllib.parse import unquote


ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def find_free_port(start_port):
    import socket
    for port in range(start_port, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


def detach_process():
    """跨平台脱离父进程管理，避免被上层托管系统回收。
    macOS/Linux: 双 fork + setsid，成为独立 session leader（PPID=1）。
    Windows: 用 subprocess.Popen + DETACHED_PROCESS 重启动自身（标记环境变量防止递归）。
    """
    if os.name == 'posix':
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
            os.setsid()
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            pass
    elif os.name == 'nt':
        import subprocess
        if os.environ.get('_CMP_DETACHED') == '1':
            return
        args = [sys.executable] + sys.argv
        env = os.environ.copy()
        env['_CMP_DETACHED'] = '1'
        try:
            proc = subprocess.Popen(args, creationflags=0x00000008,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    stdin=subprocess.DEVNULL)
        except Exception:
            return
        sys.exit(0)


def get_prefs_path():
    """返回跨平台的用户偏好存储路径（不放在技能目录内，重装不丢）。"""
    if os.name == 'nt':
        base = os.environ.get('APPDATA') or os.path.expanduser('~')
        return os.path.join(base, 'claw-markdown-preview', 'prefs.json')
    return os.path.join(os.path.expanduser('~'), '.config', 'claw-markdown-preview', 'prefs.json')


def load_prefs():
    """读取用户偏好，失败返回空 dict。"""
    try:
        with open(get_prefs_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return {}


def save_prefs(data):
    """写入用户偏好，父目录不存在则创建。"""
    path = get_prefs_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


class PreviewServer:
    """共享状态容器，供 HTTP handler 和心跳线程访问。"""

    def __init__(self, file_path=None, stdin_content=None, heartbeat_timeout=7200):
        self.file_path = file_path          # 本地 md 文件路径（None 表示 stdin 模式）
        self.stdin_content = stdin_content  # stdin 模式下的固定内容
        self.heartbeat_timeout = heartbeat_timeout
        self.last_heartbeat = time.time()
        self._content_cache = None          # 缓存上次读取的内容，避免重复读文件
        self._content_hash = None
        self._last_mtime = None

    def get_content(self):
        """获取当前 markdown 内容。文件模式下动态读取文件。"""
        if self.file_path:
            try:
                mtime = os.path.getmtime(self.file_path)
                if self._last_mtime is None or mtime != self._last_mtime:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        self._content_cache = f.read()
                    self._content_hash = hashlib.md5(
                        self._content_cache.encode("utf-8")
                    ).hexdigest()
                    self._last_mtime = mtime
                return self._content_cache
            except (FileNotFoundError, PermissionError):
                return self._content_cache or ""
        return self.stdin_content or ""

    def get_hash(self):
        """获取当前内容的 MD5 hash。"""
        self.get_content()  # 确保缓存是最新的
        return self._content_hash or ""

    def heartbeat(self):
        """更新心跳时间戳。"""
        self.last_heartbeat = time.time()

    def is_alive(self):
        """检查心跳是否在超时范围内。"""
        return (time.time() - self.last_heartbeat) < self.heartbeat_timeout


def make_handler(server_state):
    class PreviewHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=ASSETS_DIR, **kwargs)

        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                return self._serve_index()
            elif self.path == "/api/markdown":
                return self._serve_markdown_api()
            elif self.path == "/api/markdown-hash":
                return self._serve_hash()
            elif self.path == "/api/close":
                return self._handle_close()
            elif self.path == "/api/prefs":
                return self._serve_prefs()
            elif self.path.startswith("/images/"):
                return self._serve_image()
            return super().do_GET()

        def do_POST(self):
            if self.path == "/api/heartbeat":
                return self._handle_heartbeat()
            elif self.path == "/api/image":
                return self._handle_image_upload()
            elif self.path == "/api/save":
                return self._handle_save()
            elif self.path == "/api/close":
                return self._handle_close_with_save()
            elif self.path == "/api/prefs":
                return self._handle_prefs_save()
            self.send_error(404, "Not Found")

        def _serve_index(self):
            index_path = os.path.join(ASSETS_DIR, "index.html")
            if not os.path.exists(index_path):
                self.send_error(404, "index.html not found")
                return

            with open(index_path, "r", encoding="utf-8") as f:
                html = f.read()

            md_content = server_state.get_content()
            md_json = json.dumps(md_content)
            html = html.replace(
                'var MD_CONTENT = null;',
                'var MD_CONTENT = %s;' % md_json
            )

            prefs = load_prefs()
            html = html.replace(
                'var SAVED_PREFS = null;',
                'var SAVED_PREFS = %s;' % json.dumps({
                    "previewStyle": prefs.get("previewStyle"),
                    "codeTheme": prefs.get("codeTheme"),
                }, ensure_ascii=False)
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        def _serve_markdown_api(self):
            content = server_state.get_content()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(
                {"content": content}, ensure_ascii=False
            ).encode("utf-8"))

        def _serve_hash(self):
            h = server_state.get_hash()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(
                {"hash": h}, ensure_ascii=False
            ).encode("utf-8"))

        def _serve_prefs(self):
            """GET /api/prefs：返回已保存的预览风格偏好。"""
            prefs = load_prefs()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "previewStyle": prefs.get("previewStyle"),
                "codeTheme": prefs.get("codeTheme"),
            }, ensure_ascii=False).encode("utf-8"))

        def _handle_prefs_save(self):
            """POST /api/prefs：保存预览风格偏好到本地文件。"""
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
            except (json.JSONDecodeError, ValueError):
                self.send_error(400, "Invalid JSON")
                return
            prefs = load_prefs()
            if isinstance(data, dict):
                if data.get("previewStyle"):
                    prefs["previewStyle"] = data["previewStyle"]
                if data.get("codeTheme"):
                    prefs["codeTheme"] = data["codeTheme"]
            save_prefs(prefs)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

        def _handle_heartbeat(self):
            server_state.heartbeat()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

        def _handle_close(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            # 延迟关闭，让响应先发出去
            threading.Thread(target=lambda: (time.sleep(0.3), os._exit(0)), daemon=True).start()

        def _handle_close_with_save(self):
            """POST /api/close：先保存内容，再关闭服务。"""
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                try:
                    data = json.loads(body)
                    content = data.get("content", "")
                    if server_state.file_path and content:
                        with open(server_state.file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        if server_state.verbose:
                            print("[save] 内容已保存到文件", file=sys.stderr)
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))
            threading.Thread(target=lambda: (time.sleep(0.3), os._exit(0)), daemon=True).start()

        def _serve_image(self):
            """从 md 文件所在目录的 images/ 子目录提供图片。"""
            if not server_state.file_path:
                self.send_error(404, "No file path set")
                return
            md_dir = os.path.dirname(server_state.file_path)
            rel_path = unquote(self.path.lstrip("/"))
            img_path = os.path.join(md_dir, rel_path)
            # 防止路径穿越
            if not os.path.abspath(img_path).startswith(os.path.abspath(md_dir)):
                self.send_error(403, "Forbidden")
                return
            if not os.path.exists(img_path) or not os.path.isfile(img_path):
                self.send_error(404, "Image not found")
                return
            content_type, _ = mimetypes.guess_type(img_path)
            if not content_type:
                content_type = "application/octet-stream"
            with open(img_path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _handle_image_upload(self):
            """POST /api/image：接收图片 Blob，存入 md 目录的 images/ 下。"""
            if not server_state.file_path:
                self.send_error(400, "No file path set")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            content_type = self.headers.get("Content-Type", "image/png")
            ext_map = {
                "image/png": "png",
                "image/jpeg": "jpg",
                "image/gif": "gif",
                "image/webp": "webp",
                "image/svg+xml": "svg",
            }
            ext = ext_map.get(content_type, "png")
            img_id = "img-" + uuid_mod.uuid4().hex[:8]
            filename = "%s.%s" % (img_id, ext)
            md_dir = os.path.dirname(server_state.file_path)
            images_dir = os.path.join(md_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            img_path = os.path.join(images_dir, filename)
            with open(img_path, "wb") as f:
                f.write(body)
            relative_path = "images/" + filename
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"path": relative_path}).encode("utf-8"))

        def _handle_save(self):
            """POST /api/save：将编辑器内容写回 md 文件。"""
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body)
                content = data.get("content", "")
            except (json.JSONDecodeError, KeyError):
                self.send_error(400, "Invalid JSON")
                return
            if server_state.file_path:
                with open(server_state.file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                server_state._content_cache = content
                server_state._content_hash = hashlib.md5(
                    content.encode("utf-8")
                ).hexdigest()
                server_state._last_mtime = os.path.getmtime(server_state.file_path)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "hash": server_state._content_hash}).encode("utf-8"))

        def log_message(self, format, *args):
            if server_state.verbose:
                super().log_message(format, *args)

    return PreviewHandler


def heartbeat_watcher(server_state, http_server):
    """后台线程：监控心跳，超时则关闭服务。"""
    while True:
        time.sleep(2)
        if not server_state.is_alive():
            if server_state.verbose:
                print("[heartbeat] 心跳超时，自动关闭服务", file=sys.stderr)
            http_server.shutdown()
            return


def main():
    parser = argparse.ArgumentParser(description="ClawMarkDown Preview Server")
    parser.add_argument("--file", "-f", type=str, help="markdown 文件路径")
    parser.add_argument("--port", "-p", type=int, default=8765, help="HTTP 端口")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取 markdown")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--verbose", action="store_true", help="输出请求日志")
    parser.add_argument("--heartbeat-timeout", type=int, default=7200,
                        help="心跳超时秒数，超过此时间无心跳则自动关闭服务（默认 7200，即 120 分钟，避免后台标签页冻结/睡眠误杀）")
    args = parser.parse_args()

    stdin_content = None
    file_path = None

    if args.stdin:
        stdin_content = sys.stdin.read()
    elif args.file:
        file_path = os.path.abspath(args.file)
        if not os.path.exists(file_path):
            print("错误：文件不存在: %s" % args.file, file=sys.stderr)
            sys.exit(1)

    server_state = PreviewServer(
        file_path=file_path,
        stdin_content=stdin_content,
        heartbeat_timeout=args.heartbeat_timeout,
    )
    server_state.verbose = args.verbose

    port = find_free_port(args.port)
    HandlerClass = make_handler(server_state)

    http_server = http.server.HTTPServer(("127.0.0.1", port), HandlerClass)

    # 启动心跳监控线程
    watcher_thread = threading.Thread(
        target=heartbeat_watcher,
        args=(server_state, http_server),
        daemon=True,
    )
    watcher_thread.start()

    url = "http://127.0.0.1:%d" % port
    if not args.no_open:
        webbrowser.open(url)

    md_content = server_state.get_content()
    if md_content:
        print("已加载 Markdown 内容（%d 字符）" % len(md_content))
    print("== Markdown 预览服务已启动: %s ==" % url)
    print("心跳超时: %d 秒（%d 分钟）" % (args.heartbeat_timeout, args.heartbeat_timeout // 60))
    print("按 Ctrl+C 停止服务")

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        http_server.server_close()


if __name__ == "__main__":
    detach_process()
    main()
