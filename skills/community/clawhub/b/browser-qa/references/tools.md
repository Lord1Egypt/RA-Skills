# Browser QA — Automation Tools

## Tool Options

### claude-in-chrome (Recommended)

Uses your actual Chrome instance for testing:

- **Pros**: Real user conditions, all Chrome features, native performance
- **Cons**: Requires Chrome installed locally
- **Use when**: Testing complex UI with real browser state

### Playwright

Cross-browser testing (Chromium, Firefox, Safari):

- **Pros**: Cross-browser, headless capability, good API
- **Cons**: Separate test runner, slower than in-process
- **Use when**: Need multi-browser coverage

### Puppeteer

Chrome/Chromium-specific automation:

- **Pros**: Fast, simple API, good for screenshots
- **Cons**: Chrome-only, less rich than Playwright
- **Use when**: Quick smoke tests, screenshots

## Tool Comparison

| Tool | Setup | Speed | Multi-Browser | Screenshots |
|------|-------|-------|---------------|-------------|
| claude-in-chrome | Easy (existing Chrome) | Fast | No | Excellent |
| Playwright | Medium | Slow | Yes | Good |
| Puppeteer | Easy | Fast | No | Good |

## Example: Smoke Test with Playwright

```typescript
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

// Capture console errors
const errors = [];
page.on('console', msg => {
  if (msg.type() === 'error') errors.push(msg.text());
});

// Navigate and check metrics
await page.goto('https://example.com');
const vitals = await page.evaluate(() => {
  const paint = performance.getEntriesByType('paint');
  return { paint };
});

// Screenshot
await page.screenshot({ path: 'smoke-test.png' });

console.log('Errors:', errors);
console.log('Web Vitals:', vitals);
```

## Running QA in CI

Most effective in staging environment:

```bash
# After deploy to staging
npm run qa:browser -- --url https://staging.example.com

# Generates report and artifacts
# Upload report to PR review
```
