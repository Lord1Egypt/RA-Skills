---
name: powermatrix-geo-growth-orchestrator
description: Unified GEO growth workflow for brand knowledge base building, LLM visibility audits, Doubao/DeepSeek readiness review, AI-GEO content asset generation, platform draft planning for Zhihu/Toutiao/CSDN/Juejin, client delivery reports, internal QA, and 7/14/30 day retests. Use when Codex needs to analyze or improve a brand's AI search visibility, generate GEO reports, diagnose model mentions/citations/rankings, create GEO-friendly content tasks, or consolidate GEO platform workflows into one human-reviewed delivery package.
---

# PowerMatrix GEO Growth Orchestrator

This skill is now the unified GEO workflow. It can run as one self-contained skill instead of requiring separate Doubao audit, DeepSeek audit, AI-GEO content, and platform draft skills.

Use the old neighboring skills only as optional references when the user explicitly asks to inspect or preserve their original behavior. Do not require the user to understand or invoke multiple GEO skills.

## Core Promise

Turn brand materials into a human-reviewed GEO delivery package:

1. Resolve the brand entity and aliases.
2. Build or validate the brand knowledge base.
3. Plan and record LLM probes for Doubao, DeepSeek, generic LLMs, or user-provided model answers.
4. Score visibility, mentions, citations, ranking position, answer quality, factual accuracy, localization, and conversion usefulness.
5. Identify content gaps and commercial impact.
6. Generate GEO-friendly content tasks and reusable content assets.
7. Adapt tasks for Zhihu, Toutiao, CSDN, Juejin, Xiaohongshu, Douyin, or manual publishing.
8. Produce client-facing and internal QA reports.
9. Create a 7 / 14 / 30 day retest plan.

## Required First Moves

1. Identify the task type:
   - `audit_only`: visibility diagnosis and report.
   - `content_only`: content assets and platform drafts.
   - `full_workflow`: audit, gap analysis, assets, drafts, delivery report, retest plan.
   - `debug_existing_report`: investigate mismatch between model output and report.
2. Normalize the brand entity:
   - Extract `brand_name`.
   - Extract `company_name` if present.
   - Build `brand_aliases`, including abbreviations, city + brand, brand + service, legal name, common short name, old names, pinyin/English names, and likely spelling variants.
   - Keep category keywords separate from brand aliases.
3. Decide evidence level before making claims:
   - `verified_live_check`: live model/API/platform check with query, answer, time, and raw evidence.
   - `manual_check`: user-provided screenshot, copied answer, or manual summary with time/source.
   - `inferred_estimate`: reasoning from brand materials only.
   - `unverified_assumption`: weak assumption for planning only.
4. If there is no live or manual evidence, do not state rankings, scores, model citations, or "not mentioned" as fact. Output a check plan or mark findings as inferred.

## Inputs

Minimum natural-language input is acceptable. Prefer structured fields when available:

| Field | Use |
|---|---|
| `brand_materials` | Company intro, website text, product/service details, FAQ, cases, channels, compliance notes |
| `brand_name` | Primary brand/entity name |
| `brand_aliases` | Known short names, alternate names, source titles, common model spellings |
| `target_keywords` | Category and decision keywords; do not treat these as brand aliases |
| `target_models` | `doubao`, `deepseek`, `generic`, `chatgpt`, `perplexity`, `other` |
| `target_platforms` | `zhihu`, `toutiao`, `csdn`, `juejin`, `xiaohongshu`, `douyin`, `website` |
| `existing_geo_report` | Prior report, copied model answers, screenshots, source lists, citation ranks, score JSON |
| `mock_model_outputs` | User-provided or demo model answers for scoring; must not be presented as live evidence |
| `campaign_goal` | Audit, visibility improvement, content generation, lead generation, retest |
| `compliance_constraints` | Forbidden claims, industry limits, required disclaimers |

## Resource Routing

Load only the reference needed for the current task:

- Read `references/entity-evidence-rules.md` when diagnosing mention/citation/ranking mismatches, using model answers, scoring audits, or handling aliases.
- Read `references/geo-unified-modules.md` when running the full workflow or generating stage outputs.
- Read `references/platform-style-guide.md` when creating platform-specific drafts or content task plans.

Scripts and schemas:

- Use `scripts/generate_full_report.py` for dual-model report generation from structured input.
- Use `scripts/generate_client_report.py` and `scripts/generate_internal_report.py` when assembling client/internal reports from artifacts.
- Use schemas in `schemas/` and `templates/` to keep outputs consistent.

## Unified Workflow

### Stage 0: Intake

Capture brand, business category, target market, keywords, target models, target platforms, goal, constraints, and available evidence. If the brand has multiple names, create aliases before scoring.

### Stage 1: Brand Knowledge Base

Build a compact knowledge base with:

- brand definition
- products/services
- target customers
- scenarios
- selling points and evidence level
- FAQ
- channels/contact
- compliance boundary
- missing fields

Mark unknown facts as `待确认`. Never invent prices, locations, cases, certificates, rankings, or third-party endorsements.

### Stage 2: GEO Visibility Audit

Use natural, non-leading probes covering:

- spontaneous recommendation
- competitor comparison
- buying guide
- direct awareness
- price and channel
- localized consumption/use case
- platform seeding context
- local supply chain / authority / regional market

For each answer, separate:

- `answer_mention`: target entity appears in the answer body.
- `citation_mention`: target entity appears in citation/source/title/link.
- `source_rank`: target entity's rank in source/citation list.
- `brand_alias_hits`: matched aliases.
- `category_keyword_hits`: category terms only.
- `competitor_mentions`: alternatives or competitors.
- `evidence_level`: verified/manual/inferred/unverified.

Do not collapse citation rank into answer mention. Do not count category keywords as brand mentions.

### Stage 3: Gap Matrix

Convert audit results into gaps. Each gap must include scenario, involved model, evidence source, business impact, priority, and remediation action.

### Stage 4: Content Task Plan

Turn gaps into concrete tasks with platform, title, target keyword, target user, intended role, source gap, brand points to include, fact dependencies, compliance notes, and review status.

### Stage 5: GEO Content Assets

Generate reusable assets from the brand knowledge base:

- website FAQ
- `llms.txt`
- quote sentence library
- comparison explainer
- buying guide
- platform seed articles

All content must be factual, structured, low-hype, and explicit about boundaries.

### Stage 6: Platform Drafts

Route by platform:

- Zhihu: question-first, analytical, low-ad, balanced.
- Toutiao: plain-language, scenario-driven, boss-readable or consumer-readable.
- CSDN: technical tutorial, architecture, implementation, troubleshooting.
- Juejin: developer practice, engineering lessons, code/prompt examples.
- Xiaohongshu/Douyin: manual brief, visual/script outline, no automated posting.
- Website: FAQ, glossary, service page, comparison page.

Never auto-publish. Human review is mandatory.

### Stage 7: Reports

Default output mode is `full_report`. Unless the user explicitly asks for summary only, output the complete Markdown report body in the conversation and save artifacts when working locally.

The report must include:

1. Boss-readable 3 sentence conclusion.
2. Evidence level and what was actually checked.
3. Skill/module execution status.
4. Model scores and per-probe results when evidence supports scoring.
5. Mention/citation/rank breakdown.
6. Core GEO gaps and commercial impact.
7. Content assets and platform tasks.
8. 30 day action plan.
9. 7 / 14 / 30 day retest mechanism.
10. File list and missing information.

### Stage 8: Internal QA

Keep internal details out of the client report but preserve them in internal QA:

- missing artifacts
- evidence downgrade reasons
- raw answer paths
- API/tool availability
- schema validation
- compliance risks
- blocked publishing items

## Safety And Compliance

- Do not promise ranking, traffic, conversion, indexing, or model citation.
- Do not present mock/demo outputs as live model checks.
- Do not claim "not mentioned" if the raw answer or citation list was not checked.
- Do not use unauthorized accounts, credentials, cookies, or platform automation.
- Do not click publish buttons or perform engagement actions.
- For medical, legal, financial, education compliance, safety, or regulated claims, require human/professional review.

## Debugging Known Failure Modes

When a user reports "model shows us but the report says not mentioned":

1. Ask for or inspect the raw model answer, citation/source list, screenshot, copied sources, and report artifact.
2. Compare `brand_name` against `brand_aliases`.
3. Check whether the brand appeared in answer body, source title, source URL, or citation rank.
4. Check whether the report counted only exact full-name matches.
5. Check whether target keywords were mixed into brand mention scoring.
6. Correct the report by separating body mention, citation mention, source rank, and category keyword hits.

For local service brands, always expect name variants such as `city + brand`, `brand + service`, `brand + school/company`, and short brand names.
