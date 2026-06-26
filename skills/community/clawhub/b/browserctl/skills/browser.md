---
name: browser
category: Browser Commands
commands: [open, click, fill, paste, screenshot, scroll, title, last-message-content, wait]
description: "Navigate pages, interact with elements, capture screenshots, scroll, read page state, and wait for conditions."
---

# Browser Commands

Nine browser commands available via `browsectl run --type <CMD>` for direct browser interaction: navigation, clicking, typing, pasting, screenshots, scrolling, reading page state, and waiting for conditions.

> **Prerequisite:** A browser session must be active before using any of these commands. See [session.md](session.md) for `create_session` / `use_session`.

---

## Table of Contents

1. [open](#1-open) — Navigate to a URL
2. [click](#2-click) — Click an element
3. [fill](#3-fill) — Type text character-by-character
4. [paste](#4-paste) — Paste text via clipboard simulation
5. [screenshot](#5-screenshot) — Capture element to PNG
6. [scroll](#6-scroll) — Scroll page or element
7. [get_title](#7-get_title) — Read page title
8. [get_last_message](#8-get_last_message) — Extract last chat message
9. [wait_for](#9-wait_for) — Wait for a condition

---

## 1. `open`

Navigate the current tab to a URL. Bare domains like `doubao.com` are automatically prefixed with `https://`.

| | |
|---|---|
| **CLI** | `browsectl run --type open --url <URL>` |
| **Internal command type** | `open` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | string | **Yes** | — | URL to navigate to. Bare domains (e.g. `"example.com"`) are auto-prefixed with `https://`. Use `"about:blank"` for an empty page. |
| `viewport` | object `{width, height}` | No | *(unchanged)* | Resize the browser viewport after navigation. Both `width` and `height` are integers in pixels. |

### CLI Example

```sh
# Navigate to a full URL
browsectl run --type open --url "https://github.com/yorelog/browsectl"

# Bare domain — https:// is added automatically
browsectl run --type open --url example.com

# With viewport resize
browsectl run --type open --url example.com --viewport 1920,1080
```

### Example Response

```json
{
  "ok": true,
  "type": "open",
  "url": "https://doubao.com"
}
```

### Notes

- `about:blank` is the only URL that skips the `https://` prefix logic.
- The viewport resize is executed via `window.resizeTo()` after navigation completes.
- Navigation waits for the page load event before returning.

---

## 2. `click`

Click a DOM element by CSS selector. Includes smart fallback handling when clicks are intercepted by overlays, tooltips, or other covering elements.

| | |
|---|---|
| **CLI** | `browsectl run --type click --selector <CSS>` |
| **Internal command type** | `click` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `selector` | string | **Yes** | — | CSS selector of the element to click. Supports extended syntax: `CSS::text(/pattern/flags)` to filter by text content. |
| `scope` | string | No | *(full document)* | CSS selector of a scope root. Element lookup and fallback are restricted to descendants of this element. |
| `fallback` | string | No | `auto` | Strategy when native click is intercepted. Values: `"parent"`, `"sibling"`, a custom CSS selector string, or omit for automatic smart fallback. |
| `timeout` | integer | No | `20000` | Max time in milliseconds to wait for the element to appear in the DOM. |

### Click Fallback Mechanism

When a native WebDriver click is intercepted (e.g. by an overlay or modal), browsectl automatically retries:

1. **Scroll into view** — ensures the element is visible in the viewport.
2. **Apply fallback strategy:**

| Fallback value | Behavior |
|---|---|
| `"parent"` | JS click on `element.parentElement` |
| `"sibling"` | JS click on next or previous sibling element |
| *custom CSS selector* | Find the fallback element by selector and click it (native first, then JS) |
| *(omitted / auto)* | Smart cascade: try parent → sibling → self via JS |

### CLI Examples

```sh
# Basic click
browsectl run --type click --selector "#submit-btn"

# Click with text filter — click the <button> whose text matches "Sign In"
browsectl run --type click --selector "button::text(/Sign In/i)"

# Click within a scoped container
browsectl run --type click --selector ".item-action" --scope ".sidebar"

# Explicit parent fallback
browsectl run --type click --selector ".close-icon" --fallback parent

# Custom fallback selector
browsectl run --type click --selector ".hidden-radio" --fallback ".radio-label"
```

### Example Response

Successful native click:

```json
{
  "ok": true,
  "type": "click",
  "selector": "#login-button",
  "scope": null,
  "jsClick": false,
  "fallback": null
}
```

Fallback was used (intercepted):

```json
{
  "ok": true,
  "type": "click",
  "selector": ".close-icon",
  "scope": null,
  "jsClick": true,
  "fallback": "parent"
}
```

### Notes

- `jsClick: true` in the response indicates the native click was intercepted and a JavaScript-based fallback was used.
- The `fallback` field in the response shows which strategy succeeded (e.g. `"parent"`, `"sibling"`, `"selector:.radio-label"`, or the auto-resolved strategy name).
- The extended selector syntax `CSS::text(/regex/flags)` lets you filter elements by their text content using a JavaScript regex pattern. Example: `a::text(/Sign Up/i)`.

---

## 3. `fill`

Clear an input field and type text into it character by character. If no selector is given, targets the currently focused element.

| | |
|---|---|
| **CLI** | `browsectl run --type fill --text <TEXT> [--selector <CSS>]` |
| **Internal command type** | `fill` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | **Yes** | — | The text to type into the field. |
| `selector` | string | No | *(focused element)* | CSS selector of the input element. Supports `CSS::text(/pattern/flags)`. Omit to target the currently focused element. |
| `scope` | string | No | *(full document)* | CSS selector of scope root to restrict element lookup. |
| `timeout` | integer | No | `20000` | Max time in ms to wait for the element. |

### CLI Examples

```sh
# Type into a specific input
browsectl run --type fill --selector "#search-box" --text "browsectl automation"

# Type into the currently focused element
browsectl run --type fill --text "Hello, world!"

# Scoped fill
browsectl run --type fill --selector "input[name='email']" --scope ".login-form" --text "user@example.com"
```

### Example Response

```json
{
  "ok": true,
  "type": "fill",
  "text": "browsectl automation",
  "selector": "#search-box",
  "scope": null
}
```

### Notes

- **Implementation:** The element is clicked first to ensure focus, then text is cleared (`value = ''`) and typed character by character via JS, dispatching `input` events at each step.
- Works with `<input>`, `<textarea>`, and `contenteditable` elements.
- For large blocks of text, prefer [`paste`](#4-paste) which is significantly faster.
- An empty or whitespace-only selector string is treated the same as omitting the selector (uses the focused element).

---

## 4. `paste`

Paste text into an input field via clipboard simulation. Faster than `fill` for large text blocks.

| | |
|---|---|
| **CLI** | `browsectl run --type paste --text <TEXT> [--selector <CSS>]` |
| **Internal command type** | `paste` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | **Yes** | — | The text to paste. |
| `selector` | string | No | *(focused element)* | CSS selector of the input element. Supports `CSS::text(/pattern/flags)`. Omit to target the currently focused element. |
| `scope` | string | No | *(full document)* | CSS selector of scope root to restrict element lookup. |
| `timeout` | integer | No | `20000` | Max time in ms to wait for the element. |

### CLI Examples

```sh
# Paste into a specific textarea
browsectl run --type paste --selector "textarea.editor" --text "Large block of text..."

# Paste into focused element
browsectl run --type paste --text "Clipboard content here"
```

### Example Response

```json
{
  "ok": true,
  "type": "paste",
  "text": "Large block of text...",
  "selector": "textarea.editor",
  "scope": null
}
```

### Notes

- **Implementation:** Focuses the element, then simulates a `ClipboardEvent('paste')` with a `DataTransfer` payload. If the paste event is not prevented by the page, it falls back to directly setting the value via `setRangeText` (for inputs/textareas) or inserting a text node (for `contentEditable` elements), followed by dispatching `input` and `change` events.
- Handles `<input>`, `<textarea>`, and `contenteditable` elements.
- Use `paste` over `fill` when typing speed matters (e.g. pasting code, long paragraphs).
- An empty or whitespace-only selector is treated as no selector (uses the focused element).

---

## 5. `screenshot`

Capture a DOM element as a PNG image.

| | |
|---|---|
| **CLI** | `browsectl run --type screenshot --selector <CSS> [--path <PATH>]` |
| **Internal command type** | `screenshot` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `selector` | string | **Yes** | — | CSS selector of the element to capture. Supports `CSS::text(/pattern/flags)`. |
| `scope` | string | No | *(full document)* | CSS selector of scope root to restrict element lookup. |
| `path` | string | No | `"outputs/screenshot.png"` | File path to save the PNG screenshot. Parent directories are created automatically. |
| `timeout` | integer | No | `20000` | Max time in ms to wait for the element. |

### CLI Examples

```sh
# Capture an element to default path
browsectl run --type screenshot --selector "main.content"

# Capture to a specific path
browsectl run --type screenshot --selector "#chart" --path "outputs/chart-2024.png"

# Capture the full body
browsectl run --type screenshot --selector "body" --path "outputs/full-page.png"
```

### Example Response

```json
{
  "ok": true,
  "type": "screenshot",
  "path": "outputs/screenshot.png",
  "selector": "main.content",
  "scope": null
}
```

### Notes

- Parent directories for the output path are created automatically via `create_dir_all`.
- The screenshot captures only the matched element, not the full page. To capture the full page, use `"selector": "body"`.

---

## 6. `scroll`

Scroll the page or a specific element in any direction.

| | |
|---|---|
| **CLI** | `browsectl run --type scroll [--direction down] [--amount 800]` |
| **Internal command type** | `scroll` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `direction` | string | No | `"down"` | Scroll direction. One of: `"up"`, `"down"`, `"left"`, `"right"`. |
| `amount` | integer | No | `800` | Scroll distance in pixels. |
| `selector` | string | No | *(window)* | CSS selector of the element to scroll. Omit to scroll the window. |
| `behavior` | string | No | `"smooth"` | Scroll behavior. One of: `"smooth"`, `"auto"`. |

### Direction ↔ Scroll Axis Mapping

| Direction | X offset | Y offset |
|---|---|---|
| `"down"` | `0` | `+amount` |
| `"up"` | `0` | `-amount` |
| `"right"` | `+amount` | `0` |
| `"left"` | `-amount` | `0` |

### CLI Examples

```sh
# Scroll down (defaults: down, 800px, smooth)
browsectl run --type scroll

# Scroll up 400px
browsectl run --type scroll --direction up --amount 400

# Scroll a specific container
browsectl run --type scroll --selector ".chat-messages" --direction down --amount 600

# Instant scroll (no animation)
browsectl run --type scroll --direction down --amount 2000 --behavior auto
```

### Example Response

```json
{
  "ok": true,
  "type": "scroll",
  "direction": "down",
  "amount": 800,
  "x": 0,
  "y": 800,
  "behavior": "smooth"
}
```

### Notes

- Uses `window.scrollBy()` for window scrolling and `element.scrollBy()` for element scrolling, both with the `ScrollToOptions` object.
- The `x` and `y` fields in the response show the actual pixel offsets passed to `scrollBy`.
- `"smooth"` behavior animates the scroll; `"auto"` jumps instantly.
- No parameters are required — calling `scroll` with no arguments scrolls the window down 800px with smooth behavior.

---

## 7. `get_title`

Get the title of the current page.

| | |
|---|---|
| **CLI** | `browsectl run --type title` |
| **Internal command type** | `title` |

### Parameters

This command takes no parameters.

### CLI Example

```sh
browsectl run --type title
```

### Example Response

```json
{
  "ok": true,
  "type": "title",
  "title": "GitHub - yorelog/browsectl: WebDriver automation for AI agents"
}
```

### Notes

- Uses the WebDriver `getTitle` command.
- Returns the content of the `<title>` element, which may differ from any visible heading on the page.
- Useful for verifying navigation succeeded (e.g., after `open`, check the title contains an expected string).

---

## 8. `get_last_message`

Extract the content (text, HTML, images, links) of the last message block on the page. Designed for chat interfaces where you need to read the most recent AI or user response.

| | |
|---|---|
| **CLI** | `browsectl run --type last-message-content [--selector <CSS>]` |
| **Internal command type** | `last-message-content` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `selector` | string | No | `[data-testid="message-block-container"]` | CSS selector for message block containers. The tool finds ALL matching elements, then extracts content from the LAST one. |

### CLI Examples

```sh
# Use default selector (data-testid="message-block-container")
browsectl run --type last-message-content

# Custom selector for a different chat UI
browsectl run --type last-message-content --selector ".message-bubble"
```

### Example Response — Message Found

```json
{
  "ok": true,
  "type": "last-message-content",
  "data": {
    "found": true,
    "selector": "[data-testid=\"message-block-container\"]",
    "html": "<p>Here is the answer to your question.</p><img src=\"/img/chart.png\" alt=\"Chart\">",
    "text": "Here is the answer to your question.",
    "images": [
      {
        "index": 0,
        "src": "/img/chart.png",
        "alt": "Chart",
        "title": ""
      }
    ],
    "links": []
  }
}
```

### Example Response — No Messages Found

```json
{
  "ok": true,
  "type": "last-message-content",
  "data": {
    "found": false,
    "selector": "[data-testid=\"message-block-container\"]"
  }
}
```

### Extracted Data Structure

| Field | Type | Description |
|---|---|---|
| `found` | boolean | Whether at least one matching element was found. |
| `selector` | string | The CSS selector that was used. |
| `html` | string | Inner HTML of the last message element. |
| `text` | string | Trimmed `textContent` of the last message element. |
| `images` | array | All `<img>` elements inside the message. |
| `links` | array | All `<a>` elements inside the message. |

**Image object:**

| Field | Type | Description |
|---|---|---|
| `index` | integer | Zero-based index among images in the message. |
| `src` | string | Image `src` attribute. |
| `alt` | string | Image `alt` attribute. |
| `title` | string | Image `title` attribute. |

**Link object:**

| Field | Type | Description |
|---|---|---|
| `index` | integer | Zero-based index among links in the message. |
| `href` | string | Link `href` attribute. |
| `text` | string | Trimmed text content of the link. |

### Notes

- The tool uses `document.querySelectorAll(selector)` and picks the **last** element in the NodeList — i.e., the most recently appended message in typical chat UIs.
- If `found` is `false`, the `html`, `text`, `images`, and `links` fields are absent from the response.
- Adjust the `selector` to match the container structure of whatever chat interface you're automating.

---

## 9. `wait_for`

Wait for a condition to be met before continuing. Supports two modes: **condition-based polling** and **pure sleep**.

| | |
|---|---|
| **CLI** | `browsectl run --type wait [--condition <COND>] [--selector <CSS>]` |
| **Internal command type** | `wait` |

### Parameters

| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `condition` | string | **Yes** *(unless using `ms`)* | — | The condition to wait for. See condition table below. |
| `selector` | string | Depends | — | CSS selector for element-based conditions. Required for all conditions except `url`, `title`, and `js`. |
| `value` | string | Depends | `""` | Expected value. Usage depends on condition: substring for `url`/`title`, JS expression for `js`, comparison text for text/value/attribute conditions. |
| `attribute` | string | Depends | `""` | Attribute name. Required for `attribute-equals` and `attribute-contains`. |
| `timeout` | integer | No | `20000` | Max time in ms to wait before failing with a timeout error. |
| `interval` | integer | No | `250` | Polling interval in ms between condition checks. |
| `ms` | integer | No | — | **Sleep mode:** simply delay for this many milliseconds. When provided, all other condition parameters are ignored. |

### Supported Conditions

| Condition | Requires `selector` | Requires `value` | Description |
|---|---|---|---|
| `visible` / `displayed` | Yes | No | Element is displayed (not `display:none`, `visibility:hidden`, or `opacity:0`). |
| `hidden` / `not-displayed` | Yes | No | Element is NOT displayed. |
| `exist` | Yes | No | Element exists in the DOM. |
| `not-exist` / `gone` | Yes | No | Element does NOT exist in the DOM. |
| `enabled` | Yes | No | Element is not disabled (`el.disabled === false`). |
| `disabled` | Yes | No | Element is disabled (`el.disabled === true`). |
| `text-contains` | Yes | Yes | Element's `textContent` contains the expected value. |
| `text-equals` | Yes | Yes | Element's trimmed `textContent` exactly equals the expected value. |
| `value-contains` | Yes | Yes | Element's `value` property contains the expected value. |
| `value-equals` | Yes | Yes | Element's `value` property exactly equals the expected value. |
| `attribute-equals` | Yes | Yes | Element's attribute (specified by `attribute`) exactly equals the expected value. |
| `attribute-contains` | Yes | Yes | Element's attribute (specified by `attribute`) contains the expected value. |
| `clickable` | Yes | No | Element is displayed, has non-zero dimensions, and is not disabled. |
| `not-clickable` | Yes | No | Element is NOT clickable (hidden, zero-sized, or disabled). |
| `url` | No | Yes | Current page URL contains the expected value as a substring. |
| `title` | No | Yes | Current page title contains the expected value as a substring. |
| `js` | No | Yes | Evaluate `value` as a JavaScript expression; wait until it returns a truthy value. |

### CLI Examples

```sh
# Pure sleep — wait 2 seconds
browsectl run --type wait --ms 2000

# Wait for element to be visible
browsectl run --type wait --condition visible --selector "#results-panel"

# Wait for element to disappear
browsectl run --type wait --condition gone --selector ".loading-spinner"

# Wait for URL to contain a path
browsectl run --type wait --condition url --value "/dashboard"

# Wait for text content
browsectl run --type wait --condition text-contains --selector ".status" --value "Complete"

# Wait for a JS expression to be truthy
browsectl run --type wait --condition js --value "document.readyState === 'complete'"

# Wait for an attribute value
browsectl run --type wait --condition attribute-equals --selector "#progress" --attribute "data-status" --value "done"

# Custom timeout and interval
browsectl run --type wait --condition visible --selector ".lazy-image" --timeout 30000 --interval 500
```

### Example Response — Condition Met

```json
{
  "ok": true,
  "type": "wait",
  "selector": "#results-panel",
  "condition": "visible"
}
```

### Example Response — Sleep

```json
{
  "ok": true,
  "type": "wait",
  "ms": 2000
}
```

### Example Response — Timeout (Error)

```json
{
  "ok": false,
  "error": "wait_command timed out after 20000ms: selector=#results-panel, condition=visible"
}
```

### Notes

- **Polling mechanism:** The condition is evaluated every `interval` ms (default 250ms) until it returns true or the `timeout` is reached.
- **Sleep mode** (`ms` parameter) takes priority: if `ms` is set, all condition parameters are ignored and the tool simply delays.
- For `url` and `title` conditions, the check is a **substring match** — the current URL or title must contain the `value` string.
- For the `js` condition, the `value` is executed as raw JavaScript via `driver.execute()`. It should return a truthy value when the condition is met.
- If the condition is not met within the timeout, the tool returns an error with details about which selector and condition failed.
- The `visible`/`displayed` check verifies that `display` is not `none`, `visibility` is not `hidden`, and `opacity` is not `0`.
- The `clickable` check combines visibility with non-zero bounding-rect dimensions and `!el.disabled`.

---

## Quick Reference

| CLI Command | `--type` | Required Params | Description |
|---|---|---|---|
| [open](#1-open) | `open` | `url` | Navigate to URL |
| [click](#2-click) | `click` | `selector` | Click element |
| [fill](#3-fill) | `fill` | `text` | Type text (char-by-char) |
| [paste](#4-paste) | `paste` | `text` | Paste text (fast) |
| [screenshot](#5-screenshot) | `screenshot` | `selector` | Capture element to PNG |
| [scroll](#6-scroll) | `scroll` | *(none)* | Scroll page/element |
| [get_title](#7-get_title) | `title` | *(none)* | Read page title |
| [get_last_message](#8-get_last_message) | `last-message-content` | *(none)* | Extract last chat message |
| [wait_for](#9-wait_for) | `wait` | `condition` or `ms` | Wait for condition/sleep |

---

## Common Patterns

### Navigate and Verify

```json
[
  { "type": "open", "url": "https://example.com/login" },
  { "type": "wait", "condition": "visible", "selector": "#login-form" },
  { "type": "title", "comment": "verify page loaded" }
]
```

### Fill a Form and Submit

```json
[
  { "type": "fill", "selector": "input[name='email']", "text": "user@example.com" },
  { "type": "fill", "selector": "input[name='password']", "text": "secret123" },
  { "type": "click", "selector": "button[type='submit']" },
  { "type": "wait", "condition": "url", "value": "/dashboard" }
]
```

### Scroll, Screenshot, and Read

```json
[
  { "type": "scroll", "direction": "down", "amount": 1200 },
  { "type": "wait", "ms": 500 },
  { "type": "screenshot", "selector": ".results-table", "path": "outputs/results.png" }
]
```

### Chat Interface Interaction

```json
[
  { "type": "paste", "selector": "textarea.chat-input", "text": "What is the weather today?" },
  { "type": "click", "selector": "button.send" },
  { "type": "wait", "condition": "visible", "selector": "[data-testid='message-block-container']:last-child" },
  { "type": "last-message-content" }
]
```
