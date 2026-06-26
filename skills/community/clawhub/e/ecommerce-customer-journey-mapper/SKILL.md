# E-commerce Customer Journey Mapper

## Overview

E-commerce Customer Journey Mapper is a descriptive skill for DTC brands, Shopify operators, and e-commerce consultants. It synthesizes business context, customer touchpoints, reviews, FAQs, support signals, and optional funnel metrics into a stage-by-stage customer journey map.

This MVP does **not** call real analytics, heatmap, or CRM APIs. It uses built-in templates, stage heuristics, and best-practice libraries to generate a practical markdown brief.

## Trigger

Use this skill when the user wants to:
- diagnose conversion drop-off across the funnel
- map customer experience from awareness to retention
- align landing pages, ads, checkout, and retention messaging
- generate a quick journey audit for an e-commerce brand or client

### Example prompts
- "Map the customer journey for my skincare Shopify store"
- "Where are customers dropping off between ad click and checkout?"
- "Help me create a journey audit from reviews, FAQ, and landing page notes"
- "We have repeat purchase issues, can you map the weak stages?"

## Workflow

1. Collect business context, touchpoints, and analysis objective.
2. Normalize evidence into journey stages.
3. Detect likely friction points, emotion patterns, and gaps.
4. Score opportunities by impact, effort, and stage sensitivity.
5. Generate a markdown report with journey map, friction report, and action brief.

## Inputs

User can provide one or more of the following:
- store type / niche
- target market
- traffic sources
- touchpoint evidence: landing page notes, ads copy, email copy, reviews, FAQ, support logs
- optional funnel metrics
- analysis goal: drop-off diagnosis, checkout optimization, retention improvement, messaging alignment
- analysis mode: `quick` or `deep`

## Outputs

A markdown report with:
- Executive summary
- Journey stage map
- Friction point report
- Opportunity matrix
- Prioritized next-step brief

## Safety

- No real API calls or scraping
- No claims of factual analytics access
- Output quality depends on the materials provided by the user
- Recommendations are advisory, not guaranteed business outcomes

## Acceptance Criteria

- Must return markdown text
- Must cover at least 5 journey stages
- Must identify stage-specific friction points
- Must include prioritized recommendations
- Must clearly state that the analysis is heuristic and non-API-based
