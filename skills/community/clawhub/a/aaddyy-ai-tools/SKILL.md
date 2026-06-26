---
name: aaddyy-ai-tools
description: "Access 100+ AI tools via MCP — image generation, article writing, logo creation, SEO analysis, math solving, video generation. One API key, pay-per-use pricing."
homepage: https://www.aaddyy.com
metadata: {"openclaw": {"requires": {"bins": ["npx"], "env": ["AADDYY_API_KEY"]}, "primaryEnv": "AADDYY_API_KEY"}}
---

# AADDYY AI Tools for OpenClaw

Give your OpenClaw agent access to 100+ specialized AI tools — image generation, article writing, logo creation, SEO analysis, math solving, video generation, and more. All tools are accessed via AADDYY's MCP server with a single API key. Tools are loaded dynamically — as new tools go live, your agent gets them automatically.

## Prerequisites

- **Node.js 18+** with `npx` available
- **AADDYY API key** — get one free at https://www.aaddyy.com/api-keys (50 free credits, no credit card needed)

## Setup

### Step 1: Get your API key

Sign up at https://www.aaddyy.com/signup and create an API key at https://www.aaddyy.com/api-keys. Your key starts with `aip_`.

### Step 2: Add the MCP server to OpenClaw

```bash
openclaw mcp set aaddyy '{"command":"npx","args":["@aaddyy/mcp-server"],"env":{"AADDYY_API_KEY":"aip_your_key_here"}}'
```

Replace `aip_your_key_here` with your actual API key.

### Step 3: Verify the connection

```bash
openclaw mcp list
```

You should see `aaddyy` listed with 100+ tools registered. Tools are loaded dynamically from the AADDYY API — new tools appear automatically without updating the skill.

## Usage Examples

Once connected, just ask your OpenClaw agent naturally:

**Content creation:**
- "Write a professional article about AI trends in 2026"
- "Generate 5 SEO-friendly title ideas for a blog about remote work"
- "Write a follow-up email to a client"
- "Create a LinkedIn post announcing our new product"

**Image & design:**
- "Create a modern logo for a startup called NovaTech"
- "Generate a professional headshot for a team page"
- "Generate an image of a sunset over mountains, photorealistic style"

**SEO & analysis:**
- "Analyze the SEO of https://example.com and show me the top issues"
- "Research keywords related to AI tools for developers"

**Education:**
- "Solve this math problem step by step: integrate x^2 from 0 to 5"
- "Solve this physics problem: a ball thrown upward at 20 m/s, find max height"

**Video:**
- "Generate a 30-second educational video about photosynthesis"

## All Available Tools

### Content & Writing
- **Article Generator** — generate SEO-optimized articles (~5 credits)
- **Essay Writer** — academic and professional essays (~5 credits)
- **Email Writer** — professional emails for any purpose (~3 credits)
- **Title Generator** — headline and title ideas (~1 credit)
- **Caption Generator** — social media captions (~1 credit)
- **Research Blog Writer** — articles with real-time SERP data (~10 credits)
- **Synonym Finder** — alternative words and phrases (~1 credit)
- **Job Email Creator** — job application emails (~3 credits)

### Image & Design
- **Image Generator** — images from text prompts (~4 credits)
- **Logo Creator** — brand logos in multiple styles (~4 credits)
- **Headshot Generator** — professional AI headshots (~8 credits)
- **Album Cover Generator** — music artwork (~5 credits)
- **T-Shirt Designer** — apparel designs (~5 credits)
- **Jewelry Designer** — custom jewelry concepts (~5 credits)
- **Product Photo Studio** — e-commerce product photos (~8 credits)
- **Image Upscaler** — enhance resolution up to 4x (~12 credits)
- **Watermark Remover** — clean watermarks from images (~20 credits)
- **Image Prompt Creator** — reverse-engineer prompts from images (~15 credits)

### Video
- **Video Generator** — text-to-video (~50 credits)
- **Audio to Video** — convert audio to video (~50 credits)
- **Educational Clip Generator** — animated explainer videos (~60 credits)

### Social Media
- **Instagram Post Generator** — posts with captions (~5 credits)
- **LinkedIn Post Generator** — professional posts (~5 credits)

### Education
- **Math Solver** — step-by-step solutions with formulas (~1 credit)
- **Physics Solver** — step-by-step physics solutions (~1 credit)

### SEO & Analysis
- **SEO Analyzer** — full website audit with scores (~10 credits)
- **Keyword Researcher** — keyword and market analysis (~5 credits)

### Free Tools (no credits needed)
- **PDF Merge** — combine multiple PDFs
- **Image Compressor** — reduce image file sizes
- **Image to PDF** — convert images to PDF

## Pricing

Pay-per-use. **1 credit = $0.01 USD.** No monthly subscriptions.

- New accounts get **50 free credits** ($0.50) — no credit card required
- Credit packs: $5 (500), $10 (1,000), $20 (2,000), $50 (5,000)
- Each tool shows its credit cost before execution
- When credits run out, calls stop — no surprise bills

## Error Handling

| Error | Meaning | What to do |
|-------|---------|------------|
| `INSUFFICIENT_CREDITS` | Not enough credits | Top up at https://www.aaddyy.com/dashboard |
| `RATE_LIMITED` | Too many requests | Wait and retry. Default: 60 req/min |
| `UNAUTHORIZED` | Invalid API key | Check your `AADDYY_API_KEY` is correct |

## Troubleshooting

**"No tools registered"** — Make sure your API key is valid and the AADDYY backend is reachable. Test with:
```bash
curl https://backend.aaddyy.com/api/documentation/tools
```

**"Command not found: npx"** — Install Node.js 18+ from https://nodejs.org

**Tools not loading** — The MCP server fetches tools from the API on startup. If the backend is temporarily down, it retries 3 times automatically.

## Technical Details

- **Transport:** stdio (local process via npx)
- **Protocol:** MCP (Model Context Protocol)
- **NPM package:** [@aaddyy/mcp-server](https://www.npmjs.com/package/@aaddyy/mcp-server)
- **SDK (for code):** [aaddyy](https://www.npmjs.com/package/aaddyy) — `npm install aaddyy`
- **API docs:** https://www.aaddyy.com/docs
- **OpenAPI spec:** https://backend.aaddyy.com/openapi.json
- **Source code:** https://github.com/nandanv99/aaddyy-mcp

## Support

- Documentation: https://www.aaddyy.com/docs
- Skill file: https://www.aaddyy.com/skill.md
- Email: hello@aaddyy.com
- Website: https://www.aaddyy.com
