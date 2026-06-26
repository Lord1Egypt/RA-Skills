# Workflow

## Goal

Maintain a canonical Feishu identity master that can support multi-agent, multi-account routing.

## Data model

- Global subject key priority:
  1. `union_id`
  2. `user_id`
- App-local identity:
  - `open_id`
- Supporting fields:
  - `name`
  - `phone`
  - `aliases`

## Canonical flow

### A. Ingest identity records

Each record should look like:

```json
{
  "source_agent": "agent-name",
  "app_context": "feishu-app-or-agent-context",
  "open_id": "ou_xxx",
  "user_id": "gxxxx",
  "union_id": "on_xxx",
  "name": "姓名",
  "phone": "+86...",
  "captured_at": "ISO-8601 timestamp"
}
```

### B. Merge logic

1. Find subject by `union_id`
2. Else find subject by unique `user_id`
3. Else create new subject
4. If `user_id` is ambiguous, send to `pending_reviews`

### C. Outbound routing logic

Before sending a Feishu outbound action:

1. Identify the person globally using `union_id` / `user_id`
2. Resolve the target `app_context` or `accountId`
3. Read the corresponding app-local `open_id`
4. Build provider target

For Feishu direct messages:

- `target = user:<open_id>`
- `accountId = <matching Feishu account>`

## Recommended workspace layout

```text
identity/
  feishu-user-master.json
  feishu-user-master.md
  feishu-dashboard.md
```

## Why this abstraction matters

The same human may have different `open_id` values in different Feishu apps. A robust system must never confuse:

- global identity resolution
- app-local identity selection
- outbound routing format
