# HEARTBEAT.md — Periodic Routines

Your agent's regular check-in routine. Run this periodically (every 30-60 minutes, or on session start) to maintain continuity and catch up on background work.

---

## Every Session (Start)

1. **Read MEMORY.md** — Load identity and long-term context
2. **Read memory/YYYY-MM-DD.md** (today) — Check today's log
3. **Read memory/YYYY-MM-DD.md** (yesterday) — Recent context
4. **Check memory/cron-inbox.md** — Messages from other sessions
5. **Read HEARTBEAT.md** (this file) — Confirm routines

## Every Heartbeat (Periodic)

### 1. Process Cron Inbox
- Read `memory/cron-inbox.md`
- For each entry:
  - If notable → write to today's daily notes
  - If significant → update MEMORY.md
- Clear processed entries (keep header)

### 2. Check Heartbeat State
- Read `memory/heartbeat-state.json`
- Check timestamps for overdue services
- Run checks for anything past due

### 3. Service Checks (if configured)
- Email inbox check
- Calendar check
- Weather check (if relevant)
- Social media notifications
- Any other periodic monitoring

### 4. Memory Maintenance (every 3-5 heartbeats)
- Review recent daily logs (last 3-5 days)
- Promote significant items to MEMORY.md
- Remove outdated info from MEMORY.md
- Update strategy-notes.md with new learnings

### 5. Daily Notes Reminder
- Ensure `memory/YYYY-MM-DD.md` exists for today
- If starting a new day, create the file from template

## Nightly (23:00)

### Memory Extraction
- Read today's daily notes
- Extract durable facts, decisions, and lessons
- Append to MEMORY.md under relevant sections
- Mark extracted items in daily notes

## Weekly (Sunday)

### Memory Review
- Read through the week's daily logs
- Full review and distillation into MEMORY.md
- Archive old daily logs if desired
- Update strategy-notes.md

---

**Tips:**
- Keep routines lightweight — don't overwhelm the session
- Focus on inbox processing and state checks every heartbeat
- Save heavy maintenance for scheduled times
- This file is a living document — add or remove routines as needed

*Last updated: [YYYY-MM-DD]*
