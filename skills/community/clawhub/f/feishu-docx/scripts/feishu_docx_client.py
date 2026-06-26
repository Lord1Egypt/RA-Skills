import requests
import json
import os
import time
from typing import List, Dict, Any, Optional

class FeishuDocx:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = self._get_tenant_access_token()

    def _get_tenant_access_token(self) -> str:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json().get("tenant_access_token")

    def upload_file(self, file_path: str, folder_token: str):
        """上传文件获取 file_token"""
        url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # 飞书 upload_all 要求的 form-data 字段
        # 注意：使用 data 参数传递文本字段，使用 files 参数传递文件
        data = {
            "file_name": file_name,
            "parent_type": "explorer",
            "parent_node": folder_token,
            "size": str(file_size)
        }
        
        with open(file_path, 'rb') as f:
            files = {
                "file": (file_name, f, 'application/octet-stream')
            }
            res = requests.post(url, headers=headers, data=data, files=files)
            if res.status_code != 200:
                print(f"DEBUG Upload Error: {res.text}")
            res.raise_for_status()
            return res.json()["data"]["file_token"]

    def import_markdown(self, file_token: str, file_name: str, folder_token: str):
        """创建导入任务，将 Markdown 导入为 docx"""
        url = "https://open.feishu.cn/open-apis/drive/v1/import_tasks"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {
            "file_extension": "md",
            "file_token": file_token,
            "type": "docx",
            "file_name": file_name,
            "point": {
                "mount_key": folder_token,
                "mount_type": 1 # 1 为文件夹
            }
        }
        print(f"DEBUG Payload: {json.dumps(payload)}")
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code != 200:
            print(f"DEBUG Response: {res.text}")
        res.raise_for_status()
        ticket = res.json()["data"]["ticket"]
        
        check_url = f"https://open.feishu.cn/open-apis/drive/v1/import_tasks/{ticket}"
        while True:
            time.sleep(1)
            check_res = requests.get(check_url, headers={"Authorization": f"Bearer {self.tenant_access_token}"})
            check_res.raise_for_status()
            result_data = check_res.json()["data"]["result"]
            if result_data["job_status"] == 0: # 成功
                return result_data["token"]
            elif result_data["job_status"] in [1, 2]: # 进行中
                continue
            else:
                raise Exception(f"Import failed: {check_res.text}")

    def delete_file(self, file_token: str):
        """删除云空间文件 (放入回收站)"""
        url = f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}"
        }
        params = {
            "type": "file" # 对应上传时的文件类型
        }
        res = requests.delete(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()

    def create_document(self, title: str, folder_token: Optional[str] = None) -> str:
        url = "https://open.feishu.cn/open-apis/docx/v1/documents"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        payload = {"title": title}
        if folder_token:
            payload["folder_token"] = folder_token
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["data"]["document"]["document_id"]
