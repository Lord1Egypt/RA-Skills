# Calendly scopes

The OAuth scopes Calendly connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/calendly#permissions.

```bash
maton connection create calendly --scopes webhooks:read
```

| Scope | Requested |
| --- | --- |
| `webhooks:read` | By default |
| `webhooks:write` | By default |
| `availability:read` | By default |
| `availability:write` | By default |
| `event_types:read` | By default |
| `event_types:write` | By default |
| `locations:read` | By default |
| `routing_forms:read` | By default |
| `shares:write` | By default |
| `scheduled_events:read` | By default |
| `scheduled_events:write` | By default |
| `scheduling_links:write` | By default |
| `groups:read` | By default |
| `organizations:read` | By default |
| `organizations:write` | By default |
| `users:read` | Always |
