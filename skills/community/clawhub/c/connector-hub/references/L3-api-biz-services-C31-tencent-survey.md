# C31 - 腾讯问卷

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C31 |
| 连接器名 | tencent-survey |
| 显示名 | 腾讯问卷 |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 业务服务 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 创建问卷 | 创建各种题型问卷 |
| 发布问卷 | 生成问卷链接 |
| 收集答卷 | 获取问卷回答 |
| 数据分析 | 统计分析答卷数据 |
| 导出数据 | 导出答卷数据 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L3-api-biz-services-C31-tencent-survey-create-survey.py  # 创建问卷
```

### 鉴权方式

**OAuth2**：
1. 在腾讯问卷开放平台创建应用
2. 获取 `app_id` + `app_secret`
3. 用户授权获取 `access_token`
4. Token 有效期 2 小时

**环境变量配置**：
```bash
export TENCENT_SURVEY_APP_ID="your_app_id"
export TENCENT_SURVEY_APP_SECRET="your_app_secret"
```

### 核心脚本示例

**L3-api-biz-services-C31-tencent-survey-create-survey.py**：
```python
#!/usr/bin/env python3
"""创建腾讯问卷"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://wj.qq.com/api/v2"

def get_headers() -> dict:
    """获取请求头"""
    auth = AuthManager("tencent-survey")
    token = auth.get_oauth_token(
        client_id=os.environ["TENCENT_SURVEY_APP_ID"],
        client_secret=os.environ["TENCENT_SURVEY_APP_SECRET"],
        token_url=f"{API_BASE}/oauth/token"
    )
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def create_survey(title: str, questions: list, description: str = "") -> dict:
    """创建问卷"""
    headers = get_headers()
    
    payload = {
        "title": title,
        "description": description or f"问卷：{title}",
        "questions": questions
    }
    
    resp = requests.post(f"{API_BASE}/surveys", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def create_feedback_survey(title: str) -> dict:
    """创建反馈问卷"""
    questions = [
        {
            "type": "radio",
            "title": "您对我们的服务满意吗？",
            "options": ["非常满意", "满意", "一般", "不满意", "非常不满意"],
            "required": True
        },
        {
            "type": "checkbox",
            "title": "您认为我们需要改进哪些方面？",
            "options": ["产品质量", "服务态度", "响应速度", "价格", "其他"],
            "required": False
        },
        {
            "type": "text",
            "title": "您有什么建议？",
            "required": False
        }
    ]
    
    return create_survey(title, questions)

def create_satisfaction_survey(title: str) -> dict:
    """创建满意度调查"""
    questions = [
        {
            "type": "nps",
            "title": "您向朋友推荐我们的可能性有多大？",
            "min": 0,
            "max": 10,
            "required": True
        },
        {
            "type": "radio",
            "title": "您使用我们的产品多久了？",
            "options": ["不到1个月", "1-6个月", "6-12个月", "1年以上"],
            "required": True
        },
        {
            "type": "matrix",
            "title": "请评价以下方面",
            "rows": ["产品质量", "客户服务", "价格合理性", "易用性"],
            "columns": ["非常满意", "满意", "一般", "不满意", "非常不满意"],
            "required": True
        }
    ]
    
    return create_survey(title, questions)

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
问卷创建成功：

| 字段 | 值 |
|------|-----|
| 问卷 ID | {data.get('survey_id', '-')} |
| 标题 | {data.get('title', '-')} |
| 链接 | {data.get('url', '-')} |
| 创建时间 | {data.get('created_at', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建腾讯问卷")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 自定义问卷
    custom_parser = subparsers.add_parser("custom", help="自定义问卷")
    custom_parser.add_argument("title", help="问卷标题")
    custom_parser.add_argument("--questions", required=True, help="问题列表（JSON 格式）")
    custom_parser.add_argument("--desc", help="问卷描述")
    
    # 反馈问卷
    feedback_parser = subparsers.add_parser("feedback", help="反馈问卷")
    feedback_parser.add_argument("title", help="问卷标题")
    
    # 满意度调查
    satisfaction_parser = subparsers.add_parser("satisfaction", help="满意度调查")
    satisfaction_parser.add_argument("title", help="问卷标题")
    
    args = parser.parse_args()
    
    try:
        if args.command == "custom":
            questions = json.loads(args.questions)
            data = create_survey(args.title, questions, args.desc)
        elif args.command == "feedback":
            data = create_feedback_survey(args.title)
        elif args.command == "satisfaction":
            data = create_satisfaction_survey(args.title)
        else:
            parser.print_help()
            return
        
        print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**L3-api-biz-services-C31-tencent-survey-create-survey.py**：
```python
#!/usr/bin/env python3
"""获取问卷答卷"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auth_manager import AuthManager

API_BASE = "https://wj.qq.com/api/v2"

def get_headers() -> dict:
    """获取请求头"""
    auth = AuthManager("tencent-survey")
    token = auth.get_oauth_token(
        client_id=os.environ["TENCENT_SURVEY_APP_ID"],
        client_secret=os.environ["TENCENT_SURVEY_APP_SECRET"],
        token_url=f"{API_BASE}/oauth/token"
    )
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def get_responses(survey_id: str, page: int = 1, page_size: int = 100) -> dict:
    """获取答卷"""
    headers = get_headers()
    
    params = {
        "page": page,
        "page_size": page_size
    }
    
    resp = requests.get(f"{API_BASE}/surveys/{survey_id}/responses", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    responses = data.get("responses", [])
    total = data.get("total", 0)
    
    if not responses:
        return "没有答卷"
    
    output = f"## 答卷数据（共 {total} 份）\n\n"
    
    # 显示前 10 份
    for i, response in enumerate(responses[:10]):
        output += f"### 答卷 {i + 1}\n\n"
        output += f"- 提交时间：{response.get('submitted_at', '-')}\n"
        
        answers = response.get("answers", {})
        for question_id, answer in answers.items():
            output += f"- 问题 {question_id}：{answer}\n"
        
        output += "\n"
    
    if total > 10:
        output += f"\n*还有 {total - 10} 份答卷未显示*\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="获取问卷答卷")
    parser.add_argument("survey_id", help="问卷 ID")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=100, help="每页数量")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = get_responses(args.survey_id, args.page, args.page_size)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"获取失败：{e}", file=sys.stderr)
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
| 功能 | 固定 | 可自定义题型 |
| 数据处理 | 原样返回 | 可分析/可视化 |
| 多平台 | 绑定腾讯问卷 | 可对接问卷星等 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
