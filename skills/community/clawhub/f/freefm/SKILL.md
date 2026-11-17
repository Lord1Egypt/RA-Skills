---
name: freefm
description: Set up and operate the FreeFM Rust app for NetEase Private FM, including its TUI, QR login, read-only preview, append-only sync, diagnostics, and zero-LLM scheduling.
license: MIT
metadata:
  openclaw:
    emoji: "🎵"
    homepage: https://github.com/Yuxin-Qiao/FreeFM
    os: [darwin, linux]
  hermes:
    tags: [music, netease, private-fm, cli, automation, zero-llm]
    category: media
    requires_toolsets: [terminal]
---

# FreeFM

Operate FreeFM as a one-shot native CLI. Use an Agent only for interactive
setup or troubleshooting; scheduled synchronization must execute the binary
directly without a model turn.

## Guardrails

- Work only with the user's own NetEase Cloud Music account.
- Never ask the user to paste `MUSIC_U`, cookies, session files, or QR keys.
- Never print, inspect, summarize, upload, or commit credentials or playback
  URLs.
- Never unlock restricted content, replace audio URLs, download audio, or
  automatically substitute a searched recording.
- Run `preview` before the first `sync`. Only `sync` may write remotely.
- Do not schedule until one manual preview and one manual sync have succeeded.

## Locate or install the CLI

Prefer an existing `freefm` on `PATH`, then `$HOME/.local/bin/freefm`. If it is
missing, tell the user to install the public alpha from source:

```sh
cargo install --git https://github.com/Yuxin-Qiao/FreeFM --locked --root "$HOME/.local"
```

Do not run an installer without explicit user approval. FreeFM supports macOS
and Linux only.

## Interactive workflow

Run authentication in a terminal visible to the user so they can scan the QR
code with the official NetEase Cloud Music client:

```sh
freefm tui
freefm auth
freefm status --json
freefm preview --json
freefm sync
freefm sync --quiet
```

Use `freefm tui` for guided interactive setup. It is only a front end for the
commands below. Never use the TUI in a scheduler.

Confirm `authenticated=true` and `account_vip_type=0` before sync. Treat
`login_required`, `ordinary_account_required`, `api_incompatible`, ambiguous
playlist ownership, unknown availability, and any non-zero exit as a manual
review condition. Never infer success from an empty failed run.

## OpenClaw deterministic automation

Resolve the absolute binary path first. Create an operator-admin command job
with exact argv, no delivery, and no Agent/model payload:

```sh
openclaw automations create "0 * * * *" \
  --name "FreeFM hourly sync" \
  --command-argv '["/absolute/path/to/freefm","sync","--quiet"]' \
  --no-deliver \
  --timeout-seconds 120
```

Use `openclaw automations list` to obtain the job ID, then verify one run with
`openclaw automations run <job-id> --wait`. Command payloads execute inside the
Gateway scheduler without starting a model-backed turn. Do not replace
`--command-argv` with an agent message.

## Hermes no-agent automation

Install the bundled fixed-command helper, then create a script-only cron:

```sh
install -d -m 700 "$HOME/.hermes/scripts"
install -m 755 "{baseDir}/scripts/freefm-sync.sh" "$HOME/.hermes/scripts/freefm-sync.sh"
```

Hermes 0.17 may install only `SKILL.md` from a community GitHub/skills.sh
source. If `{baseDir}/scripts/freefm-sync.sh` is absent, ask for approval and
fetch the helper from the immutable source commit, then verify it before use:

```sh
helper=$(mktemp)
curl -fsSL \
  https://raw.githubusercontent.com/Yuxin-Qiao/FreeFM/c7bcf10dce142fd85c84f82173a307e91ea99adc/skills/freefm/scripts/freefm-sync.sh \
  -o "$helper"
test "$(shasum -a 256 "$helper" | awk '{print $1}')" = \
  "b9dd3bd85e32c8ce57ba11ef474149839ad898090495daf7336d396d37830fd1"
install -d -m 700 "$HOME/.hermes/scripts"
install -m 755 "$helper" "$HOME/.hermes/scripts/freefm-sync.sh"
rm -f "$helper"
```

Then create the job:

```sh
hermes cron create "0 * * * *" \
  --name freefm-hourly \
  --script freefm-sync.sh \
  --no-agent
```

Use `hermes cron list` to obtain the job ID and `hermes cron run <job-id>` for
one manual verification. `--no-agent` makes the script the job; empty stdout on
success is silent and consumes no LLM tokens.

## Verification

- `freefm status --json` reports an authenticated ordinary account.
- `freefm preview --json` reports decisions without creating or appending.
- A repeated `freefm sync --quiet` exits zero with empty stdout and stderr.
- The scheduler history reports success and no Agent/model invocation.
- FreeFM is absent from the process list between scheduled runs.

For user-facing installation, recovery, removal, and troubleshooting steps,
refer to https://github.com/Yuxin-Qiao/FreeFM/blob/main/README.zh-CN.md.
