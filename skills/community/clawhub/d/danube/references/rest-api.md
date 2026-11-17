# Danube over plain HTTP (no MCP required)

Everything the Danube MCP tools do is also a REST call. Use this when the
agent only has `curl` and `DANUBE_API_KEY` (which is exactly what this skill
gates on), or when you want to see raw responses.

```bash
BASE="https://api.danubeai.com/v1"
AUTH="danube-api-key: ${DANUBE_API_KEY}"
```

All examples below assume those two variables. Responses are JSON.

## Discover

```bash
# Semantic search across every tool you can see (catalog + your org's private tools). An
# organization's `internal` / `local_only` services are included for its members, minus the
# tools its policies do not grant this user; a `danube-org-id` header (an org id the user
# belongs to) picks which org you act in, and a key created for an org acts for it without one.
# That header only ever NARROWS: point it at the account's own *personal* org and the request
# acts for no shared org at all — internal tools, the org's shared credentials and credential
# rules, parameter defaults, org skills and the org context layer all drop out, with nothing
# in the response saying why. Send no header unless the user named a shared org.
# Describe the outcome, not the API: "send an email", "create a GitHub issue", "translate text".
curl -s -G "$BASE/tools/search" -H "$AUTH" --data-urlencode "query=send an email"

# Narrow to one service, or by tag:
curl -s -G "$BASE/tools/search" -H "$AUTH" --data-urlencode "query=issue" --data-urlencode "service_id=<SERVICE_ID>"
# <SERVICE_ID> must be the UUID. Unlike `/services/{id}/tools` and `/tools/{id}/describe`, which
# resolve a slug, this filter is an exact match on the `service_id` each tool row carries, so a
# slug scopes the search to no service and the route answers `[]` with nothing saying why.
# Live 2026-10-17: `service_id=gmail` on "send email" returned [], the service UUID returned six
# tools led by Gmail - Send Email, and `GET /services/gmail/tools` listed all six by slug.

# Narrow the page and the field: limit is 1-100 and is applied LAST, after ready_only and
# min_success_rate, so those filters never eat into your page. (The candidate pool is ~30
# before filtering, so a limit above that can still come back short. `num_results` is an
# older alias kept for the Python SDK; `limit` wins if you send both.) A tool whose name or
# slug is exactly your query is pinned first, so an exact name puts that tool at results[0].
curl -s -G "$BASE/tools/search" -H "$AUTH" \
  --data-urlencode "query=Stripe - Api Read" --data-urlencode "limit=1"
curl -s -G "$BASE/tools/search" -H "$AUTH" --data-urlencode "query=send an email" \
  --data-urlencode "ready_only=true" --data-urlencode "min_success_rate=0.9"
# ready_only keeps only tools this key can run right now; min_success_rate drops tools whose
# 30-day rate is known and below the bar (tools without a meaningful sample are kept).

# `connected_as` is the readiness-side field this route has that no MCP tool reports. It sits
# beside `readiness`, is filled only when `readiness` is "ready", and holds the identity the
# provider handed over when the credential was connected. It answers "as whom will this run",
# which `readiness` does not: Gmail takes the From header from the OAuth grant with no override.
# Not always an email — the extraction prefers one, then falls back to any stable handle the
# provider offers (an OIDC preferred_username, a Notion owner name, Slack's opaque
# authed_user.id) and finally to Slack's WORKSPACE name, so "Danube HQ" is a possible value and
# names the team rather than the actor. `null` when the provider offered nothing, and absent of
# a label entirely on a credential stored as a plain API key: it is written only on the OAuth
# callback. Three routes carry it — this one, `GET /services/{id}/tools` and
# `GET /services/public/{service_id}/tools` — and only for a caller sending a key, since the
# label is looked up against that caller's credentials. /tools/{id}/describe computes readiness
# but builds its own answer copying just `readiness` and `configuration_url`, and the MCP result
# model has no such field at all (so detail="full" does not help). Read it before sending or
# posting as a particular identity.

# All services visible to this key (includes the organization's private services).
curl -s "$BASE/services" -H "$AUTH"
curl -s "$BASE/services?service_type=api" -H "$AUTH"        # api | mcp_server | internal
# `limit` is accepted here but only bites when you also send `query` — without one you get the
# WHOLE catalogue however small a limit you asked for (?limit=3 returns every service the key
# can see, some five hundred of them; ?service_type=mcp_server&limit=3 returns every MCP one).
# Re-measured on 2026-10-14: ?limit=3 came back with 517 services and 1,619,339 bytes of JSON —
# each row carries 55 fields, so this is a real context bill, not just a long list. It grows with
# the catalogue (496 services and ~1.5 MB on 2026-09-16, 516 and ~1.6 MB on 2026-10-03), so read
# whatever figure is written here as a floor.
# So pass a query, or filter what comes back yourself; don't let the whole catalogue land in
# your context expecting the limit to hold. The MCP `list_services` tool does not have this
# problem: its client trims the list to `limit` after the call.
curl -s -G "$BASE/services" -H "$AUTH" --data-urlencode "query=email" --data-urlencode "limit=5"
# Both service lists are served from a 60-second cache: a service connected or published moments
# ago can be missing for up to a minute. Tool search and a service's tool list are not cached.

# Public catalog only — no key needed. category = communication | productivity | development |
# data | finance | marketing | social | analytics | security | infrastructure | ai_ml | design |
# education | health | other. sort = popular | new | name | trending.
curl -s "$BASE/services/public?category=communication&sort=popular&limit=20"

# Every tool of one service — a bare JSON array when there are tools to list. An MCP service
# with none answers an OBJECT instead, which is the case worth handling (an `api` service with
# no tools just returns []). An MCP service's tools are
# registered by a first sync that runs in the background (since 2026-09-13), so one connected
# moments ago answers:
#   {"tools": [], "needs_sync": true,
#    "tool_sync": {"status": "running"},
#    "message": "<Service> is connected and its tools are being discovered. Read again in a
#                few seconds."}
# Read it again in a few seconds. There is nothing to start: this read is what starts the sync
# (your credential store does not) and what restarts one a backend restart lost. Neither a
# "failed" status nor a "done" that still lists no tools is final — a read five minutes later
# tries again, and the message then explains what went wrong. It also names
# POST $BASE/services/<SERVICE_ID>/refresh-tools, but that needs the service OWNER signed in to
# the dashboard and answers 401 to an API key, so it is for the user, not for this script.
# `tool_sync` may also be missing from the object altogether — don't subscript it. Two other
# object shapes come back from this same endpoint: {"needs_configuration": true,
# "configuration_info": {...}} and {"needs_mcp_oauth": true, "mcp_oauth_info": {...}}. So test
# for a dict before iterating.
curl -s "$BASE/services/<SERVICE_ID>/tools" -H "$AUTH"
# This route takes no "limit" and returns every tool the service has — so it is the complete
# answer and the place to check whether a big service really lacks a capability. (The MCP tool
# of the same name is the one with a cap: its `limit` defaults to 50, it says nothing when it
# cuts, and it cuts on every service type, not just MCP servers.)
# How big "big" gets, live on 2026-10-23: 14 services carry 100 tools or more, Vercel alone is
# past 150 with 407, and the next nine are Campfire 142, Unusual Whales 132, Cal.com 125,
# Intercom 121, Braze 116, Similarweb 115, Zoom 114, Ramp 112 and Auth0 107. Higgsfield, which
# earlier versions of this file named beside Vercel as one of the largest, is eleventh at 105.
# Read it all as a snapshot: the figures are the `tool_count` on each /services row (confirmed
# against this route, which returned 142 rows for campfire and 407 for vercel), and an
# mcp_server's count moves on its own as the upstream changes — Higgsfield held 101 on
# 2026-09-20 and 105 since 2026-10-20 — so don't reason from a count you remember.

# The needs_mcp_oauth shape is the one to test for separately, because it carries NO
# "needs_configuration" key — a script that only checks that one reads it as "no tools":
#   {"tools": [], "needs_mcp_oauth": true,
#    "mcp_oauth_info": {"service_id": "...", "service_name": "Coupler.io",
#                       "message": "Coupler.io requires authentication via its own OAuth flow",
#                       "authorization_endpoint": "https://auth.coupler.io/oauth2/authorize",
#                       "token_endpoint": "...", "registration_endpoint": "...",
#                       "scopes_supported": ["mcp"], "auth_server_url": "..."}}
# The service's own MCP server runs the handshake and the Danube dashboard drives it, so those
# endpoints are not for this script to call. There is no configuration_url in the response
# either — compose it as https://danubeai.com/dashboard/tools/<SERVICE_ID>, send the user
# there, and read the tool list again after they connect. Don't route around the prompt with
# POST $BASE/credentials/store: that endpoint does not refuse these services, so an improvised
# token is accepted, sent as the bearer on the MCP connection, and stops YOU seeing this shape
# (the credential is per-account) — leaving a service that looks connected and fails every call.
# Store one only if the user hands you a connection token their provider actually issued.
# This shape only appears while Danube holds no tool rows for the service at all. A service
# that authorizes by OAuth but already has tools on record answers with the ordinary array
# instead, each entry carrying its own per-caller "readiness" — so read readiness per tool as
# the per-account answer, and treat needs_mcp_oauth as the narrower catalogue-side case.

# Everything needed to call one tool well: the schema, `required`, `output`, `tips`, your
# `readiness` and `configuration_url`, `defaults` (what you may omit), the same `reliability`
# block a search result carries, `usage`, and `examples`.
# Takes a slug as readily as a UUID (".../tools/gmail-send-email/describe").
# Mind the scoping of the last two, which sit side by side but answer different questions:
#   usage    -> last 30 days across ALL callers (calls, success_rate, p50_seconds,
#               common_errors), sampled from the most recent 500 executions in that window —
#               how the tool behaves for everyone.
#   examples -> YOUR account's last 3 successful calls, with no time window, so an entry can
#               be old enough to predate a schema change. Each is {parameters, executed_at},
#               where `parameters` is a real call's stored request_params verbatim: copy the
#               shape, not the values. Credential-shaped values have been masked since
#               2026-09-02 (rows written before that were not backfilled), but ordinary
#               personal data never was — so re-sending one unchanged can repeat a real
#               action against a real third party.
curl -s "$BASE/tools/<TOOL_ID>/describe" -H "$AUTH"

# This one works again. Until 2026-09-24 the bare per-tool endpoint answered 422 asking for a
# query parameter `r` that no caller could satisfy, because its auth dependency was written as
# Depends(lambda r: ...) and FastAPI read that lambda's unannotated `r` as a required query
# parameter. Fixed: verified live 2026-09-24, it returns 200 with the full tool row both plain and
# with a leftover ?r=1 (the parameter is simply ignored now). Expect the old 422 only from a
# backend deployed before that date. It takes a slug as readily as a UUID, same as /describe.
#
# The two are NOT nested, so pick by what you need. /describe adds what you want before
# executing: `required`, `usage`, `examples`, `defaults`, and POPULATED readiness,
# configuration_url and reliability — the bare route declares those three and returns null,
# because it runs no enrichment. The bare route carries the plumbing /describe drops: base_url,
# path, slug, tags, version, metadata, security_schemes and sunset_date (note that one — the
# deprecated/sunset trio is only complete here). Its pricing fields are unenriched defaults, so
# is_paid reads false and price_per_call_cents null even on a priced tool: read a price off a
# search result, never off this route. It also takes a `model` query parameter that reshapes the
# response into a provider format.
curl -s "$BASE/tools/<TOOL_ID>" -H "$AUTH"

# NOT the collection route, though — that one is the only call in this file not to make even
# once. GET $BASE/tools takes no pagination parameters at all and returns every tool row the
# caller may see (the catalogue held 12,583 rows on 2026-09-24 and 12,740 on 2026-10-23), and no
# call gets an answer out of it: probed four times on the earlier date it returned 500 (after
# 9-12s) or, past the edge's ~31s ceiling, 504. The 500 is deterministic and is Danube's own
# bug, not yours: the route is declared -> List[Tool] while its query selects five columns
# (id, name, description, tags, service_id), so every row fails response validation on
# base_url/path/method/version. The reason to avoid it rather than just skip it is that the cost
# can land on other callers: live on 2026-10-23 one such call returned 504 after 31.3s and the
# whole API was unreachable for about three minutes — the next request came back as the
# platform's "no_healthy_upstream" page, three GET /health calls returned 504, and the /health
# that finally answered reported a seconds-old process where a 23-hour-old one had been
# answering a few minutes before. No deploy explains that restart and nothing was filed as an
# error, though whether the call caused it was not established. Don't call it, don't retry it,
# and don't reproduce it to find out; nothing to report either. Use /tools/search for discovery,
# or /services/<SERVICE_ID>/tools for one service's full list.
# curl -s "$BASE/tools" -H "$AUTH"   # <- don't

# And if the catalogue's SIZE is all you wanted, this answers it in one cheap call. No key
# needed, rate-limited at 30/minute, body cached five minutes (so it is not a freshness check —
# a service published moments ago has not moved it, and a second call inside the window returns
# the identical body). Live at 12:14 UTC on 2026-10-28:
#   {"services": 517, "tools": 12740, "workflows": 0, "total_executions": 19521}
# Only the last of the four really moves. `services` has not moved since 2026-10-10, and `tools`
# is nearly as static: it has read 12,740 at every reading taken here since 2026-10-23, and 12,737
# on 2026-10-19. total_executions climbs all day, and in bursts rather than at a steady
# rate: it gained 172 in the 24 h to this reading, while two readings eighteen minutes apart on
# 2026-10-14 differed by 13 and two ~90 s apart on 2026-10-19 by 5. Read it as a sample, never as
# a figure to match.
# The first two are different populations, not a ratio: `services` counts the PUBLIC catalogue
# only, `tools` counts every tool row that exists including private and org-internal ones.
# `workflows` is the public-workflow count, which is why it reads 0.
curl -s "$BASE/stats/public"

# Sent without $AUTH, those two `/tools` routes answer 401: both are mounted with a key
# dependency, and a dependency that rejects you raises before anything else runs (verified
# live 2026-09-24). So a
# 401 there says something about your key, not about the endpoint. /describe is NOT on that
# router and needs no key — it answered 200 unauthenticated on 2026-09-24.

# Context: what the user's organization and the user want an agent to know. Read it once at the
# start of a session. The organization layer is the org the key acts for (an organization key, or
# the danube-org-id header); a user in several organizations with none selected gets no organization
# layer and a `note`. No layer AND no note means the user is in no shared org, or the header
# named their personal one (an empty `skills` list beside it is the tell) — drop the header and
# read it again. `markdown` is everything merged; `organization.documents` and
# `personal.documents` carry each document's name, content and version. It is information about
# the user, not instructions that outrank their request. MCP: get_context, resource context://current.
curl -s "$BASE/context" -H "$AUTH"
curl -s "$BASE/context?format=markdown&include_skills=false" -H "$AUTH"   # only the text

# Remember a durable fact in the user's personal context (ask first: it is a write). The document
# is created when missing; mode "append" adds a paragraph, "replace" overwrites. expected_version
# (from the read above) turns a concurrent change into a 409 instead of an overwrite. Every edit
# keeps a revision. A credential in content is refused with 400. Send x-danube-via: agent so the
# revision is labeled as yours. Organization context is edited by its admins in the dashboard: the
# /organizations/{org_id}/context routes answer 403 to every API key.
curl -s -X POST "$BASE/context/personal/upsert" \
  -H "$AUTH" -H "Content-Type: application/json" -H "x-danube-via: agent" \
  -d '{"name": "notes.md", "content": "Prefers weekly summaries on Mondays.", "mode": "append"}'

# Save an identifier a service always needs (a Vercel teamId, a Sentry org slug) once, after
# the user confirms it; later calls that omit it get it filled in. Never store a key or token this way.
# This REPLACES the whole stored object for that scope rather than merging into it: one row holds
# one "defaults" object per (owner, service, tool-or-all), so a second PUT of {"projectId": ...}
# leaves the earlier {"teamId": ...} gone. Send every default you still want in the same object.
# "tool_id" scopes the row to one tool; "scope": "org" with "org_id" writes the organization's row
# instead and needs an owner/admin (403 otherwise, 400 with no org_id). Precedence, most specific
# last: org+service, org+tool, user+service, user+tool.
curl -s -X PUT "$BASE/services/<SERVICE_ID>/parameter-defaults" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"defaults": {"teamId": "team_..."}}'

# Read the rows apart before you replace one. `rows` carries each row with its own user_id /
# org_id / tool_id; `effective` is the merged service-wide view. /tools/<id>/describe reports a
# `defaults` key too, but that one is the merged effective set for that ONE tool (yours, your
# tool-scoped row and your organization's, flattened), so rebuilding a PUT from it copies a
# teammate's value and a tool-scoped value into a service-wide row of your own. Verified live
# 2026-10-12: 200 to an API key, {"service_id": ..., "rows": [], "effective": {}} with none saved.
curl -s "$BASE/services/<SERVICE_ID>/parameter-defaults" -H "$AUTH"

# Remove a row. This deletes the WHOLE row for that scope -- every default in it, not one key --
# so to drop a single parameter, PUT the keys you still want instead (the save replaces the
# object). Unlike the PUT, these go on the QUERY STRING, not in a JSON body: a body here is
# ignored, scope falls back to "user", and you silently delete your own row instead of the org's.
# Why you would: a saved default is applied to a parameter you omit AND to one you send as null or
# "", so an explicit empty value cannot override it. Answers {"deleted": true|false}.
curl -s -X DELETE "$BASE/services/<SERVICE_ID>/parameter-defaults" -H "$AUTH"
curl -s -X DELETE "$BASE/services/<SERVICE_ID>/parameter-defaults?tool_id=<TOOL_UUID>" -H "$AUTH"
curl -s -X DELETE "$BASE/services/<SERVICE_ID>/parameter-defaults?scope=org&org_id=<ORG_ID>" -H "$AUTH"
```

**The discovery endpoints answer with a bare JSON array**, not an object wrapping one:
`GET /tools/search`, `GET /services`, `GET /services/public` and `GET /services/{id}/tools`
return `[ … ]` at the top level, so index straight into it rather than reaching for a `results`
or a `tools` key — those belong to the execution endpoints, not here. The first three are
always a list. `GET /services/{id}/tools` is the one that varies: when an **MCP** service has no
tools to give you it answers with an object instead, saying why (a sync still running, a
credential needed, an MCP OAuth flow to complete — see the recipe above), so check for a `dict`
there before iterating.

A tool object — as it comes back from search and from a service's tool list — looks like
(`/describe` reports the same schema under slightly different keys: `tool_id` rather than `id`,
`method` and `required` as well, and no `slug` and no pricing fields):

```json
{
  "id": "6f0c4361-d0cc-45df-8ee6-87b9cc1e0d37",
  "name": "Gmail - Send Email",
  "slug": "gmail-send-email",
  "description": "...",
  "service_id": "...",
  "deprecated": false,
  "deprecation_message": null,
  "sunset_date": null,
  "parameters": {
    "to":      {"name": "to", "type": "string", "description": "...", "required": true,  "location": "body"},
    "subject": {"name": "subject", "type": "string", "description": "...", "required": true, "location": "body"},
    "body":    {"name": "body", "type": "string", "description": "...", "required": false, "location": "body", "enum": null, "default": null}
  },
  "is_paid": false,
  "price_per_call_cents": null,
  "x402_enabled": false,
  "x402_price_usdc_atomic": null,
  "tips": "optional usage notes written by the publisher"
}
```

Read `required`, `type`, `enum`, and `tips` before executing. Ask the user
for any required value you don't have.

**A parameter too complex for its `type` string carries `json_schema` beside
it.** When `type` reads `object (N properties)`, or the field is an array of
objects or a union, the property names are lost from the summary, so the
parameter gets a `json_schema` key holding the upstream JSON Schema for that
field — properties, types, bounds, per-field descriptions. For example
`Apify - Call Actor`'s `callOptions` reads `object (5 properties)` and its
`json_schema` gives `build`, `memory` (a number, 128–32768), `timeout`,
`maxItems` and `maxTotalChargeUsd`; `Apify - Fetch Actor Details`' `output`
reads `object (9 properties)` and lists all nine booleans. Fill a nested
object from it rather than guessing the keys.

Two limits on reading it. **Test the value, not the key's presence** — the
same rule as the pricing fields below: `GET /tools/search` returns an
explicit `"json_schema": null` on a parameter that has none, while
`GET /tools/{id}/describe` and `GET /services/{id}/tools` omit the key
entirely. And **it is populated for MCP-backed tools only**, by the MCP
catalog converter, so a missing one does not mean the parameter is simple:
an API-backed tool's complex body parameter comes back as a bare `object`
with no `json_schema`, its shape spelled out in the parameter `description`
instead (`Airwallex - Create Payment Intent` does this for `order`,
`customer`, `payment_method` and more). It is catalog metadata either way —
the execution engine never reads it, so nothing checks your object against
it before the upstream does.

Those four pricing fields are the only place a price is exposed before the
call: `is_paid` with `price_per_call_cents` for a tool the publisher charges
credits for, `x402_enabled` with `x402_price_usdc_atomic` for one priced in
USDC. Search carries all four on both transports, nulls included; on
`GET /services/{id}/tools` a price field that is null is omitted rather than
returned as `null`, so test the value, not the key's presence. Nothing an API key can read exposes the pricing *mode*, which is a
separate matter — see the `x402` rows in the error table below.
`GET /tools/{tool_id}/describe` returns **none** of them (verified
live — its keys are `tool_id`, `name`, `description`, `service_id`, `method`,
`parameters`, `required`, `output`, `tips`, `deprecated`,
`deprecation_message`, `readiness`, `configuration_url`, `usage`, `examples`,
`defaults`, `reliability`), so read the price off the search result rather
than calling `/describe` for it. `GET /tools/public/{tool_id}` is not a
substitute either: it carries `x402_enabled` and `x402_price_usdc_atomic`,
but its `is_paid` is always `false` — that route never loads publisher
pricing, so a credits-priced tool reads as free there — it has no
`price_per_call_cents` at all, and being the unauthenticated catalogue route
it gives you no per-caller `readiness`.

Tell the user what a paid call costs before making it: a *credits* balance
below the price is refused before the upstream call, so reading the price
first saves a round trip. A thin *USDC* balance is the exception — it falls
back to the credits wallet and the call goes ahead (see the `x402` rows in
the error table below).

`slug` is a human-readable identifier accepted anywhere a tool id is executed
or inspected — `GET /tools/{id}/describe`, `GET /tools/{id}`,
`POST /tools/call/{id}` — so it is
the better thing to show the user when confirming a call. The ratings
endpoints are the exception and want the UUID: see *Rate and report a tool*
below. `deprecated: true` with a `sunset_date`
still in the future (or absent) is an advance warning on a tool that still
works; read `deprecation_message` for the replacement. Once the date has
passed the tool is dropped from search results and the execute call is refused
before anything is called (see the table below).

## Execute

Get the user's explicit confirmation first for anything that writes, sends,
deletes, spends, or stores a credential (see the guardrails in `SKILL.md`).

```bash
# One tool. Wrap the parameters in "tool_input". The wrapper is optional for the parameters
# themselves -- a body with no "tool_input" key IS the tool input (body.get("tool_input", body)),
# so {"limit": 2} and {"tool_input": {"limit": 2}} run the same call -- but "fields",
# "confirm_token" and "timeout_seconds" are read ONLY when the body carries a "tool_input" key.
# Without the wrapper they are taken for tool parameters and dropped as undeclared, and the call
# still answers 200. Verified live 2026-10-22, {"limit": 2, "fields": ["[].title"]} on Hacker
# News - Get Top Stories With Content answered 200 with "projection": null and the whole payload,
# while the enveloped form returned the two titles with "projection": {"fields": [...],
# "missing": []}. Since 2026-10-24 the envelope at least NAMES the drop on the standard HTTP
# execution path: "dropped_unknown_params": ["fields"]. That tool is a COMPOSITE, which computes
# no such list, so there it stays silent -- but live 2026-10-25 the same bare shape on the HTTP
# tool ClawHub - Get Skill answered 200 with "projection": null and exactly that list, which is
# the one machine-readable sign your control was eaten rather than honoured.
# Only "max_response_chars" is read in either shape. The one that costs you a round trip is
# "confirm_token": sent bare it never reaches the consent check, so the call answers 409 again.
# And there is no "parameters" alias on this route -- that one is MCP's, and even over
# REST a batch entry does not take it either (see the batch section below):
# {"parameters": {"limit": 2}} answered 200 with TEN stories and
# "request_params": {"parameters": {"limit": 2}, "limit": 10} -- the wrapper kept as an
# undeclared parameter, the schema default filling in the limit that never arrived. With a
# required parameter it fails instead, naming what you sent: error_type "missing_parameters",
# "Missing required parameters: q. Provided parameters: parameters."
curl -s -X POST "$BASE/tools/call/<TOOL_ID>" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"tool_input": {"to": "someone@example.com", "subject": "Hello", "body": "Hi there"}}'

# An MCP-BACKED tool that does real work before answering (an actor run, a crawl, a
# server-rendered report) can be given longer than the ~30s default: "timeout_seconds" sits
# beside "tool_input", 1-300. On an `api` service it is accepted and ignored — an HTTP tool's
# budget comes from its own catalog row and a caller cannot raise it, so narrow the request
# instead. Past 300s use the service's own async start/poll tools either way.
# A CONNECTOR tool (method "CONNECTOR": PostgreSQL, Redis, Kubernetes, the AWS ones, ...) is
# the third case: there "timeout_seconds" and "max_rows" are tool PARAMETERS, so they go INSIDE
# "tool_input" -- beside it they are the budget above and never reach the connector. The timeout
# ceiling is 55s, not 300 (the data plane's dispatch budget is 60s), default 15, and it applies
# to every connector call even on the many ops that don't advertise the pair (each Test
# Connection, most single-item reads, 9 of the 13 write tools). Bounds vary by op, so read
# describe_tool: shared max_rows is 500/5000, but DynamoDB Scan is 100/1000 and Kafka Peek
# Messages 20/500 (raise "count" there, not "max_rows"). Both clamp silently and nothing reports
# the value that applied, Scan's result.max_rows aside. On an op that does not declare the pair
# the timeout still applies, but "max_rows" is accepted and ignored.
curl -s -X POST "$BASE/tools/call/<TOOL_ID>" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"tool_input": {"url": "https://example.com"}, "timeout_seconds": 120}'

# Keep big results out of your context: name the paths you want. The result is stored under
# the returned execution_id — what is stored is the shaped response, i.e. everything left after
# this call's own "max_response_chars" (default 500000 over REST, clamped at 2,000,000 — higher
# than the 500000 ceiling the MCP server enforces; a tool that declares its own
# `metadata.max_response_chars` raises BOTH its default and that clamp for itself, which is how
# `Wikimedia Commons - Get File Bytes` returns a 3,173,276-character `content_base64` whole over
# REST with nothing sent, verified 2026-10-21) was applied, and "fields" is projected
# afterwards, so the stored copy still holds the paths you did not ask for. Any other part of it
# can be read back later without re-running the tool.
curl -s -X POST "$BASE/tools/call/<TOOL_ID>" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"tool_input": {"query": "..."}, "fields": ["items[].name", "pagination.next"]}'
curl -s -G "$BASE/tools/executions/<EXECUTION_ID>/result" -H "$AUTH" --data-urlencode "path=items[3]"
# The read-back has a cap of its own: "max_chars", default 50000, clamped to 100-2,000,000 here —
# the same ceiling the execute call uses, and four times what fetch_result can return over MCP,
# which re-applies its own 500000 silently. It trims the same way an execution response does (a
# JSON array loses whole elements off the tail, so the body stays valid JSON of the same shape and
# is simply short) and reports it as top-level "truncated" — read that before treating a fetched
# result as the whole stored copy. Probed live on 2026-09-20 against a stored 194-element result:
# a bare call on that handle returned 32 elements with "truncated": true, and the call below
# returned all 194 with "truncated": false.
curl -s -G "$BASE/tools/executions/<EXECUTION_ID>/result" -H "$AUTH" --data-urlencode "max_chars=500000"
# The stored copy is itself capped at 1,000,000 serialised chars — rarely the binding limit,
# since the shaping above (500000 by default) has usually already cut in; it only bites when
# this call asked for more than 1,000,000. When one was, the body carries "stored_truncated": true and a
# "stored_meta" block with the original size and what was dropped (whole array elements off
# the tail for JSON; a plain-text result is cut at the limit) — don't page a capped handle
# looking for elements that were never stored, narrow the original call instead.
# (fetch_result over MCP does not surface those two keys.)
# When you pass `path`, the body also carries "path_matched". False means nothing in the stored
# result matched — which otherwise looks exactly like a stored null or an empty list — so re-read
# the shape rather than concluding the tool returned nothing. The projected call above reports the
# same thing on the execute side: "projection": {"fields": [...], "missing": [paths that hit
# nothing]}, plus "matched_nothing": true when none of them matched. That last key is written
# only when true, so test it with .get() rather than subscripting it. A path that is right but
# crosses an empty list is a match, not a miss: it returns the empty list and is listed in
# "projection": {"empty": [...]} (and "path_empty": true on this endpoint).
# A path may continue into a string that carries JSON — that step is taken for you. Since
# 2026-09-10 the marker "<json>" is also accepted and skipped as an interior step, so a path
# read off the response's own "redaction" report (which spells it
# "content[0].text.<json>.deployment.phase") can be pasted here verbatim.
#
# Anchor the path on what "result" actually holds, which differs by service type. For an `api`
# service "result" is the upstream body, so the paths look like the example above (a body that
# is not JSON arrives as a raw string instead, and then "fields" is skipped altogether — no
# projection runs and "projection" comes back null, which means "never attempted" rather than
# the "matched_nothing" verdict it resembles). For an `mcp_server` service "result"
# is the upstream MCP server's own envelope, so start at "content[0].text...." or
# "structuredContent....". Since 2026-09-27 the projection also covers "structuredContent":
# a path matching the text block's document is applied to the structured copy too (and that
# copy is dropped when none of the paths match it), and when the text block is prose a bare
# document path is resolved against "structuredContent" instead of missing — live,
# fields=["results[].title"] on Cloudflare Documentation.search_cloudflare_documentation
# reported "missing": [] and returned the eight titles there, with the prose text block
# returned whole. That last fallback is all-or-nothing: it is tried only when NONE of your
# paths matched the envelope, so don't mix the two kinds in one call —
# fields=["content[0].type", "results[].title"] on that same tool kept the content block,
# reported "missing": ["results[].title"] and dropped "structuredContent" altogether.
# Danube itself adds no "data" key over REST on either path — that key belongs to the MCP
# server, which adds it for its own callers after the projection has already run, so the key
# itself is not addressable. A "data" you do see is the upstream's own, and that one matches
# normally (a GraphQL body carries one whenever execution began — Linear - Graphql Query and
# Shopify - Run Graphql Query are both `api` services).
# BUT since 2026-10-24 writing "data." in front of a path no longer costs you the values: each
# path is matched as written, and one that matched NOTHING is retried with a leading "data" or
# "result" segment peeled off -- repeatedly, so "result.data.x" loses both -- so the spelling you
# read the value at over MCP works here too.
# "projection": {"envelope_prefix_stripped": true} says a path only matched after that peel.
# Two guards: a path that matched as written is never reinterpreted (an upstream's own "data"
# still wins), and a prefix that is a real key of the value is never peeled, so "data.x" over
# {"data": {"y": 1}, "x": 2} genuinely misses instead of being answered with the sibling "x".
# A wrong path is still reported under YOUR spelling, not the peeled one. Probed live
# 2026-10-25 on the api tool ClawHub - Get Skill:
#   -d '{"tool_input": {"slug": "danube", "owner": "preston-thiele"},
#        "fields": ["data.latestVersion.version"]}'
#   → "result": {"latestVersion": {"version": "8.1.43"}},
#     "projection": {"fields": [...], "missing": [], "envelope_prefix_stripped": true}
# And on Cloudflare Documentation.migrate_pages_to_workers_guide (an mcp_server service), where
# one path peels to something real and the other peels to "anything" and still misses:
#   -d '{"tool_input": {}, "fields": ["data.content[0].type", "data.anything"]}'
#   → "result": {"content": [{"type": "text"}]},
#     "projection": {"fields": [...], "missing": ["data.anything"],
#                    "envelope_prefix_stripped": true}

# A destructive call answers with HTTP 409 and error.code "confirmation_required" (see the
# table below) when the key carries require_confirmation, OR when the tool asks for consent from
# every caller regardless of the key (tools.metadata.require_confirmation -- every write tool of
# an infrastructure connector -- or a connected system whose access policy sets writes:
# "consent" -- its HTTP surface only, not a connected database's Query tool). error.details.reason
# is "api_key" or "service_policy"; the key-side trigger wins that label whenever it applies, so
# "service_policy" is the informative value -- it means the key does NOT have the setting on.
# Show the user the tool and the parameters, get an explicit yes, then repeat the same call with
# the token (valid 5 minutes).
curl -s -X POST "$BASE/tools/call/<TOOL_ID>" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"tool_input": {"to": "someone@example.com", "subject": "Hello", "body": "Hi there"}, "confirm_token": "<error.details.confirm_token>"}'

# Up to 10 independent calls in one request. Each entry succeeds or fails on its own.
# An entry takes "fields" of its own, same meaning as on the single call above — honoured since
# 2026-09-10; before that it was accepted and silently dropped. ("max_response_chars" per entry
# is older than that and was always honoured.) An entry also takes its own "confirm_token": the
# consent gate runs per call, with both of its triggers -- a key carrying require_confirmation, or
# a tool that asks every caller regardless -- so a refused entry comes
# back as an element with "success": false and a "confirmation_required" block of its own while
# the batch still answers 200 — see "Consent inside a batch" below.
curl -s -X POST "$BASE/tools/call/batch" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"calls": [
        {"tool_id": "<TOOL_ID_1>", "tool_input": {"q": "weather in Oslo"}},
        {"tool_id": "<TOOL_ID_2>", "tool_input": {"text": "hello", "target_lang": "DE"},
         "fields": ["translations[].text"]}
      ]}'
# → {"results": [{"tool_id": "...", "success": true, "result": {...}, "error": null}, ...]}
# Over REST an element's "result" is the whole engine envelope, so the handle and the
# projection report are at results[i].result.execution_id and results[i].result.projection.
# Mind the order, which is the opposite of the MCP server's: an entry's "max_response_chars"
# (default 500000 here, or the tool's own cap when it declares one — there is no 32000 batch default over REST) trims the result BEFORE it
# is projected and before it is stored, so fetching that handle back does NOT recover a trimmed
# element. Narrow the request instead. (Over MCP the two keys are lifted onto the element's
# _meta, and its 32000 cap is applied after storing, so there the handle does recover it.)
```

### Consent inside a batch

The consent gate runs per call, not per request, and a batch never fails as a
whole because of it. Both of its triggers reach a batch entry — the key's `require_confirmation`,
and a tool that asks every caller regardless (see the `409` row in the error table). An entry it refuses comes back as its own element:

```json
{"tool_id": "...", "success": false, "result": null,
 "error": "'Gmail - Send Email' can change or send data. Show the user the tool and parameters below, get an explicit yes, then call again with confirm_token.",
 "confirmation_required": {"confirm_token": "...", "expires_in": 300,
                           "tool_id": "...", "tool_name": "...", "method": "COMPOSITE",
                           "reason": "api_key",
                           "parameters": {"to": "...", "subject": "..."}}}
```

Show the user that element's `tool_name` and `parameters`, get an explicit yes, then re-send
**that entry** with `"confirm_token"` beside its `"tool_input"`. The other entries already ran —
don't replay them. The token is bound to the key, the tool and a hash of the parameters, so
editing a parameter after the user approved invalidates it.

**Over MCP this handshake cannot be completed inside a batch at all.** `batch_execute_tools`
forwards only `tool_id`, `tool_input` and `fields`, so a `confirm_token` on a call is dropped
before the request ever leaves, and each element is rebuilt from a fixed set of keys that does
not include `confirmation_required`, so the token never reaches you either. There you get the
message alone: take that one call out of the batch and run it through `execute_tool`, which does
take `confirm_token`.

Note also what the gate does *not* cover, on either transport. It reads the publisher's
`metadata.destructive` **first and takes it as final**; only a tool row without that key falls
through to the method test, which counts anything but GET/HEAD/OPTIONS destructive. That `method`
is Danube's own routing value, so it is an HTTP verb for a plain API tool, `COMPOSITE` for one of
the provider-specific handlers (both destructive by method), and `MCP` for anything served by an
MCP server — and `MCP` says nothing about what the tool does, so those are let through unmarked.
Because the flag is read first, it works both ways: it can mark one of those MCP tools, and
`destructive: false` can clear *any* row the method would have caught, a `DELETE` or a
`COMPOSITE` as readily as the POST-based read the opt-out was meant for. A call that goes through
without a handshake has not been judged safe.

### Reading results

Every error body carries `error_type`, `fault` and `retryable` at the top level (the same three
the MCP layer puts in `_meta`). `fault` is `caller` (your parameters or credentials — fix them),
`upstream` (the third party failed — retrying later may work, and this is the only class that
moves the tool's reliability score) or `danube` (a stale catalog row or a request Danube built
wrong — neither a retry nor a `report_tool` helps). Read those before matching any message
text below. They are absent when the call never reached the execution engine (an unresolvable
tool id) or when the refusal is returned as a real HTTP status instead, such as the `402` and
`503` rows below. Nothing is prefixed onto the error text over REST — the labelled
"Request error:" / "Danube error:" wording is added by the MCP layer only.

| You see | It means | Do |
|---|---|---|
| `{"status": "success", "result": {...}}` (or the raw provider payload) | Worked | Report the specifics to the user |
| `{"status": "error", "error_type": "auth_required", "configuration_url": "..."}` | This user hasn't connected the service yet | Send the user to `configuration_url` (or https://danubeai.com/dashboard). For API-key services, if the user hands you a key and confirms, store it (see below) and retry |
| HTTP `401` | `DANUBE_API_KEY` is missing, wrong, or revoked | Ask the user to check the API Keys page (https://danubeai.com/dashboard/api-keys) |
| HTTP `403` | `This API key does not have permission to access this resource`: the key is restricted (`allowed_services` / `allowed_tools`). `Your organization does not have access to this tool`: the organization's policy, which an admin changes with a grant to the user, a team they are in, or their role (a tool the policy withholds is normally hidden from search, so this mostly comes from an id you were already holding) | Tell the user which tool was blocked and, for the second text, that an organization admin has to grant it; don't retry and don't `report_tool` it |
| `{"status": "error", "error_type": "permission_denied", "fault": "caller"}` on a `<Service> - Request`, `- Query`, `- List tables` or `- Describe table` tool | The connected system's access policy refused the method, path or table; the message names it | Tell the user what was refused and that an org admin widens the policy on the service page (or promotes the call as a named tool). Don't retry the same call, don't route around it, don't `report_tool` it. A write may come back as `confirmation_required` instead when the policy asks for consent: confirm it like any other |
| HTTP `404` | Tool ID no longer exists | Search again — never reuse IDs from memory |
| `{"status": "error", "error_type": "tool_sunset", "fault": "danube", "error": "'<tool>' was deprecated and passed its sunset date (YYYY-MM-DD): <deprecation message>. No call was made."}` (the value was the upper-case `TOOL_SUNSET` before 2026-09-10) | The tool was deprecated and its sunset date has passed. Nothing was called | Read the quoted deprecation message for the replacement and search again. The tool is also gone from search results by now, so this only reaches you from an id you were already holding |
| `{"status": "error", "error_type": "upstream_tool_missing", "retryable": false, "upstream_tool": "…", "available_tools": [...]}` (HTTP `200`, like any other body-shaped error) | The catalog row points at a tool its MCP server no longer offers — Danube's own drift, not your call. It first tries to repair silently (re-reading the server's tool list and re-running the call under the new name if the tool was just renamed), so what you're seeing is a tool that is genuinely gone | Don't retry — the message says so outright — and don't `report_tool` it: the failure files its own report automatically. Pick a replacement from `available_tools`, or search again |
| HTTP `409` with `error.code: "confirmation_required"` | A destructive call needs a `confirm_token`, because the API key has `require_confirmation` set **or** because the tool asks every caller for one whatever the key says (`tools.metadata.require_confirmation` — every write tool of an infrastructure connector — or a write on a connected system whose access policy sets `writes: "consent"`). `error.details` carries the token (`expires_in` 300 s), `tool_id`, `tool_name`, `method`, `reason` (`"api_key"` or `"service_policy"`; the key-side trigger takes the label whenever it applies, so `"service_policy"` is the one that tells you something — the key does not have the setting on) and the parameters — passed through the redactor for display, so a credential-shaped value reads `[REDACTED:…]` | Show the user that tool and those parameters, get an explicit yes, then repeat the call with `"confirm_token"` beside your **original** `"tool_input"`: the token is signed over what you sent, so re-sending a masked value breaks it. Never reuse a token without asking; don't retry the 409 blindly. Inside a batch this arrives per element instead of as a status — see "Consent inside a batch" above |
| HTTP `429` with `upgrade_url` | The account's monthly call cap: 5,000 successful calls per UTC calendar month on free, 50,000 pro, 250,000 team, uncapped enterprise (legacy `starter` 10,000). `error.details.usage` carries `tier`, `limit`, `current_usage` and `remaining` | Tell the user which figure they hit; don't loop. `upgrade_url` is the relative `/pricing` here too. A call past the cap is not always refused — see the plan-cap row in `troubleshooting.md` for the pay-as-you-go path and what it charges |
| HTTP `429` whose `error.details` holds `retry_after`, body `{"error": {"code": "rate_limited", "message": "Too many requests. Please wait N seconds before trying again.", "details": {"retry_after": N}}}` — note `error.code` is `rate_limited` on the plan cap above too, so **`error.details` is the only discriminator in the body** (`usage`/`upgrade_url` = plan cap, `retry_after` = limiter; the limiter's response also carries `Retry-After` and `X-RateLimit-Limit` headers, which the plan cap has not) | Danube's rate limiter. `/tools/search`, `/tools/call/{id}` and `/tools/call/batch` are limited by API key at the plan's rate — 60/minute free, 1000 pro, 2000 team, 3000 enterprise (legacy `starter` 300). All three require a key, so a keyless call is `401`, not a slower anonymous lane. The count is per key **and per URL path**: each path has its own bucket and the tool id is in the path, so 60/minute free means 60 per tool. The tier behind a key is cached five minutes, so an upgrade widens it within that | Read `error.details.retry_after` or the `Retry-After` header, sleep it, retry once — but don't treat it as a reset time: it is a flat 60 today. `X-RateLimit-Limit` is a description string (`"60 per 1 minute"`), not an integer. `POST /tools/call/batch` is **one** request against the rate limit however many entries it carries — useful when looping over a single tool — but each entry is still counted against the plan quota separately, so batching does not stretch the plan allowance |
| HTTP `402`, `error.code` `payment_required`, `error.message` "Daily limit for Danube's AI tools reached (N/20 today on the free plan). It resets at 00:00 UTC…", with `usage` and `upgrade_url` under `error.details` (`upgrade_url` is the *relative* `/pricing` — join it to `https://danubeai.com` before showing it) | A free-tier account has spent its 20 successful executions of Danube's own AI tools for this UTC day (the five tools in the gate's frozen name set — `Danube - Summarize Text`, `- Extract Entities`, `- Classify Text`, `- Generate Structured Data`, `- Translate Text`; the four web-intelligence `Danube - …` names and `Danube - Screenshot` are all exempt, and all five of those are registered pointing at handler functions that do not exist, so they are not executable either). Workflow steps count against the same 20. Paid tiers are uncapped here. Distinct from the workflow `402` further down, which is a lifetime cap and never resets | Wait for 00:00 UTC or tell the user to upgrade; don't loop and don't report the tool. Note `POST /tools/call/batch` does **not** map this to a status code — the element comes back `success: false` with the message in `error` and the envelope, including `error_type: "upgrade_required"`, under `result` |
| HTTP `503`, message "Danube's hosted AI tools are temporarily disabled. Other tools are unaffected." | Danube's kill switch for those same five tools is off — deliberate and account-independent | Don't retry in a loop; the rest of the catalogue is unaffected |
| `{"status": "error", "error_type": "insufficient_balance", "error": "Insufficient credits. This tool costs $X.XX. Your balance: $Y.YY. Add credits at https://danubeai.com/dashboard/finances", "cost_cents": N, "balance_cents": M}` (HTTP `200`, a body-shaped error like the rows above) | A publisher-priced tool, refused *before* the upstream call — nothing ran and nothing was charged, so `balance_cents` is the balance that was too low, not one left after a charge. `fault` is `caller` and `retryable` is `false` | Show the user `cost_cents` and `balance_cents` and the link (`/dashboard/wallet` redirects to `/dashboard/finances?tab=wallet`). Don't retry — the balance can't have changed — and don't `report_tool` it. A tool priced in USDC refuses on a limit rather than an empty wallet: "x402 spending limit exceeded: Exceeds your per-call limit of $X" carries no `error_type` of its own and is classified from that text, while a USDC balance short of the recorded price simply falls back to the ordinary credits wallet and goes ahead. Some x402 tools have their price re-derived at call time from the upstream's own `PAYMENT-REQUIRED` header and re-check both gates against it, and nothing you can read says which — a search result gives you `x402_enabled` and the price, but not the pricing mode, and `describe` gives you no pricing field at all, so match the message rather than the tool. Those answer "Insufficient USDC. Required: $X.XXXX. Balance: $Y.YYYY" (classified correctly) or "x402 payment blocked: …" with the same three limit reasons, which matches no text rule and is mis-filed as `unknown` / `fault: "danube"` — read that one's message, not its verdict, and leave it unreported; the platform files its own row |
| A value in the payload reads `[REDACTED:FIELD]` | Danube masks credential-looking values out of tool responses before returning, logging or storing them — every tool but one declared as returning a credential (next row). Applies over REST exactly as it does over MCP | Policy, not breakage. Don't ask the tool to return the raw secret; store the credential instead. The response's `redaction` object carries `count`, `fields[]` and `mode` — note the key is **always present over REST**, set to `null` when nothing was masked, so test the value rather than the key |
| `"redaction": {"passthrough_reason": "…"}` with a real secret in the payload | A credential-returning tool Danube couldn't capture (no capture mapping, self-hosted custody, or a failed store). Its value is deliberately unredacted, durable secrets included | Treat it as a live secret: hand it to the user, don't log it or echo it into a later request |
| A failed call whose `error` contains "… was not sent — `<tool>` does not declare that parameter, so Danube dropped it before making the request. If the upstream supports it, the tool's schema is missing it." (plural: `were` / `those parameters` / `them`) | You sent a parameter the tool row doesn't declare, so Danube dropped it before calling the upstream — that value never left Danube | Don't chase it upstream. Since 2026-10-24 the same names also ride the envelope as the top-level `dropped_unknown_params` (beside `defaults_applied`), so you can branch on it instead of parsing the prose — and that field is set on a **successful** call too, which is the case to actually worry about: a filter under a wrong name widens the result instead of failing anything, so read it on every call whose narrowing you rely on. Re-read the tool's `parameters` from `GET /tools/{id}/describe`; if the provider really supports the parameter, the tool's schema is missing it. Over REST this field is **always present** and `null` when there is nothing to report, so test the value rather than the key (over MCP it is absent instead). It is only informative on an `api` tool: MCP-backed tools forward parameters unfiltered, and a `COMPOSITE` tool computes no list at all, so a `null` there means "not computed", not "nothing dropped" |

## Credentials the user gives you

Only after the user explicitly provides a key in the conversation and confirms
they want it stored:

```bash
curl -s -X POST "$BASE/credentials/store" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"service_id": "<SERVICE_ID>", "credential_type": "bearer", "credential_value": "<KEY THE USER GAVE YOU>"}'
# credential_type: "bearer" or "api_key" — the tool's schema / auth_required error says which
# → {"success": true, "service_id": "...", "service_name": "...",
#    "credential_type": "bearer", "stored_as": "value",
#    "deprecated": true, "notice": "Storing plaintext credential values ... is deprecated ..."}
```

### References instead of raw secrets — where they work

A `credential_value` matching `^(env|vault)://` is stored as a **reference**:
a pointer resolved when the tool runs, rather than the secret itself.

Resolution is **not** wired into every execution path. It happens on the
standard HTTP auth-injection path — an `api` service whose tool isn't one of
the provider-specific composite handlers — and in the in-VPC data-plane agent,
which runs the services an org has marked `local_only`. A **hosted**
`mcp_server` service, and the composite handlers (Firecrawl, Notion, and
friends), read the stored string **as the secret** — so a `vault://…` string is
sent as the credential and the provider answers `401`, not a resolution error.
Store a reference only for a self-hosted deployment or a service that runs on
the data-plane agent; otherwise store the value. When in doubt, store the value.

On the data-plane path, though, a reference is the **only** thing that works: the
control plane strips every non-reference value out of the dispatch (a plaintext
secret becomes `null` with its existence flagged, so it never leaves Danube) and
the agent answers `error_type: credential_reference_unresolved`, `fault: caller`,
"… exists only as a central plaintext value. Data-plane execution requires
reference-based credentials (env:// or vault://); re-store it as a reference."
Since 2026-09-24 that includes a `local_only` **MCP** service, whose calls and
tool discovery both go through the agent — so for a `local_only` row of any kind,
ask the user which form they hold rather than defaulting to the value.

```bash
# HashiCorp Vault KV v2. The #<field> suffix is required — vault://path/to/secret
# without it is rejected at resolve time, whatever the API's deprecation notice says.
# Read with the VAULT_ADDR / VAULT_TOKEN of the process that runs the tool: your
# data-plane agent or self-hosted deployment. The hosted service has no per-customer
# Vault setting, so it cannot reach your Vault.
curl -s -X POST "$BASE/credentials/store" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"service_id": "<SERVICE_ID>", "credential_type": "bearer", "credential_value": "vault://secret/acme/api#token"}'

# Environment variable: resolved in the environment where the tool actually runs, so this
# is for self-hosted / data-plane deployments only. The hosted service accepts the store
# and then fails at execution time — env:// is off by design there (DANUBE_ALLOW_ENV_REFERENCES
# is a self-hosted/dev switch, not something Danube enables for hosted accounts).
curl -s -X POST "$BASE/credentials/store" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"service_id": "<SERVICE_ID>", "credential_type": "bearer", "credential_value": "env://ACME_API_KEY"}'
```

The response echoes `"stored_as": "reference"` and carries no `deprecated`
flag — but a successful store says nothing about whether the reference will
resolve; that only surfaces when the tool runs. A plaintext value is still
accepted on the hosted service (deprecated); self-hosted deployments reject it
with HTTP `400`. Every API error goes through one envelope, so the token you
match on is at `error.details.error`, not at the top level:

```json
{"error": {"code": "validation_error",
           "message": "{'error': 'central_credential_ingestion_disabled', 'hint': '...'}",
           "details": {"error": "central_credential_ingestion_disabled",
                       "hint": "store a reference (env:// or vault://) or configure the data-plane secret resolver"}}}
```

(`message` is a Python `repr` of the same dict, single-quoted — read
`error.details`, not `error.message`.) The MCP `store_credential` tool reports
the same condition differently: HTTP `200` with `{"success": false, "error":
"central_credential_ingestion_disabled"}`, when the MCP server runs in the same
deployment mode as the backend. Never invent a variable name or vault path: use
only what the user gave you.

Stored credentials are encrypted at rest, scoped to the user, and never
returned by any endpoint. OAuth services (Gmail, Slack, Google Calendar, …)
can only be connected by the user in the dashboard.

## Connect a system for an organization

```bash
# Owner or admin of the org only. One input per system: kind api (api.base_url, optional
# api.auth and api.openapi_url), database (database.db_type, database.connection_ref as
# env://NAME or vault://mount/path#field, never the connection string) or mcp (mcp.server_url).
# visibility: internal (default; Danube runs the calls), local_only (the org's in-network
# data-plane agent runs them; a database is always local_only on the hosted service).
# dry_run: true discovers and previews, writes nothing:
curl -s -X POST "$BASE/organizations/<ORG_ID>/connect" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"kind": "api", "name": "Billing", "visibility": "internal",
       "api": {"base_url": "https://billing.example.com", "auth": {"type": "api_key", "name": "X-API-Key"}},
       "dry_run": true}'
# → {"service": {"id": null, ...}, "tools": [{"id", "name", "generic", "method", "path"}],
#    "discovered": {"kind", "openapi", "openapi_url", "endpoint_count", "tables": [...], "error"?},
#    "policy": {"http": {...}, "sql": {...}}, "sync": "done" | "running"}
# The agent gets these tools at once: for an API every operation of a discovered OpenAPI
# document plus "<Service> - Request" (generic: "request"; parameters method, path, query,
# body, headers); for a database "<Service> - Query" (sql), "- List tables" (schema?) and
# "- Describe table" (table). They obey the service's policy: GET/HEAD on every path and no
# table allowed until an admin lists some. A refused method, path or table answers
# error_type permission_denied, fault caller: that is the policy, not a bug; tell the user.
# discovered.error = no_dataplane_agent means the database's schema was not read (no agent
# online); an admin runs discovery again with:
curl -s -X POST "$BASE/organizations/<ORG_ID>/connect/<SERVICE_ID>/discover" -H "$AUTH"
# The policy (owner/admin; PUT replaces the whole object):
curl -s "$BASE/organizations/<ORG_ID>/services/<SERVICE_ID>/policy" -H "$AUTH"
# → {"service_id", "org_id", "policy": {"http": {"allowed_methods", "allowed_path_prefixes",
#    "denied_path_prefixes", "writes": "off" | "consent" | "allowed"}, "sql": {"allowed_tables",
#    "denied_tables", "masked_columns", "max_rows"}}, "configured": bool}
# Promote a call an agent made on a generic tool into a named tool (owner/admin), from the
# execution_id of the tool_executions row, or with the call given explicitly:
curl -s -X POST "$BASE/organizations/<ORG_ID>/services/<SERVICE_ID>/promote" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Get invoice", "execution_id": "<EXECUTION_ID>"}'
curl -s -X POST "$BASE/organizations/<ORG_ID>/services/<SERVICE_ID>/promote" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Customers by region",
       "sql": {"sql": "SELECT id, name FROM customers WHERE region = :region LIMIT 50",
               "parameters": [{"name": "region", "type": "string"}]}}'
# → the named tool. 400 = nothing to promote, a residency-mode row (pass request or sql), a
# write statement; 404 = the execution belongs to another service.
# Guide: https://docs.danubeai.com/organizations/internal-tools
```

## Register from an OpenAPI document or a connector spec (advanced)

```bash
# Owner or admin of the org only. source: openapi_url | openapi_spec | mcp | connector | database.
# visibility: internal (default; Danube runs the calls, every member can see the tools),
# local_only (the org's in-network data-plane agent runs them — since 2026-09-24 that covers a
# REMOTE MCP server and a database as well as HTTP), private (the caller alone).
# On the hosted service a database MUST be local_only, because the query runs where the DSN
# lives; internal or private is refused at registration with a 400 (see below).
# dry_run: true parses and previews, writes nothing:
curl -s -X POST "$BASE/organizations/<ORG_ID>/services" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"source": "openapi_url", "openapi_url": "https://billing.example.com/openapi.json",
       "name": "Billing", "visibility": "internal", "dry_run": true}'
# → {"service": {...}, "tools": [{"name", "method", "path", "action": "create" | "update"}],
#    "errors": [...], "would_exceed_caps": false, "sync": "done"}
# Read errors, show the user the tool list, get a yes, then repeat without dry_run:
# → {"service": {...}, "tool_count": N, "tools_failed": [...], "sync": "done" | "running", "warnings": [...]}
# 400 carries the reason: no servers entry, no tools, over half the tools failed; a LOCAL (stdio)
# MCP server — "Only remote MCP servers can be registered for an organization", whatever
# visibility was asked for; a local_only MCP server_url that is not http(s) with a host; or a
# database asked to be anything but local_only — "Database connectors run only through an
# organization's data-plane agent on the hosted service; register the connector for the
# organization with visibility local_only".
# 409 = a service you cannot manage already has that name; 413 = the
# document is over 5,000,000 bytes. The org's own services: GET $BASE/organizations/<ORG_ID>/services
# Guide: https://docs.danubeai.com/organizations/internal-tools
```

## Rate and report a tool

```bash
# THIS key's own rating for one tool (nobody else's), and the public aggregate.
curl -s "$BASE/ratings/my/<TOOL_ID>" -H "$AUTH"
curl -s "$BASE/ratings/tool/<TOOL_ID>" -H "$AUTH"   # public, but send the key (see below)

# Rate a tool. Upserts on (you, tool), so calling it again edits your rating.
# tool_id must be the UUID. A string that isn't one is a 400; a well-formed UUID
# that names no tool is a 404 ("No tool with id ...") — since 2026-09-24, where
# the same input used to come back as a 500. A 404 here means the id is stale or
# mistyped: re-resolve it with /tools/search rather than retrying. Since
# 2026-09-27 that same 404 and message also answer a tool hidden from you (one on
# a service you cannot see); /tools/search hides it too, so if the re-resolve
# cannot find it, stop instead of looping.
curl -s -X POST "$BASE/ratings" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"tool_id": "<TOOL_ID>", "rating": 5, "comment": "worked first try"}'

# Report one that is broken or wrong. reason: broken | degraded |
# incorrect_output | timeout | other — anything else is a 400. This one takes
# no key (a report can be filed anonymously), but send it anyway: it is what
# attributes the report to you, and since 2026-09-27 a tool hidden from the
# caller answers 404 here, so an anonymous call sees only public tools.
curl -s -X POST "$BASE/tools/<TOOL_ID>/report" -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"reason": "incorrect_output", "description": "returns yesterdays prices"}'
```

Two of these four insist on a real tool **UUID**, not the slug you would use to
execute or describe it: `POST /ratings` and `GET /ratings/my/{id}` answer `400`
`{"error": {"code": "validation_error", "message": "tool_id must be a tool UUID,
got: 'gmail-send-email'"}}` on anything else. `POST /tools/{id}/report` is the
exception — it resolves a slug or a UUID and stores the resolved UUID — but the
matching MCP tool refuses a slug outright, so sending the UUID is what works
everywhere.

`GET /ratings/tool/{id}` is the fourth, and it never errors on the id: a bad one
is swallowed and answered `{"avg_rating": null, "rating_count": 0}`, exactly
what an unrated tool returns. Since 2026-09-27 a tool you are not allowed to see
answers that same empty body, and the check is against the caller — so send
`$AUTH` on this one even though the route is public, or your own organization's
internal tools read as unrated. Note the key names — `avg_rating` and
`rating_count` — and note that a zero there is not a verdict: the aggregate
counts only ratings whose `source` is `user` (agent-dogfooding ratings are left
out) and it is a materialized view on a five-minute refresh schedule, so a
rating submitted moments ago is not in it yet. Live on 2026-09-22, the calling
key's own rating of `6f0c4361-d0cc-45df-8ee6-87b9cc1e0d37` came back as five
stars on `/ratings/my/…` while `/ratings/tool/…` answered `rating_count: 0` for
the same tool. The `reliability` block on a search result is the number to rank
on.

Both writes take a `source` field. Leave it out: it exists to mark Danube's own
internal dogfooding traffic, and setting it tells the team to discount what you
reported. Filing the same tool + reason again while an earlier report is still
open or acknowledged bumps that report's occurrence count rather than creating a
duplicate, so there is no need to check for one first — the match being on the same
tool, reason and `source`, which is one more reason to leave `source` alone. The bump
keeps your text, folding it into the row it collapsed into, and the response *is* that
row, so an `occurrence_count` above `1` is how you tell a dedupe from an insert; a
report filed once an earlier one has been resolved or dismissed starts a fresh row
instead. See `troubleshooting.md` for the three cases where only the count moves.

## Skills and workflows

```bash
# Search covers public skills plus, with your key, your organizations' internal skills and your
# own private ones (those first; `visibility` and `org_name` say which).
curl -s -G "$BASE/skills/search" -H "$AUTH" --data-urlencode "query=summarize a webpage" --data-urlencode "limit=5"
curl -s "$BASE/skills/<SKILL_ID>" -H "$AUTH"                     # id or name
curl -s "$BASE/skills/<SKILL_ID>/download" -H "$AUTH" -o skill.zip   # zip ready for .claude/skills/
curl -s "$BASE/organizations/<ORG_ID>/skills" -H "$AUTH"           # an organization's internal skills

# Share a skill folder with the organization (a write: confirm first). The zip holds one folder in
# the Agent Skills layout (SKILL.md with name and description frontmatter, scripts/, references/,
# assets/). visibility is internal or private; replace=true publishes a new version of the skill
# that already holds the name (409 without it). An organization may limit publishing to admins.
curl -s -X POST "$BASE/skills/upload" -H "$AUTH" \
  -F "file=@my-skill.zip" -F "visibility=internal" -F "org_id=<ORG_ID>" -F "replace=false"

# Create a workflow (a write: confirm first). Two modes, and "template" is the default.
# Anything other than the exact string "instructions" is treated AS template mode -- there is no
# CHECK on the column -- so a misspelling fails with the template error below, not a mode error.
# Template mode: numbered steps, each naming a step_number and a tool_id, wired with
# {{inputs.x}} and {{steps.N.result.field}}. At least one step, or 400.
curl -s -X POST "$BASE/workflows" -H "$AUTH" -H "Content-Type: application/json" -d '{
  "name": "Summarize a page",
  "steps": [{"step_number": 1, "tool_id": "<TOOL_UUID>", "input_mapping": {"url": "{{inputs.url}}"}}]
}'
# Instructions mode: prose instructions plus the tools the orchestrator may call. Both are
# required -- an empty "instructions" or an empty "allowed_tool_ids" is a 400 ("Instructions are
# required for instruction-based workflows" / "At least one allowed tool is required"), and a
# tool you cannot see is "Tool not found: <id>". "input_schema" is optional and only describes
# the inputs to the orchestrator. Over REST the response echoes "instructions" back in full; it
# is the MCP create_workflow/update_workflow that replaces it with an "instructions_chars" count.
curl -s -X POST "$BASE/workflows" -H "$AUTH" -H "Content-Type: application/json" -d '{
  "name": "Research a company",
  "execution_mode": "instructions",
  "instructions": "Look up the company, then summarize what it sells and who it sells to.",
  "allowed_tool_ids": ["<TOOL_UUID>", "<TOOL_UUID>"],
  "input_schema": [{"name": "company", "description": "Company name or domain"}]
}'

# Give a workflow a schedule (a write, and one that keeps acting after the conversation: confirm,
# and say so). Either mode takes it, on POST /workflows or PATCH /workflows/<ID>. 5-field cron in
# an IANA timezone (default "UTC"); nothing fires until schedule_enabled is true, and enabling it
# with no cron is a 400 ("schedule_enabled requires schedule_cron"). Validated on the way in: five
# fields, a known timezone, and no faster than every 5 minutes ("Schedule may not fire more often
# than every 5 minutes"). next_run_at comes back with the row, null unless both cron and enable are
# set. Only the AUTHOR may set the cron, the timezone or the enable flag, and the refusal depends
# on how far in you are: a workflow you cannot read is a 404 ("Workflow not found"), one you can
# read but not manage is a 403 ("Only its author or an organization admin can change this
# workflow"), and only a non-author who MAY otherwise manage it (an org owner/admin, a platform
# admin) reaches the schedule 403 ("Only the workflow's author can schedule it; runs use their
# credentials"). schedule_inputs is NOT behind that gate, so such a manager can change what every
# run is called with, on the author's credentials, with no 403 and no next_run_at recompute.
# Each run executes as the author, with the
# author's credentials, with no API key allowlist applied: a key scoped by allowed_services /
# allowed_tools does not narrow the runs it schedules. A backlog after downtime collapses into one
# catch-up run, not a burst.
curl -s -X PATCH "$BASE/workflows/<WORKFLOW_ID>" -H "$AUTH" -H "Content-Type: application/json" -d '{
  "schedule_cron": "0 9 * * *",
  "schedule_timezone": "America/Chicago",
  "schedule_enabled": true,
  "schedule_inputs": {"url": "https://example.com"}
}'

curl -s "$BASE/workflows/public" -H "$AUTH"
# The full row. schedule_timezone, schedule_inputs and last_scheduled_run_at ride only on this and
# on the create/update response: the /my listing below (and /workflows/public, /workflows/org/...)
# carries just schedule_cron, schedule_enabled and next_run_at of the six (both shapes verified
# live 2026-10-12). No MCP tool reads a workflow back, so over MCP those three are visible only in
# the answer to your own write -- and the get_workflow tool the MCP server's own create/update
# response points you at does not exist.
curl -s "$BASE/workflows/<WORKFLOW_ID>" -H "$AUTH"
curl -s "$BASE/workflows/my" -H "$AUTH"                       # yours, private included
curl -s "$BASE/workflows/my?include_org=true" -H "$AUTH"      # plus ones shared with your orgs

# Move a private workflow into an organization, or back out (a write: confirm first). Same id and
# link; members see and run it with their own credentials or the org's shared ones, and its author
# keeps editing it. Only the AUTHOR may share or unshare — an org admin gets 403. Do NOT PATCH
# visibility into or out of internal: that is refused with a 400 naming these routes. The same
# pair exists for skills ($BASE/skills/<SKILL_ID>/share and /unshare).
# share-check first: it reports per step whether members can see that tool and whose credential
# the step would run with. /share refuses with a 400 naming tools members cannot use.
curl -s "$BASE/workflows/<WORKFLOW_ID>/share-check?org_id=<ORG_ID>" -H "$AUTH"
curl -s -X POST "$BASE/workflows/<WORKFLOW_ID>/share" \
  -H "$AUTH" -H "Content-Type: application/json" -d '{"org_id": "<ORG_ID>"}'
curl -s -X POST "$BASE/workflows/<WORKFLOW_ID>/unshare" -H "$AUTH"

# Run one (same confirmation rule as any other write), then poll its execution.
# Name the execution yourself with a UUID you generate: a run can outlive the HTTP
# request that started it, and if you didn't supply an id up front a timeout leaves
# you with no way to address the run that is still in flight. (The MCP
# execute_workflow tool does this for you; over curl it's on you.)
# Use a FRESH UUID each run: an unparseable one is a 400, and so is reusing one that
# already names an execution.
EXEC_ID=$(uuidgen | tr 'A-Z' 'a-z')   # or python3 -c 'import uuid;print(uuid.uuid4())'
curl -s -X POST "$BASE/workflows/<WORKFLOW_ID>/execute" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"inputs\": {\"url\": \"https://example.com\"}, \"execution_id\": \"$EXEC_ID\"}"
curl -s "$BASE/workflows/executions/$EXEC_ID" -H "$AUTH"
```

**A non-2xx is not how a workflow reports failure.** A run whose *steps* failed comes back
`200` with `status: "failed"` in the body and the failure recorded per step. Read the
body's `status`. The cases below are the ones specific to executing a workflow; the usual
`401` (bad key) and `422` (malformed body) apply here as everywhere else.

| Status | Means | Do |
|---|---|---|
| `200`, body `status: "failed"` | The run started and one or more steps failed | Read the per-step results — this is where step errors live, not in an HTTP code |
| `404` | No such workflow, or it's private and not yours. A malformed workflow id lands here too, not on a `400` | Search or list workflows again — don't retry the id |
| `402` | Free-tier account, all 5 lifetime *successful* runs using a Danube-hosted AI step are spent. Refused before any step ran, so nothing is half-done and no execution row exists | Tell the user to upgrade; **this** cap never resets, unlike the daily hosted-AI cap on `/tools/call` above. Match on the `402` and on `error.message` ("You've used all 5 free AI-powered workflow runs…"); `error.code` is `payment_required`, which is what a plan refusal should read as — don't take it for an outage |
| `200`, body `status: "failed"`, `error` starting "AI orchestration is rate limited upstream right now." | Instructions mode only: the model provider throttled Danube. Danube tried up to three times with backoff first, and gives up sooner when the wait asked for would exceed a 45-second budget shared across the whole run | Retry the run, but not immediately. Not a `report_tool` case — it is upstream of Danube, and the quoted `Upstream said:` detail is stripped of the provider's organization id and capped at 300 chars |
| `200`, body `status: "failed"`, `error` reading "Danube's hosted AI is unavailable right now, so instructions-mode workflows cannot run. This is on Danube's side; retry later." | Instructions mode only: Danube's own provider account is out of credit. Nothing the user can fix and no parameter to change. Since 2026-09-27 this replaces the provider's own billing text and URL, which used to reach callers verbatim | Tell the user it is Danube-side and try later. Template-mode workflows and every non-AI tool are unaffected. Don't retry in a loop; don't `report_tool` a tool for it |
| `200`, body `status: "failed"`, `error` starting "AI orchestration error:" | Instructions mode only: any other failure from the orchestrating model | Read the quoted detail (same stripping and 300-char cap as the rate-limit row). Retry once; if it persists, the instructions or the `allowed_tool_ids` are the thing to change |
| `400` | The execution record couldn't be created — in practice a reused or unparseable `execution_id` | Generate a fresh UUID and re-POST |
| a timeout, or your gateway's own `504` | The run outlived the HTTP request. Not cancelled, not failed — Danube itself never returns 504 here | Poll `GET /workflows/executions/$EXEC_ID`. Never re-POST — a second concurrent run duplicates every write the first one makes |

Every *error* response above uses the one envelope documented earlier in this file —
`error.code` / `error.message` / `error.details`. There is no top-level `detail` key.

## Getting an API key without the dashboard (device flow)

```bash
curl -s -X POST "$BASE/auth/device/code" -H "Content-Type: application/json" -d '{"client_name": "OpenClaw"}'
# → {"device_code": "...", "user_code": "XXXX-XXXX", "verification_url": "https://...",
#    "expires_in": 600, "interval": 5, "org_id": null, "org_name": null}
# Optional "org_id": "<org id or slug>" mints the key INTO that shared organization; the response
# echoes org_id/org_name, and an unresolvable one is 404 {"error": {"code": "not_found",
# "message": "Organization not found"}} before any code is created. See the note below.
# The USER opens verification_url and enters user_code. Then poll:
curl -s -X POST "$BASE/auth/device/token" -H "Content-Type: application/json" -d '{"device_code": "<DEVICE_CODE>"}'
# 428 → wait `interval` seconds and poll again
# 200 {"api_key": "…", "key_prefix": "…", "org_id": …} → done; store api_key as DANUBE_API_KEY
#     (opaque token, no fixed prefix)
# 410 → start over
# 429 → the endpoint's rate limit, not a verdict on the authorization; see the note below
```

**The `org_id` on `/auth/device/code` is the one chance to pick the workspace before the key
exists.** Membership is not checked when the code is created — nobody is signed in yet — but it
is when the user enters the `user_code`: a non-member's `/auth/device/authorize` answers `403`
("This device asked to join an organization you are not a member of") and the code **stays
pending**, so a colleague who is a member can authorize the same code, and from the polling side
an organization nobody present belongs to looks like `428` forever. The key the flow mints is
stamped with that organization, and an org-owned key acts for it with **no `danube-org-id`
header**. With no `org_id` the key is stamped with the user's personal organization instead,
which is not a narrowing: only a shared org switches the request's context, so such a key behaves
like any ordinary personal key and still spans every organization the user belongs to.

Both endpoints carry rate limits: 10/minute on `/auth/device/code`, 30/minute on
`/auth/device/token`. They are unauthenticated, so there is no key to count against — the bucket
is keyed by the client address as the server sees it, which behind a hosted deployment's edge
may be shared far more widely than your own machine or egress. Polling at the advertised
`interval` of 5 s is 12/minute, the rate the flow is designed around; polling tighter spends
headroom that may not be only yours, and the `429` that follows is the rate limiter, not a
verdict on the authorization. Back off by `Retry-After` and keep polling the **same**
`device_code` — it stays valid for the remainder of its 600 s, since a rate-limited poll never
reaches the handler and a pending one changes nothing (no attempt counter, no early expiry).
Starting a fresh flow instead spends one of the 10/minute and makes the user enter a new
`user_code`.

Both failures use the same error envelope as everything else in this file, with the OAuth state
string as the *message* — not as a top-level key, and not as `detail`:

```text
HTTP 428  {"error": {"code": "precondition_required", "message": "authorization_pending"}}
HTTP 410  {"error": {"code": "gone", "message": "expired_token"}}
```

Poll on the status code. (Those two `code` values date from 2026-09-12; before that both
statuses fell through the envelope's map to `internal_error`, which read like a Danube fault
rather than a normal step of the flow.)

Full reference: https://docs.danubeai.com/api-reference/introduction
