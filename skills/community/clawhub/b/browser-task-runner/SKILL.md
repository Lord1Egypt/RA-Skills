---
name: browser-task-runner
description: Plan and execute repeatable browser-based workflows such as opening sites, logging in, navigating dashboards, filling forms, exporting data, taking screenshots, and extracting page content. Use when a task depends on browser automation or scripted browser interaction on the local machine, especially for fixed multi-step website workflows.
---

# Browser Task Runner

Treat browser work as fragile. Prefer deterministic, repeatable flows over improvising clicks.

## Workflow

1. Confirm the target site and exact outcome.
2. Identify the available execution path:
   - direct web fetch/search for read-only public pages
   - local browser automation tooling if available
   - AppleScript/UI scripting as a fallback for simple fixed flows
3. Check whether the task needs authentication, MFA, CAPTCHA, or sensitive confirmation.
4. For destructive or account-changing actions, ask before proceeding.
5. Execute the smallest reliable flow and report where manual takeover may still be needed.

## Good fits

- open a fixed set of URLs
- log into a routine internal tool
- navigate to a report page
- export a CSV or PDF
- fill a repetitive form
- capture a screenshot of a page state
- scrape visible page data into a summary

## Fragile cases

Be cautious when the task involves:
- CAPTCHA
- MFA prompts
- anti-bot protections
- drag-and-drop heavy UIs
- unpredictable popups
- account settings or payment actions

In those cases, prefer a hybrid flow: automate the boring parts and let the user finish the sensitive step.

## Execution policy

Prefer this order:
1. Read-only web tools for public pages
2. Existing local automation tools/frameworks
3. macOS UI scripting for narrow, stable workflows

Do not pretend browser control exists if the tooling is absent. State what is missing and what can still be automated.

## Output pattern

Report using:
- **Goal**
- **Automation path**
- **What succeeded**
- **Where it may break**
- **Next improvement**

Keep website-specific details in scripts or references if this skill grows beyond a generic runner.
