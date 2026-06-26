#!/usr/bin/env python3
"""
Cloud-Local Bridge Web API 处理器
供云端或其他平台使用
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pairing_core import (
    create_pairing_request,
    confirm_pairing,
    get_pairing_status,
    load_state
)

# 初始化
load_state()

def handle_api_request(data):
    """
    处理 API 请求
    供任意 HTTP 客户端调用
    
    用法:
    result = handle_api_request({
        'action': 'request',
        'info': {'name': '设备名', 'user_id': 'xxx'},
        'channel': 'telegram'
    })
    """
    action = data.get('action')
    
    if action == 'request':
        # 发起配对请求
        return create_pairing_request(
            data.get('info', {}),
            data.get('channel', 'api')
        )
    
    elif action == 'confirm':
        # 确认配对
        code = data.get('code')
        return confirm_pairing(
            code,
            data.get('info', {}),
            data.get('channel', 'api')
        )
    
    elif action == 'status':
        # 查看状态
        return get_pairing_status()
    
    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}',
            'available_actions': ['request', 'confirm', 'status']
        }

def create_http_handler():
    """创建 HTTP 处理函数"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class APIHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass
        
        def send_json(self, data, status=200):
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_json({'success': False, 'error': 'Invalid JSON'}, 400)
                return
            
            result = handle_api_request(data)
            self.send_json(result)
        
        def do_GET(self):
            from urllib.parse import parse_qs, urlparse
            
            path = self.path
            query = parse_qs(urlparse(path).query)
            
            if path == '/health':
                self.send_json({'status': 'ok', 'service': 'cloud-local-bridge-api'})
            elif path == '/status':
                self.send_json(get_pairing_status())
            else:
                self.send_json({'error': 'Not found'}, 404)
    
    return APIHandler

def run_server(port=8081):
    """运行 API 服务器"""
    from http.server import HTTPServer
    
    load_state()
    handler = create_http_handler()
    server = HTTPServer(('0.0.0.0', port), handler)
    
    print(f"""
🔌 Cloud-Local Bridge API 服务已启动

📡 API 端点:
   POST /api/pair/request  - 发起配对
   POST /api/pair/confirm  - 确认配对
   GET  /status            - 查看状态
   GET  /health            - 健康检查

💡 使用示例:
   curl -X POST http://localhost:{port}/api/pair/request \\
     -H "Content-Type: application/json" \\
     -d '{{"action":"request","info":{{"name":"云端","user_id":"cloud"}}}}'
""")
    
    server.serve_forever()

# 命令行工具
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Cloud-Local Bridge API')
    parser.add_argument('--port', type=int, default=8081, help='监听端口')
    parser.add_argument('--action', choices=['request', 'confirm', 'status'], help='API 动作')
    parser.add_argument('--code', help='配对码')
    parser.add_argument('--name', help='设备名称')
    parser.add_argument('--user-id', help='用户ID')
    
    args = parser.parse_args()
    
    if args.action:
        if args.action == 'request':
            result = create_pairing_request({
                'name': args.name or 'CLI',
                'user_id': args.user_id or 'cli'
            }, 'cli')
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif args.action == 'confirm':
            result = confirm_pairing(args.code, {
                'name': args.name or 'CLI',
                'user_id': args.user_id or 'cli'
            })
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif args.action == 'status':
            print(json.dumps(get_pairing_status(), ensure_ascii=False, indent=2))
    else:
        run_server(args.port)
