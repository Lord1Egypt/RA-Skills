---
name: check-hymx-info
description: 查看 hymatrix 网络跨链 支持哪些 Token， 支持哪些链？
command: node script/index.js
---

# 获取 Hymatrix 网络 跨链信息

## Trigger

When asking users for cross-chain information, which tokens are supported?

## Output

返回 tokens 列表， 包含跨链信息，Token 的信息 等。

```json
[
  {
    "chainType": "aostest",
    "chainId": 99,
    "symbol": "AO",
    "decimals": 12,
    "name": "AO",
    "locker": "9C-Z94fVLcAExlCCOQNE2F3hXb3mDiz599dNkZvsX-0",
    "tokenId": "0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc",
    "wrappedTokenId": "SX8LisFGf3lqN1HJMa15F3FawZUdI4e8FRoE2EeoWCo",
    "logo": "",
    "stableRange": 0,
    "maxBurnAmts": {},
    "feeRecipient": "",
    "burnFees": {},
    "wrappedTokenIds": ["SX8LisFGf3lqN1HJMa15F3FawZUdI4e8FRoE2EeoWCo"]
  },
  {
    "chainType": "ethereum",
    "chainId": 1,
    "symbol": "ETH",
    "decimals": 18,
    "name": "ETH",
    "locker": "0x3D9c68E6B4c7105A6aE66c30B204A73f053bD45d",
    "tokenId": "0x0000000000000000000000000000000000000000",
    "wrappedTokenId": "KX8CqkwLcVuASe_jI4LNKWFxtE0WY9baVzuV12ZvTr4",
    "logo": "",
    "stableRange": 0,
    "maxBurnAmts": {},
    "feeRecipient": "",
    "burnFees": {},
    "wrappedTokenIds": ["KX8CqkwLcVuASe_jI4LNKWFxtE0WY9baVzuV12ZvTr4"]
  },
  {
    "chainType": "ethereum",
    "chainId": 1,
    "symbol": "USDC",
    "decimals": 6,
    "name": "USDC",
    "locker": "0x3D9c68E6B4c7105A6aE66c30B204A73f053bD45d",
    "tokenId": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "wrappedTokenId": "v3-NSt4h-OXQuA6DAkBwDTv-11UYu8Z9W5a2KRhnGpw",
    "logo": "",
    "stableRange": 0,
    "maxBurnAmts": {},
    "feeRecipient": "",
    "burnFees": {},
    "wrappedTokenIds": ["v3-NSt4h-OXQuA6DAkBwDTv-11UYu8Z9W5a2KRhnGpw"]
  },
  {
    "chainType": "hymatrix",
    "chainId": 0,
    "symbol": "AO",
    "decimals": "12",
    "name": "AO Token",
    "locker": "9C-Z94fVLcAExlCCOQNE2F3hXb3mDiz599dNkZvsX-0",
    "tokenId": "SX8LisFGf3lqN1HJMa15F3FawZUdI4e8FRoE2EeoWCo",
    "wrappedTokenId": "0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc",
    "logo": "",
    "stableRange": 0,
    "cuUrl": "https://bridge-node-dev.hymatrix.com",
    "maxBurnAmts": {
      "aostest:0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc": "1258.321226676586"
    },
    "feeRecipient": "0xe1c3124E11219C09e7B4EB75a98930e3c43C3e1c",
    "burnFees": { "aostest": "0.0000000001" },
    "wrappedTokenIds": ["0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc"]
  },
  {
    "chainType": "hymatrix",
    "chainId": 0,
    "symbol": "ETH",
    "decimals": "18",
    "name": "Ethereum Token",
    "locker": "0x3D9c68E6B4c7105A6aE66c30B204A73f053bD45d",
    "tokenId": "KX8CqkwLcVuASe_jI4LNKWFxtE0WY9baVzuV12ZvTr4",
    "wrappedTokenId": "0x0000000000000000000000000000000000000000",
    "logo": "",
    "stableRange": 0,
    "cuUrl": "https://bridge-node-dev.hymatrix.com",
    "maxBurnAmts": {
      "ethereum:0x0000000000000000000000000000000000000000": "1.945792491825996"
    },
    "feeRecipient": "0x72365DA62A3F9652a61bD11F2069AC41FBb5Bd8E",
    "burnFees": { "ethereum": "0.0005" },
    "wrappedTokenIds": ["0x0000000000000000000000000000000000000000"]
  },
  {
    "chainType": "hymatrix",
    "chainId": 0,
    "symbol": "USDC",
    "decimals": "6",
    "name": "ETH USDC",
    "locker": "0x3D9c68E6B4c7105A6aE66c30B204A73f053bD45d",
    "tokenId": "v3-NSt4h-OXQuA6DAkBwDTv-11UYu8Z9W5a2KRhnGpw",
    "wrappedTokenId": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "logo": "",
    "stableRange": 0,
    "cuUrl": "https://bridge-node-dev.hymatrix.com",
    "maxBurnAmts": {
      "ethereum:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": "9731.793325"
    },
    "feeRecipient": "0x72365DA62A3F9652a61bD11F2069AC41FBb5Bd8E",
    "burnFees": { "ethereum": "0.1" },
    "wrappedTokenIds": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"]
  }
]
```

**字段类型**

```ts
export interface HymxBridgeTokenItem {
  chainType: string
  chainId: number
  symbol: string
  decimals: number
  name: string
  locker: string
  tokenId: string
  wrappedTokenId: string
  logo: string
  stableRange: number
  maxBurnAmts: { [key: string]: string }
  feeRecipient: string
  burnFees: { [key: string]: string }
  minBurnAmt?: string
  wrappedTokenIds?: string[]
  cuUrl?: string
}
```

## **子段解释**:

- `chainType`: `Token` 所在的链，例如 `ethereum`, `arweave`, `hymatrix`。
- `chainId`: `Token` 链的 `Id`。
- `symbol`: `Token` 的 `Symbol。`
- `decimals`: `Token` 的数额精度。
- `name`: `Token` 的 全称，和 `Symbol` 字符长短不一。
- `locker`: 锁仓。
- `tokenId`: `tokenId`， `Token` 的唯一标识。
- `wrappedTokenId`: `Token` 可以跨链成 `wrappedTokenId`。该地址也是唯一标识。
- `logo`: `Token` 的图片地址。
- `stableRange`: 都是 `0`，可忽略。
- `maxBurnAmts`:最大提现的数额。不同链，不同额度。 该对象 可通过 `chainType:tokenId`为键名的形式获取键值 示例: `{"ethereum:0x0000000000000000000000000000000000000000": "1945792.491825996"}`。
- `feeRecipient`：手续费收款地址。
- `burnFees`: 提现的`手续费`。不同链，不同额度。该对象 可通过 `chainType`为键名的形式获取键值 示例: `{"ethereum": "0.0005"}`。
- `cuUrl`: 通常 `cuUrl` 存在，都是 `hymatrix` 链上的 `Token`, `hymatrix Token` 再进行交易时，需要依赖这个 `cuUrl`, 否则无法进行交易。
- wrappedTokenIds: 该字段是数组，为了防止 `tokenId` 可以跨成不同的 `wrappedTokenId`, 可通过 `wrappedTokenIds` 数组，来确认一共支持跨成哪些 `Token`, 通常都只有一个。
