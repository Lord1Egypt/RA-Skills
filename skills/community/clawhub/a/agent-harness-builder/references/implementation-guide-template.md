<!-- TEMPLATE — This is a worked example from a real 29-agent build (Decade Strategy Inc / Tori as CTO).
     Use it as the structure and pattern to follow. Replace all names, roles, businesses, models,
     and channels with the current user's. Keep the section structure, the invariants (memory limits,
     task-brief format, completion-report format, cheapest-viable-model rule), and the overall shape. -->

# OpenClaw Harness — Step-by-Step Implementation Guide
### Decade Strategy Inc | Build this in 4 phases

---

## BEFORE YOU START

You have 3 files in this package:
- `HARNESS-ARCHITECTURE.md` — the full blueprint
- `AGENT-PROFILES.md` — agent roster templates
- `TORI-SYSTEM-PROMPT.md` — Tori's operating instructions
- This file — how to actually build it

Do phases in order. Don't skip ahead.

---

## PHASE 1 — CLEAN HOUSE
*Estimated time: 2–3 hours | Do this first, nothing else works without it*

### Step 1 — Fix Tori's MEMORY.md (urgent)
Her file is at 85,441 chars. Limit is 15,000. Do this now:

```bash
# Check current size
wc -c ~/.openclaw/memory/tori/MEMORY.md

# Back it up first
cp ~/.openclaw/memory/tori/MEMORY.md ~/.openclaw/memory/tori/MEMORY-ARCHIVE-$(date +%Y%m%d).md

# Open and manually trim to most recent/relevant entries
nano ~/.openclaw/memory/tori/MEMORY.md
```

Keep only:
- Active project statuses
- Key decisions from last 30 days
- Standing rules and preferences
- Current agent roster

Archive everything else to MEMORY-ARCHIVE.md.

### Step 2 — Create shared memory directory
```bash
mkdir -p ~/.openclaw/memory/shared
mkdir -p ~/.openclaw/memory/tori
mkdir -p ~/.openclaw/memory/amadeus
mkdir -p ~/.openclaw/memory/edison
mkdir -p ~/.openclaw/memory/connie
mkdir -p ~/.openclaw/memory/rico
mkdir -p ~/.openclaw/memory/monica
mkdir -p ~/.openclaw/memory/goober
# repeat for all 24 agents
```

### Step 3 — Create shared context files
Create these in `~/.openclaw/memory/shared/`:

- `brand-guidelines.md` — Soul of the Brand, tone, voice rules
- `company-context.md` — What Decade Strategy is, all businesses, Paul's background
- `client-roster.md` — Active clients across all businesses
- `product-catalog.md` — Products/services across all businesses

Keep each under 3,000 chars. Tight and useful.

### Step 4 — Verify all Slack tokens working
```bash
openclaw gateway 2>&1 | grep -E "(starting provider|invalid_auth|socket mode)"
```
All 8 providers should say "socket mode connected". Fix any that don't before proceeding.

---

## PHASE 2 — DEFINE YOUR AGENTS
*Estimated time: 1–2 hours | You need to fill this out*

### Step 1 — Open AGENT-PROFILES.md
Fill in for every agent:
- `role` — what they actually do
- `skills` — pick from the skill tag library
- `domains` — which businesses they work in
- `memory.shared` — which shared files they need

### Step 2 — Update Tori's system prompt
Open `TORI-SYSTEM-PROMPT.md`, fill in:
- Each agent's role in the Tier 1/2/3 sections
- Any business-specific routing rules

### Step 3 — Copy Tori's system prompt into openclaw
```bash
# Tori's system prompt lives in her agent config
# Open openclaw.json and find her systemPrompt field
nano ~/.openclaw/openclaw.json
# Ctrl+W → search "tori" → find systemPrompt → paste content
```

---

## PHASE 3 — TEST TORI'S ROUTING
*Estimated time: 1 hour | Test before you scale*

### Step 1 — Start gateway and confirm all agents up
```bash
openclaw gateway
```
Watch for all providers: "socket mode connected"

### Step 2 — Send Tori a test task in Slack
In #tori-command, send:
```
Tori, draft a 2-sentence welcome message for a new Soup Club restaurant client. Route to whoever handles marketing copy.
```

Watch what happens:
- Does she identify the right agent (Amadeus)?
- Does she send a structured brief?
- Does she return the result to you?

### Step 3 — Test a multi-agent workflow
```
Tori, I need a competitive analysis of meal kit delivery services (research), then a 1-page summary formatted for a client presentation (writing). Coordinate whoever is best for each step.
```

Check:
- Did she spawn two agents?
- Did she synthesize the result?
- Was the output usable without editing?

### Step 4 — Fix what broke, repeat

---

## PHASE 4 — AUTOMATE & SCALE
*Do this after Phase 3 is solid*

### Step 1 — Set up cron workflows
Common recurring tasks to automate:
```bash
# Daily morning brief (Tori posts to #tori-command at 8am)
# Weekly MEMORY.md audit
# Monthly DeepSeek billing check
# Weekly completion digest
```

### Step 2 — Set up #completions channel
Every agent posts a 2-line summary when a task is done:
```
✅ [TASK-ID] [AGENT] completed: [what was done] | [time taken]
```

### Step 3 — Set up #alerts channel
Tori posts here for:
- Any `invalid_auth` errors
- Model fallback events
- Failed tasks
- MEMORY.md approaching size limits

### Step 4 — Monthly maintenance checklist
- [ ] Trim all MEMORY.md files
- [ ] Review model fallback log — is DeepSeek billing current?
- [ ] Review #completions for patterns (bottlenecks, underused agents)
- [ ] Update agent skill tags if roles have evolved
- [ ] Rotate Slack tokens if any are >90 days old

---

## QUICK REFERENCE — FILE LOCATIONS

| File | Path |
|---|---|
| Main config | `~/.openclaw/openclaw.json` |
| Tori's memory | `~/.openclaw/memory/tori/MEMORY.md` |
| Shared context | `~/.openclaw/memory/shared/` |
| Agent workspaces | `~/.openclaw/workspace/[agent]/` |
| Gateway logs | `/tmp/openclaw/openclaw-[date].log` |
| Stability bundles | `~/.openclaw/logs/stability/` |

---

## QUICK REFERENCE — USEFUL COMMANDS

```bash
# Start gateway
openclaw gateway

# Start gateway and watch logs
openclaw gateway 2>&1 | tee /tmp/openclaw-debug.log

# Check gateway running
lsof -i :18789

# Check log tail
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# Check MEMORY.md sizes
wc -c ~/.openclaw/memory/*/MEMORY.md

# Install as background service
openclaw gateway install
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## COMMON PROBLEMS & FIXES

| Problem | Fix |
|---|---|
| Gateway crashes on start | Check for `invalid_auth` — rotate bad Slack token |
| Agent getting wrong context | Check what's in its MEMORY.md — trim it |
| Tori not routing correctly | Update her system prompt with clearer agent skill tags |
| DeepSeek billing fallback | Top up at platform.deepseek.com or switch primary model |
| MEMORY.md too large | Trim to limit, archive the rest |
| EISDIR error | A tool is trying to read a directory as a file — check tool config |

---

*Decade Strategy Inc — OpenClaw Harness v1.0 | Built June 2026*
