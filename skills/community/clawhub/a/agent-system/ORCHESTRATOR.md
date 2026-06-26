# Orchestrator — 核心智能调度系统

> **这是 OpenClaw 的最高层控制系统。所有 Agent 均受其调度。**

---

## 🎯 核心职责

Orchestrator 不是执行者，而是**协调者**：
- 决定何时调用哪个 Agent
- 监控结果质量，决定是否需要自愈
- 管理降级模式
- 收集 metrics 用于系统进化

---

## 📋 Master Prompt

```
你是 OpenClaw 的核心智能调度系统。

你的目标不是执行单个任务，而是：
→ 以"最优结果"为导向协调所有 Agent

决策原则：
1. 优先保证结果正确性，而不是速度
2. 如果任务复杂 → 必须规划（planner）
3. 如果结果质量低 → 必须触发自愈（self_heal）
4. 如果多次失败 → 降级但给出最优可行结果
5. 持续记录 metrics 用于进化

你要像一个"系统"，而不是函数。
```

---

## 🔄 标准调度流程

```
任务输入
    ↓
┌─────────────────┐
│  复杂度评估      │
│  (complexity)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   ≤3        >3
    │         │
    ▼         ▼
 Executor   Planner
    │         │
    │         ▼
    │     Executor
    │         │
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │ Reviewer │
    │  评分   │
    └────┬────┘
         │
    ┌────┴────┐
    │         │
  ≥70       <70
    │         │
    ▼         ▼
  输出      Self-Heal
    │         │
    │    ┌────┴────┐
    │    │         │
    │   <2       ≥2
    │    │         │
    │    ▼         ▼
    │  重试    degraded_mode
    │         （降级输出）
    └────┬────┘
         │
         ▼
       结束
```

---

## 📊 决策日志（JSON）

```json
{
  "timestamp": "2026-04-02T10:40:00+08:00",
  "level": "INFO",
  "module": "orchestrator",
  "event": "task_completed",
  "details": {
    "task_type": "analysis",
    "complexity": 6,
    "route": ["planner", "executor", "reviewer"],
    "final_score": 85,
    "heal_triggered": false,
    "degraded_mode": false
  }
}
```

### 关键事件日志

| 事件 | level | 触发条件 |
|------|-------|----------|
| `task_received` | INFO | 接收到新任务 |
| `route_decided` | INFO | 确定调度路线 |
| `heal_triggered` | WARNING | 触发自愈流程 |
| `degraded_mode_entered` | ERROR | 进入降级模式 |
| `task_completed` | INFO | 任务成功完成 |
| `task_failed` | ERROR | 任务失败（无法恢复） |

---

## ⚠️ 降级模式 (degraded_mode)

当连续 2 次自愈失败时进入：

- 输出最简可行结果（不是错误）
- 标注：`⚠️ 数据不完整，结论为推断值`
- 记录 `degraded_mode_count++`
- 继续服务，不卡死

---

## 🔗 相关文件

- `AGENT_RULES.md` — 各 Agent 执行规则
- `FAILURE_LOG.md` — 历史失败记录
- `METRICS.md` — 指标追踪

---

*最后更新：2026-04-02*
