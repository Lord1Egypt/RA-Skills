---
name: crm-lead-manager
description: Manage ad-generated leads and pipeline routing from Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, and landing-page funnels.
---

# Ads CRM Leads

## Purpose
Core mission:
- lead scoring, routing SLA, follow-up cadence

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads
- this specific capability: lead scoring, routing SLA, follow-up cadence

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- lead_source
- lead_payload_fields
- qualification_goal

Optional:
- routing_rules
- response_sla
- pipeline_stages
- crm_constraints

## Output Contract
1. Lead Intake Validation
2. Qualification Logic
3. Routing and Ownership Plan
4. Follow-up Cadence
5. Pipeline Risk Alerts

## Workflow
1. Validate incoming lead schema and required fields.
2. Score lead quality using explicit rules.
3. Route leads to owner queues by fit and urgency.
4. Define follow-up timeline and SLA checks.
5. Report leakage points and recovery actions.

## Decision Rules
- If critical lead fields are missing, route to enrichment queue first.
- If lead intent is high, enforce same-day response rule.
- If low-fit leads dominate, tighten ad targeting and qualification forms.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads

Platform behavior guidance:
- Keep recommendations channel-aware; do not collapse all channels into one generic plan.
- For Meta and TikTok Ads, prioritize creative testing cadence.
- For Google Ads and Amazon Ads, prioritize demand-capture and query/listing intent.
- For DSP/programmatic, prioritize audience control and frequency governance.

## Constraints And Guardrails
- Never fabricate metrics or policy outcomes.
- Separate observed facts from assumptions.
- Use measurable language for each proposed action.
- Include at least one rollback or stop-loss condition when spend risk exists.

## Failure Handling And Escalation
- If critical inputs are missing, ask for only the minimum required fields.
- If platform constraints conflict, show trade-offs and a safe default.
- If confidence is low, mark it explicitly and provide a validation checklist.
- If high-risk issues appear (policy, billing, tracking breakage), escalate with a structured handoff payload.

## Code Examples
### Lead Scoring Rule

    score = intent_score + fit_score + urgency_score
    if score >= 80: route = high_priority

### Routing Payload

    lead_id: L-20260303-01
    route_to: team-a
    sla_hours: 4

## Examples
### Example 1: Lead quality drop
Input:
- Lead volume increased, close rate decreased
- Source: Meta and Google Ads

Output focus:
- scoring rule update
- routing correction
- feedback loop to targeting

### Example 2: SLA breach management
Input:
- Sales team delayed first response
- High-intent leads lost

Output focus:
- SLA enforcement plan
- escalation logic
- dashboard metric updates

### Example 3: Multi-market lead routing
Input:
- Leads from US and EU mixed in one queue
- Language mismatch issues

Output focus:
- region routing map
- ownership model
- automation rules

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
