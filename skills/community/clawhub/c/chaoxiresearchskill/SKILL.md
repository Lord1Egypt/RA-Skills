---
name: deep-research-framework
description: >
  This skill should be used when the user requests a structured, in-depth research on a specific
  topic, industry, technology, product, market, person, organization, or any domain-specific subject.
  Trigger phrases include: "深度调研", "帮我研究一下", "做一份调研报告", "分析一下XX行业/市场/技术",
  "写一份研究报告", "deep research", "research report", "调研", "研究报告", "行业报告",
  "竞品分析", "market research", "技术调研", "可行性分析", "尽职调查".
  This skill guides a rigorous, multi-source, evidence-balanced research process that:
  - Defines research audience and objectives before starting
  - Decomposes the topic into structured dimensions
  - Gathers evidence from multiple sources with credibility ratings
  - Includes counterevidence and conflicting viewpoints
  - Flags information gaps honestly instead of fabricating
  - Delivers a structured report plus a one-page summary card
---

# Deep Research Framework

A structured deep-research skill for producing rigorous, balanced, and actionable research reports on any topic.

## Overview

This skill enforces a disciplined research methodology. It is NOT a simple "search and summarize" tool.
It demands evidence quality control, counterevidence inclusion, and honest flagging of gaps.

Outputs:
1. **Structured Research Report** — full-depth analysis organized by dimensions
2. **One-Page Summary Card** — key findings, confidence levels, and action items

## Phase 0 — Pre-Research Clarification

Before starting research, confirm these inputs from the user or infer them from context:

| Input | Required | Default if absent |
|-------|----------|-------------------|
| Research topic | Yes | — |
| Target audience | Recommended | "decision maker / general professional" |
| Key dimensions to focus on | Optional | Use standard dimension set (see references) |
| Time scope | Optional | "recent 1–3 years unless specified" |
| Depth level | Optional | "standard" (balanced breadth and depth) |

If the topic is ambiguous, ask ONE clarifying question before proceeding.

## Phase 1 — Research Design

### 1.1 Define the Research Objective

State in 1–2 sentences: What question is this research answering, and what decision or understanding will it enable?

### 1.2 Define the Audience

State who will read this: their background, what they already know, and what they need to walk away with.

### 1.3 Scope and Constraints

- Time scope: Which period does the research cover?
- Geographic scope: Global? China? Specific region?
- Exclusions: What is explicitly out of scope?

### 1.4 Decompose into Research Dimensions

Break the topic into 4–7 dimensions. For each dimension:
- Write 2–4 key questions that need answering
- Assign a priority: Core / Supporting / Context

Use `references/dimension-templates.md` for standard dimension sets by research type (industry, technology, company, product, market).

## Phase 2 — Multi-Source Research Execution

### 2.1 Source Strategy

For each dimension, gather from at least 2–3 distinct source types:

| Source Type | Examples | Default Credibility |
|-------------|----------|---------------------|
| Primary data | Official reports, regulatory filings, academic papers | ★★★★★ |
| Industry reports | McKinsey, Gartner, IDC, CB Insights, Frost & Sullivan | ★★★★ |
| News & media | Reuters, Bloomberg, FT, 36kr, 财新, 虎嗅 | ★★★ |
| Expert commentary | Interviews, conference talks, analyst notes | ★★★ |
| Community & forums | Reddit, Zhihu, GitHub Issues, industry forums | ★★ |
| AI-generated synthesis | LLM summaries without cited sources | ★ |

See `references/credibility-rubric.md` for detailed credibility rating rules.

### 2.2 Search Execution

For each research dimension:
1. Formulate targeted search queries (try multiple angles)
2. Retrieve results using web_search or available tools
3. For each piece of evidence, record: claim, source, credibility rating, date

### 2.3 Counterevidence Requirement (MANDATORY)

For every major claim in the report, actively search for contradicting evidence:
- If counterevidence exists: include it alongside the main claim, labeled `[反面证据]`
- If no counterevidence found: note `[未发现明显反面证据，可信度待验]`
- NEVER omit counterevidence to make the report cleaner or more conclusive

### 2.4 Conflicting Information Handling

When two credible sources contradict each other:
- Present BOTH positions side-by-side
- Note the source, date, and credibility of each
- Do NOT pick a side unless evidence weight is clearly asymmetric
- Label the conflict: `[矛盾信息 — 并列呈现]`

### 2.5 Information Gap Flagging (MANDATORY)

When a key question cannot be answered from available sources:
- Mark it clearly: `[信息不足 — 无法得出可靠结论]`
- State what type of source would be needed to fill the gap
- NEVER fabricate data, statistics, or citations to fill gaps

## Phase 3 — Synthesis and Analysis

### 3.1 Evidence Weighting

Synthesize findings dimension by dimension:
- Higher-credibility sources take precedence
- Recent data (within 12 months) takes precedence over older data
- Consensus across multiple independent sources strengthens confidence

### 3.2 Insight Generation

Go beyond summarizing to identify:
- Key patterns and trends
- Surprising or counterintuitive findings
- Implications for the research objective
- Open questions that remain after research

### 3.3 Confidence Levels

Assign a confidence level to each major finding:

| Level | Meaning |
|-------|---------|
| 高 (High) | Multiple independent ★★★★+ sources agree |
| 中 (Medium) | Some evidence, limited cross-validation |
| 低 (Low) | Single source, low credibility, or conflicting signals |
| 未知 (Unknown) | Insufficient data, explicitly flagged |

## Phase 4 — Output Delivery

### 4.1 Full Research Report

Follow the template in `assets/report-template.md`. Structure:

1. **研究概览** — objective, audience, scope, date
2. **执行摘要** — 5–7 bullet key findings with confidence levels
3. **维度分析** — one section per dimension with:
   - Key findings
   - Supporting evidence (with source + credibility)
   - Counterevidence
   - Confidence level
   - Information gaps (if any)
4. **矛盾与争议** — consolidated list of conflicting information
5. **综合洞察** — cross-dimension synthesis and implications
6. **信息缺口清单** — all flagged gaps in one place
7. **参考资料** — all sources with credibility ratings

### 4.2 One-Page Summary Card

Follow the template in `assets/summary-card-template.md`. Deliver after the full report.

The card contains:
- Topic + audience + date (header)
- 3 most important findings (with confidence)
- 1 most important counterpoint
- 1 key uncertainty / gap
- Suggested next actions (if applicable)
- Overall research confidence score (High / Medium / Low)

## Quality Checklist (self-check before delivery)

Before presenting the output, verify:

- [ ] Every major claim has a cited source with credibility rating
- [ ] Counterevidence section is non-empty or explicitly noted
- [ ] All conflicting information is presented side-by-side, not resolved by choosing one
- [ ] All information gaps are explicitly labeled
- [ ] No statistics or citations were fabricated
- [ ] Confidence levels are assigned to all major findings
- [ ] One-page summary card is included
- [ ] Report follows the template structure

## Important Rules

1. **No fabrication**: If data doesn't exist, say so. Never invent statistics, quotes, or citations.
2. **No false certainty**: Do not present uncertain findings as definitive.
3. **Counterevidence is mandatory**: A report without counterevidence is incomplete.
4. **Conflicting sources must coexist**: Do not silently pick one side.
5. **Credibility must be visible**: Every claim should be traceable to a rated source.
