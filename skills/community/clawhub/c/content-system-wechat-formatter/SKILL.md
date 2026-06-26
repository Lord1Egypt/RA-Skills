---
name: wechat-formatter
description: Render article markdown into WeChat-style HTML as an independent executor. Use when Codex needs公众号排版预览, WeChat HTML output, or a publishable HTML artifact generated from an article markdown draft.
---

# WeChat Formatter

Convert article markdown into WeChat-style HTML for preview, inspection, and downstream publishing. If a sibling `*-writing-pack.json` exists, this executor will also consume summary points, highlight quotes, share copy, and ending CTA blocks.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill wechat-formatter --input content-production/drafts/ai-content-system-article.md
```

## Prepare Source Article

Start from an article markdown draft that is already written and ready for visual formatting.
If a sibling `*-writing-pack.json` exists, it will be used as an optional sidecar.

## Follow Formatting Workflow

1. Read the article markdown draft.
2. Render the content through the shared formatter runtime in `skills/wechat-formatter/runtime.py`.
3. Produce standalone WeChat preview HTML for inspection and downstream publishing.
4. When a writing-pack sidecar exists, append summary / quotes / share-copy / CTA presentation blocks without altering the source article file.
5. If `wechat-studio` is involved, let the workbench apply its own theme, typography, inline image placement, and draft-push workflow on top of this executor.

## Write Output

Write the primary exported file to:

```text
content-production/ready/<slug>-wechat.html
```

## Respect Constraints

- This skill formats and renders content; it does not author the article itself
- HTML quality depends on the article draft and current workbench state
- Workbench theme choices belong to `wechat-studio`; this skill itself should stay focused on producing HTML from Markdown

## Read Related Files

- Shared runtime: `skills/wechat-formatter/runtime.py`
- Pipeline entry: `skill_runtime/engine.py`
- Workbench integration: `skills/wechat-studio/frontend/server.py`
- Execution guide: `docs/wechat-formatter-execution-spec.md`
