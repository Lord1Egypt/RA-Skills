---
name: 区块链数据服务
description: Vitruveo MCP Server 是一个为 Vitruveo 网络提供只读区块链服务的模型上下文协议服务器，适用于AI代理访问区块链数据。
version: 1.0.0
---

# 区块链数据服务

Vitruveo MCP Server 是一个为 Vitruveo 网络提供只读区块链服务的模型上下文协议服务器，适用于AI代理访问区块链数据。

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
| Get core contract addresses | `scripts.tools.get_core_contracts` |
| Get information about an EVM network | `scripts.tools.get_chain_info` |
| Get a list of supported EVM networks | `scripts.tools.get_supported_networks` |
| Get a block by its block number | `scripts.tools.get_block_by_number` |
| Get the latest block from the EVM | `scripts.tools.get_latest_block` |
| Get the native token balance (ETH, MATIC, etc.) for an address | `scripts.tools.get_balance` |
| Get the ERC20 token balance of an Ethereum address | `scripts.tools.get_erc20_balance` |
| Get the balance of an ERC20 token for an address | `scripts.tools.get_token_balance` |
| Get detailed information about a specific transaction by its hash. Includes sender, recipient, value, data, and more. | `scripts.tools.get_transaction` |
| Get a transaction receipt by its hash | `scripts.tools.get_transaction_receipt` |
| Estimate the gas cost for a transaction | `scripts.tools.estimate_gas` |
| Read data from a smart contract by calling a view/pure function. This doesn't modify blockchain state and doesn't require gas or signing. | `scripts.tools.read_contract` |
| Check if an address is a smart contract or an externally owned account (EOA) | `scripts.tools.is_contract` |
| Get comprehensive information about an ERC20 token including name, symbol, decimals, total supply, and other metadata. Use this to analyze any token on EVM chains. | `scripts.tools.get_token_info` |
| Get ERC20 token balance for an address | `scripts.tools.get_token_balance_erc20` |
| Get detailed information about a specific NFT (ERC721 token), including collection name, symbol, token URI, and current owner if available. | `scripts.tools.get_nft_info` |
| Check if an address owns a specific NFT | `scripts.tools.check_nft_ownership` |
| Get the metadata URI for an ERC1155 token (multi-token standard used for both fungible and non-fungible tokens). The URI typically points to JSON metadata about the token. | `scripts.tools.get_erc1155_token_uri` |
| Get the total number of NFTs owned by an address from a specific collection. This returns the count of NFTs, not individual token IDs. | `scripts.tools.get_nft_balance` |
| Get the balance of a specific ERC1155 token ID owned by an address. ERC1155 allows multiple tokens of the same ID, so the balance can be greater than 1. | `scripts.tools.get_erc1155_balance` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_core_contracts
工具描述：Get core contract addresses
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_chain_info
工具描述：Get information about an EVM network
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_supported_networks
工具描述：Get a list of supported EVM networks
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_block_by_number
工具描述：Get a block by its block number
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|blockNumber|number|true| |The block number to fetch|

---

## scripts.tools.get_latest_block
工具描述：Get the latest block from the EVM
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_balance
工具描述：Get the native token balance (ETH, MATIC, etc.) for an address
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|address|string|true| |The wallet address or ENS name (e.g., '0x1234...' or 'vitalik.eth') to check the balance for|

---

## scripts.tools.get_erc20_balance
工具描述：Get the ERC20 token balance of an Ethereum address
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|address|string|true| |The Ethereum address to check|
|tokenAddress|string|true| |The ERC20 token contract address|

---

## scripts.tools.get_token_balance
工具描述：Get the balance of an ERC20 token for an address
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address or ENS name of the ERC20 token (e.g., '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' for USDC or 'uniswap.eth')|
|ownerAddress|string|true| |The wallet address or ENS name to check the balance for (e.g., '0x1234...' or 'vitalik.eth')|

---

## scripts.tools.get_transaction
工具描述：Get detailed information about a specific transaction by its hash. Includes sender, recipient, value, data, and more.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|txHash|string|true| |The transaction hash to look up (e.g., '0x1234...')|

---

## scripts.tools.get_transaction_receipt
工具描述：Get a transaction receipt by its hash
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|txHash|string|true| |The transaction hash to look up|

---

## scripts.tools.estimate_gas
工具描述：Estimate the gas cost for a transaction
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|to|string|true| |The recipient address|
|value|string|false| |The amount of ETH to send in ether (e.g., '0.1')|
|data|string|false| |The transaction data as a hex string|

---

## scripts.tools.read_contract
工具描述：Read data from a smart contract by calling a view/pure function. This doesn't modify blockchain state and doesn't require gas or signing.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|contractAddress|string|true| |The address of the smart contract to interact with|
|abi|array|true| |The ABI (Application Binary Interface) of the smart contract function, as a JSON array|
|functionName|string|true| |The name of the function to call on the contract (e.g., 'balanceOf')|
|args|array|false| |The arguments to pass to the function, as an array (e.g., ['0x1234...'])|

---

## scripts.tools.is_contract
工具描述：Check if an address is a smart contract or an externally owned account (EOA)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|address|string|true| |The wallet or contract address or ENS name to check (e.g., '0x1234...' or 'uniswap.eth')|

---

## scripts.tools.get_token_info
工具描述：Get comprehensive information about an ERC20 token including name, symbol, decimals, total supply, and other metadata. Use this to analyze any token on EVM chains.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address of the ERC20 token (e.g., '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' for USDC on Ethereum)|

---

## scripts.tools.get_token_balance_erc20
工具描述：Get ERC20 token balance for an address
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|address|string|true| |The address to check balance for|
|tokenAddress|string|true| |The ERC20 token contract address|

---

## scripts.tools.get_nft_info
工具描述：Get detailed information about a specific NFT (ERC721 token), including collection name, symbol, token URI, and current owner if available.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for Bored Ape Yacht Club)|
|tokenId|string|true| |The ID of the specific NFT token to query (e.g., '1234')|
|network|string|false| |Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. Most NFTs are on Ethereum mainnet, which is the default.|

---

## scripts.tools.check_nft_ownership
工具描述：Check if an address owns a specific NFT
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address or ENS name of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for BAYC or 'boredapeyachtclub.eth')|
|tokenId|string|true| |The ID of the NFT to check (e.g., '1234')|
|ownerAddress|string|true| |The wallet address or ENS name to check ownership against (e.g., '0x1234...' or 'vitalik.eth')|

---

## scripts.tools.get_erc1155_token_uri
工具描述：Get the metadata URI for an ERC1155 token (multi-token standard used for both fungible and non-fungible tokens). The URI typically points to JSON metadata about the token.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address of the ERC1155 token collection (e.g., '0x76BE3b62873462d2142405439777e971754E8E77')|
|tokenId|string|true| |The ID of the specific token to query metadata for (e.g., '1234')|
|network|string|false| |Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. ERC1155 tokens exist across many networks. Defaults to Ethereum mainnet.|

---

## scripts.tools.get_nft_balance
工具描述：Get the total number of NFTs owned by an address from a specific collection. This returns the count of NFTs, not individual token IDs.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address of the NFT collection (e.g., '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D' for Bored Ape Yacht Club)|
|ownerAddress|string|true| |The wallet address to check the NFT balance for (e.g., '0x1234...')|
|network|string|false| |Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. Most NFTs are on Ethereum mainnet, which is the default.|

---

## scripts.tools.get_erc1155_balance
工具描述：Get the balance of a specific ERC1155 token ID owned by an address. ERC1155 allows multiple tokens of the same ID, so the balance can be greater than 1.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tokenAddress|string|true| |The contract address of the ERC1155 token collection (e.g., '0x76BE3b62873462d2142405439777e971754E8E77')|
|tokenId|string|true| |The ID of the specific token to check the balance for (e.g., '1234')|
|ownerAddress|string|true| |The wallet address to check the token balance for (e.g., '0x1234...')|
|network|string|false| |Network name (e.g., 'vitruveo', 'optimism', 'arbitrum', 'base', 'polygon') or chain ID. ERC1155 tokens exist across many networks. Defaults to Ethereum mainnet.|

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