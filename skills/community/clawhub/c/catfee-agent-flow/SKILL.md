---
name: catfee-agent-flow
description: AgentFlow 工作流管理系统 MCP 技能。当用户说"创建项目"、"添加需求"、"查看任务"、"更新状态"、"项目列表"、"需求列表"、"上传附件"等时触发。用于管理项目和任务的完整生命周期（创建→需求→任务→状态流转），以及为实体上传附件文件。
---

# AgentFlow 工作流管理系统

## MCP 地址

- **默认地址：** `http://182.42.153.28:18900/api/mcp/sse`

## 调用脚本（推荐）

使用 `scripts/agentflow.py` 调用工具（已封装好 SSE/POST 逻辑）：

```bash
python scripts/agentflow.py <tool_name> [args...]
```

### 项目管理
```bash
python scripts/agentflow.py list_projects
python scripts/agentflow.py create_project "我的项目" "项目描述"
python scripts/agentflow.py get_project <projectId>
python scripts/agentflow.py update_project <projectId> <status>
python scripts/agentflow.py delete_project <projectId>
python scripts/agentflow.py get_project_status <projectId>
```

### 需求管理
```bash
python scripts/agentflow.py create_requirement <projectId> "需求标题" "P1" ["描述"]
python scripts/agentflow.py list_requirements <projectId>
python scripts/agentflow.py get_requirement <requirementId>
python scripts/agentflow.py update_requirement <requirementId> <field> <value>
python scripts/agentflow.py delete_requirement <requirementId>
```

### 任务管理
```bash
python scripts/agentflow.py create_task <requirementId> "任务标题" "P1" ["负责人"]
python scripts/agentflow.py list_tasks [requirementId]
python scripts/agentflow.py get_task <taskId>
python scripts/agentflow.py transition <taskId/requirementId> <fromStatus> <toStatus> ["操作人"] ["备注"]
python scripts/agentflow.py get_timeline <taskId>
```

### 文件上传 ⚠️ 重要
```bash
python scripts/agentflow.py upload_file <entityType> <entityId> <filepath>
```

**entityType 说明：**
- `project` - 项目附件
- `requirement` - 需求附件
- `task` - **任务附件（最常用）**

> ⚠️ 上传附件时，`entityType` 必须根据目标实体选择对应的类型。
> 如果要给任务上传附件，entityType 填 `task`，不是 `requirement`！

**上传流程：**
1. 调用 `get_upload_url` 获取上传地址和字段
2. 将文件 POST 为 multipart/form-data 完成上传

### 搜索
```bash
python scripts/agentflow.py search "关键词"
```

## 完整工具列表

| 类别 | 工具 | 功能 |
|------|------|------|
| 项目 | `create_project` | 创建项目 |
| 项目 | `get_project` | 获取项目详情 |
| 项目 | `list_projects` | 列出项目列表 |
| 项目 | `update_project` | 更新项目状态 |
| 项目 | `get_project_status` | 项目整体状态摘要 |
| 项目 | `delete_project` | 删除项目 |
| 需求 | `create_requirement` | 创建需求（关联到项目） |
| 需求 | `get_requirement` | 获取需求详情 |
| 需求 | `list_requirements` | 列出需求列表 |
| 需求 | `update_requirement` | 更新需求字段 |
| 需求 | `delete_requirement` | 删除需求 |
| 任务 | `create_task` | 创建任务（关联到需求） |
| 任务 | `get_task` | 获取任务详情 |
| 任务 | `list_tasks` | 列出任务列表 |
| 任务 | `transition` | 任务/需求状态流转 |
| 任务 | `get_timeline` | 查看时间线 |
| 文件 | `get_upload_url` | 获取文件上传地址和字段 |
| 文件 | `upload_file` | 完整文件上传流程 |
| 辅助 | `search` | 搜索项目/需求/任务 |
| 辅助 | `log_context` / `get_context` / `delete_context` | 上下文数据管理 |

## 状态值说明

| 状态 | 含义 |
|------|------|
| `pending` | 待处理 |
| `in_review` | 审核中 |
| `in_progress` | 进行中 |
| `completed` | 已完成 |
| `paused` | 已暂停 |
| `cancelled` | 已取消 |

---

## 📋 需求全流程开发工作流

### 标准流程：需求文档 → 任务拆解 → 附件挂载

当收到需求文档时，按以下步骤操作：

### Step 1：创建项目和需求（如果尚未创建）
```bash
# 创建项目
python scripts/agentflow.py create_project "项目名称" "项目描述"

# 创建需求（关联到项目）
python scripts/agentflow.py create_requirement <projectId> "需求标题" "P1"
```

### Step 2：进行需求拆解，生成任务文件
将需求文档按维度拆解，**每个任务生成一个独立的 md 文件**。
- 文件命名规范：`{任务ID}-{任务名称}.md`
- 每个任务文件包含：任务概述、依赖、人天、相关上下文（数据库/接口/前端页面等）
- 文件存放目录：`documents/{项目名}/task_split/`

### Step 3：批量创建任务 + 附件挂载

**⚠️ 关键原则：每个任务单独创建，附件挂载到对应任务，不要聚集上传。**

批量创建任务的脚本示例：
```python
tasks = [
    ('T01', '后端框架搭建', 'P0', 2, '基于clouddream-server初始化项目...'),
    ('T02', '数据库设计', 'P0', 3, '设计10张核心表结构...'),
    # ...更多任务
]

task_ids = {}  # 用于记录 taskId 映射

for task_id, name, priority, days, desc in tasks:
    title = f'{task_id}-{name}'
    # 1. 创建任务，获取 taskId
    result = call('create_task', {
        'requirementId': REQ_ID,
        'title': title,
        'priority': priority,
        'description': f'{desc} | {days}人天'
    })
    task_ids[task_id] = result['id']

    # 2. 等待一小段时间
    time.sleep(0.3)

# 3. 逐个上传附件到对应任务
for task_key, task_id in task_ids.items():
    filepath = f'documents/{项目名}/task_split/{task_key}-{任务名}.md'
    upload_file('task', task_id, filepath)  # entityType='task'!
    time.sleep(0.5)
```

### Step 4：状态流转
```bash
# 任务开始时
python scripts/agentflow.py transition <taskId> pending in_progress "执行人"

# 任务完成时
python scripts/agentflow.py transition <taskId> in_progress completed "执行人"

# 需求全部完成
python scripts/agentflow.py transition <requirementId> in_progress completed "执行人"
```

### 常见错误避免

| 错误做法 | 正确做法 |
|---------|---------|
| 把所有任务文件上传到一个任务附件 | 每个任务单独创建+上传到自己的附件 |
| entityType 填 `requirement` 上传任务附件 | entityType 填 `task` 上传任务附件 |
| 上传到需求附件而不是任务附件 | 任务文档 → 任务附件；需求文档 → 需求附件 |

---

## 需求开发流程集成

每次接到需求文档时，必须自动同步到 AgentFlow：

| 阶段 | AgentFlow 操作 | 状态值 |
|------|--------------|--------|
| 开始拆解 | `create_project` + `create_requirement` | `pending` |
| 逐步完成 | `create_task` + `transition` | `in_progress` |
| 全部完成 | requirement `transition` | `completed` |

详见 MEMORY.md「需求开发流程 × AgentFlow 集成规范」章节。
