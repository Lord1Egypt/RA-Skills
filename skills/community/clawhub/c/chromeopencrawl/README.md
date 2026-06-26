# OpenCrawl Skill for OpenClaw

Crawl any JavaScript-rendered webpage through **distributed real Chrome browsers**. No local browser installation needed — perfect for headless VPS environments.

Powered by [OpenCrawl](https://github.com/hlyylly/OpenCrawl).

## Why?

Your OpenClaw agent runs on a VPS without a real browser. Puppeteer/Playwright need 4GB+ RAM and complex setup. This skill gives your agent access to a **pool of real Chrome browsers** via a simple API call.

## Quick Start (use our public server)

The fastest way — use our hosted server, no deployment needed:

1. Visit **http://39.105.206.76:9877** and click **Register** (100 free credits)
2. Set environment variables:
   ```bash
   export OPENCRAWL_API_KEY=ak_your_key_from_step_1
   export OPENCRAWL_API_URL=http://39.105.206.76:9877
   ```
3. Install the skill:
   ```bash
   clawhub install hlyylly/chromeopencrawl
   ```
4. Done! Your agent can now crawl any JS-rendered page.

## Self-Hosted (deploy your own)

If you prefer full control, deploy your own OpenCrawl server:

1. Follow the guide at **https://github.com/hlyylly/OpenCrawl**
2. Set `OPENCRAWL_API_URL` to your server address
3. Create an API key via the admin panel

## Usage

Once installed, your OpenClaw agent can:

- **"Crawl https://example.com"** — Get rendered page content
- **"Crawl https://example.com and extract .article-content"** — Get specific elements
- **"Check my OpenCrawl balance"** — See remaining credits

## How It Works

```
Your Agent → OpenCrawl API → Real Chrome Worker → Render JS → Extract Content → R2 → Agent
```

- Workers are real Chrome browsers contributed by the community
- Each crawl costs 1 credit, Workers earn 1 credit per task
- Results stored on Cloudflare R2 (zero egress fees)
- Worker cookies isolated via incognito mode

## Links

- **Public Server:** http://39.105.206.76:9877
- **Source Code:** https://github.com/hlyylly/OpenCrawl
- **ClawHub:** https://clawhub.ai/hlyylly/chromeopencrawl

## License

MIT
