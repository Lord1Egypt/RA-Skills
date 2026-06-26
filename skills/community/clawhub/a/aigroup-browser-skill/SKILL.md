---
name: aigroup-browser-skill
description: Open pages with the real CN or global browser profile on spark and return the live page title plus final URL. Use this instead of web_fetch, search, canvas, or nodes when a task explicitly asks to open a site in the browser.
metadata: { "openclaw": { "emoji": "🌐", "requires": { "bins": ["python3", "oc-cn", "oc-global", "oc-browser"] } } }
homepage: https://github.com/jackdark425/aigroup-browser-skill
license: MIT
---

# AIGroup Browser Skill

Use the real browser running on `spark` instead of substituting `web_fetch`, `search`, `nodes`, or `canvas`.

## Purpose

This skill gives OpenClaw a stable browser-opening path for sites that must be opened in the actual local browser on `spark`.

It is designed for the dual-profile setup already present on the host:
- `oc-cn` for mainland Chinese sites through the CN browser profile
- `oc-global` for international sites through the global browser profile
- `oc-browser` for automatic host-based routing when the destination is unclear

## When to use

Use this skill when the user explicitly asks to open a site in the browser, especially when CN and global routing matters.

- Use `mode=cn` for China mainland sites such as `eastmoney.com`, `baidu.com`, or `bilibili.com`
- Use `mode=global` for international sites such as `huggingface.co`
- Use `mode=auto` only when routing is genuinely unclear

## Usage

```bash
python3 scripts/open_page.py '{"url":"https://huggingface.co/","mode":"global"}'
```

## Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| url | str | yes | - | Target URL to open |
| mode | str | no | auto | `cn`, `global`, or `auto` |
| timeout | int | no | 20 | Max seconds to wait for a non-empty page title |

## Output

Returns JSON with:
- `ok`
- `mode`
- `port`
- `title`
- `url`

## Workflow

1. Choose `mode=cn` for mainland Chinese destinations and `mode=global` for international destinations.
2. Run the script and wait for a real page title from the live browser session.
3. Return the browser-reported title and final URL.
4. Do not fall back to `web_fetch`, `search`, `canvas`, or `nodes` unless the user explicitly asks for those tools instead of a real browser.
