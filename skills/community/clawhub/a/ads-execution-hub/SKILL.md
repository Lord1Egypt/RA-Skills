---
name: ads-execution-hub
description: Ads Execution Hub control skill for ad campaign management and optimization across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic.
---

# Ads Execution Hub

## Purpose
Core mission:
- Serve as the dedicated ad operations and optimization interface.
- Manage planning, launch, monitoring, and scaling across ad channels.
- Standardize decision policies for bidding, budget, and performance recovery.
- Output clear operator actions for media teams.

## When To Trigger
Use this skill when the user asks for:
- campaign setup, optimization, or scaling in one or more channels
- budget and bidding decision support with performance constraints
- anomaly diagnosis and recovery actions for live campaigns
- cross-channel media operation playbooks

High-signal keywords:
- ads execution hub, run ads, campaign, media buyer
- bidding, budget, allocation, optimize, scale
- cpa, roas, performance, monitor, abtest

## Input Contract
Required:
- campaign_objective
- channel_scope
- budget_constraints
- recent_performance_snapshot

Optional:
- creative_state
- audience_state
- tracking_health
- policy_or_account_flags

## Output Contract
1. Campaign Action Plan
2. Bidding and Budget Policy
3. AB Test and Scale Model
4. Monitoring and Alert Plan
5. Operator Handoff Checklist

## Workflow
1. Normalize objective and KPI constraints.
2. Evaluate channel readiness and structure quality.
3. Produce bid and allocation actions.
4. Attach testing and scaling rules.
5. Return monitoring triggers and operator checklist.

## Decision Rules
- If measurement confidence is low, limit scale and improve tracking first.
- If ROAS is stable above threshold, allow staged budget increases.
- If CPA is unstable, reduce concurrency of experiments.
- If anomaly risk is high, prefer containment actions first.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Keep channel recommendations execution-specific and auditable.
- Align bid logic with each platform's optimization mechanics.

## Constraints And Guardrails
- No irreversible changes without rollback conditions.
- Keep every recommendation tied to KPI impact.
- Respect policy and account health constraints.

## Failure Handling And Escalation
- If required platform data is missing, return minimum data request list.
- If policy or account block appears, route to compliance/account helper.
- If spend risk is severe, trigger emergency control mode.

## Code Examples
### Campaign Control Spec

    objective: improve_roas
    channels: [Meta, GoogleAds, TikTokAds]
    budget_mode: staged_scale
    cpa_ceiling: 42
    roas_floor: 2.5

### Alert Trigger Rule

    if roas_drop_pct > 20 and spend_up_pct > 25:
      severity: high
      action: cap_budget_and_notify

## Examples
### Example 1: Launch and stabilize
Input:
- New campaign across Meta and TikTok Ads

Output focus:
- launch checklist
- first-week controls
- fallback rules

### Example 2: Scale after validation
Input:
- Stable ROAS for 10 days

Output focus:
- scale ladder
- bid policy updates
- monitoring checkpoints

### Example 3: Cross-channel anomaly
Input:
- Spend surge, mixed conversion signals

Output focus:
- anomaly triage
- containment actions
- next validation steps

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
