---
name: agent-memory-manager
description: >
  Gives the agent persistent, structured long-term memory across sessions.
  Organizes memory by project, client, trade, and domain. The agent never
  forgets what worked, who it talked to, what decisions were made, or what
  it learned. Use when the agent needs to remember context between sessions,
  retrieve past decisions, update client records, log trade outcomes, or
  build a knowledge base that compounds over time.
version: 1.0.0
author: Agent
license: MIT
metadata:
  openclaw:
    emoji: "🧠"
    security_level: L1
    always: false
    required_paths:
      read:
        - /workspace/memory/
        - /workspace/memory/index.json
        - /workspace/memory/clients/
        - /workspace/memory/projects/
        - /workspace/memory/trades/
        - /workspace/memory/knowledge/
        - /workspace/.learnings/LEARNINGS.md
      write:
        - /workspace/memory/
        - /workspace/memory/index.json
        - /workspace/memory/clients/
        - /workspace/memory/projects/
        - /workspace/memory/trades/
        - /workspace/memory/knowledge/
        - /workspace/.learnings/LEARNINGS.md
        - /workspace/AUDIT.md
    network_behavior:
      makes_requests: false
      uses_agent_telegram: false
    requires:
      bins:
        - python3
---

# Agent Memory Manager — Persistent Structured Memory

> "The palest ink is better than the best memory." — Chinese proverb
> "Compound interest works on knowledge too." — Agent principle

An agent without memory is an agent that starts from zero every session.
This skill gives the agent a **brain that persists** — organized, searchable,
and always growing. Every client, every trade, every decision, every lesson
is stored and retrievable in milliseconds.

---

## Why This Skill Exists

```
WITHOUT this skill:
  Session 1 → Agent learns client X prefers email over LinkedIn
  Session 2 → Agent contacts client X via LinkedIn → friction
  Session 3 → Agent doesn't know trade Y already failed once
  Session 4 → Agent repeats the same mistake

WITH this skill:
  Session 1 → Agent learns client X prefers email → stored
  Session 2 → Agent retrieves client X profile → uses email → ✅
  Session 3 → Agent checks trade Y history → sees it failed → adapts
  Session 4 → Agent builds on past wins, avoids past mistakes
```

**Memory compounds. Every session makes the agent smarter.**

---

## Memory Architecture — 4 Domains

```
/workspace/memory/
├── index.json              ← master index of all memory files
├── clients/                ← one file per contact/prospect/client
│   ├── [slug].json
│   └── ...
├── projects/               ← one file per active or archived project
│   ├── [slug].json
│   └── ...
├── trades/                 ← one file per trade or position
│   ├── [slug].json
│   └── ...
└── knowledge/              ← domain knowledge that accumulates
    ├── acquisition.md
    ├── trading.md
    ├── content.md
    ├── market_signals.md
    └── product.md
```

---

## Memory Operations — How the Agent Uses This Skill

### REMEMBER — Store new information

```
Triggers:
  → After any client interaction (email reply, LinkedIn message, call)
  → After any trade opened or closed
  → After any campaign result
  → After any decision made
  → After any lesson learned
  → After any new market insight from agent-shark-mindset

Command:
  python3 /workspace/memory/scripts/memory_manager.py remember \
    --domain clients \
    --id "jean-dupont" \
    --data '{"last_contact": "2026-03-16", "preferred_channel": "email"}'
```

### RECALL — Retrieve stored information

```
Triggers:
  → Before contacting any prospect (check if already in memory)
  → Before opening a trade (check if similar trade was tried before)
  → Before writing content (check what worked in the past)
  → When principal asks "do you remember [X]?"
  → Before any weekly report (pull relevant context)

Command:
  python3 /workspace/memory/scripts/memory_manager.py recall \
    --domain clients \
    --id "jean-dupont"
```

### SEARCH — Find memory by keyword

```
Triggers:
  → "What do we know about [topic]?"
  → "Have we ever contacted someone at [company]?"
  → "What trades did we try in [market]?"

Command:
  python3 /workspace/memory/scripts/memory_manager.py search \
    --query "cold email B2B SaaS"
```

### UPDATE — Enrich existing memory

```
Triggers:
  → Status change (prospect → client, lead → qualified)
  → New interaction with known contact
  → Trade closed (add outcome to trade record)
  → Project milestone reached

Command:
  python3 /workspace/memory/scripts/memory_manager.py update \
    --domain clients \
    --id "jean-dupont" \
    --field "status" \
    --value "client"
```

### FORGET — Remove or archive outdated memory

```
Triggers:
  → Contact explicitly asked to be removed
  → Trade archived (> 90 days closed)
  → Project completed and archived

Command:
  python3 /workspace/memory/scripts/memory_manager.py archive \
    --domain clients \
    --id "jean-dupont"
```

---

## Memory Schemas — What Gets Stored

### Client / Prospect record

```json
{
  "id": "jean-dupont",
  "slug": "jean-dupont",
  "domain": "clients",
  "created_at": "2026-03-16",
  "updated_at": "2026-03-16",
  "status": "prospect",
  "profile": {
    "name": "Jean Dupont",
    "company": "Acme SaaS",
    "role": "CTO",
    "email": "jean@acme.io",
    "linkedin": "linkedin.com/in/jeandupont",
    "location": "Paris, FR",
    "icp_match": "b2b-decision-maker"
  },
  "preferences": {
    "preferred_channel": "email",
    "best_time": "Tuesday morning",
    "language": "French",
    "topics_of_interest": ["AI automation", "agent systems"]
  },
  "interactions": [
    {
      "date": "2026-03-10",
      "channel": "cold_email",
      "type": "outreach",
      "subject": "saw your article on AI agents",
      "outcome": "no_reply"
    },
    {
      "date": "2026-03-14",
      "channel": "linkedin",
      "type": "connection",
      "outcome": "accepted"
    }
  ],
  "notes": "Very active on LinkedIn about AI. Posted about automation costs last week.",
  "buying_signals": ["published AI content", "hiring ML engineers"],
  "next_action": "LinkedIn message D+2 after connection",
  "next_action_date": "2026-03-16",
  "value_potential_eur": 500,
  "tags": ["saas", "cto", "ai-interested", "paris"]
}
```

### Trade record

```json
{
  "id": "BTC-long-20260316",
  "slug": "btc-long-20260316",
  "domain": "trades",
  "created_at": "2026-03-16",
  "updated_at": "2026-03-16",
  "status": "closed",
  "asset": "BTC/USDT",
  "direction": "long",
  "entry_price": 82500,
  "exit_price": 85200,
  "size_usdt": 200,
  "pnl_usdt": 6.54,
  "pnl_pct": 3.27,
  "strategy": "momentum_breakout",
  "timeframe": "4h",
  "entry_reason": "RSI oversold + volume spike + shark-mindset signal",
  "exit_reason": "target reached",
  "market_context": "BTC breaking ATH resistance zone",
  "lessons": "Entry timing was slightly early — wait for candle close confirmation",
  "tags": ["btc", "momentum", "4h", "win"]
}
```

### Project record

```json
{
  "id": "veritas-newsletter-launch",
  "slug": "veritas-newsletter-launch",
  "domain": "projects",
  "created_at": "2026-03-01",
  "updated_at": "2026-03-16",
  "status": "active",
  "name": "Veritas Corporate Newsletter",
  "objective": "Build a 1000-subscriber base generating €2K/month",
  "phase": 1,
  "milestones": [
    { "name": "First 100 subscribers", "status": "done", "date": "2026-03-10" },
    { "name": "First paid subscriber", "status": "pending", "date": null }
  ],
  "decisions": [
    {
      "date": "2026-03-05",
      "decision": "Use Substack over Brevo for initial launch",
      "reason": "Lower friction, built-in discovery",
      "type": "two-way-door"
    }
  ],
  "metrics": {
    "subscribers": 87,
    "open_rate_pct": 42,
    "revenue_eur": 0
  },
  "next_action": "Publish weekly edition Thursday",
  "tags": ["newsletter", "content", "substack"]
}
```

### Knowledge entry

```markdown
# knowledge/acquisition.md

## What works in cold email (updated 2026-03-16)

### Hooks that convert
- "saw your [article/post] on [specific topic]" → 12% reply rate
- "quick question about [their specific situation]" → 9% reply rate
- Anything referencing a recent public action they took

### Hooks that don't work
- "Hope you're doing well" → instant trash
- Generic pitch in first email → 0% reply
- Emails > 5 lines → drop-off

### Best send times
- Tuesday 09:00-11:00 → highest open rates
- Thursday 14:00-16:00 → second best
- Monday and Friday → avoid

### ICP refinements discovered
- CTOs at Series A/B SaaS respond best to technical angle
- Founders < 10 employees respond to revenue/growth angle
- Content creators respond to audience/monetization angle
```

---

## Automatic Memory Triggers — Integration with Other Skills

```
acquisition-master fires:
  → Prospect replied positively  → REMEMBER in clients/ (hot lead)
  → Prospect unsubscribed       → UPDATE status = "do_not_contact"
  → Campaign metrics logged      → UPDATE knowledge/acquisition.md

crypto-executor fires:
  → Trade closed                 → REMEMBER in trades/ with outcome
  → Strategy performed well      → UPDATE knowledge/trading.md

agent-shark-mindset fires:
  → New market signal detected   → REMEMBER in knowledge/market_signals.md
  → Opportunity acted on         → REMEMBER with outcome

ceo-master fires:
  → Decision made                → REMEMBER in projects/ decisions array
  → Weekly review done           → UPDATE relevant knowledge files
```

---

## Memory Index — index.json

Master index updated on every write operation. Allows fast lookup.

```json
{
  "last_updated": "2026-03-16T09:00:00",
  "counts": {
    "clients": 47,
    "projects": 3,
    "trades": 128,
    "knowledge_files": 5
  },
  "recent": [
    { "domain": "clients",  "id": "jean-dupont",        "updated": "2026-03-16" },
    { "domain": "trades",   "id": "BTC-long-20260316",  "updated": "2026-03-16" },
    { "domain": "projects", "id": "veritas-newsletter", "updated": "2026-03-15" }
  ],
  "hot_leads": ["jean-dupont", "marie-martin"],
  "active_trades": [],
  "active_projects": ["veritas-newsletter-launch"]
}
```

---

## Session Startup Protocol

Every time the agent starts a session, it reads memory FIRST.

```
ON SESSION START:
  1. Read /workspace/memory/index.json
     → How many clients? Active trades? Active projects?

  2. Check next_action_date for all clients
     → Any follow-up due today? → Add to task list

  3. Check active trades
     → Any positions to monitor?

  4. Check active project milestones
     → Any deadlines this week?

  5. Read relevant knowledge files for today's tasks
     → If doing cold email today → read knowledge/acquisition.md first

  6. Report to principal (optional, on request):
     "Memory loaded: 47 clients (2 hot leads), 3 active projects,
      0 open trades. 3 follow-ups due today."
```

---

## Weekly Memory Maintenance

Every Sunday at the same time as skill-combinator:

```
1. Archive clients with no interaction in 90+ days
   → Move to /workspace/memory/clients/archived/

2. Summarize closed trades from the week
   → Extract patterns → UPDATE knowledge/trading.md

3. Extract acquisition lessons from the week
   → UPDATE knowledge/acquisition.md

4. Identify top 3 memory insights for weekly CEO report
   → "This week memory revealed: [X], [Y], [Z]"

5. Update index.json counts and recent activity
```

---

## Error Handling

```
ERROR: index.json not found
  Cause:  First run — memory not initialized yet
  Action: Run memory_manager.py --init to create structure
  Log:    AUDIT.md → "Memory initialized [date]"

ERROR: Client file not found on recall
  Cause:  ID doesn't exist in memory
  Action: Create new record with available data
  Log:    No error — expected behavior for new contacts

ERROR: JSONDecodeError on any memory file
  Cause:  File corrupted or partially written
  Action: Check AUDIT.md for last write, restore from last good state
          If unrecoverable → delete corrupted file, re-create from interactions
  Log:    ERRORS.md → "Memory corruption: [file] [date]"

ERROR: Memory file too large (> 1MB single file)
  Cause:  interactions array grown too large (active contact for months)
  Action: Archive interactions older than 90 days to [id]-archive.json
  Log:    AUDIT.md → "Memory compaction: [file] [date]"

ERROR: Duplicate ID on remember operation
  Cause:  Contact already exists — should use UPDATE not REMEMBER
  Action: Auto-switch to UPDATE operation, merge new data
  Log:    AUDIT.md → "Memory merge: [id] [date]"
```

---

## Privacy and Security Rules

```
✅ Memory stays local — /workspace/memory/ only
✅ Never send raw memory files to external services
✅ Never log credentials or payment data in memory
✅ Follow GDPR principle: if contact asks to be forgotten → archive + flag
✅ Memory files are readable only within this agent's workspace

❌ Never store credit card numbers, passwords, or API keys in memory
❌ Never include raw email bodies if they contain sensitive personal data
❌ Never share a client's full profile with any other agent
```

---

## Workspace Structure

```
/workspace/memory/
├── index.json                    ← master index
├── scripts/
│   └── memory_manager.py         ← CLI tool for all operations
├── clients/
│   ├── jean-dupont.json
│   ├── marie-martin.json
│   └── archived/
│       └── old-contact.json
├── projects/
│   ├── veritas-newsletter.json
│   └── archived/
├── trades/
│   ├── BTC-long-20260316.json
│   └── archived/
└── knowledge/
    ├── acquisition.md
    ├── trading.md
    ├── content.md
    ├── market_signals.md
    └── product.md
```

---

## The Compounding Effect

```
Week 1  → 10 clients in memory, 5 trades logged
Week 4  → 40 clients, 20 trades, patterns emerging
Week 12 → 100 clients, 60 trades, knowledge files rich
Week 24 → Agent knows exactly which ICP responds best,
          which trading strategy works in which conditions,
          which content hooks resonate with which audience.

No human could track this manually.
The agent does it automatically, every session, forever.
```

**Memory is not a feature. It's the foundation of intelligence.** 🧠
