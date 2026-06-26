# Changelog

## 1.6.3 - 2026-06-05

- Keep generated Skill Card metadata out of source because ClawHub strips publisher-supplied `skill-card.md` files and generates cards server-side.

## 1.6.2 - 2026-06-05

- Publish and scan the security/admin update through ClawHub 0.19.1.

## 1.6.1 - 2026-06-05

- Document safer Bluesky login flow that uses the hidden app-password prompt.
- Hide the legacy `--password` login argument from help and warn when it is used.
- Add opt-in mutation confirmations with `BSKY_CONFIRM_MUTATIONS=1`.
- Update agent guidance to verify public/account-changing actions before running them.
- Fix stale README guidance for OpenClaw install commands and handle syntax.
- Add missing changelog and MIT-0 license files.

## 1.6.0

- Add `create-thread` / `ct` for multi-post threads.
- Add thread dry-run coverage and CI-compatible test runner fallback.
