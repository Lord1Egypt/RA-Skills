# FXAI 合约 ABI（USDT/BNB 双池）

**合约地址**：`0x8f059fEb5f34031EfFA024e9EB8C9968BfFE516a`  
**USDT（BSC）**：`0x55d398326f99059fF775485246999027B3197955`

---

## createToken（USDT 池子，兼容旧流程）

```json
[
  {
    "inputs": [
      { "internalType": "string", "name": "_name", "type": "string" },
      { "internalType": "string", "name": "_symbol", "type": "string" },
      { "internalType": "string", "name": "_meta", "type": "string" },
      { "internalType": "address", "name": "_feeTo", "type": "address" },
      { "internalType": "bytes32", "name": "_salt", "type": "bytes32" },
      { "internalType": "uint16", "name": "_taxRate", "type": "uint16" },
      { "internalType": "uint16", "name": "_mktBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_dividendBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_deflationBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_lpBps", "type": "uint16" },
      { "internalType": "uint256", "name": "_minimumShareBalance", "type": "uint256" }
    ],
    "name": "createToken",
    "outputs": [{ "internalType": "address", "name": "token", "type": "address" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

---

## createTokenWithQuote（可选 USDT/BNB 池子）

`_quoteMode`：`0=USDT`，`1=BNB`

```json
[
  {
    "inputs": [
      { "internalType": "string", "name": "_name", "type": "string" },
      { "internalType": "string", "name": "_symbol", "type": "string" },
      { "internalType": "string", "name": "_meta", "type": "string" },
      { "internalType": "address", "name": "_feeTo", "type": "address" },
      { "internalType": "bytes32", "name": "_salt", "type": "bytes32" },
      { "internalType": "uint16", "name": "_taxRate", "type": "uint16" },
      { "internalType": "uint16", "name": "_mktBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_dividendBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_deflationBps", "type": "uint16" },
      { "internalType": "uint16", "name": "_lpBps", "type": "uint16" },
      { "internalType": "uint256", "name": "_minimumShareBalance", "type": "uint256" },
      { "internalType": "uint8", "name": "_quoteMode", "type": "uint8" }
    ],
    "name": "createTokenWithQuote",
    "outputs": [{ "internalType": "address", "name": "token", "type": "address" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

---

## 买入

### buyTokensByUSDT

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" },
      { "internalType": "uint256", "name": "_usdtAmount", "type": "uint256" }
    ],
    "name": "buyTokensByUSDT",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

### buyTokensByBNB

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" }
    ],
    "name": "buyTokensByBNB",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  }
]
```

---

## 卖出（按数量）

### sellTokensToUSDT

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" },
      { "internalType": "uint256", "name": "_tokenAmount", "type": "uint256" }
    ],
    "name": "sellTokensToUSDT",
    "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

### sellTokensToBNB

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" },
      { "internalType": "uint256", "name": "_tokenAmount", "type": "uint256" }
    ],
    "name": "sellTokensToBNB",
    "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

---

## 卖出（按比例）

### sellTokensByPercentToUSDT

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" },
      { "internalType": "uint256", "name": "_percentBps", "type": "uint256" }
    ],
    "name": "sellTokensByPercentToUSDT",
    "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

### sellTokensByPercentToBNB

```json
[
  {
    "inputs": [
      { "internalType": "address", "name": "_token", "type": "address" },
      { "internalType": "uint256", "name": "_percentBps", "type": "uint256" }
    ],
    "name": "sellTokensByPercentToBNB",
    "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```
