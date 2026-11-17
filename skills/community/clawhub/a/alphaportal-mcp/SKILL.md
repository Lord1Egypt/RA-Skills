---
name: alphaportal-fpx
description: >-
  Access AlphaPortal (AlphaRoute) school-bus data — students, stops, live bus
  GPS location, arrival notifications — from a shell with curl instead of
  running the alphaportal-mcp server. Capture the signed-in web app's refresh
  token ONCE (a paste-in-console one-liner, or the fpx browser bridge), then mint
  access tokens and curl the REST API directly. Use when you want AlphaPortal
  data without the MCP, in a script, or on a machine where the MCP isn't
  installed.
---

# AlphaPortal via curl (no MCP, no runtime bridge)

AlphaPortal's app (e.g. `cmsnc.alphaportal.app` — the `cmsnc` subdomain is the
school district) has **no bot wall** on its API (`api.alpharoute.app`): once you
hold a token, plain `curl` does every call — no browser extension at runtime.
Login itself is reCAPTCHA-gated and can't be scripted, so the credential is the
**refresh token** the web app stores in your signed-in browser. It's an 8-day,
reusable JWT; from it you mint a 30-minute access token with one unauthenticated
POST (no reCAPTCHA, no MFA).

So the flow is: **capture the refresh token once → mint an access token → curl.**

## 1. Capture the refresh token (once; repeat when it expires after ~8 days)

**Option A — paste-in-console (no fpx needed).** In a signed-in AlphaPortal tab,
open DevTools → Console and run:

```js
JSON.parse(localStorage.user).User.RefreshToken
```

Copy the value into your shell:

```sh
export ALPHAPORTAL_RT='<paste the refresh token>'
```

**Option B — fpx browser bridge** (needs the ContextMint Bridge extension — from
https://github.com/nullnet-app/contextmint-bridge/releases; Chrome: load the chrome
zip unpacked; Safari isn't available yet, so use Chrome for now — plus a signed-in
`*.alphaportal.app` tab). ContextMint Bridge is the fetchproxy extension renamed, same
maintainer; source is public at https://github.com/nullnet-app/contextmint-bridge — build
it yourself or verify a release zip with `shasum -a 256 -c contextmint-bridge-chrome-<version>.zip.sha256`:

```sh
npm install -g @fetchproxy/cli                              # provides `fpx`
fpx profile add alphaportal --domain alphaportal.app
fpx profile declare alphaportal --local-storage user       # declare scope BEFORE first pairing
fpx local-storage user -p alphaportal                      # first call prints a pair code → approve in ContextMint Bridge
export ALPHAPORTAL_RT=$(fpx local-storage user -p alphaportal | jq -r '.user | fromjson | .User.RefreshToken')
```

## 2. Mint an access token (each session, or when the last one is >30 min old)

```sh
export ALPHAPORTAL_TOKEN=$(
  curl -s -X POST https://api.alpharoute.app/AlphaCore/v1/public/refresh-token \
    -H 'Content-Type: application/json' \
    -d "{\"refreshToken\":\"$ALPHAPORTAL_RT\"}" | jq -r '.data.token'
)
```

If `ALPHAPORTAL_TOKEN` is `null`, the refresh token is expired/invalid —
re-capture it (step 1).

## 3. Core call pattern

Every read is a GET with the bearer token; the envelope is `{success,data,message}`,
so pipe `.data` to `jq`.

```sh
alpha() { curl -s "https://api.alpharoute.app/$1" -H "Authorization: Bearer $ALPHAPORTAL_TOKEN"; }

# your students (grab each studentId here first)
alpha AlphaPortal/v1/user-students/list | jq '.data.students[] | {studentId, name, gradeName}'

# live bus GPS for a student's PM run (shift 0=AM, 1=PM)
alpha AlphaPortal/v1/user-students/vehicle-location/218652901/1 | jq '.data.location'

# arrival/departure notifications
alpha AlphaPortal/v1/notifications/list | jq '.data.notifications[] | {title, body, creationDate}'
```

See `references/endpoints.md` for the full endpoint list, path variables, and
ready-to-run `jq` recipes.

## In context groups

The alphaportal MCP (not this curl helper) joins the **school** group on an mcp-host
gateway. Its one canonical read, answering one line per item with `view: "brief"`:

- **what's new** — `alphaportal_list_notifications`: the bus arrival/departure alerts,
  newest first, `<student>: <title> — <ISO date> — bus alert` (at most 20, then a
  `-- N of M shown` note; `-- none` when the feed is empty), inside the untrusted-data
  envelope because the text is the district's. A line whose text would start with `-- `
  or `\` gets one leading `\`, so a district title can never read as a note.

It takes no subject and no date range: the feed covers every student on the account,
and each line names its student. Nothing here is canonical for what's due or what's on
(stops and the live bus location are lookups). A compound ask looks like "did the bus
get to school, and anything due at school?" — the group answers the bus part from this
read and the rest from the other school sources.
The MCP lifts its refresh token from a signed-in AlphaPortal tab over the browser bridge
when it holds none, so until it has one the group answers "needs your browser open"
for this source instead of an empty list.

## Status codes

- `401` — the access token expired (re-run step 2) or the refresh token died
  (re-capture, step 1).
- `400` with `developerMessage` — a required param is missing (e.g. a path
  `studentId`, or `studentId`/`radius` on a write).
- `success:false` in a `200` body — the API rejected the request; read
  `.developerMessage` / `.message`.

## Writes

Write endpoints (`radius-edit`, `setnotification`) exist and change real
transportation records; the `alphaportal-mcp` server gates them behind a
confirmation (a prompt, or a preview plus a one-time confirm token). This shell
skill has **no preview or confirmation** — curl just does it — so
treat every write as real and permanent. Request bodies are in
`references/endpoints.md`. The transportation-request submission flow is
deliberately undocumented here (its body was not fully verified).
