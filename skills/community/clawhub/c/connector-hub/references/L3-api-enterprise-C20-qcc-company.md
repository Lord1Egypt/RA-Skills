# C20 - 企查查

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C20 |
| 连接器名 | qcc-company |
| 显示名 | 企查查 |
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

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L3-api-enterprise-C20-qcc-query-basic.py  # 查询企业基础信息
```

### 鉴权方式

**动态 Token**（基于时间戳 + MD5）：
1. 在企查查开放平台 (https://openapi.qcc.com) 注册并完成企业认证
2. 获取 `AppKey` 和 `SecretKey`
3. 生成动态 Token：
   - 拼接字符串：`AppKey + timestamp + SecretKey`
   - 对字符串进行 MD5 加密并转大写
   - 将 Token 和 timestamp 放入请求头

**环境变量配置**：
```bash
export QCC_APP_KEY="your_app_key"
export QCC_SECRET_KEY="your_secret_key"
```

### 核心脚本示例

**L3-api-enterprise-C20-qcc-query-basic.py**：
```python
#!/usr/bin/env python3
"""查询企业基础信息"""

import os
import sys
import json
import time
import hashlib
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://api.qichacha.com"

def generate_token(app_key: str, secret_key: str) -> tuple:
    """生成动态 Token"""
    timestamp = str(int(time.time()))
    raw_str = f"{app_key}{timestamp}{secret_key}"
    token = hashlib.md5(raw_str.encode()).hexdigest().upper()
    return token, timestamp

def query_basic(keyword: str) -> dict:
    """查询企业基础信息"""
    app_key = os.environ["QCC_APP_KEY"]
    secret_key = os.environ["QCC_SECRET_KEY"]
    
    token, timestamp = generate_token(app_key, secret_key)
    
    headers = {
        "Token": token,
        "Timespan": timestamp
    }
    
    params = {
        "key": app_key,
        "searchKey": keyword
    }
    
    resp = requests.get(f"{API_BASE}/FuzzySearch/GetList", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    results = data.get("Result", [])
    if not results:
        return "未找到企业信息"
    
    result = results[0]
    return f"""
| 字段 | 值 |
|------|-----|
| 企业名称 | {result.get('Name', '-')} |
| 统一社会信用代码 | {result.get('CreditCode', '-')} |
| 法定代表人 | {result.get('OperName', '-')} |
| 注册资本 | {result.get('RegistCapi', '-')} |
| 成立日期 | {result.get('StartDate', '-')} |
| 经营状态 | {result.get('Status', '-')} |
| 所属行业 | {result.get('Industry', '-')} |
| 注册地址 | {result.get('Address', '-')} |
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

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新获取 AppKey 和 SecretKey |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |
