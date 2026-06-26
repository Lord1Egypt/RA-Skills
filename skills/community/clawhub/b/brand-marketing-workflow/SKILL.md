---
name: brand-marketing-workflow
description: >
  Structural documentation for the brand-marketing-workflow skill. Use when the user wants to understand, audit, or review the workflow design without exposing implementation code.
---

# Brand Marketing Workflow — Structural Reference

## What This Skill Is
A documentation-only description of the brand marketing workflow. It explains the system architecture, roles, stages, boundaries, and outputs, but contains no executable code.

## Purpose
- Describe how brand inputs are turned into marketing plans
- Clarify the handoff between strategy, production, analysis, and review
- Define the human-approval boundaries for publishing, login, payment, or other sensitive actions
- Serve as a safe replacement artifact when the published skill should be withdrawn from active use

## Structure
### 1) Input Layer
- Brand name
- Positioning
- Tone
- Audience
- Goals
- Channels
- Constraints
- Competitor scope

### 2) Planning Layer
- Normalize brand input
- Build a concise brand brief
- Define content pillars
- Define channel mapping
- Define KPI targets

### 3) Production Layer
- Draft content variants
- Draft campaign ideas
- Draft platform-specific formats
- Prepare review-ready assets

### 4) Analysis Layer
- Compare public competitor signals
- Identify messaging patterns
- Identify content gaps
- Score brand fit and iteration opportunities

### 5) Authorization Layer
- Pause on actions that cross policy or access boundaries
- Request explicit human confirmation
- Resume only after approval

### 6) Output Layer
- Brand brief
- Content plan
- Competitor summary
- Performance review
- Iteration notes
- Approval requests when needed

## Boundaries
### Allowed
- Public information review
- Structural planning
- Draft generation
- High-level workflow explanation

### Not Allowed
- Hidden scraping
- Bypassing login or platform controls
- Automatic publishing
- Payment or recharge without approval
- Any misleading claim that implementation code still ships inside this replacement artifact

---

## Implementation Details

### Entry Point

`install.sh` bootstraps the skill and delegates to the Python runtime:

```bash
exec python3 scripts/run.py "$@"
```

Usage via OpenClaw:

```bash
oc_execute_skill brand-marketing-workflow --brand "品牌名"
oc_execute_skill brand-marketing-workflow --brand "BrandName" --channels "instagram,wechat"
```

### Scripts

| Script | Role |
|--------|------|
| `scripts/workflow_orchestrator.py` | Main entry point — orchestrates all stages in sequence |
| `scripts/competitor_fetcher.py` | Fetches public competitor signals (no auth required) |
| `scripts/competitor_ai_analyzer.py` | Analyzes competitor content patterns with LLM |
| `scripts/competitor_cluster.py` | Clusters competitors by positioning and messaging |
| `scripts/authorization_manager.py` | Gate for any action requiring human approval |
| `scripts/normalize_brand_input.py` | Normalizes and validates brand input parameters |
| `scripts/content_producer.py` | Drafts content variants per channel |
| `scripts/score_content_effect.py` | Scores content variants for brand fit |

### Output Templates

All outputs are written to `templates/`:

| File | Contents |
|------|---------|
| `brand_brief.md` | Brand positioning, tone, audience, pillars |
| `content_plan.md` | Channel-specific content calendar and format map |
| `competitor_report.md` | Competitor analysis with messaging gap matrix |
| `performance_report.md` | KPI targets and scoring baseline |
| `iteration_plan.md` | Next-cycle improvement suggestions |

### Authorization Gate

Any action that touches publishing, payment, platform login, or personal data pauses and calls `authorization_manager.py`, which:

1. Emits a clear approval request to the user
2. Blocks all downstream scripts until confirmation is received
3. Logs the approval decision with timestamp

No sensitive actions are taken automatically.
