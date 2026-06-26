# Roadmap

## Completed ✅

- **v0.1–v0.5** — Digest browsing, SQLite storage, i18n, Google OAuth, Sources CRUD, Source Packs sharing, JSON/RSS Feed, Marks
- **v0.6** — Soft Delete Sources (prevent pack zombie resurrection)

## Near-term 🔨

| Priority | Feature | Description |
|----------|---------|-------------|
| P0 | **Multi-tenant Phase 1** | `raw_items` table + collection pipeline; decouple source fetching from digest generation |
| P1 | **Multi-tenant Phase 2** | Personalized digests based on user subscription combinations |
| P1 | **Sources → Cron integration** | Cron reads `/api/sources?active=true` instead of hardcoded Twitter |

## Mid-term Directions 🧭

### 1. AI Agent Embed
Embed an AI editorial assistant (Chat Widget) for interactive digest exploration:
- Floating chat bubble (bottom-right)
- Behavior-aware: observe browsing patterns, proactive suggestions
- Q&A: deep-dive into current digest topics
- Example: "What's the background on this?" "Track this topic for me"

### 2. Agent Friendly
Make the entire system AI-agent-friendly, lowering automation barriers:
- Structured API output (JSON Schema)
- MCP Server support (let Claude/GPT agents operate Digest directly)
- Webhook callbacks (source update, digest generation events)
- Idempotent operation design (safe agent retries)

### 3. Channel Push
Multi-channel proactive digest delivery — users choose how to receive:
- **Telegram Bot** — Scheduled push + on-demand queries
- **Feishu/Lark** — Group bot / DM delivery
- **Email** — Periodic email summaries (daily/weekly)
- **Slack** — Webhook / Bot integration
- **Discord** — Channel push
- **RSS/JSON Feed** — Done ✅
- Per-user: choose delivery channels + frequency preferences

## Long-term 🔭

| Feature | Description |
|---------|-------------|
| **Source Market** | Community source discovery, trending packs, category browsing |
| **Subscription combo caching** | Same subscription set = shared digest, reducing LLM costs |
| **Multi-language Digest** | Same source pool → different language outputs |
| **Paid tiers** | Source limits, premium source types, higher generation frequency |

## AI Testing (Exploring)

- Current: curl E2E scripts (66 assertions, 18 categories)
- Planned: Playwright + Midscene for UI-level AI testing
- Direction: Natural language assertions, aligned with Agent Friendly roadmap
