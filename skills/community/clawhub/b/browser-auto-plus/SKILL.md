---
name: browser-auto-plus
description: "Enhanced browser automation with error recovery, retry logic, multi-browser support, screenshot verification, and integration with web scraping. Supports Chrome, Firefox, Edge with automatic failover."
metadata:
  author: opencode
  version: 2.0
  tags: browser, automation, web-scraping, error-recovery
  compatibility: opencode
  license: MIT
---

# Browser Auto Plus

Enhanced browser automation with error recovery, retry logic, multi-browser support, and screenshot verification.

## Features

- **Multi-Browser Support**: Chrome, Firefox, Edge with automatic failover
- **Error Recovery**: Automatic retry with exponential backoff
- **Screenshot Verification**: Visual confirmation after each action
- **Web Scraping Integration**: Extract data with CSS/XPath selectors
- **CAPTCHA Handling**: Detection and manual/automatic solving
- **Proxy Support**: Route through proxies for anonymity

## Setup

```bash
# Check available browsers
npx playwright install

# Or install specific browser
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

## Commands

```bash
# Navigate
browser navigate <url>

# Interact
browser act "<action>"

# Extract data
browser extract "<instruction>" ['{}']

# Discover elements
browser observe "<query>"

# Take screenshot
browser screenshot

# Close browser
browser close
```

## Error Recovery

### Retry Logic

```javascript
// Automatic retry with exponential backoff
const retry = async (fn, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
    }
  }
};
```

### Common Errors and Solutions

| Error | Solution |
|-------|----------|
| Element not found | Use `browser observe` to discover elements |
| Timeout | Increase timeout or use retry logic |
| CAPTCHA detected | Switch to manual solving or proxy |
| Navigation failed | Check URL, network, try different browser |
| Screenshot failed | Verify browser is running |

## Multi-Browser Support

### Browser Selection

```bash
# Use specific browser
BROWSER=firefox browser navigate <url>

# Use headless mode
HEADLESS=true browser navigate <url>

# Use proxy
PROXY=http://proxy:port browser navigate <url>
```

### Browser Comparison

| Feature | Chrome | Firefox | Edge |
|---------|--------|---------|------|
| Speed | Fast | Medium | Fast |
| Memory | High | Medium | Medium |
| Stealth | Medium | High | Medium |
| Extensions | Yes | Yes | Yes |
| Best for | General | Privacy | Windows |

## Screenshot Verification

```bash
# Take screenshot after action
browser act "click Sign In"
browser screenshot

# Take screenshot with custom name
browser screenshot --name "after-login"

# Take full page screenshot
browser screenshot --full-page
```

## Web Scraping Integration

### Extract with Selectors

```bash
# Extract using CSS selector
browser extract "document.querySelectorAll('.product-title')"

# Extract using XPath
browser extract "document.evaluate('//div[@class=\"price\"]', document, null, XPathResult.ANY_TYPE, null)"

# Extract with data transformation
browser extract "
  Array.from(document.querySelectorAll('.item')).map(item => ({
    title: item.querySelector('.title').textContent,
    price: item.querySelector('.price').textContent,
    link: item.querySelector('a').href
  }))
"
```

### Anti-Detection

```bash
# Randomize user agent
browser act "set user agent to random"

# Add random delays
browser act "wait 1-3 seconds"

# Randomize viewport
browser act "set viewport to random size"
```

## CAPTCHA Handling

### Detection

```bash
# Check for CAPTCHA
browser observe "CAPTCHA, reCAPTCHA, hCaptcha, Cloudflare"

# If found, take screenshot for manual solving
browser screenshot --name "captcha"
```

### Solutions

1. **Manual Solving**: Take screenshot, solve manually, continue
2. **Proxy Rotation**: Switch IP to avoid CAPTCHA
3. **Browser Fingerprint**: Use stealth plugins
4. **Rate Limiting**: Add delays between requests

## Best Practices

1. **Always navigate first** before interacting
2. **View screenshots** after each command to verify
3. **Be specific** in action descriptions
4. **Close browser** when done
5. **Use retry logic** for flaky operations
6. **Log errors** for debugging
7. **Respect robots.txt** and rate limits
8. **Use headless mode** for automation
9. **Handle errors gracefully** with fallbacks
10. **Verify results** with screenshots/extraction

## Troubleshooting

- **Browser not found**: Install with `npx playwright install`
- **Element not found**: Use `browser observe` to discover elements
- **Timeout**: Increase timeout or check network
- **CAPTCHA**: Switch browser, use proxy, or solve manually
- **Memory leak**: Close browser periodically
- **Detection**: Use stealth mode, random delays, proxy

## Anti-Detection Techniques

1. **Random Delays**: 1-5 second delays between actions
2. **User Agent Rotation**: Randomize browser fingerprint
3. **Viewport Randomization**: Vary window size
4. **Cookie Management**: Handle cookies properly
5. **Proxy Rotation**: Change IP periodically
6. **Human-like Behavior**: Random mouse movements, scrolling

## Integration with Web Scraping

```bash
# Full scraping workflow
browser navigate "https://example.com/products"
browser observe ".product-list"
browser extract "
  Array.from(document.querySelectorAll('.product')).map(p => ({
    name: p.querySelector('.name').textContent,
    price: p.querySelector('.price').textContent,
    rating: p.querySelector('.rating').textContent
  }))
"
browser screenshot --name "products"
browser close
```
