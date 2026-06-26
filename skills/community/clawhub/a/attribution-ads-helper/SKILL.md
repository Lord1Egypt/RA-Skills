---
name: attribution-ads-helper
description: Build cross-channel attribution analysis and decision guidance for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic campaigns.
---

# Attribution Helper

## Purpose
Core mission:
- Diagnose attribution discrepancies across channels.
- Compare attribution window assumptions and their budget impact.
- Build practical attribution decision framework for optimization.
- Produce actionable attribution-aligned allocation guidance.

## When To Trigger
Use this skill when the user asks for:
- attribution model comparison
- conflicting ROAS/CAC by channel
- budget decisions under attribution uncertainty
- tracking and model interpretation support

High-signal keywords:
- attribution, tracking, model, predict
- roas, cpa, revenue, allocation, budget
- meta, googleads, tiktokads, youtubeads, dsp

## Input Contract
Required:
- channel_metrics_by_window
- attribution_windows
- conversion_event_definitions
- decision_context

Optional:
- offline_conversion_data
- holdout_or_incrementality_data
- MMM_or_ltv_inputs
- confidence_threshold

## Output Contract
1. Attribution Mismatch Map
2. Window Sensitivity Analysis
3. Decision-safe KPI View
4. Budget Reallocation Recommendation
5. Validation Experiment Plan

## Workflow
1. Normalize event and conversion definitions.
2. Compare performance under each attribution window.
3. Quantify decision deltas from model differences.
4. Propose allocation with confidence labeling.
5. Output validation experiments for unresolved gaps.

## Decision Rules
- If attribution views diverge materially, use blended guardrail plan.
- If one channel is highly view-through sensitive, reduce reliance on last-touch only.
- If incremental evidence exists, prioritize it over proxy metrics.
- If uncertainty remains high, allocate budget in capped test tranches.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Keep window comparisons explicit per channel.
- Separate platform-reported and unified-attribution decisions.

## Constraints And Guardrails
- Never mix inconsistent conversion definitions in one conclusion.
- Flag time-lag effects for high-consideration products.
- Avoid binary conclusions when model variance is large.

## Failure Handling And Escalation
- If event taxonomy is inconsistent, output normalization checklist first.
- If offline conversion pipeline is unavailable, mark blind spots and conservative policy.
- If budget decision is high-stakes, require experiment-backed confirmation.

## Code Examples
### Window Comparison Table

    channel: Meta
    roas_1d_click: 1.9
    roas_7d_click: 2.6
    delta_pct: 36.8

### Allocation Rule Under Uncertainty

    if attribution_variance_pct > 25:
      budget_mode: guarded
      max_shift_pct: 10

## Examples
### Example 1: 1d vs 7d dispute
Input:
- Team split on attribution window

Output focus:
- sensitivity table
- decision-safe policy
- validation plan

### Example 2: Channel reallocation decision
Input:
- Meta and Google show conflicting contribution

Output focus:
- mismatch diagnosis
- allocation options
- risk labels

### Example 3: Incrementality integration
Input:
- Holdout test data available

Output focus:
- model reconciliation
- updated budget recommendation
- confidence update

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
