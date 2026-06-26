---
name: auto-captcha-solver
description: Detect and solve simple image captchas during browser automation. Use when flows encounter 4-6 character text, distorted alphanumeric, numeric, rotated, or arithmetic captchas and need capture, OCR, optional calculation, input fill, and submit handling in Playwright, Puppeteer, or Selenium. Do not use for reCAPTCHA, hCaptcha, slider, or click-object challenges.
---

# Auto Captcha Solver

Use this skill to solve simple captcha images in browser automation.

## Supported Captcha Types

- 4 to 6 character text captchas
- Distorted alphanumeric captchas
- Numeric captchas
- Simple rotated characters
- Arithmetic captchas (example: `3+8`)

Do not use this skill for reCAPTCHA, hCaptcha, sliders, or click-object challenges.

## Workflow

1. Detect a captcha image element from the page.
2. Capture a screenshot buffer of the captcha.
3. Run preprocessing (`grayscale`, `contrast normalization`, `resize`, `noise reduction`).
4. Run OCR and clean output.
5. Detect arithmetic patterns and evaluate if needed.
6. Fill the captcha input and optionally submit.

## Capture Guidance

- Prefer screenshotting only the captcha element, not the full page.
- Accept only trusted `http` or `https` image URLs when reading captcha image source.
- Reject suspicious schemes like `javascript:` or `file:`.
- Enforce image size and pixel limits before OCR.

## Return Format

Return a result object with:

- `solved`: boolean
- `value`: solved captcha text
- `type`: `alphanumeric`, `numeric`, `arithmetic`, or `unknown`
- `confidence`: OCR confidence score
- `hash`: SHA1 image hash (cache key)
- `fromCache`: optional boolean when a cached answer is used

## Module Map

- `solve.js`: main entry for solving an image buffer
- `preprocess.js`: image normalization pipeline
- `ocr.js`: OCR and text cleanup with multiple passes
- `cache.js`: SHA1 captcha cache
- `browser.js`: automation helpers for Playwright, Puppeteer, and Selenium
