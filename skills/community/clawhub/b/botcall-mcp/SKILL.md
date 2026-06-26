---
name: botcall-mcp
description: Give your AI agent a real phone number for SMS verification. Provisions numbers, receives SMS, and extracts verification codes via the botcall API. Requires a BOTCALL_API_KEY from botcall.io.
---

# botcall-mcp

An MCP server that gives AI agents real phone numbers. Provision a number, receive SMS, and extract verification codes — all through tool calls.

## Setup

Install the MCP server:

```bash
claude mcp add botcall -- npx -y botcall-mcp
```

Then set your API key:

```bash
export BOTCALL_API_KEY="bs_live_..."
```

Or add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "botcall": {
      "command": "npx",
      "args": ["-y", "botcall-mcp"],
      "env": {
        "BOTCALL_API_KEY": "bs_live_..."
      }
    }
  }
}
```

## Get an API Key

Sign up at [botcall.io](https://botcall.io), pick a plan, and grab your key from Dashboard → API Keys.

## Tools

| Tool | Description |
|------|-------------|
| `provision_number` | Provision a new phone number (optional: area code, country) |
| `list_numbers` | List your provisioned phone numbers |
| `release_number` | Release a phone number |
| `get_inbox` | Get recent SMS messages |
| `get_code` | Wait for an SMS and extract the verification code (long-polls up to 30s) |
| `get_usage` | Get your plan, limits, and usage stats |

## Example Workflow

1. Call `provision_number` to get a phone number
2. Use the number to sign up for a service that requires SMS verification
3. Call `get_code` — it waits for the SMS and returns the extracted code
4. Enter the code to complete verification

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BOTCALL_API_KEY` | **Required.** Your API key from botcall.io |
| `BOTCALL_API_URL` | API base URL (default: `https://api.botcall.io`) |

## Resources

- [botcall.io](https://botcall.io) — sign up and manage your account
- [GitHub](https://github.com/danecodes/botcall-mcp) — source code
- [npm](https://www.npmjs.com/package/botcall-mcp) — package
