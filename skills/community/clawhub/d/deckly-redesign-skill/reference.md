# Deckly API Reference

Base URL: `https://deckly.art` (override with `DECKLY_API_BASE`). Auth: `Authorization: Bearer <token>`.

## Authentication

Two token types work as `Authorization: Bearer <value>`:
- A JWT from `/auth/login` or `/auth/verify-email` (expires).
- A long-lived API key (`dk_...`) created via `/auth/api-keys` (recommended for skills).

### Register in-conversation (new user)

```bash
# 1. register -> emails a 6-digit code
curl -s -X POST "$BASE/auth/register" -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"chosen-pw"}'
# 2. verify with the code -> returns a JWT
curl -s -X POST "$BASE/auth/verify-email" -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","code":"123456"}'
# -> {"access_token":"<JWT>"}
# 3. mint a long-lived key with that JWT
curl -s -X POST "$BASE/auth/api-keys" -H "Authorization: Bearer <JWT>" \
  -H 'Content-Type: application/json' -d '{"name":"deckly-skill"}'
# -> {"api_key":"dk_...", "prefix":"dk_xxxxxxxx", ...}  (shown once)
```

If `/auth/register` returns 400 "already exists", the email has an account — use login with the password instead.

### Existing user (login required to fetch a key)

```bash
curl -s -X POST "$BASE/auth/login" -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"..."}'   # -> {"access_token":"<JWT>"}
# then POST /auth/api-keys with the JWT as above to mint a dk_ key.
```

### API key management

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | `/auth/api-keys` | JWT or key | Create a key (returns full `api_key` once) |
| GET | `/auth/api-keys` | JWT or key | List keys (metadata only, no secret) |
| DELETE | `/auth/api-keys/{id}` | JWT or key | Revoke a key |

The raw `dk_` key cannot be retrieved later (only its hash is stored); mint a new one if lost.

Use the token on every protected call: `-H "Authorization: Bearer $TOKEN"`.

## Style presets

`style_preset` is a free-form string resolved server-side in this order:

1. `text_style:<id>` — text-description style, no template image. Built-in ids:
   `minimalist_corporate`, `flat_illustration`, `futuristic_tech`, `premium_presentation`, `academic_lecture`.
2. Template theme id — a folder under the server's templates dir (e.g. `dark-blue-business`, `dark-green-premium`, `dark-red-business`). List live values with `GET /templates`.
3. Any other string — AI generates a custom template set from the deck's analysis.

`GET /templates` and `GET /text-styles` are unauthenticated and return the available options.

## Endpoints used by this skill

| Step | Method | Path | Auth | Body |
|------|--------|------|------|------|
| create | POST | `/projects` | optional | `{"name": str}` |
| upload | POST | `/projects/{id}/upload` | none | multipart `file` |
| extract | POST | `/projects/{id}/analyze` | none | — |
| status | GET | `/projects/{id}/status` | owner | — |
| analysis | GET | `/projects/{id}/analysis` | owner | — |
| quote | POST | `/projects/{id}/quote` | owner | `{"slide_indices":[int]}` |
| redesign | POST | `/projects/{id}/redesign` | **required** | `RedesignRequest` |
| continue | POST | `/projects/{id}/continue` | required | — |
| slides | GET | `/projects/{id}/slides` | owner | — |
| versions | GET | `/projects/{id}/slides/{idx}/versions` | required | — |
| select version | POST | `/projects/{id}/slides/{idx}/versions/select` | required | `{"path": str}` |
| download | GET | `/projects/{id}/download` | required | — (returns pptx) |
| user | GET | `/auth/me` | required | — |

### RedesignRequest

```json
{
  "slide_indices": [1, 2, 3],
  "style_preset": "text_style:minimalist_corporate",
  "force_regenerate": false,
  "is_partial_update": false,
  "custom_prompt": null,
  "reference_slide_index": null,
  "revert_to_previous": false
}
```

- Full redesign: `is_partial_update=false`, charges by tier.
- Fine-tune one slide: `slide_indices=[N]`, `is_partial_update=true`, `force_regenerate=true`, `custom_prompt="..."` (1 credit).
- Revert one slide: `is_partial_update=true`, `force_regenerate=true`, `revert_to_previous=true` (free).
- `reference_slide_index`: reuse another slide's redesigned look as reference.

## Status values

- Extract done: `extracted` (also `analyzed`, `parsed`).
- Success terminal: `completed`, `partial_completed`, `preview_completed`, `preview_partial_completed`.
- Failure terminal: `failed`, `cancelled`, `preview_failed`.
- `preview_*` means a free 3-slide preview finished and no full pptx was assembled — call `continue` to render the paid full deck.

Poll `GET /projects/{id}/status` (every 2s for extract, 5s for redesign). Slide-level progress: `GET /projects/{id}/slides` returns `[{index, status, original_url, redesigned_url, updated_at, error_message}]` (`status` per slide: `pending|processing|completed|failed`).

## Pricing

| Selected slides | Credits | Tier |
|-----------------|---------|------|
| 1–10 | 10 | small |
| 11–20 | 20 | medium |
| 21–60 | 40 | large |

- First-time account: one free preview, 3 slides, 0 credits (auto-applied by `/redesign`).
- Fine-tune slide: 1 credit each (failed slides not charged). Revert / version select: free.
- `continue`: charges the full tier for all selected slides (used after a free preview).
- Read balance from `/auth/me` (`credit_balance`) or `/quote` (`user_balance`, `can_afford`).

## Raw HTTP flow (no Python)

```bash
BASE=https://deckly.art
TOKEN=...   # from /auth/login

# 1. create + upload
PID=$(curl -s -X POST "$BASE/projects" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"name":"My Deck"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["id"])')
curl -s -X POST "$BASE/projects/$PID/upload" -H "Authorization: Bearer $TOKEN" -F "file=@deck.pptx"

# 2. extract, then poll until status == extracted
curl -s -X POST "$BASE/projects/$PID/analyze" -H "Authorization: Bearer $TOKEN"
curl -s "$BASE/projects/$PID/status" -H "Authorization: Bearer $TOKEN"

# 3. analysis + redesign
curl -s "$BASE/projects/$PID/analysis" -H "Authorization: Bearer $TOKEN"
curl -s -X POST "$BASE/projects/$PID/redesign" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"slide_indices":[1,2,3],"style_preset":"text_style:minimalist_corporate","force_regenerate":false,"is_partial_update":false,"revert_to_previous":false}'

# 4. poll status until terminal, then download
curl -s "$BASE/projects/$PID/download" -H "Authorization: Bearer $TOKEN" -o final.pptx
```

The full OpenAPI schema is available at `$BASE/openapi.json`.
