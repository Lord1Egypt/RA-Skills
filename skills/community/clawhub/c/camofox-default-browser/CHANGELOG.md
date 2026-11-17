# Changelog

All notable changes to this Camoufox browser automation skill are documented here. This follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.1] - 2026-07-30

### Security
- Updated security guidelines to be more compliance-focused for enterprise use cases
- Added explicit warnings about cookie import risks — session cookies treated as bearer tokens with full account access
- Clarified authorized-use policy: automation only on services where user has explicit permission
- Added legal compliance note referencing computer fraud laws and Terms of Service requirements
- Improved privacy guidance for accessing accounts or data the user does not own

### Changed
- Rewrote resource management section with clearer idle/active memory footprint metrics
- Restructured environment variables documentation for better discoverability
- Updated system dependency descriptions with specific Firefox rendering context per package

---

## [1.1.0] - 2026-07-22

### Added
- Cookie import functionality via `camofox_import_cookies` — import Netscape-format cookie files for authenticated browsing sessions
- Support for `CAMOFOX_API_KEY` environment variable to gate cookie operations behind an API key
- Crash telemetry opt-out via `CAMOFOX_CRASH_REPORT_ENABLED=false` environment variable
- Comprehensive system dependencies table with purpose explanations for each shared library
- Node.js minimum and recommended version specifications in requirements section

### Security
- Initial security warning block added for cookie handling best practices
- Authorized use guidelines written into skill documentation
- Privacy notice for unauthorized account access prevention

### Fixed
- Resolved stale reference links in dependency documentation that pointed to outdated package names
- Corrected port binding clarification — server now explicitly documents `0.0.0.0` default bind address

---

## [1.0.1] - 2026-07-18

### Fixed
- Fixed snapshot description text claiming "95% smaller" — corrected to accurate "~90% smaller than raw HTML" comparison
- Resolved ambiguity in tab cleanup ordering: tabs now close cleanly without leaving orphaned browser processes
- Fixed memory scaling documentation: updated per-tab overhead from "+~80 MB" to correct "+~50 MB per additional tab"

### Changed
- Simplified workflow example from 6 steps to 4 core steps for easier mental model
- Removed redundant setup instructions already covered in SKILL.md getting-started section

---

## [1.0.0] - 2026-07-15

### Added
- Initial ClawHub release of the Camoufox default browser skill
- Core tab management tools: `camofox_create_tab`, `camofox_close_tab`, `camofox_list_tabs`
- Element interaction primitives: `camofox_click`, `camofox_type` with enter-key submission support
- Page navigation tool with search macro support for Google, YouTube, Amazon, Reddit, LinkedIn, Wikipedia, Twitter/X, Yelp, Spotify, Instagram, TikTok, Twitch, and Netflix
- Accessibility tree snapshot via `camofox_snapshot` — provides stable element refs (e1, e2, e3) plus optional base64 screenshot
- JavaScript execution via `camofox_evaluate` for page context scripts
- Screenshot capture via `camofox_screenshot`
- Scroll navigation via `camofox_scroll` with direction control (up/down/left/right) and configurable pixel amounts
- Health check endpoint at GET `/health` on localhost:9377
- Lazy browser engine launch — no resource wasted until first tab request
- Configurable idle shutdown timeout (default 5 minutes)

### Architecture
- Native C++ Camoufox server running on localhost HTTP API (port 9377 by default)
- Session isolation: separate cookies and storage per user
- Browser fingerprint managed at C++ level: navigator.hardwareConcurrency, WebGL renderer, AudioContext, screen geometry, WebRTC
- Base engine: Mozilla Firefox fork aligned with ESR versioning
- Cache-aware binary download: Camoufox distributed binary downloaded once to `/root/.cache/camoufox/` and reused across sessions
- Force re-download support by deleting cache directory

### Breaking Changes
- N/A — this is the initial stable release with no prior versions to conflict with

---

## [0.9.0-alpha] - 2026-07-08

### Added
- Prototyped basic tab creation and closure cycle
- Experimental snapshot integration using accessibility tree serialization
- Local HTTP server skeleton on port 9377 with health ping capability
- Manual verification walkthrough for anti-detection behavior on Cloudflare-protected sites

### Known Issues
- Tab references could become stale after page navigation — resolved in 1.0.0
- No crash telemetry yet — all crashes produced unstructured logs
- Dependency installation had manual steps that were error-prone on minimal Docker images

---

## [0.1.0-pre] - 2026-06-28

### Added
- Proof-of-concept `camofox_create_tab` wrapper around native Camoufox binary
- Basic click action via CSS selector targeting
- First snapshot output proving accessibility tree extraction works
- Workspace skill scaffold with SKILL.md structure and metadata fields
