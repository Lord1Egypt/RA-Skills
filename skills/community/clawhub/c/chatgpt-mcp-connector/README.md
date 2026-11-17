# chatgpt-mcp-connector

**English** · [简体中文](README.zh-CN.md)

**An onboarding skill built on top of `Waishnav/devspace`: an Agent Skill that connects a self-hosted
local MCP server to the ChatGPT web UI.**
It starts with an environment self-check and carries you all the way to "ChatGPT is actually calling
tools on my machine" — no doc-diving required along the way.

> **This repo contains none of DevSpace's source and does not modify it.** The MCP server that actually
> does the work is **`Waishnav/devspace`**; this repo is only an "install → configure → connect to
> ChatGPT" guidance layer wrapped around it — see "What this repo is" below.

> Tested on Windows 11 + Git Bash · Intel Mac · DevSpace `1.0.8` · Tailscale `1.102.4` · Node `24.15.0` ·
> the new ChatGPT UI on a Plus account.
> Version differences affect command syntax (Tailscale especially) — run `--version` before following along.
>
> **Platform support**: Windows, macOS and Linux are all supported, with no code changes to the scripts.
> - ✅ **Windows** (Windows 11 + Git Bash) and ✅ **macOS** (Intel Mac) have both been **run end to end on real
>   hardware**, stage 6 included (connector creation + OAuth authorization)
> - ⚠️ **Linux has not been verified on real hardware** — those conclusions come from reading the DevSpace
>   source; trust the actual output over the docs if they disagree
>
> Differences cluster in four places: how dependencies are installed, how the shell is resolved,
> the Tailscale service model, and path syntax.
> See [`references/cross-platform.md`](references/cross-platform.md).

---

## What this repo is (and how it relates to DevSpace)

**To be clear: this repo is not an MCP server, and it implements none of the MCP protocol.**

The MCP server that actually does the work is **`Waishnav/devspace`** (npm package
`@waishnav/devspace`, "DevSpace" below). This repo **contains none of its source and does not modify
it** — it only wraps an "install → configure → connect to ChatGPT" guidance layer around it:

| | Role | What this repo does with it |
| --- | --- | --- |
| **DevSpace** | The MCP server itself: tool implementations, path allow-list, OAuth authorization, workspaces and sessions | Only calls its CLI and config files; **not a single line of its source is changed** |
| **Tailscale** | Exposes a local port as public HTTPS | Only calls its CLI (`tailscale up` / `funnel`) |
| **ChatGPT connector** | The ChatGPT-side entry point; must be created and authorized in the web UI | The agent does it for you via browser automation |
| **This repo** | **One Agent Skill** + 2 helper scripts + a set of docs | Strings the three above into **one path that runs end to end and is hard to get wrong** |

So the accurate framing is: **DevSpace makes it *connectable*; this repo makes it *installed right,
connected, and free of landmines*.**

It is not about "how to implement MCP" but about "where you trip over while installing DevSpace
following the official docs" — the specifics are in the next section.

> If you want to understand or improve the MCP server itself, go to **`Waishnav/devspace`**.
> If you want to get it connected to ChatGPT without the landmines, use this skill.

---

## What it solves

There is no shortage of tutorials on "let ChatGPT read my local code". What actually blocks people is
never the theory — it is these:

- **One missing dependency breaks the whole pipeline**, and it usually fails at the very last step,
  after you have already invested everything;
- Tailscale login, MagicDNS and the first-time Funnel approval are **scattered across browser and admin
  console**; no script can do them, and nobody tells you where to stop;
- Get one key wrong in the DevSpace config and **the server starts but ChatGPT cannot connect** — all you
  get in the log is a vague 404;
- The official flow's `devspace init` is interactive, so it **cannot run inside automation** — you end up
  hand-editing config and stepping on landmines;
- The worst one: if the config file gets corrupted, the tooling helpfully "resets" it — the **Owner
  password is silently replaced and every connector you built is dead**.

This skill front-loads all of those traps.

---

## Features

| Capability | Detail |
| --- | --- |
| **Environment self-check + auto-fix** | 7 dependencies (Node / npm / Git / Bash / Tailscale / DevSpace / better-sqlite3) plus package-manager detection; `--install` installs what is missing |
| **Cross-platform** | Install commands, CLI locations, path syntax, shell resolution and the Tailscale service model are all handled for Windows / macOS / Linux; the scripts branch by platform, **no code changes needed** |
| **Fully automatic config writing** | Does not rely on the interactive `devspace init`; writes `config.json` from arguments and only touches keys you explicitly pass |
| **Fault tolerance & rollback** | Refuses to write when the config is corrupt and quarantines it as `.corrupt-*`, auto-backs up to `.bak`, atomic replace, timeouts, one-command `rollback` |
| **🤖 Stage 6 browser automation** | The agent drives the browser with `browser-harness` to create the connector and complete OAuth itself — **you never fill in the form**; the ownerToken is read in place and never echoed |
| **🙋 Human-in-the-loop reminders** | Explicitly marks the 7 steps that genuinely cannot be delegated (UAC elevation, browser login, Funnel approval, allowing Chrome remote debugging once, …) and flags them proactively when it detects an unlogged or unconfigured state |
| **Troubleshooting** | ~20 rows of common errors, including a "debunked false root cause" section so you do not waste time down the wrong path |
| **Security boundaries** | Explains that `allowedRoots` is *not* a sandbox, plus the symlink bypass and the `DEVSPACE_ALLOWED_HOSTS=*` risk |

---

## Prerequisites

| Item | Requirement | Notes |
| --- | --- | --- |
| OS | Windows / macOS / Linux | All three work; **Windows 11 + Git Bash and Intel Mac have both been run end to end**, Linux is unverified |
| Node.js | `>=20.12 <27` | The package README says `>=22.19 <27`; the CLI itself is more permissive |
| Bash | Windows: **mandatory** — Git Bash ★ / MSYS2 / Cygwin / WSL / PortableGit<br>macOS / Linux: `/bin/bash` (ships by default) | Windows often has several; picking the wrong one makes DevSpace behave oddly. **On Windows a missing bash is fatal** (no fallback); macOS/Linux degrade to `/bin/sh` |
| Git | Any recent version | — |
| Tailscale | `1.102.4` verified | Must be logged in with MagicDNS enabled; on Linux the CLI needs root by default — use `--operator` |
| ChatGPT | Web UI + paid account with **developer mode** enabled | Required for connectors; the agent flips the developer-mode switch itself |
| browser-harness | Optional, `0.1.8+` | Lets the agent complete stage 6 (create connector + OAuth) unattended. Without it, stage 6 falls back to manual work with an identical outcome |

> Platform quick reference (install commands / CLI locations / path syntax / common traps):
> [`references/cross-platform.md`](references/cross-platform.md).

All of the above can be checked and filled in by `env-check.mjs --install` (installs may raise a UAC prompt).

---

## Install the skill

Copy the block below **verbatim to WorkBuddy / your agent** and it will install and validate itself:

```text
Please install the chatgpt-mcp-connector skill locally for me:

Repository: https://github.com/hawklithm/chatgpt-mcp-connector
Clone it into your skill directory —
  macOS / Linux : ~/.workbuddy/skills/chatgpt-mcp-connector
  Windows       : %USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector
(On Windows `~` is NOT expanded by cmd or PowerShell — use %USERPROFILE%. Quote the path if it
contains spaces.)

  git clone https://github.com/hawklithm/chatgpt-mcp-connector.git "<target-dir>"

Then validate it with skill-creator's quick_validate.py and confirm it prints "Skill is valid!".
Finally read me the description from SKILL.md so I can confirm it will be recognized.
```

Or do it yourself — two commands (pick the line for your platform):

```bash
# 1. Clone into the user-level skill directory (available across all projects)
git clone https://github.com/hawklithm/chatgpt-mcp-connector.git ~/.workbuddy/skills/chatgpt-mcp-connector
#    Windows (cmd / PowerShell): `~` is not expanded — use %USERPROFILE%
git clone https://github.com/hawklithm/chatgpt-mcp-connector.git "%USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector"

# 2. Validate
python <skill-creator>/scripts/quick_validate.py ~/.workbuddy/skills/chatgpt-mcp-connector
```

**Where should it live?**

| Location | Scope | When to use |
| --- | --- | --- |
| `~/.workbuddy/skills/` (Windows: `%USERPROFILE%\.workbuddy\skills\`) | User-level, **all projects** | Recommended — install once, works everywhere |
| `<project>/.workbuddy/skills/` | Project-level, shared with the repo | Team work — anyone who clones the project gets it |

> If your harness uses a different skill-directory convention, installing there works too — just swap the
> paths in the prompt below to match. On Windows, quote any path that contains spaces.

No restart needed. The next time you mention "connect my local MCP to ChatGPT", it triggers.

---

## One-shot prompt: let an agent install **and** configure everything

The block above only *installs*. The one below **installs and then runs the whole pipeline**: paste it
into any harness (WorkBuddy / Claude Code / Codex / Cursor / …) and it will work through the SKILL.md
procedure — **including stage 6, creating the connector and completing OAuth**, which the agent does
itself by driving the browser with `browser-harness`, so you never fill in the form. It pauses only
where a human is genuinely required.

It can drive an arbitrary harness because the procedure lives in **files** (`SKILL.md` + `references/`).
The prompt only routes the harness there and gives it a pass criterion and a pause point per stage — it
depends on no harness-specific capability.

```text
Install and run the chatgpt-mcp-connector skill, end to end.

Goal: get a local MCP server (DevSpace) running on this machine so the ChatGPT web UI can reach it
      over public HTTPS, and can read and write files under a directory I choose.

== Setup ==

0) Fix two path variables first. Everywhere below, substitute the real values for <SKILL_DIR> and
   <PROJECT_DIR>:

   <SKILL_DIR> = where this skill is installed
       macOS / Linux : ~/.workbuddy/skills/chatgpt-mcp-connector
       Windows       : %USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector
   <PROJECT_DIR> = the directory ChatGPT may access (Step 3 asks me)

   ⚠️ Windows specifics:
     - `~` is NOT expanded by cmd or PowerShell — use %USERPROFILE% there. It does work in Git Bash.
     - Quote any path containing spaces (e.g. "C:\Program Files\Git\bin"), otherwise it gets
       truncated at the space.
     - `&&` works in cmd and PowerShell 7+; PowerShell 5.1 does not support it — run the two
       commands on separate lines instead.

1) Install the skill (idempotent — skip if already present). Repository:
       https://github.com/hawklithm/chatgpt-mcp-connector
   Clone it into <SKILL_DIR>:
       git clone https://github.com/hawklithm/chatgpt-mcp-connector.git "<SKILL_DIR>"
   If git itself is not on PATH, install Git for Windows first per
   <SKILL_DIR>/references/env-setup.md.
   If your harness uses a different skill-directory convention, install there and substitute that
   path for <SKILL_DIR> everywhere.

2) Read <SKILL_DIR>/SKILL.md in full.
   It is the authoritative procedure — follow it, not your own assumptions.
   Then read <SKILL_DIR>/references/cross-platform.md and apply only the section for this OS.

3) Ask me which directory ChatGPT may access; call it <PROJECT_DIR>.

== Execution ==

Work through the stages in order. After each stage, report what you ran, the evidence, and what comes
next — then continue. Whenever a step is marked 🙋 in SKILL.md, STOP AND ASK ME: those genuinely
cannot be done for me (UAC elevation, browser login, Funnel approval, the one-time Chrome
remote-debugging permission). **Stage 6 is not one of them** — create the connector and complete
OAuth yourself with browser-harness; do not hand that back to me.

Stage 0  Environment self-check (read-only first)
    node "<SKILL_DIR>/scripts/env-check.mjs"
    Show me the missing items and the exact install commands you intend to run.
    WAIT for me to approve, then re-run with --install.
    Pass: output ends with "✅ 全部就绪" and exit code 0.
    Note: right after installing, PATH is not refreshed, so it can still exit 1 — open a new terminal
    and re-run rather than reporting a false green.
    ⚠️ On Windows there is one extra hard criterion: **Bash must be [ok]**.
       If it shows [unavailable] with the path C:\Windows\System32\bash.exe, DevSpace has picked the
       WSL launcher instead of a real shell — and then EVERY command fails, `echo` included.
       Fix it per <SKILL_DIR>/references/troubleshooting.md → "Windows: bash shadowed by the WSL
       launcher" before going further, and restart devspace serve afterwards — the fix only takes
       effect on restart.

Stage 1  Install DevSpace
    npm install -g @waishnav/devspace
    Pass: devspace -v prints a version.

Stage 2  Install and log in to Tailscale
    Install it if missing (use the command for this OS from <SKILL_DIR>/references/cross-platform.md),
    then run tailscale up.
    🙋 PAUSE: it prints a login link; I must open it in a browser and approve the device joining my
    tailnet.
    Pass: tailscale status shows Self with an address starting 100.

Stage 3  Open the public tunnel
    tailscale funnel --bg 7676
    NEVER add --set-path=/mcp — it strips the mount path, turning public /mcp into / and returning 404,
    and the OAuth discovery routes live outside /mcp anyway. Proxy the whole port.
    🙋 If this is the first time Funnel is enabled, Tailscale prints an approval link — I have to click
    it in a browser.
    Pass: tailscale funnel status shows "(Funnel on)" plus a line reading
          "proxy http://127.0.0.1:7676".

Stage 4  Write the DevSpace config
    Show me what would change first (keep it on ONE line — backslash continuations are bash-only and
    break in Windows shells):
      node "<SKILL_DIR>/scripts/devspace-bootstrap.mjs" apply --roots "<PROJECT_DIR>" --dry-run
    Once I confirm, re-run without --dry-run to actually write it.
    Pass: the serve log's "allowed roots:" line matches what I asked for.

Stage 5  Start the server
    Change into <PROJECT_DIR> first, then run devspace serve   # must stay running; if it stops,
                                                              # ChatGPT disconnects
    ⚠️ Windows: if `where git` shows Git for Windows is NOT under %ProgramFiles%\Git (very common —
       it may live on another drive), starting directly makes DevSpace pick the WSL launcher again and
       the shell tool dies. In that case prepend Git's bin to PATH first — one line in cmd:
         set "PATH=<Git install root>\bin;%PATH%" && devspace serve
       Derive <Git install root> from `where git` (drop the trailing \cmd\git.exe), or simply copy the
       line env-check already filled in for you under "fix ①".
    Pass: http://127.0.0.1:7676/healthz returns 200, and https://<funnel-domain>/healthz returns 200.
    Note: https://<funnel-domain>/mcp returning 401 is CORRECT — that is the OAuth entry point, not a
    failure.
    🙋 Keep it running in the background and tell me how to stop it.

Stage 6  Create the connector and complete OAuth — using browser-harness, yourself
    ⚠️ You drive the browser here. This is NOT "list the values and let me fill them in".
    Do each step, then report. Re-read page state after every action to confirm it took effect.

    A) Run browser-harness --doctor
       Confirm "chrome running" and that "active browser connections" is not 0.
       ("Browser Use cloud auth" showing FAIL is expected — local Chrome does not need the cloud.)
       If connections is 0, ONLY THEN stop and ask me: I will tick "Allow remote debugging for this
       browser instance" and click Allow in Chrome. This is a ONE-TIME action.
       ⚠️ Do not retry in a loop — Chrome pops a fresh dialog for every new connection, so retrying
       just spams me.

    B) Login-wall check: new_tab("https://chatgpt.com/") + wait_for_load(), then read page_info().
       If you land on a login page, stop and tell me. NEVER fill in passwords, one-time codes or MFA.

    C) Enable developer mode (one-time): Settings -> Account security and login -> Developer mode.
       Read the toggle back afterwards to confirm.

    D) Create the connector. Use the deep link straight into the new-plugin dialog — do not hunt for
       the button on the list page:
         https://chatgpt.com/plugins#settings/Connectors?create-connector=true&redirectAfter=%2Fplugins
       Fill: name DevSpace / connection type "Server URL" / URL = https://<funnel-domain>/mcp
             / auth OAUTH / tick the acknowledgement checkbox (without it "Create" stays disabled).
       🔎 BEFORE submitting, self-check: does the "Advanced OAuth settings" button flip from the
          disabled "Enter a valid MCP server URL to view discovered OAuth settings" to an enabled
          "View discovered OAuth settings"? If it did not flip, OAuth discovery FAILED (URL missing
          /mcp, tunnel down, server not running) — do NOT submit.
       After clicking "Create", wait ≥6 seconds before judging: submission is async and the dialog
       closes a moment later, so judging too early looks like a failure.

    E) The page redirects to https://<funnel-domain>/authorize?... (note: the host changes from
       chatgpt.com to your funnel domain). Read ownerToken from ~/.devspace/auth.json
       (Windows: %USERPROFILE%\.devspace\auth.json) and fill it into the password field in place,
       then click Authorize DevSpace.
       🔐 Never print, echo or log it; never pass it as a command-line argument (that leaks it into
          shell history and the process list); when reading it back for verification, return only the
          length (43).

    Pass: the DevSpace server log shows userAgent: openai-mcp/1.0.0 with a 200 response, plus an
          mcp_session_created line.
    🙋 Last step is mine: open a new conversation and attach DevSpace from the tools menu — there is
       no public API for that.

    Two general traps: every browser-harness call resets the current tab, so re-select the tab at the
    top of each script; and the authorize flow navigates the tab from chatgpt.com to the funnel
    domain, so never hard-code chatgpt.com in your tab matcher.
    Always click via coordinates (click_at_xy), never JS .click() — JS clicks routinely fail on
    ChatGPT's React buttons.

== Rules ==

- Do not run any installer without my explicit approval for that specific command.
- Stage 6 MUST be done by you driving the browser with browser-harness. Do not hand me a list of
  values to type. Stop for me only in two cases: (1) a login wall (password / code / MFA / account
  choice), (2) the one-time Chrome remote-debugging permission.
- The Owner password never enters the chat or any log: read it from ~/.devspace/auth.json and fill
  it in place. Do not print it, echo it, or pass it as a CLI argument. Only on the manual fallback
  path (no browser-harness available) do you just tell me where the file is.
- Never use tailscale funnel --set-path; always proxy the whole port.
- If any step fails, read <SKILL_DIR>/references/troubleshooting.md before improvising. For browser
  steps, run `browser-harness --doctor` first.
- If your environment contradicts an assumption in the docs (version, path, shell), say so instead of
  guessing.
- Decide whether a dependency is usable by running its command and reading the output
  (`--version` / `where` / `which`). Do not conclude anything from "the file exists" — "the file is
  there but will not run" is a real and common case.
- After any browser action, read the state back (`js(...)` or `page_info()`). Never assume
  "I clicked it" means "it took effect".

Start with Stage 0 now.
```

**What that prompt guarantees** — i.e. the mistakes it blocks for you:

| Stage | The easy mistake when nobody is watching | Constraint in the prompt |
| --- | --- | --- |
| all | Giving only the repo *path* and no URL, so the agent cannot tell where to download from; hard-coding POSIX `~/...` paths that simply do not resolve on Windows | States `https://github.com/hawklithm/chatgpt-mcp-connector` and the full `git clone` command up front; defines `<SKILL_DIR>` with both the POSIX and the Windows `%USERPROFILE%` form |
| all | Using bash-only backslash line continuations or `~` — a Windows shell errors out | Commands are written as single lines with quoted paths; notes that `~` is not expanded and that PowerShell 5.1 lacks `&&` |
| 0 | Running `--install` without asking, or reading "PATH not refreshed yet" as an install failure | Read-only first → list commands → wait for approval; exit-code semantics spelled out |
| 0 | On Windows, ignoring Bash showing `[unavailable]` (the WSL launcher has shadowed Git Bash) and only discovering at Stage 5 that every command fails | Makes "Bash must be `[ok]`" a hard Stage-0 criterion and says serve must be restarted after fixing it |
| 2 | Re-running `tailscale up` in a loop while it is actually waiting on your browser | Explicitly designated a 🙋 pause point |
| 3 | Reflexively adding `--set-path=/mcp` → public `/mcp` 404s | Hard prohibition, with the reason |
| 4 | Writing straight to disk, or invoking the interactive `devspace init` and hanging | `--dry-run` diff is mandatory first |
| 5 | Misreading the public `/mcp` 401 as a failure and "fixing" the server | States plainly that 401 is correct |
| 5 | On Windows, running `devspace serve` directly when Git is not under `%ProgramFiles%\Git` — the shell tool is then dead | Gives the exact one-liner that prepends Git's `bin` to PATH before starting |
| 6 | Creating the connector under Settings → `Something went wrong` | Points at the `plugins` page and gives the deep link |
| 6 | Treating this stage as "human-only" and handing the user a list of values to type (when the agent could just do it) | Mandates driving the browser with `browser-harness`; stops only for a login wall or the one-time remote-debugging permission |
| 6 | Clicking "Create" and only then discovering OAuth discovery failed → `Something went wrong` again | Requires checking that the "Advanced OAuth settings" button flipped to enabled before submitting |
| 6 | Judging the result immediately after clicking "Create" (submission is async and the dialog closes a moment later) | Requires waiting ≥6 seconds before judging |
| 6 | Each `browser-harness` call resets the tab → the agent acts on the wrong tab | Says to re-select the tab per script, and not to hard-code `chatgpt.com` in the matcher (the authorize flow changes host) |
| 6 | Using JS `.click()` on React buttons → nothing happens | Requires coordinate clicks via `click_at_xy` |
| 6 | Retrying the connection in a loop → Chrome keeps popping permission dialogs at the user | Says explicitly: once only, do not retry in a loop |
| 6b | Getting the user to paste the Owner password into the chat | The agent reads it from `auth.json` in place; no printing, no CLI argument, verification returns only the length |

---

## Quick start (driving it manually)

Once installed, a single sentence to your agent is enough:

```text
Connect my local MCP to ChatGPT, using D:\projects\my-app as the accessible directory — and create
the connector and finish the OAuth authorization for me too.
```

It then walks the flow below, stopping to remind you wherever your own action is required:

```mermaid
flowchart LR
    S0["Stage 0<br/>Env self-check<br/>+ install deps"] --> S1["Stage 1<br/>Install DevSpace"]
    S1 --> S2["Stage 2<br/>Install + log in<br/>Tailscale"]
    S2 --> S3["Stage 3<br/>Open Funnel<br/>public tunnel"]
    S3 --> S4["Stage 4<br/>Write DevSpace<br/>config"]
    S4 --> S5["Stage 5<br/>Start<br/>devspace serve"]
    S5 --> S6["Stage 6 🤖<br/>browser-harness drives<br/>connector + OAuth"]

    S2 -.->|🙋 browser login| U1((you))
    S3 -.->|🙋 approve Funnel| U1
    S6 -.->|🙋 allow Chrome remote debugging (once)| U1
    S6 -.->|🙋 login wall / attach the tool| U1
```

> Stage 6 is **automated**: the agent operates the browser, fills the form and enters the Owner
> password itself. You no longer create the connector by hand. Only the two 🙋 edges above interrupt you.

### Pass criteria per stage

| Stage | Key command | Pass criterion |
| --- | --- | --- |
| 0 Env | `node scripts/env-check.mjs` | Prints "✅ 全部就绪" |
| 1 DevSpace | `npm i -g @waishnav/devspace` | `devspace -v` → `1.0.8` |
| 2 Tailscale | `tailscale up` → `tailscale status` | `Self` present, address starts with `100.` |
| 3 Tunnel | `tailscale funnel --bg 7676` | `funnel status` shows `(Funnel on)` |
| 4 Config | `devspace-bootstrap.mjs apply --roots ...` | Serve log's `allowed roots:` is as expected |
| 5 Serve | `devspace serve` | `/healthz` returns 200 locally **and** publicly |
| 6 Connector | 🤖 `browser-harness` drives the browser (agent-run) | Log shows `openai-mcp/1.0.0` + `200` |

> One easy misread at stage 5: a public `/mcp` returning **401 is correct** — that is the OAuth entry
> point, not a fault.

---

## Repository layout

```
chatgpt-mcp-connector/
├── SKILL.md                        # Main file: triggers, 0→1 flow, iron rules, reference index
├── references/                     # Per-stage detail (loaded on demand, kept out of the main context)
│   ├── cross-platform.md           # Win/mac/Linux: install commands, paths, shell, Tailscale, per-OS traps
│   ├── env-setup.md                # Stages 0–1: dependency list, per-OS install, env pitfalls
│   ├── tailscale-funnel.md         # Stages 2–3: login, Funnel prerequisites & syntax, domain derivation
│   ├── devspace-config.md          # Stages 4–5: config files, env var table, OAuth persistence
│   ├── chatgpt-connector.md        # Stage 6: browser-harness automation, manual fallback
│   └── troubleshooting.md          # Fault-tolerance design, error lookup, debunked root causes
├── scripts/
│   ├── env-check.mjs               # Environment self-check + auto-install of what is missing
│   └── devspace-bootstrap.mjs      # Config write / doctor / rollback
├── README.md                       # English (this file)
├── README.zh-CN.md                 # 简体中文
├── LICENSE
└── .gitignore
```

---

## Bundled scripts

Resolve the scripts directory once for your platform, then use `$SK` throughout:

```bash
# macOS / Linux (bash, zsh)
SK=~/.workbuddy/skills/chatgpt-mcp-connector/scripts
```

```bat
:: Windows (cmd.exe)
set "SK=%USERPROFILE%\.workbuddy\skills\chatgpt-mcp-connector\scripts"
```

```powershell
# Windows (PowerShell)
$SK = "$env:USERPROFILE\.workbuddy\skills\chatgpt-mcp-connector\scripts"
```

> **On Windows, substitute `$SK`** in the examples below: cmd wants `%SK%\env-check.mjs`,
> PowerShell wants `"$SK\env-check.mjs"`. Note that `~` is **not** expanded by cmd or PowerShell,
> which is why `%USERPROFILE%` / `$env:USERPROFILE` is used above. Quote any path containing spaces.

### `env-check.mjs` — environment self-check + auto-install

```bash
node $SK/env-check.mjs                             # read-only: results + install commands for gaps
node $SK/env-check.mjs --json                      # machine-readable (for agents)
node $SK/env-check.mjs --install                   # actually run the installs
node $SK/env-check.mjs --install --only node,git   # install only the named items
```

Exit codes: `0` all ready / `1` something missing / `2` the script itself failed.

- Node is validated against `>=20.12 <27`.
- Whether a dependency is installed is decided by **running commands** (`where` / `which` / `--version`),
  never by guessing install directories. Bash candidates come from `where bash.exe` plus a derivation
  from `where git`, so Git on any drive is found — and the scripts contain no hard-coded drive letters.
- Bash: **all candidates are listed with a recommended one** (★ Git Bash > MSYS2 > Cygwin > WSL > PortableGit).
- Tailscale login state is read from `BackendState` in `status --json`, with per-OS guidance when unlogged.
- Every check is independently wrapped; external commands run with timeouts (15s probe / 10min install).
- With `--install`, a single failure **does not abort the batch**; a summary reports
  auto-succeeded / auto-failed / needs-manual / skipped.
- If the package manager is not present, it **skips with an explanation** rather than throwing ENOENT.
- Exit codes reflect the state **at check time** — right after installing, an unrefreshed PATH still
  returns `1` rather than a false green.

> **⚠️ Consent first.** Nothing is installed by default; only an explicit `--install` executes commands.

### `devspace-bootstrap.mjs` — write the DevSpace config

```bash
node $SK/devspace-bootstrap.mjs check        # read-only: Node / tailscale / tunnel / domain / current config
node $SK/devspace-bootstrap.mjs apply --roots "D:\projects\my-app" [--port 7676] [--host 127.0.0.1] [--public-base-url https://x.ts.net] [--subagents codex,claude] [--dry-run] [--force]
node $SK/devspace-bootstrap.mjs rollback [--config|--auth]   # restore from .bak
```

That `apply` line is deliberately single-line: backslash continuation (`\`) is bash-only syntax —
cmd and PowerShell swallow the `\` as a literal character.
On macOS / Linux pass forward-slash roots instead (e.g. `/home/you/projects/my-app`).

**Behavioural guarantees**

- `check` never writes to disk.
- `apply` only touches keys you **explicitly pass**, **never overwrites an existing `ownerToken`**, and
  leaves the file alone when nothing changed (idempotent).
- `publicBaseUrl` is derived from Tailscale automatically — no manual entry.
- It **never calls** `devspace init` (that one is interactive and re-asks everything).

**Fault-tolerance guarantees**

- A corrupt config means **it refuses to write**, quarantining the original as `.corrupt-<timestamp>`
  instead of silently blanking it.
- Before writing, the existing file is backed up to `.bak` and replaced **atomically**
  (temp file + rename).
- All validation happens before any write; on failure it exits leaving **no half-written state**.

---

## Three iron rules

1. **Never `tailscale funnel --set-path=/mcp`**
   The mount path gets stripped, so public `/mcp` becomes `/` → 404; and DevSpace's OAuth routes live
   outside `/mcp` anyway. Proxy the entire origin.

2. **Create the connector on the `chatgpt.com/plugins` page**
   Settings is only for enabling developer mode. The two forms have identical fields, and taking the
   wrong one always yields `Something went wrong`.

3. **Enter the Owner password only in the browser authorization page, and never in chat or logs**
   On the manual path, never have the user paste it into chat. On the automated path the agent reads
   it from `auth.json` in place and fills the form directly — no printing, no echo, no CLI argument.

---

## Security boundaries (please read)

- `allowedRoots` is **not an OS sandbox** — shell commands run with **your local user privileges**.
- Do not put repositories containing secrets, customer data or production config behind it;
  **verify the boundary with a read-only prompt first**.
- Keep the allow-list scoped to the project you actually need; do not take the lazy route and allow a
  whole disk (the script warns on drive-root and home-directory entries).
- Watch out for symlinks inside the allow-list: known issue #45 — path comparison is string-level and
  does not resolve symlink targets.
- `DEVSPACE_ALLOWED_HOSTS=*` disables Host validation — **local debugging only**.
- Close the public entry point when you are done: `tailscale funnel reset`.
- `ownerToken` is a 43-character **plaintext** value in `auth.json` under the DevSpace config directory.
  Treat it like an account password and mind the file permissions.

---

## FAQ

| Symptom | Where to look |
| --- | --- |
| `MCP server ... does not implement OAuth` | `references/troubleshooting.md` |
| ChatGPT reports `Something went wrong` | First check that you created the connector on the `plugins` page (iron rule 2) |
| `path is outside allowed roots` | `references/devspace-config.md` |
| Tunnel domain changed, connector cannot connect | `references/tailscale-funnel.md` — recreate or Refresh the connector |
| Config corrupted / want to revert | `references/troubleshooting.md` — use `rollback` |
| Funnel unavailable | The fallback path in `references/troubleshooting.md` (cloudflared) |
| Installed, but "command not found" | `references/cross-platform.md` (PATH not refreshed / Homebrew not on PATH / npm global bin dir not on PATH) |
| `tailscale` permission errors on Linux | `sudo tailscale up --operator=$USER`, see `references/cross-platform.md` |
| Path is in the allow-list yet rejected | (1) Linux is case-sensitive: `~/Projects` and `~/projects` are different directories; (2) the directory is a **junction / symlink** whose real target is outside the root (the checker does not resolve links) |
| The error contains a WSL path like `/mnt/f/...` | You passed a WSL-style path. DevSpace is a Windows process, so `/mnt/f/x` resolves to `C:\mnt\f\x` and is always rejected. Use the native form `F:\x` — and read paths from PowerShell/cmd, not from inside WSL |
| `download_artifact` tool missing in ChatGPT | Expected — that tool is only registered on Linux |

---

## External references

- **DevSpace (the upstream core dependency)**: the MCP server itself — repo `Waishnav/devspace`,
  npm package `@waishnav/devspace`
- OpenAI connector docs: `developers.openai.com/plugins/deploy/connect-chatgpt`
- Tailscale Funnel: `tailscale.com/kb/1247/funnel-serve-use-cases`

---

## License

[MIT](LICENSE) © 2026 hawklithm
