# Fireflies access policy

An access policy limits which endpoints Fireflies connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/fireflies#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Fireflies: its 1 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create fireflies --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "POST", "path": "graphql", "when": {"graphql": "query"}}
  ],
  "deny": []
}
```

## Endpoints

The Fireflies endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | graphql (queries only) | read | graphql | Run GraphQL queries: read transcripts, meetings, users, channels, analytics and scheduler data. |
| POST | graphql (mutations only) | write | graphql | Run GraphQL mutations: upload or delete transcripts, change meetings, roles and groups, ask AskFred, create bookings. |
