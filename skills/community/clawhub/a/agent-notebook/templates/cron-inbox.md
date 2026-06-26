# Cron Inbox

Cross-session message bus. Cron jobs, sub-agents, and background tasks write here. Your main session reads and processes these during heartbeat.

---

## [YYYY-MM-DD HH:MM] Source — Brief Title
- What happened
- Key results or findings
- Any action needed by main session

## [YYYY-MM-DD HH:MM] Source — Another Event
- Details
- Links or references

---

**How it works:**
1. A cron job or sub-agent does work in an isolated session
2. It writes notable results here
3. Your main session reads the inbox during heartbeat
4. Notable events get written to daily notes and/or MEMORY.md
5. Processed entries are cleared (keep the header)

**Processing rule (for heartbeat):**
Every heartbeat, check this file. If entries exist:
1. Read all entries
2. Write notable ones to `memory/YYYY-MM-DD.md`
3. If significant, update `MEMORY.md`
4. Clear processed entries (keep the `# Cron Inbox` header)

*Last processed: [YYYY-MM-DD HH:MM]*
