# C19 - 天眼查

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C19 |
| 连接器名 | tyc-mcp |
| 显示名 | 天眼查 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 企业/商业信息查询 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 基础信息 | 企业名称/法人/资本/状态 |
| 司法风险 | 诉讼/失信/被执行 |
| 知识产权 | 专利/商标/软著 |
| 经营信息 | 融资/招投标/进出口 |
| 财务数据 | 年报/财务指标 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L3-api-enterprise-C19-tyc-query-basic.py  # 查询企业基础信息
```

### 鉴权方式

**API Token**：
1. 在天眼查开放平台 (https://open.tianyancha.com) 注册账号
2. 创建应用并获取 Token
3. 请求时将 Token 作为查询参数 `appKey` 传递

**环境变量配置**：
```bash
export TIANYANCHA_TOKEN="your_token"
```

### 核心脚本示例

**L3-api-enterprise-C19-tyc-query-basic.py**：
```python
#!/usr/bin/env python3
"""查询企业基础信息"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://open.tianyancha.com/services/open/ic"

def query_basic(keyword: str) -> dict:
    """查询企业基础信息"""
    auth = AuthManager("tianyancha")
    token = auth.get_api_key()  # 使用环境变量 TIANYANCHA_TOKEN
    
    params = {
        "appKey": token,
        "keyword": keyword
    }
    
    resp = requests.get(f"{API_BASE}/baseinfo", params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    result = data.get("result", {})
    return f"""
| 字段 | 值 |
|------|-----|
| 企业名称 | {result.get('name', '-')} |
| 统一社会信用代码 | {result.get('creditCode', '-')} |
| 法定代表人 | {result.get('legalPersonName', '-')} |
| 注册资本 | {result.get('regCapital', '-')} |
| 成立日期 | {result.get('estiblishTime', '-')} |
| 经营状态 | {result.get('regStatus', '-')} |
| 所属行业 | {result.get('industry', '-')} |
| 注册地址 | {result.get('regLocation', '-')} |
| 经营范围 | {result.get('businessScope', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="查询企业基础信息")
    parser.add_argument("keyword", help="企业名称或统一社会信用代码")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = query_basic(args.keyword)
        
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

**L3-api-enterprise-C19-tyc-query-basic.py**：
```python
#!/usr/bin/env python3
"""查询企业司法风险"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://api.tianyancha.com/services/v3"

def query_judicial(keyword: str) -> dict:
    """查询企业司法风险"""
    auth = AuthManager("tianyancha")
    api_key = auth.get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 先获取企业 ID
    params = {"keyword": keyword}
    resp = requests.get(f"{API_BASE}/company/baseinfo", headers=headers, params=params)
    resp.raise_for_status()
    company_id = resp.json().get("id")
    
    # 查询司法风险
    resp = requests.get(f"{API_BASE}/company/judicial/{company_id}", headers=headers)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    output = "## 司法风险\n\n"
    
    # 诉讼信息
    lawsuits = data.get("lawsuits", [])
    output += f"### 诉讼信息（{len(lawsuits)} 条）\n\n"
    if lawsuits:
        output += "| 案号 | 案由 | 立案日期 | 状态 |\n"
        output += "|------|------|---------|------|\n"
        for item in lawsuits[:5]:
            output += f"| {item.get('case_no', '-')} | {item.get('case_cause', '-')} | {item.get('filing_date', '-')} | {item.get('status', '-')} |\n"
    
    # 失信信息
    dishonest = data.get("dishonest", [])
    output += f"\n### 失信信息（{len(dishonest)} 条）\n\n"
    if dishonest:
        output += "| 失信被执行人 | 执行法院 | 立案日期 |\n"
        output += "|------------|---------|----------|\n"
        for item in dishonest[:5]:
            output += f"| {item.get('name', '-')} | {item.get('court', '-')} | {item.get('filing_date', '-')} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="查询企业司法风险")
    parser.add_argument("keyword", help="企业名称或统一社会信用代码")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = query_judicial(args.keyword)
        
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
| 凭证更新 | 重新申请 API Key |
| 工作流 | 无需修改 |
| 数据格式 | 字段映射可能需要调整 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 查询维度 | 固定 | 可自定义组合 |
| 数据处理 | 原样返回 | 可清洗/转换 |
| 多源验证 | 不支持 | 支持（天眼查+企查查） |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
