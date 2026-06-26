---
name: creator-collaboration-planner
description: Plan creator partnerships across TikTok, Douyin, Xiaohongshu, Instagram, YouTube, or similar channels. Use when a team needs creator mix recommendations, outreach logic, brief structure, compensation options, collaboration timeline, or risk controls without live creator marketplace or attribution platform access.
---

# Creator Collaboration Planner

## Overview

Use this skill to turn a vague creator marketing goal into a collaboration plan that the operator can actually run. It helps define creator mix, selection criteria, outreach sequence, compensation structure, brief essentials, and measurement logic.

This MVP is heuristic. It does **not** connect to live creator databases, affiliate platforms, social analytics tools, or contract systems. It relies on the user's provided campaign context, creator assumptions, and operating constraints.

## Trigger

Use this skill when the user wants to:
- build a creator collaboration plan for a launch, seasonal push, or always-on program
- choose between seeding, paid, affiliate, ambassador, or live selling partnerships
- brief creators with the right message, proof points, and deliverable expectations
- structure creator tiers, compensation, negotiation guardrails, and review cadence
- reduce creator program risk before outreach starts

### Example prompts

- "Help me build a creator plan for our new product launch on Xiaohongshu and TikTok"
- "What kind of creators should we recruit for seeding versus affiliate sales?"
- "Create a creator outreach and brief plan for a beauty campaign"
- "How should we structure fees, gifting, and tracking for micro creators?"

## Workflow

1. Capture the commercial goal, target channels, and collaboration format.
2. Choose the likely program type, creator mix, and compensation logic.
3. Define the brief, outreach sequence, and approval workflow.
4. Map risks such as misalignment, disclosure issues, and slow approvals.
5. Return a markdown collaboration plan with timeline and debrief guidance.

## Inputs

The user can provide any mix of:
- target channels such as TikTok, Douyin, Xiaohongshu, Instagram, YouTube, or Bilibili
- campaign goal such as awareness, conversion, review seeding, or launch momentum
- creator preferences such as micro creators, UGC makers, experts, affiliates, or live hosts
- deliverables, fee assumptions, gifting plan, commission logic, and approval constraints
- timeline, product samples, usage rules, and disclosure requirements
- known risks such as vague brief quality, tracking gaps, or slow legal approval

## Outputs

Return a markdown collaboration plan with:
- collaboration strategy summary
- creator mix and selection rubric
- offer structure and brief essentials
- outreach and negotiation plan
- timeline and operating rhythm
- measurement and debrief guidance
- risk controls and limitations

## Safety

- Do not claim access to live creator rosters, audience analytics, or attribution tools.
- Do not promise reach, sales, or ROAS outcomes from a creator plan.
- Compensation, legal review, and disclosure decisions remain human-approved.
- Reduce certainty when audience fit or product differentiation is weak.

## Best-fit Scenarios

- brands building creator programs without an in-house influencer lead
- operators who need a practical seeding or paid-collaboration framework
- teams that want clearer creator selection and brief quality before spending

## Not Ideal For

- automated creator recruitment or in-app campaign execution
- final legal contract drafting for regulated or highly sensitive categories
- attribution modeling that depends on live analytics or clean tracking infrastructure

## Acceptance Criteria

- Return markdown text.
- Include creator mix, brief, outreach, timeline, and risk sections.
- Keep the no-live-data limitation explicit.
- Make the output practical for a brand or ecommerce operator.
