# EVE ESI Skill for OpenClaw

An [OpenClaw](https://openclaw.ai) skill for interacting with the [EVE Online ESI API](https://developers.eveonline.com/api-explorer) (EVE Swagger Interface).

## Features

- **PKCE Authentication** — Secure OAuth2 flow via EVE SSO, auto-refreshing tokens
- **Multi-Character** — Store and manage tokens for unlimited characters
- **PI Monitoring** — Planetary Interaction status, extractor timers, storage fill levels
- **Market Prices** — Global average prices and Jita buy/sell lookups
- **ESI Queries** — Reusable Python helper with pagination, rate-limit handling, and error recovery
- **Threat Assessment** — System threat scoring using ESI kills/jumps + zKillboard PVP data
- **Route Planning** — Annotated routes with per-system threat levels
- **Dashboard Config** — Modular alert/report/market-tracking config with JSON Schema
- **Reference Docs** — Full scope list, endpoint index, auth flow details

## Structure

```
eve-esi/
├── SKILL.md                        # OpenClaw skill instructions (loaded by agent)
├── README.md                       # This file
├── .gitignore                      # Prevents token/secret commits
├── scripts/
│   ├── auth_flow.py                # One-time EVE SSO OAuth2 PKCE authentication
│   ├── get_token.py                # Token refresh helper (auto-rotates on every use)
│   ├── esi_query.py                # ESI query helper + high-level PI/market actions
│   └── validate_config.py          # Dashboard config validator
├── config/
│   ├── schema.json                 # JSON Schema for dashboard config
│   ├── example-config.json         # Ready-to-use template
│   └── esi_endpoints.json          # PI and market endpoint definitions
└── references/
    ├── authentication.md           # EVE SSO OAuth2 + PKCE details
    └── endpoints.md                # All character endpoints + scopes
```

## Installation

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/burnshall-ui/openclaw-eve-skill eve-esi
```

No pip dependencies — uses Python 3.8+ stdlib only.

## Authentication Setup

### Prerequisites

1. Register an app at [developers.eveonline.com](https://developers.eveonline.com/applications)
2. Set callback URL to `http://127.0.0.1:8080/callback`
3. Select the scopes you need (PI requires `esi-planets.manage_planets.v1`)
4. Note your **Client ID**

### One-time auth per character

```bash
# If on a remote server, set up an SSH tunnel first:
ssh -L 8080:127.0.0.1:8080 user@your-server -N

# Run the auth flow:
python3 scripts/auth_flow.py --client-id <YOUR_CLIENT_ID> --char-name main

# Open the shown URL in your browser and log in with your EVE account
```

Tokens are stored in `~/.openclaw/eve-tokens.json` (chmod 600, auto-rotated).

### Multiple characters

```bash
python3 scripts/auth_flow.py --client-id <CLIENT_ID> --char-name alt1
python3 scripts/auth_flow.py --client-id <CLIENT_ID> --char-name alt2

# List all authenticated characters:
python3 scripts/get_token.py --list
```

## Quick Start

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi

# Get a fresh access token (auto-refreshes on every call)
TOKEN=$(python3 $SKILL/scripts/get_token.py --char main)

# Wallet balance
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" \
  --endpoint "/characters/<CHAR_ID>/wallet/" --pretty

# Skill queue
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" \
  --endpoint "/characters/<CHAR_ID>/skillqueue/" --pretty

# All assets (paginated)
python3 $SKILL/scripts/esi_query.py --token "$TOKEN" \
  --endpoint "/characters/<CHAR_ID>/assets/" --pages --pretty

# PI: list all planets for a character
python3 $SKILL/scripts/esi_query.py --action pi_planets \
  --token "$TOKEN" --character-id <CHAR_ID> --pretty

# PI: parsed "needs attention" status per planet
python3 $SKILL/scripts/esi_query.py --action pi_status \
  --token "$TOKEN" --character-id <CHAR_ID> --pretty

# Market (public): Jita buy/sell snapshot for one type
python3 $SKILL/scripts/esi_query.py --action jita_price \
  --type-id 2393 --pretty

# Market (public): adjusted/average prices for all types
python3 $SKILL/scripts/esi_query.py --action market_price_bulk --pretty
```

## Planetary Interaction (PI)

The skill includes high-level PI actions that parse raw ESI data into actionable status reports.

### PI Actions

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi
TOKEN=$(python3 $SKILL/scripts/get_token.py --char main)
CHAR_ID=<your_character_id>

# List all PI planets for a character
python3 $SKILL/scripts/esi_query.py --action pi_planets \
  --token "$TOKEN" --character-id $CHAR_ID --pretty

# Full PI status with extractor timers, storage fill, attention flags
python3 $SKILL/scripts/esi_query.py --action pi_status \
  --token "$TOKEN" --character-id $CHAR_ID --pretty

# Detailed info for a specific planet
python3 $SKILL/scripts/esi_query.py --action pi_planet_detail \
  --token "$TOKEN" --character-id $CHAR_ID --planet-id <PLANET_ID> --pretty
```

### Action Mode Parameters

- `--action` supports: `pi_planets`, `pi_planet_detail`, `pi_status`, `market_price_bulk`, `jita_price`, `system_kills`, `system_jumps`, `system_info`, `route_plan`, `character_location`, `fw_systems`, `incursions`
- `--character-id` is required for PI actions and `character_location`
- `--planet-id` is required for `pi_planet_detail`
- `--type-id` is required for `jita_price`
- `--system-id` / `--system-ids` for threat-related actions
- `--origin`, `--destination`, `--route-flag` for `route_plan`

### PI Status Output

The `pi_status` action returns parsed data per planet:

| Field | Description |
|-------|-------------|
| `planet_name` | Resolved planet name (e.g. "Ikoskio VII") |
| `extractors` | List with product, expiry time, hours remaining, status |
| `storage_fill_pct` | Estimated launchpad/storage fill percentage |
| `factories` | Input/output product routing |
| `needs_attention` | `true` if extractor < 6h or storage > 80% |
| `action_required` | Human-readable description of what needs to be done |

### What PI can and cannot do

ESI provides **read-only** access to PI. The skill can:
- Monitor extractor timers and warn before expiry
- Track launchpad/storage fill levels
- Show factory routing and production chains
- Compare market prices for PI products

It **cannot** restart extractors, reroute products, or modify planet setups — that must be done in-game.

## Market Prices

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi

# Global average/adjusted prices for all items
python3 $SKILL/scripts/esi_query.py --action market_price_bulk --pretty

# Current Jita buy/sell for a specific item (e.g. Coolant = type_id 9832)
python3 $SKILL/scripts/esi_query.py --action jita_price --type-id 9832 --pretty
```

The `jita_price` action returns lowest sell, highest buy, spread, and order counts for The Forge region.

## Dashboard Config

Set up automated alerts, scheduled reports, and market price tracking:

```bash
# Copy example config
cp config/example-config.json ~/.openclaw/eve-dashboard-config.json

# Edit with your preferences
# Use $ENV:VARIABLE_NAME for tokens — never store secrets in plain text

# Validate
python3 scripts/validate_config.py ~/.openclaw/eve-dashboard-config.json
```

See [config/schema.json](config/schema.json) for the full schema.

Endpoint presets for PI and market requests are documented in [config/esi_endpoints.json](config/esi_endpoints.json).

### Alert Types

| Alert | Description |
|-------|-------------|
| `war_declared` | New war declaration against your corp |
| `structure_under_attack` | Structure attacked |
| `skill_complete` | Skill training finished |
| `wallet_large_deposit` | ISK deposit above threshold |
| `industry_job_complete` | Manufacturing/research job done |
| `pi_extractor_expired` | Planetary extraction head expired |
| `killmail` | New killmail received |
| `contract_expired` | Contract expired |

### Report Templates

| Report | Description |
|--------|-------------|
| `net_worth` | Total ISK across wallet + assets |
| `skill_queue` | Current training status |
| `industry_jobs` | Active manufacturing/research jobs |
| `market_orders` | Open buy/sell orders |
| `wallet_summary` | Recent transaction summary |
| `assets_summary` | Top asset locations by value |

## Threat Assessment & Route Planning

The skill provides threat intelligence for PI operations in low/null-sec systems.

### Data Sources

| Source | Data | Auth |
|--------|------|------|
| ESI `/universe/system_kills/` | Ship/Pod/NPC kills (last hour) | No |
| ESI `/universe/system_jumps/` | Jump traffic (last hour) | No |
| ESI `/route/{origin}/{destination}/` | Route planning | No |
| ESI `/fw/systems/` | Faction Warfare contested systems | No |
| ESI `/incursions/` | Active NPC incursions | No |
| zKillboard API | PVP kills with value (last 24h) | No |

### Threat Levels

| Level | Score | Advice |
|-------|-------|--------|
| `low` | 0-15 | Normal PI operations |
| `medium` | 15-40 | Quick in, quick out |
| `high` | 40-80 | Scout/Cloak only |
| `critical` | 80+ | Do NOT enter |

### ESI Actions

```bash
SKILL=~/.openclaw/workspace/skills/eve-esi

# System kills (last hour, optionally filtered)
python3 $SKILL/scripts/esi_query.py --action system_kills --system-ids 30002537 --pretty

# System jump traffic
python3 $SKILL/scripts/esi_query.py --action system_jumps --system-ids 30002537 --pretty

# System info (name, security status)
python3 $SKILL/scripts/esi_query.py --action system_info --system-id 30002537 --pretty

# Route planning
python3 $SKILL/scripts/esi_query.py --action route_plan --origin 30000142 --destination 30002537 --route-flag secure --pretty

# Character location
TOKEN=$(python3 $SKILL/scripts/get_token.py --char main)
python3 $SKILL/scripts/esi_query.py --action character_location --token "$TOKEN" --character-id $CHAR_ID --pretty

# FW systems & incursions
python3 $SKILL/scripts/esi_query.py --action fw_systems --pretty
python3 $SKILL/scripts/esi_query.py --action incursions --pretty
```

### Threat Assessment (Workspace Scripts)

The threat scoring logic and caching live in the agent workspace (`~/.openclaw/workspace/scripts/`), not in this repo. See `SKILL.md` for usage details.

## Security

- Tokens stored in `~/.openclaw/eve-tokens.json` with `chmod 600`
- Refresh tokens rotate on every use (EVE SSO best practice)
- PKCE flow — no client secret needed
- Dashboard config supports `$ENV:VARIABLE_NAME` to keep secrets out of files
- `.gitignore` prevents accidental token commits
- **Never commit** `eve-tokens.json` or configs with real tokens

## Scopes

The default auth flow requests these scopes:

| Scope | Purpose |
|-------|---------|
| `esi-wallet.read_character_wallet.v1` | ISK balance, journal, transactions |
| `esi-assets.read_assets.v1` | Item inventory |
| `esi-skills.read_skills.v1` | Trained skills, SP |
| `esi-skills.read_skillqueue.v1` | Skill queue |
| `esi-clones.read_clones.v1` | Jump clones, home station |
| `esi-clones.read_implants.v1` | Active implants |
| `esi-location.read_location.v1` | Current system/station |
| `esi-location.read_ship_type.v1` | Current ship |
| `esi-location.read_online.v1` | Online status |
| `esi-planets.manage_planets.v1` | PI colonies and extractors |
| `esi-industry.read_character_jobs.v1` | Industry jobs |
| `esi-markets.read_character_orders.v1` | Market orders |
| `esi-contracts.read_character_contracts.v1` | Contracts |
| `esi-killmails.read_killmails.v1` | Killmails |
| `esi-characters.read_notifications.v1` | Notifications |
| `esi-characters.read_fatigue.v1` | Jump fatigue |
| `esi-mail.read_mail.v1` | EVE mail |

Edit `SCOPES` in `auth_flow.py` to customize.

## Requirements

- Python 3.8+ (stdlib only for core ESI queries)
- OpenClaw gateway (for agent integration)
- **Redis** (optional, for PI market price caching)
- **Python `redis` package** (optional, only needed for price cache)

### Redis Setup (optional)

Redis is used to cache PI market prices with a 1-hour TTL. Without it, market prices are fetched live from ESI on every request.

```bash
# Install Redis
sudo apt install redis-server
sudo systemctl enable redis-server

# Install Python redis package
pip3 install redis

# Test
redis-cli ping   # → PONG
```

The companion script `cache_market_prices.py` (not part of this repo, lives in the agent workspace) fetches PI product prices from ESI and caches them in Redis under the key schema `eve:market:price:{type_id}`.

## Links

- [EVE ESI API Explorer](https://developers.eveonline.com/api-explorer)
- [EVE Developer Portal](https://developers.eveonline.com/applications)
- [OpenClaw Docs](https://docs.openclaw.ai)
