---
name: evite-api
description: >-
  Query and act on Evite (evite.com) events, guest lists, RSVPs, and
  messages from a shell with curl and a cookie jar — instead of running
  the evite-mcp server. Does a headless EVITE_EMAIL/EVITE_PASSWORD login
  against evite.com's internal /services/, /ajax/, and /tsunami/ APIs, no
  browser or extension involved. Use when you want Evite data/actions
  without the MCP, in a script, or on a machine where the MCP isn't
  installed. Triggers on "check my Evite", "Evite guest list", "RSVP on
  Evite from the shell", "curl Evite", "evite-api skill".
---

# Evite via curl (no MCP)

Evite has no public API — this hits the site's own internal `/services/`
(+ `/ajax/`, `/tsunami/`) layer using session cookies, exactly like
evite-mcp does. **This is a curl skill, not fpx**: Evite's login is a
plain CSRF-protected Django form POST, and reads/writes with the
resulting cookies are **not** bot-walled (Cloudflare sits in front but
doesn't trip on a plain `curl`/Node request carrying a valid session) —
so the whole flow runs server-side with a cookie jar. No signed-in
browser tab, no ContextMint Bridge extension, no bridge.

Auth model: session cookies `x-evite-session` + `evtsession`, plus a
CSRF cookie `csrftoken` sent back as the `X-CSRFToken` header on every
write. The CSRF cookie **rotates** — re-read it from the jar immediately
before each write, never cache it.

## One-time login (per shell session, until the jar's session expires)

```sh
export EVITE_EMAIL=you@example.com EVITE_PASSWORD=yourpassword   # or: op read op://.../evite/password
JAR=/tmp/evite-jar.txt
touch "$JAR" && chmod 600 "$JAR"   # jar holds the live session cookie — restrict before writing
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'

# 1. Prime: GET the homepage to obtain the csrftoken (+ anonymous session) cookies.
curl -sS -c "$JAR" -b "$JAR" -A "$UA" 'https://www.evite.com/' -o /dev/null

# 2. Login: POST creds with the primed jar + X-CSRFToken + Origin/Referer (Django's
#    HTTPS CSRF check needs all three; a cold POST without them 403s).
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -c "$JAR" -b "$JAR" -A "$UA" \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -H 'Origin: https://www.evite.com' -H 'Referer: https://www.evite.com/' \
  -d "$(jq -n --arg e "$EVITE_EMAIL" --arg p "$EVITE_PASSWORD" '{email:$e,password:$p}')" \
  'https://www.evite.com/ajax_login'
```

A `200` means the jar now holds the authenticated cookies
(`x-evite-session`, `evtsession`, a freshly-rotated `csrftoken`,
`x-evite-features`) and a JSON body with `full_name`/`user_id`/`token`.
`401 {"error":"Invalid Email Address / Password"}` = bad creds; `403
{"error":"HTTP_403"}` = the priming GET was skipped, or its `csrftoken`
wasn't echoed back.

## Reads: jar + `Accept: application/json`

```sh
curl -sS -b "$JAR" -c "$JAR" -H 'Accept: application/json' \
  'https://www.evite.com/services/events/v1/?filterBy=all&type=invitation' | jq .
```

Always pass `-b "$JAR" -c "$JAR"` **together** (read AND rewrite the same
file) — Evite occasionally re-sets cookies even on a GET, and a write's
`csrftoken` rotation must land back in the jar for the next call.

## Writes: jar + fresh `X-CSRFToken` + `Content-Type: application/json`

```sh
CSRF=$(awk -F'\t' '$6=="csrftoken"{v=$7} END{print v}' "$JAR")
curl -sS -b "$JAR" -c "$JAR" -X PUT \
  -H 'Content-Type: application/json' -H "X-CSRFToken: $CSRF" \
  -d '{"rsvpResponse":"yes","numberOfAdults":2,"numberOfKids":0}' \
  "https://www.evite.com/services/event/v1/$EVENT_ID/guests/$GUEST_ID"
```

Re-read `$CSRF` from `$JAR` **right before every write** — a stale value
403s. If a write still 401/403s with the cookie unchanged in the jar
(check `awk -F'\t' '$6=="csrftoken"'  "$JAR"` before/after), the session
itself expired: redo the one-time login.

Full endpoint list (every read + write, real paths/bodies, `jq`
recipes) is in `references/endpoints.md`.

## Notes / caveats

- **Two write bodies are still unverified upstream** (tracked as
  evite-mcp issue #3): `send_message` (`POST
  /tsunami/v1/services/event/{id}/guest/{gid}/messages`) and
  `send_invitation` (`POST /services/event/v1/{id}/send/`) — only the
  endpoints were captured live, not their exact request bodies. The MCP
  (and this skill) send `{"message": "..."}` / `{}` as the best-known
  shape; treat those two as slightly less certain than the rest.
- `list_templates` is HTML scraping (`GET /invites/{category}/`), not
  JSON — see the reference for the extraction pattern.
- **Writes here really mutate Evite** — RSVPs, cancellations,
  broadcast emails to real guests. There's no MCP-side confirm-gate in
  this skill: you are the confirm gate. Test broadcasts/sends only
  against a throwaway event with a blackholed `@example.com` guest.
- This project (evite-mcp) is developed and maintained by AI (Claude).
