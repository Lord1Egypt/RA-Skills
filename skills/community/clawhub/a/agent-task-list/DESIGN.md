# Agent 独立任务列表系统 - 设计文档

## 概述

本系统为每个 Agent 创建独立的任务队列管理，支持任务分配、状态更新、进度跟踪、历史记录。每个 Agent 拥有自己的任务队列，支持优先级调度、状态实时同步。

## 交付物清单

### 1. 任务数据模型 ✅

**文件**: `SKILL.md` 第一章

**核心数据结构**:

```typescript
// 任务属性
interface Task {
  id: string;              // 任务 ID（唯一）
  name: string;            // 任务名称
  description: string;     // 任务描述
  status: TaskStatus;      // 任务状态
  priority: number;        // 优先级（1-10）
  assigned_at: string;     // 分配时间
  started_at?: string;     // 开始时间
  completed_at?: string;   // 完成时间
  failed_at?: string;      // 失败时间
  agent_id: string;        // 关联 Agent ID
  metadata?: any;          // 扩展元数据
  error_message?: string;  // 失败时的错误信息
  retry_count?: number;    // 重试次数
}

// Agent 任务列表
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

### 2. 任务分配算法 ✅

**文件**: `SKILL.md` 第三章，`task_manager.py` 中的 `create_task` 和 `start_task`

**调度策略**:
1. 按优先级降序排序
2. 优先级相同时，按分配时间升序排序（先进先出）

```python
def get_next_task(pending_tasks: List[Task]) -> Optional[Task]:
    if not pending_tasks:
        return None
    
    # 排序：优先级降序，分配时间升序
    sorted_tasks = sorted(
        pending_tasks,
        key=lambda t: (-t['priority'], t['assigned_at'])
    )
    
    return sorted_tasks[0]
```

### 3. 任务状态流转逻辑 ✅

**文件**: `SKILL.md` 第四章，`task_manager.py` 中的状态转换函数

**状态机**:

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

**状态转换函数**:
- `create_task()`: 创建任务 → pending
- `start_task()`: pending → running
- `complete_task()`: running → completed
- `fail_task()`: running → failed
- `cancel_task()`: pending/running → cancelled
- `retry_task()`: failed → pending

### 4. 任务列表 API 设计 ✅

**文件**: `SKILL.md` 第五章，`task_manager.py`

**API 列表**:

| API | 功能 | 参数 |
|-----|------|------|
| `create` | 创建任务 | --agent, --name, --description, --priority |
| `list` | 获取 Agent 任务列表 | --agent |
| `list-all` | 获取所有 Agent 概览 | - |
| `get` | 获取任务详情 | --task-id |
| `start` | 开始执行任务 | --agent |
| `complete` | 完成任务 | --agent |
| `fail` | 标记任务失败 | --agent, --error |
| `cancel` | 取消任务 | --agent, --task-id |
| `retry` | 重试失败任务 | --agent, --task-id |
| `query` | 查询任务 | --agent, --status, --min-priority |
| `stats` | 获取统计信息 | --agent |
| `history` | 获取历史记录 | --agent, --limit |

## 技术实现

### 文件结构

```
~/.openclaw/workspace/skills/agent-task-list/
├── SKILL.md              # 技能文档
├── README.md             # 使用文档
├── DESIGN.md             # 设计文档（本文档）
└── scripts/
    ├── task_manager.py   # 核心管理脚本
    └── test_task_manager.py  # 单元测试
```

### 数据存储

```
~/.openclaw/workspace/agent-tasks/
├── agents/
│   ├── agent-coder/
│   │   └── task-list.json
│   └── agent-planner/
│       └── task-list.json
├── history/
│   ├── 2026-04/
│   │   ├── task-001.json
│   │   └── task-002.json
│   └── ...
├── task-counter.txt      # 任务 ID 计数器
└── index.json           # 全局索引
```

### 核心类/函数

**task_manager.py**:
- `create_task()`: 创建任务
- `start_task()`: 开始执行任务
- `complete_task()`: 完成任务
- `fail_task()`: 标记任务失败
- `cancel_task()`: 取消任务
- `retry_task()`: 重试失败任务
- `list_tasks()`: 获取任务列表
- `query_tasks()`: 查询任务
- `get_stats()`: 获取统计信息
- `get_history()`: 获取历史记录

## 测试覆盖

**单元测试**: `test_task_manager.py`

**测试用例**:
1. ✅ test_create_task - 创建任务
2. ✅ test_create_multiple_tasks - 创建多个任务
3. ✅ test_start_task - 开始执行任务
4. ✅ test_complete_task - 完成任务
5. ✅ test_fail_task - 任务失败
6. ✅ test_retry_task - 重试失败任务
7. ✅ test_cancel_task - 取消任务
8. ✅ test_query_tasks - 查询任务
9. ✅ test_get_stats - 获取统计信息
10. ✅ test_get_task - 获取任务详情
11. ✅ test_list_all_agents - 获取所有 Agent 概览
12. ✅ test_priority_validation - 优先级验证
13. ✅ test_start_task_without_pending - 无待办任务时开始
14. ✅ test_complete_task_without_current - 无当前任务时完成

**测试结果**: 14/14 通过

## 使用示例

### 完整工作流

```bash
# 1. 创建任务
python3 scripts/task_manager.py create \
  --agent agent-coder \
  --name "实现用户登录功能" \
  --description "实现基于 JWT 的用户登录功能" \
  --priority 8

# 2. 查看待办任务
python3 scripts/task_manager.py list --agent agent-coder

# 3. 开始执行任务
python3 scripts/task_manager.py start --agent agent-coder

# 4. 完成任务
python3 scripts/task_manager.py complete --agent agent-coder

# 5. 查看统计信息
python3 scripts/task_manager.py stats --agent agent-coder

# 6. 查看历史记录
python3 scripts/task_manager.py history --agent agent-coder
```

## 技术要点

1. **独立任务队列**: 每个 Agent 有独立的 task-list.json 文件
2. **优先级调度**: 待办队列按优先级降序、分配时间升序排序
3. **状态实时同步**: 每次状态变更立即写入文件
4. **历史记录**: 完成任务自动归档到 history 目录（按月份）
5. **全局索引**: index.json 记录所有 Agent 的任务统计

## 扩展性

### 任务依赖

```json
{
  "depends_on": ["task-001", "task-002"]
}
```

### 任务分组

```json
{
  "tags": ["feature", "urgent"],
  "group": "user-auth-module"
}
```

### 任务通知

- 任务开始执行时通知
- 任务完成时通知
- 任务失败时通知

## 与 STP 集成

本系统可与 STP（结构化任务规划）系统集成：

1. STP 创建任务计划
2. 任务计划作为任务添加到本系统
3. Agent 从本系统获取任务并执行
4. 执行结果反馈到本系统

## 总结

本系统完成了以下交付物：

1. ✅ **任务数据模型扩展**: 完整的 Task 和 AgentTaskList 接口定义
2. ✅ **任务分配算法**: 基于优先级的调度算法
3. ✅ **任务状态流转逻辑**: 完整的状态机和状态转换函数
4. ✅ **任务列表 API 设计**: 12 个 API 接口，涵盖所有任务管理功能

**技术实现**:
- 核心脚本：`task_manager.py` (700+ 行)
- 单元测试：`test_task_manager.py` (14 个测试用例，全部通过)
- 文档：SKILL.md、README.md、DESIGN.md

**设计原则**:
- 每个 Agent 独立任务队列
- 支持优先级调度
- 任务状态实时同步
- 完整历史记录
