# Agent Burner

Disposable email API for agents. No signup, no API key.

```bash
# create an inbox
curl -X POST https://api.agentburner.com/inbox
# {"address":"a3f7@caledy.com","key":"550e8400-..."}

# read emails
curl https://api.agentburner.com/inbox/550e8400-...
# {"entries":[{"from":"...","subject":"...","id":"..."}]}

# get full email
curl https://api.agentburner.com/inbox/550e8400-.../EMAIL_ID
# {"body":"...","html":"...","urls":["..."]}
```

## Install as a skill

```bash
npx skills add jsemldonado/agent-burner
```

Or point your agent at [agentburner.com/skill.md](https://agentburner.com/skill.md).

## API

| Endpoint | Description |
|----------|-------------|
| `POST /inbox` | Create inbox (returns address, key, ttl) |
| `GET /inbox/:key` | List emails |
| `GET /inbox/:key/:id` | Full email with extracted URLs |
| `DELETE /inbox/:key` | Delete inbox (optional, auto-expires) |

No auth. Inboxes expire after 1 hour (max 6). URLs extracted automatically.

## Links

- [SKILL.md](./SKILL.md) — Full API reference
- [llms.txt](./llms.txt) — LLM-friendly index
- [agentburner.com](https://agentburner.com) — Website
- [api.agentburner.com](https://api.agentburner.com) — API
