---
name: autonomous-procurement-agent
description: "Enterprise procurement quote parsing and fraud detection. Use when: (1) A supplier quote arrives as messy plain-text, OCR scan, or SAP export, (2) Cross-platform invoice reconciliation is needed across CNY/USD/EUR, (3) B2B finance teams need real-time risk auditing on vendor submissions, (4) Approval escalation thresholds need to be enforced automatically. Handles non-standard formats with dual-engine AI (regex + GPT-4o fallback), F1/F2/F3 fraud detection, and Lemon Squeezy MoR subscription."
---

# Autonomous Procurement Agent

Stop overpaying. Stop missing fraud. Every week, procurement teams lose money because a supplier's quote arrived as a messy email, a merged-cell SAP export, or a PDF scan with OCR artifacts. The unit price got misread. The line math was wrong. Nobody caught it — until the invoice was already paid.

Autonomous Procurement Agent handles every format. Every currency. With fraud detection that actually blocks, not just warns.

---

## First-Use Initialisation

Before processing any quotes, configure your environment:

```bash
# Required in production — server refuses to start without this
export LS_WEBHOOK_SECRET="your_ls_webhook_secret"

# Optional: enables GPT-4o fallback for messy formats (plain-text, OCR scans).
# Without this, Engine 2 is skipped and only regex parsing runs.
# All parsing is LOCAL without this key.
export OPENAI_API_KEY="sk-..."

# Optional: override default ports and directories
export PARSER_DATA_DIR="$HOME/.procurement-agent-data"
export PROCU_WEBHOOK_PORT="3002"

# Start the webhook server (receives LS payment events → activates license)
node webhook-handler.js &
# → Listening on http://localhost:3002/webhook/lemon-squeezy
```

Never log raw quote content, vendor names, or API keys to stdout. The parser runs entirely locally unless `OPENAI_API_KEY` is set — in which case Privacy Shield scrubs all sensitive fields before any external call.

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| Supplier quote in plain-text or email | Parse with Engine 1 (regex, <50ms) |
| Invoice has merged cells or OCR artifacts | Engine 2 triggers automatically (if `OPENAI_API_KEY` set) |
| F1 math error detected on a line item | Line blocked → whole PO escalated to REVIEW |
| F2 price spike >20% above historical avg | CRITICAL alert → auto-block |
| F3 duplicate PO within 7 days | Warning logged → duplicate flagged |
| Circuit breaker trips 2 consecutive approver failures | Safety-Freeze → all POs held for manual approval |
| Lemon Squeezy payment confirmed | Webhook writes to `data/licenses.json` automatically |
| High-value PO (>$50,000) needs LLM hint | `generateLLMHint()` called with USD-normalised structure |
| Receiving a quote without API key | Engine 1 regex only; no external calls made |

---

## Installation

### Via ClawHub (recommended)

```bash
clawhub install autonomous-procurement-agent
```

### Manual

```bash
git clone https://github.com/arya-openclaw/autonomous-procurement-agent.git \
  ~/.openclaw/skills/autonomous-procurement-agent
cd ~/.openclaw/skills/autonomous-procurement-agent
npm install
```

### Lemon Squeezy Webhook Setup

1. Go to your Lemon Squeezy dashboard → Webhooks
2. Add endpoint: `https://your-domain.com/webhook/lemon-squeezy`
3. Copy the signing secret → set as `LS_WEBHOOK_SECRET`
4. For local dev, use ngrok: `ngrok http 3002`

> **No PayPal**: Lemon Squeezy handles global tax (VAT/GST included in price) and supports Payoneer / World First / Wise payouts. PayPal is not supported due to high dispute fees and China-market account ban risk.

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LS_WEBHOOK_SECRET` | **Yes (prod)** | — | HMAC-SHA256 signing secret from LS dashboard. Server **refuses to start** without it. |
| `OPENAI_API_KEY` | No | — | OpenAI key. Only needed for Engine 2 (GPT-4o fallback). Without it, all parsing is local. |
| `LS_PRO_VARIANT_ID` | No | `999` | Lemon Squeezy variant ID for Pro tier |
| `LS_ENT_VARIANT_ID` | No | `2999` | Lemon Squeezy variant ID for Enterprise tier |
| `PARSER_DATA_DIR` | No | `~/.procurement-agent-data` | Local directory for license DB + historical price baseline |
| `CB_THRESHOLD` | No | `2` | Circuit breaker failures before Safety-Freeze triggers |
| `PROCU_WEBHOOK_PORT` | No | `3002` | Webhook HTTP server port |
| `LS_STORE_ID` | No | — | Lemon Squeezy store ID for API calls |
| `LS_API_KEY` | No | — | Lemon Squeezy API key for license management |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model for LLM fallback (only when `OPENAI_API_KEY` is set) |
| `EXCHANGE_RATE_URL` | No | Fixed table | Optional live FX rate API endpoint |
| `HISTORICAL_PRICE_URL` | No | Built-in baseline | Optional API for F2 historical price baseline |
| `PROCU_ALLOWED_TIER` | No | — | Dev override — bypasses webhook signature check. **Do not use in production.** |

---

## Scenarios

**1. Cross-Platform Quote Reconciliation**
> A manufacturing firm receives quotes from three suppliers: one as a CSV export, one as a plain-text email ("qty 8 × $2,800 = $22,400"), one as a scanned PDF forwarded from a WhatsApp photo. Procurement Agent normalises all three to a structured comparison table in under a second.

**2. B2B Finance Real-Time Risk Audit**
> Finance receives a €47,000 PO from a long-term vendor. The line items all check out mathematically — but F2 flags that the unit price for the primary component is 34% above the 6-month average. The PO is auto-blocked before the CFO's signature is requested.

---

## How F1 / F2 / F3 Work

### F1 — Calculation Verification (Enterprise only)

Every line: `unit_price × quantity ≠ line_total` → **line blocked, PO escalated**.

> Supplier quotes "8 units × $2,800 = $22,400". You calculate the same. F1 checks it. Supplier made a $200 arithmetic error in their favour. You catch it before signing.

F1 runs automatically on every parse. No configuration required.

### F2 — Price Spike Detection (Enterprise only)

Current price > historical average × 1.20 → **CRITICAL alert + auto-block**.

> Ball bearings purchased at $12/unit for 6 months. New quote: $16/unit. F2 flags this 34% spike before approval.

Baseline import (one-time):
```bash
node self-healing-parser.js import-baseline ./historical-prices.json
```

### F3 — Duplicate Quote Detection (Enterprise only)

Same vendor + same total + within 7 days → **duplicate warning**.

> Two RFQs sent. Supplier responds twice. Finance processes both. F3 catches the duplicate before you pay twice.

---

## Architecture

```
Supplier quote (any format)
        │
        ▼
┌─────────────────────┐
│  Engine 1: Regex   │  ← JSON → HTML table → CSV → Plain text
│  (< 50ms)          │
└──────────┬──────────┘
           │
    confidence < 0.5
    or messy format
           │
           ▼
┌─────────────────────┐
│  Engine 2: GPT-4o  │  ← Only runs if OPENAI_API_KEY is set.
│  (opt-in LLM)       │     All parsing is LOCAL without this key.
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │  Risk Engine │
    │  F1 / F2 /F3 │  ← Enterprise only
    └──────┬──────┘
           │
    risk_score > 0.5
           │
           ▼
    STATUS: REJECTED_FOR_REVIEW
```

---

## Parsing Output Format

Every `parseQuote()` call returns a structured result. Here is the canonical schema:

```javascript
{
  "vendor_name":     "Acme Corp",
  "po_number":       "PO-2024-0041",
  "currency":        "USD",
  "line_items": [
    {
      "description":    "Industrial Ball Bearing",
      "quantity":       8,
      "unit_price":     2800.00,
      "line_total":     22400.00,
      "extracted_raw":  "8 × $2,800 = $22,400",
      "f1_flag":        false,      // true if unit_price × qty ≠ line_total
      "f2_flag":        false,      // true if >20% above historical avg
      "anomaly":        false,
      "reason":         null
    }
  ],
  "subtotal":        22000.00,
  "tax":             1980.00,
  "total":           23980.00,
  "confidence_score": 0.93,
  "parse_method":    "regex",      // "regex" | "llm_fallback" | "html_table" | "csv"
  "is_llm_fallback": false,
  "variant_detected": null,         // "V4" | "V8" | "V10" | null
  "anomaly_flags":   [],
  "fraud_flags":     [],
  "recommendation":  "AUTO_APPROVED", // "AUTO_APPROVED" | "REVIEW" | "REJECT"
  "safety_freeze":   false,
  "llm_error":       null
}
```

### Confidence Tiers

| Score | Tier | Meaning |
|-------|------|---------|
| ≥ 0.85 | `high` | Regex pipeline succeeded cleanly |
| ≥ 0.5 | `medium` | Partial parse; some fields recovered |
| < 0.5 | `low` | Unparseable; falls back to LLM or returns error |

---

## Privacy Shield (v1.0.0+)

Before any quote content is sent to the OpenAI API, it passes through a **Privacy Shield** — a local regex sanitiser that runs before the HTTP request is made. No external services are called; no data leaves your server at this stage.

| Field | Replacement | Example |
|-------|-------------|---------|
| Supplier/vendor name | `[VENDOR_MASKED]` | `"Acme Corp" → "[VENDOR_MASKED]"` |
| Monetary amounts | `[AMOUNT_MASKED]` | `"$1,234.56" → "[AMOUNT_MASKED]"` |
| Email / phone / fax | `[PII_REDACTED]` | `"john@corp.com" → "[PII_REDACTED]"` |
| Street addresses | `[PII_REDACTED]` | `"12 Main St, Shenzhen" → "[PII_REDACTED]"` |

**Trigger**: Privacy Shield is applied automatically whenever `OPENAI_API_KEY` is set and a quote requires GPT-4o fallback. It does not run in local-only regex mode.

GPT-4o receives enough structure to validate mathematical consistency and detect anomalies — but **cannot** see actual supplier prices or identities.

---

## License Tiers

| | Free | Pro ($9.99/mo) | Enterprise ($29.99/mo) |
|---|---|---|---|
| Quotes/month | 20 | 500 | Unlimited |
| Parse formats | JSON, HTML, CSV | All formats | All formats + LLM fallback |
| **F1 Calculation Check** | — | — | ✅ Built in |
| **F2 Price Spike Detection** | — | — | ✅ Built in |
| **F3 Duplicate Detection** | — | — | ✅ Built in |
| CNY→USD Normalization | — | ✅ | ✅ |
| Approval flow | — | — | ✅ |
| Safety-Freeze circuit breaker | — | — | ✅ |
| Historical price baseline | — | — | ✅ |
| Priority support | — | — | ✅ |

---

## Generic Setup (Other AI Agents)

For Claude Code, Codex, Copilot, or other agents:

```bash
mkdir -p ~/.openclaw/skills/autonomous-procurement-agent
git clone https://github.com/arya-openclaw/autonomous-procurement-agent.git \
  ~/.openclaw/skills/autonomous-procurement-agent
cd ~/.openclaw/skills/autonomous-procurement-agent
npm install
```

Parse a quote:
```bash
node self-healing-parser.js parse '<content>' [format] '{"email":"user@example.com"}'
```

---

## Periodic Review

Review flagged POs regularly:

```bash
# List POs with active risk flags
grep -r "REJECTED_FOR_REVIEW\|CRITICAL\|suspicious" \
  ~/.procurement-agent-data/logs/ 2>/dev/null | tail -20

# Check Safety-Freeze status
grep "Safety-Freeze" ~/.procurement-agent-data/logs/*.log 2>/dev/null | tail -5

# Check license DB health
cat ~/.procurement-agent-data/data/licenses.json | python3 -m json.tool
```

---

## Best Practices

1. **Always set `LS_WEBHOOK_SECRET` in production** — the server refuses to start without it. There is no bypass flag.
2. **`OPENAI_API_KEY` is opt-in** — without it, no quote content is ever sent to any external API.
3. **Import your historical price baseline before using F2** — without it, F2 spike detection uses a conservative built-in table.
4. **Keep `PARSER_DATA_DIR` backed up** — `data/licenses.json` is the source of truth for all license state.
5. **Do not commit `data/licenses.json` to git** — add it to `.gitignore`. License records are per-install, not per-repo.
6. **Use `PROCU_ALLOWED_TIER` only in local dev** — it bypasses webhook signature validation and must never be set in production.
7. **Webhook logs are sanitised automatically** — `sanitize()` redacts email addresses and API keys before writing logs.
8. **Review F2 spike alerts promptly** — F2 is silent until a spike is detected; configure alerts accordingly.

---

## Multi-Agent Support

### OpenClaw (primary platform)

**Activation**: Automatic skill loading via ClawHub or workspace injection.

**Detection**: Trigger keywords (`supplier quote`, `purchase order`, `vendor risk`, `price spike`, `fraud detection`, `approval escalation`, `safety freeze`).

### Claude Code / Codex

**Activation**: Direct invocation or workspace injection.

**Setup**: Copy skill to `~/.openclaw/skills/autonomous-procurement-agent`, then:
```bash
export LS_WEBHOOK_SECRET="your_secret"
node webhook-handler.js &
```

**Detection**: Chat triggers listed above.

### GitHub Copilot

**Activation**: Manual prompt — reference the skill directly in conversation.

**Setup**: Add to `.github/copilot-instructions.md`:
```markdown
## Procurement Fraud Detection

When reviewing vendor quotes or purchase orders, use:
~/.openclaw/skills/autonomous-procurement-agent/self-healing-parser.js

Set OPENAI_API_KEY for LLM fallback on messy formats.
```

### Agent-Agnostic Guidance

Regardless of agent, apply Autonomous Procurement Agent when:

1. **A supplier quote arrives in a non-standard format** — plain-text, merged-cell spreadsheet, OCR scan.
2. **Multiple currencies need to be compared** — CNY, USD, EUR reconciliation.
3. **A high-value PO needs validation** — F1 catches math errors; F2 catches price spikes.
4. **Duplicate invoices are suspected** — F3 detects same-vendor same-total within 7 days.
5. **Approval thresholds need to be enforced automatically** — Safety-Freeze on circuit breaker trip.
