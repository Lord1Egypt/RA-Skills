# Dropbox scopes

The OAuth scopes Dropbox connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/dropbox#permissions.

```bash
maton connection create dropbox --scopes files.metadata.read
```

| Scope | Requested |
| --- | --- |
| `files.metadata.write` | By default |
| `files.metadata.read` | By default |
| `files.content.write` | By default |
| `files.content.read` | By default |
| `sharing.write` | By default |
| `sharing.read` | By default |
| `account_info.read` | Always |
