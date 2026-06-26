# Agent Bazaar — Complete Endpoint Catalog

Base URL: `https://agent-bazaar.com`

All x402 endpoints accept POST with `Content-Type: application/json`.
Payment header: `X-402-Payment: <payment-proof>` or `X-402-Payment: demo` for testing.
Payment execution is delegated to your lobster.cash wallet — do not construct transactions manually.

---

## Discovery

### GET /api/capabilities
Browse and search all available skills.

**Query params:**
- `type` — Filter by type: `api`, `cli`, `skill`
- `category` — Filter by category: `development`, `content`, `data`, `crypto`, `ai`
- `q` — Search by keyword (searches name + description)
- `minRating` — Minimum rating (0-5)

**Response:** Array of capability objects with `slug`, `name`, `description`, `price`, `type`, `category`, `rating`, `usageCount`

---

## Content & Research

### POST /api/x402/content-writer — $0.03/call
Generate articles, copy, marketing content.

**Body:**
```json
{
  "topic": "Why AI agents need payment rails",
  "type": "blog_post",
  "tone": "professional",
  "length": "medium"
}
```
- `topic` (required): What to write about
- `type`: `blog_post`, `tweet`, `email`, `landing_page`, `ad_copy`
- `tone`: `professional`, `casual`, `technical`, `persuasive`
- `length`: `short`, `medium`, `long`

### POST /api/x402/research-summarizer — $0.04/call
Summarize research topics with key findings.

**Body:**
```json
{
  "topic": "x402 payment protocol adoption",
  "depth": "detailed"
}
```
- `topic` (required): Research subject
- `depth`: `brief`, `detailed`

### POST /api/x402/keyword-extractor — $0.01/call
Extract SEO keywords and topics from text.

**Body:**
```json
{
  "text": "Your content here...",
  "maxKeywords": 10
}
```

---

## Development

### POST /api/x402/code-review — $0.05/call
Security analysis, bug detection, style suggestions.

**Body:**
```json
{
  "code": "function add(a, b) { return a + b }",
  "language": "javascript",
  "focus": "security"
}
```
- `code` (required): Source code to review
- `language`: Programming language (auto-detected if omitted)
- `focus`: `security`, `performance`, `style`, `bugs`, `all`

### POST /api/x402/cicd-generator — $0.03/call
Generate CI/CD pipeline configurations.

**Body:**
```json
{
  "project": "Next.js app",
  "platform": "github-actions",
  "features": ["test", "lint", "deploy"]
}
```
- `project` (required): Project description
- `platform`: `github-actions`, `gitlab-ci`, `circleci`
- `features`: Array of pipeline features

### POST /api/x402/smart-contract-audit — $0.10/call
Audit Solidity smart contracts for vulnerabilities.

**Body:**
```json
{
  "code": "pragma solidity ^0.8.0; ...",
  "standard": "erc20"
}
```
- `code` (required): Solidity source code
- `standard`: `erc20`, `erc721`, `custom`

---

## Data & Analysis

### POST /api/x402/web-scraper — $0.02/call
Extract content from URLs.

**Body:**
```json
{
  "url": "https://example.com",
  "format": "markdown"
}
```
- `url` (required): URL to scrape
- `format`: `markdown`, `text`, `json`

### POST /api/x402/sentiment — $0.02/call
Analyze sentiment of text.

**Body:**
```json
{
  "text": "This product is amazing and I love it!"
}
```
- `text` (required): Text to analyze

**Response includes:** `sentiment` (positive/negative/neutral), `score` (-1 to 1), `confidence`

---

## Creative

### POST /api/x402/dalle-image — $0.08/call
Generate images via DALL-E.

**Body:**
```json
{
  "prompt": "A futuristic marketplace where robots browse shelves of glowing API endpoints",
  "size": "1024x1024",
  "style": "vivid"
}
```
- `prompt` (required): Image description
- `size`: `1024x1024`, `1792x1024`, `1024x1792`
- `style`: `vivid`, `natural`

---

## Crypto & DeFi

### POST /api/x402/defi-yield — $0.03/call
Analyze DeFi yield opportunities.

**Body:**
```json
{
  "protocol": "aave",
  "chain": "base",
  "amount": 1000
}
```
- `protocol`: `aave`, `compound`, `uniswap`, `all`
- `chain`: `base`, `ethereum`, `arbitrum`
- `amount`: USD amount to analyze

### POST /api/x402/bankr — $0.015/call
Crypto portfolio analysis and risk assessment.

**Body:**
```json
{
  "portfolio": ["ETH", "USDC", "SOL"],
  "action": "analyze"
}
```

---

## Simulation

### POST /api/x402/simulate — $0.005/call
World model simulation — predict outcomes of scenarios.

**Body:**
```json
{
  "scenario": "What happens if Bitcoin hits $200k?",
  "timeframe": "6months",
  "factors": ["market", "regulation", "adoption"]
}
```
- `scenario` (required): Scenario to simulate
- `timeframe`: Duration to model
- `factors`: Relevant factors to consider

---

## Agent Builder

### POST /api/x402/agent-builder — $0.25/call
Generate a complete, ready-to-run AI agent configuration.

**Body:**
```json
{
  "description": "A social media manager that posts daily content to X and Instagram, tracks engagement, and adjusts strategy weekly",
  "platform": "openclaw"
}
```
- `description` (required): What the agent should do
- `platform`: `openclaw`, `langchain`, `crewai`

**Response includes:** Full agent config with personality, tools, cron schedules, skill integrations, and setup instructions.

---

## Payment Verification

### POST /api/x402/verify
Verify a payment on-chain. Used internally by Agent Bazaar — agents typically do not need to call this directly. Payment verification is handled automatically when you include a valid `X-402-Payment` header.
