# Confluence scopes

The OAuth scopes Confluence connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/confluence#permissions.

```bash
maton connection create confluence --scopes read:content:confluence
```

| Scope | Requested |
| --- | --- |
| `read:content:confluence` | By default |
| `write:content:confluence` | By default |
| `read:content-details:confluence` | By default |
| `read:space-details:confluence` | By default |
| `delete:content:confluence` | By default |
| `read:audit-log:confluence` | By default |
| `write:audit-log:confluence` | By default |
| `read:page:confluence` | By default |
| `write:page:confluence` | By default |
| `delete:page:confluence` | By default |
| `read:attachment:confluence` | By default |
| `write:attachment:confluence` | By default |
| `delete:attachment:confluence` | By default |
| `read:blogpost:confluence` | By default |
| `write:blogpost:confluence` | By default |
| `delete:blogpost:confluence` | By default |
| `read:custom-content:confluence` | By default |
| `write:custom-content:confluence` | By default |
| `delete:custom-content:confluence` | By default |
| `read:comment:confluence` | By default |
| `write:comment:confluence` | By default |
| `delete:comment:confluence` | By default |
| `read:template:confluence` | By default |
| `write:template:confluence` | By default |
| `read:label:confluence` | By default |
| `write:label:confluence` | By default |
| `read:group:confluence` | By default |
| `read:user:confluence` | By default |
| `read:configuration:confluence` | By default |
| `read:space:confluence` | By default |
| `write:space:confluence` | By default |
| `delete:space:confluence` | By default |
| `read:space.permission:confluence` | By default |
| `read:user.property:confluence` | By default |
| `read:space.setting:confluence` | By default |
| `read:inlinetask:confluence` | By default |
| `read:task:confluence` | By default |
| `write:task:confluence` | By default |
| `read:whiteboard:confluence` | By default |
| `write:whiteboard:confluence` | By default |
| `delete:whiteboard:confluence` | By default |
| `read:database:confluence` | By default |
| `write:database:confluence` | By default |
| `delete:database:confluence` | By default |
| `read:folder:confluence` | By default |
| `offline_access` | Always |
