# boxed-fetch Usage Guide

## Overview

boxed-fetch is a WebAssembly-based sandboxed web fetcher that retrieves URL content and extracts readable text. It provides secure, lightweight web scraping without exposing your system to untrusted content.

## Prerequisites

- openclaw-wasm-sandbox plugin installed
- WASM file downloaded to `~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm`

## First-Time Setup

Download the WASM file:

```javascript
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fetch/files/boxed-fetch-component.wasm",
  dest: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm"
})
```

## Core Usage

### Basic Fetch

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://example.com"],
  args: ["https://example.com"]
})
```

### Extract Readable Text

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://news.ycombinator.com"],
  args: ["https://news.ycombinator.com", "--text"]
})
```

### Pretty Print Output

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://github.com"],
  args: ["https://github.com", "--pretty"]
})
```

### Custom Headers

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://api.github.com"],
  args: ["https://api.github.com/users/guyoung", "--header", "Accept: application/json"]
})
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message with all available options |
| `--text` | Extract only readable text content |
| `--pretty` | Format JSON output with pretty printing |
| `--header <header>` | Add custom request header (can be repeated) |

## allowedOutboundHosts Examples

The `allowedOutboundHosts` parameter is **required** and must contain the exact host(s) you want to fetch from.

### Single Host

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://github.com"],
  args: ["https://github.com/guyoung"]
})
```

### Multiple Hosts

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://github.com", "https://api.github.com"],
  args: ["https://github.com", "--text"]
})
```

## Common Use Cases

### Fetching GitHub README

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://raw.githubusercontent.com"],
  args: ["https://raw.githubusercontent.com/guyoung/wasm-sandbox-node/main/README.md"]
})
```

### Extracting Article Content

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://blog.example.com"],
  args: ["https://blog.example.com/articles/how-to-use", "--text"]
})
```

### Getting API JSON Response

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fetch/files/boxed-fetch-component.wasm",
  allowedOutboundHosts: ["https://api.github.com"],
  args: ["https://api.github.com/repos/guyoung/wasm-sandbox-node", "--pretty"]
})
```

## Security Model

- **Sandboxed Execution**: Runs in WebAssembly sandbox with no access to system resources
- **Host Allowlist**: Only explicitly listed hosts can be accessed
- **HTTPS Only**: Only HTTPS URLs are permitted
- **No Cookie Propagation**: Cookies are isolated per request
