---
name: art-of-war
description: Apply Sun Tzu's Art of War principles to AI agent organization and task orchestration. Use when planning multi-agent workflows, evaluating whether to deploy agents, assessing task complexity, or optimizing agent collaboration strategies. Maps all 13 chapters to practical agent patterns.
---

# Art of War

Apply **Sun Tzu's 13 chapters** to AI agent organization and orchestration. This skill provides a framework for strategic decision-making about when, how, and which agents to deploy for maximum effectiveness with minimum waste.

## Core Principles

### 知彼知己 (Know Enemy, Know Yourself)
- **知彼**: Understand the task deeply — requirements, constraints, success criteria
- **知己**: Know your agents' capabilities, limitations, and costs
- **百战不殆**: With both, every agent deployment is calculated, not hopeful

### 上兵伐谋 (Best Strategy Attacks Plans)
- Planning > Execution. Invest in task analysis before spawning agents
- A well-planned single agent beats three confused agents
- "Win before fighting" — structure the problem so the solution is obvious

### 奇正相生 (Orthodox + Unorthodox)
- **正**: Standard workflows, proven patterns, reliable agents
- **奇**: Creative approaches, novel combinations, experimental agents
- Use 正 for reliability, 奇 for breakthrough. Never rely on 奇 alone.

### 速战速决 (Speed is Essential)
- Prolonged agent runs waste tokens and drift from intent
- Set clear termination conditions upfront
- If an agent isn't making progress in 2-3 iterations, reassess

### 先胜后战 (Victory Before Battle)
- Ensure conditions favor success before deploying agents
- If you can't articulate what "winning" looks like, don't start
- Retreat is better than wasting resources on unwinnable tasks

---

## 开工前自检（必用）

**每次部署 agent 前，填这个表。填不完别发。**

```
┌────────────────────────────────────────────────────┐
│ 五事自检 FIVE CONSTANTS                            │
├────────────────────────────────────────────────────┤
│ 道：这任务值得做吗？对齐目标吗？                    │
│   □ 是  □ 否  □ 不确定                             │
│                                                    │
│ 天：现在是时候吗？依赖准备好了吗？                  │
│   □ 是  □ 否  □ 不确定                             │
│                                                    │
│ 地：数据/上下文/工具齐了吗？                        │
│   □ 是  □ 否  □ 不确定                             │
│                                                    │
│ 将：有合适的 agent 吗？能力匹配吗？                  │
│   □ 是  □ 否  □ 不确定                             │
│                                                    │
│ 法：流程清楚吗？什么叫"做完"？                      │
│   □ 是  □ 否  □ 不确定                             │
│                                                    │
│ 得分：___/5                                        │
│ ≥4: 可以发  |  3: 先补弱点  |  <3: 别发            │
└────────────────────────────────────────────────────┘
```

**三反验证（输出事实前必做）**

```
要验证的事实：________________

□ 来源 1（Agent 内部知识）：________________
□ 来源 2（外部搜索/API）：________________
□ 来源 3（用户上下文/文档）：________________

一致 → 信  |  不一致 → 查
```

**信号监控（迭代中盯这些）**

```
⚠ 问同样的问题第二次 → 缺上下文，补
⚠ 输出越来越长 → 在填充，停
⚠ 过度自信 → 要来源，验
⚠ 回避问题 → 不会，直说
⚠ 循环论证 → 卡住，重定向

看到任一信号 → 立刻干预，别等第 5 次
```

**迭代限制（写死）**

```
最大迭代次数：3 次（默认）
Token 预算：_______
超时：_______ 分钟

到限不出结果 → 强制结论，停
```

---

## The Thirteen Chapters → Agent Patterns

### 1. 始计篇 (Laying Plans) — Task Assessment

**Before deploying any agent, run the Five Constants + Seven Metrics:**

**五事 (Five Constants):**
1. **道 (Wisdom)**: Does this task align with overall goals?
2. **天 (Timing)**: Is now the right time? Dependencies ready?
3. **地 (Environment)**: Do we have the right context/data/tools?
4. **将 (Capability)**: Which agent(s) have the right skills?
5. **法 (Process)**: What's the workflow? Success criteria?

**七计 (Seven Metrics):**
- Which side has better task clarity?
- Which side has more capable agents?
- Which side has better context/data?
- Which side has clearer success criteria?
- Which side has better tool access?
- Which side has more disciplined execution?
- Which side will waste fewer resources?

**Decision**: If you can't answer these, don't deploy. Plan first.

### 2. 作战篇 (Waging War) — Cost Awareness

**Agent runs cost tokens. Treat them like war costs:**

- **速战速决**: Set iteration limits. Force conclusions.
- **因粮于敌**: Use existing outputs/data; don't regenerate what exists
- **胜久则钝**: Long-running agents lose focus and waste tokens
- **预算先行**: Estimate token cost before starting; track as you go

**Rule**: If a task can be done in 1 agent iteration, don't use 3.

### 3. 谋攻篇 (Attack by Stratagem) — Planning Over Force

**Hierarchy of agent deployment:**

1. **上策**: Restructure the problem so it solves itself (no agent needed)
2. **中策**: Single focused agent with clear instructions
3. **下策**: Multiple agents in complex orchestration

**Avoid siege warfare**: Don't throw more agents at a poorly-defined problem.

**全胜思维**: The best outcome is winning without fighting — automate or eliminate the task entirely.

### 4. 军形篇 (Tactical Dispositions) — Defense First

**Before offense, ensure defense:**

- What can go wrong? (Hallucination, outdated info, tool failures)
- What's the rollback plan if the agent makes things worse?
- What guardrails prevent catastrophic outputs?

**先为不可胜**: Make yourself undefeatable first — have validation, version control, and undo capability.

**以待敌之可胜**: Then wait for the opportunity — deploy when conditions are favorable.

### 5. 兵势篇 (Energy/Impetus) — Momentum & Combination

**Create unstoppable momentum:**

- **势 (Shi)**: Build configurations where each agent output naturally triggers the next
- **奇正**: Combine standard agents (正) with creative approaches (奇)
- **节 (Timing)**: Release agents in waves, not all at once

**Example pattern**: Research agent → Synthesis agent → Critique agent → Final polish
Each builds on the previous, creating momentum.

### 6. 虚实篇 (Weak Points & Strong) — Strategic Targeting

**Avoid strength, attack weakness:**

- Identify the **critical bottleneck** in the task
- Don't waste agent capacity on parts you can handle yourself
- Deploy agents where they have **comparative advantage**

**避实击虚**: If an agent struggles with nuance, handle the nuance yourself; let it handle the bulk work.

**致人而不致于人**: Control where the agent focuses; don't let it drift.

### 7. 军争篇 (Maneuvering) — Indirect Approaches

**The longest path may be fastest:**

- Sometimes 2-3 focused agents beat 1 generalist agent
- Sometimes doing background research first saves 10 iterations later
- "Appear weak when strong" — let the agent explore naive approaches first, then guide

**以迂为直**: A seeming detour (extra planning, extra validation) often reaches the goal faster.

### 8. 九变篇 (Nine Variations) — Adaptability

**Agents must adapt to changing conditions:**

- Have **contingency plans**: If agent A fails, what's plan B?
- **将在外，君命有所不受**: Give agents autonomy within boundaries
- Recognize when to **change strategy** mid-execution

**Five dangerous agent faults:**
1. Reckless iteration (burns tokens)
2. Excessive caution (never completes)
3. Quick temper (argues with user)
4. Over-optimization (loses the goal)
5. Blind compliance (no pushback on bad instructions)

Watch for these; intervene early.

### 9. 行军篇 (Marching) — Environmental Awareness

**Read the signals:**

- **相敌 (Observing the enemy)**: Watch agent outputs for drift, hallucination, confusion
- **信号 (Signals)**: Repeated questions = unclear instructions; circular reasoning = stuck
- **地形 (Terrain)**: Some tasks are "difficult ground" — high uncertainty, need more oversight

**When to intervene:**
- Agent asks the same question twice
- Output quality degrades over iterations
- Agent is confident but wrong

### 10. 地形篇 (Terrain) — Task Classification

**Six terrain types → Six task types:**

| 地形 | 任务类型 | Agent 策略 |
|------|---------|-----------|
| 通形 (Accessible) | 清晰定义的任务 | 直接部署，标准流程 |
| 挂形 (Entangling) | 容易陷入细节的任务 | 设时间限制，强制输出 |
| 支形 (Stalemate) | 信息不足的任务 | 先收集信息，再决策 |
| 隘形 (Narrow) | 高约束任务 | 精确指令，严格验证 |
| 险形 (Dangerous) | 高风险任务 | 多重验证，保守策略 |
| 远形 (Distant) | 长链条任务 | 分阶段，设检查点 |

### 11. 九地篇 (Nine Grounds) — Commitment Levels

**Match resource commitment to task importance:**

| 地 | 任务重要性 | Agent 投入 |
|---|-----------|-----------|
| 散地 (Home ground) | 日常任务 | 轻量 agent，快速迭代 |
| 轻地 (Light ground) | 低价值任务 | 最小可用方案 |
| 争地 (Contentious) | 竞争/时间敏感 | 优先资源，快速部署 |
| 交地 (Open ground) | 多方协作 | 明确接口，文档先行 |
| 衢地 (Intersecting) | 多目标 | 平衡资源，避免偏废 |
| 重地 (Serious) | 高价值任务 | 多 agent 协作，充分验证 |
| 圮地 (Difficult) | 信息不足 | 先探索，后投入 |
| 围地 (Desperate) | 受约束 | 创造性方案，突破限制 |
| 死地 (Death) | 背水一战 | 全力以赴，不留退路 |

**Most tasks are 散地 or 轻地 — don't over-invest.**

### 12. 火攻篇 (Fire Attack) — Tool Usage

**Fire = powerful tools (code execution, API calls, external data):**

- **五种火 (Five fires)**:
  1. 人火 (Human fire): User-provided data/context
  2. 积火 (Accumulated fire): Cached/prepared resources
  3. 辎火 (Supply fire): Tool/API access
  4. 库火 (Arsenal fire): Code execution
  5. 队火 (Unit fire): Multi-agent collaboration

**用火的时机 (When to use fire):**
- 行必有备 (Always prepared): Have fallback if tool fails
- 发火有时 (Right timing): Don't use tools prematurely
- 发火在早 (Early): Use tools early to validate direction

**Warning**: Fire can burn you. Validate tool outputs; don't trust blindly.

### 13. 用间篇 (Spies) — Information Gathering

**Five types of intelligence sources:**

| 间 | Agent 应用 |
|---|-----------|
| 因间 (Local spies) | 利用现有文档/代码库 |
| 内间 (Inside spies) | 访问内部系统/数据库 |
| 反间 (Double agents) | 交叉验证多个信息源 |
| 死间 (Doomed spies) | 一次性查询（搜索、API） |
| 生间 (Living spies) | 持续监控（RSS、警报） |

**关键原则:**
- **三反**: Cross-verify with 3+ independent sources
- **不可偏信**: Never trust a single source
- **先知**: Gather intelligence before making decisions

---

## Quick Decision Tree

```
Task arrives
    ↓
Can I do this myself in <5 min?
    ├─ Yes → Do it (don't deploy agent)
    └─ No → Continue
    ↓
Is the task clearly defined?
    ├─ No → Plan first (始计篇)
    └─ Yes → Continue
    ↓
What's the token budget?
    ├─ Low (<10k) → Single focused agent (谋攻篇)
    └─ High → Multi-agent OK (兵势篇)
    ↓
What's the risk if wrong?
    ├─ High → Defense first (军形篇), multiple validation
    └─ Low → Speed优先 (作战篇)
    ↓
Deploy with clear success criteria
    ↓
Monitor for drift (行军篇)
    ↓
Validate output (用间篇 - cross-check)
```

---

## Usage Examples

### Example 1: Should I use an agent for this?

**User**: "I need to research competitors for our new product launch"

**Apply 始计篇**:
- 道: Aligns with business goals ✓
- 天: Launch is in 3 weeks, timing is good ✓
- 地: Need market data, competitor websites, reviews ✓
- 将: Research agent + synthesis agent ✓
- 法: Research → Synthesize → Present findings ✓

**Decision**: Deploy, but start with 因间 (existing reports) before 死间 (new searches).

### Example 2: Agent is stuck in loops

**User**: "The agent keeps asking me the same questions"

**Apply 行军篇**: This is a signal (信号). The agent is on 挂形 (entangling ground).

**Action**: 
1. Intervene early
2. Provide missing context
3. Set iteration limit: "Answer in 2 iterations max"
4. If still stuck, switch strategy (九变篇)

### Example 3: Multi-agent orchestration

**User**: "I need to build a complete market analysis report"

**Apply 兵势篇** (create momentum):
1. Research agent (收集情报)
2. Analysis agent (分析数据)
3. Critique agent (找出漏洞)
4. Writing agent (生成报告)
5. Validation agent (交叉验证)

Each output feeds the next, creating 势 (momentum).

---

## Remember

> 兵者，国之大事，死生之地，存亡之道，不可不察也
> 
> "War is a matter of vital importance to the State; the province of life or death; the road to survival or ruin. It is mandatory that it be thoroughly studied."

**Agent deployment is the same.** Treat it seriously. Plan thoroughly. Execute decisively. Review honestly.
