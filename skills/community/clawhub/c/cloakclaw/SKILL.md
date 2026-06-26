---
name: cloakclaw
description: >
  Automatic privacy proxy for AI conversations. Redacts sensitive data (names, companies,
  financials, SSNs, emails, phones, addresses, API keys, IPs, passwords, and 14 more types)
  from documents before sending to cloud LLMs, then restores originals in the response.
  24 entity types across 6 profiles (General, Legal, Financial, Email, Code, Medical).
  Use when: (1) user attaches a document (PDF, TXT, etc.), (2) user pastes sensitive text,
  (3) user mentions contracts, financials, HR docs, medical, or legal documents,
  (4) user explicitly asks for privacy/cloaking. Always-on by default.
  Requires: Node.js 22+, CloakClaw installed (`npm install -g cloakclaw`).
  Optional: Ollama for name/company detection (works without in regex-only mode).
  Optional: poppler for better PDF extraction (`brew install poppler`).
install: npm install -g cloakclaw
---

# CloakClaw — Always-On Privacy Proxy

## Prerequisites

```bash
# Required
npm install -g cloakclaw

# Optional but recommended
brew install poppler       # Better PDF text extraction
ollama pull qwen2.5:7b     # AI-powered name/company detection
```

Verify: `cloakclaw --version` should return `0.1.2` or higher.

## How It Works

1. **Detect**: When user sends a document or sensitive text, auto-detect the document type
2. **Cloak**: Run the cloaking engine (regex + local LLM) to replace sensitive entities with realistic fakes
3. **Send**: Forward cloaked text to the cloud LLM for analysis
4. **Decloak**: When response arrives, reverse all replacements to restore originals
5. **Deliver**: Send the restored response to user with a privacy footer

## Entity Types (24)

| Category | Types |
|----------|-------|
| Identity | People, Companies, Passports, Drivers License |
| Contact | Emails, Phones, Addresses |
| Financial | Dollars, Percentages, Accounts, Banks, SSNs |
| Legal | Case Numbers, Jurisdictions |
| Tech | IP Addresses, MAC Addresses, Passwords/Secrets, API Keys, URLs |
| Other | Crypto Wallets, GPS Coordinates, VIN Numbers, Medical IDs, Dates |

## Profiles (6)

- **general** — all 24 types (default for unknown documents)
- **legal** — contracts, NDAs, filings (10 types)
- **financial** — bank statements, P&L, investor docs (11 types)
- **email** — correspondence (10 types)
- **code** — .env files, configs, infra docs (9 types)
- **medical** — HIPAA-adjacent records (11 types)

## Auto-Detection Rules

**Always cloak (document attached):**
- PDF, TXT, MD, CSV, JSON, YAML, code files → auto-detect profile from content
- Legal keywords (agreement, contract, whereas, hereby) → `legal` profile
- Financial keywords (revenue, P&L, balance sheet, quarterly) → `financial` profile
- Code files (.env, .yaml, .json with secrets) → `code` profile
- Default for unrecognized → `general` profile

**Always cloak (sensitive content in text):**
- Contains SSN patterns (###-##-####)
- Contains dollar amounts > $1,000
- Contains multiple proper names + company names
- Contains IP addresses, API keys, or passwords
- User explicitly says "cloak", "private", "redact", or "protect"

**Skip cloaking:**
- Simple questions with no sensitive data
- User says "raw", "uncloak", "no cloak", or "cloakclaw off"

## Execution Flow

### Step 1: Cloak the document

```bash
node scripts/cloak.js --profile <general|legal|financial|email|code|medical> --input /path/to/file
```

Output JSON:
```json
{
  "sessionId": "a5cc1496-15b9-4b43-8506-3ea75dfe1304",
  "cloaked": "...cloaked text...",
  "entityCount": 20,
  "profile": "legal"
}
```

Or use the CLI directly:
```bash
cloakclaw cloak document.pdf --profile legal -o cloaked.txt
```

### Step 2: Send cloaked text to cloud LLM

Use the cloaked text as the document content. The user's question stays unchanged — only the document data is cloaked.

### Step 3: Decloak the response

```bash
node scripts/decloak.js --session <sessionId> --input /path/to/response.txt
```

Or CLI:
```bash
cloakclaw decloak -s <sessionId> -f response.txt
```

Output: restored text with original entities.

### Step 4: Deliver with privacy footer

Append to the response:
```
🔒 CloakClaw: {entityCount} entities protected | Profile: {profile} | Session: {sessionId_short}
```

## User Commands

- `cloakclaw off` — disable auto-cloaking for this session
- `cloakclaw on` — re-enable auto-cloaking
- `cloakclaw status` — show current settings and recent sessions
- `cloakclaw diff <sessionId>` — show what was cloaked

## Configuration

Config at `~/.cloakclaw/config.yaml`:

```yaml
ollama:
  url: http://localhost:11434
  model: qwen2.5:7b
```

### Recommended Models by RAM
| RAM | Model | Quality |
|-----|-------|---------|
| 8GB | qwen2.5:3b | Basic (regex does most work) |
| 16GB | qwen2.5:7b | Good |
| 32GB+ | qwen2.5:32b | Very good |
| 64GB+ | qwen2.5:72b | Excellent |

## Security

- AES-256-GCM encrypted mapping database
- Optional password protection (`cloakclaw password set`)
- Auto-expiry: sessions purged after 7 days
- Zero telemetry, zero cloud dependency for cloaking
- All processing runs locally

## ⚠️ Disclaimer

CloakClaw is NOT HIPAA, GDPR, SOC 2, PCI-DSS, or CCPA compliant. It is a best-effort privacy tool. Users are responsible for reviewing cloaked output before sharing.
