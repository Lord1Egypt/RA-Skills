---
name: content-scrubber
version: 1.0.0
description: "OpenClaw plugin that scrubs private infrastructure details from outgoing messages. Regex-based redaction of RFC 1918 IPs, localhost ports, SSH targets, and hostnames before they reach Discord, Telegram, or other messaging surfaces."
---

# Content Scrubber

An OpenClaw extension plugin that intercepts outgoing messages and redacts private infrastructure details before delivery.

## What It Catches

- **RFC 1918 IPv4 addresses**: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
- **Loopback addresses**: 127.x.x.x
- **localhost with ports**: localhost:8080, localhost:3000, etc.
- **SSH/SCP targets**: user@10.0.0.1:/path
- **Custom hostnames**: configurable hostname patterns

## How It Works

The plugin registers as a message interceptor. Before any message leaves OpenClaw (Discord, Telegram, Signal, etc.), it runs through regex-based scrubbing rules that replace private details with safe placeholders like `[redacted-ip]`, `[redacted-service]`, `[redacted-target]`.

Rules are deterministic (regex, not LLM), so they're fast, auditable, and never miss edge cases that an LLM scrubber would.

## Installation

1. Copy the plugin files to your OpenClaw extensions directory:
   ```
   ~/.openclaw/extensions/content-scrubber/
   ├── index.ts
   ├── openclaw.plugin.json
   └── package.json
   ```

2. Add to your `openclaw.json` plugins config:
   ```json
   {
     "plugins": {
       "entries": {
         "content-scrubber": {
           "enabled": true,
           "config": {
             "dryRun": false,
             "allowedRecipients": []
           }
         }
       }
     }
   }
   ```

3. Restart OpenClaw.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dryRun` | boolean | false | Log what would be scrubbed without actually redacting |
| `allowedRecipients` | string[] | [] | Chat IDs where scrubbing is skipped (e.g., private DMs with yourself) |

## Example

**Before scrubbing:**
> SSH into admin@10.0.0.50 and check the service on localhost:8096

**After scrubbing:**
> SSH into [redacted-target] and check the service on [redacted-service]
