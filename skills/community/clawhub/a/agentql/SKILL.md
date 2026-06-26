---
name: agentql
description: Web scraping and browser automation using AgentQL — query any webpage with natural language to extract structured data, interact with elements, and automate browser tasks. Use when asked to scrape, extract data from, or automate interactions on a webpage using natural language queries.
---

# AgentQL Skill

AgentQL lets you query webpages with natural language to extract structured data and automate browser interactions. It uses Playwright under the hood.

## Setup

AgentQL requires an API key. Set it as an environment variable:
```bash
export AGENTQL_API_KEY="your-api-key"
```
Get a free API key at https://dev.agentql.com

## Quick Start (Python)

```python
import agentql
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = agentql.wrap(browser.new_page())

    page.goto("https://example.com")

    # Query with natural language
    response = page.query_data("""
    {
        title
        main_heading
        description
    }
    """)

    print(response)
    browser.close()
```

## Write and Run a Script

```bash
# Create a new script template
agentql new-script scraper.py

# Run it
python3 scraper.py
```

## Common Patterns

### Extract structured data
```python
response = page.query_data("""
{
    products[] {
        name
        price
        rating
    }
}
""")
```

### Interact with elements
```python
response = page.query_elements("""
{
    search_box
    submit_button
}
""")
response.search_box.fill("query")
response.submit_button.click()
```

### Headless scraping
```python
browser = p.chromium.launch(headless=True)
```

### With existing page (connected to running browser)
```python
browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")  # Brave/Chrome
page = agentql.wrap(browser.contexts[0].pages[0])
```

## CLI
```bash
agentql doctor          # Check setup
agentql new-script      # Generate template script
```

## Notes
- API key required: https://dev.agentql.com (free tier available)
- Scripts run via: `python3 script.py`
- Can connect to the running Brave browser via CDP (port 9222)
