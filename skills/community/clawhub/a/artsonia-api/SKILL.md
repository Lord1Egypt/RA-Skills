---
name: artsonia-api
description: >-
  Access Artsonia (artsonia.com) student-art portfolios, comments, fans,
  teacher feedback, and downloads from a shell with curl instead of running
  the artsonia-mcp server — log in with a username/password form POST to get
  a session cookie, then curl the server-rendered member pages. Use when you
  want Artsonia data without the MCP, in a script, or on a machine where the
  MCP isn't installed.
---

# Artsonia via curl (no MCP)

Artsonia is a classic server-rendered `.asp` site — no public API, no JSON
store, no bot wall. All the data (students, portfolios, comments, fans,
feedback, awards, profile) lives in server-rendered HTML, and auth is a real
**username + password form POST** that hands back an HttpOnly session
cookie. No browser, no ContextMint Bridge extension, no `fpx` bridge is needed —
`curl` with a cookie jar reaches everything a signed-in parent account can.
(The MCP keeps `@fetchproxy/server` as an optional fallback transport for
some future walled endpoint, but nothing documented here needs it.)

This is the same data the `artsonia_*` MCP tools return, reached with `curl`
instead of a running server.

## One-time setup

```sh
export ARTSONIA_USERNAME=you@example.com
export ARTSONIA_PASSWORD='your-password'   # or: op read "op://Private/Artsonia/password"
JAR=~/.cache/artsonia-cookies.txt
mkdir -p ~/.cache   # ensure the jar's directory exists on a fresh box
: > "$JAR"   # fresh jar
```

## Log in (get the session cookie)

Read the password from stdin (`Password@-`) instead of putting it on the
command line — `--data-urlencode name=value` puts `value` in curl's argv,
which any local user can read via `ps`/`/proc` while the process runs. This
mirrors how the MCP itself sends the password: only in the POST body, never
on a command line.

```sh
printf '%s' "$ARTSONIA_PASSWORD" | curl -s -c "$JAR" -b "$JAR" -L \
  --data-urlencode "Username=$ARTSONIA_USERNAME" \
  --data-urlencode "Password@-" \
  --data-urlencode "TargetUrl=/members/" \
  --data-urlencode "Action=login" \
  -o /tmp/artsonia-login.html -w '%{http_code} %{url_effective}\n' \
  https://www.artsonia.com/members/login.asp
```

A successful login redirects away from `login.asp` (final URL ends in
`.../members/`) and leaves cookies in `$JAR`. If `url_effective` still ends
in `login.asp`, or `/tmp/artsonia-login.html` matches `You need to log
in|Parent \(or Fan\) Login`, the credentials are wrong — Artsonia has no
CSRF/`__VIEWSTATE` token, so a bad login is the only reason this fails.
Magic-link-only accounts can't use this (there's no password to POST).

Re-run this exact command any time a later request looks logged-out (see
"Session expiry" below) — `curl -c` overwrites the jar with a fresh session.

## Core call pattern

Every read is a `GET` through the jar; every write is a form-urlencoded
`POST` through the jar. Fetch to a file, then extract:

```sh
curl -s -b "$JAR" -c "$JAR" 'https://www.artsonia.com/members/' -o /tmp/dash.html
```

For the numeric ids every other endpoint needs (`artist_id`, `artwork_id`),
a plain regex on the `href` is enough and needs no extra tooling:

```sh
grep -oP '(?<=portfolio\.asp\?id=)\d+' /tmp/dash.html | sort -u
```

For the full structured fields (name, school, stats, notifications, awards,
…) don't re-derive selectors by hand — this repo already ships a
live-verified `node-html-parser` scraper (`src/parse.ts` → built
`dist/parse.js`) with one function per page. Build it once, then import it
in a one-liner and pipe the JSON to `jq`:

```sh
cd ~/git/artsonia-mcp && npm install && npm run build   # once, if dist/ is missing
node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { parseStudents } from '$(pwd)/dist/parse.js';
console.log(JSON.stringify(parseStudents(readFileSync('/tmp/dash.html', 'utf8'))));
" | jq '.'
```

`references/endpoints.md` has the ready-to-run curl command, `dist/parse.js`
import, and `jq` projection for every read and write tool, keyed to the same
paths and selectors the MCP uses.

## The one rule: resolve artist_id (and artwork_id) first

Every per-student/per-artwork endpoint needs a numeric id you can only get
from a parent call — never guess one:

1. `GET /members/` → `.artist-card` → `artist_id` (from each card's
   `portfolio.asp?id=` link).
2. `GET /artists/portfolio.asp?id=<artist_id>` → `.grid-item` that contains
   an `art.asp` link → `artwork_id`.

## Session expiry

Artsonia expires a session by **redirecting/rendering back to the login
page**, not a 401. After any GET/POST, check the response body:

```sh
grep -qE 'login\.asp|You need to log in|Parent \(or Fan\) Login' /tmp/out.html \
  && echo "EXPIRED — re-run the login step"
```

## Writes — real caveats from the MCP build

- **A 3xx is not proof a write persisted.** Artsonia's form handlers 302
  even on payloads they silently drop. Re-`GET` the page you just changed
  and confirm the field actually flipped before trusting a write.
- **Checkboxes submit `value=Y`, never `on`.** Sending `Field=on` is
  silently ignored by the server (still 302s, saves nothing).
- **The profile form is read-modify-write.** `/members/profile/`
  (`#TheForm`) bundles name/email/password/opt-ins in one form — re-POST
  every current field verbatim (blank the password fields, keep
  `DidChangePassword=N`), flipping only the one you're changing.
- **Never POST a password.** Leave `OldPassword`/`NewPassword`/
  `NewPassword2` blank/omitted.

See `references/endpoints.md` for the exact body of every write, and how to
re-read and verify each one.

## Artwork images (no auth needed)

Full-resolution images live on a public CDN — no cookie required, even for
private pieces:

```sh
curl -s -o "$artwork_id.jpg" "https://images.artsonia.com/art/full/$artwork_id.jpg"
curl -sI "https://images.artsonia.com/art/full/$artwork_id.jpg" | grep -i last-modified   # per-artwork upload date
```

Resolutions (small→large): `small` `medium` `large` `xlarge` `full`.

## Notes

- Reads/writes both go through the member site (`www.artsonia.com`);
  nothing here needs the `fetchproxy`/browser-bridge path the MCP keeps as
  an optional fallback.
- Comment-item markup on `/museum/art.asp` is unverified upstream (both
  captured accounts had 0 comments) — `references/endpoints.md` flags it.
- This project is developed and maintained by AI (Claude).
