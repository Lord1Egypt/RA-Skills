# Dropbox Business scopes

The OAuth scopes Dropbox Business connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/dropbox-business#permissions.

```bash
maton connection create dropbox-business --scopes files.metadata.read
```

| Scope | Requested |
| --- | --- |
| `files.metadata.read` | By default |
| `files.content.write` | By default |
| `files.content.read` | By default |
| `sharing.write` | By default |
| `sharing.read` | By default |
| `file_requests.write` | By default |
| `file_requests.read` | By default |
| `team_data.member` | By default |
| `team_data.team_space` | By default |
| `team_data.governance.write` | By default |
| `team_data.governance.read` | By default |
| `team_data.content.write` | By default |
| `team_data.content.read` | By default |
| `files.team_metadata.write` | By default |
| `members.write` | By default |
| `members.read` | By default |
| `groups.write` | By default |
| `groups.read` | By default |
| `sessions.modify` | By default |
| `sessions.list` | By default |
| `events.read` | By default |
| `account_info.read` | Always |
| `team_info.read` | Always |
