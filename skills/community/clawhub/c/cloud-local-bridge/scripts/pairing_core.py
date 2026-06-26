#!/usr/bin/env python3
"""
Cloud-Local Bridge 通用配对系统
支持任意通信通道完成配对（QQ/微信/Telegram/邮件等）
"""

import json
import os
import secrets
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import threading
import time

# 配对状态存储
PAIRING_STATE = {
    'requests': {},      # 等待确认的配对请求
    'pairs': {},        # 已完成的配对
    'lock': threading.Lock()
}

STATE_FILE = os.path.expanduser('~/.openclaw/bridge_pairs.json')

def load_state():
    """加载状态"""
    global PAIRING_STATE
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            PAIRING_STATE['requests'] = data.get('requests', {})
            PAIRING_STATE['pairs'] = data.get('pairs', {})

def save_state():
    """保存状态"""
    with PAIRING_STATE['lock']:
        with open(STATE_FILE, 'w') as f:
            json.dump({
                'requests': PAIRING_STATE['requests'],
                'pairs': PAIRING_STATE['pairs']
            }, f, indent=2, default=str)

def generate_pairing_code():
    """生成6位数字配对码"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def generate_device_id():
    """生成设备唯一ID"""
    return secrets.token_hex(8)

def create_pairing_request(initiator_info, channel='unknown'):
    """
    发起配对请求
    initiator_info: {'name': '设备名', 'user_id': '用户ID', 'server': 'http://xxx'}
    channel: 发起渠道（qq/wechat/telegram/email等）
    """
    with PAIRING_STATE['lock']:
        code = generate_pairing_code()
        
        PAIRING_STATE['requests'][code] = {
            'code': code,
            'initiator': initiator_info,
            'channel': channel,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=10)).isoformat()
        }
        save_state()
    
    return {
        'success': True,
        'code': code,
        'expires_in_minutes': 10,
        'message': f'配对码 `{code}`\n\n请通过任意方式（QQ/微信/邮件等）将此配对码发送给要连接的用户'
    }

def confirm_pairing(code, receiver_info, receiver_channel='unknown'):
    """
    确认配对请求
    receiver_info: {'name': '设备名', 'user_id': '用户ID', 'server': 'http://xxx'}
    """
    with PAIRING_STATE['lock']:
        # 检查请求是否存在
        if code not in PAIRING_STATE['requests']:
            return {
                'success': False,
                'error': '配对码不存在或已过期',
                'suggestion': '请让对方重新发起配对'
            }
        
        request = PAIRING_STATE['requests'][code]
        
        # 检查过期
        if datetime.now() > datetime.fromisoformat(request['expires_at']):
            del PAIRING_STATE['requests'][code]
            save_state()
            return {
                'success': False,
                'error': '配对码已过期',
                'suggestion': '请让对方重新发起配对'
            }
        
        # 防止自己配对自己
        if request['initiator'].get('user_id') == receiver_info.get('user_id'):
            return {
                'success': False,
                'error': '不能与自己配对'
            }
        
        # 创建配对
        pair_id = secrets.token_hex(8)
        pair = {
            'id': pair_id,
            'initiator': request['initiator'],
            'receiver': receiver_info,
            'created_at': datetime.now().isoformat(),
            'status': 'connected'
        }
        
        PAIRING_STATE['pairs'][pair_id] = pair
        del PAIRING_STATE['requests'][code]
        save_state()
        
        return {
            'success': True,
            'pair_id': pair_id,
            'message': '🎉 配对成功！\n\n双方设备已互联',
            'partner': {
                'name': request['initiator']['name'],
                'server': request['initiator'].get('server', '')
            }
        }

def get_pairing_status():
    """查看配对状态"""
    with PAIRING_STATE['lock']:
        pending_count = len(PAIRING_STATE['requests'])
        pairs_count = len(PAIRING_STATE['pairs'])
        
        pairs = []
        for pair_id, pair in PAIRING_STATE['pairs'].items():
            pairs.append({
                'id': pair_id,
                'partner': pair['initiator']['name'] if pair['initiator']['name'] else pair['receiver']['name'],
                'status': pair['status']
            })
        
        return {
            'pending_requests': pending_count,
            'connected_pairs': pairs_count,
            'pairs': pairs
        }

def cancel_pairing(code=None, user_id=None):
    """取消配对"""
    with PAIRING_STATE['lock']:
        if code and code in PAIRING_STATE['requests']:
            del PAIRING_STATE['requests'][code]
            save_state()
            return {'success': True, 'message': '已取消配对请求'}
        
        return {'success': False, 'error': '没有找到要取消的配对'}

# ============ QQ 消息处理器 ============

def process_qq_message(message, user_id, user_name="未知"):
    """处理 QQ 消息"""
    msg = message.strip()
    
    # 发起配对
    if msg == '配对':
        return create_pairing_request({
            'name': user_name,
            'user_id': user_id,
            'channel': 'qq'
        })
    
    # 确认配对: 配对 123456
    if msg.startswith('配对 ') and len(msg) > 3:
        code = msg[3:].strip()
        if code.isdigit() and len(code) == 6:
            result = confirm_pairing(code, {
                'name': user_name,
                'user_id': user_id,
                'channel': 'qq'
            })
            if result['success']:
                return f"""🎉 **配对成功!**

✅ 已连接设备: {result['partner']['name']}

现在开始可以协同工作!"""
            else:
                return f"❌ {result['error']}\n\n{result.get('suggestion', '')}"
    
    # 状态
    if msg == '配对状态':
        status = get_pairing_status()
        return f"""📱 **配对状态**

⏳ 待确认: {status['pending_requests']} 个
✅ 已连接: {status['connected_pairs']} 个"""
    
    # 帮助
    if msg == '配对帮助':
        return """📱 **配对帮助**

**配对流程：**
1. 发送 `配对` 获取配对码
2. 把配对码通过任意方式发给对方（QQ/微信/邮件等）
3. 对方发送 `配对 配对码` 完成配对

**其他命令：**
• `配对状态` - 查看配对状态
• `配对帮助` - 显示此帮助"""
    
    return None

# ============ Web API ============

def create_api():
    """创建 Web API 服务（供云端使用）"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse
    
    class APIHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # 静默日志
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
            except:
                self.send_error(400, 'Invalid JSON')
                return
            
            path = self.path
            
            if path == '/api/pair/request':
                # 发起配对
                result = create_pairing_request(
                    data.get('info', {}),
                    data.get('channel', 'api')
                )
                self.send_json(result)
            
            elif path == '/api/pair/confirm':
                # 确认配对
                result = confirm_pairing(
                    data.get('code'),
                    data.get('info', {})
                )
                self.send_json(result)
            
            elif path == '/api/pair/status':
                self.send_json(get_pairing_status())
            
            else:
                self.send_error(404)
        
        def do_GET(self):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            
            if self.path.startswith('/api/pair/code/'):
                code = self.path.split('/')[-1]
                with PAIRING_STATE['lock']:
                    if code in PAIRING_STATE['requests']:
                        req = PAIRING_STATE['requests'][code]
                        self.send_json({
                            'exists': True,
                            'initiator_name': req['initiator']['name'],
                            'expires_at': req['expires_at']
                        })
                    else:
                        self.send_json({'exists': False})
            else:
                self.send_json({'status': 'ok', 'service': 'cloud-local-bridge-pairing'})
        
        def send_json(self, data):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    return APIHandler

def run_api_server(port=8081):
    """运行 API 服务器"""
    load_state()
    server = HTTPServer(('0.0.0.0', port), create_api())
    print(f'🔌 配对 API 服务已启动: http://0.0.0.0:{port}')
    server.serve_forever()

# 初始化
load_state()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--api':
        run_api_server(int(sys.argv[2]) if len(sys.argv) > 2 else 8081)
    else:
        # 测试
        print("=" * 50)
        print("测试配对流程")
        print("=" * 50)
        
        # A 发起配对
        print("\n【A 通过 QQ 发起】")
        result = create_pairing_request({'name': '本地电脑', 'user_id': 'user_a'}, 'qq')
        print(f"配对码: {result['code']}")
        
        # B 通过其他方式确认
        print("\n【B 通过 API 确认】")
        result = confirm_pairing(result['code'], {'name': '云端服务器', 'user_id': 'user_b'})
        print(f"结果: {result['success']}")
        
        print("\n【状态】")
        print(get_pairing_status())
