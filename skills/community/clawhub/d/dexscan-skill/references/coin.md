# 代币接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 代币排行

**接口地址**: `POST /v3/coin/rank-page`

**接口描述**: 按指定排序维度（市值、涨幅、交易量等）查询代币排行榜，支持按链筛选与分页

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| bar | 时间周期（5m/1h/4h/24h） | true | string |
| chainName | 链名，如 SOL；传 ALL 查全链 | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |
| minValue | 成交额最小值（USD） | false | number |
| maxValue | 成交额最大值（USD） | false | number |
| minLiquid | 流动性最小值（USD） | false | number |
| maxLiquid | 流动性最大值（USD） | false | number |
| minPriceChange | 涨跌幅最小值 | false | number |
| maxPriceChange | 涨跌幅最大值 | false | number |
| minMarketCap | 市值最小值（USD） | false | number |
| maxMarketCap | 市值最大值（USD） | false | number |
| minTradeCount | 交易笔数最小值 | false | number |
| maxTradeCount | 交易笔数最大值 | false | number |
| minAddressCount | 独立交易地址数最小值 | false | number |
| maxAddressCount | 独立交易地址数最大值 | false | number |
| minHolderCount | 持仓人数最小值 | false | number |
| maxHolderCount | 持仓人数最大值 | false | number |
| minCreateTime | 代币创建时间下限（毫秒时间戳） | false | number |
| maxCreateTime | 代币创建时间上限（毫秒时间戳） | false | number |
| unit | 代币上线时长单位（YEAR/MONTH/DAY/HOUR/MINUTE） | false | string |
| minCreateDuration | 代币上线时长下限（配合 unit 使用） | false | number |
| maxCreateDuration | 代币上线时长上限（配合 unit 使用） | false | number |
| onlyMeme | 仅查询 Meme 代币，默认 false | false | boolean |
| hideHigh | 隐藏高风险代币，默认 false | false | boolean |
| hideStable | 隐藏稳定币，默认 false | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 代币排行列表 | array |
| -> chainName | 链名 | string |
| -> tokenContractAddress | 代币合约地址 | string |
| -> symbol | 代币符号 | string |
| -> uri | 项目链接 | string |
| -> icon | 代币图标 URL | string |
| -> createTime | 代币创建时间（毫秒） | string |
| -> totalSupply | 总供应量 | string |
| -> liquid | 流动性（USD） | string |
| -> holderCount | 持仓人数 | string |
| -> marketCap | 市值（USD） | string |
| -> bar | 时间周期 | string |
| -> windowStart | 统计窗口开始时间（毫秒） | string |
| -> windowEnd | 统计窗口结束时间（毫秒） | string |
| -> openPrice | 开盘价 | string |
| -> closePrice | 收盘价 | string |
| -> low | 最低价 | string |
| -> high | 最高价 | string |
| -> priceChange | 价格涨幅 | string |
| -> volume | 总成交量 | string |
| -> value | 总成交额（USD） | string |
| -> buyVolume | 买入量 | string |
| -> sellVolume | 卖出量 | string |
| -> buyValue | 买入额（USD） | string |
| -> sellValue | 卖出额（USD） | string |
| -> tradeCount | 总交易笔数 | string |
| -> buyTradeCount | 买入笔数 | string |
| -> sellTradeCount | 卖出笔数 | string |
| -> addressCount | 独立交易地址数 | string |
| -> buyAddressCount | 买入地址数 | string |
| -> sellAddressCount | 卖出地址数 | string |
| -> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 500,
        "list": [
            {
                "chainName": "SOL",
                "tokenContractAddress": "So11111111111111111111111111111111111111112",
                "symbol": "SOL",
                "uri": "https://solana.com",
                "icon": "https://static.dexscan.trade/...",
                "createTime": "1609459200000",
                "totalSupply": "555000000",
                "liquid": "5000000",
                "holderCount": "2000000",
                "marketCap": "80000000000",
                "bar": "1h",
                "windowStart": "1776118800000",
                "windowEnd": "1776122400000",
                "openPrice": "145.00",
                "closePrice": "147.50",
                "low": "144.50",
                "high": "148.20",
                "priceChange": "0.017",
                "volume": "950000",
                "value": "137750000",
                "buyVolume": "500000",
                "sellVolume": "450000",
                "buyValue": "72500000",
                "sellValue": "65250000",
                "buyTradeCount": "15000",
                "sellTradeCount": "13000",
                "tradeCount": "28000",
                "buyAddressCount": "8000",
                "sellAddressCount": "7000",
                "addressCount": "12000",
                "riskLevel": "LOW"
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：symbol, chainName, tokenContractAddress, priceChange, volume, value, marketCap, holderCount, riskLevel
- 详细信息：输出全部字段

---

## 2. 代币详情

**接口地址**: `POST /v3/coin/info`

**接口描述**: 查询单个代币的完整信息，包括基本信息、社交链接，市值、流动性、持仓分布及链上安全指标

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| chainName | 链名 | string |
| tokenContractAddress | 代币合约地址 | string |
| symbol | 代币符号 | string |
| name | 代币名称 | string |
| icon | 代币图标 URL | string |
| creator | 创建者地址 | string |
| createTime | 代币创建时间（毫秒） | string |
| totalSupply | 总供应量 | string |
| price | 当前价格（USD） | string |
| marketCap | 当前市值（USD） | string |
| liquid | 当前流动性（USD） | string |
| holderCount | 持仓人数 | string |
| volume24h | 24小时成交量 | string |
| value24h | 24小时成交额（USD） | string |
| priceChange24h | 24小时价格涨幅 | string |
| tradeCount24h | 24小时交易笔数 | string |
| creatorBalance | 创建者持仓比例 | string |
| top10BalanceSum | TOP10 地址合计持仓比例 | string |
| kolCount | KOL 持仓地址数 | number |
| newCount | 新地址持仓数 | number |
| riskTag | 风险信息 | object |
| -> address | 代币合约地址 | string |
| -> chainName | 链名 | string |
| -> level | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| -> riskTags | 风险标签列表 | array |
| --> id | 风险标签 ID | number |
| --> tag | 风险标签 | string |
| --> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| --> zhCn | 风险中文描述 | string |
| appendix | 附录信息 | object |
| -> telegram | Telegram 链接 | string |
| -> twitter | Twitter 主页链接 | string |
| -> website | 官方网站链接 | string |
| -> blog | Blog 链接 | string |
| -> whitepaper | 白皮书链接 | string |
| -> reddit | Reddit 链接 | string |
| -> slack | Slack 链接 | string |
| -> facebook | Facebook 链接 | string |
| -> github | Github 链接 | string |
| -> discord | Discord 链接 | string |
| -> email | 邮件地址 | string |
| -> btok | BTok 链接 | string |
| -> linkedin | LinkedIn 链接 | string |
| -> qq | QQ 链接 | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "chainName": "SOL",
        "tokenContractAddress": "So11111111111111111111111111111111111111112",
        "symbol": "SOL",
        "name": "Solana",
        "icon": "https://static.dexscan.trade/...",
        "creator": "CreatorAddr...",
        "createTime": "1609459200000",
        "totalSupply": "555000000",
        "price": "147.50",
        "marketCap": "80000000000",
        "liquid": "5000000",
        "holderCount": "2000000",
        "volume24h": "950000000",
        "value24h": "137750000000",
        "priceChange24h": "0.017",
        "tradeCount24h": "672000",
        "creatorBalance": "0",
        "top10BalanceSum": "55000000",
        "kolCount": 120,
        "newCount": 500,
        "riskTag": {
            "address": "So11111111111111111111111111111111111111112",
            "chainName": "SOL",
            "level": "LOW",
            "riskTags": []
        },
        "appendix": {
            "telegram": "https://t.me/example",
            "twitter": "https://twitter.com/example",
            "website": "https://example.com",
            "blog": null,
            "whitepaper": null,
            "reddit": null,
            "slack": null,
            "facebook": null,
            "github": null,
            "discord": null,
            "email": null,
            "btok": null,
            "linkedin": null,
            "qq": null
        }
    }
}
```

**输出规则**:
- 默认输出：symbol, name, price, marketCap, liquid, holderCount, priceChange24h, riskLevel
- 详细信息：输出全部字段，包含 riskTag、appendix

---

## 3. 代币信号列表

**接口地址**: `POST /v3/coin/signal-scroll`

**接口描述**: 基于链上交易行为与社媒热度生成代币评分信号，支持按链筛选，游标分页每页20条

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | false | string |
| cursor | 游标（首次不传，翻页传上次返回值） | false | object |
| -> address | 代币合约地址 | true | string |
| -> signalTime | 信号时间戳（毫秒） | true | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| cursor | 下一页游标，列表为空时为 null | object |
| -> address | 代币合约地址 | string |
| -> signalTime | 信号时间戳（毫秒） | number |
| list | 信号列表 | array |
| -> chainName | 链名 | string |
| -> address | 代币合约地址 | string |
| -> symbol | 代币符号 | string |
| -> name | 代币名称 | string |
| -> icon | 代币图标 URL | string |
| -> riskTag | 风险信息 | object |
| --> address | 代币合约地址 | string |
| --> chainName | 链名 | string |
| --> level | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| --> riskTags | 风险标签列表 | array |
| ---> id | 风险标签 ID | number |
| ---> tag | 风险标签 | string |
| ---> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| ---> zhCn | 风险中文描述 | string |
| -> top10BalanceSum | TOP10 地址持仓比例 | string |
| -> signalPrice | 最新信号推送时的价格 | string |
| -> signalMarketCap | 最新信号推送时的市值（USD） | string |
| -> signalHolder | 最新信号推送时的持仓人数 | string |
| -> price | 当前价格 | string |
| -> marketCap | 当前市值（USD） | string |
| -> holderCount | 当前持仓人数 | string |
| -> score | 最新信号评分 | number |
| -> maxPriceChange | 最新信号最大价格涨幅 | string |
| -> signalTime | 最新信号推送时间（毫秒） | number |
| -> totalSupply | 总供应量 | string |
| -> chartList | 图表数据 | array |
| --> time | 时间窗口时间戳（毫秒） | number |
| --> price | 时间窗口价格 | string |
| --> hot | 热力值 | string |
| --> tagInfo | 时间窗口成交额最大的 KOL 标签 | object |
| ---> address | 地址 | string |
| ---> name | 名称 | string |
| ---> url | 主页链接 | string |
| ---> icon | 头像 | string |
| ---> fans | 粉丝数 | number |
| ---> tag | 标签 | string |
| --> value | 时间窗口 KOL 最大成交额 | string |
| --> kolComment | 图表点触发评论的 KOL 信息 | object |
| ---> userId | 用户ID | string |
| ---> username | 用户名 | string |
| ---> url | 主页链接 | string |
| ---> icon | 头像 | string |
| ---> score | 评分 | string |
| --> signal | 是否为信号点 | boolean |
| -> hisList | 历史信号数据 | array |
| --> signalTime | 信号推送时间（毫秒） | number |
| --> score | 信号评分 | number |
| --> marketCap | 信号推送时市值（USD） | string |
| -> createTime | 代币创建时间（毫秒） | number |
| -> firstMaxPriceChange | 首次信号最大涨幅 | string |
| -> firstCreateTime | 首次信号推送时间（毫秒） | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": { "address": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump", "signalTime": 1776122402000 },
        "list": [{
            "chainName": "SOL",
            "address": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
            "symbol": "SOUL",
            "name": "Soulana",
            "icon": "https://static.dexscan.trade/images/logo/101-38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump.webp",
            "riskTag": {
                "address": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
                "chainName": "SOL",
                "level": "LOW",
                "riskTags": []
            },
            "top10BalanceSum": "0.12",
            "signalPrice": "0.000123",
            "signalMarketCap": "123000",
            "signalHolder": "500",
            "price": "0.000456",
            "marketCap": "456000",
            "holderCount": "800",
            "score": 85,
            "maxPriceChange": "2.71",
            "signalTime": 1776122402000,
            "totalSupply": "1000000000",
            "chartList": [],
            "hisList": [],
            "createTime": 1776000000000,
            "firstMaxPriceChange": "3.15",
            "firstCreateTime": 1776000000000
        }]
    }
}
```

**输出规则**:
- 默认输出：symbol, chainName, address, price, holderCount, marketCap, score, signalTime, firstMaxPriceChange
- 详细信息：输出全部字段，包含 riskTag、chartList、hisList
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 4. 代币信号排行榜

**接口地址**: `POST /v3/coin/signal-rank`

**接口描述**: 返回24小时内发出信号的代币TOP10排行，以首次信号触发后的最大涨幅降序排列

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |

**响应参数**（返回列表，最多10条）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| chainName | 链名 | string |
| address | 代币合约地址 | string |
| symbol | 代币符号 | string |
| name | 代币名称 | string |
| icon | 代币图标 URL | string |
| uri | 项目链接 | string |
| totalSupply | 总供应量 | string |
| marketCap | 当前市值（USD） | string |
| score | 信号评分 | number |
| maxPriceChange | 首次信号触发后最大涨幅 | string |
| signalTime | 最新信号时间（毫秒） | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [{
        "chainName": "SOL",
        "address": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
        "symbol": "SOUL",
        "name": "Soulana",
        "icon": "https://static.dexscan.trade/...",
        "uri": "https://soulana.io",
        "totalSupply": "1000000000",
        "marketCap": "456000",
        "score": 90,
        "maxPriceChange": "3.15",
        "signalTime": 1776122402000
    }]
}
```

**输出规则**:
- 默认输出：symbol, chainName, address, marketCap, score, maxPriceChange, signalTime
- 详细信息：输出全部字段

---

## 5. 开发者代币列表

**接口地址**: `POST /v3/coin/developer-scroll`

**接口描述**: 游标分页查询指定代币的开发者地址所创建的其他代币

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址（作为查询开发者来源） | true | string |
| size | 每次返回数量，默认 30 | false | number |
| cursor | 游标（创建时间戳毫秒，首次不传） | false | number |
| needStats | 是否返回开发者汇总统计，默认 false | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| cursor | 下一页游标（创建时间戳毫秒），列表为空时为 null | string |
| list | 开发者代币列表 | array |
| -> chainName | 链名 | string |
| -> tokenContractAddress | 代币合约地址 | string |
| -> symbol | 代币符号 | string |
| -> name | 代币名称 | string |
| -> icon | 代币图标 URL | string |
| -> creator | 创建者地址 | string |
| -> createTime | 代币创建时间（毫秒） | string |
| -> liquid | 流动性（USD） | string |
| -> totalSupply | 总供应量 | string |
| -> marketCap | 市值（USD） | string |
| -> holderCount | 持仓人数 | string |
| -> price | 当前价格 | string |
| -> volume24h | 24小时成交量 | string |
| -> value24h | 24小时成交额（USD） | string |
| -> priceChange24h | 24小时价格涨幅 | string |
| -> tradeCount24h | 24小时交易笔数 | string |
| -> appendix | 附录信息 | object |
| --> telegram | Telegram 链接 | string |
| --> twitter | Twitter 主页链接 | string |
| --> website | 官方网站链接 | string |
| --> blog | Blog 链接 | string |
| --> whitepaper | 白皮书链接 | string |
| --> reddit | Reddit 链接 | string |
| --> slack | Slack 链接 | string |
| --> facebook | Facebook 链接 | string |
| --> github | Github 链接 | string |
| --> discord | Discord 链接 | string |
| --> email | 邮件地址 | string |
| --> btok | BTok 链接 | string |
| --> linkedin | LinkedIn 链接 | string |
| --> qq | QQ 链接 | string |
| -> migrateFinished | 是否迁移完成 | boolean |
| -> migrateProgress | 迁移进度（0~1） | string |
| stats | 开发者汇总统计（needStats=true 时返回） | object |
| -> creator | 创建者地址 | string |
| -> sourceTime | 资金来源时间（毫秒） | string |
| -> sourceAddress | 资金来源地址 | string |
| -> total | 累计发币总数 | number |
| -> migrated | 已迁移数量 | number |
| -> nonMigrated | 未迁移数量 | number |
| -> topMarketCap | 市值最高代币（结构同 list 元素） | object |
| -> lastCreateCoin | 最新创建代币（结构同 list 元素） | object |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": "1776000000000",
        "list": [{
            "chainName": "SOL",
            "tokenContractAddress": "MeMeAB...",
            "symbol": "MEME",
            "name": "MemeToken",
            "icon": "https://...",
            "creator": "DevAddr...",
            "createTime": "1776000000000",
            "liquid": "50000",
            "totalSupply": "1000000000",
            "marketCap": "500000",
            "holderCount": "1200",
            "price": "0.0005",
            "volume24h": "1000000",
            "value24h": "25000",
            "priceChange24h": "0.15",
            "tradeCount24h": "5000",
            "appendix": {
                "telegram": "https://t.me/example",
                "twitter": "https://twitter.com/example",
                "website": "https://example.com",
                "blog": null,
                "whitepaper": null,
                "reddit": null,
                "slack": null,
                "facebook": null,
                "github": null,
                "discord": null,
                "email": null,
                "btok": null,
                "linkedin": null,
                "qq": null
            },
            "migrateFinished": true,
            "migrateProgress": "1.0"
        }],
        "stats": {
            "creator": "DevAddr...",
            "sourceTime": "1775990000000",
            "sourceAddress": "7BgBvyjrZX2...",
            "total": 5,
            "migrated": 3,
            "nonMigrated": 2
        }
    }
}
```

**输出规则**:
- 默认输出：symbol, chainName, tokenContractAddress, price, priceChange24h, marketCap, liquid, migrateFinished
- 详细信息：输出全部字段，包含 appendix、stats
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 6. 搜索

**接口地址**: `GET /v3/coin/search`

**接口描述**: 支持按代币名称或合约地址进行搜索

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| text | 搜索关键词，支持代币名称、代币符号、合约地址、钱包地址 | true | string |
| chainName | 链名过滤，如 SOL、BSC；不传则全链搜索 | false | string |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| coinList | 代币搜索结果列表，有结果时 addressList 为空 | array |
| -> chainName | 链名称 | string |
| -> symbol | 代币符号 | string |
| -> name | 代币名称 | string |
| -> tokenContractAddress | 代币合约地址 | string |
| -> icon | 代币图标 URL | string |
| -> uri | 项目链接 | string |
| -> creator | 创建者地址 | string |
| -> liquid | 当前流动性（USD） | string |
| -> volume24h | 24小时成交量 | string |
| -> value24h | 24小时成交额（USD） | string |
| -> priceChange24h | 24小时价格涨幅 | string |
| -> tradeCount24h | 24小时交易笔数 | string |
| -> totalSupply | 总供应量 | string |
| -> marketCap | 市值（USD） | string |
| -> holderCount | 持币地址数 | string |
| -> price | 当前价格（USD） | string |
| -> createTime | 代币创建时间（毫秒） | string |
| -> creatorBalance | 创建者持仓比例 | string |
| -> top10BalanceSum | TOP10 地址合计持仓比例 | string |
| -> kolCount | KOL 持仓地址数 | number |
| -> newCount | 新钱包地址数 | number |
| -> riskTag | 风险信息 | object |
| --> address | 代币合约地址 | string |
| --> chainName | 链名 | string |
| --> level | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| --> riskTags | 风险标签列表 | array |
| ---> id | 风险标签 ID | number |
| ---> tag | 风险标签 | string |
| ---> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| ---> zhCn | 风险中文描述 | string |
| -> appendix | 附录信息 | object |
| --> telegram | Telegram 链接 | string |
| --> twitter | Twitter 主页链接 | string |
| --> website | 官方网站链接 | string |
| --> blog | 博客链接 | string |
| --> whitepaper | 白皮书链接 | string |
| --> reddit | Reddit 链接 | string |
| --> slack | Slack 链接 | string |
| --> facebook | Facebook 链接 | string |
| --> discord | Discord 链接 | string |
| --> github | Github 链接 | string |
| --> email | 邮件 | string |
| --> btok | BTok 链接 | string |
| --> linkedin | LinkedIn 链接 | string |
| --> qq | QQ 链接 | string |
| addressList | 地址搜索结果列表，coinList 有结果时此列表为空 | array |
| -> address | 钱包地址 | string |
| -> chainName | 链名 | string |
| -> latestTime | 最近活跃时间（毫秒） | string |
| -> amount | 交易量（USD） | number |
| -> realizedPnl | 已实现利润（USD） | number |
| -> tagInfo | 地址标签信息 | object |
| --> address | 地址 | string |
| --> name | 名称 | string |
| --> url | 主页链接 | string |
| --> icon | 头像 | string |
| --> fans | 粉丝数 | number |
| --> tag | 标签类型 | string |

**响应示例（命中代币）**:

```json
{
    "code": 200,
    "data": {
        "coinList": [{
            "chainName": "SOL",
            "symbol": "SOL",
            "name": "Wrapped SOL",
            "tokenContractAddress": "So11111111111111111111111111111111111111112",
            "icon": "https://static.dexscan.trade/...",
            "creator": "CreatorAddr...",
            "liquid": "5000000",
            "volume24h": "950000000",
            "value24h": "137750000000",
            "priceChange24h": "0.017",
            "tradeCount24h": "672000",
            "totalSupply": "555000000",
            "marketCap": "80000000000",
            "holderCount": "2000000",
            "price": "147.50",
            "createTime": "1609459200000",
            "creatorBalance": "0",
            "top10BalanceSum": "55000000",
            "kolCount": 120,
            "newCount": 500,
            "riskTag": {
                "address": "So11111111111111111111111111111111111111112",
                "chainName": "SOL",
                "level": "LOW",
                "riskTags": []
            },
            "appendix": {
                "telegram": null,
                "twitter": "https://twitter.com/example",
                "website": "https://solana.com",
                "blog": null,
                "whitepaper": null,
                "reddit": null,
                "slack": null,
                "facebook": null,
                "discord": null,
                "github": null,
                "email": null,
                "btok": null,
                "linkedin": null,
                "qq": null
            }
        }],
        "addressList": []
    }
}
```

**响应示例（命中地址）**:

```json
{
    "code": 200,
    "data": {
        "coinList": [],
        "addressList": [
            {
                "address": "0xAbC123...",
                "chainName": "BSC",
                "latestTime": "1718000000000",
                "amount": 500000.00,
                "realizedPnl": 12300.50,
                "tagInfo": {
                    "address": "0xAbC123...",
                    "name": "SmartTrader",
                    "url": "https://twitter.com/example",
                    "icon": "https://example.com/avatar.png",
                    "fans": 8500,
                    "tag": "KOL"
                }
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：symbol, tokenContractAddress, price, marketCap, holderCount, priceChange24h
- 详细信息：输出全部字段，包含 riskTag、appendix

---

## 7. 社媒热度榜单

**接口地址**: `POST /v3/coin/heat-page`

**接口描述**: 查询代币的社交媒体热度数据，支持分页

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名（SOL/BSC） | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |
| heatDate | 热度日期（毫秒时间戳），不传返回最新 | false | number |
| onlyNewCoin | 仅展示新币，默认 false | false | boolean |
| onlyBlueChipCoin | 仅展示蓝筹币，默认 false | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 热度榜单列表 | array |
| -> chainName | 链名 | string |
| -> address | 代币合约地址 | string |
| -> symbol | 代币符号 | string |
| -> icon | 代币图标 URL | string |
| -> heatTime | 热度统计时间（毫秒） | number |
| -> displayHeat | 展示热度值 | number |
| -> heatRaw | 原始热度值 | number |
| -> heatEma | 平滑热度值（EMA） | number |
| -> heatChange | 热度变化量 | number |
| -> heatChangeRatio | 热度变化比例 | number |
| -> marketCap | 当前市值（USD） | number |
| -> priceChange24h | 24小时价格涨跌幅 | number |
| -> heatTopKol | 热度贡献前5 KOL 列表 | array |
| --> userId | 用户ID | string |
| --> username | 用户名 | string |
| --> twitterUrl | Twitter 主页地址 | string |
| --> twitterIcon | Twitter 头像 | string |
| -> buyTopKol | 交易买入前5 KOL 列表 | array |
| --> userId | 用户ID | string |
| --> username | 用户名 | string |
| --> twitterUrl | Twitter 主页地址 | string |
| --> twitterIcon | Twitter 头像 | string |
| -> priceTrend | 24小时价格走势数据点 | array |
| -> tweetIdList | 关联推文 ID 列表 | array |
| -> coinCreateTime | 代币创建时间（毫秒） | number |
| -> createTime | 热度记录创建时间（毫秒） | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 100,
        "list": [{
            "chainName": "SOL",
            "address": "So11111111111111111111111111111111111111112",
            "symbol": "SOL",
            "icon": "https://...",
            "heatTime": 1776122400000,
            "displayHeat": 9580.5,
            "heatRaw": 9200.0,
            "heatEma": 9400.0,
            "heatChange": 120.3,
            "heatChangeRatio": 0.013,
            "marketCap": 80000000000.0,
            "priceChange24h": 0.035,
            "heatTopKol": [],
            "buyTopKol": [],
            "priceTrend": [145.2, 146.5, 147.0],
            "tweetIdList": ["1234567890123456789"],
            "coinCreateTime": 1609459200000,
            "createTime": 1776122400000
        }]
    }
}
```

**输出规则**:
- 默认输出：address, symbol, displayHeat, heatChange, heatChangeRatio, marketCap, priceChange24h
- 详细信息：输出全部字段，包含 heatTopKol、buyTopKol、priceTrend

---

## 8. Meme代币排行

**接口地址**: `POST /v3/coin/meme-rank`

**接口描述**: 查询Meme平台代币排行，支持按新建(NEW_CREATION)、拉盘(PUMP)、完成(COMPLETED)类型筛选

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| type | 排行类型（NEW_CREATION/PUMP/COMPLETED） | true | string |
| dexs | 指定 DEX 名称列表，为空则查全部 | false | array |

**响应参数**（返回列表）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| chainName | 链名 | string |
| address | 代币合约地址 | string |
| symbol | 代币符号 | string |
| name | 代币名称 | string |
| icon | 代币图标 URL | string |
| uri | 代币元数据 URI | string |
| memeDex | 所属 Meme 平台 DEX 名称 | string |
| createTime | 代币创建时间（毫秒） | string |
| lastTransTime | 最近交易时间（毫秒） | string |
| totalSupply | 总供应量 | string |
| price | 当前价格 | string |
| marketCap | 当前市值（USD） | string |
| holderCount | 持仓人数 | string |
| migrateProgress | 迁移进度（0~1） | number |
| value1h | 1小时成交额（USD） | string |
| priceChange1h | 1小时价格涨幅 | string |
| buyTradeCount1h | 1小时买入次数 | string |
| sellTradeCount1h | 1小时卖出次数 | string |
| creatorBalance | 创建者持仓比例 | string |
| top10SumBalance | TOP10 地址合计持仓比例 | string |
| sniperSumBalance | 狙击手地址合计持仓比例 | string |
| kolSumBalance | KOL 地址合计持仓比例 | string |
| newSumBalance | 新地址合计持仓比例 | string |
| rankType | 排行类型（NEW_CREATION/PUMP/COMPLETED） | string |
| optionType | 操作类型 | string |
| createdOn | 发行平台标识 | string |
| twitter | Twitter 主页链接 | string |
| telegram | Telegram 群组链接 | string |
| website | 官方网站链接 | string |
| migrCnt | 开发者已迁移代币数量 | number |
| mintCnt | 开发者代币总数 | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [{
        "chainName": "SOL",
        "address": "MeMeAB...",
        "symbol": "MEME",
        "name": "MemeToken",
        "icon": "https://...",
        "uri": "https://...",
        "memeDex": "pump.fun",
        "createTime": "1776120000000",
        "lastTransTime": "1776122000000",
        "totalSupply": "1000000000",
        "price": "0.00005",
        "marketCap": "50000",
        "holderCount": "500",
        "migrateProgress": 0.6,
        "value1h": "25000",
        "priceChange1h": "0.25",
        "buyTradeCount1h": "200",
        "sellTradeCount1h": "150",
        "creatorBalance": "0.05",
        "top10SumBalance": "0.25",
        "sniperSumBalance": "0.1",
        "kolSumBalance": "0.15",
        "newSumBalance": "0.2",
        "rankType": "NEW_CREATION",
        "optionType": "CREATE",
        "createdOn": "pump",
        "twitter": "https://twitter.com/example",
        "telegram": "https://t.me/example",
        "website": "https://example.com",
        "migrCnt": 2,
        "mintCnt": 5
    }]
}
```

**输出规则**:
- 默认输出：symbol, chainName, address, price, marketCap, holderCount, rankType
- 详细信息：输出全部字段

---

## 9. Meme支持的DEX列表

**接口地址**: `POST /v3/coin/meme-dexs`

**接口描述**: 查询指定链上Meme模块当前支持的DEX名称列表

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |

**响应参数**:

返回 DEX 名称字符串列表。

**响应示例**:

```json
{
    "code": 200,
    "data": ["pump.fun", "moonshot", "boop.fun"]
}
```

**输出规则**:
- 输出全部字段

---

## 10. 推文热度数据

**接口地址**: `POST /v3/coin/twitter-tweets-heat`

**接口描述**: 根据推文ID集合批量查询推文的热度快照数据

**请求参数**:

请求体直接传推文 ID 的集合（`Set<number>`）：

```json
[1234567890123456789, 9876543210987654321]
```

**响应参数**（返回列表）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| snapshootTime | 快照采集时间（毫秒） | string |
| tweetId | 推文 ID | string |
| userId | 发推用户 ID | string |
| keyword | 关联关键词 | string |
| tweetText | 推文内容 | string |
| tweetTime | 推文发布时间（毫秒） | string |
| views | 浏览数 | number |
| replies | 回复数 | number |
| retweets | 转发数 | number |
| favorites | 点赞数 | number |
| bookmarks | 收藏数 | number |
| quotedTweetId | 引用的推文 ID | string |
| retweetedTweetId | 转发的原推文 ID | string |
| heatRaw | 热度贡献值 | number |
| calculateHeatRawTime | 热度计算时间（毫秒） | string |
| createdAt | 爬虫采集时间（毫秒） | string |
| updateTime | 数据更新时间（毫秒） | string |

**响应示例**:

```json
{
    "code": 200,
    "data": [{
        "snapshootTime": "1776122400000",
        "tweetId": "1234567890123456789",
        "userId": "987654321",
        "keyword": "SOL",
        "tweetText": "Bullish on Solana...",
        "tweetTime": "1776118400000",
        "views": 50000,
        "replies": 120,
        "retweets": 300,
        "favorites": 1500,
        "bookmarks": 80,
        "quotedTweetId": "",
        "retweetedTweetId": "",
        "heatRaw": 25.6,
        "calculateHeatRawTime": "1776122400000",
        "createdAt": "1776122400000",
        "updateTime": "1776122400000"
    }]
}
```

**输出规则**:
- 默认输出：tweetId, userId, tweetText, tweetTime, views, replies, retweets, favorites
- 详细信息：输出全部字段
