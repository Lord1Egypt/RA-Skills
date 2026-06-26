# QUICKSTART — Agent Memory in 20 Minutes

Your agent forgets everything between sessions. This guide gets it remembering in 20 minutes.

---

## Before You Start

**What you need:**
- Python 3.7+ (no external dependencies)
- A workspace directory for your agent (folder where it works)
- 20 minutes

**What you'll have when done:**
- A complete memory file structure in your workspace
- An agent that loads context at every session start
- Session handoff so mid-task work continues where it left off

---

## Step 1: Run the Init Script (2 minutes)

Navigate to where you downloaded this skill, then:

```bash
# Interactive — prompts you for names and timezone
python3 init_memory.py

# Or specify everything upfront
python3 init_memory.py --workspace /path/to/your/workspace --agent "YourAgentName" --user "YourName" --timezone "America/Denver"

# Or just use current directory with defaults
python3 init_memory.py --non-interactive --workspace .
```

**What it creates in your workspace:**

```
your-workspace/
├── AGENTS.md         ← Agent behavioral rules
├── USER.md           ← Who you are (agent reads this every session)
├── MASTER_MAP.md     ← Navigation index (what's where)
├── MEMORY.md         ← Long-term curated memory
├── HEARTBEAT.md      ← Periodic check checklist
├── HANDOFF.md        ← Session continuity (starts empty)
└── memory/           ← Daily logs directory (created automatically)
```

---

## Step 2: Fill In the Owner Namespace (8 minutes)

`memory/owner/` is the surgical long-term memory layer — 6 focused files instead of one monolith. Each loads independently so the agent only pulls what it needs.

**Start with the two that load every session:**

`memory/owner/identity.md` — who you and the agent are:
```markdown
## User
- Name: [Your name]
- Handle: [Your online alias]
- Timezone: America/Denver

## Agent
- Name: [Your agent's name]
- Installed: 2026-03-10
```

`memory/owner/preferences.md` — how you want to be treated:
```markdown
## Communication Style
- Direct, no filler
- Bullet points over paragraphs for technical info

## Things That Annoy Me
- [What drives you crazy when agents do it]
```

**The other four load on demand** — fill them in as sessions accumulate:
- `decisions.md` — important choices + why (loaded when decisions are needed)
- `learnings.md` — lessons, patterns, mistakes corrected (loaded after mistakes)
- `people.md` — collaborators, trusted users (loaded when people are mentioned)
- `projects.md` — active and completed work (loaded during project work)

---

## Step 3: Fill In USER.md (3 minutes)

**This is the most important file.** Open it and fill in the blanks. Your agent reads this every session — it's how it knows who you are.

At minimum, fill in:

```markdown
# USER.md

- **Name:** [Your name]
- **What to call you:** [How you want to be addressed]
- **Timezone:** [Your timezone]
- **What I'm working on:** [Current projects, goals]
- **Things to always remember:** [Your preferences, pet peeves]
- **Things I never want the agent to do:** [What drives you crazy]
```

More detail = better agent behavior. If you hate when agents explain things you already know, write that. If you want blunt feedback, write that. If you're working on something specific, write what it is.

---

## Step 4: Fill In AGENTS.md (5 minutes)

This is where the agent's rules live. The template has good defaults — customize the sections that matter to you:

**Key sections to fill in:**
- **Core Identity** — what kind of agent is this? What's its purpose?
- **How I Operate** — communication style, what it should and shouldn't do
- **Memory** — confirm the memory file loading order
- **Safety** — any hard rules (things it must never do autonomously)

The template's memory loading section is pre-filled with the correct file order:
```
1. Read HANDOFF.md first (if it has content — resume mid-task work)
2. Read USER.md
3. Read memory/YYYY-MM-DD.md (today's log)
4. Read MASTER_MAP.md
5. Read MEMORY.md (main sessions only — not group chats)
```

Don't change this order. It's designed so the agent always gets the most immediately relevant context first.

---

## Step 5: Add the Memory Prompt to Your Agent (3 minutes)

Copy this into your agent's system prompt or the `AGENTS.md` you just filled in. This is the instruction that makes memory work:

```
## Session Start Protocol

Before doing anything else, every session:

1. Check HANDOFF.md — if it has real content (not blank template), read it and follow it.
   Archive to memory/[DATE]-handoff.md, then clear back to blank.
2. Read USER.md
3. Read memory/owner/identity.md + memory/owner/preferences.md
4. Load other owner files on demand: decisions.md, learnings.md, people.md, projects.md
5. Read MASTER_MAP.md
6. Read MEMORY.md (direct sessions only — not group chats)
7. Read memory/[TODAY'S DATE].md if it exists

For group/guild chats: use memory/channels/[channel]/ only.
Owner context never enters group sessions. Group context never enters owner sessions.

The order matters. HANDOFF.md first — mid-task continuity before anything else.
Owner namespace third — surgical, only load what's relevant. MASTER_MAP before MEMORY.md.
```

**For OpenClaw:** Add this to `AGENTS.md` in your workspace — OpenClaw reads it automatically.

**For other frameworks:** Add the above to your system prompt, or to wherever your agent reads its standing instructions.

---

## Step 6: Test It (5 minutes)

Start a fresh session with your agent (not a continuation — a genuinely new session). Tell it:

```
Read your startup files and tell me what you know about me.
```

It should:
1. Read HANDOFF.md (empty — that's correct for first run)
2. Read USER.md and summarize what it learned
3. Read MASTER_MAP.md (currently a template — that's fine)
4. Tell you what it found

**If it doesn't read the files:** The memory prompt isn't loaded. Go back to Step 4 and verify where you pasted it.

**If it reads them but the files seem empty:** That's correct — you just set it up. The files fill over time.

---

## How It Works After Setup

### Daily workflow

Sessions accumulate in `memory/YYYY-MM-DD.md`. Your agent writes to today's log automatically. You don't have to do anything.

At the start of each session, the agent reads today's log — this means it picks up where yesterday left off without needing a HANDOFF.

### When to write HANDOFF.md

Use HANDOFF.md when you're stopping mid-task and want to resume exactly there:

```markdown
# Session Handoff — 2026-03-10

## WHERE WE LEFT OFF
Halfway through building the API integration. Auth is working, routes are next.

## IN PROGRESS
- auth.py: complete
- routes.py: started, not done — stopped at line 47

## NEXT ACTIONS
1. Finish routes.py (pick up at line 47)
2. Test with Postman
3. Write README

## OPEN QUESTIONS
- Should errors return 400 or 422? Decide before writing error handlers.
```

The next session reads this before anything else, picks up at line 47 of routes.py, and continues. Then clears the file.

**When NOT to write it:** Finished sessions. Casual conversations. Anything that doesn't need exact continuity. The daily log handles everything else.

### How MEMORY.md fills over time

Your agent updates MEMORY.md with:
- Important decisions and why they were made
- Things to always remember
- Lessons learned
- Key facts about you that it discovered

It also periodically consolidates the daily logs — pulling the best insights into MEMORY.md and leaving the raw notes in the daily files.

**Keep MEMORY.md under 20KB.** It loads on every session. If it gets large, move old entries to daily files.

### Keeping MASTER_MAP.md current

MASTER_MAP.md is your navigation index. Update it when:
- You add a new major project
- You add new systems or tools
- The map no longer reflects what's actually in the workspace

The agent uses it to know what files exist and what they contain — without loading everything. A stale MASTER_MAP means the agent doesn't know about new things you've added.

---

## Troubleshooting

### "My agent isn't reading the files at session start"
The memory prompt isn't in the system prompt or AGENTS.md. Re-check Step 4. The instruction needs to be somewhere the agent sees every time — not just the first time.

### "The agent reads the files but seems to forget by the end of the session"
The agent is reading at startup but not writing at session end. Add to your agent's instructions:
```
At the end of each session: update memory/[TODAY].md with what happened, decisions made, and things to remember.
```

### "MEMORY.md is getting too large"
Have the agent do a consolidation pass:
```
Read memory/YYYY-MM-DD.md files from the last week. Update MEMORY.md with only the insights worth keeping long-term. Delete or archive entries older than [X months].
```

### "The agent keeps re-reading files it already read"
Normal in some frameworks. Add to AGENTS.md: "Once you've read a file at session start, don't re-read it unless I explicitly ask."

### "I want to start fresh with a specific file"
Delete the file and re-run init_memory.py with `--workspace /path` — it only overwrites if you confirm.

### "HANDOFF.md has content from a previous session that's now stale"
Clear it manually. HANDOFF.md is yours to manage. If the session it was written for is done, delete it or move it to `memory/`.

---

## File Reference

| File | When Written | When Read | Keep Under |
|------|-------------|-----------|------------|
| `AGENTS.md` | Setup (you) + ongoing (agent) | Every session | 10KB |
| `USER.md` | Setup (you) + updates | Every session | 5KB |
| `MASTER_MAP.md` | You + agent updates | Every session | 200 lines |
| `MEMORY.md` | Agent (ongoing) | Main sessions only | 20KB |
| `HEARTBEAT.md` | You | Heartbeat polls | 2KB |
| `HANDOFF.md` | Agent (end of mid-task session) | **First** — before anything | Clear after reading |
| `memory/YYYY-MM-DD.md` | Agent (during session) | Session start | Unlimited |

---

## The One Rule

**If you want the agent to remember something, write it to a file.**

Mental notes don't survive session restarts. The agent saying "I'll remember that" doesn't survive session restarts. Files do.

When the agent learns something important: `memory/today.md`.  
When it's worth keeping long-term: `MEMORY.md`.  
When you're mid-task and need exact continuity: `HANDOFF.md`.  

That's the whole system.
