---
name: agent-task-list
description: "独立任务列表系统。为每个 Agent 创建独立的任务队列管理，支持任务分配、状态更新、进度跟踪、历史记录。每个 Agent 拥有独立的任务队列，支持优先级调度、状态实时同步。"
description_en: "Independent task list system. Creates isolated task queue management for each Agent, supporting task assignment, status updates, progress tracking, and history. Each Agent has its own task queue with priority scheduling and real-time status synchronization."
---

> **路径变量说明**（本文档通用）：
> - `<TASK_ROOT>` = `~/.openclaw/workspace/skills/agent-task-list`
> - `<TASK_SCRIPTS>` = `<TASK_ROOT>/scripts`
> - `<TASK_DATA>` = `~/.openclaw/workspace/agent-tasks`

---

# Agent 独立任务列表系统

## 概述

为每个 Agent 创建独立的任务列表管理，支持：
- **独立任务队列**：每个 Agent 拥有自己的任务队列
- **任务优先级调度**：支持任务优先级排序和调度
- **状态实时同步**：任务状态变化实时同步
- **历史记录**：完整任务执行历史记录

## 核心概念

```
Agent A
├── current_task: 当前执行任务
├── pending_tasks: 待办任务队列（按优先级排序）
├── completed_tasks: 已完成任务历史
└── failed_tasks: 失败任务记录

Agent B
├── current_task: 当前执行任务
├── pending_tasks: 待办任务队列
├── completed_tasks: 已完成任务历史
└── failed_tasks: 失败任务记录
```

---

## 一、任务数据模型

### 1.1 任务类型

| 类型 | 字段名 | 说明 |
|------|--------|------|
| 当前任务 | `current_task` | Agent 正在执行的任务（单个） |
| 待办任务 | `pending_tasks` | 等待执行的任务队列（数组） |
| 已完成任务 | `completed_tasks` | 已完成的任务历史（数组） |
| 失败任务 | `failed_tasks` | 执行失败的任务记录（数组） |

### 1.2 任务属性

```typescript
interface Task {
  // 基础属性
  id: string;              // 任务 ID（唯一）
  name: string;            // 任务名称
  description: string;     // 任务描述
  
  // 状态属性
  status: TaskStatus;      // 任务状态
  priority: number;        // 优先级（1-10，数字越大优先级越高）
  
  // 时间属性
  assigned_at: string;     // 分配时间（ISO 8601）
  started_at?: string;     // 开始时间
  completed_at?: string;   // 完成时间
  failed_at?: string;      // 失败时间
  
  // 关联属性
  agent_id: string;        // 关联 Agent ID
  
  // 扩展属性
  metadata?: Record<string, any>;  // 扩展元数据
  error_message?: string;          // 失败时的错误信息
  retry_count?: number;            // 重试次数
}

type TaskStatus = 
  | 'pending'      // 待执行
  | 'running'      // 执行中
  | 'completed'    // 已完成
  | 'failed'       // 失败
  | 'cancelled';   // 已取消
```

### 1.3 Agent 任务列表结构

```typescript
interface AgentTaskList {
  agent_id: string;
  agent_name: string;
  current_task?: Task;
  pending_tasks: Task[];
  completed_tasks: Task[];
  failed_tasks: Task[];
  created_at: string;
  updated_at: string;
}
```

---

## 二、数据存储结构

### 2.1 目录结构

```
~/.openclaw/workspace/agent-tasks/
├── agents/
│   ├── agent-coder/
│   │   └── task-list.json
│   ├── agent-planner/
│   │   └── task-list.json
│   └── ...
├── history/
│   ├── 2026-04/
│   │   ├── task-001.json
│   │   └── task-002.json
│   └── ...
├── task-counter.txt      # 任务 ID 计数器
└── index.json           # 全局索引
```

### 2.2 任务列表文件（task-list.json）

```json
{
  "agent_id": "agent-coder",
  "agent_name": "代码开发 Agent",
  "current_task": {
    "id": "task-001",
    "name": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能",
    "status": "running",
    "priority": 8,
    "assigned_at": "2026-04-10T10:00:00+08:00",
    "started_at": "2026-04-10T10:05:00+08:00",
    "agent_id": "agent-coder"
  },
  "pending_tasks": [
    {
      "id": "task-002",
      "name": "实现用户注册功能",
      "description": "实现用户注册功能，包含邮箱验证",
      "status": "pending",
      "priority": 7,
      "assigned_at": "2026-04-10T10:10:00+08:00",
      "agent_id": "agent-coder"
    }
  ],
  "completed_tasks": [],
  "failed_tasks": [],
  "created_at": "2026-04-10T09:00:00+08:00",
  "updated_at": "2026-04-10T10:05:00+08:00"
}
```

### 2.3 全局索引（index.json）

```json
{
  "agents": [
    {
      "agent_id": "agent-coder",
      "agent_name": "代码开发 Agent",
      "task_count": {
        "current": 1,
        "pending": 5,
        "completed": 10,
        "failed": 2
      },
      "last_updated": "2026-04-10T10:05:00+08:00"
    }
  ],
  "total_tasks": {
    "current": 1,
    "pending": 5,
    "completed": 10,
    "failed": 2
  }
}
```

---

## 三、任务分配算法

### 3.1 优先级调度

```python
def get_next_task(pending_tasks: List[Task]) -> Optional[Task]:
    """
    从待办队列中获取下一个任务
    
    调度策略：
    1. 按优先级降序排序
    2. 优先级相同时，按分配时间升序排序（先进先出）
    """
    if not pending_tasks:
        return None
    
    # 排序：优先级降序，分配时间升序
    sorted_tasks = sorted(
        pending_tasks,
        key=lambda t: (-t['priority'], t['assigned_at'])
    )
    
    return sorted_tasks[0]
```

### 3.2 任务分配流程

```
1. 创建任务 → pending_tasks
2. Agent 空闲时 → 从 pending_tasks 获取最高优先级任务
3. 任务开始执行 → pending_tasks → current_task
4. 任务完成 → current_task → completed_tasks
5. 任务失败 → current_task → failed_tasks
```

---

## 四、任务状态流转

### 4.1 状态机

```
        创建任务
          ↓
      [pending]
          ↓ (Agent 开始执行)
      [running]
          ↓
    ┌─────┴─────┐
    ↓           ↓
[completed]  [failed]
    ↓           ↓
  归档历史    记录错误
```

### 4.2 状态转换规则

| 转换 | 触发条件 | 操作 |
|------|----------|------|
| pending → running | Agent 开始执行任务 | 设置 started_at，从 pending_tasks 移除 |
| running → completed | 任务执行成功 | 设置 completed_at，从 current_task 移除，添加到 completed_tasks |
| running → failed | 任务执行失败 | 设置 failed_at、error_message，从 current_task 移除，添加到 failed_tasks |
| running → cancelled | 用户取消任务 | 设置 cancelled_at，从 current_task 移除 |
| pending → cancelled | 用户取消待办任务 | 从 pending_tasks 移除 |

---

## 五、API 设计

### 5.1 任务管理 API

#### 创建任务

```bash
# 创建新任务
python3 <TASK_SCRIPTS>/task_manager.py create \
  --agent <agent_id> \
  --name "<任务名称>" \
  --description "<任务描述>" \
  --priority <1-10>
```

**返回：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已添加到待办队列"
}
```

#### 获取 Agent 任务列表

```bash
# 获取指定 Agent 的任务列表
python3 <TASK_SCRIPTS>/task_manager.py list --agent <agent_id>

# 获取所有 Agent 的任务概览
python3 <TASK_SCRIPTS>/task_manager.py list-all
```

**返回：**
```json
{
  "agent_id": "agent-coder",
  "current_task": {...},
  "pending_tasks": [...],
  "completed_tasks": [...],
  "failed_tasks": [...]
}
```

#### 开始执行任务

```bash
# Agent 开始执行下一个待办任务
python3 <TASK_SCRIPTS>/task_manager.py start --agent <agent_id>
```

**返回：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "task": {...},
  "message": "任务已开始执行"
}
```

#### 完成任务

```bash
# 标记当前任务为完成
python3 <TASK_SCRIPTS>/task_manager.py complete --agent <agent_id>
```

**返回：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已完成"
}
```

#### 标记任务失败

```bash
# 标记当前任务为失败
python3 <TASK_SCRIPTS>/task_manager.py fail \
  --agent <agent_id> \
  --error "<错误信息>"
```

**返回：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已标记为失败"
}
```

#### 取消任务

```bash
# 取消当前任务或待办任务
python3 <TASK_SCRIPTS>/task_manager.py cancel \
  --agent <agent_id> \
  --task-id <task_id>
```

#### 获取任务详情

```bash
# 获取指定任务的详细信息
python3 <TASK_SCRIPTS>/task_manager.py get \
  --task-id <task_id>
```

#### 重试失败任务

```bash
# 将失败任务重新加入待办队列
python3 <TASK_SCRIPTS>/task_manager.py retry \
  --agent <agent_id> \
  --task-id <task_id>
```

### 5.2 查询 API

#### 查询任务

```bash
# 按状态查询
python3 <TASK_SCRIPTS>/task_manager.py query \
  --agent <agent_id> \
  --status <pending|running|completed|failed>

# 按优先级查询
python3 <TASK_SCRIPTS>/task_manager.py query \
  --agent <agent_id> \
  --min-priority <1-10>

# 按时间范围查询
python3 <TASK_SCRIPTS>/task_manager.py query \
  --agent <agent_id> \
  --from <ISO8601> \
  --to <ISO8601>
```

#### 统计信息

```bash
# 获取任务统计
python3 <TASK_SCRIPTS>/task_manager.py stats --agent <agent_id>
```

**返回：**
```json
{
  "agent_id": "agent-coder",
  "total": {
    "current": 1,
    "pending": 5,
    "completed": 10,
    "failed": 2
  },
  "success_rate": 0.83,
  "avg_completion_time": "25m"
}
```

---

## 六、使用示例

### 6.1 创建任务

```bash
# 为代码 Agent 创建一个任务
python3 <TASK_SCRIPTS>/task_manager.py create \
  --agent agent-coder \
  --name "实现用户登录功能" \
  --description "实现基于 JWT 的用户登录功能，包含密码加密和 Token 生成" \
  --priority 8
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已添加到 agent-coder 的待办队列"
}
```

### 6.2 Agent 开始工作

```bash
# Agent 检查是否有待办任务并开始执行
python3 <TASK_SCRIPTS>/task_manager.py start --agent agent-coder
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "task": {
    "id": "task-001",
    "name": "实现用户登录功能",
    "status": "running",
    "priority": 8
  },
  "message": "任务已开始执行"
}
```

### 6.3 完成任务

```bash
# 任务执行完成后标记为完成
python3 <TASK_SCRIPTS>/task_manager.py complete --agent agent-coder
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已完成，已归档到历史记录"
}
```

### 6.4 查看任务列表

```bash
# 查看 Agent 的任务列表
python3 <TASK_SCRIPTS>/task_manager.py list --agent agent-coder
```

**输出：**
```json
{
  "agent_id": "agent-coder",
  "agent_name": "代码开发 Agent",
  "current_task": null,
  "pending_tasks": [
    {
      "id": "task-002",
      "name": "实现用户注册功能",
      "priority": 7
    }
  ],
  "completed_tasks": [
    {
      "id": "task-001",
      "name": "实现用户登录功能",
      "completed_at": "2026-04-10T11:30:00+08:00"
    }
  ],
  "failed_tasks": []
}
```

---

## 七、脚本说明

### 7.1 task_manager.py（核心管理脚本）

```bash
# 任务创建
python3 <TASK_SCRIPTS>/task_manager.py create \
  --agent <agent_id> \
  --name <name> \
  --description <desc> \
  --priority <1-10>

# 任务列表
python3 <TASK_SCRIPTS>/task_manager.py list --agent <agent_id>
python3 <TASK_SCRIPTS>/task_manager.py list-all

# 任务执行
python3 <TASK_SCRIPTS>/task_manager.py start --agent <agent_id>
python3 <TASK_SCRIPTS>/task_manager.py complete --agent <agent_id>
python3 <TASK_SCRIPTS>/task_manager.py fail --agent <agent_id> --error <error>
python3 <TASK_SCRIPTS>/task_manager.py cancel --agent <agent_id> --task-id <task_id>

# 任务查询
python3 <TASK_SCRIPTS>/task_manager.py get --task-id <task_id>
python3 <TASK_SCRIPTS>/task_manager.py query --agent <agent_id> --status <status>

# 任务重试
python3 <TASK_SCRIPTS>/task_manager.py retry --agent <agent_id> --task-id <task_id>

# 统计信息
python3 <TASK_SCRIPTS>/task_manager.py stats --agent <agent_id>

# 历史记录
python3 <TASK_SCRIPTS>/task_manager.py history --agent <agent_id> --limit <n>
```

---

## 八、注意事项

1. **任务 ID 唯一性**：全局任务 ID 必须唯一，通过计数器保证
2. **并发安全**：多 Agent 同时操作时需加锁
3. **数据持久化**：所有状态变更需立即写入文件
4. **历史记录**：完成任务自动归档到 history 目录
5. **优先级范围**：1-10，数字越大优先级越高

---

## 九、扩展功能

### 9.1 任务依赖

未来可扩展任务依赖关系：
```json
{
  "depends_on": ["task-001", "task-002"]
}
```

### 9.2 任务分组

支持任务分组/标签：
```json
{
  "tags": ["feature", "urgent"],
  "group": "user-auth-module"
}
```

### 9.3 任务通知

任务状态变化时发送通知：
- 任务开始执行
- 任务完成
- 任务失败

---

## 意见反馈

欢迎提交 Issue 或 Pull Request！

---

## Changelog

### 2026-04-10

#### 新增
- 独立任务列表系统设计
- 任务数据模型定义
- 任务分配算法
- 任务状态流转逻辑
- 任务管理 API
- 核心管理脚本
