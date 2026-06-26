---
name: bloom-discovery
version: 4.0.1
description: >
  Agent-native discovery skill for the intent economy.
  Analyzes your MentalOS, matches use cases to your installed skills,
  lets you claim SBT proof, and optionally reports usage metrics —
  all privacy-first with local analysis.
homepage: https://bloomprotocol.ai
category: agent-tools
os: [macos, linux]
network: base-mainnet
metadata:
  {
    "openclaw": {
      "emoji": "🌸",
      "requires": { "bins": ["node", "npx"] }
    }
  }
---

# Bloom Discovery Skill

Don't browse 13,000 skills. Browse use cases.

Bloom Discovery is an agent-native skill that analyzes how you work, matches you to curated use cases, verifies your configuration, and lets you claim on-chain proof — so your agent works for you, not the other way around.

## Capabilities

### 1. Personality Analysis (MentalOS)
Reads your USER.md and conversation history (~120 messages) to map your builder personality across 4 dimensions:
- **Learning** (學習風格): Try First ↔ Study First
- **Decision** (決策風格): Gut ↔ Deliberate
- **Timing** (採用時機): Pioneer ↔ Pragmatist
- **Focus** (投入方式): All-In ↔ Diversified

Outputs: Personality type (Visionary / Explorer / Cultivator / Optimizer / Innovator), custom tagline, hidden pattern insight, AI edge guide. Includes `displayLabels` with en/zh translations for all sections.

### 2. Use Case Discovery
Intent-driven skill browsing. Instead of searching 13,000 skills, you describe what you want to accomplish and Bloom matches you to curated use cases — each a tested combination of skills.

- Fetches use case catalog from Bloom API
- Matches against your personality spectrum (novelty-seekers get new use cases, risk-averse skip DeFi)
- Keyword frequency threshold (≥ 3 mentions) to avoid noise

### 3. Verify Configuration & Claim SBT
Scans your installed skills (`~/.openclaw/skills/`) and verifies whether you have the right setup for a given use case.

- Compares installed skills against use case requirements
- Shows match percentage and missing capabilities
- Claim flow: verified config → POST /api/claim → mint SBT or get web link
- SBT = on-chain proof that you have a verified configuration

### 4. ERC-8004 Identity Registration
Register your agent identity on the ERC-8004 Agent Identity Registry (Base mainnet).

- Sends your agent profile (name, skills, endpoint) to backend for registration
- Backend handles the on-chain transaction
- Registry contract: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`

### 5. Usage Metrics (Opt-in)
Anonymized usage reporting to improve recommendations for everyone.

- Reads local OpenClaw skill directory to count install days and usage frequency
- Reports only: skill name + usage count (no conversation content, no personal data)
- **Opt-in only** — never sends data without explicit user consent
- POST /api/metrics with minimal payload

## Security & Privacy

✅ **Local analysis** — Conversation text analyzed on your machine, never uploaded
✅ **Local Differential Privacy (ε=1.0)** — Spectrum scores noised via Laplace mechanism before transmission
✅ **SHA-256 fingerprint** — Conversation hashed locally; only irreversible hash stored for dedup
✅ **Minimal transmission** — Server receives personality type + approximate scores only
✅ **Minimal writes** — Writes only `~/.bloom/agent-id.json` (returning user token, 0600 permissions) and `bloom-discoveries.md` (local sync log). Never modifies session files or USER.md
✅ **Atomic file writes** — Uses tmp+rename pattern to prevent corruption
✅ **User-initiated** — Only runs when you explicitly invoke the skill
✅ **Opt-in metrics** — Usage data never sent without consent
✅ **Open source** — Full source at [github.com/bloomprotocol/bloom-discovery-skill](https://github.com/bloomprotocol/bloom-discovery-skill)

❌ Raw conversation text is **never** sent to any server
❌ Wallet private keys are **never** transmitted
❌ Personal identifiable information is **never** collected
❌ No background data collection — only runs on explicit invocation

## Triggers

- "generate my bloom identity"
- "create my identity card"
- "analyze me"
- "what's my builder type"
- "discover my personality"
- "create my bloom card"
- "find use cases for me"
- "verify my config"
- "claim my SBT"
- "what use cases match my skills"

## Data Sources

### Primary: USER.md + Conversation History
- **USER.md** — Declared role, tech stack, interests, working style. Injected as first-class text into the personality analyzer. Falls back gracefully if not present.
- **Conversation history** — Always available from OpenClaw sessions. Analyzes topics, interests, engagement patterns.
- **Requires: Minimum 3 messages** in your session. If less than 3 messages, the skill returns a clear error.

### Secondary: Installed Skills
- **~/.openclaw/skills/** — Scanned locally for use case verification. Never uploaded.

## Output

- Personality type (Visionary / Explorer / Cultivator / Optimizer / Innovator)
- Custom tagline and description
- MentalOS spectrum (Learning, Decision, Novelty, Risk — each 0-100)
- Hidden pattern insight + AI-era playbook
- Main categories and subcategories
- Matched use cases with verification status
- Recommended skills from the Bloom skill catalog (with match scores)
- Dashboard link at bloomprotocol.ai

## Technical Details

- **Version**: 4.0.1
- **Privacy**: LDP ε=1.0 + SHA-256 fingerprint
- **Analysis Engine**: MentalOS spectrum (4 dimensions) + category mapping
- **Primary Signal**: Conversation memory (~120 messages) + USER.md
- **Processing Time**: ~60 seconds (personality) + ~5 seconds (use case matching)
- **Output**: Personality card + use case matches + tool recommendations + dashboard URL
- **Network**: Base (mainnet) — configurable via NETWORK env var
- **On-chain**: ERC-8004 Identity Registry + BloomExclusivePass SBT

## Requirements

- Node.js 18+
- No API keys or secrets required — the skill works out of the box
- Optional environment variables:
  - `BLOOM_API_URL` — API URL (default: https://api.bloomprotocol.ai)
  - `DASHBOARD_URL` — Dashboard URL (default: https://bloomprotocol.ai)

## Installation

```bash
git clone https://github.com/bloomprotocol/bloom-discovery-skill.git
cd bloom-identity-skill
npm install
```

---

Built by [Bloom Protocol](https://bloomprotocol.ai)
