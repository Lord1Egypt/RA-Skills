# Memory System — AGENTS.md Rules

Copy these rules into the agent's AGENTS.md under a `## Memory` section. Customize workspace paths and file names as needed.

---

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories, like a human's long-term memory
- **Feedback:** `memory/feedback.md` — corrections and confirmations from your human (MOST IMPORTANT)
- **Topics:** `memory/topics/*.md` — low-frequency details (environment, known issues, configs)

### Memory rules

1. **feedback must be written immediately** — when your human corrects you, update `memory/feedback.md` NOW
2. **record confirmations too** — when your human validates an approach, record it as confirmation feedback
3. **MEMORY.md is hybrid (content + pointers)** — keep it under 10KB, inline high-frequency info, details go to topics/
4. **When MEMORY.md says 'see topics/xxx.md', you MUST read that file** before answering
   - Never answer from a one-line summary alone — read the full file for context
5. **Absolute dates only** — convert relative dates to absolute when writing memories
6. **Don't memorize what tools can look up** — file paths, code structure, git history, live data
7. **Don't memorize ephemeral state** — in-progress work, temporary context, things that resolve themselves
8. **Verify technical memories before using** — service configs, bug status, versions may change. Personal preferences and history don't need verification.
9. **Memory care in heartbeat** — catch-up, consolidate, verify, tidy. Memories are never deleted, only relocated.

### MEMORY.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- Write significant events, thoughts, decisions, opinions, lessons learned
- Over time, review your daily files and update MEMORY.md with what's worth keeping

### Write It Down - No "Mental Notes"!

- **Memory is limited** — if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → update `memory/YYYY-MM-DD.md` or relevant file
- When you learn a lesson → update AGENTS.md, TOOLS.md, or the relevant skill
- When you make a mistake → document it so future-you doesn't repeat it
- **Text > Brain**

---

Replace "your human" with the actual user name for personalization.
