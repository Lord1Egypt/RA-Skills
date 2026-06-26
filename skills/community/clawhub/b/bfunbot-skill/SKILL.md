---
name: bfunbot
description: Create tokens on BSC, check fee earnings, check BFun.bot Credits balance, trigger agent credit reload, and interact with BFunBot's Agent API and BFun LLM Gateway. Use when asked to create a token via BFunBot, check fee earnings on BSC, check BFunBot BFun.bot Credits balance, check daily token creation quota, reload credits from trading wallet, or make LLM calls through BFunBot's gateway.
---

# BFunBot Skill

Create tokens on BSC, earn trading fees, and use BFunBot's BFun LLM Gateway — all from natural language commands.

**Version:** 1.0.0  
**Provider:** [BFunBot](https://bfun.bot)  
**Auth:** API key required — get yours at [bfun.bot/settings/api-keys](https://bfun.bot/settings/api-keys)  
**Install:** `install the bfunbot skill from https://github.com/BFunBot/skills/tree/main/bfunbot`

---

## Setup

### Step 1 — Get your API key
Go to [bfun.bot/settings/api-keys](https://bfun.bot/settings/api-keys) → Create API Key → copy the `bfbot_...` key.

> **Permissions:** Base API is always included. Enable **BFun LLM Gateway** if you want to use AI models. Enable **Agent Reload** if you want the agent to top up your BFun.bot Credits automatically from your trading wallet.

### Step 2 — Add BFun.bot Credits (for AI model access)
Go to [bfun.bot/credits](https://bfun.bot/credits) → Add Credit.  
Minimum $1 to start. Credits are consumed per token used.

### Step 3 — Set up BFun LLM Gateway *(optional)*
> This step registers BFunBot as your agent's AI model provider, so your agent *thinks* using Claude/GPT/Gemini billed to your BFun.bot Credits — instead of paying Anthropic/OpenAI directly. It's separate from the Agent API skill.
>
> **OpenClaw users:** follow the config below. If you're using LangChain, CrewAI, or any OpenAI-compatible framework, point your `base_url` to `https://llm.bfun.bot/v1` with your `bfbot_...` API key instead.
>
> **OpenClaw users** — add BFunBot as an LLM provider in `~/.openclaw/openclaw.json`. This is the full config with all available models — you only need to include the models you want to use.

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bfunbot": {
        "baseUrl": "https://llm.bfun.bot",
        "apiKey": "YOUR_BFBOT_API_KEY",
        "api": "openai-completions",
        "models": [
          { "id": "bfunbot-opus-4-6",              "name": "Claude Opus 4.6",          "api": "anthropic-messages", "contextWindow": 1000000,  "maxTokens": 128000 },
          { "id": "bfunbot-opus-4-5",              "name": "Claude Opus 4.5",          "api": "anthropic-messages", "contextWindow": 200000,   "maxTokens": 64000  },
          { "id": "bfunbot-sonnet-4-6",            "name": "Claude Sonnet 4.6",        "api": "anthropic-messages", "contextWindow": 1000000,  "maxTokens": 128000 },
          { "id": "bfunbot-sonnet-4-5",            "name": "Claude Sonnet 4.5",        "api": "anthropic-messages", "contextWindow": 1000000,  "maxTokens": 64000  },
          { "id": "bfunbot-haiku-4-5",             "name": "Claude Haiku 4.5",         "api": "anthropic-messages", "contextWindow": 200000,   "maxTokens": 4096   },
          { "id": "bfunbot-gpt-5-4-pro",           "name": "GPT 5.4 Pro",              "contextWindow": 1050000,    "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-4",               "name": "GPT 5.4",                  "contextWindow": 1050000,    "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-4-mini",          "name": "GPT 5.4 Mini",             "contextWindow": 400000,     "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-4-nano",          "name": "GPT 5.4 Nano",             "contextWindow": 400000,     "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-2-pro",           "name": "GPT 5.2 Pro",              "contextWindow": 400000,     "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-2",               "name": "GPT 5.2",                  "contextWindow": 400000,     "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-2-codex",         "name": "GPT 5.2 Codex",            "contextWindow": 400000,     "maxTokens": 16384 },
          { "id": "bfunbot-gpt-5-2-chat",          "name": "GPT 5.2 Chat",             "contextWindow": 128000,     "maxTokens": 16384 },
          { "id": "bfunbot-gemini-3-1-pro",        "name": "Gemini 3.1 Pro",           "contextWindow": 1048576,    "maxTokens": 16384 },
          { "id": "bfunbot-gemini-3-1-flash-lite", "name": "Gemini 3.1 Flash Lite",    "contextWindow": 1048576,    "maxTokens": 16384 },
          { "id": "bfunbot-gemini-3-flash",        "name": "Gemini 3 Flash",           "contextWindow": 1048576,    "maxTokens": 16384 },
          { "id": "bfunbot-gemini-2-5-pro",        "name": "Gemini 2.5 Pro",           "contextWindow": 1048576,    "maxTokens": 8192  },
          { "id": "bfunbot-gemini-2-5-flash",      "name": "Gemini 2.5 Flash",         "contextWindow": 1048576,    "maxTokens": 8192  },
          { "id": "bfunbot-grok-4-1",              "name": "Grok 4.1 Fast",            "contextWindow": 2000000,    "maxTokens": 16384 },
          { "id": "bfunbot-deepseek-v3-2",         "name": "DeepSeek V3.2",            "contextWindow": 164000,     "maxTokens": 16384 },
          { "id": "bfunbot-kimi-k2-5",             "name": "Kimi K2.5",                "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-mimo-v2-pro",           "name": "MiMo-V2-Pro",              "contextWindow": 1048576,    "maxTokens": 16384 },
          { "id": "bfunbot-mimo-v2-omni",          "name": "MiMo-V2-Omni",             "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-mimo-v2-flash",         "name": "MiMo-V2-Flash",            "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-seed-2-0-lite",         "name": "Seed 2.0 Lite",            "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-seed-2-0-mini",         "name": "Seed 2.0 Mini",            "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-qwen-3-coder",          "name": "Qwen3 Coder",              "contextWindow": 262144,     "maxTokens": 16384 },
          { "id": "bfunbot-qwen-3-5-plus",         "name": "Qwen3.5 Plus",             "contextWindow": 1000000,    "maxTokens": 16384 },
          { "id": "bfunbot-qwen-3-5-flash",        "name": "Qwen3.5 Flash",            "contextWindow": 1000000,    "maxTokens": 16384 },
          { "id": "bfunbot-minimax-m2-7",          "name": "MiniMax M2.7",             "contextWindow": 204800,     "maxTokens": 16384 },
          { "id": "bfunbot-minimax-m2-5",          "name": "MiniMax M2.5",             "contextWindow": 196608,     "maxTokens": 16384 },
          { "id": "bfunbot-glm-5-turbo",           "name": "GLM 5 Turbo",              "contextWindow": 202752,     "maxTokens": 16384 },
          { "id": "bfunbot-glm-5",                 "name": "GLM 5",                    "contextWindow": 80000,      "maxTokens": 16384 }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "bfunbot/bfunbot-opus-4-6":              { "alias": "bfunbot-opus-4-6" },
        "bfunbot/bfunbot-opus-4-5":              { "alias": "bfunbot-opus-4-5" },
        "bfunbot/bfunbot-sonnet-4-6":            { "alias": "bfunbot-sonnet-4-6" },
        "bfunbot/bfunbot-sonnet-4-5":            { "alias": "bfunbot-sonnet-4-5" },
        "bfunbot/bfunbot-haiku-4-5":             { "alias": "bfunbot-haiku-4-5" },
        "bfunbot/bfunbot-gpt-5-4-pro":           { "alias": "bfunbot-gpt-5-4-pro" },
        "bfunbot/bfunbot-gpt-5-4":               { "alias": "bfunbot-gpt-5-4" },
        "bfunbot/bfunbot-gpt-5-4-mini":          { "alias": "bfunbot-gpt-5-4-mini" },
        "bfunbot/bfunbot-gpt-5-4-nano":          { "alias": "bfunbot-gpt-5-4-nano" },
        "bfunbot/bfunbot-gpt-5-2-pro":           { "alias": "bfunbot-gpt-5-2-pro" },
        "bfunbot/bfunbot-gpt-5-2":               { "alias": "bfunbot-gpt-5-2" },
        "bfunbot/bfunbot-gpt-5-2-codex":         { "alias": "bfunbot-gpt-5-2-codex" },
        "bfunbot/bfunbot-gpt-5-2-chat":          { "alias": "bfunbot-gpt-5-2-chat" },
        "bfunbot/bfunbot-gemini-3-1-pro":        { "alias": "bfunbot-gemini-3-1-pro" },
        "bfunbot/bfunbot-gemini-3-1-flash-lite": { "alias": "bfunbot-gemini-3-1-flash-lite" },
        "bfunbot/bfunbot-gemini-3-flash":        { "alias": "bfunbot-gemini-3-flash" },
        "bfunbot/bfunbot-gemini-2-5-pro":        { "alias": "bfunbot-gemini-2-5-pro" },
        "bfunbot/bfunbot-gemini-2-5-flash":      { "alias": "bfunbot-gemini-2-5-flash" },
        "bfunbot/bfunbot-grok-4-1":              { "alias": "bfunbot-grok-4-1" },
        "bfunbot/bfunbot-deepseek-v3-2":         { "alias": "bfunbot-deepseek-v3-2" },
        "bfunbot/bfunbot-kimi-k2-5":             { "alias": "bfunbot-kimi-k2-5" },
        "bfunbot/bfunbot-mimo-v2-pro":           { "alias": "bfunbot-mimo-v2-pro" },
        "bfunbot/bfunbot-mimo-v2-omni":          { "alias": "bfunbot-mimo-v2-omni" },
        "bfunbot/bfunbot-mimo-v2-flash":         { "alias": "bfunbot-mimo-v2-flash" },
        "bfunbot/bfunbot-seed-2-0-lite":         { "alias": "bfunbot-seed-2-0-lite" },
        "bfunbot/bfunbot-seed-2-0-mini":         { "alias": "bfunbot-seed-2-0-mini" },
        "bfunbot/bfunbot-qwen-3-coder":          { "alias": "bfunbot-qwen-3-coder" },
        "bfunbot/bfunbot-qwen-3-5-plus":         { "alias": "bfunbot-qwen-3-5-plus" },
        "bfunbot/bfunbot-qwen-3-5-flash":        { "alias": "bfunbot-qwen-3-5-flash" },
        "bfunbot/bfunbot-minimax-m2-7":          { "alias": "bfunbot-minimax-m2-7" },
        "bfunbot/bfunbot-minimax-m2-5":          { "alias": "bfunbot-minimax-m2-5" },
        "bfunbot/bfunbot-glm-5-turbo":           { "alias": "bfunbot-glm-5-turbo" },
        "bfunbot/bfunbot-glm-5":                 { "alias": "bfunbot-glm-5" }
      }
    }
  }
}
```

> **Note:** The `agents.defaults.models` block is required — it allowlists the models and registers aliases so both the model dropdown picker and `/model` command work correctly. The `alias` must match the model `id` exactly.

Set as default model (optional):
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "bfunbot/bfunbot-sonnet-4-6"
      }
    }
  }
}
```

Then restart OpenClaw:
```
openclaw gateway restart
```

Switch models using the dropdown picker or `/model` command:
```
/model bfunbot-opus-4-6
/model bfunbot-sonnet-4-6
/model bfunbot-haiku-4-5
/model bfunbot-gpt-5-4
/model bfunbot-gemini-3-1-pro
/model bfunbot-grok-4-1
/model bfunbot-deepseek-v3-2
```

### Available Models

**Anthropic**
| Model ID | Context |
|---|---|
| `claude-opus-4-6` | 1M |
| `claude-opus-4-5` | 200k |
| `claude-sonnet-4-6` | 1M |
| `claude-sonnet-4-5` | 1M |
| `claude-haiku-4-5` | 200k |

**OpenAI**
| Model ID | Context |
|---|---|
| `gpt-5.4-pro` | 1.05M |
| `gpt-5.4` | 1.05M |
| `gpt-5.4-mini` | 400k |
| `gpt-5.4-nano` | 400k |
| `gpt-5.2-pro` | 400k |
| `gpt-5.2` | 400k |
| `gpt-5.2-codex` | 400k |
| `gpt-5.2-chat` | 128k |

**Google**
| Model ID | Context |
|---|---|
| `gemini-3.1-pro` | 1M |
| `gemini-3.1-flash-lite` | 1M |
| `gemini-3-flash` | 1M |
| `gemini-2.5-pro` | 1M |
| `gemini-2.5-flash` | 1M |

**xAI**
| Model ID | Context |
|---|---|
| `grok-4.1-fast` | 2M |

**DeepSeek**
| Model ID | Context |
|---|---|
| `deepseek-v3.2` | 164k |

**Moonshot**
| Model ID | Context |
|---|---|
| `kimi-k2.5` | 262k |

**Xiaomi**
| Model ID | Context |
|---|---|
| `mimo-v2-pro` | 1M |
| `mimo-v2-omni` | 262k |
| `mimo-v2-flash` | 262k |

**ByteDance**
| Model ID | Context |
|---|---|
| `seed-2.0-lite` | 262k |
| `seed-2.0-mini` | 262k |

**Alibaba**
| Model ID | Context |
|---|---|
| `qwen3-coder` | 262k |
| `qwen3.5-plus` | 1M |
| `qwen3.5-flash` | 1M |

**MiniMax**
| Model ID | Context |
|---|---|
| `minimax-m2.7` | 205k |
| `minimax-m2.5` | 197k |

**Z.ai**
| Model ID | Context |
|---|---|
| `glm-5-turbo` | 203k |
| `glm-5` | 80k |

Verify by asking your agent: *"what's my BFunBot BFun.bot Credits balance?"*

---

## What This Skill Can Do

### BFun LLM Gateway
Use BFunBot-hosted AI models billed against your BFun.bot Credits. Same API key for LLM calls and agent actions.

- **Check balance:** "what's my BFunBot BFun.bot Credits balance?"
- **Add credits:** "I need to top up BFunBot credits" → agent links to bfun.bot/credits
- **Reload credits:** "reload my BFunBot credits from my trading wallet" (requires Agent Reload permission + configured on Credits page)
- **Model info:** "what models does BFunBot support?"

### Token Creation
Create tokens on BSC — BFunBot handles wallet creation, gas sponsorship, and on-chain deployment.

- "launch a token called MOON on BSC"
- "create a meme coin named PEPE with ticker $PEPE on fourmeme"
- "make a test token called DEMO on flap"

Token creation is async. After calling the API, poll the job status endpoint until complete (usually 30–60 seconds).

### Created Tokens
- "what tokens have I created on BFunBot?"
- "show my BFunBot token portfolio"

### Quota
- "how many free token launches do I have left today?"
- "what's my BFunBot quota on BSC?"

### Wallet Balances
- "what's my BFunBot wallet balance?"
- "show my BNB and USDT balances on BFunBot"

### Fee Earnings
Check creator fee earnings on BSC — data is read from pre-computed DB cache (fast, no on-chain calls).

- "what are my BFunBot fee earnings?"
- "show my fee earnings summary on BSC"
- "what have I earned from my flap tokens on BSC?"
- "what have I earned from my fourmeme tokens?"
- "how much has token 0x... earned on flap?"

### Token Lookup
- "what's the price of $MOON on BFunBot?"
- "look up token 0x... on BSC"

### Account
- "show me my BFunBot profile"
- "what's my BFunBot Twitter username and wallet address?"

### Skills
- "what can BFunBot do?" → calls GET /agent/v1/skills

---

## API Reference

**Base URL:** `https://api.bfun.bot/agent/v1`  
**Auth header:** `X-Api-Key: bfbot_...`

---

### GET /me
Returns user profile, wallet addresses, and account info.

Response:
```json
{
  "twitter_user_id": "...",
  "twitter_username": "...",
  "profile_image_url": "...",
  "followers_count": 1234,
  "joined_at": "2025-01-01T00:00:00Z"
}
```

---

### GET /skills
List all available BFunBot Agent API capabilities with examples. No auth required.

Response:
```json
{
  "skills": [
    {
      "name": "token_create",
      "description": "Deploy a new token on BSC",
      "example": "POST /agent/v1/token/create {\"name\": \"MyToken\", \"symbol\": \"MTK\", \"chain\": \"bsc\"}"
    }
  ],
  "total": 9
}
```

---

### POST /token/create
Create a token on BSC (async). Returns a `job_id` to poll.

Request:
```json
{
  "name": "MOON",
  "symbol": "MOON",
  "chain": "bsc",
  "description": "To the moon",
  "source_url": "https://x.com/user/status/123",
  "image_url": "https://...",
  "platform": "flap"
}
```

- `chain`: `bsc` only
- `source_url` (optional): Twitter/X post URL — tweet image used as token image if `image_url` not provided
- `image_url` (optional): HTTP/HTTPS URL or IPFS URI — overrides source tweet image
- `platform` (optional): `flap` | `fourmeme` — defaults to chain default if omitted

Response (`202 Accepted`):
```json
{
  "job_id": 12345,
  "status": "pending",
  "chain": "bsc",
  "quota": {
    "chain": "bsc",
    "free_used_today": 1,
    "free_limit": 3,
    "sponsored_remaining": 2
  }
}
```

Pre-check errors:
- `403 insufficient_followers` — need minimum followers to create tokens
- `402 insufficient_balance` — free quota used, trading wallet balance too low
- `429 daily_cap_exceeded` — absolute daily cap reached

---

### GET /jobs/{job_id}
Poll token creation status.

Response:
```json
{
  "job_id": 12345,
  "status": "completed",
  "chain": "bsc",
  "token_address": "0x...",
  "error": null,
  "created_at": "2026-01-01T00:00:00Z",
  "completed_at": "2026-01-01T00:01:00Z"
}
```

Status values: `pending` | `processing` | `completed` | `failed`

---

### GET /token/{address}
Get token info by address.

Query: `?chain=bsc` (optional)

Response:
```json
{
  "token_address": "0x...",
  "name": "MOON",
  "symbol": "MOON",
  "chain": "bsc",
  "platform": "flap",
  "creator_twitter_username": "...",
  "price_usd": "0.0001234",
  "market_cap_usd": "12340",
  "volume_24h_usd": "500",
  "creator_reward_usd": "1.23",
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

### GET /tokens/created
Get paginated list of tokens you have created.

Query: `?page=1&page_size=20`

Response:
```json
{
  "tokens": [
    {
      "token_address": "0x...",
      "name": "MOON",
      "symbol": "MOON",
      "chain": "bsc",
      "platform": "flap",
      "created_at": "2026-01-01T00:00:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20,
  "has_more": false
}
```

---

### GET /balance/credits
Get BFun.bot Credits balance and agent reload configuration.

Response:
```json
{
  "balance_usd": "4.92",
  "balance_usd_cents": 492,
  "agent_reload": {
    "enabled": true,
    "amount_usd": 5.0,
    "daily_limit_usd": 100.0,
    "chains": ["bsc"]
  }
}
```

`agent_reload` is `null` if not configured. `enabled: false` means agent reload is off.

---

### POST /balance/credits/reload
Trigger a BFun.bot Credits reload from the trading wallet.

**Requirements:**
- User must have enabled Agent Reload at [bfun.bot/credits](https://bfun.bot/credits)
- The API key must have `reload_enabled = true`
- The API key must have `llm_enabled = true`
- Trading wallet must have sufficient USDT on BSC
- Daily reload limit must not be exceeded

This is **manually triggered by the agent** — there is no automatic background polling. Call this endpoint when the agent determines a credit reload is needed.

Response:
```json
{
  "success": true,
  "amount_usd": "5.00",
  "tx_hash": "0x...",
  "new_balance_usd": "9.92",
  "daily_used_usd": "5.00",
  "daily_remaining_usd": "95.00"
}
```

Errors:
- `403` — reload not enabled for user or key
- `429` — daily limit would be exceeded
- `400` — insufficient USDT balance on BSC trading wallet
- `500` — transaction failed

---

### POST /balance/credits/reload/disable
Emergency kill switch — agent disables its own reload permission. **Cannot be re-enabled by the agent** (human must re-enable via dashboard).

Response: `204 No Content`

---

### GET /balance/wallet
Get on-chain wallet balances (BSC only — main + trading wallets).

Response:
```json
{
  "evm_main": {
    "address": "0x...",
    "balance_bnb": "0.100000",
    "balance_usdt_bsc": "5.000000"
  },
  "evm_trading": {
    "address": "0x...",
    "balance_bnb": "0.005000",
    "balance_usdt_bsc": "0.000000"
  }
}
```

Any field may be `null` if the wallet is not set up or the RPC is unavailable. Check `*_error` fields for failure reasons.

---

### GET /fees/summary
Get total fee earnings on BSC. All data is pre-computed — fast, no on-chain calls.

Response:
```json
{
  "bsc": {
    "chain_id": 56,
    "token_count": 12,
    "total_earned_bnb": 0.053
  }
}
```

---

### GET /fees/earnings
Get per-platform fee breakdown for BSC.

Query: `?chain=bsc`

Response:
```json
{
  "chain": "bsc",
  "chain_id": 56,
  "flap":     { "total_earned_bnb": 0.042, "earning_token_count": 3 },
  "fourmeme": { "total_earned_bnb": 0.011, "earning_token_count": 1 }
}
```

---

### GET /fees/token
Get fee earnings for a specific token on BSC.

Query: `?chain=bsc&platform=flap&token_address=0x...`

- `chain`: `bsc` only
- `platform`: `flap` | `fourmeme`
- `token_address`: contract address

Response:
```json
{
  "token_address": "0x...",
  "token_name": "MyToken",
  "token_symbol": "MTK",
  "platform": "flap",
  "chain": "bsc",
  "earned_bnb": 0.021
}
```

Returns `404` if token not found or not owned by the authenticated user.

---

### GET /quota
Get daily token creation quota and trading wallet readiness for BSC.

Response:
```json
{
  "chains": [
    {
      "chain": "bsc",
      "free_used_today": 1,
      "free_limit": 3,
      "sponsored_remaining": 2,
      "can_create_paid": true,
      "trading_wallet_balance": "0.010000 BNB",
      "trading_wallet_address": "0x..."
    }
  ]
}
```

---

## BFun LLM Gateway Reference

**Base URL:** `https://llm.bfun.bot`  
**Auth:** `X-Api-Key: bfbot_...` or `Authorization: Bearer bfbot_...`

### POST /v1/messages (Anthropic format)
Compatible with Claude models via Anthropic Messages API format.

```bash
curl https://llm.bfun.bot/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_BFBOT_API_KEY" \
  -d '{
    "model": "bfunbot-haiku-4-5",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

### POST /v1/chat/completions (OpenAI format)
Compatible with all models via OpenAI Chat Completions format.

```bash
curl https://llm.bfun.bot/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_BFBOT_API_KEY" \
  -d '{
    "model": "bfunbot-gpt-5-4",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

### GET /v1/models
List available models.

### GET /v1/models/openclaw
Returns a ready-to-paste OpenClaw provider config block. No auth required.

---

## Error Codes

| Code | Meaning |
|------|---------|
| 401 | Missing or invalid API key |
| 402 | Insufficient BFun.bot Credits (LLM) or trading wallet balance (token creation) |
| 403 | Permission denied — feature not enabled for this key or user |
| 404 | Resource not found |
| 422 | Validation error — check request body |
| 429 | Rate limited or daily cap exceeded — wait before retrying |
| 500 | Server error — retry |

---

## Troubleshooting

**402 on LLM calls**  
BFun.bot Credits exhausted. Top up at [bfun.bot/credits](https://bfun.bot/credits).  
Note: BFun.bot Credits ≠ trading wallet. Topping up one doesn't affect the other.

**403 on reload**  
Either Agent Reload is not enabled for the user ([bfun.bot/credits](https://bfun.bot/credits) → Agent Reload section), or the API key doesn't have `reload_enabled`. Check both.

**401 Unauthorized**  
API key missing or invalid. Manage keys at [bfun.bot/settings/api-keys](https://bfun.bot/settings/api-keys).  
Ensure you send: `X-Api-Key: bfbot_...`

**Token creation stuck at pending**  
Poll `GET /agent/v1/jobs/{job_id}` — creation usually takes 30–60 seconds.  
If still pending after 5 minutes, check the `error` field.

**429 on reload**  
Daily reload limit exceeded. Check `daily_remaining_usd` in the balance response.

**400 on reload — insufficient balance**  
BSC trading wallet doesn't have enough USDT. Check `GET /balance/wallet` and top up.

---

## Full Documentation
- Agent API: [bfun.bot/agent](https://bfun.bot/agent)
- API Keys: [bfun.bot/settings/api-keys](https://bfun.bot/settings/api-keys)
- BFun LLM Gateway: [bfun.bot/llm](https://bfun.bot/llm)
- OpenClaw setup: [bfun.bot/llm/openclaw](https://bfun.bot/llm/openclaw)
- BFun.bot Credits: [bfun.bot/credits](https://bfun.bot/credits)
