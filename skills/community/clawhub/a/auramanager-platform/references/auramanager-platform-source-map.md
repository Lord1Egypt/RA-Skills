# auramanager-platform source map

Evidence layer for `SKILL.md`. Every contract the skill states is traced to a
current `file:line` here. Re-derive the lines with the verification commands at
the bottom before depending on an exact citation.

## Direct bearer-token HTTP access

| Behavior | File:line |
|---|---|
| Auth middleware accepts bearer token auth | `server/cmd/server/router.go:328-339` |
| Allowed CORS headers include `Authorization` | `server/cmd/server/router.go:136-139` |

The platform skill is API-first: the backend exposes authenticated HTTP routes and
accepts `Authorization` headers directly.

## Workspace routing order

| Behavior | File:line |
|---|---|
| Task-token fast path (`X-Actor-Source: task_token` -> `X-Workspace-ID`) | `server/internal/middleware/workspace.go:14-16` |
| Middleware context beats headers | `server/internal/middleware/workspace.go:17-19` |
| `X-Workspace-Slug` lookup | `server/internal/middleware/workspace.go:20-24` |
| `?workspace_slug=` lookup | `server/internal/middleware/workspace.go:25-29` |
| `X-Workspace-ID` fallback | `server/internal/middleware/workspace.go:30-32` |
| `?workspace_id=` fallback | `server/internal/middleware/workspace.go:32` |
| Allowed CORS headers include both workspace headers | `server/cmd/server/router.go:136-139` |

For non-task-token requests, the practical order is middleware context, then
`X-Workspace-Slug`, then `workspace_slug`, then `X-Workspace-ID`, then
`workspace_id`. Task-token requests are bound to `X-Workspace-ID` first.

## Personal access token endpoints and one-time plaintext behavior

| Behavior | File:line |
|---|---|
| Token routes registered | `server/cmd/server/router.go:353-358` |
| `GET /api/tokens` -> `ListPersonalAccessTokens` | `server/cmd/server/router.go:354` |
| `POST /api/tokens` -> `CreatePersonalAccessToken` | `server/cmd/server/router.go:355` |
| `POST /api/tokens/current/renew` -> `RenewCurrentPersonalAccessToken` | `server/cmd/server/router.go:356` |
| `DELETE /api/tokens/{id}` -> `RevokePersonalAccessToken` | `server/cmd/server/router.go:357` |
| Create response shape includes `Token string` | `server/internal/handler/personal_access_token.go:12-15` |
| Create handler returns raw token in create response | `server/internal/handler/personal_access_token.go:65-68` |
| List response is metadata only | `server/internal/handler/personal_access_token.go:70-93` |

The raw personal access token value is surfaced only at create time; normal list
responses return metadata such as prefix, expiry, and usage timestamps.

## Account and token onboarding surfaces

| Behavior | File:line |
|---|---|
| Public registration page is `/register` | `packages/core/paths/paths.ts:65` |
| Backend registration endpoint is `/auth/register` | `server/cmd/server/router.go:537` |
| Settings exposes the `tokens` tab | `packages/views/settings/components/settings-page.tsx:40-55` |
| Token creation UI calls the personal access token API and receives the plaintext token | `packages/views/settings/components/tokens-tab.tsx:71-73` |

The multi-device, multi-agent coordination explanation is product positioning for
new users; it does not alter the authentication or API contracts above.

## Issue API surface

| Behavior | File:line |
|---|---|
| `/api/issues/search` | `server/cmd/server/router.go:453` |
| `/api/issues/child-progress` | `server/cmd/server/router.go:454` |
| `/api/issues/children` | `server/cmd/server/router.go:455` |
| `/api/issues/grouped` | `server/cmd/server/router.go:456` |
| `GET /api/issues` | `server/cmd/server/router.go:457` |
| `POST /api/issues` | `server/cmd/server/router.go:458` |
| `GET /api/issues/{id}` | `server/cmd/server/router.go:460` |
| `GET /api/issues/{id}/comments` | `server/cmd/server/router.go:461` |
| `GET /api/issues/{id}/timeline` | `server/cmd/server/router.go:462` |
| `GET /api/issues/{id}/children` | `server/cmd/server/router.go:463` |
| `GET /api/issues/{id}/attachments` | `server/cmd/server/router.go:464` |
| `POST /api/issues/{id}/comments` | `server/cmd/server/router.go:465` |
| `PUT /api/issues/{id}` | `server/cmd/server/router.go:470` |
| `DELETE /api/issues/{id}` | `server/cmd/server/router.go:471` |
| `GET /api/issues/{id}/labels` | `server/cmd/server/router.go:472` |
| `POST /api/issues/{id}/labels` | `server/cmd/server/router.go:473` |
| `DELETE /api/issues/{id}/labels/{labelId}` | `server/cmd/server/router.go:474` |
| `GET /api/issues/{id}/metadata` | `server/cmd/server/router.go:475` |
| `PUT /api/issues/{id}/metadata/{key}` | `server/cmd/server/router.go:476` |
| `DELETE /api/issues/{id}/metadata/{key}` | `server/cmd/server/router.go:477` |
| `GET /api/issues/{id}/pull-requests` | `server/cmd/server/router.go:480` |

### Issue payload and enum contract

| Behavior | File:line |
|---|---|
| `IssueResponse` fields | `server/internal/handler/issue.go:34-53` |
| Valid issue statuses | `server/internal/handler/issue.go:57` |
| Valid issue priorities | `server/internal/handler/issue.go:58` |

`IssueResponse` includes `assignee_type` and `assignee_id`, so assignees are
polymorphic. The issue surface also exposes `metadata`, `attachments`, `labels`,
and `reactions`.

## Calendar API surface

| Behavior | File:line |
|---|---|
| `GET /api/calendar/events` | `server/cmd/server/router.go:488` |
| `POST /api/calendar/events` | `server/cmd/server/router.go:489` |
| `PUT /api/calendar/events/{id}` | `server/cmd/server/router.go:490` |
| `DELETE /api/calendar/events/{id}` | `server/cmd/server/router.go:491` |

Calendar event CRUD is part of the backend API, so the platform skill can create
and manage schedules directly.

## Agent and squad orchestration

| Behavior | File:line |
|---|---|
| List and create agents | `server/cmd/server/router.go:1099-1101` |
| List and create squads | `server/cmd/server/router.go:1020-1022` |
| List squad members and member status | `server/cmd/server/router.go:1027-1028` |
| Issue assignee supports `member`, `agent`, or `squad` | `server/internal/handler/issue.go:2654` |
| A squad-assigned issue routes execution to its leader | `server/internal/service/task.go:1639-1658` |

## Verification commands

```bash
cd server
grep -n 'Authorization' cmd/server/router.go
grep -n 'ResolveWorkspaceIDFromRequest\|X-Actor-Source\|X-Workspace-Slug\|workspace_slug\|X-Workspace-ID\|workspace_id' internal/middleware/workspace.go
grep -n '/api/tokens\|ListPersonalAccessTokens\|CreatePersonalAccessToken\|RenewCurrentPersonalAccessToken\|RevokePersonalAccessToken' cmd/server/router.go internal/handler/personal_access_token.go
grep -n 'type CreatePATResponse struct\|Token string' internal/handler/personal_access_token.go
grep -n '/api/issues\|/api/calendar' cmd/server/router.go
grep -n 'type IssueResponse struct\|validIssueStatuses\|validIssuePriorities' internal/handler/issue.go
```
