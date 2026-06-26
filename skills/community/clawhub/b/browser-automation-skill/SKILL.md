---
name: browser-relay
description: Use Browser Relay when the user wants to control a real signed-in Chrome or Chromium browser through the published browser-relay-cli package and unpacked Browser Relay extension. Trigger for tasks like opening pages, reusing tabs, clicking, typing, scrolling, searching, taking screenshots, reading visible page content, or handling DOM-hostile sites with screenshot-guided clicks. Do not use for CAPTCHA bypass, stealth scraping, or evasion of anti-bot systems.
---

# Browser Relay

Use this skill when the user wants real browser control through the local
Browser Relay runtime.

This skill is a thin wrapper around the published npm package:

- npm package: `browser-relay-cli`
- GitHub repo: `https://github.com/jasonCodeSpace/browser-relay`

## Use this skill when

- The user wants to control an already signed-in Chrome session
- The task requires opening pages, reusing tabs, clicking, typing, hovering, scrolling, or screenshots
- DOM selectors are unreliable and a screenshot-guided click is more appropriate
- The user wants a local browser relay instead of a hosted browser

## Do not use this skill when

- The user asks to bypass CAPTCHA or anti-bot systems
- The task requires stealth automation or hiding browser control
- The user only needs plain web search or static scraping

## Workflow

### 1. Make sure the runtime is available

Use `npx`, not a local repo path, unless the user explicitly wants development mode.

Quick checks:

```bash
npx browser-relay-cli version
npx browser-relay-cli extension-path
```

### 2. Start the relay

```bash
npx browser-relay-cli relay-start
```

### 3. Make sure the extension is loaded

Tell the user to:

1. Open `chrome://extensions`
2. Enable `Developer mode`
3. Click `Load unpacked`
4. Select the directory printed by `npx browser-relay-cli extension-path`

Then verify:

```bash
npx browser-relay-cli status
```

You want `extensionConnected: true`.

### 4. Operate the browser

Prefer DOM-first commands:

```bash
npx browser-relay-cli list-tabs
npx browser-relay-cli create-tab https://example.com
npx browser-relay-cli click 123456 'button'
npx browser-relay-cli type 123456 'input[name=\"q\"]' 'browser relay'
npx browser-relay-cli press 123456 Enter
npx browser-relay-cli scroll 123456 800
```

For DOM-hostile pages, switch to hybrid mode:

1. `screenshot`
2. `describe-visible`
3. `click-at` or `click-at-norm`

### 5. Prefer tab reuse

- Reuse existing relay tabs whenever possible
- Avoid opening unnecessary new tabs
- Use screenshot-guided clicks only when selector-based actions are unreliable

## Key commands

Read `references/commands.md` when you need the compact command catalog.

## Safety rules

- Do not instruct Browser Relay to bypass CAPTCHA or anti-bot challenges
- Do not claim Browser Relay is stealthy
- Do not save tokens, `.env` files, or local private credentials in the skill folder
- Keep this skill focused on the published runtime and extension workflow
