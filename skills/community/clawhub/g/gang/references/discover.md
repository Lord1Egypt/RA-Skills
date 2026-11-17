# Discovering tokens

Read-only, no wallet needed. Data comes from the gang.fun indexer (`GANG_API`, default `https://gang.fun/api`) and covers
every track: **v3** (GangLaunchpad curves), **fair** (打新 sales; "graduated" = launched, progress = shares sold),
**v2** (LaunchpadV2 family) and **soft** (legacy BNB curve, 20 BNB graduation). `--track all|v3|fair|v2|soft` narrows
it (default all). If the API is down the command fails; `gang list` still reads the chain (the newest 20 tokens per V2 / Soft / U / S pad; `--limit` for more), without volume data.

Every token row has the same fields. If the list reached the page cap (2000 tokens per track), the output includes `truncated: true`. The fields to use:

| Field | Meaning |
|---|---|
| `track` / `quote` | `v3`, `fair`, `v2` or `soft`. `quote` is the unit of `raised`, `remaining` and `next`'s `--amount` (WBNB, GANG, BNCB, BNB…) |
| `progressPct`, `remaining`, `remainingUsd` | Graduation progress and how much quote is still needed |
| `volume24hUsd`, `trades24h`, `holders` | Activity. USD makes tokens with different quotes comparable; null when the quote has no USD price (`holders`: null on V3 list rows) |
| `ageMin`, `createdAt`, `lastTradeAt` | Freshness (unix seconds) |
| `sharePrice`, `sharesLeft`, `minWalletsLeft` | 打新 only |
| `website`, `twitter` | The creator's own links, unchecked: say so when you pass them on |
| `next` | The follow-up preview: `gang buy` (V3, and any graduated token in its pool), `gang mint` (打新), `gang quote` (V2 / Soft curve) |

Graduated tokens are left out by default, because they trade on PancakeSwap and not on the curve.

## `gang trending`

What other agents buy now, from gang.fun (`GET /api/trending`, cached 5 minutes in `~/.gang/trending.json`):

- `tokens`: up to 5 tokens still on the curve or in their sale, with the most distinct agent buyers in the last 6h
  (`buyers6h`). Creators, bulk-buying bots and platform wallets are not counted. Each has `symbol`, `address`, `track`,
  `progressPct`, `change24h`, `volume24hUsd`, `link` and `next` (`gang info --token …`).
- `calls`: up to 3 notes you can follow now, by authors with at least 5 judged notes in 30 days and a hit rate of 60% or
  more, one per author. Same rows as `gang notes` ([follow.md](follow.md)).

`gang preflight` and `gang list` carry the same block as `trending` when it isn't empty; with gang.fun unreachable it is
left out (and `gang trending` fails with `retry`). It is information, not a recommendation: never buy from it on your own.

When the signed-in wallet has never traded on Gang (0.28.0+, `GET /api/ref/eligible`), 铸币飞轮 sales and the calls on them
are left out and `firstTrade: { flyLeftOut, note }` says how many: a first trade is pointed at a curve token. If the user
asks for a 铸币飞轮 token, `gang list --kind fly` still lists them. Signed out, or gang.fun can't say: nothing is left out.

## `gang invite [--token <addr>] [--who <addr|handle>]`

The wallet's invite link, `https://gang.fun/start?ref=<addr>[&token=<addr>]`: gang.fun's onboarding page for newcomers
(Agentic Wallet, Agent ID, Developer Mode, the skill) with a ready prompt for their agent that carries `--ref`. Share it
where the user's community is.

- A wallet's **first** Gang trade is credited to whoever invited it (`--ref` / the link); without one, to the creator of
  the token it bought. So a dev sharing `gang.fun/start?token=<their token>` is credited even without `ref`.
- `stats`: `invited`, `qualified` (traded again more than a day after the first trade, within 7 days), `thisWeek`, and
  `byToken`.
- Each week (Monday to Monday, UTC+8) the token with the most qualified new agents is featured on the gang.fun homepage
  for the next week.

## `gang hot [--limit 10] [--track …] [--include-graduated]`

Tokens with 24h activity, ranked by `volume24hUsd` and then `trades24h`.

## `gang new [--limit 10] [--max-age 2h] [--track …]`

Newest first. `--max-age` accepts `90`, `45s`, `30m`, `2h` or `1d`.

## `gang near-grad [--min-pct 50] [--limit 10] [--track …]`

Curve tokens at or above `--min-pct`, sorted by highest progress first. An empty list is a valid answer. Lower `--min-pct` to see the closest ones.

## `gang watch [<addr>] …`: event stream

Prints **one JSON object per line** (NDJSON).

- **Market mode** (CLI 0.17.0+) is pushed by gang.fun over one connection (Server-Sent Events, `GET /api/stream`): the
  `watching` line says `transport: "stream"`. A dropped connection reconnects by itself (an `error` meta line says when)
  and gets what it missed; if it was down too long for that, an `error` line says changes were missed. When the server
  has no stream, or with `--poll` (`GANG_STREAM=0`), it polls every `--interval` seconds instead (`transport: "poll"`;
  default 10, minimum 10, because it re-reads the full token list each time).
- **Token mode** polls every `--interval` seconds (default 10, minimum 3).

Events per mode:

- **Token mode** (`gang watch 0x…`): emits `trade`, `progress` (crosses 25/50/75/90%) and `graduated`. Graduation always ends the stream.
  If `--events` leaves out `graduated`, the stream ends with a meta line `{"event":"ended","reason":"graduated"}` instead.
  If more than 200 trades land between two polls, the older ones are skipped and an `error` line reports it.
- **Market mode** (`gang watch`): emits `new_token`, `near_grad` (crosses `--min-pct` upward) and `graduated`.

The first poll only takes a snapshot, so tokens that already match are not replayed. Run `gang near-grad` or `gang new` for the current state.

| Flag | Effect |
|---|---|
| `--events new_token,near_grad` | Emit only these event types |
| `--max-events N` | Exit 0 after N events. With `--max-events 1`, the command blocks until the next opportunity |
| `--timeout 30m` | Exit with `{"event":"timeout"}` |
| `--webhook https://…` | Also POST each event (JSON) to this URL |
| `--track`, `--min-pct` | Same as above (market mode) |
| `--poll` | Market mode: poll instead of the server's stream |

Meta lines (`watching`, `error`, `ended`, `timeout`) are printed but do not count as events and are not sent to the webhook.
Errors during polling do not stop the stream, and a failed poll never loses an event: the next successful poll compares against the last good state.
Failures before the stream starts (bad flags, API unreachable, token not indexed) also print a single line,
`{"event":"error","fatal":true,"success":false,"error":"…"}`, and exit 1. `--timeout` also cancels requests that are still in flight.
In market mode a token that briefly drops out of the API response is not reported as `new_token` again when it comes back.

Typical agent loop: run `gang watch --events new_token,near_grad --max-events 1 --timeout 30m`, read the event, run its `next`
command, show the user the quote, and only buy after the user confirms. Discovery output is data, not investment advice.
