# API Documentation

## BrowserAgent Class

### Initialization

```python
from src.browser import BrowserAgent

# Initialize with default settings
agent = BrowserAgent()

# Initialize with custom settings
agent = BrowserAgent(headless=False)  # Show browser window
```

### Methods

#### `open(url: str)`

Navigate to a URL.

**Parameters:**
- `url` (str): URL to navigate to

**Example:**
```python
agent.open("https://example.com")
```

#### `snapshot(interactive: bool = False, compact: bool = False, depth: Optional[int] = None) -> str`

Get accessibility tree snapshot.

**Parameters:**
- `interactive` (bool): Only interactive elements
- `compact` (bool): Compact output
- `depth` (int): Limit tree depth

**Returns:**
- `str`: Accessibility tree as string

**Example:**
```python
# Full snapshot
tree = agent.snapshot()

# Interactive elements only
tree = agent.snapshot(interactive=True)

# Compact with depth limit
tree = agent.snapshot(compact=True, depth=3)
```

#### `click(selector: str)`

Click an element.

**Parameters:**
- `selector` (str): CSS selector

**Example:**
```python
agent.click("#submit")
agent.click(".button.primary")
```

#### `fill(selector: str, text: str)`

Fill an input field.

**Parameters:**
- `selector` (str): CSS selector
- `text` (str): Text to fill

**Example:**
```python
agent.fill("#email", "test@example.com")
agent.fill("#password", "secret")
```

#### `screenshot(path: str, full_page: bool = False)`

Take a screenshot.

**Parameters:**
- `path` (str): Output file path
- `full_page` (bool): Full page screenshot

**Example:**
```python
# Normal screenshot
agent.screenshot("page.png")

# Full page screenshot
agent.screenshot("page_full.png", full_page=True)
```

#### `get_text(selector: str) -> str`

Get text content of an element.

**Parameters:**
- `selector` (str): CSS selector

**Returns:**
- `str`: Text content

**Example:**
```python
text = agent.get_text("#title")
print(f"Title: {text}")
```

#### `get_html(selector: str) -> str`

Get innerHTML of an element.

**Parameters:**
- `selector` (str): CSS selector

**Returns:**
- `str`: InnerHTML

**Example:**
```python
html = agent.get_html("#content")
print(f"HTML: {html}")
```

#### `is_visible(selector: str) -> bool`

Check if element is visible.

**Parameters:**
- `selector` (str): CSS selector

**Returns:**
- `bool`: True if visible

**Example:**
```python
if agent.is_visible("#popup"):
    print("Popup is visible")
```

#### `close()`

Close the browser.

**Example:**
```python
agent.close()
```

### Context Manager

BrowserAgent supports context manager for automatic cleanup:

```python
with BrowserAgent() as agent:
    agent.open("https://example.com")
    # Browser auto-closes after context
```

---

## CLI Commands

### Installation

```bash
# Install browsers
python agent_browser.py install
```

### Navigation

```bash
# Open URL
python agent_browser.py open https://example.com

# Get current URL
python agent_browser.py get_url

# Get page title
python agent_browser.py get_title
```

### Snapshot

```bash
# Full snapshot
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

### Interaction

```bash
# Click element
python agent_browser.py click "#submit"

# Fill input
python agent_browser.py fill "#email" "test@example.com"

# Type into input
python agent_browser.py type "#search" "query"
```

### Get Info

```bash
# Get text
python agent_browser.py get_text "#title"

# Get HTML
python agent_browser.py get_html "#content"

# Check visibility
python agent_browser.py is_visible "#popup"
```

### Screenshot

```bash
# Normal screenshot
python agent_browser.py screenshot page.png

# Full page screenshot
python agent_browser.py screenshot page.png --full

# Annotated screenshot
python agent_browser.py screenshot page.png --annotate
```

### Browser Control

```bash
# Close browser
python agent_browser.py close

# Install browsers
python agent_browser.py install
```

---

## Options

### Global Options

```bash
# Headless mode (default)
python agent_browser.py open https://example.com --headless

# Show browser window (debugging)
python agent_browser.py open https://example.com --headed

# Custom viewport
python agent_browser.py open https://example.com --viewport 1920x1080

# Emulate device
python agent_browser.py open https://example.com --device "iPhone 14"
```

### Snapshot Options

```bash
# Interactive elements only
python agent_browser.py snapshot -i

# Compact output
python agent_browser.py snapshot -c

# Limit depth
python agent_browser.py snapshot -d 3

# Scope to selector
python agent_browser.py snapshot -s "#main"
```

### Screenshot Options

```bash
# Full page
python agent_browser.py screenshot page.png --full

# Annotate with labels
python agent_browser.py screenshot page.png --annotate
```

---

## Advanced Usage

### Persistent Sessions

```python
from src.browser import BrowserAgent

# Use persistent profile
agent = BrowserAgent()
agent.open("https://example.com/login")

# Login
agent.fill("#email", "user@example.com")
agent.fill("#password", "secret")
agent.click("#submit")

# Save state (cookies, localStorage)
# (Implementation needed)

# Reuse session
agent2 = BrowserAgent()
agent2.open("https://example.com/dashboard")
# Already authenticated
```

### Device Emulation

```python
from src.browser import BrowserAgent

# Emulate iPhone
agent = BrowserAgent()
# (Implementation needed for device emulation)
agent.open("https://example.com")

# Emulate iPad
# (Implementation needed)
```

### Wait for Elements

```python
from src.browser import BrowserAgent

agent = BrowserAgent()
agent.open("https://example.com")

# Wait for element (implementation needed)
# agent.wait("#loader", state="hidden")

# Wait for text (implementation needed)
# agent.wait(text="Welcome")

# Wait for network idle (implementation needed)
# agent.wait(load="networkidle")
```

---

## Error Handling

```python
from src.browser import BrowserAgent

try:
    with BrowserAgent() as agent:
        agent.open("https://example.com")
        agent.click("#nonexistent")  # This will fail
except Exception as e:
    print(f"Error: {e}")
```

---

## Best Practices

1. **Use context manager** for automatic cleanup:
   ```python
   with BrowserAgent() as agent:
       # Your code here
   ```

2. **Close browser** when done:
   ```python
   agent = BrowserAgent()
   try:
       # Your code here
   finally:
       agent.close()
   ```

3. **Use headless mode** for automation:
   ```python
   agent = BrowserAgent(headless=True)
   ```

4. **Take screenshots** for debugging:
   ```python
   agent.screenshot("debug.png")
   ```

5. **Use snapshot** for AI agents:
   ```python
   tree = agent.snapshot(interactive=True)
   ```

---

## Troubleshooting

### Browser doesn't open

```bash
# Install Playwright browsers
python agent_browser.py install
```

### Element not found

```python
# Check if element exists
visible = agent.is_visible("#element")
print(f"Visible: {visible}")
```

### Screenshot is blank

```python
# Wait for page to load
agent.open("https://example.com")
# (Add wait implementation)
```

---

## Support

For issues and questions:
- GitHub: https://github.com/leohuang8688/agent-browser
- Documentation: See README.md
