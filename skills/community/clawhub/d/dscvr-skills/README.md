# DSCVR Intelligence Skill

An [Agent Skills](https://agentskills.io/home) compatible skill for querying DSCVR's crypto intelligence APIs. Works with Claude Code, Roo Code, Amp, OpenCode, and other skills-compatible AI agents.

## What It Does

**News Intelligence**
- **Event Categories** — Browse all tracked crypto event categories
- **Event List** — Search and filter crypto news events by category, date, with pagination
- **Event Detail** — Deep dive into specific events with full analysis, sources, and related coins

**Smart Money Analytics**
- **Smart Money Traders** — List and filter smart money traders by win rate, position size, style, identity, and domain

**Prediction Markets**
- **Market Categories** — Browse prediction market categories
- **Market Listings** — Browse prediction markets with smart money signals and filtering
- **Event Traders** — View smart money positions on specific prediction market events

**AI Discovery**
- **AI Categories** — Browse AI-curated event categories
- **AI Events** — List AI-curated prediction market events with filters
- **AI Search** — Search events by keyword
- **AI Event Detail** — Get detailed AI analysis for a specific event
- **Market Orderbook** — Get orderbook depth data for prediction markets

**Social Graph**
- **GraphQL** — Query DSCVR social data (users, content, portals)

All API calls are authenticated via HMAC-SHA256 signing — the skill handles this automatically.
