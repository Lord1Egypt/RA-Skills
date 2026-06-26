---
name: "a-share-multidim-quant-analysis"
description: "A-Share Multi-Dimensional Quantitative Analysis MCP Server - broker research reports, AI news analysis, and stock comprehensive analysis"
version: "1.3.0"
category: "finance"
tags: ["finance", "stock", "quantitative-analysis", "research-report", "news-analysis", "mcp", "A-share", "China"]
complexity: "beginner"
author: "Li-Evan"
---

# A-Share Multi-Dimensional Quantitative Analysis

Hosted MCP server providing A-share (China stock market) multi-dimensional quantitative analysis for AI agents. Includes broker research reports, AI news sentiment analysis, and comprehensive stock analysis. Connect directly — no deployment needed.

## Tools

### `search_research_reports`
Search broker research reports by company name. Returns full-text reports including title, source, content, and date.
- **Input**: `company_name` (e.g. "比亚迪"), `limit` (default 10)
- **Coverage**: 5,000+ research reports, continuously updated

### `search_news_analysis`
Search AI-analyzed news by company name and date range. Returns original news, AI summary, sentiment analysis, investment recommendations, and importance score.
- **Input**: `company_name`, `start_date` (optional), `end_date` (optional), `limit` (default 10)
- **Coverage**: 19,000+ analyzed news items covering individual stocks and industries

### `get_stock_analysis`
Get the latest comprehensive analysis for a stock by its code. Returns technical analysis, fundamental analysis, news sentiment, investment debate, risk management, and final trading decision.
- **Input**: `stock_code` (e.g. "601900", "000001", "300750")
- **Coverage**: 3,000+ stocks, 12,000+ analysis reports

## Setup

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "yanpan": {
      "type": "http",
      "url": "http://42.121.167.42:9800/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

That's it. No installation, no Docker, no database — just connect and use.

## Get API Key

To get your own API key, contact via WeChat: **ptcg12345**
