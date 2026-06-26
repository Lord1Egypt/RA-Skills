#!/usr/bin/env python3
"""
上传图片到飞书，获取 img_key
"""
import argparse
import json
import os
import requests

# 从环境变量或配置文件读取
APP_ID = os.environ.get('FEISHU_APP_ID', '')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {"app_id": app_id, "app_secret": app_secret}
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    
    if result.get("code") != 0:
        raise Exception(f"获取 token 失败: {result}")
    
    return result.get("tenant_access_token")


def upload_image(token: str, image_path: str) -> str:
    """上传图片，返回 img_key"""
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {'image_type': 'message'}
        resp = requests.post(url, headers=headers, files=files, data=data)
    
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"上传图片失败: {result}")
    
    return result.get("data", {}).get("image_key")


def main():
    parser = argparse.ArgumentParser(description="上传图片到飞书")
    parser.add_argument("--image", required=True, help="图片路径")
    parser.add_argument("--app-id", default=APP_ID, help="飞书 App ID")
    parser.add_argument("--app-secret", default=APP_SECRET, help="飞书 App Secret")
    args = parser.parse_args()
    
    # 获取 token
    token = get_tenant_access_token(args.app_id, args.app_secret)
    
    # 上传图片
    img_key = upload_image(token, args.image)
    
    print(json.dumps({"img_key": img_key}, ensure_ascii=False))


if __name__ == "__main__":
    main()
