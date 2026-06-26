# Athena Protocol — Memory Architecture
# Add these patterns to your AGENTS.md

## Two-Layer Memory System

Your AI needs two kinds of memory. Add this structure to your AGENTS.md:

---

```markdown
## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened each day
- **Long-term:** `MEMORY.md` — curated, distilled wisdom worth keeping permanently

### Rules
- If it matters, write it to a file. Mental notes don't survive session restarts.
- When someone says "remember this" → write to `memory/YYYY-MM-DD.md`
- When you learn a lesson → update the relevant skill or config file
- Periodically distill daily notes into MEMORY.md (weekly is enough)
```

---

## Session Startup Protocol

Add this to your AGENTS.md so your AI always starts oriented:

---

```markdown
## Session Startup

Before doing anything else, read in this order:
1. SOUL.md — who you are
2. USER.md — who you're helping  
3. memory/YYYY-MM-DD.md (today + yesterday) — recent context
4. MEMORY.md (main session only, not group chats)

This takes ~10 seconds and prevents cold-start confusion.
```

---

## No Mental Notes Rule

The single most important memory principle. Add it prominently:

---

```markdown
### ⚠️ No Mental Notes

"I'll remember this" = you won't.
If you want to remember something, write it to a file. Every time.
```

---

## Memory Maintenance (Heartbeat Task)

Add to your heartbeat or periodic review:

---

```markdown
### Memory Maintenance

Every few days:
1. Read recent daily memory files
2. Extract what's worth keeping long-term
3. Update MEMORY.md with distilled insights
4. Remove outdated entries from MEMORY.md

Daily files = raw journal. MEMORY.md = curated wisdom.
```
