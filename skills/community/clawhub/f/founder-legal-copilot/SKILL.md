---
name: founder-legal-copilot
description: Legal copilot that guides founders from incorporation to exit with 27 legal deliverables across 5 startup phases
version: 1.0.0
homepage: https://legalkit.legal
author: Danillo Costa
tags: [legal, founders, startup, term-sheet, safe, nda, incorporation, fundraising, m&a, due-diligence]
providers: [friendliai]
plugins: [redis-agent-memory, civic-nexus]
mcpServers: [apify]
---

# Founder Legal Copilot

A legal intelligence system for startup founders. Covers 27 legal deliverables across 5 startup phases — from incorporation to exit — using RAG-grounded analysis on verified legal templates from YC, NVCA, and Orrick.

> **Disclaimer:** This skill produces educational legal analysis and document drafts. It is not a substitute for advice from a licensed attorney. Always have a qualified lawyer review documents before signing.

---

## When to Use

Use this skill when a founder needs to:

- Generate a SAFE note for a pre-seed round quickly and accurately
- Review a contract for hidden risks before signing
- Run a legal health check before a fundraise or acquisition conversation
- Conduct lightweight due diligence on a counterparty, acquirer, or key hire

Do **not** use this skill for:

- Court filings or litigation strategy
- Tax advice (refer to a CPA)
- Employment disputes in progress
- Regulated industries (fintech licenses, healthcare HIPAA specifics, securities broker-dealer)

---

## Prerequisites

### Environment Variables

Copy `.env.example` to `.env` and populate:

```bash
cp .env.example .env
```

Required keys:

| Variable | Purpose |
|---|---|
| `FRIENDLIAI_API_KEY` | Primary inference (GLM-5 via Friendly.ai) |
| `CONTEXTUAL_AI_API_KEY` | RAG-grounded contract analysis |
| `APIFY_API_TOKEN` | Live SEC/corporate records scraping |
| `REDIS_URL` | Persistent deal memory across sessions |
| `ELEVENLABS_API_KEY` | Voice narration (optional) |
| `CIVIC_CLIENT_ID` | Auth and PII scrubbing |

### OpenClaw Plugins

Install required plugins before running:

```bash
openclaw plugin install redis-agent-memory
openclaw plugin install civic-nexus
openclaw mcp add apify https://mcp.apify.com
```

---

## Workflow

### Feature 1: SAFE Generator

Generates a complete, execution-ready Simple Agreement for Future Equity based on the YC Post-Money SAFE template (2018 revision).

**Input:**
```
/safe-generator
  --amount 500000
  --valuation-cap 8000000
  --discount 20
  --mfn true
  --pro-rata true
  --company "Acme Corp (Delaware C-Corp)"
  --investor "Sequoia Scout Fund"
```

**Steps:**
1. Skill validates entity type (must be Delaware C-Corp for standard SAFE)
2. Contextual AI grounds the generation against the YC template library
3. Parameters are injected into `templates/safe-post-money.md`
4. Risk flags are surfaced: unusual caps, missing pro-rata, MFN conflicts
5. Output is rendered as a complete markdown document ready for PDF export
6. Session data is stored in Redis for future reference (deal history)

**Output:** Complete SAFE document + risk summary + recommended next steps

**Common flags:**
- `--mfn`: Most Favored Nation clause (standard for first checks)
- `--pro-rata`: Pro-rata rights in next round
- `--discount`: Discount rate (0-30%; typical: 15-20%)

---

### Feature 2: Contract Reviewer

Analyzes any contract for founder-hostile terms. Compares against YC, NVCA, and Orrick baseline templates.

**Input:**
```
/contract-review --file contract.pdf
# or pipe text directly
/contract-review --text "$(cat term-sheet.md)"
```

**Steps:**
1. Document is parsed and chunked
2. Civic plugin scrubs any PII before sending to inference
3. Contextual AI compares against standard templates (Cooley GO, Orrick)
4. Eight risk dimensions are scored independently
5. Output JSON includes risk level, flagged clauses, and plain-English explanations
6. Recommendations prioritized by severity (red > yellow > green)

**Risk dimensions analyzed:**
- Liability caps and indemnification scope
- Termination triggers and notice periods
- IP ownership and work-for-hire language
- Non-compete and non-solicitation scope
- Governing law and jurisdiction
- Arbitration vs. litigation election
- Assignment rights (change of control)
- Representations and warranties

**Output format:**
```json
{
  "risk_level": "yellow",
  "score": 68,
  "flags": [...],
  "recommendations": [...],
  "confidence": 0.91
}
```

---

### Feature 3: Legal Health Check

Runs a 25-item legal checklist against the founder's described company state. Produces a scored report with prioritized remediation steps.

**Input:**
```
/health-check --stage seed --jurisdiction delaware
```

The skill will interactively ask about each item, or accept a pre-filled JSON:

```
/health-check --answers health-answers.json
```

**Checklist categories:**
- Entity and formation (items 1-5)
- Founder agreements and equity (items 6-10)
- IP protection (items 11-14)
- Compliance and governance (items 15-20)
- Fundraising readiness (items 21-25)

**Scoring:**
- Each item: 0-4 points
- Total: /100
- Bands: Critical (0-40), Needs Work (41-60), Good (61-80), Excellent (81-100)

**Output:** Scored report, prioritized to-do list, estimated attorney cost to remediate each gap

---

### Feature 4: Due Diligence

Pulls live corporate data via Apify MCP (SEC EDGAR, state records, bankruptcy databases) and produces a structured diligence report.

**Input:**
```
/due-diligence
  --entity "Acme Corp"
  --state "Delaware"
  --ein "12-3456789"
  --type acquirer
```

**Steps:**
1. Apify scrapes SEC EDGAR for any public filings
2. State corporation database queried for active status, officers, registered agent
3. Bankruptcy and UCC lien databases checked
4. Tax lien records reviewed
5. All findings compiled into structured report with red flag prioritization
6. Redis stores the report for follow-up sessions

**Data sources used:**
- SEC EDGAR full-text search
- Delaware Division of Corporations
- PACER bankruptcy records (via Apify)
- UCC filing databases

**Output:** Structured diligence report with findings, red flags (sorted by severity), and recommended follow-up actions

---

## Patterns

### Deal Memory (Redis)

Every SAFE generated and contract reviewed is stored in the Redis memory plugin with the deal name as the key. To recall a previous deal:

```
/recall-deal --name "Acme Series A"
```

This enables multi-session deal tracking without re-uploading documents.

### Multilingual Output

All four features support output in English, Spanish, Portuguese, and Mandarin:

```
/safe-generator ... --lang pt
/contract-review ... --lang es
```

### Batch Mode

Review multiple contracts in a single session:

```
/contract-review --batch contracts/ --output reports/
```

### Voice Narration

Any report can be narrated via ElevenLabs for accessibility or async review:

```
/health-check ... --voice --voice-id "rachel"
```

---

## Troubleshooting

### "Contextual AI rate limit exceeded"

The RAG analysis endpoint has a per-minute limit. Add `--no-rag` to fall back to base model analysis (lower accuracy):

```
/contract-review --file contract.pdf --no-rag
```

### "Apify actor timeout"

SEC EDGAR and state database scrapes can time out on heavily loaded actors. Retry with `--timeout 120`:

```
/due-diligence ... --timeout 120
```

### "Redis connection refused"

Check `REDIS_URL` in `.env`. For local development, run:

```bash
docker run -d -p 6379:6379 redis:alpine
```

### "SAFE generation failed: invalid entity type"

SAFEs require a Delaware C-Corp. If the company is an LLC or S-Corp, the skill will halt and recommend conversion before fundraising.

### "Civic PII scrub removed too much content"

Adjust the scrub sensitivity in `skill/config.json` under `civic.sensitivity`. Default is `medium`. Set to `low` for internal-only analysis where PII retention is acceptable.

---

## Legal Sources

All templates and analysis are grounded against verified sources. See `skill/data/sources.json` for the complete list. Primary references:

- [YC SAFE Documents](https://ycombinator.com/documents)
- [NVCA Model Legal Documents](https://nvca.org/model-legal-documents)
- [Cooley GO](https://cooleygo.com)
- [Orrick Start-Up Forms Library](https://orrick.com/practices/startups)
- [Series Seed](https://seriesseed.com)
