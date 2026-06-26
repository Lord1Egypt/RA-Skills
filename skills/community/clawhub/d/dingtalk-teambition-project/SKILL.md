---
name: dingtalk-teambition
description: "Use for anything related to Teambition tasks and projects. Triggers on: checking my todos, what tasks are due today or this week, create a task, update task status or priority or assignee or note, mark task as done, query overdue tasks, search tasks by keyword, view task details, upload file to task, check team members, query project list, add task comment with @mention, track task progress. NOT for: non-Teambition platforms or Git operations."
version: 1.0.0
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "uv"] },
        "primaryEnv": "TEAMBITION_USER_TOKEN",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

## 适用场景

✅ **适合使用本技能：**
- 查询我的待办任务、今天/本周到期的任务、逾期任务
- 创建、更新、归档任务
- 更新任务状态、优先级、执行人、备注
- 管理任务进展、评论（支持 @提及）、动态
- 上传文件到任务
- 查询项目列表、项目详情
- 查询企业成员
- 管理迭代（创建/开始/完成）

❌ **不适用场景：**
- 操作非 Teambition 平台（Jira、Asana 等）
- Git 操作或代码管理 → 直接使用 `git`
- 管理脚本未覆盖的 Teambition 组织/管理员设置

---

## 环境准备
> 获取 User Token：[Teambition 开放平台](https://open.teambition.com/user-mcp)
```bash
# 方式 1：环境变量
export TEAMBITION_USER_TOKEN="your_token"

# 方式 2：在 dingtalk-teambition/ 目录下创建 user-token.json
# {"userToken": "your_token"}

cd dingtalk-teambition && uv sync
```

---

## 核心规则

1. **`me()`**：TQL 中查询"我的"任务/项目，必须用 `executorId = me()`，禁止硬编码用户 ID
2. **时区**：`create_task.py` / `update_task.py` / `manage_sprint.py` 已内置东八区→UTC 转换，直接传本地时间即可；不要手动传 UTC 时间（会被再次转换导致偏差）。转换逻辑参考：
   ```python
   from datetime import datetime, timedelta
   user_date = "2026-03-15"
   dt = datetime.strptime(user_date, "%Y-%m-%d") - timedelta(hours=8)
   iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
   # 结果：2026-03-14T16:00:00.000Z
   ```
3. **ID→名称**：API 返回的各类 ID 字段均为原始 ID 字符串，**展示给用户前必须转换为可读名称，禁止直接展示原始 ID**。
   - **需要转换的常见 ID 字段**：
     | 字段 | 含义 | 转换方式 |
     |------|------|---------|
     | `executorId` | 执行人 | `query_members.py --user-ids <ID>` 批量查询 |
     | `creatorId` | 创建人 | `query_members.py --user-ids <ID>` 批量查询 |
     | `involveMembers` | 参与人列表 | `query_members.py --user-ids <ID1,ID2,...>` 批量查询 |
     | `sprintId` | 所属迭代 | `query_project_detail.py <projectId>` 获取迭代列表后匹配 |
     | `stageId` | 所属任务列 | 任务详情中通常包含 `stageName`，否则需查项目工作流 |
     | `projectId` | 所属项目 | 项目名通常已在上下文中，或用 `query_project_detail.py` 查询 |
     | `parentTaskId` | 父任务 | `query_task_detail.py <parentTaskId>` 获取父任务标题 |
   - **展示任务列表/详情时的必要步骤**：
     1. 收集所有任务中出现的各类 ID（去重）
     2. 批量查询对应的名称（人员用 `query_members.py`，项目/迭代/任务用各自的查询脚本）
     3. 将 ID 替换为名称后再向用户展示
   - 如果无法确定某个 ID 对应的名称，可展示为"未知"或保留该字段不展示，不要直接展示原始 ID
   ```bash
   # 按姓名搜索成员，获取 userId
   uv run scripts/query_members.py --keyword "张三"
   # 返回结果中匹配 userId，确认后用于展示或操作
   
   # 批量按用户ID查询成员（推荐用于ID转换）
   uv run scripts/query_members.py --user-ids "id1,id2,id3"
   ```
4. **优先级**：数值含义为 `0=紧急 1=高 2=中 3=低`，但**企业通常会自定义优先级名称**，脚本输出的 `priorityLabel` 仅为系统默认值，不代表该企业的真实配置。
   - **展示优先级名称前必须先查询企业配置**，查询链路：
     1. 从任务详情获取 `projectId`
     2. `uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId` 获取 `organizationId`
     3. `uv run scripts/get_priority_list.py <organizationId>` 获取企业真实优先级列表
   - 返回结果中每条优先级包含 `priority`（数值）和 `name`（企业自定义名称），以此覆盖默认 label 后再展示
   - **更新优先级前同样需要先查询**，将用户描述的优先级名称与企业配置匹配后，再用对应的 `priority` 数值调用更新接口
5. **归档 vs 删除**：归档任务会移入回收站，不在正常列表显示，可通过 `--restore` 恢复；归档不等于删除
6. **动态 vs 进展**：动态（activity）是系统自动记录的操作历史（状态变更、字段修改等）；进展（trace）是用户手动填写的阶段性状态更新
7. **迭代操作顺序**：先用 `--action create --project-id <id> --name <名>` 创建迭代获取 sprint-id，再用 `--action start --project-id <id> --sprint-id <id>` 开始，完成后用 `--action complete --project-id <id> --sprint-id <id>`；start/complete 都需要同时传 `--project-id` 和 `--sprint-id`
8. **状态查询优先**：更新任务状态时，优先使用 `get_task_statuses.py <taskId>` 直接查询该任务的工作流状态列表，无需先获取 projectId；只有创建任务需要初始状态时才用 `get_taskflow_statuses.py`
9. **按需读文档**：TQL 语法 → `references/tql.md`；进展/评论/动态/归档 → `references/task-ops.md`；错误处理 → `references/error-handling.md`
10. **文件上传流程**：先用 `upload_file.py` 上传文件获取 `fileToken`，再用 `create_comment.py --file-tokens <token>` 将文件附加到评论；两步均走脚本，无需直接调 API
11. **ID 链接渲染**：当回复中涉及任务 ID 或项目 ID 时，必须将其渲染为可点击的链接，格式如下：
    - 任务链接：`https://www.teambition.com/task/{taskId}`
    - 项目链接：`https://www.teambition.com/project/{projectId}`
12. **任务的 content = 标题**：API 返回的 `content` 字段就是任务的**标题**，向用户展示时统一使用"标题"而非"内容"，避免混淆；`create_task.py` 和 `update_task.py` 都统一使用 `--title` 参数
13. **空字段隐藏**：展示任务或项目信息时，**值为空、null、0、false 或空数组的字段应当隐藏，不向用户展示**，只展示有实际值的字段。例如：
    - 进度为 0 → 不展示进度
    - 截止时间为 null → 不展示截止时间
    - 备注为空字符串 → 不展示备注
    - 迭代为 null → 不展示迭代
    - 标签为空数组 → 不展示标签
    - 此规则适用于所有可选字段，保持信息展示简洁
    
14. **自定义字段更新格式**：使用 `--customfields` 更新任务自定义字段时，不同类型有不同格式：
    ```bash
    # 日期类型（date）：value 是数组，包含带 title 的对象，日期格式为 ISO 8601
    uv run scripts/update_task.py --task-id 'xxx' \
      --customfields '[{"customfieldId": "字段ID", "value": [{"title": "2026-03-16T00:00:00.000Z"}]}]'
    # 文本类型（text）：value 是数组，包含带 title 的对象
    uv run scripts/update_task.py --task-id 'xxx' \
      --customfields '[{"customfieldId": "字段ID", "value": [{"title": "文本内容"}]}]'
    # 单选类型（select）：value 是数组，包含带 id 的选项对象
    uv run scripts/update_task.py --task-id 'xxx' \
      --customfields '[{"customfieldId": "字段ID", "value": [{"id": "选项ID"}]}]'
    ```

15. **文件类型自定义字段上传**：使用 `upload_file_to_customfield.py` 一站式上传文件到自定义字段：
    ```bash
    uv run scripts/upload_file_to_customfield.py \
      --task-id '<taskId>' \
      --file-path '/path/to/file.pdf' \
      --customfield-id '<字段ID>'
    ```

16. **自定义字段文件类型展示**：自定义字段中类型为 `work`（文件附件）的字段，展示时必须将文件名渲染为可点击的下载链接，使用字段值中的 `downloadUrl` 字段作为链接地址，格式如下：
    - 展示格式：`[文件名](downloadUrl)`
    - 示例：`[材料.md](https://xxx.com/...)`
    - 若一个字段包含多个文件，每个文件单独渲染为一个链接
    - 禁止只展示文件名而不附带链接

17. **批量任务表格输出**：当查询返回**多个任务**（2个及以上）时，**默认使用表格形式展示**，表格列应包含：标题、状态、优先级、执行人、截止时间。单行任务仍使用文本段落形式展示，保持信息清晰易读。

18. **破坏性操作需确认**：执行**归档任务**（`archive_task.py`）、**删除**等不可逆或影响较大的操作前，**必须先向用户确认**，展示操作对象（任务标题/ID）和操作类型，获得明确同意后再执行。例如：
    - "确认归档任务「完成需求文档」(ID: xxx)吗？归档后可从回收站恢复。"
    - "确认删除该评论吗？删除后无法恢复。"

19. **空字段不返回**：API 查询任务详情时，**值为空的自定义字段不会被返回**。如果一个文件类型字段从未被赋值过，`customfields` 数组中不会包含该字段。要查看任务可填写的所有自定义字段，需要：
    ```bash
    # 1. 从任务详情获取 sfcId（任务类型ID）和 projectId
    uv run scripts/query_task_detail.py <taskId> --detail-level detailed
    
    # 2. 查询该任务类型可用的所有自定义字段
    uv run scripts/get_custom_fields.py <projectId> --sfc-id <sfcId>
    ```
    返回结果中 type 为 `work` 的字段就是文件类型字段

---

## 脚本速查

| 脚本 | 用途 | 关键参数 |
|------|------|---------|
| `query_tasks.py` | 查询任务列表（TQL），默认返回：标题、状态、优先级、执行人ID、截止时间、备注、迭代、任务列、开始时间、进度、父任务ID | `--tql <TQL>` `--page-size N` `--page-token T` `--no-details` `--extra-fields f1,f2` |
| `query_task_detail.py <id1,id2>` | 查询任务详情（支持批量） | `--detail-level simple\|detailed` `--extra-fields f1,f2` |
| `create_task.py` | 创建任务 | `--title <标题>`（必需）`--project-id` `--executor-id` `--due-date` `--priority` |
| `update_task.py` | 更新任务（多字段并行） | `--task-id <id>`（必需）`--title` `--executor-id` `--due-date` `--note` `--priority` `--taskflowstatus-id` |
| `update_task_priority.py` | 单独更新优先级（更新前必须先用 `get_priority_list.py` 查企业配置） | `--task-id <id>` `--priority <0-3>` |
| `create_comment.py` | 创建评论 | `--task-id <id>` `--content <内容>` `--mention <姓名>` `--mention-id <userId>` `--file-tokens <token>` |
| `query_projects.py` | 查询项目列表（TQL） | `--tql <TQL>` `--page-size N` `--page-token T` `--no-details` `--include-template` |
| `query_project_detail.py <id>` | 查询项目详情（支持批量） | `--detail-level simple\|detailed` `--extra-fields f1,f2` |
| `query_members.py` | 搜索成员（支持批量ID查询） | `--keyword <姓名>` `--user-ids <ID1,ID2,...>` |
| `get_task_statuses.py <taskId>` | 查询任务工作流状态列表（推荐） | `--q <关键词>` |
| `get_taskflow_statuses.py <projectId>` | 获取项目工作流状态（创建任务时用） | `--only-start` `--q <关键词>` |
| `get_custom_fields.py <projectId>` | 获取项目自定义字段配置 | `--cf-ids <IDs>` `--sfc-id <ID>` |
| `get_scenario_types.py <projectId>` | 获取项目任务类型列表 | `--q <关键词>` `--sfc-ids <IDs>` |
| `get_priority_list.py <organizationId>` | 获取企业优先级配置 | — |
| `get_current_user.py` | 获取当前登录用户信息（userId、name、email 等） | — |
| `create_trace.py` | 添加任务进展 | `--task-id <id>` `--title <标题>` `--status <1-3>` |
| `upload_file.py` | 上传文件，返回 `fileToken` | `--file-path <路径>` `--scope task:<id>` `--category attachment` |
| `archive_task.py` | 归档/恢复任务 | `--task-id <id>` `[--restore]` |
| `query_task_activity.py` | 查询任务动态 | `--task-id <id>` `--actions comment` |
| `manage_sprint.py` | 迭代管理 | `--action list\|create\|start\|complete` `--project-id <id>` `--sprint-id <id>` `--name <名>` |

### query_task_detail.py 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `任务ID` | 字符串 | 是 | 任务 ID，逗号分隔支持批量 |
| `--detail-level` | 字符串 | 否 | `simple`（默认）或 `detailed` |
| `--extra-fields` | 字符串 | 否 | simple 模式下额外包含的字段，逗号分隔 |

**simple（默认）** 包含字段：

| 字段 | 说明 |
|------|------|
| `id` | 任务 ID |
| `content` | 任务标题 |
| `isDone` | 是否完成 |
| `executorId` | 执行人 ID |
| `projectId` | 项目 ID |
| `dueDate` | 截止时间 |
| `priority` | 优先级（0=紧急，1=高，2=中，3=低） |
| `created` | 创建时间 |
| `updated` | 更新时间 |
| `note` | 备注 |

**detailed** 额外包含：`sprintId`（迭代 ID）`stageId`（任务列 ID）`startDate`（开始时间）`progress`（进度）`parentTaskId`（父任务 ID）及自定义字段等 30+ 字段

### query_project_detail.py 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `项目ID` | 字符串 | 是 | 项目 ID，逗号分隔支持批量 |
| `--detail-level` | 字符串 | 否 | `simple`（默认）或 `detailed` |
| `--extra-fields` | 字符串 | 否 | simple 模式下额外包含的字段，逗号分隔 |

**simple（默认）** 包含字段：

| 字段 | 说明 |
|------|------|
| `id` | 项目 ID |
| `name` | 项目名称 |
| `description` | 项目描述 |
| `visibility` | 可见性（public/private） |
| `isTemplate` | 是否是模板项目 |
| `creatorId` | 创建人 ID |
| `isArchived` | 是否在回收站 |
| `isSuspended` | 是否已归档 |
| `created` | 创建时间 |
| `updated` | 更新时间 |

**detailed** 额外包含：`logo`（项目 LOGO）`organizationId`（企业 ID）`uniqueIdPrefix`（任务 ID 前缀）`startDate`（开始时间）`endDate`（结束时间）等 20+ 字段

---

## TQL 快速参考

### 任务 TQL 常用场景

| 场景 | TQL |
|------|-----|
| 我的待办任务 | `executorId = me() AND isDone = false` |
| 我的逾期任务 | `executorId = me() AND isDone = false AND dueDate < startOf(d)` |
| 今天截止的任务 | `executorId = me() AND dueDate >= startOf(d) AND dueDate <= endOf(d)` |
| 本周截止的任务 | `executorId = me() AND dueDate >= startOf(w) AND dueDate <= endOf(w)` |
| 即将逾期（未来3天） | `executorId = me() AND isDone = false AND dueDate >= startOf(d) AND dueDate <= endOf(d, 3d)` |
| 过去7天更新的任务 | `executorId = me() AND updated >= startOf(d, -7d)` |
| 高优先级未完成 | `priority = 0 AND isDone = false` |
| 标题模糊搜索 | `title ~ '关键词'` |
| 全文搜索（标题+备注） | `text ~ '关键词'` |
| 指定项目的任务 | `projectId = 'xxx'` |

> 完整 TQL 语法（字段、运算符、时间函数）→ `references/tql.md`

### 项目 TQL 常用场景

| 场景 | TQL |
|------|-----|
| 我参与的项目 | `involveMembers = me()` |
| 我创建的项目 | `creatorId = me()` |
| 按名称搜索 | `nameText ~ '关键词'` |
| 已归档的项目 | `isSuspended = true` |
| 今天更新的项目 | `updated >= startOf(d) AND updated <= endOf(d)` |
| 今天创建的项目 | `created >= startOf(d) AND created <= endOf(d)` |
| 本周创建的项目 | `created >= startOf(w) AND created <= endOf(w)` |
| 本月创建的项目 | `created >= startOf(M) AND created <= endOf(M)` |
| 过去7天创建的项目 | `created >= startOf(d, -7d)` |
| 指定日期范围创建 | `created >= '2026-03-01T00:00:00.000Z' AND created <= '2026-03-31T23:59:59.999Z'` |

> ⚠️ 项目没有截止时间（dueDate）字段，只有 `created` 和 `updated`。
>
> 完整项目 TQL → `references/project-tql.md`

---

## 常用命令示例

### 查询任务

```bash
# 我的待办任务
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false"
# 注意：返回的 executorId 是原始 ID，需批量调用 query_members.py --user-ids 转换为姓名后展示

# 我的逾期任务，按截止时间升序
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false AND dueDate < startOf(d) ORDER BY dueDate ASC"
# 返回的 executorId 需批量转换为姓名：uv run scripts/query_members.py --user-ids "<id1,id2,...>"

# 本周截止的任务
uv run scripts/query_tasks.py --tql "executorId = me() AND dueDate >= startOf(w) AND dueDate <= endOf(w)"

# 标题搜索
uv run scripts/query_tasks.py --tql "title ~ '需求'"

# 查询任务详情（simple 默认，含 note）
uv run scripts/query_task_detail.py <taskId>

# 查询详细信息（含自定义字段等）
uv run scripts/query_task_detail.py <taskId> --detail-level detailed

# 批量查询多个任务
uv run scripts/query_task_detail.py id1,id2,id3
```

### 创建任务

```bash
# 基本创建
uv run scripts/create_task.py --project-id 'xxx' --title '完成需求文档'

# 完整参数创建
uv run scripts/create_task.py \
  --project-id 'xxx' \
  --title '实现登录模块' \
  --executor-id 'uid' \
  --due-date '2026-04-01' \
  --priority 1 \
  --note '参考设计稿'
```

### 更新任务

```bash
# 更新标题和优先级（多字段并行执行）
uv run scripts/update_task.py --task-id 'xxx' --title '新标题' --priority 0

# 更新截止日期和执行人
uv run scripts/update_task.py --task-id 'xxx' --due-date '2026-04-01' --executor-id 'uid'

# 更新任务状态（先查询状态 ID）
uv run scripts/get_task_statuses.py <taskId>
uv run scripts/update_task.py --task-id 'xxx' --taskflowstatus-id '状态ID'

# 单独更新优先级
uv run scripts/update_task_priority.py --task-id 'xxx' --priority 0
```

### 查询项目

```bash
# 我参与的项目
uv run scripts/query_projects.py --tql "involveMembers = me()"

# 按名称搜索
uv run scripts/query_projects.py --tql "nameText ~ '产品开发'"

# 查询项目详情
uv run scripts/query_project_detail.py <projectId>

# 获取 organizationId（用于查询优先级配置）
uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId
```

### 查询成员和当前用户

```bash
# 按姓名搜索成员
uv run scripts/query_members.py --keyword '张三'

# 批量按用户ID查询成员（推荐用于ID转换）
uv run scripts/query_members.py --user-ids "id1,id2,id3"

# 获取当前登录用户信息（userId、name、email 等）
uv run scripts/get_current_user.py
```

### 创建评论（含 @提及）

```bash
# 创建评论并 @张三（--mention 接受姓名，脚本自动查询 userId）
uv run scripts/create_comment.py \
  --task-id 'xxx' \
  --content '请张三确认一下' \
  --mention '张三'

# @多人（逗号分隔）
uv run scripts/create_comment.py \
  --task-id 'xxx' \
  --content '请张三和李四评审' \
  --mention '张三,李四'

# 已知 userId 时可直接用 --mention-id
uv run scripts/create_comment.py \
  --task-id 'xxx' \
  --content '已更新' \
  --mention-id '61cad8021deea2ac89a4cbf3'
```

### 文件上传

```bash
# 第一步：上传文件，获取 fileToken
uv run scripts/upload_file.py \
  --file-path '/path/to/doc.pdf' \
  --scope 'task:<taskId>' \
  --category attachment

# 第二步：将 fileToken 附加到评论
uv run scripts/create_comment.py \
  --task-id 'xxx' \
  --content '附件已上传，请查收' \
  --file-tokens 'token1'
```

---

## 分页查询

`query_tasks.py` 和 `query_projects.py` 均支持分页：

| 参数 | 说明 |
|------|------|
| `--page-size <N>` | 每页记录数（默认由 API 决定） |
| `--page-token <T>` | 传入上次返回的 `nextPageToken` 获取下一页 |

```bash
# 第一页
uv run scripts/query_tasks.py --tql "executorId = me()" --page-size 50

# 下一页（使用上次输出中的 nextPageToken）
uv run scripts/query_tasks.py --tql "executorId = me()" --page-size 50 --page-token "上次返回的TOKEN"
```
