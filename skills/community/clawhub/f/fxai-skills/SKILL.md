---
name: fxai-skill
displayName: FXAI
version: 1.0.3
description: 创建 V5 代币（USDT/BNB 池子可选，0税或税收四档）；支持 USDT/BNB 买入，按数量或按比例卖出到 USDT/BNB。说「FXAI」触发。依赖 BNB Chain MCP，且 MCP env 中必须配置 PRIVATE_KEY。
---

# FXAI：创建代币与买卖（USDT / BNB）

当用户输入「**FXAI**」时触发本技能。技能通过 FlapSkill 合约支持：
- 创建 V5 代币（创建时可选 **USDT 池子** 或 **BNB 池子**）
- 买入目标代币（`USDT` 或 `BNB`）
- 卖出目标代币并换回（`USDT` 或 `BNB`）
- 按比例卖出（可换回 `USDT` 或 `BNB`）

**FlapSkill 合约地址**：`0x8f059fEb5f34031EfFA024e9EB8C9968BfFE516a`  
**USDT（BSC）**：`0x55d398326f99059fF775485246999027B3197955`  
**前置要求**：已配置 [BNB Chain MCP](https://docs.bnbchain.org/showcase/mcp/skills/) 且 MCP `env` 中必须存在 `PRIVATE_KEY`，否则无法发送任何链上交易。

**外部上传说明**：执行 `scripts/upload-token-meta.js` 时，会把你提供的本地图片文件与简介、官网等元数据上传到 Flap API `https://funcs.flap.sh/api/upload`，用于生成创建代币所需的 `_meta` CID。

---

## 1. 创建代币

### 1.1 函数

- `createToken(...)`：选择创建不同的池子
- `createTokenWithQuote(..., _quoteMode)`：可选池子
  - `_quoteMode=0` -> USDT
  - `_quoteMode=1` -> BNB

### 1.2 规则

- 0税：`_taxRate=0`，分配参数都填 `0`，`salt` 用 8888。
- 有税：`_taxRate` 范围 `1~1000`（3%=300）；`_mktBps + _dividendBps + _deflationBps + _lpBps = 10000`；`salt` 用 7777。
- 若 `_dividendBps > 0`，`_minimumShareBalance >= 10_000 ether`。

### 1.3 `_meta` 与 `_salt`

在技能目录执行：
- `node scripts/upload-token-meta.js <图片路径> "<简介>" "<官网>" [twitter] [telegram]`
- `node scripts/find-vanity-salt.js 8888`（0税）
- `node scripts/find-vanity-salt.js 7777` 或 `node scripts/find-vanity-salt.js 7777 v2`（有税）

注意：
- `upload-token-meta.js` 会读取本地图片并上传到 `https://funcs.flap.sh/api/upload`
- `find-vanity-salt.js` 仅在本地计算 `_salt`，不会上传私钥
- 若依赖未安装，先执行 `npm install`

### 1.4 MCP 调用

`write_contract`：
- `contractAddress`: `0x8f059fEb5f34031EfFA024e9EB8C9968BfFE516a`
- `abi`: 见 [references/contract-abi.md](references/contract-abi.md)
- `network`: `bsc`

创建 USDT 池子（兼容旧流程）：
- `functionName`: `createToken`
- `args`: `[_name, _symbol, _meta, _feeTo, _salt, _taxRate, _mktBps, _dividendBps, _deflationBps, _lpBps, _minimumShareBalance]`

创建 BNB 池子（默认）或显式选择池子：
- `functionName`: `createTokenWithQuote`
- `args`: `[_name, _symbol, _meta, _feeTo, _salt, _taxRate, _mktBps, _dividendBps, _deflationBps, _lpBps, _minimumShareBalance, _quoteMode]`

---

## 2. 买入

### 2.1 用 USDT 买入

1. 先授权 USDT（`approve_token_spending`）
- `tokenAddress`: `0x55d398326f99059fF775485246999027B3197955`
- `spenderAddress`: `0x8f059fEb5f34031EfFA024e9EB8C9968BfFE516a`
- `amount`: 人类可读数量（如 `"10"`）

2. 调用：
- `functionName`: `buyTokensByUSDT`
- `args`: `[_token, _usdtAmountWei]`

### 2.2 用 BNB 买入

调用：
- `functionName`: `buyTokensByBNB`
- `args`: `[_token]`
- `value`: BNB 数量（由交易 value 传入）

---

## 3. 卖出

### 3.1 按数量卖出

先授权目标代币给 FlapSkill，再调用：
- 换 USDT：`sellTokensToUSDT(_token, _tokenAmount)`
- 换 BNB：`sellTokensToBNB(_token, _tokenAmount)`

### 3.2 按比例卖出

`_percentBps`：`10000=100%`，`5000=50%`，`1000=10%`。

先授权目标代币给 FlapSkill，再调用：
- 换 USDT：`sellTokensByPercentToUSDT(_token, _percentBps)`
- 换 BNB：`sellTokensByPercentToBNB(_token, _percentBps)`

---

## 4. 对话示例

创建 BNB 池子：

```text
FXAI 创建代币
名称：AAA
符号：AAA
池子：BNB
税点：3%
税收地址：0x...
营销税点：40%
持币分红税点：30%
回购销毁税点：20%
LP回流税点：10%
最低持币数量：10000
```

买入示例：
- `FXAI 买入 50 U 0x代币地址`
- `FXAI 买入 0.2 BNB 0x代币地址`

卖出示例：
- `FXAI 卖出 10000 代币 到 USDT 0x代币地址`
- `FXAI 按比例卖出 30% 到 BNB 0x代币地址`

---

## 5. 参考

- ABI：[references/contract-abi.md](references/contract-abi.md)
- 脚本：`scripts/upload-token-meta.js`、`scripts/find-vanity-salt.js`
- BNB Chain MCP: [BNB Chain Skills](https://docs.bnbchain.org/showcase/mcp/skills/)
