# Design.md Extractor

<p align="center">
  <a href="README.md"><strong>English</strong></a>
  ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-2563eb?style=for-the-badge">
  <img alt="Tests passing" src="https://img.shields.io/badge/tests-passing-22c55e?style=for-the-badge">
  <img alt="Node.js" src="https://img.shields.io/badge/runtime-Node.js-475569?style=for-the-badge">
  <img alt="Local first" src="https://img.shields.io/badge/local--first-DESIGN.md-7c3aed?style=for-the-badge">
</p>

Local-first `DESIGN.md` extraction skill for turning a webpage URL or local HTML file into AI-friendly design documentation.

Design.md Extractor helps AI coding agents inspect visible webpage styles locally, infer practical design tokens, and write a reusable `DESIGN.md` without model API calls or uploading page data. It samples computed styles with Playwright, then generates colors, typography, spacing, radius, shadow, and component guidance for frontend implementation.

## Features

- Generates AI-friendly `DESIGN.md` from a URL or local HTML file.
- Writes an optional `design-snapshot.json` with extraction evidence for debugging.
- Extracts colors, typography, spacing, radius, shadows, and basic component patterns.
- Infers semantic color roles such as primary, surface, text, muted, border, and focus.
- Detects common UI components such as primary buttons, cards, badges, inputs, and nav links.
- Bundles the extractor runtime in `lib/design-extractor-core` so the skill does not depend on a parent monorepo.
- Runs locally with Playwright and does not call AI/model APIs.
- Includes publish metadata for ClawHub, SkillHub, and OneTool via `publish.config.json`.

## Quick Start

```bash
cd skills/design-md-extractor
pnpm install --frozen-lockfile
npm test
```

Generate from a public webpage:

```bash
node scripts/extract-design.mjs \
  --url https://example.com \
  --out ./design.md \
  --snapshot ./design-snapshot.json
```

Generate from a local HTML file:

```bash
node scripts/extract-design.mjs \
  --url file:///absolute/path/to/page.html \
  --out ./design.md \
  --snapshot ./design-snapshot.json
```

If Playwright cannot find a browser, pass one explicitly:

```bash
node scripts/extract-design.mjs \
  --url https://example.com \
  --out ./design.md \
  --snapshot ./design-snapshot.json \
  --executable-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

After extraction, the skill writes:

- `design.md`
- `design-snapshot.json` when `--snapshot` is provided

## Commands

```bash
node scripts/extract-design.mjs --url <url_or_file_url> [--out design.md] [--snapshot design-snapshot.json]
node scripts/extract-design.mjs --url <url_or_file_url> --viewport 1440x900
node scripts/extract-design.mjs --url <url_or_file_url> --timeout 30000
node scripts/extract-design.mjs --url <url_or_file_url> --executable-path <browser_executable>
npm run test:publish
npm run test:fixture
npm test
```

## Skill Workflow

Use this skill when an agent needs a concrete design reference before building or restyling UI:

```bash
pnpm install --frozen-lockfile
node scripts/extract-design.mjs --url https://stripe.com --out DESIGN.md --snapshot design-snapshot.json
```

Review `DESIGN.md`, then use the generated tokens and component notes as implementation context. Treat the output as a practical starting point, not a hand-authored brand book.

## Publish Package

This repository keeps generated package artifacts out of git. Build a marketplace upload package with a publisher skill or release script:

```bash
node /absolute/path/to/skill-publisher/scripts/publish-skill.mjs . \
  --platform all \
  --package minimal \
  --out dist/publish
```

The minimal package includes:

- `SKILL.md`
- `README.md` and `README.zh-CN.md`
- `package.json` and `pnpm-lock.yaml`
- `agents/`
- `scripts/`
- `references/`
- `fixtures/`
- `lib/`

Use the generated zip as the GitHub Release asset or marketplace upload file.

## Repository Notes

For a public GitHub repository, keep generated artifacts such as `dist/` and dependency folders such as `node_modules/` out of git. Publish zip files through GitHub Releases when needed.

## Privacy

Design.md Extractor analyzes only the URL or local file explicitly provided by the user. It does not crawl additional pages, call model APIs, upload page HTML, upload DOM data, upload CSS, upload screenshots, or collect browsing history.

## Disclaimer

Generated design tokens are inferred from visible computed styles. They may miss hidden states, authenticated pages, responsive variants, animation details, proprietary assets, or brand rules that are not visible in the loaded page.
