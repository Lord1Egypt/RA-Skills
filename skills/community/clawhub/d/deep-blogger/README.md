# Blog Writer — 深度博客写作助手

**v1.0.1** · *Write with depth. Think with rigor. Communicate with clarity.*

> 🇨🇳 **中文简介：** 一个面向严肃写作者的博客写作 Skill，覆盖七类主题，每类有专属写作模板。强制要求历史溯源、批判性思维与精确定义；在遇到复杂概念时自动调用 [Concept Decoder](https://clawhub.ai/onlybelter/concept-decoder)；在科研与论文类文章中强制引用文献；在编程类文章中包含最佳实践与反模式分析。
>
> 🇬🇧 **English Summary:** A structured blog-writing skill for serious writers, covering seven article categories, each with a dedicated template. Enforces historical context, critical thinking, and precise definitions across all categories. Automatically integrates [Concept Decoder](https://clawhub.ai/onlybelter/concept-decoder) for complex concepts; mandates citations for scientific and paper-walkthrough articles; requires best-practice and anti-pattern sections for all programming articles.

---

## Table of Contents · 目录

1. [What Is This? · 这是什么？](#what-is-this)
2. [Quick Start · 快速开始](#quick-start)
3. [Depth Levels · 深度档位](#depth-levels)
4. [Seven Article Categories · 七类写作场景](#seven-categories)
5. [Universal Writing Principles · 通用写作原则](#universal-principles)
6. [Concept Decoder Integration · 概念解码器集成](#concept-decoder)
7. [Citation Standards · 引用规范](#citations)
8. [Error Handling · 异常处理](#error-handling)
9. [Why This Approach Works · 设计理念](#why-it-works)
10. [Suitable Topics · 适用主题示例](#suitable-topics)
11. [Notes & License · 备注与许可](#notes)

---

## 1. What Is This? · 这是什么？ {#what-is-this}

### English

**Blog Writer** is an AI writing skill designed for intellectually rigorous long-form blog articles. Unlike generic "write me a blog post" prompts, this skill enforces a set of structural and epistemic standards that distinguish serious writing from content generation:

- **Breadth + Depth:** Every article traces the historical origin of its topic, situates it in a broader system, and digs into the technical or conceptual core.
- **Critical Thinking by Default:** No article is complete without presenting both supporting evidence and genuine limitations, criticisms, or open questions.
- **Precision Without Pedantry:** Important concepts are defined accurately; complex ones are decoded intuitively via Concept Decoder.
- **Category-Aware Structure:** Seven article types, each with a tailored template — from paper walkthroughs to science communication to programming tutorials.

### 中文

**Blog Writer** 是一个面向严肃长文写作的 AI 写作 Skill。它不是简单的"帮我写一篇博客"提示词，而是一套有明确结构标准和认识论要求的写作框架：

- **广度与深度并重：** 每篇文章都要追溯主题的历史起源，将其置于更大的系统中理解，并深入技术或概念核心。
- **批判性思维是默认设置：** 没有同时呈现支持证据与真实局限/争议的文章，不算完整。
- **精确而不晦涩：** 重要概念给出准确定义；复杂概念通过 Concept Decoder 进行直观解码。
- **场景感知结构：** 七类文章类型，每类有专属模板——从论文解读到科普写作，从编程教程到数学概念。

### Design Philosophy · 设计哲学

> *"A blog post that only presents one side is an advertisement, not an article."*
> 「只呈现一面的博客文章是广告，不是文章。」

Three principles guide every article this skill produces:

| # | Principle | 原则 |
|---|-----------|------|
| 1 | **Origin before content** — understand where an idea came from before explaining what it is | **溯源优先** — 先理解一个想法从何而来，再解释它是什么 |
| 2 | **Dialectics over advocacy** — present the strongest version of opposing views, not a strawman | **辩证而非倡导** — 呈现对立观点最有力的版本，而非稻草人 |
| 3 | **Intuition before formalism** — build the mental model first, then introduce the precise language | **直觉先于形式** — 先建立心智模型，再引入精确语言 |

---

## 2. Quick Start · 快速开始 {#quick-start}

### Trigger Syntax · 触发语法

```
/blog [topic]
/blog [topic], [category]
/blog [topic], [category], [length]
```

The category and length are optional. If the category is omitted, it will be inferred from the topic. If ambiguous, the skill will ask for clarification.

类别和长度均为可选项。省略类别时，Skill 会根据主题自动推断；若主题存在歧义，会先询问确认。

### Examples · 示例

```bash
# 自动推断类别 / Auto-inferred category
/blog Python异步编程
/blog 贝叶斯定理
/blog 《哥德尔、艾舍尔、巴赫》书评

# 指定类别 / Explicit category
/blog 肿瘤微环境中的细胞通讯, 科学研究
/blog Attention Is All You Need, 科学论文解读
/blog 费曼学习法, 思维方法

# 指定长度 / With length
/blog 拉普拉斯算子, 数学概念, long
/blog 为什么睡眠如此重要, 科普, short

# 英文触发 / English trigger
/blog replica symmetry breaking, scientific research, deep
/blog best practices for async Python, programming
```

### Category Auto-Inference Rules · 类别自动推断规则

| Signal in Topic · 主题信号 | Inferred Category · 推断类别 |
|--------------------------|---------------------------|
| 论文名 / arXiv ID / "paper walkthrough" | 📄 科学论文解读 |
| 研究领域名词 + "进展/综述/overview" | 🔬 科学研究 |
| 编程语言 / 框架 / 库名 / "最佳实践" | 💻 编程技术 |
| 数学术语 / 定理名 / 公式名 | 📐 数学概念 |
| "学习法" / "思维" / "方法论" / "认知" | 🧠 思维方法 |
| 书名（含书名号）/ "书评" / "读后感" | 📚 书评/综述 |
| "为什么" / "科普" / "通俗解释" | 🌍 科普文章 |

---

## 3. Depth Levels · 深度档位 {#depth-levels}

| Level · 档位 | Trigger · 触发 | Length · 字数 | Best For · 适用场景 |
|-------------|--------------|--------------|-------------------|
| **Short · 简版** | `, short` | ~800–1200 words | 科普入门、思维方法概览 |
| **Standard · 标准** | *(default · 默认)* | ~2000–3500 words | 大多数主题的完整处理 |
| **Long · 深度** | `, long` | ~4000–6000 words | 数学概念、论文解读、领域综述 |

**Short mode** covers: Hook → History → Core Concept → Critical Take → Further Reading
**简版** 覆盖：引子 → 历史 → 核心概念 → 批判性视角 → 延伸阅读

**Standard mode** covers: Full category template, all Universal Principles applied
**标准版** 覆盖：完整类别模板，所有通用原则生效

**Long mode** adds: Full mathematical derivations, Glossary section, extended historical narrative, Layer 4–6 Concept Decoder integration
**深度版** 额外包含：完整数学推导、术语表、扩展历史叙事、Concept Decoder 深度集成

---

## 4. Seven Article Categories · 七类写作场景 {#seven-categories}

### 📄 科学论文解读 · Paper Walkthrough

**目标 / Goal:** 帮助读者理解一篇具体的科学论文——其背景、贡献、方法、结果与意义——而无需先读完原文。
Help readers understand a specific scientific paper — its context, contributions, methods, results, and significance — without requiring them to read the full paper first.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 论文身份卡 | Paper Identity Card |
| §2 | 为什么这篇论文重要 | Why This Paper Matters |
| §3 | 阅读前置知识 | Background Prerequisites |
| §4 | 论文结构导读 | Paper Structure Roadmap |
| §5 | 核心贡献（是什么） | Core Contributions (the "What") |
| §6 | 方法深度解析（怎么做） | Methods Deep Dive (the "How") |
| §7 | 结果与意义 | Results and What They Mean |
| §8 | 批判性评估 ✅⚠️❓🔁 | Critical Evaluation |
| §9 | 影响与传承 | Impact and Legacy |

**特殊要求 / Special Requirements:**
- 引用原文为 `[Paper]`，其他参考文献为 `[Author, Year]` · Cite the decoded paper as `[Paper]`; others as `[Author, Year]`
- §8 批判性评估为**强制项** · §8 Critical Evaluation is **mandatory**
- 核心公式必须附有符号定义和直观解释 · Core equations must include symbol definitions and plain-language interpretation

---

### 🔬 科学研究 · Scientific Research

**目标 / Goal:** 对一个研究领域进行严谨、平衡的综述，适合初入该领域的研究者或需要系统梳理的专家。
A rigorous, balanced overview of a research topic — suitable for researchers entering a field or experts wanting a structured synthesis.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 核心科学问题 | The Central Question |
| §2 | 历史发展脉络（含时间线）| Historical Development |
| §3 | 知识现状地图 ✅🔄❓ | Current State of Knowledge |
| §4 | 主要方法与工具 | Key Methods and Tools |
| §5 | 批判性分析 | Critical Analysis |
| §6 | 未来方向 | Future Directions |

**特殊要求 / Special Requirements:**
- 引用为**强制项**，优先最新文献（≤5年）与高引经典 · Citations are **mandatory**; prefer recent (≤5 years) and seminal high-citation works
- 知识现状须区分"已确立共识 / 活跃争议 / 开放问题"三类 · Knowledge status must distinguish established consensus, active debate, and open questions

---

### 💻 编程技术 · Programming & Technology

**目标 / Goal:** 技术准确、实践导向的文章，帮助开发者理解并正确使用某项技术。
A technically accurate, practically useful article that helps developers understand and correctly apply a technology.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 这项技术解决什么问题 | What Problem Does This Solve? |
| §2 | 历史背景与演进 | Historical Context & Evolution |
| §3 | 核心概念 | Core Concepts |
| §4 | 工作原理（内部机制）| How It Works |
| §5 | 代码示例（渐进式）| Code Examples |
| §6 | ✅ 最佳实践 | Best Practices |
| §7 | ❌ 反模式：应规避的用法 | Anti-Patterns: What to Avoid |
| §8 | 批判性评估（何时用 / 不用）| Critical Evaluation |

**特殊要求 / Special Requirements:**
- §6 最佳实践和 §7 反模式均为**强制项** · §6 Best Practices and §7 Anti-Patterns are both **mandatory**
- 每条反模式遵循固定格式：问题 → 错误示例 → 正确做法 · Each anti-pattern follows: Problem → Bad Example → Fix
- 所有代码必须语法正确、可运行 · All code must be syntactically correct and runnable

**反模式格式示例 / Anti-Pattern Format Example:**
```python
# ❌ Anti-pattern: Bare except clause
try:
    result = risky_operation()
except:          # catches EVERYTHING including KeyboardInterrupt
    pass

# ✅ Fix: Catch specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    handle_error(e)
```

---

### 📐 数学概念 · Mathematical Concepts

**目标 / Goal:** 让一个数学概念真正被理解——不仅形式上正确，而且直觉上可把握。
Make a mathematical concept genuinely understandable — not just formally correct, but intuitively grasped.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 这个数学解决什么问题 | The Problem This Math Solves |
| §2 | 历史发展（必须）| Historical Development |
| §3 | 直觉基础（类比先行）| Intuitive Foundation |
| §4 | 形式化发展（含推导）⚡ | Formal Development |
| §5 | 例子与特殊情形 | Examples and Special Cases |
| §6 | 联系与推广 | Connections and Generalizations |
| §7 | 批判性视角 | Critical Perspective |

**特殊要求 / Special Requirements:**
- 本类别与 Concept Decoder 高度重合，核心概念**优先调用** Concept Decoder · This category overlaps most with Concept Decoder; always trigger it for the central concept
- 若存在多个等价定义，全部列出并解释等价性 · If multiple equivalent definitions exist, present all and explain their equivalence
- 每个展示公式后必须附一句直白解释 · Every display equation must be followed by a plain-language interpretation

**数学写作格式 / Math Formatting:**
- 展示公式：`$$...$$`，居中，如被引用则编号
- 行内公式：`$...$`
- 关键步骤标记 ⚡
- 超过5个公式时提供符号表

---

### 🧠 思维方法 · Mental Models & Thinking Methods

**目标 / Goal:** 以知识诚实、实践可操作、抵制过度简化的方式呈现一种思维框架。
Present a thinking framework in a way that is intellectually honest, practically actionable, and resistant to oversimplification.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 这个方法解决什么认知问题 | The Cognitive Problem |
| §2 | 起源与思想史 | Origin and Intellectual History |
| §3 | 框架解释（含精确定义）| The Framework Explained |
| §4 | 实例演示（≥2个不同领域）| Worked Examples |
| §5 | 效果证据 | Evidence and Effectiveness |
| §6 | 批判性分析 ✅⚠️🚫 | Critical Analysis |
| §7 | 实践应用（可操作步骤）| Practical Application |

**特殊要求 / Special Requirements:**
- §6 须明确区分：适用场景 / 失效场景 / 常见误用 · §6 must distinguish: when it works / when it fails / common misapplications
- 区分轶事证据与实证研究 · Distinguish anecdotal evidence from empirical research
- 与竞争框架进行比较 · Compare with competing frameworks

---

### 📚 书评 / 文献综述 · Book Review / Literature Survey

**目标 / Goal:** 帮助读者判断是否值得阅读该作品，以及应该从中获取什么。
A critical, structured evaluation that helps readers decide whether to read the work and what to take from it.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 作品身份卡 | Work Identity Card |
| §2 | 作者与写作背景 | Author and Context |
| §3 | 核心论点 / 主旨 | Core Arguments / Thesis |
| §4 | 内容综合（长文）| Chapter Synthesis (Long only) |
| §5 | 优点 | Strengths |
| §6 | 缺点与批评（强制）| Weaknesses and Criticisms |
| §7 | 与同类作品比较 | Comparison with Related Works |
| §8 | 适读人群 | Who Should Read This |

**特殊要求 / Special Requirements:**
- §6 为**强制项**，且须引用已有批评文献（如有）· §6 is **mandatory** and should cite existing critical responses where available
- §7 须比较至少2部同类作品 · §7 must compare at least 2 similar works
- 引用格式：APA · Citation format: APA

---

### 🌍 科普文章 · Science Communication

**目标 / Goal:** 让有智识的非专业读者理解一个科学或技术主题，同时不牺牲准确性与知识诚实。
Make a scientific or technical topic accessible to an intelligent non-specialist reader, without sacrificing accuracy or intellectual honesty.

**核心结构 / Key Structure:**

| Section | 内容 | Content |
|---------|------|---------|
| §1 | 钩子：为什么你应该关心 | The Hook: Why Should You Care? |
| §2 | 故事：历史叙事（必须）| The Story: Historical Narrative |
| §3 | 概念：简单解释 | The Concept: Explained Simply |
| §4 | 深度：进一步探索（可选）| The Depth: Going Further (optional) |
| §5 | 意义：所以呢？ | The Implications: So What? |
| §6 | 批判诚实 | Critical Honesty |

**特殊要求 / Special Requirements:**
- Concept Decoder 应**主动**调用（快速模式），而非被动等待 · Concept Decoder should be triggered **proactively** (quick mode)
- 公式最小化：必要时用类比替代，若必须出现则作为句子引入 · Minimize formulas; use analogies instead; if essential, introduce as a sentence
- §6 须纠正常见误解，区分"有前景的研究"与"已确立事实" · §6 must correct misconceptions and distinguish "promising research" from "established fact"
- 写作标准：面向"有好奇心的16岁读者" · Writing standard: "curious 16-year-old" benchmark

---

## 5. Universal Writing Principles · 通用写作原则 {#universal-principles}

以下六条原则对**所有类别、所有长度**的文章强制生效。
The following six principles apply to **all categories and all length levels** without exception.

| # | Principle · 原则 | Requirement · 要求 | Mandatory? |
|---|-----------------|-------------------|------------|
| **P1** | **Origin and History First · 溯源优先** | 每篇文章必须包含主题的起源与发展历史，核实人物、时间、机构 | ✅ All |
| **P2** | **Systemic Perspective · 系统视角** | 将主题置于更大的系统中，展示其依赖关系与上下文 | ✅ All |
| **P3** | **Critical Thinking · 批判性思维** | 必须呈现正反两面；明确标注争议性主张 | ✅ All |
| **P4** | **Precise Definitions · 精确定义** | 重要概念首次出现时给出准确定义；复杂概念调用 Concept Decoder | ✅ All |
| **P5** | **Math with Intuition · 数学+直觉** | 每个展示公式后附直白解释；先定义符号；标记关键步骤 ⚡ | ✅ When math present |
| **P6** | **Fact Verification · 事实核查** | 人名、时间、地点、机构、统计数据须可溯源；不确定时明确标注 | ✅ All |

### P6 Fact Verification Checklist · 事实核查清单

在完成任何文章草稿前，逐项确认：
Before finalizing any article draft, verify each item:

- [ ] 所有人名：全名、所属机构、国籍是否正确？· All named persons: full name, affiliation, nationality correct?
- [ ] 所有日期：发表/发明/事件年份是否正确？· All dates: year of publication/invention/event correct?
- [ ] 所有机构名：拼写是否正确，是否仍然存在？· All institutional names: spelled correctly, still active?
- [ ] 所有引用统计数据：来源是否可追溯？· All cited statistics: source traceable?
- [ ] 所有引用语录：是否经原始来源核实？· All attributed quotes: verified against original source?

---

## 6. Concept Decoder Integration · 概念解码器集成 {#concept-decoder}

**Concept Decoder** (https://clawhub.ai/onlybelter/concept-decoder) 是本 Skill 的核心依赖工具，用于对复杂概念进行第一性原理解构。

**Concept Decoder** is a core dependency of this skill, used to deconstruct complex concepts from first principles.

### When to Trigger · 触发条件

| Condition · 条件 | Action · 动作 |
|-----------------|--------------|
| 一个概念需要超过2句话才能准确定义 · A concept requires more than 2 sentences to define accurately | `/decode [concept]` |
| 该概念是文章核心且非平凡 · The concept is central to the article and non-trivial | `/decode [concept], deep` |
| 写作科普文章时遇到技术术语 · Writing science communication with a technical term | `/decode [concept], quick` |
| 数学概念类文章的核心概念 · Central concept in a mathematical concepts article | `/decode [concept], deep` (优先) |
| 用户在文章中途询问"X是什么" · User asks "what is X?" mid-article | `/decode [concept]` |

### How to Embed · 嵌入方式

在文章中以"概念聚焦"块的形式嵌入 Concept Decoder 的输出：
Embed Concept Decoder output as a "Concept Spotlight" block within the article:

```markdown
> 💡 **概念聚焦 · Concept Spotlight: [概念名称]**
>
> [在此嵌入 Concept Decoder 的 Layer 1+2 输出（快速模式）
>  或 Layer 1–4 输出（标准/深度模式）]

如上文概念聚焦所述，[概念] 的核心含义是……
As explained in the Concept Spotlight above, [concept] means...
```

### Integration by Category · 各类别集成深度

| Category · 类别 | Integration Level · 集成深度 | Default Mode · 默认模式 |
|----------------|---------------------------|----------------------|
| 数学概念 | 核心用途，优先调用 · Primary use, always trigger | Deep |
| 科普文章 | 主动调用，面向大众 · Proactive, audience-aware | Quick |
| 科学论文解读 | 前置知识模块中调用 · Called in prerequisites section | Standard |
| 科学研究 | 遇复杂方法论概念时调用 · For complex methodological concepts | Standard |
| 编程技术 | 遇复杂底层概念时调用 · For complex underlying concepts | Standard |
| 思维方法 | 遇认知科学概念时调用 · For cognitive science concepts | Quick |
| 书评/综述 | 遇作品核心概念时调用 · For the work's central concepts | Standard |

---

## 7. Citation Standards · 引用规范 {#citations}

### Summary Table · 汇总表

| Category · 类别 | Required? · 是否必须 | Format · 格式 | Placement · 位置 |
|----------------|--------------------|--------------|--------------| 
| 📄 科学论文解读 | ✅ 强制 | `[Author et al., Year]` | 行内 + 末尾列表 |
| 🔬 科学研究 | ✅ 强制 | `[Author et al., Year, Journal]` | 行内 + 末尾列表 |
| 📐 数学概念 | ✅ 推荐 | `Author, *Title*, Year` | 行内 + 末尾列表 |
| 🧠 思维方法 | ✅ 推荐 | `Author, *Title*, Year` | 行内 + 末尾列表 |
| 📚 书评/综述 | ✅ 强制 | APA 格式 | 行内 + 末尾列表 |
| 🌍 科普文章 | ✅ 推荐 | `Author, *Title*, Source, Year` | 末尾"延伸阅读"列表 |
| 💻 编程技术 | ⚡ 来源决定 | `[Source Name, URL]` | 末尾列表 |

### General Rules · 通用规则

1. **不引用无法核实的来源** · Never cite a source you cannot verify
2. **优先一手来源** · Prefer primary sources over secondary sources — cite the original paper, not a blog post about the paper
3. **科学主张必须引用原始论文** · For scientific claims, cite the original research, not a popular article
4. **争议性主张须明确标注** · If a claim is contested, say so explicitly rather than omitting the citation
5. **不确定时诚实标注** · When uncertain, flag it: *(date unverified)*, *(attribution disputed)*

### Reference List Format · 参考文献列表格式

**科学论文 / Scientific paper:**
```
[1] Vaswani, A., et al. (2017). Attention is all you need.
    Advances in Neural Information Processing Systems, 30.
```

**书籍 / Book:**
```
[2] Hofstadter, D. R. (1979). Gödel, Escher, Bach: An Eternal Golden Braid.
    Basic Books.
```

**网络资源 / Web resource:**
```
[3] Python Software Foundation. (2024). asyncio — Asynchronous I/O.
    https://docs.python.org/3/library/asyncio.html [Accessed: 2024-01-15]
```

---

## 8. Error Handling · 异常处理 {#error-handling}

### Topic Too Broad · 主题过于宽泛

**Example:** `/blog 人工智能` / `/blog machine learning`

**Response:** 提出4–6个子主题，请用户选择一个角度；若用户想写系列文章，提供建议的写作顺序。
Propose 4–6 sub-topics; ask user to choose an angle; offer a suggested series order if they want multiple articles.

---

### Topic Ambiguous · 主题存在歧义

**Example:** `/blog 熵` (热力学熵？信息熵？哲学意义上的熵？)

**Response:** 列出所有合理解读，询问用户选择哪个角度；也可提供"统一视角"文章，但须在各节明确标注所讨论的是哪种熵。
List all valid interpretations; ask which angle to take; offer a unified treatment with clearly labeled sections as an alternative.

---

### Category Cannot Be Inferred · 无法推断类别

**Response:** 询问目标读者：
Ask about the target audience:
> "这篇文章的目标读者是谁？
> A) 专业研究者 / B) 开发者 / C) 大众读者 / D) 学生"
> "Who is the target reader? A) Researchers / B) Developers / C) General public / D) Students"

答案通常可以唯一确定类别。· The answer usually resolves the category.

---

### Insufficient Information for Fact Verification · 事实核查信息不足

**Response:** 不编造日期、人名或统计数据。明确标注不确定内容，建议用户发布前核实。
Do not fabricate dates, names, or statistics. Flag uncertain content explicitly; recommend verification before publishing.

推荐核查数据库 / Recommended verification sources:
- 学术文献：arXiv, PubMed, Google Scholar, Semantic Scholar
- 编程文档：官方文档, GitHub Releases, Changelog
- 历史事实：Wikipedia（仅作初步核查）+ 原始文献

---

### Topic Requires Real-Time Information · 主题需要实时信息

**Response:** 明确标注知识截止日期，建议发布前核实最新进展。
Clearly flag the knowledge cutoff; recommend checking for recent developments before publishing.

> ⚠️ **注意 / Note:** 以下内容基于训练数据，可能不包含最新进展。建议发布前在 arXiv / PubMed / 官方文档中核实。
> The following content is based on training data and may not reflect the latest developments. Please verify in arXiv / PubMed / official documentation before publishing.

---

## 9. Why This Approach Works · 设计理念 {#why-it-works}

### 认知科学依据 · Cognitive Science Foundations

本 Skill 的设计基于三条有实证支持的学习与写作原则：
This skill's design rests on three empirically supported principles of learning and writing:

**原则一：先动机，后形式 · Motivation Before Formalism**
> 认知负荷理论（Sweller, 1988）表明，在没有先建立问题动机的情况下直接引入形式定义，会导致"孤立元素效应"——学习者无法将新信息整合进已有知识结构。
> Cognitive Load Theory (Sweller, 1988) shows that introducing formal definitions without first establishing motivation causes the "isolated elements effect" — learners cannot integrate new information into existing knowledge structures.

**原则二：辩证呈现增强批判性思维 · Dialectical Presentation Builds Critical Thinking**
> 研究表明（Kuhn, 1991; Halpern, 2014），仅呈现单一观点的文章会强化确认偏误；而主动呈现对立证据能显著提升读者的论证质量评估能力。
> Research shows (Kuhn, 1991; Halpern, 2014) that single-perspective articles reinforce confirmation bias; actively presenting opposing evidence significantly improves readers' ability to evaluate argument quality.

**原则三：历史叙事提升记忆留存 · Historical Narrative Improves Retention**
> 情节记忆（episodic memory）比语义记忆（semantic memory）更持久（Tulving, 1972）。将概念嵌入其发现的历史故事中，能显著提升长期记忆留存率。
> Episodic memory is more durable than semantic memory (Tulving, 1972). Embedding concepts in the historical story of their discovery significantly improves long-term retention.

---

## 10. Suitable Topics · 适用主题示例 {#suitable-topics}

| Category · 类别 | Example Topics · 示例主题 |
|----------------|------------------------|
| 📄 科学论文解读 | Attention Is All You Need · AlphaFold 2 · A Mathematical Theory of Communication |
| 🔬 科学研究 | 肿瘤微环境中的免疫逃逸 · 单细胞测序技术进展 · 量子纠错研究现状 |
| 💻 编程技术 | Python 异步编程 · Rust 所有权系统 · Docker 最佳实践 · Git 工作流 |
| 📐 数学概念 | 贝叶斯定理 · 傅里叶变换 · 黎曼流形 · 信息熵 · 奇异值分解 |
| 🧠 思维方法 | 费曼学习法 · 第一性原理思维 · 卡片盒笔记法 · 心智对比 |
| 📚 书评/综述 | 《哥德尔、艾舍尔、巴赫》· 《统计学习要素》· 《人类简史》|
| 🌍 科普文章 | 为什么睡眠如此重要 · 量子计算能做什么 · 癌症是如何发生的 |

**不适用场景 / Not suitable for:**
- 简短问答（直接回答更高效）· Quick Q&A (direct answer is more efficient)
- 正式学术论文（体裁规范不同）· Formal academic papers (different genre conventions)
- 新闻报道（时效性要求超出能力范围）· News reporting (real-time requirements exceed capability)

---

## 11. Notes & License · 备注与许可 {#notes}

### Notes · 备注

- 本 Skill 生成文章草稿；用户在发布前应核实所有事实性内容。· This skill generates article drafts; users should verify all factual content before publishing.
- Concept Decoder (https://clawhub.ai/onlybelter/concept-decoder) 是本 Skill 的依赖工具，遇到复杂概念时应主动调用。· Concept Decoder is a dependency; trigger it proactively for complex concepts.
- 对于科学和数学类文章，宁可精确也不要过度简化——不准确的科普比诚实的复杂性危害更大。· For scientific and mathematical articles, err toward precision over simplification — inaccurate popularization is worse than honest complexity.
- P3（批判性思维）要求不可妥协：只呈现一面的文章是广告，不是文章。· P3 (Critical Thinking) is non-negotiable: a one-sided article is an advertisement, not an article.
- 对不确定的事实诚实标注，这是特性，不是缺陷。· Intellectual honesty about uncertain facts is a feature, not a weakness.

### Companion Skills · 配套 Skill

| Skill | 用途 | Link |
|-------|------|------|
| **Concept Decoder** | 复杂概念第一性原理解构 | https://clawhub.ai/onlybelter/concept-decoder |

### License · 许可

MIT License · 自由使用、修改与分发，保留原始署名。
Free to use, modify, and distribute with attribution.

---

*Built for writers who believe that clarity is not the enemy of rigor, and that every reader deserves both.*
*为那些相信清晰不是严谨的敌人、每位读者都值得两者兼得的写作者而构建。*