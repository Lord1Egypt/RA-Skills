#!/usr/bin/env python3
"""
解析飞书合并转发消息，提取可读内容（支持用户名查询）

凭证获取优先级：
1. 命令行参数 --app-id / --app-secret
2. 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET
3. OpenClaw 配置文件 ~/.openclaw/openclaw.json

Usage:
  ./parse_forward.py <message_id>
  ./parse_forward.py <message_id> --app-id <id> --app-secret <secret>
  echo '<json>' | ./parse_forward.py --stdin
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from functools import lru_cache


# 全局 token 缓存
_token_cache = {}


def get_feishu_credentials(args_app_id=None, args_app_secret=None):
    """
    获取飞书凭证，优先级：
    1. 命令行参数
    2. 环境变量
    3. OpenClaw 配置
    """
    # 1. 命令行参数
    if args_app_id and args_app_secret:
        return args_app_id, args_app_secret
    
    # 2. 环境变量
    env_app_id = os.environ.get('FEISHU_APP_ID')
    env_app_secret = os.environ.get('FEISHU_APP_SECRET')
    if env_app_id and env_app_secret:
        return env_app_id, env_app_secret
    
    # 3. OpenClaw 配置
    openclaw_config_path = Path.home() / '.openclaw' / 'openclaw.json'
    if openclaw_config_path.exists():
        try:
            with open(openclaw_config_path) as f:
                config = json.load(f)
            feishu_config = config.get('channels', {}).get('feishu', {})
            config_app_id = feishu_config.get('appId')
            config_app_secret = feishu_config.get('appSecret')
            if config_app_id and config_app_secret:
                return config_app_id, config_app_secret
        except:
            pass
    
    return None, None


def get_access_token(app_id: str, app_secret: str) -> str:
    """获取飞书 tenant_access_token"""
    cache_key = f"{app_id}:{app_secret}"
    if cache_key in _token_cache:
        return _token_cache[cache_key]
    
    resp = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': app_id, 'app_secret': app_secret}
    )
    data = resp.json()
    if data.get('code') != 0:
        raise Exception(f"Failed to get token: {data}")
    token = data['tenant_access_token']
    _token_cache[cache_key] = token
    return token


def fetch_message(message_id: str, token: str) -> dict:
    """获取消息详情"""
    resp = requests.get(
        f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return resp.json()


@lru_cache(maxsize=100)
def get_user_name(open_id: str, token: str) -> str:
    """获取用户名（带缓存）"""
    try:
        resp = requests.get(
            f'https://open.feishu.cn/open-apis/contact/v3/users/{open_id}?user_id_type=open_id',
            headers={'Authorization': f'Bearer {token}'}
        )
        data = resp.json()
        if data.get('code') == 0:
            user = data.get('data', {}).get('user', {})
            return user.get('name') or user.get('en_name') or user.get('nickname') or open_id[:15] + '...'
    except:
        pass
    return open_id[:15] + '...'


def get_sender_display(sender: dict, token: str = None) -> str:
    """获取发送者显示名称"""
    sender_type = sender.get('sender_type', '')
    sender_id = sender.get('id', 'unknown')
    
    if sender_type == 'app':
        return f"[机器人] {sender_id[:20]}"
    elif sender_type == 'user' and token:
        name = get_user_name(sender_id, token)
        return name
    else:
        return f"[{sender_type}] {sender_id[:15]}..."


def parse_content(msg: dict) -> str:
    """解析消息内容为可读文本"""
    msg_type = msg.get('msg_type', '')
    body = msg.get('body', {})
    content = body.get('content', '')
    
    if msg_type == 'merge_forward':
        return '[合并转发消息]'
    
    if msg_type == 'text':
        try:
            data = json.loads(content)
            return data.get('text', content)
        except:
            return content
    
    if msg_type == 'post':
        try:
            data = json.loads(content)
            title = data.get('title', '')
            elements = data.get('content', [])
            texts = []
            if title:
                texts.append(f"【{title}】")
            for row in elements:
                for el in row:
                    if el.get('tag') == 'text':
                        texts.append(el.get('text', ''))
                    elif el.get('tag') == 'img':
                        texts.append('[图片]')
                    elif el.get('tag') == 'a':
                        texts.append(f"[链接: {el.get('text', '')}]")
            return ''.join(texts)
        except:
            return content
    
    if msg_type == 'interactive':
        try:
            data = json.loads(content)
            title = data.get('title', '')
            elements = data.get('elements', [])
            texts = []
            if title:
                texts.append(f"【{title}】")
            for row in elements:
                for el in row:
                    if el.get('tag') == 'text':
                        texts.append(el.get('text', ''))
                    elif el.get('tag') == 'img':
                        texts.append('[图片]')
            return ''.join(texts) if texts else f'[卡片消息] {title}'
        except:
            return f'[卡片消息] {content[:100]}...'
    
    if msg_type == 'image':
        return '[图片]'
    if msg_type == 'file':
        return '[文件]'
    if msg_type == 'audio':
        return '[语音]'
    if msg_type == 'video':
        return '[视频]'
    if msg_type == 'sticker':
        return '[表情]'
    
    return f'[{msg_type}] {content[:100]}...' if len(content) > 100 else f'[{msg_type}] {content}'


def format_time(timestamp_ms: str) -> str:
    """格式化时间戳"""
    try:
        ts = int(timestamp_ms) / 1000
        return datetime.fromtimestamp(ts).strftime('%m-%d %H:%M')
    except:
        return timestamp_ms


def format_output(data: dict, output_format: str = 'text', token: str = None) -> str:
    """格式化输出"""
    items = data.get('data', {}).get('items', [])
    
    if not items:
        return "No messages found"
    
    sub_messages = [m for m in items if m.get('upper_message_id')]
    
    if output_format == 'json':
        return json.dumps({
            'parent': items[0] if items else None,
            'messages': sub_messages,
            'count': len(sub_messages)
        }, ensure_ascii=False, indent=2)
    
    lines = []
    lines.append(f"📨 合并转发消息 ({len(sub_messages)} 条)")
    if sub_messages:
        lines.append(f"来源群: {sub_messages[0].get('chat_id', 'unknown')}")
    lines.append("-" * 40)
    
    for msg in sub_messages:
        sender = msg.get('sender', {})
        sender_display = get_sender_display(sender, token)
        time_str = format_time(msg.get('create_time', ''))
        content = parse_content(msg)
        
        lines.append(f"[{time_str}] {sender_display}")
        lines.append(f"  {content}")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='解析飞书合并转发消息')
    parser.add_argument('message_id', nargs='?', help='消息 ID')
    parser.add_argument('--app-id', help='飞书 App ID (或设置 FEISHU_APP_ID 环境变量)')
    parser.add_argument('--app-secret', help='飞书 App Secret (或设置 FEISHU_APP_SECRET 环境变量)')
    parser.add_argument('--stdin', action='store_true', help='从 stdin 读取 JSON')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('--no-names', action='store_true', help='不查询用户名')
    
    args = parser.parse_args()
    
    if not args.stdin and not args.message_id:
        parser.print_help()
        sys.exit(1)
    
    # 获取凭证
    app_id, app_secret = get_feishu_credentials(args.app_id, args.app_secret)
    
    if not args.stdin and (not app_id or not app_secret):
        print("Error: 无法获取飞书凭证。请通过以下方式之一提供：", file=sys.stderr)
        print("  1. 命令行参数: --app-id <id> --app-secret <secret>", file=sys.stderr)
        print("  2. 环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET", file=sys.stderr)
        print("  3. OpenClaw 配置: ~/.openclaw/openclaw.json", file=sys.stderr)
        sys.exit(1)
    
    token = None
    if app_id and app_secret and not args.no_names:
        try:
            token = get_access_token(app_id, app_secret)
        except Exception as e:
            print(f"Warning: 获取 token 失败: {e}", file=sys.stderr)
    
    if args.stdin:
        data = json.load(sys.stdin)
    elif args.message_id:
        if not token:
            token = get_access_token(app_id, app_secret)
        data = fetch_message(args.message_id, token)
    else:
        parser.print_help()
        sys.exit(1)
    
    if data.get('code') != 0:
        print(f"Error: {data.get('msg', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    
    print(format_output(data, args.format, token))


if __name__ == '__main__':
    main()
