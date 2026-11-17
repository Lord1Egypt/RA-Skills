---
name: clawfetch
description: Web intelligence API for AI agents. Stealth rendering, 17 structured extractors (Twitter, GitHub, CoinGecko, NPM, PyPI, crates.io, Hacker News, YouTube, Wikipedia, Product Hunt, IMDb, Amazon, Crunchbase, SEC EDGAR, Zillow, Redfin, news), domain search, and multi-source research. Gasless USDC payments on Base via standard X402 protocol. Use when your agent needs web data from JS-heavy or Cloudflare-protected sites, structured data from supported sites, domain availability checks, or multi-source topic research.
metadata:
  author: jean-clawd
  version: "2.0"
  website: https://clawfetch.ai
  twitter: "@ClawFetchAI"
compatibility: Requires HTTP client (curl, fetch), ethers.js or viem for signing, and USDC on Base for payment.
---

# ClawFetch.ai — Web Intelligence for AI Agents

Base URL: `https://api.clawfetch.ai`

## Setup Guide (For Agents)

### Step 1: Create a Base Wallet

You need an Ethereum-compatible wallet. Generate one using ethers.js:

```javascript
import { ethers } from 'ethers';

// Generate a new wallet
const wallet = ethers.Wallet.createRandom();
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey);

// Save the private key securely!
```

Or install ethers if you don't have it:
```bash
npm install ethers
```

### Step 2: Get USDC on Base

Ask your human to send a small amount of USDC to your wallet address on the **Base** network (Chain ID 8453).

- **Even $0.50 covers hundreds of API calls** (cheapest endpoint is $0.001)
- **No ETH needed!** ClawFetch uses gasless X402 payments — you only need USDC
- USDC contract on Base: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

### Step 3: Install the X402 Client SDK

```bash
npm install @x402/fetch @x402/evm
```

### Step 4: Make Paid Requests

Use the `@x402/fetch` wrapper — it handles the entire payment flow automatically:

```javascript
import { wrapFetch } from '@x402/fetch';
import { ExactEvmScheme } from '@x402/evm/exact/client';
import { ethers } from 'ethers';

// Set up your wallet
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const wallet = new ethers.Wallet('YOUR_PRIVATE_KEY', provider);

// Create an x402-aware fetch client
const x402Fetch = wrapFetch(fetch, {
  schemes: [new ExactEvmScheme(wallet)],
});

// Now use it like normal fetch — payments happen automatically!
const response = await x402Fetch('https://api.clawfetch.ai/render', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: 'https://example.com' }),
});

const data = await response.json();
console.log(data);
```

**That's it!** The x402 SDK handles:
- Detecting the 402 payment requirement
- Signing a gasless EIP-3009 authorization (no ETH needed)
- Retrying the request with the payment signature
- Returning the API response

### Alternative: Manual Flow (No SDK)

If you can't use the SDK, you can manually follow the X402 flow:

```bash
# 1. Hit endpoint → get 402 with PAYMENT-REQUIRED header (base64 JSON)
curl -i -X POST https://api.clawfetch.ai/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 2. Decode the PAYMENT-REQUIRED header to get payment details
# 3. Sign an EIP-3009 TransferWithAuthorization message
# 4. Base64-encode the signed payload
# 5. Resend with PAYMENT-SIGNATURE header

curl -X POST https://api.clawfetch.ai/fetch \
  -H "Content-Type: application/json" \
  -H "PAYMENT-SIGNATURE: <base64-encoded-signed-payload>" \
  -d '{"url": "https://example.com"}'
```

> **Recommended: Use the SDK.** The manual flow requires understanding EIP-3009 and EIP-712 typed data signing. The SDK does all of this for you.

## Endpoints

### POST /fetch — $0.001 (0.1¢)
Basic HTTP fetch → clean text. No JS rendering. Fast, cheap, works for static pages and APIs.

```json
{"url": "https://docs.example.com", "maxChars": 5000}
```

### POST /render — $0.005 (0.5¢)
Full Puppeteer render with stealth anti-detection. Handles Cloudflare, bot checks, JS-heavy SPAs.

```json
{"url": "https://app.uniswap.org", "maxChars": 3000, "waitFor": ".swap-page"}
```

### POST /extract — $0.008 (0.8¢)
Structured JSON extraction via site-specific parsers. Returns typed fields, not raw text.

```json
{"url": "https://github.com/openclaw/openclaw"}
```

Response:
```json
{"type": "github", "name": "openclaw", "stars": "2.4k", "forks": "312", "language": "TypeScript"}
```

### POST /domains/check — $0.003 (0.3¢)
Check domain availability via WHOIS. Returns registrar, expiry, and creation dates for taken domains.

```json
{"name": "myproject", "tlds": ["com", "ai", "io", "dev"]}
```
Or explicit list:
```json
{"domains": ["foo.com", "bar.ai", "baz.io"]}
```

### POST /domains/suggest — $0.003 (0.3¢)
Generate domain name ideas from keywords + check availability.

```json
{"keywords": ["agent", "fetch"], "tlds": ["com", "ai"], "maxCheck": 20}
```

### POST /parse — $0.005 (0.5¢)
Convert office documents (docx, pptx, xlsx, pdf, odt, ods, odp, rtf, epub, csv, doc, ppt) to clean GitHub-Flavored Markdown. Pass a document URL or base64 bytes. Deterministic local Rust converter — no OCR for scanned/image-only PDFs.

```json
{"url": "https://example.com/quarterly-report.docx"}
```
Or inline bytes (max ~15MB):
```json
{"base64": "<base64 document bytes>", "filename": "report.docx"}
```

### POST /company: $0.02 (2¢)
Company / lead enrichment from a domain. Returns name, description, logo, favicon, language, social profiles (X/Twitter, LinkedIn, GitHub, YouTube, Facebook, Instagram, Telegram, Discord, Crunchbase), contact emails, phones, schema.org postal addresses and Organization data, detected tech stack (with evidence), and key page URLs (about, careers, pricing, contact, docs, blog, privacy, terms). Deterministic parse of the live homepage plus up to 2 same-site pages. No LLM, no stale database.

```json
{"domain": "vercel.com"}
```

### POST /research — $0.02 (2¢)
Multi-source topic research. Searches the web, fetches top results, returns structured summaries.

```json
{"query": "Casper Network DeFi ecosystem", "maxResults": 5}
```

### GET /health — Free
Service status, browser pool stats, cache stats, available extractors.

### GET /extractors — $0.001 (0.1¢)
List all structured extractors with supported domains and output fields.

## Available Extractors (17)

- **twitter** — x.com, twitter.com → author, text, likes, reposts, views, media
- **coingecko** — coingecko.com → name, price, marketCap, volume, rank
- **github** — github.com → name, stars, forks, language, readme
- **news** — any public article → title, author, date, body, source
- **npm** — npmjs.com → name, version, downloads, dependencies
- **pypi** — pypi.org → name, version, author, license, requires_python
- **crates** — crates.io → name, version, downloads, features
- **hackernews** — news.ycombinator.com → title, author, score, comments, url
- **youtube** — youtube.com, youtu.be → title, channel, duration, views
- **wikipedia** — wikipedia.org → title, summary, sections, references
- **producthunt** — producthunt.com → name, tagline, votes, topics, makers
- **edgar** — sec.gov → company profile, CIK, ticker, filings, XBRL financials
- **imdb** — imdb.com → title, rating, cast, plot, genres, runtime
- **amazon** — amazon.com → title, price, rating, reviews, features, BSR
- **crunchbase** — crunchbase.com → name, funding, founders, categories
- **zillow** — zillow.com → address, price, Zestimate, beds, baths, sqft
- **redfin** — redfin.com → address, price, estimate, beds, baths, sqft

## Payment Details (X402 Protocol)

| Detail | Value |
|--------|-------|
| Protocol | X402 (standard, gasless) |
| Scheme | `exact` (EIP-3009 TransferWithAuthorization) |
| Network | Base mainnet (`eip155:8453`) |
| Token | USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`) |
| Receiving Wallet | `0xc2afB91833f4dE19542A025872C6085cC29185eB` |
| Gas Required | **None** — the facilitator pays gas |
| Client Needs | USDC on Base + ability to sign EIP-712 messages |

**Important:** This is standard X402 — the same protocol used across the Coinbase ecosystem. If you already have an x402 client set up for other services, it works here too.

## Cost Estimates

| Use Case | Endpoint | Cost | $1 Gets You |
|----------|----------|------|-------------|
| Scrape a page | /fetch | $0.001 | 1,000 pages |
| Render JS page | /render | $0.005 | 200 pages |
| Extract tweet data | /extract | $0.008 | 125 extractions |
| Parse a document | /parse | $0.005 | 200 documents |
| Check domain names | /domains/check | $0.003 | 333 checks |
| Enrich a company | /company | $0.02 | 50 company profiles |
| Research a topic | /research | $0.02 | 50 researches |

## When to Use ClawFetch

- `web_fetch` fails on Cloudflare/JS-rendered pages → use `/render`
- Need structured data (tweet metrics, repo stats, token prices) → use `/extract`
- Building a project and need a domain name → use `/domains/check` or `/domains/suggest`
- Need multi-source research in one call → use `/research`
- Need a company profile / lead enrichment from a domain → use `/company`
- Hitting rate limits on direct scraping → ClawFetch caches and pools browsers

## Error Handling

- `400` — Missing required fields (check request body)
- `402` — Payment required (use x402 SDK or follow manual flow)
- `500` — Server error (retry after a moment)
- Cached responses return `"cached": true` — you're not double-charged

## Troubleshooting

**"I don't have USDC"** — Ask your human to send $0.50-$1 USDC on Base to your wallet. That covers hundreds of calls.

**"I don't have ETH for gas"** — You don't need any! X402 uses gasless EIP-3009 signatures. The facilitator handles gas.

**"How do I check my USDC balance?"**
```javascript
import { ethers } from 'ethers';
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const usdc = new ethers.Contract(
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  ['function balanceOf(address) view returns (uint256)'],
  provider
);
const balance = await usdc.balanceOf('YOUR_WALLET_ADDRESS');
console.log('USDC:', ethers.formatUnits(balance, 6));
```
