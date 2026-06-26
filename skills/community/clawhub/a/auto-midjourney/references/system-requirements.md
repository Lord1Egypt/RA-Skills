# System Requirements

Use this file when the user asks what devices or operating systems are supported.

## Current support status

- macOS: supported and validated in this skill
- Windows: browser/CDP path is designed to work, but not validated in this repo yet
- Linux: browser/CDP path is designed to work, but not validated in this repo yet

## Required software

- Python 3
- Node.js
- `npm install` once in this skill directory to restore `playwright-core` when needed
- Google Chrome or Chromium with DevTools remote debugging available
- A logged-in Midjourney Alpha web session

## Important implementation detail

This skill does not need a powerful GPU on the user's machine because Midjourney rendering happens in Midjourney's cloud.

The local machine is responsible for:

- launching Chrome
- reusing the authenticated browser session
- watching page resources for completed images
- downloading or converting result files

## Browser transport notes

- The preferred live path is browser/CDP transport rather than raw HTTP
- When `playwright-core` is installed, the skill can attach to the live Chrome session through Playwright over CDP
- Use `MJ_BROWSER_BACKEND=playwright` to force Playwright or `MJ_BROWSER_BACKEND=cdp` to force the legacy CDP scripts
- On macOS, the skill can still fall back to AppleScript if CDP fetch hits trouble
- On Windows and Linux, the intended path is CDP only

## When to set `MJ_CHROME_APP`

Set `MJ_CHROME_APP` explicitly when:

- Chrome is installed in a non-default location
- the system has multiple Chrome-family browsers
- auto-detection does not find the correct executable
