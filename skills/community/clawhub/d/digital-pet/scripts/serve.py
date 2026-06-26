#!/usr/bin/env python3
"""
Labubu 3D 展示服务器
启动本地HTTP服务器来查看3D模型
"""

import http.server
import socketserver
import os
import sys

PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # 添加CORS头以支持本地开发
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    print(f"🧸 Labubu 3D 展示服务器")
    print(f"=" * 40)
    print(f"📁 目录: {DIRECTORY}")
    print(f"🌐 地址: http://localhost:{PORT}")
    print(f"=" * 40)
    print(f"按 Ctrl+C 停止服务器\n")

    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ 服务器已启动!")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"\n❌ 端口 {PORT} 已被占用")
            print(f"请尝试使用其他端口，或关闭占用该端口的程序")
        else:
            raise

if __name__ == "__main__":
    main()
