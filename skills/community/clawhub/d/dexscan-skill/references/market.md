# 行情接口

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
- 详细信息：输出全部字段，包含 tagInfo、riskTag、stats 等嵌套数据

---

## 2. 代币详情

**接口地址**: `POST /v3/coin/info`

**接口描述**: 查询单个代币的完整信息，包括基本信息、社交链接、市值、流动性、持仓分布及链上安全指标

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
| --> riskLevel | 风险等级 | string |
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
            "website": "https://example.com"
        }
    }
}
```

**输出规则**:
- 默认输出：symbol, name, price, marketCap, liquid, holderCount, priceChange24h, riskLevel
- 详细信息：输出全部字段，包含 tagInfo、riskTag、appendix、stats 等嵌套数据

---

## 3. 交易活动列表

**接口地址**: `POST /v3/market/trade-scroll`

**接口描述**: 游标分页查询指定代币的链上交易记录，返回买卖方向、交易金额、地址标签（KOL/DEV/TOP10等）及交易时间

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| swapTypes | 交易类型列表（1-买入，2-卖出） | false | array |
| minValue | 成交额最小值（USD） | false | number |
| maxValue | 成交额最大值（USD） | false | number |
| address | 过滤指定钱包地址 | false | string |
| begin | 起始时间（毫秒时间戳） | false | number |
| end | 结束时间（毫秒时间戳） | false | number |
| dexEnum | DEX 类型枚举值 | false | number |
| timeDesc | 是否按时间倒序，默认 true | false | boolean |
| size | 每次返回数量，默认 50 | false | number |
| cursor | 游标（首次不传，翻页传上次返回值） | false | object |
| -> blockTime | 上次最后一条交易的区块时间（yyyy-MM-dd HH:mm:ss） | false | string |
| -> blockHeight | 上次最后一条交易的区块高度 | false | string |
| -> transIndex | 上次最后一条交易的 EVENT 索引 | false | number |
| -> instIndex | 上次最后一条交易的指令索引 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| cursor | 下一页游标 | object |
| -> blockTime | 区块时间（yyyy-MM-dd HH:mm:ss） | string |
| -> blockHeight | 区块高度 | string |
| -> transIndex | EVENT 索引 | number |
| -> instIndex | 指令索引 | number |
| list | 交易记录列表 | array |
| -> address | 钱包地址 | string |
| -> baseAddress | 代币合约地址 | string |
| -> baseSymbol | 代币符号 | string |
| -> baseAmount | 代币成交数量 | string |
| -> quoteAddress | 计价代币地址 | string |
| -> quoteSymbol | 计价代币符号 | string |
| -> quoteAmount | 计价代币数量 | string |
| -> blockTime | 区块时间（毫秒） | string |
| -> blockHeight | 区块高度 | string |
| -> transIndex | EVENT 索引 | number |
| -> instIndex | 指令索引 | number |
| -> transHash | 交易哈希 | string |
| -> swapType | 交易类型（1-买入，2-卖出） | number |
| -> price | 成交价格 | string |
| -> value | 成交额（USD） | string |
| -> dexEnum | DEX 枚举值 | number |
| -> dexAddress | DEX 地址 | string |
| -> poolAddress | 池子地址 | string |
| -> tagInfo | 地址标签信息 | object |
| --> address | 地址 | string |
| --> name | 名称 | string |
| --> url | 主页链接 | string |
| --> icon | 头像 | string |
| --> fans | 粉丝数 | number |
| --> tag | 标签 | string |
| -> tags | 交易标签集合（DEV/KOL/TOP10/SNIPER/NEW） | array |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": "2026-04-14 10:00:00",
            "transIndex": 5,
            "instIndex": 0
        },
        "list": [
            {
                "address": "7BgBvyjrZX1...",
                "baseAddress": "So11111111111111111111111111111111111111112",
                "baseSymbol": "SOL",
                "baseAmount": "10.5",
                "quoteAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "quoteSymbol": "USDC",
                "quoteAmount": "1522.5",
                "blockTime": "1776122400000",
                "blockHeight": "320000000",
                "transIndex": 5,
                "instIndex": 0,
                "transHash": "5UcRj...",
                "swapType": 1,
                "price": "145.00",
                "value": "1522.5",
                "dexEnum": 1,
                "dexAddress": "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc",
                "poolAddress": "HJPjoW...",
                "tagInfo": null,
                "tags": ["KOL"]
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：blockTime, swapType, address, baseSymbol, baseAmount, price, value, tags
- 详细信息：输出全部字段，包含 tagInfo、riskTag 等嵌套数据
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 4. 流动性变化列表

**接口地址**: `POST /v3/market/liquid-scroll`

**接口描述**: 游标分页查询指定代币的流动性增减事件，返回添加/移除流动性的金额、LP地址及操作时间

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| swapTypes | 操作类型（1-添加，2-移除） | false | array |
| minValue | 操作金额最小值（USD） | false | number |
| maxValue | 操作金额最大值（USD） | false | number |
| address | 过滤指定 LP 地址 | false | string |
| begin | 起始时间（毫秒时间戳） | false | number |
| end | 结束时间（毫秒时间戳） | false | number |
| dexEnum | DEX 类型枚举值 | false | number |
| timeDesc | 是否按时间倒序，默认 true | false | boolean |
| size | 每次返回数量，默认 50 | false | number |
| cursor | 游标（首次不传，翻页传上次返回值） | false | object |
| -> blockTime | 上次最后一条记录的区块时间（yyyy-MM-dd HH:mm:ss） | false | string |
| -> blockHeight | 上次最后一条记录的区块高度 | false | string |
| -> transIndex | 上次最后一条记录的 EVENT 索引 | false | number |
| -> instIndex | 上次最后一条记录的指令索引 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| cursor | 下一页游标 | object |
| -> blockTime | 区块时间（yyyy-MM-dd HH:mm:ss） | string |
| -> blockHeight | 区块高度 | string |
| -> transIndex | EVENT 索引 | number |
| -> instIndex | 指令索引 | number |
| list | 流动性变化列表 | array |
| -> address | LP 操作地址 | string |
| -> blockTime | 操作时间（毫秒） | string |
| -> blockHeight | 区块高度 | string |
| -> transIndex | EVENT 索引 | number |
| -> instIndex | 指令索引 | number |
| -> transHash | 交易哈希 | string |
| -> swapType | 操作类型（1-添加，2-移除） | number |
| -> dexEnum | DEX 枚举值 | number |
| -> dexName | DEX 名称 | string |
| -> dexIcon | DEX 图标 URL | string |
| -> dexAddress | DEX 地址 | string |
| -> poolAddress | 池子地址 | string |
| -> value | 操作金额（USD） | string |
| -> tokens | 涉及代币列表 | array |
| --> tokenContractAddress | 代币合约地址 | string |
| --> symbol | 代币符号 | string |
| --> amount | 数量 | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": "2026-04-14 10:00:00",
            "transIndex": 2,
            "instIndex": 0
        },
        "list": [
            {
                "address": "7BgBvyjrZX1...",
                "blockTime": "1776122400000",
                "blockHeight": "320000000",
                "transIndex": 2,
                "instIndex": 0,
                "transHash": "3RkTj...",
                "swapType": 1,
                "dexEnum": 1,
                "dexName": "Raydium",
                "dexIcon": "https://...",
                "dexAddress": "routeUGWgWzqBWFcrCfv8tritsqukccJPu3q5GPP3xS",
                "poolAddress": "HJPjoW...",
                "value": "10000",
                "tokens": [
                    {
                        "tokenContractAddress": "So11111111111111111111111111111111111111112",
                        "symbol": "SOL",
                        "amount": "68.97"
                    },
                    {
                        "tokenContractAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                        "symbol": "USDC",
                        "amount": "10000"
                    }
                ]
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：blockTime, swapType, address, value, tokens（含 symbol、amount）
- 详细信息：输出全部字段
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 5. 代币盈利列表

**接口地址**: `POST /v3/market/pnl-coin-list`

**接口描述**: 查询指定代币的持有者盈亏统计，返回各地址的买入成本、当前市值、已实现/未实现盈亏数据

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| type | 地址标签筛选（DEV/KOL/TOP10/SNIPER/NEW） | false | string |
| holderList | 是否只查持仓中地址，默认 false | false | boolean |
| addresses | 批量钱包地址列表，最多10个 | false | array |

**响应参数**（返回列表）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| address | 钱包地址 | string |
| baseAddress | 代币合约地址 | string |
| chainName | 链名 | string |
| symbol | 代币符号 | string |
| icon | 代币图标 URL | string |
| beginTime | 首次买入时间（毫秒） | string |
| latestBeginTime | 最近一次买入时间（毫秒） | string |
| latestTime | 最近交易时间（毫秒） | string |
| buyAmount | 累计买入数量 | number |
| buyAmountDeposit | 累计买入数量（含划入） | number |
| buyValue | 累计买入额（USD） | number |
| buyValueDeposit | 累计买入额（含划入，USD） | number |
| buyNumber | 买入次数 | number |
| sellAmount | 累计卖出数量 | number |
| sellValue | 累计卖出额（USD） | number |
| sellNumber | 卖出次数 | number |
| buyAvgPrice | 买入均价 | number |
| sellAvgPrice | 卖出均价 | number |
| price | 当前价格 | number |
| balance | 当前持仓数量 | number |
| totalSupply | 总供应量 | number |
| nativeBalance | 原生代币余额 | number |
| balanceValue | 当前持仓市值（USD） | number |
| realizedPnl | 已实现盈亏（USD） | number |
| unrealizedPnl | 未实现盈亏（USD） | number |
| totalPnl | 总盈亏（USD） | number |
| realizedPnlRatio | 已实现盈亏比例 | number |
| unrealizedPnlRatio | 未实现盈亏比例 | number |
| totalPnlRatio | 总盈亏比例 | number |
| holdingPeriod | 持仓时长（毫秒） | string |
| sourceAddress | 资金来源地址 | string |
| sourceTime | 资金来源时间（毫秒） | string |
| riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| tags | 地址标签集合（DEV/KOL/TOP10/SNIPER/NEW） | array |
| tagInfo | 地址标签信息 | object |
| -> address | 地址 | string |
| -> name | 名称 | string |
| -> url | 主页链接 | string |
| -> icon | 头像 | string |
| -> fans | 粉丝数 | number |
| -> tag | 标签 | string |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "address": "7BgBvyjrZX1...",
            "baseAddress": "So11111111111111111111111111111111111111112",
            "chainName": "SOL",
            "symbol": "SOL",
            "beginTime": "1776000000000",
            "latestTime": "1776122400000",
            "buyAmount": 100.0,
            "buyValue": 14500.0,
            "buyNumber": 3,
            "sellAmount": 50.0,
            "sellValue": 7500.0,
            "sellNumber": 2,
            "buyAvgPrice": 145.0,
            "price": 147.5,
            "balance": 50.0,
            "balanceValue": 7375.0,
            "realizedPnl": 250.0,
            "unrealizedPnl": 375.0,
            "totalPnl": 625.0,
            "realizedPnlRatio": 0.034,
            "holdingPeriod": "122400000",
            "riskLevel": "NONE",
            "tags": ["KOL"],
            "tagInfo": null
        }
    ]
}
```

**输出规则**:
- 默认输出：address, symbol, balance, balanceValue, buyValue, sellValue, realizedPnl, realizedPnlRatio, totalPnl, totalPnlRatio, tags
- 详细信息：输出全部字段，包含 tagInfo、riskTag 等嵌套数据

---

## 6. 开发者代币列表

**接口地址**: `POST /v3/coin/developer-scroll`

**接口描述**: 游标分页查询指定代币的开发者地址所创建的其他代币，返回代币名称、创建时间、涨跌幅等信息

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
        "list": [
            {
                "chainName": "SOL",
                "tokenContractAddress": "MeMeAB...",
                "symbol": "MEME",
                "name": "MemeToken",
                "creator": "DevAddr...",
                "createTime": "1776000000000",
                "liquid": "50000",
                "marketCap": "500000",
                "holderCount": "1200",
                "price": "0.0005",
                "value24h": "25000",
                "priceChange24h": "0.15",
                "appendix": {
                    "telegram": "https://t.me/example",
                    "twitter": "https://twitter.com/example",
                    "website": "https://example.com"
                },
                "migrateFinished": true,
                "migrateProgress": "1.0"
            }
        ],
        "stats": {
            "creator": "DevAddr...",
            "total": 5,
            "migrated": 3,
            "nonMigrated": 2
        }
    }
}
```

**输出规则**:
- 默认输出：symbol, chainName, tokenContractAddress, price, priceChange24h, marketCap, liquid, creatorBalance, migrateFinished
- 详细信息：输出全部字段，包含 appendix、migrateProgress 等嵌套数据
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 7. 代币近期统计信息

**接口地址**: `POST /v3/market/coin-summary`

**接口描述**: 查询代币各时间周期（5m/1h/4h/24h）的近期行情概要，包括价格、涨跌幅、成交量及 KOL 交易统计

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |

**响应参数**（返回列表，每个时间周期一条记录）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| chainName | 链名 | string |
| tokenContractAddress | 代币合约地址 | string |
| bar | 统计时间粒度（5m/1h/4h/24h） | string |
| windowStart | 统计窗口开始时间（毫秒） | string |
| openPrice | 开盘价 | string |
| closePrice | 收盘价 | string |
| low | 最低价 | string |
| high | 最高价 | string |
| priceChange | 价格涨幅 | string |
| volume | 总成交量 | string |
| value | 总成交额（USD） | string |
| buyVolume | 买入量 | string |
| sellVolume | 卖出量 | string |
| buyValue | 买入额（USD） | string |
| sellValue | 卖出额（USD） | string |
| tradeCount | 总交易笔数 | string |
| buyTradeCount | 买入笔数 | string |
| sellTradeCount | 卖出笔数 | string |
| addressCount | 总交易地址数 | string |
| buyAddressCount | 买入地址数 | string |
| sellAddressCount | 卖出地址数 | string |
| valueKol | KOL 成交额（USD） | number |
| buyValueKol | KOL 买入成交额（USD） | number |
| sellValueKol | KOL 卖出成交额（USD） | number |
| buyAddressKol | KOL 买入地址数 | number |
| sellAddressKol | KOL 卖出地址数 | number |
| totalAddressKol | KOL 总地址数 | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "chainName": "SOL",
            "tokenContractAddress": "So11111111111111111111111111111111111111112",
            "bar": "1h",
            "windowStart": "1776118800000",
            "openPrice": "145",
            "closePrice": "147.5",
            "low": "144.5",
            "high": "148.2",
            "priceChange": "0.017",
            "volume": "950000",
            "value": "137750000",
            "buyVolume": "600000",
            "sellVolume": "350000",
            "buyValue": "87000000",
            "sellValue": "50750000",
            "tradeCount": "28000",
            "buyTradeCount": "15000",
            "sellTradeCount": "13000",
            "addressCount": "12000",
            "buyAddressCount": "8000",
            "sellAddressCount": "7000",
            "valueKol": 5500000.0,
            "buyValueKol": 3200000.0,
            "sellValueKol": 2300000.0,
            "buyAddressKol": 45,
            "sellAddressKol": 30,
            "totalAddressKol": 60
        }
    ]
}
```

**输出规则**:
- 默认输出：输出所有字段
- 详细信息：输出全部字段

---

## 8. K线历史数据

**接口地址**: `POST /v3/market/kline-historical`

**接口描述**: 查询代币指定时间粒度（1m/5m/1h/1d等）的K线历史数据，返回开高低收及成交量序列

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| bar | K线粒度（1m/5m/15m/30m/1h/4h/1D/1W） | true | string |
| before | 查询该时间之前的数据（毫秒时间戳） | false | number |
| after | 查询该时间之后的数据（毫秒时间戳） | false | number |
| limit | 最多返回条数，默认 400，最大 1500 | false | number |
| useNativePricing | 是否使用原生代币计价，默认 false（USD 计价） | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| kline | K线数据，每条为数组格式 `[时间戳, 开, 高, 低, 收, 量, 额]` | array |
| finalTime | 最新一条K线时间（毫秒时间戳） | string |

**kline 每条格式（数组，按下标顺序）**:

| 下标 | 说明 |
|------|------|
| 0 | 时间戳（毫秒，string 类型） |
| 1 | 开盘价 |
| 2 | 最高价 |
| 3 | 最低价 |
| 4 | 收盘价 |
| 5 | 成交量（代币数量） |
| 6 | 成交额（USD） |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "kline": [
            ["1776118800000", "145.00", "148.20", "144.50", "147.50", "950000", "137750000"],
            ["1776115200000", "143.00", "146.00", "142.80", "145.00", "880000", "127600000"]
        ],
        "finalTime": "1776118800000"
    }
}
```

**输出规则**:
- 默认输出：输出 kline 全部字段（time, open, high, low, close, volume）
- 详细信息：输出全部字段

---

## 9. Meme代币排行

**接口地址**: `POST /v3/coin/meme-rank`

**接口描述**: 查询Meme平台代币排行，支持按新建(NEW_CREATION)、拉盘(PUMP)、完成(COMPLETED)类型筛选，返回价格、进度、社媒热度等数据

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
    "data": [
        {
            "chainName": "SOL",
            "address": "MeMeAB...",
            "symbol": "MEME",
            "name": "MemeToken",
            "memeDex": "pump.fun",
            "createTime": "1776120000000",
            "lastTransTime": "1776122000000",
            "price": "0.00005",
            "marketCap": "50000",
            "holderCount": "500",
            "migrateProgress": 0.6,
            "value1h": "25000",
            "priceChange1h": "0.25",
            "buyTradeCount1h": "200",
            "sellTradeCount1h": "150",
            "rankType": "NEW_CREATION",
            "migrCnt": 2,
            "mintCnt": 5
        }
    ]
}
```

**输出规则**:
- 默认输出：symbol, chainName, address, price, marketCap, holderCount, rankType
- 详细信息：输出全部字段，包含 progress、heat、telegram、twitter 等嵌套数据

---

## 10. Meme支持的DEX列表

**接口地址**: `POST /v3/coin/meme-dexs`

**接口描述**: 查询指定链上Meme模块当前支持的DEX名称列表，用于前端筛选器初始化

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
- 默认输出：输出所有字段
- 详细信息：输出全部字段

---

## 11. 代币流动性池子列表

**接口地址**: `POST /v3/market/pool-top`

**接口描述**: 查询代币流动性最高的前20个池子，返回所属DEX、配对代币、流动性金额及24小时交易量

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| tokenContractAddress | 代币合约地址 | true | string |

**响应参数**（返回列表，最多20条，按流动性降序）:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| poolAddress | 池子合约地址 | string |
| dexEnum | DEX 枚举值 | number |
| dexName | DEX 名称 | string |
| dexIcon | DEX 图标 URL | string |
| liquid | 池子流动性（USD） | string |
| poolCoins | 池子内代币列表 | array |
| -> tokenContractAddress | 代币合约地址 | string |
| -> symbol | 代币符号 | string |
| -> balance | 代币数量 | string |
| -> value | 代币价值（USD） | string |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "poolAddress": "HJPjoW...",
            "dexEnum": 1,
            "dexName": "Raydium",
            "dexIcon": "https://...",
            "liquid": "5000000",
            "poolCoins": [
                {
                    "tokenContractAddress": "So11111111111111111111111111111111111111112",
                    "symbol": "SOL",
                    "balance": "34482",
                    "value": "5086000"
                },
                {
                    "tokenContractAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    "symbol": "USDC",
                    "balance": "5000000",
                    "value": "5000000"
                }
            ]
        }
    ]
}
```

**输出规则**:
- 默认输出：poolAddress, dexName, liquid, poolCoins（含 symbol、balance、value）
- 详细信息：输出全部字段

---

## 12. 搜索

**接口地址**: `GET /v3/coin/search`

**接口描述**: 支持按代币名称或合约地址进行搜索。搜索逻辑如下：

- 若搜索内容匹配到代币（名称或合约地址），返回代币列表，`addressList` 为空；
- 若搜索内容格式为链上地址且未匹配到代币，则将其作为钱包地址查询，返回地址列表，`coinList` 为空。

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
        "coinList": [
            {
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
                }
            }
        ],
        "addressList": []
    }
}
```

**输出规则**:
- 默认输出：symbol, tokenContractAddress, price, marketCap, holderCount, priceChange24h
- 详细信息：输出全部字段，包含 coinList、addressList 完整数据
