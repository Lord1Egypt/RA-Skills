#!/usr/bin/env python3
"""
记忆同步监控 Web 服务器
提供状态页面和 API
"""

import http.server
import socketserver
import json
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/awu/.openclaw/workspace")
STATUS_FILE = WORKSPACE / "cron_status.json"
HTML_FILE = WORKSPACE / "cron_status.html"
PORT = 8000

class MemoryMonitorHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE), **kwargs)
    
    def do_GET(self):
        """处理 GET 请求"""
        if self.path == '/':
            self.path = '/cron_status_clickable.html'
        elif self.path == '/api/status':
            self.send_status()
            return
        elif self.path == '/api/refresh':
            # 刷新状态
            self.refresh_status()
            self.path = '/api/status'
            self.send_status()
            return
        elif self.path == '/api/memories':
            # 获取记忆详细列表
            self.send_memories()
            return
        
        super().do_GET()
    
    def send_status(self):
        """发送状态 JSON"""
        try:
            with open(STATUS_FILE, 'r') as f:
                status = json.load(f)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(status, indent=2, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def refresh_status(self):
        """刷新状态"""
        try:
            os.system(f"cd {WORKSPACE} && python3 cron_monitor.py > /dev/null 2>&1")
        except:
            pass
    
    def send_memories(self):
        """发送记忆详细列表"""
        try:
            import sqlite3
            db_path = WORKSPACE / "memory.db"
            
            if not db_path.exists():
                self.send_error(404, "Database not found")
                return
            
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 查询所有记忆
            cursor.execute("""
                SELECT id, name, description, type, content, source_file, created_at, classified_type
                FROM memories
                ORDER BY created_at DESC, id DESC
                LIMIT 100
            """)
            
            memories = []
            for row in cursor.fetchall():
                memories.append({
                    'id': row['id'],
                    'name': row['name'],
                    'description': row['description'],
                    'type': row['type'],
                    'content': row['content'],
                    'source_file': row['source_file'],
                    'created_at': row['created_at'],
                    'classified_type': row['classified_type']
                })
            
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(memories, indent=2, ensure_ascii=False)
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))

def run_server(port=PORT):
    """运行 HTTP 服务器"""
    with socketserver.TCPServer(("", port), MemoryMonitorHandler) as httpd:
        print(f"🚀 记忆同步监控 Web 服务已启动")
        print(f"======================================")
        print(f"📊 状态页面：http://localhost:{port}/")
        print(f"📡 API 端点：http://localhost:{port}/api/status")
        print(f"🔄 手动刷新：http://localhost:{port}/api/refresh")
        print(f"======================================")
        print(f"💡 按 Ctrl+C 停止服务")
        print(f"")
        httpd.serve_forever()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
