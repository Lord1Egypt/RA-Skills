# Changelog

All notable changes to this project are documented in this file.

## 1.0.3 - 2026-11-02

### Fixed

- Long-running MCP sessions now recover from an explicit Bring HTTP 401 by reauthenticating with the configured account. Previously, restarting the MCP server was necessary after its access token became invalid.
- Concurrent requests and late responses from an older authentication generation share a single renewal instead of triggering a login storm. Successful renewal must retain the same account identity.
- Read requests (GET/HEAD) are retried at most once after renewal. Mutating requests are never automatically replayed, avoiding duplicate or uncertain shopping-list changes.

### Security

- Validate authentication headers before adopting a token and sanitize malformed-header failures without exposing credentials or tokens.
- Keep public asset requests unauthenticated and reject redirects for authenticated API requests. Network errors, HTTP 5xx responses, and failed renewal do not trigger retry loops.

### Verification

- Added deterministic authentication-recovery regressions covering concurrent renewal, bounded retries, identity changes, malformed headers, public-request isolation, and mutation non-replay.

## 1.0.2 - 2026-08-29

### Changed

- Repositioned the package and Official MCP Registry descriptions around the photo-first workflow.
- Updated public skill metadata to the same release version.

## 1.0.1 - 2026-08-29

### Added

- Official MCP Registry metadata under `io.github.schnueck/bring-photo-mcp`.
- Transparent AI-assisted development and verification disclosure in both READMEs.

### Changed

- Public author metadata standardized as `Thomas Schnuecker`.

## 1.0.0 - 2026-08-29

### Added

- Public npm package metadata, executable entrypoint, MIT license, security policy, and safe configuration template.
- Public thin `SKILL.md` for MCP-only deterministic Bring operations, including photo-led classification, 30-code-point specifications, duplicate policy, verified moves, and per-list partial results.
- Generic stdio, Hermes, and OpenClaw client configuration examples.
- Explicit one-release migration and rollback guidance retaining `bring-safe`.

### Security

- Published package is allowlisted to distributable runtime and documentation artifacts; no credentials, list identifiers, product photos, or local operational data are included.
