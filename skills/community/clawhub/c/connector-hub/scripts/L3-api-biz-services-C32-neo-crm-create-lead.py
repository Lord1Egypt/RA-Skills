#!/usr/bin/env python3
"""创建销售线索（销售易 CRM）"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://open.neocrm.com/api/v1"

def create_lead(name: str, company: str, phone: str = "", email: str = "", 
               source: str = "", description: str = "") -> dict:
    """创建线索
    
    Args:
        name: 联系人姓名
        company: 公司名称
        phone: 电话
        email: 邮箱
        source: 来源
        description: 描述
    
    Returns:
        API 响应
    """
    # 简化实现，实际需要 OAuth2 授权
    access_token = os.environ.get("NEO_CRM_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 NEO_CRM_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": name,
        "company": company,
        "phone": phone,
        "email": email,
        "source": source,
        "description": description or f"线索：{name} - {company}"
    }
    
    resp = requests.post(f"{API_BASE}/leads", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
线索创建成功：

| 字段 | 值 |
|------|-----|
| 线索 ID | {data.get('id', '-')} |
| 姓名 | {data.get('name', '-')} |
| 公司 | {data.get('company', '-')} |
| 电话 | {data.get('phone', '-')} |
| 邮箱 | {data.get('email', '-')} |
| 来源 | {data.get('source', '-')} |
| 创建时间 | {data.get('created_at', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建销售线索")
    parser.add_argument("name", help="联系人姓名")
    parser.add_argument("company", help="公司名称")
    parser.add_argument("--phone", help="电话")
    parser.add_argument("--email", help="邮箱")
    parser.add_argument("--source", help="来源")
    parser.add_argument("--desc", help="描述")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_lead(args.name, args.company, args.phone, args.email, args.source, args.desc)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
