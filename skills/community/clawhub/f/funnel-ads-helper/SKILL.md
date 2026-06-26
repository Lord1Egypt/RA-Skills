---
name: funnel-ads-helper
description: Diagnose and optimize full conversion funnels for paid traffic from Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and Shopify Ads campaigns.
---

# Funnel Helper

## Purpose
Core mission:
- Analyze conversion funnel drop-off by stage.
- Identify bottlenecks from ad click to checkout or lead submit.
- Recommend stage-specific optimization actions.
- Define funnel experiment roadmap and expected impact.

## When To Trigger
Use this skill when the user asks for:
- conversion funnel diagnosis
- CVR optimization planning
- landing page and checkout improvement sequence
- funnel experiment design tied to ROAS/CPA goals

High-signal keywords:
- conversion, funnel, checkout, cvr
- cpa, roas, traffic, landing page
- campaign, optimize, retarget

## Input Contract
Required:
- funnel_stage_metrics
- traffic_source_breakdown
- conversion_goal
- observation_window

Optional:
- session_replay_notes
- form_or_checkout_logs
- segment_breakdowns
- experiment_history

## Output Contract
1. Funnel Stage Health Scorecard
2. Bottleneck Priority Ranking
3. Optimization Actions by Stage
4. Experiment Roadmap with KPI impact
5. Monitoring and Iteration Rules

## Workflow
1. Normalize funnel definitions and stage metrics.
2. Rank drop-off severity and opportunity size.
3. Map root causes (message mismatch, UX friction, trust gap, etc.).
4. Recommend stage-specific actions and experiments.
5. Define monitoring thresholds and iteration cadence.

## Decision Rules
- If top-funnel CTR is strong but CVR is weak, prioritize LP and checkout fixes.
- If add-to-cart is strong but purchase is weak, prioritize trust/payment friction fixes.
- If retargeting conversion is low, review audience freshness and offer relevance.
- If funnel data is sparse, run diagnostic experiments before major redesign.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads

Platform behavior guidance:
- Keep funnel interpretation tied to traffic intent by channel.
- Distinguish ad-side and on-site bottlenecks before action.

## Constraints And Guardrails
- Do not infer funnel causes without stage-level evidence.
- Keep test queue prioritized by expected impact and effort.
- Avoid simultaneous high-impact changes that break attribution clarity.

## Failure Handling And Escalation
- If stage definitions are inconsistent, output a canonical funnel mapping first.
- If missing checkout data blocks diagnosis, request minimum event payload.
- If conversion drops sharply during active changes, trigger rollback review.

## Code Examples
### Funnel Health Schema

    stages:
      - impression_to_click
      - click_to_viewcontent
      - viewcontent_to_addtocart
      - addtocart_to_checkout
      - checkout_to_purchase
    primary_metric: stage_cvr

### Bottleneck Prioritization Rule

    impact_score = dropoff_pct * traffic_volume * margin_weight
    sort_by: impact_score_desc

## Examples
### Example 1: CVR collapse
Input:
- Click volume stable, purchases down

Output focus:
- stage bottleneck map
- immediate fixes
- monitor plan

### Example 2: Checkout friction
Input:
- Add-to-cart high, checkout completion low

Output focus:
- checkout friction hypotheses
- test sequence
- expected lift range

### Example 3: Funnel rebuild plan
Input:
- Multi-channel traffic with inconsistent landing paths

Output focus:
- canonical funnel design
- stage KPI definitions
- experiment roadmap

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
