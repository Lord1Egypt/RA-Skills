---
name: asale-buy-hermes
version: 0.2.7
description: "Switch Hermes between buying from the asale market and using its own subscription, and see which running sessions are still on the old config. 在「从 asale 市场买」和「用它自己的订阅」之间切换 Hermes，并查看哪些正在运行的会话还用着旧配置。"
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. Always run buy_tools before set_buy_tool for tool hermes. tool_processes is listing only — never signal those pids."}}
---

# asale-buy-hermes

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Switch Hermes between buying from the asale market and using its own subscription, and see which running sessions are still on the old config.

## Trigger Keywords

- make Hermes buy from the market
- point Hermes at asale
- asale buy hermes

## Authentication

Two separate things have to be true.

**1. The local daemon must be running, and you need its token.** `asaled` writes
`~/.asale/daemon.token` (mode 0600) on first run and requires it on every `/rpc`
call, loopback included.

```bash
asale status            # is the daemon up, and on which port
asale start             # start it if it is not
```

```bash
# Every /rpc call carries the daemon token — loopback included.
TOKEN=$(cat ~/.asale/daemon.token)
call() {
  body=$2; [ -n "$body" ] || body='{}'
  # --noproxy is not optional: a machine with HTTP_PROXY set sends even
  # 127.0.0.1 through it, and the proxy answers 502 with an empty body,
  # which reads exactly like a broken daemon.
  curl -sS --noproxy 127.0.0.1 -X POST "http://127.0.0.1:9700/rpc/$1" \
    -H 'content-type: application/json' -H "x-asale-token: $TOKEN" -d "$body"
}
```

A connection refused means the daemon is not running — say so and stop. Starting
it is the user's call.

`~/.asale/asaled.bind` holds the port the last `asale start` used; fall back to
`127.0.0.1:9700`. A bind on `0.0.0.0` is not a destination — keep the port and
dial loopback.

**2. Selling and buying need a signed-in asale account.** The daemon mints the
consumer key and registers the seller against that session. There is no CLI
login: open the app (`asale open`) and sign in there. Without it you get
`errors.session.signInToSell` / `errors.session.signInToBuy`, which is not
something to work around.

## About & Provenance

- **Source**: [github.com/asale-ai/asale](https://github.com/asale-ai/asale)
- **Homepage**: [asale.ai](https://asale.ai)
- **Install**: `curl -fsSL https://asale.ai/dl/install.sh | sh` (Windows:
  `irm https://asale.ai/dl/install.ps1 | iex`). `asale update` re-runs the same
  installer.
- **Config**: `~/.asale/` — the token, the SQLite store and the daemon's logs.
  `$ASALE_DATA_DIR` moves all of it.

This skill talks to a daemon on **your own machine**. Nothing here reaches the
asale servers directly; the daemon does that, over its own authenticated
session. The token file is the only credential this skill reads, and it never
leaves the loopback interface.

## How It Works

Buying points one locally installed AI CLI at asale's local proxy instead of at
the vendor. The switch rewrites that tool's own config file — and only that
tool's, so the switches are fully independent — and injects an asale key the
tool's config never has to hold in plain sight. Every file it touches is
snapshotted first, so switching off restores the original byte-for-byte.

Requests then go to the proxy, which decides per request: if your own
subscription window has room and the mode allows it, it goes straight upstream
and costs nothing; otherwise it is bought from the market.

Hermes is the one tool that does not keep its config in a `~/.<tool>` directory.
`HERMES_HOME` decides it when set — its installer writes that as a *user*
environment variable, so a terminal that was already open when Hermes was
installed will not have it. Where that is unset, an existing config decides
before the default does (`~/.hermes` on POSIX, `%LOCALAPPDATA%\hermes` on
Windows). `config_paths` in `buy_tools` is the authoritative answer for this
machine — read it rather than assuming.

The switch also refuses to edit a `config.yaml` it cannot parse: a file Hermes
would ignore is one where writing `base_url` changes nothing, and reporting that
as "in effect" is how a switch comes to look on for days while the agent is
still on its defaults.

## Usage

### 1. Look before switching

```bash
call buy_tools
call market_models          # the catalog, to pick model ids from
```

The `hermes` row carries `installed`, `enabled` (the switch), `in_effect` (its live
config really points at the proxy), `models` and `config_paths`.

**This tool needs a model selection.** It offers exactly the models its config
names, so an empty `models` leaves it with an asale provider and nothing to
pick. Turning the switch on without one is not a working setup — say so rather
than reporting it as done.

### 2. Turn buying on

```bash
call set_buy_tool '{"tool":"hermes","enabled":true,"models":["claude-fable-5"]}'
```

`models` omitted leaves the current selection alone; `[]` clears it. Config
rewritten: `<HERMES_HOME>/config.yaml` — four scalar keys inside its `model:` block.

### 3. Say which sessions are still on the old config

```bash
call tool_processes
```

Hermes only reads its config **at startup**, so a session that is already running
keeps the old one. `running.hermes` lists the ones still on it, by pid, with the
command line they were started with.

`scanned: false` means the machine's process table could not be read — that is
"we do not know", not "nothing is running", and must not be reported as the
latter.

### 4. Turn buying off

```bash
call set_buy_tool '{"tool":"hermes","enabled":false}'
```

The original config comes back byte-for-byte.

### If `enabled` is true but `in_effect` is false

Something else rewrote the config after asale did (another switcher, an editor,
an installer). Re-running step 2 repairs it; `open_config_path` opens the file
for the user to look at.

```bash
call open_config_path '{"path":"<one of config_paths>"}'
```

**CRITICAL INSTRUCTION FOR AGENT**:

1. Run `buy_tools` before every `set_buy_tool`. The switch and the model
   selection are independent, and writing from a stale reading silently
   overwrites what the user chose.
2. **Never list the pids from `tool_processes` as things to kill, and never kill
   one.** A CLI is attached to a terminal nothing outside it can hand a new
   process to; killing one throws away whatever it was doing. Report them and
   let the user restart what they choose.
3. After turning the switch on, tell the user it takes effect on the tool's
   **next** start. A switch reported as "done" while their current session still
   spends their own subscription is a wrong answer.
4. If buying is refused with `errors.session.signInToBuy`, stop and say so.

## Error Handling

| Code | Error Type | Example Message |
| --- | --- | --- |
| — | Daemon not running | `curl: (7) Failed to connect to 127.0.0.1 port 9700` |
| 401 | Bad or missing token | `{"key":"errors.daemon.unauthorized","message":"unauthorized (missing or bad X-Asale-Token)"}` |
| 400 | Not signed in (selling) | `{"key":"errors.session.signInToSell","message":"sign in before selling"}` |
| 400 | Not signed in (buying) | `{"key":"errors.session.signInToBuy","message":"sign in before buying"}` |
| 400 | Unknown account | `{"message":"unknown account"}` |
| 400 | Bad tool id | `{"message":"unknown tool: <id>"}` |

> **AGENT CRITICAL INSTRUCTION**:
> 1. Errors carry a `key` as well as a `message`. The `key` is a stable
>    translation id — quote it, do not paraphrase the message.
> 2. On `errors.session.signInToSell` / `errors.session.signInToBuy`, tell the
>    user to sign in from the app (`asale open`) and stop. Do not retry, and do
>    not look for another route to the same effect.
> 3. On a connection failure, report that the daemon is down and let the user
>    decide whether to start it. Do not run `asale start` unasked.

## Tips

Visit https://asale.ai for more information. The same switches have a UI in the
desktop app and in any browser — `asale open` opens it, and anything this skill
does can be checked there.
