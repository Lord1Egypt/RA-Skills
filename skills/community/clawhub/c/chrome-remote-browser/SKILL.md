---
name: chrome-remote-browser
description: Guide for AI agents on how to use Chrome Remote Debugging (CDP on port 9222) to automate browser interactions. Covers the full lifecycle — connecting, navigating, taking screenshots, reading page structure, clicking/typing/scrolling, executing JavaScript, and handling common pitfalls. Use this when an AI agent needs to interact with web pages in Chrome, especially login-gated or JavaScript-rendered pages that web_fetch cannot handle.
---

# Chrome Remote Browser — AI Agent Usage Guide

A comprehensive guide for AI agents on how to control Chrome via Remote Debugging Protocol (CDP) on port 9222. This enables interaction with authenticated sessions (Google, GitHub, dashboards, etc.) without needing separate login credentials.

## Overview

### What is Chrome Remote Debugging?

Chrome can expose a debugging interface on a local TCP port (default: 9222). When enabled, external tools can:
- Open/close tabs
- Navigate to URLs
- Read page content (DOM, accessibility tree)
- Take screenshots
- Click buttons, fill forms, scroll
- Execute JavaScript

### When to Use the Browser Tool

| Scenario | Use |
|----------|-----|
| Public facts, search queries | `web_search` (simpler, faster) |
| Fetching public page content | `web_fetch` (lightweight, no browser needed) |
| Login-gated pages (Google Console, GitHub, dashboards) | **`browser`** |
| JavaScript-rendered content (SPAs) | **`browser`** |
| Visual inspection (charts, layouts, screenshots) | **`browser`** |
| Interactive tasks (clicking, form filling, multi-step flows) | **`browser`** |

**Rule of thumb**: Try `web_fetch` first for public pages. Use `browser` when you need authentication, JavaScript rendering, or interaction.

## Prerequisites

Chrome must be running with remote debugging enabled:

```
--remote-debugging-port=9222
```

The user should see something like:
```
Server running at: 127.0.0.1:9222
```

## Core Workflow

Every browser automation task follows this cycle:

```
start → open(url) → screenshot + snapshot → act/execute_js → screenshot + snapshot → ... → done
```

**Golden rule**: Always take a **screenshot** and/or **snapshot** before and after every action. This is how you "see" and "understand" the page.

## API Reference

### 1. `status` — Check Connection

Check if the browser is connected and list open tabs.

```json
{"action": "status"}
```

Returns: Connection status and list of currently open tabs with their `targetId`s.

### 2. `open` — Open a URL

Navigate to a URL in a new tab.

```json
{"action": "open", "targetUrl": "https://example.com"}
```

Returns: A `targetId` (string) that you use for all subsequent actions on this tab.

**IMPORTANT**: Save the `targetId` — you need it for every other action.

### 3. `screenshot` — Capture Visual State

Take a screenshot of the page. This is how you "see" the page.

```json
{"action": "screenshot", "targetId": "<targetId>"}
```

Optionally save to a file:
```json
{"action": "screenshot", "targetId": "<targetId>", "savePath": "/path/to/output.png"}
```

Returns: A CDN URL of the screenshot image that you can view.

**When to screenshot:**
- After opening a page (to see its initial state)
- After clicking a button (to see the result)
- After scrolling (to see new content)
- When you need to read visual data (charts, images, layouts)
- Before reporting results to the user

### 4. `snapshot` — Read Page Structure (Accessibility Tree)

Get a text representation of the page's DOM structure. Interactive elements are assigned reference IDs (`ref`).

```json
{"action": "snapshot", "targetId": "<targetId>"}
```

Returns: An accessibility tree like:

```
[ref=e1] link "Home"
[ref=e2] button "Sign In"
[ref=e3] textbox "Email address"
[ref=e4] textbox "Password"
[ref=e5] button "Submit"
heading "Welcome to Example"
text "Some content here..."
[ref=e6] link "Learn more"
```

**Key concept**: The `ref` values (e.g., `e1`, `e2`, `e3`) are your handles for interacting with elements. You use these in `act` commands.

**When to snapshot:**
- After opening a page (to find interactive elements)
- After any page state change (new elements may appear)
- When you need to find a specific button, link, or form field
- Before clicking (to get the correct `ref` for the target element)

### 5. `act` — Interact with Page Elements

Perform actions on elements identified by their `ref` from a snapshot.

#### Click

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "click", "ref": "e2"}}
```

#### Type (into a focused/clicked element)

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "type", "ref": "e3", "text": "hello@example.com"}}
```

With Enter key submission:
```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "type", "ref": "e3", "text": "search query", "submit": true}}
```

#### Fill (multiple fields at once)

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "fill", "fields": [
  {"ref": "e3", "value": "hello@example.com"},
  {"ref": "e4", "value": "password123"}
]}}
```

#### Scroll

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "scroll", "direction": "down", "amount": 500}}
```

Directions: `"up"`, `"down"`, `"left"`, `"right"`

#### Press a key

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "press", "key": "Enter"}}
```

Common keys: `"Enter"`, `"Tab"`, `"Escape"`, `"ArrowDown"`, `"ArrowUp"`

#### Wait

```json
{"action": "act", "targetId": "<targetId>", "request": {"kind": "wait", "timeout": 3000}}
```

Wait for a specified time in milliseconds. Use after navigation or actions that trigger page loads.

### 6. `execute_js` — Run JavaScript

Execute arbitrary JavaScript in the page context. Extremely powerful for extracting data that isn't visible in the accessibility tree.

```json
{"action": "execute_js", "targetId": "<targetId>", "script": "document.title"}
```

Returns: The result of the JavaScript expression.

**Common use cases:**

Extract text content:
```javascript
document.querySelector('#result-stats').textContent
```

Extract data from tables:
```javascript
JSON.stringify(Array.from(document.querySelectorAll('table tr')).map(r => Array.from(r.cells).map(c => c.textContent.trim())))
```

Get all links:
```javascript
JSON.stringify(Array.from(document.querySelectorAll('a[href]')).map(a => ({text: a.textContent.trim(), href: a.href})))
```

Scroll to bottom:
```javascript
window.scrollTo(0, document.body.scrollHeight)
```

Extract chart/SVG data:
```javascript
JSON.stringify(Array.from(document.querySelectorAll('[aria-label]')).map(el => el.getAttribute('aria-label')))
```

### 7. `navigate` — Navigate in Current Tab

Navigate the current tab to a new URL (without opening a new tab).

```json
{"action": "navigate", "targetId": "<targetId>", "url": "https://example.com/page2"}
```

### 8. `tabs` — List Open Tabs

```json
{"action": "tabs"}
```

### 9. `close` — Close a Tab

```json
{"action": "close", "targetId": "<targetId>"}
```

## Step-by-Step Example: Filling a Google Form

Here's a complete example workflow:

```
Step 1: Open the page
  → browser.open("https://console.cloud.google.com/...")
  → Get targetId: "ABCD1234"

Step 2: See what's on the page
  → browser.screenshot("ABCD1234")
  → See: A form with various fields
  → browser.snapshot("ABCD1234")
  → See: [ref=e1] textbox "Name" / [ref=e2] dropdown "Type" / [ref=e5] button "Create"

Step 3: Fill in the name
  → browser.act("ABCD1234", {kind: "click", ref: "e1"})
  → browser.act("ABCD1234", {kind: "type", ref: "e1", text: "My Application"})

Step 4: Select from dropdown
  → browser.act("ABCD1234", {kind: "click", ref: "e2"})
  → browser.snapshot("ABCD1234")  ← MUST re-snapshot to see dropdown options!
  → See: [ref=e10] option "Web application" / [ref=e11] option "Desktop app"
  → browser.act("ABCD1234", {kind: "click", ref: "e10"})

Step 5: Submit
  → browser.act("ABCD1234", {kind: "click", ref: "e5"})
  → browser.screenshot("ABCD1234")  ← Verify the result
```

## Critical Rules & Best Practices

### Rule 1: ALWAYS Snapshot Before Acting

```
❌ BAD:  open → click e5 (from memory or assumption)
✅ GOOD: open → snapshot → find ref → click ref → snapshot (verify)
```

The `ref` IDs change every time the page state changes. Never reuse refs from a previous snapshot after any navigation or interaction.

### Rule 2: ALWAYS Screenshot After State Changes

After clicking, submitting, or navigating, always take a screenshot to verify the result before proceeding. Things that can go wrong:
- The click didn't register
- A loading spinner appeared
- An error dialog popped up
- The page navigated somewhere unexpected

### Rule 3: Re-snapshot After EVERY Page Change

When you click a button, open a dropdown, or navigate — the DOM changes. Old `ref` IDs become invalid. You MUST take a new snapshot to get fresh refs.

```
click dropdown → snapshot (get new refs for options) → click option
```

### Rule 4: Handle Page Load Delays

Many pages (especially SPAs like Google Cloud Console) load content asynchronously. After navigating:

```
navigate → wait(2000-3000) → screenshot + snapshot
```

If the page still looks empty or loading, wait longer and retry.

### Rule 5: Handle Google Account Switching

Google services may show a different account than expected. Check for account indicators:
- Look for user avatar/email in the top-right corner
- If wrong account, look for account switcher or use `?authuser=N` URL parameter:
  - `authuser=0` = first Google account
  - `authuser=1` = second Google account
  - Add to any Google URL: `https://console.cloud.google.com/...?authuser=1`

### Rule 6: Element Not Found Errors

If you get "Element ref not found":
1. The page likely changed since your last snapshot
2. Take a fresh snapshot
3. Find the new ref for the element you want
4. Retry with the new ref

### Rule 7: Don't Over-rely on Screenshots Alone

Screenshots show what the page looks like, but:
- You can't click on screenshot pixels
- You need `snapshot` to get interactive element refs
- Use screenshots for verification, snapshots for interaction

### Rule 8: Sequential, Not Parallel

Browser actions are inherently sequential — one tab, one state at a time. Do NOT try to parallelize browser operations on the same tab.

### Rule 9: Minimize Actions

Each action has latency and potential for failure. Plan your workflow:
- Use `fill` for multiple form fields instead of individual `type` calls
- Use `execute_js` for data extraction instead of clicking through pagination
- Use URL parameters instead of clicking through menus when possible

### Rule 10: File Downloads

Chrome remote debugging **cannot reliably intercept file downloads**. If you need to download a file:
- Try to get the download URL via `execute_js` and use `web_fetch` instead
- Or note the download URL/path for the user to handle manually

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| "Element e11 not found" | Page changed after snapshot | Re-snapshot, find new ref |
| Page looks blank after navigate | Content loading asynchronously | `wait(3000)` then screenshot |
| Wrong Google account | Multiple accounts logged in | Add `?authuser=N` to URL |
| CAPTCHA appeared | Too many automated actions | Slow down, add delays between actions |
| Dropdown options not visible | Haven't re-snapshotted after click | Click dropdown → snapshot → click option |
| Form submit didn't work | Button ref was stale | Re-snapshot, find fresh button ref, click |
| Can't find a button | Element is below fold / in scrollable area | Scroll down, then re-snapshot |
| Screenshot shows loading spinner | Page still loading | Wait 2-5 seconds, retry screenshot |
| JavaScript returns undefined | Selector doesn't match | Check the page source, try different selectors |
| Tab closed unexpectedly | Page navigated away (e.g., OAuth redirect) | List tabs, find the new tab/targetId |

## Advanced Patterns

### Pattern: Extracting Data from Google Charts

Google's charts are often rendered as SVG/Canvas. To extract underlying data:

```javascript
// Try aria-labels on chart elements
JSON.stringify(Array.from(document.querySelectorAll('[aria-label]')).map(el => {
  var label = el.getAttribute('aria-label');
  if (label && /\d/.test(label)) return label;
  return null;
}).filter(Boolean))
```

```javascript
// Try embedded data scripts
JSON.stringify(Array.from(document.querySelectorAll('script')).filter(s => 
  s.textContent.includes('AF_initDataCallback')
).map(s => s.textContent.substring(0, 500)))
```

### Pattern: Handling Multi-Page Workflows

For wizards/multi-step forms:

```
1. snapshot → fill step 1 fields → click "Next"
2. wait(2000) → snapshot → fill step 2 fields → click "Next"
3. wait(2000) → snapshot → verify summary → click "Submit"
4. wait(3000) → screenshot → verify confirmation
```

### Pattern: Navigating Google Cloud Console

Google Cloud Console is a complex SPA. Tips:
- Use direct URLs whenever possible instead of clicking through menus
- Example: `https://console.cloud.google.com/apis/library/searchconsole.googleapis.com?project=PROJECT_ID`
- Always include `?project=PROJECT_ID` to avoid project-switching issues
- Pages may take 3-5 seconds to load; always wait before interacting
- The sidebar menu may cover content; close it if it's in the way

### Pattern: Extracting Search Results Count

For Google Search (`site:example.com`):

```javascript
document.querySelector('#result-stats')?.textContent || 'No result stats found'
```

## Workflow Template

Use this template for any browser automation task:

```
1. PLAN: What do I need to accomplish? What URL do I start at?
2. OPEN: browser.open(url) → save targetId
3. OBSERVE: screenshot + snapshot → understand the page
4. ACT: Identify the right ref → perform action (click/type/fill)
5. VERIFY: screenshot + snapshot → did it work?
6. REPEAT: Steps 3-5 until task is complete
7. EXTRACT: Use execute_js or snapshot to collect results
8. REPORT: Present findings to user with screenshots as evidence
```

## Quick Reference

| Action | When to Use | Returns |
|--------|-------------|---------|
| `open(url)` | Start: open a page | `targetId` |
| `screenshot(targetId)` | See the page visually | CDN image URL |
| `snapshot(targetId)` | Read page structure, get element refs | Accessibility tree text |
| `act(click, ref)` | Click buttons, links, dropdowns | — |
| `act(type, ref, text)` | Type into input fields | — |
| `act(fill, fields)` | Fill multiple fields at once | — |
| `act(scroll, direction)` | Scroll the page | — |
| `act(press, key)` | Press keyboard keys | — |
| `act(wait, timeout)` | Wait for page loads | — |
| `execute_js(script)` | Extract data, run custom logic | Script result |
| `navigate(url)` | Go to new URL in same tab | — |
| `tabs()` | List open tabs | Tab list |
| `close(targetId)` | Close a tab | — |
