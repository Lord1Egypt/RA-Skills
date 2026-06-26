# Voting — partner / stakeholder feedback on a deployed lookbook

A lookbook is more useful when the customer's partner (or a stylist friend, or an event co-host) can react to it. This reference describes the **voting capability**: thumbs up/down per look and per item, free-text comments, stored on Cloudflare KV via Pages Functions.

**Default behavior:** `scripts/deploy-lookbook.sh` bakes voting into every Cloudflare Pages deploy. The agent supplies a KV namespace id (one-time setup, reused across lookbooks); the script handles copying Functions, rendering `wrangler.toml`, pulling favicons, injecting the UI, deploying, and smoke-testing `/api/votes` after the upload.

Opt out per-deploy with `--no-voting` (read-only static lookbook, no `/api/*`). Skip when:

- The customer explicitly asks for a static lookbook ("no form", "just the photos")
- The deploy target isn't Cloudflare Pages (voting is Cloudflare-specific by design — see *Why Cloudflare-only* below)

Surface a one-line confirmation before sharing the URL: *"The lookbook URL will include a vote form — anyone with the link can submit feedback. OK?"* The form is unobtrusive when no one votes, but the customer should know it's there before sending the link to a partner.

## Architecture (~80 lines of code, no DB, no auth)

```
                                                       ┌────────────────────────┐
   ┌────────┐  GET /         ┌──────────────────┐      │  KV namespace          │
   │ viewer │ ─────────────▶ │ Cloudflare Pages │      │  LOOKBOOK_VOTES        │
   └────────┘                │  static index.   │      │                        │
                             │  html (with vote │      │  vote:<lid>:<ts>:<r>   │
                             │  UI baked in)    │      │   → JSON {voter,       │
                             └──────────────────┘      │      looks{}, items{}, │
                                       │                │      comment, ...}     │
                                       │ POST /api/vote │                        │
                                       ▼                │                        │
                             ┌──────────────────┐      │                        │
                             │ functions/api/   │ ────▶│                        │
                             │  vote.js         │      │                        │
                             │  (writes 1 key)  │      │                        │
                             └──────────────────┘      │                        │
                                                       │                        │
   ┌────────┐  GET /api/votes  ┌──────────────────┐   │                        │
   │ owner  │ ─────────────▶   │ functions/api/   │ ──▶│                        │
   └────────┘                  │  votes.js        │   │                        │
                               │  (list + tally)  │   │                        │
                               └──────────────────┘   └────────────────────────┘
```

Three pieces:

1. **One KV namespace** (`LOOKBOOK_VOTES`) — created once per Cloudflare account, reused across lookbooks. Each vote is one key. The lookbook id is prefixed into the key so the same namespace can serve many concurrent lookbooks.
2. **Two Pages Functions** — `functions/api/vote.js` (POST handler) and `functions/api/votes.js` (owner-side GET tally). Both <40 lines, no external deps.
3. **Voting UI** — a `<section class="vote">` block injected into `index.html` after the deterministic build. CSS + JS are inline; the form posts to `/api/vote`.

No login, no session, no sign-up flow. The page URL is the shared secret — the customer sends it to the partner over iMessage, the partner taps and votes. For higher-stakes contexts (e.g. an event committee), add a signed-link param or a cookie inside `vote.js`.

## Schema

### POST `/api/vote` request body

```jsonc
{
  "voter":   "Sasha",           // 1..60 chars; the partner's name
  "comment": "love the cream linen, navy polo is meh on the body",  // 0..1000 chars
  "looks":  { "look1": "up", "look2": "down" },     // per-look thumbs; optional
  "items":  { "BM13139.1653OLNSTL": "up", ... }     // per-item thumbs, keyed by SKU; optional
}
```

Values for `looks` and `items` are strict — only `"up"` / `"down"`. Anything else is silently dropped server-side.

### Stored KV key + value

```
key:   vote:<lookbook_id>:<iso_ts>:<rand>
value: {
  "voter": "Sasha",
  "comment": "...",
  "looks": { ... },
  "items": { ... },
  "ts":  "2026-05-11T15:30:24.293Z",
  "ip":  "47.155.105.127",                    // CF-Connecting-IP at POST time
  "ua":  "Mozilla/5.0 ...",                   // first 200 chars
  "lookbook_id": "2026-05-11-la-dinners-weekend"
}
```

### GET `/api/votes` response

```jsonc
{
  "ok": true,
  "tally": {
    "count": 2,
    "looks":     { "look1": { "up": 2, "down": 0 }, "look2": { "up": 1, "down": 1 } },
    "items":     { "BM13139...": { "up": 2, "down": 0 }, ... },
    "voters":    [{ voter, ts, comment, looks, items }, ...]
  },
  "votes":  [<raw record>, ...]
}
```

## Setup — agent-side procedure

### Happy path — `scripts/deploy-lookbook.sh` does everything

```bash
# Once per Cloudflare account — create + save the KV namespace id:
CLOUDFLARE_ACCOUNT_ID=<account-id> wrangler kv namespace create LOOKBOOK_VOTES
# → returns id, e.g. "0e0b9122c04141f8b79b43d1081b3697"
# Save to profile.md as: lookbook_votes_kv_id: <id>

# Then every deploy:
bash scripts/deploy-lookbook.sh \
  ~/.buck-mason-stylist/runs/<lookbook_id>/deploy \
  buckmason-<project-slug> \
  --auto \
  --kv-id <id>      # or set $LOOKBOOK_VOTES_KV_ID once and omit
```

That's it. The script:

1. Copies `templates/voting/functions-api-vote.js` → `<deploy>/functions/api/vote.js`
2. Copies `templates/voting/functions-api-votes.js` → `<deploy>/functions/api/votes.js`
3. sed-renders `templates/voting/wrangler.toml.example` → `<deploy>/wrangler.toml` (filling in project, lookbook id, KV id)
4. Pulls Buck Mason's favicon set from `buckmason.com` (only if not already present)
5. Runs `scripts/inject-voting-ui.py` to inject the thumbs UI + favicon link tags
6. Deploys from inside the deploy dir so wrangler picks up `wrangler.toml` + `functions/`
7. After deploy: runs the existing `validate-lookbook.py --url` gates + a HEAD on `/api/votes` to confirm Functions are live

Opt out with `--no-voting` to deploy a read-only static lookbook (no `/api`, no form, no `wrangler.toml`).

### KV namespace creation gotcha

As of wrangler 4.86.0, `kv namespace create` returns *"Authentication error [code: 10000]"* without `CLOUDFLARE_ACCOUNT_ID` set, even when `wrangler whoami` is happy. `CF_ACCOUNT_ID` also works but is deprecated. Save the returned id once per account; `--kv-id` flag (or `$LOOKBOOK_VOTES_KV_ID` env, or `profile.md → lookbook_votes_kv_id`) keeps subsequent deploys one-line.

### Manual procedure (when not using the deploy wrapper)

If you're deploying to Cloudflare Pages by hand (e.g., wrangler from another tool), do the steps the wrapper would have done:

```bash
DEPLOY=<run_dir>/deploy
PROJECT=buckmason-<slug>
LOOKBOOK_ID=<run_dir's basename>
KV_ID=<your kv namespace id>

mkdir -p "$DEPLOY/functions/api"
cp templates/voting/functions-api-vote.js   "$DEPLOY/functions/api/vote.js"
cp templates/voting/functions-api-votes.js  "$DEPLOY/functions/api/votes.js"
sed -e "s|<PROJECT_NAME>|$PROJECT|g" \
    -e "s|<LOOKBOOK_ID>|$LOOKBOOK_ID|g" \
    -e "s|<KV_NAMESPACE_ID>|$KV_ID|g" \
    templates/voting/wrangler.toml.example > "$DEPLOY/wrangler.toml"

# Favicons (idempotent — skip if already present)
curl -sS -o "$DEPLOY/favicon-32.png"       "https://www.buckmason.com/favicon-32x32.png"
curl -sS -o "$DEPLOY/favicon-16.png"       "https://www.buckmason.com/icons/icon-48x48.png"
curl -sS -o "$DEPLOY/apple-touch-icon.png" "https://www.buckmason.com/icons/icon-192x192.png"
curl -sS -o "$DEPLOY/favicon.ico"          "https://www.buckmason.com/favicon.ico"

python3 scripts/inject-voting-ui.py --deploy-dir "$DEPLOY"

cd "$DEPLOY"
wrangler pages project create "$PROJECT" --production-branch main   # first time only
wrangler pages deploy . --project-name "$PROJECT" --branch main --commit-dirty=true
```

You'll see *"✨ Uploading Functions bundle"* in the output — that's the signal Pages picked up `functions/api/*.js`. If you don't see it, wrangler isn't reading the `functions/` directory; double-check that the cwd is the deploy dir at deploy time.

### Smoke-test the round-trip

```bash
URL=https://<PROJECT_NAME>.pages.dev

# POST a sample vote
curl -sS -X POST "$URL/api/vote" -H 'content-type: application/json' \
  -d '{"voter":"smoke","looks":{"look1":"up","look2":"down"},"items":{"<sku>":"up"},"comment":"test"}'

# GET tally
curl -sS "$URL/api/votes" | jq .tally
```

Then **delete the smoke-test record** so the partner's tally starts at 0:

```bash
CLOUDFLARE_ACCOUNT_ID=<account-id> \
  wrangler kv key delete --namespace-id=<KV_NAMESPACE_ID> \
  "vote:<LOOKBOOK_ID>:<ts>:<rand>" --remote
```

### Hand the URLs back to the customer

- **`https://<PROJECT_NAME>.pages.dev/`** — the lookbook + vote form. Share this with the partner.
- **`https://<PROJECT_NAME>.pages.dev/api/votes`** — the owner-only tally. Keep private.

There's no auth on the tally endpoint by design (URL is the shared secret). If the customer wants real privacy on the tally, add a `request.headers.get("authorization") === env.OWNER_TOKEN` check at the top of `votes.js` and a corresponding `OWNER_TOKEN` var in `wrangler.toml`.

## Security model — what's protected and what isn't

| Concern | Status | Notes |
|---|---|---|
| Anyone-with-the-URL can vote | **By design** | The page URL is the shared secret. For higher-stakes deploys, add a signed-link param. |
| Anyone-with-the-URL can read the tally | **By design, mitigated by URL secrecy** | `/api/votes` returns full vote history including IPs. Don't post the URL publicly; tighten with `OWNER_TOKEN` if needed. |
| Vote stuffing | **Soft mitigation** | The UI greys the submit button after one POST. Determined attackers can replay. KV records `CF-Connecting-IP` so duplicates are visible in the tally. For real anti-stuffing, add a rate-limit binding or a Turnstile widget. |
| Cross-lookbook leakage | **Mitigated** | Each KV key is prefixed with `vote:<lookbook_id>:`. `/api/votes` reads only its own prefix via the `LOOKBOOK_ID` env var. |
| PII / privacy | **Voter-chosen** | Free-text name + comment. Tell the customer what they're sharing. No emails, no auth tokens. |
| Cost | **Cloudflare free tier** | KV free tier: 100K reads, 1K writes, 1 GB storage per day. A lookbook campaign is <100 votes total. |

## Why Cloudflare-only

The lookbook already deploys to Cloudflare Pages (`references/hosting-options.md` → Cloudflare Pages is the default and most-tested transport). Reusing the same surface for voting:

- Avoids a second hosting provider (no Netlify Forms + Cloudflare static, no separate Vercel backend).
- Co-locates static + dynamic — same domain, same deploy command, same auth.
- KV is a 1-line storage primitive; D1/Postgres would be overkill for thumbs.

If a future hosting transport in `references/hosting-options.md` lands (Netlify, Vercel, surge), an analogous `templates/voting/<host>/` set can be added. Today only Cloudflare is wired.

## Files in this skill that implement this

- `scripts/inject-voting-ui.py` — post-build HTML injector (thumbs UI + favicon links). Idempotent.
- `templates/voting/functions-api-vote.js` — POST handler. Copy to `<deploy>/functions/api/vote.js`.
- `templates/voting/functions-api-votes.js` — GET tally handler. Copy to `<deploy>/functions/api/votes.js`.
- `templates/voting/wrangler.toml.example` — `name` + `LOOKBOOK_ID` var + KV binding. Copy to `<deploy>/wrangler.toml`.
- `references/voting.md` — this file.
