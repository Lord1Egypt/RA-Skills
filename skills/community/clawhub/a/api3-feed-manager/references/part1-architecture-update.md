# Part 1 Architecture Update

## Important correction

Further review shows the Part 1 skill should not be modeled only as a generic "feed funding helper".

However, for the agent use case in this project, the correct practical model is **not** per-dApp proxy deployment.

## Agent-specific constraint

For these agents, we should use the **generic proxy on Api3 Market**.

Reason:
- OEV can accrue to Api3 in this mode
- permissionless deployment of individual dApp-specific proxies is not currently available for our intended fully permissionless agent flow

So the skill should optimize for what agents can actually do today, not for a cleaner but unavailable theoretical path.

## Revised role of the skill

The skill should primarily do four things:

1. discover the relevant feed on Api3 Market
2. classify whether the feed is active / usable / non-operational
3. return the correct **generic Market proxy** or integration artifact for downstream agents
4. when needed, help move a known but inactive feed toward usability through funding/activation paths

## Why this matters

A downstream agent using this skill should be able to ask:
- "I need an Api3 price feed for asset X on chain Y"

and get back:
- whether the feed is known on Market
- whether it appears operational
- the generic Market proxy / feed integration details to use
- whether the feed is already usable
- if not usable, what is missing (e.g. activation/funding)

## What the skill should not assume

The skill should **not** assume:
- that a dApp-specific Api3ReaderProxyV1 can be permissionlessly deployed for the agent today
- that the ideal OEV-capturing deployment pattern is available to agent users right now

## Design implication

The architecture should now prioritize:
1. live feed discovery from Api3 Market metadata
2. readiness classification
3. generic proxy resolution / integration artifact return
4. non-operational feed activation/funding support

## Updated implementation direction

Near-term implementation should focus on:
- improving live discovery matching
- extracting/returning the generic Market proxy path where possible
- identifying discoverable but non-operational feeds
- only then extending toward activation/funding workflows

## Why this is the correct compromise

This design is less theoretically perfect than per-dApp proxy deployment, but it matches the actual permissionless capability available to agent users now.

That is the right tradeoff for this project.
