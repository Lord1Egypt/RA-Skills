---
name: "chrome_web_automation"
description: "Use when the user wants browser automation in an existing Chrome session: click, fill, inspect tabs, capture screenshots, or debug web flows."
---


# Chrome Web Automation

Use this skill before any browser interaction that depends on the user's live Chrome session.

## Workflow
1. Start by inspecting current tabs and browser context.
2. Navigate or select the right tab.
3. Snapshot the page before interacting.
4. Click, type, submit, and screenshot using stable references.
5. Re-snapshot after navigation or large DOM updates.

## Best Fits
- Web app debugging
- Form filling
- Screenshot capture
- Console or tab inspection
- Reproducing UI issues in a user browser session

## Guardrails
- Re-snapshot when element references go stale.
- Do not assume current tab state without checking.
- Prefer explicit browser actions over ambiguous natural-language leaps.

## Example Requests
- Open the current Chrome session and reproduce this checkout bug.
- Fill the form, capture screenshots, and show me where validation breaks.

## Inputs
- Target site or current tab context
- Desired browser actions
- Artifacts to capture

## Outputs
- Browser interaction transcript
- Screenshots or evidence
- Reproduction notes

## Success Criteria
- The correct tab or page was inspected.
- Interactions were completed against fresh page state.
- Useful artifacts were captured when needed.

## Non-Goals
- Synthetic browser testing unrelated to the user browser context

## Source Provenance
Derived from `src/skills/bundled/claudeInChrome.ts`.
