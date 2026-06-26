---
name: botcall
description: Phone numbers for AI agents. Provision numbers, receive SMS, extract verification codes. Use when you need to sign up for services, receive 2FA codes, or handle phone verification.
homepage: https://botcall.io
metadata:
  clawdbot:
    emoji: "📱"
    requires:
      env: [BOTCALL_API_KEY]
      bins: [botcall]
    primaryEnv: BOTCALL_API_KEY
    install:
      - id: botcall-cli
        kind: node
        package: botcall
        bins: [botcall]
        label: Install botcall CLI (npm)
---

# botcall - Phone Numbers for AI Agents

Provision phone numbers and receive SMS verification codes.

## Setup

1. Get an API key at https://botcall.io
2. Authenticate:
```bash
botcall auth login --api-key bs_live_YOUR_KEY
```

## Commands

### Check your plan and usage
```bash
botcall usage
```

### Provision a phone number
```bash
botcall provision
botcall provision --area-code 206  # Seattle area code
```

### List your numbers
```bash
botcall list
```

### View received messages
```bash
botcall inbox
botcall inbox --limit 20
```

### Wait for verification code
```bash
botcall get-code              # Wait up to 120s
botcall get-code --timeout 60 # Custom timeout
```
Returns just the code (e.g., `847291`) for easy parsing.

### Release a number
```bash
botcall release <number-id>
```

### Upgrade plan
```bash
botcall upgrade starter  # $9/mo - 1 number, 100 SMS
botcall upgrade pro      # $29/mo - 5 numbers, 500 SMS
```

### Manage billing
```bash
botcall billing  # Opens Stripe portal
```

## Example: Sign up for a service

```bash
# 1. Get a number
botcall provision --area-code 415
# Output: +14155551234

# 2. Use number to sign up (your agent does this)

# 3. Wait for verification code
CODE=$(botcall get-code --timeout 120)
echo "Code received: $CODE"

# 4. Enter code to complete signup
```

## MCP Integration

For Claude Desktop/Cursor, add to your MCP config:

```json
{
  "mcpServers": {
    "botcall": {
      "command": "npx",
      "args": ["@botcallio/mcp"],
      "env": {
        "BOTCALL_API_KEY": "bs_live_YOUR_KEY"
      }
    }
  }
}
```

## Pricing

- **Free**: No numbers (signup only)
- **Starter** ($9/mo): 1 number, 100 SMS
- **Pro** ($29/mo): 5 numbers, 500 SMS

## Links

- Website: https://botcall.io
- npm CLI: https://www.npmjs.com/package/botcall
- MCP: https://www.npmjs.com/package/@botcallio/mcp
