---
name: dappier
description: Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more. Build powerful AI agents with Dappier.
homepage: https://dappier.com
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["node"],"env":["DAPPIER_API_KEY"]},"primaryEnv":"DAPPIER_API_KEY"}}
---

# Dappier

Enable fast, free real-time web search and access premium data from trusted media brands—news, financial markets, sports, entertainment, weather, and more. Build powerful AI agents with Dappier.

## Tools

### 1. Real Time Search

Real-time web search to access the latest news, stocks, gold stocks, UK stock market, global market performance, financial news, weather, travel information, deals, and more.

```bash
node {baseDir}/scripts/realtime-search.mjs "query"
```

Examples:

```bash
node {baseDir}/scripts/realtime-search.mjs "latest news today"
node {baseDir}/scripts/realtime-search.mjs "weather in New York today"
node {baseDir}/scripts/realtime-search.mjs "best travel deals this week"
node {baseDir}/scripts/realtime-search.mjs "gold price today"
```

### 2. Stock Market Data

Only use this if user query requires real-time financial news, stock prices, and trades. The query **must include a stock ticker symbol** (e.g. AAPL, TSLA, MSFT, GOOGL) to retrieve real-time stock prices, financial news, or market data.

```bash
node {baseDir}/scripts/stock-market.mjs "query with ticker symbol"
```

Examples:

```bash
node {baseDir}/scripts/stock-market.mjs "AAPL stock price today"
node {baseDir}/scripts/stock-market.mjs "TSLA latest financial news"
node {baseDir}/scripts/stock-market.mjs "MSFT earnings report"
node {baseDir}/scripts/stock-market.mjs "GOOGL revenue growth"
node {baseDir}/scripts/stock-market.mjs "AMZN market cap"
```

### 3. Sports News

Fetch AI-powered Sports News recommendations. Get real-time news, updates, and personalized content from top sports sources like Sportsnaut, Forever Blueshirts, Minnesota Sports Fan, LAFB Network, Bounding Into Sports, and Ringside Intel.

```bash
node {baseDir}/scripts/sports-news.mjs "query"
node {baseDir}/scripts/sports-news.mjs "query" --top_k 5
node {baseDir}/scripts/sports-news.mjs "query" --algorithm trending
```

Options:

- `--top_k <count>`: Number of results (default: 9)
- `--algorithm <type>`: Search algorithm - `most_recent` (default), `semantic`, `most_recent_semantic`, or `trending`

Examples:

```bash
node {baseDir}/scripts/sports-news.mjs "NFL playoff results"
node {baseDir}/scripts/sports-news.mjs "NBA trade rumors" --algorithm trending
node {baseDir}/scripts/sports-news.mjs "MLB scores today" --top_k 5
node {baseDir}/scripts/sports-news.mjs "Premier League standings"
node {baseDir}/scripts/sports-news.mjs "UFC fight results this week" --algorithm most_recent
```

### 4. Benzinga Financial News

Access real-time financial news from Benzinga.com. Use this for latest financial or stock news.

```bash
node {baseDir}/scripts/benzinga-news.mjs "query"
node {baseDir}/scripts/benzinga-news.mjs "query" --top_k 5
node {baseDir}/scripts/benzinga-news.mjs "query" --algorithm trending
```

Options:

- `--top_k <count>`: Number of results (default: 9)
- `--algorithm <type>`: Search algorithm - `most_recent` (default), `semantic`, `most_recent_semantic`, or `trending`

Examples:

```bash
node {baseDir}/scripts/benzinga-news.mjs "latest market news"
node {baseDir}/scripts/benzinga-news.mjs "NVDA news" --algorithm most_recent
node {baseDir}/scripts/benzinga-news.mjs "AAPL earnings" --top_k 5
node {baseDir}/scripts/benzinga-news.mjs "inflation report markets" --algorithm trending
```

### 5. Lifestyle News

Fetch AI-powered Lifestyle News recommendations. Access current lifestyle updates, analysis, and insights from leading lifestyle publications like The Mix, Snipdaily, Nerdable, and Familyproof.

```bash
node {baseDir}/scripts/lifestyle-news.mjs "query"
node {baseDir}/scripts/lifestyle-news.mjs "query" --top_k 5
node {baseDir}/scripts/lifestyle-news.mjs "query" --algorithm trending
```

Options:

- `--top_k <count>`: Number of results (default: 9)
- `--algorithm <type>`: Search algorithm - `most_recent` (default), `semantic`, `most_recent_semantic`, or `trending`

Examples:

```bash
node {baseDir}/scripts/lifestyle-news.mjs "wellness trends 2026"
node {baseDir}/scripts/lifestyle-news.mjs "family routine hacks" --algorithm trending
node {baseDir}/scripts/lifestyle-news.mjs "home organization tips" --top_k 5
node {baseDir}/scripts/lifestyle-news.mjs "celebrity lifestyle news" --algorithm most_recent
```

### 6. Research Papers Search

Perform a real-time research paper search. Provides instant access to over 2.4 million open-access scholarly articles across domains including physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics.

```bash
node {baseDir}/scripts/research-papers.mjs "query"
```

Examples:

```bash
node {baseDir}/scripts/research-papers.mjs "transformer architecture original paper"
node {baseDir}/scripts/research-papers.mjs "recent arXiv papers on diffusion models"
node {baseDir}/scripts/research-papers.mjs "graph neural networks survey 2024"
```

### 7. Stellar AI (Solar & Roof Analysis)

Get advanced roof analysis and solar panel placement recommendations with just a residential home address. Powered by Digital Satellite Imagery (DSM) and solar irradiance insights for precise energy estimates.

```bash
node {baseDir}/scripts/stellar-ai.mjs "residential home address"
```

Examples:

```bash
node {baseDir}/scripts/stellar-ai.mjs "1600 Amphitheatre Parkway, Mountain View, CA"
node {baseDir}/scripts/stellar-ai.mjs "1 Hacker Way, Menlo Park, CA"
node {baseDir}/scripts/stellar-ai.mjs "221B Baker Street, London"
```

## Notes

- Needs `DAPPIER_API_KEY` from https://platform.dappier.com/profile/api-keys
- Dappier provides real-time data from trusted media brands
- Use **Real Time Search** for general queries (news, weather, travel, deals, etc.)
- Use **Stock Market Data** specifically for financial queries with ticker symbols
- Use **Sports News** for sports-related queries — returns articles with titles, authors, sources, and summaries
- Use **Benzinga Financial News** for finance/news queries — returns Benzinga articles with titles, sources, and summaries
- Use **Lifestyle News** for lifestyle topics — returns articles with titles, sources, and summaries
- Use **Research Papers Search** for scholarly / academic queries — returns an AI-generated response based on open-access papers
- Use **Stellar AI** for solar feasibility questions when you have a specific residential address
