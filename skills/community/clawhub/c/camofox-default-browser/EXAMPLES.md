---
type: Skill Examples
title: "Camoufox Default Browser — Usage Examples"
timestamp: "2026-07-30T13:06:00+07:00"
---

# Camoufox Default Browser — Comprehensive Usage Examples

This file provides practical, copy-ready patterns for the `camofox_*` tool suite. Each example includes the exact tool calls and context on when to apply that pattern.

---

## 1. Basic Navigation

### Open Tab → Navigate → Snapshot → Interact → Close

The canonical lifecycle:

```text
1. Create tab (optional initial URL)
2. Navigate to target page
3. Snapshot to get element refs (e1, e2, …)
4. Click/type/select using those refs
5. Take screenshot for visual proof
6. Close tab to free resources
```

**Example:** Browse a news article and extract the headline.

```python
# Step 1: Create a new tab with an optional start URL
tab = camofox_create_tab(url="https://example.com")

# Step 2: Navigate to target
camofox_navigate(tabId=tab["tabId"], url="https://example.com/article/123")

# Step 3: Wait for load, then snapshot
snapshot = camofox_snapshot(tabId=tab["tabId"])
# snapshot returns accessibility tree with refs like:
# e1 — "Welcome to Example Domain" (heading)
# e2 — "More information..." (paragraph)

# Step 4: Click something if needed
camofox_click(tabId=tab["tabId"], ref="e3")

# Step 5: Screenshot for verification
camofox_screenshot(tabId=tab["tabId"])

# Step 6: Clean up
camofox_close_tab(tabId=tab["tabId"])
```

**When to use:** Almost every workflow starts here. Use `camofox_navigate` instead of passing URL to `create_tab` when you need clean navigation state (avoids intermediate redirect pages). Always close tabs after work to avoid resource leaks (~200 MB per active session).

---

## 2. Search Macros

Camoufox supports search macros that handle login-aware, anti-bot Google/Youtube/Amazon searches automatically.

### Google Search

```python
tab = camofox_create_tab()
camofox_navigate(
    tabId=tab["tabId"],
    macro="@google_search",
    query="best Italian restaurant Jakarta"
)
snapshot = camofox_snapshot(tabId=tab["tabId"])
```

Use when you need organic search results without triggering CAPTCHA or bot detection. The macro bypasses standard Playwright blocking that Google applies to headless browsers.

### YouTube Search

```python
tab = camofox_create_tab()
camofox_navigate(
    tabId=tab["tabId"],
    macro="@youtube_search",
    query="tutorial React hooks 2026"
)
snapshot = camofox_snapshot(tabId=tab["tabId"])
```

Use for video research, content discovery, or competitor analysis. Results include video titles, channel names, view counts, and durations in the snapshot.

### Amazon Product Search

```python
tab = camofox_create_tab()
camofox_navigate(
    tabId=tab["tabId"],
    macro="@amazon_search",
    query="mechanical keyboard wireless"
)
snapshot = camofox_snapshot(tabId=tab["tabId"])
```

Use for price comparison, product research, or availability checks. Results include pricing, ratings, and shipping info. Note: Amazon is heavily guarded — Camoufox's fingerprint management makes this viable where standard browser tools fail.

**Available macros:** `@google_search`, `@youtube_search`, `@amazon_search`, `@reddit_search`, `@wikipedia_search`, `@twitter_search`, `@yelp_search`, `@spotify_search`, `@netflix_search`, `@linkedin_search`, `@instagram_search`, `@tiktok_search`, `@twitch_search`.

---

## 3. Form Automation

### Login Form Fill + Submit

```python
tab = camofox_create_tab()
camofox_navigate(tabId=tab["tabId"], url="https://app.example.com/login")

# Snapshot to identify field refs
snap = camofox_snapshot(tabId=tab["tabId"])
# Suppose: e2 = email input, e3 = password input, e4 = submit button

# Method A: Type then click
camofox_type(tabId=tab["tabId"], ref="e2", text="user@example.com")
camofox_type(tabId=tab["tabId"], ref="e3", text="secretpass123")
camofox_click(tabId=tab["tabId"], ref="e4")

# Method B: Type + press Enter (faster for single-field submission)
camofox_type(tabId=tab["tabId"], ref="e2", text="user@example.com", pressEnter=True)
```

**When to use Method B:** When the form has a single actionable field or when pressing Enter triggers the natural form submission event. Avoid on multi-field forms where not all fields are filled.

### Multi-Step Form Handling

```python
# Step 1: Fill first page
camofox_navigate(tabId=tab["tabId"], url="https://form.example.com/step1")
snap = camofox_snapshot(tabId=tab["tabId"])
camofox_type(tabId=tab["tabId"], ref="e3", text="John Doe")
camofox_click(tabId=tab["tabId"], ref="e7")  # Next button

# Step 2: Take snapshot again — refs may differ!
snap2 = camofox_snapshot(tabId=tab["tabId"])
camofox_type(tabId=tab["tabId"], ref="e2", text="john@example.com")
camofox_type(tabId=tab["tabId"], ref="e5", text="+62812xxxxxxx")
camofox_click(tabId=tab["tabId"], ref="e9")  # Complete button

# Verify completion
camofox_screenshot(tabId=tab["tabId"])
```

**Critical rule:** Refs (e1, e2, e3) are **per-page**. After navigating or clicking to next step, always re-snapshot — old refs become stale. Never cache refs across steps.

---

## 4. Cookie Import Workflow

Export cookies from your local browser as Netscape-format (`cookies.txt`), then import into Camoufox for authenticated sessions.

### Export Cookies Locally

From Chrome/Firefox DevTools Console:

```javascript
// Chrome: paste into DevTools Console
var cookieString = document.cookie;
console.log(cookieString);
```

Or use a browser extension to export full Netscape format. Save as `/tmp/cookies.txt`.

### Import into Camoufox

```python
# Create a fresh tab targeting the same domain
tab = camofox_create_tab()

# Import cookies file
camofox_import_cookies(
    cookiesPath="/tmp/cookies.txt",
    domainSuffix=".example.com"  # optional: restrict to specific domain
)

# Now navigate — you're authenticated!
camofox_navigate(tabId=tab["tabId"], url="https://app.example.com/dashboard")
snapshot = camofox_snapshot(tabId=tab["tabId"])
```

**When to use:** LinkedIn automation, GitHub private repos, any site requiring login where interactive login via UI would trigger security prompts. Also useful for preserving session across multiple automation runs.

**Security note:** Imported cookies are bearer tokens. They grant full account access. Only import cookies you own or are authorized to use. Delete the cookie file after import when done.

---

## 5. Screenshot Capture

### Standard Screenshot

```python
tab = camofox_create_tab(url="https://news.example.com")
camofox_snapshot(tabId=tab["tabId"])  # snapshots include embedded screenshot by default
camofox_screenshot(tabId=tab["tabId"])  # explicit standalone screenshot
```

### Scroll Before Screenshot (for long pages)

```python
tab = camofox_create_tab(url="https://product.example.com")
camofox_scroll(tabId=tab["tabId"], direction="down", amount=2000)
camofox_screenshot(tabId=tab["tabId"])
```

Use this pattern before capturing pages with infinite scroll or lazy-loaded content. Scroll enough to trigger loading, wait briefly (via another action call), then screenshot.

### Screenshot for Verification

Always take a screenshot before declaring task completion. Attach it to your report so the user can visually verify the result. This is part of the RPDV verification gate — don't just say "done," show evidence.

---

## 6. JavaScript Execution

### Extract Page Data

```python
tab = camofox_create_tab(url="https://example.com")
result = camofox_evaluate(
    tabId=tab["tabId"],
    expression="document.title"
)

# Extract all links
result = camofox_evaluate(
    tabId=tab["tabId"],
    expression="[...document.querySelectorAll('a')].map(a => ({href: a.href, text: a.textContent.trim()}))"
)
```

### Modify Page Content

```python
# Override clipboard for testing
camofox_evaluate(
    tabId=tab["tabId"],
    expression="navigator.clipboard.writeText = async (text) => { window._clipContent = text; }"
)
```

### Handle Async Operations

```python
# Wait for dynamic content to load, then extract
result = camofox_evaluate(
    tabId=tab["tabId"],
    expression="(async () => { await new Promise(r => setTimeout(r, 2000)); return document.querySelector('.lazy-loaded').textContent; })()"
)
```

Use `evaluate` sparingly — snapshot usually gives you what you need. Reserve `evaluate` for complex data extraction, DOM manipulation, or when the accessibility tree doesn't expose the information you need.

---

## 7. Multi-Tab Workflow

### Open, Work, Collect, Close

```python
# Step 1: Open multiple tabs
tab1 = camofox_create_tab(url="https://google.com/search?q=topic+a")
tab2 = camofox_create_tab(url="https://google.com/search?q=topic+b")
tab3 = camofox_create_tab(url="https://google.com/search?q=topic+c")

# Step 2: Work on them sequentially (one at a time, since each tab operates independently)
snap1 = camofox_snapshot(tabId=tab1["tabId"])
snap2 = camofox_snapshot(tabId=tab2["tabId"])
snap3 = camofox_snapshot(tabId=tab3["tabId"])

# Step 3: Collect results
results = [snap1, snap2, snap3]

# Step 4: Clean up all tabs
camofox_close_tab(tabId=tab1["tabId"])
camofox_close_tab(tabId=tab2["tabId"])
camofox_close_tab(tabId=tab3["tabId"])
```

### List and Manage Existing Tabs

```python
# Check what's already open
tabs = camofox_list_tabs()
# Returns list of {tabId, url, title} objects

# Find a specific tab by URL pattern
target_tab = None
for t in tabs:
    if "dashboard" in t["url"]:
        target_tab = t["tabId"]
        break

if target_tab:
    camofox_screenshot(tabId=target_tab)
```

**When to use:** Bulk research (searching multiple queries simultaneously), batch scraping, comparing content across pages, or monitoring multiple sources. Remember: each tab consumes ~200 MB RAM. Don't open more than necessary.

---

## 8. Error Handling & Fallback Patterns

### Retry on Blocking / Loading Timeout

```python
import time

def navigate_with_retry(tab_id, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            camofox_navigate(tabId=tab_id, url=url)
            # Brief wait for page to start rendering
            camofox_snapshot(tabId=tab_id)  # this will raise if page is empty/blocked
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)  # back off between retries
                continue
            return False
    return False

tab = camofox_create_tab()
success = navigate_with_retry(tab["tabId"], "https://site.example.com/page")
if not success:
    camofox_close_tab(tabId=tab["tabId"])
    # Fall back to web_fetch or built-in browser
```

### Fallback to Built-In Browser Tool

When Camoufox encounters persistent issues (server crash, unsupported protocol, etc.):

```python
# Primary: Camoufox
try:
    tab = camofox_create_tab()
    camofox_navigate(tabId=tab["tabId"], url="https://example.com")
    camofox_snapshot(tabId=tab["tabId"])
except Exception:
    # Fallback: built-in browser tool (Playwright/Chromium)
    # Requires profile setup but works for non-guarded sites
    browser(action="navigate", url="https://example.com")
    browser(action="snapshot", compact=True)
```

### Graceful Degradation Strategy

```
Priority chain:
1. camofox_* tools — anti-bot protected, best for guarded sites
2. web_fetch — lightweight, no browser needed (URL-only, no JS)
3. browser tool — Playwright/Chromium fallback
4. web_search — last resort, returns snippets only

Rule: Start with camofox. If it fails due to server issues (not blocking),
fall through the chain. Document which level worked for future reference.
```

---

## Quick Reference: Tool Decision Matrix

| Situation | Recommended Tool(s) |
|-----------|-------------------|
| Google search, login-required sites | `camofox_create_tab` + `@google_search` macro |
| Simple URL content (no JS render needed) | `web_fetch` (skip browser entirely) |
| Clicking buttons, filling forms | `camofox_snapshot` → `camofox_click/type` |
| Extracting structured data | `camofox_evaluate` with DOM selectors |
| Verifying page state | `camofox_screenshot` + attach to report |
| Bulk/research operations | Multiple `camofox_create_tab` + sequential processing |
| Authenticated access | `camofox_import_cookies` before navigation |
| Server unavailable / crashing | Fallback to `browser` tool or `web_fetch` |

---

*Generated 2026-07-30. Last reviewed against SKILL.md v1.1.0.*
