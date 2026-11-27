# Cal.com scopes

The OAuth scopes Cal.com connections can ask for. Pass the ones the task needs with `--scopes` (repeatable or comma-separated) when creating the connection, or to `maton connection reauthorize` to change them later. *Always* scopes are added whatever you pass, *By default* ones are requested when you pass none, and *Optional* ones only when you pass them. Change them only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/calcom#permissions.

```bash
maton connection create cal-com --scopes EVENT_TYPE_READ
```

| Scope | Requested |
| --- | --- |
| `EVENT_TYPE_READ` | By default |
| `EVENT_TYPE_WRITE` | By default |
| `BOOKING_READ` | By default |
| `BOOKING_WRITE` | By default |
| `SCHEDULE_READ` | By default |
| `SCHEDULE_WRITE` | By default |
| `APPS_READ` | By default |
| `APPS_WRITE` | By default |
| `PROFILE_WRITE` | By default |
| `WEBHOOK_READ` | By default |
| `WEBHOOK_WRITE` | By default |
| `VERIFIED_RESOURCES_READ` | By default |
| `VERIFIED_RESOURCES_WRITE` | By default |
| `CREDITS_READ` | By default |
| `CREDITS_WRITE` | By default |
| `INSIGHTS_READ` | By default |
| `TEAM_EVENT_TYPE_READ` | By default |
| `TEAM_EVENT_TYPE_WRITE` | By default |
| `TEAM_BOOKING_READ` | By default |
| `TEAM_SCHEDULE_READ` | By default |
| `TEAM_SCHEDULE_WRITE` | By default |
| `TEAM_PROFILE_READ` | By default |
| `TEAM_PROFILE_WRITE` | By default |
| `TEAM_MEMBERSHIP_READ` | By default |
| `TEAM_MEMBERSHIP_WRITE` | By default |
| `TEAM_APPS_READ` | By default |
| `TEAM_APPS_WRITE` | By default |
| `TEAM_ROUTING_FORM_READ` | By default |
| `TEAM_ROUTING_FORM_WRITE` | By default |
| `TEAM_WORKFLOW_READ` | By default |
| `TEAM_WORKFLOW_WRITE` | By default |
| `TEAM_VERIFIED_RESOURCES_READ` | By default |
| `TEAM_VERIFIED_RESOURCES_WRITE` | By default |
| `TEAM_INSIGHTS_READ` | By default |
| `ORG_EVENT_TYPE_READ` | By default |
| `ORG_BOOKING_READ` | By default |
| `ORG_SCHEDULE_READ` | By default |
| `ORG_SCHEDULE_WRITE` | By default |
| `ORG_PROFILE_READ` | By default |
| `ORG_PROFILE_WRITE` | By default |
| `ORG_MEMBERSHIP_READ` | By default |
| `ORG_MEMBERSHIP_WRITE` | By default |
| `ORG_ROUTING_FORM_READ` | By default |
| `ORG_ROUTING_FORM_WRITE` | By default |
| `ORG_WEBHOOK_READ` | By default |
| `ORG_WEBHOOK_WRITE` | By default |
| `ORG_INSIGHTS_READ` | By default |
| `ORG_ATTRIBUTES_READ` | By default |
| `ORG_ATTRIBUTES_WRITE` | By default |
| `PROFILE_READ` | Always |
