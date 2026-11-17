# 多智能体编排 Playbook

> 配合 [skills/multi-agent-orchestration](../skills/multi-agent-orchestration/SKILL.md) 使用。本篇是「决策方法论」层：何时上多 Agent、怎么选模式 / 框架、通信怎么搭、踩坑怎么救。子技能里放不下的判断与坑都在这里。

## 1. 决策树：多 Agent 还是单 Agent？

```
任务来了
├─ 能否由一个 Agent + 几个工具在 < 1 轮内完成？ ── 是 ─→ 单 Agent（别编排）
├─ 需要 ≥2 种专职角色且产出要互相依赖？ ── 是 ─→ 多 Agent
├─ 多个独立侧面要并行提速 / 增多样性？ ── 是 ─→ 多 Agent（并行）
├─ 需要多视角辩论 / 互相挑错来提质？ ── 是 ─→ 多 Agent（共识）
└─ 失败要隔离、单点不能拖垮整体？ ── 是 ─→ 多 Agent（韧性）
```

红线：

- 任务能一次说清、无需角色拆分 → 单 Agent。多 Agent 带来通信开销、上下文膨胀、成本翻倍。
- 「为了看起来高级」而上多 Agent 是最常见的反模式。

## 2. 决策树：选哪种编排模式？

```
子任务之间
├─ 强顺序依赖（A 的输出是 B 的输入） ──→ 顺序链
├─ 完全独立、可同时跑 ──→ 并行
├─ 有「总控 + 多个专家」的层级 ──→ 层次（Manager→Specialist）
├─ 需要多方辩论达成共识 / 仲裁 ──→ 共识
└─ 大型系统、Agent 间弱耦合、靠共享存储协作 ──→ 工具中介
```

要点：

- 顺序链最容易实现也最稳，先用它。
- 并行要小心「聚合」这一步：多份结果怎么去重 / 加权 / 冲突消解，提前定规则。
- 层次模式里 Manager 只做编排与质检，别让它既当裁判又当运动员（把所有活都自己干）。

## 3. 框架选型矩阵

| 框架 | 最佳场景 | 强项 | 注意 | 代码骨架 |
|------|---------|------|------|---------|
| CrewAI | 角色清晰、层级结构 | Agent/Task/Crew 概念直观，sequential/hierarchical process | 复杂状态 / 有环流程不擅长 | `Crew(agents=..., tasks=..., process=Process.sequential)` |
| AutoGen | 多轮对话、协商、谈判 | GroupChat + Manager，speaker 自动选择 | 轮次（max_round）要控，否则无限聊 | `GroupChat(agents=..., max_round=10)` + `GroupChatManager` |
| LangGraph | 有状态 / 有环工作流 | StateGraph 显式节点与边，可编译可持久化 | 样板代码多，状态 schema 要设计 | `StateGraph(State).add_node().add_edge().compile()` |
| Swarm | 简单 handoff、对话式路由 | Agent + functions 做路由，极轻 | 只适合简单分流，无复杂编排 | `Swarm().run(agent=triage, messages=...)` |

选型口诀：**要角色 → CrewAI；要聊天协商 → AutoGen；要状态 / 有环 → LangGraph；要分流 → Swarm。**

## 4. 通信协议

### 4.1 直连消息

适合 Agent 数量少、关系固定。

```python
agent_a.send_message(agent_b, {
    "type": "request",
    "action": "analyze_document",
    "document": doc_content,
    "context": {"deadline": "urgent"},
})
```

### 4.2 工具中介（共享记忆）

适合大型系统，Agent 不直接对话，靠共享存储协作。

```python
# Agent A 写入共享记忆
shared_memory.write("findings", {"market_size": "$5B", "growth": "20%"})

# Agent B 读取
findings = shared_memory.read("findings")
```

坑：共享记忆要有读写边界与版本，否则 Agent 会读到半截状态。

### 4.3 管理器广播

适合统一下发变更（截止时间、优先级）。

```python
manager.broadcast("update_all_agents", {
    "new_deadline": "tomorrow",
    "priority": "critical",
})
```

## 5. 踩坑与救法（Pitfalls Playbook）

| 坑 | 现象 | 解法 |
|----|------|------|
| Agent 冲突 | 两个 Agent 结论打架、互相覆盖 | 角色边界划清；明确决策权；设冲突仲裁 Agent / 权威层级 |
| 慢执行 | 整体比单 Agent 还慢 | 能并行就并行；缓存贵操作；预处理数据；设超时 |
| 质量差 | 结果拼凑、逻辑断点 | 更好的 prompt / 指令；更对口工具；加质检 Agent；结果聚合策略 |
| 工作流复杂 | 链路难维护、易错 | 拆小队；层次结构；清晰任务定义；好的状态管理；文档化 |
| 上下文膨胀 | token 爆炸、成本失控 | 共享记忆只在需要时读；Agent 只带自己需要的 context；结果摘要后再传 |
| 静默失配 | 解析 / 匹配失败不报错，输出全 0 | 大正则拆成多条小正则；断言失败要抛异常而非静默归零 |

## 6. 实现清单（Implementation Checklist）

- [ ] 每个 Agent 的 role / goal / expertise 已定义
- [ ] 每个 Agent 可用工具已列清
- [ ] 工作流模式已定（顺序 / 并行 / 层次）
- [ ] 通信模式已定（直连 / 共享记忆 / 广播）
- [ ] 任务定义与 handoff 点已明确
- [ ] 每个任务的成功标准已设
- [ ] 错误处理与降级策略已加
- [ ] 监控 / 日志已接（审计追溯）
- [ ] 单 Agent 自测通过后再联调
- [ ] 质量与成本已评估（完成率 / 耗时 / token / 错误率）
- [ ] 工作流与决策已文档化

## 7. 起步建议

1. **从小开始**：先 2-3 个 Agent
2. **工作流写清楚**：Agent 怎么交互
3. **充分测试**：单独测 + 联调测
4. **密切监控**：盯性能与结果
5. **迭代**：基于结果精修
6. **再扩**：逐步加 Agent 与复杂度
