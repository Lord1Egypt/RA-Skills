# ClawSite

Agent-first static website hosting microservice, modeled after [ClawMail](https://github.com/MixerBox/clawmail).

## Status (2026-04-29)

✅ **v1 deployed to dev + prod, smoke-tested live, partner mode confirmed working end-to-end.**

| Env | API | Site URL pattern | Partner secret on |
|---|---|---|---|
| Dev / staging | `https://api.dev.clawsite.ai` | `<slug>.dev.clawsite.ai` | `claws-instance-controller-staging` Lambda env (`PARTNER_CLAWSITE_SECRET`) |
| Prod | `https://api.clawsite.ai` | `<slug>.clawsite.ai` | `claws-instance-controller` Lambda env (`PARTNER_CLAWSITE_SECRET`) |

CloudFront distribution IDs: dev `E3VZOWBAWTVYBK`, prod `ESXYWGNPX39MP`.

Both envs live in AWS account `974718210214` (us-east-1), same account as ClawMail. Route53 zone `clawsite.ai` is shared between dev/prod.

**Email-OTP path is implemented but inert until MBID provisions a `serverKey` for the `clawsite-dev` / `clawsite-prod` apps in MBID `TABLE_APP`.** Once that's done, set `MBID_SERVER_KEY` on the api Lambda env (Terraform var: `mbid_server_key`) and email registration unlocks. Partner mode (the only path ZenClaw uses today) doesn't depend on this.

## Reference repos

- `~/Work/MixerBox/clawmail/` — the structural model. When in doubt about a pattern (`globalThis.__routes`, Vitest mocks, Terraform), look at how ClawMail does it.
- `~/Work/MixerBox/zenclaw/` — the first partner. Plan 2 (`configure-clawsite` controller action + sandbox env injection + `clawsite-ai` skill install) lands there.
- `~/Work/MixerBox/microservice/microservice/kubernetes/livapp/apps/mb-id/` — MBID service we delegate email verification to.

## Quick reference

- **Language:** TypeScript (Node.js 20, ES2022 modules)
- **Test:** `npx vitest run`
- **Typecheck:** `npx tsc --noEmit`
- **Build:** `node build.mjs` (outputs `.mjs` to `dist/`)
- **Deploy** (Terraform: `terraform/` dir, two workspaces `dev` + `prod`):
  ```bash
  # build + zip Lambda artifact (load-bearing filename: api.zip)
  node build.mjs
  cd dist && zip -j api.zip api.mjs api.mjs.map

  # dev — uses claws-instance-controller-staging partner secret
  cd ../terraform && terraform workspace select dev && terraform apply \
    -var "site_domain=dev.clawsite.ai" \
    -var "api_domain=api.dev.clawsite.ai" \
    -var "environment=staging" \
    -var "partner_secret=$(aws lambda get-function-configuration \
      --function-name claws-instance-controller-staging \
      --query 'Environment.Variables.PARTNER_CLAWSITE_SECRET' --output text)"

  # prod — uses claws-instance-controller partner secret
  terraform workspace select prod && terraform apply \
    -var "site_domain=clawsite.ai" \
    -var "api_domain=api.clawsite.ai" \
    -var "environment=prod" \
    -var "mbid_api_base_url=https://api.id.mixerbox.com" \
    -var "partner_secret=$(aws lambda get-function-configuration \
      --function-name claws-instance-controller \
      --query 'Environment.Variables.PARTNER_CLAWSITE_SECRET' --output text)"
  ```

  The `partner_secret` flow: ZenClaw's controller Lambda holds `PARTNER_CLAWSITE_SECRET` as an env var (set once via `aws lambda update-function-configuration`); ClawSite's Terraform reads it at apply time so the two sides cannot drift. Same pattern as ClawMail's `PARTNER_CLAWMAIL_SECRET`.
- **Hot-patch Lambda code only** (when only src/ changed, no infra): `node build.mjs && cd dist && zip -j api.zip api.mjs api.mjs.map && for fn in clawsite-staging-api clawsite-api; do aws lambda update-function-code --function-name "$fn" --zip-file fileb://api.zip; done`
- **Publish skill to ClawHub:** `clawhub publish .` (run from repo root; `SKILL.md` is the manifest)
- **Spec:** [`docs/superpowers/specs/2026-04-15-clawsite-design.md`](docs/superpowers/specs/2026-04-15-clawsite-design.md)

### Resource naming convention

`local.prefix` in `terraform/main.tf` derives the AWS resource name prefix from `var.environment`:

- `var.environment = "prod"` → `local.prefix = "clawsite"` → `clawsite-api`, `clawsite-manifest`, `clawsite-sites-<account>`
- anything else (typically `staging` for dev workspace) → `local.prefix = "clawsite-${env}"` → `clawsite-staging-api`, `clawsite-staging-manifest`, `clawsite-staging-sites-<account>`

The dev workspace uses `environment=staging` to match ZenClaw's `claws-instance-controller-staging` controller naming. **`-var environment=...` is required on every apply** (no default — pass `prod` for prod, `staging` for dev).

## Architecture (single Lambda)

| Lambda | Trigger | Purpose |
|---|---|---|
| `api` | API Gateway HTTP API (`ANY /{proxy+}`) | All REST endpoints — register, sites CRUD, deploy, purge-cache |

There used to be a `cleanup` Lambda intended for daily housekeeping, but it had no EventBridge trigger and nothing to clean (quota counters self-expire via DDB TTL; slug tombstones are by-design permanent). Removed 2026-04-30. If real housekeeping logic emerges later, re-add the Lambda + EventBridge rule together.

Storage:
- **DynamoDB** single table `clawsite[-staging]-manifest` — accounts, API keys, sites, slug reservations, quota counters. GSIs: `byApiKeyHash`, `byMbid`.
- **S3** `clawsite[-staging]-sites-<account-id>` — static site files, partitioned by slug prefix.
- **CloudFront** distribution + CloudFront Function for `<slug>` host → S3 prefix routing.

## MBID integration (email OTP)

Email OTP registration delegates to **MBID** (`api.id.{dev.,}mixerbox.com`). ClawSite calls:
- `POST /api/request_email_verify` → returns a `verifyToken` JWT we pass back as our `challengeId`
- `PUT /api/verify_email` → returns `user.uuid` which becomes our `mbidUserId`

Net effect: **every ClawSite account is keyed by an MBID UUID**. Partner-mode registration (ZenClaw) and email-OTP registration both deduplicate via the same `byMbid` GSI — one user, one ClawSite account, regardless of how they arrived.

To activate email-OTP path:
1. Register `clawsite-dev` and `clawsite-prod` as apps in MBID's `TABLE_APP` to obtain `serverKey` values
2. Update Lambda env vars: `MBID_SERVER_KEY` (the serverKey for that env) and `MBID_API_BASE_URL` (already set per env)

Email-OTP code is in place with mocked tests; real serverKey just unlocks the production path.

### Removed from original spec (no longer relevant)

The spec originally called for self-hosted SES + SQS + a `deliver-email` Lambda. The MBID rework dropped all of that:

- ❌ No SES domain identity / DKIM / SPF / DMARC
- ❌ No SQS verification queue / DLQ
- ❌ No `deliver-email` Lambda (architecture went 3 → 2 Lambdas)
- ❌ No DynamoDB `challenge#*` items (MBID's own `verifyToken` JWT is stateless on our side)

If re-reading the spec, treat any reference to those items as historical.

## Branching

- `main` — what's deployed to prod (auto-deploy is manual via `terraform apply` on prod workspace)
- `develop` — staging-equivalent; merges back to `main` after smoke tests
- Bug fixes / features land via `fix/*` or `feat/*` branches → develop → main

## Project structure

```
src/
├── handlers/
│   ├── api.ts              # API Gateway entry; regex route table on globalThis.__routes
│   └── routes/             # one file per endpoint group, registered via side-effect imports
│       ├── register.ts
│       ├── sites.ts
│       ├── deploy.ts
│       └── purge.ts
├── lib/                    # AWS-thin utilities
│   ├── auth.ts             # SHA-256 + timing-safe apiKey verify + partner secret check
│   ├── cloudfront.ts       # invalidatePrefix() helper
│   ├── dynamo.ts           # DDB DocumentClient + PK/SK builders + table/GSI names + hourWindow()
│   ├── errors.ts           # AppError class, JSON response helpers, CORS headers
│   ├── id.ts               # acc_, site_, csk_live_* ID generators
│   ├── mbid.ts             # MBID thin client (requestEmailVerify, verifyEmail)
│   ├── quota.ts            # Hourly window counters with atomic increments
│   ├── s3.ts               # S3 client + bucket name
│   ├── slug.ts             # Random adjective-animal-NN slug + fallback hex slug
│   ├── validate.ts         # File extension whitelist, size limits, QUOTA constants
│   └── zip.ts              # Streaming zip extraction with validation
└── middleware/
    └── auth.ts             # Bearer apiKey → AuthContext via byApiKeyHash GSI
build.mjs                   # esbuild bundler (entry: api.ts, cleanup.ts)
terraform/                  # AWS infra; workspaces dev + prod
tests/                      # Vitest tree mirrors src/
docs/superpowers/{specs,plans}/  # Design specs and execution plans
```

## Key patterns

### Route registration
Routes register via side-effect imports in `src/handlers/api.ts`. Each route file calls `route(method, path, handler)` at module level. Routes are stored in `globalThis.__routes` to avoid ESM circular-import TDZ issues — same pattern as ClawMail.

Public (no-auth) routes: `route('POST', '/path', handler, { public: true })` — currently only `/v1/register`.

The `route()` function defensively initializes `globalThis.__routes` because esbuild bundling can place dependency module top-level code before the entry's initialization. See comment in `api.ts` for context.

### Auth
`Authorization: Bearer <token>`:
- `csk_live_*` → SHA-256 hash → DynamoDB GSI lookup `byApiKeyHash` (per-account API key)
- Partner secret → on `POST /v1/register` only, matched in handler before falling through to email-mode body shapes

### Single-table DynamoDB
Active PK/SK prefixes (live in code):
- `account#<id>` + `meta` / `apikey#<hash>` / `site#<id>` / `quota#<action>#<window>`
- `slug#<slug>` + `meta` (global slug reservation; status flips to `tombstoned` on site delete and stays forever — prevents URL takeover)

`account#<id>` + `meta` includes a `sitesCount` numeric field, atomically updated by site CRUD operations to enforce the per-account site quota race-free (see `src/handlers/routes/sites.ts`).

GSIs: `byApiKeyHash` (apiKey lookup → accountId), `byMbid` (MBID UUID → accountId for cross-flow idempotency).

### Quota enforcement
- Per-account site count: atomic via `sitesCount` counter on account meta + conditional update inside the site-creation TransactWrite. Can never race.
- Per-hour deploy / purge frequency: hourly window counter in `src/lib/quota.ts`, gated on a single conditional `ADD count :one` inside the action handler.

### ClawHub publishing
`SKILL.md` at the repo root is the agent-facing API doc + ClawHub manifest. Published via `clawhub publish .`. Skill slug: `clawsite-ai`. Once Plan 2 lands, ZenClaw sandboxes will `clawhub install clawsite-ai` during provisioning.

### Testing
Vitest with `vi.mock('@lib/dynamo')`. Route handler tests also mock `@handlers/api` to export a no-op `route` function, avoiding circular imports. Path aliases live in both `tsconfig.json` and `vitest.config.ts` — keep them in sync.

## Known gaps / follow-ups

- **Plan 2 (ZenClaw integration)** is in flight in `~/Work/MixerBox/zenclaw` on `feat/configure-clawsite-action`. Adds the `configure-clawsite` controller action + manifest fields. Sandbox-side env injection + `clawhub install clawsite-ai` are still TODO.
