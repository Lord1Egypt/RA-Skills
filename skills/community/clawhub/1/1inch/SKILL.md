# 1inch DEX 聚合器技能

## 描述
1inch 是一个去中心化交易所 (DEX) 聚合器，通过智能路由算法在多个 DEX 之间寻找最优交易路径。本技能提供 1inch API v5.2 的客户端实现，支持获取报价和执行代币交换。

## 功能
- 获取最优交易报价
- 执行 DEX 代币交换
- 支持多链和多 DEX 聚合
- Gas 估算和优化
- 限价单支持

## API 端点
- **基础 URL**: `https://api.1inch.dev/swap/v5.2`
- **获取报价**: `GET /quote` - 获取交易报价
- **执行交换**: `GET /swap` - 获取交换交易数据

## 使用方法

### Python 客户端
```python
from oneinch_client import OneInchClient

client = OneInchClient(api_key="your_api_key")

# 获取交易报价
quote = client.get_quote(
    chain_id=1,  # Ethereum
    from_token_address="0x...",
    to_token_address="0x...",
    amount="1000000000000000000"  # 1 ETH in wei
)

# 获取支持的代币
tokens = client.get_tokens(chain_id=1)
```

### DEX 交易
```python
from oneinch_swap import OneInchSwap

swap = OneInchSwap(api_key="your_api_key")

# 执行代币交换
tx_data = swap.swap(
    chain_id=1,
    from_token_address="0x...",
    to_token_address="0x...",
    amount="1000000000000000000",
    from_address="0x...",
    slippage=1  # 1%
)
```

## API 参考

### get_quote 参数
- `chain_id`: 链 ID (1=Ethereum, 56=BSC, 137=Polygon, etc.)
- `from_token_address`: 输入代币地址
- `to_token_address`: 输出代币地址
- `amount`: 输入数量 (最小单位)
- `protocols`: (可选) 指定使用的协议
- `gas_price`: (可选) Gas 价格
- `complexity_level`: (可选) 路由复杂度级别

### swap 参数
- `chain_id`: 链 ID
- `from_token_address`: 输入代币地址
- `to_token_address`: 输出代币地址
- `amount`: 输入数量
- `from_address`: 发送方地址
- `slippage`: 滑点容忍度 (百分比，1=1%)
- `disable_estimate`: (可选) 禁用 Gas 估算
- `allow_partial_fill`: (可选) 允许部分成交

## 响应格式

### Quote 响应
```json
{
  "fromToken": {
    "symbol": "ETH",
    "name": "Ethereum",
    "decimals": 18,
    "address": "0x...",
    "logoURI": "..."
  },
  "toToken": {
    "symbol": "USDC",
    "name": "USD Coin",
    "decimals": 6,
    "address": "0x...",
    "logoURI": "..."
  },
  "fromTokenAmount": "1000000000000000000",
  "toTokenAmount": "1850000000",
  "protocols": [...],
  "estimatedGas": 150000
}
```

### Swap 响应
```json
{
  "tx": {
    "from": "0x...",
    "to": "0x...",
    "data": "0x...",
    "value": "1000000000000000000",
    "gasPrice": "20000000000",
    "gas": 150000
  },
  "toTokenAmount": "1850000000",
  "fromTokenAmount": "1000000000000000000"
}
```

## 支持的链
- Ethereum (1)
- BSC (56)
- Polygon (137)
- Optimism (10)
- Arbitrum (42161)
- Avalanche (43114)
- Fantom (250)
- Gnosis (100)
- 更多...

## 错误处理
- 400: 请求参数错误
- 401: API 密钥无效
- 404: 代币或路由未找到
- 429: 请求速率限制
- 500: 服务器错误

## 速率限制
- 免费计划：100 请求/秒
- 需要 API 密钥：https://portal.1inch.dev/

## 依赖
- `requests`: HTTP 客户端库
- Python 3.8+
