# Validation Checklist — Post Sub-Agent Execution

Run this after EVERY sub-agent returns design/frontend work. Build passing is necessary but not sufficient.

## 1. Build Check
```bash
npm run build  # or equivalent
```
If it fails, fix before anything else.

## 2. JS Syntax Check (for client-side scripts)
```bash
node -e "new Function(require('fs').readFileSync('path/to/file.js','utf8'))"
```
Catches `export` in non-module scripts, syntax errors, undeclared variables at parse time.

## 3. CSS ↔ JS Integration
- Grep for CSS class names used in selectors that JS should toggle
- Verify JS actually adds/removes those classes
- Check z-index layering: background < canvas < overlay < content
- Verify `opacity` transitions have both the CSS initial state AND the JS trigger

## 4. Visual Verification (if Playwright available)
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900}, color_scheme="dark")
    page.goto("URL", wait_until="networkidle")
    page.wait_for_timeout(3000)
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()
```
Review the screenshot for: layout breaks, invisible elements, overflow, text readability over backgrounds.

## 5. Responsive Spot-Check
- Does the mobile nav still work?
- Do cards stack properly at 375px?
- Is touch target size ≥44px on interactive elements?

## 6. Theme/Motion Checks
- `data-theme="light"` — are transparent backgrounds adjusted?
- `prefers-reduced-motion: reduce` — are animations disabled?
- If Canvas: does it skip initialization under reduced motion?

## 7. Asset Verification
- Image dimensions match expectations (don't trust filenames)
- OG images: 1200x630, <500KB
- CDN cache: bump version params if updating cached assets

## 8. Content Audit
- No placeholder text or TODO markers left in HTML
- Astro template expressions properly escaped (`{curlyBraces}` in code blocks need `{'{'}`/`{'}'}`)
- Meta descriptions match new content
