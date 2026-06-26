# Cross-Session Context Sync

## The Problem

OpenClaw session types and their context access:

```
┌─────────────┐  FILES   ┌──────────────┐
│  Main DM    │ ──────→  │  MEMORY.md   │ ← Only main session reads
│  (full ctx) │ ←──────  │  daily logs  │ ← Main + heartbeat read
└─────────────┘          │  progress.md │ ← Any session can read/write
       ↓                 └──────────────┘
  HISTORY (dies)                ↓
                          DISK (survives)
       ↑                        ↓
┌─────────────┐          ┌──────────────┐
│  Cron Job   │ ──────→  │  payload msg │ ← Only context source
│  (no ctx)   │  no file  │  (embedded)  │
└─────────────┘  access   └──────────────┘
```

## Solutions by Scenario

### Scenario 1: Cron Needs Main Session Context

**Problem**: Cron job runs in isolation, doesn't know user preferences, current state, etc.

**Solution A: Embed in Payload** (for small context)
```
payload.message = "你是日报推送 agent。规则：\n" +
  "1. 读取 weekly-ai-browser-news-2026-W1.md\n" +
  "2. 找到今天日期对应的日报\n" +
  "3. 推送到 chat:oc_xxx\n" +
  "当前日报格式：见 memory/daily-news-format.md"
```

**Solution B: Self-Loading from Files** (for larger context)
```
payload.message = "你是日报推送 agent。\n" +
  "1. 读取 memory/daily-news-rules.md 获取完整规则\n" +
  "2. 按规则执行\n" +
  "3. 如果规则文件不存在，回复需要配置"
```

**Solution C: Shared State File** (for dynamic state)
- Main session writes state to `memory/shared-state.json`
- Cron reads the file at runtime
- Both sessions update as needed

### Scenario 2: Subagent Needs Progress Context

**Problem**: Subagent spawned for continuing a task doesn't know where to resume.

**Solution**: Progress file pattern
```
sessions_spawn(
  task: "继续读 Chromium 源码。先读 memory/chromium-extensions-progress.md 了解进度，然后从下一步开始",
  ...
)
```

### Scenario 3: Heartbeat Needs Task State

**Problem**: Heartbeat needs to check if tasks need attention.

**Solution**: Structured state files
```json
// memory/heartbeat-state.json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800
  },
  "activeTasks": {
    "chromium-reading": {
      "progress": 7.01,
      "lastSession": "2026-03-17T00:19:00+08:00",
      "status": "in-progress"
    }
  }
}
```

Heartbeat reads this → knows what to check → updates after checking.

### Scenario 4: Multi-Channel User (DM + Group)

**Problem**: User talks in DM and group, context split across both.

**Solution**: 
- MEMORY.md (main session only) = source of truth
- Daily logs = raw records from all channels
- Key rule: "DM 和群推送内容必须一致，从统一文件读取"

## Coordination Patterns

### Pattern: File-Based Producer-Consumer

```
Producer Session (e.g., nightly cron):
  1. Generate content
  2. Write to shared file (e.g., weekly-report.md)
  3. Done

Consumer Session (e.g., morning cron):
  1. Read shared file
  2. Deliver content
  3. Done
```

**Critical**: Both must agree on file format. Document it in MEMORY.md or a shared rules file.

### Pattern: Progress Checkpointing

```
Session starts:
  Read(progress-file) → state = {completed: [...], next: X}

Session work:
  Process items X..Y
  state.completed += [X..Y]
  state.next = Y+1

Session ends:
  Write(progress-file, state)
```

### Pattern: State Lease

For preventing concurrent modification:
```json
{
  "lock": {
    "holder": "session-abc123",
    "acquiredAt": "2026-03-17T10:00:00Z",
    "expiresAt": "2026-03-17T11:00:00Z"
  }
}
```

Usually overkill for OpenClaw (rare concurrent access), but useful for cron race conditions.

## Common Pitfalls

1. **"I wrote it to MEMORY.md but cron can't see it"**
   → MEMORY.md only loads in main session. Use payload embedding or separate file.

2. **"Subagent doesn't remember what I told it"**
   → Subagents have no history. Put everything in the task message or a file.

3. **"Two sessions overwrote each other's progress"**
   → Use append-only logs or atomic writes. For progress files, include full state (not deltas).

4. **"Cron keeps failing but I don't know why"**
   → Check `cron runs <jobId>` for error logs. Add verbose logging to payload.

## Debugging Cross-Session Issues

```bash
# Check cron execution history
openclaw cron list
openclaw cron runs <jobId>

# Check session context usage
# In-session: /status shows context %

# Check what files are being read
# Look at daily logs for file access records
```
