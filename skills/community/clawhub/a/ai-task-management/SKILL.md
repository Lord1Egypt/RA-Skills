---
name: ai-task-management
description: 零依赖、高性能的任务管理技能。当用户需要创建、查询、更新、删除任务或获取任务统计时使用此技能。
version: 1.0.0
platform: macOS (Apple Silicon)
---

## 触发条件

当用户提到以下关键词或意图时触发此技能：

### 创建任务
- "创建任务"、"新建任务"、"添加一个任务"、"帮我记个事"
- "我要做一个..."、"记得做..."、"提醒我..."

### 查询任务
- "查看任务"、"查询任务"、"我的任务"、"有什么任务"
- "待处理的任务"、"未完成的任务"

### 更新任务
- "更新任务"、"提交初审"、"取消任务"、"修改任务"
- "完成初核"
- "标记为已完成"、"删除任务"

### 任务统计
- "任务统计"、"任务概况"、"有多少任务"
- "完成情况如何"

### 任务详情
- "任务详情"、"查看某个任务"、"任务信息"

### 回收任务
- "回收任务"、"任务到期"、"重置任务状态"

### 删除任务
- "彻底删除"、"物理删除"、"删除任务"

### 更新技能
- "更新技能"、"升级技能"、"检查更新"


## 安装

### 方式一：通过 pip 安装（推荐）

```bash
# 从 GitHub 安装最新版本
pip install git+https://github.com/xfwgithub/aitask-skill.git

# 或从本地源码安装
git clone https://github.com/xfwgithub/aitask-skill.git
cd aitask-skill
pip install -e .
```

### 方式二：直接下载二进制

```bash
# 下载最新版本的完整包（包含 Web UI 静态资源）
wget https://github.com/xfwgithub/aitask-skill/releases/latest/download/task-skill.zip
unzip task-skill.zip
cd task-skill
./task-skill --version

# 或者下载指定版本
# wget https://github.com/xfwgithub/aitask-skill/releases/download/v0.4.3/task-skill-v0.4.3.zip
```

## 配置 AI Agent 技能

安装完成后，将 `SKILL.md` 复制到你的 AI Agent 技能目录：

```bash
# 复制 SKILL.md 到技能目录（只复制这个文件！）
cp /path/to/SKILL.md <你的技能目录>/task-management/

# 验证
ls <你的技能目录>/task-management/
# 应该只看到 SKILL.md 文件
```

**重要说明**：
- ✅ 技能目录**只需要** `SKILL.md` 文件
- ✅ 二进制文件和静态资源会自动下载到 Python 包目录
- ❌ **不要**把整个 task-skill 包复制到技能目录
- ℹ️ 技能目录位置取决于你使用的 IDE/Agent 配置

## 初始化

安装完成后，验证安装：

```bash
# 查看版本
task-skill --version

# 查看帮助
task-skill --help

# 启动 Web 服务器（用于人机协作界面）
task-skill --server
```

## 工具函数

### create-task
创建新任务

**参数**:
- `--title` (string, 必需): 任务标题
- `--project` (string, 必需): 项目名称
- `--description` (string, 可选): 任务描述
- `--priority` (int, 可选): 优先级 1-4（1=Critical/2=High/3=Medium/4=Low），默认 3
- `--assignee` (string, 可选): 负责人姓名
- `--parent` (string, 可选): 父任务 UUID（创建子任务时使用）

**调用示例**:
```bash
# 创建普通任务
task-skill create-task --title "审查文档" --project "aitask-skill" --priority 2 --description "检查完整性"

# 创建子任务
task-skill create-task --title "子任务-收集资料" --project "demo" --parent abc-123
```

### list-tasks / ls
查询任务列表

**参数**:
- `--status` (string, 可选): 状态筛选（pending/agent_working/agent_review/human_review/done/cancelled）
- `--project` (string, 可选): 项目筛选
- `--limit` (int, 可选): 返回数量限制

**调用示例**:
```bash
task-skill list-tasks --status pending
task-skill ls --project demo --limit 10
```

### get-task
获取任务详情

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill get-task abc-123
```

### claim-task
领取任务（pending → agent_working）

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill claim-task abc-123
```

### submit-review
提交初审（agent_working → agent_review）

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill submit-review abc-123
```

### review-task
提交人工审核（agent_review → human_review）

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill review-task abc-123
```

### approve-task
人工审核通过（human_review → done）

**⚠️ 警告**: 此命令属于人工审核步骤。除非用户明确指示“审核通过”或“标记为已完成”，否则 AI Agent 绝对不能自动调用此命令！

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill approve-task abc-123
```

### cancel-task
取消任务（任意状态 → cancelled）

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill cancel-task abc-123
```

**任务状态说明**：
- `pending` - 待办（等待 agent 领取）
- `agent_working` - Agent 工作中（agent 已领取，正在处理）
- `agent_review` - Agent 审核中（agent 提交初审后，等待 agent 自己审核确认）
- `human_review` - 人工审核中（agent 审核通过后，提交给人工审核）
- `done` - 完成（人工审核通过。**注意：AI Agent 不得擅自将任务变更为此状态，必须由人类明确授权**）
- `cancelled` - 已取消

### delete-task
物理删除任务（彻底删除）

**注意**: 此操作不可恢复，请谨慎使用！建议先使用 `cancel-task` 将任务状态改为 cancelled（取消），确认不再需要后再使用此功能彻底删除。

**参数**:
- `uuid` (string, 必需): 任务 UUID

**调用示例**:
```bash
task-skill delete-task abc-123
```

### recycle-tasks
回收到期未完成的 Agent 任务

**逻辑**:
- 回收 `due_date` 之前创建的、状态为 `agent_working` 的任务
- 回收后任务状态变为 `pending`（重新进入待办池）

**参数**:
- `--due-date` (string, 可选): 截止时间，回收此日期前创建的超时任务

**调用示例**:
```bash
task-skill recycle-tasks --due-date 2026-03-22
```

### stats
获取仪表盘统计信息

**参数**: 无

**调用示例**:
```bash
task-skill stats
```
