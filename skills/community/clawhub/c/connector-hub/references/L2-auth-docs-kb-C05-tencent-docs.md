# C05 - 腾讯文档

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C05 |
| 连接器名 | tencent-docs |
| 显示名 | 腾讯文档 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 文档/知识库 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 创建文档 | Word/Excel/PPT |
| 编辑文档 | 内容读写 |
| 分享文档 | 权限管理 |
| 导出文档 | 下载为文件 |
| 评论协作 | 多人协作 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L2-auth-docs-kb-C05-tencent-docs-create-doc.py  # 创建文档
```

### 鉴权方式

**OAuth2（推荐）**：
1. 在腾讯文档开放合作平台 (https://docs.qq.com/open) 注册开发者
2. 创建应用并获取 `client_id` + `client_secret`
3. 引导用户授权：`https://docs.qq.com/oauth/v2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=all`
4. 用授权码换取访问令牌：`GET https://docs.qq.com/oauth/v2/token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code&code={code}`
5. 获取 `access_token` + `refresh_token` + `user_id`（Open-Id）
6. 调用业务 API 时在请求头携带：`Access-Token`、`Client-Id`、`Open-Id`

**环境变量配置**：
```bash
export TENCENT_DOCS_CLIENT_ID="your_client_id"
export TENCENT_DOCS_CLIENT_SECRET="your_client_secret"
```

### 核心脚本示例

**L2-auth-docs-kb-C05-tencent-docs-create-doc.py**：
```python
#!/usr/bin/env python3
"""创建腾讯文档"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://docs.qq.com/openapi/drive/v2"

def create_document(title: str, doc_type: str = "doc", access_token: str = None, 
                   client_id: str = None, open_id: str = None) -> dict:
    """创建文档"""
    if not access_token:
        auth = AuthManager("tencent-docs")
        access_token = auth.get_cached_token()
    
    headers = {
        "Access-Token": access_token,
        "Client-Id": client_id or os.environ["TENCENT_DOCS_CLIENT_ID"],
        "Open-Id": open_id or os.environ.get("TENCENT_DOCS_OPEN_ID", ""),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "title": title,
        "type": doc_type  # doc, sheet, slide
    }
    
    resp = requests.post(f"{API_BASE}/files", headers=headers, data=data)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="创建腾讯文档")
    parser.add_argument("title", help="文档标题")
    parser.add_argument("--type", choices=["doc", "sheet", "slide"], default="doc")
    parser.add_argument("--token", help="访问令牌")
    parser.add_argument("--client-id", help="应用 ID")
    parser.add_argument("--open-id", help="用户 Open-Id")
    
    args = parser.parse_args()
    
    try:
        result = create_document(args.title, args.type, args.token, args.client_id, args.open_id)
        
        if result.get("ret") == 0:
            data = result.get("data", {})
            print(f"文档创建成功：")
            print(f"  标题：{data.get('title')}")
            print(f"  链接：{data.get('url')}")
            print(f"  ID：{data.get('ID')}")
            print(f"  类型：{data.get('type')}")
        else:
            print(f"创建失败：{result.get('msg')}")
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
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

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 单一 API | 可编排多步 |
| 输出 | 原样返回 | 可自定义格式 |
| 迁移 | 重配连接器 | 改 API 地址 |
