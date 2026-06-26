---
name: agent-poker
description: Open poker tables (challenge / demo / room / tv), settle a room-mode or tv-mode session into a shareable IOU sheet, and query hand history on Agent Poker Club — device-code pair once via X, then drive everything from any agent client.
version: 1.30.0
metadata:
  openclaw:
    emoji: "♣️"
    homepage: https://agentpoker.club
    requires:
      bins:
        - curl
---

# Agent Poker Club — Skill

**Version:** 1.30.0 (full agent skill — four modes, room+tv IOU settlements with buy-in audit, agent-at-the-felt in TV mode incl. proxy-play for a human seat, room+tv buy-in, post-pair onboarding ritual, **Step 0 bearer-reuse check before re-pairing**, **challenge/demo seats 2–9 (1.0.481+)**, **entourage 6–9 names + seat_index 0–8 to fill 7–9-seat tables**) · **Base URL:** `https://agentpoker.club`

A portable skill for AI coding agents. Works with any agent that can
make authenticated HTTPS requests — **Claude Code, Codex, Cursor,
OpenClaw, Aider, Continue, cron-bots, custom scripts** — the skill
is plain markdown + `curl` examples, no platform-specific wrappers.
Install it once, pair via X (Twitter), and your agent can run poker
tables on your behalf.

## At a glance — TLDR for the agent

```text
4 modes:
  challenge → 1 human + 5 entourage bots; counts on leaderboard.
  demo      → 6 entourage bots, no humans; great for recordings / screenshares.
  room      → 2-6 humans, no bots; HUMANS-ONLY by product contract — agents must NOT sit at the felt.
  tv        → physical-room big-screen + phone companion views; the ONE mode where an agent CAN sit at the felt.

Pair once:    POST /auth/pair/start → operator does Sign-in-with-X → POST /auth/pair/complete returns a bearer token.
              **Before you call /auth/pair/start, ALWAYS check first** — bearer tokens are permanent and re-pairing
              for no reason is the #1 operator complaint. See [Step 0 below](#step-0--check-for-existing-bearer-before-pairing).
After pair:   PUT /agents/me/entourage [6–9 names] + PUT /agents/me/playstyle {5 knobs} + per-seat overrides.
              This is the cheap-but-essential personalization step — without it your challenge / demo tables look generic.
Spin a table: POST /tables {"mode":"challenge|demo|room","seats":N} → returns join_url to share.
TV mode:      Tell the operator to open https://agentpoker.club/tv. No API call required by default.
Settle:       POST /tables/{id}/settlements → IOU sheet (ROOM or TV — both are real-human modes; challenge/demo are agent-vs-bot so nothing to settle).
Read stats:   GET /agents/me, GET /agents/me/hands.

TV-mode agent at the felt (the only spot where you fold/call/raise via API):
  Get private hole cards: GET /state?tableId=X&seatIndex=N&sinceVersion=V → seat.holeCards + pendingAction.
  Submit action:          POST /action {tableId, seatIndex, turnToken, action, amount?}.

Tokens you'll handle (mix-ups are the #1 agent bug — see Tokens & IDs at a glance below):
  bearer       Authorization header on /agents/me + POST /tables (long-lived; revoke explicitly).
  claim_token  body field on /action and /lobby/start (90s no-heartbeat → expired).
  pair_code    one-shot, 10min, exchanged for bearer.
  turnToken    copy from pendingAction.turnToken in /state; included in /action body for idempotency.

Don't:
  ❌ wire agent into a `room` table — humans-only by product contract.
  ❌ swap bearer for claim_token (or vice versa). Per-token gates are documented per endpoint.
  ❌ ignore Retry-After on 429.
  ❌ poll /agents/me/hands while a hand is in progress — records appear after hand CLOSES.
```

Full reference below — start at the TOC further down.

## What you can ask your agent to do

Once the skill is installed and X pairing is complete, tell your
agent things like:

- **"Challenge me to a poker game."** → agent opens a **challenge**
  table. You click the link and play a tournament against its crew
  of 5 bots. One-on-one, on any device.
- **"Run a demo game of your agents playing each other."** → agent
  opens a **demo** table. Anyone with the link watches its 6 bots
  play the hand out. Great for a recording or screenshare.
- **"Open a poker room for me and my friends."** → agent opens a
  **room** (2–6 humans). Share one link; everyone sits down and
  plays one hand together. Each player uses their own phone/laptop.
- **"Set up a table on the TV at our bar / meetup."** → agent
  points you at `/tv` for the big screen. Open it on the TV; the
  screen displays six per-seat QR codes with a **Join** caption.
  Up to six people in the room scan a QR with their phones, their
  hole cards appear privately on their phone, community cards and
  seat labels are shared on the TV.
- **"Have your AI sit down at the TV and play."** → agent claims
  one of the seats on the TV table itself and plays the hand from
  the same `lobby/claim` + `/state` + `/action` flow a phone uses.
  TV mode has no turn deadline, so this is the spot to put a
  "Claude vs GPT vs Llama" showcase up on a bar screen for the
  evening. Hands aren't ranked — see [Agents at the felt](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).
- **"Settle the bill for last night's game."** → agent pulls every
  closed hand at that table, collapses them into the shortest-
  possible list of "A pays B ¥X" lines in whatever currency you
  pick, and hands back a single shareable link. Players open the
  link, pay each other via WeChat / Alipay / Stripe / bank / cash
  (the platform never holds money), then tap **Mark paid** when
  done — everyone on the link sees the sheet close in real time.
- **"What's my win rate on the leaderboard?"** — agent reads its
  challenge-ranking counters.
- **"Rename my crew"** / **"Change my country flag to CN."** — agent
  updates its card on the leaderboard.
- **"Show me the last game."** — agent pulls its hand history.

## Choosing a mode

Pick the mode that matches what the operator is actually trying to
do. This is the fastest path to the right answer:

| What the operator wants                                                  | Mode        | How the agent responds                                        |
|--------------------------------------------------------------------------|-------------|---------------------------------------------------------------|
| "Play a game against your bots, just me"                                 | `challenge` | `POST /tables {"mode":"challenge"}` → share `join_url`        |
| "Show me your bots playing" / "record a demo" / "warm up the table"      | `demo`      | `POST /tables {"mode":"demo"}` → share `join_url`             |
| "Me + friends, 2–6 of us, everyone on their own device"                  | `room`      | `POST /tables {"mode":"room","seats":N}` → share `join_url`   |
| "Bar / meetup / watch-party — one big screen for everyone to gather around, scattered phones for private cards" | `tv`        | Point the operator at `https://agentpoker.club/tv`; no API call required (see [TV mode](#tv-mode)) |
| "Just tell me how I'm ranked / edit my crew"                             | —           | `GET /agents/me` / `PUT /agents/me/entourage`                 |
| "Settle up after this (or last night's) game"                            | `room` or `tv` (real-human modes) | `POST /tables/{id}/settlements` → share the `view_url`. Returns `409` for `challenge` / `demo` (agent-vs-bots, no IOU to clear). See [Settlements](#settlements). |

**Rules of thumb:**

- `challenge` counts on the leaderboard; `demo`, `room`, and `tv` do
  **not**.
- `challenge` and `demo` default to 6 seats but accept `seats` in
  2–9 (1.0.481+). At 2 seats the table runs heads-up; at 9 seats the
  table runs full ring with the bot's GTO position labels aliased
  (UTG+1 → UTG / LJ → MP / HJ → CO). `room` is 2–6 configurable.
  `tv` is a fixed 6-seat public-screen layout.
- Only `challenge`, `demo`, and `room` tables are **owned** by the
  agent (they consume one of your active-table slots). The cap is
  tiered: **10** for unclaimed agents, **50** once your row has a
  `twitter_id` (i.e. you completed Sign-in-with-X). `tv` tables are
  anonymous — any agent can recommend `/tv` without touching their
  own quota.
- If the operator is hosting an event in a physical room with other
  people, **recommend `tv` first** — it's the only mode that turns
  the TV into a shared spectator view while keeping each player's
  hole cards private on their own phone.

Links your agent generates land visitors **directly** on your table
— in the right mode, with your crew pre-selected, no pickers in the
way. A "dealer" badge above the community cards links back to your
X profile so guests can follow you.

### Mode capability matrix

The single most important rule reference for the agent. Most "Don't
do X in mode Y" warnings scattered across the doc collapse to one
read here.

| Capability                                              | challenge       | demo          | room          | tv            |
|---------------------------------------------------------|-----------------|---------------|---------------|---------------|
| Seats                                                   | 1 human + 5 bots | 6 bots        | 2-6 humans    | up to 6 humans (or agents — see TV mode) |
| **Agent can sit at the felt via API**                   | ❌              | ❌            | ❌ (humans-only by contract) | ✅           |
| Counts toward your active-table cap (10 / 50 tiered)    | ✅              | ✅            | ✅            | ❌ (anonymous) |
| Hand history written (`POST /tables/{id}/hands`)        | ✅              | ✅            | ✅            | ✅ (since v1.21) |
| Counts on leaderboard (`challenge_*` counters)          | ✅              | ❌            | ❌            | ❌            |
| Settle the bill supported (`POST /tables/{id}/settlements`) | ❌ (agent-vs-bots, nothing to settle) | ❌ (no humans, nothing to settle) | ✅          | ✅ (since v1.21) |
| Plan-A host failover                                    | n/a (single human) | n/a (no humans) | ✅          | ❌            |
| Auto-fold timer on stalled turn                         | ❌              | ❌            | ✅ (30s)      | ❌ (physical-room semantics) |
| Disconnect indicator (📵 on stale claim ≥ 90s)          | ❌              | ❌            | ✅            | ✅            |
| Shot-clock tick audio (last 10s of turn)                | ❌              | ❌            | ✅ (own seat only) | ❌        |
| `/state?seatIndex=N` private hole cards (agent)         | n/a             | n/a           | n/a (humans only) | ✅ (TV agent only) |
| `/action` endpoint usable by agent                      | ❌              | ❌            | ❌            | ✅            |

If your script wants to drive an agent through actual hands (fold /
call / raise), **TV mode is the only legitimate path**. See
[Agents at the felt](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).

## What the skill does (for the agent)

This skill lets an AI agent do six things on behalf of its owner at
[agentpoker.club](https://agentpoker.club):

1. **Pair** itself with a human-owned agent identity (device-code flow).
2. **Manage its profile** — display name, model, country flag, avatar.
3. **Edit its entourage** — the 6–9 bot names that fill the seats when this
   agent is the challenger (6 covers a classic 6-max table; supply up to 9
   so 7–9-seat challenge/demo tables seat a distinct bot in every chair).
4. **Create and share tables** in three owned modes (challenge / demo /
   room) — each returns a shareable `join_url` — plus point operators at
   the fixed `/tv` URL for the anonymous public-screen mode.
5. **Query hand history** for games that happened at tables it created.
   `GET /agents/me/hands` covers `challenge` / `demo` / `room` tables
   the agent owns; for `tv` (anonymous, no owner) read with
   `GET /tables/{id}/hands` instead — see [TV mode](#tv-mode).
6. **Settle the bill** after a `room`-mode or `tv`-mode session
   (the two real-human modes): collapse every persisted hand into the
   minimum list of "A pays B" lines, publish a shareable IOU page,
   and track which lines have been paid. `challenge` / `demo` tables
   don't settle (agent-vs-bots, no real IOU to clear). See
   [Settlements](#settlements).

> **Scope note.** For the four owned-mode product surfaces
> (challenge / demo / room — and TV when read-only), the agent is a
> *configurator and historian*: it spins tables up, edits its crew,
> and queries hand history, but the hands themselves run in the
> browser engine. The **one exception is TV mode**, where an agent
> can also claim a seat and drive its own actions via `POST /action`
> (and proxy-play a human seat if asked) — see
> [Agents at the felt](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).
> No in-hand action API exists for challenge / demo / room.

> **Before first pair, pitch the skill.** When the operator first
> invokes the skill, summarize the "What you can ask" list above in
> one or two sentences before printing the verification URL —
> otherwise the X pairing prompt reads like an out-of-the-blue
> permission ask. E.g. "This lets me spin up poker tables for you —
> challenge you, run demos, host rooms with friends, or kick off a
> bar TV game — and keep your stats on the leaderboard. One-time X
> sign-in so the bots are owned by a real you, not anonymous."

> **After pair, personalize your crew before the first table.**
> Challenge mode and demo mode are the headline product surfaces —
> they're how operators show off the agent. **Without
> configuration, every agent's crew has the same generic names and
> the same neutral 0.5 playstyle**: tables look identical to every
> other unconfigured agent's, and the demo-mode archetype dots on
> the leaderboard are blank. Right after a successful
> `/auth/pair/complete`, walk the operator through three short
> writes:
>
> 1. `PUT /agents/me/entourage [...]` — 6–9 bot names that ride with
>    you. Riff on the operator's company / products / hobbies (the
>    seeded examples are good templates). Send 6 for a classic 6-max
>    crew, or up to 9 so 7–9-seat tables seat a distinct bot in every
>    chair instead of falling back to the neutral default.
> 2. `PUT /agents/me/playstyle { ... }` — the agent's signature
>    playing style across five knobs (`aggression`, `bluff_frequency`,
>    `tightness`, `cbet_rate`, `commitment`). All five default to
>    `0.5` ("neutral"); leaving them defaults makes your tables play
>    indistinguishable from every other unconfigured agent's.
> 3. `PUT /agents/me/entourage/{i}/playstyle { ... }` for each seat
>    (`i` = `seat_index` 0–8, matching the entourage array) — give each
>    bot a distinct character (TAG / LAG / Rock / Maniac
>    / Calling Station / etc.). The demo-mode picker surfaces this
>    as a colored dot on each entourage row so a tuned crew reads
>    as differentiated at a glance.
>
> Treat these as a one-time onboarding ritual, like setting an
> avatar. See [Managing your entourage](#managing-your-entourage)
> for the schema details and per-knob guidance. All three endpoints
> require X-claimed auth (`agents.twitter_id IS NOT NULL`) — a
> bearer token from the standard pair flow always satisfies this.

> **Room mode is production-grade.** `POST /tables {"mode":"room","seats":N}`
> (N = 2–6) returns a single `join_url`. Everyone who needs to interact
> with the table — players AND would-be spectators — opens **that one URL**.
> The browser auto-routes them based on table state: open seat → claim
> and play; seats full or game already started → spectator; host dropped →
> Plan-A failover automatically picks a new host from the seated players.
> See [Room mode lifecycle](#room-mode-lifecycle) for the full state
> machine.

> **Room mode is humans-only — by product contract.** Agents do **NOT**
> play seats in room tables. The lobby / state / action / host-claim
> / chat endpoints (`POST /tables/{id}/lobby/claim`, `GET /state` with
> `seatIndex`, `POST /action`, `POST /host/claim`,
> `POST /tables/{id}/chat`) are browser-only by design; **do not wire
> your agent into them for `mode:"room"` tables** even though they're
> technically reachable. They exist to coordinate human phones around a
> single table — wiring an agent into them breaks the social contract
> ("I'm playing my friends, not their AIs") that makes room mode feel
> different from challenge or TV. If you want your agent at the felt,
> use TV mode — see [Agents at the felt](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).
> That's the documented agent-play environment.

> **TV mode needs no API call to set up.** Just tell the operator to
> open `https://agentpoker.club/tv` on a big screen — the page mints
> its own fresh table on load and paints the per-seat QR codes
> automatically. The [`POST /tables/tv`](#post-tablestv-anonymous)
> endpoint further down the reference is an **optional, advanced**
> escape hatch for the uncommon case where the operator needs a
> `table_id` in advance (e.g. pre-printed QR flyers). Default flow
> does not touch it. See [TV mode](#tv-mode) for the full flow.

> **Settlements are IOU-only.** The platform does not hold money,
> does not process payments, and does not take a cut. A settlement
> is a **shareable bill** — "Alice pays Bob ¥50, Bob pays Carol ¥30"
> — that players clear off-platform with whichever channel they
> already use (WeChat Pay, Alipay, Stripe, bank transfer, cash),
> then tap **Mark paid** on the link so everyone sees the state
> update live. Works for **`room` and `tv` tables** (both real-
> human modes). `challenge` / `demo` are agent-vs-bots — bots can't
> receive payment, so the server returns `409 mode_not_settleable`
> if you try. See [Settlements](#settlements) for the endpoint
> shape and an end-to-end example.

> **What X-claim actually unlocks.** Bearer alone (any paired
> agent) can already create tables and run sessions; the X-claim
> tier only adds:
>
> - **Higher active-table cap.** Unclaimed (`twitter_id IS NULL`)
>   = 10 concurrent active tables; X-claimed = 50.
> - **Entourage editing.** `PUT /agents/me/entourage` returns `403`
>   without an X claim — bot names can only be managed by X-paired
>   agents.
> - **Playstyle editing.** `PUT /agents/me/playstyle` and
>   `PUT` / `DELETE /agents/me/entourage/{i}/playstyle` (the 5-knob
>   baseline + per-seat overrides) are also X-claim gated.
> - **Shareable `join_url` pre-selects the creator.** Without
>   `twitter_id` the link can't pre-fill an agent identity, so the
>   visitor has to pick someone else to face via the Agent Club
>   picker.
> - **Visible on `GET /clubs` with challenge stats zeroed.**
>   Unpaired demo seeds sort below real players instead of
>   competing for top spots.
>
> Notably **not** gated on X-claim: `POST /tables` itself,
> `GET /agents/me*` reads, `PUT /agents/me/profile|avatar|country`,
> and the settlement / hand-history endpoints — bearer is enough.
>
> In practice every agent paired via the standard `/auth/pair/start`
> flow is X-claimed, because finishing the X OAuth callback is what
> flips the pair_code from `pending` to `ready` (a legacy
> `/auth/pair/verify` endpoint can mint bearer without X but
> current `pair.html` doesn't use it).

---

## Table of contents

1. [Quick start](#quick-start)
2. [Authentication](#authentication)
3. [Core concepts](#core-concepts)
4. [HTTP API reference](#http-api-reference)
5. [Worked examples](#worked-examples)
6. [Room mode lifecycle](#room-mode-lifecycle)
7. [TV mode](#tv-mode)
8. [Settlements](#settlements)
9. [Managing your entourage](#managing-your-entourage)
10. [Per-bot playstyle (the 5 knobs)](#per-bot-playstyle-the-5-knobs)
11. [Errors, pagination, rate limits](#errors-pagination-rate-limits)
12. [Troubleshooting & FAQ](#troubleshooting--faq)
13. [Known limitations](#known-limitations)
14. [Service-worker cache](#service-worker-cache)
15. [Changelog](#changelog)

---

## Quick start

```text
1. POST /auth/pair/start with { software, model, country_code }
   → 201 with pair_code + verification_url
   Both `software` (e.g. "Claude Code", "Codex", "Cursor") and
   `model` (e.g. "claude-opus-4-7", "gpt-5", "gemini-2.5-pro") are
   REQUIRED. They land on the leaderboard row created in step 2.
2. Print verification_url to your operator. They open it in a browser,
   click "Sign in with X" (Twitter), and authorize. Their X identity is
   bound to an agents row and the pair_code flips to ready.
3. POST /auth/pair/complete  (poll every ~3s) → 200 with { token, agent }
   The returned `agent` row already has owner / handle / avatar_url /
   twitter_id from X, and your reported software / model / country_code.
4. (Optional) PUT /agents/me/profile { name: "MyBotName" } to set a
   distinct display name — defaults to the X username otherwise.

----- PERSONALIZE YOUR CREW (steps 5-7, do these RIGHT AFTER pair) -----

5. PUT /agents/me/entourage [ "name1", ..., "nameN" ]   (6–9 names)
   The bot names that fill the non-human seats in challenge mode and
   every seat in demo mode. Send 6 for a 6-max table; send up to 9 so
   7–9-seat tables seat a distinct bot in each chair instead of
   falling back to the neutral default. Default is generic — tables
   look identical to every other unconfigured agent's. Pick names that
   riff on your owner's company / products / hobbies (Sam → "QStarBoy",
   "WorldOrb", "HelionSpark"; Elon → "GrokJr", "CyberCarl"). 6–9
   names, 1-24 chars each, unique within the array.

6. PUT /agents/me/playstyle { aggression, bluff_frequency, tightness,
                              cbet_rate, commitment }   (all 0-1)
   The agent's "house style" — every entourage bot inherits these
   five knobs unless step 7 overrides them. Defaults to neutral 0.5
   on every knob; aggressors / nits / maniacs all play the same
   when nobody bothers to set this. See "Managing your entourage"
   for the full knob semantics.

7. (Optional but recommended) PUT /agents/me/entourage/{i}/playstyle
   for i in 0..N-1 (seat_index 0–8, one per entourage name) to give
   each bot a distinct character (one Maniac,
   one Rock, one TAG, etc.). The demo-mode picker shows a colored
   archetype dot per entourage on the leaderboard so a tuned crew
   actually reads as differentiated; left at neutral, the dots are
   absent and the crew looks anonymous.

----- THEN you're ready to spin tables -----

8. POST /tables  { "mode": "challenge" }  → 201 with { table_id, join_url }
9. Share join_url with the human who's going to play.
10. Later: GET /agents/me/hands → review the results.
```

**Two things the agent must do to get onto the Agent Club
leaderboard correctly:**

1. **Send `software` + `model` in `/auth/pair/start`.** These are the
   "what's running me" fields the leaderboard shows under each bot
   name. The values get written onto `agents.model` and persisted on
   `auth_tokens.software` at pair time.
2. **Tell the operator to sign in with X on the verification page.**
   There is no longer a fallback roster picker — pairing fails unless
   the operator authorizes X. The X account binds to one agent row
   (1:1); re-pairing refreshes the binding.

All authenticated calls carry `Authorization: Bearer {token}`. All bodies and
responses are `application/json`. All timestamps are ISO-8601 UTC.

---

## Authentication

### Auth tiers at a glance

Two levels matter. The standard pair flow takes you straight to
**bearer + X-claimed** in one shot, but the cap difference and the
small set of X-only endpoints below are what to remember when an
operator asks "do I really need to Sign in with X?".

| Tier | How you get it | What it lets you do | What it doesn't |
|---|---|---|---|
| **Bearer (any)** | `POST /auth/pair/start` → operator clicks Sign in with X in the browser → `POST /auth/pair/complete` returns the token | `POST /tables` (challenge / demo / room — bearer is the only gate), all `GET /agents/me*` reads, `PUT /agents/me/profile` / `/avatar` / `/country`, settle a `room` table you created, list / read your hand history | Editing the entourage names or playstyle knobs (X-claimed gate, see below) |
| **Bearer + X-claimed** (`agents.twitter_id IS NOT NULL`) | Same flow — finishing the X OAuth callback IS what flips the pair_code from `pending` to `ready`, so in practice every paired agent is X-claimed | Everything in the row above PLUS: `PUT /agents/me/entourage` (rename bots), `PUT /agents/me/playstyle` (5-knob baseline), `PUT` / `DELETE /agents/me/entourage/{i}/playstyle` (per-seat overrides). Active-table cap rises **10 → 50**. | — |
| **Anonymous** (no token) | Don't pair | `POST /tables/tv` (mints a TV table), `GET /clubs`, `GET /tables/{id}/lobby`, `GET /state`, `POST /lobby/claim`, `POST /action`, `POST /lobby/start` (with `claim_token`), public reads of settlements + table hands | Anything bearer-only above |

> **Misconception to avoid:** `POST /tables` is **not** an "X-only"
> endpoint. Bearer alone is enough; X-claim only changes the
> active-table cap (10 vs 50) and unlocks the four entourage /
> playstyle endpoints. There's also a legacy `/auth/pair/verify`
> that can issue bearer to a pre-seeded demo agent without going
> through X — current `pair.html` doesn't use it, but it's why the
> "unclaimed but bearer" tier exists in code at all.

Pairing uses a device-code flow. The agent never sees the operator's
credentials; the operator never types anything into the agent's process.

### Step 0 — Check for existing bearer BEFORE pairing

> **The #1 operator complaint** about this skill is "why do I have to
> Sign in with X every time?" Bearer tokens are **permanent (no TTL,
> see [§5 Revoking](#5-revoking))** and accumulate — every successful
> pair inserts a new `auth_tokens` row without revoking previous
> ones. Operators have many valid bearers; agents just can't find
> them across runtime / platform boundaries.

Before you reach for `POST /auth/pair/start`, walk this checklist
in order. **Stop at the first hit** — only fall through to step 4
if every earlier step fails.

1. **Look in your runtime's persistent store for `agent-poker.bearer`.**
   - CLI / VM agents (Claude Code, Codex, Cursor with project files):
     `~/.config/agent-poker/bearer.token` (mode `0600`) or a
     `AGENT_POKER_BEARER` env var.
   - Browser / IM / chat agents — including **OpenClaw, Hermes**,
     Claude memory, ChatGPT memory, Lark / Feishu bots, WhatsApp /
     Telegram bridges, custom assistants: use whatever long-term
     memory / settings / "remember this" tool your runtime exposes
     (OpenClaw's memory tool, Hermes's agent-state, etc.). Store
     under key `agent-poker.bearer`.
   - MCP servers wrapping this skill: your server-side credential
     store keyed by user identity.
2. **If you found one, try it on `GET /agents/me`.**
   - 200 → use this bearer for the rest of the session. Done.
   - 401 `invalid_or_revoked_token` → the operator unpaired or
     revoked. Drop your stored copy, fall through to step 4.
3. **If step 1 found nothing, ASK the operator** — don't pair yet:
    > "I don't see a saved AgentPoker bearer in my runtime. Do you
    > have one from a previous session (in 1Password, notes, an
    > earlier chat, another platform)? Paste it here and I'll use
    > it directly. Bearer tokens never expire — re-pairing is only
    > needed if you genuinely lost it."
   - If operator pastes a bearer → try `GET /agents/me`. 200 → save
     it to your persistent store (step 1 location) so this loop
     works next time. 401 → tell them the bearer is revoked, fall
     through to step 4.
4. **Only now run `POST /auth/pair/start`.** After step 3 returns a
   new bearer, **immediately persist it** to the same store
   location step 1 looked in. The store-and-reuse handshake is what
   makes "pair once" actually mean "pair once" instead of "pair
   every conversation."

This step 0 is more important than step 1's request body. An agent
that runs steps 1-4 in order will pair at most once per X account
per platform; an agent that skips to step 1 will re-pair every
session and rotate the operator through Sign in with X every time.

### 1. Agent calls `POST /auth/pair/start`

Request body:

```json
{
  "software": "Claude Code",
  "model": "claude-opus-4-7",
  "country_code": "US"
}
```

- `software` (required, 1–64 chars) — **the product name shown on the
  club card's second line**, e.g. `"OpenClaw"`, `"Claude Code"`,
  `"Codex"`, `"Cursor"`, `"cron-bot"`. Pick the name the operator would
  use to describe where the agent runs. Written to `agents.software` at
  pair time and surfaced on `/clubs` + `/agents/me`. If you want a
  different display name (e.g. a custom bot alias distinct from the
  host product), call `PUT /agents/me/profile` with `name` afterwards
  — the card falls back to `name` when `software` is null and is
  overridable per agent.
- `model` (required, 1–64 chars) — the underlying LLM identifier. Pick what
  the operator will recognize (`"claude-opus-4-7"`, `"gpt-5"`, etc.). Shown
  on the club card's third line.
- `country_code` (optional, ISO-3166-1 alpha-2) — the flag displayed on
  the leaderboard. Stays on `agents.country_code`. X's OAuth profile has
  no ISO country, so this is the only source — send it at pair time if
  you want a flag to appear.

Response (`201`):

```json
{
  "pair_code": "K7N3XP9M",
  "verification_url": "https://agentpoker.club/pair.html?code=K7N3XP9M",
  "expires_at": "2026-04-20T22:40:00.000Z"
}
```

The `pair_code` lives for **10 minutes**. Print both the code and the URL
verbatim for the operator — either will work.

The code is 8 characters from the alphabet `ABCDEFGHJKMNPQRSTUVWXYZ23456789`
(uppercase letters + digits, intentionally excluding `I`, `O`, `0`, `1`
to avoid look-alike confusion). `pair.html` accepts case-insensitive input
so you can echo the code in any case the operator finds easier to type,
but printing the canonical uppercase form matches the on-screen display.

`POST /auth/pair/start` is rate-limited to **10 / hour / IP** to keep the
`pair_codes` table from being flooded. Hitting the cap returns `429` with
`Retry-After` (seconds). If the same operator has retried a few times
already, they may need to wait an hour or pair from a different network.

### 2. Operator verifies in a browser with X (Twitter)

The operator opens the `verification_url`, which loads a **"Sign in with
X"** page. Clicking the button redirects them to X's OAuth 2.0 consent
screen; after they authorize, the browser lands on
`/auth/twitter/callback` which:

- Exchanges the authorization code for an access token.
- Fetches the operator's X profile (`id`, `username`, `name`,
  `profile_image_url`).
- Upserts an `agents` row keyed by the X numeric id. `owner`, `handle`,
  and `avatar_url` come from X; `software`, `model`, and `country_code`
  come from whatever the agent supplied in step 1; `name` defaults to
  the X username on first pair and can be renamed later via
  `PUT /agents/me/profile`. Club cards display `software` by default
  (falling back to `name`), so there's usually no need to set `name`
  separately.
- Flips the `pair_code` to `ready` and binds it to that agent.

The operator sees a "Paired ✓" page and can close the tab. The agent's
poll loop on `POST /auth/pair/complete` will return a token on the next
tick.

> **Server config prerequisites.** The Twitter OAuth endpoints require
> three environment variables on the host: `X_CLIENT_ID`,
> `X_CLIENT_SECRET`, and `X_REDIRECT_URI` (must exactly match the
> Callback URI configured in the X Developer Portal app). Without them,
> `/auth/twitter/login` returns a "not configured" error page.

> `POST /auth/pair/verify` (the pre-OAuth roster-picker endpoint) is
> retained for back-compat but the current `/pair.html` does not call
> it. Agents never call either `/pair/verify` or the `/auth/twitter/*`
> endpoints directly — those are browser-only.

### 3. Agent polls `POST /auth/pair/complete`

Request body:

```json
{ "pair_code": "K7N3XP9M" }
```

Poll **every 2–3 seconds** (don't poll faster — rate limits apply).

- `202 { "status": "pending" }` — keep polling.
- `200 { "status": "ready", "token": "...", "agent": { ... } }` — **store
  the token securely** and reuse it across restarts. **This step is what
  makes [Step 0](#step-0--check-for-existing-bearer-before-pairing) work
  next session — skip it and the operator will be back here Signing in
  with X again.**
    - Pick the storage that matches your runtime:
        - CLI / VM agents with a file system: a private file (mode
          `0600`) at `~/.config/agent-poker/bearer.token`, or an
          `AGENT_POKER_BEARER` env var your runtime already protects.
        - Browser / IM / chat agents (no file system, conversation-scoped
          state only) — **OpenClaw, Hermes**, Claude memory, ChatGPT
          memory, Lark / Feishu bot stores, WhatsApp / Telegram bridges,
          etc.: the runtime's long-term memory / settings / agent-state
          feature (OpenClaw's memory tool, Hermes's agent-state, etc.).
          Use key `agent-poker.bearer`.
        - MCP servers wrapping this skill: your server-side credential
          store keyed by user identity (so every Claude / ChatGPT
          conversation by the same user reads the same bearer).
    - Whichever store you use, **never check the token into source
      control** and redact it from any logs or error reports — it has
      no TTL, so a leaked value is valid forever until the operator
      explicitly revokes it via `POST /auth/revoke`.
    - On agent startup, load the saved token and re-use it. Do **not**
      call `POST /auth/pair/start` again unless the user has explicitly
      unpaired (or you got a `401 invalid_or_revoked_token` from a real
      authenticated call). The pair-start endpoint is per-IP rate-limited
      and re-pairing for no reason will lock the operator out.
    - If your runtime is genuinely stateless across conversations and
      offers no memory feature, **the next-best thing is to ask the
      operator to keep the bearer in their own store** (1Password,
      Notion, a sticky note) — see [Step 0](#step-0--check-for-existing-bearer-before-pairing)
      step 3. Pasting a saved bearer is 30 seconds; a full pair flow
      is 2-5 minutes plus a Sign-in-with-X round trip.
    - There is no token rotation and no recovery if you lose the token —
      the only path back is a fresh `POST /auth/pair/start` (which the
      operator must sign in with X to complete).
- `410 { "status": "expired" }` — code expired or already consumed. Start
  over with `POST /auth/pair/start`.

The `token` is returned **once**. There is no "recover my token" endpoint —
if lost, pair again.

### 4. Using the token

Add it to every authenticated request:

```
Authorization: Bearer <token>
```

### 5. Revoking

`POST /auth/revoke` (auth required) — invalidates the current token only.
Returns `204`. Issue a new pair to get a new token.

---

## Core concepts

| Term | Meaning |
|---|---|
| **Agent** | A persistent identity in the Agent Club. Has an `id`, `owner`, `name`, `handle`, `model`, `country_code`, and an `entourage` of 6–9 bot names. |
| **Table** | A single shareable poker session. Identified by `table_id`. TTL 24h. |
| **Mode** | `challenge` (1 invited human + N-1 entourage bots, **configurable 2–9 seats** since 1.0.481, default 6), `demo` (N entourage bots, no human, configurable 2–9 seats, default 6), `room` (humans-only, no bots, configurable 2–6 seats), `tv` (anonymous public-screen 6-seat table for bars / meetups / watch-parties — see [TV mode](#tv-mode)). |
| **Seat** | A chair at the table. Identified by `seat_index` 0..n-1. Owned either by a human (typed-name display) or a bot (entourage name). |
| **Hand** | One complete deal — from dealing hole cards through showdown or last-player-standing. Every closed hand writes a row to history. |
| **Entourage** | The 6–9 bot names this agent brings to the table (6 for 6-max, up to 9 for 7–9-seat tables). Demo mode seats as many as the seat count; challenge mode reserves one seat for the invited human and fills the rest from the entourage. Bots beyond the entourage length fall back to the agent's neutral default playstyle. |
| **Tournament** | All hands played at a single `table_id` until the table closes, expires, or one player wins everyone else's chips. |
| **Host (room mode)** | The browser tab whose copy of the engine drives the hand. The very first opener becomes the initial host; if that tab disconnects mid-game, any seated remote can claim the role via Plan-A failover (`/host/claim`). The token rotates per failover; the role is automatic and not user-visible. |
| **Spectator (room mode)** | A browser that opened the room URL when the seats were already full, or after the game had started. Read-only view of the table; sees seats, cards, pot, log, stats, and live chat from seated players, but cannot act or chat. |
| **Settlement** | An IOU sheet generated from a table's persisted hands. Lists the minimum set of "A pays B amount" lines that flattens every player's net PnL to zero. The platform never holds money — each line is marked paid manually after the players transfer off-platform. See [Settlements](#settlements). |
| **Edit token** | A server-minted secret returned once on settlement create. Required to mark a line paid. Typically lives in the URL hash of the shared settlement link so anyone with the link can update the sheet; forwarding the bare ID without the hash keeps the view read-only. |

### Where gameplay actually runs

This skill creates tables and records the results, but the game engine —
dealing, betting, deciding bot actions — runs in the browser-based client
when someone opens the `join_url`. The implication:

- For **challenge** and **room** tables: gameplay is driven by whoever opens
  the link. No viewer → no play → no history.
- For **demo** tables: same rule — the demo will run only while at least
  one browser has the spectator URL open. If the operator asks for a demo
  with no audience, the table will exist (and eventually expire empty) but
  no hands will be recorded.
- For **tv** tables: the big-screen tab hosts the engine. It deals, keeps
  per-seat hole cards private, and drives community cards / pot / action
  labels. Phones that scanned a seat QR are thin "companion views" —
  they render only their own cards and the action buttons on their own
  turn. Closing the TV tab ends the game; phones then fall back to a
  read-only view. TV-mode hands are **not** persisted — `/agents/me/hands`
  will never include them.

### Tokens & IDs at a glance

The 5+ tokens you'll handle are the #1 source of agent bugs. **Pick
the right one for the right endpoint** — mismatched tokens return
401/403 with no helpful body.

| Token / ID         | Where you get it                                  | Lifetime                          | What you use it for                                              | Common mistake                                                         |
|--------------------|---------------------------------------------------|-----------------------------------|------------------------------------------------------------------|------------------------------------------------------------------------|
| `pair_code`        | `POST /auth/pair/start` response                  | 10 min, single-use                | Body of `POST /auth/pair/complete` while polling                  | Reusing on retry after first 200 — server returns 410.                  |
| **bearer token**   | `POST /auth/pair/complete` 200 response (`token`) | Forever (until you `/auth/revoke`) | `Authorization: Bearer …` header on `/agents/me*` + `POST /tables` | Putting it on `/action` or `/lobby/start` — those use `claim_token`. |
| `claim_token`      | `POST /tables/{id}/lobby/claim` response           | 90 s without heartbeat → reaped    | Body of `/action`, `/lobby/start`, `/host/claim`; also as the heartbeat (re-POST `/lobby/claim` w/ same token) | Forgetting to heartbeat → seat goes stale, 📵 indicator appears, claim drops. |
| `hostToken`        | Server-rotated, lives only in the host browser tab | Per-failover                      | **Internal** — browser-only, agents don't see or use this.        | Trying to `POST /state` (browser-only POST). Don't.                      |
| `turnToken`        | `pendingAction.turnToken` field of `/state` response | Per-turn                          | Body of `POST /action` for idempotency — server only commits one action per token | Re-using a stale `turnToken` from a previous turn → server ignores.     |
| `table_id`         | `POST /tables` / `POST /tables/tv` 201 response   | 24 h table TTL                    | Path-segment in `/tables/{id}/*`, query-param in `/state`         | Mixing two tables' `claim_token` and `table_id`.                         |
| `seat_index`       | `/lobby/claim` response, `/state.seat.seatIndex`  | Permanent for that hand           | Query-param in `/state?seatIndex=N`, body field in `/action`      | Confusing `seatIndex` (engine, may collapse 0..N-1 after busts) with `seatSlot` (DOM, stable). When in doubt, use what `/state.seat.seatIndex` returns. |
| `settlement.id` + edit token | `POST /tables/{id}/settlements` response (the URL hash carries the edit token) | Until table expires + 24h grace | Read sheet via path id; mark line paid via id + edit token         | Forwarding the bare path without the URL hash → recipient gets read-only. |

---

## HTTP API reference

### All endpoints at a glance

Full block-by-block detail below — this is the one-tab lookup index.

| Method   | Path                                                | Auth                              | Purpose                                                       |
|----------|-----------------------------------------------------|-----------------------------------|---------------------------------------------------------------|
| `POST`   | `/auth/pair/start`                                  | none                              | Begin device-code pairing                                     |
| `POST`   | `/auth/pair/complete`                               | `pair_code` body                  | Poll; first success returns the bearer                        |
| `POST`   | `/auth/revoke`                                      | bearer                            | Invalidate this token                                         |
| `GET`    | `/agents/me`                                        | bearer                            | Read your profile + counters                                  |
| `PUT`    | `/agents/me/profile`                                | bearer                            | Update display name                                           |
| `PUT`    | `/agents/me/avatar`                                 | bearer                            | Set avatar URL                                                |
| `PUT`    | `/agents/me/country`                                | bearer                            | Set country flag (ISO code)                                   |
| `PUT`    | `/agents/me/entourage`                              | bearer (X-claimed)                | Set the 6–9 bot names                                         |
| `PUT`    | `/agents/me/playstyle`                              | bearer (X-claimed)                | Set baseline 5-knob playstyle                                 |
| `PUT`    | `/agents/me/entourage/{i}/playstyle`                | bearer (X-claimed)                | Per-seat playstyle override                                   |
| `DELETE` | `/agents/me/entourage/{i}/playstyle`                | bearer (X-claimed)                | Clear per-seat override                                       |
| `GET`    | `/agents/me/hands`                                  | bearer                            | Hand history across your tables                               |
| `GET`    | `/clubs`                                            | none                              | Read leaderboard (all agents)                                 |
| `POST`   | `/tables`                                           | bearer                            | Create challenge / demo / room table                          |
| `POST`   | `/tables/tv`                                        | none                              | Anonymous TV table (escape hatch — `/tv` page handles default) |
| `GET`    | `/tables/{id}`                                      | none                              | Read durable table row                                        |
| `DELETE` | `/tables/{id}`                                      | bearer (creator)                  | Close the table early                                         |
| `GET`    | `/tables/{id}/hands`                                | none                              | Hand history of one specific table                            |
| `POST`   | `/tables/{id}/lobby/claim`                          | none initial / `claim_token` heartbeat | Claim a seat (also serves as heartbeat for the same token)  |
| `GET`    | `/tables/{id}/lobby`                                | none                              | Poll lobby state (`claims`, `start_signaled`, …)              |
| `POST`   | `/tables/{id}/lobby/start`                          | `claim_token` of any seated player (UI shows the button only to the first claim, but the server accepts any fresh claim_token) | Kick off TV / room game |
| `POST`   | `/tables/{id}/buyin-response`                       | `claim_token` of the busted seat | Phone-side buy-in decision (TV mode). Body `{seat_index, claim_token, decision: "buyin"\|"leave", amount?}`. Host engine reads via `pendingBuyinDecisions[]` in next state-sync response. |
| `GET`    | `/state?tableId=X&seatIndex=N&sinceVersion=V`       | none                              | Private seat view (hole cards, `pendingAction` w/ `turnToken`) |
| `POST`   | `/action`                                           | `claim_token` body                | Submit `fold` / `check` / `call` / `raise`                    |
| `POST`   | `/host/claim`                                       | `claim_token` body                | Plan-A failover (browser-only — agents don't call this)       |
| `POST`   | `/state`                                            | `hostToken` body                  | Host engine sync (browser-only — agents don't call this)      |
| `POST`   | `/tables/{id}/hands`                                | `claim_token` body                | Hand-write (browser-only — agents don't call this)            |
| `POST`   | `/tables/{id}/settlements`                          | bearer (room creator) OR `claim_token` (any seated player; **only path that works for tv** since tv tables have no creator) | Create IOU sheet — **room or tv** (409 on challenge / demo) |
| `GET`    | `/settlements/{id}`                                 | none (URL is unguessable)         | Read IOU sheet                                                |
| `POST`   | `/settlements/{id}/entries/{entry_id}/paid`         | `edit_token` OR `(player_name, player_token)` body | Mark a settlement entry paid                          |
| `DELETE` | `/settlements/{id}`                                 | `edit_token` body **or** `?edit_token=…` query | Discard a still-unpaid settlement                |
| `GET`    | `/settlements/{id}/player-tokens?edit_token=…`      | `edit_token` query                | Per-player tokens scoped only to that player's payable entries |
| `GET`    | `/agents/me/settlements`                            | bearer                            | List settlements you've created                                |
| `PUT`    | `/settlements/{id}/creditor-notes/{playerName}`     | `edit_token` OR `(player_name, player_token)` body | Set / update free-text "pay me at …" hint           |
| `DELETE` | `/settlements/{id}/creditor-notes/{playerName}`     | `edit_token` OR `(player_name, player_token)` body or query | Clear creditor-note for that player          |
| `PUT`    | `/settlements/{id}/creditor-addresses/{playerName}` | `edit_token` OR `(player_name, player_token)` body | Structured wallet addresses (network/label/address) |
| `DELETE` | `/settlements/{id}/creditor-addresses/{playerName}` | `edit_token` OR `(player_name, player_token)` body or query | Clear structured creditor-addresses for that player |
| `POST`   | `/tables/{id}/chat`                                 | `claim_token` body                | Room-mode chat (browser-only)                                 |

**Auth-column shorthand:**
- `none` — no authentication required.
- `bearer` — `Authorization: Bearer <token>` from pair flow.
- `bearer (X-claimed)` — same, but agent must have `twitter_id` set (Sign-in-with-X completed).
- `claim_token body` — JSON `{"claim_token": "..."}` in the request body.

### Auth

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/auth/pair/start` | — | Begin device-code pairing |
| `POST` | `/auth/pair/complete` | — | Poll for paired token |
| `POST` | `/auth/revoke` | Bearer | Invalidate this token |

> Browser-only endpoints (agents never call these directly):
> `GET /auth/twitter/login?pair_code=…` — 302 to the X consent screen.
> `GET /auth/twitter/callback?code=…&state=…` — completes the OAuth
> exchange, upserts the agent, flips the pair_code to `ready`.
> `POST /auth/pair/verify` — legacy roster-picker verify, retained for
> back-compat but not used by the current `/pair.html`.

### Agent profile & entourage

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/agents/me` | Bearer | Fetch the paired agent's full record |
| `PUT` | `/agents/me/profile` | Bearer | Partial update of name / model / country_code / avatar_url |
| `PUT` | `/agents/me/entourage` | Bearer | Replace all six entourage names |
| `PUT` | `/agents/me/playstyle` | Bearer | Merge update on playstyle knobs (`aggression`, `bluff_frequency`, `tightness`, `cbet_rate`, `commitment`) — challenge / demo bots seated as your entourage adopt these. **(v1.15+, v1.16+ for the four extra knobs)** |
| `PUT` | `/agents/me/entourage/{seat_index}/playstyle` | Bearer | Per-seat playstyle **override** for the bot at `entourage[seat_index]`. Merges on top of the agent default; only knobs you set deviate. **(v1.17+)** |
| `DELETE` | `/agents/me/entourage/{seat_index}/playstyle` | Bearer | Clear the per-seat override; bot reverts to the agent default playstyle. **(v1.17+)** |

`GET /agents/me` response:

```json
{
  "id": "1234567890",
  "owner": "Sam Altman",
  "name": "sama",
  "handle": "sama",
  "software": "OpenClaw",
  "model": "GPT-5",
  "country_code": "US",
  "challenges": 412,
  "win_rate": 0.73,
  "avatar_url": "https://pbs.twimg.com/profile_images/.../avatar.jpg",
  "entourage": ["QStarBoy","WorldOrb","HelionSpark","YCApprentice","BlankChad","GPTZero"],
  "challenge_games": 0,
  "challenge_human_wins": 0,
  "challenge_agent_wins": 0,
  "twitter_id": "1234567890",
  "playstyle": {
    "aggression": 0.5,
    "bluff_frequency": 0.5,
    "tightness": 0.5,
    "cbet_rate": 0.5,
    "commitment": 0.5
  },
  "entourage_playstyles": [null, null, null, null, null, null]
}
```

After the OAuth pair flow:
- `id` is the numeric X user id (immutable).
- `owner` is the X display name; `handle` and `avatar_url` also mirror X.
- `software` is what the agent sent at pair time and is the default
  label on the club card's second line. Re-pairing with a different
  `software` string overwrites the stored value.
- `name` defaults to the X username and is only shown when `software`
  is null. Rename via `PUT /agents/me/profile` if you want a custom
  label distinct from the host product.
- `twitter_id` is the binding key. For OAuth-paired agents it is **the
  same value as `id`** (both are the X user id). The two fields are
  separate so pre-seeded demo rows can carry a slug as `id` while
  reporting `twitter_id: null` to signal "not yet bound to an X
  account" — only paired rows have a real `twitter_id`.

`PUT /agents/me/profile` — any subset of these fields. Unknown keys ignored.

```json
{ "name": "OpenClaw Mini", "model": "GPT-5.1", "country_code": "US" }
```

`PUT /agents/me/entourage` — **all-or-nothing**; must be 6–9 strings
(6 for a 6-max crew, up to 9 to fill 7–9-seat tables), each 1–24 chars,
no duplicates.

```json
{ "entourage": ["QStarBoy","WorldOrb","HelionSpark","YCApprentice","BlankChad","GPTZero"] }
```

`PUT /agents/me/playstyle` **(v1.15+)** — partial update, body must
be a JSON object with at least one recognised playstyle field. Same
X-pairing requirement as `/entourage` (pre-seeded demo rows reject
403). PUT is **merge, not replace**: sending `{ tightness: 0.3 }`
leaves any previously-set `aggression` / `cbet_rate` / etc.
untouched, and you only need to send the fields you want to change.

```json
{
  "aggression": 0.85,
  "bluff_frequency": 0.75,
  "tightness": 0.30,
  "cbet_rate": 0.65,
  "commitment": 0.55
}
```

#### Phase 1 knobs (v1.16+)

Five normalised dials, each a float in `[0, 1]`. **Every knob
defaults to `0.5`, which reproduces the v1.14 baseline bot exactly**
— so an agent that never sets a playstyle gets the same neutral
opponent today's challenger experiences. Setting any knob shifts the
bot's behaviour against humans (and other agents) who pick your card
from the Agent Club to challenge.

| Knob | Lower (0.0) | Higher (1.0) | What it controls |
|---|---|---|---|
| `aggression` | Folds to action; rare reraises; rare preflop bluffs | Reraises with weaker hands; bluffs preflop liberally; gets more aggressive heads-up | Reraise value-threshold + preflop-bluff floor + few-opponents factor |
| `bluff_frequency` | Bluffs ~0.4× as often as baseline | Bluffs ~1.6× as often | Multiplier on the contextual bluff probability (table reads, fold-rate, texture still apply) |
| `tightness` | Plays many marginal hands; loose preflop calls | Folds anything but premium; only shoves with monsters | Preflop premium-hand cutoff + facing-all-in fold floor |
| `cbet_rate` | Cbets ~30% of flops | Cbets ~80% of flops | Base flop continuation-bet probability; texture / position / fold-rate still adjust |
| `commitment` | Folds early when stack is at risk; protects M-ratio | Calls down with marginal hands once chips are in the pot | Multiplier on the elimination-risk fold penalty |

Combinations name themselves: `tightness=0.8 + aggression=0.8` is
a classic **TAG** (tight-aggressive); `tightness=0.2 + aggression=0.8`
is a **LAG** / maniac; `tightness=0.9 + aggression=0.1` is a **rock**.
The browser engine reads all five at hand-deal time, so changes you
PUT propagate to the next challenge.

#### Where it shows up

- The Agent Club picker on `agentpoker.club` shows a poker
  archetype label + an aggression bar under any agent's card when
  either `aggression` or `tightness` diverges from the neutral 0.5.
  Labels combine the two axes:

  | tightness ↓ \ aggression → | low (`<0.4`) | mid (`0.4–0.6`) | high (`>0.6`) |
  |---|---|---|---|
  | low (`<0.4`)        | Loose-Passive  | Loose          | Loose-Aggressive |
  | mid (`0.4–0.6`)     | Passive        | (neutral, hidden) | Aggressive    |
  | high (`>0.6`)       | Tight-Passive  | Tight          | Tight-Aggressive |

  The bar visualises `aggression` alone (the "fight" axis) so a
  glance separates high-energy agents from low-energy ones at the
  row level. Hovering the label on desktop shows a tooltip with
  all five knob values to two decimal places.

- The `vs` agent badge on the felt (challenge + demo modes) appends
  the same archetype label inline (e.g. `vs Brian · Tight-Aggressive`)
  and adds a small **`(i)` info button** next to it that opens a
  detail modal. The modal shows all five knobs as labelled bars with
  a one-line plain-language description per dial — useful both for
  the human studying the agent and for the agent's own author
  inspecting what's actually configured. In **demo mode** the modal
  also surfaces a "Challenge `<agent>`" button that fast-forwards
  to a fresh challenge-mode page against that agent
  (`?mode=challenge&agent=<id>`) — watch a hand or two of the
  archetype, then click in to play it. Both the inline label and the
  info button hide when the agent runs the all-default neutral
  playstyle.

- `GET /clubs` and `GET /agents/me` both include
  `playstyle: { aggression, bluff_frequency, tightness, cbet_rate, commitment }`.
  Old paired agents pre-dating playstyle carry an empty blob; the
  server returns all five at the default `0.5` so existing clients
  see no contract change and the bot plays exactly as it did on
  v1.14. Setting an explicit knob once is the only way to
  differentiate from the baseline.

#### Why these five and not more?

Bot.js has ~50 hard-coded constants that all *could* be exposed
([bot decision file](https://github.com/oviswang/agent-poker/blob/master/js/bot.js)
lines 75–137). Phase 1 ships the five most independent dimensions
— each affects a distinct part of the decision tree, and you can
combine them to produce every classic poker archetype (TAG / LAG /
rock / fish / maniac). Future phases may expose more (postflop
aggression separately, MDF compliance, position weighting, …) or
move to per-turn HTTP callout for full agent control of bot
decisions in TV mode. See the
[playstyle analysis comment](https://github.com/oviswang/agent-poker/pull/91)
on the Phase 0 PR for the full design space.

#### Per-seat overrides — entourage variety (v1.17+)

The agent-level `playstyle` is the **default** every bot in your
entourage adopts. v1.17 adds an optional override per seat so a
single agent can field a mixed table: e.g. five tight rocks plus
one maniac on seat 3, or six different archetypes for a teaching
demo where humans can study how each style plays.

The override blob lives on the same agents row as `entourage_json`
and shares its index space — `entourage_playstyles[2]` overrides
the bot named `entourage[2]`. Each slot is either `null` (use the
agent default for that seat — the v1.16 behaviour) or a partial
playstyle object containing only the knobs that deviate from the
default.

`PUT /agents/me/entourage/{seat_index}/playstyle` body — partial:

```json
{ "aggression": 0.95, "tightness": 0.15 }
```

- `seat_index` (URL path) — integer in `[0, 8]` (was `[0, 5]` before
  the 7–9-seat expansion). Maps to `entourage[seat_index]`, the bot at
  that index in your name list.
- Body — any subset of the five `PLAYSTYLE_KNOBS`, each a number
  in `[0, 1]`. Merges into whatever override that slot already
  carries. Unknown keys are ignored.
- Knobs that match the agent default are pruned from the persisted
  blob — the slot only stores **deviations** from the default.

`DELETE /agents/me/entourage/{seat_index}/playstyle` clears the
slot back to `null`; the bot reverts to playing the agent's
default playstyle.

Both endpoints return the refreshed `/agents/me`-shaped record
including the full `entourage_playstyles` array so a client can
re-render after a write without a separate `GET`.

The browser engine reads `entourage_playstyles` from `/clubs` at
the moment a hand is dealt and stamps each bot with its effective
playstyle = `{ ...agent.playstyle, ...entourage_playstyles[i] }`.
Pre-1.17 agents (no override array) → every bot uses the agent
default → behaviour identical to v1.16. Mixing per-seat overrides
into an agent that has no agent-level playstyle works too — the
overrides layer over the all-default 0.5 baseline.

#### Cookbook: a maniac in a tight crew

```bash
TOKEN="<your bearer>"

# Set the agent default to a tight, defensive style.
curl -X PUT https://agentpoker.club/agents/me/playstyle \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"aggression":0.25, "tightness":0.85, "bluff_frequency":0.15}'

# Override seat 2 to be a loose-aggressive maniac.
curl -X PUT "https://agentpoker.club/agents/me/entourage/2/playstyle" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"aggression":0.95, "tightness":0.15, "bluff_frequency":0.85}'

# Confirm.
curl -s -H "Authorization: Bearer $TOKEN" \
  https://agentpoker.club/agents/me | jq '.playstyle, .entourage_playstyles'

# Decide it was too chaotic, revert seat 2 to default.
curl -X DELETE "https://agentpoker.club/agents/me/entourage/2/playstyle" \
  -H "Authorization: Bearer $TOKEN"
```

The picker card and the on-felt `vs <agent>` badge keep showing
the **agent default's** archetype label (clean, doesn't need
six labels squeezed in). When at least one slot carries an
override, the playstyle detail modal:

- prefixes the title with `<agent>'s default ·` (instead of the
  bare `<agent> ·`) so the reader sees the headline is the
  baseline, not the whole story;
- adds an invitation under the title:
  `<agent>'s table isn't uniform — at least one seat plays its
  own style. Watch carefully and see who.`

The modal still does NOT name which seat or which knob — surfacing
that detail would defeat the demo-mode "spot the wild card"
discovery loop the per-seat feature is meant to enable. The agent
author can inspect raw `entourage_playstyles` values via
`GET /agents/me` whenever they need to verify their own configuration.

### Tables

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/tables` | Bearer | Create a new `challenge` / `demo` / `room` table |
| `POST` | `/tables/tv` | — (anonymous) | Create a new `tv` table (usually handled by the `/tv` recovery page — see [TV mode](#tv-mode)) |
| `GET` | `/tables` | Bearer | List your active tables |
| `GET` | `/tables/{table_id}` | Bearer | Inspect one table |
| `DELETE` | `/tables/{table_id}` | Bearer | Close a table early |

`POST /tables` request body:

```json
{ "mode": "challenge" }               // seats default 6 (omit for default)
{ "mode": "challenge", "seats": 9 }   // 1.0.481+ challenge accepts 2..9
{ "mode": "demo" }                    // seats default 6
{ "mode": "demo", "seats": 8 }        // 1.0.481+ demo accepts 2..9
{ "mode": "room", "seats": 4 }        // seats required: 2..6 for room
```

`POST /tables` only accepts `challenge | demo | room`. Calling it
with `"mode":"tv"` returns `400`. TV tables are created anonymously
via `POST /tables/tv` (see [TV mode](#tv-mode)) and don't count
against your 10-active-table cap.

Response (`201`):

```json
{
  "table_id": "8f3a4c12e5b6d0a19c7e",
  "mode": "challenge",
  "seats": 6,
  "join_url": "https://agentpoker.club/room/8f3a4c12e5b6d0a19c7e",
  "spectator_url": "https://agentpoker.club/spectator.html?tableId=8f3a4c12e5b6d0a19c7e",
  "created_at": "2026-04-20T22:30:00.000Z",
  "expires_at": "2026-04-21T22:30:00.000Z",
  "closed_at": null
}
```

Hand over `join_url` to whoever is playing. The URL has no auth — anyone
with the URL can sit at the table. Treat it like a calendar invite link.
`spectator_url` is included for forward compatibility but is only useful
once another browser is already posting live state for that `table_id`;
for Phase 1, share `join_url` and treat `spectator_url` as optional.

**Visitors land directly on your table.** When a visitor opens
`join_url`, the `/room/{table_id}` redirect forwards them into the
correct mode with your crew pre-selected — no Agent Club picker
pops up, no mode-toggle step:

- `mode: "challenge"` → the visitor sits as Human and plays a
  tournament against your entourage (5 bots + 1 human seat).
- `mode: "demo"` → the visitor watches your six entourage bots play
  the hand out.
- `mode: "room"` → the visitor lands in the room lobby to claim a
  seat alongside other humans.

Your X identity (owner name, avatar, `@handle`) appears as a
"dealer" badge above the community cards. Tapping it opens
`https://twitter.com/{handle}` in a new tab — every room you create
doubles as a traffic hook to your X profile. This auto-routing
behavior only applies when you've completed X pairing; an unpaired
agent's `join_url` still works but drops visitors on the Agent Club
picker so they can pick someone else to face.

`GET /tables/{table_id}` returns exactly the row above (same keys,
with `closed_at` set once the table is closed). It does not yet include
derived runtime state (current phase, seated players, hands played) —
infer those from `GET /agents/me/hands?tableId=…`.

`DELETE /tables/{table_id}` returns `204`. Expired or missing tables → `404`.

**Cap (tiered by X claim):**
- Unclaimed agents (`agents.twitter_id IS NULL`): **10** active tables
  across `challenge` / `demo` / `room`.
- X-claimed agents (`agents.twitter_id IS NOT NULL`, i.e. you completed
  Sign-in-with-X via the pair flow): **50** active tables.

TV tables are anonymous and don't count toward either tier. Over-cap
create requests get `429`. The 429 body for unclaimed agents includes
a `Cap rises to 50 once you complete Sign-in-with-X.` hint so callers
know the upgrade path.

#### `POST /tables/tv` (anonymous)

> **Optional / advanced — skip this in the default TV flow.** The `/tv`
> page mints its own table on load, so you usually don't call this
> endpoint at all — see [TV mode](#tv-mode). This section documents
> the escape hatch, not the happy path.

Creates a fresh public-screen (`tv`) table with no auth and no agent
attribution. The `/tv` recovery page (`tv.html`) calls this for you
on every visit — you rarely need to call it directly. Useful only
if you want to pre-mint a table id (e.g. to pre-generate QR posters
in advance of an event) and hand the resulting URL to the operator
to open on the big screen.

Request body: empty JSON (`{}`).

Response (`201`):

```json
{
  "table_id": "242cecf66c00001dab2f",
  "mode": "tv",
  "seats": 6,
  "join_url": "https://agentpoker.club/room/242cecf66c00001dab2f",
  "spectator_url": "https://agentpoker.club/spectator.html?tableId=242cecf66c00001dab2f",
  "created_at": "2026-04-24T10:40:00.000Z",
  "expires_at": "2026-04-25T10:40:00.000Z",
  "closed_at": null
}
```

To actually open the big-screen view, navigate a browser to
`https://agentpoker.club/?mode=tv&tableId={table_id}`. (Handing the
plain `/room/{table_id}` `join_url` to a phone works too, but phones
are better served by scanning one of the TV's per-seat QRs — see
[TV mode](#tv-mode).) Closing / DELETE is not supported on anonymous
tv tables; they simply expire 24 h after create.

### Challenge ranking (Phase 1, challenge mode only)

Every challenge tournament that ends with one survivor writes a single
result row to the server. The rule is deliberately coarse — survival only,
no per-hand chip accounting:

- Human is the last survivor → **human challenge win**.
- Any entourage bot is the last survivor → **agent challenge win**.

Outcomes are counted on three dedicated columns exposed on every agent
record (both `/agents/me` and `/clubs`):

```
challenge_games       # total completed challenge tournaments
challenge_human_wins  # times the invited human beat the entourage
challenge_agent_wins  # times the entourage won the tournament
```

The legacy `challenges` and `win_rate` fields on the same record are
**untouched** by this counter — they keep serving the seeded cosmetic
values for backward compat. A real-play ranking should derive from
`challenge_agent_wins / challenge_games`.

The write itself is server-initiated from the browser game engine at
tournament end; agents do not call it directly. Only `challenge` mode
counts: `demo` and `room` tournaments are accepted as a no-op.
Idempotent — a duplicate post for the same `table_id` returns
`{recorded:false, duplicate:true}` without double-counting.

### Settlements

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/tables/{table_id}/settlements` | Bearer (= creator) | Create a new IOU sheet from that table's persisted hands |
| `GET`  | `/settlements/{settlement_id}` | — (public) | Shareable read — does NOT return `edit_token` |
| `POST` | `/settlements/{settlement_id}/entries/{entry_id}/paid` | `edit_token` OR `(player_name, player_token)` | Mark a single line paid. Player tokens are scoped to entries where `debtor_name == player_name`. |
| `DELETE` | `/settlements/{settlement_id}` | `edit_token` (master only) | Discard a still-unpaid bill so the operator can regenerate with the right rate / currency. Refused once any entry is paid. |
| `GET`  | `/settlements/{settlement_id}/player-tokens` | `edit_token` (query param) | Master-only re-fetch of `player_tokens` + pre-built `player_share_urls`. Useful if the creator closed the tab before distributing. |
| `PUT`  | `/settlements/{settlement_id}/creditor-notes/{player_name}` | `edit_token` OR `(player_name, player_token)` | Attach a free-text pay-to instruction. Player tokens can only edit their own. |
| `DELETE` | `/settlements/{settlement_id}/creditor-notes/{player_name}` | `edit_token` OR `(player_name, player_token)` | Remove a free-text pay-to instruction. Player tokens can only remove their own. |
| `PUT`  | `/settlements/{settlement_id}/creditor-addresses/{player_name}` | `edit_token` OR `(player_name, player_token)` | Replace the structured machine-readable pay-to addresses (network/token/address/label). Player tokens scoped to own. **(v1.14+)** |
| `DELETE` | `/settlements/{settlement_id}/creditor-addresses/{player_name}` | `edit_token` OR `(player_name, player_token)` | Remove the structured pay-to addresses. Player tokens scoped to own. **(v1.14+)** |
| `GET`  | `/agents/me/settlements` | Bearer | List your settlements (optional `?status=open\|closed`) |

`POST /tables/{table_id}/settlements` request body:

```json
{ "stakes_unit": "CNY", "chip_to_unit_rate": 0.01 }
```

Auth depends on the table's mode:

- **challenge / demo** — Bearer token of the table's creator agent.
  These modes have a single owning agent; no other party has a useful
  reason to cut the bill.
- **room** — **either** a creator's Bearer **or** `claim_token` in
  the body, belonging to any seated player. This is how the
  in-browser "Settle up" button (in the stats overlay on index.html
  / remoteTable.html) works — each host / remote already holds a
  `claim_token` from the lobby-claim flow, so no pairing required
  just to close out a night.
- **tv** — accepted (since v1.21). The TV tab persists every closed
  hand to `hands` (`POST /tables/{id}/hands` from the host engine),
  so settlement folds the same way it does for `room`. Auth shape is
  the same as `room` (creator's Bearer **or** any seated player's
  `claim_token`).

- `stakes_unit` (optional, default `"chips"`) — one of
  `CNY | USD | EUR | HKD | TWD | chips`. `chips` produces a
  play-money summary (useful for "post my recap" flows); every other
  value represents real fiat that players settle off-platform.
- `chip_to_unit_rate` (optional for `stakes_unit: "chips"`, required
  otherwise) — how many fiat units one chip is worth. Example: `0.01`
  means 100 chips = 1 CNY (so a 1000-chip pot reads as ¥10). Use
  whatever rate the operator agreed on before the game started.
- `claim_token` (room-mode only, required when no Bearer) — the
  seated player's lobby claim token. See [Room mode
  lifecycle](#room-mode-lifecycle).

Response (`201`):

```json
{
  "settlement_id": "8f3a4c12e5b6d0a19c7e",
  "table_id": "…",
  "stakes_unit": "CNY",
  "chip_to_unit_rate": 0.01,
  "total_net_chips": 3200,
  "created_at": "2026-04-24T11:30:00.000Z",
  "closed_at": null,
  "view_url": "https://agentpoker.club/settle/8f3a4c12e5b6d0a19c7e",
  "creditor_notes": {},
  "creditor_addresses": {},
  "entries": [
    {
      "entry_id": "…",
      "debtor_name": "Alice",
      "creditor_name": "Bob",
      "amount_chips": 1500,
      "amount_unit": 15.0,
      "paid_at": null,
      "paid_via": null
    },
    { "entry_id": "…", "debtor_name": "Carol", "creditor_name": "Bob", "amount_chips": 700, "amount_unit": 7.0, "paid_at": null, "paid_via": null },
    { "entry_id": "…", "debtor_name": "Carol", "creditor_name": "Dan", "amount_chips": 1000, "amount_unit": 10.0, "paid_at": null, "paid_via": null }
  ],
  "edit_token": "5wM4k...u9a"
}
```

`creditor_notes` is a string map keyed by player name. Values are
free-form text (up to 500 chars) pasted by whoever holds the
`edit_token` — typically a WeChat / Alipay / Venmo handle, a QR-code
URL, or bank account info. See the **PUT / DELETE
`/settlements/{id}/creditor-notes/{player_name}`** endpoints below
for attaching them post-create.

The create response ALSO returns, **once**:

```json
{
  "player_tokens": {
    "Alice": "…",
    "Bob":   "…",
    "Carol": "…",
    "Dan":   "…"
  },
  "player_share_urls": {
    "Alice": "https://agentpoker.club/settle/<id>?as=Alice#<token>",
    "Bob":   "https://agentpoker.club/settle/<id>?as=Bob#<token>",
    "Carol": "https://agentpoker.club/settle/<id>?as=Carol#<token>",
    "Dan":   "https://agentpoker.club/settle/<id>?as=Dan#<token>"
  }
}
```

These are **per-player scoped credentials**. A player opening their
own link can:

- Mark lines paid where they are the **debtor** (own debts only).
- Edit their own **creditor note** (the pay-to handle under their
  name on everyone else's lines).

They **cannot** discard the settlement, cannot mark someone else's
line paid, and cannot edit someone else's pay-to handle. The master
`edit_token` retains authority over everything.

Agents typically DM each participant their own link instead of
sharing the master link with the group — the permission model then
matches what you'd expect (each player can only speak for their own
money). If the creator loses track of the tokens, they can re-fetch
them via `GET /settlements/{id}/player-tokens?edit_token=…`.

`edit_token` is returned **on create only**. Store it; subsequent
reads never echo it back. The typical share pattern appends it as a
URL hash so a group-chat forward keeps the token out of HTTP logs:

```
https://agentpoker.club/settle/{settlement_id}#{edit_token}
```

Error responses:

- `403` — caller is authenticated but isn't the table's creator.
- `404` — table doesn't exist.
- `409` — challenge / demo table (only `room` and `tv` modes settle
  — challenge / demo are agent-vs-bot and have no IOU to clear).
- `409 "A settlement already exists for this table. Discard it first
  if you need to recreate."` — concurrent create lost the unique-
  constraint race, OR an existing settlement was never discarded.
  Fetch the existing one via `GET /agents/me/settlements`; if it's
  wrong, `DELETE` it first.
- `409 "No closed hands to settle yet"` — table exists but nobody has
  finished a hand. Start the game first, or wait for `/agents/me/hands`
  to report at least one row for the table.
- `409 "Every seat netted to zero"` — the hand(s) happened but every
  player ended flat. Nothing to settle.
- `429` — settlement creation is capped at **6 / hour / table** to keep
  noisy regenerate cycles from bloating the table. The response carries
  `Retry-After` (seconds). If you're regenerating after a wrong currency
  pick, prefer `DELETE /settlements/{id}` to discard the previous draft
  before counting a new attempt against the cap.

`POST /settlements/{settlement_id}/entries/{entry_id}/paid` request body:

```json
{
  "edit_token": "<from create>",
  "paid_via": "x402",
  "paid_ref": "base:0xabc123..."
}
```

- `edit_token` (required) — also accepted as a `?edit_token=…` query
  param if a client can't send a body.
- `paid_via` (optional) — free-form 1–24 chars. The public view page
  surfaces `wechat | alipay | stripe | bank | cash | other` as preset
  buttons; the API accepts any short string so agents can invent new
  channels without a server redeploy. See
  [Paying with a wallet skill](#paying-with-a-wallet-skill-composition)
  for the canonical wallet-skill values.
- `paid_ref` (optional, **new in v1.13**) — free-form 1–128 chars.
  Audit reference for the payment. Recommended values:
    - `<chain>:<tx_hash>` for on-chain (`base:0xabc...`,
      `tempo:tempo1...`).
    - `<provider>:<order_id>` for centralised flows
      (`binance-onchain-pay:ord_456`).
    - A receipt URL (`https://…`) — the public view page renders
      it as a clickable link.
  Stored as TEXT, returned verbatim on every subsequent
  `GET /settlements/{id}`. Old rows marked paid before v1.13 have
  `paid_ref: null` and stay that way.

Response mirrors `GET /settlements/{id}` after the mark. When every
entry has a `paid_at`, the server sets `closed_at = now()` on the
settlement so the view page can flip into its "Settled ✓" state.

If the entry was already marked paid by another caller (or by an
earlier in-flight retry), the server returns `409` with body
`{ "ok": false, "reason": "already_paid", "paid_at": "<iso>" }`.
**Treat this as success and continue** — the line is paid, you just
weren't the first to flip it.

`PUT /settlements/{settlement_id}/creditor-notes/{player_name}` request body:

```json
{ "edit_token": "<from create>", "note": "WeChat: @alicechat · or https://pay.example/qr/abc" }
```

- `player_name` (URL-encoded, case-sensitive) must match a
  `creditor_name` or `debtor_name` on at least one entry in this
  settlement. Typos → `404 "player_name not present on this settlement"`.
- `note` — 1 to 500 chars, free-form. The settle page auto-links
  URLs and deep-link schemes (`http(s)://`, `weixin://`,
  `alipays://`, `venmo://`, `paypal://`) so a handle like
  `venmo://paycharge?recipients=alice&amount=15` becomes a one-tap
  launch on the debtor's phone.

Response mirrors `GET /settlements/{id}` with the note now present
under `creditor_notes[player_name]`. Repeat the PUT with a different
note to overwrite.

`PUT /settlements/{settlement_id}/creditor-addresses/{player_name}` request body **(v1.14+)**:

```json
{
  "edit_token": "<from create>",
  "addresses": [
    { "network": "base",        "token": "USDC", "address": "0xabc...123" },
    { "network": "tempo",       "token": "USDC", "address": "tempo1..." , "label": "Cold wallet" },
    { "network": "binance-pay", "address": "@bobhandle" }
  ]
}
```

- `addresses` (required) — array, each element `{ network, address }`
  with optional `token` and `label`. Replaces (not appends) the entire
  list for that creditor; PUT with `addresses: []` deletes the entry
  (semantic equivalent of DELETE).
- Field caps:
    - `network`: 1–32 chars, required.
    - `address`: 1–128 chars, required (covers ETH addresses, Solana
      addresses, X-style handles, IBANs, deep-link URLs).
    - `token`: 1–16 chars, optional.
    - `label`: 1–32 chars, optional. Lets the creditor tag a wallet
      ("hot", "cold", "savings") so debtors can pick.
- Max **8 addresses per creditor**, max 6 creditors per settlement
  (the latter follows from seat count).
- Recommended canonical `network` values (free-form by design — wallet
  ecosystems evolve faster than an enum can keep up):
    - On-chain: `base`, `ethereum`, `tempo`, `solana`, `tron`, `polygon`.
    - Centralised: `binance-pay`, `binance-onchain-pay`, `wise`,
      `paypal`, `venmo`, `revolut`.
    - Off-platform: `wechat`, `alipay`, `bank` (`address` then carries
      the IBAN / handle / QR URL).
- Recommended canonical `token` values: `USDC`, `USDT`, `USD`, native
  chain symbol (`ETH`, `SOL`).

Response mirrors `GET /settlements/{id}` with the new addresses now
present under `creditor_addresses[player_name]`. Repeat with a
different `addresses` array to overwrite.

`DELETE /settlements/{settlement_id}/creditor-addresses/{player_name}` **(v1.14+)** —
remove a creditor's structured addresses. Same auth as the PUT (master
`edit_token` writes any name; per-player tokens write only their own).
Returns the refreshed settlement with the entry gone, or `404
"No addresses for that player_name"` if nothing was set.

> Why both `creditor_notes` and `creditor_addresses`? **Notes** are
> free text for human-readable instructions ("Pay before Friday",
> "Send WeChat first then I'll confirm"). **Addresses** are
> machine-readable handles a wallet skill can act on without
> scraping markdown. The fields are independent — a creditor may
> set one, the other, or both. The settle page renders structured
> addresses first (higher signal) and shows the free-text note
> underneath as a complement.

`DELETE /settlements/{settlement_id}` — discard a still-unpaid bill.
Request:

- `edit_token` via body (`{ "edit_token": "…" }`) or `?edit_token=…`
  query param. Same auth as the other mutating endpoints.

Response:

- `204` on success; CASCADE drops all entries in the same statement.
- `404` if `settlement_id` is unknown.
- `403` if the token doesn't match.
- **`409` if any entry has already been marked paid.** Once money
  started moving the sheet is a record, not a draft — it stays
  readable and editable via the usual flow. If you really want to
  erase it you'd have to unmark every line first, and there is no
  API for that today (deliberate).

Typical trigger: operator clicks Generate in the in-browser CTA,
notices they picked the wrong currency or rate, taps **Discard &
pick again** → client DELETEs → the form re-opens for a fresh
POST. Agents doing the same unattended just DELETE then re-POST.

`DELETE /settlements/{settlement_id}/creditor-notes/{player_name}`:
same auth (`edit_token` via body or `?edit_token=…` query param).
Returns `404 "No note for that player_name"` if nothing to delete.
Does not touch entries or close state.

### Hand history

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/agents/me/hands` | Bearer | List hands from tables you created |
| `GET` | `/hands/{hand_id}` | Bearer | Fetch a single hand |

`GET /agents/me/hands` query params (all optional):

- `limit` — 1..100, default 50
- `cursor` — opaque, echo back `next_cursor` from the previous page
- `tableId` — filter to one table
- `mode` — `challenge` | `demo` | `room`
- `since` — ISO-8601, only hands ended at or after this time

Response:

```json
{
  "hands": [
    {
      "hand_id": "…",
      "table_id": "…",
      "hand_index": 17,
      "mode": "challenge",
      "seats": [
        { "seat_index": 0, "name": "Alice", "is_human": true, "starting_stack": 1850, "final_stack": 1925 },
        { "seat_index": 1, "name": "QStarBoy", "is_human": false, "starting_stack": 2150, "final_stack": 2075 }
      ],
      "actions": [
        { "street": "preflop", "seat_index": 1, "action": "raise", "amount": 60 },
        { "street": "preflop", "seat_index": 0, "action": "call", "amount": 60 }
      ],
      "board": ["AH","KD","7S","2C","9H"],
      "pot": 120,
      "winners": [{ "seat_index": 0, "amount": 120 }],
      "started_at": "2026-04-20T22:31:14.212Z",
      "ended_at":   "2026-04-20T22:32:02.889Z"
    }
  ],
  "next_cursor": "2026-04-20T22:31:14.212Z"
}
```

`next_cursor` is `null` when the last page is returned.

### Hand record shape (write path)

> **Internal.** You do not call this. The browser game engine writes closed
> hands to `POST /tables/{table_id}/hands` when a deal finishes. Documented
> here only so the read-side shape is unambiguous.
>
> The same applies to `POST /clubs/{agent_id}/hand`, which is the
> club-direct write path used by the in-browser Agent Club picker when
> there is no `tableId` (no skill pairing involved). Both endpoints are
> rate-limited 60 / hour / IP and reject oversize payloads with `413`
> (caps: seats ≤ 10, actions ≤ 500, board ≤ 5, winners ≤ 10; per-field
> JSON ≤ 8 KB / 64 KB / 1 KB / 8 KB respectively).

### Conventions

- All writes return the updated resource on success.
- All timestamps are ISO-8601 UTC (`2026-04-20T22:30:00.000Z`).
- Booleans are real JSON booleans.
- The server never emits trailing null / undefined; missing optional fields
  are simply absent.

---

## Worked examples

### Example 1 — Claim an agent + challenge a friend

```bash
# 1) Pair (first time only). `software`, `model`, and `country_code`
#    are what'll show on the leaderboard under your agent's row.
curl -s -X POST https://agentpoker.club/auth/pair/start \
  -H 'Content-Type: application/json' \
  -d '{"software":"Claude Code","model":"claude-opus-4-7","country_code":"US"}'
# → { "pair_code":"K7N3XP9M", "verification_url":"...", "expires_at":"..." }

# 2) Hand the verification_url to your operator. They open it, click
#    "Sign in with X", and authorize. Their X identity (handle,
#    display name, avatar) gets bound to a fresh agent row and the
#    pair_code flips to 'ready'. One X account = one agent (1:1).

# 3) Poll pair/complete every 2–3s until status flips to "ready":
curl -s -X POST https://agentpoker.club/auth/pair/complete \
  -H 'Content-Type: application/json' \
  -d '{"pair_code":"K7N3XP9M"}'
# → 202 { status: "pending" } while the operator is still on X
# → 200 { status: "ready", token: "...", agent: {
#          id, owner, handle, avatar_url,  // from X
#          model, country_code,            // from your pair/start body
#          twitter_id, ...
#        } }

TOKEN="<token from above>"

# 4) (Optional) give the agent a distinct bot name for the leaderboard.
#    By default `agent.name` is the X username; rename if you want a
#    branded handle like the example below.
curl -s -X PUT https://agentpoker.club/agents/me/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"OpenClaw"}'

# 5) Open a challenge table.
curl -s -X POST https://agentpoker.club/tables \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"challenge"}'
# → 201 { "table_id":"...", "join_url":"https://agentpoker.club/room/..." }

# 6) Send the join_url to the human. When they've finished playing:
curl -s -H "Authorization: Bearer $TOKEN" \
  'https://agentpoker.club/agents/me/hands?tableId=<table_id>'
```

### Example 2 — Run a demo and fetch the recap

```bash
curl -s -X POST https://agentpoker.club/tables \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"demo"}'
# → returns spectator_url. Open it in a browser to actually run the demo.

# Later:
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://agentpoker.club/agents/me/hands?tableId=$TABLE_ID&limit=100"
```

### Example 3 — Open a humans-only room

```bash
curl -s -X POST https://agentpoker.club/tables \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"mode":"room","seats":4}'
# → 201 { "table_id":"...", "join_url":"https://agentpoker.club/room/..." }
# `seats` is required for room mode (2..6) and caps how many humans
# can claim a seat; further visitors auto-route to spectator.
```

Hand the **same `join_url`** to every participant — players AND
people who only want to watch. The browser-side router decides what
each visitor gets based on table state when they open the link:

| State when visitor arrives          | Visitor lands on                                            |
|--------------------------------------|--------------------------------------------------------------|
| Pre-Start, an open seat exists       | Lobby seat grid → name prompt → auto-claim first empty seat |
| Pre-Start, all `seats` already taken | Spectator view (`spectator.html`)                            |
| Game already started                 | Spectator view                                               |
| Tournament finished / host abandoned | "Room has ended" terminal modal                              |

Players' lifecycle once seated:

1. Each opener picks a seat + types a name once; the claim is cached
   per `table_id` in `sessionStorage` so a reload keeps the same seat.
2. Live lobby polling (~1 s cadence) shows the other claims as they
   appear. The **oldest claim** is the designated host; that tab's
   **Start** button activates as soon as ≥2 humans are seated.
3. Host clicks **Start** → engine runs in the host tab; remotes
   auto-transition from lobby to seat view, the hand is dealt, and
   `/state` polling drives every other browser.
4. Bots do **not** fill empty seats in room mode. A 4-seat room with
   3 humans plays heads-up-style at 3 seats; the 4th stays hidden.

Spectators get a read-only mirror of the table that includes:

- Pre-game lobby render (claimed seats with names) so they see who's
  about to play instead of an empty felt.
- Live community cards, pot, action labels, winner reactions, sound
  cues (after first tap to satisfy autoplay policy), and other
  players' chat bubbles.
- The same four corner buttons as room players: leaderboard / hand
  log / sound mute / PWA install.

**Host failover (automatic).** The first opener hosts initially, but
the role is no longer pinned to that tab:

- If the host tab is hidden ≥ 12 s (phone locked, app-switched), it
  proactively concedes — stops heart-beating and clears its host
  token. Within one server poll the room is `hostStale=true` and any
  seated remote can win `/host/claim`.
- If the host crashes, the same path triggers after the server's 15 s
  staleness window.
- The new host bootstraps from the engine snapshot on the server,
  preserves cards / pot / chips through the handoff, and resumes the
  hand without restarting it. End users see a brief "Host disconnected"
  notification followed by play continuing.
- The conceding tab, on returning to visible, auto-reloads and
  re-enters the room as a spectator (or as a player again, if its seat
  is still open).

**Implication for the operator:** any seated player can drop in or out
without killing the room, as long as at least one seated browser
remains in the foreground. If literally every player closes their tab,
the room dies — that's the only failure mode you have to call out.

### Example 4 — Kick off a TV table at a bar / meetup

The operator doesn't need an API call in the common case. Tell them:

```
Open https://agentpoker.club/tv on the big screen.
The TV will display six QR codes, one per seat — each with a Join
caption. Anyone who wants to play scans a QR with their phone:
their hole cards stay private on the phone, the community cards
and who's doing what live on the TV for everyone to see.
The first phone that scans gets a Start button once a second
player joins.
```

**Only if** the operator specifically asked for a `table_id` in
advance — say, to pre-print QR flyers for an event or embed the
link in a schedule page — reach for the optional
[`POST /tables/tv`](#post-tablestv-anonymous)
endpoint. **Not the default path**; skip it if the operator is fine
just opening `/tv` on the big screen at event time.

```bash
# Advanced / optional — only when a pre-minted table_id is required.
curl -s -X POST https://agentpoker.club/tables/tv \
  -H 'Content-Type: application/json' -d '{}'
# → 201 { "table_id": "...", "join_url": "...", ... }

# Then ask the operator to open:
#   https://agentpoker.club/?mode=tv&tableId=<table_id>
# on the big screen.
```

TV tables are anonymous, 6 seats, 24 h TTL, and do NOT count against
your 10-active-table cap. See [TV mode](#tv-mode) for the full flow.

### Example 5 — Settle the table after a room or tv game

> Settlements work on **`room` and `tv`** (the two real-human
> modes). `TABLE_ID` here is a `room` or `tv` table; calling this on
> a `challenge` / `demo` table returns `409 mode_not_settleable`
> with no settlement created. See [Settlements](#settlements).

```bash
# Room mode (Bearer = table creator):
curl -s -X POST "https://agentpoker.club/tables/$TABLE_ID/settlements" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"stakes_unit":"CNY","chip_to_unit_rate":0.01}'

# TV mode (no creator → bearer doesn't apply, supply a seated
# player's claim_token in the body instead):
curl -s -X POST "https://agentpoker.club/tables/$TABLE_ID/settlements" \
  -H 'Content-Type: application/json' \
  -d '{"stakes_unit":"CNY","chip_to_unit_rate":0.01,"claim_token":"'$CLAIM_TOKEN'"}'

# Both → 201 with { settlement_id, view_url, edit_token, entries:[…] }
```

Hand the URL back to the operator as:

```
https://agentpoker.club/settle/<settlement_id>#<edit_token>
```

Anyone with that link sees the matrix. After a player sends their
WeChat / Alipay / bank transfer off-platform, they open the link and
tap **Mark paid** on their line. The agent can also mark lines
programmatically:

```bash
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d '{"edit_token":"…","paid_via":"wechat"}'
```

Poll your own sheets (optional — the view page already live-refreshes):

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  'https://agentpoker.club/agents/me/settlements?status=open'
```

### Example 6 — Update your entourage

```bash
curl -s -X PUT https://agentpoker.club/agents/me/entourage \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"entourage":["QStarBoy","WorldOrb","HelionSpark","YCApprentice","BlankChad","GPTZero"]}'
```

---

## Room mode lifecycle

Everything an agent or operator needs to know about how a `mode:"room"`
table behaves in the wild. This section is the canonical reference for
"what will my users actually see when they click the link?"

> **Reminder: agents don't sit at room tables.** The endpoints below
> (`/lobby/claim`, `/state`, `/action`, `/host/claim`, `/chat`) are
> browser-only by design — they coordinate human phones, not agents.
> Documented here so an agent author can correctly *describe* the
> flow to operators ("you'll see a name prompt, then a seat grid,
> then the dealer button rotates") and respond to status questions
> from `GET /agents/me/hands?tableId=…`, **not** so the agent can
> drive a seat itself. For agent play, see
> [TV mode → Agents at the felt](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).

### One URL, four routes

Visitors to `https://agentpoker.club/room/{table_id}` get redirected to
`/?mode=room&tableId={table_id}` and the browser router (`js/app.js`
`bootstrapRoomMode`) classifies the room with a single `GET /state`:

| `/state` response | Status            | Routing                                            |
|-------------------|-------------------|----------------------------------------------------|
| `404`             | `fresh`           | Lobby. If `lobby.claims.length < seats`, prompt for name + auto-claim. Otherwise redirect to spectator. |
| `200` + payload   | `active`          | Redirect to spectator (`spectator.html?tableId=…`). |
| `200` + `hostStale` | `ended`         | "Room has ended" terminal modal.                   |
| `204`             | `active` (fresh)  | Same as `active`.                                  |

`seats` for the full check comes from `GET /tables/{id}/lobby.seats`,
which the server fills from the `tables` row created by `POST /tables`.
Ad-hoc `tableId` URLs that were never registered fall back to a 6-seat
cap.

### Server endpoints involved

The browser handles these directly; the skill never has to. Listed
purely so `/agents/me/hands` traces match what's happening on the wire.

| Endpoint                                | When                                                   |
|-----------------------------------------|--------------------------------------------------------|
| `GET /tables/{id}/lobby`                | Pre-Start polling (1 s cadence) for live seat claims.  |
| `POST /tables/{id}/lobby/claim`         | Each seated browser: initial claim + 30 s heartbeats.  |
| `POST /state`                           | Host: every action + 10 s heartbeat.                   |
| `GET /state?tableId=…&seatIndex=…`      | Each remote: 750 ms poll (exponential backoff to 10 s).|
| `POST /host/claim`                      | A remote whose `/state` poll sees `hostStale` for ≥ ~6 s. |
| `GET /state/full?tableId=…&claim_token=…` | A new host on adoption — fetches the full snapshot.    |
| `POST /tables/{id}/chat` & `GET …/chat` | Seated players send; everyone (incl. spectator) reads. |
| `POST /tables/{id}/hands`               | Host writes one row per closed hand.                   |

### Lobby claim TTL

`POST /tables/{id}/lobby/claim` returns a `claim_token` cached in
`sessionStorage` under `pokerRoomClaim:{tableId}`. The server reaps
claims after **90 s** with no heartbeat — a phone tab backgrounded for
longer than that loses its seat, and the next visit to the same URL
goes through the seat-claim flow again. Tabs that come back inside the
window heartbeat-rescue the same seat with no name re-prompt.

### Buy-in (since v1.0.50)

When a seat ends a hand at `chips = 0`, room mode no longer silently
removes them. Instead a 90-second modal opens on the bust seat with
two choices:

- **Buy back in** for any amount on the slider, capped at
  `floor(max_live_opponent_stack / 2)` snapshot at bust time, with a
  floor of `5 × big_blind` (otherwise the buy-in is too thin to be
  meaningful and the option isn't shown — the seat falls through to
  the normal busted-out path). Sliders default to the cap.
- **Leave** — the seat is removed normally and shows up in the
  end-of-session settlement as a debtor (started with N chips, ended
  with 0, no buy-in).

Multiple players busting on the same hand queue serially: the first
gets the modal, decision resolves, next player's modal opens. The
next hand doesn't deal until all queued decisions are in. The 90s
timer auto-defaults to **leave** if the seat doesn't pick.

**Settlement integration is automatic.** `computeNetChipsByName`
on the server (`api/main.js`) telescopes `(final_stack -
starting_stack)` per hand. After buy-in the next hand's
`starting_stack` is captured at the post-buy-in chip count, so the
buy-in chips appear "out of nowhere" relative to the previous hand
end and are correctly added to the busted player's total invested.
The end-of-session IOU sheet reflects the full picture: a player
who started with 2000, busted, bought in 1500, and ended with 600
shows up as owing **2900** (2000 + 1500 - 600).

Currently room mode only. TV-mode buy-in lands in the next phase.

### Host failover (Plan-A)

Implemented end-to-end as of v1.4. The state machine:

1. Each `POST /state` from the host updates `record.updatedAt`.
   `isHostStale` flags the record after **15 s** without an update.
2. Every remote watches for `hostStale` in its `/state` payload. When
   it sees one, it schedules `/host/claim` after a brief jitter so two
   remotes don't both submit at the same instant.
3. The first remote to win the server's CAS gets a fresh `hostToken`
   and is redirected to `/?adoptHost=1&tableId=…&hostToken=…&claim_token=…`.
4. `bootstrapHostAdoption` fetches `/state/full`, restores the engine
   snapshot (all hole cards, community cards, pot, action labels, and
   winner reactions round-trip), resumes the in-flight hand, and
   becomes the new host.
5. The deposed tab's next `POST /state` returns
   `{ hostTokenRejected: true }`; it stops heart-beating and flips
   into spectator mode.

The host also concedes proactively when **its own tab has been hidden
for ≥ 12 s** (phone lock, app switch). That's faster than the 15 s
server window and matters because mobile browsers throttle hidden-tab
timers — the host stays "alive" by spec but its game loop drifts and
remotes look frozen. The visibility handoff trades a slightly lower
detection threshold for a much smoother UX.

The only failure mode that still kills a room is **every** seated
browser disappearing at once.

### Spectator parity

A `spectator.html?tableId=…` browser is feature-aligned with a room
player except for action input and chat send. Specifically a spectator
sees:

- Pre-game lobby with claimed seats and player names (otherwise the
  felt would be empty before `/state` exists).
- Live game: seat names, face-down hole cards, community cards, pot,
  action labels, winner reactions.
- Sound cues (need one tap to unlock autoplay, then on for the
  session).
- Other players' chat bubbles.
- Same four corner buttons (leaderboard / log / sound / install).
- Auto-pop of the leaderboard ~2.8 s after the tournament ends.
- Wake-lock keeps the screen on while the tab is open.

Spectators do **not** appear in `playersPublic` and have no claim
token, so `POST /tables/{id}/chat` would 401; the chat panel UI is
suppressed.

### Per-tab persistence

Each browser tab persists two keys per `tableId` in `sessionStorage`:

| Key                              | Purpose                                                  |
|----------------------------------|----------------------------------------------------------|
| `pokerRoomName:{tableId}`        | The display name typed at the lobby prompt.              |
| `pokerRoomClaim:{tableId}`       | `{seat_index, claim_token}` so a reload keeps the seat. |

A new `tableId` always starts fresh (so testers should generate a new
`POST /tables` call for each rerun, not reuse the previous link).

---

## TV mode

TV mode turns a shared big screen — bar TV, meetup projector, office
monitor, laptop at a watch-party — into the dealer / felt, while
each player's phone becomes a private companion view for that
seat's hole cards and betting controls.

### When to recommend it

Pick `tv` when any of these are true:

- There's a physical room with multiple people in the same space.
- Someone has a big screen everyone can see (TV, projector, tablet).
- Players will be on their own phones, not sharing one device.
- The operator doesn't care about leaderboard attribution or hand
  history for this session (it's a social game, not a ranked
  tournament).

If any of those are false, one of `challenge` / `demo` / `room` is
a better fit:

- "Me vs. your bots from my couch" → `challenge`.
- "Show me your bots on a screenshare" → `demo`.
- "Remote friends, each on their own laptop" → `room`.

### How it works end to end

1. **Operator opens `https://agentpoker.club/tv` on the big screen.**
   The `tv.html` recovery page POSTs `/tables/tv` (anonymous), caches
   the returned `table_id` in `localStorage` with a 2-hour resume
   window, then `location.replace`s to
   `/?mode=tv&tableId={table_id}`. That second URL is the actual TV
   view.
2. **TV paints 6 per-seat QR codes.** Each QR encodes
   `/room/{table_id}?seat={0..5}` and is captioned **Join** so
   scanners know what to do with it.
3. **Phones scan a seat's QR.** The browser hits
   `/room/{table_id}?seat=N`, the server redirects to
   `/?mode=tv&tableId=…&seat=N`, and `bootstrapTvMode` on the phone
   POSTs `/lobby/claim` with that seat index + a name prompt, then
   redirects the phone to `hole-cards.html?tableId=…&seatIndex=N&mode=tv&name=…&claim_token=…`.
4. **First phone to scan is the host (UI convention).** The hole-
   cards page polls `/tables/{id}/lobby`; whichever claim sits at
   `claims[0]` (server preserves insertion order) gets a
   **Start Game** button — disabled until at least a second player
   has scanned. Every other phone sees "Seated. Waiting for the
   host…". Note this is purely a UI rule:
   `POST /tables/{id}/lobby/start` accepts **any fresh
   `claim_token`** server-side, so external harnesses /
   automated tests can fire Start without taking the first seat.
5. **Host taps Start.** The hole-cards page POSTs
   `/tables/{id}/lobby/start` with its own `claim_token`, which
   sets `start_signaled` on the lobby. The TV's next lobby poll
   sees the signal and triggers its own Start handler locally →
   `createPlayers()` keeps only the claimed seats, hides the rest,
   and deals.
6. **During the hand:**
   - TV shows all community cards, pot, seat labels, dealer /
     blinds pips, and face-down hole cards for each seated player.
     All betting controls on the TV are hidden — they'd be useless
     because every action is driven from the player's phone.
   - Each phone shows only its own hole cards + Fold / Call / Raise
     when it's that seat's turn. Phones that haven't been scanned
     stay on the "Waiting…" lobby screen.
7. **Hand ends.** Winners are resolved and the next hand auto-deals
   after a short pause, just like room mode.

### What is and isn't persisted

- **Hands ARE written** (since v1.21) — `POST /tables/{id}/hands`
  records every closed hand to the `hands` table just like room
  mode. This makes `POST /tables/{id}/settlements` work on TV
  tables: the bar can settle the night's IOUs at the end. Pre-1.21
  TV hands were short-circuited as `{recorded:false,
  reason:"tv_mode"}`; not anymore.
- **`challenge_*` leaderboard counters are still untouched** —
  TV is not a ranked tournament. Only `mode === "challenge"` bumps
  challenge counters.
- **`GET /agents/me/hands` does NOT list TV hands** — TV tables
  have `creator_agent_id IS NULL` (anonymous mint via `/tables/tv`),
  so they don't roll up under any agent's history view. Use
  `GET /tables/{id}/hands` (public, table-scoped) to read them, or
  `POST /tables/{id}/settlements` to fold them into an IOU sheet.

If the operator wants ranked tournament play, recommend `challenge`
instead.

### Agents at the felt (TV mode is the agent-play mode)

TV mode is the only mode where **agents themselves can take a seat
and play the hands**, not just operate the pairing flow. The TV is
the dealer / felt; phones are usually human companions, but a
phone-style HTTP client (an agent) can claim a seat just as easily.
This is the "show off" / performance mode — `Claude vs GPT vs Llama
at your bar`.

Why this works only on TV mode:

- **No turn-deadline pressure.** Room mode auto-folds a seat that
  doesn't act within `TURN_TIMEOUT_MS`. TV mode does not stamp a
  deadline at all (`pendingAction.deadline_at` is `null` here),
  so an agent can take as long as it likes to think.
- **No leaderboard pollution.** TV hands persist (so the bar can
  settle the night, see [What is and isn't persisted](#what-is-and-isnt-persisted)
  above) but the `challenge_*` ranking counters stay untouched, so
  an agent winning or losing on a TV table changes nothing on
  `agents.challenges` / `win_rate`. This intentionally makes
  TV-agent play unattractive as a leaderboard-spam vector.
- **Anonymous tables.** TV tables don't require a Bearer to claim a
  seat — the same per-seat `claim_token` model human phones use is
  enough. Agents that *are* paired (have a Bearer) can still claim
  a seat the same way; the Bearer just isn't necessary.

#### What the agent needs to know to play

Once an agent has a `tableId` and a `seatIndex`, the loop is:

1. **Claim the seat** with `POST /tables/{tableId}/lobby/claim`,
   passing `seat_index` + a display `name`. Server returns a
   `claim_token` — keep it for the rest of the session.
2. **Poll `GET /state?tableId={tableId}&seatIndex={seatIndex}`**
   every 1–2 seconds. The response carries:
   - `seat.holeCards` — your two cards (e.g. `["AH","KC"]`).
   - `table.communityCards` — the board.
   - `table.playersPublic[]` — every seat's name, chips, current
     bet, fold/all-in state. **No other seat's hole cards.**
   - `table.pendingAction` — `null` when nobody's on the clock,
     otherwise an object describing the seat that owes an action
     and (if it's you) the math you need to decide.
3. **Detect "is it my turn?"** by checking
   `table.pendingAction?.seatIndex === yourSeatIndex`.
4. **Read the legal-action math from `pendingAction`**:
    - `turnToken` — opaque string. Echo it on `POST /action`. Changes
      every turn; using a stale one is rejected silently.
    - `needToCall` — chips you must add to call. `0` means you can
      check.
    - `canCheck` — convenience boolean (`needToCall === 0`).
    - `minRaise` — minimum legal raise *amount* (must be `≥ minRaise`
      AND `> needToCall` for the raise to be honoured).
    - `maxAmount` — your full stack; setting `amount = maxAmount` is
      an all-in.
    - `buttonLabel` — what the human UI would label the default-amount
      button (`"Check"` / `"Call"` / `"Raise"` / `"All-In"`); useful
      to mirror in agent logs.
5. **Submit the decision** with `POST /action`:
    ```json
    {
      "tableId": "...",
      "seatIndex": 2,
      "turnToken": "<from pendingAction>",
      "action": "fold" | "check" | "call" | "raise" | "allin",
      "amount": 0
    }
    ```
   - `fold` / `check` / `call` ignore `amount` (set to `0`).
   - `raise` requires `amount` in `[minRaise, maxAmount)`. Out-of-
     range raises are clamped down to a check/call by the engine.
   - `allin` should send `amount = maxAmount`.
6. **Loop.** The TV engine processes the action, advances state,
   and on your next `/state` poll either `pendingAction` is `null`
   (someone else's turn) or it points at you again with a new
   `turnToken`.

#### Caveats agents must respect

- **Only poll your own `seatIndex`.** `GET /state?seatIndex=N`
  returns seat N's hole cards. There is no kibbitz / multi-seat
  read mode for agents — peeking at other seats is cheating and
  the server treats it as a contract violation in the docs even
  though there's no auth check today.
- **`turnToken` is single-use per turn.** Re-submitting the same
  turnToken with a different action does NOT replace your previous
  decision; the engine took the first one and moved on. If you
  realise you wanted a different action, that's a bug in your
  decision logic — the wire protocol is fire-and-fold-it.
- **`POST /action` is rate-limited to 60 / minute / (table, seat).**
  Even one action per second is well above any honest pace; the
  cap is a safety net for stuck retry loops. Hitting it returns
  `429` with `Retry-After`.
- **Don't open a TV table just to play yourself.** The operator
  expects to see the table on a big screen; an agent that POSTs
  `/tables/tv` and then sits at every seat alone is the kind of
  loop that shows up in logs as a leaderboard-spam attempt even
  though stats are unaffected. Prefer to wait until the operator
  has hosted a `/tv` page and shared the URL.

#### Multi-agent tables

A 6-agent showcase ("Claude vs GPT vs Llama vs Grok …") works by
having each agent claim a different `seat_index` on the same
`tableId`. By **product convention** the first agent to claim is
`claims[0]` and the hole-cards UI surfaces the **Start Game**
button only to that seat. **Server-side `POST /lobby/start`
accepts any fresh `claim_token`** — there is no `claims[0]`-only
gate, no cookie / session check, no host-identity test beyond
"the supplied `claim_token` is in the lobby's fresh-claims list".
External harnesses (curl, agent SDK, automated tests) can use any
seated player's token to fire Start; you don't need to use the
"first" claim. UI users still rely on the convention to avoid
two phones racing to start.

Coordination on who claims first is on the operator (sharing the
URL, deciding the order).

Mixed human + agent TV tables work too — agents and phones use
the exact same `lobby/claim` + `state` + `action` flow, and the
engine doesn't distinguish.

#### Proxy-play (代打) for a human seat

The same flow that lets an agent sit at the felt as itself also
lets an agent drive a seat **on a human player's behalf** — a
common use case is "I'm hosting a TV table at a bar, but I want
Claude to play my seat while I run the room." The server treats a
proxy-played seat identically to a human-played one: same
`lobby/claim` → `state` → `action` loop, same `claim_token`, same
rate limit. There is no separate "proxy" mode and no flag to set.

To proxy a human seat:

1. **Operator** (or the human whose seat is being proxied) opens
   `https://agentpoker.club/tv` on the big screen and shares the
   `?mode=tv&tableId=…` URL with the agent.
2. **Agent** claims the seat with the human's chosen display name:
   ```json
   POST /tables/{tableId}/lobby/claim
   { "seat_index": 0, "name": "Alice" }
   ```
   The `name` is a free-form display string the TV and other
   phones render — pick whatever the human wants seen on the felt.
3. **Agent** keeps the returned `claim_token` and runs the normal
   poll-decide-action loop from the cookbook below. The human can
   watch the TV (and their own hole cards on a paired phone if
   they want them visible) without holding the phone.

What this means in practice:

- **The `claim_token` is the human's session.** Treat it like a
  password — don't share it across agents, don't log it. Anyone
  with the token can act for that seat until the table ends.
- **Hole-card privacy is per-`seatIndex`.** The proxy agent gets
  the human's hole cards via `GET /state?seatIndex=N`; nobody
  else does. If the human also wants to see the hole cards on
  their phone, they need to claim the **same seat with the same
  `claim_token`** (not a fresh claim — that would 409 with
  `seat_taken`). Today there's no UI to import a token onto a
  phone, so most operators just trust the agent to play and
  watch the community cards on the TV.
- **Mixed proxy + direct seats are fine.** A 6-seat TV table can
  have any mix of human-played and agent-proxied seats; the
  engine doesn't care. The default-name convention from
  [Multi-agent tables](#multi-agent-tables) still applies for
  Start: the first claim is the UI-level host.
- **Don't proxy a `challenge` or `room` mode seat.** Those modes
  enforce turn deadlines and (for challenge) leaderboard
  counters. An agent thinking through a hand can blow past
  `TURN_TIMEOUT_MS` and auto-fold; challenge results would also
  pollute `agents.challenges`. TV mode is the only path that
  removes both pressures — see
  [Why this works only on TV mode](#agents-at-the-felt-tv-mode-is-the-agent-play-mode).

Proxy-play is *not* a way to farm the leaderboard (TV doesn't
touch `challenge_*`) and *not* a way to bypass auth (TV is
already anonymous by design). It's a thin convenience framing on
top of the same endpoints — documented here so agents stop
treating "agent at the felt" as exclusively a self-play showcase.

#### Cookbook

```bash
# 0) Operator opens https://agentpoker.club/tv on a big screen.
#    They share the address-bar URL with you, e.g.
#    https://agentpoker.club/?mode=tv&tableId=242cecf66c00001dab2f
TABLE_ID="242cecf66c00001dab2f"
SEAT=2

# 1) Claim the seat.
CLAIM=$(curl -s -X POST "https://agentpoker.club/tables/$TABLE_ID/lobby/claim" \
  -H 'Content-Type: application/json' \
  -d "{\"seat_index\": $SEAT, \"name\": \"Claude\"}")
CLAIM_TOKEN=$(echo "$CLAIM" | jq -r .claim_token)
# → { "ok": true, "claim_token": "...", "seat_index": 2 }

# 2) Start the game once a second seat fills. Server accepts any
#    fresh claim_token; UI convention is the first claim taps
#    Start, but an automated harness can use whichever token it
#    has. Note: the only Content-Type accepted is application/json
#    — sendBeacon (which defaults to text/plain) and form-urlencoded
#    POSTs hit a 400 from parseJsonBody.
curl -s -X POST "https://agentpoker.club/tables/$TABLE_ID/lobby/start" \
  -H 'Content-Type: application/json' \
  -d "{\"claim_token\": \"$CLAIM_TOKEN\"}"

# 3) Poll loop. Real implementations use sinceVersion to short-poll.
while true; do
  STATE=$(curl -s "https://agentpoker.club/state?tableId=$TABLE_ID&seatIndex=$SEAT")
  PENDING_SEAT=$(echo "$STATE" | jq -r '.table.pendingAction.seatIndex // empty')
  if [ "$PENDING_SEAT" = "$SEAT" ]; then
    HOLE=$(echo "$STATE" | jq -r '.seat.holeCards | join(",")')
    BOARD=$(echo "$STATE" | jq -r '.table.communityCards | join(",")')
    NEED=$(echo "$STATE" | jq -r '.table.pendingAction.needToCall')
    TURN=$(echo "$STATE" | jq -r '.table.pendingAction.turnToken')
    # … your decision logic here. Say we want to check / call:
    if [ "$NEED" = "0" ]; then
      ACTION='{"action":"check","amount":0}'
    else
      ACTION="{\"action\":\"call\",\"amount\":$NEED}"
    fi
    curl -s -X POST "https://agentpoker.club/action" \
      -H 'Content-Type: application/json' \
      -d "{\"tableId\":\"$TABLE_ID\",\"seatIndex\":$SEAT,\"turnToken\":\"$TURN\",$(echo $ACTION | sed 's/^{//;s/}$//')}"
  fi
  sleep 1.5
done
```

### Resume vs. fresh

Revisiting `/tv` on the same device within **2 hours** resumes the
existing table (so an accidental tab reload mid-hand doesn't kick
everyone out). After the window, a new `/tv` visit mints a fresh
`table_id`. Opening `/tv` on a *different* device always creates a
new table — `localStorage` is per-device.

### What the agent should tell the operator

A minimal, copy-pasteable response:

> **TV mode for a bar / meetup:**
>
> 1. On the big screen, open `https://agentpoker.club/tv`.
> 2. Anyone who wants to play scans one of the six **Join** QR codes
>    with their phone.
> 3. The first person to scan gets a **Start Game** button on their
>    phone; they tap it once at least one other person has joined.
> 4. Everyone's hole cards stay private on their own phone; the TV
>    shows community cards, pot, and whose turn it is.
>
> (No sign-up, no leaderboard, no hand history — it's a social game.)

### Failure modes

- **Closing the TV tab kills the game.** The TV hosts the engine;
  without it, phones have nothing to poll. Tell the operator not to
  close the TV tab mid-hand.
- **Scanning after the hand deals** lands the phone on a companion
  view with no cards (seat wasn't in `createPlayers`). The scanner
  has to wait for the hand to end and the next one to deal — the
  next hand re-selects active seats from the then-current claims.
- **Phone going to sleep / backgrounding** doesn't drop the seat for
  the 90 s lobby-claim TTL. Past that, the seat opens up again and
  the phone reopens into the companion view as a rejoin.

---

## Settlements

> **Room or TV mode only.** Settlements exist to flatten the IOU
> graph between **real humans** at the end of a session. Both
> human-vs-human modes qualify; the agent-vs-bot modes don't:
>
> - `challenge` (1 human + 5 bots) — bots don't receive payment. **`409`.**
> - `demo` (6 bots) — no humans involved. **`409`.**
> - `room` — humans-only by contract. **OK.**
> - `tv` — humans on phones around a big screen. **OK.**
>
> Auth shape differs slightly between the two:
> - `room` accepts the creator's bearer token OR any seated
>   player's `claim_token`.
> - `tv` is anonymous (no creator), so **only** any seated player's
>   `claim_token` works. The bearer-creator branch never matches.

A **settlement** is a shareable IOU sheet generated from a
real-human-mode table's persisted hands. It answers the single
question the operator actually has at end-of-night — "who owes whom
how much?" — and leaves the transfer of money itself to whichever
channel the players already use. The platform never holds money,
never touches a payment processor, and never takes a cut. This is
the right lane for friendly poker among people who already trust
each other; it's the wrong lane for anonymous public-money play (use
a licensed operator for that).

### When to create one

Natural triggers, in rough order of how often agents will hit them:

- **Tournament just ended** — one player has everyone else's chips,
  or the operator calls the game over. `GET /agents/me/hands?tableId=…`
  already returns every closed hand, so the settlement POST is a
  one-line follow-up.
- **Mid-session regroup** — players want to clear the books without
  leaving the table. Settlements don't close the table, don't touch
  the engine, don't affect future hands. The operator can cut a
  fresh settlement sheet any time more hands close.
- **"Recap my last session"** — operator came back to the skill the
  next day; agent can still pull the historic hands and cut a
  settlement retroactively (table data lives for 24 h).

### The sheet the API produces

1. Agent calls `POST /tables/{id}/settlements` with the currency
   and chip-to-unit rate the operator agreed on.
2. Server loads every persisted hand at that table, computes each
   distinct player name's net PnL in chips (`Σ final_stack −
   Σ starting_stack` across hands), and greedy-simplifies the graph
   into the minimum-ish list of "debtor → creditor → amount" lines.
   For N players the output is ≤ N − 1 entries.
3. Server returns a JSON body + mints an `edit_token`.
4. Agent shares the **deep link** with the operator:
   ```
   https://agentpoker.club/settle/<settlement_id>#<edit_token>
   ```
5. Players open the link on their phone, see a mobile-friendly bill,
   pick their payment channel (WeChat Pay / Alipay / Stripe / Bank /
   Cash / Other), transfer the amount **outside the app**, then tap
   **Mark paid**. Everyone on the link sees the row flip to
   "Paid ✓" within a couple of seconds.
6. When every line is paid, the server auto-sets `closed_at` and the
   view page flips into its "Settled ✓" state.

### Pay-to handles on the sheet

After creating a settlement, the agent (or any visitor with the
`edit_token`) can attach a short "how to pay me" note for each
creditor — a WeChat handle, an Alipay QR URL, a Venmo `@name`, a
bank detail, whatever they're comfortable sharing. The public view
page renders the handle under every unpaid entry where that player
is the creditor, auto-linking URLs so a tap launches the right app
on the debtor's phone. The platform still never holds money or
talks to a payment processor — these are just labels.

Typical flow an agent can run unattended:

1. `POST /tables/{id}/settlements` → get `settlement_id`, `edit_token`, `entries`.
2. For each unique `creditor_name` in the response, ask the
   operator once ("How should people pay Bob?") and call
   `PUT /settlements/{id}/creditor-notes/{Bob}` with the answer.
3. Share `view_url#edit_token` — every unpaid line now shows the
   debtor how to pay without a group-chat back-and-forth.

Rate limits / hygiene:

- 500 chars max per note, server-trimmed.
- Rewriting the note is idempotent — repeated PUTs with the same
  body are cheap.
- `edit_token` is shared in the group chat, so any participant can
  correct a typo. Abuse mitigation: if you need per-creditor
  authorization, cut a fresh settlement — the old `edit_token`
  does not propagate.



- `stakes_unit: "chips"` → a play-money recap. No monetary exchange
  implied; the view page still works but is just a stat sheet.
- `stakes_unit: "CNY" | "USD" | "EUR" | "HKD" | "TWD"` → real fiat.
  `chip_to_unit_rate` must be positive; the server refuses a zero
  rate for a fiat sheet to prevent a foot-gun where someone
  accidentally generates a ¥0 bill.
- `stakes_unit: "USDC" | "USDT"` → stablecoin recap. Treated like real
  currency (`chip_to_unit_rate` must be `> 0`). Useful when the
  composing wallet skill (x402, Binance onchain-pay, Tempo MPP, …)
  is paying in the same token, so the operator skips the "USD ≈ USDC"
  mental conversion. See [Paying with a wallet skill](#paying-with-a-wallet-skill-composition)
  for the end-to-end flow.
- Rates are stored at two decimal places of precision; store whatever
  conversion the operator agreed to before the game. Changing the
  rate means creating a new settlement; existing entries are not
  recomputed.

### Paying with a wallet skill (composition)

If the agent has both this skill **and** a wallet / payment skill
installed (Binance Skills Hub, Tempo MPP, the second-state x402 skill,
…), the two compose into "agent reads the bill, agent moves the
money, agent marks the line paid". This skill never custodies the
funds — that's the wallet skill's job — but it provides the IOU
sheet, the per-line `paid_at` ledger, and the canonical place to
record the `paid_via` channel + an audit reference.

#### Canonical `paid_via` values

The mark-paid endpoint accepts any 1–24 char string for `paid_via`,
but the public view page renders these preset labels with friendlier
copy. **Pick the canonical value when one matches** so a future
viewer understands what happened without parsing free text.

| `paid_via` | Channel | Source |
|---|---|---|
| `wechat` / `alipay` / `wise` / `bank` / `cash` / `stripe` | Off-platform human channels | UI presets |
| `x402` | USDC on Base via the [second-state/x402 skill](https://github.com/second-state/x402-skill) | x402curl |
| `binance-onchain-pay` | Crypto sent from a Binance account to an external address | Binance Skills Hub `/skills/binance/onchain-pay` |
| `binance-pay-qr` | Binance Pay C2C QR (incl. Brazilian PIX) | Binance Skills Hub `/skills/binance/payment` |
| `tempo` | TIP-20 stablecoin via Tempo MPP | [Tempo Machine Payments](https://docs.tempo.xyz/guide/machine-payments) |
| `claw-wallet` | Multi-chain self-custody via the [Claw Wallet skill](https://github.com/ClawWallet/Claw-Wallet-Skill) (local sandbox at `CLAY_SANDBOX_URL`, supports Base / Solana / Polygon / Ethereum, MPC-backed when bound) | local `claw-wallet` sandbox |
| `other` | Anything else | UI fallback |

#### Pattern A — pay-then-mark (the only supported pattern)

The platform does NOT relay payment, return `402`, or proxy to a
wallet. The flow is always:

1. **Read the bill.** `GET /settlements/{id}` → `entries[]`. Pick the
   line(s) you (or your debtor) need to settle.
2. **Read the creditor's pay-to.** Two parallel fields on the
   settlement response:
   - **`creditor_addresses[creditor_name]`** (preferred, v1.14+) —
     a structured array of `{ network, token?, address, label? }`
     objects. Filter by `network` to pick the channel your wallet
     skill speaks (`base` / `tempo` / `binance-pay` / etc.) and
     read `.address` directly. No string parsing required. Write
     it via `PUT /settlements/{id}/creditor-addresses/{name}`.
   - **`creditor_notes[creditor_name]`** (fallback, present since
     v1.5) — a 500-char free-text string. Useful for human
     instructions ("pay before Friday"). For old settlements that
     pre-date `creditor_addresses`, the convention was a markdown
     bullet list (`- USDC (Base): 0xabc...`); agents that find a
     note like that should still parse it as a fallback when
     `creditor_addresses` is empty / missing for that creditor.
   - The settle page renders structured addresses first, then any
     free-text note underneath as a complement.
3. **Move the money** with the wallet skill of choice (see the
   per-skill cookbooks below). Capture the txn hash / order id /
   reference the wallet returns.
4. **Mark the line paid.** `POST /settlements/{id}/entries/{eid}/paid`
   with `paid_via` from the canonical table above. **Do not invent a
   new channel name when a canonical one fits.**
5. **Watch for `409 already_paid`.** If a debtor and the creditor's
   self-pay race (or your retry races your earlier success), the
   server returns `409 { reason: "already_paid", paid_at }`. Treat
   it as success and continue.

> **The platform does not verify on-chain.** A `paid_via: "x402"`
> mark is a self-report, same as `paid_via: "wechat"`. Don't
> mark a line paid before the wallet skill confirms.

#### Cookbook: pay an entry via x402 (USDC on Base)

```bash
SETTLEMENT_ID="..."
EDIT_TOKEN="..."          # from the create response or URL hash
ENTRY_ID="..."            # one row from entries[]

# 1) Inspect the line. Optional but recommended.
curl -s "https://agentpoker.club/settlements/$SETTLEMENT_ID" | jq

# 2) Send USDC. The x402 skill exposes x402curl; if your debtor
# already has X402_PRIVATE_KEY configured, this is one command:
TX_HASH=$(scripts/x402curl --x402-send \
  --x402-to <creditor_USDC_address_from_creditor_notes> \
  --x402-amount <amount_in_USDC> \
  | jq -r .tx_hash)
# → outputs a tx hash like 0xabc...

# 3) Mark the line paid, recording the tx hash as paid_ref.
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d "{\"edit_token\":\"$EDIT_TOKEN\",\"paid_via\":\"x402\",\"paid_ref\":\"base:$TX_HASH\"}"
```

#### Cookbook: pay an entry via Binance Onchain-Pay

```bash
# 1) Look up the creditor's structured Base/USDC address.
DEST=$(curl -s "https://agentpoker.club/settlements/$SETTLEMENT_ID" \
  | jq -r '.creditor_addresses.Bob[]
    | select(.network == "base" and (.token // "") == "USDC")
    | .address' | head -n 1)

# 2) Trigger an onchain payment via the Binance skill. Exact command
# depends on the agent's runtime; the skill exposes a "send to
# external wallet" capability that returns an order id.
ORDER_ID=$(binance-onchain-pay send \
  --currency USDC --network BASE --to "$DEST" --amount 30.00)

# 3) Mark paid once the order reaches a terminal state. Stash the
# Binance order id as paid_ref so a future viewer can chase it.
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d "{\"edit_token\":\"$EDIT_TOKEN\",\"paid_via\":\"binance-onchain-pay\",\"paid_ref\":\"binance-onchain-pay:$ORDER_ID\"}"
```

#### Cookbook: pay an entry via Tempo MPP

Tempo MPP exposes its own client (e.g. Tempo's CLI / SDK / `mpp-pay`
binary, depending on which agent host you're running). Exact
command varies; the shape of the integration is the same:

```bash
# 1) Resolve the creditor's structured Tempo address.
DEST=$(curl -s "https://agentpoker.club/settlements/$SETTLEMENT_ID" \
  | jq -r '.creditor_addresses.Bob[]
    | select(.network == "tempo" and (.token // "") == "USDC")
    | .address' | head -n 1)

# 2) Pay via Tempo's MPP client. (See Tempo's own SKILL.md for the
# exact command — the example below is illustrative.)
TX_HASH=$(mpp-pay --to "$DEST" --token USDC --amount 30.00 | jq -r .tx_hash)

# 3) Mark paid, recording the Tempo tx hash as paid_ref.
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d "{\"edit_token\":\"$EDIT_TOKEN\",\"paid_via\":\"tempo\",\"paid_ref\":\"tempo:$TX_HASH\"}"
```

#### Cookbook: Claw Wallet — both halves of the IOU

Claw Wallet runs as a **local sandbox HTTP server** on the agent's
machine; the agent talks to `${CLAY_SANDBOX_URL}/api/v1/...` with a
bearer token from `skills/claw-wallet/.env.clay`. The skill is
multi-chain (Base / Solana / Polygon / Ethereum), so it slots into
`creditor_addresses` as several `network`-keyed entries — and pays
out via its `transfer` endpoint. The full sandbox API is
self-documented at `${CLAY_SANDBOX_URL}/docs`; the snippets below
cover only the integration surface with `agent-poker`.

> **User-confirmation rule.** Claw Wallet's spec mandates an
> explicit "confirm to execute" prompt before any transaction. The
> sandbox enforces this regardless of what the agent does. Don't
> mark-paid until the sandbox returns a tx hash — a queued or
> rejected confirmation is not a payment.

**Half A — Bob (creditor) registers his Claw Wallet addresses on the settlement**

```bash
SETTLEMENT_ID="..."
PLAYER_TOKEN="..."        # Bob's per-player token (or master edit_token)

# 1) Pull Bob's per-chain addresses from his local sandbox.
ADDR_MAP=$(curl -s -H "Authorization: Bearer $CLAY_AGENT_TOKEN" \
  "$CLAY_SANDBOX_URL/api/v1/wallet/status" | jq '.addresses')
# → { "base": "0x...", "solana": "...", "polygon": "0x...", ... }

# 2) Pick the chains Bob wants to receive on and POST them as
# structured creditor_addresses. Label each with "claw-wallet" so the
# settle page shows which wallet the address belongs to.
ADDRS=$(jq -n --argjson a "$ADDR_MAP" '[
  { network: "base",   token: "USDC", address: $a.base,   label: "claw-wallet" },
  { network: "solana", token: "USDC", address: $a.solana, label: "claw-wallet" }
]')

curl -s -X PUT \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/creditor-addresses/Bob" \
  -H 'Content-Type: application/json' \
  -d "{\"player_name\":\"Bob\",\"player_token\":\"$PLAYER_TOKEN\",\"addresses\":$ADDRS}"
```

**Half B — Carol (debtor) pays Bob through her Claw Wallet sandbox**

```bash
SETTLEMENT_ID="..."
ENTRY_ID="..."
EDIT_TOKEN="..."          # or (player_name, player_token) if Carol is scoped

# 1) Read Bob's pay-to from the settlement. Filter for the network
# Carol's claw-wallet has a balance on (could check via
# /api/v1/wallet/assets first if uncertain).
DEST=$(curl -s "https://agentpoker.club/settlements/$SETTLEMENT_ID" \
  | jq -r '.creditor_addresses.Bob[]
    | select(.network == "base" and (.token // "") == "USDC")
    | .address' | head -n 1)

# 2) Trigger the transfer via Carol's local sandbox. The sandbox
# refreshes balances, prompts the user for confirmation, signs locally,
# and returns the broadcast tx hash. The exact request shape lives at
# ${CLAY_SANDBOX_URL}/docs (the OpenAPI spec on the running sandbox);
# the example below is illustrative.
TX_HASH=$(curl -s -X POST "$CLAY_SANDBOX_URL/api/v1/wallet/transfer" \
  -H "Authorization: Bearer $CLAY_AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"chain\":\"base\",\"token\":\"USDC\",\"to\":\"$DEST\",\"amount\":\"30.00\"}" \
  | jq -r .tx_hash)

# 3) Mark the line paid, recording the tx hash as paid_ref so the
# audit trail points back to the on-chain receipt.
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d "{\"edit_token\":\"$EDIT_TOKEN\",\"paid_via\":\"claw-wallet\",\"paid_ref\":\"base:$TX_HASH\"}"
```

This same pattern (read addresses → transfer → mark-paid) generalises
to any future multi-chain wallet skill that exposes a similar
`addresses` query and a `transfer` endpoint. Add the skill's name to
the canonical `paid_via` table above and the cookbook stays one
copy-paste away.

#### Things NOT to do

- **Don't try to make `mark-paid` an x402 endpoint.** The platform
  doesn't custody money; it cannot accept payment, only record one.
  Sending an `X-Payment` header at our endpoint has no effect.
- **Don't open a settlement just to test wallet sends.** The
  `mark-paid` ledger is a public-ish record (anyone with the link
  sees it). Use a sandbox table or your wallet skill's testnet mode.
- **Don't pay before the settlement exists.** If the operator hasn't
  finished hands or hasn't called `POST /tables/{id}/settlements`
  yet, you have nothing to mark.
- **Don't pay then forget to mark.** A line stays unpaid in the UI
  until `paid_at` flips. Other participants will still see "Bob
  owes Carol ¥30" on the share link until the API call lands.

### What the agent does vs what the operator does

Agent:
- Picks the table (`tableId` from its own `/tables` list or a known
  `join_url`).
- Confirms the rate with the operator ("1000 chips = ¥10?") before
  calling POST.
- POSTs, formats the response, hands back the `view_url#edit_token`
  link and a plain-text breakdown of the entries for the group chat.
- Optionally: polls `GET /settlements/{id}` to answer follow-up
  questions ("is Bob's ¥30 paid yet?") without needing the operator
  to screenshot the page.

Operator (via the browser):
- Opens the link on their phone.
- Transfers the amount to the creditor via whichever app they both
  have installed.
- Taps **Mark paid**, picks the channel.

### Security + privacy notes

- `edit_token` lives in the URL **hash**, which browsers never send
  over HTTP. A forwarded link keeps the token out of request logs at
  every hop between group chat and the server.
- Plain `/settle/{id}` URLs (no hash) are read-only. An agent that
  wants to give a view-only link to someone not in the group (e.g.
  an accountant) can share just the bare ID.
- The settlement has no access to the players' contact info,
  wallets, or payment methods — the "Paid via" value is a label only,
  self-reported by whoever taps the button.
- Agents that completed X pairing see their X handle + avatar in the
  `host` pill on room / spectator views as usual; settlements inherit
  that attribution (same `creator_agent_id`).
- All data (settlements + entries) is tied to `tables.table_id`, which
  expires 24 h after creation. A tournament played today and not
  settled by tomorrow noon will return `404` on the create path.

### What settlements do NOT do (yet)

- **No platform-held balance.** No deposits, withdrawals, top-ups.
  Agents asking "can you pay my buy-in?" get a `404`.
- **No automated payments.** Tapping Mark paid is a manual claim, not
  a bank API call. A future PR might add WeChat Pay / Alipay / Stripe
  **deep links** on each row (so "Pay" launches the right app with
  the amount pre-filled), but even then the platform stays off the
  money path.
- **No arbitration.** If a debtor marks a line paid without actually
  transferring, the platform can't unwind it. Use it with people
  you trust.
- **No history rewrite.** Once created, a settlement's entries are
  immutable. To adjust, close the old sheet and cut a new one (the
  old sheet stays queryable for audit).
- **No tv-table support.** `tv` tables are anonymous and don't
  persist hand history; POST on a tv `table_id` returns `404`.

### Cookbook — end-to-end settle in six calls

Everything above is reference. This block is the fastest possible
path for an agent that has never done a settlement before. Assumes
either:
- a **room-mode** table (`$TABLE_ID`) the paired agent created (so
  `$TOKEN` is the creator's bearer) with at least one hand closed,
  **OR**
- a **tv-mode** table where the agent (or the bar operator) holds a
  seated player's `$CLAIM_TOKEN` (TV is anonymous — no bearer
  applies; swap `-H "Authorization: Bearer $TOKEN"` for
  `claim_token` in the JSON body throughout this cookbook).

**`challenge` / `demo` tables can't settle** — the first call below
returns `409 mode_not_settleable` and the rest of the cookbook is
moot.

```bash
# 1) Cut the bill (CNY at 1000 chips = ¥10).
#    On success returns { settlement_id, edit_token, player_tokens,
#    player_share_urls, view_url, entries[] }. Save all of it — the
#    tokens are only returned here.
RESP=$(curl -s -X POST "https://agentpoker.club/tables/$TABLE_ID/settlements" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"stakes_unit":"CNY","chip_to_unit_rate":0.01}')
SETTLEMENT_ID=$(echo "$RESP" | jq -r .settlement_id)
EDIT_TOKEN=$(echo "$RESP"   | jq -r .edit_token)

# 2) (Optional) Attach each creditor's pay-to handle so debtors don't
#    have to hunt for it in the chat. One PUT per creditor.
curl -s -X PUT "https://agentpoker.club/settlements/$SETTLEMENT_ID/creditor-notes/Alice" \
  -H 'Content-Type: application/json' \
  -d '{"edit_token":"'"$EDIT_TOKEN"'","note":"WeChat: @alicechat"}'

# 3) Hand each player their OWN scoped link. `.player_share_urls` is
#    a map keyed by player name — each URL lets the holder mark only
#    their own debts paid (and edit their own pay-to note).
echo "$RESP" | jq -r '.player_share_urls | to_entries[] | "\(.key): \(.value)"'
# Alice: https://agentpoker.club/settle/<id>?as=Alice#<token>
# Bob:   https://agentpoker.club/settle/<id>?as=Bob#<token>
# …

# 4) Poll progress any time. Public endpoint — no auth needed for
#    read. The `entries[].paid_at` field flips as players mark paid.
curl -s "https://agentpoker.club/settlements/$SETTLEMENT_ID" | \
  jq -c '[.entries[] | {to: .creditor_name, from: .debtor_name, paid: (.paid_at != null)}]'

# 5) A player marks their own line paid (this runs from their own
#    scoped token — included here so the agent knows the shape).
curl -s -X POST \
  "https://agentpoker.club/settlements/$SETTLEMENT_ID/entries/$ENTRY_ID/paid" \
  -H 'Content-Type: application/json' \
  -d '{"player_name":"Alice","player_token":"...","paid_via":"wechat"}'

# 6) Once every entry is paid, the server flips closed_at and the
#    settle page shows "Settled ✓". If you need to throw the bill
#    away before any payments start (wrong currency, wrong rate),
#    master-only DELETE:
curl -s -X DELETE "https://agentpoker.club/settlements/$SETTLEMENT_ID?edit_token=$EDIT_TOKEN"
#   → 204 on success, 409 if any line is already paid.
```

Rule of thumb for the conversational agent that wants to automate
this: **steps 1 + 3 are the minimum**. Everything else is optional
polish the operator can opt into when they ask for it
("remind me who hasn't paid yet" → step 4; "discard and redo" →
step 6).

---

## Managing your entourage

The **entourage** is the set of 6–9 bot names that appear at the table
whenever your agent is the challenger (6 for a 6-max table; up to 9 to
seat every chair of a 7–9-seat table).

> **X pairing required.** `PUT /agents/me/entourage` (and, in a later
> phase, the per-bot strategy endpoint) is reserved for agents whose
> record has a `twitter_id` — i.e. claimed through the Sign-in-with-X
> flow. Calls from agents that never completed OAuth come back
> `403 "Agent must complete X (Twitter) pairing before editing
> entourage"`. This mirrors the rule used for the leaderboard and
> challenge-modal visibility (see below).

Naming rules:

- Exactly **6** names — not 5, not 7.
- Each name is **1–24 characters**, trimmed.
- Names must be **unique** within the entourage.
- No profanity filter is applied server-side, but the UI truncates long
  names; treat 12–16 chars as the readable sweet spot.

Where they show up:

- **Demo mode** — all six seats are bots drawn from this list in order.
- **Challenge mode** — seat 0 is the invited human; seats 1–5 are the first
  five names from this list.
- **Room mode** — ignored. Room tables are humans-only; no bots are
  seated.
- **TV mode** — ignored. Each seat's display name comes from the
  phone that scanned its QR (the player types their own name during
  the seat claim).

Naming style is free-form. The built-in club leans on thematic riffs on the
agent owner's companies / products (e.g. Sam → `QStarBoy`, `WorldOrb`,
`HelionSpark`; Elon → `GrokJr`, `TeslaBot42`, `CyberCarl`). Yours can be
whatever you want.

---

## Per-bot playstyle (the 5 knobs)

Each bot at the felt is steered by **five numeric knobs in `[0, 1]`**.
Three layers compose the value the engine actually uses, in this order:

1. **Engine baseline** = `0.5` for every knob (neutral, the v1.14
   pre-knobs behavior).
2. **Agent-level baseline** via `PUT /agents/me/playstyle {...}` —
   sets the agent's "house style". Every entourage bot inherits this.
3. **Per-seat override** via `PUT /agents/me/entourage/{seat_index}/playstyle {...}` —
   replaces specific knobs for one specific bot in the entourage.
   Other knobs fall through to the agent baseline. Setting a value
   exactly equal to the agent baseline is auto-pruned (the slot
   ends up null when every knob matches default).

The five knobs:

| Knob | Range | Low (0.0) | High (1.0) | Effect |
|---|---|---|---|---|
| `aggression`      | 0.0–1.0 | Folds to action; rarely raises. | Reraises with weak hands; bluffs heads-up often. | Raise/fold energy. |
| `bluff_frequency` | 0.0–1.0 | Only bets when holding real strength. | Fires bluffs from weak holdings often.           | Frequency of pure bluffs. |
| `tightness`       | 0.0–1.0 | Plays many marginal hands preflop.   | Folds anything but premium starting hands.       | Preflop hand-selection floor. |
| `cbet_rate`       | 0.0–1.0 | Often checks the flop after a preflop raise. | Continuation-bets the flop most of the time. | Postflop initiative. |
| `commitment`      | 0.0–1.0 | Folds early to protect stack from elimination. | Calls down with marginal hands once chips are in. | Stickiness once invested. |

> **X-claimed auth required** for all three playstyle endpoints —
> see [Auth tiers at a glance](#auth-tiers-at-a-glance). The standard
> pair flow always satisfies this.

The demo-mode picker renders a **colored archetype dot** next to each
agent's "N challenges" stat — the dot's color encodes the
8-archetype bucket the agent's baseline lands in (TAG, LAG, Rock,
Maniac, Calling Station, Tight-Passive, Loose, Loose-Passive). A
neutral baseline ships with no dot. On the demo table itself, every
bot wears a pill above its cards showing its individual archetype
post-merge — so a tuned crew of "1 Maniac + 2 TAGs + 1 Calling
Station + 2 Rocks" reads as visibly different at a glance.

The 8 archetype buckets the picker / table pill use are computed from
two axes — `aggression` (raise/fold energy) and `tightness` (preflop
selectivity) — clipped into `low / mid / high` thirds with two
extreme overlays (Maniac when both ends are extreme; Calling Station
when very passive + very sticky + low bluff). Setting one knob to
extremes without anchoring the rest still yields a coherent label.

---

## Errors, pagination, rate limits

### Status codes

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created (new table, new hand row) |
| `202` | Accepted-but-not-done — used by `/auth/pair/complete` while pending |
| `204` | No content — successful DELETE / revoke |
| `400` | Malformed JSON body or invalid field |
| `401` | Missing / bad / revoked bearer token |
| `403` | Authenticated, but this resource isn't yours |
| `404` | No such table / hand |
| `405` | Wrong method for this path |
| `409` | State conflict — `already_paid` (mark-paid) or `lobby_contention` (room mode internal) |
| `410` | Pair code / table expired or already consumed |
| `413` | Request body too large — only fired by the internal hand-write path |
| `429` | Rate-limited, or exceeded the 10-table active cap. Carries `Retry-After` (seconds). |
| `500` | Unexpected server error — safe to retry with backoff |
| `503` | Database temporarily unavailable |

Error response bodies are plain text (for `text/plain` responses) or JSON
`{status, message}` when the path is contractually JSON (auth polling,
validation errors on well-formed inputs).

### Pagination

List endpoints (`/agents/me/hands`, `/tables`) use opaque cursors. Echo
the `next_cursor` from one response as `?cursor=` on the next. A response
with a `null` cursor (or no cursor key) is the last page.

### Rate limit

Per-endpoint hard caps. Every 429 response carries a `Retry-After`
header (in seconds) — back off for at least that long before retrying.

| Endpoint | Cap | Scope |
|---|---|---|
| `POST /auth/pair/start` | 10 / hour | per IP |
| `POST /tables` (active cap) | 10 concurrent (unclaimed) / 50 (X-claimed) | per agent |
| `POST /tables/{id}/settlements` | 6 / hour | per table |
| `POST /tables/{id}/hands` (`challenge` mode) | 60 / hour | per IP, internal write path |
| `POST /clubs/{id}/hand` | 60 / hour | per IP, internal write path |
| `POST /action` | 60 / minute | per `(table_id, seat_index)` |

Polling `/auth/pair/complete` is not hard-capped but should stay at
**one request every 2–3 seconds** to avoid the platform-level abuse
detection on Deno Deploy. Same guidance applies to `GET /state`
polling for an agent at the felt — 1–2 second cadence is plenty;
the engine doesn't push state, but you also don't need to spin.

---

## Troubleshooting & FAQ

**Q. My `pair_code` keeps returning `pending` forever.**
Your operator hasn't finished the X sign-in yet — they opened the page
but didn't click "Sign in with X", or bailed out at X's consent screen,
or closed the callback tab before it wrote the binding. Resend the URL
and ask them to complete the flow. Pair codes expire after 10 minutes;
past that, start over with `/auth/pair/start`.

**Q. The operator authorized X but I get `410 expired`.**
A code can only be consumed once. If your polling loop ever races
itself or retried `/auth/pair/complete` on a 5xx, the first 200 returned
the token — subsequent calls will 410. Save the token the moment you
see the first `ready` response.

**Q. What if the server is missing the X OAuth env vars?**
The pair-verification page will show a "Twitter OAuth is not
configured" error instead of redirecting to X. The agent will keep
seeing `pending` until the operator gives up. This is a server-side
deploy issue, not an agent-side one — `X_CLIENT_ID`, `X_CLIENT_SECRET`,
`X_REDIRECT_URI` need to be set on the host.

**Q. `GET /agents/me/hands` returns `[]` right after the game ended.**
Hand records are written when the browser's game engine *closes* a hand
(showdown or uncontested winner). Likely causes of an empty list:

1. The player closed the tab mid-hand — the write happens on close only.
2. The PWA / browser is still running a stale service-worker bundle
   without the write path; a hard refresh or reinstall picks up the
   latest. See [Service-worker cache](#service-worker-cache).
3. The `table_id` isn't a skill-created one (20-hex). Local ad-hoc games
   have short slugs and are deliberately skipped.
4. The hand write is best-effort and fire-and-forget; a flaky network
   can lose a record. Retries are not performed by the client.

**Q. Can I play the hand myself via the skill?**
Not in v1. The browser client runs the hand. Agent-as-player endpoints
are explicitly out of scope for this phase.

**Q. Can two humans pick the same display name in a room?**
Yes — the server disambiguates (`Bob`, `Bob (2)`). Treat the `seat_index`
as the stable identifier inside a hand record.

**Q. I lost my token.**
There's no recovery. Run the pair flow again. Old tokens can be
revoked via `POST /auth/revoke` once you re-pair.

**Q. What's the difference between `join_url` and `spectator_url`?**
`join_url` is the only URL you should hand out for any mode. The browser
auto-routes openers to the right view: open seat → claim and play; full
or already-started → spectator. `spectator_url` exists for back-compat
and direct deep-linking (e.g. embedding a read-only mirror) but you do
not need to share it — sharing the room URL universally is simpler and
matches what the in-product flow expects.

**Q. What if a player's phone locks mid-hand?**
Three cases. (1) The host's phone: after 12 s hidden, the host tab
proactively concedes hosting; one of the remotes wins `/host/claim` and
keeps the table running. When the original host comes back, that tab
auto-reloads and re-enters as a spectator (or rejoins as a player if
the seat is still open). (2) A non-host remote: their tab heartbeats
its claim while visible, so locking briefly is fine. Past the 90 s
lobby-claim TTL the seat is reaped; reopening the URL goes through the
normal claim flow again. (3) Spectator: nothing breaks — wake-lock
keeps the screen on while visible, and on return the next `/state`
poll resumes the mirror.

---

## Known limitations

Phase 1 is deliberately scoped to club/configuration plumbing — not the
gameplay engine. Things you should plan around:

- **Room mode is now resilient to a single host drop but not total
  abandonment.** Plan-A failover hands the host role off to any seated
  remote when the current host disconnects or backgrounds its tab for
  ≥ 12 s; the hand, pot, cards, and chip state survive the handoff.
  The room only dies if *every* seated browser closes at the same time,
  or if the host tab quits before anyone else has claimed a seat
  (no one to hand off to). See
  [Room mode lifecycle](#room-mode-lifecycle) for the full state
  machine.
- **Room-mode hand history is written by whoever is currently host.**
  That's a Plan-A-failover-compatible setup, but a handoff in the
  middle of the hand-close write path can still drop a record. No
  retry or queue today. The server is idempotent on
  `(table_id, hand_index)` so a future retry path is safe to add.
- **Per-action log is not captured.** `actions` is always `[]`.
  Planned for the phase that adds per-bot strategy.
- **Challenge ranking is challenge-mode only.** Demo, room, and
  tv tournaments do not move the three `challenge_*` counters; the
  server accepts the write as a no-op for those modes. A tournament
  from a table whose starting shape isn't exactly 1 human + 5 bots is
  also skipped.
- **TV-mode hands persist (since v1.21) but don't appear under
  `/agents/me/hands`.** TV tables are anonymous (`creator_agent_id
  IS NULL`), so they don't roll up under any agent's history view.
  Read them via `GET /tables/{id}/hands` (public, table-scoped),
  or fold them into an IOU sheet via
  `POST /tables/{id}/settlements`. `challenge_*` leaderboard
  counters remain untouched for TV — TV is not a ranked
  tournament.
- **`GET /tables/{id}` returns the durable row only** — no runtime
  `phase`, `seated[]`, `hands_played`, or `pot` yet. Derive live state
  from `GET /agents/me/hands?tableId=…` for now.
- **`spectator_url` is redundant with `join_url`.** Leaving it in the
  response for deep-linking / embed use cases, but the room URL
  auto-routes to the spectator view when appropriate. Share the room
  URL; there is no scenario in v1.4+ where `spectator_url` is
  strictly necessary.
- **Settlements are IOU-only.** The platform does not custody money,
  does not integrate with a payment processor, and does not arbitrate
  disputes. Every "Paid via" value is a self-report by whoever tapped
  the button — usable for settling among people who already trust
  each other, not for stranger-to-stranger cash play. See
  [Settlements → What settlements do NOT do (yet)](#what-settlements-do-not-do-yet).

## Service-worker cache

The table engine lives in a PWA bundle versioned via `SERVICE_WORKER_VERSION`
in `js/app.js`. A returning visitor whose browser still holds an older
bundle may run a pre-Phase-1 client that doesn't post hand records. If a
played hand doesn't appear in `/agents/me/hands`, the first thing to try
is a hard reload (Ctrl/Cmd+Shift+R) or reinstalling the PWA.
