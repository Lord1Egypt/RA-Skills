---
name: bloom
description: >
  Agent-native discovery skill for the intent economy.
  Analyzes your MentalOS, matches use cases, verifies config,
  claims SBT proof, and reports opt-in usage metrics —
  all privacy-first with local analysis.
user-invocable: true
command-dispatch: tool
metadata: {"requires": {"bins": ["node", "npx"], "env": ["OPENCLAW_USER_ID"]}, "optional_env": ["JWT_SECRET", "BLOOM_API_URL", "DASHBOARD_URL", "NETWORK"]}
permissions:
  - read:conversations  # Reads last ~120 messages for LOCAL analysis only
  - read:filesystem     # Reads ~/.openclaw/skills/ for use case verification
  - network:external    # Sends analysis results (NOT raw text) to Bloom API
---

# Bloom Discovery

**Don't browse 13,000 skills. Browse use cases.**

Your agent analyzes how you work, matches you to curated use cases, verifies your configuration, and lets you claim on-chain proof.

## What You Get

### Personality Analysis (MentalOS)
- **Personality Type** — Visionary, Explorer, Cultivator, Optimizer, or Innovator
- **Custom Tagline** — A one-liner that captures your style
- **MentalOS Spectrum** — Learning, Decision, Novelty, Risk (each 0-100)
- **Hidden Pattern Insight** — Something about yourself you might not realize
- **AI-Era Playbook** — Your leverage, blind spot, and next move
- **Tool Recommendations** — Matched from the Bloom skill catalog

### Use Case Discovery
- Describe your intent → get matched use cases (curated skill combinations)
- Personality-aware ranking (novelty seekers get new use cases, risk-averse skip DeFi)
- Each use case = tested combination of skills that solve a real problem

### Verify & Claim SBT
- Scans `~/.openclaw/skills/` to verify you have the right setup for a use case
- Shows match percentage and missing capabilities
- Claim SBT = on-chain proof of your verified configuration
- No wallet? Get a web link instead

### Usage Metrics (Opt-in)
- Anonymized usage reporting: skill name + frequency only
- Improves recommendations for everyone
- **Never sends data without your explicit consent**

## How It Works

Just type `/bloom` in your chat.

Bloom reads your USER.md and recent conversations to:
- **Map your MentalOS** — your operating style across 4 dimensions
- **Find your blind spots** — patterns you might not notice yourself
- **Match use cases** — intent-driven skill combinations
- **Verify your setup** — check if you have what you need
- **Recommend matched tools** — personalized picks from the Bloom catalog

No surveys. No complex setup. No auth flows.

## Quick Start

1. **Chat a little first** (at least 3 messages) so Bloom has context.
2. Type **`/bloom`**.
3. You'll get your **Identity Card + use case matches + dashboard link**.
4. If you're brand new, Bloom will ask **4 quick questions** and generate your card immediately.

## Activation

Say any of these:
- `/bloom`
- "analyze me"
- "what's my builder type"
- "discover my personality"
- "create my bloom card"
- "find use cases for me"
- "verify my config"
- "claim my SBT"

## Security & Privacy

✅ Local analysis — conversation text never leaves your device
✅ Local Differential Privacy (ε=1.0) — spectrum scores noised before transmission
✅ SHA-256 fingerprint — only irreversible hash stored for dedup
✅ Minimal transmission — server sees personality type + approximate scores only
✅ Read-only — never writes or modifies your files
✅ User-initiated — only runs when you invoke it
✅ Opt-in metrics — usage data never sent without consent
✅ Open source — [github.com/bloomprotocol/bloom-discovery-skill](https://github.com/bloomprotocol/bloom-discovery-skill)

❌ Raw text never sent to any server
❌ Wallet keys never transmitted
❌ No PII collection
❌ No background data collection

## Permissions & Data Flow

**Read Conversations** — Reads your last ~120 messages to detect interests and personality patterns. **All conversation text is processed locally on your machine.** Raw message content is never sent to any external server.

**Read Filesystem** — Reads `~/.openclaw/skills/` to verify installed skills against use case requirements. Directory listing only — no file content is read or transmitted.

**External Network** — After local analysis, sends **only derived results** to Bloom Protocol API (`api.bloomprotocol.ai`):
- Personality type (e.g. "The Visionary")
- MentalOS spectrum scores (4 numbers, 0-100)
- Interest categories (e.g. "AI Tools", "Productivity")
- Generated tagline and description
- Use case match results
- Opt-in usage metrics (skill name + frequency only)

**Connections:** `api.bloomprotocol.ai` (identity + catalog + metrics) · `bloomprotocol.ai` (dashboard, read-only)

## Installation

```bash
clawhub install bloom-discovery
```

## Technical Details

- **Version**: 4.0.0
- **Privacy**: LDP ε=1.0 + SHA-256 fingerprint
- **Analysis Engine**: MentalOS spectrum (4 dimensions) + category mapping
- **Primary Signal**: Conversation memory (~120 messages) + USER.md
- **Processing Time**: ~60 seconds (personality) + ~5 seconds (use case matching)
- **Output**: Personality card + use case matches + tool recommendations + dashboard URL

---

**Built by [Bloom Protocol](https://bloomprotocol.ai)**

Making supporter identity portable and provable.
