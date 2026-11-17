# Dumb Panel Task CLI

`ddp.exe` can list tasks, read their logs, run them and stop them. It cannot create one,
change its cron expression, or delete it. Editing `daidai.db` directly works, but the
service reads its task table only at startup, so nothing changes until
`Restart-Service DumbPanel -Force` — which needs an Administrator shell.

This is a single-file CLI that talks to the panel's own HTTP API instead. The API writes
the row **and** re-registers the job with the live scheduler, so edits take effect
immediately, without elevation and without a restart.

## Contents

| Path | What it is |
| --- | --- |
| `scripts/ddp_task_api.py` | The CLI. Python 3.10+, standard library only. |
| `SKILL.md` | Skill manifest and operating notes. |
| `references/api_reference.md` | Endpoints, task fields, JWT claims, and the error cases found while testing. |

## Setup

There is nothing to install — no dependencies, no package, no build step. Put the script
anywhere and run it with Python 3.10 or newer.

The CLI locates the panel root by walking up from its own directory and the current
directory, looking for `Dumb-Panel/.jwt_secret`. If the panel lives somewhere else:

```bash
python scripts/ddp_task_api.py --panel-root /path/to/panel list
```

or set the environment variable once:

```bash
export DAIDAI_PANEL_ROOT=/path/to/panel
python scripts/ddp_task_api.py list
```

On Windows PowerShell:

```powershell
$env:DAIDAI_PANEL_ROOT = "C:\path\to\panel"
python scripts\ddp_task_api.py list
```

Prerequisites on the panel side:

- The backend is running. Default is `http://127.0.0.1:5700`; the actual port is read
  from `config.yaml`.
- At least one unexpired web login session exists in `user_sessions`. Sign in through the
  web UI once if the CLI reports that none is available.

## Commands

```bash
python scripts/ddp_task_api.py list
python scripts/ddp_task_api.py get 18
python scripts/ddp_task_api.py raw GET /tasks/groups

python scripts/ddp_task_api.py create \
  --name "nightly backup" \
  --command "task backups/run.py" \
  --cron "15 3 * * *" \
  --delay 300

python scripts/ddp_task_api.py update 18 --patch '{"cron_expression":"20 3 * * *"}'
python scripts/ddp_task_api.py disable 18
python scripts/ddp_task_api.py enable 18
python scripts/ddp_task_api.py run 18
python scripts/ddp_task_api.py stop 18
python scripts/ddp_task_api.py delete 19 --yes
```

`--command` is always `task <path relative to Dumb-Panel/scripts/>`, and the script file
must already exist. `--delay` sets the task's random delay in seconds. Extra or override
fields go through `--json '{"timeout":900}'`, or `--json @payload.json` to read a file.

`update` fetches the full task first, strips the read-only fields, merges the patch, then
sends a complete `PUT`. Partial bodies are not reliably accepted. `--patch-only` sends
just the patch for builds that do accept them.

`delete` removes the task record, not the script file, and requires `--yes` on purpose.
Run `get <id>` first to confirm the name.

`raw <METHOD> <path>` calls any `/api` route directly, which covers endpoints the CLI does
not wrap — groups, labels, cron templates, import/export, batch operations and log files.

## Confirming a change actually took effect

```bash
python scripts/ddp_task_api.py get 18 | python -c "import json,sys; print(json.load(sys.stdin)['next_run_at'])"
```

A populated `next_run_at` means the scheduler picked the job up. `null` means the row is
in SQLite but the service never loaded it — almost always the result of a direct DB edit,
in which case a service restart is required.

One caveat: `ddp.exe task run <id>` starts a separate scheduler in the current user
session. A clean exit there does not prove the service account can run the same job.

## Authentication

The API expects `Authorization: Bearer <JWT>`. Rather than scraping a token out of a
browser, the CLI reads the panel's own signing key from `Dumb-Panel/.jwt_secret`, picks an
unexpired session from `user_sessions`, and signs a short-lived HS256 token with matching
claims. The key, the `jti` and the token are never printed or written to disk, and requests
never leave `127.0.0.1`.

This only works on the machine holding the key material. Keep `.jwt_secret` and
`daidai.db` out of version control and out of any published documentation.

Two details that tend to cost time: claims must include `"token_type": "access"` or the
server answers 401 with a token-type error, and local requests need to bypass the system
proxy (`ProxyHandler({})`, or curl's `--noproxy '*'`) or they can hang.

## Quirks worth knowing

- `POST /tasks` ignores `status` and `enabled` in the body. New tasks are always enabled;
  `create --disabled` follows up with a `disable` call to work around it.
- `POST /tasks` also ignores `sort_order` and `list_order` — both land as `0`. Use
  `PUT /tasks/sort`. Ordering does not affect execution.
- The service injects `TZ=Asia/Shanghai` into child processes. Python on Windows parses
  that as a POSIX TZ and ends up seven hours off; scripts run by the panel should set
  `os.environ["TZ"] = "CST-8"` at the top.
- On Windows the service runs as `LocalSystem` in Session 0 and cannot read the current
  user's `APPDATA`. Scripts depending on per-user credentials need their own file fallback.
- `ddp.exe` probing `wmic.exe`, `reg.exe` and `sc.exe` can trip local application
  blacklists. The task still runs and exits 0; no action needed.
- `ddp.exe status` reporting "no running daidai-server process" is a Session 0 visibility
  artefact, not an outage. Check the backend health endpoint instead.

## Compatibility

Verified against Dumb Panel 3.4.2 on Windows with the service hosted by WinSW. Endpoint
names were taken from the shipped frontend bundle (`web/assets/task-*.js`). Other builds
may expose a slightly different route set; `raw GET /tasks` plus the reference doc are the
quickest way to check.

Full endpoint and field tables live in `references/api_reference.md`.
