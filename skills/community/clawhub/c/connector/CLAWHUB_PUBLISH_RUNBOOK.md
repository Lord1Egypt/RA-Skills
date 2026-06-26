# ClawHub Publish Runbook

This runbook assumes your package is published to npm and listed in ClawHub.

## 0) Monorepo -> Dedicated Repo Sync

This package is developed in this monorepo under:

- `packages/launchthat-openclaw-connector`

And mirrored to:

- `https://github.com/launchthatbot/connect.git`

### Automated sync (recommended)

- Workflow: `.github/workflows/sync-skill-mirrors.yml`
- Triggered on `main` pushes that touch the package path.
- Requires repository secret:
  - `LAUNCHTHATBOT_REPO_PAT` (PAT with push access to `launchthatbot/connect`, `launchthatbot/import`, `launchthatbot/convex`, and `launchthatbot/git-ops`)

### Source of truth and writer policy

- **Source of truth repo for connector code is this monorepo path**: `packages/launchthat-openclaw-connector`.
- The `launchthatbot/connect` repository is a **publish mirror** and should be treated as read-only for feature development.
- Avoid direct commits to `launchthatbot/connect` to prevent multi-writer drift.
- If an emergency hotfix is applied in `launchthatbot/connect`, immediately port it back into this monorepo package and re-run sync.

### One-time bootstrap commands (local)

```bash
git remote add connector git@github.com:launchthatbot/connect.git
git subtree split --prefix=packages/launchthat-openclaw-connector -b split/openclaw-connector
git push connector split/openclaw-connector:main
```

### Manual sync fallback (local)

```bash
SPLIT_SHA="$(git subtree split --prefix=packages/launchthat-openclaw-connector main)"
git push connector "${SPLIT_SHA}:main"
```

## 1) Pre-flight

- Ensure `README.md`, `SECURITY.md`, and `CLAWHUB_LISTING_TEMPLATE.md` are current.
- Run:

```bash
pnpm --filter launchthat-openclaw-connector check:release
pnpm --filter launchthatbot test:openclaw:e2e
```

- Validate package contents:

```bash
cd packages/launchthat-openclaw-connector
npm pack --dry-run
```

## 2) Publish package

From repo root:

```bash
pnpm --filter launchthat-openclaw-connector build
pnpm --filter launchthat-openclaw-connector exec npm publish --access public
```

## 3) Create/Update ClawHub listing

- Open `https://clawhub.ai/` publisher dashboard.
- Copy content from `CLAWHUB_LISTING_TEMPLATE.md`.
- Fill platform-specific fields:
  - package name/version
  - category/tags
  - support contact
  - changelog/release notes
  - pricing plan metadata (if used)

## 4) Security metadata to include

- Outbound-only network behavior
- Data minimization guarantees
- Secret handling methods (env/file/prompt)
- Signature verification support
- Incident reporting channel from `SECURITY.md`

## 5) Post-publish verification

- Install package in a clean OpenClaw environment.
- Run auth-link flow and confirm:
  - heartbeat accepted
  - events ingest accepted
  - replay endpoint returns events
- Verify dashboard reflects connected instance in LaunchThatBot.

## 6) Rollback plan

- If release has an issue:
  - deprecate affected npm version
  - publish patched version
  - update ClawHub listing notes with affected version range and fix
