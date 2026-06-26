# Changelog — Claw Post skill (ClawHub)

All notable changes to the **Claw Post** OpenClaw skill bundle published on [ClawHub](https://clawhub.ai/) are documented here.

Users can generate a fresh `SKILL.md` from the dashboard at [clawpost.net](https://clawpost.net) (same template as ClawHub). The file uses **placeholder** API examples only — configure `CLAWPOST_API_KEY` in OpenClaw or your agent’s environment; copy the real key from the dashboard separately. Regenerate the committed bundle with `pnpm run export:clawhub-skill` from `web/` after editing `web/lib/clawpost-skill.ts`.

## [Unreleased]

## [1.5.1] - 2026-04-06

### Security

- **Dashboard skill download** no longer embeds the user’s real API key. All examples use `YOUR_CLAWPOST_API_KEY`; operators set `CLAWPOST_API_KEY` via env / secret store (aligns with OpenClaw trust review).

### Changed

- **Wording**: Softer, verifiable claims for social credential handling and extension scope; prerequisites clarify key is copied from the dashboard, not baked into the skill file.
- **Changelog intro** rephrased to remove misleading “key injection” language.

## [1.5.0] - 2026-04-06

### Fixed

- **ClawHub scanner–friendly frontmatter**: `metadata.openclaw` now includes `requires: { "env": ["CLAWPOST_API_KEY"] }` as a single-line JSON string. Removed the duplicate YAML `env:` block so registry summaries and SKILL.md stay consistent.

### Added

- **`clawhub-skill/SKILL.md`** in-repo (placeholder key only) for publishing without using the dashboard.
- **`web` script** `export:clawhub-skill` — regenerates `clawhub-skill/SKILL.md` from `generateClawPostSkill`.

## [1.4.1] - 2026-04-06

### Fixed
- Registry metadata sync: Re-published with explicit clawhub.json env declaration to resolve persistent "Required env vars: none" display in registry summary.
- Minor formatting cleanup in SKILL.md (removed remaining escaped backslashes for cleaner parsing).

### Notes
- The metadata mismatch is a known ClawHub registry behavior. This re-publish forces re-processing of clawhub.json.

## [1.4.0] - 2026-04-05

### Fixed

- **Registry metadata alignment (critical)**: `clawhub.json` now ships with `env.CLAWPOST_API_KEY` marked `required: true` and `primary: true`. When publishing, registry-level fields **must also be set** via the ClawHub upload form / CLI so the top-level listing shows "Required env vars: CLAWPOST_API_KEY" and "Primary credential: CLAWPOST_API_KEY". This resolves the remaining "metadata mismatch" caution flag.

### Changed

- **Expanded listing description**: tagline and description in `clawhub.json` now cover all four platforms, Facebook Groups automation, zero-credential security model, and pricing — replacing the narrow "Posts tweets to X" text.
- **"Why Claw Post" section rewritten** in SKILL.md: stronger differentiation (zero credential exposure, lower ban risk, Facebook Groups automation, simple setup vs OAuth-based tools). Replaces the previous generic version.
- **License** corrected to `MIT-0` in `clawhub.json` to match the ClawHub listing.
- **Tags** expanded: added `x`, `facebook-groups`, `automation`, `zero-credential` for better discovery.

## [1.3.0] - 2026-04-05

### Changed

- **Canonical API host is live on production**: `https://api.clawpost.net` is now the default everywhere the product ships (Firebase App Hosting env, Next.js fallbacks, extension and desktop defaults). SKILL.md examples and the API Base URL section match this endpoint.
- **Migration note**: the historical Cloud Run URL (`claw-post-api-ukpr57vsgq-uc.a.run.app`) may still resolve to the same service during transition; existing agents or old downloaded skills are not required to change immediately. Prefer `api.clawpost.net` for new integrations.

### Added

- **ClawHub / registry**: when publishing this version, set **Primary environment variable** to `CLAWPOST_API_KEY`, mark it **required**, and use a short description aligned with SKILL.md frontmatter (e.g. key from dashboard after pairing the extension).

### Notes (ecosystem, not in SKILL.md)

- Chrome extension **1.1.4+** includes `host_permissions` for both `https://api.clawpost.net/*` and the legacy `*.run.app` host so updated clients work during DNS and URL cutover.

## [1.2.0] - 2026-04-05

### Fixed

- **Metadata alignment**: added explicit `env` block in SKILL.md frontmatter declaring `CLAWPOST_API_KEY` as required with description, matching what the ClawHub registry expects. Resolves the "undeclared credential" caution flag.
- **Replaced hard-coded Cloud Run URL** (`claw-post-api-ukpr57vsgq-uc.a.run.app`) with the stable branded domain `api.clawpost.net`. Removed the "Do not use api.clawpost.net" line that contradicted user expectations.
- **Error table formatting**: `503 EXTENSION_NOT_PAIRED` row cleaned up (`503 / EXTENSION_NOT_PAIRED`).

### Added

- **"Why Claw Post" section** at the top of SKILL.md — highlights zero-credential design, human-like posting, multi-platform single endpoint, Facebook Groups power, and pricing.
- **"Security and privacy" section** — explicitly states: no social-platform creds leave the browser, extension scope is limited, API key is tenant-scoped & rotatable, HTTPS only, instruction-only skill (no executable code). Links to Terms of Service.
- Prerequisites now recommend setting `CLAWPOST_API_KEY` as an env var (not just pasting inline), with links to Chrome Web Store and Terms of Service.
- Auth section now advises reading from the environment variable at runtime.

## [1.1.0] - 2026-04-05

### Added

- **TikTok** posting guidance (video + caption via `mediaPaths`).
- **Facebook groups**: search (`POST /v1/groups/search`), join (`POST /v1/facebook/groups/join`), membership status (`POST /v1/facebook/groups/status`), and feed vs group posting with `platformPayload` (`groupUrl` / `groupId`).
- **Recommended workflow** section: discover → join → post, with reliability notes for search results.

### Changed

- Capability table and examples aligned with current API (X, LinkedIn, Facebook, TikTok).
- Error handling table expanded (`group_not_approved`, `challenge_required`, extension/tab errors).
- OpenClaw metadata: `primaryEnv: CLAWPOST_API_KEY` and API docs link.

## [1.0.0] - 2026-02-16

### Added

- Initial skill template: posting to **X** and **LinkedIn**, **media upload**, job polling, base URL and `clawpost-api-key` authentication, prerequisites for extension pairing and browser login.
