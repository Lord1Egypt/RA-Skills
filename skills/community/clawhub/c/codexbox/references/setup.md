# codexbox setup

See [SKILL.md](../SKILL.md#security--safety) for the full destructive-operation and unauthenticated-surface warnings before running any mode that binds a port.

## Requirements

- Docker
- Codex auth: `OPENAI_API_KEY` (pay-as-you-go) or a ChatGPT Plus/Pro/Team subscription (`codexbox login --device-auth`)
- Optional: SSH key for git-over-SSH inside the container (the installer generates one)

For ordinary agent work, use the installed `codexbox` command from the target
workspace. Do not replace it with a hand-written Docker invocation. The
wrapper handles the workspace, state, SSH, image, and nested launch context.

## Quick Install (wrapper)

The one-liner installer pulls the image, creates persistent Codex/SSH dirs, and installs the `codexbox` wrapper on `PATH`.

**Recommended: download, inspect, then run.** Piping a remote script straight into bash executes unreviewed remote code as you. Download it, read it, then run it:

```bash
curl -fsSL -o install.sh https://raw.githubusercontent.com/psyb0t/docker-codexbox/main/install.sh
less install.sh          # read it before running anything
bash install.sh          # minimal image, the default
# CODEXBOX_FULL=1 bash install.sh        # full image, every development tool pre-installed
# bash install.sh codex                  # custom command name
```

`CODEXBOX_FULL=1` must be set before `install.sh` runs: the installer needs it in `bash`'s environment. The choice is baked into the installed wrapper; you don't need to set it again afterward.

### Install from a local checkout

From this repository, build and install without pulling a published codexbox
image:

```bash
make install       # minimal image
make install-full  # full image

# wrapper only, no build or pull; select full when needed
make install-wrapper
CODEXBOX_FULL=1 make install-wrapper
```

The installer-only `CODEXBOX_SRC_LOCAL=true` flag skips `docker pull` and
requires the selected local image to already exist. `make install-wrapper`
uses that existing image without rebuilding it.

**Verify:** `codexbox --version` should print the codex CLI version.

```bash
codexbox                                  # interactive
codexbox exec "inspect this workspace"    # one-shot
CODEXBOX_FULL=1 codexbox exec "run tests" # temporary full image
```

For a wrapper-started server, use `CODEXBOX_ENV_` before every variable that
must reach the container. For example,
`CODEXBOX_ENV_CODEXBOX_API_MODE=1 codexbox` starts API mode.

### Sibling boxes

Install `codexbox`, `claudebox`, and `pibox` in the same command directory,
normally `/usr/local/bin`, to make the sibling commands available inside a
box. The parent mounts only the wrapper files read-only. A sibling wrapper then
runs through the host Docker daemon and mounts its own host data directory.

## Image Variants

| Image | Tag | Contents |
|---|---|---|
| Minimal (default) | `psyb0t/codexbox:latest` | Codex, Node.js, Python, `uv`, Docker, Git, `jq`, `curl` |
| Full | `psyb0t/codexbox:latest-full` | Everything in minimal + Go, gopls/Delve/golangci-lint/staticcheck/gofumpt, Python lint/type/test tooling, JS/TS lint/format/framework CLIs, GitHub CLI, Terraform, kubectl, Helm, build tools (CMake/ClangFormat/Valgrind/GDB/strace/ltrace), Postgres/MySQL/SQLite/Redis clients, editors/shell tools |

`CODEXBOX_FULL` is binary: unset or `0` selects minimal, `1` selects full, and any other value fails. `CODEXBOX_IMAGE` is the highest-priority explicit override if you want a specific tag regardless of `CODEXBOX_FULL`.

## Manual Docker Use

Use raw Docker only for an explicitly requested container deployment. Use the
wrapper for interactive, one-shot, and local service runs. All direct Docker
shapes for service deployment are in [../SKILL.md](../SKILL.md).

Minimal foreground-mode boilerplate:

```bash
docker run -d --name codexbox \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD:/workspace" \
  -v "$HOME/.codex:/home/aicode/.codex" \
  <mode env vars here> \
  -p <port>:<port> \
  psyb0t/codexbox:latest
```

## Environment Variable Reference

### Wrapper-only (host-side, read by `wrapper.sh`, not passed into the container as-is)

| Var | Default | What it does |
|---|---|---|
| `OPENAI_API_KEY` | none | Forwarded into the container; seeds `auth.json` when a container first starts |
| `OPENAI_BASE_URL` | none | Point codex at an OpenAI-compatible endpoint instead of the default API |
| `CODEXBOX_IMAGE` | installed image | Override the image the wrapper runs |
| `CODEXBOX_FULL` | installed choice (`0` initially) | `0` forces minimal, `1` forces full |
| `CODEXBOX_DATA_DIR` | `~/.codex` | Host dir mounted as `CODEX_HOME` (auth + config + sessions + per-workspace root-session pins) |
| `CODEXBOX_SSH_DIR` | `~/.ssh/codexbox` | SSH key dir mounted into the container |
| `CODEXBOX_MAX_MEM` | `10g` | Per-container memory limit |
| `CODEXBOX_CONTAINER_NAME` | derived from `$PWD` | Override the per-workspace container name |
| `CODEXBOX_ENV_*` | none | Forward arbitrary env into the container (prefix stripped: `CODEXBOX_ENV_FOO=bar` → `FOO=bar` inside) |
| `CODEXBOX_MOUNT_*` | none | Mount extra host dirs (`/host:/container`, or a bare path for same-path-both-sides) |
| `CODEXBOX_MODE_CRON` / `CODEXBOX_MODE_CRON_FILE` | none | Wrapper trigger: starts the cron scheduler as a long-running background container instead of the interactive one. Translated internally to `CODEXBOX_CRON_MODE` / `CODEXBOX_CRON_MODE_FILE` inside the container. |

### Container-side mode flags

Naming convention: `CODEXBOX_<MODE>_MODE=1` is the on/off flag, `CODEXBOX_<MODE>_MODE_<KNOB>=...` is its config.

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_API_MODE` | `0` | Boot the HTTP API server (foreground) |
| `CODEXBOX_TELEGRAM_MODE` | `0` | Boot the Telegram bot (foreground) |
| `CODEXBOX_CRON_MODE` | `0` | Boot the cron scheduler (foreground; in-thread when telegram is also on) |
| `CODEXBOX_MCP_MODE` | `0` | Expose MCP, mounted at `/mcp/` in API mode, or as a standalone sidecar elsewhere |

Foreground modes (API/Telegram/Cron) are mutually exclusive, except Telegram+Cron together (cron runs in-thread inside the telegram process). API wins if set alongside anything else. MCP mode is independent: it coexists with whatever foreground mode is running, or with none at all (shell-only + MCP sidecar).

### API mode config

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_API_MODE_PORT` | `8080` | Port the API server binds to |
| `CODEXBOX_API_MODE_TOKEN` | empty | Bearer token for the API surface (`/run`, `/files/*`, `/openai/v1/*`). Empty = no auth |

With `CODEXBOX_API_MODE_TOKEN` unset the API surface (`/run`, `/files/*`, `/openai/v1/*`) is unauthenticated: anyone who can reach it gets run-execution and full workspace file access. Set the token and bind to loopback / behind an authenticating proxy before exposing it beyond localhost.

### Telegram mode config

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_TELEGRAM_MODE_TOKEN` | none | Bot token from @BotFather |
| `CODEXBOX_TELEGRAM_MODE_CONFIG` | `~/.aicodebox/telegram.yml` | Path to the telegram config YAML |
| `CODEXBOX_TELEGRAM_MODE_OVERRIDES` | `~/.aicodebox/telegram_overrides.json` | Per-chat override store (model/effort/system prompts) |

### Cron mode config

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_CRON_MODE_FILE` | none | Path to the cron YAML |
| `CODEXBOX_CRON_MODE_HISTORY_DIR` | `~/.aicodebox/cron` | Cron state root. Run history lands under `<root>/history/<workspace>/<timestamp>-<job>/` (`meta.json`, `stdout.log`, `stderr.log`, `result.txt`, `telegram.json`), per-job summaries at `<root>/<job>.jsonl`, and the telegram reply inbox at `<root>/telegram_messages.json` |

### MCP mode config

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_MCP_MODE_PORT` | `8081` | Port the sidecar MCP server binds to (ignored when mounted inside API mode) |
| `CODEXBOX_MCP_MODE_TOKEN` | empty | Bearer token for MCP. Empty = no auth. No fallback to `API_MODE_TOKEN` |
| `CODEXBOX_MCP_MODE_ALLOWED_HOSTS` | loopback hosts | Comma-separated MCP `Host` allowlist. Add each reverse-proxy host name |
| `CODEXBOX_MCP_MODE_ALLOWED_ORIGINS` | loopback HTTP origins | Comma-separated MCP browser Origin allowlist. Add each reverse-proxy origin |

With `CODEXBOX_MCP_MODE_TOKEN` unset the MCP surface (`run_prompt`, `list_files`, `read_file`, `write_file`, `delete_file`) is unauthenticated: anyone who can reach it gets full workspace file access. This surface has its own bearer; setting `CODEXBOX_API_MODE_TOKEN` does not protect it. Set the token and bind to loopback / behind an authenticating proxy before exposing it beyond localhost.

MCP also keeps DNS rebinding protection enabled. Loopback hosts and origins work by default; a reverse proxy, tunnel, or public DNS name needs its exact `CODEXBOX_MCP_MODE_ALLOWED_HOSTS` and browser `CODEXBOX_MCP_MODE_ALLOWED_ORIGINS` values added before MCP is reachable through it.

### Workspace & runtime

| Var | Default | What it does |
|---|---|---|
| `CODEXBOX_WORKSPACE` | `/workspace` | Root workspace dir inside the container |
| `CODEXBOX_CONTAINER_NAME` | `aicodebox` | Scopes per-container state files (auth, etc.) |
| `CODEXBOX_AVAILABLE_MODELS` | none | **Required for API mode.** CSV list returned by `/openai/v1/models` and shown in the Telegram `/model` picker |
| `CODEXBOX_AVAILABLE_EFFORTS` | `none,minimal,low,medium,high,xhigh,max` | Override the effort/reasoning list shown by the Telegram `/effort` picker |
| `CODEXBOX_MODEL` | none | Default model for the shell path (interactive TUI and `codexbox exec`), passed as `-c model="..."` before your own arguments, so `-m` still wins. It does not set the model of API, MCP, Telegram or cron runs. |
| `CODEXBOX_REASONING_EFFORT` | none | Default reasoning effort for the shell path, passed as `-c model_reasoning_effort="..."`. Same scope as `CODEXBOX_MODEL`. Neither has an `AICODEBOX_` alias. |

Every `CODEXBOX_X` name above also works as `AICODEBOX_X` (the base image's native naming): the entrypoint translates `CODEXBOX_X` to `AICODEBOX_X` when only the codexbox-prefixed one is set. If both are set, `AICODEBOX_X` wins.

### Init scripts and user bin

`$HOME/.aicodebox/bin` is on `PATH` ahead of everything else, for codex, for init scripts, and for `docker exec` shells. `$HOME/.aicodebox/init.d/*.sh` run once per container, after the image's own `/aicodebox-init.d/*.sh`, as `aicode` with passwordless sudo; a failing script is logged and the rest still run. Init now runs once per container rather than once per bind-mounted state directory, so scripts placed there need to tolerate re-running on every new container.

## Ports

| Port | Default var | Service |
|---|---|---|
| 8080 | `CODEXBOX_API_MODE_PORT` | HTTP API (`/run`, `/files`, `/openai/v1/*`) + MCP mounted at `/mcp/` when `CODEXBOX_MCP_MODE=1` |
| 8081 | `CODEXBOX_MCP_MODE_PORT` | Standalone MCP sidecar, only when MCP mode is on and API mode is not |

No port is exposed by default in Telegram-only or cron-only or shell-only deployments (they're outbound-only / no HTTP surface unless MCP mode is also enabled).

## Auth Setup

### API key

```bash
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  -v "$PWD/.codex:/home/aicode/.codex" \
  psyb0t/codexbox:latest \
  exec "say HELLO"
```

Seeded into `$CODEX_HOME/auth.json` the first time each container starts (`codex login --with-api-key` under the hood). Safe to leave set permanently: it never overwrites an existing ChatGPT-subscription login.

### ChatGPT subscription

```bash
docker run -it \
  -v "$HOME/.codex:/home/aicode/.codex" \
  psyb0t/codexbox:latest \
  login --device-auth
```

Prints a URL + short code for one-time browser approval. `~/.codex` **must** be bind-mounted or the login is lost when the container is removed. Every later run against the same bind-mounted `~/.codex` reuses it, no `OPENAI_API_KEY` needed. `codex login status` reports the active mode; `codex logout` clears it.

## Management

```bash
codexbox stop              # stop this dir's running container(s)
codexbox clear-session      # drop saved codex sessions (keeps auth + config)
docker logs -f codexbox-api # tail logs for a manually-run named container
docker pull psyb0t/codexbox:latest   # update
```

## Development / Testing

The builds pull the published aicodebox base, so no sibling checkout is needed.

```bash
make help              # list targets
make build             # psyb0t/codexbox:latest on psyb0t/aicodebox:v0.18.4
make build-full        # psyb0t/codexbox:latest-full on psyb0t/aicodebox:v0.18.4-full
make lint              # shellcheck, shfmt, ruff and pyright, all in containers
make test-ci           # credential-free tests, as CI runs them
make test              # full e2e suite (needs .env.test: OPENAI_API_KEY or a subscription login, optional Telegram creds)
```

Full details: https://psyb0t.github.io/docker-codexbox/development/
