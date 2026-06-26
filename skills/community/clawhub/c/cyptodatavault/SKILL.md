# DataVault Skill

> 📊 **DataVault** - 全球领先的 Web3 Data Value 平台
> 
> Empowering AI Agents with Institutional-Grade Crypto Market Data

## Overview

DataVault is a comprehensive cryptocurrency market data infrastructure that provides unified access to multi-source market data through a standardized API layer. This skill exposes **13 core tools** for AI agents to access real-time crypto prices, on-chain data, and DeFi metrics.

With 101+ MCP Tools under the hood, DataVault connects to:
- **5+ Exchanges**: Binance, OKX, Bybit, Bitget, Gate.io
- **On-Chain Networks**: Ethereum, BSC, Solana, Polygon, Arbitrum
- **DeFi Protocols**: DeFi Llama, CoinCap

## Features

| Category | Tools | Description |
|----------|-------|-------------|
| **Market Data** | 5 | Real-time prices, funding rates, market summary |
| **On-Chain** | 3 | ETH balance, transactions, gas prices |
| **DeFi** | 5 | TVL, yields, stablecoins |
| **Core** | 101+ | MCP Tools total |

## Quick Start

```python
from skill import call_tool

# Get Bitcoin price
result = call_tool("get_price", symbol="BTC/USDT")
print(result)
# {"symbol": "BTC/USDT", "last": 74536.1, "bid": 74530.0, "ask": 74540.0, ...}
```

## Tools Reference

### Market Data Tools

#### `get_price`
Get real-time price for a cryptocurrency symbol.

```python
call_tool("get_price", symbol="BTC/USDT")
call_tool("get_price", symbol="ETH/USDT")
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `symbol` | string | Yes | Trading symbol (e.g., "BTC/USDT") |
| `exchange` | string | No | Specific exchange |

#### `get_all_prices`
Get all available market prices.

```python
call_tool("get_all_prices")
```

#### `get_funding_rate`
Get funding rate for a symbol.

```python
call_tool("get_funding_rate", symbol="BTC/USDT")
```

#### `get_market_summary`
Get market overview with top gainers/losers.

```python
call_tool("get_market_summary")
```

#### `get_best_price`
Find best price across all exchanges.

```python
call_tool("get_best_price", symbol="BTC/USDT")
```

---

### On-Chain Tools

#### `get_eth_balance`
Get ETH balance for an address.

```python
call_tool("get_eth_balance", address="0xd8dA6BF26964aF9D7eEd002fE87A6555f0aBc6f8")
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | string | Yes | Ethereum wallet address |

#### `get_eth_transactions`
Get transaction history for an address.

```python
call_tool("get_eth_transactions", address="0xd8dA6BF26964aF9D7eEd002fE87A6555f0aBc6f8", limit=20)
```

#### `get_gas_price`
Get current Ethereum gas prices.

```python
call_tool("get_gas_price")
```

---

### DeFi Tools

#### `get_defi_tvl`
Get DeFi total value locked rankings.

```python
call_tool("get_defi_tvl")
call_tool("get_defi_tvl", chain="ethereum")
```

#### `get_protocol_tvl`
Get TVL for a specific protocol.

```python
call_tool("get_protocol_tvl", protocol="aave")
call_tool("get_protocol_tvl", protocol="makerdao")
```

#### `get_chain_tvl`
Get TVL rankings by blockchain.

```python
call_tool("get_chain_tvl")
```

#### `get_yields`
Get yield farming data.

```python
call_tool("get_yields")
call_tool("get_yields", protocol="aave")
```

#### `get_stablecoins`
Get stablecoin market data.

```python
call_tool("get_stablecoins")
```

---

## Usage Examples

### Example 1: Get Bitcoin Price

```
Input: What's the current BTC price?

AI Response:
call_tool("get_price", symbol="BTC/USDT")
→ Returns: {"symbol": "BTC/USDT", "last": 74536.1, ...}
→ "BTC is currently trading at $74,536.10"
```

### Example 2: Check Vitalik's ETH Balance

```
Input: How much ETH does Vitalik have?

AI Response:
call_tool("get_eth_balance", address="0xd8dA6BF26964aF9D7eEd002fE87A6555f0aBc6f8")
→ Returns: {"eth_value": 2445.32, "usd_value": 18170000}
→ "Vitalik has approximately 2,445 ETH (~$18M)"
```

### Example 3: Check Gas prices

```
Input: Should I send ETH now or wait for cheaper gas?

AI Response:
call_tool("get_gas_price")
→ Returns: {"fast": 30, "standard": 25, "slow": 20}
→ "Current gas: Fast 30 gwei, Standard 25 gwei. 
   Consider waiting if not urgent."
```

---

## Configuration

### Environment Variables

Optional - works out of the box without config:

```bash
# .env (optional)
ETHERSCAN_API_KEY=your_key
```

### Required Python Packages

```
requests>=2.31.0
ccxt>=4.3.0
fastapi>=0.109.0
uvicorn>=0.27.0
```

---

## Testing

```bash
# Verify skill works
python -c "from skill import get_skill; print(get_skill().health())"

# Test a tool
python -c "from skill import call_tool; print(call_tool('get_price', symbol='BTC/USDT'))"
```

---

## License

MIT License

---

## Links

- **GitHub**: https://github.com/wangshuniguang/DataVault
- **Discord**: https://discord.gg/datavault
- **Website**: https://datavault.io

---

*Built with ❤️ for the Web3 AI community*

**Version**: 1.1.0  
**Last Updated**: 2026-04-14