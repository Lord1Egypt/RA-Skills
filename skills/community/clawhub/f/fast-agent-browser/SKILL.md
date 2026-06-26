# Agent Browser Skill

**Fast, Python-based browser automation CLI for AI agents**

---

## Overview

Agent Browser is a browser automation tool designed for AI agents. It provides a simple CLI interface to control web browsers using Playwright.

---

## Features

- Fast CLI for browser automation
- AI-friendly snapshot command
- Full page interaction (click, fill, type, etc.)
- Semantic element finding (role, text, label, etc.)
- Smart waiting (element, text, URL, network)
- Screenshot and PDF support
- File upload support
- JavaScript execution
- Cookie and storage management

---

## Installation

```bash
cd ~/.openclaw/workspace/skills/agent-browser

# Install Python dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
python3 agent_browser.py install
```

---

## Basic Usage

### Open a URL

```bash
python3 agent_browser.py open https://example.com
```

### Get Page Snapshot

```bash
# Full accessibility tree
python3 agent_browser.py snapshot

# Interactive elements only
python3 agent_browser.py snapshot -i

# Compact output
python3 agent_browser.py snapshot -c
```

### Interact with Elements

```bash
# Click element
python3 agent_browser.py click "#submit"

# Fill input field
python3 agent_browser.py fill "#email" "test@example.com"

# Type text
python3 agent_browser.py type "#search" "query"
```

### Get Information

```bash
# Get text content
python3 agent_browser.py get_text "#title"

# Get HTML
python3 agent_browser.py get_html "#content"

# Get current URL
python3 agent_browser.py get_url

# Get page title
python3 agent_browser.py get_title
```

### Take Screenshot

```bash
# Normal screenshot
python3 agent_browser.py screenshot page.png

# Full page screenshot
python3 agent_browser.py screenshot page.png --full
```

### Wait for Elements

```bash
# Wait for element
python3 agent_browser.py wait "#loader" --state hidden

# Wait for text
python3 agent_browser.py wait --text "Welcome"

# Wait for network idle
python3 agent_browser.py wait --load networkidle
```

### Find Elements

```bash
# Find by role
python3 agent_browser.py find --role button --name "Submit"

# Find by text
python3 agent_browser.py find --text "Sign In"

# Find by label
python3 agent_browser.py find --label "Email"
```

### Close Browser

```bash
python3 agent_browser.py close
```

---

## Advanced Usage

### Form Automation

```bash
# Fill form
python3 agent_browser.py fill "#name" "John Doe"
python3 agent_browser.py fill "#email" "john@example.com"

# Select dropdown
python3 agent_browser.py select "#country" "US"

# Check checkbox
python3 agent_browser.py check "#terms"

# Submit form
python3 agent_browser.py click "#submit"
```

### File Upload

```bash
python3 agent_browser.py upload "#file" file1.txt file2.txt
```

### Scroll Page

```bash
# Scroll down
python3 agent_browser.py scroll down 500

# Scroll up
python3 agent_browser.py scroll up 100

# Scroll element
python3 agent_browser.py scroll down 200 --selector "#main"
```

### Execute JavaScript

```bash
python3 agent_browser.py eval "document.title"
python3 agent_browser.py eval "window.innerWidth"
```

### Get Element Info

```bash
# Get input value
python3 agent_browser.py get_value "#email"

# Get attribute
python3 agent_browser.py get_attr "#link" href

# Get bounding box
python3 agent_browser.py get_box "#element"

# Count elements
python3 agent_browser.py count ".item"
```

---

## Options

### Global Options

```bash
# Headless mode (default)
python3 agent_browser.py open https://example.com --headless

# Show browser window
python3 agent_browser.py open https://example.com --headed

# Custom viewport
python3 agent_browser.py open https://example.com --viewport 1920x1080
```

### Snapshot Options

```bash
# Interactive elements only
python3 agent_browser.py snapshot -i

# Compact output
python3 agent_browser.py snapshot -c

# Limit depth
python3 agent_browser.py snapshot -d 3
```

### Screenshot Options

```bash
# Full page
python3 agent_browser.py screenshot page.png --full

# Annotate with labels
python3 agent_browser.py screenshot page.png --annotate
```

---

## AI Workflow

### Optimal AI Agent Workflow

```bash
# 1. Navigate to page
python3 agent_browser.py open https://example.com

# 2. Get snapshot with refs
python3 agent_browser.py snapshot -i

# 3. AI identifies target elements

# 4. Execute actions
python3 agent_browser.py click "@e1"
python3 agent_browser.py fill "@e2" "input text"

# 5. Get new snapshot if page changed
python3 agent_browser.py snapshot -i
```

---

## Examples

### Example 1: Login Flow

```bash
# Open login page
python3 agent_browser.py open https://example.com/login

# Fill credentials
python3 agent_browser.py fill "#email" "user@example.com"
python3 agent_browser.py fill "#password" "secret"

# Click submit
python3 agent_browser.py click "#submit"

# Wait for dashboard
python3 agent_browser.py wait --url "**/dashboard"

# Take screenshot
python3 agent_browser.py screenshot dashboard.png
```

### Example 2: Data Extraction

```bash
# Open page
python3 agent_browser.py open https://example.com/products

# Get product titles
python3 agent_browser.py get_text ".product-title"

# Get prices
python3 agent_browser.py get_text ".product-price"

# Take screenshot
python3 agent_browser.py screenshot products.png
```

### Example 3: Form Submission

```bash
# Open form
python3 agent_browser.py open https://example.com/contact

# Fill fields
python3 agent_browser.py fill "#name" "John Doe"
python3 agent_browser.py fill "#email" "john@example.com"
python3 agent_browser.py fill "#message" "Hello!"

# Select dropdown
python3 agent_browser.py select "#subject" "Support"

# Check terms
python3 agent_browser.py check "#terms"

# Submit
python3 agent_browser.py click "#submit"

# Wait for confirmation
python3 agent_browser.py wait --text "Thank you"
```

---

## Security Notes

### Input Sanitization

All user inputs are sanitized before use:

- Selectors are validated
- Text inputs are escaped
- URLs are validated
- JavaScript execution requires explicit command

### Safe Commands

All commands are safe and do not execute arbitrary code:

- No shell injection possible
- No command injection possible
- All inputs are validated

### Best Practices

1. Use headless mode for automation
2. Validate all inputs before use
3. Use explicit selectors
4. Close browser when done
5. Use timeouts for waits

---

## Troubleshooting

### Browser Does Not Open

```bash
# Install Playwright browsers
python3 agent_browser.py install
```

### Element Not Found

```bash
# Check if element exists
python3 agent_browser.py is_visible "#element"

# Get snapshot to verify
python3 agent_browser.py snapshot -i
```

### Screenshot Is Blank

```bash
# Wait for page to load
python3 agent_browser.py wait --load networkidle

# Take screenshot after wait
python3 agent_browser.py screenshot page.png
```

### Timeout Errors

```bash
# Increase timeout
python3 agent_browser.py wait "#element" --timeout 60000
```

---

## API Reference

For detailed API documentation, see `docs/api.md`.

### BrowserAgent Class

```python
from src.browser import BrowserAgent

# Initialize
agent = BrowserAgent(headless=True)

# Navigate
agent.open("https://example.com")

# Get snapshot
tree = agent.snapshot(interactive=True)

# Interact
agent.click("#submit")
agent.fill("#email", "test@test.com")

# Get info
text = agent.get_text("#title")
html = agent.get_html("#content")

# Screenshot
agent.screenshot("page.png")

# Close
agent.close()
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

MIT License - See LICENSE file for details.

---

## Support

For issues and questions:

- GitHub: https://github.com/leohuang8688/agent-browser
- Documentation: See README.md and docs/api.md

---

**Happy Automating!**
