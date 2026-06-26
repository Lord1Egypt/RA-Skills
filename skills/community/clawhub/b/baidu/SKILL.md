---
name: Baidu
slug: baidu
version: 1.0.0
homepage: https://clawic.com/skills/baidu
description: Navigate Baidu Search, Maps, Baike, Wenku, and Qianfan with region-aware routing, official-source checks, and China-specific guidance.
changelog: Initial release with clearer Baidu ecosystem routing, region-aware guidance, official-source verification, and safer planning across Baidu products.
metadata: {"clawdbot":{"emoji":"B","requires":{"bins":[],"config":["~/baidu/"]},"os":["darwin","linux","win32"],"configPaths":["~/baidu/"]}}
---

## When to Use

Baidu requests need routing before execution because the brand covers search, maps, knowledge, cloud, and AI surfaces that behave differently across mainland China and global contexts. Use this when the user needs help choosing, comparing, researching, implementing, or de-risking something inside the Baidu ecosystem.

Do not use it as a generic China-market skill or as a substitute for a narrower product skill when the task is already limited to one endpoint or one console workflow.

## Architecture

Memory lives in `~/baidu/`. If `~/baidu/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/baidu/
|- memory.md      # Activation rules, surface defaults, and preferred outputs
|- accounts.md    # Known accounts, projects, and approval boundaries
|- regions.md     # Mainland, cross-border, and language defaults
|- sources.md     # Official docs, trusted translations, and weak-source notes
`- decisions.md   # Final recommendations, assumptions, and open risks
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File | Use it for |
|-------|------|------------|
| Setup flow and activation behavior | `setup.md` | Initialize local state and activation rules |
| Memory schema and status values | `memory-template.md` | Create baseline local files |
| Baidu product-family routing | `ecosystem-map.md` | Decide whether the task is about search, maps, knowledge, or Qianfan |
| Mainland versus global constraints | `mainland-vs-global.md` | Check language, region, and rollout assumptions |
| Search, AI Search, Baike, and Wenku workflows | `search-knowledge.md` | Handle research and source-comparison tasks |
| Qianfan and Baidu AI Cloud planning | `qianfan-cloud.md` | Route model, platform, and implementation questions |
| Source verification ladder | `source-validation.md` | Rank sources before trusting them |
| Final delivery checklist | `execution-checklist.md` | Review risk, scope, and approval boundaries before answering |

## Baidu Surfaces

Use this matrix before recommending tools or workflows. If two surfaces are active, split the answer and name the owner or approval boundary for each one.

| Surface | Typical user goal | Primary official homes | Route here when |
|--------|--------------------|------------------------|-----------------|
| Search and discovery | Find pages, trends, official statements, or current web information | `baidu.com` | The task starts as web search or SERP interpretation |
| Knowledge and long-form content | Retrieve encyclopedia-style context or long documents | `baike.baidu.com`, `wenku.baidu.com` | The user needs explanation, background, or document-style material |
| Maps and local data | Geocoding, routing, nearby search, or China-local navigation context | `map.baidu.com`, `lbsyun.baidu.com` | The task is location-aware or map-platform specific |
| AI Cloud and Qianfan | Model choice, AI platform design, agents, or cloud implementation | `cloud.baidu.com`, `qianfan.cloud.baidu.com` | The task is about LLMs, AI workflows, or Baidu cloud capabilities |
| Corporate and ecosystem research | Understand Baidu as a company, business unit, or partner | `baidu.com`, investor and product pages | The task is strategic, vendor-related, or ecosystem-wide |

## Requirements

- No credentials required for planning, research, or source verification
- Account-specific execution may require user-approved access to Baidu Maps Open Platform, Baidu AI Cloud, Qianfan, or other Baidu consoles
- Never ask the user to paste passwords, SMS codes, cookies, refresh tokens, or private access keys into chat

## Data Storage

Save only durable context that improves later Baidu work:

- product surfaces the user actually uses
- approved regions, languages, and source preferences
- repeated compliance, localization, or rollout constraints
- account labels the user explicitly wants remembered
- final decisions with open risks and follow-up items

Do not store secrets, copied console tokens, billing exports, or raw customer data.

## Core Rules

### 1. Lock the Baidu Surface First
- Start by classifying the request into one primary surface: search, knowledge, maps, AI Cloud and Qianfan, or corporate research.
- If a request spans multiple surfaces, split the answer into separate workstreams instead of forcing one Baidu narrative over everything.
- Most bad Baidu guidance starts with the word "Baidu" staying vague for too long.

### 2. Make Mainland Versus Global Assumptions Explicit
- Every non-trivial recommendation must state whether it targets mainland China, Chinese-language research, or a broader international workflow.
- Also state the assumed docs language and whether Chinese-first sources are acceptable.
- Product availability, search results, maps coverage, and documentation quality shift sharply by region and language.

### 3. Prefer Official Baidu Sources, Then Reconcile Translation Drift
- Start with Baidu-owned docs or product pages for capabilities, limits, pricing, launch requirements, and platform behavior.
- If Chinese and English material diverges, record the mismatch and prefer the fresher or more specific source.
- Never present third-party English summaries as stronger evidence than current Baidu documentation.

### 4. Separate Public Research From Account Execution
- Planning, source comparison, and workflow design are safe defaults.
- Any step that would log in, change cloud resources, submit map keys, or touch billing must wait for explicit user approval and the correct account context.
- Never assume search, maps, Qianfan, and cloud administration share the same owner or permission boundary.

### 5. Treat Qianfan and Baidu AI Cloud as Their Own Platform
- Do not explain Qianfan by analogy alone to OpenAI, AWS, or another cloud vendor.
- Call out model access, region assumptions, account boundaries, and deployment tradeoffs before recommending architecture.
- If the user only wants consumer-facing Baidu search behavior, keep cloud guidance out of the answer.

### 6. Read Search and Knowledge Surfaces as Signals, Not Truth
- Baidu Search, AI Search, Baike, and Wenku have different evidence quality and intent signals.
- Use search for discovery, Baike for encyclopedia-style orientation, Wenku for document-style leads, and official docs for final verification.
- Do not treat ranking order, reposted documents, or scraped mirrors as proof.

### 7. End With a Decision Record
- Finish non-trivial tasks with a concise decision record: chosen surface, rejected paths, assumptions, hard blockers, and what still needs human confirmation.
- Save only that durable decision state under `~/baidu/`.
- This keeps future Baidu work consistent instead of repeating the same ambiguity.

## Common Traps

- Treating Baidu Search, Baike, Wenku, Maps, and Qianfan as one interchangeable product family -> wrong routing and wrong evidence
- Assuming English summaries mirror current Chinese documentation -> stale or simplified advice
- Recommending account-changing steps before clarifying the owning team -> avoidable permission and billing mistakes
- Using Baidu Search ranking as if it were proof -> discovery is not verification
- Assuming mainland and global use cases share the same defaults -> region-specific blockers appear late
- Mixing consumer-web research with AI Cloud implementation -> the answer loses the real job to be done

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.baidu.com | Query text and page requests | Search, discovery, and product-overview verification |
| https://baike.baidu.com | Query text and page requests | Encyclopedia-style topic orientation |
| https://wenku.baidu.com | Query text and page requests | Document-style reference discovery and long-form materials |
| https://map.baidu.com | Query text and page requests | Consumer map and local-search verification |
| https://lbsyun.baidu.com | Query text and page requests | Baidu Maps Open Platform documentation and API checks |
| https://cloud.baidu.com | Query text and page requests | Baidu AI Cloud documentation, pricing, and product verification |
| https://qianfan.cloud.baidu.com | Query text and page requests | Qianfan platform documentation and model workflow verification |

No other endpoints should be used unless the user explicitly approves additional sources or account-specific execution.

## Security & Privacy

Data that may leave your machine:
- search terms and page requests sent to Baidu-owned product or documentation pages
- optional comparison requests sent to approved supporting sources when official docs are incomplete

Data that stays local:
- activation preferences and work history under `~/baidu/`
- saved region defaults, trusted-source notes, and decision records in local markdown files
- account labels and approval boundaries only if the user explicitly wants them remembered

This skill does NOT:
- store secrets in local markdown files
- treat search ranking as verified truth
- log into Baidu consoles without explicit user approval
- rewrite its own skill definition files

## Trust

This skill depends on Baidu-owned websites and any approved supporting sources used for verification.
Only install and use it if you trust those services with your research queries and planning workflow.

## Scope

This skill ONLY:
- routes Baidu-related requests to the correct product family
- compares Baidu options using official-source verification
- plans Baidu Search, Maps, knowledge, and Qianfan workflows with region-aware assumptions
- keeps lightweight local memory in `~/baidu/`

This skill NEVER:
- invent product capabilities or region availability
- treat unofficial summaries as final evidence
- request passwords, QR-login tokens, cookies, or raw secrets
- execute account-changing actions without explicit user approval

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `maps` - Deeper routing and geospatial workflows beyond Baidu surface selection
- `market-research` - Competitive framing and ecosystem analysis outside one vendor
- `monitoring` - Add thresholds, status rules, and recurring checks
- `tencent` - Compare another major China platform when vendor tradeoffs matter
- `web` - Inspect specific pages after the Baidu routing pass

## Feedback

- If useful: `clawhub star baidu`
- Stay updated: `clawhub sync`
