---
name: deep-fix
description: Use this skill when facing badcases, repeated patches, prompt bloat, duplicated logic, routing failures, or architecture review. 当遇到 badcase、重复补丁、Prompt 膨胀、规则堆叠、路由失败、架构评审时使用。Trigger on: "how do I fix this case", "the prompt keeps getting longer", "we keep patching the same thing", "this agent keeps choosing the wrong tool", "should this be a rule or a model call", "is this worth abstracting", "our system is full of if/else" — 以及「这个 case 怎么修」「prompt 越来越长」「老是在打补丁」「这应该是规则还是模型判断」「值不值得抽象」「代码/流程越来越乱」。These are signals of a missing abstraction — not just a missing fix.
---

# Deep Fix

机制层修复，*quick fix* 的对立面。不是更快修一个 case，而是用最简洁、最精准、最可复用的机制解决**一类**问题。

**核心前提：** 一个或几个看似孤立的问题，几乎从不真正孤立。它们是信号——指向缺失的抽象、误用的能力、或已堆积的补丁债。

```
case → pattern → mechanism → reusable skill/module → evaluation loop
单点    共性      机制           可复用能力                  评测闭环
```

弱解法继续加补丁。强解法通过引入正确抽象，**减少**系统里散落的补丁。

---

## Step 0 — 先收集证据，再开口

**在提任何建议之前**，先问这 4 个问题。没有答案就问，不要跳过。

```
Q1. 这个问题在同一个地方出现过几次了？
    （1 次 / 2–3 次 / 4 次以上）

Q2. 处理它的逻辑分散在几个地方？
    （一处 / 2–3 处 / 更多）

Q3. 有没有办法客观判断「修好了」？
    （有测试/eval/指标 / 只能主观看 / 完全没有）

Q4. 上次修这里之后，有没有让别的地方变差？
    （没有 / 不确定 / 有）
```

**答案解读：**

| 模式 | 信号 | 行动 |
|---|---|---|
| Q1=1次，Q4=没有 | 孤立 case | 可以 case fix，但先命名风险 |
| Q1≥3次 或 Q2≥3处 | 补丁扩散 | 必须升维，不能再打补丁 |
| Q3=只能主观看 | eval 缺失 | 先建评测，再改算法 |
| Q4=有 | 系统边界问题 | 加载 `references/procedure.md` |

> 有代码库的用户可以运行 `references/deep-fix-scan.py [path]` 补充量化证据。脚本只输出观测事实，不做判断——判断是 Claude 的事。

---

## Step 0.5 — 定位门控

如果问题涉及以下任何一项，**停止设计机制，先问清楚**：

- 产品定位未定（「哪种用法才是正确用法」没有答案）
- 价值标准缺失（「什么叫做好了」没有客观标准）
- 没有 eval 真值（改来改去靠主观印象）

遇到上述情况：问 2–3 个定位问题，**等用户回答后再继续**。在定位未定的前提下输出完整方案，是把架构债务换了个形式继续藏。

---

## Step 1 — 抑制补丁冲动

在提出任何以下动作前——加 if/else、加关键词、加正则、加一句 prompt、加一个分支——先命名风险：

> *「这可能只是 case 层症状，不是真正的问题边界。」*

---

## Step 2 — 归类失败模式

哪层失败了？

| 类型 | 信号 |
|---|---|
| **Semantic 语义** | 同一意图有多种表达，规则无法枚举完 |
| **Context 上下文** | 单独对话正常，多轮/跨会话失败 |
| **Routing 路由** | 工具/模式选错，或靠表层词命中 |
| **System boundary 系统边界** | 相同逻辑在多处出现；prompt 做了代码该做的事 |
| **Evaluation 评测** | 改了感觉好些，但没有客观判据 |

→ 需要精确归类：`references/patterns.md`（完整 A–G + 诊断问题 + 子类型）

### STOP 信号

看到以下任何信号，立即停下，回到 Step 0：

- 已为同一个问题提过 2 条以上规则或修复
- 同一个模块出现在两个不同 case 的失败路径里
- 用户说过「上次也改过这里」
- 提出的解法里包含关键词列表或 if/else 意图分支
- **3 次修复失败 → 强制架构审查**（加载 `references/procedure.md`）

---

## Step 3 — 选抽象层级，输出判决

```
case fix        → 只修这个 case（慎用，需说明为何不升维）
pattern rule    → 狭窄、边界清晰、低风险的重复模式
mechanism       → 可复用流程：router / verifier / normalizer / context-builder
deep module     → 接口简单、内部能力强的代码/逻辑抽象
skill           → 面向 Agent 的可复用任务流程
harness         → 编排、状态、记忆、评测协调层
migration path  → 存量补丁系统的渐进迁移路径
```

推荐路径：`case → pattern → mechanism → skill/module → eval`

---

## 输出格式 / Output Format

**默认：对话模式。** 除非用户明确要完整方案，否则不用 7 个 section。

**对话模式**（默认）：

```
根因：[1–2 句，直接说清楚是什么层的问题]

选项：
  A. [方向] — [代价]
  B. [方向] — [代价]

我倾向 [X]，原因是 [一句话]。但这取决于 [关键问题]。

需要你回答：[1–2 个问题，停，等回答]
```

**文档模式**（用户要完整方案时）：

```
## Direct Judgment    [case/rule/mechanism/module/skill/harness/migration]
## Problem Reframe    这不只是 X，是 Y 层问题
## Shared Root        共性根因
## Existing Capability Check
## Recommended Mechanism   Name / Input / Process / Output / Boundary
## Why Not a Patch
## Eval Plan          Positive / Negative / Boundary / Regression
## Final Verdict
```

---

## 分诊表 / Reference Map

| 症状 | 加载 |
|---|---|
| 多个 case，怀疑共因，需完整流程 | `references/procedure.md` |
| 根因不清，需精确归类 | `references/patterns.md` |
| 启发式 + 反模式 + 例子 | `references/heuristics.md` |
| 值不值得抽象，时机判断 | `references/abstraction-readiness.md` |
| Prompt 越来越长 | `references/prompt-decompose.md` |
| 存量系统已补丁化 | `references/patch-audit.md` |
| 有代码库，需量化证据（可选） | `references/deep-fix-scan.py` |

---

## 何时不用 / When NOT to Use

- 真正的一次性 edge case，无结构泛化信号
- 用户明确要 demo 临时补丁，且承认这是技术债
- 第一次出现，没有重复信号——先观察
- 纯审美/风格，无功能影响

**过早抽象本身也是 Deep Fix 反模式。**

---

## 三个基础思想

**大道至简** — 把复杂度放在正确层级。一个干净机制解决一类问题，外部接口简单，内部能力充足。简洁不是减少代码，是减少*不必要*的代码。

**抽象升维** — 修之前先追问：这些 case 是否共享用户场景、语义模式、流程瓶颈？系统里是否已有可复用能力？正确答案是规则、机制、模块、Skill，还是更深层重构？

**Karpathy 式 AI 工程观** — Prompt、Skill、Memory、Eval 都是程序的一部分。把重复推理外化为稳定资产。重复出现的机制，应该沉淀为可复用认知资产。

完整影响来源：`references/heuristics.md`

---

**最终原则：** 大道至简的最高形态，不是规则更少——而是因为正确抽象已经存在，那些不必要的规则根本不需要再写。
