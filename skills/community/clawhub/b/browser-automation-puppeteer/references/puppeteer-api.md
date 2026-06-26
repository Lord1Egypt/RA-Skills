# Puppeteer API Reference

Complete reference for Puppeteer used in this skill.

## Browser Launch

```javascript
const browser = await puppeteer.launch({
  headless: 'new',           // 'new' = faster headless
  args: [
    '--no-sandbox',          // Required for Linux
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu'
  ]
});
```

## Page Navigation

```javascript
await page.goto(url, {
  waitUntil: 'networkidle2',  // Wait until network is idle
  timeout: 30000               // 30s timeout
});

// Alternative wait strategies:
// 'load' - default
// 'domcontentloaded' - faster
// 'networkidle0' - stricter
// 'networkidle' - strictest
```

## Content Extraction

### $$eval (Multiple Elements)

```javascript
const data = await page.$$eval('selector', elements => {
  return elements.map(el => ({
    text: el.textContent.trim(),
    href: el.href,
    src: el.src
  }));
});
```

### $eval (Single Element)

```javascript
const text = await page.$eval('.title', el => el.textContent.trim());
```

### Inner HTML/Text

```javascript
const html = await page.$eval('.container', el => el.innerHTML);
const text = await page.$eval('.container', el => el.innerText);
```

## Waiting

### Wait for Selector

```javascript
await page.waitForSelector('.loaded-content', { timeout: 10000 });
```

### Wait for Function

```javascript
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length >= 10;
});
```

### Wait for Navigation

```javascript
await Promise.all([
  page.waitForNavigation(),
  page.click('.submit-btn')
]);
```

## Click & Type

```javascript
await page.click('#submit-button');
await page.type('#search-input', 'search term');
await page.focus('#input');
await page.keyboard.press('Enter');
```

## Evaluate (Raw JS in Page Context)

```javascript
const result = await page.evaluate(() => {
  const items = document.querySelectorAll('.item');
  return Array.from(items).map(item => ({
    title: item.querySelector('h3')?.textContent,
    price: item.querySelector('.price')?.textContent
  }));
});
```

## Screenshots

```javascript
// Full page
await page.screenshot({ path: 'full.png', fullPage: true });

// Specific area
await page.screenshot({ path: 'header.png', clip: { x: 0, y: 0, width: 800, height: 200 } });

// Element
const el = await page.$('.chart');
await el.screenshot({ path: 'chart.png' });
```

## PDF Generation

```javascript
await page.pdf({
  path: 'page.pdf',
  format: 'A4',
  printBackground: true
});
```

## Handle New Tabs/Windows

```javascript
const [newPage] = await Promise.all([
  new Promise(resolve => browser.once('targetcreated', target => resolve(target.page()))),
  page.click('a[target="_blank"]')
]);
await newPage.waitForSelector('.content');
```

## Request Interception

```javascript
await page.setRequestInterception(true);
page.on('request', req => {
  if (req.resourceType() === 'image' || req.resourceType() === 'stylesheet') {
    req.abort();  // Block images/stylesheets
  } else {
    req.continue();
  }
});
```

## Set Headers

```javascript
await page.setExtraHTTPHeaders({
  'Authorization': 'Bearer token123'
});
```

## Cookies

```javascript
// Get cookies
const cookies = await page.cookies();

// Set cookies
await page.setCookie({
  name: 'session',
  value: 'abc123',
  domain: '.example.com'
});
```

## Evaluate XPath

```javascript
const elements = await page.evaluate(() => {
  const result = [];
  const iter = document.evaluate('//div[@class="item"]', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE);
  for (let i = 0; i < iter.snapshotLength; i++) {
    result.push(iter.snapshotItem(i).textContent);
  }
  return result;
});
```

## Common Issues

### Element not found

```javascript
// Check if element exists
const el = await page.$('.selector');
if (!el) {
  console.log('Element not found');
} else {
  // Proceed
}
```

### Timeout errors

```javascript
// Increase timeout
await page.goto(url, { timeout: 60000 });

// Or wrap in try/catch
try {
  await page.waitForSelector('.content', { timeout: 5000 });
} catch (e) {
  console.log('Selector not found within timeout');
}
```