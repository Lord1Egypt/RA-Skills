---
name: dtc-ads-helper
description: Diagnose DTC ads performance across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, and Shopify Ads by validating pixel attribution, account structure, creative signals, and conversion funnel opportunities.
---

# DTC Helper

## Purpose
Core mission:
- Validate pixel and attribution readiness for OCPX-style optimization.
- Analyze account structure and creative performance to explain ROAS volatility.
- Provide scale path and budget lift recommendations.
- Output landing page and conversion funnel optimization actions.

## When To Trigger
Use this skill when the user asks for:
- DTC store growth troubleshooting
- ROAS instability diagnosis
- scaling strategy after initial traction
- landing page and funnel optimization for paid traffic

High-signal keywords:
- dtc, ecommerce, shop, checkout, conversion
- roas, cpa, budget, scale, optimize
- pixel, tracking, attribution, campaign

## Input Contract
Required:
- store_url
- platform_account_snapshot
- pixel_event_snapshot
- recent_performance_window

Optional:
- creative_report
- landing_page_metrics
- cohort_ltv
- inventory_constraints

## Output Contract
1. Pixel and Attribution Readiness Verdict
2. ROAS Volatility Root-Cause Tree
3. Scale Path and Budget Lift Plan
4. Landing Page and Funnel Fixes
5. Execution Priority Queue

## Workflow
1. Check event completeness for core commerce events.
2. Audit campaign/adset/ad structure and budget fragmentation.
3. Compare creative performance by funnel stage.
4. Diagnose ROAS swings by channel, offer, and audience.
5. Produce scale-safe budget and funnel actions.

## Decision Rules
- If Purchase event quality is low, pause aggressive scale and fix tracking first.
- If creative fatigue is detected, prioritize new hooks before raising budget.
- If funnel CVR is below threshold, route spend to best-converting LP first.
- If LTV is unknown, avoid over-bidding on upper-funnel traffic.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Shopify Ads

Platform behavior guidance:
- Meta/TikTok for creative-led demand creation.
- Google for intent capture and bottom-funnel efficiency.
- Shopify events must stay consistent with platform conversion definitions.

## Constraints And Guardrails
- Do not infer profitability without COGS or contribution assumptions.
- Mark attribution blind spots explicitly.
- Keep scale recommendations bounded by measurement confidence.

## Failure Handling And Escalation
- If pixel data is incomplete, output tracking repair plan first.
- If account permission blocks data access, provide minimum data request packet.
- If severe policy risk exists, route to Ads Compliance Review.

## Code Examples
### OCPX Readiness Check (YAML)

    required_events:
      - ViewContent
      - AddToCart
      - InitiateCheckout
      - Purchase
    event_quality_threshold: high
    readiness: conditional

### ROAS Volatility Slice (JSON)

    {
      "window": "last_14d",
      "worst_segment": "retargeting-video-1",
      "roas_drop_pct": 31,
      "suspected_causes": ["creative_fatigue", "audience_overlap"]
    }

## Examples
### Example 1: Sudden ROAS drop
Input:
- DTC store ROAS down 25% in 10 days

Output focus:
- root-cause breakdown
- quick stabilizing actions
- budget protection rules

### Example 2: Scale decision
Input:
- Profitable baseline, wants 2x spend

Output focus:
- safe scaling ladder
- creative replacement cadence
- funnel readiness checklist

### Example 3: LP conversion issue
Input:
- CTR stable, CVR down

Output focus:
- LP diagnosis
- checkout friction fixes
- retest plan

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
