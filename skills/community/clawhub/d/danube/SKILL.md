---
name: danube
description: Governed tool access for your agent — one Danube API key unlocks your organization's own tools plus a large, growing catalog of ready-made services. Search, inspect, and execute tools over native MCP or plain curl, with explicit confirmation before anything that writes, sends, spends, or deletes.
metadata:
  openclaw:
    emoji: "🌊"
    homepage: https://docs.danubeai.com/sdk/openclaw
    requires:
      env:
        - DANUBE_API_KEY
      bins:
        - curl
    primaryEnv: DANUBE_API_KEY
    envVars:
      - name: DANUBE_API_KEY
        required: true
        description: Danube API key from https://danubeai.com/dashboard/api-keys (API Keys in the dashboard sidebar; an opaque token — no fixed prefix)
    always: false
---

# Danube — Governed Tool Access for Agents

Danube makes an organization's own tools — plus a large and growing catalog of ready-made services — callable by AI agents through a single API key, with permissions, spending limits, and an audit trail handled by the platform. The catalog changes constantly and includes tools the user's organization connected privately, so **never assume what is available — search first.**

## Guardrails (read these first)

- **Read freely, act with consent.** Discovery — listing services, searching tools, reading schemas, checking ratings, balances, or limits — needs no confirmation. Before any action that **writes, sends, posts, deletes, purchases, spends wallet funds, stores a credential, changes spending limits, or creates/updates/deletes a skill or workflow** — and before **any batch execution** — show the user the exact tool and parameters and get an explicit "yes".
- **Honour the confirmation handshake.** If `execute_tool` comes back with `_meta.confirmation_required: true`, that call will not run until someone consents: show the user the tool and the `parameters` from the response, get an explicit yes, then call again with the `confirm_token` (valid 5 minutes). Never call again with the token without asking. **Re-send your own original parameters, not the ones the response displayed** — those are passed through the redactor first, so a credential-shaped value comes back as `[REDACTED:…]`, while the token is signed over what you actually sent; echoing the masked form back invalidates it.
- **Two separate things raise that handshake, and only one of them is a setting on the key.** Either the account's key carries `require_confirmation`, *or* the tool itself demands consent from every caller whatever the key says — so a handshake can arrive on a key that has the setting switched off, and is not evidence that someone switched it on. The tool-side trigger covers two cases. A tool row marked `metadata.require_confirmation` always needs the token, and that is every **write** tool of the catalog's infrastructure connectors — thirteen of them, across eight of the seventeen services: `PostgreSQL - Execute Statement`, `MySQL - Execute Statement`, `ClickHouse - Execute Statement`, `Redis - Set`, `Redis - Delete`, `Redis - Expire`, `Apache Kafka - Produce Message`, `Kubernetes - Restart Rollout`, `Kubernetes - Scale Deployment`, `AWS DynamoDB - Put Item`, `AWS DynamoDB - Update Item`, `AWS DynamoDB - Delete Item` and `AWS Lambda - Invoke`. Every one of them says a confirmation is required in its own published description, so you can see it coming before you call (seven word it as "every call needs an explicit confirmation"; the rest say "with a confirmation on every call" or just "with a confirmation"). An organization's own connected-system copy of the same connector carries the flag too, and the only thing that lifts it there is an admin setting that system's policy to `writes: "allowed"` — a key carrying `require_confirmation` would still ask. The second case is narrower than it sounds: a write through a connected system's generic `<Service> - Request` tool when the service's access policy sets `http.writes: "consent"`. It is the HTTP surface only — a write through a connected database's `Query` tool does not reach this trigger. Over REST the `409` reports `error.details.reason` as `"api_key"` or `"service_policy"`, and adds "This service's access policy requires a confirmation for every write." to the message for the latter. Read `reason` by precedence rather than as the sole cause: the key-side trigger wins the label whenever it applies, so `"service_policy"` is the informative one — it means the key does *not* have the setting on. **Over MCP you cannot tell** — `_meta` carries `confirm_token`, `expires_in` and `parameters` and drops `reason` — so read the handshake as this tool's own requirement rather than as a fact about the account's settings. Either way the response is not a failure and the answer is the same: show, ask, re-send with the token.
- **Its silence is not a safety verdict.** The destructive test in front of that gate reads the publisher's `metadata.destructive` **first, and whatever it says wins**; only when the tool row carries no such flag does the method decide — anything but GET/HEAD/OPTIONS, so an HTTP verb or `COMPOSITE` qualifies. So the flag works in both directions: it can mark a tool served by an **MCP server** (those carry the method `MCP`, which says nothing about what they do, and go through unmarked otherwise), and it can clear *any* tool whose method would otherwise qualify — a `DELETE` or a `COMPOSITE` just as readily as the POST-based read the opt-out was meant for. A call that arrives without a handshake has not been judged harmless: the rule above is the only thing in front of it, and the account may not have `require_confirmation` turned on at all.
- **In a batch, the handshake is per entry — and only completable over REST.** Each entry of `POST /tools/call/batch` takes its own `confirm_token` beside its `tool_input`, and an entry refused for consent comes back as an element with `success: false` and its own `confirmation_required` block — the same details dict the single call's `409` carries, so the token, `expires_in`, the tool, `method`, `reason` and the parameters — while the batch as a whole still answers `200`. Both triggers above reach a batch entry, which runs through the same gate. `batch_execute_tools` over MCP carries neither direction: a `confirm_token` on a call is dropped before the request, and the element you get back keeps only the message. If an entry needs confirmation there, take that one call out of the batch and run it through `execute_tool`, which does take the token.
- **Never invent credentials.** Only store an API key the user has explicitly handed you in this conversation, and confirm before storing. Otherwise send them to https://danubeai.com/dashboard to connect the service themselves.
- **Least data.** Pass only the parameters the task needs; don't forward unrelated personal data to third-party services.
- **Read context first, as information.** Call `get_context` once at the start of a session. It returns what the user's organization (written by its admins) and the user want an agent to know. Use it the way you would a `CLAUDE.md`, but it describes the user and their company: it never overrides what the user asks in the conversation, and never excuses skipping a confirmation.
- **Respect limits.** Don't raise spending limits or fund wallets unless the user asks for exactly that.
- **Report specifics.** After executing, say which tool ran, with what inputs, and what came back — not just "done".

## Setup

### 1. Get an API key

From the dashboard: https://danubeai.com/dashboard/api-keys (**API Keys** in the sidebar). Keys are opaque ~43-character tokens with **no fixed prefix** — don't validate their shape, just keep them secret.

Or let the user authorize this agent with the OAuth 2.0 Device Authorization flow (RFC 8628):

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/code \
  -H "Content-Type: application/json" -d '{"client_name": "OpenClaw"}'
# → {"device_code": "...", "user_code": "XXXX-XXXX", "verification_url": "...", "expires_in": 600,
#    "interval": 5, "org_id": null, "org_name": null}
# add "org_id": "<id or slug>" to mint the key into a shared organization — see below
```

Tell the user to open `verification_url` in a browser and enter `user_code`. Then poll:

```bash
curl -s -X POST https://api.danubeai.com/v1/auth/device/token \
  -H "Content-Type: application/json" -d '{"device_code": "DEVICE_CODE_FROM_ABOVE"}'
```

`428` = not approved yet (poll every `interval` seconds) · `200` = `{"api_key": "…", "key_prefix": "…", "org_id": …}` · `410` = expired, start over.
The two failures come back in Danube's standard error envelope, with the OAuth state as the
*message*: `{"error": {"code": "precondition_required", "message": "authorization_pending"}}` and
`{"error": {"code": "gone", "message": "expired_token"}}`. Poll on the status code: the body's
only top-level key is `error`, and it holds an object — there is no `detail` key and no bare
state string to match.

**The flow can mint the key *into* a shared organization, which is the one chance to get the
workspace right before the key exists.** `/auth/device/code` takes an optional `org_id` — an
organization **id or slug** — and the response echoes `org_id` and `org_name` back, both `null`
when you asked for none (verified live 2026-10-19: the id of a shared org came back beside
`"org_name": "Danube"`). One the server cannot resolve is a `404` in the ordinary envelope,
`{"error": {"code": "not_found", "message": "Organization not found"}}`, raised before any code
is created. Membership is *not* checked at this point — nobody is signed in yet — it is checked
when the user enters the `user_code`: a user who is not a member of the organization the device
asked for is refused with a `403` ("This device asked to join an organization you are not a
member of") and **the code stays pending**, so a colleague who *is* a member can still authorize
that same code. From your side an organization nobody present belongs to therefore looks like
`428` until the code expires, rather than an error. A *personal* organization is accepted here
too — it is not rejected, it simply gives you the default described next — so passing one buys
nothing.

What it buys is the thing the *Tools the user's organization registered* section below is about:
the minted key is stamped with that organization, and an org-owned key acts for it **with no
`danube-org-id` header at all**. Ask for it only when the user named a shared organization to
work in, and don't pass their personal one thinking it is the neutral choice — you don't need to.
With no `org_id` the key is stamped with the user's personal organization, and that is *not* the
narrowing the header version of it would be: only a **shared** org switches the request's
context, so a personal-org key keeps the ordinary personal behaviour and still spans every
organization the user belongs to.

**Respect `interval`, and know that a fourth status can appear.** The code is good for
`expires_in` seconds (600, i.e. ten minutes) and the two endpoints carry rate limits of their
own: 10 requests/minute on `/auth/device/code` and 30/minute on `/auth/device/token`. These
calls are unauthenticated, so there is no key to count them against — the bucket is keyed by
the client address *as the server sees it*, which behind a hosted deployment's edge may be far
more widely shared than your own machine or egress. Treat the 30/minute as a limit you could
meet even when nothing is wrong. At the advertised `interval` of 5 seconds you poll 12 times a
minute, which is the rate the flow is designed around; poll tighter and you are spending someone
else's headroom as well as your own.

The resulting `429` is **not** one of the three statuses above, so don't read it as a failed
authorization — it says nothing about whether the user has approved. Back off by `Retry-After`
(see *The two `429`s* below) and carry on polling **the same `device_code`**: a rate-limited
poll never reaches the handler, and an ordinary pending one changes nothing, so the code stays
valid for the rest of its ten minutes. Starting a fresh flow instead spends one of the
10/minute on the other endpoint and makes the user enter a new `user_code`.

### 2. Make the key available to OpenClaw

Set `DANUBE_API_KEY` in the environment, or in `openclaw.json`:

```json5
{ skills: { entries: { danube: { apiKey: "YOUR_DANUBE_API_KEY" } } } }
```

### 3a. Connect natively over MCP (recommended)

OpenClaw has a built-in MCP client. Register Danube's server once and its tools become ordinary OpenClaw tools (`search_tools`, `execute_tool`, …):

```bash
openclaw mcp set danube '{"url":"https://mcp.danubeai.com/mcp","transport":"streamable-http","headers":{"danube-api-key":"YOUR_DANUBE_API_KEY"}}'
openclaw mcp doctor danube --probe
```

Use the real key value in `headers` (not `${DANUBE_API_KEY}`). The server also speaks MCP OAuth: use `"auth":"oauth"` instead of `headers`, then `openclaw mcp login danube`.

**What the probe counts is not 33, and the names it prints are not bare.** Live on 2026-10-27
against OpenClaw 2026.10.8, `openclaw mcp probe danube --json` put `servers.danube.tools` at
**33** — the number `tools/list` returns — while the flat `tools` array beside it held **37**, each
entry written `danube__<tool>`: `danube__search_tools`, `danube__execute_tool`,
`danube__get_context`, and so on. The four extras are the client's own bridges to the other two MCP
surfaces, built from the capabilities the handshake advertises rather than served by Danube:
`danube__prompts_list`, `danube__prompts_get`, `danube__resources_list` and
`danube__resources_read`. So 37 is the right count to see there, 33 the right count of *Danube*
tools, and `danube__prompts_list` comes back empty however often you call it — this server
registers no prompt at all (*Beside its 33 tools* below). The prefix is the client's, not Danube's,
and the separator has differed between OpenClaw versions, so match a tool on the part after it:
everywhere in this file tools are named bare, `search_tools` and `execute_tool`.

**Signing in now means a Danube account, not a pasted key — and the refresh token has a trap
worth knowing before you automate around it.** Until 2026-10-04 `/oauth/authorize` asked the user
to paste an API key and handed it straight back as a one-year token. It now validates the request
and redirects the browser to Danube's own consent page, where the user signs in and approves the
client (verified live 2026-10-05: a well-formed authorize request answers `302` to
`https://danubeai.com/oauth/consent?request=…`). What that changes for you:

- **PKCE is mandatory** — `code_challenge_method=S256`, no exceptions; without it the endpoint
  answers `400 invalid_request` before anything else. Registration is open, so an unknown
  `client_id` is still accepted. The metadata at
  `https://mcp.danubeai.com/.well-known/oauth-authorization-server` is authoritative for the four
  endpoints and advertises `authorization_code` and `refresh_token`.
- **The `scope` you ask for is a label, and the consent screen never shows it.** The metadata
  advertises five (`tools:read`, `tools:execute`, `services:read`, `skills:read`,
  `context:read`), but nothing validates the parameter against them: live on 2026-10-07 an
  authorize request carrying `scope=not_a_real_scope admin:everything` answered the same `302`
  to the consent page as one carrying no `scope` at all — there is no `invalid_scope` path. The
  consent screen shows the client's self-asserted name, the redirect host and the workspace
  picker, and no list of permissions, so what the user approves is *who* and *which workspace*,
  never *what*. Past consent the string is dropped rather than narrowed: the approval does not
  carry it to the grant, every connection is created with the full default set, and the token
  response echoes that set back however little you asked for. Nothing enforces it downstream
  either — the access token resolves to the connection's hidden key, which is injected as an
  ordinary `danube-api-key` carrying no permissions — so all 33 MCP tools stay callable. Like
  `?tools=` below, read it as a declaration, not a permission boundary: asking for less is not a
  way to narrow a connection. What does narrow one is a key you issue yourself with
  `allowed_services` / `allowed_tools` set on it, used in place of an OAuth connection; an
  organization can also deny tools for anything acting in its workspace, which reaches a
  connection approved for that organization.
- **The user picks a workspace on the consent screen, and the two choices are not symmetrical.**
  Approving for a **shared organization** binds the connection to it: the grant's hidden key
  carries that org, every backend call is made for it without the client sending anything, and
  the organization's internal tools, shared credentials, parameter defaults, skills and context
  layer are what the connection sees. Approving for **"Personal"** does *not* do the mirror
  image — it does **not** narrow the connection to personal-only. The personal org is
  deliberately never forwarded as the acting workspace (it would select the Personal workspace
  and hide every shared org), so such a connection behaves like an ordinary personal API key
  with no workspace header: it still spans every organization the user belongs to. So read
  "Personal" at consent as "don't pin this to one organization", not as "keep this out of my
  organizations". A user who wants the second thing cannot get it by narrowing this connection:
  the key behind a connected app is created with no permissions, is never shown, and the
  Connected apps page only lists and revokes. The way to hand an agent a restricted credential
  is still a pasted API key with `allowed_services` / `allowed_tools` set on it in the
  dashboard, used instead of an OAuth connection.
- **Tokens are short-lived and rotate.** The access token (`dmcp_at_…`) lasts one hour; the
  refresh token (`dmcp_rt_…`) is spent on every use and replaced, with a 90-day idle expiry.
  **Re-presenting a refresh token you have already exchanged revokes the whole connection** —
  the user has to approve the client again. There is a 30-second grace for the genuine race (a
  rotation whose response you lost, two refreshes in flight at once), which answers
  `invalid_grant` "Refresh token was already used" and leaves the grant alive; past that window
  the same replay is read as theft and the connection is revoked. So store only the newest pair
  and never retry a refresh with a token you kept "just in case". Both outcomes are
  `invalid_grant`, so the error alone will not tell you which one you just caused.
- **Read the `401` before deciding what to do**, because three different things answer `401` and
  only one of them is fixed by refreshing. A `WWW-Authenticate` carrying `error="invalid_token"`
  is the access token expired or revoked — refresh it. Without that marker the message is the
  tell: "API key required…" means no credential reached the server at all, and "Invalid API key"
  means one did and was rejected (a revoked or mistyped key). Neither of those two is a token
  problem, so refreshing or re-running sign-in will not clear them.
- **Revoking** is `POST /oauth/revoke` (RFC 7009), or the user's **Connected apps** page at
  https://danubeai.com/dashboard/connected-apps; removing someone from an organization revokes
  their connections too. A revoked token can keep working for up to a minute — the server caches
  an introspection for 60 seconds — so don't read one more successful call as the revoke having
  failed.
- **Pasted keys were not deprecated by any of this.** A bearer token without the `dmcp_at_`
  prefix is still treated as an API key, so the `headers` form above and every connection made
  before 2026-10-04 keep working unchanged.

**The key header has an alias on this server, and carrying it over to `curl` fails quietly.** The
MCP server reads the key from either `danube-api-key: <key>` or `Authorization: Bearer <key>`, and
the `401` it sends when neither is present names both. The REST API accepts only the first, and
what the second does there depends on the route (both verified live 2026-10-03): a route that
*requires* a key refuses it — `/v1/tools/search` answered
`401 {"error":{"code":"unauthorized","message":"API key required"}}`, a message that reads as "you
sent no key" when the key was simply in the header REST reserves for a dashboard JWT — while a
route whose auth is *optional* ignores it without saying so: `/v1/services?limit=3` answered `200`
with byte-for-byte the response the same call returns carrying no credentials at all, so whatever
the key would have unlocked is silently missing. Keep `curl` on `danube-api-key`. Hand-probing the
MCP endpoint has two more traps worth knowing before you read a failure as a bad key — POST is the
only verb that does anything, and an unauthenticated request never reaches routing — both in
`{baseDir}/references/troubleshooting.md`.

To keep the tool list small, append `?tools=core` to the URL, or a comma list such as
`?tools=core,workflows`; without it all 33 tools are described to the model. The groups that list
tools are `core` (11 — `get_context`, discovery, execution, credentials, and `report_tool`),
`workflows` (6), `wallet` (6), `skills` (5), `feedback` (4 — `submit_rating`, `get_my_rating`,
`get_tool_ratings`, `get_recommendations`) and `context` (1 — `update_context`). `core` is added
to whatever you ask for, so search, execute and `get_context` can't be filtered out by accident (`?tools=wallet` lists 17). Unrecognised names are dropped silently: a
typo alongside a valid group just gives you fewer tools than you asked for (`?tools=core,workfows`
lists the same 11 as `?tools=core`), and if *none* of the names is a real group the parameter is
ignored altogether and you get the full 33. Either way it fails quietly, never with an error.
**Capitalisation and stray spaces are not among the ways to get it wrong**, though, so don't let
that silence make you over-careful with the spelling: each name is lower-cased and stripped
before it is matched, so `?tools=CORE` is `?tools=core` and `?tools=%20Core%20,%20Workflows%20`
is `?tools=core,workflows`. All of this verified live on 2026-10-23 against
`https://mcp.danubeai.com/mcp`, counting the `tools/list` reply: no parameter 33, `?tools=core`
11, `?tools=CORE` 11, that spaced and capitalised pair 17, and `?tools=workfows` on its own 33.
Re-counted on 2026-10-28, every number above still held: `?tools=core` 11, `?tools=context` 12,
`?tools=feedback` 15, `?tools=skills` 16, `?tools=wallet,workflows` 23, `?tools=nonsense` 33. Six
counts re-taken on 2026-10-29 were unchanged again — no parameter 33, `?tools=core` 11,
`?tools=context` 12, `?tools=feedback` 15, `?tools=skills` 16, `?tools=wallet,workflows` 23 — and
`?tools=nonsense` was not among them that day. All seven, that one included, were re-counted
unchanged on 2026-10-30, and all seven again on 2026-10-31.

**There is a seventh group, `website`, and it lists nothing.** Its four tools reached the server on
2026-10-28 but are withheld from every listing until the MCP deployment is told to show them, which
the hosted one is not: `?tools=website` returned `core`'s 11 and nothing else that day, and the
same on 2026-10-29, 2026-10-30 and 2026-10-31, so asking for it is harmless and gains you
nothing, and the total stays 33. If you ever need to know whether
a deployment *does* list them, check the right flag — **two independent flags on two apps** are
involved here. The listing is gated on a setting of the **MCP** app, while
`GET /v1/website-tools/status` reports the **backend**'s (it answered `enabled: false` beside
`worker_online: false` on 2026-10-28, and the same on every reading since, through 2026-10-31 —
the whole body is below). They
are meant to be turned on together, and on the hosted server neither is, but a `status` reading
`enabled: true` on its own would not prove the four are listed — count `tools/list`.

Two things about that one route, since this file is sending you to it. **It wants to know who you
are** — unlike `/v1/stats/public` and `/tools/{id}/describe`, it is mounted behind the ordinary
profile dependency, so an unauthenticated call is a `401` rather than the body (live 2026-10-29,
2026-10-30 and 2026-10-31: `401` bare, `200` with `danube-api-key`; a signed-in dashboard session's JWT is accepted on the
same dependency). And **the `scope` field in its answer is not about your key.** The full body
reads `{"enabled": false, "worker_online": false, "builds_per_day": 5, "scope":
"read_only_signed_out"}`, and that last value is a string literal in the route rather than a
verdict on the access you called with, so every caller reads the same value whatever their key
allows. The two booleans are the answer you came for; don't read `scope` as a permission check
that failed.

**The filter narrows `tools/list` and nothing else.** `tools/call` is deliberately not filtered, so
a connection opened with `?tools=core` can still run a tool from a group it never listed, as long
as it knows the name — live on 2026-09-23, `get_tool_ratings` and `get_spending_limits` both
returned normally over a `?tools=core` connection whose `tools/list` held ten tools (eleven since `get_context` joined `core`). That is
convenient (no reconnecting to rate a tool you just ran) and worth not misreading in the other
direction: the parameter is a context-size setting, not a permission boundary. Nothing on the
connection restricts which of the 33 tools may be called. A key's own `allowed_services` /
`allowed_tools` permissions, set in the dashboard, are a different control and don't close that
gap either — they scope which *marketplace* services and tools the key may search and execute, not
which of Danube's own MCP tools it may use.

**Every one of the 33 tools carries MCP annotations, and they describe the Danube verb rather
than the tool it carries.** Each entry of `tools/list` comes with the standard
`readOnlyHint` / `destructiveHint` / `idempotentHint` / `openWorldHint` quartet, so an OpenClaw
client that gates on them has something to read before it calls. Read them as a statement about
the Danube tool you are calling, not about the marketplace tool it runs — which is the whole
trap, because the two most consequential tools are the ones whose hint can't know:
`execute_tool` and `batch_execute_tools` are both stamped `destructiveHint: true` with
`openWorldHint: true` **always**, whether the call behind them sends an email or lists your
Gmail labels. So a client prompting on `destructiveHint` prompts on every catalogue call
including pure reads, and a `destructiveHint: true` there is not evidence the tool being run
writes anything. The marketplace tool's own flag is a different field entirely — the
publisher's `metadata.destructive`, which drives the platform's `confirm_token` gate described
above.

The `readOnlyHint: true` direction is the dependable one: the 16 tools carrying it are exactly
the discovery and inspection calls this skill says need no confirmation — `list_services`,
`search_tools`, `get_service_tools`, `describe_tool`, `fetch_result`, `get_context`,
`get_wallet_balance`, `get_spending_limits`, `get_agent_info`, `list_workflows`,
`get_workflow_execution`, `search_skills`, `get_skill`, `get_my_rating`, `get_tool_ratings` and
`get_recommendations`. **Nine** tools carry
`destructiveHint: true` (`execute_tool`, `batch_execute_tools`, `store_credential`,
`execute_workflow`, `fund_agent_wallet`, `update_skill`, `delete_skill`, `update_workflow`,
`delete_workflow`), and four carry `openWorldHint: true` (`execute_tool`,
`batch_execute_tools`, `execute_workflow`, `fund_agent_wallet`).

**The fourth hint is populated as well.** Live on 2026-10-30 and re-counted unchanged on
2026-10-31, `idempotentHint: true` is on **24** of the 33: all 16 read-only ones, where a repeat
is trivially safe anyway, plus **eight** writes — `set_parameter_defaults`, `store_credential`,
`submit_rating`, `update_skill`, `update_workflow`, `update_spending_limits`, `delete_skill` and
`delete_workflow`. The nine writes reading `false` are the informative set: `execute_tool`,
`batch_execute_tools`, `execute_workflow`, `fund_agent_wallet`, `create_skill`, `create_workflow`,
`register_agent`, `report_tool` and `update_context`. Read it as "is a repeat of this call safe",
and note that here the always-on value errs the *opposite* way from `destructiveHint`:
`execute_tool` and `batch_execute_tools` read `false` whatever they run, so this hint never
promises a retry is harmless. Where the behaviour is one this file already describes, the two
agree — `submit_rating` upserts your own rating, which is why it sits on the idempotent side,
while `update_context` defaults to `mode="append"`, so a repeat adds a second paragraph rather
than rewriting the first (*Context* below; `expected_version` is the guard). The one `false` worth
not over-reading is `report_tool`: a repeat there is deduped rather than discarded, and
`{baseDir}/references/troubleshooting.md` says what the bump actually changes. All four values are
hand-declared per tool in `mcp/mcp_server.py` rather than derived from anything the tool does, so
a wrong one is possible — they stay a coarse client-side signal, and the ask-first rule above is
what decides.

**Don't read the hints as this skill's consent list, though — eight tools that change something
are not flagged destructive.** `update_spending_limits`, `create_skill`, `create_workflow`,
`update_context`, `register_agent`, `set_parameter_defaults`, `submit_rating` and `report_tool`
all come through with `readOnlyHint: false` **and** `destructiveHint: false`, and three of them
— changing spending limits, creating a skill, creating a workflow — are things the guardrails
at the top of this file tell you to confirm. The hints are a coarse client-side signal; the
ask-first rule above is the one that decides.

**Of the other five, two carry an ask-first rule of their own further down this file, and only
three are genuinely yours to call unasked.** The guardrail's list opens with the word **writes**,
which is broad enough to cover all five, so none of them is excluded by that list on a plain
reading — don't resolve the tension by deciding for yourself which writes count. This file resolves
it explicitly instead, and here is the whole of it. Two have their own instruction and it stands:
*Wallet & agents* says to get an **explicit yes** before `register_agent`, because it creates a
separate account that cannot be deleted, holding an unrestricted API key returned once, and
*Context* says of
`update_context` "it is a write, so ask first" before you store a durable fact about the user.
The remaining three — `set_parameter_defaults`, `submit_rating` and `report_tool` — are the ones
you are free to call without stopping: each writes to Danube's own records rather than to a
service the user connected, none spends anything, and none deletes anything. For
`set_parameter_defaults` it goes further and tells you to save a confirmed identifier **without
asking first**, then say in one line what you saved (*Working with tools* below). That is a default
this file sets deliberately, not the guardrail being overridden in passing.

So: those three, and nothing else by analogy. An action that leaves the user's account — sends,
posts, spends, stores a credential, or touches a skill or workflow — needs a yes however
unflagged its hints are, and a write you are unsure about gets asked about. And the licence on
two of the three is narrower than "no confirmation needed" sounds, because **a rating and a report
are neither private nor reversible.** Both reach the tool's publisher (a report lands in that
publisher's queue), a rating's stars also feed a **public, keyless** per-tool average, and neither
has a delete route: re-rating overwrites your own rating (`submit_rating` upserts), while a filed
report cannot be withdrawn at all. So rate or report only from your own experience of a call you
actually made, and tell the user you did it rather than leaving it silent.

### 3b. Or use plain `curl` — no MCP needed

Every capability below is also a REST call against `https://api.danubeai.com/v1` with the header `danube-api-key: $DANUBE_API_KEY`. Copy-paste recipes: `{baseDir}/references/rest-api.md`.

## Working with tools

Every task follows **Explore → Inspect → (Confirm) → Execute → Report.**

| Goal | MCP tool | REST |
|---|---|---|
| See what services exist | `list_services(query, limit, detail?)` — a `limit` over **25** silently drops to the compact form | `GET /services` |
| Find a tool for a task | `search_tools(query, service_id?, limit?, detail?)` | `GET /tools/search?query=…` |
| All tools of one service | `get_service_tools(service_id, limit?, detail?)` — `limit` defaults to **50** | `GET /services/{id}/tools` (no limit; returns every tool) |
| Full schema of one tool | `describe_tool(tool_id)` (the listings above summarise) | `GET /tools/{tool_id}/describe` (prefer it to the bare `GET /tools/{tool_id}` — see below) |
| Run a tool | `execute_tool(tool_id, parameters, fields?)` | `POST /tools/call/{tool_id}` with `{"tool_input": {…}}` — the wrapper is optional for the parameters and required for `fields` / `confirm_token` / `timeout_seconds`, see below |
| Run up to 10 at once | `batch_execute_tools(calls)` | `POST /tools/call/batch` |
| Inspect one tool before first use | `describe_tool(tool_id)` | `GET /tools/{tool_id}/describe` |
| Read a stored result back | `fetch_result(execution_id, path?, max_response_chars?)` | `GET /tools/executions/{execution_id}/result?path=…&max_chars=…` |
| Remember a per-service default | `set_parameter_defaults(service_id, defaults, tool_id?)` | `PUT /services/{service_id}/parameter-defaults` |

**`execute_tool` resolves a name by *searching*, so an identifier that names nothing runs the
nearest tool instead.** Over MCP the call takes `tool_name` as an alternative to `tool_id` — and a
`tool_id` that is not a valid UUID is not refused either, it is quietly re-read as a name. Both
land in the same place: the string goes through a five-result `search_tools`, an exact `name` match
wins, and **when nothing matches exactly the first result is executed**. The `match` signal
described under *Discovery tips* is not consulted on this path.

An identifier that really exists is safe, and for the reason given under *when you already know a
tool's exact name* below: the search pins a tool whose name or slug **is** the query to the top,
ignoring case and punctuation, ahead of every readiness and reliability re-ordering. So a
correctly spelled name or slug runs the tool you named — verified live on 2026-10-09, where the
slugs `hacker-news-get-top-stories-with-content` and `hacker-news-search-by-date` each ran their
own tool. What is not safe is an identifier you guessed, half-remembered or mistyped. Live the same
day, `tool_name: "Hacker News - Get Front Page Story Titles"` — a name no tool carries — ran
`Hacker News - Get New Stories With Content` and returned the *newest* stories as an ordinary
success, with nothing in `result` saying a different tool had run. And the nearest neighbour need
not be anything like what you asked for: a search for `"zzqq blorptacular frobnicate wibblesnorf"`
came back with three `match: "weak"` tools led by `DigitalOcean Droplets - Image Create` — which
is what a name that garbled would have resolved to. The call itself would then have failed as a
`bad_request` or stopped at the confirmation gate, since that tool is a write with three required
parameters, but where it resolved to is the point.

So pass the UUID whenever you have one, and when you pass a name you did not just read off a
search result, check `_meta.tool_id` and `_meta.tool_name` — which name the tool that actually
ran — before you believe the payload. One nuance if you call the same name twice: only an exact
`name` hit is remembered (five minutes, per key and acting organization), so a best guess is
re-searched every time and can land somewhere else as the catalogue shifts.

**No execution path other than that one resolves a name.** Over REST, and for each entry of
`batch_execute_tools`, the identifier goes to the backend, which matches a UUID on `id` and
anything else on `slug` **exactly** — so a slug is a precise lookup there, and a tool's display
name is simply a miss. Live on 2026-10-09 one batch carried both spellings of the same tool:
`"hacker-news-get-top-stories-with-content"` answered `success: true`, while
`"Hacker News - Get Top Stories With Content"`, the row's real name, answered `success: false`
with `error: "Tool not found"`. A batch entry's parameters belong in `tool_input`; **over MCP**
`parameters` and `params` are accepted as aliases for it, as `params` is for `execute_tool`'s
`parameters`, but REST reads neither on a batch entry — send `tool_input` there or the tool runs
on empty input.

**On a *single* REST call the `tool_input` wrapper is optional for the parameters and required
for `fields`, `confirm_token` and `timeout_seconds` — the second half is the one worth
remembering.**
`POST /v1/tools/call/{tool_id}` reads the whole body as the tool's input when the body carries
no `tool_input` key (`body.get("tool_input", body)`, `routers/tools.py`), so `{"limit": 2}` and
`{"tool_input": {"limit": 2}}` run the same call — both verified live 2026-10-22 on
`Hacker News - Get Top Stories With Content`, each answering with two stories and
`request_params: {"limit": 2}`. What the bare shape loses is the controls that ride *beside*
`tool_input`: `fields`, `confirm_token` and `timeout_seconds` are each read only when the body
has a `tool_input` key, so without the wrapper they are taken for tool parameters and dropped as
undeclared, and the call still answers `200`. **Since 2026-10-24 that drop is at least named** —
on the standard HTTP execution path the envelope carries `dropped_unknown_params: ["fields"]`,
which is the one machine-readable sign your control was eaten rather than honoured (verified live
2026-10-25: `{"slug": …, "owner": …, "fields": ["latestVersion.version"]}` bare on
`ClawHub - Get Skill` answered `200` with `projection: null` and exactly that list). But the tool
in the reading below is a `COMPOSITE`, and that path computes no such list, so on those it stays
silent and `projection: null` is all you get. Live the same day, `{"limit": 2, "fields":
["[].title"]}` came back `200` with `projection: null`, the full story objects, and `fields`
echoed back inside `request_params`, while `{"tool_input": {"limit": 2}, "fields":
["[].title"]}` returned the two titles alone with `projection: {"fields": […], "missing": []}`.
(`max_response_chars` is the exception — it is read in either shape.) The one that bites is
`confirm_token`, since a token sent without the wrapper never reaches the consent check and the
call answers `409` again, which reads as a token that does not work. It is worse than one wasted
round trip: the token is signed over a hash of the tool input (`hash_args(tool_input)`,
`services/consent.py`), and bare the token is *part* of that input, so every retry hashes
differently and is answered with a fresh token — a loop rather than a refusal. So always send
`tool_input`: it is the only shape every recipe in this file holds for.

**And don't carry MCP's `parameters` over to REST — it is read as a parameter of that name.**
That alias is MCP's — and even over REST a *batch* entry does not take it either, per the
paragraph above — so on this route the wrapper becomes an undeclared parameter and your values
never arrive. On a tool whose
parameters are all optional that is a silent wrong answer: live 2026-10-22,
`{"parameters": {"limit": 2}}` on that same tool answered `200` with **ten** stories and
`request_params: {"parameters": {"limit": 2}, "limit": 10}` — the wrapper kept as a parameter
the row does not declare (so dropped before the upstream request) and the schema's own default
filling in the `limit` that never got there. On a tool with a required parameter it fails
instead, and the message names what you did send rather than what you meant:
`error_type: "missing_parameters"`, "Missing required parameters: q. Provided parameters:
parameters." (live, `HealthData.gov - Autocomplete Dataset Names`). Read either one as the body
shape, never as a value you forgot.

**`GET /v1/tools/{tool_id}` works again — `/describe` is still what to read before executing,
and the collection route beside it is still unusable.** Until 2026-09-24 the per-tool route
answered `422`,
demanding a query parameter `r` that had no valid value, because its auth dependency was written
as `Depends(lambda r: …)` and FastAPI read that lambda's unannotated `r` as a required *query*
parameter. That is fixed: both routes now depend on the real dependency, and the per-tool route
returns the tool row normally — verified live on 2026-09-24, `200` with the full object both
plain and with a leftover `?r=1`. If you are talking to a backend deployed before that date you
may still meet the `422`; there is nothing to report or retry either way, just use `/describe`.

**This file dates a handful of behaviours that way, so here is the one check that tells you which
side of a date you are on — and what it can't tell you.** `GET https://api.danubeai.com/health`
needs no key and reports `started_at`, the boot time of the REST backend process. Since a process
can't be running code that didn't exist when it booted, `uptime_seconds` is a floor on the age of
the code answering you, with no ceiling: a restart reboots the image it already had, so a recent
`started_at` proves nothing. The one direction that reads: a `started_at` *earlier* than the date
on one of these notes makes the pre-fix behaviour the likely one — likely, not certain, since
those dates are when a fix was verified rather than when it shipped. **It dates the REST backend
only.** `api.danubeai.com` and `mcp.danubeai.com` are separate deployments, and the MCP server
publishes no build or boot time at all, so the notes below marked as MCP-layer changes can't be
dated from outside. Neither version number the MCP server does report helps —
`{baseDir}/references/troubleshooting.md` explains what those two numbers actually are.

**Still read `GET /v1/tools/{tool_id}/describe` before a first call — but the two are not
nested, so know what each one drops.** `/describe` is what adds the things you actually need
before executing: `required`, the tool's recent `usage`, your own `examples`, saved `defaults`,
and *populated* `readiness`, `configuration_url` and `reliability`. The bare route declares
those last three and returns them `null` — it runs no enrichment — so it cannot answer "can I
call this now". What the bare route carries and `/describe` leaves out is the plumbing:
`base_url`, `path`, `slug`, `tags`, `version`, `metadata`, `security_schemes` and
**`sunset_date`**. That last one matters, because this file tells you to read `deprecated`
together with `sunset_date` and `/describe` has only the first two of that trio. Both take a
slug as readily as a UUID (verified live: `…/tools/gmail-send-email` and
`…/tools/gmail-send-email/describe` both `200`). One caution on the bare row: its pricing
fields are unenriched defaults, so `is_paid` reads `false` and `price_per_call_cents` `null`
even on a priced tool — read a price off a search result, never off this route.

**`GET /v1/tools` (the whole collection) is the one route in this file not to call even once.**
It takes no pagination parameters at all and returns every tool row the caller may see — the
catalogue held 12,583 rows on 2026-09-24 and 12,740 on 2026-10-23 — and you cannot get an answer
out of it: probed four times on the earlier date it answered `500` (after 9–12 s) or, once the
edge's ~31 s ceiling was reached, `504`. The `500` is not a mystery and it is not about your
call: the route is declared `-> List[Tool]` while the query behind it selects five columns
(`id, name, description, tags, service_id`), so every row fails response validation on four
required fields it does not carry (`base_url`, `path`, `method`, `version`). That is a bug in
Danube's own route — deterministic, not retryable, and not something a parameter changes.
**What makes it worth avoiding rather than merely useless is that the cost can land on everyone
else.** Live on 2026-10-23 one such call answered `504` after 31.3 s and the whole API was
unreachable for about three minutes: the next request, an ordinary `GET /v1/stats/public`, came
back as the hosting platform's `no_healthy_upstream` page, three `GET /health` calls in a row
answered `504`, and the `/health` that finally answered reported a process seconds old where one
23 hours old had been answering a few minutes earlier. No deploy explains that restart and
nothing was filed as an error — but whether the call caused it was not established, and it is
not a thing to reproduce in order to find out. Use `GET /v1/tools/search?query=…` for discovery,
or `GET /v1/services/{id}/tools` for one service's full list.

**Without a key those two routes answer `401`, not the body** — the collection and per-tool
routes are mounted with a key dependency, and a dependency that rejects you raises before
anything else runs (verified live 2026-09-24). Read a `401` there as being about your key.
`/describe` is *not* on that router and needs no key at all — it answered `200` unauthenticated
on 2026-09-24. Over MCP none of that key-and-`404` business applies, but only `describe_tool` carries the
full schema: since 2026-09-25 `search_tools` and `get_service_tools` answer with a compact
summary unless you ask for more (see *A listing is a summary now* below).

**You never have to call either of them to learn how big the catalogue is.** `GET
https://api.danubeai.com/v1/stats/public` needs no key, is rate-limited at 30/minute, and
answers in one cheap call: `{"services": 517, "tools": 12740, "workflows": 0,
"total_executions": 19963}` at 12:25 UTC on 2026-10-31 — the live figure behind the row count
above, and still the same number. **Only the last of the four really moves.** `services` has not
moved since 2026-10-10, twenty-one days now, and `tools` is nearly as static: it has read 12,740
at every reading taken here since 2026-10-23, eight days and counting, while over the day from
the previous reading (19,803 executions at 12:20 UTC on 2026-10-30) the execution counter
gained 160. So expect that one number, and in practice
only that one, to differ from whatever is written down. Don't read any such difference as a
rate, either — it arrives in bursts: two readings eighteen minutes apart on 2026-10-14 differed
by 13, and two about ninety seconds apart on 2026-10-19 differed by 5. **Those bursts have a
mechanism, and it means the counter is never live.** `total_executions` is not counted at
request time: the route sums the `tool_execution_counts` **materialized view**, which a
database job refreshes every five minutes and which skips a refresh outright while the previous
one is still running (a guard added after a refresh that normally takes 5–8 seconds took 129 s
during a database stall). That lag sits *behind* the five-minute response cache described below,
so the two stack: a reading can approach ten minutes behind the calls that produced it on the
cadence alone, and go past that whenever a refresh is skipped or runs long. The view also leaves
out Danube's own internal probe traffic, so this is a count of real callers' executions rather
than of every row in the execution log. Read it as a rough size of the platform, never as a
receipt that a call you just made was recorded — `_meta.execution_id` on that call is the
receipt. Read its first two numbers as different populations rather than a ratio: `services` counts the
**public** catalogue only, while `tools` counts every tool row that exists, the ones belonging
to private and organization-internal services included. The `workflows` beside them is the
public-workflow count, which is why it reads `0` rather than meaning the account has none.
**The body is cached for five minutes**, so it is not a freshness check: a service published or
a tool registered moments ago will not move these numbers yet, and calling again inside the
window returns the identical body rather than a new reading. `GET /health` carries the same
whole-catalogue population as `index.lexical_rows`, read off the running process's search index
rather than the database; the `index.tools` beside it counts the rows that carry an embedding
the index could use, so it is never the larger of the two and a gap is rows it had none for,
usually ones still waiting to be embedded, not a fault. The two therefore read **equal** once
every row carries a usable embedding, as they did on 2026-10-17 (12,736 each, on a process up
23 hours) and at every reading taken here since — 2026-10-29, 2026-10-30 and 2026-10-31,
12,740 each on a process up 23 hours all three times: no gap is a fully embedded index, not a sign the two
fields mean the same thing. **One of the four numbers above is on `/health` too, and fresher.**
Its `catalogue.services` is counted off the in-process catalogue snapshot, which selects with
the same `visibility = 'public'` filter over the same table this route uses — not a second
population — and carries an `age_seconds` saying how old the copy in hand is. The snapshot is
rebuilt on a **two-minute** cycle (backing off to five minutes after a slow or failed tick), and
a service created or changed *through the API* wakes the refresher at once, so only a change
made behind the backend's back waits for a tick. That still beats this route's five-minute
cache, which no write invalidates. On 2026-10-31 both routes read 517 and that age read 6
seconds. So when the public service count is what you want and you want it current, read it
there instead of waiting out this body's window.

### Reading what comes back

`execute_tool` returns `{result, _meta}` once a call actually reaches a tool. When the tool
returned JSON, the already-parsed object is at **`result.data`**. Read that;
`result.content[0].text` then holds only the pointer `JSON result: see result.data`, so the
payload is not sent twice. A text-only result stays in `result.content[0].text`. Don't index `_meta`
blindly: it is absent when the lookup itself failed (no `tool_id` or `tool_name` given, or
neither resolves).

**A tool whose own JSON carries a `content` key is still ordinary JSON.** `Google Drive -
Download File Content` answers `{"content": "<the file text>", "mimeType": …}`, which from the
outside looks like the MCP `{content: [...], isError}` envelope Danube unwraps. Since 2026-09-27
the envelope is recognised only when `content` is a **list** (or, with no `content`, when
`isError` is a boolean), so a body like that one lands whole in `result.data` like any other.
Before that fix it was unwrapped as an envelope, walked one character at a time, and failed with
`'str' object has no attribute 'get'` — **after the backend had already run the call and logged
it as a success**. If you meet that error against an older deployment, treat the call as done:
re-running it repeats whatever it did.

**When the payload is not JSON there is no `result.data` at all** — plan for that rather than
reading a missing key as an empty result. Danube adds `data` only when the upstream body (or,
on an MCP server, one of its text blocks) parses as JSON, so a tool that answers in Markdown
or prose has none, whichever kind of service it is: live, the HTTP tool `ClawHub - Get Skill
File` returned 25,635 characters of Markdown under `content[0].text` with no `data`, and the
MCP-backed `Cloudflare Documentation.migrate_pages_to_workers_guide` did the same with its
5,423-character guide. Fall back in this order: `result.data` when it is there, then
`result.structuredContent` on an MCP-backed tool that sends one, and only then
`result.content[0].text`.

**`structuredContent` is capped and trimmed like any other payload — since 2026-09-27 it is no
longer the uncapped copy this file used to describe.** `max_response_chars` reaches it whenever it
is an object or an array, which the MCP spec requires, and it is then trimmed the two ways a JSON
payload is: losing whole array elements off the tail, or degrading to `_truncated_partial_json`
when there is no array big enough to trim. Its trim is reported in `_meta` (`truncated`,
`truncation_note`, `dropped_items`). Live on
`Cloudflare Documentation.search_cloudflare_documentation`, the call this file once cited as
proof of the opposite: capped at 100 chars, the text block came back cut *and*
`structuredContent` came back as `{"results": []}` — 17,778 characters trimmed to 15, with
`_meta.dropped_items` reporting `results` as 0 kept of 8. **That empty collection is the trap
worth knowing**: trimming keeps it valid JSON of the right shape, so a `structuredContent` whose
list has been emptied reads exactly like a genuine "no results". Check `_meta.truncated` before
believing it. (When both payloads are trimmed, `_meta`'s sizes are merged rather than per-block —
the largest original and the last payload's final size — so read them as "something was cut",
not as a measurement of one block. The same holds when only `structuredContent` was cut: those
sizes then describe it alone, beside a text block nothing trimmed.) It is also **dropped outright
when it is the same document as `result.data`** — the test is exact equality after both copies have
been shrunk, so any structural difference keeps it, and a text block carrying a JSON *array* always
does, since `structuredContent` is an object. So it stays second in the order above because it
arrives parsed, not because it escapes your cap.

**A tool that hands back a file is the one case where the payload goes missing without
`truncated` being set.** A tool whose job is to return bytes (the catalogue's
`Wikimedia Commons - Get File Bytes` is the live example) puts them base64-encoded in
`content_base64`, beside a `mime`. Over MCP that key is lifted out of the text before the result
is shaped, because a few hundred KB of base64 is both useless to read and larger than the
response cap, which would cut it into an invalid file. Two things then happen:

- **An image the client can display is attached as an MCP image block** — `image/jpeg`,
  `image/png`, `image/gif` or `image/webp`, up to 5,000,000 base64 characters — and
  `_meta.image_block: true` says so. You do not have to decode anything; it is already in the
  conversation as an image.
- **`content_base64` in the JSON is set to `null`** unless the whole result fits in the
  `max_response_chars` you asked for. `_meta` then carries `content_base64_omitted: true`,
  `content_base64_chars` (the real length) and a `file_note` — which names an exact number to
  pass **only when that number is one you could actually pass**. Your budget is clamped to the
  MCP layer's own 500,000-character ceiling before it is compared against the file, so once the
  whole result would need more than that there is no number at all: the note says instead that
  the file "is over the 500,000-character MCP limit" and offers the REST API, the SDK, the CLI
  or a smaller `width`. Any file much over ~370 KB crosses that line, so on this tool the
  numberless branch is the ordinary case rather than the edge one, and no `max_response_chars`
  gets you past it — the tool's own, far larger cap is honoured on the REST path only. The
  image block is a separate limit and survives this one, but only up to its own 5,000,000
  characters: past that there is no image either, and the note says the file is "not shown"
  rather than "attached as an image block". Since this tool returns up to 8 MB, a file between
  roughly 3.75 MB and that ceiling comes back as metadata alone.

**`_meta.truncated` stays `false` through all of that**, so the truncation check this file tells
you to make everywhere else will not catch it: a `content_base64` of `null` beside
`truncated: false` means the bytes were withheld, never that the tool returned nothing. Test
`_meta.content_base64_omitted`, and read the rest of the row (`mime`, `width`, `height`, `bytes`,
the licence fields) as the real answer it is. Verified live 2026-10-05 on that tool, asking for
`File:Mona Lisa, by Leonardo da Vinci, from C2RMF retouched.jpg` at `width=120`: the image
arrived as an image block, `data.content_base64` was `null`, `_meta.content_base64_chars` 9,828,
`file_note` said to pass `max_response_chars=10031`, and `truncated` was `false`. (Those two
figures are that file at that width — expect your own; it is the shape that is stable.) The
other branch, live 2026-10-21 on the same file with no `width`: 3,173,276 base64 characters (a
2,379,957-byte 1920x2861 JPEG), still attached as an image block, `content_base64` `null`, and a
`file_note` carrying no number to pass — "it is over the 500,000-character MCP limit, so call
the tool through the Danube REST API, SDK or CLI". **None of this happens over REST** —
`POST /v1/tools/call/{tool_id}` returned that same file's 3,173,276-character `content_base64`
whole, `truncated: false`, with no `max_response_chars` sent at all, which is why the note offers
the REST API, the SDK or the CLI as the way to get bytes you actually need to keep.

Over REST Danube adds no `data` key on any path: `result` is the upstream body, or for an
`mcp_server` service the upstream envelope, so a `data` you do find there is the upstream's own.

Oversized payloads are trimmed. A JSON array is trimmed at element boundaries, so it stays
parseable; plain text is cut mid-string with an inline `... [truncated - response was N
chars, …]` note; and a JSON object with no array big enough to trim degrades to
`{"_truncated_partial_json": "<prefix>", "_truncated": true}` — valid JSON, but the
object's own keys are gone, so re-request it rather than parsing that. Check
`_meta.truncated`, and `_meta.truncation_note` for what went. **In that last case
`_meta.dropped_items` is still reported, and it is counting against a document you only hold a
prefix of.** The trim empties arrays first and degrades the whole object only when that still
leaves it over the cap, but it reports the arrays it emptied either way — so `dropped_items` reads
like an otherwise-complete answer missing a few list entries, when what you have is the opening
bytes of one. Live on 2026-10-27, `ClawHub - Get Skill` at `max_response_chars: 20000` came back as
`_truncated_partial_json` while `dropped_items` reported three arrays at 0 kept of 5, 1 and 1.
`truncation_note` does name the mode — "no array large enough to trim, so only a prefix of its
serialization is returned" — but **not in its last sentence**: that is the generic "Pass
max_response_chars to request more…" advice, which closes every *size* trim this layer reports.
Don't key on position. Match on the mode sentence, or on the `_truncated_partial_json` key itself,
and read either before the counts. (A batch element's note is assembled differently again — see
`{baseDir}/references/troubleshooting.md` — so the advice line can sit mid-note there or be absent
altogether.) To get the rest, raise
`max_response_chars` (default 50000, hard max 500000) or follow `_meta.cursor` when the
upstream paginates. When a tool is resolved by *name*, that tool's own per-tool default
replaces the 50000 — in **either** direction, and the one such figure Danube's own registrar
writes raises it rather than lowering it: `Wikimedia Commons - Get File Bytes` declares
12,000,000 (live on its row as `metadata.max_response_chars`), which the MCP layer then clamps
back to its own 500,000 ceiling. Any publisher may set the key on a tool they own, so a smaller
one is possible too; the direction is what you cannot assume. Read a per-tool figure as "a
different default, still never above 500000 here", not as "a smaller one". It is read on the name path only — pass the UUID
and the default is the ordinary 50000. **Inside `batch_execute_tools` the
per-element default is lower — 32000 over MCP, since a batch multiplies it by up to ten** — so
a payload that survives a single call can still be trimmed as one element of a batch. (Raw
REST has no such batch default; an entry with no `max_response_chars` gets 500000 — or that
tool's own cap, since a batch entry runs through the same per-tool resolution as a single call.) Truncated
≠ broken — don't `report_tool` it.

**On a batch element `truncated: true` means "something was dropped somewhere", not "this layer
cut it" — so read what did before raising the cap.** Since 2026-10-04 an element also discloses a
trim made *before* the MCP server saw the result, which it used to swallow: a list the backend had
already shortened to its own 500000-char cap passed the per-element shaping untouched and the
element read `truncated: false` with no note at all (the report behind the fix: `Apify - Get
Dataset Items` in a batch handed back 65 items beside a `structuredContent.itemCount` of 200).
Two of the three causes are not `calls[].max_response_chars`, and `_meta` says which you have:

- A **row cap** on an infrastructure connector carries `reason` (`"row_cap"`), `row_count` and a
  `hint`, and its note says the result was "cut by row_cap, not by response size" — the lever is
  `max_rows` *inside* `tool_input`, and raising the response cap returns not one more row. Since
  nothing was cut by size, `original_response_chars` and `response_chars` are left out of `_meta`
  altogether here. Read it off `reason`/`hint`, though, not off those missing figures: an envelope
  that arrives `truncated` with no shape report at all also has none, and says so in its note
  ("dropped before it reached this server, and the report did not say how much").
- An earlier **backend** trim rides in `dropped_items` too, and a path there labelled
  `"<path> (before this trim)"` is the earlier layer's count, not this one's — the two layers root
  their paths differently, since the backend does not unwrap MCP envelopes, so don't read its
  `kept` beside this layer's as one story. That label appears only when this layer trimmed
  something as well; when the element fit the per-element cap and only the backend trimmed, the
  path arrives unlabelled under its own name. Where both trimmed the same array, `kept` is what
  you were handed and `total` is what the upstream really returned.

So read `_meta.truncation_note` first: raising a cap that was never the limit buys nothing.
`_meta.execution_id` still reads the stored copy back — but what was stored is what the backend
already shaped, so on a row cap the handle hands you the same rows and only `max_rows` gets more.

**A slow MCP-backed tool can be given more time.** `execute_tool` takes `timeout_seconds` for a
single call — 1 to 300, defaulting to about 30 — and `POST /tools/call/{tool_id}` accepts the
same key beside `tool_input`. It reaches only tools served by an MCP server (an Apify actor
run, a crawl, a report rendered server-side are the cases worth raising it for). **On an `api`
service it is accepted and then ignored**: an HTTP tool's budget comes from its own catalog row
(30 s unless the publisher set otherwise), which a caller cannot extend — so if one of those
keeps timing out, the fix is a narrower request or a `report_tool`, not a bigger number. Past
300 seconds the work belongs in an asynchronous flow either way: start it, keep the handle it
returns, and poll with that service's own status tool.

**An infrastructure connector's tools are the third case, and there `timeout_seconds` is a
parameter rather than a sibling of `tool_input`.** On a connector tool (PostgreSQL, MySQL,
ClickHouse, Redis, Kafka, Kubernetes, the AWS ones, Grafana, Prometheus, …) `timeout_seconds`
and `max_rows` are ordinary tool parameters, so they belong **inside `tool_input`** with the
rest — a `timeout_seconds` placed beside `tool_input` is the MCP/`api` budget above and never
reaches the connector. The timeout ceiling is **55 seconds**, not 300, because the call has to
finish inside the data plane's 60-second dispatch budget; the default is 15. That ceiling is
enforced on every connector call whether or not the tool advertises the parameter — and plenty
do not: an op opts into the shared limits pair, and **43 of the 119 connector operations** skip
it, among them every `Test Connection`, the single-item and `Describe` reads, the two that carry
their own caps (`Kubernetes - Get Pod Logs` has `tail_lines`, 200 by default and 5000 at most;
`Redis - Info` caps nothing), and **nine of the thirteen write tools** named above. Those list neither parameter in their schema, and the
asymmetry matters: the timeout still applies if you send it, while `max_rows` on an op that
doesn't declare it is accepted and ignored — the same trap as `timeout_seconds` on an `api`
service above. `describe_tool` is the authority on which a given tool
declares, and on its bounds, because an op may set its own: the shared `max_rows` is 500 by
default with a ceiling of 5000, but `AWS DynamoDB - Scan` is 100 with a ceiling of 1000 and
`Apache Kafka - Peek Messages` is 20 with a ceiling of 500. Both limits are **clamped
silently** — ask for 300 seconds and the call runs with 55, ask for 5000 rows on Scan and you
get 1000 — and nothing reports the value that actually applied (`AWS DynamoDB - Scan`'s
`result.max_rows` aside), so treat the schema's bounds as the budget rather than assuming what
you sent survived. On `Apache Kafka - Peek Messages` the lever is `count` (or `from: latest-N`,
which recomputes it); `max_rows` is only a hard cap there, so raising it alone still returns 20. A timeout here says so in its own
words: "Raise timeout_seconds (up to 55) or narrow the request."

**Not every connector is infrastructure, and the one that isn't needs no credential at all.**
The same connector machinery now also backs ordinary public catalogue services that run on
Danube's own side with no connection to configure — `Wikimedia Commons` (four tools: file search,
file info, category listing and the `Get File Bytes` above) is the first. It has no credential
schema, so its tools read `readiness: "ready"` for every account with nothing to connect
(verified live 2026-10-05), and it is not offered as an organization system. Treat it as a
connector for *calling* purposes: the 55-second ceiling is enforced on its calls too, and where
a `timeout_seconds` is declared it is an ordinary parameter inside `tool_input` — on these four
that is `Get File Bytes` alone, the other three declaring neither limit. **Its default is 30
seconds, not the 15 the rest of this section quotes**, since the op declares the parameter
itself rather than opting into the shared pair; the 55-second ceiling is the same. None of the credential,
placement or data-plane paragraphs apply to it, so read the ceiling as a property of connector
calls rather than of the dispatch budget that explains it elsewhere. The seventeen-service,
119-operation counts in this file are the infrastructure connectors only and do not include it.

**Credential values are masked before you ever see them.** Every tool response passes
through Danube's redactor on the way out, and unless the tool is one specifically declared
as returning a credential (see below), anything that reads as a secret — API keys, tokens,
passwords, connection strings — comes back as `[REDACTED:<FIELD>]`. That is
platform policy, not a broken tool: don't `report_tool` it, and don't ask the tool to
return the raw value. When there is something to report, the redaction object carries an
exact `count` plus a `fields` list — the first 50 masked values, each with its `path`,
`key`, and the `rule` that caught it — and a `mode`. It lives at `_meta.redaction` over
MCP, where the key is absent when nothing was masked, and at top-level `redaction` over
REST, where the key is always present and simply `null`. Either way, test the value, not
the key. Pagination cursors and identifiers are exempt by name, so paging keeps working.

A tool whose whole *purpose* is to mint a credential is not redacted into uselessness.
Where Danube can, it captures the secret for you: the new value is stored as the user's
credential for the target service and `_meta.redaction.stored_credentials` says where it
landed, so the service's later calls pick it up through ordinary credential injection and
you never hold the value.

**Where it can't, the secret reaches you raw** — a tool marked as returning a credential
with no capture mapping, a self-hosted deployment (custody stays in the customer's own
environment), or a store that failed. These come back completely unmasked with
`_meta.redaction.passthrough_reason` explaining why, alongside `count: 0`. This is
not limited to short-lived handoff tokens like a Plaid *link* token: a Plaid **access**
token, a rotated webhook signing secret, and other durable secrets pass through this way.
A named case in the catalogue today is `DigitalOcean Spaces - Spaces Key Create` (slug
`digitalocean-spaces-spaces-key-create`), declared `returns_credential` with a `passthrough`
capture since 2026-10-17 precisely because DigitalOcean shows a new Spaces key's `secret_key`
once and nowhere else — masked, the key the caller just asked for would be unusable. It is the
fourth cause of an unmasked payload, beside the three above: a tool declared `passthrough`
outright, because the caller asked for a key to use elsewhere rather than a credential for Danube
to hold.
Treat anything that arrives unmasked as a live secret — show the user where to put it,
don't echo it back, and don't paste it into a later call's parameters.

Discovery tips:
- **Every search result says whether it really matches, and a page of nothing but `weak` usually
  means the catalogue has nothing that fits.** Semantic search always returns its nearest
  neighbours, so a query for something Danube does not have comes back full of confident-looking
  wrong answers: before a Postgres connector existed, "run SQL against Postgres" returned PostHog's
  HogQL tool and Elasticsearch's SQL endpoint ranked exactly like real hits, and agents called
  them. So `search_tools` stamps each result with **`match`** — `"strong"` when the result's name,
  description and service name together carry at least 60% of the weight of the query's
  *distinctive* words (a word most tools share, like "run" or "list", counts for little;
  "postgres" or "pod" counts for a lot), `"weak"` when it only resembles the query. A query that
  appears verbatim inside the tool's own name scores full marks outright. Only those two labels are
  ever stamped — the 90% band exists for ordering, so there is no `"full"` value to look for — and
  `match` reorders the page ahead of the readiness band, though it is not the last word on the
  order: named-service promotion, sample-data demotion and exact-match pinning all run after it.
  Read it as a verdict on each result rather than on the page's sequence, and don't `report_tool` a
  weak one — nothing failed.
- **Two things to check before you act on a page of `weak` ones.** Searching for an exact slug or
  tool name produces one: `gmail-send-email` is a single token that appears nowhere in "Gmail -
  Send Email", so its coverage is zero and it is stamped `weak` — while exact-match pinning puts
  that very tool at the top of the page anyway. And the rephrasing tip below still applies: try
  another phrasing once before telling the user the catalogue has nothing. **`match` is also
  search-only, and it can be absent.** `get_service_tools` and `describe_tool` don't carry it (over
  REST a tool list may serialise it as an explicit `null`; over MCP the key is simply left out),
  and nothing is stamped at all when the query reduces to no usable keywords (all stop words, or
  nothing over one character) or while the backend's in-process lexical index is unloaded, as it is
  for a few minutes after a restart. So a missing `match` means "not judged", never `weak`.
- **`GET /health` tells you when you are inside that window, and it costs you one tier of the
  ordering as well as the label.** The `index` block in that body is the running process's
  search index, and it is **`null` outright until the first build finishes** — the handler copies
  the index's own status, which reports nothing before then — while a loaded one reads
  `{"tools": …, "lexical_rows": …, "word_index_mb": …, "age_seconds": …,
  "full_build_age_seconds": …, "building": …}`, as it did on 2026-10-31: 12,740 and 12,740,
  `building: false`. A `null` there is the tell for this cause (the bullet above has the other
  one, a query with no usable keywords), because the word frequencies `match` is scored against
  are read from that index's lexical half and the scorer returns **no weights at all** without
  it. What goes with the missing label is the sort it drives: the same no-weights path returns
  the result list **untouched**, so the match-tier ordering described above (full, then
  strong, then weak) does not run either. What still runs is everything layered on top of it —
  named-service promotion, sample-data demotion, the reliability filter and exact-match pinning
  are all independent of this index — so the page is not unordered, it has lost one tier of
  ordering, and `results[0]` for an exactly-named tool is still that tool. Read a missing
  `match` as "not judged" *and* "not match-ordered"; if that tier matters, search again a
  minute later rather than re-wording the query.
- **A listing is a summary now; `describe_tool` is the schema.** Since 2026-09-25 `search_tools`
  and `get_service_tools` over MCP default to `detail="summary"`. An entry then carries `id`,
  `slug`, `name`, `service_id`, a `description` **truncated at 300 characters** (a trailing `…`
  is the tell), `parameters` reduced to `name -> {type, required}` with `enum` kept only when it
  lists eight values or fewer, `readiness`, and `has_tips: true` when the tool has publisher
  tips (plus `match` on a search result — see the bullet above). What a summary drops: each parameter's `description`, `json_schema`, `default` and
  `minimum`/`maximum`, and the tips text itself. (The declared `output` and the plumbing —
  `base_url`, `path`, `metadata`, `security_schemes` — are a separate matter: the MCP layer's own
  tool model has never declared them, so no listing carries them at *either* detail level and
  `detail="full"` will not produce them. They live on the REST rows.) So read a listing to *pick* a
  tool and `describe_tool(tool_id)` to *call* it — the split this file already asked for is now
  in the payload. `detail="full"` restores the old shape on every result, but that is the
  expensive direction, not the safe one: the same 20 Apollo results are 19,422 characters as
  summaries and 89,696 in full, and the reason for the change was a search coming back too
  large to read. Reach for `describe_tool` on the one tool you picked instead. Three more fields
  are thinner rather than gone — `reliability` keeps only `calls_30d`, `success_rate_30d`,
  `p50_seconds`, `last_error_class` and `flagged`; `configuration_url` appears only when
  `readiness` is not `ready`; and the pricing and deprecation keys appear only when they are
  set (next two bullets). **This is an MCP-layer change only** — `GET /v1/tools/search` and
  `GET /v1/services/{id}/tools` over REST still return the full rows.
- Every search result carries `readiness`: `ready` means you can execute it now, `needs_credential` means the service needs a credential this account has not connected (send the user to `configuration_url`), `unavailable` means the service is retired. Ready tools are favoured: a tool that needs setup yields a few places to ready ones, so a clearly better match still comes first. Prefer a ready tool over a similar one that needs setup.
- **`ready` answers whether the call will work, not whose account it will act as — and over MCP
  you cannot find out.** For a tool that acts on the caller's behalf those are different
  questions: Gmail takes the From header from the OAuth grant and exposes no override, so a
  perfectly `ready` `Gmail - Send Email` sends from whichever Google account someone connected,
  which need not be the one the user has in mind. Danube records that identity when the provider
  hands one over at connect time and reports it as **`connected_as`** beside `readiness`, set
  only alongside `ready`. **Read it as "the identity the provider named", not "the email
  address"**: it is an email where the provider supplies one, but the extraction falls back to
  whatever stable handle it offers instead — an OIDC `preferred_username`, a Notion owner name,
  Slack's `authed_user.id` (an opaque `U…`), and last of all Slack's *workspace* name, so
  `"Danube HQ"` is a possible value and tells you the team rather than the actor. It is `null`
  when the provider offered nothing, and a credential stored as a plain API key rather than
  through OAuth has no label at all — the field is only ever written on the OAuth callback.
  **Three REST routes carry it**, and it is populated on each only for a caller the label can be
  looked up for (i.e. one sending a key): `GET /v1/tools/search`, `GET /v1/services/{id}/tools`
  and `GET /v1/services/public/{service_id}/tools`. Nothing over MCP carries it: the MCP layer's
  own result model has no such field, so `search_tools` and `get_service_tools` drop it at the
  boundary — `detail="full"` included, because that dumps the same model (verified live
  2026-10-08: a `detail="full"` search for `Gmail - Send Email` on an account with Gmail
  connected returned `readiness: "ready"` and no `connected_as` key at all). `describe_tool` and
  `GET /v1/tools/{id}/describe` miss it for a different reason — the describe response is built
  as its own dict that copies only `readiness` and `configuration_url`, which is why the key
  doesn't appear in that route's verified key list in `{baseDir}/references/rest-api.md`. So if
  the task is to send, post or spend as a particular identity, don't infer it from `ready`: read
  `connected_as` off one of those three routes, and if what comes back is a handle or a workspace
  rather than the address you expected, say so and let the user confirm the actor before you
  call.
- **A deprecated tool says so on the result**, through `deprecated`, `deprecation_message` and `sunset_date`. Over MCP those three keys are present *only when the tool is deprecated*, so their absence is the answer "not deprecated" rather than missing data; `detail="full"` and REST spell out `deprecated: false` on every result instead. A deprecated tool is still listed and still runs while its sunset date is absent or in the future — that is an advance warning, and the message usually names what to use instead, so read it and switch rather than reporting the tool. Once the date has passed the tool disappears from search altogether, and `execute_tool` refuses it before calling anything — the message reads "… was deprecated and passed its sunset date (DATE): … No call was made." Both transports now name it outright: `error_type` is `tool_sunset` with `fault: "danube"` — top-level over REST, in `_meta` over MCP. (Until 2026-09-10 the value was the upper-case `TOOL_SUNSET` and the MCP layer passed no field at all, so keep matching the message text too if you may be talking to an older backend.) Search again for the replacement; nothing about it is retryable.
- **A priced tool says so on the search result, before you call it.** There are four pricing fields: `is_paid` and `price_per_call_cents` (the credits price) and `x402_enabled` with `x402_price_usdc_atomic` (the USDC one). Over MCP a listing carries them **only when the tool is actually priced** — `is_paid: true` with its price, `x402_enabled: true` with its own — so on a free tool all four keys are simply absent, and that absence means free rather than unknown (`detail="full"` and REST still spell out `is_paid: false` on every result). `describe_tool` / `GET /tools/{tool_id}/describe` carries **none** of them, so the result you already have is where to read a price — a `describe` call won't tell you. Name the cost to the user before running a paid tool rather than discovering it from the refusal: a *credits* balance below the price is refused before the upstream call (see `insufficient_balance` below), which costs a round trip and reads like breakage when it isn't. (A thin *USDC* balance is the exception — it falls back to the credits wallet and goes ahead.) What none of these fields tells you is the pricing *mode* — see that same section for why an x402 price can still be re-derived at call time.
- Describe the *outcome* in natural language (`"send an email"`, `"create a GitHub issue"`, `"translate text"`); search is semantic.
- **But when you already know a tool's exact name, search for exactly that.** A tool whose name or slug matches the query exactly is pinned first, ahead of the readiness and reliability re-orderings, so `results[0]` is the tool you named. Every result now carries a `slug` (`stripe-api-read`) beside its id, and a slug is accepted everywhere a tool id is *executed or inspected* — `execute_tool`, `describe_tool`, `POST /tools/call/{id}`, `GET /tools/{id}/describe` and the bare `GET /tools/{id}` (confirmed live 2026-09-24: `…/tools/gmail-send-email` and `…/tools/gmail-send-email/describe` both resolve to that tool). The quality-signal tools are the exception and want the UUID: see *The quality signal* below. Prefer the slug when showing the user what you're about to run; it is far more readable than a UUID. It is not a reason to skip searching, though: resolve the tool in this session rather than replaying an identifier from memory.
- Sample-data services (JSONPlaceholder, DummyJSON) are ranked behind every real result unless your query names one of them. They need no credential, so they would otherwise outrank the real tools of a service the user hasn't connected yet. If one turns up for a generic query, treat it as what it is — a fake-data sandbox, not an integration to offer the user.
- If the first query misses, rephrase and try again before concluding a capability doesn't exist. The catalog is far larger than you'd guess.
- `list_services` is served from a cache refreshed every 60 seconds, so a service connected or published moments ago can be missing from it for up to a minute; `search_tools` and `get_service_tools(service_id)` are not cached. Don't conclude a service doesn't exist from one `list_services` miss; search for one of its tools instead.
- **`get_service_tools` stops at 50 tools over MCP, and nothing in the answer says so.** Its
  `limit` parameter defaults to 50 and the list is simply cut to that length — no total, no
  cursor, no truncation flag — so the rest of a large service's tools are indistinguishable from
  tools it doesn't have. It is not an MCP-server quirk: the cut is unconditional, and the largest
  services in the catalog are `api` ones (Vercel has 407 tools). Live on 2026-10-20: Higgsfield
  carries 105 tool rows, the default call returned 50 and `limit=500` returned all 105 — nothing
  clamps the number you pass, so pass a big one (500) rather than reasoning about the service's
  size, which moves anyway (the same service held 101 rows on 2026-09-20). Two knock-on effects worth knowing: a
  list of exactly 50 proves nothing by itself, because a service that really has 50 looks
  identical; and `needs_configuration` is derived from the sliced list, so on a larger service
  that flag describes only the first 50 tools. The REST route takes no `limit` and returns the
  whole list, so `GET /services/{id}/tools` is already the complete answer — and when the
  question is really "can this service do X", `search_tools(query, service_id=…)` answers it
  without the page at all — mind that its own `limit` defaults to 10.
- **A service's slug reads its tools and scopes a search to nothing.** `get_service_tools` and
  `GET /services/{id}/tools` resolve a service slug as readily as its UUID, so the identifier you
  already have usually works: live on 2026-10-17 the slug `gmail` listed that service's tools over
  MCP and all six of them over `GET /v1/services/gmail/tools`. The `service_id` **filter** on
  `search_tools` is the exception, and it fails quietly. It is matched for exact equality against
  the `service_id` each tool row carries, which is always the UUID, so a slug scopes the search to
  no service at all and the page comes back empty, with nothing saying the filter was the cause.
  An empty page is also what a service with no such tool looks like, which is how this reads as an
  answer rather than a mistake, and the bullet above sends you to this very call from a
  `get_service_tools` you may well have made with the slug. Live the same minute,
  `service_id: "gmail"` on the query `send email` answered `[]` both over MCP and over
  `GET /v1/tools/search`, while the service's own UUID
  answered with `Gmail - Send Email` first. So take the UUID off the row `list_services` or a
  search result gave you, and re-check an empty scoped search with it before telling the user the
  service cannot do the thing.
- **`list_services` has a third parameter, and asking for more than 25 services silently empties the rows.** `detail` takes `"auto"` (the default), `"full"` or `"compact"`, and `auto` means full up to a `limit` of 25 and compact above it — the switch is on the `limit` you asked for, not on how many rows came back. A compact row keeps `id`, `name` and `tool_count` and sets `description` to `""` and `url` to `null` rather than dropping the keys (the published output schema requires them), and nothing in the answer says the level changed. Live on 2026-10-15 one query answered with full descriptions at `limit: 25` and with `description: ""` and `url: null` on every row at `limit: 26`. So a page of blank descriptions is the detail level, not a catalogue that has none: keep the limit at 25 or below, or pass `detail: "full"` explicitly with a bigger one — bearing in mind what `compact` exists to avoid: the constant's own note puts the full form at ~330,000 characters at `limit: 500`, with a backend lookup per zero-tool row on top. Unlike the `?tools=` group filter, a value this parameter doesn't recognise fails loudly rather than being dropped: `detail: "brief"` answers "detail must be one of auto, full, compact, got 'brief'".
- **A service the listing reports with no tools is left out of the result altogether**, so a page can come back shorter than the `limit` you asked for while more results exist — and the service you searched for by name can be the one missing. Two conditions have to meet, which is narrower than it sounds: the catalogue's own `tool_count` must be exactly `0`, **and** below the compact threshold a live check of the service's tool list has to come back empty as well. Above the threshold that check is skipped, so the catalogue's `0` is the whole test — which means the same query can return a *different set* of services at `limit: 25` and at `limit: 26`, not merely differently-filled rows. A count that arrived `null` rather than `0` is **not** dropped: it survives and reads `tool_count: 0`, and in a compact listing that zero is the raw value rather than a recounted one, so one service can report a different count on either side of the threshold. Live on 2026-10-15, `GET /v1/services?query=Day AI` over REST returned ten rows of which `Day AI`, `Read AI` and `Peec AI` carried `tool_count: 0`, and `list_services(query: "Day AI")` over MCP returned exactly the other seven, with `Day AI` itself absent from a search for it by name. The dropped rows are usually MCP servers nobody has connected yet — `Day AI` is an `mcp_server` row with no tools registered — which is the `needs_mcp_oauth` case described under *When a tool needs credentials*; their tools appear once someone authorizes the service in the dashboard. So don't read the absence as "no such service": `GET /v1/services` over REST returns the zero-tool rows, and the user connects the service from the dashboard.
- **The `-32602` "Invalid request parameters" failure this file used to describe here is fixed.** A page holding a service whose `tool_count` arrived `null` used to fail the MCP layer's own `Service` model, which declares that field an `int`, and the whole page failed with it; the count is now coerced to `0` before the model sees it (`mcp/mcp_server.py`, 2026-09-28). Only that cause is closed — any other value the model's fields cannot take would still fail the page the same way — but `tool_count` was the one that did it. `query: "Day AI"` — the query this file used to name as having failed five times running on 2026-09-15, and still failing on 2026-09-23 — returns normally (live 2026-10-15). The MCP server publishes no build or boot time, so you cannot tell from outside which side of that date you are on: if you do meet the error against an older deployment, the old reading still holds — it belongs to the *page* rather than to the service you wanted, re-sending the identical call will not clear it, a different phrasing may, and `search_tools` and `GET /v1/services` are unaffected. Nothing to `report_tool` either way — this is Danube's own API, not a marketplace tool.
- Read the tool's parameter schema (`required`, `type`, `enum`, `tips`) before executing — from `describe_tool`, since an MCP listing carries neither the per-parameter detail nor the `tips` text, only `has_tips`; ask the user for anything required that you don't have. Never reuse tool IDs from memory — search again.
- **A parameter whose `type` reads `object (N properties)` carries its real schema beside it.** When a field's type is too complex for the summary string — a nested object, an array of objects, or a union — the parameter also has a `json_schema` key holding the upstream JSON Schema for that field: property names, types, bounds and descriptions. MCP-backed tools declare these routinely, and the summary alone leaves you guessing the keys. Live examples: `Apify - Call Actor`'s `callOptions` reads `object (5 properties)` and its `json_schema` names `build`, `memory` (128–32768), `timeout`, `maxItems` and `maxTotalChargeUsd` with a line of guidance each; `Apify - Fetch Actor Details`' `output` reads `object (9 properties)` and lists all nine booleans. **Where it rides depends on how you asked.** `describe_tool` always carries it. An MCP *listing* no longer does: since 2026-09-25 `search_tools` and `get_service_tools` summarise every parameter to `{type, required}` and drop `json_schema` outright, so a `callOptions` that reads `object (5 properties)` in a search result has no schema beside it at all — call `describe_tool(tool_id)` for it (or re-run the listing with `detail="full"`, which restores it). Over REST `GET /tools/search` is unchanged and still carries it, with an explicit `"json_schema": null` on a parameter that has none, while `describe_tool` and `get_service_tools` leave the key out in that case. Because absent and `null` both occur, **read it with `.get("json_schema")` rather than by testing whether the key is there.** **It is filled in for MCP-backed tools only**, so its absence tells you nothing about the parameter: an API-backed tool's complex body parameter reads a bare `object` with no `json_schema` at all, and its shape is described in the parameter's own `description` instead (`Airwallex - Create Payment Intent` spells several out that way). Read whichever of the two you get rather than inventing keys — it is catalog metadata, so nothing validates your object against it before the upstream sees it.
- Pass only parameters the schema declares. On the standard HTTP execution path, Danube drops anything the tool row doesn't declare *before* making the upstream request, so an invented parameter never reaches the provider. **Since 2026-10-24 every answer names what it dropped, on a success as well as a failure**: `dropped_unknown_params` lists those names — `_meta.dropped_unknown_params` over MCP (on each element's `_meta` inside `batch_execute_tools` too), a top-level field of the REST envelope beside `defaults_applied`. Read it on **every** call whose result you are about to trust, because the successful call is the dangerous one: a *filter* spelled under a wrong name doesn't fail anything, it just never reaches the provider, so the upstream answers everything and a result silently wider than the one you asked for is indistinguishable from a correctly narrowed one. (That is a real incident, not a hypothetical — a Danube routine passed `completed_at_after`/`completed_at_before` to `Apollo.io - Search Outreach Emails`, whose declared names are `emailer_message_date_range[min]`/`[max]`, and read three unfiltered pages back as 200s.) So if the field is there, the answer is not narrowed the way you asked: re-read the declared names with `describe_tool` and call again. Live on 2026-10-25, `ClawHub - Get Skill` with `include_versions` and `updated_after` alongside its real `slug`/`owner` answered `200` with `dropped_unknown_params: ["include_versions", "updated_after"]` on both transports. A **failed** call additionally spells it out in prose, and that text is unchanged: "`'x'` was not sent — `<tool>` does not declare that parameter, so Danube dropped it before making the request. If the upstream supports it, the tool's schema is missing it." Either way, treat it as a sign the tool's schema may be missing a parameter the provider does support, rather than as the upstream ignoring your value. **Empty means "nothing was dropped" only where the list is computed at all**: the HTTP path computes it, and tools backed by an MCP server forward your parameters as given (so the upstream really did see them and there is nothing to report), but a `COMPOSITE` tool never bucketed them in the first place and reports nothing either way — live, the same two invented names on `Hacker News - Get Top Stories With Content` (method `COMPOSITE`) produced no report at all. On those, an un-narrowed result is still your only clue. **The two transports spell "nothing to report" differently**, so test the value, not the key: over REST the field is *always* present and is `null` when there is nothing (the route sets no `response_model`, so the envelope ships every declared key), while over MCP `_meta` carries it only when non-empty and the key is simply absent otherwise.
- Results called in the last 30 days also carry `reliability` — the full block below on `describe_tool`, on REST, and on `detail="full"`, but only five of its keys on an MCP listing's summary (see that bullet above, and don't look for `p95_seconds`, `error_classes` or `faults` on a default search result): `window_days`, `calls_7d`, `calls_30d`, `success_rate_30d`, `p50_seconds`, `p95_seconds`, `last_success_at`, `last_failure_at`, `last_error_class`, `last_error_type`, an `error_classes` breakdown, a `faults` breakdown, `auth_failures_30d`, `caller_failures_30d`, `danube_failures_30d`, `upstream_failures_30d`, `distinct_callers_30d`, `flagged` and `refreshed_at`. When two tools fit, prefer the higher success rate; a `flagged` tool (under 80% success on 20+ calls) is a last resort, and say so to the user. `success_rate_30d` is `null` under 10 calls — that is too small a sample to rank on, not a bad tool. Results are relevance-ordered with a bounded reliability nudge; pass `ready_only=true` to see only tools you can call now, or `min_success_rate=0.9` to drop tools with a known-poor 30-day rate.
- **The score counts only what the tool is answerable for.** Since 2026-09-10 the sample behind `calls_30d` and `success_rate_30d` is successes plus `upstream` failures — the third party's own. Failures attributed to the *caller* (a missing credential, values the upstream correctly rejected) or to *Danube* (a stale row, a request Danube built wrong) are reported beside the rate and left out of it, so neither can push a tool over the `flagged` line. `faults` breaks the 30-day failures down by `caller` / `upstream` / `danube`, and the three `*_failures_30d` counters give the same thing as totals. A large `danube_failures_30d` is a Danube-side bug already queued for repair, not a reason to steer the user off a working tool; a large `caller_failures_30d` (of which `auth_failures_30d` is the credential part) is other callers' setup, not the tool. This generalises the older rule that only `auth` failures were excluded.
- `last_error_type` is the execution engine's own verdict (the `error_type` vocabulary below) on the most recent **upstream** failure — not on the most recent failure of any kind. `last_failure_at` and `last_error_class` are drawn from that same upstream-only row, which is why a caller-side failure minutes ago leaves all three untouched: they describe how the *provider* last let this tool down. `last_error_type` is additionally `null` for failures recorded before 2026-09-10, so `last_error_class` is the one populated on older rows.
- Read `last_error_class` before writing a tool off: `validation`, `upstream_4xx`, `upstream_5xx`, `timeout` or `other` (null when the tool has no counted failure). Upstream throttling has no class of its own — a `429` lands in `upstream_4xx` or `upstream_5xx` depending on how the provider worded it, so neither one is proof of a server fault. `auth` — a caller's missing or invalid credential — never appears here by design; it shows up only in the counters — `error_classes`, `auth_failures_30d`, and the wider `caller_failures_30d` / `faults` that now contain it — and those failures are left out of `calls_30d` and `success_rate_30d` entirely, so they can't push a tool over the `flagged` line. A tool with a large `auth_failures_30d` is one other callers haven't connected, not a broken one: if your account has the service connected, judge it on the rate.
- Before a tool you have not used successfully in this session, call `describe_tool(tool_id)` (REST: `GET /tools/{tool_id}/describe`): it returns the schema, your `readiness` and `configuration_url`, `usage`, `examples`, `defaults`, and the **full** `reliability` block — so you can compare a tool and read its schema in one call. (An MCP listing's summary keeps five of that block's keys; see *A listing is a summary now* above.) **Two of those are scoped differently than they look.** `usage` (calls, success rate, `p50_seconds`, `common_errors`) covers the last 30 days **across all callers**, not yours (the most recent 500 executions in that window). It is how the tool behaves for everyone, which is what makes `common_errors` worth reading before a first call. `examples` is the opposite: it is **your own account's** last successful calls and nobody else's. `defaults` is what `set_parameter_defaults` has saved, i.e. the parameters you may safely omit — it merges your own with any your organization has set, so a value there may be a teammate's.
- **`usage` and `reliability` count different things, so the two disagree by design — and only `usage` names a break that is Danube's own.** `reliability`'s sample is successes plus `upstream` failures, per the bullet above; `usage` is every execution row in the window whatever the fault (minus Danube's own probe calls), with `success_rate` the plain share of successes among them. So a tool broken on Danube's side reads clean in the block you were told to rank on and admits it in the other. Live on 2026-10-13, `Kalshi - Get Historical Fills` answered `usage: {calls: 3, success_rate: 0.667}` with `common_errors` quoting `Unknown Kalshi composite tool: Get Historical Fills`, beside a `reliability` block carrying `calls_30d: 1`, `success_rate_30d: null`, `flagged: false` and `null` in all three of `last_failure_at`, `last_error_class` and `last_error_type` — that failure present only as `faults: {danube: 1}` and `danube_failures_30d: 1`. Two limits on `common_errors`: at most **five** distinct messages, each grouped by its **first 120 characters**, so two failures that open alike are counted as one. And `reliability` is a materialized view refreshed every ten minutes, so it lags as well — `refreshed_at` is the tell, and a call made since then (the extra success behind those two call counts, here) is simply not in it yet, on a search result as much as on a describe. An MCP listing's *summary* carries neither `faults` nor the `*_failures_30d` counters, so a default `search_tools` page cannot show you this; `detail="full"` and REST carry the whole block, and `describe_tool` is the only place the failure's own **message** is readable.
- **`examples` are real past calls, not sample data — copy the shape, not the values.** Each entry is `{parameters, executed_at}`, where `parameters` is the stored `request_params` of one of your account's own successful executions, verbatim — so it holds whatever was actually sent: real recipients, real message bodies, real record ids from some earlier task. It can also carry execution controls that are not schema parameters at all (`async`, `previewOutput` show up on the Apify entries), so check each key against the schema before copying it. Credential-shaped values have been masked since 2026-09-02 (older rows were never backfilled), but ordinary personal data never was. Use them to see which parameters a working call sets and how they're spelled, then fill in the values for *this* task — re-sending one verbatim can repeat a real action against a real third party. Don't echo them back to the user either; they may belong to a different piece of work. Note also that, unlike `usage`, `examples` has **no time window**: it is the three most recent successes however old, so an entry can predate a change in the tool's schema.
- If a service always needs the same identifier (Vercel `teamId`, a Sentry org slug, a DigitalOcean app id), save it with `set_parameter_defaults(service_id, {"teamId": "…"})` as soon as a call using it has succeeded, without asking first, and tell the user in one line what you saved; they see it on the service's page in the Danube dashboard and can remove it there. Later calls that omit it get it filled in (`_meta.defaults_applied` says which). Don't save one-off values such as a single record id, and never save a key or token this way.
- **A save replaces the stored object for that scope — it does not merge into it.** One row holds
  one `defaults` object per (owner, service, tool-or-all), and a save overwrites that object
  wholesale, so `set_parameter_defaults(svc, {"projectId": …})` after
  `set_parameter_defaults(svc, {"teamId": …})` leaves the row holding only `projectId`, with the
  `teamId` you saved earlier silently gone. Send every default you still want in the same object.
  **Don't read the current set off `describe_tool` to rebuild it**, either: that `defaults` key is
  the *merged effective* set for one tool — your service-wide row, your tool-scoped row and
  anything your organization set, flattened into one — so writing it back copies a teammate's
  value, and a value meant for one tool, into a service-wide row of your own. The route that
  keeps them apart is `GET /v1/services/{id}/parameter-defaults`, which answers
  `{"service_id": …, "rows": [...], "effective": {...}}` with each row carrying its own
  `user_id` / `org_id` / `tool_id` (verified live 2026-10-12: `200` to an API key). **No MCP tool
  reads it**, so over MCP either track what you saved this session or read it over `curl`.
- **`tool_id` narrows a save to one tool**, and the precedence is fixed, most specific last:
  organization+service, organization+tool, you+service, you+tool. So your own service-wide
  default already outranks anything your organization set, and a tool-scoped one of yours
  outranks all three. Reach for it when a value is right for one tool of a service and wrong for
  the rest; leave it out for an identifier the whole service needs.
- **An explicit empty value does not beat a *saved* default.** A saved default is filled in for a
  parameter you omit *and* for one you send as `null` or `""`, so you cannot blank one for a
  single call. (A default declared in the tool's own schema behaves the opposite way — presence
  of the key is all that counts there, so an explicit `null` wins. These are two different
  mechanisms.) To stop a saved one being filled in, either save the set again without that key —
  a save replaces the object, per the bullet above — or `DELETE
  /services/{id}/parameter-defaults`, which removes **the whole row** for that scope, every
  default in it, not the one key (add `?tool_id=…` to target a tool-scoped row instead). Either
  way, read the list of keys that were filled in rather than assuming your empty value survived:
  `_meta.defaults_applied` over MCP, top-level `defaults_applied` over REST, and the key is
  absent when nothing was filled in.
- Keep big results out of your context: pass `fields: ["items[].name", "pagination.next"]` to `execute_tool` to receive only those paths. The result is stored under `_meta.execution_id`; `fetch_result(execution_id, path)` (REST: `GET /tools/executions/{id}/result?path=…`) reads any other part of it back without re-running the tool.
- **The read-back has a size cap of its own, and it defaults to 50000 characters** — a whole
  stored result is not what a bare `fetch_result` necessarily hands you. It takes
  `max_response_chars` (REST: `max_chars` on the query string); the floor is 100 on both, the
  ceiling differs — 500000 over MCP, 2,000,000 over REST, the same ceiling the execute call uses.
  It trims exactly the way an execution response does, in all three of that paragraph's modes: a
  JSON array loses whole elements off its tail and stays valid JSON of the right shape, plain text
  is cut mid-string, and an object with no array big enough to trim degrades to
  `_truncated_partial_json` with its own keys gone. The array case is the one to watch, because a
  short-but-well-formed list is the one that reads as a complete answer. Live on 2026-09-20
  against a stored 194-element result: the default fetch returned 32 elements with
  `truncated: true` on both transports, while `max_response_chars: 500000` returned all 194 with
  `truncated: false` — the stored copy had been whole the whole time.
- **On a fetch, `truncated` reports the backend's trim and not the MCP layer's.** Read it
  (`_meta.truncated` over MCP, top-level `truncated` over REST) before treating a fetched result
  as complete — but over MCP it is only half the signal: a `max_response_chars` above 500000 is
  silently clamped to 500000 and applied *after* the backend has answered, so a result cut by
  that clamp comes back with the flag reading clean. Don't ask for more than 500000 there. When
  the stored result is genuinely larger, read it in pieces with `path`, or fetch the same handle
  over REST, where the ceiling is 2,000,000.
- **A batch entry takes `fields` too, and since 2026-09-10 it is honoured** — before that it was accepted and silently dropped. Put it beside `tool_input` on any element of `batch_execute_tools` (REST: any entry of `POST /tools/call/batch`). Each element then carries its own projection report and execution handle: `_meta.projection` / `_meta.execution_id` over MCP, `results[i].result.projection` / `.execution_id` over REST. **The two transports trim in opposite orders, so the advice differs.** Over MCP prefer `fields` to a bigger `max_response_chars`: the 32000-char per-element cap is applied *after* the backend has projected and stored, so a projection keeps a verbose payload whole, and `fetch_result` on the element's handle reaches everything the backend kept — up to its own 500000-char shaping limit, since the MCP layer never forwards your cap to it. Reaches, not returns: the fetch applies its own 50000-char default on the way back (see `max_response_chars` above), so raise that on the fetch or the handle hands you a trimmed copy of an untrimmed result. Over REST an entry's `max_response_chars` (default 500000 there, not 32000) trims *before* the result is projected and before it is stored — so there a narrower request is the only real lever, and fetching a trimmed element's handle back does not recover what the cap cut. Over MCP the element's payload also sits at `result` itself, with no `data` wrapper (over REST that slot holds the whole envelope, with the payload one level further in) — but either way the paths are written against the same shape you would use on the single call.
- **The stored copy has its own ceiling: 1,000,000 serialised characters** — but it is rarely the ceiling that binds, because what gets stored is what the response *shaping* already produced. Over MCP your `max_response_chars` on an execute call never reaches the backend at all (the MCP layer applies its own cap afterwards), so the stored copy is shaped at the backend's 500000 default and can't exceed it; the 1,000,000 ceiling only bites over REST, and only when a call asks for more than that. Past whichever limit applies first, a JSON result loses whole array elements from the tail (still valid JSON of the same shape, just short) and a plain-text one is simply cut at the limit. The REST handle then says so with `stored_truncated: true` and a `stored_meta` block giving the original size and what was dropped; `fetch_result` over MCP carries **neither** key, so there an oversized handle is quietly partial. If you are paging a very large result by path and the tail is missing, re-run the tool with a narrower request rather than concluding the upstream had nothing more.
- **On an MCP-backed tool, write `fields` and `path` against the upstream envelope — but a leading `data.` no longer costs you the call.** The projection runs in the backend, on the result *before* the MCP layer shapes it, so it sees the upstream MCP server's envelope, while `data` is a key the MCP layer adds afterwards. The clean path therefore starts at `content[0].text.…` (a JSON-carrying text block is stepped into for you, see below) or at `structuredContent.…` where the server sends one. **Since 2026-10-24 the spelling you read the value at works too**: each path is matched as written, and one that matched *nothing* is retried with a leading `data` or `result` segment peeled off — repeatedly, so `result.data.x` loses both — so `data.content[0].type` resolves to `content[0].type` and `_meta.projection.envelope_prefix_stripped: true` (REST: `projection.envelope_prefix_stripped`) says that is what happened. Before that fix such a path came back as an empty success with only `matched_nothing` to explain it — the failure mode that had a Danube routine read `[]` from `Sentry - List Issues` for `data[].shortId` and nearly file "no production errors" against a project with an issue still firing. Two guards keep the peeling honest: a path that matched **as written** is never reinterpreted (so an upstream server's own `data` key still wins, as before), and a prefix that is a real key of the value is never peeled — `data.x` over `{"data": {"y": 1}, "x": 2}` addresses something that exists and genuinely missed, rather than being answered with the sibling `x`. What the peel does *not* do is reach the `data` key the MCP layer adds, because that key does not exist yet when the projection runs: confirmed live on both transports against `Cloudflare Documentation.migrate_pages_to_workers_guide`, `fields: ["data.content[0].type", "data.anything"]` kept the content block and reported `missing: ["data.anything"]` with `envelope_prefix_stripped: true` — the first path peeled to something real, the second peeled to `anything` and still matched nothing. A genuinely wrong path is still reported under **your** spelling, so compare `missing` against what you sent rather than against the peeled form. **`structuredContent` is projected too, and when the text block is prose your paths resolve against it** (both since 2026-09-27). When the text block carries the document, the same paths are applied to the structured copy beside it and it is dropped when none of them match — before that fix it rode along whole, so a projection down to one field still returned the entire document in `structuredContent`. When the text block is *prose*, a path written against the document matches nothing in the envelope and is then resolved against `structuredContent` instead: live, `fields: ["results[].title"]` on `Cloudflare Documentation.search_cloudflare_documentation` reported `missing: []` and returned `structuredContent.results` as eight `{title}` objects. **That fallback is all-or-nothing, so don't mix the two kinds of path in one call**: it is tried only when *none* of your paths matched the envelope, so adding an envelope path alongside a document one loses the document one — `fields: ["content[0].type", "results[].title"]` on that same tool keeps the content block, reports `missing: ["results[].title"]`, and drops `structuredContent` entirely. Ask for document paths on their own, or address `structuredContent.…` explicitly. **But that case does not shrink the response** — the prose text block is not projected and came back whole (~16 KB), so when size is what you are after, pair `fields` with `max_response_chars` rather than reading a clean `projection` report as a small result. One artifact to know about over MCP: if your projection keeps a `content[]` block of `type: "text"` but not its `text`, the MCP layer re-adds `"text": ""` on the way out (REST returns the block without it), so read `_meta.projection` rather than treating that empty string as something the tool returned. On an HTTP-backed tool none of this applies — there the projection sees the upstream body, which is the same object `result.data` holds.
- **`fields` is ignored outright when `result` itself is not an object or an array**, and says nothing about it. That happens on an **HTTP-backed** tool whose body is not JSON — it arrives as a raw string, and the projection is skipped: `projection` is `null` over REST and absent from `_meta` over MCP, which is not the same as `matched_nothing` and is the one case where a missing report means "never attempted" rather than "everything matched" (live: `fields` on `ClawHub - Get Skill File` returned its whole 25,635-character Markdown body untouched). It does **not** happen on an MCP-backed tool however prose-like its answer is, because `result` there is the envelope *dict* and the projection runs against that as usual. Narrow the request itself on the tools where `fields` can't help.
- **A path that matched nothing is reported, not silently empty.** Write `fields` and `path` against the shape described above, and when a projection comes back empty check the flag before concluding the tool returned nothing: on `execute_tool`, `_meta.projection.missing` lists the paths that hit nothing and `_meta.projection.matched_nothing` is true when none of them matched; on `fetch_result`, `_meta.path_matched` is `false` and the text block says so outright ("Nothing in the stored result matched the path … The result itself is intact"). REST reports the same thing as `path_matched` in the `GET /tools/executions/{id}/result` body. A correct path over an empty collection is not a miss: it comes back as that empty list and is listed in `_meta.projection.empty` (on `fetch_result`, `path_matched: true` plus `_meta.path_empty: true`). So a `false` means the path is wrong; re-read the original shape rather than re-running the tool. The key is *absent*, not `false`, when the backend doesn't report it, so test it as `_meta.get("path_matched") is False`. One more key can appear beside those on `execute_tool`: `envelope_prefix_stripped: true` means at least one path only matched after a leading `data`/`result` segment was peeled off it (the bullet above) — the values are right, so treat it as a note on your spelling rather than a problem. `fetch_result` takes the same peeling step but **reports nothing about it**: that path carries only `path_matched` and `path_empty`, so a `path` of yours may have been peeled silently and there is no key to look for.
- **A path may continue into a string that carries JSON.** MCP-backed tools routinely hand back their real payload as text inside a string, and a path written straight through it used to match nothing. It is now resolved against the JSON document the string carries — either the string that *is* JSON, or JSON fenced in the `<untrusted-data-…>` markers Supabase's MCP server wraps results in — and the fragment comes back parsed, in place of the string. So write `fields` against the shape you can see in the payload and don't route around a string in the middle of it. A path *ending* at a string still returns the string unchanged, and prose with a JSON fragment loose somewhere inside it is still a miss. Since 2026-09-10 the step `<json>` is also accepted and skipped as an interior step, which means a path read straight off `_meta.redaction` — that report spells the same place as `content[0].text.<json>.deployment.phase` — can be pasted into `fields` or `path` verbatim instead of being hand-edited. (Before that date the marker was matched as a literal key and the path silently hit nothing.) The trade is that a real key spelled `<json>` is unreachable; no upstream is known to have one.

### When a call fails, read whose failure it was

A failed `execute_tool` is attributed for you, so you don't have to guess from prose whether
the provider is down, your parameters were wrong, or Danube's own catalog row is stale. Three
fields carry it — `_meta.error_type`, `_meta.fault` and `_meta.retryable` over MCP, the same
three at the top level of the response over REST:

| `fault` | What it means | What to do |
|---|---|---|
| `caller` | The request itself was rejected: a missing or invalid credential, a value the provider correctly refused, a resource you named that doesn't exist, a plan or spending cap | Fix the parameters or credentials before retrying. Not the tool's fault — don't `report_tool` it |
| `upstream` | The third party failed: a 5xx, a timeout, a refused connection, throttling it didn't tie to the user's plan, an MCP server that couldn't be reached | Retrying later may work. This is the only class that moves the tool's reliability score |
| `danube` | Danube's own handling: a stale catalog row, a request it built wrong, a credential it couldn't resolve, an internal exception | Neither a retry nor a `report_tool` helps — a genuine defect here is recorded for repair on its own, and the rest (a sunset tool, a retired service, a disabled tool) are deliberate catalog states, not bugs to chase. Pick another tool or tell the user |

`error_type` is the specific class inside that verdict (`missing_parameters`, `auth_required`,
`rate_limited`, `plan_rate_limited`, `timeout`, `endpoint_missing`, `upstream_tool_missing`,
`bad_request`, `not_found`, …), and `retryable` says whether the *identical* call could succeed
later. **That set is narrower than "every `upstream` type", and it is not one caller-side
exception but two.** `retryable` is derived from `error_type` alone, and exactly nine values
carry it: seven `upstream` ones (`server_error`, `timeout`, `connection_error`, `rate_limited`,
`upstream_error`, `mcp_transport_error`, `dataplane_timeout`) and two `caller` ones
(`plan_rate_limited`, below, and `no_dataplane_agent`, further down) whose window reopens
without anyone changing the call. One `upstream` verdict is deliberately *not* retryable:
`dataplane_execution_failed`, where the organization's data-plane agent ran the call and
reported a failure without saying which kind — unclassified is not known to be transient, so it
answers `retryable: false` despite being `upstream`. An error site that knows more than its type
does may also set the field itself, so read `retryable` as given rather than re-deriving it from
the verdict. Prefer these three fields to matching on the message text,
which is what the rest of this file falls back to for older backends.

**Two of those separate a throttle the user's own plan imposed from one the provider imposed.**
A `429`-style refusal the provider itself explains as *the connected plan's* ceiling — its
message carrying both a throttle word and something like "upgrade your plan", "/pricing",
"quota exceeded" or a monthly/daily limit — is `plan_rate_limited`, which is `fault: "caller"`
and `retryable: true`: the window reopens on its own, so waiting works, but the ceiling is the
user's own plan on that third-party service and calling harder will not move it. A plain `429`
with no such wording is `rate_limited` / `fault: "upstream"`. Since only `upstream` failures move
a tool's reliability score, the split is also what stops a plan cap — hit by fanning parallel
calls through a batch, say — from flagging a tool that works. Don't `report_tool` either one:
tell the user their plan on that service is the limit, and slow down rather than looping.

**That split is narrower than it looks: it needs the provider's own words, so it reaches
MCP-backed results and not an HTTP tool's `429`.** `plan_rate_limited` is decided by reading the
error *text*, which is available on an MCP server's `isError` body. An `api`-service tool's
failure is classified from its HTTP status line by a path that never sees the response body, so
its `429` stays `rate_limited` / `upstream` however plainly the body names the plan — and a
text-classified message that embeds a status (`HTTP 429`, `Client error '429 Too Many
Requests'`) short-circuits the same way, because the status is matched before the wording. This
is a known gap on Danube's side, not something your call can change. So on an HTTP-backed tool,
read a `rate_limited`/`upstream` verdict as possibly still being the user's plan cap, and check
the message before telling them a provider is throttling everyone.

Don't confuse either of these with the account's **Danube** plan quota, which is a different
layer with a confusingly similar name — see *The two `429`s* and *Rate limits* below.

**Over MCP the error text usually repeats the verdict**, opening with `Request error:`,
`<Service> error:` (the service is taken from the tool name's `<Service> - <Action>` shape, and
falls back to `Upstream service error` when the name doesn't have it) or `Danube error:`, then
a sentence of advice. Treat that as a convenience for showing the user, not something to match
on: two of the most common failures — `auth_required` and an insufficient wallet balance —
return their own dedicated text with no prefix at all, and over REST nothing is prefixed. The
three fields are the reliable signal.

Don't confuse `error_type` with the `last_error_class` in a search result's `reliability`
block: they are separate vocabularies. `error_type` is the execution engine's verdict on one
call; `last_error_class` is the reliability view's coarser after-the-fact bucket
(`validation`, `upstream_4xx`, `upstream_5xx`, `timeout`, `other`).

Inside `batch_execute_tools` the same three fields ride on each *element's* own `_meta`, not on
a top-level one — read them per element.

They can still be absent. A failure that never reached the execution engine has none: an
unresolvable `tool_id`, or, over MCP, a `tool_name` whose search came back *empty* or failed
outright (which answers `Tool '…' not found` with no `_meta` at all). That second case is rarer
than it sounds: a name that matches nothing *well* is not a failure at all but a substitution, per
*`execute_tool` resolves a name by searching* above. And a refusal the REST layer turns into a real HTTP status — `402` for a plan
cap, `503` for a disabled tool — *was* attributed, but the status is raised in place of the
body, so the fields don't survive to the caller. Read all three with `.get()` and fall back to
the message whenever they're missing.

### A Google connection can be connected and still refuse

Gmail and Google Drive are one place where `readiness: "ready"` and a working connection still
do not mean a tool will run — not the only one (Slack's `missing_scope` and `not_in_channel`
answer with the same `permission_denied` / `fault: caller` and want a re-authorization or an
invite to the channel, and the enterprise access policy further down is a third), but the one
with the least obvious cause.

Danube's own Google client asks only for the scopes Google approves without a paid security
review — for Gmail that is **send only**. So on a connection whose grant was recorded under that
narrowed client (from 2026-09-26), `Gmail - Send Email` works while `Read Inbox`,
`Search Emails`, `Get Email`, `Reply to Email` and `Trash Email` are refused
before the call, and on Drive a file Danube did not itself create or open is refused too (the
`drive.file` grant cannot see it; its upstream `404` is reported as the scope gap it really is).
`Send Email` plus those five are the whole of Gmail on Danube — **there is no
`Gmail - Get Profile` row to call**, though the engine's scope gate names one (live 2026-10-20:
`GET /v1/services/gmail/tools` returned exactly those six, and `/v1/tools/gmail-get-profile`
answered `404`). Don't reach for
it from this list or any other memory of the service: per *`execute_tool` resolves a name by
searching* above, a name no tool carries runs the nearest result instead of failing.
**An older connection is not affected**: a grant stored before Danube recorded scopes is treated
as holding the full set, so it keeps reading mail, and such a connection only ever hits this if
Google itself answers `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`, which maps to the same error. So
read the error as the authority on what a given connection lacks, rather than assuming every
Google connection is narrowed.

The refusal is `error_type: "permission_denied"`, `fault: "caller"`, `retryable: false`, with a
message naming what the connection lacks and a `configuration_url`. **It is not the enterprise
access policy** described further down, and not a credential to store: the fix is for the user
to reconnect that service with **their own Google Cloud project** ("Connect", then "Use your
own Google project"), which can request every scope. Don't retry it, don't route around it to
another Google tool, and don't `report_tool` it — the tool is fine. Tell the user which
capability is missing and send them to that link.

### When a tool needs credentials

A result containing `"error_type": "auth_required"` (with `fault: "caller"`) usually means this user hasn't connected that service yet — read the `reason` below before assuming it:
1. Prefer sending the user to the `configuration_url` in the error (or https://danubeai.com/dashboard) to connect it — the only path for OAuth services such as Gmail, Slack, or Google Calendar.
2. For API-key services, if the user explicitly gives you the key and confirms, call `store_credential(service_id, credential_type="bearer", credential_value=…)`, then retry.

**Read `auth_required.reason` before you pick one of those two — there are three, and one of
them makes both wrong.** (It sits inside the `auth_required` block, which over MCP is
`_meta.auth_required`, not at the top level.)

- `missing` is the plain case above: nothing is stored, so connect or store a key.
- `rejected` means Danube *does* hold a credential and the service refused it (an upstream
  `401`). The user has to reconnect at `configuration_url`; storing the same key again will not
  help, and neither will retrying.
- `org_policy` means the user's organization has a credential rule for this service, and the
  rule — not a missing key — is why there was nothing to call with. The error then also carries
  `credential_policy` with that rule's `mode`, `org_id` and `org_name` — the last of which can be
  `null`, as the org lookup behind it is best-effort, so fall back to "the user's organization"
  rather than printing "null". When `mode` is
  **`shared`**, the organization requires its own shared credential and has not added one:
  **do not offer `store_credential`**, because a key stored for this user would be ignored.
  Say that an owner or admin of that organization needs to add it in the Danube dashboard.
  When `mode` is `personal` the organization requires each member's own key and ignores the
  shared one, so step 2 is exactly right — ask this user for theirs.

Over MCP the server already writes the `shared` case out in words ("… requires its shared
credential … a personal credential stored with store_credential would not be used"). Take that
at face value rather than falling back to the generic ask-for-a-key script.

`get_service_tools` reports `needs_configuration: true` only when *every* tool of the service is `needs_credential` for this account — every tool it returned, that is, which over MCP is the first 50 at most (see the discovery tip above); it is derived from the per-tool `readiness` field, which is the answer for any single tool. A service mixing credential-free and credential-bearing tools reports `false`, so read `readiness` on the tool you are about to call rather than the service-level flag.

When it *is* true, read the `configuration_required` block instead of guessing what to ask for. The keys are always present: `service_id`, `service_name`, `message`, `configuration_url`, `instructions` and `credential_schema`. `service_name` can still be null (the lookup behind it is best-effort) — fall back to the service you asked about rather than showing the user "null". For a service whose credential shape Danube knows, it also carries a `credential_schema` — the field names, labels, help text and any eligibility notes — and the `instructions` then name those fields ("Ask the user for: …"). `credential_schema` stays `null` for a service with no registered schema, which is common for plain API-key services; there, ask for the one key or send the user to `configuration_url`. Don't invent field names it doesn't list.

**On some MCP services a null `credential_schema` is not the tell it looks like.** A service
whose own MCP server runs an OAuth handshake — Coupler.io and Outreach are live examples —
answers `get_service_tools` with `needs_mcp_oauth: true`. Over MCP that arrives *alongside*
`needs_configuration: true` and a `configuration_required` block whose `credential_schema` is
`null`, which reads exactly like the plain API-key case above; over REST it arrives as
`{"tools": [], "needs_mcp_oauth": true, "mcp_oauth_info": {…}}` carrying **no
`needs_configuration` key at all**, so a curl caller has to test for this one on its own. The
right move either way is to send the user to the dashboard, which runs the handshake:
`https://danubeai.com/dashboard/tools/<service_id>` (over MCP this is already built for you as
`configuration_required.configuration_url`; over REST the response carries no URL, so compose
it from the `service_id`). Then read the tool list again once they say they've connected — the
tools are discovered from the MCP server only after authorization, by the background sync
described below. Two things not to do: don't walk the user through the
`authorization_endpoint` / `token_endpoint` / `registration_endpoint` in `mcp_oauth_info` —
those are the *provider's* and the dashboard is what drives them; and don't reach for
`store_credential` to get around the prompt. That endpoint does not refuse these services — it
will happily store a bearer value and the connection will send it — so a guessed or improvised
token gets accepted, stops *you* seeing the `needs_mcp_oauth` shape, and hides the Connect
prompt behind a credential that doesn't work. (The credential is yours alone, so the prompt is
still there for everyone else — you have hidden it only from yourself.) Store one only if the user actually hands you a
connection token their provider issued.

**This envelope is about the catalog, not about your account.** It appears only while Danube
holds no tool rows for the service at all, so a connector that authorizes by OAuth but whose
tools are already on record never produces it — Notion answers with an ordinary list of its
tools and `needs_mcp_oauth: false` (45 of them live on 2026-10-24, where this file said 44 on
2026-09-15 — a count that moves, so read it off the call rather than from here). Those entries carry the usual per-caller
`readiness`, which is what tells you whether *your* account still needs to connect. So read
`readiness` on the tool you mean to call as the per-account answer, exactly as for any other
service, and treat `needs_mcp_oauth` as the narrower "Danube hasn't seen this server's tools
yet either" case.

**An empty tool list can mean "not yet" rather than "none".** An MCP service's tools are
registered by a first sync that runs in the background (since 2026-09-13), so a service
connected moments ago may have none on record yet — registering a large server's takes tens of
seconds. `get_service_tools` then answers `tools: []` alongside `tool_sync` (`{"status":
"running"}`, later `"done"` or `"failed"`) and a `message` saying to read again; over REST,
`GET /services/{id}/tools` carries `needs_sync: true` as well. **Read it again in a few
seconds.** When the user connects the service in the dashboard the sync starts there; after
your own `store_credential` nothing is running until you read the tool list, and that first
read is what starts it — so the fix is always another read, never a call you have to make.
Treat `tool_sync` defensively: it can come back `{}` with no `status` at all, and over REST it can be missing from the object entirely. Neither `failed`
nor an empty `done` is final — a read five minutes later starts a fresh attempt. The `message`
also names `POST /services/{id}/refresh-tools`, but that endpoint needs the service **owner**
signed in to the dashboard and answers `401` to an API key, so it is something to tell the user
about, not something for you to call. Don't report a service the user just connected as having
no tools, and don't `report_tool` anything — no tool has been called.

`credential_value` takes either the raw secret or a **reference** — a pointer resolved when the tool runs, so the secret is never held centrally.

**References only work on some execution paths.** A reference is resolved on the standard HTTP auth-injection path — an `api` service whose tool isn't one of the provider-specific composite handlers — and by the in-VPC data-plane agent, which runs the services an org has marked `local_only`. Everything else reads the stored string **as the secret**: a hosted `mcp_server` service, and composite handlers for services like Firecrawl or Notion. Give one of those a `vault://…` string and it goes out as the credential itself, and the provider answers `401`. So: **store a reference only for a self-hosted deployment, or for a service that runs on the org's data-plane agent; otherwise store the value.** If you aren't sure which path a service takes, store the value — unless the service is `local_only`, where the paragraph below applies instead.

**On the data-plane path a reference is not merely supported — it is the only thing that works.**
The control plane strips every non-reference value out of the dispatch it sends the agent: a
plaintext secret is replaced with `null` and only its *existence* is flagged, so the value never
leaves Danube. The agent then refuses the call with `error_type: credential_reference_unresolved`
(`fault: "caller"`, not retryable) and a message naming the field — "… exists only as a central
plaintext value. Data-plane execution requires reference-based credentials (env:// or vault://);
re-store it as a reference." Since 2026-09-24 this reaches **MCP** services too: a `local_only`
MCP server has its calls *and* its tool discovery dispatched through the agent, so the
"`mcp_server` reads the stored string as the secret" rule above holds for a **hosted** MCP
service and is *reversed* for a `local_only` one. For a `local_only` service of any kind, ask the
user which form they have rather than defaulting to the value — there is no plaintext fallback.

| `credential_value` | Stored as | Resolves |
|---|---|---|
| `vault://<mount>/<path>#<field>` (the `#<field>` is required) | reference | against the `VAULT_ADDR` / `VAULT_TOKEN` of whatever process runs the tool — your data-plane agent or self-hosted deployment. The hosted service has no per-customer Vault setting, so it can't reach your Vault |
| `env://VAR_NAME` | reference | in the environment where the tool actually runs, so self-hosted / data-plane only. On the hosted service `env://` stores fine but **fails at execution time**: it is off by design there (`DANUBE_ALLOW_ENV_REFERENCES` is a self-hosted/dev switch, not something to ask Danube to enable) |
| the raw key | value | the working default on the hosted service — deprecated but accepted; self-hosted rejects it outright with `central_credential_ingestion_disabled` |

Never invent a variable name or vault path — use only what the user gave you, and ask which form they want if it isn't obvious. A successful store echoes `"stored_as": "reference"` or `"value"`, adding `"deprecated": true` and a `notice` when a plaintext value was stored. Note that a successful store proves nothing about whether the reference will resolve — that only shows up when the tool runs.

### The two `429`s, which share an error code

There are two unrelated refusals behind that status and **`error.code` does not tell them
apart** — both read `rate_limited`. The plan cap is raised as a plain `429` whose detail Danube's
envelope wraps, so it inherits the status's generic code; the rate limiter sets the same string
deliberately. Branch on `error.details`, which is where they actually differ:

| `error.details` holds | Which refusal | What to do |
|---|---|---|
| `usage` and `upgrade_url` (the relative `/pricing` — join it to `https://danubeai.com`) | The account's **plan quota**, which is a monthly one: 5,000 successful calls per UTC calendar month on free, 50,000 on pro, 250,000 on team, uncapped on enterprise | Stop and tell the user, naming the figure — `usage` carries `tier`, `limit`, `current_usage` and `remaining`. Retrying never clears it, and the window is the calendar month, so there is nothing to wait out |
| `retry_after` | Danube's **rate limiter** | Yours to absorb: wait, then retry once. Don't mention it to the user |

Getting this backwards is the failure worth avoiding: an agent that matches `error.code ==
"rate_limited"` and retries will loop on a plan cap the rest of this file tells it to report.

`retry_after` is also in a `Retry-After` header, and `X-RateLimit-Limit` carries the limit that
was hit — as slowapi's description *string* (`"60 per 1 minute"`), not a number, so don't parse
it as one. Read `retry_after` and sleep it rather than inventing a backoff, but don't read
meaning into its value: it is currently a flat **60** on every rate-limited response, not a
computed time-to-reset.

### Rate limits — the budget you are spending

Searching and executing (`GET /tools/search`, `POST /tools/call/{tool_id}`,
`POST /tools/call/batch`) are limited by **API key**, at a rate set by the account's plan: 60
requests/minute on free, 1000 on pro, 2000 on team, 3000 on enterprise (a legacy `starter` tier
still sees 300). A plan upgrade takes up to five minutes to widen it, because the tier behind a
key is cached that long. These three endpoints all require a key, so there is no anonymous rate
to fall back to — a call without one is a `401`, not a slower lane.

**The budget is counted per key *and per URL path*, not as one pool.** Each path keeps its own
bucket, so `/tools/search` and `/tools/call/batch` have separate allowances, and — because the
tool id is *in* the path — so does every individual tool. On the free plan that means 60
calls/minute to any one tool rather than 60 across all of them: hammering a single tool in a
loop is what exhausts a bucket, while spreading work across different tools barely touches it.

**A batch is one request however many calls it carries** — `batch_execute_tools` and
`POST /tools/call/batch` both reach the backend as a single HTTP request (no per-call fallback
loop on either transport). Note *which* bucket that one request comes out of: `/tools/call/batch`
is its own path, so a batch never touches the per-tool bucket at all. Ten calls to the same tool
spend ten of that tool's minute when sent one at a time, and one of `/tools/call/batch`'s minute
when sent together. So batching is the move when you are looping over a single tool — but it is
not a general speed-up, and it buys you **only** rate-limit headroom: each entry is still checked
against the account's plan quota individually, so a batch of ten spends ten executions of the
plan allowance exactly as ten single calls would. Batch only calls you would have made anyway,
and remember a batch still needs the user's explicit yes.

### Paid tools, missing upstream tools, and the hosted-AI caps

**A tool the publisher charges for is refused before it runs, and tells you exactly how short
you are.** The balance check happens ahead of the upstream call, so nothing half-executes. The
verdict is `error_type: "insufficient_balance"` with `fault: "caller"` and `retryable: false`,
and the message is quotable: "Insufficient credits. This tool costs $X.XX. Your balance: $Y.YY.
Add credits at https://danubeai.com/dashboard/finances". Over REST the same two figures come back
machine-readably as `cost_cents` and `balance_cents` — `balance_cents` is the balance that was
too low, not a balance after a charge, because no charge happened. Over MCP neither field exists:
the two figures are in the message text, as dollars. What MCP's `_meta` adds instead is
`insufficient_balance: true` beside the three attribution fields, and the text gains numbered
top-up steps. This is one of the two failures that arrive with no `Request error:` / `Danube
error:` prefix, so match the fields, not the opening words. A tool priced in USDC (x402) refuses
on a **limit** rather than on an empty wallet, and which message you get depends on how it is
priced. Against the price Danube holds on record you get "x402 spending limit exceeded: Exceeds
your per-call limit of $X" (or the platform maximum, or the daily one) — the engine sets no
`error_type` for it, but the phrase "spending limit" is what classifies it onto the same verdict.
A USDC balance too thin for that price is *not* a refusal there: the call falls back to the
ordinary credits wallet and goes ahead. Two other x402 messages exist, and **you cannot tell in
advance which tools produce them** — a search result carries `x402_enabled` and the price, but
nothing an API key can read exposes the pricing *mode*, and `describe` carries no pricing at
all — so match on the message, never on the tool. Both come from a price
re-derived at call time from the upstream's own `PAYMENT-REQUIRED` header, which can exceed what
the earlier check cleared. "Insufficient USDC. Required: $X.XXXX. Balance: $Y.YYYY" classifies
correctly, and over MCP carries the same numbered top-up steps as the credits case. "x402 payment
blocked: …" — carrying the same three limit reasons as above — matches none of the engine's text
rules, so it is mis-filed as `unknown` with `fault: "danube"`, and over MCP it even arrives
prefixed `Danube error:` with advice to wait for a repair. That one is the rare case where the
message beats the verdict: ignore the label, it is the account's own limit rather than a Danube
bug, and there is nothing for you to `report_tool` (the platform files its own row for it). Both
top-up links reach one page:
`/dashboard/wallet` redirects to `/dashboard/finances?tab=wallet`, the same Finances page the
credits message names. Show the user the two figures and the link; don't retry, and don't raise a
spending limit unless they ask for exactly that.

`error_type: "upstream_tool_missing"` is the catalog-drift failure that is **Danube's** fault rather than
yours or the provider's: the catalog row points at a tool its MCP server no longer offers. (It is
a body-shaped error, not an HTTP status — over REST the call still answers `200` with
`status: "error"`; over MCP it arrives as `isError: true` with the fields below in `_meta`.) Danube tries to repair it on the spot first — it re-reads the server's tool list and, if
the tool was merely renamed, re-runs your call under the new name and hands you the real result,
so most drift never reaches you at all. What you see is the case where the tool is genuinely
gone. The response carries `retryable: false`, the `upstream_tool` the row pointed at, and
`available_tools` — the tools the server *does* offer. Take the answer at face value: it has
already been reported automatically, so don't `report_tool` it and don't retry. Pick a
replacement from `available_tools`, or search again.

**A row with no executor behind it is the other Danube-side break, and the fault, not the
`error_type`, is what names it.** Some catalogue rows are `COMPOSITE` ones — `method: "COMPOSITE"` on the row, meaning
Danube runs a multi-step handler for them rather than one HTTP request — and such a row can be
registered while the handler that would serve it never ships. The call then dies in a few
milliseconds, before anything reaches the provider, with `Unknown <Service> composite tool:
<Tool action>` when the service has a handler but not that action, or `Unknown composite tool
service: <Service>` when it has none at all. (Three services word the first one `Unknown <Service>
tool action: <action>` instead — Railway, SEC EDGAR and Rate API.) The verdict is always
`fault: "danube"` with `retryable: false`; the `error_type` is `unknown`, because none of those
messages matches the engine's text rules, unless the handler stamped one of its own on the way
out (Slack's fallthrough sets `internal_error`) — so read the fault, not the type. Take it at
face value: no parameter you change can clear it, a retry cannot either, and the platform files
its own report, so don't `report_tool` it. The rest of the service is usually healthy — reach for
the sibling tool its description names (live: `Kalshi - Get Historical Fills` and `- Get
Historical Positions` were in the catalogue from 2026-09-21 and callable only from 2026-10-12,
while `Kalshi - Get Fills` and `- Get Positions` worked throughout; `Slack - Upload File` was the
same case in September) — or tell the user. **A default search result will not warn you**: such a row
carries a full description and parameter schema, reads `readiness: "ready"`, and because every
failure on it is Danube's it never reaches `success_rate_30d`, `last_error_class` or `flagged`.
A `detail="full"` result or a REST row does carry `faults: {danube: N}`, which is the one place
a listing can show it.
`describe_tool` is where the message surfaces, in `usage.common_errors` — see *`usage` and
`reliability` count different things* under *Discovery tips* above.

Danube's own AI tools carry a **separate daily cap on a free account: 20 successful executions
per UTC day**, on direct `execute_tool` calls as well as on workflow steps. Past it the call is
refused with "Daily limit for Danube's AI tools reached (N/20 today on the free plan). It resets
at 00:00 UTC…" — over REST an HTTP `402` whose `error.code` is `payment_required`, over MCP a
result with `isError: true` quoting the same message in `content[0].text`. Tripping it *inside* a
workflow is not a 402 at all: that step simply fails with the message and the run comes back
`200` with `status: "failed"`. It resets, so it is not the lifetime workflow cap below; either
wait or tell the user to upgrade, and don't `report_tool` it.

**Which tools that covers is a short, exact list — five, not the nine this file used to name.**
The cap, the kill switch and the workflow trial all read one frozen set of tool *names*, and it
holds `Danube - Summarize Text`, `- Extract Entities`, `- Classify Text`,
`- Generate Structured Data` and `- Translate Text` — the five that have an executable handler.
The web-intelligence names beside them — `Danube - Webpage Summary`, `- Extract Structured Data`,
`- Company Research`, `- Discover APIs` — are outside all three gates, and outside execution too:
the onboarding script registers them pointing at handler functions that do not exist, and
dispatch is by display name, so such a call would answer `Unknown Danube tool: <name>. Available:
…` listing the five above rather than running. `Danube - Screenshot` is outside the caps as a
browser capture, as this file has always said — and, like those four, its row points at a handler
that does not exist either.

**In practice, don't reach for any `Danube - …` tool by name.** Checked on 2026-10-11 from a
working key, neither `Danube - Translate Text` nor `Danube - Webpage Summary` resolved to a Danube
row: an exact-name `search_tools` for each returned only unrelated `weak` results, and an exact
name or slug is pinned to the top of the page whatever else re-ordered it, so a reachable row
would have been first. `list_services(query: "Danube")` returned no Danube service either — though that last one is weaker evidence than it reads, since a row the catalogue reports with no tools is dropped from that listing (see *A service the listing reports with no tools* above).
Whether such rows are absent, retired or hidden from a given key, the practical answer is the
same, and name resolution makes guessing worse rather than harmless: `execute_tool` falls back to
the first search result when nothing matches exactly, so a half-remembered `Danube - …` name runs
whatever ranked first. Search for the capability and call what the catalogue actually returns.

### Tools the user's organization registered

Alongside the catalog, an organization can register its own services with visibility `internal` (Danube runs the calls) or `local_only` (the organization's in-network data-plane agent runs them). They show up in `search_tools` and `list_services` only for members of that organization, and only for the tools the organization's policies grant this user; everyone else gets a `404`, the same as a tool that does not exist. Which organization you act in is set by the key: a key created for an organization acts for it on its own, and a `danube-org-id` header (an organization id the user belongs to) chooses one explicitly and wins over the key — **but that header can only ever narrow, and one value of it narrows to nothing.** Every account also has a *personal* organization ("Personal" in the dashboard's workspace switcher), and naming that one puts the request outside every shared organization: its internal tools, its shared credentials and credential rules, its parameter defaults, its skills and its context layer all drop out, and nothing in the response says the header did it. A user who belongs to two or more shared organizations gets a `note` on `GET /v1/context`, but it blames the wrong thing — it reads as "you belong to several organizations, send the header to pick one", which is the advice that caused this. A user in one shared organization gets no note at all. Live on 2026-09-28, one key's `GET /v1/context` returned the organization's layer and six skills with no header at all, and no organization layer and zero skills with the caller's own personal org in the header. So don't set the header to the user's own organization thinking it is the neutral choice: **send no header** unless the user named a shared organization to act in. Over MCP this is handled for you — since 2026-09-27 the server forwards an organization the client asked for, or a shared organization the key is bound to, but never the key's personal-org default. Five things to read:

- **`403` with `Your organization does not have access to this tool`** is the organization's policy, not the key's `allowed_tools`. Don't retry and don't `report_tool` it: tell the user an admin of the organization has to grant the tool (or its service) to them, a team they are in, or their role. A public catalog tool can be refused this way too, when the organization you act in explicitly denies it; that deny does not follow you outside the organization's context. A tool the policy withholds is normally hidden from search, so this mostly appears on an id you were holding.
- **Generic tools on a connected system.** A system an admin connected from one URL carries a small governed surface next to any named tools. For an API it is `<Service> - Request` (parameters `method`, `path`, `query`, `body`, `headers`; the credential is injected for you, so never put one in `headers`). For a database it is `<Service> - List tables`, `<Service> - Describe table` and `<Service> - Query` (one read-only `SELECT` in `sql`). Prefer a named tool when one fits. Otherwise call **List tables** and **Describe table** before **Query**, so the statement names real tables and columns, and keep a Request to `GET` or `HEAD` unless the user asked for a write. The service's access policy decides what these tools may reach: which methods and path prefixes, which tables, which columns come back masked as `[REDACTED:<column>]`, and the row cap.
- **`error_type: permission_denied` with `fault: caller` on one of those tools is the policy, not a bug.** The message names the refused method, path or table. Don't retry the same call, don't look for another path to the same data, and don't `report_tool` it: tell the user what was refused and that an admin can widen the policy on the service page, or promote the call as a named tool. A write (`POST`, `PUT`, `PATCH`, `DELETE`) may instead come back as `confirmation_required` when the policy asks for consent: show the user the call and repeat it with the token, like any other confirmed call.
- **A `local_only` tool whose agent isn't polling fails at once, and it is one of the two retryable `caller` verdicts.** A `local_only` service's calls — and an infrastructure connector's, where the connection stores `env://` / `vault://` references rather than values — run on an agent the organization hosts inside its own network, so if no active agent of that organization has polled within the last **two minutes**, the call is refused before anything is queued — `error_type: "no_dataplane_agent"`, `fault: "caller"`, `retryable: true`, with the message "No data-plane agent is online for this organization." Nothing ran, and nothing about your parameters or credentials was wrong: the organization's agent is down or not enrolled, which is theirs to fix. Because it is retryable the identical call can work once an agent is back, but **don't retry in a tight loop** — a negative liveness answer is cached for five seconds, so an immediate second attempt gets the same refusal from cache without even re-checking. Tell the user their data-plane agent is offline and ask them to start or enroll one. Two neighbours look similar and are *not* retryable: `dataplane_required` (a **database** connector registered on the hosted service without `local_only`, so the row's placement has to change — "No query was run") and `driver_missing` (the agent image was built without that engine's driver). Don't `report_tool` any of the three; none of them says anything about the tool.
- **Connecting or registering a system** is an owner/admin action. `POST /organizations/{org_id}/connect` takes one input (`kind: "api"` with `api.base_url`, `kind: "database"` with `database.connection_ref`, `kind: "mcp"` with `mcp.server_url`) and `"dry_run": true` first, which discovers and previews without writing anything; `POST /organizations/{org_id}/services` with `source` (`openapi_url`, `openapi_spec`, `mcp`, `connector` or `database`) is the advanced path for a document or spec the user already holds. Two visibility rules are worth passing on, both enforced at registration with a `400` (a `dry_run` surfaces the same reason before anything is written, but as a `200` with the text in `errors[]` — read the list, not the status): a **database** connector must be `local_only` on the hosted service, because the query runs where the DSN lives, and anything else is refused with "Database connectors run only through an organization's data-plane agent on the hosted service; register the connector for the organization with visibility local_only" (on the `connect` route, `kind: "database"` defaults to `local_only` for you); and an **MCP** server may be `local_only` since 2026-09-24, but only a *remote* one — a stdio server is refused with "Only remote MCP servers can be registered for an organization" whatever visibility was asked for. Confirm with the user before the real write, like any other. Guide: https://docs.danubeai.com/organizations/internal-tools

## Beyond tools

Available through the same connection, same guardrails:
- **Skills:** `search_skills`, `get_skill`, `create_skill`, `update_skill`, `delete_skill`. Search covers public skills, the user's organizations' internal skills and their own private ones, the last two first; `visibility` (`public`, `internal`, `private`) and `org_name` say which. The skills `get_context` lists are the ones meant for this user: load one with `get_skill` when a task calls for it. `get_skill` returns SKILL.md, every text file with its `path` in the skill folder, and a `download_url` (the whole skill as a zip ready for `.claude/skills/`, fetched with the `danube-api-key` header; binary files are only in the zip). `create_skill` takes `visibility` `private` or `internal` (every member of the organization, `org_id` defaulting to the one the connection acts for); an organization can limit publishing to its owners and admins. To hand a skill the user already has to their team, don't rewrite its visibility — `POST /skills/{id}/share` moves it (same id, same link) and `/skills/{id}/unshare` moves it back; see the workflow bullet below, where the same pair works the same way.
- **Workflows:** `list_workflows`, `create_workflow`, `update_workflow`, `delete_workflow`, `execute_workflow`, `get_workflow_execution`
  - **`list_workflows` takes a `scope`, and since 2026-09-27 it has four values, not
    three.** `"mine"` (yours, private included), `"org"` (the ones a colleague shared with the
    user's organization, which the user runs with their own credentials or the organization's
    shared ones), `"public"`, and `"all"` — the default, which returns yours first, then the
    organization's, then the public catalog. Rows say whose they are: `owned_by_you: true`, or
    `shared_with_org: true` with `org_name`. Reach for `"org"` when the user means "the one the
    team uses" rather than one of their own. Over `curl` the same two lists are
    `GET /workflows/my` and `GET /workflows/my?include_org=true`.
  - **Sharing a workflow with an organization is a move, and it has its own route.**
    `POST /workflows/{id}/share` (optionally `{"org_id": "…"}`, otherwise the organization the
    connection acts for) turns the author's private workflow `internal`, keeping the same id and
    link; `/workflows/{id}/unshare` moves it back and members lose access at once. Only its
    **author** may do either — an organization's own admin gets a `403` — and both are writes,
    so ask first. Don't try it through `PATCH`: moving `visibility` into or out of `internal`
    there is refused with a `400` that names these two routes. Read
    `GET /workflows/{id}/share-check` before sharing one: it reports, per step, whether members
    can see that tool and whose credential the step would run with, and `/share` itself refuses
    with a `400` naming the tools members can't use — every run would fail at that step.
  - **A workflow can carry its own schedule, and the runs it fires are governed differently
    from the call that set it up.** `create_workflow` and `update_workflow` both take `schedule_cron` (a standard
    5-field expression), `schedule_timezone` (an IANA name, default `"UTC"`), `schedule_enabled`
    (default `false`) and `schedule_inputs` (the input object every scheduled run is called
    with). Nothing fires until `schedule_enabled` is `true`, and enabling it with no cron is a
    `400` ("schedule_enabled requires schedule_cron"). The pair is validated on the way in — five
    fields, a timezone `zoneinfo` recognises, and **no faster than every five minutes**
    ("Schedule may not fire more often than every 5 minutes"). `next_run_at` in the response is
    when it fires next, and is `null` whenever either the cron or the enable flag is missing.
    **Only the author may set the cron, the timezone or the enable flag**, and the refusal you
    get depends on how far in you are: a workflow you cannot even read is a `404` ("Workflow not
    found"), one you can read but not manage is a `403` ("Only its author or an organization
    admin can change this workflow"), and only a non-author who *may* otherwise manage it — an
    organization owner or admin, a platform admin — reaches the schedule-specific `403` ("Only
    the workflow's author can schedule it; runs use their credentials"). **`schedule_inputs` is
    not behind that gate**, so such a manager can change what every scheduled run is called with,
    on the author's credentials, without tripping any of the three and without `next_run_at`
    being recomputed. Don't read "author-only" as covering the inputs.
    **Confirm it like any other write, and say that it keeps firing** — it is the one write here
    that goes on acting after the conversation ends. Each run executes as the author, with the
    author's credentials, and with **no API key permissions applied**: a key scoped by
    `allowed_services` / `allowed_tools` limits what you can drive directly and does not limit
    the scheduled runs you set up with it. The backend's own worker (on by default) polls once a
    minute and takes at most 20 due workflows a poll; a backlog built up during downtime
    collapses into one catch-up run rather than a burst, because the next fire time is computed
    from now rather than from the slot that was missed.
    **Reading a schedule back is lopsided.** A listing — `list_workflows`, `GET /workflows/my`,
    `/workflows/public`, `/workflows/org/{org_id}` — carries only `schedule_cron`,
    `schedule_enabled` and `next_run_at` of the six schedule fields (verified live 2026-10-12);
    `schedule_timezone`, `schedule_inputs` and `last_scheduled_run_at` ride on the full row,
    which is the create/update response and `GET /v1/workflows/{id}` and nothing else. No MCP
    tool reads a workflow back, so over MCP you see those three only in the answer to your own
    write — to check a schedule you did not just set, read the full row over `curl`. (The MCP
    server will point you at a `get_workflow` tool for this, in `create_workflow`'s description
    and in a `_note` on every create/update response. **No such tool exists** — the server
    serves 33 and that is not one of them, so don't go looking for it.)
  - **A workflow runs in one of two modes, and `create_workflow` defaults to the simpler one.**
    `execution_mode` is `"template"` unless you say otherwise: numbered `steps`, each naming a
    `tool_id` and wiring its inputs with `{{steps.N.result.field}}` / `{{inputs.field}}`.
    `execution_mode: "instructions"` is the other one — you write `instructions` in prose and
    hand it `allowed_tool_ids`, and a Danube-hosted model orchestrates, choosing which of those
    tools to call and in what order. Both are writes, so confirm first. Instructions mode
    validates up front and refuses with a `400`: an empty `instructions` ("Instructions are
    required for instruction-based workflows"), an empty `allowed_tool_ids` ("At least one
    allowed tool is required"), or an id you cannot see ("Tool not found: …") — so resolve every
    tool with `search_tools` before creating one. `input_schema`, a list of `name` /
    `description` pairs, is optional and tells the orchestrator what the run's inputs mean. One
    thing not to misread as data loss: over MCP the create/update response does **not** echo
    `instructions` back — a 7 KB body is normal for this mode, so the MCP layer replaces it with
    an `instructions_chars` count. Over REST it comes back in full.
  - **In instructions mode the answer is in `output`, not in the step results.** The
    orchestrator's closing message — the synthesis or report the instructions asked for — is the
    execution's `output` field; `step_results` holds only the individual tool calls it made
    along the way, and a template run has no `output` at all. So an agent that reads only
    `step_results`, as *A failed run is not an error status* below otherwise tells you to, will
    report a successful instructions run as if it returned nothing. Read `output` first there
    and fall back to the steps. On a free-tier account an execution of *either* mode also carries
    `hosted_ai_trial_remaining` — how many of the 5 free hosted-AI runs are left *after* this one
    — whenever the workflow **declares** a hosted-AI tool: `allowed_tool_ids` in instructions
    mode, the steps' `tool_id`s in template mode. Declaring is enough, so a run that offered the
    orchestrator such a tool and never called it still reports a number (undecremented; only a
    hosted-AI step that actually succeeded spends one). It is `null` on a paid plan, and on any
    workflow that declares none.
  - **When the orchestrator itself fails, the `error` string says whose fault it is** — and none
    of these is worth a `report_tool`, because no marketplace tool failed. "AI orchestration is
    rate limited upstream right now. Please retry this workflow in a moment. Upstream said: …" is
    the provider throttling Danube, which had already tried up to three times with backoff before
    giving up (sooner, when the wait the provider asks for would blow a 45-second budget shared
    across the whole run) — so retry the run, but not at once. "Danube's hosted AI is unavailable right now, so
    instructions-mode workflows cannot run. This is on Danube's side; retry later." is exactly
    what it says: Danube's own provider account is out of credit, there is nothing the user can
    fix and no parameter to change. Since 2026-09-27 that is what you get; before it, callers
    were handed the provider's own billing text and URL, which meant nothing to them. Any other
    failure of the model call itself reads "AI orchestration error: …". Two more come from the
    orchestration loop rather than the call: "Workflow stopped after 15 orchestration rounds
    without completing its instructions" is the safety limit, and means the instructions were
    only partly carried out — narrow them or split the workflow rather than re-running it
    unchanged; and "Every tool this workflow may use is kept out of hosted AI prompts by its
    organization's settings (Hosted AI can use internal tools is off)" is an organization policy,
    decided before any model call, for the user's admins to change. All of them come back the
    ordinary way — `200` with `status: "failed"` and the string in `error`, not as an HTTP error.
    Where an upstream detail is quoted (the rate-limit and "AI orchestration error" strings, not
    the fixed ones) it is stripped of the provider's organization id and capped at 300
    characters, so a cut-off message there is deliberate.
  - **A workflow execution is trimmed differently from a tool result, so the keys you check are
    not the same.** `execute_workflow` and `get_workflow_execution` take their own
    `max_response_chars` (default 50000, hard max 500000, and the floor is 1000 rather than the
    100 that applies elsewhere). Over the cap, the *step payloads* are what gives: each oversized
    step's `result` becomes `{"truncated": "<prefix>", "_truncation_note": …}` and the execution
    grows a top-level `_truncation_note` naming the full size and the `execution_id` to re-read
    with. There is no `_meta` on a workflow execution and no `_meta.truncated` to test, so the
    rule from *Reading what comes back* does not carry over here. Nor is a missing note proof of a
    whole answer: the step payloads are the only thing this path trims, so an execution with no
    steps to cut — an instructions run that did its work in one long `output` — goes over the cap
    without a note. What is never trimmed is the part you most need: `status`, `error` and
    instructions mode's `output` are preserved whatever the cap.
  - A workflow can outlive the call that started it. `execute_workflow` answering
    `status: "running"` with an `execution_id` means it is **still going, not failed** —
    poll `get_workflow_execution(execution_id)`. Never re-run it: a second concurrent run
    duplicates every write the first one makes. Over `curl` you get a plain timeout rather
    than that response, so treat *any* timeout on an execute call the same way.
  - **A failed run is not an error status.** A workflow whose steps fail still answers
    normally, with `status: "failed"` in the body. Read the body's `status` and the
    per-step results — don't infer success from the absence of an error. (In instructions
    mode read `output` as well, per *the answer is in `output`* above.)
  - HTTP `402` blocks the run before any step executes: a free-tier account gets 5
    *successful* lifetime workflow runs that use a Danube-hosted AI step. The message says
    so verbatim ("You've used all 5 free AI-powered workflow runs…"); match on that and the
    402. The envelope's `code` is `payment_required` — a plan refusal, not an outage.
    Tell the user to upgrade — retrying won't help, *this* cap never resets, unlike the
    daily hosted-AI cap above.
- **Quality signal:** `get_tool_ratings`, `get_my_rating`, `submit_rating`, `report_tool`, `get_recommendations` — if a tool fails or returns bad output, `report_tool` it so it gets fixed. All five want a tool's UUID, and two of them say nothing when they don't get one: read the next section before trusting what they return.
- **Wallet & agents:** `get_wallet_balance`, `get_spending_limits`, `update_spending_limits`,
  `fund_agent_wallet`, `register_agent`, `get_agent_info` — and three of them do not behave like
  the rest of this file's tools: one refuses an ordinary account, one starts a payment without
  checking what kind of account it is, and one creates a whole new account.
  - **`get_agent_info` refuses an ordinary account**, which is the common case rather than an
    edge one. It reads the *agent* profile behind the key, and every account created by signing
    up in the dashboard is a human one, so it answers `400` — "This endpoint is for agents only.
    Use /v1/users/me for human accounts." Over MCP that arrives as a tool error with the REST
    envelope flattened into the text, which reads like a platform fault; it isn't, and there is
    nothing to `report_tool` (live 2026-10-16). For what you probably wanted, `get_wallet_balance`
    answers on any account (`balance_cents`, `formatted`, `has_wallet`) and `get_spending_limits`
    gives the caps; the route the message names has no MCP tool of its own. What a human account
    cannot read this way is the *agent profile* — the USDC figures are not agent-only:
    `fund_agent_wallet` returns the same `balance_usdc`, and the `deposit_address` is a single
    platform address shared by every account rather than one of your own.
  - **`fund_agent_wallet` has no such check, and its two methods top up two different wallets.**
    It works on a human account, and that agent-only refusal is the only check of its kind here,
    so the one tool that starts a payment is the one that never asks what kind of account it is.
    It does know *whose*: both methods act on the caller's own wallets. `method:
    "card_checkout"` returns a Stripe URL that lands in the **credits** wallet (the cents balance
    `get_wallet_balance` reads and a priced tool charges), while `method: "crypto"` returns the
    USDC deposit address. The response's `balance_usdc` is the USDC figure either way, so after a
    card checkout the number handed back is not the balance that is about to change. Neither
    method moves money by itself — the card path returns a URL someone has to complete in a
    browser, the crypto path an address — but both start a funding flow, so get an explicit yes
    first.
  - **`register_agent` creates a separate account, not a sub-account of the user.** It is the one
    tool here that sends no credential at all, so nothing ties the result to the caller: the new
    account gets its own profile under a generated `agent-…@agents.danubeai.com` address (the
    `operator_email` you pass is contact detail, not a login), its own personal organization
    (best-effort — if that step fails, the account and its key are still returned), the free
    tier, and an **unrestricted** API key returned once, in the tool result. Unrestricted is the
    right word: a key made this way carries no per-key scoping at all, so what bounds it is the
    new account's own organization membership at the tool-call boundary, not a permission list.
    Nobody can sign into the account in the dashboard and there is no second copy of that key. So
    this is not a way to give an agent its own access to *this* user's services — it reaches none
    of them — and because creating an account is a state change the MCP hints don't flag, get an
    explicit yes before calling it. The backend also returns a `getting_started` block (the free
    tier, the endpoints, three credential-free tools to try, what to read next) that the MCP
    result has no field for, so over MCP it is dropped silently; `GET /v1/agents/getting-started`
    serves the same block, needs no key, and is the way to read it (live 2026-10-22: `200`).
    Its size is not a fixture to check against: the three tools under `try_first` are picked
    from the live catalogue and carry their full parameter schemas, so the body grew from
    2,727 bytes on 2026-10-16 to 3,212 on 2026-10-22 with nothing about the endpoint having
    changed. Which three they are moves the same way — read what it returns rather than
    remembering a tool from it.
- **Context:** `get_context` (read at session start) and `update_context` (remember a durable fact in the user's personal context). See *Context* below.

### The quality signal: ids that must be UUIDs, and a zero that isn't one

**Every one of these takes a tool's UUID, not the slug the rest of this file tells you to
prefer** — and they fail in four different ways, only one of which is loud.

`submit_rating` and `report_tool` are the loud ones: over MCP they check the value themselves and
refuse before sending anything ("tool_id must be a tool's UUID. Use search_tools to look it up…").
`report_tool`'s `reason` is a closed set too — `broken`, `degraded`, `incorrect_output`,
`timeout`, `other` — refused the same way, before a report is filed.

A UUID that is well-formed but names no tool is a separate case, and since 2026-09-24 it is
answered cleanly: `submit_rating` comes back `404` ("No tool with id …") rather than the `500` it
used to raise. So a `404` here means the id is stale or mistyped, not that rating is broken —
re-resolve the tool with `search_tools` and submit against the id you get back.

Since 2026-09-27 that same `404`, carrying the same message, also answers **a tool you are not
allowed to rate** — one on a service hidden from you. Re-resolving does not clear that one,
because search hides the same tool: if `search_tools` cannot find the tool your id names, stop
rather than looping. `report_tool` refuses a hidden tool with a `404` too, though its message is the plainer
`Tool not found`. Both read as missing rather than forbidden, so a `404` is never by itself
evidence that the tool does not exist. As
with `get_my_rating` below, the status only survives over REST: through MCP the refusal arrives
flattened into a string, so there is no code to branch on and the message is the signal.

`get_my_rating` has no such guard and fails one step later, at the backend, with a `400`. Over
REST that is the ordinary envelope, `{"error": {"code": "validation_error", "message": "tool_id
must be a tool UUID, got: 'gmail-send-email'"}}`; over MCP the same refusal arrives flattened into
a string — `{"error": "API request failed with status 400 (Details: {…})", "isError": true}` — so
there is no `error.code` to match on. Both live, 2026-09-22.

**`get_recommendations` doesn't fail at all, which is worse.** Its `tool_id` goes into a query on
a UUID column inside a `try` that only logs, and the same unresolved string is what the endpoint
excludes from its own results — so a slug raises nothing, matches no co-usage, and quietly leaves
you with the generic popular list. **Judge it by `reason`, which is the part of the tell that holds
still** — `Frequently used together` is a real co-usage hit, `Popular` is the fallback every caller
gets, so a page reading `Popular` all the way down is the failure. The tool turning up in its own
recommendations is the second tell, and worth knowing only as "anywhere in the page": it sits
wherever the popular ranking puts it, which moves. Live on 2026-10-27,
`get_recommendations("supabase-execute-sql")` returned five entries all reading `Popular`, with
`Supabase - Execute SQL` itself *second*, behind `Slack - Post Message` — it was first when this
was checked on 2026-09-22 — while the same call on that tool's UUID returned five entries all
reading `Frequently used together` and left it out.

So take the `id` off the search result for all five, even though the `slug` is what you showed the
user.

Over plain REST one of them does take a slug: `POST /tools/{tool_id}/report` looks the tool up by
id *or* slug and stores the resolved UUID, so the same operation is accepted over curl and refused
over MCP. Sending the UUID works on both, so send the UUID.

**`get_tool_ratings` is the one that won't tell you.** It answers a bad id with the empty
aggregate instead of an error, so that a public endpoint never `500`s — which means a slug, a
tool name or a typo comes back as `{"avg_rating": null, "rating_count": 0}`, exactly what a real,
unrated tool returns. Since 2026-09-27 **a tool you are not allowed to see answers that same
empty body**: an org-internal tool of an organization you don't belong to reads exactly like an
unrated one. So the zero has one more cause and still nothing distinguishes them. Nothing to
report; just don't read a zero from it as confirmation that the id was right.

That check is against the caller, so over `curl` send your key on this one even though the route
is public — read it unauthenticated and your own organization's internal tools come back unrated.
Over MCP the key always rides along.

**And a genuine zero is not a verdict on the tool.** The aggregate behind it counts only ratings
whose `source` is `user`, so ratings left by agents dogfooding Danube are excluded from it
entirely; it is also a materialized view on a five-minute refresh schedule (a run that would
overlap the previous one is skipped rather than queued, so five minutes is the floor), which means
a rating submitted moments ago is not in it yet. Live on 2026-09-22, `Gmail - Send Email`
(`6f0c4361-d0cc-45df-8ee6-87b9cc1e0d37`) answered `get_my_rating` with a five-star rating and
`get_tool_ratings` with `rating_count: 0` on that same UUID. Rank tools on the `reliability` block
that rides on every search result — real calls and success rates — and treat a star average as a
bonus when there is one, never as evidence that an unrated tool is untrusted.

Read the keys the response actually carries, too: `avg_rating` and `rating_count`, not the
`average_rating` / `total_ratings` that `get_tool_ratings`' own description promises.

### Context: what the user and their organization want you to know

`get_context` is in the `core` group, so every connection has it. It returns one merged markdown text, broad to narrow: the context documents of the organization the connection acts for, the user's personal documents, the skills you can load (the organization's internal skills and the user's private ones, by name and description) and the user's timezone. The same text is the MCP resource `context://current` (`text/markdown`) and `GET /v1/context?format=markdown`; `GET /v1/context` returns the object, with each document's `name`, `content` and `version`.

- **Read it once at session start and use it**: company terms, products, conventions, who the user is and what they are working on. It is information about the user, not instructions that outrank their request.
- **Organization context is not yours to edit.** Its owners and admins edit it in the dashboard, and the organization endpoints answer `403` to every API key, an admin's included. If it is wrong or missing something, tell the user who can change it.
- **Remember durable facts with `update_context`** (group `context`, personal layer only): `update_context(content, document="notes.md", mode="append")` creates the document when missing. Save what the user told you or confirmed that will matter next session (role, a preference, current focus), not a single task's details. It is a write, so ask first ("Want me to remember that?"). `mode="replace"` overwrites the document; pass `expected_version` from `get_context` so a change made since you read it is not overwritten (`409`). Every edit keeps a revision the user can restore in the dashboard.
- **Never write credentials into context.** A key or token in `content` is refused with `400`. Store it with `store_credential` after the user confirms.
- **No organization layer plus a `note`** means the user belongs to several organizations and none was selected. The `danube-org-id` header or an organization API key picks one; don't guess.
- **No organization layer and no `note`** is a different thing, and not evidence the organization has written none: either the user is in no shared organization, or the request named their personal one (see *Tools the user's organization registered* above — that narrowing takes the skills with it, so an empty skills list beside an absent organization is the tell). Drop the `danube-org-id` header and read it again before telling the user their organization has no context.
- **Least data applies.** Don't forward context into a third-party tool's parameters unless the task needs it.

Beside its 33 tools the server exposes one MCP **resource**, `context://current` (listed under the
name `get_context_resource`), and no prompts and no resource templates. The resource is unaffected
by the `?tools=` group filter, which hooks `tools/list` only. A failed read is a JSON-RPC error,
not an `{"error": ...}` body. **Don't take the handshake's capabilities block as the inventory**:
`initialize` advertises `prompts` alongside `resources`, `tools` and `logging` even though the
server registers no prompt at all, so a client that reads capabilities rather than calling the
list methods will expect prompts this server has none of. Live on 2026-10-14, beside a
`prompts: {"listChanged": true}` capability, `prompts/list` answered `{"prompts": []}` and
`resources/templates/list` answered `{"resourceTemplates": []}`. Ask for the list.

**OpenClaw is one of those clients, which is where the extra four tools in *Connect natively over
MCP* come from.** It reads the advertised `prompts` and `resources` capabilities and synthesizes a
tool for each list and fetch method — `danube__prompts_list`, `danube__prompts_get`,
`danube__resources_list`, `danube__resources_read` — so they appear beside the 33 whether or not
the server has anything to put behind them. Two consequences: the prompt pair is dead weight here
and `danube__prompts_list` will always answer empty, and `danube__resources_read` points at the
same merged markdown `get_context` returns rather than at anything new — the single resource it can
read is `context://current`, whose own description says it carries "the same text the get_context
tool returns as `markdown`", and a live `resources/read` on 2026-10-27 returned exactly that.
Prefer `get_context`; it is the one this file's advice is written around.

Something not working? `{baseDir}/references/troubleshooting.md`

## Links

- Dashboard: https://danubeai.com/dashboard · Docs: https://docs.danubeai.com · OpenClaw guide: https://docs.danubeai.com/sdk/openclaw
- MCP server: https://mcp.danubeai.com/mcp · Privacy: https://danubeai.com/privacy · Terms: https://danubeai.com/terms
