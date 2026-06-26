# Agent Concurrency Controller

>
> OpenClaw Agent并发安全调度器
> 基于Claude Code三层架构模式（Tool→ToolUse→Task）实现
>
> **核心原则**：默认Fail-Closed，串行队列，显式权限日志

## 背景问题

原生OpenClaw spawn子Agent时：
- 6个cron任务因**isolated session网络冲突**频繁失败
- 敏感操作（公众号发布、文件覆盖）无**权限审计**
- 大结果直接回显导致**token爆炸**

**根因**：Claude Code原生的Agent调度缺乏并发安全控制

## 解决方案

### 1. 三层调度模型

```
┌─────────────────────────────────────────┐
│  Layer 3: Task Queue (队列层)           │
│  - 优先级排序 (priority: 1-10)           │
│  - 依赖图拓扑排序                         │
│  - 串行消费（默认）                       │
└─────────────────────────────────────────┘
                    ↓ 出队
┌─────────────────────────────────────────┐
│  Layer 2: ToolUse Context (执行层)        │
│  - 权限检查 (checkPermissions)           │
│  - 并发安全检查 (isConcurrencySafe)       │
│  - 超时熔断机制                           │
└─────────────────────────────────────────┘
                    ↓ spawn
┌─────────────────────────────────────────┐
│  Layer 1: Agent Instance (实例层)         │
│  - isolated session (默认)               │
│  - main session (上下文连续任务)           │
│  - subagent 生命周期管理                   │
└─────────────────────────────────────────┘
```

### 2. Fail-Closed默认值

参考Claude Code原始设计：

```python
TOOL_DEFAULTS = {
    isConcurrencySafe: () => False,  # 默认串行
    isReadOnly: () => False,          # 默认会修改
    isDestructive: () => False,       # 默认不破坏
    checkPermissions: () => ({ behavior: 'allow' }),
}
```

**应用到OpenClaw**：
- 所有spawn操作默认 `is_concurrency_safe=False`
- 必须显式声明才能并行
- 资源冲突自动降级为串行

### 3. 敏感操作分级

| Level | 说明 | 行为 | 示例 |
|-------|------|------|------|
| **normal** | 普通操作 | ALLOW + LOG | 查询、搜索 |
| **sensitive** | 敏感操作 | ALLOW + LOG | 文件覆盖、配置修改 |
| **critical** | 关键操作 | ASK + LOG | 公众号发布、付款、外发 |

### 4. Coordinator协调原则

参考Claude Code Coordinator原始设计，应用于cron调度：

**原则1：永远先Synthesize**
```
错误：子Agent直接回给用户
正确：子Agent结果 → 父Agent合成 → 统一输出
```

**原则2：并行是默认策略（需显式安全标记）**
```
is_concurrency_safe=True 才能并发
否则串行队列
```

**原则3：Worker结果 = 内部信号**
```
不是对话伙伴，是状态机触发器
MAINTENANCE_REPORT 格式输出
```

## 使用方式

### Python API

```python
from agent_concurrency_controller import spawn_agent_safe, on_agent_complete

# 安全spawn Agent（默认Fail-Closed）
result = spawn_agent_safe(
    task="调研Claude Code架构",
    agent_type="researcher",
    runtime="subagent",
    priority=3,                    # 优先级（越小越高）
    is_concurrency_safe=False,     # Fail-Closed（默认）
    sensitive_level="normal",      # normal/sensitive/critical
    timeout_seconds=300
)

# result: QUEUED:researcher-20260403-151500
#          or STARTED:researcher-20260403-151500

# 任务完成回调
on_agent_complete(
    task_id="researcher-20260403-151500",
    success=True,
    result={"output": "调研完成"}
)
```

### Skill集成

在SKILL.md中声明：
```yaml
whenToUse: |
  需要spawn子Agent时先检查队列深度
  避免并行isolated session导致网络冲突
permissions:
  - agent:spawn (带队列控制)
  - file:write (日志目录)
  - log:append
```

## 日志审计

### 并发日志 (`logs/agent-concurrency.log`)
```json
{"timestamp": "2026-04-03T15:15:00", "task_id": "researcher-001", "status": "QUEUED", "queue_depth": 2}
{"timestamp": "2026-04-03T15:16:30", "task_id": "researcher-001", "status": "START_FROM_QUEUE", "queue_depth": 1}
{"timestamp": "2026-04-03T15:18:00", "task_id": "researcher-001", "status": "COMPLETED"}
```

### 敏感操作日志 (`logs/sensitive-operations.log`)
```json
{"timestamp": "2026-04-03T15:20:00", "task_id": "publisher-001", "sensitive_level": "critical", "decision": "ASK_USER_CONFIRMATION"}
```

## 部署验证

验证队列功能：
```powershell
python skills/agent-concurrency-controller/agent_concurrency_controller.py
```

输出：`{'running': [], 'pending': [], 'queue_depth': 0}`

## 迁移检查清单

将旧cron任务迁移到安全调度器：

- [ ] 识别所有 `sessions_spawn` 调用
- [ ] 添加 `is_concurrency_safe` 标记（默认False）
- [ ] 设置 `sensitive_level`（外发=critical）
- [ ] 添加 `on_agent_complete` 回调
- [ ] 验证日志输出

## 关联文件

| 文件 | 作用 |
|------|------|
| `agent_concurrency_controller.py` | 核心控制器实现 |
| `logs/agent-concurrency.log` | 队列执行日志 |
| `logs/sensitive-operations.log` | 权限审计日志 |
| `memory/agent-queue-state.json` | 队列状态持久化 |

## 参考

- Claude Code 架构：`memory/learnings/claude-code-architecture-2026-04-03.md`
- Claude Code 源码：https://github.com/ultraworkers/claw-code-parity
- 安全设计：https://clawhub.ai/1491007406/cc-insider

## 版本

- **v1.0.0** (2026-04-03): 初始实现，Fail-Closed并发控制+敏感权限日志
