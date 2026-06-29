# Agent 独立任务列表系统

为每个 Agent 创建独立的任务队列管理，支持任务分配、状态更新、进度跟踪、历史记录。

## 功能特性

- ✅ **独立任务队列**：每个 Agent 拥有自己的任务队列
- ✅ **任务优先级调度**：支持任务优先级排序和调度（1-10）
- ✅ **状态实时同步**：任务状态变化实时同步
- ✅ **历史记录**：完整任务执行历史记录
- ✅ **任务重试**：支持失败任务重试
- ✅ **统计信息**：任务统计和成功率计算

## 任务类型

| 类型 | 字段名 | 说明 |
|------|--------|------|
| 当前任务 | `current_task` | Agent 正在执行的任务（单个） |
| 待办任务 | `pending_tasks` | 等待执行的任务队列（数组） |
| 已完成任务 | `completed_tasks` | 已完成的任务历史（数组） |
| 失败任务 | `failed_tasks` | 执行失败的任务记录（数组） |

## 任务属性

```typescript
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
```

## 快速开始

### 1. 创建任务

```bash
# 为代码 Agent 创建一个任务
python3 scripts/task_manager.py create \
  --agent agent-coder \
  --name "实现用户登录功能" \
  --description "实现基于 JWT 的用户登录功能" \
  --priority 8
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "task": {
    "id": "task-001",
    "name": "实现用户登录功能",
    "status": "pending",
    "priority": 8
  },
  "message": "任务已添加到 agent-coder 的待办队列"
}
```

### 2. 开始执行任务

```bash
# Agent 开始执行下一个待办任务
python3 scripts/task_manager.py start --agent agent-coder
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "task": {
    "id": "task-001",
    "name": "实现用户登录功能",
    "status": "running"
  },
  "message": "任务已开始执行"
}
```

### 3. 完成任务

```bash
# 任务执行完成后标记为完成
python3 scripts/task_manager.py complete --agent agent-coder
```

**输出：**
```json
{
  "status": "success",
  "task_id": "task-001",
  "message": "任务已完成，已归档到历史记录"
}
```

### 4. 查看任务列表

```bash
# 查看 Agent 的任务列表
python3 scripts/task_manager.py list --agent agent-coder
```

## 命令参考

### 任务管理

| 命令 | 说明 |
|------|------|
| `create` | 创建新任务 |
| `start` | 开始执行任务 |
| `complete` | 完成任务 |
| `fail` | 标记任务失败 |
| `cancel` | 取消任务 |
| `retry` | 重试失败任务 |

### 查询命令

| 命令 | 说明 |
|------|------|
| `list` | 获取 Agent 任务列表 |
| `list-all` | 获取所有 Agent 任务概览 |
| `get` | 获取任务详情 |
| `query` | 查询任务（支持过滤） |
| `stats` | 获取统计信息 |
| `history` | 获取历史记录 |

## 任务状态流转

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

## 优先级调度

任务按优先级降序排序，优先级相同时按分配时间升序排序（先进先出）：

```python
# 排序规则
sorted_tasks = sorted(
    pending_tasks,
    key=lambda t: (-t['priority'], t['assigned_at'])
)
```

## 数据存储

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
├── task-counter.txt
└── index.json
```

## 运行测试

```bash
# 运行所有单元测试
python3 scripts/test_task_manager.py
```

## 注意事项

1. **任务 ID 唯一性**：全局任务 ID 必须唯一，通过计数器保证
2. **并发安全**：多 Agent 同时操作时需加锁
3. **数据持久化**：所有状态变更需立即写入文件
4. **历史记录**：完成任务自动归档到 history 目录
5. **优先级范围**：1-10，数字越大优先级越高

## 扩展功能

### 任务依赖

未来可扩展任务依赖关系：

```json
{
  "depends_on": ["task-001", "task-002"]
}
```

### 任务分组

支持任务分组/标签：

```json
{
  "tags": ["feature", "urgent"],
  "group": "user-auth-module"
}
```

### 任务通知

任务状态变化时发送通知：
- 任务开始执行
- 任务完成
- 任务失败

## 与 STP 集成

本系统可与 STP（结构化任务规划）系统集成：

1. STP 创建任务计划
2. 任务计划作为任务添加到本系统
3. Agent 从本系统获取任务并执行
4. 执行结果反馈到本系统

## 贡献

欢迎提交 Issue 或 Pull Request！

## License

MIT
