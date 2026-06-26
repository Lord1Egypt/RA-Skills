---
name: check-ao-transaction
description: Check transaction status on AO bridge
command: node script/index.js
---

# Multi Chain Transaction Checker

## Trigger

当用户提供交易 ID 或哈希值并询问以下信息时，请使用此技能：

## Input

{
"tx_hash": "transaction hash"
}

## Output

```json
{
  "rawId": 1773755697333,
  "createdAt": "2026-03-17T13:54:57.333Z",
  "updatedAt": "2026-03-17T15:23:03.604Z",
  "txType": "burn",
  "chainType": "arweave",
  "txId": "hcdE4lfIlNEXGp9bV4fggyHMJ3-kha4Zozv7Ax4F-mU",
  "sender": "y3-JfAs4xSwhpIFCvX0sIsAtZMHGxtutQ7yP6xuH4AI",
  "recipient": "y3-JfAs4xSwhpIFCvX0sIsAtZMHGxtutQ7yP6xuH4AI",
  "quantity": "1462196993511",
  "symbol": "AR",
  "decimals": 12,
  "blockHeight": 1878366,
  "fromTokenId": "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10",
  "toTokenId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
  "fee": "300000000000",
  "feeRecipient": "4S58xCqS6uKcrvqb2JlrCWllC2VIBs7qxU15QbWa3ZI",
  "confirmNum": 0,
  "confirmRange": 0,
  "status": "waiting",
  "targetChainTxHash": ""
}
```

**字段类型**

```ts
export interface BridgeHymxListItem {
  rawId: number
  createdAt: string
  updatedAt: string
  txType: 'burn' | 'mint'
  chainType: string
  txId: string
  sender: string
  recipient: string
  quantity: string
  symbol: string
  decimals: number
  blockHeight: number
  fromTokenId: string
  toTokenId: string
  fee: string
  feeRecipient: string
  confirmNum: number
  confirmRange: number
  status:
    | 'success'
    | 'unPackaged'
    | 'waiting'
    | 'confirmed'
    | 'failed'
    | 'submintAosFailed'
    | 'notOnChain'
  targetChainTxHash: string
}
```

## **子段解释**:

- `rawId`: 游标
- `createdAt`: 创建交易的时间。
- `updatedAt`: 每当 `status` 改变会立即更新的时间。
- `txType`: 交易类型 `mint`代表充值, `burn` 代表提现。
- `chainType`: `txType` 等于 `mint` 代表 `chainType` 链到 ao 网络,`txType`等于 `burn` 代表 ao 网络 到 `chainType` 链。
- `txId`: 交易哈希。
- `sender`: 发起人的地址。
- `recipient`: 收款人地址。
- `quantity`: 实际到账交易金额，若 `fee` 不为空，则代表 `quantity` + `fee` = 发起人交易时的金额。
- `symbol`: `Token` 的 `Symbol`, 是 `fromTokenId` 的 `symbol`。注意 info 提示
- `decimals`: `Token` 的数额精度。 是 `fromTokenId` 的 `decimals`。 注意 info 提示
- `blockHeight`: 当前交易的区块高度。
- `fromTokenId`: 存入/铸造 的 `tokenId`。注意 info 提示
- `toTokenId`: 提取/销毁 的 `tokenId` 。注意 info 提示
- `fee`: 手续费。
- `feeRecipient`：手续费收款地址。
- `status`: 当前交易的状态，根据下方 info 中 status 返回给用户。
- `confirmNum`: 总共需要确认多少个区块。
- `confirmRange`: 目前已经确认了多少区块。
- `targetChainTxHash`: 目标链的哈希。

:::info

- fromToken/toToken `fromTokenId` 和 `toTokenId` 要根据交易类型拍判断谁是(存入/铸造)或(提取/销毁)，交易类型 `txType` 确定资产流向——若为 `mint` (存入/铸造)，原始资产为 `fromTokenId`，目标资产为 `toTokenId`；若为非 `mint` (提取/销毁)，则方向相反。

- status: Agent 需根据 `txType` 判定交易

### 当 `txType = mint`

- `unPackaged` → `待上链`
- `waiting` 或 `confirmed`
  - `confirmRange > 0` → `待确认`
  - `confirmRange <= 0` → `待收款`
- 其他状态 → （如 `success`, `failed`, `packageing`）直接映射至对应的多语言标签。

### 当 `txType = burn`

- `unPackaged` → `待燃烧`
- `waiting` → `待执行`
- 其他状态 → （如 `success`, `failed`, `packageing`）直接映射至对应的多语言标签。
  :::
