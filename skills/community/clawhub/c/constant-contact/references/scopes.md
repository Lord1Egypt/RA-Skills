# Constant Contact scopes

The OAuth scopes Constant Contact connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/constant-contact#permissions.

```bash
maton connection create constant-contact --scopes account_update
```

| Scope | Requested |
| --- | --- |
| `account_update` | By default |
| `contact_data` | By default |
| `campaign_data` | By default |
| `offline_access` | Always |
| `account_read` | Always |
