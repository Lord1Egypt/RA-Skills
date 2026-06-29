---
name: Cross-border Data Privacy Readiness Guide
description: Get a practical, step-by-step privacy compliance checklist for any market — GDPR, CCPA, LGPD, PIPL, and more. Skip the legal jargon and get an actionable readiness plan with templates for privacy policies, cookie banners, data-processing agreements, and DSAR workflows.
version: v1.0.0
tags: cross-border, data-privacy, gdpr, compliance, international-law
---

# Cross-border Data Privacy Readiness Guide

## Overview

A readiness checklist for overseas digital businesses handling customer data, covering GDPR-style principles, consent, retention, vendors, and incident response.

This is a pure descriptive OpenClaw skill for overseas expansion planning. It provides frameworks, templates, checklists, decision criteria, and risk reminders. It does **not** execute code, call APIs, access the network, scrape websites, submit forms, make purchases, send messages, or perform any external action.

## When to Use

Use this skill when the user needs structured help with cross-border data privacy readiness guide in a cross-border or international expansion context.

Typical trigger phrases include:
- GDPR readiness
- cross-border data privacy
- international privacy checklist
- overseas user data
- privacy compliance preparation

## Target Users

Founders, product managers, operations teams, marketers, and compliance coordinators preparing for overseas users.

## Inputs to Collect

Ask for or infer the following context before producing the final framework:

- Target market or list of candidate markets
- Product, service, category, or business model
- Current business stage and domestic traction, if any
- Target customer segment and purchase context
- Expansion goal, timeline, budget range, and constraints
- Existing assets such as brand story, content, team, channels, customer data, or partners
- Known risks, assumptions, compliance concerns, and decision deadlines

If important inputs are missing, state the assumptions clearly and provide a version that can be refined later.

## Workflow

1. Inventory the customer data the business collects, why it is collected, where it is stored, who accesses it, and which vendors process it.
2. Map privacy obligations at a principle level: notice, consent or lawful basis, minimization, retention, access rights, deletion, security, and cross-border transfer.
3. Identify product, marketing, analytics, support, and vendor workflows that may create privacy risk in the target market.
4. Prioritize readiness actions such as privacy notice updates, consent review, data-retention rules, vendor review, request handling, and incident preparation.
5. Define questions for qualified privacy counsel so the team can turn the readiness map into jurisdiction-specific compliance work.

## Output Modules

### Data inventory map
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

### Consent and lawful-basis checklist
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

### Vendor and processor review
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

### Retention and deletion policy template
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

### User-rights request workflow
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

### Incident response preparation
- Purpose: turn the user's market context into a structured planning component.
- Include: assumptions, recommended actions, decision criteria, and questions that require local validation.
- Output style: concise tables, checklists, and bullet-point rationale rather than generic advice.

## Example Prompts

Try these real-world scenarios to see what this skill can produce:

**Prompt 1: Multi-Jurisdiction Compliance Audit**
> "We're a DTC ecommerce brand shipping to 40+ countries. We collect: email, shipping address, purchase history, and browsing behavior via Facebook Pixel + Google Analytics. We're not sure if we're compliant everywhere. Audit our data practices and tell us what we need to fix for GDPR (EU), CCPA (California), LGPD (Brazil), and PIPL (China)."
> → Output: Data inventory map (what we collect × where × why), jurisdiction compliance gap analysis (4-column matrix: requirement, current status, gap, fix), prioritized action plan (critical: consent management platform, privacy policy updates, DPA with vendors; high: DSAR workflow, data retention policy; medium: cookie consent for non-EU), vendor compliance checklist (Meta, Google, Shopify, payment processors), ready-to-adapt template bundle (privacy policy, cookie banner copy, DSAR response template)

**Prompt 2: SaaS GDPR Readiness**
> "We're a US-based B2B SaaS with 30% EU customers. We process customer CRM data as a data processor. A German enterprise prospect is asking for our GDPR compliance documentation before signing a €200K deal. Build the compliance pack we need to send them."
> → Output: Enterprise compliance pack checklist (DPA, SOC 2 report reference, data processing register, sub-processor list, cross-border transfer mechanism — SCC documentation, technical security measures document, breach notification procedure), document-by-document template/outline, 7-day sprint plan to assemble the pack

**Prompt 3: App Privacy for Global Launch**
> "We're launching a mobile app (fitness tracking with social features) on iOS and Android globally. We collect: health data, location, contacts (for friend-finding), and photos. Build the privacy launch playbook for App Store and Google Play compliance across US, EU, and South Korea."
> → Output: Data-type risk classification (health=high, location=high, contacts=medium, photos=medium), per-platform requirements matrix (Apple Privacy Nutrition Labels, Google Data Safety section), per-jurisdiction requirements (GDPR Art 9 for health data, South Korea PIPA location consent), privacy screen designs (consent flows per data type), privacy policy (user-friendly + legally compliant), launch-ready checklist

## Getting Started

👋 **cb-data-privacy-readiness-guide installed!**

I turn privacy laws into practical checklists — what you need to fix, templates you can use, and the order to fix it in.

Start your compliance check:
> "Audit our data privacy compliance for [markets]. We collect: [data types]. Our business: [business model]."

Tell me what data you handle and where your customers are. I'll show you the gaps and give you the templates.

## Safety and Limitations

Privacy and data-transfer rules are legal matters; use qualified privacy counsel for compliance decisions.

Additional limitations:

- No professional legal, tax, financial, medical, employment, investment, or compliance advice.
- No guarantee of market success, conversion improvement, legal compliance, or platform acceptance.
- Verify local laws, platform policies, consumer expectations, and current market facts with qualified professionals and reliable sources.
- Avoid stereotyping cultures or users; treat all cultural observations as hypotheses requiring local validation.

## Acceptance Criteria

- Creates a plain-language data inventory
- Identifies privacy readiness gaps
- Includes consent, retention, vendor, and access-rights checkpoints
- Provides implementation priority levels
- States that it is not legal advice
- Provides structured, market-aware outputs rather than generic overseas expansion advice.
- Includes explicit assumptions, evidence gaps, and validation steps.
- Stays pure descriptive with no code execution, API calls, browsing, network access, or external side effects.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "We are a US-based SaaS expanding to the EU. Assess our GDPR readiness - we use AWS US-East, Mailchimp, and Stripe." | Readiness scorecard: data residency (non-compliant - data in US-East), subprocessors (need DPAs for Mailchimp and Stripe), consent mechanism (cookie banner is non-compliant), privacy policy (missing EU-specific sections). Priority remediation roadmap. |
| 2 | "Map the data-privacy requirements for launching in Brazil (LGPD), Japan (APPI), and South Korea (PIPA) simultaneously." | Comparison matrix: consent requirements, data-localization mandates, breach-notification timelines, DPO requirements, and cross-border transfer restrictions per country. Overlap analysis showing where a single policy can cover multiple markets. |
| 3 | "Generate a DSAR (Data Subject Access Request) response template that works across GDPR and LGPD." | Combined template with jurisdiction-specific annotations: response timeline (GDPR: 30 days, LGPD: 15 days), required disclosures, exemption justifications, and record-keeping requirements. |


### Scenario 2: 做海外业务要遵守什么数据合规要求
**User input:** "我的App有1000个美国用户，听说GDPR和CCPA很严格。我需要做什么才能合规又不花太多钱？"
**Expected output:** 小团队数据合规入门——第一步：搞清楚适用哪些法律（美国用户用CCPA、欧洲用户用GDPR、中国用户用个人信息保护法，按用户所在地而不是公司所在地）；第二步：必须有的文档（隐私政策——参考同类App的模板然后在Notion/Google Doc上修改、Cookie横幅——用免费工具如Cookiebot生成、数据删除流程——建一个邮箱专门处理用户删除请求）；第三步：不必花大钱的（暂时不需要专门的数据保护官，如果你<1000个欧洲用户；CCPA对年收入<2500万美元的公司有豁免）；第四步：检查第三方SDK（所有用到的分析/广告SDK是否合规，Google Analytics 4有基本合规功能）。关键工具：iubenda/FreePrivacyPolicy生成基本文档。
