# Selector Syntax Reference

browsectl extends standard CSS selectors with a custom **text-matching** extension: `::text(/regex/flags)`. This document is the canonical reference for the selector syntax accepted by all element-targeting commands.

---

## Quick Syntax Overview

```
CSS_SELECTOR                        ← plain CSS selector
CSS_SELECTOR::text(/PATTERN/FLAGS)  ← CSS + text regex filter
```

| Component | Required | Description |
|---|---|---|
| `CSS_SELECTOR` | **Yes** | Any valid CSS selector (`querySelectorAll`-compatible) |
| `::text(` | No | Marker that begins the text-matching extension |
| `/PATTERN/` | If `::text(` is present | JavaScript regex pattern delimited by `/` |
| `FLAGS` | No | Zero or more regex flag characters after the closing `/` |
| `)` | If `::text(` is present | Closing paren — must be the last character |

---

## Standard CSS Selectors

All selectors that work with `document.querySelectorAll()` are supported as-is.

| Selector | What It Matches |
|---|---|
| `button` | Any `<button>` element (tag name) |
| `.class-name` | Any element with `class="class-name"` |
| `#element-id` | The element with `id="element-id"` |
| `div.card > h2` | An `<h2>` that is a direct child of `<div class="card">` |
| `input[type="text"]` | An `<input>` with `type="text"` (attribute selector) |
| `[data-testid="msg"]` | Any element with a matching `data-testid` attribute |
| `div.tab:nth-child(2)` | The second child `<div class="tab">` (pseudo-class) |
| `ul.menu li:first-child a` | The link inside the first `<li>` of `<ul class="menu">` |

These are passed directly to `querySelectorAll` with no transformation.

---

## Extended Text Regex Syntax — `::text()`

### Format

```
CSS_SELECTOR::text(/PATTERN/FLAGS)
```

The `::text()` pseudo-extension **filters** the elements matched by the CSS part, keeping only those whose `textContent` matches a JavaScript regular expression.

### Parsing Rules

1. The parser scans for the **last** occurrence of the marker `::text(` in the selector string.
2. Everything **before** `::text(` is extracted as the CSS selector.
3. The CSS part must be **non-empty** — `::text(/foo/)` alone is invalid.
4. Inside the parentheses must be a **JavaScript regex literal**: `/pattern/flags`.
5. The pattern between the `/` delimiters must be **non-empty**.
6. The closing `)` must be the **last character** of the selector string.
7. Flag characters (after the closing `/`) must be ASCII-alphabetic.

### Supported Regex Flags

| Flag | Name | Effect |
|---|---|---|
| `i` | Case-insensitive | `/submit/i` matches "Submit", "SUBMIT", "submit" |
| `g` | Global | Rarely needed — matching uses `.test()`, not `.match()` |
| `m` | Multiline | `^` and `$` match line boundaries, not just string boundaries |
| `s` | dotAll | `.` matches newline characters as well |

Flags can be combined: `/pattern/ims`.

### How It Works Internally

When a selector contains `::text()`, browsectl executes the following JavaScript in the browser:

1. `document.querySelectorAll(cssSelector)` collects all elements matching the CSS part.
2. For each element, the trimmed `element.textContent` is tested with `new RegExp(pattern, flags).test(text)`.
3. The **first** element that passes the regex test is returned.
4. If **no** element matches, the command retries according to the polling interval until the timeout expires.

When a `scope` is also provided, step 1 becomes `scopeElement.querySelectorAll(cssSelector)`.

---

## Examples

### Basic Text Matching

| Selector | Meaning |
|---|---|
| `button::text(/Submit/)` | A `<button>` whose text contains "Submit" (case-sensitive) |
| `button::text(/Submit/i)` | Same, but case-insensitive |
| `a.nav-link::text(/^Home$/)` | An `<a class="nav-link">` whose text is **exactly** "Home" |
| `.menu-item::text(/video/i)` | A `.menu-item` containing "video" in any case |

### Regex Patterns

| Selector | Meaning |
|---|---|
| `div.card::text(/Price: \$\d+/)` | A `.card` containing a price like "Price: $42" |
| `span::text(/\d{4}-\d{2}-\d{2}/)` | A `<span>` containing a date like "2025-01-15" |
| `td::text(/^(Active\|Pending)$/)` | A `<td>` whose text is exactly "Active" or "Pending" |
| `li::text(/step\s+\d+/i)` | An `<li>` containing "Step 1", "step 22", etc. |

### Unicode / Non-Latin Text

| Selector | Meaning |
|---|---|
| `div.tab::text(/^视频$/)` | A tab whose text is exactly "视频" |
| `button::text(/Hébergement/i)` | A button containing the French word |
| `span::text(/\p{L}+/u)` | A span containing Unicode letters (requires `u` flag in browser) |

### Complex CSS + Text

| Selector | Meaning |
|---|---|
| `div.sidebar ul > li a::text(/Settings/)` | A deeply nested link containing "Settings" |
| `[data-testid="row"] td:nth-child(3)::text(/\d+%/)` | Third column of a test-id row, containing a percentage |
| `form#login button[type="submit"]::text(/Log in/i)` | A specific submit button filtered by its label |

---

## Scope Parameter

Many commands accept a **`scope`** parameter — a plain CSS selector that limits where elements are searched.

| Parameter | Type | Description |
|---|---|---|
| `selector` | string | The element to find (CSS or CSS + `::text()`) |
| `scope` | string | CSS selector for the container to search within |

When `scope` is provided:

1. `document.querySelector(scope)` finds the scope root element.
2. The `selector` is resolved **within** the scope root's descendants only.
3. For `click`, fallback strategies are also restricted to the scope subtree.
4. If the scope element itself is not found, the command fails immediately with `"scope element not found"`.

### Scope Examples

```json
{ "selector": "button.submit", "scope": "form#login-form" }
```

```json
{ "selector": "a::text(/Next Page/i)", "scope": "nav.pagination" }
```

```sh
browsectl run --type click --selector ".item-action" --scope ".sidebar"
```

> **Note:** The `scope` parameter is always a **plain CSS selector** — it does not support `::text()`.

---

## Escaping Guide

Because selectors flow through multiple layers (your editor → shell or JSON → browsectl parser → JavaScript `RegExp`), backslash escaping requires care.

### In CLI (Shell)

Use **single quotes** around the selector to prevent shell interpolation:

```sh
# Single quotes — safest, no escaping needed for regex:
browsectl run --type click --selector 'button::text(/Submit/i)'

# Backslashes in patterns — single quotes pass them through:
browsectl run --type click --selector 'span::text(/\d{4}-\d{2}-\d{2}/)'

# Dollar signs — single quotes prevent shell expansion:
browsectl run --type click --selector 'div::text(/Price: \$\d+/)'
```

If you must use double quotes in shell, escape backslashes:

```sh
browsectl run --type click --selector "span::text(/\\d{4}-\\d{2}-\\d{2}/)"
```

### In JSON (Batch Files)

JSON requires **double-escaping** backslashes — once for JSON string parsing, once for the regex:

```json
{
  "type": "click",
  "selector": "span::text(/\\d{4}-\\d{2}-\\d{2}/)"
}
```

```json
{
  "type": "click",
  "selector": "div.card::text(/Price: \\$\\d+/)"
}
```

| You Want the Regex | JSON String Value |
|---|---|
| `/\d+/` | `"span::text(/\\d+/)"` |
| `/\$\d+/` | `"div::text(/\\$\\d+/)"` |
| `/foo\/bar/` | `"a::text(/foo\\/bar/)"` |
| `/\bword\b/i` | `"p::text(/\\bword\\b/i)"` |

---

## Supported Commands

The selector syntax (plain CSS and CSS + `::text()`) is accepted by these commands:

| Command | Selector Parameters | Notes |
|---|---|---|
| `click` | `selector`, `scope`, `fallback` | `fallback` can also be a CSS selector string |
| `fill` | `selector`, `scope` | `selector` is optional — omit to target focused element |
| `paste` | `selector`, `scope` | `selector` is optional — omit to target focused element |
| `screenshot` | `selector`, `scope` | Captures the matched element as a PNG |
| `scroll` | `selector` | Optional — omit to scroll the viewport |
| `wait_for` | `selector` | Used with `visible`, `hidden`, `exist` conditions |
| `get_last_message` | `selector` | Container selector for message extraction |

---

## Error Messages

| Error | Cause |
|---|---|
| `"selector cannot be empty"` | An empty string was passed as the selector |
| `"CSS part is empty before ::text("` | Nothing before `::text(` — e.g. `::text(/foo/)` |
| `"expected ')' at end"` | Missing closing paren after the regex literal |
| `"expected /pattern/flags"` | Content inside `::text()` is not a valid regex literal |
| `"missing closing '/' in /pattern/flags"` | No closing `/` found in the regex |
| `"pattern cannot be empty"` | Empty pattern: `::text(//i)` |
| `"flags must be alphabetic"` | Non-letter characters in flags position |
| `"no element matched selector with text regex: ..."` | The CSS + regex combo matched zero elements |
| `"scope element not found: ..."` | The `scope` CSS selector matched nothing |
| `"wait_find timed out after Nms ..."` | Element not found within the timeout window |

---

## Tips & Best Practices

1. **Start with plain CSS** — only add `::text()` when multiple elements share the same CSS selector and you need to disambiguate by content.

2. **Prefer exact matches** — use `^` and `$` anchors (`/^Submit$/`) to avoid matching unintended elements whose text happens to contain your pattern.

3. **Use case-insensitive** — the `i` flag (`/submit/i`) is more resilient to UI copy changes.

4. **Keep scope narrow** — a `scope` parameter reduces the search space and avoids matching duplicates in other parts of the page.

5. **Test selectors in DevTools** — run `document.querySelectorAll("your-css")` in the browser console first, then add `::text()` filtering if needed.

6. **Watch for whitespace** — `textContent` is trimmed before matching, but inner whitespace is preserved. Use `\s+` in patterns when spacing may vary.
