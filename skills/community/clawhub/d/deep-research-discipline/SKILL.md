---
name: deep-research-discipline
description: "Evidence-first workflow for multi-source deep research: requires cited sources, three-state confidence labels, cross-validation, and an independent review gate. Use when asked to research a topic in depth, verify claims across several sources, compare options, or produce a cited report. Tool-agnostic; needs only search, page fetch, and file read/write. Not for quick lookups, single-source summaries, or real-time data."
license: MIT
---

# Deep Research Discipline

A process for producing research reports whose claims can be traced, graded, and challenged — rather than a search recipe.

> This skill was developed and refined through agent operation, not hand-authored as a prompt template. See the repository README for provenance.

## Applicability

**Use for**
- Multi-source fact gathering where being wrong is costly (market, technical, policy, competitor, standards).
- Claims that need to be separated into verified / single-source / unresolved.
- Reports that another person or agent must be able to audit later.

**Do not use for**
- A single lookup, a definition, or a quick link summary.
- Real-time values (prices, scores, incidents) where any cached source is stale by definition.
- Decisions requiring private/internal data the researcher cannot access.
- Legal, medical, or safety-critical advice — this process improves traceability, not professional judgment.

## Capability boundary

Required (the workflow cannot run without these):
- Keyword search over the public web.
- Fetching a URL and extracting readable text.
- Reading and writing local files.

Optional (improves coverage; absence causes explicit degradation, never silent degradation):
- Date-range or recency filtering.
- PDF / Office / scanned-document extraction.
- Social or community sources (forums, social platforms).
- Code execution (for calculations over collected data).

**Known limits** — state these in the report when relevant:
- Paywalled, login-gated, or deleted content may be unreachable; search snippets are not evidence.
- Search indexes lag; a “not found” result does not prove non-existence.
- Non-English and offline sources are under-covered unless deliberately searched.
- Secondary reporting can inherit the errors of its primary source.
- This process reduces the probability of unsupported claims; it does not eliminate error.

## Step 0 — Capability check

Before searching, list which required and optional capabilities are actually available in this environment, and write one line in the working notes:

`capabilities: search=<yes/no> fetch=<yes/no> files=<yes/no> dates=<yes/no> documents=<yes/no> social=<yes/no>`

Any capability marked `no` must appear later in the report's limitations section. **Completion criterion:** the capability line exists and matches what the tools actually do.

## Step 1 — Frame the question

Split the request into 3–6 answerable sub-questions. For each, note the claim type (fact, number, date, causal explanation, opinion) and what evidence would settle it.

**Completion criterion:** every sub-question has a claim type and an acceptable evidence definition.

## Step 2 — Search anchors

For each sub-question, derive anchors before searching: the exact entity name, the likely original publisher (regulator, vendor, standards body, paper), and a fallback query if the first returns noise.

Prefer the most primary source that can answer it: official document > dataset > first-hand report > reputable secondary > aggregator > social post.

**Completion criterion:** each sub-question has at least one named primary-source candidate.

## Step 3 — Collect with independence

For every material claim, collect at least two sources that are **independent** — not two outlets quoting the same press release or the same dataset.

Record for each source: URL, publisher, publication date, retrieval time, and whether it is primary or secondary.

**Completion criterion:** every claim in the final report maps to at least one recorded source; material claims have two independent ones or an explicit single-source flag.

## Step 4 — Grade the evidence

Label every material claim with one of three states:

| State | Meaning |
|---|---|
| `verified` | Two or more independent sources agree, or one authoritative primary source states it explicitly. |
| `single-source` | Only one source, or multiple sources derived from one origin. |
| `unresolved` | Sources conflict, or no adequate source was found. |

Numbers, dates, and version identifiers must carry the source and retrieval date inline.

**Completion criterion:** no material claim is left unlabeled; conflicts are shown, not averaged away.

## Step 5 — Resolve conflicts

When sources disagree, do not pick the more convenient one. Check, in order: publication date, whether one source cites the other, definition differences, scope differences, and known errata. If still unresolved, report both with the conflict stated.

**Completion criterion:** each conflict has either a resolution with evidence or an explicit `unresolved` entry.

## Step 6 — Write the report

Use this structure:

```
# <topic>
## One-line answer
## Key findings (3–5, each with evidence state)
## Key data (number, source, date)
## Conflicting or missing evidence
## Analysis (per sub-question, traceable)
## Limitations (capability gaps, paywalls, coverage)
## Independent review record (BLOCKING)
## References (URL + retrieval time)
```

**Completion criterion:** every section present; the limitations section names every `no` capability from Step 0.

## Step 7 — Independent review (blocking)

Have a separate reviewer — a different agent, session, or person — re-check 3–5 core data points against primary sources, without seeing the draft's conclusion first. Record each as PASS / FAIL / INCONCLUSIVE with the reviewer's own command or citation.

If no independent reviewer is available, say so explicitly in the report and mark the review section `not performed`. Do not present self-review as independent review.

**Completion criterion:** the review section exists, names the reviewer type, and lists per-point verdicts or an explicit `not performed`.

## Degradation rules

- Missing social capability → “community sentiment not covered”, never implied.
- Missing document extraction → “original document not read; summary only”.
- Search returns nothing → run at least two alternative query formulations and one alternative source type before concluding absence.
- Never convert a snippet into a quotation; open the page or mark it unread.

## Final self-check

1. Every number has a source and a date.
2. Every claim has a state label.
3. Material claims have two independent sources, or are flagged.
4. Limitations list matches the Step 0 capability line.
5. Review section is real, or explicitly `not performed`.

Optional channel mapping: see `references/adapters.md`.
