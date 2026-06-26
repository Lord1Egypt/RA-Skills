#!/usr/bin/env python3
"""
飞书图片发送模块
"""
import requests
import json

class FeishuImageSender:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or "cli_a92d303bf7f9dcc8"
        self.app_secret = app_secret or "uvP39NArvXPjzPG2bvdZZs2SfZ231YFk"
        self.token = None
    
    def get_token(self):
        """获取tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        resp = requests.post(url, json=data)
        result = resp.json()
        return result.get("tenant_access_token")
    
    def upload_image(self, image_path):
        """上传图片获取image_key"""
        if not self.token:
            self.token = self.get_token()
        
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"image_type": "message"}
            resp = requests.post(url, headers=headers, files=files, data=data)
        
        result = resp.json()
        return result.get("data", {}).get("image_key")
    
    def send_image(self, image_path, user_id):
        """发送图片到用户"""
        if not self.token:
            self.token = self.get_token()
        
        image_key = self.upload_image(image_path)
        if not image_key:
            return {"error": "上传图片失败"}
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {
            "receive_id": user_id,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key})
        }
        
        resp = requests.post(url, headers=headers, json=data)
        return resp.json()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python feishu_image.py <图片路径> <用户ID>")
        sys.exit(1)
    
    sender = FeishuImageSender()
    result = sender.send_image(sys.argv[1], sys.argv[2])
    print(result)
