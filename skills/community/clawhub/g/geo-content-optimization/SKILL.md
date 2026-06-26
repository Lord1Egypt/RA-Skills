---
name: geo-content-optimization
description: Optimize articles, landing pages, docs, and brand content for visibility, citation, and recommendation in generative AI systems such as ChatGPT, Claude, Gemini, Perplexity, and AI Overviews. Use when the user asks about GEO, AEO, AI SEO, LLM visibility, answer engine optimization, AI citations, AI share of voice, structured content for LLMs, rewriting content to be more citable/extractable, improving Chinese content for AI discovery, or building a repeatable workflow to improve how a brand or page gets surfaced in AI-generated answers.
---

# GEO Content Optimization

Use this skill when the user wants to improve how content gets discovered, extracted, cited, and recommended by AI answer engines.

Default goal:
- make content easier for AI systems to extract and quote
- increase brand/topic association
- improve odds of being cited in AI-generated answers
- turn fuzzy “AI SEO” talk into a concrete editorial workflow

## What GEO means in practice

Treat GEO as **content clarity + extractability + authority + distribution** for AI-mediated discovery.

Do not promise rankings.
Do not claim a guaranteed placement in ChatGPT, Claude, Gemini, or Perplexity.
Frame the work as improving:
- visibility
- citation likelihood
- answer inclusion probability
- brand/topic association

## Core workflow

1. **Clarify the target**
   Identify:
   - brand / product / person / site
   - target topics and queries
   - target engines (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews)
   - page type: article, landing page, docs, FAQ, comparison page, glossary, category page
   - desired outcome: cited, summarized, compared, recommended, remembered

2. **Choose the GEO mode**
   - **Audit mode**: evaluate existing content and find gaps
   - **Rewrite mode**: rewrite an article/page for stronger extractability and citation value
   - **Brief mode**: create an outline for a GEO-first article
   - **Entity mode**: strengthen brand/entity-topic associations
   - **Comparison mode**: create “X vs Y”, alternatives, best-for, use-case content
   - **FAQ mode**: generate structured Q&A blocks optimized for answer engines
   - **Chinese GEO mode**: rewrite Chinese content for higher clarity, quotability, and AI citation fitness

3. **Evaluate against the GEO checklist**
   Check for:
   - clear topic-entity association in first 150 words
   - direct answer blocks near the top
   - headings that mirror user queries
   - scannable facts, comparisons, steps, pros/cons, definitions
   - updated facts and explicit dates when relevant
   - named entities, product names, use cases, and terminology consistency
   - quotable lines that an answer engine can easily lift
   - supporting evidence, examples, and concrete claims

4. **Rewrite for extraction**
   Prefer:
   - direct, plain answers before nuance
   - short paragraphs
   - clear subheads
   - structured lists and tables
   - definition-style sentences
   - use-case phrasing
   - comparison framing

5. **Add answer-engine hooks**
   Typical hooks:
   - “What is X?”
   - “How does X work?”
   - “Who is X for?”
   - “X vs Y”
   - “Best X for …”
   - “Common mistakes”
   - “FAQ”

6. **Package the deliverable**
   Return in this order when relevant:
   - GEO diagnosis
   - rewrite priorities
   - revised structure
   - rewritten content or sections
   - FAQ block
   - distribution suggestions
   - measurement suggestions

## Chinese GEO guidance

For Chinese content, optimize for:
- 开头 3 句内说清“它是什么 / 适合谁 / 为什么值得看”
- 避免空泛抒情和长铺垫
- 用可摘录句代替抽象判断
- 多用“是什么 / 为什么 / 怎么做 / 和谁比 / 适合谁”结构
- 补 FAQ、对比块、结论块
- 让每个段落单独摘出来也能成立

## Writing rules for GEO

- Answer the implied question early.
- Put the clearest version of the truth first.
- Write for extraction, not suspense.
- Use explicit nouns over vague pronouns.
- Repeat the core entity-topic pair naturally.
- Prefer “X is …” / “X helps …” / “X is best for …” structures.
- Use tables when a reader may ask for comparison.
- Keep strong, quotable sentences that can survive outside the page context.
- When facts may age, add date context.

## What usually hurts GEO

Avoid these anti-patterns:
- long throat-clearing intros
- vague thought-leadership with no answer blocks
- brand pages that never clearly say what the product is
- weak headings that don’t match user query language
- only abstract benefits, no concrete use cases
- excessive marketing language with low information density
- hidden definitions buried deep in the page
- no FAQ / no comparison / no direct answer sections

## Deliverable patterns

### Audit output
- Current GEO score / diagnosis
- Top 5 weaknesses
- Top 5 fixes
- Suggested new headings
- Suggested FAQ block

### Rewrite output
- New title
- Better intro
- Revised H2/H3 structure
- Rewritten sections
- FAQ block
- Suggested comparison table

### Brief output
- Target query cluster
- Entity/topic framing
- Search/answer intent
- Outline
- extraction hooks
- proof/examples to include

## Measurement guidance

Use these indicators when possible:
- AI citation presence
- AI mention frequency
- share of voice in answer engines
- branded query growth
- referral traffic from AI surfaces when available
- impression / click shifts on high-intent informational pages

## Bundled resources

- `references/geo-principles.md` — core GEO concepts, terminology, and practical heuristics
- `references/query-patterns.md` — common answer-engine query patterns to map content against
- `references/rewrite-playbook.md` — tactical rewrite moves for articles, landing pages, and docs
- `references/chinese-geo-playbook.md` — Chinese GEO rewrite patterns for公众号/官网/品牌内容
- `references/demo-use-cases.md` — demo-friendly before/after scenarios you can show or sell
- `scripts/geo_audit.py` — lightweight audit for markdown/html/text pages using GEO heuristics
- `scripts/geo_rewrite_brief.py` — generate a structured GEO rewrite brief from raw content

## How to use the scripts

Quick audit:

```bash
python3 scripts/geo_audit.py <file>
```

Rewrite brief:

```bash
python3 scripts/geo_rewrite_brief.py <file>
```

Rewrite output package:

```bash
python3 scripts/geo_rewrite_output.py <file>
```

Use scripts for a fast first pass, then apply editorial judgment.

## Default stance

Be concrete.
Be skeptical of hype.
Turn “AI SEO” into visible content changes, not buzzword theater.
cripts/geo_rewrite_brief.py <file>
```

Use scripts for a fast first pass, then apply editorial judgment.

## Default stance

Be concrete.
Be skeptical of hype.
Turn “AI SEO” into visible content changes, not buzzword theater.
