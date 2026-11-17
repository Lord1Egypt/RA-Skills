# Dumb Panel Task API Reference

Environment used for verification: Dumb Panel 3.4.2 on Windows, hosted as the
`DumbPanel` service (WinSW / `LocalSystem`). Web base `http://127.0.0.1:5700`, API prefix
`/api`, database `Dumb-Panel/daidai.db`. The port comes from `server.port` in
`config.yaml`.

## 1. Three ways to change a task

| Route | Capabilities | Takes effect immediately | When to use |
| --- | --- | --- | --- |
| `ddp.exe task ...` | `list` / `logs` / `run` / `stop` | read-only or manual run | inspection, troubleshooting, smoke tests |
| Panel Web API | full CRUD, toggles, ordering, import/export | **yes**, the server re-registers with the scheduler | default choice |
| Direct `daidai.db` edit | anything in theory | **no**, needs `Restart-Service DumbPanel -Force` (Administrator) | backend stopped, bulk migration |

`ddp.exe --help` lists every subcommand; there is no `task add`, `task update` or
`task delete`. Note that `ddp.exe task run` does not go through the service — it starts a
separate scheduler in the current user session. A successful manual run therefore does
not prove the service account can execute the same job (`LocalSystem` / Session 0).

## 2. Authentication

The API expects `Authorization: Bearer <JWT>`. For a local, non-interactive script, the
token can be signed locally:

1. Key: `Dumb-Panel/.jwt_secret`, printable text. **Use the raw file bytes** (`strip()`
   is enough); do not hex- or base64-decode it.
2. Session: take an unexpired row from `user_sessions` for `jti`, `user_id`, `username`,
   then read `role` from `users`. Middleware checks that `jti` exists in `user_sessions`,
   is not in `token_blocklist`, and that `users.enabled = 1`.
3. Sign an HS256 JWT with HMAC-SHA256:

```json
{
  "user_id": 1,
  "username": "<your panel username>",
  "role": "admin",
  "jti": "<user_sessions.jti>",
  "token_type": "access",
  "exp": 1730000000,
  "iat": 1729996400
}
```

`"token_type": "access"` is **required**; omitting it returns 401 with a token-type error.
Variants such as `"token_type": "web"` or `"token_kind": "access"` do not work.

When `jwt.secret` is left empty in `config.yaml`, the panel generates a secret and
persists it to `.jwt_secret`. `access_token_expire` defaults to 480h, but a self-signed
one-hour token is plenty — sign a fresh one per invocation.

Local requests must bypass the system proxy: `urllib.request.build_opener(ProxyHandler({}))`
or curl's `--noproxy '*'`. A transparent proxy can slow or break calls to `127.0.0.1`.

## 3. Endpoints

Route names were extracted from the API module in the shipped frontend bundle
(`web/assets/task-*.js`). Entries marked "verified" were exercised against 3.4.2; the rest
are listed from the frontend definitions.

### Task CRUD

| Method | Path | Description | Status |
| --- | --- | --- | --- |
| GET | `/tasks` | list tasks, returns `{"data":[...]}` | verified |
| GET | `/tasks/groups` | groups | untested |
| GET | `/tasks/labels` | labels | untested |
| GET | `/tasks/notification-channels` | notification channels | untested |
| POST | `/tasks` | create a task | verified, 201 |
| PUT | `/tasks/:id` | update a task | verified, 200 |
| DELETE | `/tasks/:id` | delete a task | verified, 200 |
| PUT | `/tasks/:id/enable` | enable | verified, 200 |
| PUT | `/tasks/:id/disable` | disable | verified, 200 |
| PUT | `/tasks/:id/run` | trigger a server-side run | frontend definition |
| PUT | `/tasks/:id/stop` | stop a running task | frontend definition |
| PUT | `/tasks/:id/pin` / `/unpin` | pin / unpin | frontend definition |
| POST | `/tasks/:id/copy` | duplicate | frontend definition |
| PUT | `/tasks/sort` | reorder, body `{source_id,target_id,position}` | frontend definition |
| POST | `/tasks/import` | import, body `{tasks:[...]}` | frontend definition |
| GET | `/tasks/export` | export | frontend definition |

### Batch, logs, helpers

| Method | Path |
| --- | --- |
| PUT | `/tasks/batch`, `/tasks/batch/enable`, `/tasks/batch/disable`, `/tasks/batch/add-labels`, `/tasks/batch/notify` |
| DELETE | `/tasks/batch/delete`, `/tasks/clean-logs` |
| POST | `/tasks/batch/run`, `/tasks/delete-preview`, `/tasks/cron/parse` |
| GET | `/tasks/cron/templates`, `/tasks/:id/stats`, `/tasks/:id/latest-log`, `/tasks/:id/live-logs`, `/tasks/:id/log-files` |
| GET | `/tasks/:id/log-files/:filename`, `/raw-ticket`, `/archive-ticket`, `/archive` |
| DELETE | `/tasks/:id/log-files/:filename` |

The `raw` subcommand reaches any of them:

```bash
python scripts/ddp_task_api.py raw POST /tasks/cron/parse --json '{"expression":"15 3 * * *"}'
```

## 4. Task fields

Fields returned by `GET /tasks`:

| Group | Fields |
| --- | --- |
| Identity | `id`, `name`, `command`, `python_version`, `task_type` |
| Schedule | `cron_expression`, `cron_expressions`, `random_delay_seconds`, `stop_schedule`, `depends_on`, `allow_multiple_instances`, `timeout`, `success_exit_codes`, `max_retries`, `retry_interval` |
| State | `status` (1/0), `enabled` (bool), `last_run_at`, `last_run_status`, `last_running_time`, `last_skip_at`, `last_skip_reason`, `pid`, `log_path`, `next_run_at` |
| Timestamps | `created_at`, `updated_at` |
| Display | `sort_order`, `list_order`, `is_pinned`, `labels`, `display_labels`, `subscription_labels` |
| Notifications | `notify_on_failure`, `notify_on_success`, `notify_on_abort`, `notification_channel_id`, `notification_channel_enabled`, `notification_channel_name` |
| Environment | `env_scope`, `env_groups`, `env_names` |
| Hooks | `task_before`, `task_after` |

### Read-only fields to strip before PUT

`id`, `created_at`, `updated_at`, `last_run_at`, `last_run_status`,
`last_running_time`, `last_skip_at`, `last_skip_reason`, `pid`, `log_path`,
`next_run_at`, `display_labels`, `subscription_labels`,
`notification_channel_name`, `notification_channel_enabled`.

The CLI's `update` follows GET → strip → merge patch → PUT and returns 200 with no
lost fields. `--patch-only` has not been verified against this build; avoid it on
production tasks.

### Default POST body

```json
{
  "name": "nightly backup",
  "command": "task backups/run.py",
  "cron_expression": "15 3 * * *",
  "task_type": "cron",
  "status": 1,
  "enabled": true,
  "python_version": "3.12",
  "random_delay_seconds": 300,
  "timeout": 0,
  "success_exit_codes": "0",
  "max_retries": 0,
  "retry_interval": 0,
  "env_scope": "all",
  "env_groups": [],
  "env_names": [],
  "notify_on_failure": true,
  "notify_on_success": false,
  "notify_on_abort": false,
  "notification_channel_id": 1,
  "allow_multiple_instances": false,
  "is_pinned": false,
  "labels": [],
  "task_before": "",
  "task_after": "",
  "stop_schedule": "",
  "depends_on": null
}
```

`command` runs with `Dumb-Panel/scripts/` as its working directory and always has the form
`task <relative path>`.

## 5. Verified behaviour

| Operation | Result | Finding |
| --- | --- | --- |
| `POST /tasks` | 201, `next_run_at` populated immediately | the scheduler registers jobs dynamically; no service restart needed |
| `POST /tasks` with `status:0, enabled:false` | 201, but returns `enabled:true, status:1` | **POST ignores enable flags**; disable with a follow-up call |
| `POST /tasks` with `sort_order/list_order` | both land as 0 | ordering goes through `/tasks/sort` |
| `PUT /tasks/:id` changing name and cron | 200, `next_run_at` recalculated | full-body merge works |
| `PUT /tasks/:id/disable` | 200, `status=0, enabled=false` | correct way to disable |
| `PUT /tasks/:id/enable` | 200, `status=1, enabled=true` | reversible |
| `DELETE /tasks/:id` | 200 | removes the record only; script files are untouched |
| `ddp.exe task run <id>` | exit code 0 | local blacklist alerts for `wmic` / `reg` / `sc` do not affect execution |

When testing against a live panel, use a cron expression that will not fire soon
(for example `0 0 1 1 *`) and delete the task afterwards.

## 6. Error reference

| Symptom | Cause |
| --- | --- |
| 401 `{"error":"missing authorization token"}` | no `Authorization` header |
| 401 `{"error":"token type error"}` | claims missing `"token_type":"access"` |
| 401 `{"error":"invalid or expired token"}` | wrong signing key, expired `exp`, unknown or blocklisted `jti` |
| 404 `{"error":"route not found"}` | wrong path (for example `/api/task/list`; the correct one is `/api/tasks`) |
| New task has empty `next_run_at` | direct DB write was never loaded by the scheduler; restart the service |
| `ddp.exe status` reports no running server process | Session 0 visibility artefact; check the backend health endpoint instead |

## 7. Direct database edits (not recommended)

Only when the backend is stopped or during a bulk migration:

- The `tasks` table has primary key `id`, uses `cron_expression` (**not** `cron`), and
  stores the enable flag in `status`. There is no `enabled` column — that is synthesised
  by the API layer.
- With `daidai.db-wal` / `-shm` present, editing the file by hand can corrupt it. Always
  go through a sqlite3 connection and commit properly.
- A restart is mandatory afterwards: `Restart-Service DumbPanel -Force`, Administrator.
  The service definition is in `DumbPanel.xml` with `onfailure action="restart"`.
- Back up `daidai.db` first.
- `ddp.exe backup create` exports task configuration; `GET /tasks/export` is another way
  to keep a reference copy before rebuilding.

## 8. Related files

| Path | Purpose |
| --- | --- |
| `Dumb-Panel/.jwt_secret` | session signing key (**sensitive**, never commit or publish) |
| `Dumb-Panel/daidai.db` | tasks, users, sessions, logs |
| `config.yaml` | `server.port`, data directory |
| `web/assets/task-*.js` | frontend API module, source for endpoint definitions |
| `web/assets/apiData-*.js` | built-in API documentation (auth notes, route listing) |
