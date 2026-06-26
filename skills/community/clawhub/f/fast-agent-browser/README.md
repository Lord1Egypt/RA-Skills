# 🌐 Agent Browser

**Fast, Python-based browser automation CLI for AI agents**

[![Version 0.1.0](https://img.shields.io/badge/version-0.1.0-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- 🚀 **Fast CLI** - Command-line interface for browser automation
- 🤖 **AI-Friendly** - Optimized for AI agent workflows
- 📸 **Screenshots** - Full page and element screenshots
- 🌳 **Snapshot** - Accessibility tree with element refs
- 🖱️ **Interact** - Click, fill, type, hover, and more
- 📊 **Get Info** - Text, HTML, attributes, styles
- ⏳ **Wait** - Wait for elements, text, URLs, network idle
- 🔍 **Find** - Semantic locators (role, text, label, etc.)
- 📱 **Responsive** - Device emulation and viewport control
- 🔐 **Auth** - Session persistence and cookie management

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills/agent-browser

# Install Python dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Basic Usage

```bash
# Open a URL
python agent_browser.py open https://example.com

# Get snapshot
python agent_browser.py snapshot

# Click an element
python agent_browser.py click "#submit"

# Fill a form
python agent_browser.py fill "#email" "test@example.com"

# Take screenshot
python agent_browser.py screenshot page.png

# Close browser
python agent_browser.py close
```

---

## 📖 Commands

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `open` | Navigate to URL | `open https://example.com` |
| `snapshot` | Get accessibility tree | `snapshot -i` |
| `click` | Click element | `click "#submit"` |
| `fill` | Fill input field | `fill "#email" "test@test.com"` |
| `screenshot` | Take screenshot | `screenshot page.png` |
| `close` | Close browser | `close` |

### Get Info

| Command | Description | Example |
|---------|-------------|---------|
| `get text` | Get text content | `get text "#title"` |
| `get html` | Get innerHTML | `get html "#content"` |
| `get url` | Get current URL | `get url` |
| `get title` | Get page title | `get title` |

### Wait Commands

| Command | Description | Example |
|---------|-------------|---------|
| `wait` | Wait for element | `wait "#loader" --state hidden` |
| `wait --text` | Wait for text | `wait --text "Welcome"` |
| `wait --load` | Wait for load state | `wait --load networkidle` |

---

## 🎯 AI Workflow

### Optimal AI Agent Workflow

```bash
# 1. Navigate and get snapshot
python agent_browser.py open https://example.com
python agent_browser.py snapshot -i

# 2. AI identifies target refs from snapshot
# 3. Execute actions using refs
python agent_browser.py click "@e2"
python agent_browser.py fill "@e3" "input text"

# 4. Get new snapshot if page changed
python agent_browser.py snapshot -i
```

### Snapshot Options

```bash
# Full accessibility tree
python agent_browser.py snapshot

# Interactive elements only
python agent_browser.py snapshot -i

# Compact output
python agent_browser.py snapshot -c

# Limit depth
python agent_browser.py snapshot -d 3

# Combine options
python agent_browser.py snapshot -i -c -d 5
```

---

## 🔧 Advanced Usage

### Persistent Sessions

```bash
# Use persistent profile
python agent_browser.py open https://example.com --profile ~/.myapp-profile

# Reuse authenticated session
python agent_browser.py open https://example.com/dashboard --profile ~/.myapp-profile
```

### Device Emulation

```bash
# Emulate iPhone
python agent_browser.py open https://example.com --device "iPhone 14"

# Custom viewport
python agent_browser.py open https://example.com --viewport 1920x1080
```

### Headed Mode (Debugging)

```bash
# Show browser window
python agent_browser.py open https://example.com --headed
```

---

## 📁 Project Structure

```
agent-browser/
├── src/
│   ├── __init__.py
│   └── browser.py         # Core browser agent
├── tests/
│   └── test_browser.py    # Test suite
├── examples/
│   └── basic_usage.py     # Usage examples
├── docs/
│   └── api.md             # API documentation
├── agent_browser.py       # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🧪 Testing

```bash
# Install test dependencies
pip3 install pytest pytest-playwright

# Run tests
pytest tests/
```

---

## 📝 Examples

### Example 1: Login Flow

```bash
# Open login page
python agent_browser.py open https://example.com/login

# Fill credentials
python agent_browser.py fill "#email" "user@example.com"
python agent_browser.py fill "#password" "secret"

# Click submit
python agent_browser.py click "#submit"

# Wait for dashboard
python agent_browser.py wait --url "**/dashboard"

# Take screenshot
python agent_browser.py screenshot dashboard.png
```

### Example 2: Form Automation

```bash
# Open form
python agent_browser.py open https://example.com/form

# Fill fields
python agent_browser.py fill "#name" "John Doe"
python agent_browser.py fill "#email" "john@example.com"
python agent_browser.py fill "#message" "Hello!"

# Select dropdown
python agent_browser.py select "#country" "US"

# Check checkbox
python agent_browser.py check "#terms"

# Submit
python agent_browser.py click "#submit"
```

### Example 3: Data Extraction

```bash
# Open page
python agent_browser.py open https://example.com/products

# Get product titles
python agent_browser.py get text ".product-title"

# Get prices
python agent_browser.py get text ".product-price"

# Take screenshot
python agent_browser.py screenshot products.png
```

---

## 🔐 Security

### Session Persistence

```bash
# Save auth state
python agent_browser.py state save myapp.json

# Load auth state
python agent_browser.py state load myapp.json
```

### Cookie Management

```bash
# Get cookies
python agent_browser.py cookies

# Set cookie
python agent_browser.py cookies set session abc123

# Clear cookies
python agent_browser.py cookies clear
```

---

## 📊 API Reference

### BrowserAgent Class

```python
from src.browser import BrowserAgent

# Initialize
agent = BrowserAgent(headless=True)

# Navigate
agent.open("https://example.com")

# Get snapshot
tree = agent.snapshot(interactive=True, compact=True)

# Interact
agent.click("#submit")
agent.fill("#email", "test@test.com")

# Get info
text = agent.get_text("#title")
html = agent.get_html("#content")
visible = agent.is_visible("#button")

# Screenshot
agent.screenshot("page.png", full_page=True)

# Close
agent.close()
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

GitHub: [@leohuang8688](https://github.com/leohuang8688)

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation library
- [Click](https://click.palletsprojects.com/) - CLI framework
- [OpenClaw](https://github.com/openclaw/openclaw) - AI assistant framework

---

**Happy Automating! 🤖🌐**
