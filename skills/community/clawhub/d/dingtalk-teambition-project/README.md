# DingTalk Teambition AI Skill

Teambition 项目和任务管理 AI Skill，通过 TQL（查询语言）灵活查询和管理 Teambition 项目、任务、成员等。

## 功能特性

- **任务管理**：查询、创建、更新、归档任务，支持优先级设置和状态流转
- **项目管理**：查询项目列表和详情，管理项目成员
- **迭代管理**：创建、开始、完成迭代（Sprint）
- **评论与进展**：创建评论、添加任务进展、上传附件
- **成员查询**：按姓名搜索项目成员
- **自定义字段**：支持查询和更新任务的自定义字段

## 环境准备

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置认证

**方式一：环境变量（推荐）**
```bash
export TEAMBITION_USER_TOKEN="your_teambition_user_token"
```

**方式二：配置文件**
在项目目录下创建 `user-token.json`：
```json
{"userToken": "your_teambition_user_token"}
```

> 获取 User Token：[Teambition 开放平台](https://open.teambition.com/user-mcp)

## 快速开始

### 查询我的待办任务

```bash
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false"
```

### 创建任务

```bash
uv run scripts/create_task.py \
  --project-id 'your_project_id' \
  --title '完成需求文档' \
  --due-date '2026-04-01' \
  --priority 1
```

### 查询项目

```bash
uv run scripts/query_projects.py --tql "involveMembers = me()"
```

## 脚本列表

| 脚本                      | 用途                       |
| ------------------------- | -------------------------- |
| `query_tasks.py`          | 查询任务列表（支持 TQL）   |
| `query_task_detail.py`    | 查询任务详情（支持批量）   |
| `create_task.py`          | 创建任务                   |
| `update_task.py`          | 更新任务（多字段并行）     |
| `update_task_priority.py` | 更新任务优先级             |
| `archive_task.py`         | 归档/恢复任务              |
| `create_comment.py`       | 创建评论（支持 @提及）     |
| `create_trace.py`         | 添加任务进展               |
| `query_projects.py`       | 查询项目列表（支持 TQL）   |
| `query_project_detail.py` | 查询项目详情（支持批量）   |
| `query_members.py`        | 搜索成员（支持批量ID查询） |
| `manage_sprint.py`        | 迭代管理（创建/开始/完成） |
| `get_task_statuses.py`    | 查询任务工作流状态         |
| `get_priority_list.py`    | 获取企业优先级配置         |
| `get_custom_fields.py`    | 获取项目自定义字段         |
| `upload_file.py`          | 上传文件                   |
| `query_task_activity.py`  | 查询任务动态               |

## TQL 查询示例

### 任务查询

```bash
# 我的待办
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false"

# 本周截止的任务
uv run scripts/query_tasks.py --tql "executorId = me() AND dueDate >= startOf(w) AND dueDate <= endOf(w)"

# 逾期任务
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false AND dueDate < startOf(d)"

# 标题搜索
uv run scripts/query_tasks.py --tql "title ~ '关键词'"
```

### 项目查询

```bash
# 我参与的项目
uv run scripts/query_projects.py --tql "involveMembers = me()"

# 按名称搜索
uv run scripts/query_projects.py --tql "nameText ~ '产品开发'"
```

> 完整 TQL 语法请参考 `references/tql.md` 和 `references/project-tql.md`

## 核心规则

1. **使用 `me()` 查询当前用户**：TQL 中查询"我的"任务/项目，必须用 `executorId = me()`，禁止硬编码用户 ID

2. **时区自动转换**：`create_task.py`、`update_task.py`、`manage_sprint.py` 已内置东八区→UTC 转换，直接传本地时间即可

3. **ID 转名称**：API 返回的各类 ID 字段（如 `executorId`、`creatorId` 等）展示给用户前必须转换为可读名称

4. **优先级查询**：企业通常会自定义优先级名称，展示前需先用 `get_priority_list.py` 查询企业配置

5. **任务链接渲染**：任务 ID 渲染为 `https://www.teambition.com/task/{taskId}`，项目 ID 渲染为 `https://www.teambition.com/project/{projectId}`

6. **`content` = 标题**：API 返回的 `content` 字段就是任务标题，展示时使用"标题"而非"内容"

## 项目结构

```
dingtalk-teambition/
├── scripts/           # 核心脚本目录
│   ├── query_tasks.py
│   ├── create_task.py
│   ├── update_task.py
│   └── ...
├── references/        # 参考文档
│   ├── tql.md        # TQL 完整语法
│   ├── project-tql.md # 项目 TQL 语法
│   ├── task-ops.md   # 任务操作指南
│   ├── error-handling.md # 错误处理
│   └── ...
├── package.json      # Skill 元数据
├── pyproject.toml    # Python 依赖
└── README.md         # 本文件
```

## 技术栈

- **Python** >= 3.8
- **依赖管理**：uv
- **HTTP 请求**：requests

## 相关链接

- [Teambition 开放平台](https://open.teambition.com/)
- [SKILL.md](./SKILL.md) - 完整使用文档
