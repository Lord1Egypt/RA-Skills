# Publish Handoff

## Goal
Hand the final article to the WeChat publishing workflow with minimal ambiguity.

## Required final artifacts

- article markdown file
- cover image path if available
- optional inline image list
- optional QR code image path

## Frontmatter contract

```yaml
---
title: ...
author: 阿爪
summary: ...
coverImage: relative/or/absolute/path
---
```

## Recommended publish step

Use the existing WeChat posting workflow after markdown is ready.

Example:

```bash
bun skills/baoyu-post-to-wechat/scripts/wechat-api.ts <article.md> --theme modern --color black
```

## Notes

- QR code should usually remain as an inline image near the end, not as cover.
- Cover should be a separate visual if available.
- If only one image exists and it is a QR code, do not auto-use it as cover.
