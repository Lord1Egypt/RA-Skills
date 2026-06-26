# Common Browser Automation Patterns

## Login Flow

```python
from playwright.sync_api import sync_playwright

def login_flow(url, username, password, username_selector, password_selector, submit_selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.fill(username_selector, username)
        page.fill(password_selector, password)
        page.click(submit_selector)
        page.wait_for_load_state("networkidle")
        return {"title": page.title(), "url": page.url}

# Usage
result = login_flow(
    "https://site.com/login",
    "user@example.com",
    "secret",
    "#username",
    "#password",
    "button[type=submit]"
)
```

## Search and Extract Results

```python
def search_and_extract(search_url, query, search_input, search_button, results_selector):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)
        page.fill(search_input, query)
        page.click(search_button)
        page.wait_for_selector(results_selector, timeout=10000)
        results = page.query_selector_all(results_selector)
        return [
            {
                "text": el.inner_text()[:200],
                "href": el.get_attribute("href")
            }
            for el in results[:20]
        ]
```

## Infinite Scroll Pagination

```python
def scroll_and_extract(page, item_selector, max_scrolls=10):
    """Scroll to load more items, then extract."""
    seen = set()
    items = []
    for _ in range(max_scrolls):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        els = page.query_selector_all(item_selector)
        for el in els:
            href = el.get_attribute("href") or ""
            if href not in seen:
                seen.add(href)
                items.append({"text": el.inner_text()[:200], "href": href})
        # Check if "no more" indicator appears
        if page.query_selector(".no-more-results"):
            break
    return items
```

## Modal Dialog

```python
def handle_modal(page, trigger_selector, modal_selector, action_selector=None):
    """Click trigger, wait for modal, optionally click action inside."""
    page.click(trigger_selector)
    page.wait_for_selector(modal_selector, timeout=5000)
    if action_selector:
        page.click(action_selector)
        page.wait_for_selector(modal_selector, state="hidden")
```

## File Download

```python
def download_with_browser(url, download_selector, save_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        with browser.expect_download() as dl_info:
            page.goto(url)
            page.click(download_selector)
        download = dl_info.value
        download.save_as(save_path)
```

## Screenshot Comparison

```python
def screenshot_comparison(url1, url2, selector, out1, out2):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for i, url in enumerate([url1, url2]):
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.locator(selector).screenshot(
                path=[out1, out2][i]
            )
            page.close()
```

## Waiting for Network Idle

```python
# After form submission
page.click("button[type=submit]")
page.wait_for_load_state("networkidle", timeout=15000)

# After navigation
page.goto(url)
page.wait_for_response(lambda r: "api/results" in r.url)

# Specific element to appear
page.wait_for_selector("#results-loaded", state="visible", timeout=15000)
```

## Multi-Tab Flow

```python
def multi_tab():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page1 = browser.new_page()
        page1.goto("https://site.com/page1")
        # Open link in new tab
        with browser.contexts()[0].expect_page() as new_page_info:
            page1.click("a.open-in-new-tab")
        page2 = new_page_info.value
        page2.wait_for_load_state("load")
        # Work with both tabs
        results = page2.content()
        page1.click("button.next")
        browser.close()
```

## Handling Anti-Bot

```python
BROWSER_ARGS = [
    '--disable-blink-features=AutomationControlled',
    '--disable-dev-shm-usage',
    '--no-sandbox',
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
]

def stealth_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=BROWSER_ARGS)
        # Remove webdriver property
        page = browser.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        return page
```

## Error Recovery

```python
def robust_navigate(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=15000)
                page.wait_for_load_state("domcontentloaded")
                return {"success": True, "title": page.title()}
        except Exception as e:
            if attempt == max_retries - 1:
                return {"success": False, "error": str(e)}
```

## Conditional Extract

```python
def extract_if_exists(page, selectors_list):
    """Try multiple selectors, return first match."""
    for selector in selectors_list:
        try:
            el = page.wait_for_selector(selector, timeout=3000)
            return {"found": selector, "text": el.inner_text()[:500]}
        except:
            continue
    return {"found": None}
```
