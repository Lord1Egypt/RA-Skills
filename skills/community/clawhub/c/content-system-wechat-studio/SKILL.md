---
name: wechat-studio
description: Launch a local WeChat article workbench for Markdown import, WeChat HTML preview, theme tuning, image selection, and optional draft push. Use when Codex needs a browser-based preview and manual QA layer before publishing.
---

# WeChat Studio

Use `wechat-studio` as the manual workbench between generated article assets and final publishing. On ClawHub, this skill is published as `content-system-wechat-studio`.

## Quick Start

Install the shared Python dependencies and the workbench frontend dependency:

```bash
.venv/bin/pip install -r requirements.txt
cd skills/wechat-studio/frontend && npm install
```

Start the local server:

```bash
python3 skills/wechat-studio/frontend/server.py
```

Open the workbench in the browser:

```text
http://127.0.0.1:4173
```

The image defaults shown in the settings page should reflect the adjacent `generate-image` runtime:

```text
provider: openai
api base: https://new.suxi.ai/v1
model: nano-nx
```

## Use This Skill When

- You need a local WeChat preview before publishing
- You want to import Markdown into a reusable article workspace
- You want to adjust theme, typography, and layout manually
- You need to review cover images or inline image slots
- You want to push a checked article into the WeChat draft box

## Default Workflow

1. Start the server and open the local workbench.
2. Import a Markdown article or switch to an existing article workspace.
3. Review the generated WeChat preview and article metadata.
4. Tune theme, typography, cover, and inline images.
5. Push the final checked version to the WeChat draft box if needed.

Use the settings page to distinguish:

- configured image values from the current `md2wechat` setup
- effective image values that `generate-image` actually injects at runtime

## Related Skills

- `wechat-formatter` provides the WeChat HTML render step
- `generate-image` provides the article companion images
- `case-writer-hybrid` and `humanizer-zh` typically feed the upstream article draft

## Notes

- This is a workbench skill, not a pure one-shot executor
- Draft push depends on the local WeChat publishing configuration already being available
- Article workspaces live under `skills/wechat-studio/content/articles/`
- Users with an existing 香蕉制作平台 can use it directly
- Users without one can open [job.suxi.ai](https://job.suxi.ai/), generate an `SK`, place it into the token field, and log in
