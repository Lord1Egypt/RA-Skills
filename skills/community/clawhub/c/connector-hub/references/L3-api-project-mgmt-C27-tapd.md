# C27 - TAPD

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C27 |
| 连接器名 | tapd |
| 显示名 | TAPD |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 项目管理 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 需求管理 | 创建/查询/更新需求 |
| Bug 管理 | 创建/查询/更新 Bug |
| 迭代管理 | 迭代规划/进度跟踪 |
| 工时管理 | 工时记录/统计 |
| 报表统计 | 迭代报告/燃尽图 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-project-mgmt-C27-tapd-create-story.py  # 创建需求
└── L3-api-project-mgmt-C27-tapd-create-bug.py    # 创建 Bug
```

### 鉴权方式

**Basic Auth**：
1. 在 TAPD 项目设置中获取 API Token
2. 请求头添加 `Authorization: Basic {base64(workspace_id:token)}`

**环境变量配置**：
```bash
export TAPD_WORKSPACE_ID="your_workspace_id"
export TAPD_API_TOKEN="your_api_token"
```

### 核心脚本示例

**L3-api-project-mgmt-C27-tapd-create-story.py**：
```python
#!/usr/bin/env python3
"""创建 TAPD 需求"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://api.tapd.cn/stories"

def create_story(title: str, description: str = "", priority: str = "2", owner: str = "") -> dict:
    """创建需求"""
    auth = AuthManager("tapd")
    
    workspace_id = os.environ["TAPD_WORKSPACE_ID"]
    api_token = os.environ["TAPD_API_TOKEN"]
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "workspace_id": workspace_id,
        "name": title,
        "description": description or f"需求：{title}",
        "priority": priority,  # 1-紧急 2-高 3-中 4-低
        "owner": owner,
        "status": "planning"  # planning/developing/testing/closed
    }
    
    resp = requests.post(
        API_BASE,
        headers=headers,
        json=payload,
        auth=(workspace_id, api_token)
    )
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    story = data.get("Story", {})
    return f"""
需求创建成功：

| 字段 | 值 |
|------|-----|
| ID | {story.get('id', '-')} |
| 标题 | {story.get('name', '-')} |
| 状态 | {story.get('status', '-')} |
| 优先级 | {story.get('priority', '-')} |
| 负责人 | {story.get('owner', '-')} |
| 创建时间 | {story.get('created', '-')} |
| 链接 | https://www.tapd.cn/{story.get('workspace_id')}/stories/view/{story.get('id')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建 TAPD 需求")
    parser.add_argument("title", help="需求标题")
    parser.add_argument("--desc", help="需求描述")
    parser.add_argument("--priority", choices=["1", "2", "3", "4"], default="2", help="优先级")
    parser.add_argument("--owner", help="负责人")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_story(args.title, args.desc, args.priority, args.owner)
        
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

**L3-api-project-mgmt-C27-tapd-create-bug.py**：
```python
#!/usr/bin/env python3
"""创建 TAPD Bug"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://api.tapd.cn/bugs"

def create_bug(title: str, description: str = "", severity: str = "normal", 
               priority: str = "2", owner: str = "", module: str = "") -> dict:
    """创建 Bug"""
    workspace_id = os.environ["TAPD_WORKSPACE_ID"]
    api_token = os.environ["TAPD_API_TOKEN"]
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "workspace_id": workspace_id,
        "title": title,
        "description": description or f"Bug：{title}",
        "severity": severity,  # fatal/serious/normal/slight
        "priority": priority,  # 1-紧急 2-高 3-中 4-低
        "owner": owner,
        "module": module,
        "status": "open"  # open/resolved/closed
    }
    
    resp = requests.post(
        API_BASE,
        headers=headers,
        json=payload,
        auth=(workspace_id, api_token)
    )
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    bug = data.get("Bug", {})
    return f"""
Bug 创建成功：

| 字段 | 值 |
|------|-----|
| ID | {bug.get('id', '-')} |
| 标题 | {bug.get('title', '-')} |
| 严重程度 | {bug.get('severity', '-')} |
| 优先级 | {bug.get('priority', '-')} |
| 状态 | {bug.get('status', '-')} |
| 负责人 | {bug.get('owner', '-')} |
| 创建时间 | {bug.get('created', '-')} |
| 链接 | https://www.tapd.cn/{bug.get('workspace_id')}/bugs/view/{bug.get('id')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建 TAPD Bug")
    parser.add_argument("title", help="Bug 标题")
    parser.add_argument("--desc", help="Bug 描述")
    parser.add_argument("--severity", choices=["fatal", "serious", "normal", "slight"], default="normal")
    parser.add_argument("--priority", choices=["1", "2", "3", "4"], default="2")
    parser.add_argument("--owner", help="负责人")
    parser.add_argument("--module", help="模块")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_bug(args.title, args.desc, args.severity, args.priority, args.owner, args.module)
        
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
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新获取 API Token |
| 工作流 | 无需修改 |
| 字段映射 | 可能需要调整字段名 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义字段 |
| 数据处理 | 原样返回 | 可生成报告 |
| 多平台 | 绑定 TAPD | 可对接其他平台 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
