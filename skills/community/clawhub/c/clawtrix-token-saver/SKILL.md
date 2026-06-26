---
name: token-saver
description: >
  Reduce Claude API token consumption and track spending. Diagnoses waste
  patterns, recommends optimizations, and generates cost reports. Use when:
  (1) User asks about "tokens", "cost", "spending", "expensive", "cheaper",
  "optimize prompt", "token budget", or "save tokens". (2) Spending spike
  detected in usage logs. (3) Starting a new agent setup and want to configure
  cost-efficient model routing. (4) After adding new skills and want to check
  system prompt size impact. Never installs or modifies config without showing
  a diff and getting confirmation first.
metadata:
  openclaw:
    emoji: 💰
    requires:
      env: ["ANTHROPIC_API_KEY"]
---

# Token Saver

Your Claude API bill is mostly avoidable waste. Heartbeats running on Sonnet. Extended thinking on calendar checks. MEMORY.md that hasn't been trimmed in weeks. Token Saver finds the waste, quantifies it, and helps you fix it.

Free. No backend. No auth required.

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| "How much am I spending?" | Run Step 1 — fetch usage stats |
| Spending spike | Run Step 2 — diagnose waste patterns |
| "Make it cheaper" | Run Step 3 — generate ranked recommendations |
| Want to apply fixes | Run Step 4 — show diff, get confirmation, apply |
| Weekly cost check | Run Step 5 — generate cost report |

---

## Step 1 — Fetch Current Usage

Pull recent usage from the Anthropic API:

```bash
# Get usage for the last 7 days
curl -s "https://api.anthropic.com/v1/usage?days=7" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" | jq '.'
```

If the usage endpoint is unavailable, estimate from conversation history:
- Count turns in current session
- Estimate tokens per turn by model (Haiku: ~500, Sonnet: ~1500, Opus: ~3000)
- Multiply by per-token cost (see pricing table below)

**Claude Pricing (March 2026):**

| Model | Input (per 1M) | Output (per 1M) | Best for |
|-------|----------------|-----------------|----------|
| claude-opus-4-6 | $15.00 | $75.00 | Complex reasoning, multi-file edits |
| claude-sonnet-4-6 | $3.00 | $15.00 | Daily driver: email, research, code |
| claude-haiku-4-5 | $0.80 | $4.00 | Heartbeats, simple lookups, sub-agents |

Extended thinking tokens are billed at the output rate.

---

## Step 2 — Diagnose Waste Patterns

Check for each of these patterns in order:

### Pattern 1: Expensive model on heartbeats
**Signal:** Agent config sets Sonnet or Opus as default; heartbeat runs 48x/day.
**Cost:** ~$4.30/month extra vs Haiku baseline.

```bash
# Check openclaw.json for heartbeat model config
cat openclaw.json 2>/dev/null | jq '.models // .model // "not configured"'
```

Flag if default model ≠ `claude-haiku-4-5` and no heartbeat-specific override exists.

### Pattern 2: Extended thinking on simple tasks
**Signal:** Thinking enabled globally; agent handles calendar, weather, simple lookups.
**Cost:** $3–15/month depending on budget and frequency.

```bash
# Check for thinking config
cat openclaw.json 2>/dev/null | jq '.thinking // "not configured"'
```

Flag if `thinking.enabled: true` with no task-type restrictions.

### Pattern 3: Bloated system prompt
**Signal:** SOUL.md + AGENTS.md + MEMORY.md + all installed skills > 5,000 tokens combined.
**Cost:** 10–20% on every single API call.

```bash
# Estimate token counts (rough: 4 chars ≈ 1 token)
wc -c SOUL.md AGENTS.md MEMORY.md 2>/dev/null
# Estimate: bytes / 4 = approximate tokens
```

Flag if total > ~20,000 characters (≈5,000 tokens).

### Pattern 4: Uncompacted conversation history
**Signal:** Session has 40+ turns; history tokens compound on every new message.
**Cost:** 5–15% overhead on long sessions.

Count conversation turns in context. Flag if > 40 turns without `/compact`.

### Pattern 5: Redundant skills loaded
**Signal:** Multiple skills installed that overlap in function (e.g., 3 research tools).
**Cost:** Each skill adds ~100–500 characters to system prompt on every turn.

```bash
# List installed skills
openclaw skills list 2>/dev/null
```

Flag if > 8 skills installed or if obvious overlap exists.

---

## Step 3 — Generate Ranked Recommendations

After diagnosis, output a prioritized fix list. Format:

```
─────────────────────────────────────
TOKEN SAVER REPORT — [DATE]
─────────────────────────────────────

WASTE DETECTED:

  🔴 HIGH IMPACT — Heartbeats running on Sonnet
     Estimated waste: ~$4.00/month
     Fix: Set heartbeat model to claude-haiku-4-5 in openclaw.json

  🟡 MEDIUM IMPACT — Extended thinking enabled globally
     Estimated waste: ~$8.00/month
     Fix: Restrict thinking to tasks with complexity: high flag

  🟡 MEDIUM IMPACT — System prompt at ~6,200 tokens
     Estimated waste: ~12% on all calls
     Fix: Trim MEMORY.md — remove entries older than 14 days

  🟢 LOW IMPACT — 11 skills installed, possible overlap
     Estimated waste: ~$1.50/month
     Fix: Audit and disable rarely-used skills in openclaw.json

─────────────────────────────────────
Total estimated monthly savings if all fixes applied: ~$13.50
─────────────────────────────────────
```

---

## Step 4 — Apply Fixes (With Confirmation)

**NEVER edit files without showing the diff and getting explicit confirmation.**

### Fix A: Model routing in openclaw.json

Show proposed change:
```json
// BEFORE:
{ "model": "claude-sonnet-4-6" }

// AFTER:
{
  "model": "claude-sonnet-4-6",
  "models": {
    "heartbeat": "claude-haiku-4-5",
    "subagent": "claude-haiku-4-5",
    "reasoning": "claude-sonnet-4-6"
  }
}
```

Ask: "Apply this change to openclaw.json? (yes/no)"

Only apply if confirmed.

### Fix B: Trim MEMORY.md

Identify entries older than 14 days. Show lines to remove. Ask for confirmation before deleting.

### Fix C: Disable extended thinking for simple tasks

Check openclaw.json thinking config. Show proposed config change. Confirm before applying.

---

## Step 5 — Generate Cost Report

Run the cost report script if available:

```bash
python3 skills/token-saver/scripts/token_report.py 2>/dev/null
```

If script unavailable, generate inline estimate:

```
─────────────────────────────────────
COST ESTIMATE — Week of [DATE]
─────────────────────────────────────

Model breakdown (estimated):
  claude-sonnet-4-6   ~$18.40  (main agent turns)
  claude-haiku-4-5    ~$0.80   (heartbeats — if configured)
  Extended thinking   ~$6.20   (thinking turns)

Top cost drivers:
  1. Heartbeats        ~48/day × 7 days = 336 calls
  2. Research tasks    ~12 calls with extended thinking
  3. System prompt     ~4,800 tokens × all calls

Projected monthly: ~$109
─────────────────────────────────────
```

---

## Model Routing Reference

Recommended openclaw.json configuration for cost efficiency:

```json
{
  "models": {
    "default": "claude-sonnet-4-6",
    "heartbeat": "claude-haiku-4-5-20251001",
    "subagent": "claude-haiku-4-5-20251001",
    "reasoning": "claude-sonnet-4-6"
  },
  "thinking": {
    "enabled": true,
    "budgetTokens": 4000,
    "taskFilter": ["complexity:high", "type:debug", "type:architecture"]
  }
}
```

Typical savings vs all-Sonnet baseline: **50–70% reduction** with no quality loss on daily tasks.

---

## Privacy

Token Saver reads local files only (openclaw.json, MEMORY.md, SOUL.md). It calls the Anthropic usage API with your own API key. No data leaves your environment except to Anthropic's own endpoint.

---

## Version

v0.1.0 — 2026-03-31 — Initial release. Waste detection, ranked recommendations, safe apply with confirmation, cost reports.
