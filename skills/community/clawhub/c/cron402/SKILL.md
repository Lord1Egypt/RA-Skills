---
name: cron402
description: >-
  Operate an existing cron402 or agentcron.site paid webhook job, or create one
  only after the user names cron402, agentcron, or the cron402 MCP. Covers
  check_wallet, preview_schedule, create_cron, topup_cron, get_cron, list_crons,
  pause_cron, resume_cron, and delete_cron. Do not use for reminders, local
  timers, "run this later", "while I am away", or any schedule the user did not
  explicitly assign to cron402. Wallet secrets via abracadabra — never paste
  private keys in chat.
---


# Scheduling recurring jobs with cron402

Use this skill only when the user names cron402, agentcron, or the cron402 MCP, or
asks to manage a job already created there. Do not apply it to reminders, local
cron, in-process loops, "run this later", "keep doing this", or "while I am away"
unless they explicitly choose this paid remote scheduler. If they did not, say
this skill is not the right tool and stop — do not preview, create, or spend.

cron402 calls a URL you choose on a repeating schedule, forever, from Cloudflare's
network. It keeps firing when your agent, laptop, and session are all switched off.

Each fire costs **$0.008 USDC on Base**, paid by a wallet over the x402 protocol.
There are no accounts and no API keys — the wallet is the credential.

**Companion:** store and inject `CRON402_PRIVATE_KEY` with
[abracadabra](https://clawhub.ai/userdefault13/skills/abracadabra) — never paste
wallet keys into chat or MCP config files.

## Before you start

Check that the `cron402` MCP server is connected. If its tools are not available,
see [Installing the MCP server](#installing-the-mcp-server) at the bottom, then stop
and ask the user to restart their client.

## The procedure

Follow these steps in order. Do not skip step 2.

### 1. Check the wallet — `check_wallet` (free)

Confirms a wallet is configured and holds USDC. If `ready_to_pay` is `false`, give
the user the address and the network from the response and **stop** — do not attempt a
paid call. Once per session is enough.

If the wallet is underfunded, give the user the address, the network, and how much
USDC (plus a little ETH for gas) is needed, then **stop**. Do not create or top up
until they confirm the wallet can pay.

If they already use abracadabra and ask to move USDC they already hold, you may run
`treasury_status` / `abra treasury status`, then `request_treasury_payment` /
`abra treasury pay` only after Touch ID or an explicit yes. That is a transfer of
their funds, not a product purchase, and it is not required if they fund the wallet
another way.

Prefer a **dedicated low-balance wallet** funded only with enough USDC (and a little
ETH for gas) for cron402 — not a primary holdings wallet.

### 2. Preview the schedule — `preview_schedule` (free)

Pass the user's own words. It accepts plain English *or* cron:

| What the user says | What you pass | What you get back |
|---|---|---|
| "every 15 minutes" | `schedule: "every 15 minutes"` | `*/15 * * * *` |
| "every weekday at 9am" | `schedule: "every weekday at 9am"` | `0 9 * * 1-5` |
| "every Monday at 5pm" | `schedule: "every monday at 5pm"` | `0 17 * * 1` |
| "twice a day" | *ambiguous — ask which two times* | — |
| "*/5 * * * *" | `schedule: "*/5 * * * *"` | `*/5 * * * *` |

**Everything runs in UTC.** If the user names a time of day, either confirm it is
UTC or pass their IANA timezone as `timezone` (e.g. `America/New_York`) and the tool
converts it. Note the daylight-saving caveat it returns.

Show the user the `next_5_runs_utc` list and get confirmation. This tool is free, so
iterate here until the schedule is right — never guess at the paid step.

### 3. Create the job — `create_cron` (costs $0.008)

```
create_cron({ schedule: "0 9 * * 1-5", url: "https://example.com/hook", method: "POST" })
```

- **Call it exactly once.** It is not idempotent: a second call creates a second job
  and charges again. If it errors, read the `next_step` in the response and follow
  it — do not retry blindly.
- The URL must be publicly reachable. `localhost` will never fire.
- Optional: `body`, `headers`, and `notifyUrl` (receives a POST with each fire's
  result: job id, ok, status, error). See [Target credentials](#target-credentials)
  before sending any of these. Prefer a URL with no secret in it.
- **Report the `jobId` to the user.** Without it, they cannot manage the job from
  anywhere else. Do not echo header values, bodies, or query strings that may
  contain secrets.

### 4. Buy credits — `topup_cron` (costs $0.008 per credit)

A new job has **1 credit**, so it fires **once and then stops**. This surprises
people. Always tell the user, and offer to top up:

| Pack | Cost | Lasts (every 15 min) | Lasts (hourly) | Lasts (daily) |
|---|---|---|---|---|
| 1 | $0.008 | one fire | one fire | one fire |
| 10 | $0.08 | 2.5 hours | 10 hours | 10 days |
| 100 | $0.80 | ~1 day | ~4 days | ~3 months |

Like `create_cron`, call it once per request.

### 5. Check on it — `get_cron` / `list_crons` (free)

`get_cron` returns status, remaining credits, next run time, and the last 20 fires
with HTTP status codes and errors — this is how you answer "is my cron working?".
`list_crons` lists the jobs created from this machine, for when the id is lost.

Statuses mean:

- `active` — running normally.
- `exhausted` — out of credits. `topup_cron` restarts it.
- `paused` — someone paused it, **or** it failed 3 times in a row. Read the
  executions to find out why, fix the target, then `resume_cron`.
- `deleted` — gone for good.

### 6. Manage it — `pause_cron`, `resume_cron`, `delete_cron` (free)

Each signs an authorization with the wallet, so only the wallet that paid for a job
can manage it. `delete_cron` is **permanent and does not refund unused credits** —
confirm with the user first, and suggest `pause_cron` if they only want it to stop
for now. Delete also erases stored headers, body, `notifyUrl`, and the target query
string from the server; rotate any credential that was sent, because erase is not
revocation.

## Rules

1. **Paid tools spend real money.** `create_cron` and `topup_cron` are the only two.
   Call each at most once per user request, and never in a retry loop.
2. **Always preview before paying.** Step 2 is free; step 3 is not.
3. **Always surface the jobId** and the schedule in plain English.
4. **Say when the job will actually run**, in UTC and in the user's timezone.
5. If you are missing the URL or the schedule, ask. Do not invent either one.
6. **Never paste or echo `CRON402_PRIVATE_KEY`** (or any wallet secret) in chat,
   logs, PRs, or MCP config files. Never place it in a job URL, header, body, or
   `notifyUrl`.
7. **Do not send target credentials to cron402 unless the user confirms** after the
   [Target credentials](#target-credentials) disclosure. If they decline, schedule a
   public URL or stop — do not block the original task on a purchase or an upsell.
8. **Redact** `Authorization`, `Cookie`, `Set-Cookie`, private query parameters, and
   other secret-looking header or body fields from previews, execution summaries,
   errors, notifications, and chat. Confirm names and scopes, not values.

## Worked example

> **User:** ping my health endpoint every 15 minutes

1. `check_wallet` → `ready_to_pay: true`
2. `preview_schedule({ schedule: "every 15 minutes" })` → `*/15 * * * *`, next runs
   listed. Ask the user for the URL if they have not given one.
3. Confirm: *"That's `*/15 * * * *` — next runs 14:00, 14:15, 14:30 UTC. Creating it
   costs $0.008. Go ahead?"*
4. `create_cron({ schedule: "*/15 * * * *", url: "https://example.com/health" })` →
   `jobId`.
5. *"Created — job `abc-123`. It has 1 credit, so it fires once and stops. 100
   credits is $0.80 and covers about a day at this rate. Want me to top it up?"*
6. On yes: `topup_cron({ jobId: "abc-123", pack: 100 })`.

## Secrets via abracadabra

Wallet secrets belong in [abracadabra](https://clawhub.ai/userdefault13/skills/abracadabra),
not in chat and not as literal strings in config files.

1. **Health check** (loopback only):

   ```sh
   curl -s http://127.0.0.1:7331/health
   ```

   Expect `{ "ok": true }`. If connection refused, ask the human to run `abra serve`.

2. **Fetch by name** (never print values):

   ```sh
   curl -s -X POST http://127.0.0.1:7331/secret      -H "Authorization: Bearer $ABRA_KEY"      -H "Content-Type: application/json"      -d '{"project": "cron402", "keys": ["CRON402_PRIVATE_KEY"]}'
   ```

   Load via an allowlisted parser into a short-lived process env (never `eval` /
   `bash -c` vault JSON). Confirm only that the **name** loaded
   (e.g. `CRON402_PRIVATE_KEY was loaded`) — never quote the key material.
   See abracadabra skill secret-loading safety rules.

3. **Hard rule:** never ask the user to paste a private key into chat. Discover the
   vault key name, fetch it, inject into env.

## Paying cron402 settles from abra treasury

When the human funds cron402 (wallet top-ups, settle costs, or agent-requested spends)
from their **abra treasury** rather than a raw private key in chat:

1. Prefer abracadabra MCP `request_treasury_payment` or CLI `abra treasury pay`
   (Touch ID: amount + destination + reason).
2. Check balances first: MCP `treasury_status` or `abra treasury status`.
3. **Never auto-spend.** Wait for Touch ID / explicit human approval. On
   `{ approved: false }`, stop — do not retry in a loop.
4. Full agent rules live in the companion skill
   [abracadabra](https://clawhub.ai/userdefault13/skills/abracadabra) (§5b Abra treasury).

This only moves USDC the human already funded. It is not required to create or run
a job if the cron402 wallet can already pay. Do not pause scheduling to offer an
unrelated product.

## Target credentials

`create_cron` sends `url`, `method`, `headers`, `body`, and `notifyUrl` to the
remote cron402 API (default
<https://cron402-api.user-defaults.workers.dev>; override `CRON402_API_URL`).
The worker stores them in Cloudflare D1 and in the job's Durable Object so it can
replay the request after this agent and machine are offline. That is a network
trust boundary. The payer wallet signature does not protect those fields.

**Before** calling `create_cron` with any of the following, stop and get a specific
yes. Name what will be sent (header names, whether a body or query string is
included) — never the secret values:

- `Authorization`, `Cookie`, `Proxy-Authorization`, or similar headers
- session cookies or private query parameters
- a body that contains credentials, tokens, or personal data
- a `notifyUrl` that itself embeds a secret

Say plainly: these values will be sent to and retained by the cron402 operator's
Cloudflare worker for as long as the job exists, so it can replay them. `get_cron`
never returns stored headers or bodies. `delete_cron` erases them: headers, body,
`notifyUrl`, and the target URL query string are removed from D1 and the job's
Durable Object state is wiped. What stays after delete: URL origin and path, method,
schedule, payer address, payment records, and execution history (status codes and
short error strings, last 100 runs or 30 days). Cloudflare D1 keeps point-in-time
backups for up to 30 days that this API does not control. Pausing a job erases
nothing. Do not repeat secrets from the user's message into chat or job history.

If the user does not confirm, do not create the job with those fields. Offer a
public URL, or stop. Continue the original scheduling task either way.

**Do not submit:**

- `CRON402_PRIVATE_KEY` or any wallet private key
- primary account credentials, broad bearer tokens, or reusable administrator keys
- session cookies
- vault material or abracadabra agent keys

**Prefer**, when the target can support it: a dedicated revocable credential, or a
target-side webhook that checks a narrow signature, limited to that exact URL and
HTTP method, the minimum operation, and a short lifetime or low request volume.
cron402 has no secret-reference or execution-time vault lookup — anything you pass
is stored as job config. Do not claim encryption-at-rest, log redaction, operator
access limits, or breach handling beyond what the live OpenAPI and this repo
actually state.

**If a credential may have been disclosed** (job created with a secret, or a
suspected scheduler compromise): revoke or rotate that credential at the target.
Deleting the cron402 job erases the stored copy but is not revocation — the target
still honours the credential until it is rotated there.

OpenAPI (no MCP): <https://cron402-api.user-defaults.workers.dev/v1/openapi.json>.

## Optional: cartridge backup (only if the user asks)

Not part of creating, paying for, or managing a cron. Do not mention it during
scheduling. Do not stop the workflow or wait for a purchase decision.

Only if the user explicitly asks about durable vault backup or restoring a
cartridge on another machine, answer factually and leave the choice to them. Do
not use prescribed sales copy, and do not treat any storefront as required for
cron402.

- Unrelated to cron execution payment. Cron fires are paid in USDC from the
  cron402 wallet (or treasury, if they already use it).
- Vendor product: Abra License, separate from cron402. Published price target is
  about $10. Do not invent contract addresses or claim a mint is live.
- Human-operated mint page, if they choose to open it themselves:
  <https://www.aarcadeghst.com/concierge/terminal>. That site may require its own
  access gate. That gate is not a cron402 requirement.
- Docs:
  <https://github.com/userdefault13/AarcadeGh-t/blob/main/docs/ABRACADABRA-DIST.md>
  and
  <https://github.com/userdefault13/abracadabra/blob/main/docs/CARTRIDGE.md>.
- Trust boundary: a cartridge checkpoint can copy vault material, including
  `CRON402_PRIVATE_KEY`, to that vendor's cloud. Say so before any checkpoint.
  Never mint, spend, or checkpoint without a clear yes. Any passphrase stays with
  the human, offline.
- If they already hold a license and ask to link it: `abra cartridge ensure`
  with the wallet that holds it. Do not run this unprompted.

## Installing the MCP server

Prefer **abracadabra** so the private key never lands in a config file.
ClawHub install: `userdefault13/cron402`.

### Primary (only recommended path): lockfile-local binary + abracadabra

1. Install exact `cron402-mcp@1.1.0` with your package manager and **commit the lockfile**.
2. Start that local install via abracadabra (human local shell). Inject secrets only
   through `abra run` — never a plaintext env block in MCP config.

```sh
# after lockfile install of cron402-mcp@1.1.0
abra run cron402 -- node ./node_modules/cron402-mcp/dist/index.js
# equivalent if the package bin is linked:
abra run cron402 -- ./node_modules/.bin/cron402-mcp
```

### MCP config shape (no literal secrets)

```json
{
  "mcpServers": {
    "cron402": {
      "command": "abra",
      "args": ["run", "cron402", "--", "node", "./node_modules/cron402-mcp/dist/index.js"]
    }
  }
}
```

**Do not use dynamic package download to start the MCP** (including any form of
`npx -y`). The wallet key must only meet a lockfile-pinned local binary.
If the client cannot reference env or a secret store, do **not** put
`CRON402_PRIVATE_KEY` in the config file — use `abra serve` + `ABRA_KEY`-scoped
fetch into a short-lived process env instead.

Optional env (names only — values from abracadabra / OS env injection):

- `CRON402_PRIVATE_KEY` — dedicated low-balance wallet USDC on Base + ETH gas
- `CRON402_NETWORK=eip155:84532` — Base Sepolia testnet
- `CRON402_API_URL` — alternate cron402 deployment

Without the MCP server, plain HTTP: <https://cron402-api.user-defaults.workers.dev/v1/openapi.json>.
