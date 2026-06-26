# C07 - Notion

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C07 |
| 连接器名 | notion |
| 显示名 | Notion |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 文档/知识库 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 页面管理 | 创建/查询/更新页面 |
| 数据库 | 查询/创建数据库记录 |
| Block 操作 | 添加/更新/删除 Block |
| 搜索 | 全文搜索 |
| 评论 | 添加/查询评论 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L2-auth-docs-kb-C07-notion-create-page.py
└── L2-auth-docs-kb-C07-notion-query-database.py
```

### 鉴权方式

**Internal Integration Token（推荐）**：
1. 在 Notion 设置中创建 Integration
2. 获取 Internal Integration Token
3. 在页面/数据库中添加 Integration

**OAuth2（应用分发）**：
1. 在 Notion 开发者中心创建 OAuth 应用
2. 获取 `client_id` + `client_secret`
3. 用户授权获取 `access_token`

**环境变量配置**：
```bash
# Internal Integration
export NOTION_TOKEN="secret_xxxxxxxxxxxxxxxx"

# OAuth2
export NOTION_CLIENT_ID="your_client_id"
export NOTION_CLIENT_SECRET="your_client_secret"
```

### 核心脚本示例

**L2-auth-docs-kb-C07-notion-query-database.py**：
```python
#!/usr/bin/env python3
"""查询 Notion 数据库"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def get_headers() -> dict:
    """获取请求头"""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("未设置 NOTION_TOKEN 环境变量")
    
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def query_database(database_id: str, filter_obj: dict = None, 
                  sorts: list = None, page_size: int = 100) -> dict:
    """查询数据库"""
    headers = get_headers()
    
    payload = {
        "page_size": page_size
    }
    
    if filter_obj:
        payload["filter"] = filter_obj
    
    if sorts:
        payload["sorts"] = sorts
    
    resp = requests.post(
        f"{API_BASE}/databases/{database_id}/query",
        headers=headers,
        json=payload
    )
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    results = data.get("results", [])
    
    if not results:
        return "没有找到记录"
    
    output = f"## 查询结果（{len(results)} 条）\n\n"
    
    # 提取属性名
    if results:
        properties = results[0].get("properties", {})
        prop_names = list(properties.keys())
        
        # 表格头
        output += "| " + " | ".join(prop_names) + " |\n"
        output += "| " + " | ".join(["---"] * len(prop_names)) + " |\n"
        
        # 表格内容
        for result in results[:10]:  # 最多显示 10 条
            properties = result.get("properties", {})
            row = []
            for prop_name in prop_names:
                prop = properties.get(prop_name, {})
                value = extract_property_value(prop)
                row.append(str(value))
            output += "| " + " | ".join(row) + " |\n"
    
    return output

def extract_property_value(property: dict) -> str:
    """提取属性值"""
    prop_type = property.get("type")
    
    if prop_type == "title":
        title_array = property.get("title", [])
        return title_array[0].get("plain_text", "") if title_array else ""
    elif prop_type == "rich_text":
        text_array = property.get("rich_text", [])
        return text_array[0].get("plain_text", "") if text_array else ""
    elif prop_type == "number":
        return str(property.get("number", ""))
    elif prop_type == "select":
        select = property.get("select")
        return select.get("name", "") if select else ""
    elif prop_type == "multi_select":
        multi_select = property.get("multi_select", [])
        return ", ".join([s.get("name", "") for s in multi_select])
    elif prop_type == "date":
        date = property.get("date")
        return date.get("start", "") if date else ""
    elif prop_type == "checkbox":
        return "✓" if property.get("checkbox") else "✗"
    elif prop_type == "url":
        return property.get("url", "")
    elif prop_type == "email":
        return property.get("email", "")
    elif prop_type == "phone_number":
        return property.get("phone_number", "")
    else:
        return f"[{prop_type}]"

def main():
    parser = argparse.ArgumentParser(description="查询 Notion 数据库")
    parser.add_argument("database_id", help="数据库 ID")
    parser.add_argument("--filter", help="过滤条件（JSON 格式）")
    parser.add_argument("--sorts", help="排序条件（JSON 格式）")
    parser.add_argument("--page-size", type=int, default=100, help="每页数量")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        filter_obj = json.loads(args.filter) if args.filter else None
        sorts = json.loads(args.sorts) if args.sorts else None
        
        data = query_database(args.database_id, filter_obj, sorts, args.page_size)
        
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

**L2-auth-docs-kb-C07-notion-create-page.py**：
```python
#!/usr/bin/env python3
"""创建 Notion 页面"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def get_headers() -> dict:
    """获取请求头"""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise ValueError("未设置 NOTION_TOKEN 环境变量")
    
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

def create_page(parent_id: str, parent_type: str = "page_id", 
               title: str = "", content: str = "") -> dict:
    """创建页面"""
    headers = get_headers()
    
    # 构建父级
    if parent_type == "page_id":
        parent = {"page_id": parent_id}
    else:
        parent = {"database_id": parent_id}
    
    # 构建属性
    properties = {}
    if title:
        properties["title"] = {
            "title": [
                {
                    "text": {
                        "content": title
                    }
                }
            ]
        }
    
    # 构建内容
    children = []
    if content:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        })
    
    payload = {
        "parent": parent,
        "properties": properties,
        "children": children
    }
    
    resp = requests.post(f"{API_BASE}/pages", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
页面创建成功：

| 字段 | 值 |
|------|-----|
| 页面 ID | {data.get('id', '-')} |
| 链接 | {data.get('url', '-')} |
| 创建时间 | {data.get('created_time', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建 Notion 页面")
    parser.add_argument("parent_id", help="父级页面/数据库 ID")
    parser.add_argument("--type", choices=["page_id", "database_id"], default="page_id")
    parser.add_argument("--title", help="页面标题")
    parser.add_argument("--content", help="页面内容")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_page(args.parent_id, args.type, args.title, args.content)
        
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

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | Notion API 稳定 |
| 凭证更新 | 重新创建 Integration |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 数据处理 | 原样返回 | 可清洗/转换 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 Token |
