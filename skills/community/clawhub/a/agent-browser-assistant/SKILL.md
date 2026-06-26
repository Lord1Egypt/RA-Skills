---
name: agent-browser-assistant
description: For browser automation tasks, web data scraping, form filling, page screenshots, UI testing, and more.
---

# Agent Browser Assistant

An intelligent browser control assistant providing browser automation, data scraping, and testing capabilities.

## Use Cases

Opening web pages, clicking/typing/scrolling, taking screenshots/recordings, extracting web content, exporting table data, automated form filling, batch operations, scheduled tasks, login authentication, UI testing, regression testing.

## Quick Start

Use the `browser` tool for all browser operations:

```python
# Open a web page
browser(action="open", url="https://example.com")

# Take a screenshot
browser(action="screenshot")

# Click an element
browser(action="act", kind="click", ref="button-submit")

# Type text
browser(action="act", kind="type", ref="input-username", text="user@example.com")

# Scroll the page
browser(action="act", kind="scroll", y=500)

# Get a page snapshot
browser(action="snapshot")
```

## Core Capabilities

### 1. Page Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| open | Open a specified URL | `action="open", url="..."` |
| snapshot | Get page structure | `action="snapshot"` |
| screenshot | Take a page screenshot | `action="screenshot"` |
| navigate | Navigate to a URL | `action="navigate", url="..."` |
| close | Close a tab | `action="close", targetId="..."` |

### 2. Element Interaction

Use the `act` operation for page interaction:

- **click**: Click an element (ref: element reference)
- **type**: Type text (ref: input reference, text: content)
- **press**: Press a keyboard key (key: key name)
- **hover**: Hover over an element
- **select**: Select from a dropdown
- **fill**: Fill a form (fields: field dictionary)
- **scroll**: Scroll the page (x/y: coordinates)

### 3. Data Scraping

Extract data from web pages:

```python
# Get a page snapshot to analyze structure
browser(action="snapshot")

# Extract table data - using selector
browser(action="act", kind="evaluate", selector="table.data", fn="Array.from(document.querySelectorAll('tr')).map(r => Array.from(r.querySelectorAll('td')).map(c => c.innerText))")
```

### 4. Automated Workflows

Automated form filling:

```python
browser(action="act", kind="fill", fields=[
    {"ref": "input-email", "value": "user@example.com"},
    {"ref": "input-password", "value": "password123"}
])
browser(action="act", kind="click", ref="button-login")
```

Batch operations:

```python
# Iterate through list items
for i in range(1, 6):
    browser(action="act", kind="click", ref=f"item-{i}")
```

### 5. Testing Capabilities

UI testing scenarios:

- Regression Testing: Verify that page functionality works correctly
- Performance Monitoring: Page load time
- Element Existence Check: Verify that key elements are visible

## Advanced Usage

### Waiting for Page Load

```python
browser(action="act", kind="wait", loadState="domcontentloaded", timeMs=5000)
```

### Handling Dialogs

```python
browser(action="dialog", kind="accept")  # Confirm
# or
browser(action="dialog", kind="dismiss")  # Cancel
```

### File Upload

```python
browser(action="upload", ref="input-file", paths=["C:/path/to/file.pdf"])
```

### PDF Export

```python
browser(action="pdf", path="C:/output/page.pdf")
```

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| profile | Browser profile | "openclaw" |
| target | Browser target | "sandbox" |
| slowly | Slow motion mode | false |
| timeoutMs | Timeout duration | 30000 |

## Common Selector Patterns

- Button: `button[type="submit"]`, `#submit-btn`
- Input: `input[name="email"]`, `#username`
- Link: `a[href*="login"]`
- Table: `table.data tr`
- List: `.item-list li`

## Notes

1. Use `snapshot` to get page structure before performing element operations
2. Dynamic content may require waiting for it to finish loading
3. For logged-in state operations, use `profile="user"` to reuse the user's browser
4. For large-scale data scraping, consider pagination to avoid timeouts