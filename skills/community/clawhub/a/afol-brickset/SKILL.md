---
name: brickset
description: Use the included Brickset CLI for LEGO set search/details, images, instructions, reviews, login/user hash, collection, wishlist, and notes with guarded account writes.
version: 1.0.0
---

# Brickset AFOL skill

Use this skill when a user asks for Brickset-backed LEGO set details, extra images, building instructions, community reviews, or explicit Brickset account workflows such as collection, wishlist, ratings, quantities, and personal notes.

Primary interface: `scripts/brickset`.

The skill is self-contained for archive distribution and wraps the Brickset API directly using checked-in references inside this skill directory:
- OpenAPI reference: `references/openapi/brickset.yaml`
- Public prompt guidance: `references/prompts/brickset-tools.txt`
- Private prompt guidance: `references/prompts/brickset-private-tools.txt`
- CLI source: `scripts/brickset_cli.py`

Do not scrape Brickset vendor docs or invent parameters when these checked-in references answer the endpoint shape. If the reference is insufficient, say exactly what is missing.

## Authentication

Required environment variable for all Brickset calls:

```bash
export BRICKSET_API_KEY=...
```

Optional environment variables:

```bash
export BRICKSET_USER_HASH=...      # preferred for private/account workflows
export BRICKSET_USERNAME=...       # only for `scripts/brickset login`
export BRICKSET_PASSWORD=...       # only for `scripts/brickset login`
export BRICKSET_BASE_URL=https://brickset.com/api/v3.asmx
```

Never print, commit, log, or paste real API keys, passwords, or user hashes. Prefer `BRICKSET_USER_HASH` over username/password once available.

Brickset auth placement matters:
- Every verified API operation is `POST`.
- The request body is `application/x-www-form-urlencoded`.
- `apiKey` is a form field, not JSON and not an HTTP bearer token.
- Public read calls still send `userHash=` as an empty form field unless a real `BRICKSET_USER_HASH` is intentionally used.
- Complex filters and collection mutations go in a `params` form field whose value is a JSON string.

The CLI handles that shape, which is the main reason to use it instead of ad-hoc curl.

## CLI quick reference

Run commands from this skill directory:

```bash
scripts/brickset --help
scripts/brickset sets --set-number 10270-1
scripts/brickset details --set-number 10270-1
scripts/brickset images --set-id 30142
scripts/brickset instructions --set-number 10270-1
scripts/brickset reviews --set-id 30142
scripts/brickset login
scripts/brickset collection
scripts/brickset wishlist
scripts/brickset notes
```

Private read commands (`collection`, `wishlist`, `notes`, or `sets --owned/--wanted`) require `BRICKSET_USER_HASH`.

Mutating commands are guarded. They do nothing unless passed `--yes`; use `--dry-run` first:

```bash
scripts/brickset collection-set --dry-run --set-id 30142 --own 1 --qty-owned 1
scripts/brickset collection-set --dry-run --set-id 30142 --want 1
scripts/brickset collection-set --dry-run --set-id 30142 --notes "placeholder note" --rating 5
```

## Safety rules

Read-only by default:
- `sets`
- `details`
- `images`
- `instructions`
- `reviews`
- `login` (authentication only; treat the returned hash as secret)
- `collection`
- `wishlist`
- `notes`

Mutating operations require explicit user confirmation in the current conversation before execution:
- `collection-set --own 1` or `--own 0`
- `collection-set --want 1` or `--want 0`
- `collection-set --qty-owned ...`
- `collection-set --notes ...`
- `collection-set --rating ...`
- `collection-set --params-json ...` whenever it changes account state

Stored credentials are not permission. Before any mutation, restate the exact Brickset account change, set identifier, quantity, wishlist/owned state, rating, and notes, then wait for explicit confirmation such as "yes, add it to Brickset" or "confirm rating update".

The CLI enforces this mechanically: mutating commands fail unless `--yes` is passed, and `--dry-run` prints the request shape with credentials redacted.

If the user asks to "add to my collection" without naming a provider and both Brickset/Rebrickable could apply, ask which provider to use before mutating anything.

## Endpoint coverage

- `POST /getSets` via `sets`, `details`, `collection`, and `wishlist`
- `POST /getAdditionalImages` via `images`
- `POST /getInstructions2` via `instructions`
- `POST /getReviews` via `reviews`
- `POST /login` via `login`
- `POST /setCollection` via `collection-set --yes`
- `POST /getUserNotes` via `notes`

Treat collection, wishlist, rating, quantity, and personal-note data as private. Summarize only what the user needs.

## Brickset setID rule

Brickset set numbers and internal set IDs are not interchangeable.

Use `details` or `sets` first when the user gives a public set number and you need a Brickset internal `setID` for images, reviews, or account writes:

```bash
scripts/brickset details --set-number 10270-1
```

Then use the returned `setID`:

```bash
scripts/brickset images --set-id "$SET_ID"
scripts/brickset reviews --set-id "$SET_ID"
scripts/brickset collection-set --dry-run --set-id "$SET_ID" --own 1
```

`instructions` is the exception in this checked-in OpenAPI reference: it uses the public set number directly:

```bash
scripts/brickset instructions --set-number 10270-1
```

Do not convert form calls to JSON requests. That is the classic foot-gun here.

## Public read workflows

### Search/details

```bash
scripts/brickset sets --set-number 10270-1
scripts/brickset sets --query "Galaxy Explorer"
scripts/brickset sets --params-json '{"theme":"Space","year":2022}'
```

Use `details --set-number` for the common exact-set lookup. Responses include Brickset metadata such as theme, subtheme, pieces, minifigs, release status, ratings, review counts, images, barcodes, dimensions, LEGO.com pricing, and the internal `setID` when available.

### Images

Resolve `setID` with `details`, then:

```bash
scripts/brickset images --set-id "$SET_ID"
```

Use for extra photos, alternate angles, box backs, detail shots, or images beyond the main thumbnail.

### Instructions

```bash
scripts/brickset instructions --set-number 10270-1
```

Return PDF links and explain instruction codes when helpful: BI numbers, version numbers, and booklet numbers.

### Reviews and opinions

When the user asks for opinions, community feedback, ratings, whether a set is good, or whether it is worth buying, use Brickset reviews before pricing tools.

Resolve `setID` with `details`, then:

```bash
scripts/brickset reviews --set-id "$SET_ID"
```

Summarize real review text and star ratings. Do not invent sentiment if there are no reviews.

## Private read workflows

### Obtain a user hash

Only use `login` when private workflows require it and the user has explicitly provided or approved credential use through environment variables:

```bash
scripts/brickset login
```

The response contains `hash`. Store it as `BRICKSET_USER_HASH` in approved secret storage if persistence is requested. Never commit it or paste it in a PR/comment.

### Collection and wishlist reads

```bash
scripts/brickset collection
scripts/brickset wishlist
scripts/brickset sets --owned 1
scripts/brickset sets --wanted 1
```

### User notes

```bash
scripts/brickset notes
```

Use for personal set notes and note-backed collection context.

## Mutating workflows

Do not run these with `--yes` until the user explicitly confirms the exact action.

### Add to owned collection

After explicit intent and `setID` resolution:

```bash
scripts/brickset collection-set --yes --set-id "$SET_ID" --own 1 --qty-owned 1
```

### Remove from owned collection

```bash
scripts/brickset collection-set --yes --set-id "$SET_ID" --own 0
```

### Add to wishlist

```bash
scripts/brickset collection-set --yes --set-id "$SET_ID" --want 1
```

### Remove from wishlist

```bash
scripts/brickset collection-set --yes --set-id "$SET_ID" --want 0
```

### Update quantity, notes, or rating

```bash
scripts/brickset collection-set --yes --set-id "$SET_ID" --qty-owned 2 --notes "placeholder note" --rating 5
```

Keep notes under Brickset's documented limit from the verified spec guidance: 1000 characters. Rating is 1-5.

## Live smoke checks

Local, no-network checks:

```bash
python3 -m py_compile scripts/brickset_cli.py
scripts/brickset collection-set --dry-run --set-id 30142 --own 1 --qty-owned 1
```

Read-only live smoke check, only when `BRICKSET_API_KEY` is configured:

```bash
scripts/brickset details --set-number 10270-1
```

If `BRICKSET_USER_HASH` is configured, private read smoke checks are allowed:

```bash
scripts/brickset notes
```

Summarize only response shape/counts/status. Do not paste private notes, collection contents, credentials, hashes, or user profile data into logs, PRs, task summaries, or chat.

Never use `collection-set --yes` as a smoke test unless the user explicitly asks for that real Brickset account mutation.

## Response guidance

- Mention Brickset as the source when returning review, instruction, image, or collection data.
- For opinion questions, cite/summarize Brickset reviews first before switching to price/value analysis.
- For images and instructions, return direct URLs when the API provides them.
- For collection/wishlist writes, report exactly what service was changed: Brickset collection or Brickset wishlist.
- If an API response has `status: error`, surface the message and stop rather than pretending the operation succeeded.
