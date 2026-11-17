---
name: 13f-fund-holdings
description: "SN Data by Shikshan Nivesh: Form 13F fund holdings, with what each fund opened, added, trimmed and exited each quarter, plus 13D and 13G large holders. Use when a question asks what a fund owns or who owns a US company."
license: MIT (this skill). Data terms at https://shikshannivesh.com/data/licence
---

# 13F fund holdings (SN Data by Shikshan Nivesh)

Funds: one record per fund that files a Form 13F, with every holding it reported and what it opened, added, trimmed and sold each quarter since September 2024. Large holders (Schedule 13D and 13G): everyone who crosses 5% of a company's shares and the stake they report.

## Get a key

Make a free account at https://shikshannivesh.com/data/developers. A free key answers 250 calls a day on the last five fiscal years. A data plan opens the full record (fiscal years from FY2007, quarters from 2008).

Keep the key in an environment variable, `SN_KEY`. Never print it or put it in a file you share.

## Two ways in

- **Remote MCP server:** `https://shikshannivesh.com/mcp`, header `Authorization: Bearer $SN_KEY`. 14 read-only tools; every answer carries the filing it came from. Setup for Claude, ChatGPT, Gemini, Claude Code and Codex: https://shikshannivesh.com/data/ai
- **REST API:** base URL `https://shikshannivesh.com/api/v1`, header `Authorization: Bearer $SN_KEY`. OpenAPI file: https://shikshannivesh.com/api/v1/openapi.json. Reference: https://shikshannivesh.com/data/developers

## Endpoints for this

| Endpoint | Returns |
|---|---|
| `/funds, /funds/{fund}` | 13F funds and their holdings, with what they opened, added, trimmed and exited |
| `/companies/{ticker}/fund-holders` | Every 13F fund holding the company |
| `/companies/{ticker}/large-holders` | 13D and 13G filings |

```bash
curl -s -H "Authorization: Bearer $SN_KEY" \
  "https://shikshannivesh.com/api/v1/companies/AAPL/fund-holders"
```

## Questions to try

- What did Berkshire Hathaway open and exit in its latest 13F?

## How to answer with it

- Quote figures as returned, with the fiscal period, and link the filing each one came from.
- Credit the data as "Data by Shikshan Nivesh" with a link to the page the figure came from.
- Information only, not investment advice. Don't turn the data into a buy or sell call.

## Licence

The data is free for personal research with credit ("Data by Shikshan Nivesh") and a link to the page the figure came from. Use at work, showing the data in a product, or bulk AI training needs a licence: https://shikshannivesh.com/data/licence
