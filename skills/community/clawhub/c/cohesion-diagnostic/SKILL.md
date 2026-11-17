---
name: cohesion-diagnostic
description: 诊断英文心理学论文结论部分的衔接与连贯问题，输出结构化诊断报告。检测主题句、信息流、指代清晰度、连接词使用。
version: 1.0.0
metadata:
  openclaw:
    user-invocable: true
    homepage: "https://clawhub.ai/你的用户名/cohesion-diagnostic"
---

# 衔接与连贯诊断 Skill

## 触发条件

当用户上传英文心理学论文的 **Conclusion/Discussion** 部分，并提出以下请求时触发：

- "帮我诊断这段结论的衔接问题"
- "检查这段讨论的连贯性"
- "分析信息流和指代清晰度"
- "看看连接词用得怎么样"
- "帮我诊断衔接与连贯"

## 诊断步骤

### 第一步：接收输入

接收用户上传的 Conclusion/Discussion 段落文本。

### 第二步：分句分段

将文本按段落和句子进行拆分，为后续诊断做准备。

### 第三步：按四项维度逐一诊断

#### 维度1：段落主题句（Topic Sentences）

检查每段首句是否满足以下条件：

**✅ 正例标准**（基于10篇心理学顶刊论文提取）：
- 首句包含主题标记词：`implication`、`finding`、`result`、`limitation`、`direction`、`issue`、`effect`、`contribution`
- 首句长度 ≥ 10 个单词
- 首句包含回指标记：`These findings`、`This result`、`Our data` 等

**✅ 优秀句式模板**（引用自范文）：
- "The first implication of these results concerns..." — Stephens et al. (2007)
- "These findings have important implications for understanding..." — Kraus et al. (2012)
- "Several limitations of this study should be acknowledged..." — Piff et al. (2010)
- "Future research might fruitfully explore..." — Bargh et al. (1996)

**❌ 问题句式**：
- 首句仅为简单结果复述（如 "We found X."）
- 首句长度 < 10 词且无主题标记词

**判定阈值**：
- ≥75% 段落有清晰主题句 → ✅ 通过
- 50%-74% → ⚠️ 中风险
- <50% → 🔴 高风险


#### 维度2：信息流（Information Flow）

检查句子间是否遵循 "已知→新信息" 原则。

**✅ 正例模式**（基于10篇范文统计，占60%以上）：
- "These findings [已知] demonstrate that [新]..." — Willis & Todorov (2006)
- "This effect [已知] was particularly pronounced among [新]" — Piff et al. (2010)
- "Such patterns [已知] suggest that [新]" — Stephens et al. (2007)
- "Specifically, [细化前句提到的发现]" — Goel et al. (2010)

**回指标记词表**：
- `These findings`
- `This result`
- `Such patterns`
- `Our data`
- `The present study`
- `This effect`
- `This account`

**❌ 问题模式**：
- 连续 3 句以上句首均为全新信息（无回指标记）
- 句首频繁使用虚主语 `It is suggested that...`

**判定阈值**：
- 回指结构占比 ≥ 40% → ✅ 通过
- 20%-39% → ⚠️ 中风险
- <20% → 🔴 高风险


#### 维度3：指代清晰度（Referential Clarity）

检查指示词（`this`、`these`、`it`、`they`）的先行词是否明确。

**✅ 推荐指代方式**（引用自范文）：
- "These findings suggest that..." — Willis & Todorov (2006)
- "This result is consistent with..." — Baron & Kenny (1986)
- "Our data indicate that..." — Bargh et al. (1996)
- "The present study provides..." — Epley et al. (2004)
- "Such patterns suggest that..." — Stephens et al. (2007)

**❌ 禁止/避免的指代方式**：
- 孤立 `This suggests that...`（前句有多个潜在先行词）
- 虚主语 `It is suggested that...`（归属不明，AI味标志）
- 虚主语 `It can be observed that...`
- 被动语态 `It was found that...`（弱化主体）

**判定阈值**：
- 无孤立 This、无虚主语 → ✅ 通过
- 出现 1 次 → ⚠️ 中风险
- 出现 ≥ 2 次 → 🔴 高风险


#### 维度4：连接词与Hedging使用

检查连接词是否学术化、Hedging是否充分。

**✅ 学术连接词**（推荐）：
- `however`（表转折）
- `nevertheless`（表让步-转折）
- `therefore`（表因果）
- `moreover` / `furthermore`（表追加）
- `consequently` / `accordingly`（表结果/推论）

**✅ Hedging（模糊限制语）**（推荐）：
- `may`、`could`、`might`（表达可能性）
- `suggests`、`indicates`（表达指向性证据）
- `likely`、`possibly`（表达概率）
- `appears`（表达观察性判断）

**✅ Hedging使用频率标准**（基于范文统计）：
- 建议每千词至少 8 个 Hedges
- Bargh et al. (1996) 范文：每千词 12 个 Hedges

**❌ 问题模式**：
- 简单连接词 `and`/`but`/`so` 每千词 > 3 次
- 全文 Hedges < 5 个（过度声称风险）
- Boosters（`clearly`、`strongly`、`extremely`）与 Hedges 比例 > 1:1

**判定阈值**：
- 简单连接词 ≤ 3/千词 且 Hedges ≥ 8 → ✅ 通过
- 简单连接词 > 3/千词 或 Hedges 5-8 个 → ⚠️ 中风险
- Hedges < 5 个 → 🔴 高风险


### 第四步：输出诊断报告

按以下格式输出报告：
╔══════════════════════════════════════════════════════════════╗
║ 【衔接与连贯诊断报告】 ║
╚══════════════════════════════════════════════════════════════╝

【整体评分】：X.X/5.0

【一、段落主题句诊断】（✅通过 / ⚠️中风险 / 🔴高风险）
─────────────────────────────────────────────────
具体检测结果...
示例对照：
✅ 正例参考："The first implication of these results concerns..." — Stephens et al. (2007)
❌ 问题对照："We found X."（主题句不清晰）

【二、信息流诊断】（✅通过 / ⚠️中风险 / 🔴高风险）
─────────────────────────────────────────────────
具体检测结果...
示例对照：
✅ 正例参考："These findings demonstrate that..." — Willis & Todorov (2006)
❌ 问题对照：连续3句句首均为新信息

【三、指代清晰度诊断】（✅通过 / ⚠️中风险 / 🔴高风险）
─────────────────────────────────────────────────
具体检测结果...
示例对照：
✅ 正例参考："These findings suggest that..." — Willis & Todorov (2006)
❌ 问题对照："This suggests that..."（指代不明）

【四、连接词与Hedging诊断】（✅通过 / ⚠️中风险 / 🔴高风险）
─────────────────────────────────────────────────
具体检测结果...
示例对照：
✅ 正例参考：Bargh et al. (1996) 每千词12个Hedges
❌ 问题对照：全文Hedges < 5个

【五、Example对照参考】
─────────────────────────────────────────────────
本诊断基于以下10篇心理学顶刊论文的写作特征提取：

Baron & Kenny (1986) JPSP

Willis & Todorov (2006) Psychological Science

Bargh, Chen & Burrows (1996) JPSP

Piff et al. (2010) JPSP

Stephens, Markus & Townsend (2007) JPSP

Kraus et al. (2012) Psychological Review

Epley et al. (2004) JPSP

Goel, Mason & Watts (2010) JPSP

Anderson, Kraus & Galinsky (2012) Psychological Science

Baron-Cohen, Leslie & Frith (1985) Cognition

═══════════════════════════════════════════════════════════════

### 第五步：给出修改建议

针对每个检测到的问题，提供具体的修改建议，并引用范文中的正例作为参照目标。