---
name: detect-ai-flavor
description: Detect AI flavor in long-form articles (Chinese & English) to judge whether text reads like AI-generated or human-written. Auto-detects language and applies language-specific indicators. Triggers: 有没有AI味, evaluate AI writing, detect AI-generated content.
agent_created: true
---

# Detect AI Flavor — AI味检测

判断中文或英文长文是AI写的还是人写的。自动识别语言，应用中文/英文各自的检测指标。6维度评估，输出评分表 + 原文证据 + 改进建议。

---

# 中文版

## 目的

评估文章中的"AI味"——能区分AI生成文本和人类写作的可检测模式。输出结构化评估，包含各维度分数、原文证据和可操作的改进建议。

## 触发时机

当用户问"这篇文章有没有AI味"、想判断文字是否像AI写的、需要区分人类/AI/混合写作、或需要降低AI味的写作建议时触发。

## 语言识别

评估前必须先检测文章语言。中文和英文的AI味特征不同，用错指标会导致误判。

- 中文内容占比 >70% → 使用**中文指标**
- 英文内容占比 >70% → 使用**英文指标**
- 中英混合 → 分别评估各语段，在报告中注明

## 评估框架

对文本应用六个维度，每个维度用四级制评分：

| 等级 | 含义 |
|------|------|
| ✅ 偏好 | 人类感强，无明显AI痕迹 |
| ⚠️ 中度 | 有AI模式但不占主导 |
| ❌ 重 | 明显的AI模式遍布全文 |
| N/A | 不适用 |

## 维度一：结构模式

AI生成的中文文章章节长度相近、编号整齐。人类写作会打破结构。

**AI味指标：**
- 多个编号章节（一/二/三…）长度相近
- 平行小标题格式整齐（小菜园 → 老乡鸡 → 米村拌饭）
- 列举式推进："第一…第二…第三…"
- 结构"设计感"过强，不像"自然生长"

**例外：** 财经深度报道（36氪、晚点LatePost）常用章节格式，符合体裁规范时降低扣分。

## 维度二：句式节奏

AI文本句子长度高度统一。人类写作有长短变化、单句段、突兀转折。

**AI味指标：**
- 句子长度集中在25-40字，方差低
- 每段都是"观点→论据→小结"模式
- 没有单独成段的短句制造节奏
- 过渡词机械："此外"、"另一方面"、"值得注意的是"

**人类特征：**
- 长短句明显交错
- 刻意断句："但商家呢？"、"先看账单。"
- 分段靠直觉而非模板

## 维度三：用词风格

AI过度使用行业术语，脱离具体语境。

**AI味指标：**
- 术语堆砌："赋能"、"生态"、"底层逻辑"、"闭环"、"抓手"
- 术语清单式罗列："运营杠杆、单位经济学、防御性壁垒"
- 抽象名词主导，缺少具体事物和感官细节
- 每个判断都加限定词："在一定程度上"、"总体而言"

**人类特征：**
- 术语少而精准，总绑定具体语境
- 有具体细节："一杯奶茶1.9元"、"把自己喝进了急诊室"
- 口语化表达："差不多"、"大概就是"
- 敢不精确

## 维度四：逻辑推进

AI默认用穷举式、面面俱到的分析。人类敢于站队、留白。

**AI味指标：**
- 完美二元分析："若X则A；反之则B"
- 每个论点紧跟反方论点
- 所有问题都有答案，没有悬而未决
- 分析像百科全书条目

**人类特征：**
- 有明确立场，哪怕可争议
- 承认不确定："我也说不准"、"这个得看具体情况"
- 留有余地，不把所有线头都收了
- 分析有观点，不是全景扫描

## 维度五：表达温度

这是最强的信号。AI文本零人格——没有幽默、没有脾气、没有个人经历。

**AI味指标：**
- 全文零情绪波动
- 没有幽默、讽刺或自嘲
- 没有具名人物和直接引语
- 语气始终是"分析师"，没有人格切换
- 每段像是不同人写的——没有作者同一性

**人类特征：**
- 具名来源 + 真实引语
- 黑色幽默或荒诞细节："有人把自己喝进了急诊室"
- 一致的人格渗透全文
- 口语化质问："他敢吗？他不敢。"

## 维度六：信息密度与呼吸感

AI每句话都在输出内容。人类写作有"废话"——不是无用的，是呼吸用的。

**AI味指标：**
- 每句都在推进论证，零冗余
- 没有"这个问题我想了很久"、"说实话"这类低密度句
- 信息密度全程均匀高能
- 读起来像压缩文件——高效但累

**人类特征：**
- 有低密度呼吸段，给节奏服务
- 元评论："有意思的是…"、"这里有一个容易被忽略的点"
- 刻意重复达到修辞效果
- 文章会呼吸

## 中文AI味关键词速查

```
术语堆砌: 赋能, 生态, 底层逻辑, 闭环, 抓手, 深度, 全面, 布局
结构词: 首先/其次/最后, 一方面/另一方面, 值得注意的是, 总体而言
句式: 在…的背景下, 随着…的发展, 从…到…的转变
修饰: 在很大程度上, 一定程度上, 相对而言
```

## 输出格式

### 1. 语言识别
说明检测到的语言和使用的指标集。

### 2. 综合判定
一句话结论："AI味偏高 / 中度 / 偏低"。

### 3. 维度评分表

```
| 维度 | 评分 | 关键证据 |
|------|------|---------|
| 结构模式 | ✅/⚠️/❌ | 一行观察 |
| 句式节奏 | ✅/⚠️/❌ | 一行观察 |
| 用词风格 | ✅/⚠️/❌ | 一行观察 |
| 逻辑推进 | ✅/⚠️/❌ | 一行观察 |
| 表达温度 | ✅/⚠️/❌ | 一行观察 |
| 信息密度 | ✅/⚠️/❌ | 一行观察 |
```

### 4. 详细分析
对⚠️或❌的维度，提供1-3处原文引用，解释为什么是AI味。

### 5. 来源判定
- **纯AI生成**：所有维度强AI模式
- **AI生成+人工修改**：AI骨架可见，但人工加入了细节/引语
- **人写+AI润色**：人类声音占主导，AI模式仅限结构/格式
- **纯人写**：无明显AI模式

### 6. 改进建议
如有AI味，提供2-4条具体改进建议，按影响力排序。

## 对比模式

多篇对比时追加横向表格：

```
| | 文章A | 文章B | 文章C |
|---|---|---|---|
| AI味 | ⚠️ 中低 | ❌ 偏高 | ✅ 低 |
| 人物细节 | 无 | 无 | ✅ |
| 口语化 | 有 | 无 | ✅ |
| 更像 | 人写+AI改 | AI写+人改 | 人写为主 |
```

## 参考资料

- `references/evaluation-examples.md` — 中文评估校准案例
- `references/indicator-checklist.md` — 32项快速检测清单（中文）

---

# English Version

## Purpose

Evaluate articles for "AI味" (AI flavor) — detectable patterns that distinguish AI-generated text from human writing. Output a structured assessment with dimension-level scores, concrete evidence, and actionable improvement suggestions.

## When to Use

Trigger when the user asks "does this have AI味", wants to know if text reads like AI-generated content, needs to distinguish between human/AI/mixed writing, or wants advice to reduce AI-like patterns.

## Language Detection

Before evaluation, detect the article's primary language. Chinese and English have different AI-flavor signatures — applying the wrong indicator set produces false results.

- If >70% of content is Chinese characters → apply **Chinese indicators** (see Chinese section above)
- If >70% of content is Latin alphabet → apply **English indicators** (this section)
- If mixed (bilingual) → evaluate each language segment separately, note the mix in the assessment

## Evaluation Framework

Apply six dimensions using a 4-level scale:

| Level | Meaning |
|-------|---------|
| ✅ Good | Feels human; little to no AI trace |
| ⚠️ Moderate | Some AI patterns present but not dominant |
| ❌ Heavy | Strong AI patterns throughout |
| N/A | Not applicable |

## Dimension 1: Structural Patterns

English AI text tends toward rigid essay structure with predictable scaffolding.

**AI Indicators:**
- Every paragraph opens with a signpost: "First,...", "Additionally,...", "Furthermore,...", "Finally,..."
- Predictable section flow: Introduction → Background → Analysis → Implications → Conclusion
- Subtitles feel template-generated: "The Rise of X", "Why Y Matters", "What This Means for Z"
- Uniform paragraph length (4–6 sentences each)
- Multiple numbered sections of near-equal length

**Human Indicators:**
- Asymmetric structure — some sections are long, others are a single sentence
- Headers that surprise rather than summarize
- Organic flow that doesn't telegraph itself

## Dimension 2: Sentence Rhythm

English AI text defaults to rhythmic monotony — every sentence is a complete, grammatically perfect thought.

**AI Indicators:**
- Sentence length clusters around 18–28 words with low variance
- Repeated sentence openers: "This...", "These...", "Such...", "It is..."
- "Not only... but also..." constructions appear multiple times
- Every paragraph ends with a neat transition to the next
- Overuse of semicolons; formal compound sentences dominate

**Human Indicators:**
- Sentence fragments used for rhythm: "Not even close." "Wrong question."
- Sentence openers vary naturally
- Paragraphs sometimes end abruptly — no forced transition
- Informal constructions mixed with formal ones

## Dimension 3: Word Choice & Terminology

English AI text uses a recognizable set of "AI-favorite" words and phrases.

**AI Indicators:**

Overused transition phrases:
- "delve into", "explore how", "unpack", "navigate the complexities of"
- "it is worth noting that", "it is important to consider"
- "in today's rapidly evolving landscape", "in an era of..."

Overused adjectives:
- "crucial", "critical", "essential", "fundamental", "pivotal", "vibrant", "robust", "seamless"

Overused hedging:
- "may potentially", "could arguably", "tends to suggest"
- "a nuanced understanding", "a multifaceted approach"

Overused structural phrases:
- "not only... but also..."
- "on one hand... on the other hand..."
- "a testament to", "underscores the importance of"

**Human Indicators:**
- Plain language dominates; jargon used only when it carries specific meaning
- Concrete examples over abstract frameworks
- Idiomatic, colloquial, or culturally specific expressions
- Occasional imprecision or informality

## Dimension 4: Logical Flow

AI defaults to exhaustive, balanced analysis. Human writers take positions and leave gaps.

**AI Indicators:**
- Perfect binary analysis: "While X offers Y, Z presents challenges"
- Every claim immediately followed by its counter-argument
- "Some argue X. However, others contend Y. Ultimately, the truth lies somewhere in between."
- No unresolved tension; every question gets an answer
- Analysis reads like an encyclopedia entry

**Human Indicators:**
- Takes a clear position, even if debatable
- Admits uncertainty: "I'm not sure about this"
- Leaves some threads unresolved
- Analysis shows a point of view, not a survey

## Dimension 5: Human Warmth

This is the strongest signal. AI text has zero personality.

**AI Indicators:**
- Zero emotional variation throughout the text
- No humor, irony, or self-deprecation
- No specific, named individuals with direct quotes
- Voice is consistently "analyst" with no personal register
- Every paragraph could have been written by a different person — no author identity

**Human Indicators:**
- Specific named sources with real quotes
- Dry wit, understatement, or self-aware asides
- Cultural references that feel lived-in, not cited
- A consistent personality bleeds through the analysis

## Dimension 6: Information Density

AI packs every sentence with substantive content. Human writing has breathing room.

**AI Indicators:**
- Every sentence advances the argument; zero redundancy
- No "useless" sentences like "Honestly, I've been thinking about this"
- Information density is uniformly high throughout
- Reads like a compressed file — efficient but exhausting

**Human Indicators:**
- Occasional low-density segments that serve rhythm
- Meta-commentary: "Here's the interesting part"
- Deliberate repetition for rhetorical effect
- The text breathes

## English AI-Flavor Keyword Quick Reference

```
Transitions:  delve into, explore how, navigate, unpack, furthermore, moreover
Hedges:       may potentially, could arguably, tends to suggest, nuanced
Adjectives:   crucial, critical, essential, pivotal, vibrant, robust, seamless
Phrases:      not only...but also..., a testament to, it is worth noting that
Frames:       in today's landscape, in an era of, as we move forward
Closers:      ultimately, in conclusion, the key takeaway, as we have seen
```

## Output Format

### 1. Language Detection
State detected language and which indicator set was applied.

### 2. Overall Assessment
Single-sentence verdict: "High / Moderate / Low AI flavor."

### 3. Dimension Score Table

```
| Dimension | Score | Key Evidence |
|-----------|-------|--------------|
| Structure | ✅/⚠️/❌ | One-line observation |
| Rhythm    | ✅/⚠️/❌ | One-line observation |
| Word Choice | ✅/⚠️/❌ | One-line observation |
| Logic     | ✅/⚠️/❌ | One-line observation |
| Warmth    | ✅/⚠️/❌ | One-line observation |
| Density   | ✅/⚠️/❌ | One-line observation |
```

### 4. Detailed Analysis
For dimensions scored ⚠️ or ❌, provide 1-3 concrete quotes with explanation.

### 5. Probable Origin
- **Pure AI**: All dimensions show strong AI patterns
- **AI + Human Edit**: AI skeleton visible but human edits added details
- **Human + AI Polish**: Human voice dominates; AI patterns limited to structure
- **Pure Human**: No significant AI patterns

### 6. Improvement Suggestions
2-4 concrete, actionable changes ranked by impact.

## Comparison Mode

Cross-comparison table for multiple articles:

```
| | Article A | Article B | Article C |
|---|---|---|---|
| AI Flavor | ⚠️ Moderate | ❌ Heavy | ✅ Low |
| Details/Quotes | None | None | ✅ |
| Colloquial | Yes | No | ✅ |
| Likely Origin | Human + AI polish | AI + Human edit | Pure human |
```

## Reference Material

- `references/evaluation-examples.md` — Calibrated Chinese evaluation examples
- `references/indicator-checklist.md` — 32-item rapid checklist

---

## Usage Note

- When evaluating a **Chinese** article: read the Chinese section above for indicator details, output results in Chinese
- When evaluating an **English** article: read the English section above for indicator details, output results in English
- When evaluating a **bilingual** article: apply both sections, note the mix
- Always auto-detect language before starting the evaluation
