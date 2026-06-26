---
name: creative-ads-helper
description: Generate and evaluate ad creatives for Meta (Facebook/Instagram), TikTok Ads, YouTube Ads, Google Ads, and Amazon Ads with script generation, performance scoring, fatigue timing, and inspiration references.
---

# Creative Helper

## Purpose
Core mission:
- Generate image and video ad script concepts.
- Analyze post-launch creative performance and score assets.
- Detect fatigue cycles and recommend replacement timing.
- Provide inspiration references and industry creative patterns.

## When To Trigger
Use this skill when the user asks for:
- new ad concept generation
- creative scoring and post-analysis
- fatigue diagnosis and replacement schedule
- vertical-specific inspiration examples

High-signal keywords:
- creative, ads, script, video, image
- performance, score, fatigue, insights
- campaign, roas, cpa, optimize

## Input Contract
Required:
- product_offer
- target_audience
- funnel_stage
- existing_creative_context

Optional:
- brand_guidelines
- prohibited_claims
- placement_constraints
- performance_data

## Output Contract
1. Creative Angle and Script Set
2. Creative Scorecard
3. Fatigue Cycle Assessment
4. Replacement and Test Schedule
5. Inspiration Reference Notes

## Workflow
1. Define creative objective by funnel stage.
2. Generate script options by angle family.
3. Score creatives against performance and compliance criteria.
4. Detect fatigue signals by trend and frequency.
5. Produce replacement and retest sequence.

## Decision Rules
- If CTR drops with rising frequency, mark fatigue risk high.
- If strong hook but weak CVR, revise offer framing before visual overhaul.
- If platform format mismatch exists, adapt script priority by placement.
- If no historical data, start with diversified angle set and faster iteration.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), TikTok Ads, YouTube Ads, Google Ads, Amazon Ads

Platform behavior guidance:
- Meta/TikTok: hook speed and first 3 seconds are critical.
- YouTube: longer narrative and proof stacking can work.
- Google/Amazon display: concise value proposition and CTA clarity.

## Constraints And Guardrails
- Avoid unrealistic claims or policy-sensitive copy.
- Separate subjective style feedback from metric-backed conclusions.
- Keep replacement recommendations tied to measurable thresholds.

## Failure Handling And Escalation
- If performance data is absent, output provisional scorecard with confidence label.
- If policy risk is detected, route to Ads Compliance Review.
- If creative production capacity is constrained, prioritize highest-impact variants.

## Code Examples
### Creative Scoring Rubric

    weights:
      hook_strength: 0.25
      offer_clarity: 0.25
      visual_attention: 0.20
      cta_strength: 0.15
      policy_safety: 0.15

### Fatigue Detector

    if ctr_drop_pct >= 20 and frequency >= 2.8:
      fatigue_level: high
      action: rotate_primary_creative

## Examples
### Example 1: New launch script pack
Input:
- Need 5 short-video hooks for cold traffic

Output focus:
- script list
- angle mapping
- CTA variants

### Example 2: Creative score review
Input:
- 15 creatives with last-14-day metrics

Output focus:
- score ranking
- keep/kill suggestions
- next variant ideas

### Example 3: Fatigue replacement timing
Input:
- Top creative slowing down

Output focus:
- fatigue diagnosis
- replacement timing
- backup creative queue

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
