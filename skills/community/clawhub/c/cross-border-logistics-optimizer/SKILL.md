---
name: cross-border-logistics-optimizer
description: Compare cross-border e-commerce shipping options, packaging tactics, customs-risk signals, and speed-versus-cost tradeoffs for sellers, operations teams, and marketplace operators. Use when choosing routes, carriers, declaration practices, or packaging plans for parcel shipments without relying on live carrier APIs.
---

# Cross-border Logistics Optimizer

## Overview

Use this skill to turn shipment notes into a practical route recommendation brief. It is optimized for parcel-level e-commerce decisions, especially when a seller needs to balance shipping cost, transit speed, customs reliability, and packaging risk.

This MVP is advisory only. It does **not** fetch live rates, customs rules, or carrier SLAs. It relies on built-in logistics heuristics and common e-commerce exception patterns.

## Trigger

Use this skill when the user wants to:
- compare shipping lanes for international e-commerce orders
- choose between cheap, fast, or low-risk logistics modes
- identify customs-delay risks and declaration pitfalls
- reduce dimensional-weight or packaging mistakes
- create a short decision memo for an ops team

### Example prompts
- "Compare shipping options from China to Germany for cosmetics"
- "We need the safest route to Brazil for a fragile parcel"
- "How should I package low-value accessories going to Canada?"
- "Help me choose between cheap and fast cross-border shipping"

## Workflow

1. Capture the origin, destination, parcel profile, product type, and business priority.
2. Detect likely risk signals such as customs sensitivity, dimensional-weight pressure, or restricted goods handling.
3. Compare three lane patterns with tradeoff notes.
4. Recommend the best-fit route, packaging posture, and documentation focus.
5. Return the result as a markdown decision brief.

## Inputs

The user can provide any mix of:
- origin and destination countries
- weight and parcel dimensions
- product category or sensitivity
- declared value
- carrier preferences or service-level goals
- priority, such as cheapest, fastest, or safest
- known issue patterns, such as customs delay or damage

## Outputs

Return a markdown report with:
- executive summary
- route comparison table
- recommended shipping plan
- packaging checklist
- customs and exception risks
- assumptions and follow-up actions

## Safety

- Do not claim access to live rates or carrier systems.
- Treat all customs and compliance guidance as directional, not legal advice.
- Avoid guaranteed delivery claims.
- Call out when the input lacks dimensions, value, or product sensitivity details.

## Examples

### Example 1
Input: China to Germany, cosmetics, tracked service preferred.

Output: recommend a duty-aware direct line over the cheapest untracked option, plus declaration and leakage-control notes.

### Example 2
Input: US to Canada, small accessories, cost priority.

Output: compare economy tracked, direct line, and express courier options, with dimensional-weight mitigation advice.

## Acceptance Criteria

- Return markdown text.
- Include a 3-option lane comparison.
- Explain why the recommended lane fits the stated priority.
- Include at least one packaging note and one customs-risk note.
