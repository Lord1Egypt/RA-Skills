---
name: eve-esi
description: "Query and manage EVE Online characters via the ESI (EVE Swagger Interface) REST API. Performs OAuth2/PKCE browser login and stores plus auto-refreshes long-lived OAuth tokens locally in ~/.openclaw/eve-tokens.json. Read-only by default and can reach any ESI endpoint, including non-character public data; state-changing writes (mail, fittings, market orders, planetary interaction) happen only when explicitly invoked with --allow-write. Use when the user asks about EVE Online character data, wallet balance, ISK transactions, assets, skill queue, skill points, clone locations, implants, fittings, contracts, market orders, mail, industry jobs, killmails, planetary interaction, loyalty points, or any other EVE account management task."
type: scripts
includes:
  - scripts/auth_flow.py
  - scripts/get_token.py
  - scripts/esi_query.py
  - scripts/token_store.py
  - scripts/user_agent.py
  - scripts/validate_config.py
  - config/schema.json
  - config/example-config.json
  - config/esi_endpoints.json
  - references/authentication.md
  - references/endpoints.md
auth:
  method: oauth2_pkce
  provider: EVE SSO (login.eveonline.com)
  credential_storage: "~/.openclaw/eve-tokens.json"
  setup: "Run scripts/auth_flow.py once per character with a valid EVE Client ID. Ask the user which scope profile they want first (basic|pi|industry|full, default pi) — do not pick for them. Tokens are stored locally and auto-refreshed by scripts/get_token.py."
  required_for: "All authenticated ESI endpoints (wallet, assets, skills, PI, industry, etc.). Public endpoints work without auth."
env:
  - name: EVE_CLIENT_ID
    description: "EVE Developer Application Client ID (from https://developers.eveonline.com/applications). Not needed at runtime — pass directly to auth_flow.py via --client-id. Only set as env var if using $ENV: references in your dashboard config."
    required: false
    sensitive: false
  - name: EVE_TOKEN_MAIN
    description: "ESI OAuth2 access token for the main character. Not needed at runtime — scripts auto-manage tokens via ~/.openclaw/eve-tokens.json (created by auth_flow.py). Only set as env var if using $ENV: references in your dashboard config."
    required: false
    sensitive: true
  - name: EVE_REFRESH_MAIN
    description: "ESI OAuth2 refresh token for automatic access token renewal. Not needed at runtime — scripts auto-manage tokens via ~/.openclaw/eve-tokens.json. Only set as env var if using $ENV: references in your dashboard config."
    required: false
    sensitive: true
  - name: TELEGRAM_BOT_TOKEN
    description: "Telegram Bot API token for sending alerts and reports. Only needed if Telegram notifications are configured."
    required: false
    sensitive: true
  - name: TELEGRAM_CHAT_ID
    description: "Telegram chat ID where notifications are sent. Only needed if Telegram notifications are configured."
    required: false
    sensitive: false
  - name: DISCORD_WEBHOOK_URL
    description: "Discord webhook URL for sending alerts and reports. Only needed if Discord notifications are configured."
    required: false
    sensitive: true
---

# Data Handling

This skill communicates with the following external services. Every outbound
call is either a public/unauthenticated CCP endpoint, an OAuth2 flow against
the official EVE SSO, or an optional, user-configured notification sink.

- **EVE Online ESI API** (`esi.evetech.net`) — official EVE Online REST API
  (operated by CCP Games) for all character and universe data queries.
  Includes bulk lookup endpoints such as `POST /characters/affiliation/`
  and `POST /universe/names/`, which resolve public numeric IDs
  (character/corp/alliance/type IDs) to public data. These POST bodies never
  contain tokens, credentials, or private account data — only IDs that are
  already public in-game. Authenticated endpoints (wallet, assets, skills,
  etc.) send the OAuth2 bearer token only to this same host, per ESI's own
  API contract.
- **EVE SSO** (`login.eveonline.com`) — official OAuth2/PKCE authorization
  server for EVE Online. Used only for the login/token-refresh flow described
  in `references/authentication.md`.
- **EVE Developer Portal** (`developers.eveonline.com/applications`) —
  official CCP portal where the *user* registers their own EVE application
  and obtains a Client ID. This skill never calls this URL programmatically;
  it is referenced in documentation only, as the one-time manual step a user
  performs before running `scripts/auth_flow.py --client-id <...>`.
- **zKillboard API** (`zkillboard.com/api/`) — optional, public, unauthenticated.
  Only used for PVP threat-assessment features; disabled unless threat/route
  scripts are invoked.
- **Telegram Bot API** — optional, only contacted if the user sets
  `TELEGRAM_BOT_TOKEN` and configures alerts.
- **Discord Webhooks** — optional, only contacted if the user sets
  `DISCORD_WEBHOOK_URL` and configures alerts.

No character data, tokens, or credentials are sent to any third-party server
beyond the above. Telegram/Discord only receive the specific alert text the
user has configured — never raw account data or tokens.

# What this skill can access, and what it will not do

**Read-only by default.** GET requests and the documented bulk-lookup POST
endpoints run normally. Any other POST, plus PUT and DELETE, is refused unless
you pass `--allow-write` explicitly. Without that flag this skill cannot send
mail, change contacts, alter contracts, open in-game windows, or modify your
account in any way.

**Sensitive data.** The scopes you grant during `auth_flow.py` decide what the
skill can read. Several are genuinely private: wallet balance and full ISK
transaction history, complete asset lists, mail contents, contracts, clone and
implant locations, and current in-space location. Grant only the scopes your
use case needs — the skill works fine with a narrow scope set, and public
endpoints need no scopes at all.

## Agent instruction: ask before you authenticate

**Do not choose a scope profile on the user's behalf.** Scopes are granted once
and stay granted until revoked, so this is the user's decision, not yours.

Before running `auth_flow.py`, show the user the profiles and ask which one
they want:

| Profile | Scopes | Grants access to |
|---|---|---|
| `basic` | 7 | Skills, skill queue, clones, implants, location, ship, online status |
| `pi` **(default)** | 8 | `basic` plus Planetary Interaction |
| `industry` | 11 | `basic` plus assets, industry jobs, market orders, contracts |
| `full` | 17 | Everything, **including wallet balance, ISK history and mail** |

`python3 scripts/auth_flow.py --list-scope-profiles` prints the exact scope
list for each. `--scopes "<space separated>"` takes an explicit set.

If the user has not expressed a preference, use the default and say so — do not
silently pick `full` because it is convenient. If a later query fails for lack
of a scope, report which scope is missing and let the user decide whether to
re-authenticate with a wider profile.

The final gate is outside this skill: EVE SSO shows the user a consent screen
listing every requested scope, and nothing is granted until they approve it in
their browser.

**Token handling.** Access tokens are bearer credentials: anyone holding one can
read your account until it expires (~20 min). Refresh tokens are long-lived and
rotate on each use.

- Prefer `esi_query.py --char <name>`, which refreshes the token in-process. The
  token never enters argv.
- Avoid `--token "$TOKEN"` and `curl -H "Authorization: Bearer $TOKEN"`: command
  lines are visible to any local user via `ps`, and land in your shell history.
  Use `--token-stdin` when a token must come from outside.
- Never paste a token into a config file, a bug report, a log, or a chat message.

**Alert transmission.** If you configure Telegram or Discord, the alert text you
define is sent to those services in plaintext over their APIs. Do not template
raw wallet figures or asset inventories into alerts you would not want stored on
a third-party server.

# EVE Online ESI

The ESI (EVE Swagger Interface) is the official REST API for EVE Online third-party development.

- **Base URL**: `https://esi.evetech.net` — no version segment.
- **Versioning**: send `X-Compatibility-Date: 2026-08-04` on every request. CCP
  has replaced the old `/latest`, `/legacy` and `/v5` URL prefixes with this
  header ([dev blog](https://developers.eveonline.com/blog/changing-versions-v42-was-getting-out-of-hand)).
  A request that omits it does not get the newest behaviour — it gets the
  *oldest* one ESI still serves. `esi_query.py` sets the header itself; override
  it with `--compatibility-date` or `EVE_ESI_COMPATIBILITY_DATE`.
- **Spec**: `https://esi.evetech.net/meta/openapi.json` (OpenAPI 3.1) or
  `https://esi.evetech.net/meta/openapi-3.0.json` (OpenAPI 3.0). The old
  `swagger.json` is deprecated and no longer receives new routes
  ([dev blog](https://developers.eveonline.com/blog/changing-specs-from-swagger-to-openapi)).
- **Valid compatibility dates**: <https://esi.evetech.net/meta/compatibility-dates>
- **Changelog**: <https://esi.evetech.net/meta/changelog> — check this before
  bumping the compatibility date, and adjust for any `is_breaking` entry on an
  endpoint this skill uses.
- **API Explorer**: <https://developers.eveonline.com/api-explorer>
- **User-Agent**: every request identifies the skill and links its source repo,
  because CCP treats anonymous traffic as grounds for throttling. Set
  `EVE_ESI_CONTACT` to an email, `discord:name` or `eve:charname` to add the
  contact CCP would rather have.

## Skill Location

All scripts live at: `~/.openclaw/workspace/skills/eve-esi/scripts/`

Always use full paths when calling scripts:
```bash
SKILL=~/.openclaw/workspace/skills/eve-esi
```

## Authentication

Tokens are stored in `~/.openclaw/eve-tokens.json` (created by auth_flow.py, chmod 600).
All scripts (`get_token.py`, `esi_query.py`) read from this file directly — **no env vars are required for normal operation.**

**First-time setup** (once per character). The Client ID comes from the user's
own application at <https://developers.eveonline.com/applications> — it is not
stored anywhere by this skill, so ask the user for it rather than hunting for
it. Ask which scope profile they want before running this; do not choose for
them.

```bash
# 0. In the EVE application, the Callback URL must be exactly
#    http://localhost:8080/callback — the developer portal allows the http
#    scheme only for the host `localhost` and rejects 127.0.0.1 on save.
# 1. Set up SSH tunnel on your local PC:
#    ssh -L 8080:127.0.0.1:8080 user@your-server -N
# 2. Run auth flow on server (pass Client ID directly):
python3 ~/.openclaw/workspace/skills/eve-esi/scripts/auth_flow.py \
  --client-id <YOUR_CLIENT_ID> --char-name main --scope-profile <basic|pi|industry|full>
# 3. Open the shown URL in browser, log in with EVE account
```

**Preferred: let the query script handle the token.** `--char <name>` resolves and
refreshes the token in-process, so it never appears on a command line, in shell
history, or in your logs:
```bash
python3 ~/.openclaw/workspace/skills/eve-esi/scripts/esi_query.py --char main \
  --endpoint "/characters/<CHAR_ID>/wallet/" --pretty
```

Only if you genuinely need the raw token elsewhere (it expires after ~20 min,
refresh is automatic):
```bash
python3 ~/.openclaw/workspace/skills/eve-esi/scripts/get_token.py --char main
```
Do not capture it into a shell variable and pass it as `--token "$TOKEN"` —
that exposes it via `ps` and shell history. Use `--token-stdin` if a token must
be handed over.

**List authenticated characters:**
```bash
python3 ~/.openclaw/workspace/skills/eve-esi/scripts/get_token.py --list
```

For full OAuth2/PKCE details: see `references/authentication.md`.

## Calling ESI directly

The `curl` examples below are reference material for the raw API. Every one of
them goes through this helper, which sets the two headers ESI expects: a
compatibility date, so the response contract stays pinned, and a User-Agent, so
CCP can see who is calling. `esi_query.py` sets both by itself — that is one
reason it is the preferred path.

```bash
ESI="https://esi.evetech.net"
COMPAT="2026-08-04"
UA="OpenClaw-ESI-Skill/1.3.3 (+https://github.com/burnshall-ui/openclaw-eve-skill)"

esi() { curl -s -H "X-Compatibility-Date: $COMPAT" -H "User-Agent: $UA" "$@"; }
```

## Public endpoints (no auth)

```bash
# Character public info
esi "$ESI/characters/2114794365/" | python -m json.tool

# Portrait URLs
esi "$ESI/characters/2114794365/portrait/"

# Corporation history
esi "$ESI/characters/2114794365/corporationhistory/"

# Bulk affiliation lookup
esi -X POST "$ESI/characters/affiliation/" \
  -H "Content-Type: application/json" \
  -d '[2114794365, 95538921]'
```

## Character info (authenticated)

> These put the token on a command line, where `ps` and shell history expose it.
> For day-to-day use prefer `esi_query.py --char <name>` (see
> [Using the query script](#using-the-query-script)).

```bash
TOKEN="<your_access_token>"
CHAR_ID="<your_character_id>"

# Online status (scope: esi-location.read_online.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/online/"
```

## Wallet

```bash
# Balance (scope: esi-wallet.read_character_wallet.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/wallet/"

# Journal (paginated)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/wallet/journal/?page=1"

# Transactions
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/wallet/transactions/"
```

## Assets

```bash
# All assets (paginated; scope: esi-assets.read_assets.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/assets/?page=1"

# Resolve item locations
esi -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890, 9876543210]' \
  "$ESI/characters/$CHAR_ID/assets/locations/"

# Resolve item names
esi -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[1234567890]' \
  "$ESI/characters/$CHAR_ID/assets/names/"
```

## Skills

```bash
# All trained skills + total SP (scope: esi-skills.read_skills.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/skills/"

# Skill queue (scope: esi-skills.read_skillqueue.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/skillqueue/"

# Attributes (intelligence, memory, etc.)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/attributes/"
```

## Location and ship

```bash
# Current location (scope: esi-location.read_location.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/location/"

# Current ship (scope: esi-location.read_ship_type.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/ship/"
```

## Clones and implants

```bash
# Jump clones + home station (scope: esi-clones.read_clones.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/clones/"

# Active implants (scope: esi-clones.read_implants.v1)
esi -H "Authorization: Bearer $TOKEN" "$ESI/characters/$CHAR_ID/implants/"
```

## More endpoints

For contracts, fittings, mail, industry, killmails, market orders, mining, planetary interaction, loyalty points, notifications, blueprints, standings, and all other character endpoints, see [references/endpoints.md](references/endpoints.md).

## Dashboard Config

The skill defines and validates a config format for alerts, reports and market
tracking. It does **not** execute any of it: there is no poller, no scheduler
and no notification sender in this skill. Do not tell the user their alerts are
running because a config exists — the config is a description that some other
automation has to act on. `validate_config.py` checks that a config is well
formed and that the stored token actually carries the scopes it references.

- **Schema**: [config/schema.json](config/schema.json) — full JSON Schema with all fields, types, and defaults
- **Example**: [config/example-config.json](config/example-config.json) — ready-to-use template

### Features

| Module | Description |
|--------|-------------|
| **Alerts** | Real-time polling for war decs, structure attacks, skill completions, wallet changes, industry jobs, PI extractors, killmails, contracts, clone jumps, mail |
| **Reports** | Cron-scheduled summaries: net worth, skill queue, industry, market orders, wallet, assets |
| **Market** | Price tracking with absolute thresholds and trend detection |

### Security

Do **not** write tokens into the dashboard config file. There are two supported
places for credentials, and they do not conflict:

| Location | What lives there | Who writes it |
|----------|------------------|---------------|
| `~/.openclaw/eve-tokens.json` | The canonical token store: refresh tokens + client IDs, one entry per character. Created `chmod 600`, rewritten atomically, lock-protected. | `auth_flow.py` / `get_token.py` |
| Dashboard config JSON | No secrets. Reference env vars if a value is unavoidable. | You |

The scripts read the token store directly, so a normal setup needs **no**
credentials in the config file and no env vars at all. Only use `$ENV:`
references if you drive the dashboard from a system that cannot reach the
token store:

```json
{
  "token": "$ENV:EVE_TOKEN_MAIN",
  "refresh_token": "$ENV:EVE_REFRESH_MAIN"
}
```

The config file should live outside the workspace (e.g. `~/.openclaw/eve-dashboard-config.json`).

### Validate a config

```bash
python scripts/validate_config.py path/to/config.json

# Show example config
python scripts/validate_config.py --example

# Show JSON schema
python scripts/validate_config.py --schema
```

## Using the query script

Pass `--char <name>` and the script refreshes the stored token itself. The token
never appears on a command line, so `ps` and shell history cannot leak it.

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi
# Replace 'main' with your --char-name if you authenticated under a different name.
CHAR_ID=$(python3 $SKILL/scripts/get_token.py --char main --char-id)

# Simple query
python3 $SKILL/scripts/esi_query.py --char main --endpoint "/characters/$CHAR_ID/wallet/" --pretty

# Fetch all pages of assets
python3 $SKILL/scripts/esi_query.py --char main --endpoint "/characters/$CHAR_ID/assets/" --pages --pretty

# Bulk lookup POST (asset names) — a read-only lookup, no --allow-write needed
python3 $SKILL/scripts/esi_query.py --char main --endpoint "/characters/$CHAR_ID/assets/names/" \
  --method POST --body '[1234567890]' --pretty
```

If you must supply a token from elsewhere, pipe it in rather than passing `--token`:

```bash
printf '%s\n' "$TOKEN" | python3 $SKILL/scripts/esi_query.py --token-stdin --endpoint /characters/$CHAR_ID/wallet/
```

## Best practices

- **Caching**: respect the `Expires` header; do not poll before it expires.
  Polling around the cache is treated as circumventing it and can get you banned.
- **Error limits**: monitor `X-ESI-Error-Limit-Remain`; back off when low. A 4xx
  costs five times what a 2xx costs, so validate input before sending it.
- **Rate limits**: routes under bucket limiting report `X-Ratelimit-Remaining`
  and answer with `429` plus `Retry-After` once the bucket is empty.
  `esi_query.py` honours both, and warns once a bucket drops below 20%.
- **User-Agent**: always set a descriptive User-Agent with contact info.
- **Pagination**: check the `X-Pages` response header; iterate with `?page=N`.
- **Versioning**: do not use URL prefixes. `/latest/`, `/legacy/`, `/dev/` and
  `/v5/` are deprecated — send the `X-Compatibility-Date` header instead, and
  pin it to a date you have actually reviewed. `esi_query.py` strips a version
  prefix if one reaches it anyway.
- **Scheduling**: stagger periodic jobs rather than firing them all on `*/5`.

## Threat Assessment & Route Planning

The skill provides threat intelligence for PI systems in low/null-sec space. Data sources: ESI (kills, jumps, FW, incursions) and zKillboard (PVP activity).

### ESI Threat Endpoints

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi

# System kills (last hour) — all or filtered
python3 $SKILL/scripts/esi_query.py --action system_kills --pretty
python3 $SKILL/scripts/esi_query.py --action system_kills --system-ids 30002537,30045337 --pretty

# System jump traffic (last hour)
python3 $SKILL/scripts/esi_query.py --action system_jumps --system-ids 30045337 --pretty

# System info (name, security status)
python3 $SKILL/scripts/esi_query.py --action system_info --system-id 30002537 --pretty

# Route planning (flags: secure, shortest, insecure)
python3 $SKILL/scripts/esi_query.py --action route_plan --origin 30000142 --destination 30002537 --route-flag secure --pretty

# Character location (requires auth)
python3 $SKILL/scripts/esi_query.py --action character_location --char main --character-id $CHAR_ID --pretty

# Faction warfare systems
python3 $SKILL/scripts/esi_query.py --action fw_systems --pretty

# Active incursions
python3 $SKILL/scripts/esi_query.py --action incursions --pretty
```

### Threat Assessment Scripts (Workspace)

> **Hinweis:** Die Workspace-Skripte (`threat_query.py`, `cache_threat_data.py`, `cache_market_prices.py`) sind Referenz-Beschreibungen und müssen erst im Agent-Workspace erstellt werden, bevor sie genutzt werden können.

These scripts live in `~/.openclaw/workspace/scripts/` (not in the skill repo):

```bash
# Threat level for specific systems
python3 ~/.openclaw/workspace/scripts/threat_query.py --action threat_assessment --system-ids 30002537,30045337

# Threat for all PI systems across all characters
python3 ~/.openclaw/workspace/scripts/threat_query.py --action threat_assessment_pi

# Route with per-system threat annotation
python3 ~/.openclaw/workspace/scripts/threat_query.py --action route_annotated --origin 30000142 --destination 30002537

# Route from character's current location
python3 ~/.openclaw/workspace/scripts/threat_query.py --action route_annotated --character main --destination 30045337

# Full PI + Threat morning briefing
python3 ~/.openclaw/workspace/scripts/threat_query.py --action pi_briefing
```

### Threat Levels

| Level | Score | Meaning |
|-------|-------|---------|
| `low` | 0-15 | Normaler PI-Betrieb |
| `medium` | 15-40 | Schnell rein, schnell raus |
| `high` | 40-80 | Nur mit Scout/Cloak |
| `critical` | 80+ | NICHT reinfliegen |

### Threat Cache

Threat data is cached in Redis (30min TTL for ESI, 1h for zKillboard). The cache is updated every 30 minutes via cron:

```bash
# Update cache manually
python3 ~/.openclaw/workspace/scripts/cache_threat_data.py

# Show cached threat data
python3 ~/.openclaw/workspace/scripts/cache_threat_data.py --check
```

## Resolving type IDs

ESI returns numeric type IDs (e.g. for ships, items, skills). Resolve names via:

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi

# Single type
python3 $SKILL/scripts/esi_query.py --endpoint "/universe/types/587/" --pretty

# Bulk names (up to 1000 IDs)
python3 $SKILL/scripts/esi_query.py --endpoint "/universe/names/" \
  --method POST --body '[587, 638, 11393]' --pretty
```
