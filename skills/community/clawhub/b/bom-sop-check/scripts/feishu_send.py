#!/usr/bin/env python3
"""
飞书文件发送脚本
使用飞书 API 直接上传并发送文件
"""

import os
import sys
import json
import requests
from typing import Optional, Tuple

# 飞书配置 - 从 OpenClaw 配置读取
OPENCLAW_CONFIG = "/root/.openclaw/openclaw.json"

def load_feishu_config() -> Tuple[str, str]:
    """加载飞书配置"""
    try:
        with open(OPENCLAW_CONFIG, 'r') as f:
            config = json.load(f)
        channels = config.get('channels', {})
        feishu = channels.get('feishu', {})
        app_id = feishu.get('appId', '')
        app_secret = feishu.get('appSecret', '')
        return app_id, app_secret
    except Exception as e:
        print(f"加载配置失败: {e}")
        return '', ''

def get_tenant_token(app_id: str, app_secret: str) -> Optional[str]:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": app_id, "app_secret": app_secret}
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        result = resp.json()
        if result.get('code') == 0:
            return result.get('tenant_access_token')
        else:
            print(f"获取token失败: {result}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def upload_file(token: str, file_path: str) -> Optional[str]:
    """上传文件到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    
    # 确定文件类型
    ext = os.path.splitext(file_path)[1].lower()
    file_type_map = {
        '.xlsx': 'xlsx',
        '.xls': 'xls',
        '.pdf': 'pdf',
        '.doc': 'doc',
        '.docx': 'docx',
        '.png': 'png',
        '.jpg': 'jpg',
        '.jpeg': 'jpeg',
    }
    file_type = file_type_map.get(ext, 'stream')
    
    headers = {"Authorization": f"Bearer {token}"}
    file_name = os.path.basename(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            data = {
                'file_type': file_type,
                'file_name': file_name,
            }
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
            result = resp.json()
            if result.get('code') == 0:
                return result.get('data', {}).get('file_key')
            else:
                print(f"上传失败: {result}")
                return None
    except Exception as e:
        print(f"上传异常: {e}")
        return None

def send_file_message(token: str, receive_id: str, file_key: str, receive_id_type: str = 'open_id') -> bool:
    """发送文件消息"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        result = resp.json()
        if result.get('code') == 0:
            print(f"发送成功: {result.get('data', {}).get('message_id')}")
            return True
        else:
            print(f"发送失败: {result}")
            return False
    except Exception as e:
        print(f"发送异常: {e}")
        return False

def send_text_message(token: str, receive_id: str, text: str, receive_id_type: str = 'open_id') -> bool:
    """发送文本消息"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        result = resp.json()
        return result.get('code') == 0
    except Exception as e:
        print(f"发送文本异常: {e}")
        return False

def send_file(receive_id: str, file_path: str, text: str = None, receive_id_type: str = 'open_id') -> bool:
    """
    发送文件给指定用户
    
    Args:
        receive_id: 接收者ID (open_id 或 chat_id)
        file_path: 本地文件路径
        text: 附加文本消息（可选）
        receive_id_type: ID类型 (open_id, chat_id, user_id)
    """
    # 加载配置
    app_id, app_secret = load_feishu_config()
    if not app_id or not app_secret:
        print("错误: 缺少飞书配置")
        return False
    
    # 获取 token
    token = get_tenant_token(app_id, app_secret)
    if not token:
        print("错误: 获取 token 失败")
        return False
    
    # 发送文本消息
    if text:
        send_text_message(token, receive_id, text, receive_id_type)
    
    # 上传文件
    print(f"上传文件: {file_path}")
    file_key = upload_file(token, file_path)
    if not file_key:
        print("错误: 上传文件失败")
        return False
    
    print(f"文件已上传: {file_key}")
    
    # 发送文件消息
    return send_file_message(token, receive_id, file_key, receive_id_type)


def main():
    if len(sys.argv) < 3:
        print("用法: python3 feishu_send.py <receive_id> <file_path> [text_message]")
        print("示例: python3 feishu_send.py ou_xxx /path/to/file.xlsx '校对结果'")
        sys.exit(1)
    
    receive_id = sys.argv[1]
    file_path = sys.argv[2]
    text = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        sys.exit(1)
    
    success = send_file(receive_id, file_path, text)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
