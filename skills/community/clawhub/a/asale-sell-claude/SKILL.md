---
name: asale-sell-claude
version: 0.2.7
description: "Put a Claude Code / Claude subscription on the asale market: import it, set a price floor and a concurrency cap, and see which of its models are actually selling. 把 Claude Code / Claude 订阅挂到 asale 市场上：导入账号、设定价格底价与并发上限，并查看它的哪些模型真的在卖。"
metadata: {"clawdbot":{"emoji":"📤","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. Always run list_accounts before set_account_sell for provider claude, and never lower minRatio without asking."}}
---

# asale-sell-claude

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Put a Claude Code / Claude subscription on the asale market: import it, set a price floor and a concurrency cap, and see which of its models are actually selling.

## Trigger Keywords

- sell my Claude subscription
- put Claude Pro / Max on the market
- rent out Claude Code quota
- asale sell claude

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

Selling is per subscription account, not per machine. The daemon holds its own
copy of the account's credential (it never reads or writes the CLI's config on
this side), declares the account's models to the market as *lanes*, and serves
other people's requests from it — inside the limits you set: a price floor, how
many requests at once, and an optional daily token cap.

A lane leaves the market on its own whenever the market price drops under your
floor, and comes back when it recovers. Nothing has to be switched off and on
again for that.

The credential is whichever of these this machine has, in this order: the
macOS keychain entry `Claude Code-credentials`, `~/.claude/.credentials.json`,
and opencode's `~/.local/share/opencode/auth.json` (its `anthropic` OAuth entry
is the same Claude subscription reached through a different front door). Two
stores holding the same login share a token fingerprint and merge into one
account rather than showing up twice.
## Usage

### 1. Find the subscription

```bash
call discovery_scan          # what this machine holds — imports nothing
call import_cli_all          # import everything found
call list_accounts           # what is connected, and on what terms
```

A Claude subscription is found in the Claude Code keychain entry, in
`~/.claude/.credentials.json`, or in opencode's `auth.json`. All three land as
one `claude` account when they hold the same login — `sources` on the row lists
every store it was seen in.

Pick the row whose `provider` is `claude`. Its `account_id` is what every later call
names it by.

### 2. Put it on the market

```bash
call set_account_sell '{"provider":"claude","accountId":"<id>","enabled":true,"minRatio":10,"concurrency":5,"dailyLimit":0}'
```

Every field past `enabled` is optional and keeps its current value when omitted.
`dailyLimit` is in tokens; `0` means no cap.

### The price floor

`minRatio` is a whole percentage **of the vendor's list price** — `60` means "I
will not sell below 60% of list". `100` is list price.

- `5` is the platform's floor. The market never prices anything below it, so a
  floor of 5 never withholds anything.
- `10` is the default a fresh account starts on.

There is no "any price" setting: every account trades against a floor. Lowering
one is a real decision about money — propose it, do not just do it.


### 3. Check what is actually selling

```bash
call list_lanes '{"provider":"claude","accountId":"<id>"}'
```

One row per model: `status`, `paused_reason`, `requires_user`, `ratio` (what the
market pays now), `min_ratio` (your floor).

| `status` | Means |
| --- | --- |
| `selling` | On the market. |
| `withheld` | Below your floor (`paused_reason: "price"`). Returns on its own. |
| `cooldown` | A recent failure; back at `resume_at`. |
| `paused` | Needs a person. Read `paused_reason`, fix it, then `resume_lane`. |
| `exhausted` | The subscription's own quota window is spent. |
| `expired` | The credential needs re-authenticating. |

```bash
call resume_lane '{"provider":"claude","accountId":"<id>","model":"<model>"}'
```

### 4. Take it off the market

```bash
call set_account_sell '{"provider":"claude","accountId":"<id>","enabled":false}'
```

Switching off is local work and does not need a session — being unable to *stop*
selling because a session lapsed would be the worse failure.

**CRITICAL INSTRUCTION FOR AGENT**:

1. Run `list_accounts` before every `set_account_sell`. The switch, the floor and
   the concurrency are independent, and a value set from a stale reading silently
   overwrites what the user chose.
2. Never lower `minRatio` on your own initiative. Propose the number and the
   reason, and let the user answer.
3. `resume_lane` only after the thing `paused_reason` names is actually fixed.
   Clearing a pause that still applies just puts the lane back into it, and each
   round costs the seller's reputation.
4. If selling is refused with `errors.session.signInToSell`, stop and say so.

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
