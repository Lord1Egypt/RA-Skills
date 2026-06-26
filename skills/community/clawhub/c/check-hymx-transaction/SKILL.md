---
name: check-transaction
description: Check transaction status on Hymatrix bridge
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
  "rawId": 594,
  "createdAt": "2026-03-17T15:00:34.835Z",
  "updatedAt": "2026-03-17T15:00:34.835Z",
  "txType": "burn",
  "ChainType": "aostest",
  "TokenId": "0syT13r0s0tgPmIed95bJnuSqaD29HQNN8D3ElLSrsc",
  "WrappedTokenId": "SX8LisFGf3lqN1HJMa15F3FawZUdI4e8FRoE2EeoWCo",
  "txId": "gXZ8rxlGsj0yebaNXvBT9jNp68YCSfo40l6suH7tz_w",
  "sender": "0x578Dde4A4e00FF74c31E3645C28f06bE35D8aDEA",
  "recipient": "XWDOELeht4sdZ1HggZHM95OjEQIzTvoTnoJVt_u6Z9k",
  "blockHeight": 0,
  "amount": "105951171869250",
  "fee": "0",
  "feeRecipient": "0x72365DA62A3F9652a61bD11F2069AC41FBb5Bd8E",
  "status": "waiting",
  "targetChainTxHash": "",
  "approveTx": ""
}
```

**字段类型**

```ts
export interface BridgeHymxListItem {
  rawId: number
  createdAt: string
  updatedAt: string
  txType: 'burn' | 'mint'
  ChainType: string
  TokenId: string
  WrappedTokenId: string
  txId: string
  sender: string
  recipient: string
  blockHeight: number
  amount: string
  fee: string
  feeRecipient: string
  status:
    | 'success'
    | 'unPackaged'
    | 'waiting'
    | 'confirmed'
    | 'failed'
    | 'submintAosFailed'
    | 'notOnChain'
  targetChainTxHash: string
  errMsg?: string
  userAddress?: string
}
```

## **子段解释**:

- `rawId`: 游标
- `createdAt`: 创建交易的时间。
- `updatedAt`: 每当 `status` 改变会立即更新的时间。
- `txType`: 交易类型 `mint`代表充值 `burn` 代表提现。
- `ChainType`: `txType`等于 `mint` 代表 `ChainType`链到 hymatrix 网络,`txType`等于 `burn`代表 hymatrix 网络 到 `ChainType`链。
- `TokenId`: 存入/铸造 的 `tokenId`。注意 info 提示
- `WrappedTokenId`: 提取/销毁 的 `tokenId` 。注意 info 提示
- `txId`: 交易哈希。
- `sender`: 发起人的地址。
- `recipient`: 收款人地址。
- `amount`: 交易金额，若`fee`不为空，则收款账户需要缴纳手续费代表 `amount` - `fee` = 实际到账金额。
- `fee`: 手续费。
- `feeRecipient`：手续费收款地址。
- `status`: 当前交易的状态，根据下方 info 中 status 返回给用户。
- `targetChainTxHash`: 目标链的哈希。
- `errMsg`: 当交易失败时，该字段回返回失败的原因。
-

:::info

- fromToken/toToken `TokenId` 和 `WrappedTokenId` 要根据交易类型拍判断谁是(存入/铸造)或(提取/销毁)，交易类型 `txType` 确定资产流向——若为 `mint` (存入/铸造)，原始资产为 `TokenId`，目标资产为 `WrappedTokenId`；若为非 `mint` (提取/销毁)，则方向相反。

- status: Agent 需根据 `txType` 判定交易阶段——若为 `mint` (存入)，`unPackaged` 为待上链，`waiting`/`confirmed` 为待收款 (wrapping)；若为非 `mint` (提取)，`unPackaged` 为待燃烧，`waiting` 为待执行。其余状态（如 `success`, `failed`, `packageing`）直接映射至对应的多语言标签。
  :::
