---
name: exmail-mcp-setup
description: Set up a Tencent enterprise email MCP connector for WorkBuddy. Use this when the user wants to connect exmail to read and search emails. Replaces the broken mcp-email npm package.
agent_created: true
---

# Tencent Enterprise Email MCP Setup

Set up a custom MCP server to connect Tencent enterprise email (exmail.qq.com) to WorkBuddy.
Provides three tools: `get_recent_emails`, `search_emails`, `get_email_content`.

## Prerequisites

Two pieces of information are required from the user:

1. **Email address**: e.g. `user@company.com`
2. **Auth code (客户端专用密码)**: generated in exmail admin panel, NOT the login password.
   Path: exmail.qq.com → Settings → Account → Client-specific password → Generate

Ask for these if not provided. The email type is always `exmail`, do not ask about it.

## Why Not Use the `mcp-email` npm Package

The `mcp-email` package on npm is broken for WorkBuddy:

1. **stdout pollution**: Contains `console.log()` calls that write to stdout, corrupting MCP's JSON-RPC protocol over stdio. MCP requires stdout to carry only JSON-RPC messages.
2. **NODE_OPTIONS conflict**: WorkBuddy's runtime sets `NODE_OPTIONS=--use-system-ca` which modern Node.js rejects, killing the process immediately.
3. **Old MCP SDK**: Uses SDK v0.6.1, incompatible with current WorkBuddy's MCP client.

**Do NOT use `mcp-email`.** Always deploy the custom server below.

## Deployment Steps

### Step 1: Create the MCP server directory

```bash
mkdir -p ~/.workbuddy/mcp-servers/exmail-mcp
```

### Step 2: Copy the reference server code

The working server code is at `references/index.js` in this skill. Copy it:

```bash
cp <skill-path>/references/index.js ~/.workbuddy/mcp-servers/exmail-mcp/index.js
```

### Step 3: Install dependencies

Use the **managed Node.js** binary, NOT the system one:

```bash
cd ~/.workbuddy/mcp-servers/exmail-mcp
~/.workbuddy/binaries/node/versions/22.12.0/bin/npm init -y
~/.workbuddy/binaries/node/versions/22.12.0/bin/npm pkg set type=module
~/.workbuddy/binaries/node/versions/22.12.0/bin/npm install @modelcontextprotocol/sdk imap mailparser nodemailer dotenv
```

### Step 4: Configure mcp.json

Read `~/.workbuddy/mcp.json` first to check for existing MCP servers. Add the `exmail` entry to the `mcpServers` object:

```json
{
  "mcpServers": {
    "exmail": {
      "command": "$HOME/.workbuddy/binaries/node/versions/22.12.0/bin/node",
      "args": [
        "$HOME/.workbuddy/mcp-servers/exmail-mcp/index.js"
      ],
      "env": {
        "EMAIL_USER": "<user@company.com>",
        "EMAIL_PASSWORD": "<auth-code>",
        "NODE_OPTIONS": "",
        "NODE_TLS_REJECT_UNAUTHORIZED": "0"
      }
    }
  }
}
```

Key points:
- Use **absolute paths** to the managed Node.js binary. Never use `npx`.
- `"NODE_OPTIONS": ""` is CRITICAL — clears the `--use-system-ca` that crashes the process.
- `"NODE_TLS_REJECT_UNAUTHORIZED": "0"` avoids TLS issues on exmail IMAP.

### Step 5: Tell the user to enable the connector

After writing mcp.json, tell the user:
- Open WorkBuddy connector management page
- Find `exmail` entry
- Click "Trust" (信任) to enable

### Step 6: Verify

After the user enables it, test with the `mcp__exmail__get_recent_emails` tool (or `search_emails` / `get_email_content`).

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Connection closed (-32000)` | stdout polluted or NODE_OPTIONS conflict | Verify `NODE_OPTIONS: ""` in env and no `console.log` in index.js |
| Process exits immediately | stdin EOF | Normal — WorkBuddy keeps pipe open, only fails in manual `< /dev/null` tests |
| `imap` module not found | Missing dependency | Re-run `npm install` in the server directory |
| Login failed | Wrong password | Use auth code (客户端专用密码), not login password |

## How to Test Before Enabling (Optional)

Use a Node.js spawn test script instead of piping to stdin — piping won't work because the MCP server reads from stdin and a pipe that closes will kill it:

```js
import { spawn } from 'child_process';
const s = spawn(nodePath, [serverPath], {
  env: { EMAIL_USER: '...', EMAIL_PASSWORD: '...', NODE_OPTIONS: '', NODE_TLS_REJECT_UNAUTHORIZED: '0' },
  stdio: ['pipe', 'pipe', 'pipe']
});
s.stdout.on('data', d => console.log(d.toString()));
s.stderr.on('data', d => console.error('STDERR:', d.toString()));
s.stdin.write(JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2024-11-05',capabilities:{},clientInfo:{name:'test',version:'1.0'}}}) + '\n');
```

If the response includes `"result":{"protocolVersion":"2024-11-05"...}`, the server is working.
