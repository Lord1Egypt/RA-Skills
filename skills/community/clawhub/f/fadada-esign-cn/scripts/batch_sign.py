#!/usr/bin/env python3
"""
法大大批量签署工具

支持从 Excel 或 CSV 文件批量创建签署任务

Usage:
    python batch_sign.py --config config.json --input batch_data.xlsx --template template_id
    python batch_sign.py --config config.json --input batch_data.csv --file contract.pdf

Excel/CSV 文件格式:
| client_task_id | task_subject | signer_user_id | signer_type | signer_page | signer_x | signer_y | field_party_a | field_amount | ... |
"""

import argparse
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    import csv

try:
    from fadada_api import OpenApiClient, ServiceClient, SignTaskClient, DocClient
    from fadada_api.models import *
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    import requests


class FadadaBatchSigner:
    """法大大批量签署工具"""
    
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
        
        self._token = None
        self.results = []
        self.errors = []
    
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
    
    def load_batch_data(self, input_path: str) -> List[Dict]:
        """加载批量数据"""
        print(f"加载数据文件: {input_path}")
        
        if PANDAS_AVAILABLE:
            if input_path.endswith('.xlsx') or input_path.endswith('.xls'):
                df = pd.read_excel(input_path)
            else:
                df = pd.read_csv(input_path, encoding='utf-8')
            
            # 将 NaN 替换为空字符串
            df = df.fillna('')
            records = df.to_dict('records')
        else:
            records = []
            with open(input_path, 'r', encoding='utf-8') as f:
                if input_path.endswith('.csv'):
                    reader = csv.DictReader(f)
                    for row in reader:
                        records.append(row)
                else:
                    raise Exception("未安装 pandas，仅支持 CSV 格式")
        
        print(f"加载了 {len(records)} 条记录")
        return records
    
    def upload_file(self, file_path: str) -> str:
        """上传文件"""
        token = self._get_access_token()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        print(f"上传文件: {file_name}")
        
        if SDK_AVAILABLE:
            upload_info = self.doc_client.get_file_upload_url(
                access_token=token,
                file_name=file_name,
                file_size=file_size
            )
            upload_url = upload_info.data.upload_url
            file_id = upload_info.data.file_id
            
            with open(file_path, 'rb') as f:
                requests.put(upload_url, data=f)
            
            return file_id
        else:
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
            
            with open(file_path, 'rb') as f:
                requests.put(upload_url, data=f)
            
            return file_id
    
    def create_single_task(self, record: Dict, template_id: Optional[str] = None, file_id: Optional[str] = None) -> Dict:
        """创建单个签署任务"""
        token = self._get_access_token()
        
        # 提取任务信息
        client_task_id = record.get('client_task_id') or f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{record.get('index', 0)}"
        task_subject = record.get('task_subject', '批量签署任务')
        
        # 提取签署人信息
        signer = {
            "client_user_id": record.get('signer_user_id'),
            "signer_type": record.get('signer_type', 'PERSONAL'),
            "sign_type": record.get('sign_type', 'POSITION'),
            "sign_order": int(record.get('signer_order', 1)) if record.get('signer_order') else 1
        }
        
        if signer["sign_type"] == "POSITION":
            signer["sign_position"] = {
                "page": int(record.get('signer_page', 1)),
                "x": float(record.get('signer_x', 100)),
                "y": float(record.get('signer_y', 200)),
                "seal_id": record.get('signer_seal_id', '')
            }
        elif signer["sign_type"] == "KEYWORD":
            signer["sign_keyword"] = {
                "keyword": record.get('signer_keyword', '签名'),
                "match_strategy": record.get('signer_match_strategy', 'FIRST')
            }
        
        # 构建请求
        if template_id:
            # 模板模式 - 提取所有 field_ 开头的字段
            fill_values = []
            for key, value in record.items():
                if key.startswith('field_') and value:
                    field_id = key.replace('field_', '')
                    fill_values.append({
                        "field_id": field_id,
                        "field_value": str(value)
                    })
            
            payload = {
                "access_token": token,
                "client_task_id": client_task_id,
                "task_subject": task_subject,
                "template_id": template_id,
                "template_fill_values": fill_values,
                "signers": [signer],
                "callback_url": self.callback_url
            }
        else:
            # 文件模式
            payload = {
                "access_token": token,
                "client_task_id": client_task_id,
                "task_subject": task_subject,
                "file_id": file_id,
                "signers": [signer],
                "callback_url": self.callback_url
            }
        
        # 调用 API
        if SDK_AVAILABLE:
            create_req = CreateSignTaskReq()
            for key, value in payload.items():
                setattr(create_req, key, value)
            
            response = self.sign_task_client.create_sign_task(create_req)
            return {
                "success": True,
                "client_task_id": client_task_id,
                "task_id": response.data.task_id,
                "status": response.data.task_status
            }
        else:
            url = f"{self.server_url}/sign-task/create-sign-task"
            response = requests.post(url, json=payload)
            result = response.json()
            
            if result.get("code") != "0":
                return {
                    "success": False,
                    "client_task_id": client_task_id,
                    "error": result.get('message', 'Unknown error'),
                    "error_code": result.get('code')
                }
            
            return {
                "success": True,
                "client_task_id": client_task_id,
                "task_id": result["data"]["task_id"],
                "status": result["data"]["task_status"]
            }
    
    def process_batch(
        self,
        records: List[Dict],
        template_id: Optional[str] = None,
        file_id: Optional[str] = None,
        max_workers: int = 5,
        delay: float = 0.5
    ):
        """批量处理"""
        print(f"\n开始批量创建签署任务...")
        print(f"并发数: {max_workers}, 任务间延迟: {delay}秒")
        print("-" * 60)
        
        total = len(records)
        completed = 0
        failed = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_record = {}
            for idx, record in enumerate(records):
                record['index'] = idx
                # 添加延迟避免请求过快
                if idx > 0 and delay > 0:
                    time.sleep(delay)
                
                future = executor.submit(self.create_single_task, record, template_id, file_id)
                future_to_record[future] = record
            
            # 处理结果
            for future in as_completed(future_to_record):
                record = future_to_record[future]
                try:
                    result = future.result()
                    if result["success"]:
                        self.results.append(result)
                        completed += 1
                        print(f"✓ [{completed}/{total}] {result['client_task_id']} -> {result['task_id']}")
                    else:
                        self.errors.append({
                            "record": record,
                            "error": result.get("error"),
                            "error_code": result.get("error_code")
                        })
                        failed += 1
                        print(f"✗ [{failed}] {result['client_task_id']}: {result.get('error')}")
                except Exception as e:
                    failed += 1
                    self.errors.append({
                        "record": record,
                        "error": str(e)
                    })
                    print(f"✗ [{failed}] {record.get('client_task_id')}: {e}")
        
        print("-" * 60)
        print(f"批量处理完成: 成功 {completed}, 失败 {failed}, 总计 {total}")
    
    def generate_report(self, output_path: str):
        """生成报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total": len(self.results) + len(self.errors),
                "success": len(self.results),
                "failed": len(self.errors)
            },
            "successful_tasks": self.results,
            "failed_tasks": self.errors
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_path}")
        
        # 同时生成 CSV 报告
        if PANDAS_AVAILABLE and self.results:
            csv_path = output_path.replace('.json', '_success.csv')
            df = pd.DataFrame(self.results)
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"成功任务 CSV: {csv_path}")


def create_sample_excel(output_path: str):
    """创建示例 Excel 文件"""
    if not PANDAS_AVAILABLE:
        print("错误: 需要安装 pandas 才能创建示例文件")
        print("pip install pandas openpyxl")
        return
    
    # 模板模式示例数据
    template_data = [
        {
            "client_task_id": "task_001",
            "task_subject": "服务协议 - 张三",
            "signer_user_id": "user_zhangsan",
            "signer_type": "PERSONAL",
            "sign_type": "POSITION",
            "signer_page": 1,
            "signer_x": 100,
            "signer_y": 200,
            "field_party_a": "甲方科技有限公司",
            "field_party_b": "张三",
            "field_amount": "10000",
            "field_date": "2024-03-27"
        },
        {
            "client_task_id": "task_002",
            "task_subject": "服务协议 - 李四",
            "signer_user_id": "user_lisi",
            "signer_type": "PERSONAL",
            "sign_type": "POSITION",
            "signer_page": 1,
            "signer_x": 100,
            "signer_y": 200,
            "field_party_a": "甲方科技有限公司",
            "field_party_b": "李四",
            "field_amount": "20000",
            "field_date": "2024-03-27"
        }
    ]
    
    df = pd.DataFrame(template_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"示例文件已创建: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="法大大批量签署工具")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--input", required=True, help="批量数据文件 (Excel 或 CSV)")
    parser.add_argument("--template", help="模板 ID (模板模式)")
    parser.add_argument("--file", help="合同文件路径 (文件模式)")
    parser.add_argument("--output", default="batch_report.json", help="输出报告路径")
    parser.add_argument("--workers", type=int, default=5, help="并发数 (默认: 5)")
    parser.add_argument("--delay", type=float, default=0.5, help="任务间延迟 (秒, 默认: 0.5)")
    parser.add_argument("--create-sample", help="创建示例 Excel 文件")
    
    args = parser.parse_args()
    
    # 创建示例文件
    if args.create_sample:
        create_sample_excel(args.create_sample)
        return
    
    # 验证参数
    if not args.template and not args.file:
        print("错误: 请提供 --template (模板模式) 或 --file (文件模式)")
        sys.exit(1)
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 创建批量签署器
    batch_signer = FadadaBatchSigner(config)
    
    try:
        # 加载数据
        records = batch_signer.load_batch_data(args.input)
        
        if not records:
            print("错误: 数据文件为空")
            sys.exit(1)
        
        # 文件模式需要上传文件
        file_id = None
        if args.file:
            file_id = batch_signer.upload_file(args.file)
        
        # 批量处理
        batch_signer.process_batch(
            records=records,
            template_id=args.template,
            file_id=file_id,
            max_workers=args.workers,
            delay=args.delay
        )
        
        # 生成报告
        batch_signer.generate_report(args.output)
        
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
