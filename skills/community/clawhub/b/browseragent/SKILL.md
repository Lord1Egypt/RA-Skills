---
name: browseragent
description: "Browser automation with human-like behavior. Use when: sites require JavaScript, login sessions, form filling, clicking, scrolling, or complex interactions. Simulates real user behavior to avoid bot detection."
homepage: https://playwright.dev
metadata: { "openclaw": { "emoji": "🤖", "requires": { "bins": ["node", "npx"], "npm": ["playwright"] } } }
---

# BrowserAgent Skill

Automate browser interactions with human-like behavior for complex web tasks.

## When to Use

✅ **USE this skill when:**

- Sites require JavaScript rendering
- Login/authentication needed
- Form filling and submission
- Clicking buttons, navigating menus
- Scrolling to load content (infinite scroll)
- Taking screenshots of web pages
- Downloading files from web
- Complex multi-step workflows
- Sites with bot detection (with human simulation)
- Testing web applications
- Data extraction from dynamic sites

## When NOT to Use

❌ **DON'T use this skill when:**

- Simple static content (use WebScraper)
- Single URL fetch (use web_fetch tool)
- High-volume scraping (respect site limits)
- Sites explicitly blocking automation
- Tasks that violate terms of service

## Installation

```bash
# Install Playwright
npm install -g playwright

# Install browsers (Chrome, Firefox, Safari)
npx playwright install

# Install Chrome extension for stealth (optional)
npm install -g playwright-extra playwright-extra-plugin-stealth
```

## Core Commands

### Basic Page Navigation

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: false,  // Set true for background execution
    slowMo: 100       // Slow down by 100ms (human-like)
  });
  
  const page = await browser.newPage({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  
  await page.goto('https://example.com', { waitUntil: 'networkidle' });
  await browser.close();
})();
```

### Human-Like Behavior

```javascript
// Random delay between actions (human thinking time)
async function humanDelay(min = 1000, max = 3000) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await page.waitForTimeout(delay);
}

// Random mouse movement simulation
async function humanMove(element) {
  const box = await element.boundingBox();
  const x = box.x + Math.random() * box.width;
  const y = box.y + Math.random() * box.height;
  await page.mouse.move(x, y, { steps: 10 });  // Multiple steps = smoother
}

// Click with human behavior
async function humanClick(selector) {
  await humanDelay(500, 1500);  // Think before clicking
  const element = await page.$(selector);
  await humanMove(element);
  await element.click();
  await humanDelay(1000, 2000);  // Wait after clicking
}

// Type with random speed (like real typing)
async function humanType(selector, text) {
  await humanDelay(500, 1000);
  await page.click(selector);
  await page.waitForTimeout(300);
  
  for (const char of text) {
    await page.keyboard.type(char, { delay: Math.random() * 50 + 50 });
  }
}
```

### Login Session Management

```javascript
// Save login state
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();

await page.goto('https://example.com/login');
await humanType('#email', 'user@example.com');
await humanType('#password', 'secret123');
await humanClick('button[type="submit"]');

// Wait for login to complete
await page.waitForNavigation({ waitUntil: 'networkidle' });

// Save cookies/storage for reuse
await page.context().storageState({ path: './session.json' });
await browser.close();

// Reuse session later
const browser2 = await chromium.launch({ headless: false });
const context = await browser2.newContext({
  storageState: './session.json'
});
const page2 = await context.newPage();
await page2.goto('https://example.com');  // Already logged in!
```

### Screenshot & Recording

```javascript
// Full page screenshot
await page.screenshot({ 
  path: 'fullpage.png', 
  fullPage: true 
});

// Element screenshot
const element = await page.$('.product-card');
await element.screenshot({ path: 'product.png' });

// Start screen recording (video)
const browser = await chromium.launch({
  recordVideo: { dir: 'videos/', size: { width: 1920, height: 1080 } }
});
```

### Data Extraction

```javascript
// Extract structured data
const data = await page.evaluate(() => {
  const products = [];
  document.querySelectorAll('.product-item').forEach(item => {
    products.push({
      name: item.querySelector('.name')?.textContent.trim(),
      price: item.querySelector('.price')?.textContent.trim(),
      image: item.querySelector('img')?.src,
      url: item.querySelector('a')?.href
    });
  });
  return products;
});

console.log(JSON.stringify(data, null, 2));
```

### Form Filling

```javascript
// Fill form fields
await humanType('#firstName', 'John');
await humanType('#lastName', 'Doe');
await humanType('#email', 'john@example.com');

// Select dropdown
await page.selectOption('select#country', 'US');

// Check checkbox/radio
await page.check('#terms');
await page.check('input[value="premium"]');

// File upload
await page.setInputFiles('input[type="file"]', '/path/to/file.pdf');

// Submit form
await humanClick('button[type="submit"]');
await page.waitForNavigation({ waitUntil: 'networkidle' });
```

### Scrolling & Infinite Scroll

```javascript
// Scroll to bottom
await page.evaluate(() => {
  window.scrollTo(0, document.body.scrollHeight);
});

// Incremental scroll (human-like)
async function scrollPage() {
  const scrollStep = 300;
  const delay = 500;
  let position = 0;
  
  while (position < document.body.scrollHeight) {
    window.scrollTo(0, position);
    position += scrollStep;
    await new Promise(r => setTimeout(r, delay));
  }
}

await page.evaluate(scrollPage);

// Wait for lazy-loaded content
await page.waitForSelector('.lazy-loaded-item');
```

### Handling Popups & Dialogs

```javascript
// Handle alert/confirm
page.on('dialog', async dialog => {
  console.log(`Dialog message: ${dialog.message()}`);
  await dialog.accept();  // or dialog.dismiss()
});

// Handle new tab popup
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('a[target="_blank"]')
]);
await newPage.bringToFront();

// Close popup
await page.click('.popup-close');
```

### Wait Strategies

```javascript
// Wait for element
await page.waitForSelector('.content', { timeout: 10000 });

// Wait for element to be visible
await page.waitForSelector('.button', { state: 'visible' });

// Wait for navigation
await page.waitForNavigation({ waitUntil: 'networkidle' });

// Wait for specific URL
await page.waitForURL('**/dashboard');

// Wait for text content
await page.waitForFunction(
  () => document.body.innerText.includes('Success'),
  { timeout: 5000 }
);

// Custom wait condition
await page.waitForFunction(
  () => document.querySelectorAll('.item').length > 10,
  { timeout: 10000 }
);
```

## Advanced: Stealth Mode

```javascript
const playwright = require('playwright-extra');
const stealth = require('playwright-extra-plugin-stealth');

playwright.use(stealth());

const browser = await playwright.chromium.launch({
  headless: false,
  args: [
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
    '--disable-dev-shm-usage'
  ]
});

const page = await browser.newPage();

// Additional stealth
await page.evaluateOnNewDocument(() => {
  // Override navigator.webdriver
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
  
  // Override plugins
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
  });
  
  // Override languages
  Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
  });
});
```

## Common Workflows

### 1. Login + Data Extraction

```javascript
async function loginAndScrape() {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();
  
  // Login
  await page.goto('https://example.com/login');
  await humanType('#username', 'myuser');
  await humanType('#password', 'mypass');
  await humanClick('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: 'networkidle' });
  
  // Navigate to data page
  await page.goto('https://example.com/data');
  await humanDelay(2000, 3000);
  
  // Extract data
  const data = await page.evaluate(() => {
    // ... extraction logic
  });
  
  await browser.close();
  return data;
}
```

### 2. Multi-Page Scraping

```javascript
async function scrapeMultiplePages() {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();
  const results = [];
  
  for (let i = 1; i <= 5; i++) {
    await page.goto(`https://example.com/products?page=${i}`);
    await humanDelay(2000, 4000);  // Human-like delay between pages
    
    const items = await page.evaluate(() => {
      // ... extract items
    });
    results.push(...items);
    
    // Click next page
    if (i < 5) {
      await humanClick('.next-page');
      await page.waitForNavigation({ waitUntil: 'networkidle' });
    }
  }
  
  await browser.close();
  return results;
}
```

### 3. Form Submission with Verification

```javascript
async function submitForm() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto('https://example.com/contact');
  
  // Fill form
  await humanType('#name', 'John Doe');
  await humanType('#email', 'john@example.com');
  await humanType('#message', 'Hello!');
  
  // Submit
  await humanClick('button[type="submit"]');
  
  // Verify submission
  await page.waitForSelector('.success-message', { timeout: 5000 });
  const success = await page.$('.success-message') !== null;
  
  await browser.close();
  return success;
}
```

## Error Handling

```javascript
async function robustScrape(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const browser = await chromium.launch({ headless: false });
      const page = await browser.newPage();
      
      await page.goto(url, { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });
      
      // ... scraping logic
      
      await browser.close();
      return result;
      
    } catch (error) {
      console.log(`Attempt ${i + 1} failed: ${error.message}`);
      if (i === retries - 1) throw error;
      await new Promise(r => setTimeout(r, 2000 * (i + 1)));  // Exponential backoff
    }
  }
}
```

## Human Behavior Patterns

### Mouse Movement

```javascript
// Bezier curve mouse movement (natural looking)
async function smoothMove(startX, startY, endX, endY, duration = 1000) {
  const steps = 20;
  const startTime = Date.now();
  
  for (let i = 0; i <= steps; i++) {
    const progress = i / steps;
    const t = progress * Math.PI;
    
    // Ease in-out
    const ease = (1 - Math.cos(t)) / 2;
    
    const x = startX + (endX - startX) * ease;
    const y = startY + (endY - startY) * ease;
    
    await page.mouse.move(x, y);
    await page.waitForTimeout(duration / steps);
  }
}
```

### Typing Patterns

```javascript
// Realistic typing with errors and corrections
async function realisticType(selector, text) {
  await page.click(selector);
  
  const words = text.split(' ');
  for (const word of words) {
    // Occasional typo (5% chance)
    if (Math.random() < 0.05 && word.length > 3) {
      const pos = Math.floor(Math.random() * word.length);
      const typo = word.slice(0, pos) + 'x' + word.slice(pos + 1);
      await page.keyboard.type(typo, { delay: 80 });
      // Backspace and correct
      await page.keyboard.press('Backspace');
      await page.waitForTimeout(200);
      await page.keyboard.type(word[pos], { delay: 80 });
    } else {
      await page.keyboard.type(word + ' ', { delay: 60 });
    }
    
    // Random pause between words
    await page.waitForTimeout(Math.random() * 300 + 100);
  }
}
```

### Scroll Patterns

```javascript
// Human-like scrolling (variable speed, occasional pauses)
async function humanScroll() {
  let position = 0;
  const maxScroll = await page.evaluate(() => document.body.scrollHeight - window.innerHeight);
  
  while (position < maxScroll) {
    const scrollAmount = Math.random() * 200 + 100;
    position = Math.min(position + scrollAmount, maxScroll);
    
    await page.evaluate(y => window.scrollTo(0, y), position);
    
    // Random pause
    await page.waitForTimeout(Math.random() * 1000 + 500);
    
    // Occasional scroll back up (reading behavior)
    if (Math.random() < 0.1) {
      const backScroll = Math.random() * 100;
      await page.evaluate(y => window.scrollBy(0, -y), backScroll);
      await page.waitForTimeout(500);
    }
  }
}
```

## Configuration Reference

### Browser Launch Options

```javascript
{
  headless: false,           // false = visible browser
  slowMo: 100,               // Slow operations by 100ms
  channel: 'chrome',         // Use Chrome instead of Chromium
  executablePath: '/path/to/chrome',  // Custom browser path
  args: [                    // Browser arguments
    '--disable-blink-features=AutomationControlled',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu'
  ]
}
```

### Page Context Options

```javascript
{
  viewport: { width: 1920, height: 1080 },
  userAgent: 'Mozilla/5.0 ...',
  locale: 'en-US',
  timezoneId: 'America/New_York',
  geolocation: { longitude: -74.0, latitude: 40.7 },
  permissions: ['geolocation', 'notifications'],
  colorScheme: 'light',  // or 'dark'
  deviceScaleFactor: 1,
  isMobile: false,
  hasTouch: false
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Site detects bot | Use stealth plugin, add human delays |
| Element not found | Increase wait time, check selector |
| Timeout errors | Increase timeout, check network |
| Captcha appears | Use real session, reduce request rate |
| Memory leak | Close browser, dispose contexts |
| Slow performance | Use headless mode, reduce slowMo |

## Security & Ethics

⚠️ **Important Guidelines:**

1. **Respect robots.txt** - Check site's scraping policy
2. **Rate limiting** - Add delays (2-5s between actions)
3. **Terms of Service** - Don't violate site ToS
4. **Personal data** - Don't scrape PII without consent
5. **Authentication** - Only use your own credentials
6. **Copyright** - Respect intellectual property
7. **Server load** - Don't overwhelm servers

## Related Skills

- **WebScraper** - For simple static content extraction
- **web_search** - For finding URLs to scrape
- **coding-agent** - For processing extracted data

## Quick Reference

```bash
# Install
npm install -g playwright
npx playwright install

# Run script
node browser-script.js

# Debug with inspector
PWDEBUG=1 node browser-script.js

# Record interactions
npx playwright codegen https://example.com
```
