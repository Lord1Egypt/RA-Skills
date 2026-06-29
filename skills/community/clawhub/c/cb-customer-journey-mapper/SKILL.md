---
name: Cross-border Customer Journey Mapper
description: Map complete customer journeys for any overseas market — with localized touchpoints, cultural buying triggers, and conversion barriers. Output a visual-ready journey map, not just theory — complete with pain points, opportunities, and channel recommendations.
version: v1.0.0
tags: cross-border, customer-journey, ux-research, international-markets
---

# Cross-border Customer Journey Mapper

## Overview

This skill provides a structured method for mapping the end-to-end customer journey for overseas customers, from initial awareness through purchase, onboarding, retention, and advocacy. It recognizes that trust dynamics, channel preferences, and the role of social proof shift significantly across cultures and markets. The framework guides you through mapping each stage of the journey in the target market, auditing local channel touchpoints, diagnosing trust barriers and friction points, aligning messages and proof points to local expectations, designing a retention and advocacy loop, and building a stage-by-stage measurement plan.

The framework is designed for product, marketing, customer experience, and growth teams building international customer funnels.

## When to Use

- You are entering a new market and need to understand how your customers discover, evaluate, and buy from you differently than at home
- Your conversion rates in an overseas market are lower than expected and you want to diagnose where customers are dropping off
- You are localizing your product or service and need to know which journey stages require the most redesign
- You want to build a shared understanding of the international customer journey across your product, marketing, and sales teams
- You are preparing for a market launch and want to validate your channel and message strategy before investing heavily

## Inputs to Collect

1. **Product or service:** what you sell, the typical purchase decision timeline, and the post-purchase experience
2. **Target market(s):** specific country or region, language, and urban vs. rural distribution
3. **Current funnel data:** conversion rates at each stage if you already operate in the market; or competitive benchmarks if you are entering fresh
4. **Channel knowledge:** which platforms, marketplaces, and offline touchpoints are relevant in the target market for your category
5. **Customer segment:** whether you are targeting consumers (B2C) or businesses (B2B), and any known segment differences in the market
6. **Trust signals available:** what proof points, reviews, certifications, or brand associations you currently have to offer
7. **Known friction points:** any feedback, support tickets, or reviews that already surface issues in the current journey

## Workflow

1. Define the overseas customer segment and map the full journey from trigger and awareness through consideration, purchase, onboarding, retention, and advocacy.
2. List the local touchpoints customers use at each stage, including search, social platforms, marketplaces, creator content, reviews, communities, partner channels, sales conversations, and support channels.
3. Diagnose stage-by-stage friction and trust gaps such as unfamiliar brand origin, unclear local proof, language uncertainty, payment concern, delivery anxiety, return policy doubt, and after-sales support risk.
4. Align messages, proof assets, channel owners, support actions, and product or operations changes to the specific friction points found at each journey stage.
5. Create a measurement and research plan that identifies where the journey leaks, what evidence is needed, and which interview, survey, analytics, or experiment should happen next.

## Output Modules

1. **Journey-Stage Map** — six-stage map with primary channels, content types, and estimated stage durations per market
2. **Local Channel Touchpoint Inventory** — comprehensive touchpoint list per stage per market
3. **Trust and Friction Diagnosis** — trust barriers and friction points by stage with severity rating
4. **Message and Proof-Point Alignment** — message strategy, proof point types, and channel format guidance by stage
5. **Retention and Advocacy Loop** — onboarding, engagement, advocacy trigger, and feedback loop designs
6. **Journey Measurement Plan** — stage-level metrics with baseline targets and review cadence

## Example Prompts

Try these real-world scenarios to see what this skill can produce:

**Prompt 1: Ecommerce Journey Map**
> "Map the customer journey for a Japanese consumer buying premium tea from our UK-based online store. From first awareness (Instagram/Pinterest discovery) through purchase, delivery, and repurchase. Include cultural-specific touchpoints: omotenashi expectations, gift-packaging norms, and the Japanese review culture."
> → Output: 7-stage journey map (Awareness → Consideration → Purchase → Payment → Delivery → Unboxing → Post-Purchase), touchpoint inventory per stage with channel (Instagram, Rakuten comparison, LINE messaging), cultural annotations (gift-wrapping expectation, review thoroughness norm, trust-badge hierarchy for JP), pain points (shipping time anxiety, English-only checkout friction, payment method gaps), opportunity map (LINE integration, Rakuten Ichiba presence, Japanese-language review nudges), KPI recommendations per stage

**Prompt 2: B2B SaaS Onboarding Journey**
> "Our project management SaaS has great conversion in North America but terrible onboarding completion in Germany. German users seem to want more documentation before trying features, and they drop off at the 'invite team members' step. Map the German-user onboarding journey and redesign it."
> → Output: Current-state journey map (signup → first project → invite team → first collaboration → paid conversion), German-user behavior overlay (documentation-first pattern, privacy concerns at invite step, group-decision pattern), drop-off analysis per step with data, redesigned journey (add self-service documentation hub before feature tour, replace 'invite team' with 'share workspace link,' add DSGVO compliance reassurance), A/B test plan for redesigned flow

**Prompt 3: Cross-Border B2C Marketplace Journey**
> "We run a cross-border marketplace connecting Southeast Asian artisans with US/EU buyers. Map the buyer journey for US customers, then for German customers. Highlight where the journeys diverge and what we need to localize."
> → Output: Dual journey map (US vs DE), parallel-stage comparison, divergence points (payment preferences: credit card vs SOFORT/PayPal; trust signals: social proof vs certifications; delivery expectations: speed vs reliability; return behavior: infrequent vs common), localization action plan (14 specific changes), impact-priority matrix

## Getting Started

👋 **cb-customer-journey-mapper installed!**

I map every step your overseas customers take — from discovery to repurchase — with cultural nuances built in.

Start mapping:
> "Map the customer journey for [product] in [market]. Our typical customer discovers us through [channel] and buys because [reason]."

Give me your market and product, and I'll map the full journey with pain points and opportunities.

## Safety and Limitations

Customer journey maps are planning and diagnostic tools, not confirmed representations of how real customers behave. They are hypotheses that must be validated through customer research, analytics data, and continuous iteration. Journey maps built from desk research or assumptions about a market are especially prone to error; validate critical assumptions before investing significantly in journey redesigns based on them.

## Acceptance Criteria

- Covers all six journey stages (awareness, consideration, purchase, onboarding, retention, and advocacy) with market-specific details
- Identifies and rates trust barriers by stage per market
- Maps local proof points and channel touchpoints for each stage with explicit "present vs. not present" status
- Includes friction-reduction action items for at least the three highest-severity friction points per market
- Defines at least one metric per journey stage with baseline targets and review cadence


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "Map the end-to-end customer journey for a French customer buying our premium home goods vs. a US customer." | Side-by-side journey maps (Awareness → Consideration → Purchase → Delivery → Post-purchase). French journey divergences: higher reliance on third-party review sites (Trustpilot), preference for bank-transfer payment (not credit card), higher post-purchase service expectations (thank-you note expectation). |
| 2 | "Identify the top 3 friction points in our checkout flow for Middle Eastern customers." | Friction analysis: (1) no COD option (65% of UAE e-commerce is COD), (2) Arabic language toggle hidden on mobile, (3) no Tamara/Tabby BNPL option (expected in KSA/UAE). Impact: estimated 22% cart abandonment attributable to these three issues. |
| 3 | "We are redesigning our onboarding for the Indian market. Map the ideal first-7-days journey and compare with current reality." | Ideal vs. reality gap analysis: Ideal includes WhatsApp onboarding drip (not email - Indian users prefer WhatsApp), local payment demo (UPI integration), and regional-language tutorial video. Current: English-only email drip with US-centric examples. Redesign roadmap. |


### Scenario 2: 海外客户从知道到买的路径怎么画
**User input:** "我们做跨境电商想把客户的购物旅程画出来，但不知道他们每个环节在想什么怎么优化。"
**Expected output:** 跨境电商客户旅程地图——认知阶段（客户通过TikTok/IG/Google发现你的品牌，关键：封面图和标题决定了要不要点进来）；考虑阶段（客户查看你的亚马逊页面/独立站，关键：评价数量和质量、价格对比、产品描述的细节度）；购买阶段（客户决定下单，关键：支付方式的便利性PayPal/Apple Pay、运费是否免费、退换货政策的透明度）；留存阶段（收到货后，关键：拆箱体验包装设计、产品实际性能、客服响应速度）；忠诚阶段（使用一段时间后，关键：是否触发复购的邮件/短信、社交媒体的品牌感召力）。优化建议：每个阶段找出客户最常问的3个问题+最常遇到的3个卡点，逐个解决。
