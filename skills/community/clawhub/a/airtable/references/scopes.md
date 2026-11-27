# Airtable scopes

The OAuth scopes Airtable connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/airtable#permissions.

```bash
maton connection create airtable --scopes data.records:read
```

| Scope | Requested |
| --- | --- |
| `data.records:read` | By default |
| `schema.bases:read` | By default |
| `data.recordComments:read` | By default |
| `data.recordComments:write` | By default |
| `data.records:write` | By default |
| `schema.bases:write` | By default |
| `user.email:read` | Always |
