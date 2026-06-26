# HEARTBEAT.md — Periodic Routines

Your agent's regular check-in routine.

---

## Every Session (Start)

1. **Read MEMORY.md** — Load identity and long-term context
2. **Read memory/YYYY-MM-DD.md** (today) — Check today's log
3. **Read memory/YYYY-MM-DD.md** (yesterday) — Recent context
4. **Check memory/cron-inbox.md** — Messages from other sessions

## Every Heartbeat (Periodic)

### 1. Process Cron Inbox
- Read `memory/cron-inbox.md`
- For each entry: write notable ones to daily notes, update MEMORY.md if significant
- Clear processed entries

### 2. Service Checks
- Email inbox check (every 60 min)
- Calendar check (every 60 min)
- Social notifications (every 30 min)

### 3. Memory Maintenance (every 3-5 heartbeats)
- Review recent daily logs
- Promote significant items to MEMORY.md
- Update strategy-notes.md

## Nightly (23:00)

### Memory Extraction
- Extract durable facts from daily notes
- Append to MEMORY.md
- Mark daily notes as extracted

*Last updated: 2026-05-23*
