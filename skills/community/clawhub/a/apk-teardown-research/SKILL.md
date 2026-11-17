---
name: apk-teardown-research
description: Analyzes Android APKs through the Crawlora API — submit an APK or public URL, inspect static-analysis results, compare versions, build timelines, and compare ownership signals — returning clean JSON. Use for mobile-app security, provenance, SDK, permission, signing, and release-history research.
---

# APK teardown research

Submit Android packages for static analysis and compare completed teardown
jobs as normalized JSON. This skill is for authorized analysis of packages you
are allowed to inspect.

## When to use this skill

- Inspect manifest, permissions, signing, SDK, library, and tech-stack signals.
- Diff two versions of the same app.
- Build a multi-version release timeline.
- Compare two different packages for possible common ownership signals.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

Submit one `.apk`/`.xapk` or HTTPS `file_url` with
`/apk-teardown/jobs`. Poll the returned job path until complete, then use
`/apk-teardown/diff`, `/apk-teardown/timeline`, or
`/apk-teardown/compare-ownership` with completed job ids. Never submit
packages or URLs without the necessary authorization.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).
