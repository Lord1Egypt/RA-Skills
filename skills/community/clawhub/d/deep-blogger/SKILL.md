# Blog Writer — 深度博客写作助手 · v1.0.1

针对特定主题撰写结构完整、逻辑清晰、深入浅出的博客文章。支持七类写作场景，每类有专属写作模板与规范。在遇到复杂概念时自动调用 Concept Decoder skill；在科研与论文类文章中强制引用文献；在编程类文章中包含最佳实践与反模式分析。

---

## Overview

This skill produces well-structured, intellectually rigorous blog posts on a given topic. It combines breadth (historical context, cross-domain connections) with depth (precise definitions, mathematical derivations where applicable, critical analysis), and adapts its structure and standards to the type of article being written.

**Language policy:** Respond in the same language the user writes in. Mixed input defaults to Chinese.

---

## When to Use This Skill

Use `/blog` to trigger this skill when:

- User wants to write or draft a blog post on a specific topic
- User wants a structured, publication-ready article (not a quick answer)
- User says things like "帮我写一篇关于X的博客"、"write a blog post about X"、"draft an article on X"

**Do NOT use this skill when:**
- User only needs a brief explanation (use direct answer or `/decode` instead)
- User needs a formal academic paper (different genre conventions apply)

---

## Trigger Syntax

```
/blog [topic]
/blog [topic], [category]
/blog [topic], [category], [length]
```

**Examples:**
```
/blog Python异步编程
/blog 肿瘤微环境中的细胞通讯, 科学研究
/blog 贝叶斯定理, 数学概念, long
/blog Attention Is All You Need 论文解读
/blog 费曼学习法, 思维方法
/blog 为什么睡眠如此重要, 科普
/blog 《哥德尔、艾舍尔、巴赫》书评
```

If category is not specified, infer from the topic. If ambiguous, ask the user to confirm.

---

## Article Length Levels

| Level | Trigger | Approx. Length | Suitable For |
|-------|---------|----------------|-------------|
| **Short** | `, short` | ~800–1200 words | 科普、思维方法入门 |
| **Standard** | *(default)* | ~2000–3500 words | 大多数主题 |
| **Long** | `, long` | ~4000–6000 words | 数学概念、论文解读、综述 |

---

## Universal Writing Principles

These apply to **all** article categories without exception.

### P1 — Origin and History First · 溯源优先
Every article must include the **origin and development history** of the topic:
- Who first proposed it? When? In what context?
- How has it evolved? What were the key turning points?
- What is the current state of the field?
- *Verify all factual claims*: names, dates, institutions, events must be accurate.

### P2 — Systemic, Global Perspective · 系统视角
Treat the topic as part of a larger system:
- What does this concept connect to? What does it depend on?
- What broader trends or frameworks does it belong to?
- Avoid treating the topic as an isolated island.

### P3 — Mandatory Critical Thinking · 批判性思维（强制）
Every article must present **both sides** of the argument:
- What are the strengths, successes, and evidence in favor?
- What are the limitations, criticisms, failure cases, or open questions?
- Explicitly label contested claims as contested; do not present one view as universal truth.
- For scientific topics: distinguish established consensus from active debate.

### P4 — Precise Definitions · 精确定义
For every important concept introduced:
- Provide a clear, accurate definition on first use
- If the concept is complex or counterintuitive → trigger **Concept Decoder**:
  ```
  [CALL: concept-decoder @ https://clawhub.ai/onlybelter/concept-decoder]
  /decode [concept name]
  ```
- Summarize key concepts in a **Glossary** section at the end (for Long articles)

### P5 — Mathematics with Intuition · 数学 + 直觉
When mathematical formulas or derivations are included:
- Define every symbol before use
- Show the derivation incrementally (don't jump steps)
- Always follow a formula with a **plain-language interpretation**
- Use visual descriptions or analogies to build intuition
- Mark the conceptually critical step with ⚡
- Maximum formula density: no more than 1 display equation per 200 words on average

### P6 — Fact Verification · 事实核查
Before finalizing any article, verify each item:

- [ ] 所有人名：全名、所属机构、国籍是否正确？· All named persons: full name, affiliation, nationality correct?
- [ ] 所有日期：发表/发明/事件年份是否正确？· All dates: year of publication/invention/event correct?
- [ ] 所有机构名：拼写是否正确，是否仍然存在？· All institutional names: spelled correctly, still active?
- [ ] 所有引用统计数据：来源是否可追溯？· All cited statistics: source traceable?
- [ ] 所有引用语录：是否经原始来源核实？· All attributed quotes: verified against original source?

---

## Article Structure Template (Universal)

Every article follows this spine, with category-specific sections inserted at marked positions:

```
1. Hook / Opening
2. [CATEGORY-SPECIFIC: Context Block]
3. Historical Background & Development
4. Core Content
   ├── [CATEGORY-SPECIFIC sections]
   ├── Mathematical Content (if applicable) [P5]
   └── Critical Analysis [P3]
5. [CATEGORY-SPECIFIC: Special Section]
6. Summary & Key Takeaways
7. Further Reading / References
8. [OPTIONAL] Glossary
```

---

## Category-Specific Templates

<!-- [I-01 FIX] Category order aligned with README:
     论文解读 → 科学研究 → 编程技术 → 数学概念 → 思维方法 → 书评 → 科普 -->

---

### 📄 Category 1: 科学论文解读 (Paper Walkthrough)

**Trigger keywords:** "论文解读"、"paper walkthrough"、"解读这篇论文"、"读懂X论文"

**Goal:** Help readers understand a specific scientific paper — its context, contributions, methods, results, and significance — without requiring them to read the full paper first.

#### Required Sections

**§1 — Paper Identity Card**
```
标题：
作者：（第一作者 + 通讯作者，其余可省略）
期刊/会议：
发表年份：
DOI / arXiv链接：
引用数（截至写作时）：
一句话概括：
```

**§2 — Why This Paper Matters**
- What problem was the field struggling with before this paper?
- Why was this paper a breakthrough (or why is it controversial)?
- Who should read this paper and why?

**§3 — Background: What You Need to Know First**
- List 3–5 prerequisite concepts
- For each complex prerequisite → trigger Concept Decoder
- Cite 2–3 key background papers

**§4 — Paper Structure Roadmap**
- Brief guide to the paper's sections (what each section does, not what it says)
- Highlight which sections are essential vs. skippable for different readers

**§5 — Core Contributions (the "What")**
- List the paper's main claims/contributions as numbered points
- For each: state it precisely, then explain it in plain language

**§6 — Methods Deep Dive (the "How")**
- Explain the key methodological innovations
- Include core equations with full symbol definitions and intuitive explanations [P5]
- Flag any methodological assumptions or limitations

**§7 — Results and What They Mean**
- Key experimental/theoretical results
- What do the numbers/figures actually tell us?
- Compare to prior state-of-the-art

**§8 — Critical Evaluation** [P3 — MANDATORY]
- ✅ Strengths: what the paper does well
- ⚠️ Limitations: what the paper does not address or assumes away
- ❓ Open questions: what remains unresolved after this paper
- 🔁 Subsequent work: has the community validated, extended, or challenged these results?

**§9 — Impact and Legacy**
- Citation trajectory and field impact
- Papers that directly built on this work (cite 2–3)
- Has the paper's influence grown or faded over time?

**Citation standard:** Cite the paper being decoded as [Paper] throughout; all other references as [Author, Year].

---

### 🔬 Category 2: 科学研究 (Scientific Research)

**Trigger keywords:** 科研综述、研究进展、领域综述、research overview

**Goal:** A rigorous, balanced overview of a research topic — suitable for researchers entering a field or experts wanting a structured synthesis.

#### Required Sections

**§1 — The Central Question**
- State the core scientific question this field is trying to answer
- Why does it matter? (scientific significance + broader implications)

**§2 — Historical Development** [P1 — MANDATORY]
- Timeline of key milestones (use a text-based timeline or table)
- Founding figures and their contributions (verify names/dates [P6])
- Paradigm shifts: what changed the field's direction?

**§3 — Current State of Knowledge**
- What is firmly established (consensus)?
- What is actively debated?
- What is unknown?
- Use a **Knowledge Map** table:
  ```
  | Status | Claims |
  |--------|--------|
  | ✅ Established consensus | ... |
  | 🔄 Active debate | ... |
  | ❓ Open question | ... |
  ```

**§4 — Key Methods and Tools**
- Dominant experimental / computational / theoretical approaches
- Include core equations where central to the field [P5]
- For complex methods → trigger Concept Decoder

**§5 — Critical Analysis** [P3 — MANDATORY]
- Major controversies in the field
- Reproducibility concerns (if any)
- Methodological blind spots
- Alternative interpretations of key results

**§6 — Future Directions**
- Most promising open problems
- Emerging methods or paradigm shifts on the horizon

**Citation standard:** MANDATORY. Cite recent papers (≤5 years preferred) AND seminal high-citation works. Format: [Author et al., Year, Journal]. Full list at end.

---

### 💻 Category 3: 编程技术 (Programming & Technology)

**Trigger keywords:** 编程、代码、框架、库、算法实现、技术选型

**Goal:** A technically accurate, practically useful article that helps developers understand and correctly apply a technology.

#### Required Sections

**§1 — What Problem Does This Solve?**
- The concrete pain point this technology addresses
- What existed before and why it was insufficient

**§2 — Historical Context & Evolution** [P1 — RECOMMENDED]
- Origin of the technology (creator, year, motivation)
- Major version milestones and what changed
- Current ecosystem status (actively maintained? deprecated? fragmented?)

**§3 — Core Concepts**
- Key abstractions and their precise definitions [P4]
- Mental model: how should a developer think about this?
- For complex concepts → trigger Concept Decoder

**§4 — How It Works (Internals)**
- Architecture / mechanism explanation
- Include diagrams (ASCII or described) where helpful
- Mathematical foundations if relevant [P5]

**§5 — Code Examples**
- Minimal working example first (the "hello world")
- Progressive complexity: basic → intermediate → advanced
- All code must be syntactically correct and runnable
- Annotate non-obvious lines

**§6 — ✅ Best Practices** [MANDATORY for all programming articles]
- Numbered list of recommended patterns
- For each: explain *why* it's a best practice, not just *what* to do
- Include performance, security, and maintainability considerations

**§7 — ❌ Anti-Patterns: What to Avoid** [MANDATORY for all programming articles]
- Common mistakes and misuses
- Each anti-pattern follows this fixed format:

<!-- [I-04 FIX] Added concrete code-block format example, consistent with README -->
```python
# ❌ Anti-pattern: [name]
# Problem: [what goes wrong and why]
[code showing the bad pattern]

# ✅ Fix:
[correct approach]
```

- Include subtle pitfalls that even experienced developers miss

**§8 — Critical Evaluation** [P3 — MANDATORY]
- When to use this technology (and when NOT to)
- Trade-offs vs. alternatives
- Known limitations, edge cases, version compatibility issues

**Citation standard:** Official documentation, RFC/PEP/spec documents, authoritative blog posts (e.g., engineering blogs from major tech companies). Format: [Source Name, URL, accessed date].

---

### 📐 Category 4: 数学概念 (Mathematical Concepts)

**Trigger keywords:** 数学、定理、证明、公式、代数、分析、几何、概率

**Goal:** Make a mathematical concept genuinely understandable — not just formally correct, but intuitively grasped.

**Primary tool:** This category has the highest overlap with Concept Decoder. For the central concept, **always** trigger Concept Decoder first, then expand into the full article structure.

#### Required Sections

**§1 — The Problem This Math Solves** [P1 — MANDATORY]
- What question or difficulty motivated this concept?
- What failed before it existed?

**§2 — Historical Development** [P1 — MANDATORY]
- Origin: who, when, in what context?
- Key contributors and their roles
- Surprising historical facts (e.g., simultaneous independent discovery, long delays between invention and application)

**§3 — Intuitive Foundation**
- Everyday analogy (concrete, visual)
- Where the analogy breaks — be explicit
- Cross-domain analogy (structural parallel in another field)

**§4 — Formal Development** [P5 — MANDATORY]
- Precise definition(s) — if multiple equivalent definitions exist, present all and explain why they're equivalent
- Key theorems with proof sketches (full proofs in appendix/footnote for Long articles)
- Incremental formula build-up with ⚡ marking the critical step
- Plain-language interpretation after every display equation

<!-- [I-05 FIX] Added category-specific math formatting block, consistent with README -->
**Math Formatting Rules (this category):**
- Display equations: `$$...$$`, centered; number them if cross-referenced
- Inline math: `$...$`
- Mark the conceptually critical derivation step with ⚡
- For articles with 5+ equations: include a **Symbol Table** before §4

**§5 — Examples and Special Cases**
- Simplest non-trivial example first
- Boundary cases: what happens at the limits?
- Numerical examples where illuminating (code optional)

**§6 — Connections and Generalizations**
- What broader framework contains this concept?
- What does it reduce to in special cases?
- Surprising appearances in other fields (lateral connections)

**§7 — Critical Perspective** [P3 — MANDATORY]
- Alternative definitions or formulations (and why they differ)
- Historical controversies (e.g., debates over rigor, constructivism vs. formalism)
- Where the concept breaks down or requires extension

**Citation standard:** Cite original papers AND standard textbooks. Format: Author, *Title*, Publisher/Journal, Year.

---

### 🧠 Category 5: 思维方法 (Mental Models & Thinking Methods)

**Trigger keywords:** 思维、方法论、学习、认知、决策、心智模型

**Goal:** Present a thinking framework in a way that is intellectually honest, practically actionable, and resistant to oversimplification.

#### Required Sections

**§1 — The Cognitive Problem**
- What failure mode in human thinking does this method address?
- Concrete example of the problem (a story or scenario)

**§2 — Origin and Intellectual History** [P1 — RECOMMENDED]
- Who developed this framework? In what field?
- Has it been validated empirically? (cognitive science, psychology, education research)
- For concepts with scientific backing → cite relevant research

**§3 — The Framework Explained**
- Clear, precise definition [P4]
- Step-by-step breakdown
- For complex cognitive concepts → trigger Concept Decoder

**§4 — Worked Examples**
- At least 2 concrete examples from different domains
- Show the method being applied, not just described

**§5 — Evidence and Effectiveness**
- What does the research say? (cite if available)
- Anecdotal vs. empirical evidence — distinguish clearly

**§6 — Critical Analysis** [P3 — MANDATORY]
- ✅ When this method works well
- ⚠️ When it fails or backfires
- 🚫 Common misapplications and oversimplifications
- Competing frameworks and how they compare

**§7 — Practical Application**
- Concrete, actionable steps to implement this method
- Common obstacles and how to overcome them
- How to know if it's working

**Citation standard:** Cognitive science and psychology papers where available. Popular books cited as secondary sources. Format: Author, *Title*, Year.

---

### 📚 Category 6: 书评 / 文献综述 (Book Review / Literature Survey)

**Trigger keywords:** 书评、读书笔记、文献综述、review、读后感

**Goal:** A critical, structured evaluation that helps readers decide whether to read the work and what to take from it.

#### Required Sections

**§1 — Work Identity Card**
```
书名/综述主题：
作者：
出版社/期刊：
出版年份：
页数/篇数：
核心主张（一句话）：
```

**§2 — Author and Context** [P1 — RECOMMENDED]
- Who is the author? What is their background and credibility?
- Why did they write this? What was the intellectual context?
- How was it received when published?

**§3 — Core Arguments / Thesis**
- What is the central claim or organizing framework?
- How is the argument structured?
- Key concepts introduced — define precisely [P4]; trigger Concept Decoder if complex

**§4 — Chapter-by-Chapter / Paper-by-Paper Synthesis** *(for Long articles)*
- Not a summary of each chapter, but a synthesis of the argumentative arc
- Identify the 3–5 most important ideas

**§5 — Strengths** [P3]
- What does the work do exceptionally well?
- What new insight does it provide?
- Quality of evidence and argumentation

**§6 — Weaknesses and Criticisms** [P3 — MANDATORY]
- Logical gaps or unsupported claims
- Missing perspectives or blind spots
- Has the work been criticized in the literature? Cite critics.
- Has subsequent research confirmed or challenged the claims?

**§7 — Comparison with Related Works**
<!-- [I-13 FIX] Changed "2–3 similar works" to "at least 2", consistent with README -->
- Compare with **at least 2** similar books/surveys
- What does this work offer that others don't?
- What do the others offer that this one misses?

**§8 — Who Should Read This**
- Ideal reader profile
- Prerequisites
- How to read it (cover-to-cover? selectively? in what order?)

**Citation standard:** Full bibliographic entry for the reviewed work; APA format for all other references.

---

### 🌍 Category 7: 科普文章 (Science Communication)

**Trigger keywords:** 科普、面向大众、通俗解释、为什么、怎么理解

**Goal:** Make a scientific or technical topic accessible to an intelligent non-specialist reader, without sacrificing accuracy or intellectual honesty.

**Primary tool:** Concept Decoder should be triggered **proactively** for any concept that would be opaque to a non-specialist. Prefer the "quick" decode mode for science communication.

#### Required Sections

**§1 — The Hook: Why Should You Care?**
- Open with a surprising fact, a counterintuitive result, or a relatable scenario
- Connect the topic to something in the reader's daily life
- State the central question in plain language

**§2 — The Story: Historical Narrative** [P1 — MANDATORY]
- Tell the history as a human story, not a timeline
- Focus on the moments of discovery, confusion, and insight
- Name the people involved (verify [P6]) — science is done by humans

**§3 — The Concept: Explained Simply**
<!-- [I-06 FIX] Added "curious 16-year-old" writing standard, consistent with README -->
- Writing standard: **"explain to a curious 16-year-old"** — intelligent but without specialist background
- Analogy first, technical term second
- For each technical term introduced: define it immediately in plain language
- Trigger Concept Decoder (quick mode) for any concept requiring more than 2 sentences to explain
- **Minimize formulas**: if a formula is essential, introduce it as a sentence, not an equation

**§4 — The Depth: Going Further**
- For readers who want more: one level deeper
- Introduce one or two key technical ideas with careful scaffolding
- This section can be marked as "optional" or "for the curious"

**§5 — The Implications: So What?**
- What does this mean for science / technology / society?
- What questions does it open up?
- What is still unknown?

**§6 — Critical Honesty** [P3 — MANDATORY]
- What does the science NOT tell us?
- Where is there genuine uncertainty?
- Common misconceptions to correct
- Avoid hype: distinguish "promising research" from "established fact"

**Citation standard:** Cite authoritative sources (Nature, Science, major textbooks, institutional reports). Keep citations light in the main text; collect at end as "Further Reading."

---

## Concept Decoder Integration

**Concept Decoder** (https://clawhub.ai/onlybelter/concept-decoder) is a core dependency of this skill.

### Trigger Conditions · 触发条件

When any of the following conditions are met, pause the article draft and call Concept Decoder:

| Condition | Action |
|-----------|--------|
| A concept requires more than 2 sentences to define accurately | `/decode [concept]` |
| A concept is central to the article and non-trivial | `/decode [concept], deep` |
| Writing a science communication article with a technical term | `/decode [concept], quick` |
| Central concept in a mathematical concepts article | `/decode [concept], deep` (priority) |
| User explicitly asks "what is X?" mid-article | `/decode [concept]` |

### Integration by Category · 各类别集成深度

<!-- [I-07 FIX] Added 7-category integration depth table, consistent with README -->

| Category · 类别 | Integration Level · 集成深度 | Default Mode · 默认模式 |
|----------------|---------------------------|----------------------|
| 📐 数学概念 | 核心用途，优先调用 · Primary use, always trigger | Deep |
| 🌍 科普文章 | 主动调用，面向大众 · Proactive, audience-aware | Quick |
| 📄 科学论文解读 | 前置知识模块中调用 · Called in prerequisites section | Standard |
| 🔬 科学研究 | 遇复杂方法论概念时调用 · For complex methodological concepts | Standard |
| 💻 编程技术 | 遇复杂底层概念时调用 · For complex underlying concepts | Standard |
| 🧠 思维方法 | 遇认知科学概念时调用 · For cognitive science concepts | Quick |
| 📚 书评/综述 | 遇作品核心概念时调用 · For the work's central concepts | Standard |

### Embedding Protocol · 嵌入方式

1. Insert a clearly marked block: `> 💡 **Concept Spotlight:** [concept name]`
2. Call Concept Decoder and embed the Layer 1+2 output (quick) or Layer 1–4 output (standard/deep)
3. Resume article after the spotlight block
4. Cross-reference: "As explained in the Concept Spotlight above, [concept] means..."

---

## Citation Standards

### Summary Table · 汇总表

| Category · 类别 | Required? · 是否必须 | Format · 格式 | Placement · 位置 |
|----------------|--------------------|--------------|-----------------| 
| 📄 科学论文解读 | ✅ 强制 | `[Author et al., Year]` | 行内 + 末尾列表 |
| 🔬 科学研究 | ✅ 强制 | `[Author et al., Year, Journal]` | 行内 + 末尾列表 |
| 📐 数学概念 | ✅ 推荐 | `Author, *Title*, Year` | 行内 + 末尾列表 |
| 🧠 思维方法 | ✅ 推荐 | `Author, *Title*, Year` | 行内 + 末尾列表 |
| 📚 书评/综述 | ✅ 强制 | APA 格式 | 行内 + 末尾列表 |
| 🌍 科普文章 | ✅ 推荐 | `Author, *Title*, Source, Year` | 末尾"延伸阅读"列表 |
| 💻 编程技术 | ⚡ 来源决定 | `[Source Name, URL, accessed date]` | 末尾列表 |

### Reference List Format · 参考文献格式示例

<!-- [I-08 FIX] Added three concrete format examples, consistent with README -->

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

### General Rules · 通用规则

<!-- [I-09 FIX] Added 5th rule about contested claims, consistent with README -->
1. Never cite a source you cannot verify · 不引用无法核实的来源
2. Prefer primary sources over secondary sources · 优先一手来源
3. For scientific claims: cite the original paper, not a blog post about the paper · 科学主张引用原始论文
4. If a claim is uncertain or contested, say so explicitly rather than omitting the citation · 不确定时诚实标注
5. When uncertain about a fact, flag it explicitly: *(date unverified)*, *(attribution disputed)* · 用标注代替猜测

---

## Error Handling

### Topic is too broad · 主题过于宽泛
- Example: `/blog 人工智能`
- Response: Propose 4–6 sub-topics; ask user to choose one or specify an angle
- Offer a suggested learning path if the user wants a series

### Topic is ambiguous · 主题存在歧义
- Example: `/blog 熵` (thermodynamic? information-theoretic? philosophical?)
- Response: List the interpretations; ask which angle to take; offer to cover all with clear section separation

### Category cannot be inferred · 无法推断类别
<!-- [I-11 FIX] Added A/B/C/D prompt template, consistent with README -->
- Ask the user:
  > "这篇文章的目标读者是谁？
  > A) 专业研究者 / B) 开发者 / C) 大众读者 / D) 学生"
  >
  > "Who is the target reader?
  > A) Researchers / B) Developers / C) General public / D) Students"
- The answer usually resolves the category uniquely.

### Insufficient information for fact verification · 事实核查信息不足
- Do not fabricate dates, names, or statistics
- Flag uncertain facts explicitly: *(date unverified)*, *(attribution disputed)*
- Recommend the user verify before publishing
- Suggested verification sources · 推荐核查数据库:
  - 学术文献：arXiv, PubMed, Google Scholar, Semantic Scholar
  - 编程文档：官方文档, GitHub Releases, Changelog
  - 历史事实：Wikipedia（仅作初步核查）+ 原始文献

### Topic requires real-time information · 主题需要实时信息
<!-- [I-10 FIX] Added warning template block and recommended database list, consistent with README -->
- Flag clearly with the following warning block:

> ⚠️ **注意 / Note:** 以下内容基于训练数据，可能不包含最新进展。建议发布前在 arXiv / PubMed / 官方文档 / GitHub Releases 中核实。
> The following content is based on training data and may not reflect the latest developments. Please verify in arXiv / PubMed / official documentation before publishing.

---

## Formatting Standards

### Headers
- H1: Article title only
- H2: Major sections
- H3: Subsections
- Avoid going deeper than H3 in the article body

### Math
- Display equations: `$$...$$`, centered, numbered if referenced
- Inline math: `$...$`
- Every display equation followed by a plain-language interpretation
- Symbol table for articles with 5+ equations

### Code
- Always specify language in fenced code blocks
- Maximum 30 lines per block; break longer examples into labeled parts
- Anti-pattern examples clearly labeled with `# ❌ Anti-pattern` comment

### Lists
<!-- [I-15 FIX] Added nesting depth limit, consistent with README -->
- Use bullet lists for unordered items (features, options)
- Use numbered lists for sequential steps or ranked items
- **Do not nest lists deeper than 2 levels**

---

## Notes

- This skill generates article drafts; the user should review all factual claims before publishing
- P3 (Critical Thinking) is non-negotiable: a blog post that only presents one side is an advertisement, not an article
- For scientific and mathematical articles, err on the side of more precision rather than less — imprecise popularization is worse than honest complexity
- When in doubt about a fact, say so — intellectual honesty is a feature, not a weakness

### Companion Skills · 配套 Skill

<!-- [I-16 FIX] Added structured Companion Skills table, consistent with README -->

| Skill | 用途 | Link |
|-------|------|------|
| **Concept Decoder** | 复杂概念第一性原理解构 · Deconstruct complex concepts from first principles | https://clawhub.ai/onlybelter/concept-decoder |