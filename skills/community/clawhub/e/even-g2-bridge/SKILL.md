---
name: even-g2-bridge
description: "Connect Even Realities G2 smart glasses to OpenClaw via Cloudflare Worker. Deploys a bridge that routes G2 voice commands to your OpenClaw Gateway — same agent, same memory, same tools, just voice instead of typing. Supports short conversations (direct reply on glasses), long tasks (background processing with Telegram delivery), and image generation (DALL-E → Telegram). Use when: setting up G2 glasses with OpenClaw, deploying the G2 bridge worker, or troubleshooting G2 ↔ OpenClaw connectivity."
license: MIT
compatibility: "Requires: Cloudflare account (free plan works), OpenClaw Gateway with HTTP API enabled. Optional: OpenAI API key (image gen), Telegram bot (rich content delivery)."
metadata:
  author: dAAAb
  version: "5.0.0"
  repository: https://github.com/dAAAb/openclaw-even-g2-bridge-skill
  icon: assets/icon.png
  required_secrets:
    - name: GATEWAY_URL
      description: "Your OpenClaw Gateway URL (e.g. https://your-gateway.example.com)"
      required: true
    - name: GATEWAY_TOKEN
      description: "OpenClaw Gateway auth token — stored in CF Worker secrets, never exposed to glasses"
      required: true
    - name: G2_TOKEN
      description: "Token for G2 glasses authentication — you choose this value"
      required: true
    - name: ANTHROPIC_API_KEY
      description: "Anthropic API key for fallback when Gateway is unreachable"
      required: true
    - name: TELEGRAM_BOT_TOKEN
      description: "Telegram bot token for delivering rich content (images, code, long text)"
      required: false
    - name: TELEGRAM_CHAT_ID
      description: "Telegram chat ID for content delivery"
      required: false
    - name: OPENAI_API_KEY
      description: "OpenAI API key for DALL-E image generation"
      required: false
  security_notes: |
    Two-layer token auth: G2 glasses only know G2_TOKEN. GATEWAY_TOKEN stays in
    Worker secrets, never exposed to glasses. If glasses are lost, change only G2_TOKEN.
    Consider using a scoped, least-privilege Gateway token for the Worker.
---

# Even Realities G2 × OpenClaw Bridge

Deploy a Cloudflare Worker that connects Even Realities G2 smart glasses to your OpenClaw Gateway.

## What It Does

```
G2 Glasses → (voice→text) → CF Worker → OpenClaw Gateway → Full Agent
                                ↓                              ↓
                          G2 display (text)            Telegram (rich content)
```

- **Short tasks** (chat, questions): Gateway responds → displayed on G2
- **Long tasks** (write code, articles): G2 shows "Working on it..." → result sent to Telegram
- **Image generation**: DALL-E generates → sent to Telegram (G2 can't show images)
- **Fallback**: If Gateway is down, falls back to direct Claude API

## Prerequisites

1. Even Realities G2 glasses with Even app (v0.0.7+ with "Add Agent" support)
2. OpenClaw Gateway with HTTP API enabled
3. Cloudflare account (free plan works)
4. Anthropic API key (fallback)
5. Optional: OpenAI API key (image gen), Telegram bot token (rich content delivery)

## Setup

### 1. Enable OpenClaw Gateway HTTP API

On your OpenClaw host, enable the chat completions endpoint:

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

Verify:
```bash
curl -X POST https://YOUR_GATEWAY_URL/v1/chat/completions \
  -H "Authorization: Bearer YOUR_GATEWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"hi"}]}'
```

### 2. Deploy Cloudflare Worker

Copy `scripts/worker.js` to your project, then deploy:

```bash
# Install wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler deploy
```

Or use the Cloudflare Dashboard: Workers & Pages → Create → Upload `worker.js`.

### 3. Set Secrets

```bash
# Required
wrangler secret put GATEWAY_URL      # Your OpenClaw Gateway URL
wrangler secret put GATEWAY_TOKEN    # Your Gateway auth token
wrangler secret put G2_TOKEN         # Token for G2 glasses auth (you choose)
wrangler secret put ANTHROPIC_API_KEY # Fallback when Gateway is down

# Optional (for Telegram delivery of rich content)
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_CHAT_ID

# Optional (for image generation)
wrangler secret put OPENAI_API_KEY
```

### 4. Configure G2 Glasses

In Even app → Settings → Add Agent:
- **Name**: Your agent name (e.g., "Cloud Lobster")
- **URL**: `https://YOUR_WORKER.workers.dev`
- **Token**: The `G2_TOKEN` you set above

### 5. Test

```bash
curl -X POST https://YOUR_WORKER.workers.dev \
  -H "Authorization: Bearer YOUR_G2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw","messages":[{"role":"user","content":"Hello, who are you?"}]}'
```

## Architecture

### Request Flow

1. G2 converts speech → text, sends as OpenAI chat completion format
2. Worker authenticates via `G2_TOKEN`
3. Worker classifies request:
   - **Image gen** → DALL-E + Telegram (immediate G2 ack)
   - **Long task** → immediate G2 ack + background Gateway call → Telegram
   - **Short task** → proxy to Gateway → return to G2
4. Gateway runs full agent loop (memory, tools, skills)
5. Response filtered for G2 display (no URLs, code blocks → Telegram)

### Security

Two-layer token auth:
```
G2 --[G2_TOKEN]--> Worker --[GATEWAY_TOKEN]--> Gateway
```

- G2 only knows `G2_TOKEN` — if glasses are lost, change only this token
- `GATEWAY_TOKEN` stays in Worker secrets, never exposed to glasses
- Gateway HTTP API should be behind auth (token or password mode)

### G2 Display Limitations

- 576×136 pixels, monochrome green, ~48 chars wide
- Text only (no images, no markdown rendering)
- Worker auto-filters: URLs → `[link]`, code blocks → `[code]`, long text → truncated
- Non-displayable content forwarded to Telegram

## Customization

Edit the task classification regex in `worker.js`:
- `isLongTask()` — patterns that trigger background processing
- `isImageGenRequest()` — patterns that trigger DALL-E

## Troubleshooting

- **G2 says "Unauthorized"**: Check G2_TOKEN matches in Worker secrets and Even app
- **"Gateway not configured"**: Verify GATEWAY_URL and GATEWAY_TOKEN secrets are set
- **Timeout on short tasks**: Gateway may be slow; increase `SHORT_TIMEOUT` (max ~25s for CF Workers)
- **No Telegram delivery**: Check TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID secrets
- **Gateway returns 404**: Ensure `chatCompletions.enabled: true` in OpenClaw config + restart
