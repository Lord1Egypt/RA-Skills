---
name: breadcrumb-writer
description: "Do NOT use regularly. If updating HEARTBEAT.md: one entry only, replace (never append), at most once per hour. See AGENTS.md for task board."
metadata: { "openclaw": { "emoji": "🍞" } }
---

# Breadcrumb / HEARTBEAT.md updates

**Prefer:** Main agent updates HEARTBEAT.md directly per AGENTS.md (task board: Active Tasks, Context, Completed). Heartbeat agent runs every 60m from gateway config.

**If you do write to HEARTBEAT.md:**

1. **At most once per hour.** Before writing, check the file: if it was updated in the last 60 minutes, do not write. Do not run this more often than once per hour.
2. **One entry only.** Replace the entire file with a single short status block. Do not append. Do not add multiple "Recent Activity" or "System Status" sections.
3. **No clutter.** Keep the file small: one block with Active Tasks (if any), Context (brief), and optionally Completed. No repeated blocks, no "Last 3 exchanges", no timestamps per section.

Violating these rules clutters HEARTBEAT and confuses the heartbeat agent.