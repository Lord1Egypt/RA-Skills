"""
settings_server — 设置可视化界面 HTTP 服务

启动后打开浏览器即可看到设置面板，修改后自动隔扇区生效。
"""

import http.server
import json
import os
import sys

SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, SKILL_DIR)
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from scripts.settings_manager import load, save, validate, FIELD_LABELS, FIELD_OPTIONS, FIELD_DESCRIPTIONS, DEFAULT_SETTINGS, get_defaults

PORT = int(os.environ.get("SETTINGS_PORT", "9099"))
HTML_PATH = os.path.join(SKILL_DIR, "scripts", "templates", "settings.html")


class SettingsHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/load":
            self._send_json(load())
        elif self.path == "/api/defaults":
            self._send_json(get_defaults())
        elif self.path == "/api/schema":
            self._send_json({
                "field_labels": FIELD_LABELS,
                "field_options": {k: v for k, v in FIELD_OPTIONS.items()},
                "field_descriptions": FIELD_DESCRIPTIONS,
            })
        elif self.path == "/":
            self._serve_html()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/save":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                self._send_json({"ok": False, "error": f"JSON解析失败: {e}"}, 400)
                return

            errs = validate(data)
            if errs:
                self._send_json({"ok": False, "error": "; ".join(errs)}, 400)
                return

            save(data)
            self._send_json({"ok": True, "data": load()})
        elif self.path == "/api/reset":
            save(get_defaults())
            self._send_json({"ok": True, "data": load()})
        else:
            self._send_json({"ok": False, "error": "Not found"}, 404)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _serve_html(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if os.path.exists(HTML_PATH):
            with open(HTML_PATH, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(b"<h1>settings.html not found</h1>")

    def log_message(self, fmt, *args):
        print(f"[settings] {args[0]}" if args else "")


def main():
    server = http.server.HTTPServer(("0.0.0.0", PORT), SettingsHandler)
    print(f"\n  ⚙️ activity-duration-estimation 设置面板")
    print(f"  ─────────────────────────────────────")
    print(f"  http://localhost:{PORT}")
    print(f"  按 Ctrl+C 停止服务\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  服务已停止")
        server.server_close()


if __name__ == "__main__":
    main()
