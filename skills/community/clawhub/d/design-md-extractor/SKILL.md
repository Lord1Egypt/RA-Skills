---
name: design-md-extractor
description: Use when the user wants to generate DESIGN.md or design.md from a webpage URL by running a local, rule-based design token extraction script. The skill opens the user-provided URL with Playwright, samples computed styles locally, infers colors, typography, spacing, radius, shadows, and basic components, then writes AI-coding-friendly design documentation without model API calls.
---

# Design.md Extractor

Use this skill to turn a user-provided webpage URL into `design.md`/`DESIGN.md` using local deterministic extraction.

## Default Workflow

1. Confirm the user provided a URL or local HTML file path.
2. From this skill directory, run `pnpm install --frozen-lockfile` if `node_modules/playwright` is missing.
3. Run `scripts/extract-design.mjs` from this skill directory.
4. Prefer writing both:
   - `design.md` for the human/model-facing design guide.
   - `design-snapshot.json` for evidence and debugging.
5. Inspect the generated `design.md` before reporting results.
6. If extraction fails, report the exact failure and whether it was navigation, browser, sampling, dependency installation, or generation.

## Commands

Generate from a URL:

```bash
pnpm install --frozen-lockfile
node scripts/extract-design.mjs --url https://example.com --out ./design.md --snapshot ./design-snapshot.json
```

Generate from a local HTML file:

```bash
pnpm install --frozen-lockfile
node scripts/extract-design.mjs --url file:///absolute/path/to/page.html --out ./design.md --snapshot ./design-snapshot.json
```

The script is self-contained and loads its bundled extractor core from `lib/design-extractor-core`. It auto-detects common macOS browser executables. If Playwright cannot find a browser, pass one explicitly:

```bash
node scripts/extract-design.mjs --url https://example.com --out ./design.md --snapshot ./design-snapshot.json --executable-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

## Rules

- Analyze only URLs or files explicitly provided by the user.
- Do not crawl additional pages.
- Do not use AI/model APIs.
- Do not upload page HTML, CSS, DOM, screenshots, browsing history, or extracted data.
- Do not infer login-only or hidden states unless the loaded page visibly exposes them.
- Treat generated design tokens as a practical starting point, not a hand-authored brand book.

## References

- Read `references/snapshot-schema.md` when you need the DesignSnapshot shape.
- Read `references/extraction-rules.md` when modifying extraction behavior or explaining confidence limits.
