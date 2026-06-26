---
name: agentic-engineering/supervising
description: Agentic Engineering 分支：Supervising。多 Agent 编排与监督，基于 LangGraph 状态机范式。触发：需要协调多个 Agent 协同工作、设计状态机流转、人机协同审批、长期运行系统的监督控制。
---

# Supervising — 多 Agent 编排与监督

## 定位

本分支是 `agentic-engineering` 的 supervising 子分支，专注：

- **状态维持型**范式（非任务交付型）
- 执行器常驻 idle，事件/状态变化触发唤醒
- 状态机的存在不是为了 close task，而是为了 **trigger task**

## 核心抽象：LangGraph 五大能力

| 能力 | 含义 | 适用场景 |
|------|------|----------|
| 持久化执行 | Checkpoint 快照，失败后从断点恢复 | 长时运行任务（天/周级） |
| 人机协同 | interrupt + Command(resume)，关键节点人工拦截 | 审批、风控、决策确认 |
| 全方位记忆 | 短期工作记忆 + 跨会话长期记忆 | 需要上下文连续性的系统 |
| 可观测性 | LangSmith 可视化调试 | 复杂 Agent 行为审计 |
| 生产级部署 | 可扩展基础设施 | 长期运行的有状态智能体系统 |

## 架构要素

### 1. State — 共享状态

所有节点共享的全局状态容器，TypedDict 定义，通过 Reducer 演进（不可变，追加而非覆盖）。

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    current_task: Optional[str]
    pending_approval: Optional[dict]
    executor_status: dict  # idle / running / waiting
```

### 2. Node — 执行器

每个 Node 是一个业务逻辑函数，接收 State，返回 State 更新。执行器生命周期 **独立于任务**——常驻 idle，被触发时唤醒。

```python
def supervisor_node(state: AgentState):
    """监督节点：检查状态，决定触发哪个执行器"""
    if state["pending_approval"]:
        return {"executor_status": {"approval_check": "running"}}
    return {"executor_status": {"idle": True}}
```

### 3. Edge — 流转控制

- **普通边**：顺序执行
- **条件边**：根据 State 动态路由（状态机核心）

```python
def should_trigger(state: AgentState) -> Literal["execute", "wait", "human_review"]:
    if state["pending_approval"]:
        return "human_review"
    if state["current_task"]:
        return "execute"
    return "wait"  # 保持 idle
```

### 4. Checkpoint — 断点恢复

每个 super-step 自动保存状态快照，支持：
- **中断恢复**：GraphInterrupt → Command(resume)
- **时间回溯**：回滚到历史 Checkpoint
- **人工审批**：interrupt_before / interrupt_after

### 5. Cycle — 循环推理

LangGraph 原生支持循环（区别于 DAG），实现 Agent 的"思考-行动-观察"闭环。

## 编排模式

### 模式 A：监督者模式（Supervisor）

```
Supervisor → 分配任务 → Executor A / B / C → 汇报结果 → Supervisor
     ↑                                                    |
     └──────────────── 状态检查 ←─────────────────────────┘
```

- Supervisor 是唯一决策者
- Executor 只执行，不自主行动
- 适用于：任务明确、流程可控的场景

### 模式 B：对抗辩论模式（Debate）

```
Analyst → Bull Agent ←→ Bear Agent → Research Manager → Trader
```

- 多视角对抗，暴露逻辑漏洞
- 适用于：决策风险高、需要多角度验证的场景

### 模式 C：事件驱动模式（Event-Driven）

```
Event Source → State Change → Condition Edge → Executor Wake → Back to Idle
```

- 执行器常态 idle，事件触发唤醒
- 适用于：持续运行系统、监控系统

## 人机协同策略

| 策略 | 触发方式 | 场景 |
|------|----------|------|
| 静态断点 | interrupt_before=["node"] | 已知高危操作 |
| 动态断点 | interrupt() 在节点内部 | 运行时条件触发 |
| 状态审查 | 人工修改 Checkpoint 后 resume | 需要修正 AI 决策 |

## 开发范式选择

| 范式 | 特点 | 适用 |
|------|------|------|
| Graph API | 显式 StateGraph + add_node/add_edge | 需要精细控制路由 |
| Functional API | @entrypoint + @task 装饰器 | Pythonic，if/else + while |

**建议**：先掌握 Graph API（理解 Checkpoint 和 State 流转），再用 Functional API 提升开发效率。

## 关键原则

1. **Trigger > Poll** — 事件驱动优于轮询，状态机的目的是 trigger task
2. **Idle is good** — 执行器常驻 idle 是正常态，不是浪费
3. **Checkpoint everything** — 每步都持久化，长时任务必须可恢复
4. **Human at the gate** — 高风险操作必须设人机协同断点
