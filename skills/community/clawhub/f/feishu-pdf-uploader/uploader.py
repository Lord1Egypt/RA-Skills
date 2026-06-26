#!/usr/bin/env python3
"""
Feishu PDF Uploader - 自动上传PDF到飞书云盘
"""

import os
import sys
import requests
import json
from pathlib import Path

class FeishuPDFUploader:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or os.getenv('FEISHU_APP_ID')
        self.app_secret = app_secret or os.getenv('FEISHU_APP_SECRET')
        self.token = None
        
    def get_token(self):
        """获取tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                self.token = resp.json().get("tenant_access_token")
                return self.token
        except Exception as e:
            print(f"获取token失败: {e}")
        return None
    
    def upload_pdf(self, file_path, folder_token, custom_name=None):
        """上传PDF文件"""
        if not self.token:
            self.get_token()
        
        if not os.path.exists(file_path):
            return {"error": "文件不存在"}
        
        file_size = os.path.getsize(file_path)
        file_name = custom_name or os.path.basename(file_path)
        
        # 1. 获取上传凭证
        prepare_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_prepare"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        prepare_data = {
            "file_name": file_name,
            "parent_type": "explorer",
            "parent_node": folder_token,
            "size": file_size
        }
        
        try:
            resp = requests.post(prepare_url, headers=headers, json=prepare_data, timeout=10)
            if resp.status_code != 200:
                return {"error": f"获取上传凭证失败: {resp.text}"}
            
            upload_info = resp.json().get("data", {})
            
            # 2. 上传文件内容
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # 3. 完成上传
            finish_url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_finish"
            finish_data = {
                "upload_id": upload_info.get("upload_id"),
                "block_num": 1
            }
            
            resp = requests.post(finish_url, headers=headers, json=finish_data, timeout=10)
            if resp.status_code == 200:
                result = resp.json().get("data", {})
                return {
                    "success": True,
                    "file_token": result.get("file_token"),
                    "url": result.get("url"),
                    "file_name": file_name
                }
            else:
                return {"error": f"完成上传失败: {resp.text}"}
                
        except Exception as e:
            return {"error": f"上传失败: {str(e)}"}

def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description='上传PDF到飞书云盘')
    parser.add_argument('file', help='PDF文件路径')
    parser.add_argument('--folder', required=True, help='目标文件夹token')
    parser.add_argument('--name', help='自定义文件名')
    args = parser.parse_args()
    
    uploader = FeishuPDFUploader()
    result = uploader.upload_pdf(args.file, args.folder, args.name)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
