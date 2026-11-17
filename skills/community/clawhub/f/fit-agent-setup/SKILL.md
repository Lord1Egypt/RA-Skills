---
name: fit-agent-setup
description: "Install and onboard FitAgent for Intervals.icu fitness coaching: install the CLI, initialise a workspace, configure credentials securely, fetch initial data, and verify readiness. Use when the user wants to set up, install, connect, or troubleshoot FitAgent."
---

# FitAgent setup

Set up [FitAgent](https://github.com/jogvan-k/fit-agent), a local CLI that
synchronises a coaching workspace with [Intervals.icu](https://intervals.icu).
The CLI never calls an LLM; it retrieves and renders data so a coaching agent
can reason from it.

## 1. Preflight

Run:

```sh
fit-agent --version
```

If a version is returned, skip to **2. Initialise the workspace**. Otherwise,
identify the operating system and ask whether Homebrew or Go is preferred only
when both are available and the user has no preference.

## 2. Install the CLI

### Homebrew (recommended on macOS or Linux)

```sh
brew tap jogvan-k/tap
brew install fit-agent
```

### Go 1.25 or later

```sh
go install github.com/jogvan-k/fit-agent/cmd/fit-agent@latest
```

Ensure `$(go env GOPATH)/bin` is on `PATH` before continuing.

After either method, verify exactly which binary will run:

```sh
command -v fit-agent
fit-agent --version
```

Do not install another copy if a usable FitAgent binary is already present.

## 3. Initialise in the intended workspace

Work in the OpenClaw workspace that will hold the athlete's coaching files, then
run:

```sh
fit-agent init
```

Let the athlete enter their Intervals.icu API key into FitAgent's interactive
prompt. Never request the key in chat, store it in a markdown note, echo it,
or put it in a shell command.

The initialised workspace should contain a `fit-agent/` directory, including
`ATHLETE-PROFILE.md`, `TRAINING-PLAN.md`, and the generated data directories.

## 4. First data refresh

Fetch enough history for useful coaching context:

```sh
fit-agent fetch --since 90d
```

Report only the high-level result. Do not paste raw activity, wellness, or API
payloads into chat.

## 5. Verify readiness

Confirm:

```sh
fit-agent --version
find fit-agent -maxdepth 1 -type f -name 'ATHLETE-PROFILE.md' -o -name 'TRAINING-PLAN.md'
find fit-agent -maxdepth 1 -type d \( -name activities -o -name wellness -o -name planned-workouts \)
```

If the fetch failed, preserve the error message, diagnose the configured
Intervals.icu credentials/profile and network access, and retry only after the
cause is clear. Do not recreate the workspace or overwrite its athlete-owned
files as a generic fix.

## 6. Hand-off

Once the workspace is healthy, explain that the athlete can now ask their agent
to:

- review recent workload and wellness;
- build or revise a training plan;
- create structured workouts; or
- check whether today's session should be adjusted.

For a remote calendar update, the coaching flow must always preview first:

```sh
fit-agent sync-workouts --from YYYY-MM-DD --to YYYY-MM-DD --dry-run
```

Only perform the non-dry-run sync after the athlete approves the reported
change, unless they have recorded an explicit standing preference to push after
a successful preview.

## Safety boundaries

- Treat `fit-agent/activities/`, `fit-agent/wellness/`, and
  `fit-agent/.cache/` as machine-owned; inspect but do not edit them.
- Keep API keys and raw personal activity data out of chats, commits, logs, and
  skills.
- Do not diagnose injuries or acute symptoms; recommend appropriate clinical
  assessment where indicated.
