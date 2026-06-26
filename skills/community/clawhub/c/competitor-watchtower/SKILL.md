---
name: competitor-watchtower
description: Build a lightweight competitor monitoring brief across DTC sites, marketplaces, social channels, and promo surfaces. Use when a team needs pricing or promo scans, assortment watchlists, messaging comparison, threat assessment, or response options without live scraping, BI, or market-intelligence platform access.
---

# Competitor Watchtower

## Overview

Use this skill to turn scattered competitor observations into a structured watch brief. It helps operators focus on the signals that matter most, frame the likely threat or opportunity, and decide what to monitor, ignore, or respond to next.

This MVP is heuristic. It does **not** connect to live price trackers, scraping tools, ad libraries, marketplace APIs, or analytics systems. It relies on the user's supplied competitor notes, channel context, and business priorities.

## Trigger

Use this skill when the user wants to:
- monitor competitor pricing, promo pressure, launches, or assortment moves
- compare competitor messaging, proof strategy, or service promises
- build a weekly watchlist for ecommerce or marketplace operators
- convert rough screenshots or notes into a structured competitor brief
- decide whether a competitor move needs a response now, later, or not at all

### Example prompts

- "Help me build a weekly competitor watchlist for Amazon and TikTok Shop"
- "A rival brand is discounting hard. How should we frame the threat?"
- "Turn these pricing and launch notes into a competitor brief"
- "What should we monitor when a premium competitor launches a new bundle?"

## Workflow

1. Capture the watch purpose, market surface, and named competitors if available.
2. Choose the likely watch mode, such as pricing, launch, creative, or service scan.
3. Organize the highest-signal moves into a threat and opportunity view.
4. Suggest response paths, watch cadence, and owner roles.
5. Return a markdown competitor brief with assumptions and limits.

## Inputs

The user can provide any mix of:
- channels or surfaces such as DTC sites, Amazon, Tmall, TikTok Shop, Xiaohongshu, or retail
- competitor notes about price, discounts, bundles, reviews, assortment, shipping, or messaging
- strategic context such as launch period, promo window, margin pressure, or brand positioning
- internal priorities such as price integrity, share defense, new customer acquisition, or category expansion
- evidence quality notes such as screenshots, anecdotal field notes, or incomplete observations

## Outputs

Return a markdown competitor brief with:
- competitive situation summary
- signal grid by watch category
- threat and opportunity notes
- response options and watch cadence
- owner hints and assumption notes

## Safety

- Do not claim access to live scraped data or market-intelligence platforms.
- Treat competitor interpretation as directional unless the evidence is strong and recent.
- Do not recommend deceptive, anti-competitive, or policy-violating actions.
- Final pricing, assortment, and legal decisions remain human-approved.

## Best-fit Scenarios

- ecommerce teams that need a practical weekly or campaign-based competitor scan
- marketplace sellers facing visible price or promo pressure
- founders or operators who need structure before reacting to a rival move

## Not Ideal For

- real-time scraping or automated alerting infrastructure
- legal claims about competitor misconduct without verified evidence
- formal market sizing or investor-grade intelligence work

## Acceptance Criteria

- Return markdown text.
- Include signal grid, response options, and limits sections.
- Keep the advisory and no-live-data framing explicit.
- Make the brief useful for commercial operators, not just analysts.
