# Publish To ClawHub / OpenClaw Hub

This repository is prepared as an OpenClaw skill package under the public slug `aigroup-browser-skill`.

## Pre-publish checklist

- Confirm `SKILL.md` name, description, metadata, and homepage are correct
- Confirm `README.md` matches the final public positioning
- Confirm `scripts/open_page.py` is executable and works on the target host
- Confirm the repository is public and pushed to `main`
- Confirm the display name should remain `AIGroup Browser Skill`

## Local validation

Run these checks before publishing:

```bash
openclaw skills info aigroup-browser-skill
python3 scripts/open_page.py '{"url":"https://huggingface.co/","mode":"global"}'
python3 scripts/open_page.py '{"url":"https://www.eastmoney.com/","mode":"cn"}'
```

## Publish with clawhub CLI

If `clawhub` is already installed and authenticated, publish from the repository root:

```bash
cd /path/to/aigroup-browser-skill
clawhub publish
```

If the CLI asks for metadata, use:

- Name: `AIGroup Browser Skill`
- Slug: `aigroup-browser-skill`
- Summary: `Open pages with the real CN or global browser profile on spark and return the live page title plus final URL.`
- Category intent: browser automation, routing, OpenClaw skills

## Suggested listing copy

### One-line summary

OpenClaw skill for opening sites in the real browser on `spark`, with explicit mainland-China and international routing.

### Longer description

`aigroup-browser-skill` gives OpenClaw a browser-first path for tasks where a site must be opened in the live browser instead of through `web_fetch`, `search`, `canvas`, or `nodes`. It supports CN and global browser profiles, host-based routing, and CDP-backed verification of the final page title and URL.

## Suggested tags

- openclaw
- skill
- browser
- automation
- cdp
- routing
- china
- python

## After publish

- Install the published Hub skill in a clean test workspace
- Confirm the Hub copy preserves `SKILL.md` metadata
- Confirm examples in the listing still match current behavior
- If needed, add screenshots or a short demo GIF to the repository README
