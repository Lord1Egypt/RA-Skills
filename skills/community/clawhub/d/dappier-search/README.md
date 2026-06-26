# Dappier Skill (dappier-search)

Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more.

This repo contains small Node.js CLI scripts that call the Dappier API.

## Requirements

- Node.js (must provide a global `fetch`, i.e. Node 18+ recommended)
- A Dappier API key in the `DAPPIER_API_KEY` environment variable

## Get your Dappier API key

1. Sign in at https://platform.dappier.com
2. Go to https://platform.dappier.com/profile/api-keys
3. Create/copy an API key
4. Export it in your shell:

```bash
export DAPPIER_API_KEY="YOUR_KEY_HERE"
```

## Usage

All tools are run via `node` and a script in [`scripts/`](scripts/).

### Real-time search

```bash
node scripts/realtime-search.mjs "latest news today"
```

### Stock market data (query must include a ticker)

```bash
node scripts/stock-market.mjs "AAPL stock price today"
```

### Sports news

```bash
node scripts/sports-news.mjs "NBA trade rumors" --algorithm trending --top_k 5
```

### Benzinga financial news

```bash
node scripts/benzinga-news.mjs "NVDA news" --algorithm most_recent
```

### Lifestyle news

```bash
node scripts/lifestyle-news.mjs "wellness trends 2026" --top_k 5
```

### Research papers search

```bash
node scripts/research-papers.mjs "recent arXiv papers on diffusion models"
```

### Stellar AI (solar & roof analysis)

```bash
node scripts/stellar-ai.mjs "1600 Amphitheatre Parkway, Mountain View, CA"
```

## Output format

Scripts print markdown-friendly sections (for example: `## Real Time Search Results`) and then the returned content.

## Documentation

- Full skill tool docs and examples: [`SKILL.md`](SKILL.md)
- Project changelog: [`CHANGELOG.md`](CHANGELOG.md)
- License: [`LICENSE`](LICENSE)
