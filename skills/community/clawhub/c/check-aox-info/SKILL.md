---
name: check-aox-info
description: 查看 AO 网络 跨链，支持哪些 Token， 支持哪些链？ 目前关闭或开启了哪条链的充值或提现功能。
command: node script/index.js
---

# 获取 AO 网络基本信息

## Trigger

当用户问到 AO 网络 跨链的基本信息时。

- 都有哪些交易对？
- 某一个链当前是否可以充值或提现？
- 某一个链提现手续费是多少？

## Output
返回 `closeServer`关闭功能数据，以及跨链 ` tokens` 包含 `Token` 的信息 等。
### 示例返回

```json
{
  "closeServer": {
    "closeBaseMint": true,
    "closeEthMint": false,
    "closeBscMint": false,
    "closeArweaveMint": false,
    "closeEthBurn": true,
    "closeBscBurn": true,
    "closeArweaveBurn": true,
    "closeTransfer": true
  },
  "tokens": [
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wUSDC",
      "decimals": 6,
      "name": "Ethereum-Wrapped USDC",
      "stableRange": 0,
      "locker": "",
      "tokenId": "7zH9dlMNoxprab9loshv3Y7WG45DOny_Vrq9KrXObdQ",
      "wrappedTokenId": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "minBurnAmt": "0.271524",
      "burnFee": "0.271524",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "w4EVER",
      "decimals": 18,
      "name": "Ethereum-Wrapped 4EVER",
      "stableRange": 0,
      "locker": "",
      "tokenId": "y9NnhY2RtCz0JP7LMJM8lIG2yGpZDAg0FUMYwDK_0Pg",
      "wrappedTokenId": "0xe355De6a6043b0580Ff5A26b46051A4809B12793",
      "minBurnAmt": "5000",
      "burnFee": "2000",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wANS",
      "decimals": 18,
      "name": "Ethereum-Wrapped ANS",
      "stableRange": 0,
      "locker": "",
      "tokenId": "kCHI8LYxZf1NsmRoHCKHsf6PD4sMAvfPsMSkLta54Rw",
      "wrappedTokenId": "0x937EFa4a5Ff9d65785691b70a1136aAf8aDA7e62",
      "minBurnAmt": "0",
      "burnFee": "0",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wANYONE",
      "decimals": 18,
      "name": "Ethereum-Wrapped ANYONE",
      "stableRange": 0,
      "locker": "",
      "tokenId": "H41CVAmengY3BuSz1aLjFJf26RKFbj0ENGTI7aG8j-U",
      "wrappedTokenId": "0xFeAc2Eae96899709a43E252B6B92971D32F9C0F9",
      "minBurnAmt": "0",
      "burnFee": "0",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wETH",
      "decimals": 18,
      "name": "Ethereum-Wrapped ETH",
      "stableRange": 0,
      "locker": "",
      "tokenId": "cBgS-V_yGhOe9P1wCIuNSgDA_JS8l4sE5iFcPTr0TD0",
      "wrappedTokenId": "0x0000000000000000000000000000000000000000",
      "minBurnAmt": "0.00013",
      "burnFee": "0.00013",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wUSDT",
      "decimals": 18,
      "name": "BSC-Wrapped USDT",
      "stableRange": 0,
      "locker": "",
      "tokenId": "7j3jUyFpTuepg_uu_sJnwLE6KiTVuA9cLrkfOp2MFlo",
      "wrappedTokenId": "0x55d398326f99059fF775485246999027B3197955",
      "minBurnAmt": "1",
      "burnFee": "0.5",
    },
    {
      "chainType": "ao",
      "chainId": 0,
      "symbol": "wAR",
      "decimals": 12,
      "name": "Wrapped AR",
      "stableRange": 0,
      "locker": "",
      "tokenId": "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10",
      "wrappedTokenId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "minBurnAmt": "0.5",
      "burnFee": "0.3",
    },
    {
      "chainType": "arweave",
      "chainId": 0,
      "symbol": "AR",
      "decimals": 12,
      "stableRange": 10,
      "locker": "AKQcAkNtnNXmEWBMMxfJ08oeoHP3RLs2jshRGnje1ow",
      "tokenId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
      "wrappedTokenId": "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10"
    },
    {
      "chainType": "ethereum",
      "chainId": 1,
      "symbol": "USDC",
      "decimals": 6,
      "stableRange": 20,
      "locker": "0xB3F2f559Fe40c1F1eA1e941E982d9467208e17ae",
      "tokenId": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "wrappedTokenId": "7zH9dlMNoxprab9loshv3Y7WG45DOny_Vrq9KrXObdQ"
    },
    {
      "chainType": "ethereum",
      "chainId": 1,
      "symbol": "4EVER",
      "decimals": 18,
      "stableRange": 20,
      "locker": "0xB3F2f559Fe40c1F1eA1e941E982d9467208e17ae",
      "tokenId": "0xe355De6a6043b0580Ff5A26b46051A4809B12793",
      "wrappedTokenId": "y9NnhY2RtCz0JP7LMJM8lIG2yGpZDAg0FUMYwDK_0Pg"
    },
    {
      "chainType": "ethereum",
      "chainId": 1,
      "symbol": "ANS",
      "decimals": 18,
      "stableRange": 20,
      "locker": "0xB3F2f559Fe40c1F1eA1e941E982d9467208e17ae",
      "tokenId": "0x937EFa4a5Ff9d65785691b70a1136aAf8aDA7e62",
      "wrappedTokenId": "kCHI8LYxZf1NsmRoHCKHsf6PD4sMAvfPsMSkLta54Rw"
    },
    {
      "chainType": "ethereum",
      "chainId": 1,
      "symbol": "ANYONE",
      "decimals": 18,
      "stableRange": 20,
      "locker": "0xB3F2f559Fe40c1F1eA1e941E982d9467208e17ae",
      "tokenId": "0xFeAc2Eae96899709a43E252B6B92971D32F9C0F9",
      "wrappedTokenId": "H41CVAmengY3BuSz1aLjFJf26RKFbj0ENGTI7aG8j-U"
    },
    {
      "chainType": "ethereum",
      "chainId": 1,
      "symbol": "ETH",
      "decimals": 18,
      "stableRange": 20,
      "locker": "0xB3F2f559Fe40c1F1eA1e941E982d9467208e17ae",
      "tokenId": "0x0000000000000000000000000000000000000000",
      "wrappedTokenId": "cBgS-V_yGhOe9P1wCIuNSgDA_JS8l4sE5iFcPTr0TD0"
    },
    {
      "chainType": "bsc",
      "chainId": 56,
      "symbol": "USDT",
      "decimals": 18,
      "stableRange": 20,
      "locker": "0x694f7D125557b0d43080932D61ad5EAEC203CDb9",
      "tokenId": "0x55d398326f99059fF775485246999027B3197955",
      "wrappedTokenId": "7j3jUyFpTuepg_uu_sJnwLE6KiTVuA9cLrkfOp2MFlo"
    }
  ]
}
```

## 字段解释

`closeServer` 表示一组**功能开关配置**，用于控制哪些充值、提现、转账功能被禁用。

规则说明：

- `true` 表示 **关闭 / 禁用**
- `false` 表示 **开启 / 不禁用**

---

## 字段含义

`closeServer` 是业务功能禁用配置，用于控制不同链上的充值、提现，以及系统转账功能是否可用。

## 规则

- 字段值为 `true`：表示该功能已关闭 / 禁用
- 字段值为 `false`：表示该功能开启 / 可正常使用

## 业务语义

在本系统中：

- `Mint` 表示 **充值**
- `Burn` 表示 **提现**
- `Transfer` 表示 **转账**

链字段含义：

- `Base` 表示 **Base 链**
- `Eth` 表示 **Ethereum 链**
- `Bsc` 表示 **BSC 链**
- `Arweave` 表示 **Arweave 链**

## 字段定义

- `closeBaseMint`
  - 含义：是否关闭 **Base 链充值功能**

- `closeEthMint`
  - 含义：是否关闭 **Ethereum 链充值功能**

- `closeBscMint`
  - 含义：是否关闭 **BSC 链充值功能**

- `closeArweaveMint`
  - 含义：是否关闭 **Arweave 链充值功能**

- `closeEthBurn`
  - 含义：是否关闭 **Ethereum 链提现功能**

- `closeBscBurn`
  - 含义：是否关闭 **BSC 链提现功能**

- `closeArweaveBurn`
  - 含义：是否关闭 **Arweave 链提现功能**

- `closeTransfer`
  - 含义：是否关闭 **系统转账功能**

## 当前配置对应的状态

根据当前配置：

- `closeBaseMint: true`
  - Base 链充值：已关闭

- `closeEthMint: false`
  - Ethereum 链充值：已开启

- `closeBscMint: false`
  - BSC 链充值：已开启

- `closeArweaveMint: false`
  - Arweave 链充值：已开启

- `closeEthBurn: true`
  - Ethereum 链提现：已关闭

- `closeBscBurn: true`
  - BSC 链提现：已关闭

- `closeArweaveBurn: true`
  - Arweave 链提现：已关闭

- `closeTransfer: true`
  - 转账功能：已关闭

## 当前系统状态总结

当前系统中：

- Base 链充值已关闭
- Ethereum 链充值开启
- BSC 链充值开启
- Arweave 链充值开启
- Ethereum 链提现已关闭
- BSC 链提现已关闭
- Arweave 链提现已关闭
- 转账功能已关闭

## 链充值/提现关闭时的回复规则

当检测到某些链的充值或提现功能被关闭时，需要按 **链** 和 **操作类型** 进行归类后再回复用户，尽量合并相同状态，避免重复逐条播报。

### 回复原则

- 如果多个链关闭的是同一种操作，则合并成一句回复。
- 如果某条链同时关闭了充值和提现，则在同一句中同时说明。
- 如果不同链关闭的操作不同，则按链分组后分别回复。
- 文案统一使用“网络或系统正在升级维护，xxx 暂不可用”。

### 文案模板

#### 1. 多条链关闭相同操作
适用于多个链都只关闭了同一种操作，例如都关闭提现：

`{chains}` 网络或系统正在升级维护，`{actions}` 暂不可用。

示例：
- Ethereum、Arweave、BSC 网络或系统正在升级维护，提现暂不可用。
- Ethereum、BSC 网络或系统正在升级维护，充值暂不可用。

---

#### 2. 单条链同时关闭充值和提现
适用于某一条链同时关闭充值和提现：

`{chain}` 网络或系统正在升级维护，充值、提现暂不可用。

示例：
- Ethereum 网络或系统正在升级维护，充值、提现暂不可用。

---

#### 3. 不同链关闭的操作不同
适用于不同链关闭的操作不一致，需要分开描述：

`{chains1}` 网络或系统正在升级维护，`{actions1}` 暂不可用。`{chains2}` 网络或系统正在升级维护，`{actions2}` 暂不可用。

示例：
- Ethereum 网络或系统正在升级维护，充值、提现暂不可用。Arweave、BSC 网络或系统正在升级维护，提现暂不可用。
- Ethereum、BSC 网络或系统正在升级维护，充值暂不可用。Arweave 网络或系统正在升级维护，提现暂不可用。

---

`tokens` 用于描述**同一种资产在不同链上的映射关系**，以及该资产在跨链过程中的基础配置。该数组中有两种 不同类型的 `Token`, `AO` 网络和`其他网络` 也就是 `ethereum` 链 或 `arweave` 链.

## 字段定义
- `chainType`：`Token` 所在的链，例如 `ethereum`, `arweave`, `ao`。
- `chainId`: `Token` 链的 `Id`。
- `symbol`: `Token` 的 `Symbol。`
- `decimals`: `Token` 的数额精度。
- `stableRange`: 需要等待多少个区块，在ao网络不会存在，可忽略。但在原生链中会存在，例如： `ethereum` 需要 `20`个区块, `arweave` 需要 `10` 个区块。
- `name`: `Token` 的全称，和 `Symbol` 字符长短不一， 仅在 ao 网络中存在。
- `locker`: 锁仓地址。
- `tokenId`: `tokenId`， `Token` 的唯一标识。
- `wrappedTokenId`: `Token` 可以跨链成 `wrappedTokenId`。该地址也是唯一标识。
- `minBurnAmt`： 在提现时需要，是最小提现数额，没有则是 `0`。
- `burnFee`: 在提现时所需要的手续费，没有则是 `0`。

## 记录

- [ ] 记录查询结果到 memory（如重要）
