---
name: daidai-panel-task-crud
description: Create, edit, delete and toggle Dumb Panel cron tasks via its HTTP API, when ddp.exe has no command or a daidai.db edit won't load.
---

# Dumb Panel Task CRUD

Tasks live in the `tasks` table of `Dumb-Panel/daidai.db`. `ddp.exe` only ships
`task list / logs / run / stop` — there is no add, update or delete. Two ways to change
tasks remain: the panel's own Web API (preferred, takes effect immediately), or writing
SQLite directly (requires an Administrator service restart).

Always prefer the API. On `POST`, `PUT` and `DELETE /api/tasks` the server updates the
in-memory scheduler alongside the database, so no elevation and no restart are needed.

## Which route to take

1. Just listing, reading logs or triggering a run → `ddp.exe task list|logs|run|stop`.
2. Creating, renaming, changing a cron expression or command, enabling, disabling or
   deleting → `scripts/ddp_task_api.py` from this skill.
3. Direct `daidai.db` edits are only justified when the backend is stopped or during a
   bulk migration. Afterwards `Restart-Service DumbPanel -Force` (Administrator) is
   required, otherwise the service keeps its stale in-memory task table.
4. After any change, verify with `next_run_at` (see below).

## Quick start

The script finds the panel root by walking up from its own location and the working
directory, looking for `Dumb-Panel/.jwt_secret`. Override with `--panel-root` or the
`DAIDAI_PANEL_ROOT` environment variable.

```bash
S="scripts/ddp_task_api.py"

python "$S" list
python "$S" get 18
python "$S" raw GET /tasks/groups
```

Authentication is handled locally: the script reads `Dumb-Panel/.jwt_secret` and an
unexpired row from `user_sessions`, then signs a short-lived HS256 access JWT. The key,
`jti` and token are never printed or persisted. At least one valid web login session must
exist — sign in through the web UI once if not.

## Create

```bash
python "$S" create --name "nightly backup" \
  --command "task backups/run.py" \
  --cron "15 3 * * *" --delay 300
```

- `--command` is always `task <path relative to Dumb-Panel/scripts/>`; create the script
  file first.
- `--delay` maps to `random_delay_seconds`.
- Add `--disabled` to create an already-disabled task. This is implemented as a second
  call to the disable endpoint, because `POST /tasks` ignores `status` and `enabled`.
- Use `--json '{"timeout":900}'` (or `--json @payload.json`) for extra or override fields.
  Defaults such as notification channel 1, Python 3.12, `env_scope=all` and
  `success_exit_codes="0"` are in `DEFAULT_TASK`; the full field list is in
  `references/api_reference.md`.

## Update, toggle, run

```bash
python "$S" update 18 --patch '{"cron_expression":"20 3 * * *","name":"nightly backup"}'
python "$S" disable 18
python "$S" enable 18
python "$S" run 18
python "$S" stop 18
```

By default `update` does GET → strip read-only fields → merge patch → PUT, so no
configuration is silently cleared. `--patch-only` sends only the patch and should only be
used on builds known to accept partial bodies.

## Delete

```bash
python "$S" delete 19 --yes
```

Only the task record is removed, never the script file. Do not add `delete_script=1` to a
`DELETE` request. `--yes` is an intentional second confirmation; run `get <id>` first.

## Verify that a change took effect

```bash
python "$S" get 18 | python -c "import json,sys; print(json.load(sys.stdin).get('next_run_at'))"
```

- A value such as `2027-01-02T00:00:00+08:00` means the scheduler has picked the job up;
  the change is live, no restart needed.
- Empty or `null` means the row exists but was never loaded — usually a direct DB edit.
- `ddp.exe task run <ID>` is useful for a smoke test, but it starts a separate scheduler in
  the current user session. It does not prove the service account can run the job.

## Constraints and gotchas

- `POST /api/tasks` ignores `status` / `enabled`: every new task starts enabled. Disable
  it afterwards via `PUT /tasks/:id/disable`.
- `POST /api/tasks` also ignores `sort_order` / `list_order` (both become 0). Ordering is
  done through `PUT /tasks/sort` and does not affect execution.
- `ddp.exe task run` may trigger local application-blacklist alerts for `wmic.exe`,
  `reg.exe` and `sc.exe`. Execution is unaffected and the exit code stays 0; do not retry
  or work around the alerts.
- The service injects `TZ=Asia/Shanghai`; Windows Python parses that as a POSIX TZ and
  ends up seven hours off. Panel-run Python scripts should set
  `os.environ["TZ"] = "CST-8"` at the top.
- The service runs as `LocalSystem`, which cannot read the current user's `APPDATA`.
  Scripts relying on per-user credentials need their own file fallback.
- `ddp.exe status` reporting no running `daidai-server` process is a Session 0 visibility
  artefact; trust the backend health endpoint.
- Never place `.jwt_secret`, `daidai.db`, a signed token or any credential value into
  documentation or a repository. Describe locations and procedures only.

## Resources

- `scripts/ddp_task_api.py` — authentication plus the CRUD CLI: `list`, `get`, `create`,
  `update`, `delete`, `run`, `enable`, `disable`, `stop`, `raw`.
- `references/api_reference.md` — endpoint table, task fields, JWT claims, read-only
  fields to strip on PUT, and an error/symptom reference. Load it when investigating an
  unfamiliar endpoint or a failing request.
