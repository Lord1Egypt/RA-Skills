#!/usr/bin/env python3
"""
法大大签署任务创建工具

Usage:
    python create_sign_task.py --config config.json --file contract.pdf --signer user_123
    python create_sign_task.py --config config.json --template template_id --data data.json

示例配置文件 config.json:
{
    "app_id": "your_app_id",
    "app_secret": "your_app_secret",
    "server_url": "https://api.fadada.com",
    "callback_url": "https://your-app.com/callback"
}
"""

import argparse
import json
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 假设使用法大大 Python SDK
# 如果没有安装 SDK，可以使用 requests 直接调用 API
try:
    from fadada_api import OpenApiClient, ServiceClient, SignTaskClient, DocClient, EUIClient
    from fadada_api.models import *
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    import requests


class FadadaSignTaskCreator:
    """法大大签署任务创建器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.app_id = config["app_id"]
        self.app_secret = config["app_secret"]
        self.server_url = config["server_url"]
        self.callback_url = config.get("callback_url", "")
        
        if SDK_AVAILABLE:
            self.client = OpenApiClient(
                app_id=self.app_id,
                app_secret=self.app_secret,
                server_url=self.server_url
            )
            self.service_client = ServiceClient(self.client)
            self.sign_task_client = SignTaskClient(self.client)
            self.doc_client = DocClient(self.client)
            self.eui_client = EUIClient(self.client)
        else:
            self.access_token = None
        
        self._token = None
        self._token_expires = None
    
    def _get_access_token(self) -> str:
        """获取 Access Token（带缓存）"""
        if SDK_AVAILABLE:
            response = self.service_client.get_access_token()
            return response.data.access_token
        else:
            # 使用 requests 直接调用 API
            if self._token and self._token_expires and datetime.now() < self._token_expires:
                return self._token
            
            url = f"{self.server_url}/service/get-access-token"
            payload = {
                "app_id": self.app_id,
                "app_secret": self.app_secret,
                "grant_type": "client_credentials"
            }
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"获取 Token 失败: {result.get('message')}")
            
            self._token = result["data"]["access_token"]
            expires_in = result["data"].get("expires_in", 7200)
            self._token_expires = datetime.now() + timedelta(seconds=expires_in - 300)
            return self._token
    
    def upload_file(self, file_path: str) -> str:
        """上传文件"""
        token = self._get_access_token()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"正在上传文件: {file_name} ({file_size} bytes)")
        
        if SDK_AVAILABLE:
            # 获取上传 URL
            upload_info = self.doc_client.get_file_upload_url(
                access_token=token,
                file_name=file_name,
                file_size=file_size
            )
            upload_url = upload_info.data.upload_url
            file_id = upload_info.data.file_id
            
            # 上传文件
            with open(file_path, 'rb') as f:
                requests.put(upload_url, data=f)
            
            return file_id
        else:
            # 直接 API 调用
            url = f"{self.server_url}/doc/get-file-upload-url"
            payload = {
                "access_token": token,
                "file_name": file_name,
                "file_size": file_size
            }
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"获取上传 URL 失败: {result.get('message')}")
            
            upload_url = result["data"]["upload_url"]
            file_id = result["data"]["file_id"]
            
            # 上传文件
            with open(file_path, 'rb') as f:
                requests.put(upload_url, data=f)
            
            print(f"文件上传成功，File ID: {file_id}")
            return file_id
    
    def create_sign_task_from_file(
        self,
        file_id: str,
        signers: List[Dict],
        task_subject: str,
        client_task_id: Optional[str] = None,
        expire_days: int = 30
    ) -> Dict:
        """从文件创建签署任务"""
        token = self._get_access_token()
        
        if not client_task_id:
            client_task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        expire_time = (datetime.now() + timedelta(days=expire_days)).strftime('%Y-%m-%dT%H:%M:%S')
        
        print(f"创建签署任务: {task_subject}")
        print(f"任务 ID: {client_task_id}")
        print(f"签署人数量: {len(signers)}")
        
        # 构建签署人列表
        signer_list = []
        for idx, signer_data in enumerate(signers, 1):
            signer = {
                "client_user_id": signer_data["user_id"],
                "signer_type": signer_data.get("type", "PERSONAL"),
                "sign_type": signer_data.get("sign_type", "POSITION"),
                "sign_order": signer_data.get("order", idx)
            }
            
            if signer["sign_type"] == "POSITION":
                signer["sign_position"] = {
                    "page": signer_data.get("page", 1),
                    "x": signer_data.get("x", 100),
                    "y": signer_data.get("y", 200),
                    "seal_id": signer_data.get("seal_id", "")
                }
            elif signer["sign_type"] == "KEYWORD":
                signer["sign_keyword"] = {
                    "keyword": signer_data["keyword"],
                    "match_strategy": signer_data.get("match_strategy", "FIRST")
                }
            
            signer_list.append(signer)
        
        if SDK_AVAILABLE:
            signer_objects = []
            for s in signer_list:
                signer = Signer()
                signer.client_user_id = s["client_user_id"]
                signer.signer_type = s["signer_type"]
                signer.sign_type = s["sign_type"]
                signer.sign_order = s["sign_order"]
                
                if "sign_position" in s:
                    signer.sign_position = SignPosition(**s["sign_position"])
                if "sign_keyword" in s:
                    signer.sign_keyword = SignKeyword(**s["sign_keyword"])
                
                signer_objects.append(signer)
            
            create_req = CreateSignTaskReq()
            create_req.access_token = token
            create_req.client_task_id = client_task_id
            create_req.task_subject = task_subject
            create_req.file_id = file_id
            create_req.signers = signer_objects
            create_req.expire_time = expire_time
            create_req.callback_url = self.callback_url
            
            response = self.sign_task_client.create_sign_task(create_req)
            
            return {
                "task_id": response.data.task_id,
                "client_task_id": response.data.client_task_id,
                "status": response.data.task_status
            }
        else:
            url = f"{self.server_url}/sign-task/create-sign-task"
            payload = {
                "access_token": token,
                "client_task_id": client_task_id,
                "task_subject": task_subject,
                "file_id": file_id,
                "signers": signer_list,
                "expire_time": expire_time,
                "callback_url": self.callback_url
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"创建签署任务失败: {result.get('message')}")
            
            return {
                "task_id": result["data"]["task_id"],
                "client_task_id": result["data"]["client_task_id"],
                "status": result["data"]["task_status"]
            }
    
    def create_sign_task_from_template(
        self,
        template_id: str,
        template_data: Dict,
        signers: List[Dict],
        task_subject: str,
        client_task_id: Optional[str] = None,
        expire_days: int = 30
    ) -> Dict:
        """从模板创建签署任务"""
        token = self._get_access_token()
        
        if not client_task_id:
            client_task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        expire_time = (datetime.now() + timedelta(days=expire_days)).strftime('%Y-%m-%dT%H:%M:%S')
        
        print(f"创建模板签署任务: {task_subject}")
        print(f"模板 ID: {template_id}")
        
        # 构建模板填充值
        fill_values = [
            {"field_id": k, "field_value": v}
            for k, v in template_data.items()
        ]
        
        # 构建签署人列表
        signer_list = []
        for idx, signer_data in enumerate(signers, 1):
            signer_list.append({
                "client_user_id": signer_data["user_id"],
                "signer_type": signer_data.get("type", "PERSONAL"),
                "sign_order": signer_data.get("order", idx)
            })
        
        if SDK_AVAILABLE:
            fill_objects = [TemplateFillValue(**fv) for fv in fill_values]
            signer_objects = []
            for s in signer_list:
                signer = Signer()
                signer.client_user_id = s["client_user_id"]
                signer.signer_type = s["signer_type"]
                signer.sign_order = s["sign_order"]
                signer_objects.append(signer)
            
            create_req = CreateSignTaskReq()
            create_req.access_token = token
            create_req.client_task_id = client_task_id
            create_req.task_subject = task_subject
            create_req.template_id = template_id
            create_req.template_fill_values = fill_objects
            create_req.signers = signer_objects
            create_req.expire_time = expire_time
            create_req.callback_url = self.callback_url
            
            response = self.sign_task_client.create_sign_task(create_req)
            
            return {
                "task_id": response.data.task_id,
                "client_task_id": response.data.client_task_id,
                "status": response.data.task_status
            }
        else:
            url = f"{self.server_url}/sign-task/create-sign-task"
            payload = {
                "access_token": token,
                "client_task_id": client_task_id,
                "task_subject": task_subject,
                "template_id": template_id,
                "template_fill_values": fill_values,
                "signers": signer_list,
                "expire_time": expire_time,
                "callback_url": self.callback_url
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"创建签署任务失败: {result.get('message')}")
            
            return {
                "task_id": result["data"]["task_id"],
                "client_task_id": result["data"]["client_task_id"],
                "status": result["data"]["task_status"]
            }
    
    def get_sign_url(self, task_id: str, user_id: str) -> str:
        """获取签署链接"""
        token = self._get_access_token()
        
        if SDK_AVAILABLE:
            from fadada_api.models import GetSignTaskSignUrlReq
            req = GetSignTaskSignUrlReq()
            req.access_token = token
            req.task_id = task_id
            req.client_user_id = user_id
            
            response = self.eui_client.get_sign_task_sign_url(req)
            return response.data.sign_url
        else:
            url = f"{self.server_url}/eui/get-sign-task-sign-url"
            payload = {
                "access_token": token,
                "task_id": task_id,
                "client_user_id": user_id
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"获取签署链接失败: {result.get('message')}")
            
            return result["data"]["sign_url"]


def main():
    parser = argparse.ArgumentParser(description="法大大签署任务创建工具")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--file", help="要签署的文件路径")
    parser.add_argument("--template", help="模板 ID")
    parser.add_argument("--data", help="模板数据 JSON 文件路径")
    parser.add_argument("--subject", required=True, help="任务主题")
    parser.add_argument("--signers", required=True, help="签署人信息 JSON 文件路径")
    parser.add_argument("--task-id", help="自定义任务 ID")
    parser.add_argument("--expire-days", type=int, default=30, help="任务过期天数")
    parser.add_argument("--output", help="输出结果到文件")
    
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 加载签署人信息
    with open(args.signers, 'r', encoding='utf-8') as f:
        signers = json.load(f)
    
    # 创建任务创建器
    creator = FadadaSignTaskCreator(config)
    
    try:
        if args.file:
            # 文件签署模式
            print("=== 文件签署模式 ===")
            file_id = creator.upload_file(args.file)
            result = creator.create_sign_task_from_file(
                file_id=file_id,
                signers=signers,
                task_subject=args.subject,
                client_task_id=args.task_id,
                expire_days=args.expire_days
            )
        elif args.template:
            # 模板签署模式
            print("=== 模板签署模式 ===")
            if not args.data:
                print("错误: 模板模式需要提供 --data 参数指定模板数据文件")
                sys.exit(1)
            
            with open(args.data, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            result = creator.create_sign_task_from_template(
                template_id=args.template,
                template_data=template_data,
                signers=signers,
                task_subject=args.subject,
                client_task_id=args.task_id,
                expire_days=args.expire_days
            )
        else:
            print("错误: 请提供 --file 或 --template 参数")
            sys.exit(1)
        
        print("\n=== 任务创建成功 ===")
        print(f"任务 ID: {result['task_id']}")
        print(f"应用任务 ID: {result['client_task_id']}")
        print(f"任务状态: {result['status']}")
        
        # 获取签署链接
        print("\n=== 签署链接 ===")
        for signer in signers:
            try:
                sign_url = creator.get_sign_url(result['task_id'], signer['user_id'])
                print(f"签署人 {signer['user_id']}: {sign_url}")
            except Exception as e:
                print(f"签署人 {signer['user_id']}: 获取链接失败 - {e}")
        
        # 输出到文件
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到: {args.output}")
        
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
