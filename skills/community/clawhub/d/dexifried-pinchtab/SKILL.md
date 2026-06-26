---
name: pinchtab
description: Browser automation via HTTP API. Use for headless browser control, web automation, form filling, data extraction, and interactive element interaction. Supports launching instances, navigating pages, taking screenshots, extracting page structure, and clicking elements.
---

# PinchTab Skill

## Description
PinchTab is an HTTP server that provides programmatic control over a browser. It supports launching browser instances, navigating to pages, extracting page structure, and interacting with elements like buttons or forms.

### When to Use
Use this skill for tasks like:
- Automating browser workflows (e.g., logins, form submissions).
- Extracting data or snapshots from web pages.
- Testing interactive web elements.

## Quick Start
Below is a guide to using the PinchTab skill:

### 1. Launching a Browser Instance
You can launch a new browser instance via the API:

```bash
bash scripts/launch_browser.sh
```

### 2. Navigating to a URL
Navigate to a URL with the following command:

```bash
bash scripts/navigate_to_url.sh https://example.com
```

### 3. Extracting Page Snapshot
Get the page structure and save it locally:

```bash
bash scripts/get_page_snapshot.sh
```

### 4. Clicking an Element
Simulate a button click on a webpage:

```bash
bash scripts/click_element.sh "<css_selector>"
```

### 5. Taking Screenshots (Base64 Decode + Send to Telegram)
Capture a screenshot, decode the base64, and send to Telegram:

**Bash:**
```bash
export PINCHTAB_TOKEN="your_token"
export TELEGRAM_BOT_TOKEN="your_bot_token"
bash scripts/screenshot_and_send.sh <tab_id> <telegram_chat_id>
```

**Python (more features):**
```bash
export PINCHTAB_TOKEN="your_token"
python3 scripts/decode_screenshot.py <tab_id> \
  --output /path/to/screenshot.jpg \
  --send-telegram <chat_id> \
  --caption "My screenshot"
```

## Example: Google Homepage
PinchTab successfully navigated to Google and extracted the page structure:

![Google Screenshot](assets/google-screenshot.png)

This demonstrates:
- Browser launch and page navigation
- Interactive element extraction (About, Store, Advertising links, etc.)
- Ready for automation (clicking, form filling, data extraction)

## Documentation
Check the `references/` folder for detailed API documentation, common workflows, and troubleshooting tips.