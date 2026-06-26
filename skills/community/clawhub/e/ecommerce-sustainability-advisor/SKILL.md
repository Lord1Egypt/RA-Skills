---
name: ecommerce-sustainability-advisor
description: Generate practical e-commerce sustainability improvement plans, packaging recommendations, claim-risk cautions, and phased action roadmaps for founders, operations leads, and ESG-minded brand teams. Use when evaluating packaging waste, fulfillment impact, returns, sourcing choices, or marketing claims without live carbon-accounting or compliance APIs.
---

# E-commerce Sustainability Advisor

## Overview

Use this skill to convert rough sustainability concerns into a practical action brief for an e-commerce business. It focuses on operational hotspots such as packaging, shipping, returns, sourcing, and environmental claims.

This MVP is operational and heuristic. It does **not** perform formal carbon accounting, scientific lifecycle assessment, or legal review. It uses built-in best-practice patterns to suggest pragmatic next steps and claim wording cautions.

## Trigger

Use this skill when the user wants to:
- find the biggest sustainability improvement opportunities in an e-commerce operation
- reduce packaging waste or fulfillment impact
- improve sustainability messaging without drifting into greenwashing
- create a short-term and medium-term action roadmap
- align brand, ops, and procurement teams around practical changes

### Example prompts
- "Review our packaging and sustainability claims for a home-goods brand"
- "What are the biggest sustainability wins for our beauty e-commerce business?"
- "We want to sound eco-friendly without making risky claims"
- "Help me reduce returns and packaging waste in our fashion store"

## Workflow

1. Capture the product type, packaging details, fulfillment model, and claim language.
2. Detect the highest-impact operational hotspots.
3. Recommend near-term and medium-term changes that balance impact, feasibility, and customer expectations.
4. Flag risky marketing language or unsupported environmental claims.
5. Return a markdown roadmap with cautions and KPI ideas.

## Inputs

The user can provide any mix of:
- product category or business model
- packaging materials and parcel profile
- sourcing and fulfillment setup
- shipping model and return patterns
- environmental claims or marketing copy
- cost or implementation constraints

## Outputs

Return a markdown brief with:
- executive summary
- impact hotspots
- 90-day action roadmap
- claim wording cautions
- KPI starter pack
- assumptions and limitations

## Safety

- Do not claim scientific or legal certainty.
- Treat claim-risk guidance as a caution, not a legal opinion.
- Avoid unsupported carbon, biodegradability, or recyclability promises.
- State clearly when recommendations rely on incomplete operational data.

## Examples

### Example 1
Input: home-goods brand using oversized boxes and vague green messaging.

Output: identify packaging as the biggest hotspot, recommend right-sizing and recycled-material pilots, and suggest safer wording.

### Example 2
Input: fashion seller with high returns.

Output: highlight returns reduction, fit guidance, and packaging redesign as the main sustainability wins.

## Acceptance Criteria

- Return markdown text.
- Identify at least 3 hotspots, cautions, or action areas.
- Include both operational actions and communication-risk guidance.
- Make it clear that the advice is directional and non-certified.
