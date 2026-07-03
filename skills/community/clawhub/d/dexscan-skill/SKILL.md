---
name: dexscan-skill
description: >
  使用此技能获取链上市场数据：代币行情、代币信息、信号、社交热度、聪明钱地址。

  **触发场景**：
  - 用户提到 dexscan
  - 用户提到代币行情、价格、市值、成交量、流动性、涨跌幅、持币地址数
  - 用户提到代币信号、首次信号推送最大涨幅、信号推送
  - 用户提到代币热度、热度排行榜、KOL讨论
  - 用户提到聪明钱、牛人榜、地址盈亏
  - 用户提到搜索代币、搜索地址
---

# DexScan 技能说明

## 目录结构

```
dexscan-skill/
├── SKILL.md              # 主技能文件（当前文件）
├── .env                  # API 密钥配置文件
├── scripts/
│   └── dexscan.js        # API 调用脚本（get/post封装+签名认证）
├── references/
│   ├── coin.md           # 代币接口文档
│   ├── address.md        # 地址接口文档
│   └── market.md         # 行情接口文档
└── assets/               # 资源文件目录
```

## API 调用方式

所有 API 调用通过 `scripts/dexscan.js` 导出的方法实现：

```javascript
const dexscan = require('./scripts/dexscan.js');
await dexscan.queryCoinRankPage({ chainName: 'SOL', bar: '1h', page: 1, pageSize: 20 });
```

## 认证机制

API 请求头包含签名认证：
- `ACCESS-KEY`：
  - `.env` 文件配置（最高优先级）：`DS_ACCESS_KEY`，未配置时使用环境变量
- `ACCESS-TIMESTAMP`：当前毫秒时间戳
- `ACCESS-SIGN`：`HMAC-SHA256(ACCESS-KEY + ":" + ACCESS-TIMESTAMP)` 的 Base64 编码

SECRET-KEY：
- `.env` 文件配置（最高优先级）：`DS_SECRET_KEY`，未配置时使用环境变量

`.env` 文件位于 skill 工作目录下，格式示例：
```
DS_ACCESS_KEY = "your_access_key_here"
DS_SECRET_KEY = "your_secret_key_here"
```

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

### 代币接口

| 接口名称 | 用户意图                                                         | 推荐接口 |
|----------|--------------------------------------------------------------|----------|
| 代币排行 | 按时间粒度分页查询代币排行榜，支持成交额、流动性、涨跌幅、市值、交易笔数、持币地址数等多维过滤与排序           | `queryCoinRankPage` |
| 代币详情 | 查代币详细信息，包含代币名称、代币符号、创建者、流动性、代币价格、代币市值、总供应量、代币24h交易量、代币24h交易额 | `queryCoinInfo` |
| 代币信号列表 | 查询24小时信号，支持游标分页，每页返回20条，含代币价格、市值、信号评分、首次信号最大涨幅               | `queryCoinSignalScroll` |
| 信号排行榜 | 查询24小时信号排行榜 TOP10，基于首次信号最大涨幅降序，最新信号推送时间降序                    | `queryCoinSignalRank` |
| 开发者代币列表 | 查某代币的开发者创建的代币                                                | `queryCoinDeveloperScroll` |
| 代币搜索 | 通过关键字搜索代币或者地址                                                | `queryCoinSearch` |
| 社媒热度排行 | 社媒热度列表，含热度贡献 Top5 KOL、买入 Top5 KOL、24h 价格走势及推文 AI 总结          | `queryCoinHeatPage` |
| Meme币排行 | 查询meme币新创建、带发射、已发射的代币列表                                      | `queryCoinMemeRank` |
| Meme支持的DEX列表 | 查Meme支持的DEX列表                                                | `queryCoinMemeDexs` |
| 推文热度 | 查询指定推文 ID 的热度数据，包含浏览、回复、转发、点赞、热度贡献值                          | `queryCoinTwitterTweetsHeat` |

### 行情接口

| 接口名称 | 用户意图 | 推荐接口 |
|--------|----------|----------|
| 交易活动列表 | 游标分页查询指定代币的链上交易记录，返回买卖方向、交易金额、地址标签（KOL/DEV/TOP10等）及交易时间 | `queryMarketTradeScroll` |
| 流动性变化列表 | 游标分页查询指定代币的流动性增减事件，返回添加/移除流动性的金额、LP地址及操作时间/移除记录 | `queryMarketLiquidScroll` |
| 代币盈利列表 | 查询指定代币的持有者盈亏统计，返回各地址的买入成本、当前市值、已实现/未实现盈亏数据 | `queryMarketPnlCoinList` |
| 代币近期统计信息 | 查询代币各时间周期（5m/1h/4h/24h）的近期行情概要，包括价格、涨跌幅、成交量及 KOL 交易统计 | `queryMarketCoinSummary` |
| K线历史数据 | 查询代币指定时间粒度（1m/5m/1h/1d等）的K线历史数据，返回开高低收及成交量序列 | `queryMarketKlineHistorical` |
| 代币流动性池子列表 | 查询代币流动性最高的前20个池子，返回所属DEX、配对代币、流动性金额及24小时交易量 | `queryMarketPoolTop` |

### 地址接口

| 接口名称 | 用户意图 | 推荐接口 |
|----------|----------|----------|
| 地址交易历史 | 游标分页查询指定地址的链上交易记录，返回代币名称、买卖方向、交易金额、盈亏及交易时间 | `queryAddressTradeScroll` |
| 地址盈亏分析列表 | 分页查询指定地址持有的代币盈亏情况，返回买入均价、持仓量、已实现盈亏、未实现盈亏及盈亏比例 | `queryAddressPnlPage` |
| 地址资产组合列表 | 分页查询指定地址当前持有的代币资产，按持仓市值降序返回代币名称、数量、均价及当前价值 | `queryAddressAssetTop` |
| 地址开发者代币列表 | 分页查询指定开发者地址曾发行的代币列表，返回代币名称、发行时间、当前价格及涨跌幅 | `queryAddressDeveloperPage` |
| 聪明钱/牛人榜 | 分页查询链上盈利能力排名靠前的地址，基于已实现盈亏、胜率等指标综合排序，返回地址标签、交易统计及盈亏数据 | `queryAddressRankPage` |

## 模块接口文档

- **代币接口**：详见 [references/coin.md](references/coin.md)
  - 代币排行（rank-page）
  - 代币详情（info）
  - 代币信号列表（signal-scroll）
  - 代币信号排行榜（signal-rank）
  - 开发者代币列表（developer-scroll）
  - 搜索（search）
  - 社媒热度榜单（heat-page）
  - Meme代币排行（meme-rank）
  - Meme支持DEX列表（meme-dexs）
  - 推文热度数据（twitter-tweets-heat）
- **地址接口**：详见 [references/address.md](references/address.md)
  - 地址盈亏分析（pnl-page）
  - 地址资产组合（asset-top）
  - 地址交易历史（trade-scroll）
  - 地址开发者代币（developer-page）
  - 牛人榜（rank-page）
- **行情接口**：详见 [references/market.md](references/market.md)
  - 交易活动列表（trade-scroll）
  - 流动性变化列表（liquid-scroll）
  - 代币盈利列表（pnl-coin-list）
  - 代币近期统计（coin-summary）
  - K线历史数据（kline-historical）
  - 代币流动性池子列表（pool-top）
