---
name: CFCRM Build
slug: cfcrm-build
author: Meghan Gamma (for SuccessBrian Ecosystem)
source: https://contactflowcrm.com
description: Multi-version build plan for ContactFlowCRM (CFCRM). Guides agents through v1→v5 phased development with deliverables, checklists, and success criteria per version. Activate when building, reviewing, or planning CFCRM development.
version: 1.0.0
license: MIT
metadata: {"openclaw":{"emoji":"🏗️","requires":{"env":[],"bins":[]},"primaryEnv":""}}
---

# CFCRM Build — Multi-Version Roadmap

## When to Activate

Activate this skill when the user or an agent:
- Asks about CFCRM build status or next steps
- Needs to understand what to build in each version
- Wants to check off completed items against a version checklist
- Plans development sprints for ContactFlowCRM
- Asks "what version is CFCRM at?" or "what's next for CFCRM"
- Reviews CFCRM progress across the ecosystem

**Keywords (25+):** cfcrm, contactflowcrm, build plan, roadmap, v1, v2, v3, v4, v5, version, phase, mvp, launch, development, sprint, milestone, build status, what's next, go to market, ship, deliverables, checklist, alpha, beta, release, contactflow, crm build

## First Interaction

> **🏗️ CFCRM Build Planner**
>
> ContactFlowCRM v1 through v5 roadmap is loaded. Current version tracking, deliverables, and ship checklists are available.
>
> **Commands:**
> - `/cfcrm-build status` — Overall build progress (all versions)
> - `/cfcrm-build plan [v1|v2|v3|v4|v5]` — Detailed plan
> - `/cfcrm-build checklist [v1|v2|v3|v4|v5]` — Launch checklist
> - `/cfcrm-build next` — What to build right now
> - `/cfcrm-build summary` — One-page roadmap overview
>
> Which version are we working on?

## Version Architecture

```
v1 (Foundation) → v2 (Smart Nurture) → v3 (Monetization) → v4 (Intelligence) → v5 (Scale)
```

Each version requires the previous. No staging features in earlier versions.

## Commands

### `/cfcrm-build status`

Show current build progress across all 5 versions.

1. Check for persisted status in ecosystem_knowledge on Alpha (search: `cfcrm-build-*`).
2. If no data, assume v1 pre-launch state.
3. Show progress table with estimated completion per version.
4. Recommend next action.

### `/cfcrm-build plan [v1|v2|v3|v4|v5]`

Detailed build plan for a version.

1. If no version specified, prompt user.
2. Display: theme, prerequisites, deliverables table, technical notes, effort estimate.
3. For deliverable details, reference the CFCRM knowledge base.

### `/cfcrm-build checklist [v1|v2|v3|v4|v5]`

Ship checklist for a version.

1. Show all deliverables as checkboxes.
2. Ask user if any can be marked complete.
3. If all green, suggest moving to next version.
4. Persist completion to ecosystem_knowledge.

### `/cfcrm-build next`

Single next action.

1. Find first uncompleted deliverable in current version.
2. Present as clear actionable task with reason and reference.

### `/cfcrm-build summary`

Condensed one-page roadmap (all 5 versions, 50 lines max).

## Version Plans

### v1 — Foundation (MVP)

**Theme:** Functional CRM that captures leads, manages contacts, tracks logins, and integrates with Systeme.io.

| ID | Deliverable | Notes | Effort |
|----|------------|-------|--------|
| V1-01 | Contact CRUD | Name, email, WhatsApp, source, status | Medium |
| V1-02 | 9-digit Hex UID generation | Collision-free, # prefix handling | Low |
| V1-03 | Full-text search | Name, email, phone -> 200ms | Low |
| V1-04 | CSV import + field mapping | 5k+ rows | Medium |
| V1-05 | Fuzzy deduplication | Email/phone match, flag | Medium |
| V1-06 | Auth + login/logout tracking | RLS, cfcrm_user_logins/logouts | Medium |
| V1-07 | Webhook receiver | POST, UTM parse | Medium |
| V1-08 | Systeme.io sync | Bidirectional | Medium |
| V1-09 | Basic dashboard | Contact count, lead flow | Low |
| V1-10 | Mobile-responsive UI | React + Tailwind | Medium |

**Total: ~3-4 weeks**

### v2 — Smart Nurture

**Theme:** Know when to reach out and when to cool off. Deliverability protection + conversion timing.

| ID | Deliverable | Notes | Effort |
|----|------------|-------|--------|
| V2-01 | Trust-Velocity scoring (0-100) | Touch engagement + time | High |
| V2-02 | Cooling Protocol (3-stage) | Active/Cool/Dormant | Medium |
| V2-03 | Resurrection trigger | SmartLink/DM reactivates | Low |
| V2-04 | Webhook retry with backoff | 3 retries -> dead letter | Medium |
| V2-05 | UTM parsing + storage | All params | Low |
| V2-06 | Lead source analytics | Dashboard | Medium |

**Total: ~2-3 weeks**

### v3 — Monetization

**Theme:** Ecosystem participants earn. Pro-Coach, cross-sell, bookings.

| ID | Deliverable | Notes | Effort |
|----|------------|-------|--------|
| V3-01 | Pro-Coach 75-day sprint | Cohorts, uploads, approvals | High |
| V3-02 | Paid coaching unlock | 90% rating threshold | Medium |
| V3-03 | Revenue split engine | 70/30 coach/platform | Medium |
| V3-04 | Booking Hub via webhooks | TidyCal/Calendly | High |
| V3-05 | Got Backup cross-sell trigger | Auto at trust threshold | Low |
| V3-06 | Tier flags in contact profile | Track tier membership | Low |

**Total: ~4 weeks**

### v4 — Intelligence

**Theme:** Full cross-channel visibility. WhatsApp logging, Hotness Index, enrichment.

| ID | Deliverable | Notes | Effort |
|----|------------|-------|--------|
| V4-01 | Cross-channel touch tracking | Email, SMS, WhatsApp, DM | High |
| V4-02 | WhatsApp Habit Logging | NLP parse -> streak | High |
| V4-03 | Hotness Index (0-100) | Zoom/Video/1-on-1 exposure | Medium |
| V4-04 | Enrichment credits system | 50/100/500 per tier | Medium |
| V4-05 | Social Reach Aggregator | Multi-platform followers | Medium |

**Total: ~3-4 weeks**

### v5 — Scale

**Theme:** Performance, multi-tenant isolation, API docs, marketplace.

| ID | Deliverable | Notes | Effort |
|----|------------|-------|--------|
| V5-01 | Materialized Views | 15-min refresh, aggregate only | High |
| V5-02 | RLS audit + hardening | Cross-tenant isolation | Medium |
| V5-03 | OpenAPI documentation | Auto-generated | Low |
| V5-04 | Performance optimization | Sub-500ms queries | Medium |
| V5-05 | Elite Creator Marketplace | Course creation + 50/30/20 split | High |
| V5-06 | Data enrichment API | Credits-based | Medium |

**Total: ~4 weeks**

## Guardrails

1. **Never build v2 before v1** — Strict version dependency
2. **Never build v4 features in v1** — Discipline on scope
3. **P0 items must ship** — No launch without all P0 green
4. **Confirm production testing** before marking complete
5. **Fixed version boundaries** — Not negotiable without full plan redesign
6. **No secrets in code** — Use {{ env.VAR_NAME }}

## Failure Handling

1. Unknown version: show `/cfcrm-build plan` help
2. Missing data: assume v1 default state
3. Unrecognized command: list available
4. Conflicting status: prefer ecosystem_knowledge, ask user if stale

## Example Prompts

1. "What's the current CFCRM build status?"
2. "Show me the v1 launch checklist"
3. "What do I need to build next?"
4. "Can we build Elite Marketplace now?" -> "That's v5. Check v1 first."
5. "One-page roadmap" -> runs summary
6. "Mark V1-03 complete"
7. "What version includes WhatsApp logging?" -> "v4"
