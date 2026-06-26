---
name: Dropshipping Product Research
version: v1.0.0
tags: dropshipping, product-research, ecommerce-sourcing, market-validation, competitive-analysis
---

# Dropshipping Product Research

## Overview

Dropshipping Product Research helps beginners and small operators evaluate whether a product is worth testing. It is a descriptive, non-API MVP focused on structured scoring, risk filtering, and clear go / test / reject decisions.

## Trigger

Use this skill when the user wants to:
- evaluate a product idea for dropshipping
- compare multiple product candidates
- estimate risk, margin, and creative fit
- build a weekly shortlist for testing

### Example prompts
- "Evaluate this product for dropshipping in the US"
- "Should I test a galaxy projector or pet grooming glove?"
- "Give me a go / test / reject recommendation"
- "Help me score 3 product ideas for my store"

## Workflow

1. Capture candidate, market, and positioning constraints.
2. Infer demand, competition, margin, creative angle, and risk.
3. Produce a viability score and recommendation.
4. Summarize why it may win, why it may fail, and what to test next.

## Inputs
- product name or keyword
- optional product link or niche
- target market
- price target or cost hints
- mode: single product / batch / trend scouting

## Outputs
- viability score
- sub-scores: demand, competition, margin, creative fit, risk
- recommendation: Go / Test / Reject
- memo with hypotheses and next steps


## Usage Scenarios

1. **User input:** "Score these 5 product ideas for a US-focused Shopify dropshipping store."
→ **Expected output:** 5-product scorecard — demand (Google Trends + Amazon BSR proxy), competition (ad-intensity check, review-count saturation), margin (cost-price vs. market-price with ad-cost breakeven), creative potential (video-ad suitability score), risk (shipping time, return rate, IP infringement check) — ranked with go/test/reject verdict.
2. **User input:** "I found a product on AliExpress with 10,000 orders. Is it too late to enter?"
→ **Expected output:** Market-saturation analysis — competition-velocity check, ad-auction heat (CPM trend), differentiation-gap assessment, and "late entrant" strategy options (niche-down, geo-target underserved region, content-first approach).
3. **User input:** "Build a weekly product-research workflow I can run in 3 hours every Sunday."
→ **Expected output:** Weekly research SOP — trend-scanning (30 min), criteria-scoring top candidates (90 min), supplier-vetting (45 min), creative-brainstorming (15 min) — with scoring spreadsheet template and decision-journal format.



### Scenario 2: 在多多跨境找爆品的野路子
**User input:** "我在Temu上做店群，但不知道选什么品好。有没有快速找到下一个爆品的方法？"
**Expected output:** 拼多多/Temu选品方法论——第一步：关注抖音/小红书/快手带货直播间，看哪个品在密集推广但淘宝/拼多多上竞争还不激烈（搜索量上升但商家数还没暴涨的阶段）；第二步：在1688跨境专供频道按"新品"排序，找最近上架且供应商有现货的品；第三步：在Temu和SHEIN前台按"飙升"和"最新"排序，看哪些品突然涨起来但还没被刷屏；第四步：用Google Trends查关键词在目标国（美国/欧洲）的搜索趋势，找搜索量上升30%以上的品。关键工具：1688跨境专供+神鹰数据+Google Trends+Temu前台。

## Safety
- No marketplace scraping or real-time trend API access
- No guarantee of profit or compliance clearance
- Recommendations are heuristic and should be validated with real tests

## Acceptance Criteria
- Must output markdown
- Must include all five scoring dimensions
- Must include Go / Test / Reject recommendation
- Must include at least three risk or execution notes
