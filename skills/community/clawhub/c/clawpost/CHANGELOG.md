# Changelog — Claw Post skill (ClawHub)

All notable changes to the **Claw Post** OpenClaw skill bundle published on [ClawHub](https://clawhub.ai/) are documented here.

Users can generate a fresh `SKILL.md` from the dashboard at [clawpost.net](https://clawpost.net) (same template as ClawHub). The file uses **placeholder** API examples only — configure `CLAWPOST_API_KEY` in OpenClaw or your agent’s environment; copy the real key from the dashboard separately. Regenerate the committed bundle with `pnpm run export:clawhub-skill` from `web/` after editing `web/lib/clawpost-skill.ts`.

## [Unreleased]

## [2.3.0] - 2026-11-14

### Added

- **X replies, Facebook comments/threaded replies, LinkedIn comments** documented in the skill capability table and REST sections (`POST /v1/x/reply`, `/v1/facebook/comment`, `/v1/linkedin/comment`). Facebook `comment_id=` URLs create threaded replies with no top-level fallback.
- **Notifications loop** documented: `check_notifications` → `list_replies` → `reply_to_comment` (or platform tool) → `mark_reply_read`.
- Full **17 MCP tools** listed for OAuth clients.

### Changed

- **Join policy**: agent may join a Facebook group when the user asks (`join_facebook_group`, 5/day); does not auto-join on its own.
- **Pricing copy**: plans differ only by monthly post count; every plan covers every platform and action; Free = 25 posts/month.
- Removed em dashes from public skill copy. Short video guides are built into setup (no tutorial promise).

### Notes

- **ClawHub republish required**: human must republish after merging so the registry listing updates.

## [2.2.1] - 2026-08-31

### Added

- **Bird migration guidance** — skill frontmatter description now mentions bird / steipete bird CLI skill 404 as a trigger. "Why Claw Post" section includes a callout for users coming from the defunct Bird CLI (`steipete/bird` repo, `brew install steipete/tap/bird`, ClawHub `bird` card all return 404). Points users to the full slug `@daydreamnationtechlabs/clawpost` and warns against short-name installs.
- **Article: Bird skill 404** — new page at `/articles/bird-skill-404` explains the Bird CLI deprecation, clarifies that Birdclaw is an archive (not a posting skill), and lists alternatives (Birdclaw for archives, xurl for official API, Claw Post for browser-based posting).

### Notes

- **ClawHub republish required**: this agent cannot publish to ClawHub. A human must republish the skill after merging to update the registry listing.

## [2.1.0] - 2026-08-27

### Added

- **Reddit comments (browser actions)** — agents can reply on a specific Reddit post or comment via `POST /v1/reddit/comment` with `text` + `targetUrl` (must include `/comments/`). Runs in the user’s logged-in Chrome through the paired extension; no Reddit API key. Poll `GET /v1/jobs/:id`; on success `postUrl` is the live comment permalink.
- **MCP tool `create_reddit_comment`** — same capability for OAuth MCP clients (`https://mcp.clawpost.net/mcp`).
- **ClawHub listing** — tagline, description, and tags now include Reddit comments / browser actions.

### Changed

- **Skill frontmatter description**, capabilities table, MCP tools list, and prerequisites now cover Reddit (`reddit.com` login).

## [2.0.0] - 2026-05-05

### Added

- **MCP server** — MCP-compatible agents (Claude, GPT, and others) can now connect directly at `https://mcp.clawpost.net/mcp` via OAuth 2.0. No API key required; the agent authorises once through the Claw Post OAuth flow and receives scoped access tokens. Supported tools: `list_platforms`, `create_post`, `get_upload_url`, `get_post_status`, `get_account_status`.
- **`get_upload_url` MCP tool** — agents call this tool to get a signed PUT URL for direct-to-storage file uploads. `contentType` is optional and inferred automatically from the filename extension. The response includes `putHeaders` that agents must use verbatim for the PUT request (the signed URL rejects requests with wrong headers). Validates the file type against the target platform before uploading.
- **`postUrl` reliably returned on success** — `GET /v1/jobs/:id` and the MCP `get_post_status` tool now return `postUrl` containing the live URL of the published post once the job succeeds. Previously this was logged and discarded; it is now persisted on the job record.
- **`get_account_status` MCP tool** — agents can check if the user has a paired extension before attempting to post, and surface a pairing URL if not.

### Changed

- **All platforms now use remote workflow mode.** X, LinkedIn, Facebook, TikTok, and Instagram all execute via the declarative remote workflow executor. This enables server-side workflow fixes without client releases and unlocks `postUrl` extraction for all platforms.
- **`contentType` is now optional on `POST /v1/media/upload-url`.** The API infers the MIME type from the filename extension automatically. Passing a `contentType` that conflicts with the filename extension returns a `400` error. A new optional `platform` field validates the file type against the platform's supported formats before the upload URL is issued.
- **X success detection fixed.** The workflow now waits up to 45 seconds for X to finish processing uploaded media before clicking Post (instead of a fixed 5-second delay). Success is only declared when a tweet URL is extracted from the confirmation toast — eliminating false-positive `succeeded` statuses for failed posts.

## [1.6.0] - 2026-04-14

### Added

- **Instagram posting support.** `platform: "instagram"` now publishes to the Instagram feed via the extension's remote workflow executor. Requires at least one image or video in `mediaPaths`.
- **TikTok** promoted from preview to GA, including large-file video uploads via the two-step signed URL flow.
- **Large media upload endpoint** (`POST /v1/media/upload-url`) documented in the capabilities table — returns a signed GCS `uploadUrl` for files that exceed the proxy's direct-upload limit.

### Changed

- **Capabilities table** and platform prose list all five supported platforms (X, LinkedIn, Facebook, TikTok, Instagram).
- **Prerequisites** mention `instagram.com` as a supported login domain.

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
