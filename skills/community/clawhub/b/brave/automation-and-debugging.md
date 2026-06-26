# Automation and Debugging

## Chromium Tooling Still Applies

Brave can usually be automated with Chromium-compatible tooling:
- Playwright
- Puppeteer
- Chrome DevTools Protocol clients

The browser engine is not the whole story. Shields, profile state, and built-in blocking can change automation outcomes.

## Remote Debugging Rules

Enable remote debugging only when the user explicitly approves it.

Before enabling:
- choose a dedicated test or automation profile
- avoid the user's daily profile when possible
- define how long the port should stay open
- verify whether the task needs observation only or active control

Turn it off after the task unless the user wants a persistent local automation setup.

## Automation Sanity Checks

Before blaming the tool, verify:
- Brave launched with the expected profile
- the DevTools endpoint is reachable
- the failing behavior reproduces without extensions if extensions are not part of the test
- the same script is not depending on Chrome-only assumptions

## Brave-Specific Failure Patterns

- A page element never appears because Shields blocked the underlying script
- Automation succeeds in a clean profile but fails in the daily profile because extensions alter the DOM
- Remote debugging attaches correctly but the target tab is the wrong profile or window

## Verification Rule

A successful attachment is not the finish line.
Confirm the real outcome in the browser:
- correct profile
- correct tab or window
- expected site behavior
- expected artifact such as screenshot, login state, or loaded extension
