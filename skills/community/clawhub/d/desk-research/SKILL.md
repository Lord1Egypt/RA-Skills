---
name: desk-research
description: Structured desk research workflow for market, company, policy, product, and competitor questions. Use when a user asks for secondary research, landscape scans, evidence-based summaries, source triangulation, or insight synthesis from public information.
---

# Desk Research

Execute this workflow for any desk-research request.

## 0) Load methodology checklist (first)

Read `references/methodology.md`, `references/deep-writing-patterns.md`, and `references/quality-checklist.md` and apply all as guardrails.

## 1) Define the research brief

Write 4 lines before searching:
- Research question (1 sentence)
- Scope (time, geography, industry)
- Must-answer sub-questions (3-6 bullets)
- Output format needed by user

If the question is vague, propose assumptions explicitly and continue.

## 2) Build a source plan

Collect evidence in this priority order:
1. Primary/official sources (government, regulator, company filings, product docs)
2. Reputable secondary analysis (major research firms, established media)
3. Community signals (forums/social) only as supporting evidence

Require at least 2 independent sources for every key claim.

## 3) Gather evidence fast

For each sub-question:
- Find 3-8 candidate sources
- Keep the highest-signal sources
- Extract only claim + evidence + date + link

Reject sources that are undated, anonymous, or purely opinionated unless the user asked for sentiment.

## 4) Score source reliability

Tag each source:
- A = official primary source
- B = credible secondary source
- C = weak/indicative source

When claims conflict, prefer newer A/B sources and explicitly note uncertainty.

## 5) Synthesize insights

Convert notes into:
- Facts (well-supported)
- Interpretations (reasoned but inferential)
- Unknowns (gaps needing validation)

Never present interpretation as fact.

### Source hard rule (critical)
For all final research outputs:
- Every major factual claim must include source + date.
- Every key viewpoint, analytical framework, stage model, or category split must either:
  1. cite a source, or
  2. be explicitly labeled as the report author's synthesis / working model.
- Do not present an unsupported framework as if it were an established industry fact.
- If a conclusion combines multiple sources, cite the main supporting sources inline or in the same paragraph.

## 5.5) Deepening loop (mandatory)

Before final delivery, run at least 2 rounds of self-questioning:

Round A — Coverage challenge
- What did I miss by source type, time window, or geography?
- Which category/conclusion is over-dependent on one source?
- What contradicts my current conclusion?

Round B — Decision challenge
- If this conclusion is wrong, what evidence would prove it wrong?
- Which part is descriptive but not decision-useful?
- What next data pull would most change the recommendation?

After each round, update findings and confidence.

## 6) Deliver in concise structure

Use this exact section order:
1. Core Questions (2 questions)
2. One-sentence Verdict
3. Executive Summary (5-8 bullets)
4. Key Findings by sub-question (with metric anchors)
5. Evidence Table (claim | source | date | reliability)
6. Confidence tags (High/Medium/Low per major claim)
7. Risks / Uncertainty
8. What would falsify this conclusion
9. Next Verification Steps / Todo

Inline citation rule:
- In the body, append source/date after key claims whenever it helps verification.
- For analytical frameworks or stage models, add `Source:` or `Author synthesis based on:` explicitly.
- Do not leave major frameworks floating without attribution.

For output shape and compact template, use `references/output-template.md`.

## 7) Quality bar before sending

Check all items:
- Every major claim has source/date
- No single-source critical claim
- Time/geography scope matches user ask
- Clear separation of fact vs interpretation
- Actionable takeaway included
- Each promising case uses the full 9-part deep case framework
- Each promising case includes one final case-summary paragraph: what it does / who pays / business model / why pay
- Each key section ends with decision implication (so-what)

## 8) Case-depth hard rule (for startup/case research)

When the task is startup/use-case research, apply these hard requirements:
- For each promising case, collect at least 3 website evidence snippets (feature/pricing/use-flow)
- Add at least 1 metric anchor from trusted dataset (revenue/MRR/growth)
- Include at least 1 risk point and 1 falsification condition
- Do not submit if any case is only descriptive without judgment
