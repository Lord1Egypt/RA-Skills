# ATXSwap 技能

BSC 上 **ATXSwap** 智能体去中心化交换协议的技能包。同一份 `SKILL.md` 同时兼容以
**Claude Code** 和 **OpenClaw** 为代表的客户端，无需为不同客户端维护多份目录。

[**English**](./README.md)

- **GitHub**: https://github.com/agentswapx/skills
- **SDK (npm)**: [`atxswap-sdk`](https://www.npmjs.com/package/atxswap-sdk)
- **SDK 源码 / 文档**: [agentswapx/atxswap-sdk](https://github.com/agentswapx/atxswap-sdk)

项目背景与简要[团队介绍](https://docs.atxswap.com/zh/guide/team)见 ATXSwap 文档站（[English](https://docs.atxswap.com/guide/team)）。本文档说明技能能力与脚本用法。

## 能力范围

- 为当前技能实例创建单个钱包（**不支持导入已有私钥**）
- 查询 ATX 价格、余额、LP 仓位和 ERC20 代币信息
- 在 PancakeSwap V3 上买卖 ATX/USDT
- 预估自定义区间流动性、添加流动性、减仓、收手续费、销毁空仓位 NFT
- 转账 BNB、ATX、USDT 或任意 ERC20 代币

## 目录结构

```text
atxswap/
├── SKILL.md
├── README.md
├── README.zh.md
├── PUBLISH.md
├── CHANGELOG.md
├── .clawhubignore
├── .gitignore
├── package.json
└── scripts/
    ├── _helpers.js
    ├── wallet.js
    ├── query.js
    ├── swap.js
    ├── liquidity.js
    └── transfer.js
```

## 安装

### OpenClaw 安装

```bash
openclaw skills install atxswap
```

### Claude Code 安装

```bash
git clone https://github.com/agentswapx/skills.git
cd skills/atxswap && npm install
```

默认会使用内置的 6 个 BSC 公共 RPC 端点做 fallback。如需覆盖，可将
`BSC_RPC_URL` 设为单个地址或逗号分隔的多个地址（按从左到右的优先级回退）：

```bash
export BSC_RPC_URL="https://my-private-rpc.example.com,https://bsc-dataseed.bnbchain.org"
```

## 常用命令

```bash
cd skills/atxswap && node scripts/wallet.js list
cd skills/atxswap && node scripts/query.js price
cd skills/atxswap && node scripts/query.js quote buy 1
cd skills/atxswap && node scripts/query.js positions <address> <tokenId>
cd skills/atxswap && node scripts/liquidity.js quote-add usdt 0.1 --range-percent 20
```

在支持 `${SKILL_DIR}` 注入的运行时中，建议使用 `cd "${SKILL_DIR}"`，以便技能
能在客户端管理的任意安装目录下正常运行。

## 流动性预估

做自定义区间流动性时，不要在对话里直接猜另一边代币数量。建议先预估，再执行写入：

```bash
cd "${SKILL_DIR}" && node scripts/liquidity.js quote-add usdt 0.1 --range-percent 20
cd "${SKILL_DIR}" && node scripts/liquidity.js add --base-token usdt --amount 0.1 --range-percent 20 --from <address>
```

支持的区间模式：

- `--range-percent <n>`：以当前 ATX 价格为中心展开，例如 `20` 表示 `-20% ~ +20%`
- `--min-price <p> --max-price <p>`：显式指定 `1 ATX = 多少 USDT`
- `--tick-lower <n> --tick-upper <n>`：直接指定 V3 tick

推荐流程：

1. 先执行 `query.js price` 或 `liquidity.js quote-add`
2. 把返回的 `estimatedAmounts` 展示给用户
3. 等用户确认
4. 再执行 `liquidity.js add`

## 手续费预览

收手续费前，先预览目标仓位：

```bash
cd "${SKILL_DIR}" && node scripts/query.js positions <address> <tokenId>
cd "${SKILL_DIR}" && node scripts/liquidity.js collect <tokenId> --from <address>
```

`query.js positions` 会根据流动性 L、价格区间与当前池价计算 **仓内代币约数**（**`principalAtx`** / **`principalUsdt`**、`principal0`/`principal1`，与前端 `getAmountsForLiquidity` 同源）；并给出 **`priceRangeUsdtPerAtx`**（区间内 USDT/ATX）、**`currentPriceUsdtPerAtx`**、**`currentPriceInRange`**；待收 **`pendingFees`**（`atx`、`usdt`），以及链上 `tokensOwed*` 与 `collectable*`。说明「头寸里有多少币」时请引用 **`principal*`**；说明区间与现价用价格字段而非 tick；判断是否值得收割时优先看 **`pendingFees`** / **`collectable*`**。

`liquidity.js remove <tokenId> <percent>` 现在本身就会发起一笔链上 `multicall`：
`decreaseLiquidity` -> `collect` -> 且当 `percent = 100` 时再 `burn`。
也就是说，100% 移除会在销毁 NFT 前自动收走当前可提取资金。若 `remove ... 100` 已成功，再对同一个
`tokenId` 执行 `collect` 报错是预期行为，因为该头寸 NFT 已不存在。

## 安全规则

1. 不要在聊天输出中暴露私钥或密码。
2. 所有写操作前，必须先预览价格、报价、余额或仓位。
3. 交换、转账、流动性操作前，必须等待用户明确确认。
4. 所有写操作都按主网真实资产处理。
5. 删除钱包前，必须先要求用户导出并备份加密 keystore。
6. 删除钱包还需要第二次确认：用户必须明确发送 `force delete wallet`。
7. 转账时，必须把 `(资产, from, to, amount)` 作为一笔唯一转账意图来处理，并在执行前完整复述给用户确认。
8. 一旦转账命令已经返回 `txHash`，就视为这笔转账已经发出；除非用户明确要求“再转一次”，否则不能对同一笔转账自动重复发送。
9. 如果转账执行处于不确定状态，例如 RPC 超时、网络中断、命令输出不完整但可能已经签名/广播，不能盲目重试；必须先查链上状态或余额变化，再让用户确认是否重试。
10. 用户询问“当前余额”“现在还有多少币”“当前 LP 持仓”“待收手续费”“还剩多少 ATX”这类现时状态时，必须先重新查询链上最新数据，不能直接复用聊天里之前的结果、缓存值或记忆中的数字。

## 防重复转账

为避免重复转账，建议固定执行下面的最小流程：

1. 先查余额或钱包状态
2. 明确展示 `(资产, from, to, amount)`
3. 等用户对这组参数明确确认
4. 只执行一次转账命令
5. 返回 `txHash`
6. 如果用户再次发出相同请求，先确认他们是否真的要再转一笔，而不是引用上一次结果

## 实时查询约束

涉及下面这些问题时，必须先查链上再回答：

- 钱包余额
- ATX / USDT 持仓
- LP NFT 仓位
- 仓位里的 `principalAtx` / `principalUsdt`
- 待收手续费
- 当前池价、报价

推荐约束：

1. 余额问题先跑 `query.js balance`
2. LP / 持仓问题先跑 `query.js positions`
3. 价格问题先跑 `query.js price`
4. 报价问题先跑 `query.js quote`
5. 如果查询失败，要明确说明“本次未能刷新链上最新数据”，不能拿旧结果顶替

## 删除钱包

只有在以下两个条件都满足后，才能删除钱包：

1. 用户已明确确认加密 keystore 备份完成
2. 用户已明确发送 `force delete wallet`

然后再执行：

```bash
cd "${SKILL_DIR}" && node scripts/wallet.js delete <address> --backup-confirmed yes --force-phrase "force delete wallet"
```
