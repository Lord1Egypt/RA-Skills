# 地址接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 地址盈亏分析列表

**接口地址**: `POST /v3/address/pnl-page`

**接口描述**: 分页查询指定地址持有的代币盈亏情况，返回买入均价、持仓量、已实现盈亏、未实现盈亏及盈亏比例

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| address | 钱包地址 | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |
| baseAddress | 过滤指定代币合约地址 | false | string |
| hideHighRisk | 隐藏高风险代币，默认 false | false | boolean |
| hideClearance | 隐藏已清仓代币，默认 false | false | boolean |
| hideLowValue | 隐藏低价值代币，默认 false | false | boolean |
| minRealizedPnlRatio | 已实现盈亏比例最小值（如 0.1 表示 10%） | false | number |
| maxRealizedPnlRatio | 已实现盈亏比例最大值 | false | number |
| minUnrealizedPnlRatio | 未实现盈亏比例最小值 | false | number |
| maxUnrealizedPnlRatio | 未实现盈亏比例最大值 | false | number |
| minTotalPnlRatio | 总盈亏比例最小值 | false | number |
| maxTotalPnlRatio | 总盈亏比例最大值 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 盈亏列表 | array |
| -> address | 钱包地址 | string |
| -> baseAddress | 代币合约地址 | string |
| -> chainName | 链名 | string |
| -> symbol | 代币符号 | string |
| -> icon | 代币图标 URL | string |
| -> beginTime | 首次买入时间（毫秒） | string |
| -> latestBeginTime | 最近一次买入时间（毫秒） | string |
| -> latestTime | 最近交易时间（毫秒） | string |
| -> buyAmount | 累计买入数量 | number |
| -> buyAmountDeposit | 累计买入数量（含划入） | number |
| -> buyValue | 累计买入额（USD） | number |
| -> buyValueDeposit | 累计买入额（含划入，USD） | number |
| -> buyNumber | 买入次数 | number |
| -> sellAmount | 累计卖出数量 | number |
| -> sellValue | 累计卖出额（USD） | number |
| -> sellNumber | 卖出次数 | number |
| -> buyAvgPrice | 买入均价 | number |
| -> sellAvgPrice | 卖出均价 | number |
| -> price | 当前价格 | number |
| -> balance | 当前持仓数量 | number |
| -> totalSupply | 总供应量 | number |
| -> nativeBalance | 原生代币余额 | number |
| -> balanceValue | 当前持仓市值（USD） | number |
| -> realizedPnl | 已实现盈亏（USD） | number |
| -> unrealizedPnl | 未实现盈亏（USD） | number |
| -> totalPnl | 总盈亏（USD） | number |
| -> realizedPnlRatio | 已实现盈亏比例 | number |
| -> unrealizedPnlRatio | 未实现盈亏比例 | number |
| -> totalPnlRatio | 总盈亏比例 | number |
| -> holdingPeriod | 持仓时长（毫秒） | string |
| -> sourceAddress | 资金来源地址 | string |
| -> sourceTime | 资金来源时间（毫秒） | string |
| -> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | string |
| -> tags | 地址标签集合（DEV/KOL/TOP10/SNIPER/NEW） | array |
| -> tagInfo | 地址标签信息 | object |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 50,
        "list": [
            {
                "address": "7BgBvyjrZX1...",
                "baseAddress": "MeMeAB...",
                "chainName": "SOL",
                "symbol": "MEME",
                "icon": "https://...",
                "beginTime": "1776000000000",
                "latestBeginTime": "1776050000000",
                "latestTime": "1776122400000",
                "buyAmount": 1000000.0,
                "buyAmountDeposit": 1100000.0,
                "buyValue": 500.0,
                "buyValueDeposit": 550.0,
                "buyNumber": 2,
                "sellAmount": 500000.0,
                "sellValue": 350.0,
                "sellNumber": 1,
                "buyAvgPrice": 0.0000005,
                "sellAvgPrice": 0.0000007,
                "price": 0.0000006,
                "balance": 500000.0,
                "totalSupply": 1000000000.0,
                "nativeBalance": 1.5,
                "balanceValue": 300.0,
                "realizedPnl": 100.0,
                "unrealizedPnl": 150.0,
                "totalPnl": 250.0,
                "realizedPnlRatio": 0.2,
                "unrealizedPnlRatio": 0.25,
                "totalPnlRatio": 0.45,
                "holdingPeriod": "122400000",
                "sourceAddress": "7BgBvyjrZX2...",
                "sourceTime": "1775990000000",
                "riskLevel": "MEDIUM",
                "tags": ["DEV", "KOL"],
                "tagInfo": null
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：symbol, baseAddress, price, balance, balanceValue, buyValue, sellValue, realizedPnl, realizedPnlRatio, unrealizedPnl, unrealizedPnlRatio, totalPnl, totalPnlRatio, riskLevel
- 详细信息：输出全部字段，包含 tagInfo、tags

---

## 2. 地址资产组合列表

**接口地址**: `POST /v3/address/asset-top`

**接口描述**: 分页查询指定地址当前持有的代币资产，按持仓市值降序返回代币名称、数量、均价及当前价值

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| address | 钱包地址 | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 资产列表 | array |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 5,
        "list": [
            {
                "chainName": "SOL",
                "tokenContractAddress": "So11111111111111111111111111111111111111112",
                "symbol": "SOL",
                "icon": "https://...",
                "address": "7BgBvyjrZX1...",
                "price": 147.5,
                "priceChange24h": "0.017",
                "balance": 100.0,
                "value": 14750.0,
                "ratio": 0.75
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：symbol, tokenContractAddress, price, priceChange24h, balance, value, ratio
- 详细信息：输出全部字段

---

## 3. 地址交易历史

**接口地址**: `POST /v3/address/trade-scroll`

**接口描述**: 游标分页查询指定地址的链上交易记录，返回代币名称、买卖方向、交易金额、盈亏及交易时间

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| address | 钱包地址 | true | string |
| tokenContractAddress | 过滤指定代币合约地址 | false | string |
| swapTypes | 交易类型列表（1-买入，2-卖出） | false | array |
| size | 每次返回数量，默认 30 | false | number |
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
| -> symbol | 代币符号 | string |
| -> icon | 代币图标 URL | string |
| -> blockTime | 区块时间（yyyy-MM-dd HH:mm:ss） | string |
| -> blockHeight | 区块高度 | string |
| -> transIndex | EVENT 索引 | number |
| -> instIndex | 指令索引 | number |
| -> swapType | 交易类型（1-买入，2-卖出） | number |
| -> amount | 代币成交数量 | number |
| -> amountPnl | 盈亏数量（已卖出部分） | number |
| -> price | 成交价格 | number |
| -> value | 成交额（USD） | number |
| -> pnl | 本次交易盈亏（USD） | number |
| -> nativePrice | 原生代币价格 | number |
| -> marketCap | 交易时市值（USD） | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": "2026-04-14 10:00:00",
            "blockHeight": "320000000",
            "transIndex": 3,
            "instIndex": 0
        },
        "list": [
            {
                "address": "7BgBvyjrZX1...",
                "baseAddress": "So11111111111111111111111111111111111111112",
                "symbol": "SOL",
                "icon": "https://...",
                "blockTime": "2026-04-14 10:00:00",
                "blockHeight": "320000000",
                "transIndex": 3,
                "instIndex": 0,
                "swapType": 1,
                "amount": 10.0,
                "amountPnl": 0.0,
                "price": 145.0,
                "value": 1450.0,
                "pnl": 25.0,
                "nativePrice": 1.0,
                "marketCap": 80000000000.0
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：blockTime, symbol, swapType, amount, price, value, pnl
- 详细信息：输出全部字段
- 分页提示：cursor 不为空时提示"还有更多数据，如需继续请告知"

---

## 4. 地址开发者代币列表

**接口地址**: `POST /v3/address/developer-page`

**接口描述**: 分页查询指定开发者地址曾发行的代币列表，返回代币名称、发行时间、当前价格及涨跌幅

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| chainName | 链名，如 SOL、BSC | true | string |
| addressDev | 开发者钱包地址 | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 代币列表 | array |
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

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 5,
        "list": [
            {
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
            }
        ]
    }
}
```

**输出规则**:
- 默认输出：symbol, tokenContractAddress, price, priceChange24h, marketCap, liquid, createTime, migrateFinished
- 详细信息：输出全部字段，包含 appendix

---

## 5. 牛人榜

**接口地址**: `POST /v3/address/rank-page`

**接口描述**: 分页查询链上盈利能力排名靠前的地址，基于已实现盈亏、胜率等指标综合排序

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|------|------|------|------|
| bar | 统计周期（7d/30d/90d） | true | string |
| chainName | 链名，如 SOL、BSC | true | string |
| page | 页码，默认 1 | false | number |
| pageSize | 每页数量，默认 10 | false | number |
| tag | 地址标签筛选，可选值：KOL | false | string |
| minPnl | 总盈亏最小值（USD） | false | number |
| maxPnl | 总盈亏最大值（USD） | false | number |
| minWinRatio | 胜率最小值（0~1） | false | number |
| maxWinRatio | 胜率最大值（0~1） | false | number |
| minNumber | 交易笔数最小值 | false | number |
| maxNumber | 交易笔数最大值 | false | number |
| minValue | 成交额最小值（USD） | false | number |
| maxValue | 成交额最大值（USD） | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|------|------|------|
| total | 总数 | number |
| list | 地址排行列表 | array |
| -> address | 钱包地址 | string |
| -> chainName | 链名 | string |
| -> bar | 统计周期 | string |
| -> pnl | 总盈亏（USD） | number |
| -> pnlRatio | 总盈亏比例 | number |
| -> buyValue | 累计买入额（USD） | number |
| -> sellValue | 累计卖出额（USD） | number |
| -> buyNumber | 买入次数 | number |
| -> sellNumber | 卖出次数 | number |
| -> number | 总交易笔数 | number |
| -> value | 当前资产规模（USD） | number |
| -> winRatio | 胜率（0~1） | number |
| -> buyAvgPrice | 买入均价 | number |
| -> lastTransTime | 最近交易时间（毫秒） | string |
| -> updateTime | 数据更新时间（毫秒） | string |
| -> pnlTrend | 盈亏趋势（key 为日期，value 为当日盈亏） | object |
| -> highPnlCoins | 盈利最高的代币列表 | array |
| --> tokenContractAddress | 代币合约地址 | string |
| --> icon | 代币图标 URL | string |
| --> symbol | 代币符号 | string |
| --> pnl | 盈亏（USD） | string |
| --> pnlRatio | 盈亏比例 | string |
| -> tagInfo | 地址标签信息 | object |
| --> address | 地址 | string |
| --> name | 名称 | string |
| --> url | 主页链接 | string |
| --> icon | 头像 | string |
| --> fans | 粉丝数 | number |
| --> tag | 标签 | string |
| -> aiLabel | AI 标签信息 | object |
| --> address | 地址 | string |
| --> chainName | 链名 | string |
| --> bar | 统计周期 | string |
| --> evidence | 得分依据列表 | array |
| --> summary | AI 小结 | string |
| --> label | 标签列表 | array |
| --> score | 得分 | number |
| --> updateTime | 更新时间 | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 1000,
        "list": [{
            "address": "7BgBvyjrZX1...",
            "chainName": "SOL",
            "bar": "7d",
            "pnl": 58000.0,
            "pnlRatio": 2.35,
            "buyValue": 25000.0,
            "sellValue": 83000.0,
            "buyNumber": 12,
            "sellNumber": 10,
            "number": 22,
            "value": 108000.0,
            "winRatio": 0.80,
            "buyAvgPrice": 2083.33,
            "lastTransTime": "1776122400000",
            "updateTime": "1776208800000",
            "pnlTrend": {
                "2026-05-01": "12000",
                "2026-05-02": "20000",
                "2026-05-03": "58000"
            },
            "highPnlCoins": [{
                "tokenContractAddress": "MeMeAB...",
                "icon": "https://...",
                "symbol": "MEME",
                "pnl": "45000",
                "pnlRatio": "1.8"
            }],
            "tagInfo": {
                "address": "7BgBvyjrZX1...",
                "name": "CryptoWhale",
                "url": "https://twitter.com/CryptoWhale",
                "icon": "https://...",
                "fans": 50000,
                "tag": "KOL"
            },
            "aiLabel": {
                "address": "7BgBvyjrZX1...",
                "chainName": "SOL",
                "bar": "7d",
                "evidence": ["高胜率", "持仓周期短"],
                "summary": "该地址擅长把握短期趋势",
                "label": ["高频交易", "趋势跟随"],
                "score": 88,
                "updateTime": "1776208800000"
            }
        }]
    }
}
```

**输出规则**:
- 默认输出：address, chainName, pnl, pnlRatio, winRatio, number, value, lastTransTime
- 详细信息：输出全部字段，包含 tagInfo、aiLabel、highPnlCoins、pnlTrend
