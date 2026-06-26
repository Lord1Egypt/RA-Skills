---
name: dexscan-skill
description: >
  使用此技能获取链上市场数据：代币行情、牛人榜、社交热度、信号。

  **触发场景**：
  - 用户提到 dexscan
  - 用户提到代币行情、价格、市值、成交量、流动性、涨跌幅、持币地址数
  - 用户提到代币信号、首次信号推送最大涨幅、信号推送
  - 用户提到代币热度、热度排行榜、KOL讨论
  - 用户提到聪明钱、牛人榜
---

# DexScan 技能说明

## 目录结构

```
dexscan-skill/
├── SKILL.md              # 主技能文件（当前文件）
├── scripts/
│   └── dexscan.js        # API 调用脚本（get/post封装+签名认证）
├── references/
│   ├── signal.md         # 代币信号接口文档
│   ├── market.md         # 行情接口文档
│   ├── address.md        # 地址情况接口文档
│   ├── address-rank.md   # 地址牛人榜接口文档
│   └── heat.md           # 热度接口文档
└── assets/               # 资源文件目录
```

## API 调用方式

所有 API 调用通过 `scripts/dexscan.js` 导出的方法实现：

```javascript
const dexscan = require('./scripts/dexscan.js');

// 信号列表查询（游标分页）
await dexscan.querySignalList({ chainName: 'SOL' });
await dexscan.querySignalList({ chainName: 'SOL', cursor: { address: 'xxx', signalTime: 1234567890 } });

// 信号排行榜查询
await dexscan.querySignalRank({ chainName: 'SOL' });

// 行情模块 - 代币排行查询
await dexscan.queryCoinRank({ chainName: 'SOL', bar: '1h', page: 1, pageSize: 20 });

// 行情模块 - 交易活动列表
await dexscan.queryTradeScroll({ chainName: 'SOL', tokenContractAddress: 'xxx' });

// 地址情况模块 - 地址交易历史
await dexscan.queryAddressTradeScroll({ chainName: 'SOL', address: 'xxx' });

// 地址情况模块 - 地址盈亏分析
await dexscan.queryAddressList({ chainName: 'SOL', address: 'xxx' });
```

## 认证机制

API 请求头包含签名认证：
- `ACCESS-KEY`：
  - 操作系统环境变量（最高优先级）：`DS_ACCESS_KEY`，环境变量未设置时使用公用默认配置（低频限制，仅适用于轻量体验）
- `ACCESS-TIMESTAMP`：当前毫秒时间戳
- `ACCESS-SIGN`：`HMAC-SHA256(ACCESS-KEY + ":" + ACCESS-TIMESTAMP)` 的 Base64 编码

SECRET-KEY：
- 操作系统环境变量（最高优先级）：`DS_SECRET_KEY`，环境变量未设置时使用公用默认配置（低频限制，仅适用于轻量体验）

## 支持的链名称

必须使用以下链名称之一：`SOL, BSC, Base, ETH, Polygon, Arbitrum, Optimism, Avalanche, Monad, SUI`

## 通用行为规则

1. **语言**：始终以用户提问的语言回复
2. **链名称**：用户未指定链时默认使用 `SOL`；用户给出别称（如"以太坊"）时映射为对应链名（`ETH`）
3. **错误处理**：API 返回 `code !== 200` 时，展示 `msg` 字段内容，不展示空数据
4. **时间字段格式化**：响应数据中字段名含 `time` 或 `date`（不区分大小写）的字段，按客户端默认时区转换为 `yyyy-MM-dd HH:mm:ss` 展示；`cursor` 对象内的字段除外，保持原始值
5. **数值格式化**：
   - 价格：小数位超过16位时保留16位小数，截断多余位数
   - 金额/市值：`≥1B` 显示为 `xB`，`≥1M` 显示为 `xM`，`≥1K` 显示为 `xK`
   - 涨跌幅/收益率：转为百分比，保留2位小数，正值加 `+` 前缀（如 `+12.34%`）
   - 胜率/比例：转为百分比，保留1位小数
6. **分页提示**：响应包含 `cursor` 字段时提示"还有更多数据，如需继续请告知"；无 `cursor` 时提示"已显示全部数据"
7. **默认输出**：`data` 不为空时，必须按各模块文档定义的默认字段输出，不可省略；用户要求详细信息时输出完整字段

## 接口选择指引

| 用户意图 | 推荐接口 |
|----------|----------|
| 查代币信号/推送列表 | `querySignalList` |
| 查信号排行榜 | `querySignalRank` |
| 查代币行情排行 | `queryCoinRank` |
| 查代币详细信息、价格、市值、24h涨幅、24h成交额、符号、创建时间、流动性、持币地址数 | `queryCoinInfo` |
| 查代币近期统计 | `queryCoinSummary` |
| 查K线历史数据 | `queryKlineHistorical` |
| 查某代币的链上交易记录 | `queryTradeScroll` |
| 查某代币的流动性变化 | `queryLiquidScroll` |
| 查某代币的持仓盈亏 | `queryPnlCoinList` |
| 查开发者关联代币 | `queryDeveloperScroll` |
| 查Meme币排行 | `queryMemeRank` |
| 查Meme支持的DEX列表 | `queryMemeDexs` |
| 查某地址的交易历史 | `queryAddressTradeScroll` |
| 查某地址的盈亏分析 | `queryAddressList` |
| 查某地址的持仓资产 | `queryAddressAssetTop` |
| 查开发者创建的代币 | `queryDeveloperPage` |
| 查聪明钱/牛人榜 | `queryAddressRank` |
| 查社交热度排行 | `queryCoinHeatPage` |
| 查推文热度 | `queryTwitterTweetsHeat` |

## 模块接口文档

- **代币信号模块**：详见 [references/signal.md](references/signal.md)
  - 信号列表查询（分页，游标方式）
  - 信号排行榜查询（TOP10）
- **行情模块**：详见 [references/market.md](references/market.md)
  - 代币排行查询（coin-rank）
  - 交易活动列表（trade-scroll）
  - 流动性变化列表（liquid-scroll）
  - 代币盈利列表（pnl-coin-list）
  - 开发者代币列表（developer-scroll）
  - 代币统计信息（coin-summary）
  - 代币信息（coin-info）
  - K线历史数据（kline-historical）
  - Meme代币排行（meme-rank）
  - Meme支持DEX列表（meme-dexs）
- **地址情况模块**：详见 [references/address.md](references/address.md)
  - 地址交易历史（address-trade-scroll）
  - 地址盈亏分析（address-list）
  - 地址资产组合（address-asset-top）
  - 地址开发者代币（developer-page）
- **地址牛人榜模块**：详见 [references/address-rank.md](references/address-rank.md)
- **热度模块**：详见 [references/heat.md](references/heat.md)
  - 社交热度列表（coin-heat-page）
  - 推文热度数据（twitter-tweets-heat）