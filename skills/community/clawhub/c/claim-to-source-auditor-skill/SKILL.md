---
name: claim-to-source-auditor
slug: claim-to-source-auditor-skill
displayName: Claim-to-Source Auditor
version: "1.0.9"
description: When the user asks to audit, fact-check, verify, or cross-check an
  article, report, draft, or series. Triggered by
  审稿/审计/核验/事实检查/来源追溯/查一下这个数据/核对/审查/跨平台一致性/三平台统一/回归检查/有没有事实错误/这个引用对不对/跟上次比有没有退化.
  Extracts verifiable claims, traces them to L0 primary or L1 reliable secondary
  sources, marks each as 通过/部分支持/缺证/错误/判断, and produces a structured audit
  report with P0-P2 severity. Supports cross-platform version comparison and
  regression gold-set re-runs. Only audits facts and sources — does not edit
  style or argument structure.
description_zh: 审稿核验器
description_en: Claim-to-Source Auditor
not_for:
  - Plagiarism or originality-detection scans
  - Legal, regulatory, or localization compliance review (use a localization or compliance skill)
  - Rewriting style, tone, or argument structure
  - Formatting citations or bibliographies
agent_created: true
---

# Claim-to-Source Auditor

## When to use

Use this skill when the user wants to:

- Fact-check a long-form article, report, or analysis before publication.
- Verify that claims in a published piece still hold against current sources.
- Check whether the same facts are consistent across multiple platform versions of the same article.
- Audit academic citations, regulatory claims, financial numbers, internal data, or direct quotes.
- Build a regression gold set so future revisions can be checked for fact-regression.
- Validate that external incidents are attributed correctly across event facts, platform statements, and author judgments.

## Do not use

- For style editing, structure critique, or argument-strength assessment — this skill only audits factual claims and their source support.
- For cross-material wording/number consistency across sibling materials → use cross-material-consistency-auditor.
- For full pre-publish compliance review of a marketing draft → use a dedicated compliance-review skill if one is installed.

## Architecture

Default to a fixed workflow running in shadow mode — read output, compare to sources, produce an audit table. Do not modify the source article unless the user explicitly asks for revision. Always separate audit from editing.

Target: 30–50 high-risk claims per article batch. High-risk means: specific numbers, dates, percentages, dollar amounts, regulatory conclusions, named individuals, institution affiliations, direct quotes, paper details, and incident attributions.

## Evidence hierarchy

Assign every source used to one of three levels:

| Level | Definition | Examples |
|---|---|---|
| L0 primary | Original, verifiable, unfiltered | Court judgments, official regulatory text, company filings, raw operational logs, author's original social-media post, arXiv pre-print |
| L1 reliable secondary | Trusted reporting with named sources | Bloomberg, Reuters, The Register, Fortune, a peer-reviewed journal article with a DOI |
| L2 supplementary | Indirect or unverified | Aggregated media summaries, a research archive that cites but does not quote the original, an LLM-generated summary of a paper |

- A claim can pass only when supported by L0 or L1.
- L2 can support partial-pass or help explain a gap; it cannot make a claim pass on its own.
- If L0 and L1 disagree, surface both and flag the conflict.

## Workflow

### Step 1: [LLM] Extract high-risk claims

Read the article body and extract every claim that falls into one or more of these categories:

1. Specific numbers or percentages.
2. Dates, time ranges, and timelines.
3. Direct quotes attributed to a named person.
4. Dollar, euro, or other currency amounts.
5. Regulatory conclusions.
6. Academic paper details.
7. Named institutions, roles, or affiliations.
8. Incident summaries that assign cause or blame.

For each claim, record: claim text, category, line or section reference, and whether it is a fact or the author's own judgment.

### Step 2: [Deterministic] Collect available evidence

For each claim, identify available local sources: research databases, internal operational logs, prior fact-check reports, and clean gold-set records from earlier audits.

For claims requiring external verification, search for: official judgments, company announcements, regulatory texts, original social-media posts, and trusted media reports.

### Step 3: [LLM] Classify each claim

Assign one of five statuses:

| Status | Criteria |
|---|---|
| 通过 | L0 or L1 source directly supports the exact claim as written |
| 部分支持 | Core event or number exists, but the text overstates scope, causation, precision, or legal meaning |
| 缺证 | No L0 or L1 source found; only L2 or no source at all |
| 错误 | L0 or L1 source directly contradicts the claim |
| 判断 | Reasonable author analysis that no single source can prove or disprove |

Assign a severity:

- P0: must be corrected before next publication (wrong author, wrong number, fabricated or uncitable quote, wrong regulatory claim).
- P1: should be tightened or sourced (overstated scope, missing attribution, imprecise date or currency, inference presented as fact).
- P2: acceptable as-is with minor sourcing notes.

### Step 4: [LLM] Cross-platform verification

When the same article exists in multiple languages or platforms, check every high-risk claim across all versions:

- Are numbers, dates, and people's names identical?
- Are source annotations present in every version?
- Are regulatory conclusions translated without adding or losing meaning?

Mark each item as 一致, 近似, 偏差, or 错误.

### Step 5: [LLM] Separate layers in incident attribution

When an article describes a real-world incident, split it into three layers:

1. What is agreed to have happened.
2. How the platform or parties involved described it.
3. How the author interprets it.

Only layer 1 can pass as a verified fact. Layers 2 and 3 cannot be written as if they are the same thing.

### Step 6: [Deterministic] Save a regression gold set

After every audit, save the claim list and verdicts as a CSV. When the article is revised, re-run the same claims to check for regression. A gold-set item that was previously 通过 and now fails counts as a regression event.

### Step 7: [LLM] Produce the audit report

Output a structured report containing:

- Article name, platform, and audit date.
- Summary counts: total claims, 通过, 部分支持, 缺证, 错误, 判断 by severity.
- P0 list with required corrections.
- Cross-platform comparison (if applicable).
- Regression check against any prior gold set.
- Source register with URLs.

## Hard rules

1. Only L0 or L1 sources can make a claim pass. L2 is supplementary only.
2. Papers, court judgments, and regulatory texts must never be silently altered. Mark any paraphrase, translation, or correction explicitly. Never present a paraphrase as a direct quotation.
3. Published articles may be revised directly when the user accepts a change. Every change to a paper citation, judgment, or regulatory reference must carry an annotation.
4. Separate event facts, platform/party attributions, and author interpretation — do not compress them into a single sentence.
5. Synthesized numbers (totals, percentages, ratios computed from sources) must show their arithmetic; a computed claim presented without its inputs is treated as unsourced and fails.
6. Regulatory materials define jurisdiction-specific requirements. Do not compress them into universal prohibitions.
7. A prior fact-check report is a regression oracle, not proof that the current version is clean. Compare every historical P0/P1 item against the current text.
8. The default for any claim without a verifiable source is 缺证, not 通过.
9. Never invent evidence to fill a gap. If a source cannot be found, report it as a gap.

## Pitfalls

- Vendor conference recap and product education articles require a separate genre check. Treat the official event page as evidence for the event, speaker, title, and published agenda only; treat detailed architecture, customer outcomes, internal adoption counts, and implementation metrics as vendor/talk claims unless the original slides, recording, logs, or independent source are available.
- A vendor's internal benchmark can pass as an accurately reported vendor result, but it cannot pass as independent evidence of category-wide superiority. Preserve task source, environment scope, benchmark conditions, competitor identity, judge design, and replication status.
- Do not infer that a local file is unpublished merely because the folder is named `drafts`. The user, a CMS record, or a publication log is authoritative.
- A direct quote in an article that cannot be found in the reported source is a P0, even if the surrounding story is true.
- Near-miss numbers are still mismatches. An audit that reports 5810 when the source says 5817 must flag the difference.
- Cross-platform periods are high-risk. If one version reads "2024" and the other "2025", the different year is an error, not a paraphrase.
- Regulatory documents exist in specific jurisdictions. Never write "FDA, EU MDR, and China's regulations all say the same thing" without checking the governing text.

## Failure handling

| Scenario | Action |
|---|---|
| Source is behind a paywall or blocked | Mark the claim as 缺证; note the source is unavailable |
| Source URL is dead (404) or only an archived snapshot exists | Mark as 缺证 unless a retrievable archived snapshot with its own access date can be cited as the source; note link rot and do not treat the live URL as L0/L1 evidence |
| Primary source and secondary source disagree | Surface both with verbatim quotes; flag the conflict |
| Claim involves a future prediction | Mark as 判断; do not treat it as a fact |
| Foreign-language regulatory text | Use an official translation if available; otherwise mark as 部分支持 and flag language limitation |
| Internal operational log unavailable | Mark the claim as 部分支持; note which specific log is missing |
| Previously verified claim now fails | Flag as gold-set regression; escalate to P0 review |

## Verification

Before delivering, verify:

- Every P0 has a specific source that contradicts or fails to support the claim.
- The cross-platform audit table covers the same claims on every platform.
- The gold-set CSV loads cleanly and has the same number of rows as the current audit.
- Paper authors, journal names, case numbers, and years are checked against the original source, not against an intermediary archive.
- The audit report states which claims could not be verified and why.

## Output format

1. **Audit-problems CSV**: one row per claim, columns for claim-id, article, claim-text, status, severity, evidence-summary, and required-action.
2. **Audit report**: structured Markdown containing the summary table, P0 list, P1 summary, cross-platform comparison, regression check, source register, and final pass/fail/conditional decision.
3. **Gold-set CSV** (optional, for regression): one row per claim with the verdict from the most recent audit.

Lead with the decision, then evidence, boundaries, and next-stage actions.
