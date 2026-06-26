# Pre-Publish Security Checklist

Run this checklist before every release to ClawHub/npm.

## 1) Code and dependency safety

- [ ] `pnpm --filter launchthat-openclaw-connector lint`
- [ ] `pnpm --filter launchthat-openclaw-connector typecheck`
- [ ] `pnpm --filter launchthat-openclaw-connector build`
- [ ] `pnpm --filter launchthatbot test:openclaw:e2e` passes
- [ ] review dependency changes in lockfile for unexpected packages

## 2) Secrets and auth handling

- [ ] no docs/examples require passing secrets in CLI args
- [ ] env/file/prompt secret input paths still work
- [ ] ingest tokens are scoped and revocable
- [ ] signature mode documented and tested

## 3) Data minimization checks

- [ ] connector only sends canonical event fields
- [ ] no prompt/chat/env/file content included in payload by default
- [ ] metadata examples do not include sensitive values

## 4) API security checks

- [ ] rate limits active for ingest + heartbeat
- [ ] signature verification enabled in production (`OPENCLAW_REQUIRE_SIGNATURE=true`)
- [ ] timestamp skew window is enforced
- [ ] idempotency keys still dedupe replayed events

## 5) Local runtime security

- [ ] default queue path is inside user config directory
- [ ] queue file permissions are restrictive
- [ ] `--persist-queue=false` behavior verified for locked-down environments
- [ ] connector runs under a non-privileged user in deployment docs

## 6) Listing and trust artifacts

- [ ] `README.md` reflects current security behavior
- [ ] `SECURITY.md` includes disclosure process
- [ ] `SKILL.md` exists at repo root and imports cleanly in ClawHub
- [ ] `skill-examples.md` matches current connector behavior
- [ ] `CLAWHUB_LISTING_TEMPLATE.md` updated with latest guarantees
- [ ] release notes include security-relevant changes

## 7) Final publish gate

- [ ] run `pnpm --filter launchthat-openclaw-connector check:release`
- [ ] inspect `npm pack --dry-run` output for unintended files
- [ ] tag release with semver and changelog entry
