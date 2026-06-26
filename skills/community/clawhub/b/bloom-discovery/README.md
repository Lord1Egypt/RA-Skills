# Bloom Discovery Skill

**Don't browse 13,000 skills. Browse use cases.**

[![Version](https://img.shields.io/badge/version-4.0.0-blue)](https://github.com/bloomprotocol/bloom-discovery-skill)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-green)](https://openclaw.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-purple)](https://clawhub.ai/unicornbloom/bloom-discovery)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

---

## The Problem

| Without Bloom | With Bloom |
|--------------|------------|
| Browse 13,000 skills manually | Describe your intent, get matched use cases |
| Install skills one by one, hope they work together | Each use case = tested skill combination |
| No idea if your setup is complete | Verify config → see what's missing |
| No proof of your expertise | Claim SBT → on-chain verified identity |
| Recommendations based on popularity | Recommendations based on how you actually work |

---

## What It Does

### 1. Personality Analysis (MentalOS)

Reads your USER.md and conversation history to map your builder personality:

- **5 Types**: Visionary, Explorer, Cultivator, Optimizer, Innovator
- **4 Spectrums**: Learning (Try First ↔ Study First), Decision (Gut ↔ Analytical), Novelty (Early Adopter ↔ Proven First), Risk (All In ↔ Measured)
- **Hidden Patterns**: 6 detectors surface insights you might not see yourself
- **AI-Era Playbook**: Personalized leverage, blind spots, and next moves

```
/bloom
```

~60 seconds. No surveys. No auth.

### 2. Use Case Discovery

Intent-driven skill browsing. You say what you want to accomplish; Bloom matches you to curated use cases — each a tested combination of skills.

- Personality-aware ranking (novelty seekers → new use cases, risk-averse → skip DeFi)
- Keyword frequency threshold (≥ 3 mentions) filters noise
- Each use case comes with skill requirements and verification status

```
"find use cases for me"
```

### 3. Verify Configuration & Claim SBT

Scans your installed skills (`~/.openclaw/skills/`) and verifies your setup against use case requirements.

- Match percentage + missing capabilities
- Claim flow: verified config → mint SBT (on-chain proof)
- No wallet? Fallback to web link at bloomprotocol.ai
- SBT = soulbound token proving your verified configuration

```
"verify my config"
"claim my SBT"
```

### 4. Usage Metrics (Opt-in)

Anonymized reporting to improve recommendations for everyone.

- Reports only: skill name + usage frequency
- No conversation content. No personal data.
- **Opt-in only** — never sends data without your explicit consent

---

## Quick Start

### OpenClaw

```bash
clawhub install bloom-discovery
/bloom
```

### Developers

```bash
git clone https://github.com/bloomprotocol/bloom-discovery-skill.git
cd bloom-identity-skill
npm install
cp .env.example .env

# Run from session file
npx tsx scripts/run-from-session.ts \
  ~/.openclaw/agents/main/sessions/<SessionId>.jsonl \
  <userId>
```

---

## MentalOS Spectrum

| Spectrum | Low (0) | High (100) | Question |
|----------|---------|------------|----------|
| **Learning** | Try First | Study First | Jump in or read the docs? |
| **Decision** | Gut | Analytical | Instinct or methodical? |
| **Novelty** | Early Adopter | Proven First | Bleeding edge or battle-tested? |
| **Risk** | All In | Measured | Go big or hedge? |

## 5 Personality Types

| Type | Style |
|------|-------|
| **The Visionary** | High conviction + high intuition — backs bold ideas early |
| **The Explorer** | Low conviction + high intuition — experiments widely |
| **The Cultivator** | High contribution — builds communities and shares knowledge |
| **The Optimizer** | High conviction + low intuition — doubles down on what works |
| **The Innovator** | Low conviction + low intuition — spots patterns others miss |

---

## Security & Privacy

✅ **Local analysis** — Conversation text analyzed on your machine, never uploaded
✅ **Local Differential Privacy (ε=1.0)** — Spectrum scores noised via Laplace mechanism
✅ **SHA-256 fingerprint** — Conversation hashed locally; only irreversible hash stored
✅ **Minimal transmission** — Server receives personality type + approximate scores only
✅ **Minimal writes** — Only writes `~/.bloom/agent-id.json` (returning user token, 0600 perms) and `bloom-discoveries.md`. Never modifies session files or USER.md
✅ **Atomic file writes** — Uses tmp+rename pattern to prevent corruption
✅ **Input validation** — Regex guards on session IDs, Twitter handles, file paths, agent IDs
✅ **No shell injection** — All external commands use `execFile` (no shell interpolation)
✅ **Timeouts** — All network requests have 5–10s abort signals
✅ **Opt-in metrics** — Usage data never sent without consent
✅ **Open source** — Audit the algorithm yourself

❌ Raw conversation text **never** sent to any server
❌ Wallet private keys **never** transmitted
❌ No PII collection
❌ No background data collection
❌ File reads **restricted** to user's home directory

---

## Configuration

```bash
# Required
JWT_SECRET=your_secret_key_here

# Recommended
BLOOM_API_URL=https://api.bloomprotocol.ai
DASHBOARD_URL=https://bloomprotocol.ai
NETWORK=base-mainnet
```

See [.env.example](.env.example) for all options.

---

## Architecture

```
Conversation + USER.md
        │
        ▼
  ┌─────────────┐
  │  Personality │ ← Local analysis (LDP ε=1.0)
  │  Analyzer    │
  └──────┬──────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────────┐
│Use Case│ │Skill Recomm.│
│Matcher │ │  Pipeline   │
└───┬────┘ └──────┬─────┘
    │              │
    ▼              ▼
┌────────┐  ┌───────────┐
│Verify  │  │ Dashboard │
│& Claim │  │   Card    │
└────────┘  └───────────┘
```

---

## Links

- **Homepage**: [bloomprotocol.ai](https://bloomprotocol.ai)
- **ClawHub**: [clawhub.ai/unicornbloom/bloom-discovery](https://clawhub.ai/unicornbloom/bloom-discovery)
- **Source**: [github.com/bloomprotocol/bloom-discovery-skill](https://github.com/bloomprotocol/bloom-discovery-skill)
- **Dashboard**: [bloomprotocol.ai/agents](https://bloomprotocol.ai/agents)
- **Docs**: [bloomprotocol.ai/docs](https://bloomprotocol.ai/docs)

---

**Built by [Bloom Protocol](https://bloomprotocol.ai)**

*Agent-native intent economy curation platform.*

*Built with [@openclaw](https://openclaw.ai), [@coinbase](https://www.coinbase.com/cloud), and [@base](https://base.org)*
