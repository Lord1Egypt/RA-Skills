---
name: fiu-market-assistant
description: "FIU MCP Market Data and Trading Assistant. Use when user wants to query stock quotes, K-line, trade stocks, check positions, or analyze market data for HK/US/CN markets."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  openclaw:
    requires:
      env:
        - FIU_MCP_TOKEN
      binaries:
        - curl
        - jq
        - date
        - bash
      primaryCredential: FIU_MCP_TOKEN
---

# /fiu-market-assistant — FIU Market Data & Trading

Provides stock market data query and trading capabilities via FIU MCP Server. Supports HK, US, and CN stock markets with quotes, K-line, order book, capital flow, and trading operations.

Arguments passed: `$ARGUMENTS`

---

## Quick Start (One Command Setup)

```bash
# First time setup - configure MCP and set token
/fiu-market-assistant setup YOUR_FIU_MCP_TOKEN
```

After setup, simply use natural language:
```
Query Tencent Holdings quote
Show AAPL daily K-line
Buy 100 shares Tencent
```

---

## Dispatch on Arguments

### No args — show status

1. **Check FIU_MCP_TOKEN** - show if token is configured (masked)
2. **Show available markets** - list HK, US, CN, toolkit
3. **Show quick commands** - list available dispatch commands
4. **What next** - guide user:
   - No token → "Run `/fiu-market-assistant setup <token>` to configure"
   - Configured → "Ready! Ask me anything like 'Query 00700 quote'"

### `setup <token>` — quick setup (recommended)

1. Save token to config file `~/.fiu-market/config`
2. Create MCP config `.mcp.json` with all 7 FIU services
3. Test connectivity
4. Confirm and guide restart

### `test` — test connectivity

1. Check FIU_MCP_TOKEN is set
2. Test each market endpoint with tools/list
3. Show which services are working
4. Report any errors

### `discover <market>` — discover available tools

List all available tools for a specific market:

```
/fiu-market-assistant discover hk_sdk
/fiu-market-assistant discover cn_sdk
```

### `quote <symbol>` — query quote

Query real-time quote for a stock:

```
/fiu-market-assistant quote 00700
/fiu-market-assistant quote AAPL
/fiu-market-assistant quote 600519
```

### `kline <symbol> [type]` — query K-line

Query K-line data:

```
/fiu-market-assistant kline 00700        # daily
/fiu-market-assistant kline 00700 1      # weekly
/fiu-market-assistant kline AAPL 5       # 1-min for US
```

### `search <keyword>` — search stock code

Search for stock by name:

```
/fiu-market-assistant search 腾讯
/fiu-market-assistant search Apple
```

### `trade <action> <symbol> <qty> [price]` — trade

Place orders (default SIMULATE mode):

```
/fiu-market-assistant trade buy 00700 100 380
/fiu-market-assistant trade sell AAPL 50 150
/fiu-market-assistant trade buy 600519 1000 200
```

### `positions` — query positions

```
/fiu-market-assistant positions
```

### `cash` — query cash

```
/fiu-market-assistant cash
```

### `orders` — query orders

```
/fiu-market-assistant orders
```

### `capflow <symbol>` — capital flow

```
/fiu-market-assistant capflow 00700
```

---

## MCP Servers Reference

### Market Endpoints

| Service | Market | URL |
|---------|--------|-----|
| stockHkF10 | HK F10 | https://ai.szfiu.com/stock_hk_f10/ |
| stockUsF10 | US F10 | https://ai.szfiu.com/stock_us_f10/ |
| stockCnF10 | CN F10 | https://ai.szfiu.com/stock_cn_f10/ |
| stockHkSdk | HK SDK | https://ai.szfiu.com/stock_hk_sdk/ |
| stockUsSdk | US SDK | https://ai.szfiu.com/stock_us_sdk/ |
| stockCnSdk | CN SDK | https://ai.szfiu.com/stock_cn_sdk/ |
| szfiuToolkit | Search | https://ai.szfiu.com/toolkit/ |

### Feature Support by Market

| Feature | HK (港股) | US (美股) | CN (A股) |
|---------|-----------|-----------|----------|
| Quote | ✅ | ✅ | ✅ |
| K-line | ✅ | ✅ | ✅ |
| Order Book | ✅ | ✅ | ✅ |
| Tick Data | ✅ | ✅ | ✅ |
| Intraday | ✅ | ✅ | ✅ |
| Capital Flow | ✅ | ✅ | ✅ |
| Capital Distribution | ✅ | ✅ | ✅ |
| Sector List | ✅ | ✅ | ✅ |
| Stock Filter | ✅ | ✅ | ✅ |
| Market Ranking | ✅ | ✅ | ✅ |
| F10 Data | ✅ | ✅ | ✅ |
| Trading | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ |

---

## Usage Tips

1. **Use search first** to find correct stock code
2. **Default mode is SIMULATE** - use "REAL" for real trading
3. **HK stocks**: use format `00700.HK` or just `00700`
4. **US stocks**: use format `AAPL` or `AAPL.US`
5. **CN stocks**: use format `600519.SZ` or `000001.SZ`
6. **Rate limit**: 15 orders per 30 seconds
7. **Get token**: https://ai.szfiu.com/auth/login

## Important Notes

- Trading defaults to SIMULATE mode for safety
- Real trading requires explicit "REAL" confirmation
- Always check market status before trading
- The setup command will create/overwrite ~/.mcp.json (standard MCP config file)
- Backup is created automatically before overwriting
- Config files are stored with restricted permissions (600) - only owner can read
- This skill adds 7 FIU MCP entries to your MCP configuration
- Other MCP-enabled tools may also use ~/.mcp.json - review after setup if needed