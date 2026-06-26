---
name: boxed_curl
description: Run curl requests safely in a sandbox, supporting GET/POST/HTTP headers, with complete network isolation.
---

# Boxed Curl Skill

Run curl-like HTTP requests safely within a WASM sandbox with network access control.

## Triggering Method

Use this skill when the user says:

- "boxed curl", "boxed curl"
- "Sandbox version of curl", "Sandbox curl", "Secure curl"
- "Make a request using boxed-curl", "Help me with boxed-curl"
- "Send a secure HTTP request", "Secure GET/POST request"
- "沙箱版 curl"、"沙箱 curl"、"安全的 curl"
- "用 boxed-curl 请求"、"帮我 boxed-curl"
- "发一个安全的 HTTP 请求"、"安全的 GET/POST 请求"

## ⚠️ Required Plugin

**This skill requires the `openclaw-wasm-sandbox` plugin version `>= 0.2.0`.**

The `wasm-sandbox-download` tool was added in version 0.2.0. If the plugin is not installed or version is lower:

```bash
openclaw plugins install clawhub:openclaw-wasm-sandbox
openclaw plugins update openclaw-wasm-sandbox
openclaw gateway restart
```

Verify the version:
```bash
openclaw plugins inspect openclaw-wasm-sandbox
```

Look for `Version: 0.2.0` or higher in the output.

## ⚠️ WASM File Required

**This skill requires the WASM component file to be downloaded first.**

If the WASM file does not exist locally, use the `wasm-sandbox-download` tool to download it:

### Step 0: Download WASM File

```javascript
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-curl/files/boxed_curl_component.wasm",
  output: "<skill_dir>/files/boxed_curl_component.wasm",
  resume: false,
  timeout: 60000
})
```

**Important:** Set `resume: false` for initial download. The download destination is `github.com` which supports resume.

## Tool: wasm-sandbox-run

Use the `wasm-sandbox-run` tool to execute the WASM component after the WASM file is available.

## How It Works

1. **Check for WASM file** — If not found, download using `wasm-sandbox-download`
2. User provides curl-like arguments (URL with optional options)
3. AI extracts the URL and any curl options
4. AI determines `allowedOutboundHosts` based on the target host
5. AI calls `wasm-sandbox-run` with the arguments and network permissions

## Supported Features

| Option | Description | Status |
|--------|-------------|--------|
| `-X, --request METHOD` | HTTP method (GET, POST, PUT, DELETE, etc.) | ✅ |
| `-H, --header HEADER` | Add request header | ✅ |
| `-d, --data DATA` | Request body data | ✅ |
| `-i, --include` | Include response headers | ✅ |
| `-L, --location` | Follow redirects | ✅ |
| `-v, --verbose` | Verbose output | ✅ |
| `-o, --output FILE` | Output to file | ⚠️ Not supported |

## Usage Pattern

### Step 1: Extract Arguments

Parse the user's input:
- **URL** — the target endpoint
- **curl options** — `-X`, `-H`, `-d`, etc.
- **`allowedOutboundHosts`** — if user explicitly provided it

### Step 2: Determine Network Access

If user did NOT specify `allowedOutboundHosts`, infer from URL:

| URL Pattern | `allowedOutboundHosts` |
|-------------|------------------------|
| `https://api.github.com/*` | `https://api.github.com` |
| `https://httpbin.org/*` | `https://httpbin.org` |
| `https://raw.githubusercontent.com/*` | `https://raw.githubusercontent.com` |
| Any HTTPS URL | `https://<host>` (extract host from URL) |

### Step 3: Call wasm-sandbox-run

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://<target-host>"],
  args: ["<curl options>", "<URL>"]
})
```

## Examples

### GET Request
User says: "fetch data from https://httpbin.org/get"

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://httpbin.org"],
  args: ["https://httpbin.org/get"]
})
```

### POST with JSON Body
User says: `curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"name":"value"}'`

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://httpbin.org"],
  args: ["-X", "POST", "-H", "Content-Type:application/json", "-d", "{\"name\":\"value\"}", "https://httpbin.org/post"]
})
```

### GET with Headers
User says: "fetch with custom Authorization header"

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://httpbin.org"],
  args: ["-H", "Authorization:Bearer token123", "https://httpbin.org/get"]
})
```

### GitHub API Request
User says: "get GitHub user info for 'octocat'"

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://api.github.com"],
  args: ["https://api.github.com/users/octocat"]
})
```

### GET with Response Headers
User says: "fetch with -i flag to see response headers"

```javascript
wasm-sandbox-run({
  wasmFile: "<skill_dir>/files/boxed_curl_component.wasm",
  allowedOutboundHosts: ["https://httpbin.org"],
  args: ["-i", "https://httpbin.org/get"]
})
```

## Important Notes

- **Always set `allowedOutboundHosts`** — sandbox blocks all outbound HTTP by default
- **Download WASM first if missing** — use `wasm-sandbox-download` tool
- **Extract host from URL** automatically when user doesn't specify
- **Use `/post` endpoint for POST** — `/get` returns 405 Method Not Allowed
- **args order**: curl options first, URL last
- **JSON in -d**: escape quotes properly (e.g., `{\"key\":\"value\"}`)
