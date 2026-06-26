#!/usr/bin/env python3
"""
Cloud-Local Bridge 自然语言配对处理器
支持自然语言理解，无需记忆指令
自动交换连接信息（服务器地址 + Token）
"""

import json
import os
import secrets
from pathlib import Path
from datetime import datetime, timedelta
import re

# 配对状态存储
PAIRING_STATE_FILE = Path(os.path.expanduser('~/.openclaw/bridge_pairing_state.json'))
BRIDGE_CONFIG_FILE = Path(os.path.expanduser('~/.openclaw/bridge.json'))

def load_state():
    """加载配对状态"""
    if PAIRING_STATE_FILE.exists():
        with open(PAIRING_STATE_FILE, 'r') as f:
            return json.load(f)
    return {'pending': {}, 'pairs': {}}

def save_state(state):
    """保存配对状态"""
    PAIRING_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PAIRING_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)

def load_bridge_config():
    """加载 Bridge 配置"""
    if BRIDGE_CONFIG_FILE.exists():
        with open(BRIDGE_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_bridge_config(config):
    """保存 Bridge 配置"""
    BRIDGE_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BRIDGE_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def generate_pairing_code():
    """生成6位配对码"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def create_pairing_request(user_id, user_name="未知"):
    """发起配对请求"""
    state = load_state()
    
    # 检查是否已有待处理的请求
    if user_id in state.get('pending', {}):
        pending = state['pending'][user_id]
        return {
            'action': 'pending',
            'code': pending['code'],
            'message': f"📋 你已有一个待处理的配对请求\n\n🔢 配对码：`{pending['code']}`\n\n请让对方发送「配对 {pending['code']}」完成配对\n\n⏰ 有效期至：{pending['expires_at'][:16].replace('T', ' ')}"
        }
    
    # 检查是否已有配对的设备
    existing_pairs = state.get('pairs', {}).get(user_id, {})
    if existing_pairs:
        partner_names = [p.get('partner_name', '未知') for p in existing_pairs.values()]
        return {
            'action': 'already_paired',
            'message': f"✅ 你已经配对了 {len(partner_names)} 个设备：\n\n• " + "\n• ".join(partner_names) + "\n\n如需添加新设备，请先「取消配对」"
        }
    
    # 获取本地的 Bridge 连接信息
    config = load_bridge_config()
    local_server = config.get('local', {}).get('server', '') if config else ''
    local_token = config.get('local', {}).get('token', '') if config else ''
    
    # 创建新请求
    code = generate_pairing_code()
    expires = datetime.now() + timedelta(minutes=10)
    
    if 'pending' not in state:
        state['pending'] = {}
    
    state['pending'][user_id] = {
        'code': code,
        'user_id': user_id,
        'user_name': user_name,
        'server': local_server,
        'token': local_token,
        'created_at': datetime.now().isoformat(),
        'expires_at': expires.isoformat()
    }
    save_state(state)
    
    # 生成提示消息
    if local_server:
        info_msg = f"\n📡 你的服务器：{local_server}"
    else:
        info_msg = "\n💡 提示：请先运行 bridge_server.py 启动服务"
    
    return {
        'action': 'created',
        'code': code,
        'message': f"""📱 **发起配对成功!**

🔢 配对码：`{code}`

📋 把这个配对码发送给要连接的设备（通过 QQ/微信/邮件等任意方式）

对方只需发送：「配对 {code}」

⏰ 10分钟内有效{info_msg}"""
    }

def confirm_pairing(code, user_id, user_name="未知"):
    """确认配对请求"""
    state = load_state()
    
    # 查找配对码对应的发起者
    initiator_id = None
    initiator_info = None
    
    for uid, pending in state.get('pending', {}).items():
        if pending['code'] == code:
            initiator_id = uid
            initiator_info = pending
            break
    
    if not initiator_id:
        # 检查是否是已配对的
        for pair_id, pair in state.get('pairs', {}).get(user_id, {}).items():
            if pair.get('code') == code:
                return {
                    'action': 'already_paired',
                    'message': f"✅ 你们已经配对过了！\n\n设备：{pair.get('partner_name', '未知')}\n\n服务器：{pair.get('server', '未知')}"
                }
        
        return {
            'action': 'not_found',
            'message': f"❌ 配对码 `{code}` 不存在或已过期\n\n请让对方重新发起配对"
        }
    
    # 防止自己配对自己
    if initiator_id == user_id:
        return {
            'action': 'self_pairing',
            'message': "❌ 不能与自己配对"
        }
    
    # 获取自己的 Bridge 连接信息
    config = load_bridge_config()
    my_server = config.get('local', {}).get('server', '') if config else ''
    my_token = config.get('local', {}).get('token', '') if config else ''
    
    # 创建配对
    pair_id = secrets.token_hex(8)
    
    if 'pairs' not in state:
        state['pairs'] = {}
    
    # 保存发起者的配对信息
    if initiator_id not in state['pairs']:
        state['pairs'][initiator_id] = {}
    state['pairs'][initiator_id][pair_id] = {
        'partner_id': user_id,
        'partner_name': user_name,
        'code': code,
        'server': initiator_info.get('server', ''),
        'token': initiator_info.get('token', ''),
        'paired_at': datetime.now().isoformat()
    }
    
    # 保存确认方的配对信息
    if user_id not in state['pairs']:
        state['pairs'][user_id] = {}
    state['pairs'][user_id][pair_id] = {
        'partner_id': initiator_id,
        'partner_name': initiator_info['user_name'],
        'code': code,
        'server': initiator_info.get('server', ''),
        'token': initiator_info.get('token', ''),
        'paired_at': datetime.now().isoformat()
    }
    
    # 清理待处理请求
    del state['pending'][initiator_id]
    save_state(state)
    
    # 生成连接信息
    partner_server = initiator_info.get('server', '')
    if partner_server:
        connect_info = f"\n🔗 对方服务器：{partner_server}"
    else:
        connect_info = "\n⚠️ 对方尚未启动 Bridge 服务"
    
    return {
        'action': 'success',
        'pair_id': pair_id,
        'partner_server': partner_server,
        'partner_token': initiator_info.get('token', ''),
        'message': f"""🎉 **配对成功!**

✅ 已成功连接：{initiator_info['user_name']}{connect_info}

现在开始可以：
• 让对方执行命令
• 共享文件
• 协同工作

发送「查看配对」查看已连接设备"""
    }

def get_pairing_status(user_id):
    """获取配对状态"""
    state = load_state()
    
    pairs = state.get('pairs', {}).get(user_id, {})
    
    if not pairs:
        return {
            'action': 'no_pairs',
            'message': """📱 **配对状态**

❌ 还没有配对任何设备

发送「配对」或「我想连接云端」发起配对请求"""
        }
    
    pair_list = []
    for pair_id, pair in pairs.items():
        status = "✅ 在线" if pair.get('status') == 'connected' else "⏸️ 离线"
        server = pair.get('server', '')
        if server:
            pair_list.append(f"• {pair.get('partner_name', '未知')} ({status})\n  {server}")
        else:
            pair_list.append(f"• {pair.get('partner_name', '未知')} ({status})")
    
    return {
        'action': 'has_pairs',
        'count': len(pairs),
        'pairs': list(pairs.values()),
        'message': f"""📱 **配对状态**

已连接 {len(pairs)} 个设备：
{chr(10).join(pair_list)}"""
    }

def cancel_pairing(user_id):
    """取消配对"""
    state = load_state()
    
    if user_id in state.get('pending', {}):
        del state['pending'][user_id]
        save_state(state)
        return {
            'action': 'cancelled',
            'message': "✅ 已取消配对请求"
        }
    
    return {
        'action': 'no_pending',
        'message': "❌ 没有待取消的配对请求"
    }

# 自然语言处理模式
NATURAL_PATTERNS = {
    'initiate': [
        '配对', '发起配对', '我要配对', '想配对',
        '连接', '连接设备', '添加设备', '添加好友',
        '和云端连接', '连接云端', '连接本地',
        '添加云端', '添加本地', '互相关联',
        '关联设备', '关联云端', '关联本地',
        'pair', 'pairing', 'connect'
    ],
    'status': [
        '查看配对', '配对状态', '已配对', '已连接',
        '我的设备', '连接列表', '配对列表', '设备列表',
        '我的配对', 'show pairs', 'list pairs'
    ],
    'cancel': [
        '取消配对', '取消连接', '删除配对', '移除设备',
        '删除设备', '断开连接', '取消关联'
    ],
    'help': [
        '配对帮助', '帮助配对', '如何配对', '怎么配对',
        '配对教程', '连接帮助', 'help pairing'
    ]
}

def process_natural_language(message, user_id, user_name="未知"):
    """处理自然语言消息"""
    msg = message.strip()
    
    # 确认配对（配对 123456）- 优先级最高
    match = re.match(r'^配对\s*(\d{6})$', msg)
    if match:
        return confirm_pairing(match.group(1), user_id, user_name)
    
    # 发起配对
    for pattern in NATURAL_PATTERNS['initiate']:
        if msg.lower() == pattern.lower() or pattern in msg.lower():
            return create_pairing_request(user_id, user_name)
    
    # 检查已配对设备
    state = load_state()
    pairs = state.get('pairs', {}).get(user_id, {})
    
    if pairs:
        for pattern in NATURAL_PATTERNS['status']:
            if pattern in msg.lower():
                return get_pairing_status(user_id)
        
        for pattern in NATURAL_PATTERNS['cancel']:
            if pattern in msg.lower():
                return cancel_pairing(user_id)
        
        for pattern in NATURAL_PATTERNS['help']:
            if pattern in msg.lower():
                return {
                    'action': 'help',
                    'message': """📱 **配对帮助**

**发起配对：**
发送「配对」或「我想连接云端」

**确认配对：**
发送「配对 123456」

**查看状态：**
发送「查看配对」或「我的设备」

**取消配对：**
发送「取消配对」"""
                }
    
    # 检查 pending
    pending = state.get('pending', {}).get(user_id)
    if pending:
        for pattern in NATURAL_PATTERNS['status']:
            if pattern in msg.lower():
                return {
                    'action': 'pending',
                    'message': f"📋 你已有一个待处理的配对请求\n\n🔢 配对码：`{pending['code']}`\n\n请让对方发送「配对 {pending['code']}」完成配对\n\n⏰ 有效期至：{pending['expires_at'][:16].replace('T', ' ')}"
                }
        
        for pattern in NATURAL_PATTERNS['cancel']:
            if pattern in msg.lower():
                return cancel_pairing(user_id)
    
    return None

# ============ Bridge 配置管理 ============

def save_local_config(server, token):
    """保存本地 Bridge 配置"""
    config = load_bridge_config() or {}
    config['local'] = {
        'server': server,
        'token': token
    }
    save_bridge_config(config)
    return config

def get_partner_info(user_id):
    """获取已配对的设备信息"""
    state = load_state()
    pairs = state.get('pairs', {}).get(user_id, {})
    
    partners = []
    for pair_id, pair in pairs.items():
        partners.append({
            'name': pair.get('partner_name', '未知'),
            'server': pair.get('server', ''),
            'token': pair.get('token', '')
        })
    
    return partners

if __name__ == '__main__':
    # 测试
    import shutil
    
    # 清理
    if PAIRING_STATE_FILE.exists():
        shutil.copy(PAIRING_STATE_FILE, str(PAIRING_STATE_FILE) + '.bak')
    os.remove(PAIRING_STATE_FILE)
    
    print("=" * 60)
    print("测试配对流程（带连接信息交换）")
    print("=" * 60)
    
    # 1. A 发起（本地）
    print("\n【A 本地发起】")
    r = create_pairing_request('user_a', '本地电脑')
    print(f"动作: {r['action']}")
    print(f"配对码: {r['code']}")
    code = r['code']
    
    # 模拟 A 运行了 bridge_server.py
    save_local_config('http://192.168.1.100:8080', 'secret_token_abc')
    
    # 2. B 确认（云端）
    print("\n【B 云端确认】")
    r = confirm_pairing(code, 'user_b', '云端服务器')
    print(f"动作: {r['action']}")
    print(f"对方服务器: {r.get('partner_server', 'N/A')}")
    
    # 模拟 B 也运行了 bridge_server.py
    save_local_config('http://cloud.example.com:8080', 'secret_token_xyz')
    
    # 3. A 查看状态
    print("\n【A 查看配对状态】")
    r = get_pairing_status('user_a')
    print(f"动作: {r['action']}")
    print(r['message'])
    
    # 4. 获取 B 的连接信息
    print("\n【A 获取 B 的连接信息】")
    partners = get_partner_info('user_a')
    for p in partners:
        print(f"设备: {p['name']}")
        print(f"服务器: {p['server']}")
        print(f"Token: {p['token'][:20]}...")
