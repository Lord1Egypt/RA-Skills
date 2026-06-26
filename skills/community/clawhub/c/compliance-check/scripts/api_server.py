#!/usr/bin/env python3
"""
合规检查 HTTP API：供元器/插件等通过 URL 调用，无需安装额外依赖（仅标准库）。
启动: python api_server.py [--port 8000]
接口: POST /check   Body JSON: {"text": "待检查的文案"}  返回: 与 check.py 相同的 JSON
"""
import json
import sys
import os

# 确保能 import 同目录的 check
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import run_check

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class CheckHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_POST(self):
        if self.path != '/check' and not self.path.rstrip('/').endswith('/check'):
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8', errors='replace')
            data = json.loads(body) if body.strip() else {}
            text = data.get('text', data.get('content', ''))
        except Exception as e:
            self.send_response(400)
            self._send_cors()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'error': f'请求体需为 JSON，且包含 text 或 content: {e}'}, ensure_ascii=False).encode('utf-8'))
            return

        result = run_check(text, format_report=False)
        out = json.dumps(result, ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self._send_cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(out))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, format, *args):
        pass  # 可改为 print 方便调试


def main():
    port = int(os.environ.get('PORT', 8000))
    if '--port' in sys.argv:
        i = sys.argv.index('--port')
        if i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    server = HTTPServer(('0.0.0.0', port), CheckHandler)
    print(f'合规检查 API 已启动: http://0.0.0.0:{port}/check')
    print('POST JSON: {"text": "待检查的文案"}')
    server.serve_forever()


if __name__ == '__main__':
    main()
