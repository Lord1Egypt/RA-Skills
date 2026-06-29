# Communication Protocols — 神经链设计

Inter-agent communication is the nervous system of an AI-native company. Single-channel communication is a single point of failure.

## Three-Channel Redundancy Architecture

```
┌─────────┐  sessions_send  ┌─────────┐
│ Agent A │ ←─────────────→ │ Agent B │
└─────────┘                 └─────────┘
     │                           │
     │    shared/files/          │
     └────────┬──────────────────┘
              │
     ┌────────┴──────────────────┐
     │   Tencent Docs / Cloud    │
     └───────────────────────────┘
```

## Channel 1: sessions_send (Primary)

Fastest path. Zero latency. Direct agent-to-agent.

Use for:
- Real-time alerts and notifications
- Task handover between departments
- CEO directives to departments

```javascript
// Example: DataCenter sends to Brand department
sessions_send({
  sessionKey: "brand-main",
  message: "今天的热点情报已采集完毕，3条可转化为品牌内容"
})
```

## Channel 2: Shared Files (Sync)

File-based message boxes in `company/shared/messages/{department}/`.

Use for:
- Async communication (write now, read later)
- Audit trail (all messages are persistent files)
- Bulk data transfer (attachments, reports)

Directory structure:
```
company/shared/messages/
├── datacenter/
│   └── msg_20260625_0830_to_brand.md
├── brand/
│   └── msg_20260625_2200_daily_report.md
├── sales/
├── finance/
├── legal/
├── inspector/
└── admin/
```

File naming convention: `msg_{YYYYMMDD}_{HHMM}_{to_dept}.md`

## Channel 3: Cloud Documents (Resilience)

Tencent Docs / Feishu Docs as fallback.

Use for:
- Cross-platform access (when agent is on different machine)
- Long-form collaborative documents
- CEO dashboards and reports

## Channel 4: Workspace Markers (Status Flags)

File-based status indicators for async handover.

```
company/shared/schedule/
├── datacenter_ready.flag
├── brand_published.flag
├── morning_sync_complete.flag
```

A department writes a `.flag` file when it completes a milestone. Dependent departments check for the flag before proceeding.

## Failure Modes and Recovery

| Failure | Symptom | Recovery |
|---------|---------|----------|
| sessions_send blocked | Message not delivered | Fall back to shared file |
| Shared file not written | Missing file | Fall back to Tencent Docs |
| All channels down | Total silence | Inspector detects via heartbeat check |
| Stale flags | Flag exists but work not done | Timestamp verification in flag content |

## Broadcast Pattern

When information needs to reach all departments simultaneously:

1. Write to `company/shared/broadcast/` directory
2. Set a broadcast flag
3. Each department's cron checks for new broadcasts on wake

## Anti-Patterns

- **Private DMs between agents** — Creates invisible communication that can't be audited
- **CEO as message router** — The CEO is not a switchboard. Agents talk to agents.
- **Email for agent communication** — External channels add latency and failure points
- **Single channel dependency** — "It's always worked" is how outages begin
