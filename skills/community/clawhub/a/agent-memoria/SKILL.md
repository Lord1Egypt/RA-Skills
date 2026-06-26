---
name: memoria
description: >
  Gives your OpenClaw agent persistent memory across every session. MEMORIA maintains
  a structured knowledge layer: who you are, what you're building, every decision made,
  every lesson learned, every project in flight. Your agent stops being a stranger and
  starts being a colleague who was there for everything. Zero cloud. Zero API keys.
  All memory lives in a single local markdown file you own and control forever.
version: 1.0.2
author: contrario
tags:
  - latest
  - memory
  - productivity
  - context
  - persistence
  - developer
  - founder
  - personal
  - knowledge
requirements:
  binaries: []
  env: []
license: MIT
---

# MEMORIA — Persistent Memory Layer for AI Agents

You now operate with persistent memory. A single file on this machine holds everything
that matters about the person you work with. You read it at the start of every session.
You update it as you learn new things. You are no longer starting from zero.

---

## MEMORY FILE LOCATION

Look for the memory file at these locations in order:

```
~/.memoria/memory.md          ← primary (recommended)
~/memoria.md                  ← fallback
./memoria.md                  ← workspace fallback
```

If none exist, create `~/.memoria/memory.md` and run the setup below.

> **Security setup (run once after install):**
> ```bash
> mkdir -p ~/.memoria
> chmod 700 ~/.memoria
> touch ~/.memoria/memory.md
> chmod 600 ~/.memoria/memory.md
> echo ".memoria/" >> ~/.gitignore
> echo "memoria.md" >> ~/.gitignore
> ```
> This ensures the memory file is never accidentally committed or synced to cloud.

---

## MEMORY FILE STRUCTURE

The memory file is plain markdown. Human-readable. Git-friendly. Yours forever.

```markdown
# MEMORIA — [Name]'s Intelligence Layer
Last updated: [DATE]

## WHO I AM
Name: 
Location: 
Profession: 
Background: 
Languages: 

## WHAT I'M BUILDING
[Project name]: [One-line description] — Status: [Active/Paused/Done]
[Project name]: [One-line description] — Status: [Active/Paused/Done]

## MY STACK
Languages: 
Frameworks: 
Infrastructure: 
Tools: 
AI Models: 

## ACTIVE GOALS
- [Goal] — Deadline: [DATE] — Priority: [High/Med/Low]

## DECISIONS LOG
### [DATE] — [Decision title]
Decision: 
Reason: 
Alternatives rejected: 
Review date: 

## LESSONS LEARNED
- [DATE] — [Lesson] — Source: [project/mistake/experiment]

## PEOPLE & CONTEXT
- [Name]: [Role, relationship, context]

## PREFERENCES
Communication style: 
Detail level: 
Code style: 
Output format: 

## RECURRING PROBLEMS
- [Problem pattern] → [Solution that worked]

## CURRENT FOCUS (this week)
[What matters most right now]

## BLOCKED / WAITING
- [Item] — Waiting for: [what] — Since: [DATE]
```

---

## SESSION STARTUP PROTOCOL

At the beginning of every conversation:

**1. READ** — Load the memory file. Scan all sections.

**2. ORIENT** — Build a mental model:
   - Who is this person?
   - What are they working on right now?
   - What decisions have they made that I should not contradict?
   - What are their preferences (detail level, tone, format)?
   - What were they blocked on last time?

**3. CALIBRATE** — Adjust your behavior:
   - Match their communication style
   - Use their project names, not generic terms
   - Reference their stack when giving technical advice
   - Apply their preferences automatically — never ask questions you already know the answer to

**4. CONFIRM (only if memory exists)** — On first message of session, one line only:
   ```
   🧠 Memory loaded. [Name], [current focus or active project]. Ready.
   ```
   If no memory file found:
   ```
   🧠 No memory found. Let's build yours — what's your name and what are you working on?
   ```

---

## MEMORY UPDATE PROTOCOL

Update the memory file when you learn something worth keeping.
Before writing, briefly notify the user:
```
🧠 Saving to memory: [one-line description of what's being added]
```
This keeps the user in control and aware of what is being persisted.

### ALWAYS update when:
- User mentions a new project, technology, or goal
- A decision is made (record it in Decisions Log)
- A lesson is learned from a mistake or experiment
- A preference is revealed ("I prefer...", "I always...", "I hate when...")
- A blocker is resolved or created
- Current focus changes

### HOW to update:
```bash
# Always backup before writing
cp ~/.memoria/memory.md ~/.memoria/memory.md.bak

# Patch the specific section — never overwrite the full file
```

### NEVER:
- Delete existing entries (add "SUPERSEDED" tag if outdated)
- Overwrite the full file (always patch specific sections)
- Store passwords, API keys, tokens, or any credentials
- Store IP addresses, private URLs, or access codes
- Add noise — every entry must be actionable or informative

---

## INTELLIGENCE AMPLIFICATION

MEMORIA doesn't just store. It amplifies.

### Pattern Detection
After 5+ lessons learned entries, look for patterns:
```
PATTERN DETECTED: You've hit the same problem 3 times.
Problem: [X]
Each time: [what happened]
Permanent fix: [recommendation]
```

### Decision Consistency Check
Before making a recommendation, check the Decisions Log.
If your recommendation contradicts a past decision, flag it:
```
⚠️ Note: On [DATE] you decided [X] because [Y].
My current recommendation goes against that.
Has something changed?
```

### Proactive Context
When user asks about a topic that connects to past entries, surface it:
```
This connects to [PROJECT] — you noted on [DATE] that [relevant insight].
```

### Weekly Synthesis (trigger: "weekly review" or Monday morning)
Generate a structured brief:
```
## MEMORIA WEEKLY BRIEF — [DATE]

WINS THIS WEEK:
- [auto-detected from lessons/decisions]

DECISIONS MADE:
- [from decisions log]

STILL BLOCKED:
- [from blocked section]

PATTERNS THIS WEEK:
- [any emerging patterns]

FOCUS RECOMMENDATION FOR NEXT WEEK:
- [based on goals + blocked + active projects]
```

---

## MEMORY COMMANDS

Users can control memory with natural language. Detect these intents:

| User says | Action |
|---|---|
| "Remember that..." | Add to appropriate section immediately |
| "Forget about X" | Mark entry as ARCHIVED, never delete |
| "What do you know about me?" | Pretty-print full memory summary |
| "Update my focus to X" | Replace Current Focus section |
| "I decided to X" | Add to Decisions Log with today's date |
| "That was a mistake" | Add to Lessons Learned |
| "I'm blocked on X" | Add to Blocked/Waiting |
| "X is unblocked" | Mark as resolved, move to Lessons if applicable |
| "Show me my decisions" | List Decisions Log, newest first |
| "What have I been avoiding?" | Cross-reference Blocked + Goals |

---

## PRIVACY ARCHITECTURE

All memory is local. Nothing leaves the machine.

```
~/.memoria/               ← chmod 700 (owner only)
├── memory.md             ← chmod 600 (primary memory file)
├── memory.md.bak         ← backup created before each write
└── archive/              ← optional: periodic manual snapshots
```

> **Before each write:** the agent creates `memory.md.bak` as a safety copy.
> This is guidance for the agent — no background process runs automatically.
> For scheduled backups, set up a cron job manually if needed.

> **Cloud sync warning:** Add `~/.memoria/` to `.gitignore` and any
> Dropbox/iCloud/OneDrive ignore list to prevent accidental cloud upload.

---

## INITIALIZATION FLOW

When a new user runs `clawhub install memoria` and starts their first session:

```
🧠 MEMORIA v1.0.0 — Memory Layer Active

No memory file found. Let's build your intelligence layer.
This takes 2 minutes and makes every future session 10x better.

I'll ask you 5 questions. Answer however you like.

1. What's your name and what do you do?
2. What's the main thing you're building or working on right now?
3. What's your tech stack? (languages, frameworks, tools)
4. What's your biggest current challenge or blocker?
5. How do you prefer I communicate? (brief/detailed, formal/casual, Greek/English)

[After answers: auto-populate the memory file and confirm]

✅ Memory file created at ~/.memoria/memory.md
   443 characters of context loaded.
   From now on, every session starts where the last one ended.
```

---

## MULTI-PROJECT INTELLIGENCE

For users with multiple active projects (common for solo founders):

```markdown
## PROJECT INDEX
### [Project Name]
Status: Active | Paused | Done
Stack: 
Revenue: €X/month
Next milestone: 
Key decisions: [link to decisions log entries]
Last worked on: [DATE]
```

When user switches context between projects:
```
Switching to [Project Name] context.
Last worked on: [DATE]
At that time: [what was happening]
Current status: [from memory]
```

---

## COMPANION SKILLS

MEMORIA works best paired with:

- **apex-agent** — APEX uses memory context to give sharper, more personalized responses
- **github** — Memory logs which repos belong to which projects
- **obsidian** — Memory syncs with Obsidian vault for richer note-taking
- **tavily-web-search** — Research results can be saved to memory as lessons

Install all:
```bash
clawhub install memoria
clawhub install apex-agent
```

---

## ACTIVATION CONFIRMATION

When MEMORIA loads successfully, output exactly:

```
🧠 MEMORIA active. [X] entries loaded. Your agent remembers everything.
```

If memory file is new/empty:
```
🧠 MEMORIA active. No history yet — let's start building yours.
```

Then proceed with the session. Never explain the framework further unless asked.

---

*MEMORIA v1.0.1 — Because your agent should know you.*
*Built on the belief that context is the most valuable thing in any relationship.*
