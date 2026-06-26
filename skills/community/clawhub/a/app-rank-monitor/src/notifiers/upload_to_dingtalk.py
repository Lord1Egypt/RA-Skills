#!/usr/bin/env python3
"""
钉钉文件上传工具
参考穿山甲 OFD 技能中的钉钉配置
"""

import httpx
import json
import yaml
from pathlib import Path

# 从配置文件读取钉钉企业应用配置
config_path = Path(__file__).parent.parent.parent / "config" / "dingtalk.yaml"
DINGTALK_CLIENT_ID = None
DINGTALK_CLIENT_SECRET = None
DINGTALK_CHAT_ID = None
FILE_UPLOAD_WEBHOOK = None

if config_path.exists():
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        dingtalk_config = config.get("dingtalk", {})
        DINGTALK_CLIENT_ID = dingtalk_config.get("client_id")
        DINGTALK_CLIENT_SECRET = dingtalk_config.get("client_secret")
        DINGTALK_CHAT_ID = dingtalk_config.get("chat_id")
        FILE_UPLOAD_WEBHOOK = dingtalk_config.get("webhook")
else:
    raise FileNotFoundError(f"钉钉配置文件不存在：{config_path}")


def get_access_token() -> str:
    """获取钉钉 access_token"""
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": DINGTALK_CLIENT_ID,
        "appsecret": DINGTALK_CLIENT_SECRET
    }
    
    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(url, params=params)
            result = response.json()
            
            if result.get('errcode') == 0:
                return result.get('access_token', '')
            else:
                print(f"❌ 获取 access_token 失败：{result}")
                return ""
    except Exception as e:
        print(f"❌ 获取 token 异常：{e}")
        return ""


def upload_file(file_path: str) -> str:
    """
    上传文件到钉钉
    
    Args:
        file_path: 文件路径
    
    Returns:
        媒体 ID，失败返回空字符串
    """
    access_token = get_access_token()
    if not access_token:
        return ""
    
    # 钉钉媒体上传 API
    upload_url = f"https://oapi.dingtalk.com/media/upload"
    
    try:
        with open(file_path, 'rb') as f:
            files = {
                'media': f
            }
            params = {
                'access_token': access_token,
                'type': 'file'
            }
            
            with httpx.Client(timeout=30) as client:
                response = client.post(upload_url, params=params, files=files)
                print(f"上传响应状态码：{response.status_code}")
                print(f"上传响应内容：{response.text[:500]}")
                
                result = response.json()
                
                if result.get('errcode') == 0:
                    media_id = result.get('media_id', '')
                    print(f"✅ 文件上传成功，media_id: {media_id}")
                    return media_id
                else:
                    print(f"❌ 文件上传失败：{result}")
                    return ""
    except Exception as e:
        print(f"❌ 上传异常：{e}")
        return ""


def send_file_to_chat(media_id: str, file_name: str) -> bool:
    """
    发送文件到钉钉群聊
    
    Args:
        media_id: 媒体 ID
        file_name: 文件名
    
    Returns:
        是否发送成功
    """
    access_token = get_access_token()
    if not access_token:
        return False
    
    # 发送文件消息 API
    send_url = f"https://oapi.dingtalk.com/chat/send"
    
    try:
        data = {
            "chatid": DINGTALK_CHAT_ID,
            "sender_id": "system",
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        
        params = {
            "access_token": access_token
        }
        
        with httpx.Client(timeout=30) as client:
            response = client.post(send_url, params=params, json=data)
            print(f"发送响应状态码：{response.status_code}")
            print(f"发送响应内容：{response.text[:500]}")
            
            result = response.json()
            
            if result.get('errcode') == 0:
                print(f"✅ 文件已发送到群聊")
                return True
            else:
                print(f"❌ 发送失败：{result}")
                return False
    except Exception as e:
        print(f"❌ 发送异常：{e}")
        return False


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python upload_to_dingtalk.py <文件路径>")
        print("示例：python upload_to_dingtalk.py reports/ios_top-free_20260316_xxxxxx.md")
        return 1
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在：{file_path}")
        return 1
    
    print(f"📄 准备上传文件：{file_path}")
    
    # Step 1: 上传文件
    media_id = upload_file(file_path)
    if not media_id:
        return 1
    
    # Step 2: 发送到群聊
    file_name = Path(file_path).name
    if send_file_to_chat(media_id, file_name):
        print(f"✅ 文件上传完成：{file_name}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
