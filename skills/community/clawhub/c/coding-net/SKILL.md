---
name: coding-net
version: 1.1.0
description: 查询和操作腾讯 Coding DevOps 平台（e.coding.net）的迭代、事项（需求/缺陷/任务）、团队成员等数据，包括创建需求和缺陷。当用户涉及 Coding 平台操作时触发，如「查迭代」「查事项」「当前迭代的需求」「Coding 上的 bug」「团队成员列表」「assignee」「新建需求」「创建缺陷」。所有 API 均需环境变量 CODING_TOKEN。
---

# Coding Open API Skill

## 启动引导（每次对话开始时必须执行）

**第一步：收集 token**

检查用户消息是否已包含 token。若未提供，检查环境变量：
```bash
python3 -c "import os; print('已设置' if os.environ.get('CODING_TOKEN') else '未设置')"
```
若均未提供，向用户询问：「请提供您的 Coding 个人访问令牌（Bearer Token）」

**第二步：验证 token，确认团队**

```python
import sys; sys.path.insert(0, "path/to/coding-net/scripts")
from core import bootstrap
result = bootstrap(token="<token>")
if result["error"]:
    print("✗", result["error"])
else:
    t = result["team"]
    print(f"✓ Token 有效  团队: {t['name']}  ({t['host']})")
```

**第三步：确认项目标识**

告知用户已验证团队，然后询问：
「请提供项目 URL 或项目标识。URL 格式为 `https://<团队>.coding.net/p/<项目标识>/`，项目标识是 `/p/` 后面的部分（如 `biaopin-swiftagent`）。」

> ⚠️ **不要猜项目名**。Coding.net 区分"显示名"和"项目标识"，API 只认项目标识。
> 用户说"项目叫 swiftagent"≠ 标识就是 `swiftagent`，必须追问 URL。

**第四步：验证项目 + 展示迭代列表，让用户选择**

```python
result = bootstrap("biaopin-swiftagent", token="<token>")
if result["error"]:
    print("✗", result["error"])
else:
    print("项目下的迭代列表：")
    for it in result["iterations"]:
        print(f"  [{it['code']}] {it['name']}")
```

将迭代列表展示给用户，询问：「请问您要查看哪个迭代？」

完成以上四步后，再执行用户的实际查询请求。

---

## 环境配置（可选，配置后免传参）

| 变量 | 说明 |
|------|------|
| `CODING_TOKEN` | Bearer Token |
| `CODING_DEFAULT_PROJECT_NAME` | 默认项目标识（URL 中 `/p/` 后的部分） |
| `CODING_DEFAULT_ITERATION_CODE` | 默认迭代 Code（整数） |

## 脚本结构

```
scripts/
├── core.py        — HTTP 客户端、Token 解析、CodingAPIError
├── iterations.py  — 迭代 API（依赖 core）
├── issues.py      — 事项 API（依赖 core + iterations）
└── members.py     — 团队成员 API（依赖 core）
```

在 Python 中使用（脚本已处理 sys.path，直接 import 即可）：

```python
import sys
sys.path.insert(0, "path/to/scripts")
from iterations import get_iteration_list_code_and_name
from issues import describe_issue, describe_issue_list, create_issue, describe_defect_types, \
    extract_members_from_issue_list, get_custom_fields_from_issues
from members import get_team_members_id_and_name
```

## 公开函数速查

### iterations.py

```python
get_iteration_list_code_and_name(project_name=None, *, token=None) -> [{'code': int, 'name': str}]
```
分页拉取全量迭代列表。返回的 `code` 即 `describe_issue_list(iteration=...)` 所需值。

### issues.py

```python
describe_issue_list(
    project_name=None, *,   # 省略时读 CODING_DEFAULT_PROJECT_NAME
    issue_type="ALL",       # ALL / REQUIREMENT / DEFECT / MISSION
    limit="2000",
    assignee_ids=None,      # [int] — API 侧过滤（不可靠，建议配合 filter_issues 二次过滤）
    iteration=None,         # int  — 省略时读 CODING_DEFAULT_ITERATION_CODE；已内置客户端二次过滤
    status_types=None,      # None→TODO+PROCESSING; []→不过滤; ['TODO',...]→指定
    base_issue_type=None,   # REQUIREMENT / DEFECT / MISSION
    token=None,
) -> dict
# Response.IssueList 每条含：
#   Code, Name, Type, IssueStatusName, IssueStatusType, Priority,
#   Assignees([{"id": int, "name": str}]),  ← 处理人数组（非 Creator/Handler）
#   IterationCode, IterationName, StartDate, DueDate, CustomFields
```

```python
filter_issues(
    items: list,            # describe_issue_list 返回的 IssueList
    *,
    assignee_name=None,     # 处理人姓名（模糊匹配，不区分大小写）
    assignee_id=None,       # 处理人 ID（精确匹配）
    iteration_code=None,    # 迭代 Code 二次过滤（API 侧过滤失效时使用）
) -> list
```

```python
describe_issue(project_name=None, issue_code=0, *, token=None) -> dict
# 返回 {Name, Description, IssueStatusName, AssigneeName, CreatorName}
```

```python
create_issue(
    project_name=None, *,
    name: str,                  # 标题（必填）
    issue_type="REQUIREMENT",   # REQUIREMENT / DEFECT / MISSION
    description="",
    priority=2,                 # 0=低 1=中 2=高(默认) 3=紧急（API 文档定义）
    assignee_id=None,           # int — 成员 ID（见 members.py 或从事项列表反查）
    iteration=None,             # int — 省略时读 CODING_DEFAULT_ITERATION_CODE
    start_date=None,            # str 'YYYY-MM-DD' — 部分项目必填
    due_date=None,              # str 'YYYY-MM-DD' — 部分项目必填
    label_ids=None,             # [int] — 部分项目必填，缺失报 issue_project_label_required
    working_hours=None,         # float — 工时（小时），部分项目必填
    issue_type_id=None,         # int — 事项大类 ID（非缺陷子类型）
    defect_type_id=None,        # int — 缺陷子类型 ID，来自 describe_defect_types
    token=None,
) -> dict  # {Code, Name, IssueStatusName, AssigneeName, CreatorName}
```

```python
describe_defect_types(project_name=None, *, token=None) -> [{'id': int, 'name': str}]
# 返回缺陷子类型列表，对应 create_issue(defect_type_id=...)
```

```python
extract_members_from_issue_list(issues_result: dict) -> [{'id': int, 'name': str}]
# 从 describe_issue_list 返回值中提取去重成员，用于 DescribeTeamMembers 无权限时的替代
```

```python
get_custom_fields_from_issues(
    project_name=None, *,
    issue_type="REQUIREMENT",   # 按事项类型采样
    sample=10,                  # 采样条数
    token=None,
) -> [{'id': int, 'name': str}]
# 通过采样现有事项推断项目自定义字段（绕开需高权限的 DescribeIssueCustomFieldsBoundToProject）
# 创建事项前必须先调用，将必填字段通过 custom_field_values 传入 create_issue
```

### members.py

```python
get_team_members_id_and_name(*, token=None) -> [{'id': int, 'name': str}]
```
分页拉取全量团队成员。`id` 可用于 `describe_issue_list(assignee_ids=[...])` 过滤。
**注意**：部分 token 无 `DescribeTeamMembers` 权限，会报错，此时改用 `extract_members_from_issue_list`。

## 常见工作流

**查指定迭代下某处理人的需求（标准流程）：**
```python
import sys; sys.path.insert(0, "path/to/coding-net/scripts")
from issues import describe_issue_list, filter_issues

result = describe_issue_list(project_name, iteration=22904, issue_type="REQUIREMENT", status_types=[])
issues = result["Response"]["IssueList"]

# 客户端按处理人过滤（API 侧过滤不可靠）
my_issues = filter_issues(issues, assignee_name="wangyin")
for it in my_issues:
    assignees = ", ".join(a["name"] for a in it["Assignees"])
    print(f"#{it['Code']} [{it['IssueStatusName']}] {it['Name']} — {assignees}")
```

**从事项列表提取成员（DescribeTeamMembers 无权限时的替代方案）：**
```python
from issues import describe_issue_list, extract_members_from_issue_list

result = describe_issue_list(project_name, iteration=code, status_types=[])
members = extract_members_from_issue_list(result)
# [{'id': 9403993, 'name': 'wangyin'}, ...]
```

**查单条事项详情（含描述）：**
```python
from issues import describe_issue
detail = describe_issue(project_name, issue_code=12345)
```

**创建需求（必须先检测自定义字段）：**

> ⚠️ 项目可能配置了必填自定义字段（如"提测日期"），直接创建会报 `issue_custom_field_required`。
> 先调用 `get_custom_fields_from_issues()` 推断字段列表，再传入 `custom_field_values`。

```python
from issues import create_issue, get_custom_fields_from_issues

# 第一步：检测项目自定义字段
custom_fields = get_custom_fields_from_issues(project_name, issue_type="REQUIREMENT")
# 返回示例：[{"id": 38589683, "name": "提测日期"}, ...]
# 向用户确认各字段值，必填字段必须传入

# 第二步：创建需求
issue = create_issue(
    project_name,
    name="支持 XX 功能",
    start_date="2026-06-17",
    due_date="2026-06-30",
    custom_field_values=[
        {"Id": 38589683, "Content": "2026-06-30"},  # 提测日期
        # 其他必填自定义字段...
    ],
)
print(issue["Code"], issue["Name"])
```

**创建缺陷（含项目级必填字段）：**
```python
from issues import describe_issue_list, extract_members_from_issue_list, describe_defect_types, create_issue, filter_issues

# 1. 从事项列表反查成员 ID
result = describe_issue_list(project_name, iteration=code, status_types=[])
members = extract_members_from_issue_list(result)
uid = next(m["id"] for m in members if m["name"] == "张三")

# 2. 查缺陷子类型
defect_types = describe_defect_types(project_name)  # [{'id': 36666669, 'name': '功能缺陷'}, ...]

# 3. 创建（start_date/due_date/label_ids/working_hours 按项目配置决定是否必填）
issue = create_issue(
    project_name,
    name="登录页面报 500 错误",
    issue_type="DEFECT",
    priority=1,
    assignee_id=uid,
    iteration=code,
    start_date="2026-06-17",
    due_date="2026-06-20",
    label_ids=[123],
    working_hours=2.0,
    defect_type_id=defect_types[0]["id"],
)
```
