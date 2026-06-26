#!/bin/bash
# screenshot.sh - Take a full-page screenshot of an HTML file using Chrome + puppeteer-core
# Usage: ./screenshot.sh <path-to-html> [output-path] [width]
#   output-path defaults to /tmp/screenshot.png
#   width defaults to 420

set -euo pipefail

HTML_FILE="$1"
OUTPUT="${2:-/tmp/screenshot.png}"
WIDTH="${3:-420}"

if [ ! -f "$HTML_FILE" ]; then
  echo "ERROR: HTML file not found: $HTML_FILE" >&2
  exit 1
fi

# Resolve absolute path
HTML_FILE="$(cd "$(dirname "$HTML_FILE")" && pwd)/$(basename "$HTML_FILE")"

# Check for puppeteer-core
# Find puppeteer-core (in npm global node_modules)
NPM_GLOBAL="$(npm root -g 2>/dev/null)"
if [ ! -d "$NPM_GLOBAL/puppeteer-core" ]; then
  echo "ERROR: puppeteer-core not found. Install: npm install -g puppeteer-core" >&2
  exit 1
fi
NODE_PATH="$NPM_GLOBAL${NODE_PATH:+:$NODE_PATH}"

# Check Chrome
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME" ]; then
  echo "ERROR: Chrome not found at $CHROME" >&2
  exit 1
fi

# Start a local HTTP server for serving the HTML
PORT=8877
SERVER_PID=""
cleanup() {
  if [ -n "$SERVER_PID" ]; then
    kill "$SERVER_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

DIR="$(dirname "$HTML_FILE")"
NAME="$(basename "$HTML_FILE")"

cd "$DIR"
python3 -m http.server "$PORT" --bind 127.0.0.1 &
SERVER_PID=$!
sleep 0.8

# Run puppeteer-core screenshot
NODE_PATH="$NODE_PATH" node -e "
const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '$CHROME',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({width: $WIDTH, height: 900});
  await page.goto('http://127.0.0.1:$PORT/$NAME', {waitUntil: 'networkidle0', timeout: 15000});
  const height = await page.evaluate(() => document.documentElement.scrollHeight);
  await page.setViewport({width: $WIDTH, height: height});
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({path: '$OUTPUT', fullPage: true});
  await browser.close();
  console.log('OK: ' + height + 'px');
})().catch(e => { console.error(e.message); process.exit(1); });
" 2>&1

echo "Screenshot saved: $OUTPUT"
