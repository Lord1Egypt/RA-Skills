---
name: aicoin-trading
description: "**CEX 中心化交易所**(Binance / OKX / Bybit / Bitget 等)的下单交易工具。严格规则:(1) 所有订单必须通过 node scripts/exchange.mjs create_order 执行,禁止写自定义代码下单 (2) create_order 分两步:第一次返回预览,展示给用户等确认,用户说确认后第二次加 confirmed=true 执行 (3) 禁止自动确认,禁止跳过预览 (4) 平仓必须用 close_position,禁止用 create_order 构建平仓单。Trigger 关键词: 'buy on okx', 'sell on binance', '在 OKX 买 BTC', '在 Binance 下单', '做多 BTC 永续', '杠杆做空 ETH', '平掉我的 SOL 仓位', 'CEX 下单', '现货买入', '合约开仓', '永续平仓', '止盈止损', 'long', 'short', 'leverage', '买', '卖', '下单', '做多', '做空', '开仓', '平仓', '平掉', '关仓'. **路由提示**: 用户说"链上 swap / Uniswap / DEX 买 PEPE / Solana 上买"是**链上 DEX 交易**,应走 `aicoin-onchain` 而不是本 skill. Hyperliquid 上的下单也走 aicoin-onchain(HL 是链上 perp DEX),不是这里. 本 skill **只**处理 CEX 现货 + 永续合约下单。"
metadata: { "openclaw": { "primaryEnv": "AICOIN_ACCESS_KEY_ID", "requires": { "bins": ["node"] }, "homepage": "https://www.aicoin.com/opendata", "source": "https://github.com/aicoincom/coinos-skills", "license": "MIT" } }
---

> **运行脚本**: 从 SKILL.md 所在目录运行 `node scripts/exchange.mjs <action>`. 三引擎(OpenClaw / Hermes / Claude Code)容器自动加载 skill, 直接 `cd` 到 skill 目录即可.

# AiCoin Trading — 下单专用

## ⛔ 铁律（违反任何一条都是严重错误）

1. **禁止写代码下单。** 不准写 `import ccxt`、`new ccxt.okx()`、`fetch("https://...")` 或任何自定义代码来下单。所有订单只能通过 `node scripts/exchange.mjs create_order` 执行。
2. **禁止自动确认。** `create_order` / `close_position` 第一次调用返回预览（含风险提示），你必须把预览完整展示给用户，等用户回复"确认"或"yes"后，才能第二次调用加 `"confirmed":"true"` 执行。
3. **禁止修改用户参数。** 余额不够就告诉用户，不准自动调整数量或杠杆。
4. **禁止主动平仓。** 除非用户明确要求。
5. **平仓必须用 `close_position`。** 禁止用 `create_order` 构建平仓单（容易开反向单）。
6. **杠杆 / 保证金模式改动必须先确认。** `set_trading_params` 和 `set_leverage` 不是只读操作 — 它们改交易所账户的合约配置，直接影响后续所有订单的保证金占用、爆仓价、强平距离。100x 杠杆和 5x 杠杆的爆仓距离差 20 倍，用户没明确说改之前不准 silent set。**调用前必须**：用自然语言告诉用户你准备把哪个交易所、哪个交易对的杠杆 / margin_mode 从什么改成什么、影响是什么，等用户回复"确认"或"yes"才能执行。

> **反例 ❌**：用户说"开 100x 多 BTC"，你不反问杠杆是不是写错了直接 `set_trading_params leverage=100` 然后下单 — 用户可能是口误想说 10x，100x 直接 silent 设了风险极高。
> **正确 ✅**：先回"100x 杠杆爆仓距离只有约 0.95%（不算手续费），BTC 一根 5 分钟 K 线就能扫掉。确认是 100x 还是想说 10x？"，等用户明确回答再 set。

## 下单流程（两步，不可跳过）

```
步骤1: node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap"}'
→ 返回预览（交易对、方向、数量、价格、杠杆、保证金、风险提示）
→ 你必须把所有字段展示给用户

步骤2: 用户确认后
node scripts/exchange.mjs create_order '{"exchange":"okx","symbol":"BTC/USDT:USDT","type":"market","side":"buy","amount":1,"market_type":"swap","confirmed":"true"}'
→ 实际下单
```

## 平仓流程（两步，不可跳过）

**平仓必须用 `close_position`，禁止用 `create_order` 手动构建平仓单（容易开反向单）。**

```
步骤1: node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap"}'
→ 返回所有持仓预览（交易对、方向、张数、盈亏）
→ 展示给用户

步骤2: 用户确认后
node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap","confirmed":"true"}'
→ 市价平掉所有持仓（自动 reduceOnly）

步骤3: 执行后必须验证 + 总结（不可省略）
node scripts/exchange.mjs positions '{"exchange":"okx","market_type":"swap"}'
→ 确认仓位已清空，然后用一句话告诉用户结果（平了什么、盈亏多少）
```
指定交易对只平部分：加 `"symbol":"BTC/USDT:USDT"`

> **为什么有步骤3**: close_position 的返回有时被 streaming 截断，用户看不到结果。多查一次 positions 既能确认平仓成功，又能把结论写进最终消息让用户看到。

## 下单前准备

| 步骤 | 命令 | 是否需要确认 |
|------|------|------------|
| 设置杠杆+保证金模式 | `node scripts/exchange.mjs set_trading_params '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"margin_mode":"isolated","market_type":"swap"}'` | **需要**（见铁律 #6） |
| 单独设杠杆 | `node scripts/exchange.mjs set_leverage '{"exchange":"okx","symbol":"BTC/USDT:USDT","leverage":10,"market_type":"swap"}'` | **需要**（见铁律 #6） |
| 查合约信息 | `node scripts/exchange.mjs markets '{"exchange":"okx","market_type":"swap","base":"BTC"}'` | 不需要（只读） |

**杠杆 / 保证金确认模板**（直接照抄换数字）：
> "我准备把 OKX BTC/USDT 永续杠杆改为 **{N}x**，margin_mode = **{isolated/cross}**。这会影响后续这个交易对所有订单的保证金占用和爆仓距离（{N}x 杠杆爆仓约 {1/N*100}% 不计手续费）。确认改吗？"

确认后再实际调 `set_trading_params` / `set_leverage`。如果用户说"算了"、"先别"、"我再想想"，**不要**调脚本。

## 其他命令

| 操作 | 命令 |
|------|------|
| 平仓（全部或指定） | `node scripts/exchange.mjs close_position '{"exchange":"okx","market_type":"swap"}'` — 加 `"symbol":"BTC/USDT:USDT"` 只平单个 |
| 取消订单 | `node scripts/exchange.mjs cancel_order '{"exchange":"okx","symbol":"BTC/USDT","order_id":"xxx"}'` |

## 数量

**合约自动换算：** amount 传用户说的币数量（如 0.01），脚本自动转张数。传整数则视为张数。
**用 USDT 金额下单：** 当用户说"用10U做多"或"花10 USDT开仓"，传 `cost=10`（USDT保证金金额），不要传 amount。脚本会根据当前价格、杠杆自动计算合约张数。
**现货：** amount = 币数量。

**格式：** 现货 `BTC/USDT`，合约 `BTC/USDT:USDT`，Hyperliquid 用 USDC: `BTC/USDC:USDC`。

**交易所：** Binance, OKX, Bybit, Bitget, Gate.io, HTX, Pionex, Hyperliquid。
