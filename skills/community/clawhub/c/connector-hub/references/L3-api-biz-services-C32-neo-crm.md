# C32 - 销售易 CRM

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C32 |
| 连接器名 | neo-crm |
| 显示名 | 销售易 CRM |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 业务服务 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 客户管理 | 创建/查询/更新客户 |
| 线索管理 | 线索录入/转化跟踪 |
| 商机管理 | 商机创建/阶段推进 |
| 联系人 | 联系人信息管理 |
| 销售报表 | 销售漏斗/业绩统计 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-biz-services-C32-neo-crm-create-lead.py     # 创建线索
└── L3-api-biz-services-C32-neo-crm-query-pipeline.py  # 查询销售漏斗
```

### 鉴权方式

**OAuth2**：
1. 在销售易开放平台创建应用
2. 获取 `client_id` + `client_secret`
3. 用户授权获取 `access_token`
4. Token 有效期 2 小时

**环境变量配置**：
```bash
export NEO_CRM_CLIENT_ID="your_client_id"
export NEO_CRM_CLIENT_SECRET="your_client_secret"
```

### 核心脚本示例

**L3-api-biz-services-C32-neo-crm-create-lead.py**：
```python
#!/usr/bin/env python3
"""创建销售线索"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://open.neocrm.com/api/v1"

def get_headers() -> dict:
    """获取请求头"""
    auth = AuthManager("neo-crm")
    token = auth.get_oauth_token(
        client_id=os.environ["NEO_CRM_CLIENT_ID"],
        client_secret=os.environ["NEO_CRM_CLIENT_SECRET"],
        token_url=f"{API_BASE}/oauth/token"
    )
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def create_lead(name: str, company: str, phone: str = "", email: str = "", 
               source: str = "", description: str = "") -> dict:
    """创建线索"""
    headers = get_headers()
    
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
```

**L3-api-biz-services-C32-neo-crm-query-pipeline.py**：
```python
#!/usr/bin/env python3
"""查询销售漏斗"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://open.neocrm.com/api/v1"

def get_headers() -> dict:
    """获取请求头"""
    auth = AuthManager("neo-crm")
    token = auth.get_oauth_token(
        client_id=os.environ["NEO_CRM_CLIENT_ID"],
        client_secret=os.environ["NEO_CRM_CLIENT_SECRET"],
        token_url=f"{API_BASE}/oauth/token"
    )
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def query_pipeline(user_id: str = None, date_range: str = "month") -> dict:
    """查询销售漏斗"""
    headers = get_headers()
    
    params = {
        "date_range": date_range  # week, month, quarter, year
    }
    
    if user_id:
        params["user_id"] = user_id
    
    resp = requests.get(f"{API_BASE}/pipeline", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    stages = data.get("stages", [])
    
    output = "## 销售漏斗\n\n"
    output += "| 阶段 | 商机数 | 金额（¥） | 转化率 |\n"
    output += "|------|--------|----------|--------|\n"
    
    total_amount = 0
    for stage in stages:
        amount = stage.get("amount", 0)
        total_amount += amount
        output += f"| {stage.get('name', '-')} | {stage.get('count', 0)} | ¥{amount:,.2f} | {stage.get('conversion_rate', '-')} |\n"
    
    output += f"\n**总金额：¥{total_amount:,.2f}**\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询销售漏斗")
    parser.add_argument("--user-id", help="用户 ID")
    parser.add_argument("--date-range", choices=["week", "month", "quarter", "year"], default="month")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = query_pipeline(args.user_id, args.date_range)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"查询失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新申请应用凭证 |
| 工作流 | 无需修改 |
| 字段映射 | 可能需要调整字段名 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义字段 |
| 数据处理 | 原样返回 | 可生成报表 |
| 多平台 | 绑定销售易 | 可对接纷享销客等 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
