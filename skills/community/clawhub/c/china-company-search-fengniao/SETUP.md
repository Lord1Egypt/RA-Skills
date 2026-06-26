# Fengniao China Company Search — Setup Guide

## Works Out of the Box

No configuration required. A built-in public API key is included and used automatically.

If you have a paid Fengniao account, set your private key as an environment variable `FN_API_KEY` — it will take priority over the built-in key.

## Prerequisites

- Node.js 18 or higher

Verify your Node.js version:

```bash
node -v
```

## Quota

The built-in public key has a daily usage limit (200 calls). Current quota and remaining usage are shown at https://www.riskbird.com/skills.

When the API returns `code=9999` with a message containing "访问已达上限", the daily public quota is exhausted. Configure a private key or retry the next day.

## Setting a Private API Key (Optional)

Set temporarily in the current terminal session (expires when terminal closes).

**macOS / Linux**

```bash
export FN_API_KEY="your-api-key"
```

**Windows PowerShell**

```powershell
$env:FN_API_KEY = "your-api-key"
```

**Windows CMD**

```cmd
set FN_API_KEY=your-api-key
```

## Local Verification

```bash
# 1. Test tool discovery (no network required)
node scripts/tool.mjs discover "company shareholders"

# 2. Test fuzzy search (requires API key, must use Chinese company name)
node scripts/tool.mjs call biz_fuzzy_search --params '{"key":"腾讯"}'

# 3. Test dimension query (use entid from previous step)
node scripts/tool.mjs call biz_basic_info --params '{"entid":"AerjZTfkSh0"}'
```

## Security Boundaries

- Credentials are read from the environment variable `FN_API_KEY` (or built-in fallback)
- Only reads `tools.json` and `references/` files within the skill package
- Does not read user home directory, agent config, or shell startup files
- Does not write any local files
- API credentials are sent via URL parameter `apikey`, not HTTP headers

## Production Note

The public release uses the production endpoint `https://m.riskbird.com/prod-qbb-api`. If you need to switch endpoints for a private deployment, fork the skill and modify the source — do not expose switchable endpoints in a public marketplace package.
