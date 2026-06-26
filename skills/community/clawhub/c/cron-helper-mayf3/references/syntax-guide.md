# Cron Job Syntax Guide

## Job Schema

### All Fields

```json
{
  "id": "string (required, unique)",
  "agentId": "string (required)",
  "name": "string (required)",
  "enabled": "boolean (required)",
  "schedule": {
    "kind": "cron | every (required)",
    "expr": "cron expression (required if kind=cron)",
    "everyMs": "milliseconds (required if kind=every)",
    "tz": "timezone string (recommended)"
  },
  "sessionTarget": "isolated | main (optional)",
  "wakeMode": "now | scheduled (optional)",
  "payload": {
    "kind": "agentTurn (required)",
    "message": "string (required — the prompt)",
    "timeoutSeconds": "number (optional, recommended 120-600)"
  },
  "delivery": {
    "mode": "announce | none (required)",
    "channel": "feishu | discord | telegram | signal | webchat (required if mode=announce)",
    "to": "chat:oc_xxx | user:ou_xxx (required if mode=announce)"
  }
}
```

## Schedule Types

### Cron Expression

Standard 5-field cron: `minute hour day-of-month month day-of-week`

```json
{ "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" }
```

Special characters: `*` (any), `,` (list), `-` (range), `/` (step)

| Expression | Meaning |
|------------|---------|
| `0 10 * * *` | Every day at 10:00 |
| `*/5 * * * *` | Every 5 minutes |
| `0 */2 * * *` | Every 2 hours |
| `0 10 * * 1` | Every Monday at 10:00 |
| `0 0 1 * *` | 1st of every month |
| `0 9,17 * * *` | 9AM and 5PM daily |

### Every (Fixed Interval)

```json
{ "kind": "every", "everyMs": 3600000 }
```

Common values: `60000` (1min), `300000` (5min), `3600000` (1hr), `86400000` (1day)

## Delivery Configuration

### Valid Channels

`feishu`, `discord`, `telegram`, `signal`, `webchat`

### Valid `to` Formats

- Group chat: `"chat:oc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`
- User DM: `"user:ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"`

### ❌ Invalid (Common Mistakes)

```json
// Missing channel
{ "mode": "announce", "to": "chat:oc_xxx" }  // ❌

// Invalid channel value
{ "mode": "announce", "channel": "last", "to": "chat:oc_xxx" }  // ❌

// Using peer object (deprecated)
{ "mode": "announce", "peer": { "kind": "group", "id": "oc_xxx" } }  // ❌

// Missing to
{ "mode": "announce", "channel": "feishu" }  // ❌
```

### ✅ Correct

```json
{ "mode": "announce", "channel": "feishu", "to": "chat:oc_xxx" }
```
