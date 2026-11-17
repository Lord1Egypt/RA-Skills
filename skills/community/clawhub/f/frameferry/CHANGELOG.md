# Changelog

## 0.2.1 - 2026-09-06

- Identify the pagination sentinel by observing which element the provider's own `IntersectionObserver` watches, instead of assuming the last rendered `.post-card`.
- Fix stalled pagination: a carousel renders its slides as sibling `.post-card`s after the post's top-level card, so centering the final DOM card parked the real sentinel outside the observer's 200px `rootMargin` and growth stopped.
- Retain the markup heuristics as fail-closed fallbacks for pages where the probe was not installed: first card of the trailing same-`data-id` run, then the last card.
- Report `sentinelIndex`, `sentinelId`, and `sentinelSource` in the returned pagination state.
- Correct the documented pagination contract to the observed-sentinel mechanism and its fallback order.
- Correct the `dateParsed` documentation: a provider string with no explicit year, or one that does not parse, is preserved verbatim rather than converted to a timestamp.

## 0.2.0 - 2026-09-05

- Add category-aware archive selection for posts, reels, stories, and highlights.
- Preserve the full baseline regression inventory and add export/privacy/bootstrap coverage for the new content-selection and ZIP paths.
- Keep post completeness honest: unknown post denominators are `ACTION_REQUIRED`, advertised shortfalls stay `PARTIAL`, and stale failed-overlap entries are retried/cleared correctly.
- Add safe local ZIP export with JSON inventories, receipt sidecars, byte re-verification, stale-`.part` handling, checksums, atomic finalize, and ZIP32-safe limits.
- Document installed-skill bootstrap and local CLI-path usage without assuming a global `frameferry` binary.
- Optional OpenClaw orchestration guide remains documentation-only; the download runtime still has no LLM dependency.

## 0.1.0 - 2026-09-05

- Initial public skill and CLI.
- Bounded full archive and sync modes.
- Durable lock, manifest, status, and SHA-256 receipt model.
- Conservative InstaCognito selector contract and provider URL validation.
- Offline node:test coverage and bwrap sandbox launcher.
