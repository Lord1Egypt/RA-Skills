---
name: asale-sell-endpoint
version: 0.2.7
description: "Sell a custom OpenAI-compatible endpoint on the asale market: probe it, connect it as an account, and price it above what its own tokens cost. 把自定义 OpenAI 兼容端点挂到 asale 市场上卖：先探测、接入成账号，并把价格定在它自己的 token 成本之上。"
metadata: {"clawdbot":{"emoji":"📤","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. connect_custom_endpoint spends and stores the user's API key — confirm before calling. Never call remove_custom_endpoint."}}
---

# asale-sell-endpoint

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Sell a custom OpenAI-compatible endpoint on the asale market: probe it, connect it as an account, and price it above what its own tokens cost.

## Trigger Keywords

- sell an API endpoint
- resell an OpenAI-compatible API
- connect a custom endpoint to asale
- asale sell endpoint

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

A custom endpoint is sold as an account like any other, except that its
credential is an API key you supply rather than a subscription this machine was
already signed into. It is also the one seller whose tokens have a marginal
cost, which is what the price floor has to be set against.

## Usage

### 1. Connect the endpoint

```bash
call connect_custom_endpoint '{"baseUrl":"https://api.example.com/v1","apiKey":"<key>","label":"house","minRatio":10,"concurrency":5}'
```

The daemon validates the URL and probes `GET {base}/models` with the key
**before storing anything**, so a wrong host or a dead key fails here rather
than on the first buyer. `wire` is optional — left out, the probe tries each
dialect and keeps the first that answers, which is the right default because the
moment of connecting is when its operator is least sure ("OpenAI-compatible" is
written on hosts that also serve `/messages`).

The reply names what happened:

| Field | Means |
| --- | --- |
| `account_id` | The account id every later call names it by. |
| `wire` | The protocol the endpoint actually answered on. |
| `endpoint_models` | How many models it serves. |
| `sellable_models` | How many of those the market trades. |

Re-running it with the same `label` updates that account in place — endpoint,
key and terms are all rewritten and the cached model list is replaced.

### 2. Review and adjust the terms

```bash
call list_custom_endpoints
call custom_endpoints_status
call set_account_sell '{"provider":"custom","accountId":"<id>","enabled":true,"minRatio":30,"concurrency":10}'
```

### The price floor

`minRatio` is a whole percentage **of the vendor's list price** — `60` means "I
will not sell below 60% of list". `100` is list price.

- `5` is the platform's floor. The market never prices anything below it, so a
  floor of 5 never withholds anything.
- `10` is the default a fresh account starts on.

There is no "any price" setting: every account trades against a floor. Lowering
one is a real decision about money — propose it, do not just do it.

A metered endpoint is the one case where the floor is not only about profit: set
it under what your own tokens cost and every sale loses money. Work the number
out from the endpoint's own pricing before proposing it.

### 3. Refresh or remove

```bash
call refresh_custom_endpoint '{"accountId":"<id>"}'   # re-probe the model list
call set_account_sell '{"provider":"custom","accountId":"<id>","enabled":false}'
```

**CRITICAL INSTRUCTION FOR AGENT**:

1. `connect_custom_endpoint` spends the user's key on a probe request and stores
   it. Confirm the URL and the key with the user before calling it — never as an
   incidental step of something else.
2. Never call `remove_custom_endpoint`. Switching selling off is reversible;
   removing the account is not.
3. Set `minRatio` from the endpoint's real cost per token, not from the default.
   The default exists for subscriptions, where the marginal token is already
   paid for.
4. Read `sellable_models` back to the user. "Connected, 400 models, selling 12"
   is the answer they need; "connected" alone is not.

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
