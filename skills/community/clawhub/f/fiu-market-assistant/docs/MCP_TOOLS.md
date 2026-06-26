# FIU MCP Tools Reference

## Known Tool Mappings

Tool names may differ between markets. Below are the confirmed tool names.

### F10 Markets (hk_f10, us_f10, cn_f10)

| Tool | HK | US | CN |
|------|----|----|----|
| company_info | `companyInfo` | `companyInfo` | `companyInfo` |
| financials | `financials` | `financials` | `financials` |
| dividend | `dividend` | `dividend` | `dividend` |
| split_history | `splitHistory` | `splitHistory` | `splitHistory` |
| holders | `holders` | `holders` | `holders` |
| news | `news` | `news` | `news` |
| industry | `industry` | `industry` | `industry` |
| prospectus | - | - | `prospectus` |
| public_listing | - | - | `publicListing` |

### SDK Markets (hk_sdk, us_sdk, cn_sdk)

| Tool | HK | US | CN |
|------|----|----|----|
| Quote | `post_v3_stock_quote` | `post_v1_stock_quote` | `post_v1_stock_quote` |
| K-Line | `post_v3_chart_kline_list` | *check API* | *check API* |
| Order Book | `post_v3_order_book` | *check API* | *check API* |
| Tick | `post_v3_tick_trade` | *check API* | *check API* |
| Intraday | `post_v3_intraday` | *check API* | *check API* |
| Capital | `post_v3_capital_flow` | *check API* | *check API* |
| Capital Dist | `post_v3_capital_distribution` | *check API* | *check API* |
| Sector List | `post_v3_sector_list` | *check API* | *check API* |
| Sector Stocks | `post_v3_sector_stocks` | *check API* | *check API* |
| Stock Sector | `post_v3_stock_sector` | *check API* | *check API* |
| Stock Filter | `post_v3_stock_filter` | *check API* | *check API* |
| Ranking | `post_v3_market_ranking` | *check API* | *check API* |
| Trade | `trade` | `trade` | `trade` |
| Cancel | `cancel_order` | `cancel_order` | `cancel_order` |
| Modify | `modify_order` | `modify_order` | `modify_order` |
| Query Cash | `query_cash` | `query_cash` | `query_cash` |
| Query Pos | `query_positions` | `query_positions` | `query_positions` |
| Query Orders | `query_orders` | `query_orders` | `query_orders` |
| Futures | `futures_trade` | `futures_trade` | `futures_trade` |

### Toolkit (toolkit)

| Tool | Description |
|------|-------------|
| `search` | Securities code search |
| `stock_info` | Stock basic info |

## Discover Available Tools

Use this command to list all available tools for a market:

```bash
curl -s -X POST https://ai.szfiu.com/stock_hk_sdk/ \
  -H "Authorization: Bearer $FIU_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | grep "^data:" | sed 's/^data: //' | jq
```

Replace the endpoint URL for other markets:
- `https://ai.szfiu.com/stock_us_sdk/`
- `https://ai.szfiu.com/stock_cn_sdk/`
- `https://ai.szfiu.com/stock_hk_f10/`
- `https://ai.szfiu.com/stock_us_f10/`
- `https://ai.szfiu.com/stock_cn_f10/`
- `https://ai.szfiu.com/toolkit/`

## Usage Examples

### Quote
```bash
mcp_router.sh hk_sdk post_v3_stock_quote fields=snapshot
mcp_router.sh us_sdk post_v1_stock_quote symbol=AAPL fields=snapshot sessionId=1
mcp_router.sh cn_sdk post_v1_stock_quote symbol=600519 fields=snapshot sessionId=1
```

### K-Line
```bash
mcp_router.sh hk_sdk post_v3_chart_kline_list symbol=00700.HK type=0 count=100
# For CN/US, discover the correct tool name first
```

### Trade
```bash
mcp_router.sh hk_sdk trade action=buy symbol=00700.HK qty=100 price=380
```

### Search
```bash
mcp_router.sh toolkit search keyword=腾讯
```
