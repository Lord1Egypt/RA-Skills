# auto-captcha-solver

Automatically detect and solve simple captchas in browser automation using OCR.

## Features

- Supports 4-6 character text captchas
- Supports distorted alphanumeric and numeric captchas
- Supports simple rotated characters
- Supports arithmetic captchas like `3+8=`
- SHA1 hash cache to avoid repeated OCR work
- Multiple OCR passes with confidence scoring
- Playwright, Puppeteer, and Selenium helpers
- CPU-only operation, no GPU required

## Not Supported

- reCAPTCHA
- hCaptcha
- Slider captchas
- Click-object captchas

## Installation

```bash
npm install
```

Dependencies:

- `tesseract.js`
- `sharp`
- `crypto` (Node built-in)

## Project Structure

```text
auto-captcha-solver/
  SKILL.md
  solve.js
  preprocess.js
  ocr.js
  cache.js
  browser.js
  package.json
  README.md
```

## Basic Usage

```js
const fs = require("fs");
const { solveCaptchaImage, calibrateCaptcha } = require("./solve");

async function run() {
  const img = fs.readFileSync("./captcha.png");
  // Optional supervised calibration when you know the real answer.
  await calibrateCaptcha(img, "2VM9", { caseMode: "preserve" });
  const result = await solveCaptchaImage(img, { caseMode: "preserve" });
  console.log(result);
}

run().catch(console.error);
```

Calibrated answers are saved in `.captcha-verified.json` by image SHA1 hash.
Use `caseMode: "preserve"` for mixed-case captchas such as `pfJU`.

To inspect OCR candidates for tuning:

```js
const result = await solveCaptchaImage(img, { debug: true });
console.log(result.debug.topCandidates);
```

## Playwright Integration

```js
const { chromium } = require("playwright");
const { solveCaptchaPlaywright } = require("./browser");

async function run() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("https://example.com/login");

  const solved = await solveCaptchaPlaywright(page, {
    imageSelectors: ['img[alt*="captcha" i]'],
    inputSelectors: ['input[name="captcha"]'],
    submitSelector: 'button[type="submit"]',
    autoSubmit: true
  });

  console.log(solved);
  await browser.close();
}

run();
```

## Puppeteer Integration

```js
const puppeteer = require("puppeteer");
const { solveCaptchaPuppeteer } = require("./browser");

async function run() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto("https://example.com/login");

  const solved = await solveCaptchaPuppeteer(page, {
    imageSelectors: ['img[src*="captcha" i]'],
    inputSelectors: ['input[id*="captcha" i]'],
    submitSelector: 'button[type="submit"]'
  });

  console.log(solved);
  await browser.close();
}

run();
```

## Selenium Integration

```js
const { Builder } = require("selenium-webdriver");
const { solveCaptchaSelenium } = require("./browser");

async function run() {
  const driver = await new Builder().forBrowser("chrome").build();
  await driver.get("https://example.com/login");

  const solved = await solveCaptchaSelenium(driver, {
    imageSelectors: ['img[alt*="captcha" i]'],
    inputSelectors: ['input[name="captcha"]'],
    submitSelector: 'button[type="submit"]'
  });

  console.log(solved);
  await driver.quit();
}

run();
```

## OpenClaw Integration

Use the skill when an agent needs to handle simple captcha steps in automation:

1. detect captcha image element
2. screenshot captcha image
3. call `solveCaptchaImage(buffer)` or browser helper
4. fill the captcha input with the returned `value`
5. submit form

## Security Controls

- Validates input is an image buffer
- Restricts maximum image bytes and pixel count
- Accepts trusted image URL schemes only (`http`, `https`, `data:image`)
- Avoids shell execution and command injection paths

## Performance Notes

- Uses lightweight preprocessing before OCR
- Reuses a shared OCR worker across requests
- Uses hash cache to skip repeated OCR
- Uses multi-variant preprocessing and candidate scoring for better OCR hit rate
- Typical simple captcha flow is optimized for near sub-second solves on modern CPUs

## Limitations

- Accuracy depends on captcha distortion level and font complexity
- Arithmetic parser supports binary operations (`+`, `-`, `*`, `/`)
- Fallback vision is optional and must be provided by caller (`fallbackVision` option)
