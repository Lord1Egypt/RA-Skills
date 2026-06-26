---
name: boxed-http-server
description: "WebAssembly sandbox static HTTP server with HTTP Basic auth and proxy support. Use when starting a static file server, configuring HTTP authentication, setting up HTTP proxy/reverse proxy, or running a local development server."
---

# boxed-http-server

A lightweight static HTTP server based on WebAssembly sandbox, with support for HTTP Basic authentication and HTTP proxy/reverse proxy.

## Trigger When

Use this skill when the user describes (触发场景):

- **Starting a static file server** (启动静态文件服务器)
- **Configuring HTTP Basic authentication** (配置 HTTP 认证)
- **Setting up HTTP proxy or reverse proxy** (设置 HTTP 代理或反向代理)
- **Running a local development server** (搭建本地开发服务器)
- **Deploying a static website** (部署静态网站)
- **Adding authentication to a static site** (为静态网站添加认证保护)

## Prerequisites

- **openclaw-wasm-sandbox plugin**: Must be installed and enabled, version `>=0.4.0`
- **wasm file download**: Download required before first use

## Download wasm File

```js
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-http-server/files/boxed_http_server_component.wasm",
  dest: "~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm"
})
```

Or via command line:

```bash
curl -L -o ~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm \
  "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-http-server/files/boxed_http_server_component.wasm"
```

## Start Static File Server

```js
wasm-sandbox-serve({
  wasmFile: "~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm",
  workDir: ["~/.openclaw/skills/boxed-http-server/files"]
})
```

Or via command line:

```bash
openclaw wasm-sandbox serve ~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm \
  -i 192.168.1.100 -p 8080 --work-dir /path/to/website
```

## HTTP Basic Authentication

Protect your website with username/password authentication:

```js
wasm-sandbox-serve({
  wasmFile: "~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm",
  workDir: ["~/.openclaw/skills/boxed-http-server/files"],
  args: ["--config-var", "username=admin", "--config-var", "password=admin"]
})
```

## HTTP Proxy / Reverse Proxy

Proxy external APIs through the server. Requires `allowedOutboundHosts` for the target domain:

```js
wasm-sandbox-serve({
  wasmFile: "~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm",
  workDir: ["~/.openclaw/skills/boxed-http-server/files"],
  allowedOutboundHosts: ["https://httpbin.org"],
  args: ["--config-var", "proxy=\"[{\\\"path\\\": \\\"/httpbin\\\",\\\"target\\\" :\\\"https://httpbin.org\\\",\\\"headers\\\": {\\\"Authorization\\\": \\\"Bearer abcd1234\\\"}}]\""]
})
```

## Combined Example: Static Site + API Proxy

Serve a static website while proxying external APIs to avoid CORS issues:

```js
wasm-sandbox-serve({
  wasmFile: "~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm",
  workDir: ["/home/user/website"],
  allowedOutboundHosts: ["https://api.weather.com", "https://wttr.in"],
  args: ["--config-var", "proxy=\"[{\\\"path\\\": \\\"/weather\\\",\\\"target\\\": \\\"https://wttr.in\\\"}]\""]
})
```

Then update your frontend to call `/weather` instead of the external API directly.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wasmFile` | string | Yes | Path to the wasm component file |
| `workDir` | string[] | Yes | Website root directories (served as static files) |
| `allowedOutboundHosts` | string[] | No | Allowed external domains for proxy mode |
| `args` | string[] | No | Command-line args for auth and proxy config |

### CLI Options (for openclaw wasm-sandbox serve)

| Option | Short | Description |
|--------|-------|-------------|
| `--ip <ip>` | `-i` | Socket IP to bind to |
| `--port <port>` | `-p` | Socket port to bind to (0-65535) |
| `--work-dir <dir>` | | Website root directory |
| `--config-var <var>` | | WASI config variables |
| `--allowed-outbound-hosts <hosts>` | | Allowed external domains (proxy mode) |

### Available args Config

- `--config-var username=<username>` - Set Basic auth username
- `--config-var password=<password>` - Set Basic auth password
- `--config-var proxy=<JSON>` - Set proxy rules in JSON format

### proxy Config Format

```json
[
  {
    "path": "/httpbin",
    "target": "https://httpbin.org",
    "headers": {
      "Authorization": "Bearer abcd1234"
    }
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Proxy path prefix (requests matching this prefix will be proxied) |
| `target` | string | Target full URL |
| `headers` | object | Optional custom headers to add to the proxied request |

## Security Model

Boxed HTTP Server runs inside WebAssembly sandbox with capability-based security:

- **No implicit access**: WASM module has zero access by default
- **Explicit grants only**: Access must be explicitly allowed via configuration
- **Network isolation**: Outbound network access is denied by default
- **Resource limits**: Supports timeout, memory, stack size, and fuel limits

## Architecture

```
User Request
    ↓
OpenClaw Gateway
    ↓
Wasm Sandbox Plugin
    ↓
boxed_http_server_component.wasm
    ↓
├── Static File Handler (workDir)
├── Basic Auth Handler (args: username/password)
└── Proxy Handler (args: proxy config)
    ↓
Response to Client
```

## Example: Full Deployment

Deploy a static website at `http://192.168.158.134:8080`:

```bash
# 1. Download wasm file (if not exists)
curl -L -o ~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm \
  "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-http-server/files/boxed_http_server_component.wasm"

# 2. Start server
openclaw wasm-sandbox serve \
  ~/.openclaw/skills/boxed-http-server/files/boxed_http_server_component.wasm \
  -i 192.168.158.134 \
  -p 8080 \
  --work-dir /home/user/website
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "wasm file not found" | Run the download step first |
| "Connection refused" | Check IP and port, ensure firewall allows access |
| "CORS errors in frontend" | Use proxy mode to route external APIs through the server |
| "Authentication not working" | Ensure username and password are set in args |
| "Proxy returns 403" | Add target domain to allowedOutboundHosts |
