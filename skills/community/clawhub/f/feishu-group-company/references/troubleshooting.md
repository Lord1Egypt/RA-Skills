# Troubleshooting

## Expected behavior

### Plain message, no @mention
- Coordinator account: replies once
- Specialist accounts: reject with `no bot mention`

Expected log clues:
- Specialist: `rejected: no bot mention in group ...`
- Coordinator: `dispatch complete (replies=1)`

### Message that @mentions a specialist bot
- Mentioned specialist: `dispatch complete (replies=1)`
- Coordinator: `dispatch complete (replies=0)`
- Other specialists: `rejected: no bot mention`

## Common mistakes

### 1. Used `group` instead of `groups`
Wrong:
```json
"accounts": {
  "fullstack-dev": {
    "group": {
      "oc_xxx": { "requireMention": true }
    }
  }
}
```

Right:
```json
"accounts": {
  "fullstack-dev": {
    "groups": {
      "oc_xxx": { "requireMention": true }
    }
  }
}
```

### 2. Renamed accountId but forgot bindings
If the account is renamed from `bot-fullstack-dev` to `fullstack-dev`, update bindings too:
```json
{
  "agentId": "fullstack-dev",
  "match": {
    "channel": "feishu",
    "accountId": "fullstack-dev"
  }
}
```

### 3. Specialist bot lacks Feishu group message permission
Symptoms:
- No inbound log lines for that account in the target group
- Bot works in DM but not in group

### 4. Group top-level rule left open for everyone
If top-level `channels.feishu.groups.<chatId>.requireMention` is `false`, every bot that receives group traffic may answer unless it has its own stricter per-account override.

## Recommended verification sequence

1. Send a plain message in the group
2. Confirm only coordinator replies
3. @mention one specialist bot
4. Confirm only that specialist replies
5. Confirm coordinator finishes with `replies=0` on that mentioned-specialist case
