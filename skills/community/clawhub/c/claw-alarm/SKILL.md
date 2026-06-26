---
name: configure-user-alarm
description: Read, create, update, snooze, and delete alarms on a user's iPhone running ClawAlarm. Use when the user asks to set an alarm, change an existing alarm's time/recurrence/label, snooze or disable an alarm, list their current alarms, or pair a new device. The skill talks to the ClawAlarm cloud-sync API and a silent APNS push reconciles the change onto the phone.
---

# Configure User Alarm

## Overview

This skill lets you set and manage alarms on a user's iPhone running the ClawAlarm app.

ClawAlarm is a cloud-synced alarm clock. Each install registers a per-device Durable Object on a Cloudflare Worker (`api.claw-alarm.com`), and any change made through the API is fanned out to the phone over a silent APNS push. The phone then re-fetches the alarm list and reconciles it into AlarmKit (the iOS native alarm framework). End result: when you `POST /v1/account/alarms` from this skill, the phone rings on schedule — no app foreground required.

You can use this skill to:

- **List** the user's current alarms.
- **Create** a new alarm (one-off, daily, weekdays, weekends, or arbitrary weekday mask).
- **Update** an existing alarm's time, label, recurrence, sound, or enabled state.
- **Snooze** a currently-ringing alarm (intent-driven snoozes only).
- **Delete** an alarm.
- **Inspect** device status (last sync time, push health, pending revision).

All interaction goes through `scripts/alarm-api.sh`, a thin curl wrapper over the API. The CLI fetches the live OpenAPI spec from `/openapi.json` so the available routes, request bodies, and responses always reflect the deployed worker — there is no separately-versioned client to drift.

The full machine-readable spec lives at:

- **Spec:** `https://api.claw-alarm.com/openapi.json`
- **Reference UI:** `https://api.claw-alarm.com/reference` (Scalar-rendered)

## Pairing & authentication

Before this skill can configure anything, the phone has to hand the CLI a bearer token. ClawAlarm uses a one-time pairing-code handshake to do that.

### How the pairing handshake works

1. **On the phone:** the user opens the ClawAlarm app and taps "Connect Claude" (or whatever the equivalent setting is in the current build). The app calls `POST /v1/pairing/init`, which mints a fresh `accountId`, a long-lived bearer `token`, and a 6-letter `code` of the form `ABC-DEF`. The phone stores the token locally and displays the code to the user.
2. **In this skill:** the user pastes the code into the chat. You exchange it for the same token by running:

   ```bash
   scripts/alarm-api.sh pair ABC-DEF
   ```

   Internally, that runs `POST /v1/pairing/exchange` with `{"code":"ABC-DEF"}`, validates the returned token by hitting `GET /v1/account/status`, and writes it to `.env` next to the skill (or `~/.claw-alarm-cli/.env` with `--location=global`).
3. **From here on,** every API request from `alarm-api.sh` carries `Authorization: Bearer <token>` and lands on the same Durable Object as the phone's own writes.

Codes are **single-use** and **expire 10 minutes after issue**. If the user takes too long, ask them to refresh on the phone (or — if you're already paired and just want to add another non-iOS client — run `scripts/alarm-api.sh refresh`, which mints a new code on the existing account).

### One token = one device

A token is bound to exactly one ClawAlarm install. The Durable Object key is derived from the `accountId` baked into the token; there is no notion of "account with multiple devices" in the current API.

That means:

- To configure alarms on **one** phone, do the pairing handshake **once**.
- To configure alarms on a **second** phone, do the pairing handshake **again** from a separate location. There's no shared state — each device has its own alarm list and its own token.
- The token does not expire on a timer. It's invalidated only by the user explicitly resetting pairing on the device.

### Storing the token

The bearer token is a secret in the cryptographic sense — anyone holding it can read and rewrite the alarm list on the paired device. **However:**

- It can only configure alarms. It cannot read contacts, location, photos, payment info, or anything else on the phone.
- Its blast radius is one device.
- It does not roll. Re-pairing is cheap (one tap on the phone).

Given that, it is **safe to commit the token to a project-local `CLAUDE.md`, an `.env`, or any other config file you'd normally pin to a repo for personal-project use.** You do not need a secrets manager. The default `alarm-api.sh pair` command writes the token to `<skill>/.env`, which the skill `.gitignore`s, but you can also paste it into your `CLAUDE.md` so future sessions auto-load it without re-pairing:

```
# In ~/.claude/CLAUDE.md or project CLAUDE.md
CLAW_ALARM_API_TOKEN=<paste-token-here>
```

The CLI resolves credentials in this order:

1. `CLAW_ALARM_API_TOKEN` from the current shell environment.
2. Local saved token at `<skill>/.env`.
3. Global saved token at `~/.claw-alarm-cli/.env`.

Use `scripts/alarm-api.sh auth status` to see which one is active.

## Listing & updating alarms

Once authenticated, the CLI is a generic curl wrapper. Every endpoint on the deployed worker is reachable through it — the help text is generated from the live OpenAPI spec, so anything documented there is callable here.

### Discover available routes

```bash
# All routes, with example payloads inferred from the spec.
scripts/alarm-api.sh --help

# Full schema for one route (params, request body, responses).
scripts/alarm-api.sh --help /v1/account/alarms
scripts/alarm-api.sh --help /v1/account/alarms/{id}
```

### Common workflows

**List alarms:**

```bash
scripts/alarm-api.sh /v1/account/alarms
```

Returns `{ object: "list", data: [Alarm, ...], device_revision: <int> }`. The `device_revision` is the per-device monotonic counter — clients can short-circuit a refresh when it hasn't changed.

**Create a daily 7:30 am alarm:**

```bash
scripts/alarm-api.sh -m POST -d '{
  "label": "Wake up",
  "local_time": { "hour": 7, "minute": 30 },
  "recurrence": { "type": "daily" },
  "time_zone": "America/Los_Angeles"
}' /v1/account/alarms
```

**Create a weekdays-only alarm:**

```bash
scripts/alarm-api.sh -m POST -d '{
  "label": "Stand-up",
  "local_time": { "hour": 9, "minute": 0 },
  "recurrence": { "type": "weekdays" },
  "time_zone": "America/Los_Angeles"
}' /v1/account/alarms
```

**Create an arbitrary-weekday alarm (e.g. Mon/Wed/Fri):**

`recurrence.weekday_mask` is a 7-bit bitmask. Bit 0 = Sunday, bit 1 = Monday, …, bit 6 = Saturday.
Mon (2) | Wed (8) | Fri (32) = 42.

```bash
scripts/alarm-api.sh -m POST -d '{
  "label": "Gym",
  "local_time": { "hour": 6, "minute": 15 },
  "recurrence": { "type": "weekly_mask", "weekday_mask": 42 },
  "time_zone": "America/Los_Angeles"
}' /v1/account/alarms
```

**Create a one-off alarm:**

```bash
scripts/alarm-api.sh -m POST -d '{
  "label": "Flight",
  "local_time": { "hour": 4, "minute": 45 },
  "recurrence": { "type": "none" },
  "one_off_local_date": { "year": 2026, "month": 5, "day": 12 },
  "time_zone": "America/Los_Angeles"
}' /v1/account/alarms
```

**Update an alarm:**

PATCH only the fields you want to change. Pass the alarm's current `revision` as `If-Match` to detect concurrent edits from the phone.

```bash
scripts/alarm-api.sh -m PATCH -d '{
  "local_time": { "hour": 8, "minute": 0 }
}' /v1/account/alarms/<id>
```

To use optimistic concurrency, add the header manually with curl, or omit it for a last-write-wins update on a known-stable alarm.

**Disable / re-enable an alarm:**

```bash
scripts/alarm-api.sh -m PATCH -d '{ "enabled": false }' /v1/account/alarms/<id>
```

**Snooze a ringing alarm (intent-driven only):**

The body is an ISO instant, not a duration — clock skew between client and server otherwise turns a 5-minute snooze into 4:55 or 5:05.

```bash
scripts/alarm-api.sh -m POST -d '{
  "snoozed_until": "2026-05-04T07:35:00Z"
}' /v1/account/alarms/<id>/snooze
```

**Delete an alarm:**

```bash
scripts/alarm-api.sh -m DELETE /v1/account/alarms/<id>
```

**Inspect device status:**

```bash
scripts/alarm-api.sh /v1/account/status
```

Includes `last_synced_with_device`, `device_revision`, `last_push_sent_at`, `last_push_failure_code`, and `next_fire_at` (server-computed preview of the next scheduled fire across all enabled alarms).

### Important schema notes

Authoritative shapes live in the OpenAPI spec — always prefer `alarm-api.sh --help <route>` over guessing — but a few things are worth highlighting because they're easy to get wrong:

- **`local_time` is local-clock, not UTC.** Recurring alarms store a clock-time spec (hour/minute) plus a recurrence rule plus a `time_zone`. The device recomputes the next absolute fire date each cycle, which keeps daily and weekday alarms DST- and travel-correct. Do not pretranslate the hour to UTC.
- **`time_zone` is required and must be an IANA name** (`America/Los_Angeles`, `Europe/Zurich`, etc.). When the user asks for "7am" without specifying a zone, default to the zone the phone is currently in if you can infer it from `/v1/account/status`'s `next_fire_at`; otherwise ask.
- **`one_off_local_date` is required iff `recurrence.type === "none"`.** The schema doesn't enforce that pairing — the repository does — so the API will reject the wrong combination with `BadRequest`.
- **Field names on the wire are `snake_case`.** The rest of the worker codebase is camelCase; the wire uses Stripe-style snake_case so any future non-TS client reads naturally.
- **Mutating endpoints accept an optional `If-Match: <revision>` header** for optimistic concurrency. The CLI's `-d` shorthand only sets the body, not arbitrary headers — use raw `curl` if you need it.

### Errors you'll see

The error union is declared in `src/api/errors.ts` on the worker. The shapes are:

- `400 BadRequest` — malformed payload, wrong recurrence/date combination, invalid `weekday_mask`, etc.
- `401 Unauthorized` — missing/invalid bearer token.
- `404 NotFound` — alarm id doesn't exist on this device.
- `409 Conflict` — `If-Match` revision didn't match the stored revision.
- `410 PairingCodeExpired` / `404 PairingCodeNotFound` — pairing-handshake failures.
- `500 InternalServerError` — bug; report and retry.

## Where the docs come from

The ClawAlarm worker is built on `@effect/platform`'s `HttpApi`, which means **the OpenAPI spec is generated from the same `HttpApi` definitions that produce the request/response handlers**. There is no separate spec to keep in sync — they are the same artifact.

If a route exists, it's in `/openapi.json`. If a route is in `/openapi.json`, it's callable. The Scalar UI at `/reference` is a renderer over that spec.

When investigating an unfamiliar route, the right order is:

1. `scripts/alarm-api.sh --help <route>` — fast, machine-readable, scoped.
2. `https://api.claw-alarm.com/reference` — interactive, full surface, shows examples.
3. The worker source under `cloudflare-worker/src/api/groups/` and `cloudflare-worker/src/api/schemas/` — only when behavior is unclear from the schema alone (e.g. cross-field invariants like "one_off_local_date is required iff recurrence.type === 'none'").

## Local testing

Point the CLI at a local `wrangler dev` instance:

```bash
CLAW_ALARM_API_BASE_URL=http://127.0.0.1:8787 scripts/alarm-api.sh pair ABC-DEF
CLAW_ALARM_API_BASE_URL=http://127.0.0.1:8787 scripts/alarm-api.sh /v1/account/alarms
```

The base URL is read fresh on every invocation, so you can flip between local and production by toggling the env var.
