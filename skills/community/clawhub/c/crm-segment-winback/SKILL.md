---
name: crm-segment-winback
description: Define CRM segments (new, active, lapsed, VIP, at-risk, churned), build winback triggers, and generate personalized re-engagement campaign ideas across email, SMS, WeChat, and app push. Use when CRM managers, operators, or founders need a segment health brief, winback strategy, or lifecycle campaign calendar without live CRM API, marketing automation, or analytics platform access.
---

# CRM Segment & Winback

## Overview

Use this skill to turn rough customer data notes and lifecycle goals into a structured CRM segment brief and winback campaign strategy. It applies a built-in lifecycle stage framework, winback trigger library, and channel suitability matrix to generate operator-ready recommendations.

This MVP is heuristic. It does **not** connect to live CRM platforms (Klaviyo, Braze, SMS tools, WeChat Work), analytics, or customer data warehouses. It relies on the user's provided segment context, purchase history notes, and campaign goals.

## Trigger

Use this skill when the user wants to:
- define or refine CRM customer segments (new, active, lapsed, VIP, at-risk, churned)
- build winback triggers and timing for lapsed or churned customers
- plan a lifecycle email or SMS campaign sequence across onboarding, retention, and winback
- assess segment health and identify which segments need immediate re-engagement
- generate personalized offer and message ideas for a specific segment

### Example prompts

- "Help me define our CRM segments for a DTC skincare brand"
- "Build a winback strategy for customers who haven't purchased in 90 days"
- "Create a lifecycle campaign calendar for new customers, VIPs, and lapsed buyers"
- "What SMS and email sequence should we use to reactivate churned subscribers?"

## Workflow

1. Capture the business context, customer lifecycle stage, and campaign goal.
2. Define or refine the segment framework based on recency, frequency, monetary, and engagement signals.
3. Identify winback triggers and optimal re-engagement timing per segment.
4. Map segments and campaign types to channels (email, SMS, WeChat, push).
5. Return a markdown CRM brief with segment definitions, winback triggers, channel matrix, and campaign ideas.

## Inputs

The user can provide any mix of:
- business type: DTC brand, marketplace seller, subscription, hybrid
- existing segment notes: current segment names, definitions, or gaps
- customer data context: purchase frequency, average order value, churn patterns, email/SMS opt-in rates
- campaign goal: reduce churn, increase LTV, reactivate lapsed buyers, promote VIP loyalty
- available channels: email (Klaviyo, Mailchimp), SMS (Klaviyo, SMSBump), WeChat, app push
- lifecycle stage: new customer onboarding, ongoing retention, winback, VIP cultivation

## Outputs

Return a markdown brief with:
- segment framework summary (recency, frequency, monetary, engagement tiers)
- segment health scorecard (size, AOV, churn risk, engagement quality per segment)
- winback trigger library (timing, signal, offer type)
- channel suitability matrix (which channel works best for each segment and campaign type)
- personalized message and offer ideas per segment and channel
- campaign sequence outline (email/SMS flow with subject line ideas and timing)
- KPI framework for segment and campaign performance (open rate, CTR, conversion, LTV)

## Safety

- No live CRM platform, customer data warehouse, or marketing automation access.
- Segment definitions are directional; actual segment assignment depends on data quality and platform logic.
- Do not claim guaranteed re-engagement rates or LTV improvements.
- Offer decisions, discount levels, and frequency management remain human-approved.

## Best-fit Scenarios

- DTC brands and small-to-mid-market ecommerce teams with email and SMS programs
- operators building CRM strategy from scratch or refining an existing fragmented approach
- teams that need winback campaign ideas without deep CRM tool expertise

## Not Ideal For

- real-time customer data analysis, automated segmentation, or live campaign execution
- highly regulated industries with strict privacy or consent requirements (healthcare, financial)
- enterprise-grade CRM setups requiring complex behavioral or predictive modeling

## Acceptance Criteria

- Return markdown text.
- Include segment framework, winback trigger library, and channel matrix.
- Cover at least 3 distinct segments with campaign ideas.
- Make data-quality assumptions explicit when segment notes are partial.
- Keep the brief practical for CRM managers and ecommerce operators.
