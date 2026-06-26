# AI 新闻驱动 BNB 策略交易 Skill (TypeScript, Node.js 20+)

> ⚠️ 高风险提示：本项目仅用于研究与示例。任何实盘交易都有资金损失风险。

## 功能概览

- 新闻摄取：REST 轮询（可扩展 WS）
- 信号：规则模型 + 可选 OpenAI 模型（失败自动降级）
- 策略：事件驱动买卖（WBNB <-> 稳定币）
- 风控：仓位、日损、交易次数、滑点、冷却、失败进入 SAFE_MODE
- 执行：1inch 报价与交易（支持 dry-run）
- CLI：`start | status | panic | revoke-approvals`

## 安装

```bash
npm install
cp .env.example .env
```

## 配置

关键项：

- `DRY_RUN=true`（默认）
- `NEWS_API_URL` 新闻 JSON 接口
- `EVM_PRIVATE_KEY` 或 `ENCRYPTED_KEY_PATH + KEY_PASSPHRASE`
- `ONEINCH_API_KEY`（建议配置）

## 私钥加密（推荐）

```bash
npm run key:encrypt -- --out ./secrets/key.json
```

然后设置：

- `EVM_PRIVATE_KEY=` 留空
- `ENCRYPTED_KEY_PATH=./secrets/key.json`
- `KEY_PASSPHRASE=你的口令`

## 运行

### Dry-run

```bash
npm run start -- start
```

### 状态

```bash
npm run start -- status
```

### 立即停机（panic）

```bash
npm run start -- panic
```

### 撤销授权

```bash
npm run start -- revoke-approvals
```

## 常见问题

1. `Missing key material`
   - 检查私钥或加密文件配置
2. `quote failed`
   - 检查 1inch API key、网络连通性、token 地址
3. 频繁 SAFE_MODE
   - 提高新闻源质量，降低交易频率，放宽阈值前先 dry-run 验证

## 默认地址

- WBNB: `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
- USDT(BSC): `0x55d398326f99059fF775485246999027B3197955`
- Pancake Router v2: `0x10ED43C718714eb63d5aA57B78B54704E256024E`
