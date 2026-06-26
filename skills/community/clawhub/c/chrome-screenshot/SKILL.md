---
name: chrome-screenshot
description: "Take full-page screenshots of HTML files as PNG images using Chrome + puppeteer-core, without downloading any browser. Use when: (1) rendering a data visualization report and delivering it as an image, (2) converting an HTML page to a shareable screenshot, (3) the user asks for an image/PNG/PDF of an HTML report, (4) the canvas or browser tool is unavailable or impractical. Also generates PDF via Chrome's print-to-PDF."
---

# Chrome Screenshot

Converts HTML files to PNG screenshots (or PDF documents) using the system's installed Chrome via puppeteer-core.

## Prerequisites

- Chrome installed at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- puppeteer-core installed globally: `npm install -g puppeteer-core`
- Node.js

## Script: `scripts/screenshot.sh`

```
scripts/screenshot.sh <html-file> [output-path] [width]
```

- `html-file`: Path to the HTML file (required)
- `output-path`: Output PNG path (default: `/tmp/screenshot.png`)
- `width`: Viewport width in px (default: `420`, good for mobile/微信)

The script:
1. Starts a local HTTP server on port 8877
2. Opens the HTML in headless Chrome via puppeteer-core
3. Measures the full page height and captures a full-page screenshot
4. Saves as PNG, cleans up the HTTP server

## Usage

### Screenshot an HTML report

```bash
bash scripts/screenshot.sh /path/to/report.html /tmp/output.png 420
```

Then send the image via the message tool:

```json
{
  "action": "send",
  "media": "/tmp/output.png",
  "message": "📊 Report Title"
}
```

### PDF output (optional)

Chrome's print-to-PDF can generate PDFs instead:

```bash
bash scripts/screenshot.sh /path/to/report.html /tmp/output.pdf 420
```

## Notes

- Do NOT use this skill for web browsing or page interaction—only for screenshotting locally authored HTML.
- The HTML file is served via Python's `http.server`. Make sure `python3` is available.
- For the best visual result in the screenshot, author the HTML with an explicit width matching the screenshot width.
- The HTTP server binds to 127.0.0.1 on port 8877.
