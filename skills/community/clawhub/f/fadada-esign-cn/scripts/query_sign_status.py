#!/usr/bin/env python3
"""
法大大签署任务状态查询工具

Usage:
    python query_sign_status.py --config config.json --task-id task_xxx
    python query_sign_status.py --config config.json --client-task-id client_task_xxx
    python query_sign_status.py --config config.json --task-id task_xxx --download ./signed_contract.pdf
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, Optional, List

try:
    from fadada_api import OpenApiClient, ServiceClient, SignTaskClient
    from fadada_api.models import *
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    import requests


class FadadaSignTaskQuery:
    """法大大签署任务查询器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.app_id = config["app_id"]
        self.app_secret = config["app_secret"]
        self.server_url = config["server_url"]
        
        if SDK_AVAILABLE:
            self.client = OpenApiClient(
                app_id=self.app_id,
                app_secret=self.app_secret,
                server_url=self.server_url
            )
            self.service_client = ServiceClient(self.client)
            self.sign_task_client = SignTaskClient(self.client)
        
        self._token = None
    
    def _get_access_token(self) -> str:
        """获取 Access Token"""
        if SDK_AVAILABLE:
            response = self.service_client.get_access_token()
            return response.data.access_token
        else:
            if self._token:
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
            return self._token
    
    def query_task(self, task_id: Optional[str] = None, client_task_id: Optional[str] = None) -> Dict:
        """查询签署任务详情"""
        if not task_id and not client_task_id:
            raise ValueError("请提供 task_id 或 client_task_id")
        
        token = self._get_access_token()
        
        if SDK_AVAILABLE:
            if task_id:
                response = self.sign_task_client.get_sign_task(token, task_id=task_id)
            else:
                response = self.sign_task_client.get_sign_task(token, client_task_id=client_task_id)
            
            data = response.data
            return {
                "task_id": data.task_id,
                "client_task_id": data.client_task_id,
                "task_subject": data.task_subject,
                "task_status": data.task_status,
                "signers": [
                    {
                        "user_id": s.client_user_id,
                        "type": s.signer_type,
                        "status": s.sign_status,
                        "sign_time": s.sign_time
                    }
                    for s in data.signers
                ],
                "create_time": data.create_time,
                "complete_time": data.complete_time,
                "expire_time": data.expire_time
            }
        else:
            url = f"{self.server_url}/sign-task/get-sign-task"
            payload = {"access_token": token}
            if task_id:
                payload["task_id"] = task_id
            else:
                payload["client_task_id"] = client_task_id
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"查询任务失败: {result.get('message')}")
            
            data = result["data"]
            return {
                "task_id": data["task_id"],
                "client_task_id": data["client_task_id"],
                "task_subject": data["task_subject"],
                "task_status": data["task_status"],
                "signers": [
                    {
                        "user_id": s["client_user_id"],
                        "type": s["signer_type"],
                        "status": s["sign_status"],
                        "sign_time": s.get("sign_time")
                    }
                    for s in data["signers"]
                ],
                "create_time": data.get("create_time"),
                "complete_time": data.get("complete_time"),
                "expire_time": data.get("expire_time")
            }
    
    def download_signed_file(self, task_id: str, output_path: str) -> bool:
        """下载已签署的文件"""
        token = self._get_access_token()
        
        print(f"获取文件下载链接...")
        
        if SDK_AVAILABLE:
            response = self.sign_task_client.get_sign_task_file_url(token, task_id=task_id)
            download_url = response.data.file_url
            file_name = response.data.file_name
        else:
            url = f"{self.server_url}/sign-task/get-sign-task-file-url"
            payload = {
                "access_token": token,
                "task_id": task_id
            }
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"获取下载链接失败: {result.get('message')}")
            
            download_url = result["data"]["file_url"]
            file_name = result["data"]["file_name"]
        
        print(f"正在下载文件: {file_name}")
        
        # 下载文件
        file_response = requests.get(download_url)
        if file_response.status_code != 200:
            raise Exception(f"下载文件失败: HTTP {file_response.status_code}")
        
        with open(output_path, 'wb') as f:
            f.write(file_response.content)
        
        file_size = len(file_response.content)
        print(f"文件已保存: {output_path} ({file_size} bytes)")
        return True
    
    def cancel_task(self, task_id: str, reason: str = "") -> bool:
        """撤销签署任务"""
        token = self._get_access_token()
        
        print(f"正在撤销任务: {task_id}")
        
        if SDK_AVAILABLE:
            self.sign_task_client.cancel_sign_task(token, task_id=task_id, reason=reason)
        else:
            url = f"{self.server_url}/sign-task/cancel-sign-task"
            payload = {
                "access_token": token,
                "task_id": task_id,
                "cancel_reason": reason
            }
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                raise Exception(f"撤销任务失败: {result.get('message')}")
        
        print("任务撤销成功")
        return True
    
    def format_status(self, status: str) -> str:
        """格式化状态显示"""
        status_map = {
            "DRAFT": "草稿",
            "SIGNING": "签署中",
            "COMPLETED": "已完成",
            "REJECTED": "已拒绝",
            "CANCELLED": "已撤销",
            "EXPIRED": "已过期"
        }
        return status_map.get(status, status)
    
    def print_task_info(self, task_info: Dict):
        """打印任务信息"""
        print("\n" + "=" * 60)
        print("签署任务详情")
        print("=" * 60)
        print(f"任务 ID:        {task_info['task_id']}")
        print(f"应用任务 ID:    {task_info['client_task_id']}")
        print(f"任务主题:       {task_info['task_subject']}")
        print(f"任务状态:       {self.format_status(task_info['task_status'])}")
        print(f"创建时间:       {task_info['create_time']}")
        if task_info['complete_time']:
            print(f"完成时间:       {task_info['complete_time']}")
        if task_info['expire_time']:
            print(f"过期时间:       {task_info['expire_time']}")
        
        print("\n签署人状态:")
        print("-" * 60)
        for signer in task_info['signers']:
            status_icon = "✓" if signer['status'] == "SIGNED" else "○"
            print(f"  {status_icon} {signer['user_id']} ({signer['type']})")
            print(f"     状态: {signer['status']}")
            if signer['sign_time']:
                print(f"     签署时间: {signer['sign_time']}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="法大大签署任务状态查询工具")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--task-id", help="任务 ID")
    parser.add_argument("--client-task-id", help="应用任务 ID")
    parser.add_argument("--download", help="下载已签署文件到指定路径")
    parser.add_argument("--cancel", action="store_true", help="撤销任务")
    parser.add_argument("--cancel-reason", default="", help="撤销原因")
    parser.add_argument("--output", help="输出结果到 JSON 文件")
    parser.add_argument("--watch", action="store_true", help="持续监控任务状态")
    parser.add_argument("--interval", type=int, default=10, help="监控间隔（秒）")
    
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 创建查询器
    query = FadadaSignTaskQuery(config)
    
    try:
        if args.watch:
            # 持续监控模式
            print("进入监控模式，按 Ctrl+C 退出...")
            import time
            last_status = None
            
            while True:
                try:
                    task_info = query.query_task(args.task_id, args.client_task_id)
                    current_status = task_info['task_status']
                    
                    if current_status != last_status:
                        query.print_task_info(task_info)
                        last_status = current_status
                        
                        if current_status in ["COMPLETED", "REJECTED", "CANCELLED", "EXPIRED"]:
                            print("\n任务已结束，退出监控")
                            break
                    else:
                        print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 状态: {query.format_status(current_status)}", end="")
                    
                    time.sleep(args.interval)
                    
                except KeyboardInterrupt:
                    print("\n\n监控已停止")
                    break
        else:
            # 单次查询模式
            task_info = query.query_task(args.task_id, args.client_task_id)
            query.print_task_info(task_info)
            
            # 下载文件
            if args.download:
                if task_info['task_status'] == "COMPLETED":
                    query.download_signed_file(task_info['task_id'], args.download)
                else:
                    print(f"\n警告: 任务尚未完成（当前状态: {query.format_status(task_info['task_status'])}），无法下载文件")
            
            # 撤销任务
            if args.cancel:
                if task_info['task_status'] in ["DRAFT", "SIGNING"]:
                    confirm = input(f"\n确认撤销任务 '{task_info['task_subject']}'? (y/N): ")
                    if confirm.lower() == 'y':
                        query.cancel_task(task_info['task_id'], args.cancel_reason)
                    else:
                        print("已取消")
                else:
                    print(f"\n错误: 当前状态为 {query.format_status(task_info['task_status'])}，无法撤销")
            
            # 输出到文件
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(task_info, f, ensure_ascii=False, indent=2)
                print(f"\n结果已保存到: {args.output}")
    
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
