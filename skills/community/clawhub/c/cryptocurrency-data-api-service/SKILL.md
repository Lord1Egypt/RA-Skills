---
name: 加密货币数据API服务
description: DexPaprika MCP Server是一个提供实时加密货币和DEX数据访问的API服务，专为AI助手设计，无需配置即可获取代币、流动池和DEX数据。
version: 1.0.0
---

# 加密货币数据API服务

DexPaprika MCP Server是一个提供实时加密货币和DEX数据访问的API服务，专为AI助手设计，无需配置即可获取代币、流动池和DEX数据。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| REQUIRED FIRST STEP: Get all supported blockchain networks. Always call this first to see available networks before using any network-specific functions. Returns network IDs like "ethereum", "solana", etc. | `scripts.tools.getNetworks` |
| Get available DEXes on a specific network. First call getNetworks to see valid network IDs. | `scripts.tools.getNetworkDexes` |
| PRIMARY POOL FUNCTION: Get top liquidity pools on a specific network. This is the MAIN way to get pool data - there is NO global pools function. Use this instead of any "getTopPools" or "getAllPools" concepts. | `scripts.tools.getNetworkPools` |
| Get pools from a specific DEX on a network. First use getNetworks, then getNetworkDexes to find valid DEX IDs. | `scripts.tools.getDexPools` |
| Get detailed information about a specific pool. Requires network ID from getNetworks and a pool address. | `scripts.tools.getPoolDetails` |
| Get detailed information about a specific token on a network. First use getNetworks to get valid network IDs. | `scripts.tools.getTokenDetails` |
| Get liquidity pools containing a specific token on a network. Great for finding where a token is traded. | `scripts.tools.getTokenPools` |
| Get historical price data (OHLCV) for a pool - essential for price analysis, backtesting, and visualization. Requires network and pool address. | `scripts.tools.getPoolOHLCV` |
| Get recent transactions for a specific pool. Shows swaps, adds, removes. Requires network and pool address. | `scripts.tools.getPoolTransactions` |
| Search across ALL networks for tokens, pools, and DEXes by name, symbol, or address. Good starting point when you don't know the specific network. | `scripts.tools.search` |
| Get high-level statistics about the DexPaprika ecosystem: total networks, DEXes, pools, and tokens available. | `scripts.tools.getStats` |
| Get batched prices for multiple tokens on a specific network. Pass an array of token addresses; unknown tokens are omitted. | `scripts.tools.getTokenMultiPrices` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.getNetworks
工具描述：REQUIRED FIRST STEP: Get all supported blockchain networks. Always call this first to see available networks before using any network-specific functions. Returns network IDs like "ethereum", "solana", etc.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.getNetworkDexes
工具描述：Get available DEXes on a specific network. First call getNetworks to see valid network IDs.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|page|number|false|0.0|Page number for pagination|
|limit|number|false|10.0|Number of items per page (max 100)|
|sort|string|false|"desc"|Sort order|
|orderBy|string|false| |How to order the returned data|

---

## scripts.tools.getNetworkPools
工具描述：PRIMARY POOL FUNCTION: Get top liquidity pools on a specific network. This is the MAIN way to get pool data - there is NO global pools function. Use this instead of any "getTopPools" or "getAllPools" concepts.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (required) - e.g., "ethereum", "solana"|
|page|number|false|0.0|Page number for pagination|
|limit|number|false|10.0|Number of items per page (max 100)|
|sort|string|false|"desc"|Sort order|
|orderBy|string|false|"volume_usd"|Field to order by|

---

## scripts.tools.getDexPools
工具描述：Get pools from a specific DEX on a network. First use getNetworks, then getNetworkDexes to find valid DEX IDs.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|dex|string|true| |DEX identifier from getNetworkDexes (e.g., "uniswap_v3")|
|page|number|false|0.0|Page number for pagination|
|limit|number|false|10.0|Number of items per page (max 100)|
|sort|string|false|"desc"|Sort order|
|orderBy|string|false|"volume_usd"|Field to order by|

---

## scripts.tools.getPoolDetails
工具描述：Get detailed information about a specific pool. Requires network ID from getNetworks and a pool address.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|poolAddress|string|true| |Pool address or identifier|
|inversed|boolean|false|false|Whether to invert the price ratio|

---

## scripts.tools.getTokenDetails
工具描述：Get detailed information about a specific token on a network. First use getNetworks to get valid network IDs.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|tokenAddress|string|true| |Token address or identifier|

---

## scripts.tools.getTokenPools
工具描述：Get liquidity pools containing a specific token on a network. Great for finding where a token is traded.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|tokenAddress|string|true| |Token address or identifier|
|page|number|false|0.0|Page number for pagination|
|limit|number|false|10.0|Number of items per page (max 100)|
|sort|string|false|"desc"|Sort order|
|orderBy|string|false|"volume_usd"|Field to order by|
|reorder|boolean|false| |If true, reorders the pool so that the specified token becomes the primary token for all metrics|
|address|string|false| |Filter pools that contain this additional token address|

---

## scripts.tools.getPoolOHLCV
工具描述：Get historical price data (OHLCV) for a pool - essential for price analysis, backtesting, and visualization. Requires network and pool address.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|poolAddress|string|true| |Pool address or identifier|
|start|string|true| |Start time for historical data (Unix timestamp, RFC3339 timestamp, or yyyy-mm-dd format)|
|end|string|false| |End time for historical data (max 1 year from start)|
|limit|number|false|1.0|Number of data points to retrieve (max 366) - adjust for different analysis needs|
|interval|string|false|"24h"|Interval granularity: 1m, 5m, 10m, 15m, 30m, 1h, 6h, 12h, 24h|
|inversed|boolean|false|false|Whether to invert the price ratio for alternative pair perspective (e.g., ETH/USDC vs USDC/ETH)|

---

## scripts.tools.getPoolTransactions
工具描述：Get recent transactions for a specific pool. Shows swaps, adds, removes. Requires network and pool address.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|poolAddress|string|true| |Pool address or identifier|
|page|number|false|0.0|Page number for pagination (up to 100 pages)|
|limit|number|false|10.0|Number of items per page (max 100)|
|cursor|string|false| |Transaction ID used for cursor-based pagination|

---

## scripts.tools.search
工具描述：Search across ALL networks for tokens, pools, and DEXes by name, symbol, or address. Good starting point when you don't know the specific network.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search term (e.g., "uniswap", "bitcoin", or a token address)|

---

## scripts.tools.getStats
工具描述：Get high-level statistics about the DexPaprika ecosystem: total networks, DEXes, pools, and tokens available.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.getTokenMultiPrices
工具描述：Get batched prices for multiple tokens on a specific network. Pass an array of token addresses; unknown tokens are omitted.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|network|string|true| |Network ID from getNetworks (e.g., "ethereum", "solana")|
|tokens|array|true| |Array of token contract addresses. Serialized as repeatable query (?tokens=a&tokens=b).|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据