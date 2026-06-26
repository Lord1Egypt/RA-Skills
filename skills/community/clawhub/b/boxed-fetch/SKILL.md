---
name: boxed-fetch
description: "Lightweight web scraping tool based on WebAssembly sandbox mechanism. Fetches URL content and extracts readable text. Use when you need to fetch webpage content, extract readable text from HTML, or perform sandboxed HTTP requests. Requires openclaw-wasm-sandbox plugin. Trigger when: user asks to fetch a URL, scrape webpage content, extract readable text from HTML, or get page content from a specific URL / 抓取网页、获取URL内容、提取可读文本、网页内容抓取。"
---

# boxed-fetch

WebAssembly-based sandboxed web fetcher for retrieving URL content and extracting readable text.

**Trigger when:** user asks to fetch a URL, scrape webpage content, extract readable text from HTML, or get page content from a specific URL / 抓取网页、获取URL内容、提取可读文本、网页内容抓取。

## Quick Start

1. **Download WASM file** (first time only):
   ```
   wasm-sandbox-download({
     url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fetch/files/boxed-fetch-component.wasm",
     dest: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm"
   })
   ```

2. **Run fetch**:
   ```
   wasm-sandbox-run({
     wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
     allowedOutboundHosts: ["<target-host>"],
     args: ["<target-url>"]
   })
   ```

## Fetching a URL

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://github.com"],
  args: ["https://github.com/guyoung/wasm-sandbox-node/blob/main/README.md"]
})
```

## Getting Help

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: [],
  args: ["--help"]
})
```

## Important Notes

- **allowedOutboundHosts is required**: You must specify the exact host(s) you want to fetch from
- **First use**: Download the WASM file before running for the first time
- **URLs must use HTTPS**: The sandbox only supports HTTPS URLs

## Detailed Usage

See [references/usage.md](references/usage.md) for comprehensive usage instructions including all options and examples.
