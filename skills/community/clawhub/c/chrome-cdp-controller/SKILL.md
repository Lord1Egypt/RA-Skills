---
name: chrome-cdp-controller
description: Control local Chrome browser via Chrome DevTools Protocol (CDP) using Puppeteer. Use when you need to automate browser tasks like navigating pages, clicking elements, filling forms, taking screenshots, executing JavaScript, or intercepting network responses. Works with Chrome instances that already have CDP enabled. Common use cases include web scraping (e.g., "Search iPhone on Taobao and get prices"), automated testing, interacting with web apps (e.g., "Ask ChatGPT a question"), or monitoring network traffic.
---

# Chrome CDP Controller (Puppeteer)

Control and automate a Chrome browser that's already running with CDP enabled, using Puppeteer.

## Key Features

- **Non-intrusive**: Connects to your existing Chrome, opens a new tab, operates, then closes only that tab
- **Your browser stays open**: Never closes your existing tabs or browser
- **Clean automation**: Each task runs in its own tab, which is automatically closed when done

### 1. Chrome with CDP Enabled

Chrome must be running with remote debugging enabled. If not already started:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222 &
```

### 2. Get WebSocket URL

Visit `http://localhost:9222/json/version` to get the `webSocketDebuggerUrl`, for example:
```
ws://127.0.0.1:9222/devtools/browser/FFA7276F8E8E51645BD2AC9BE6B79607
```

Or use this one-liner:
```bash
curl -s http://localhost:9222/json/version | grep -o '"webSocketDebuggerUrl":"[^"]*"' | cut -d'"' -f4
```

### 3. Install Dependencies

```bash
cd chrome-cdp-controller
npm install
```

This installs `puppeteer-core` which is lightweight (doesn't download Chromium).

## Usage

### Command-Based Execution

Create a JSON file with commands:

**commands.json:**
```json
[
  {"type": "navigate", "url": "https://www.baidu.com"},
  {"type": "wait", "seconds": 2},
  {"type": "screenshot", "path": "/tmp/screenshot.png"},
  {"type": "evaluate", "script": "document.title"}
]
```

Execute:
```bash
node scripts/cdp_controller.js --ws "ws://127.0.0.1:9222/devtools/browser/..." --commands commands.json
```

### Node.js API

```javascript
const { CDPController } = require('./scripts/cdp_controller.js');

(async () => {
  const controller = new CDPController('ws://127.0.0.1:9222/devtools/browser/...');
  await controller.connect();
  
  // Navigate
  await controller.navigate('https://www.taobao.com');
  
  // Fill form
  await controller.fill('#q', 'iPhone');
  await controller.press('Enter');
  await controller.wait(3);
  
  // Extract data
  const result = await controller.evaluate(`
    Array.from(document.querySelectorAll('.item'))
      .slice(0, 10)
      .map(item => ({
        title: item.querySelector('.title')?.textContent.trim(),
        price: item.querySelector('.price')?.textContent.trim()
      }))
  `);
  console.log(result.result);
  
  // Intercept network
  await controller.startIntercept('*api*');
  // ... perform actions ...
  const responses = controller.getInterceptedResponses();
  
  await controller.close();
})();
```

## Available Commands

### Navigation
- **navigate** - Go to URL
  - `url`: Target URL
  - `waitUntil`: "load", "domcontentloaded", or "networkidle2" (default)

### Interaction
- **click** - Click an element
  - `selector`: CSS selector
  - `timeout`: Timeout in milliseconds (default: 5000)

- **fill** - Fill a form field (selects all, then types)
  - `selector`: CSS selector
  - `text`: Text to fill
  - `timeout`: Timeout in milliseconds (default: 5000)

- **type** - Type text character by character
  - `selector`: CSS selector
  - `text`: Text to type
  - `delay`: Delay between characters in ms (default: 50)
  - `timeout`: Timeout in milliseconds (default: 5000)

- **press** - Press a key
  - `key`: Key name (Enter, Tab, Escape, etc.)

### Data Extraction
- **get_text** - Get text content of a single element
  - `selector`: CSS selector

- **get_all_text** - Get text content of all matching elements
  - `selector`: CSS selector

- **evaluate** - Execute JavaScript and return result
  - `script`: JavaScript code

### Network Interception
- **start_intercept** - Start intercepting network responses
  - `url_pattern`: URL pattern to match (substring match, e.g., "api")

- **get_intercepted** - Get all intercepted responses

- **clear_intercepted** - Clear intercepted responses list

### Utilities
- **screenshot** - Take a screenshot
  - `path`: Output file path
  - `fullPage`: Capture full page (default: false)

- **wait_for_selector** - Wait for element to appear
  - `selector`: CSS selector
  - `timeout`: Timeout in milliseconds (default: 5000)

- **wait** - Sleep for a duration
  - `seconds`: Number of seconds to wait

## Common Workflows

### Example 1: Search Taobao for iPhone Prices

**taobao-search.json:**
```json
[
  {"type": "navigate", "url": "https://www.taobao.com"},
  {"type": "wait", "seconds": 2},
  {"type": "fill", "selector": "#q", "text": "iPhone"},
  {"type": "press", "key": "Enter"},
  {"type": "wait", "seconds": 5},
  {"type": "evaluate", "script": "Array.from(document.querySelectorAll('.item, [class*=\"Item\"]')).slice(0, 10).map(item => ({ title: item.querySelector('.title, [class*=\"title\"]')?.textContent.trim().substring(0, 80), price: item.querySelector('.price, [class*=\"price\"]')?.textContent.trim() }))"}
]
```

Run:
```bash
WS_URL=$(curl -s http://localhost:9222/json/version | grep -o '"webSocketDebuggerUrl":"[^"]*"' | cut -d'"' -f4)
node scripts/cdp_controller.js --ws "$WS_URL" --commands taobao-search.json
```

**Note**: Selectors may vary. Use browser DevTools (F12) to inspect elements.

### Example 2: Ask ChatGPT a Question

**chatgpt-ask.json:**
```json
[
  {"type": "navigate", "url": "https://chat.openai.com"},
  {"type": "wait_for_selector", "selector": "textarea", "timeout": 10000},
  {"type": "type", "selector": "textarea", "text": "What is artificial intelligence?"},
  {"type": "press", "key": "Enter"},
  {"type": "wait", "seconds": 10},
  {"type": "get_text", "selector": "[data-message-author-role='assistant']:last-of-type"}
]
```

### Example 3: Intercept API Responses

**intercept-api.json:**
```json
[
  {"type": "start_intercept", "url_pattern": "graphql"},
  {"type": "navigate", "url": "https://example.com"},
  {"type": "wait", "seconds": 3},
  {"type": "get_intercepted"}
]
```

For more examples, see [references/examples.md](references/examples.md).

## Workflow

When automating browser tasks:

1. **Get WebSocket URL**: 
   - If you already have it (e.g., `ws://127.0.0.1:9222/devtools/browser/...`), use it directly
   - Otherwise, fetch from `http://localhost:9222/json/version`

2. **Determine selectors**: 
   - For known sites (Taobao, ChatGPT, etc.), check [references/examples.md](references/examples.md)
   - For unknown sites, navigate first and use `evaluate` with `document.querySelector` to test selectors
   - Use browser DevTools (F12) to inspect elements

3. **Build command sequence**:
   - Start with `navigate`
   - Add `wait` or `wait_for_selector` between steps
   - Use `fill` for form inputs, `click` for buttons
   - Use `evaluate` for complex data extraction
   - Add `start_intercept` before navigation if monitoring network traffic

4. **Execute**:
   - Save commands to JSON file
   - Run: `node scripts/cdp_controller.js --ws "<websocket-url>" --commands <file>`
   - Parse JSON output

5. **Handle failures**:
   - If selectors fail, inspect with DevTools
   - If timing issues occur, increase wait times or use `wait_for_selector`
   - If connection fails, verify Chrome is running with CDP enabled

## Tips

- **Wait times**: Use `wait_for_selector` instead of fixed `wait` when possible
- **Selectors**: Prefer ID (`#id`) > class (`.class`) > attribute (`[attr='value']`)
- **Network interception**: Start intercepting BEFORE navigating
- **JavaScript**: Use `evaluate` for complex data extraction
- **Screenshots**: Useful for debugging

## Troubleshooting

### Connection Failed
- Ensure Chrome is running with `--remote-debugging-port=9222`
- Verify WebSocket URL is correct
- Check Chrome version compatibility with puppeteer-core

### Element Not Found
- Verify selector with DevTools (F12)
- Add `wait_for_selector` before interaction
- Check if element is in an iframe

### Module Not Found
```bash
cd chrome-cdp-controller
npm install
```
