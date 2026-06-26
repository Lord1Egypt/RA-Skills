---
name: feishu-group-memory
description: "Extract and store structured information from Feishu group messages, then query it and get AI-generated insights. Use when the user wants to: record what's been discussed in a group, look up a customer or project status, get a summary of recent activity, or ask for advice based on chat history. Supports built-in industry knowledge packs (sales, customer service, legal, project management) and custom packs generated from a plain-language description. Read operations are free; analysis and advice are billed per call via SkillPay."
homepage: https://github.com/your-github/feishu-group-memory
metadata: {"clawdbot":{"emoji":"🧠","files":["scripts/*","industries/*","templates/*"]}}
---

# Feishu Group Memory

## Architecture

Scripts handle **data only** — no LLM calls inside scripts:
- `onboarding.py` — read/write industry knowledge pack config
- `listener.py` — fetch raw messages from Feishu; save analyzed records
- `query.py` — keyword search over stored records
- `billing.py` — SkillPay charge/balance/payment-link

**All AI analysis is done by you** (the OpenClaw model): deciding what to record, extracting structured fields, generating advice, writing summaries.

---

## Quick Reference

| Operation | Script | Billed |
|-----------|--------|--------|
| Check industry config | `onboarding.py check` | Free |
| Load built-in industry pack | `onboarding.py setup --industry` | Free |
| Save custom industry pack | `onboarding.py save --content` | Free |
| Find group by name | `listener.py find_chat --name` | Free |
| Fetch raw messages | `listener.py fetch_raw` | Free |
| Save analyzed records | `listener.py save_records` | Free |
| Search records | `query.py search` | Free |
| List records by period | `query.py list_records` | Free |
| Fetch + analyze messages | (fetch_raw → you analyze → save_records) | 0.005 USDT |
| Get AI advice | (query → you advise) | 0.003 USDT |
| Generate summary report | (list_records → you summarize) | 0.005 USDT |

---

## First Use: Onboarding

At the start of every session, check whether an industry pack is configured:

```bash
python3 {baseDir}/scripts/onboarding.py check --workspace ~/.openclaw/workspace
```

- `{"configured": true, "context": "..."}` → load the `context` field and proceed
- `{"configured": false}` → run onboarding before anything else

### Onboarding conversation

Ask the user:

> "Before we start, I'd like to understand what your group is mainly used for so I can record and analyze the right things.
>
> Choose one, or describe it in your own words:
> 1. 📈 Sales tracking (leads, quotes, deals)
> 2. 🎧 Customer support (tickets, issues, complaints)
> 3. ⚖️ Legal matters (contracts, risks, cases)
> 4. 📋 Project management (tasks, milestones, blockers)
> 5. ✍️ Describe my own use case"

### Saving the config

**Built-in industry (options 1–4):**
```bash
python3 {baseDir}/scripts/onboarding.py setup \
  --industry sales \
  --workspace ~/.openclaw/workspace
```
Valid slugs: `sales` / `customer-service` / `legal` / `project`

**Custom description (option 5):**

Using the user's description and the template at `{baseDir}/templates/context-template.md`, **generate the knowledge pack yourself**, then save it:
```bash
python3 {baseDir}/scripts/onboarding.py save \
  --content "YOUR GENERATED CONTENT" \
  --workspace ~/.openclaw/workspace
```

Confirm with the user: "Got it! I'll use this context going forward. Which group would you like me to start recording?"

---

## Feature: Record Group Messages

**Trigger:** "record X group", "fetch messages from X", "capture what's been discussed in X"

### Step 1 — Find the group
```bash
python3 {baseDir}/scripts/listener.py find_chat --name "KEYWORD"
```
If multiple results, show them and ask the user to pick one.

### Step 2 — Fetch raw messages
```bash
python3 {baseDir}/scripts/listener.py fetch_raw \
  --chat_id CHAT_ID \
  --limit 100 \
  --workspace ~/.openclaw/workspace
```
Returns an array of `{msg_id, time, sender, text}` objects.

### Step 3 — You analyze
Using the loaded industry knowledge pack (from `onboarding check`), go through each message and decide:
- Is it worth recording?
- What category does it belong to?
- Who or what is the key entity (person, company, project)?
- What structured fields can be extracted?
- What is the urgency (`high` / `medium` / `low`)?

### Step 4 — Save the records
```bash
python3 {baseDir}/scripts/listener.py save_records \
  --chat_id CHAT_ID \
  --workspace ~/.openclaw/workspace \
  --records '[{"msg_id":"...","time":"...","sender":"...","raw_text":"...","category":"...","key_entity":"...","summary":"...","fields":{...},"urgency":"high"}]'
```

### Step 5 — Report to user
Summarize what was found, e.g.:
> "Analyzed 100 messages. Saved 12 items:
> - 3 customer intent signals (Li, Wang, Chen)
> - 5 follow-up actions
> - 4 pricing discussions
>
> 2 high-urgency items — want me to walk through them?"

### Billing
```bash
python3 {baseDir}/scripts/billing.py charge \
  --user_id USER_ID --amount 0.005 --label "message analysis"
```
If `payment_required` is returned, show the top-up link and stop.

---

## Feature: Query Records

**Trigger:** "how is Wang doing", "what happened with Acme last week", "show me recent follow-ups"

```bash
python3 {baseDir}/scripts/query.py search \
  --query "KEYWORD" \
  --workspace ~/.openclaw/workspace
```

Returns matching records as raw JSON. **You** turn them into a natural-language answer, e.g.:
> "Here's what I have on Wang (Wang Zong):
> - Jan 15: Said he can sign next week (high priority)
> - Jan 12: Asked about discount options, still considering
>
> Last contact was 3 days ago — worth reaching out today."

No charge for queries.

---

## Feature: AI Advice

**Trigger:** "how should I follow up with X", "give me some advice", "help me think through this"

First, search for relevant records:
```bash
python3 {baseDir}/scripts/query.py search \
  --query "KEYWORD" \
  --workspace ~/.openclaw/workspace
```

Then reload the industry pack if needed:
```bash
python3 {baseDir}/scripts/onboarding.py check --workspace ~/.openclaw/workspace
```

**Using the "Advice Templates" section of the knowledge pack and the retrieved records, give the user concrete, actionable advice directly.**

```bash
python3 {baseDir}/scripts/billing.py charge \
  --user_id USER_ID --amount 0.003 --label "AI advice"
```

---

## Feature: Summary Report

**Trigger:** "summarize today", "weekly report", "what happened this week"

```bash
python3 {baseDir}/scripts/query.py list_records \
  --period today|week|all \
  --workspace ~/.openclaw/workspace
```

**You write the summary.** Example structure:

> **Weekly Summary (Jan 13–19)**
>
> 28 items recorded across 7 customers.
>
> **Action required (3)**
> - Li Zong: ready to sign — prepare draft contract
> - Wang Zong: price sticking point — request special approval
>
> **By category**
> - Customer intent: 12 | Follow-ups: 8 | Pricing: 5 | Other: 3
>
> **Suggestion:** 2 customers haven't been contacted in 5+ days.

```bash
python3 {baseDir}/scripts/billing.py charge \
  --user_id USER_ID --amount 0.005 --label "summary report"
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No industry pack configured | Run onboarding first |
| Group not found | "I couldn't find a group called 'X'. Could you give me the full name?" |
| No records yet | "Nothing recorded yet. Want me to fetch messages from that group now?" |
| `payment_required` | Show the top-up link from `message` field, stop, wait for user |
| Missing Feishu credentials | Ask user to configure `channels.feishu.accounts` in `openclaw.json` |
