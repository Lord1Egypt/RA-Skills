# AgentSafe Scan — API quick map

Base: `https://agentsafe.up.railway.app`  
Version field is on every successful response (`version`).

## Health

`GET /health` → `{ "status": "ok", "version": "…" }`

## Root product card

`GET /` → pricing, wallet, social, example payload, legal disclaimer

## Scan one skill

`POST /v1/scan`

Required: either `content` **or** `url`  
Recommended: stable `agent_id`  
Optional: `policy` (`default` | `paranoid` | `research`), `payment_tx`

Success highlights:

| Path | Meaning |
|------|---------|
| `report.risk_band` | cleanish → critical |
| `report.decision.action` | deny / review / allow_with_caution |
| `report.content_fingerprint` | sha for drift checks |
| `report.capability_signals` | shell / secrets / network / obfuscation flags |
| `free_tier` | used / limit / remaining |
| `next_action` | refuse / review / allow / pay steps |
| `payment` | price, chain, receive_wallet, paid |

Over free: **HTTP 402** with pay instructions (same body shape).

## Batch

`POST /v1/scan/batch` with `items: [{id?, content?|url?}, …]`  
Each item counts against free quota.

## Examples

`GET /v1/examples` — **synthetic** educational fixtures only (invalid hosts / toy patterns). Not live malware kits.

## Stats

`GET /v1/stats` — counts only (no skill payloads). Process-local counters may reset on redeploy.

## Skill + brief

| Path | Use |
|------|-----|
| `GET /skill.md` | This skill text served hot |
| `GET /llms.txt` | Compact agent brief |
| `GET /docs` | OpenAPI UI |

## Packs

- `GET /v1/packs` — catalog
- `POST /v1/packs/activate` — `{agent_id, pack_id, payment_tx}`
- `GET /v1/packs/status?agent_id=` — entitlement + quota

## Watch / rescan (v0.1.8+)

- `GET /v1/watch?agent_id=` — list watches
- `POST /v1/watch/add` — `{agent_id, url}`
- `POST /v1/watch/check` — `{agent_id, watch_id}`
- `POST /v1/watch/remove` — `{agent_id, watch_id}`
- `GET /v1/watch/due` — watches due for check
