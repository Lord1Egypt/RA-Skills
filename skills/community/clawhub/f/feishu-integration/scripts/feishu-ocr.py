#!/usr/bin/env python3
"""
飞书图片 OCR 识别工具
"""

import json
import sys
import requests
from typing import Optional


def get_feishu_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if result.get("code") != 0:
        raise Exception(f"获取 token 失败: {result}")
    
    return result.get("tenant_access_token")


def ocr_image(image_key: str, tenant_token: str) -> str:
    """
    使用飞书 OCR API 识别图片文字
    
    Args:
        image_key: 图片 key
        tenant_token: 访问令牌
        
    Returns:
        识别出的文字内容
    """
    url = "https://open.feishu.cn/open-apis/optical-char-recognition/v1/image/recognize_basic"
    headers = {
        "Authorization": f"Bearer {tenant_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json={"image_key": image_key})
    result = response.json()
    
    if result.get("code") != 0:
        raise Exception(f"OCR 识别失败: {result}")
    
    texts = result.get("data", {}).get("texts", [])
    return "\n".join([t.get("text", "") for t in texts])


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: feishu-ocr.py <image_key> <tenant_token>")
        print("示例: feishu-ocr.py 'img_v3_xxx' 'token'")
        sys.exit(1)
    
    image_key = sys.argv[1]
    tenant_token = sys.argv[2]
    
    try:
        text = ocr_image(image_key, tenant_token)
        print(text)
    except Exception as e:
        print(f"OCR 失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
