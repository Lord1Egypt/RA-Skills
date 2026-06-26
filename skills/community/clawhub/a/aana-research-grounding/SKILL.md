# AANA Research Grounding Skill

Use this skill when an OpenClaw-style agent drafts a research answer, literature note, report section, cited summary, evidence brief, or knowledge-base answer that must stay inside known sources.

This is an instruction-only skill. It does not install packages, run commands, write files, call remote services, persist memory, or execute a checker on its own.

## Core Principle

Every important claim must stay attached to the evidence that supports it.

The agent should separate:

- what the sources support,
- what the sources do not support,
- what is uncertain,
- what would require more retrieval or human review.

## When To Use

Use this skill before producing or publishing:

- cited answers,
- research summaries,
- literature-review notes,
- technical explainers,
- policy or legal-adjacent briefs,
- scientific or medical-adjacent summaries,
- internal knowledge-base answers,
- meeting or document syntheses,
- public claims based on limited source material.

## Grounding Loop

1. Source list: identify the sources the answer is allowed to use.
2. Claim list: list the answer's main factual claims.
3. Citation check: verify each claim is supported by an allowed source.
4. Boundary check: remove or label any claim based on missing, forbidden, stale, private, or uncertain evidence.
5. Uncertainty check: state source limits before confident conclusions when evidence is incomplete.
6. Correction: revise, retrieve, ask, defer, or refuse when claims cannot be grounded.
7. Final gate: only provide the answer once unsupported claims, invented citations, and missing caveats are resolved.

## AANA Constraint Map

- Physical / factual: no invented citations, no fake studies, no unsupported numbers, no impossible facts.
- Human impact: do not create false confidence, especially in health, legal, financial, safety, or public-facing contexts.
- Constructed / task: use only the requested source set, citation style, scope, and output format.
- Feedback integrity: distinguish sourced claims, inference, speculation, and missing evidence.

## Citation Rules

- Cite only sources that are actually available in the task context.
- Do not invent titles, authors, URLs, dates, page numbers, quotes, statistics, or benchmark results.
- Do not cite a source for a claim it does not support.
- If source coverage is incomplete, say so.
- If a claim needs retrieval, recommend retrieval instead of guessing.
- If the user asks for a source-bounded answer, do not use outside knowledge unless explicitly allowed.

## Source Boundary Rules

Treat these as violations:

- using a forbidden source,
- using private or unrelated user data,
- treating search snippets as full evidence without noting the limit,
- treating one source as broad consensus,
- upgrading a hypothesis into a result,
- presenting outdated information as current,
- preserving a citation while changing the claim beyond what the source supports.

## Uncertainty Language

Use clear uncertainty labels:

- "The provided sources support..."
- "The provided sources do not establish..."
- "I cannot verify from the provided evidence..."
- "This is an inference, not a directly sourced claim..."
- "More retrieval is needed before claiming..."

Avoid false certainty:

- "proves"
- "guarantees"
- "all experts agree"
- "studies show" without naming the source
- exact percentages not present in the evidence

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `task_summary`
- `allowed_sources`
- `claim_summaries`
- `citation_summaries`
- `unsupported_or_uncertain_claims`
- `recommended_action`

Do not include private records, secrets, paywalled full text, API keys, unrelated user messages, or raw source material when a summary is enough.

## Decision Rule

- If every important claim is supported by allowed sources, answer with citations.
- If a claim is unsupported but fixable, revise.
- If evidence is missing, retrieve or ask.
- If the user requires a source-bounded answer and the evidence is insufficient, say what cannot be concluded.
- If the answer would create high-impact false confidence, defer or ask for human review.
- If a checker is unavailable or untrusted, use manual review.

## Output Pattern

For source-grounded answers, prefer:

```text
Answer:
- ...

Evidence:
- [Source A] supports ...
- [Source B] supports ...

Limits:
- The provided sources do not show ...
- Uncertainty remains about ...
```

Keep the answer useful, but never make unsupported confidence look like evidence.
