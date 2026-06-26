#!/usr/bin/env python3
# send_image.py - 上传图片并发送到飞书群

import sys
import os
import requests

# 导入配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.py")

def load_config():
    """加载配置"""
    if not os.path.exists(CONFIG_FILE):
        print("❌ 配置文件不存在！")
        print("请先创建配置文件：")
        print("  1. cp config.example.py config.py")
        print("  2. 编辑 config.py 填入您的 APP_ID、APP_SECRET、WEBHOOK_URL")
        sys.exit(1)
    
    # 添加脚本目录到路径
    sys.path.insert(0, SCRIPT_DIR)
    
    try:
        from config import APP_ID, APP_SECRET, WEBHOOK_URL
    except ImportError as e:
        print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)
    
    # 检查配置是否有效
    if "your_" in APP_ID or "your_" in APP_SECRET or "your_" in WEBHOOK_URL:
        print("❌ 请先在 config.py 中填入您的实际配置！")
        print("当前配置是模板，请替换为您的 APP_ID、APP_SECRET、WEBHOOK_URL")
        sys.exit(1)
    
    return APP_ID, APP_SECRET, WEBHOOK_URL


def get_tenant_access_token(app_id, app_secret):
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    result = resp.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token")
    else:
        raise Exception(f"获取 token 失败: {result.get('msg')}")


def upload_image(image_path, app_id, app_secret):
    """上传图片到飞书"""
    if not os.path.exists(image_path):
        raise Exception(f"文件不存在: {image_path}")
    
    token = get_tenant_access_token(app_id, app_secret)
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {'image_type': 'message'}
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.post(url, headers=headers, files=files, data=data)
    
    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["image_key"]
    else:
        raise Exception(f"上传失败: {result.get('msg')}")


def send_to_webhook(image_key, webhook_url):
    """通过 webhook 发送图片"""
    resp = requests.post(webhook_url, json={
        "msg_type": "image",
        "content": {
            "image_key": image_key
        }
    }, headers={
        "Content-Type": "application/json"
    })
    return resp.json()


def main():
    if len(sys.argv) < 2:
        print("用法: python send_image.py <图片路径>")
        print("示例: python send_image.py /Users/xxx/Desktop/test.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # 加载配置
    try:
        APP_ID, APP_SECRET, WEBHOOK_URL = load_config()
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        sys.exit(1)
    
    print(f"📤 正在上传图片: {image_path}")
    
    try:
        # 上传图片
        image_key = upload_image(image_path, APP_ID, APP_SECRET)
        print(f"✅ 上传成功")
        print(f"   image_key: {image_key}")
        
        # 发送到群
        print("📤 正在发送到群...")
        result = send_to_webhook(image_key, WEBHOOK_URL)
        
        if result.get("StatusCode") == 0 or result.get("code") == 0:
            print("✅ 发送成功！")
        else:
            print(f"❌ 发送失败: {result}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()