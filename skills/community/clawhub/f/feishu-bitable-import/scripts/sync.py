#!/usr/bin/env python3
"""
飞书多维表格数据同步脚本
支持增量同步、全量覆盖、仅新增三种模式
自动推断数据类型，自动创建缺失字段
"""

import argparse
import json
import os
import time
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

APP_ID = os.getenv("FEISHU_APP_ID")
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

class FeishuBitableSync:
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or APP_ID
        self.app_secret = app_secret or APP_SECRET
        self.access_token = None
        self.token_expire_time = 0
        
    def get_access_token(self) -> str:
        """获取飞书访问令牌"""
        now = int(time.time())
        if self.access_token and now < self.token_expire_time:
            return self.access_token
            
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, json=data, timeout=10).json()
        if resp.get("code") != 0:
            raise Exception(f"获取token失败: {resp}")
        self.access_token = resp["tenant_access_token"]
        self.token_expire_time = now + resp["expire"] - 300
        return self.access_token
    
    def request(self, method: str, url: str, **kwargs) -> Dict:
        """发送请求，自动带token"""
        token = self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json; charset=utf-8"
        kwargs["headers"] = headers
        
        for i in range(3):  # 重试3次
            try:
                resp = requests.request(method, url, timeout=30, **kwargs).json()
                if resp.get("code") == 0:
                    return resp
                if resp.get("code") == 99991400:  # 限流
                    time.sleep(5)
                    continue
                raise Exception(f"API错误: {resp}")
            except requests.exceptions.Timeout:
                time.sleep(2)
                continue
        raise Exception("重试次数过多")
    
    def get_table_meta(self, app_token: str, table_id: str) -> Dict:
        """获取表格元数据"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        resp = self.request("GET", url)
        return {f["field_name"]: f for f in resp["data"]["items"]}
    
    def create_field(self, app_token: str, table_id: str, name: str, type_id: int) -> Dict:
        """创建新字段"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        data = {
            "field_name": name,
            "type": type_id,
        }
        resp = self.request("POST", url, json=data)
        return resp["data"]
    
    def list_records(self, app_token: str, table_id: str) -> List[Dict]:
        """获取所有现有记录"""
        records = []
        page_token = None
        
        while True:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
            params = {"page_size": 500}
            if page_token:
                params["page_token"] = page_token
            resp = self.request("GET", url, params=params)
            records.extend(resp["data"]["items"])
            
            if not resp["data"]["has_more"]:
                break
            page_token = resp["data"]["page_token"]
            
        return records
    
    def create_record(self, app_token: str, table_id: str, fields: Dict) -> Dict:
        """创建一条记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        data = {"fields": fields}
        return self.request("POST", url, json=data)
    
    def update_record(self, app_token: str, table_id: str, record_id: str, fields: Dict) -> Dict:
        """更新一条记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        data = {"fields": fields}
        return self.request("PUT", url, json=data)
    
    def delete_record(self, app_token: str, table_id: str, record_id: str) -> Dict:
        """删除一条记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        return self.request("DELETE", url)
    
    @staticmethod
    def infer_field_type(values: List[Any]) -> int:
        """根据列数据推断飞书字段类型
        
        类型ID参考:
        1: Text, 2: Number, 3: SingleSelect, 4: MultiSelect, 5: DateTime, 
        7: Checkbox, 11: User, 13: Phone, 15: URL
        """
        # 过滤空值
        valid_values = [v for v in values if pd.notna(v)]
        if not valid_values:
            return 1  # 默认文本
        
        # 统计唯一值
        unique_values = set(str(v) for v in valid_values)
        
        # 复选框检测: 只有是/否、真/假、Y/N等
        checkbox_patterns = {'是', '否', '真', '假', 'y', 'n', 'yes', 'no', 'true', 'false', '1', '0'}
        if all(str(v).lower() in checkbox_patterns for v in valid_values):
            return 7
        
        # 手机号检测
        phone_pattern = re.compile(r'^1[3-9]\d{9}$')
        if all(phone_pattern.match(str(v).strip()) for v in valid_values if str(v).strip()):
            return 13
        
        # URL检测
        url_pattern = re.compile(r'^https?://')
        if all(url_pattern.match(str(v).strip()) for v in valid_values if str(v).strip()):
            return 15
        
        # 日期检测
        date_patterns = [
            r'^\d{4}-\d{1,2}-\d{1,2}',  # 2023-01-15
            r'^\d{4}/\d{1,2}/\d{1,2}',   # 2023/01/15
            r'^\d{1,2}/\d{1,2}/\d{4}',   # 01/15/2023
        ]
        date_count = sum(1 for v in valid_values if any(re.match(p, str(v)) for p in date_patterns))
        if date_count / len(valid_values) > 0.8:
            return 5
        
        # 数字检测
        try:
            numeric_count = 0
            for v in valid_values:
                float(str(v).replace(',', ''))
                numeric_count += 1
            if numeric_count / len(valid_values) > 0.8:
                return 2
        except:
            pass
        
        # 单选检测: 唯一值少，重复率高
        if len(unique_values) <= 20 and len(unique_values) / len(valid_values) < 0.3:
            return 3
        
        # 多选检测: 包含逗号或分号分隔
        if any(',' in str(v) or ';' in str(v) for v in valid_values):
            return 4
        
        # 默认文本
        return 1
    
    @staticmethod
    def convert_value(value: Any, field_type: int) -> Any:
        """转换值为飞书格式"""
        if pd.isna(value):
            return ""
        
        if field_type == 5:  # DateTime
            if isinstance(value, datetime):
                return int(value.timestamp() * 1000)
            return str(value)  # 飞书会自动解析
        
        if field_type == 2:  # Number
            if isinstance(value, str):
                return float(value.replace(',', ''))
            return value
        
        if field_type == 7:  # Checkbox
            return str(value).lower() in {'是', '真', 'y', 'yes', 'true', '1'}
        
        return str(value)
    
    def sync(
        self,
        df: pd.DataFrame,
        app_token: str,
        table_id: str,
        mode: str = "incremental",
        primary_key: str = None,
    ) -> Dict:
        """
        同步数据
        
        Args:
            df: 数据框
            app_token: 飞书应用token
            table_id: 表格ID
            mode: incremental(增量)/full(全量)/append(仅新增)
            primary_key: 主键列名，用于匹配已有记录
        """
        stats = {"created": 0, "updated": 0, "deleted": 0, "fields_created": 0}
        
        # 1. 获取现有字段
        existing_fields = self.get_table_meta(app_token, table_id)
        print(f"现有字段: {len(existing_fields)} 个")
        
        # 2. 自动创建缺失字段
        for col in df.columns:
            if col not in existing_fields:
                # 推断类型
                type_id = self.infer_field_type(df[col].tolist())
                print(f"自动创建字段: {col} (类型ID: {type_id})")
                self.create_field(app_token, table_id, col, type_id)
                stats["fields_created"] += 1
                # 刷新字段列表
                existing_fields = self.get_table_meta(app_token, table_id)
        
        # 3. 全量覆盖模式: 删除所有现有记录
        if mode == "full":
            existing_records = self.list_records(app_token, table_id)
            print(f"全量覆盖: 删除现有 {len(existing_records)} 条记录")
            for record in existing_records:
                self.delete_record(app_token, table_id, record["record_id"])
                stats["deleted"] += 1
        
        # 4. 增量/增量模式: 获取现有记录建立索引
        existing_records_map = {}
        if mode == "incremental" and primary_key:
            existing_records = self.list_records(app_token, table_id)
            for record in existing_records:
                pk_value = str(record["fields"].get(primary_key, "")).strip()
                if pk_value:
                    existing_records_map[pk_value] = record["record_id"]
            print(f"增量同步: 已索引 {len(existing_records_map)} 条现有记录")
        
        # 5. 逐行插入/更新
        for _, row in df.iterrows():
            fields = {}
            for col in df.columns:
                field_meta = existing_fields.get(col)
                if not field_meta:
                    continue
                value = self.convert_value(row[col], field_meta["type"])
                fields[col] = value
            
            if mode == "incremental" and primary_key:
                pk_value = str(row[primary_key]).strip()
                if pk_value in existing_records_map:
                    # 更新
                    self.update_record(app_token, table_id, existing_records_map[pk_value], fields)
                    stats["updated"] += 1
                else:
                    # 新增
                    self.create_record(app_token, table_id, fields)
                    stats["created"] += 1
            else:
                # 新增
                self.create_record(app_token, table_id, fields)
                stats["created"] += 1
            
            # 限流，每50条休息一下
            if (stats["created"] + stats["updated"]) % 50 == 0:
                time.sleep(2)
        
        return stats


def main():
    parser = argparse.ArgumentParser(description='同步数据到飞书多维表格')
    parser.add_argument('--input', required=True, help='输入文件: .csv .xlsx .json')
    parser.add_argument('--app-token', required=True, help='飞书 app_token')
    parser.add_argument('--table-id', required=True, help='飞书 table_id')
    parser.add_argument('--mode', default='incremental', choices=['incremental', 'full', 'append'], 
                       help='同步模式: incremental增量/full全量/append仅新增')
    parser.add_argument('--primary-key', help='主键列名(增量同步需要)')
    parser.add_argument('--sheet-name', help='Excel sheet 名称(可选)')
    args = parser.parse_args()
    
    # 读取数据
    input_path = args.input
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path, dtype=str)
    elif input_path.endswith('.xlsx') or input_path.endswith('.xls'):
        if args.sheet_name:
            df = pd.read_excel(input_path, sheet_name=args.sheet_name, dtype=str)
        else:
            df = pd.read_excel(input_path, dtype=str)
    elif input_path.endswith('.json'):
        df = pd.read_json(input_path)
    else:
        raise Exception("不支持的文件格式，请使用 .csv .xlsx .json")
    
    print(f"读取数据完成: {len(df)} 行 × {len(df.columns)} 列")
    
    # 检查环境变量
    if not APP_ID or not APP_SECRET:
        raise Exception("请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    
    # 执行同步
    sync = FeishuBitableSync()
    stats = sync.sync(df, args.app_token, args.table_id, args.mode, args.primary_key)
    
    print("\n✅ 同步完成!")
    print(f"- 新增: {stats['created']} 条")
    print(f"- 更新: {stats['updated']} 条")
    print(f"- 删除: {stats['deleted']} 条")
    print(f"- 自动创建字段: {stats['fields_created']} 个")


if __name__ == "__main__":
    main()
