---
name: chrome-cdp-browser-operator
description: windows-friendly chrome automation through an existing Chrome profile via CDP, with human-like mouse and keyboard input, browser attachment checks, page navigation, search workflows, guarded drafting, and optional notifications. use when chatgpt needs to drive a real Chrome session on port 9222, attach to a logged-in profile, or operate a safer browser workflow than brittle ad-hoc automation.
---

# Chrome CDP Browser Operator

Use this skill when a real browser session is required and the browser is already open through a dedicated Chrome profile.

## Core resources

- `scripts/browser_operator.py` attaches to Chrome over CDP, falls back to a local launch when configured, can navigate X, draft guarded replies, and emit notifications.
- `scripts/install_chrome_cdp_browser_operator.py` writes a Windows config plus starter scripts.
- `references/cdp-setup.md` explains the intended Chrome profile and port setup.

## Workflow

1. Launch Chrome with the dedicated profile and remote debugging enabled.
2. Run `browser_operator.py check` to verify that CDP attachment works.
3. Run `browser_operator.py search` or `run-cycle` in draft mode first.
4. Review the draft bundle before enabling apply mode.
5. Keep notifications optional and low-noise.

## Rules

- Use the browser skill for real browser presence, not spam or deceptive mass outreach.
- Keep public replies low volume and reviewable.
- Prefer draft mode for new workflows.
- If CDP becomes flaky, use the built-in launch fallback instead of rewriting the whole operator.
