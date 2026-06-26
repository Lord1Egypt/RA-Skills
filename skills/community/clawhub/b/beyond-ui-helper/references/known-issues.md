# Known Issues & DX Watchlist

## npm audit advisories (2026-03-24)

- 53 advisories (8 low / 31 moderate / 14 high) reported.
- Major upgrades pending:
  - Storybook 7 → 10 (multiple transitive advisories).
  - vite-plugin-dts ≥ 4.5.4 to address `@microsoft/api-extractor` chain.
  - tsup ≥ 8.5.1 to fix esbuild CVEs.
  - rollup ≥ 4.59.0 (path traversal).
  - react-router-dom ≥ 7.12.1 (CSRF/XSS).
  - react-syntax-highlighter 16.1.1+ (Prism security patch).
  - Misc utilities (`giget`, `tar`, `cross-spawn`, `validator`, `nanoid`, `brace-expansion`).
- Track progress via Trello #10 and note impacts before publishing.

## Storybook migration

- Current stack built on Storybook 7. Migration to 10 introduces new builder/framework package names and config changes.
- Validate stories after migration; follow official upgrade guide.
- Coordinate with Trello #11 (lint/test failures) to keep CI green.

## Clipboard API fallback

- Component Showcase uses the Clipboard API, which requires HTTPS or `localhost`.
- In non-secure previews, Beyond-UI now surfaces a fallback toast. Document this when teams embed the showcase in other environments.

## Browserslist data freshness

- Trello #12 tracks updating `browserslist` / `caniuse-lite` data in the build pipeline.
- Run `npx update-browserslist-db@latest` (with CI approval) and commit results to reduce warnings.

## Packaging & publishing reminders

- Always run lint/test/build before packaging the skill or cutting a release.
- Validate the skill with `scripts/package_skill.py` to avoid structure or metadata issues.
- When publishing to Clawhub, include a summary referencing relevant Trello tickets and audit notes.

Keep this file updated as new advisories or workflow quirks surface so downstream agents have up-to-date context.
