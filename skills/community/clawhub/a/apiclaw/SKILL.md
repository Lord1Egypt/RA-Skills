---
name: apiclaw
description: "API discovery + Direct Call for AI agents. ⚠️ Without your own API keys, requests proxy through NordSym (full payloads). With your keys in ~/.secrets/, calls go direct to providers."
version: 1.2.3
author: nordsym
tags: [api, mcp, discovery, integration, direct-call]
configPaths: 
  - "~/.secrets/replicate.env"
  - "~/.secrets/openrouter.env"
  - "~/.secrets/firecrawl.env"
  - "~/.secrets/e2b.env"
  - "~/.secrets/github.env"
  - "~/.secrets/elevenlabs.env"
  - "~/.secrets/resend.env"
  - "~/.secrets/46elks.env"
  - "~/.secrets/twilio.env"
envVars:
  - REPLICATE_API_TOKEN
  - OPENROUTER_API_KEY
  - FIRECRAWL_API_KEY
  - E2B_API_KEY
  - GITHUB_TOKEN
  - ELEVENLABS_API_KEY
  - RESEND_API_KEY
  - ELKS_API_USER
  - ELKS_API_PASSWORD
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
network:
  - "api.replicate.com"
  - "openrouter.ai"
  - "api.firecrawl.dev"
  - "api.e2b.dev"
  - "api.github.com"
  - "api.elevenlabs.io"
  - "api.resend.com"
  - "api.46elks.com"
  - "api.twilio.com"
  - "adventurous-avocet-799.convex.site (proxy fallback)"
source: "https://github.com/nordsym/apiclaw"
npm: "@nordsym/apiclaw"
---

# APIClaw

The API layer for AI agents. Find, evaluate, and integrate APIs in milliseconds.

## ⚠️ Important: Proxy Behavior

**With your own credentials** (`~/.secrets/*.env`): Requests go **directly** to provider APIs. Your data never touches NordSym servers.

**Without credentials**: Requests proxy through NordSym, including **full payloads** (prompts, message content, etc.). Do not send sensitive data via proxy.

## Installation

```bash
npx @nordsym/apiclaw
```

Audit first: [GitHub](https://github.com/nordsym/apiclaw) | [npm](https://npmjs.com/package/@nordsym/apiclaw)

## What It Does

- **Search 16,000+ APIs** by capability — natural language queries
- **Compare** pricing, rate limits, features across providers
- **Direct Call** — execute API calls instantly

## Live Direct Call Providers

| Provider | What You Get |
|----------|--------------|
| **Replicate** | Run any ML model — Flux, Llama, Whisper, SDXL |
| **OpenRouter** | 100+ LLMs — GPT-4, Claude, Mixtral, Gemini |
| **E2B** | Secure code sandbox — run Python, JS, any language |
| **Firecrawl** | Web scraping — extract data from any URL |
| **GitHub** | Repos, issues, code search, file operations |
| **ElevenLabs** | Voice synthesis — text to speech |
| **Resend** | Transactional email API |
| **46elks** | Swedish SMS & voice |
| **Twilio** | Global SMS & voice |

## MCP Tools

| Tool | Description |
|------|-------------|
| `discover_apis` | Search by capability, get ranked matches |
| `get_api_details` | Full spec, auth, endpoints, examples |
| `direct_call` | Execute API calls through APIClaw |
| `list_categories` | Browse all 30+ categories |

## Example Usage

> "Run Flux on Replicate to generate a cyberpunk cityscape"

> "Use E2B to execute this Python script and return the output"

> "Scrape the pricing page from competitor.com using Firecrawl"

## Links

- Website: https://apiclaw.nordsym.com
- GitHub: https://github.com/nordsym/apiclaw
- npm: https://npmjs.com/package/@nordsym/apiclaw
