# FDE Delivery Loop handover contract

This skill owns Stage 3 only. Do not absorb the responsibilities of adjacent skills.

## Minimum upstream input

### #1 Problem discovery

- Customer issues with source, current workflow and target roles
- Facts, assumptions, constraints and unproven value judgments
- Key stakeholders and issues requiring clarification

### #2 POC Project Contract

- Key roles such as customer and internal leaders, approval/security, etc.
- POC issues, passing criteria, timeboxing and input from both parties
- Confirmed scope, prohibitions and next steps after failure

Without sufficient input, the PRD can only be a draft condition. Don’t escalate speculation into confirmed needs.

## Minimum downstream handover

| Downstream Skills | What to expect from this PRD |
|---|---|
| #4 Deployment Architect | Data sources, systems, permissions, integration expectations, environment constraints, Mock boundaries, risks |
| #5 Agent Skill Designer | User tasks, input and output, rules, tool boundaries, Guardrails, upgrades, evaluation cases |
| #6 POC Runner | Passing Thresholds, User Journeys, AC, Test/Demo Scenarios, Test Data Boundaries |
| #7 Adoption and Value | Expected results, indicator definitions, data sources, owners, unconfirmed baselines/goals |

## Conflict handling

Stop expanding requirements and mark `[To be confirmed]` when: customer evidence conflicts with the POC contract; AC cannot be mapped via standards; data/permissions/integrations are not confirmed; Demo relies on pretending to be online capabilities; or value indicators have no data source/owner.
