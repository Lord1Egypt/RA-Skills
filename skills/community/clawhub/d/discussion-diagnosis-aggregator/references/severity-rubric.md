# Aggregator Severity Rubric — 严重度判定标准

## 用途
本文件是 `discussion-diagnosis-aggregator` 评估 issue 严重度的官方标准。

---

## 三级严重度定义

### Critical（必须修复）

**定义**: 削弱 take-home message; 做出 data 不支持的 claim; 缺失必要的 move。

#### 典型 Critical issues

| 类别 | 例子 | 触发维度 |
|---|---|---|
| **缺失必要 move** | 完全无 contribution statement | Structure, Conventions |
| **缺失 limitations 段** | Discussion 无任何 limitations | Structure, Conventions |
| **Over-claim** | "We prove that X causes Y"（用 prove）| Vocabulary, Logic |
| **Causal overreach** | Correlational study 推因果 | Logic |
| **Take-home 丢失** | 全 Discussion 无清晰核心 claim | Cohesion |
| **Tense 完全错位** | Past / Present 全混乱 | Grammar |
| **Happy words 极端堆叠** | "groundbreaking revolutionary unprecedented" | Vocabulary, Conventions |

#### 判定规则
- 出现 1 次 = Critical
- 如果 issue 出现在 load-bearing claim（take-home 相关）→ Critical
- 如果 issue 出现在非关键 claim → Major

---

### Major（应当修复）

**定义**: 显著削弱某个 move; 在 load-bearing claim 中误用 modal / hedge; 破坏 citation 链。

#### 典型 Major issues

| 类别 | 例子 | 触发维度 |
|---|---|---|
| **Hedge 与 claim 不匹配** | 强 claim 用弱 hedge | Vocabulary |
| **Modal 形式错误** | "should looks" | Grammar |
| **Citation 断裂** | 引文无 relationship word | Conventions |
| **Tense 部分错位** | 个别段时态混乱 | Grammar |
| **Topic sentence 缺失** | 多段直接进入 details | Cohesion |
| **Future work vague** | "more research is needed" | Vocabulary, Conventions |
| **Single causal explanation** | 无 alternative explanation | Logic |
| **Limitation 过强** | "Our study cannot prove anything" | Logic, Vocabulary |

#### 判定规则
- 出现 1-2 次 = Major
- 如果 issue 影响 reader 对核心 claim 的理解 = Major

---

### Minor（建议修复）

**定义**: 风格问题; 小型 register 问题; 非 load-bearing 的用词。

#### 典型 Minor issues

| 类别 | 例子 | 触发维度 |
|---|---|---|
| **Connective 单一** | 全用 "Furthermore" | Cohesion |
| **Passive 略多** | 多处被动但 agent 清晰 | Grammar |
| **Happy words 略多** | 3-4 个 happy words（不是堆叠）| Vocabulary, Conventions |
| **Vague abstract recommendation** | "Researchers should be careful" | Conventions |
| **Hedged comparative 过少** | "more likely" 等少用 | Vocabulary |

#### 判定规则
- 出现 1-3 次 = Minor
- 不影响核心 claim 理解 = Minor

---

## 严重度判定决策树

```
问题
├── 削弱 take-home? ──────────── YES → Critical
├── 缺失必要 move? ───────────── YES → Critical
├── 缺失重要 move? ───────────── YES → Major
├── 在 load-bearing claim? ───── YES → Critical; NO → 继续
├── 影响 reader 理解? ────────── YES → Major; NO → 继续
├── 多次出现? ────────────────── 3+ 次 → Major
└── 风格问题? ────────────────── YES → Minor
```

---

## 严重度 × 维度的标准映射

| 维度 | Critical | Major | Minor |
|---|---|---|---|
| Structure | F 或 D 缺失 | 顺序乱 | 单 move 弱 |
| Cohesion | 无 take-home | 段间断裂 | connective 单一 |
| Grammar | 多处 agreement 错误 | modal 形式错 | passive 略多 |
| Vocabulary | 用 "prove" | hedge 与 claim 不匹配 | happy words 略多 |
| Logic | causal overreach | 无 alternative | data-spec 混乱 |
| Conventions | 无 limitations | future work vague | happy words 略多 |

---

## 跨维度 issue 的严重度

当一个 issue 被多维度同时标记时（参见 `cross-dimension-map.md`），使用**最高严重度**作为最终严重度。

例子：
- "We prove that X causes Y" 被 Vocabulary（over-claim）和 Logic（causal overreach）同时标记 → **Critical**（取最高）

---

## 位置权重

如果 issue 出现在 Discussion 的**关键位置**，严重度上调一级：

| 位置 | 加权 |
|---|---|
| 第一段（opening）| +1 级 |
| 末段（closing）| +1 级 |
| Take-home 段落 | +1 级 |
| 中间段 | 无加权 |

例子：
- 段 1（opening）的"In this study, we..." 反模式 → Minor + 1 = **Major**

---

## Top-3 优先级计算

公式：**Priority = Severity × Frequency × Position Weight**

| Severity | Weight |
|---|---|
| Critical | 3 |
| Major | 2 |
| Minor | 1 |

| Frequency | Weight |
|---|---|
| 3+ 次 | 3 |
| 2 次 | 2 |
| 1 次 | 1 |

| Position | Weight |
|---|---|
| Opening / Closing / Take-home | 3 |
| 中间段 | 1 |

---

## 相关文件

- `cross-dimension-map.md` — 跨维度 issue 的合并规则
- `output-template.md` — 报告模板
- `examples/` — 正反例对照