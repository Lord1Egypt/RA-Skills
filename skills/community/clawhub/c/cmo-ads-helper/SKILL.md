---
name: cmo-ads-helper
description: Support CMO-level planning across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic with revenue, profit, cashflow, ROAS, and LTV strategy modeling.
---

# CMO Helper

## Purpose
Core mission:
- Parse top-level business goals (revenue, profit, cashflow) into executable growth paths.
- Simulate budget allocation and channel structure with ROAS and LTV forecasts.
- Produce quarterly and annual growth strategy with risk alerts.
- Generate board-ready growth reports.

## When To Trigger
Use this skill when the user asks for:
- annual or quarterly growth planning
- high-level budget allocation by channel
- ROAS/LTV forecast and risk evaluation
- CMO report narratives for leadership updates

High-signal keywords:
- growth, revenue, profit, roi, roas, ltv
- ads, media, campaign, forecast, model, allocation
- strategy, budget, dashboard, report, predict

## Input Contract
Required:
- business_targets: revenue_target, profit_target, cashflow_target
- planning_horizon: quarter or year
- budget_pool: total budget and flexibility range
- current_mix: channel spend and KPI baseline

Optional:
- market_constraints
- hiring_or_resource_limits
- inventory_or_supply_constraints
- risk_tolerance

## Output Contract
1. Executive Goal Decomposition
2. Growth Path by Quarter (or month)
3. Channel Allocation Simulation (base/upside/downside)
4. ROAS/LTV Forecast Assumptions and outputs
5. Risk Radar and Mitigation Plan
6. CMO Report Outline

## Workflow
1. Normalize top goals into quantifiable KPI tree.
2. Build growth path candidates by objective priority.
3. Simulate channel budget structure under multiple scenarios.
4. Forecast ROAS and LTV under attribution assumptions.
5. Flag risks and attach mitigation owners.
6. Export leadership-ready summary.

## Decision Rules
- If cashflow is constrained, prioritize payback speed over max scale.
- If profit target conflicts with growth target, optimize blended margin first.
- If uncertainty is high, widen confidence ranges and use staged budget release.
- If one channel dominates risk, cap exposure and add redundancy channels.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Meta/TikTok: fast learning via creative breadth.
- Google/Amazon: demand-capture and intent-driven efficiency.
- DSP: incremental reach and controlled frequency.

## Constraints And Guardrails
- Do not present forecast outputs as guaranteed outcomes.
- Separate assumptions, historical facts, and modeled estimates.
- Keep all recommendations linked to measurable KPI deltas.

## Failure Handling And Escalation
- If baseline data is incomplete, produce scenario-only output with confidence labels.
- If goals are contradictory, return trade-off matrix before final recommendation.
- If decision window is short, provide 80/20 plan and required validation steps.

## Code Examples
### Quarterly Growth Model (YAML)

    horizon: Q3-2026
    targets:
      revenue: 2500000
      profit: 620000
      cashflow: positive
    channels:
      Meta: 0.35
      GoogleAds: 0.30
      TikTokAds: 0.15
      AmazonAds: 0.10
      DSP: 0.10

### Forecast Table Schema (JSON)

    {
      "scenario": "base",
      "blended_roas": 2.9,
      "projected_ltv": 145,
      "risk_level": "medium"
    }

## Examples
### Example 1: Quarterly board plan
Input:
- Need Q3 growth plan with profit floor

Output focus:
- channel budget simulation
- risk warnings
- executive summary points

### Example 2: Annual strategy reset
Input:
- Revenue target increased by 40%
- Cashflow pressure exists

Output focus:
- staged growth roadmap
- payback-sensitive allocation
- guardrails

### Example 3: Budget cut scenario
Input:
- Spend reduced by 20%
- KPI targets unchanged

Output focus:
- re-prioritization logic
- expected trade-offs
- mitigation actions

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
