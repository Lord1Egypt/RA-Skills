# 行情接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 分页查询代币排行

**接口地址**: `POST /v3/market/coin-rank`

**接口描述**: 按时间粒度分页查询代币排行榜，支持过滤和排序

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名，ALL查全链 | true | string |
| bar | 时间粒度（5m/1h/4h/24h） | true | string |
| page | 页数 | false | number |
| pageSize | 页大小 | false | number |
| order | 排序 | false | array |
| -> column | 排序字段 | true | string |
| -> asc | 是否正序 | true | boolean |
| minValue | 成交额最小值 | false | number |
| maxValue | 成交额最大值 | false | number |
| minLiquid | 流动性最小值 | false | number |
| maxLiquid | 流动性最大值 | false | number |
| minPriceChange | 涨跌幅最小值 | false | number |
| maxPriceChange | 涨跌幅最大值 | false | number |
| minMarketCap | 市值最小值 | false | number |
| maxMarketCap | 市值最大值 | false | number |
| minTradeCount | 交易笔数最小值 | false | number |
| maxTradeCount | 交易笔数最大值 | false | number |
| minAddressCount | 活跃地址数最小值 | false | number |
| maxAddressCount | 活跃地址数最大值 | false | number |
| minHolderCount | 持币地址数最小值 | false | number |
| maxHolderCount | 持币地址数最大值 | false | number |
| minCreateTime | 创建时间最小值（时间戳ms） | false | number |
| maxCreateTime | 创建时间最大值（时间戳ms） | false | number |
| onlyMeme | 只看Meme币 | false | boolean |
| hideHigh | 隐藏高风险 | false | boolean |
| hideStable | 隐藏稳定币 | false | boolean |
| unit | 单位 | false | string |
| minCreateDuration | 创建时长最小值（秒） | false | number |
| maxCreateDuration | 创建时长最大值（秒） | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| total | 总数 | true | number |
| list | 列表 | true | array |
| -> chainName | 链名 | true | string |
| -> tokenAddressBase | 代币合约地址 | true | string |
| -> symbol | 代币符号 | true | string |
| -> icon | 代币图标 | false | string |
| -> createTime | 创建时间（时间戳ms） | false | number |
| -> totalSupply | 总供应量 | false | number |
| -> liquid | 流动性 | false | number |
| -> holderCount | 持币地址数 | false | number |
| -> marketCap | 市值 | false | number |
| -> bar | 时间粒度 | true | string |
| -> windowStart | 窗口开始时间 | false | number |
| -> windowEnd | 窗口结束时间 | false | number |
| -> openPrice | 开盘价 | false | number |
| -> closePrice | 收盘价 | false | number |
| -> high | 最高价 | false | number |
| -> low | 最低价 | false | number |
| -> priceChange | 涨跌幅 | false | number |
| -> buyVolume | 买入量 | false | number |
| -> sellVolume | 卖出量 | false | number |
| -> volume | 成交量 | false | number |
| -> buyValue | 买入额 | false | number |
| -> sellValue | 卖出额 | false | number |
| -> value | 成交额 | false | number |
| -> buyTradeCount | 买单数 | false | number |
| -> sellTradeCount | 卖单数 | false | number |
| -> tradeCount | 总交易数 | false | number |
| -> buyAddressCount | 买入地址数 | false | number |
| -> sellAddressCount | 卖出地址数 | false | number |
| -> addressCount | 总活跃地址数 | false | number |
| -> memeDex | Meme发射平台 | false | string |
| -> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | false | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 5142,
        "list": [
            {
                "chainName": "SOL",
                "tokenAddressBase": "CkYTCPCUZVdzQ4hQk67ridrRjACMznd5YChZ2gvyeRP2",
                "symbol": "Make Coin",
                "uri": "",
                "icon": "https://static.dexscan.trade/images/logo/101-CkYTCPCUZVdzQ4hQk67ridrRjACMznd5YChZ2gvyeRP2.png",
                "createTime": "1777512593000",
                "totalSupply": "99999999999",
                "liquid": "14321.53604331449",
                "holderCount": "127",
                "marketCap": "6656182.0287034381797123",
                "windowStart": "1777524600000",
                "windowEnd": "1777528205000",
                "bar": "1h",
                "low": "0.000036526226736",
                "high": "0.0000671919523579",
                "buyVolume": "151865100646.2384",
                "sellVolume": "151892802960.51132",
                "buyValue": "10021637.484819049",
                "sellValue": "10021536.819835437",
                "buyTradeCount": "1726",
                "sellTradeCount": "1725",
                "buyAddressCount": "9",
                "sellAddressCount": "8",
                "addressCount": "9",
                "openPrice": "0.000036526226736",
                "closePrice": "0.0000665618202877",
                "windowSize": "3600000",
                "volume": "303757903606.74972",
                "value": "20043174.304654486",
                "ondoValue": "",
                "tradeCount": "3451",
                "priceChange": "0.8223",
                "memeDex": "",
                "riskLevel": "MEDIUM",
                "offset": "30453672",
                "coinKey": "SOL_CkYTCPCUZVdzQ4hQk67ridrRjACMznd5YChZ2gvyeRP2"
            }
        ],
        "extend": ""
    },
    "msg": "操作成功",
    "reqId": "2049732973843210240"
}
```

---

## 2. 游标查询交易活动列表

**接口地址**: `POST /v3/market/trade-scroll`

**接口描述**: 游标分页查询指定代币的链上交易记录

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| swapTypes | 交易类型（1-买入，2-卖出） | false | array |
| minValue | 成交额最小值（USD） | false | number |
| maxValue | 成交额最大值（USD） | false | number |
| address | 按钱包地址筛选 | false | string |
| begin | 起始时间戳（毫秒） | false | number |
| end | 截止时间戳（毫秒） | false | number |
| dexEnum | DEX类型枚举值 | false | number |
| timeDesc | 是否时间倒序 | false | boolean |
| size | 每页数量，默认50 | false | number |
| cursor | 游标，首次不传 | false | object |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| cursor | 下一页游标 | false | object |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| list | 交易列表 | false | array |
| -> transHash | 交易Hash | true | string |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| -> swapType | 交易类型（1-买入，2-卖出） | true | number |
| -> address | 钱包地址 | true | string |
| -> baseAddress | 代币地址 | true | string |
| -> baseSymbol | 代币符号 | true | string |
| -> baseAmount | 代币数量 | true | number |
| -> quoteAddress | 报价代币地址 | true | string |
| -> quoteSymbol | 报价代币符号 | true | string |
| -> quoteAmount | 报价代币数量 | true | number |
| -> price | 成交价格 | true | number |
| -> value | 成交价值（USD） | true | number |
| -> dexEnum | DEX类型枚举 | false | number |
| -> dexAddress | DEX地址 | false | string |
| -> poolAddress | 池子地址 | false | string |
| -> tagInfo | 地址标签信息 | false | object |
| --> address | 地址 | true | string |
| --> name | 名称 | true | string |
| --> url | 主页链接 | true | string |
| --> icon | 头像 | true | string |
| --> fans | 粉丝数 | true | number |
| --> tag | 标签 | true | string |
| -> tags | 交易标签（DEV/KOL/TOP10/SNIPER/NEW） | false | array |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": 1776124800000,
            "blockHeight": 325000000,
            "transIndex": 5,
            "instIndex": 0
        },
        "list": [
            {
                "transHash": "5UUH9RTDiSpq6HKS6bp4NdU9PNJpXRXuiw6ShBTBhgH2abc",
                "blockTime": 1776124900000,
                "blockHeight": 325000001,
                "transIndex": 3,
                "instIndex": 0,
                "swapType": 1,
                "address": "AoTXYoy7kPLCx2DHJq35wiPV8aLKVYF2ShhcZS3XYk9H",
                "baseAddress": "So11111111111111111111111111111111111111112",
                "baseSymbol": "SOL",
                "baseAmount": 10.5,
                "quoteAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "quoteSymbol": "USDC",
                "quoteAmount": 1450.25,
                "price": 138.12,
                "value": 1450.25,
                "dexEnum": 1,
                "dexAddress": "9W959DqEETiGZocYWCQPaJ6sBmUzgfxXfqGeTEdp3aQP",
                "poolAddress": "HJPjoWUrhoZzkNfRpHuieeFk9WcZWjwy6PBjZ81ngndJ",
                "tagInfo": null,
                "tags": []
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789058"
}
```

---

## 3. 游标查询流动性变化列表

**接口地址**: `POST /v3/market/liquid-scroll`

**接口描述**: 游标分页查询指定代币的流动性添加/移除记录

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| swapTypes | 流动性变更类型（1-添加，2-移除） | false | array |
| minValue | 总额最小值（USD） | false | number |
| maxValue | 总额最大值（USD） | false | number |
| address | 按钱包地址筛选 | false | string |
| begin | 起始时间戳（毫秒） | false | number |
| end | 截止时间戳（毫秒） | false | number |
| dexEnum | DEX类型枚举值 | false | number |
| timeDesc | 是否时间倒序 | false | boolean |
| size | 每页数量，默认50 | false | number |
| cursor | 游标，首次不传 | false | object |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| cursor | 下一页游标 | false | object |
| list | 流动性记录列表 | false | array |
| -> transHash | 交易Hash | true | string |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| -> swapType | 变更类型（1-添加，2-移除） | true | number |
| -> address | 钱包地址 | true | string |
| -> poolAddress | 池子地址 | false | string |
| -> dexEnum | DEX类型枚举 | false | number |
| -> dexName | DEX名称 | false | string |
| -> dexIcon | DEX图标 | false | string |
| -> dexAddress | DEX地址 | false | string |
| -> value | 成交价值（USD） | false | number |
| -> tokens | 涉及代币列表 | false | array |
| --> tokenContractAddress | 代币合约地址 | true | string |
| --> symbol | 代币符号 | true | string |
| --> amount | 代币数量 | true | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": 1776124800000,
            "blockHeight": 325000000,
            "transIndex": 2,
            "instIndex": 0
        },
        "list": [
            {
                "transHash": "3xyzABCDEFGH1234567890abcdefghijklmnopqrstuvwxyz",
                "blockTime": 1776124900000,
                "blockHeight": 325000001,
                "transIndex": 1,
                "instIndex": 0,
                "swapType": 1,
                "address": "AoTXYoy7kPLCx2DHJq35wiPV8aLKVYF2ShhcZS3XYk9H",
                "poolAddress": "HJPjoWUrhoZzkNfRpHuieeFk9WcZWjwy6PBjZ81ngndJ",
                "dexEnum": 1,
                "dexName": "Raydium",
                "dexIcon": "https://static.dexscan.trade/dex/raydium.png",
                "dexAddress": "9W959DqEETiGZocYWCQPaJ6sBmUzgfxXfqGeTEdp3aQP",
                "value": 5000.00,
                "tokens": [
                    {
                        "tokenContractAddress": "So11111111111111111111111111111111111111112",
                        "symbol": "SOL",
                        "amount": 36.2
                    },
                    {
                        "tokenContractAddress": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                        "symbol": "USDC",
                        "amount": 5000.0
                    }
                ]
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789059"
}
```

---

## 4. 查询代币盈利列表

**接口地址**: `POST /v3/market/pnl-coin-list`

**接口描述**: 查询指定代币的持仓地址盈亏数据列表

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| type | 地址类型筛选（DEV/KOL/TOP10/SNIPER/NEW） | false | string |
| holderList | true时按持仓量排序返回Holder列表 | false | boolean |
| addresses | 批量钱包地址列表，最多10个 | false | array |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| address | 钱包地址 | true | string |
| baseAddress | 代币合约地址 | true | string |
| chainName | 链名 | false | string |
| symbol | 代币符号 | false | string |
| icon | 代币图标 | false | string |
| price | 当前价格 | false | number |
| balance | 当前持仓数量 | false | number |
| balanceValue | 当前持仓价值（USD） | false | number |
| beginTime | 首次买入时间戳 | false | number |
| latestBeginTime | 最近一次买入时间戳 | false | number |
| latestTime | 最近交易时间戳 | false | number |
| buyAmount | 总买入数量 | false | number |
| buyAmountDeposit | 总买入数量（含转入） | false | number |
| buyValue | 总买入金额（USD） | false | number |
| buyValueDeposit | 总买入金额（含转入，USD） | false | number |
| buyNumber | 买入次数 | false | number |
| buyAvgPrice | 平均买入价格 | false | number |
| sellAmount | 总卖出数量 | false | number |
| sellValue | 总卖出金额（USD） | false | number |
| sellNumber | 卖出次数 | false | number |
| sellAvgPrice | 平均卖出价格 | false | number |
| realizedPnl | 已实现盈亏（USD） | false | number |
| realizedPnlRatio | 已实现盈亏比例 | false | number |
| unrealizedPnl | 未实现盈亏（USD） | false | number |
| unrealizedPnlRatio | 未实现盈亏比例 | false | number |
| totalPnl | 总盈亏（USD） | false | number |
| totalPnlRatio | 总盈亏比例 | false | number |
| totalSupply | 代币总供应量 | false | number |
| nativeBalance | 原生代币余额 | false | number |
| sourceAddress | 资金来源地址 | false | string |
| sourceTime | 资金来源时间戳 | false | number |
| riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | false | string |
| holdingPeriod | 持仓时长（毫秒） | false | number |
| tagInfo | 地址标签信息 | false | object |
| -> address | 地址 | true | string |
| -> name | 名称 | true | string |
| -> url | 主页链接 | true | string |
| -> icon | 头像 | true | string |
| -> fans | 粉丝数 | true | number |
| -> tag | 标签 | true | string |
| tags | 地址类型标签（DEV/KOL/TOP10/SNIPER/NEW） | false | array |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "address": "AV7PjXHL5JXZ1YoYRoN9Dsstg1x2UciBupMCXcJP8gUz",
            "baseAddress": "5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd",
            "beginTime": "1777520304000",
            "latestBeginTime": "1777520304000",
            "latestTime": "1777520327000",
            "buyAmount": 278185185.185185,
            "buyAmountDeposit": 0,
            "buyValue": 871.7286212677658,
            "buyValueDeposit": 0,
            "buyNumber": 1,
            "sellAmount": 278185185.18518496,
            "sellValue": 5173.580729897584,
            "sellNumber": 25,
            "realizedPnl": 4301.852108629819,
            "unrealizedPnl": 0,
            "totalPnl": 4301.852108629819,
            "realizedPnlRatio": 4.93485243420548,
            "unrealizedPnlRatio": 0,
            "totalPnlRatio": 4.934852434205477,
            "buyAvgPrice": 0.0000031336270502236307,
            "sellAvgPrice": 0.00001859761412691185,
            "price": 0.0000027634590209,
            "balance": 0,
            "totalSupply": 999977065.842766,
            "nativeBalance": 19.595221918,
            "balanceValue": 0,
            "sourceAddress": "7fxc53tKLwxdc52D3kGF9h9aPEQWYTa7ivZfhAFYbtB4",
            "sourceTime": "1772326231000",
            "chainName": "SOL",
            "symbol": "MEGAMEN",
            "icon": "https://static.dexscan.trade/images/logo/101-5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd.jpeg",
            "riskLevel": "NONE",
            "tagInfo": "",
            "tags": [
                "DEV"
            ],
            "holdingPeriod": "23000"
        }
    ],
    "msg": "操作成功",
    "reqId": "2049734000365559808"
}
```

---

## 5. 游标查询开发者代币列表

**接口地址**: `POST /v3/market/developer-scroll`

**接口描述**: 游标分页查询指定代币的关联开发者创建的代币列表

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| size | 每页数量，默认30 | false | number |
| cursor | 游标（创建时间戳ms），首次不传 | false | number |
| needStats | 是否返回开发者统计数据 | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| cursor | 下一页游标（创建时间戳ms） | false | number |
| list | 代币列表 | false | array |
| -> chainName | 链名 | true | string |
| -> tokenAddressBase | 代币合约地址 | true | string |
| -> symbol | 代币符号 | true | string |
| -> name | 代币名称 | true | string |
| -> icon | 代币图标 | false | string |
| -> creator | 创建者地址 | false | string |
| -> price | 当前价格 | false | number |
| -> priceChange | 24h涨跌幅 | false | number |
| -> marketCap | 市值 | false | number |
| -> liquid | 流动性 | false | number |
| -> volume | 24h成交量 | false | number |
| -> value | 24h成交额 | false | number |
| -> totalSupply | 总供应量 | false | number |
| -> holderCount | 持币地址数 | false | number |
| -> createTime | 创建时间戳 | false | number |
| -> creatorBalance | 创建者持仓数量 | false | number |
| -> creatorBalanceRatio | 开发者持仓比例（0~1） | false | number |
| -> top10BalanceSum | Top10持仓合计 | false | number |
| -> tradeCount | 总交易笔数 | false | number |
| -> telegram | Telegram链接 | false | string |
| -> twitter | Twitter链接 | false | string |
| -> website | 官网链接 | false | string |
| -> kolCount | KOL持仓地址数 | false | number |
| -> newCount | 新钱包持仓地址数 | false | number |
| -> migrateFinished | 是否完成迁移 | false | boolean |
| -> migrateProgress | 迁移进度（0~1） | false | number |
| -> riskTag | 风险标签信息 | false | object |
| --> address | 代币地址 | true | string |
| --> chainName | 链名 | true | string |
| --> level | 风险等级（NONE/LOW/MEDIUM/HIGH） | true | string |
| --> riskTags | 风险标签列表 | false | array |
| ---> id | 标签ID | true | number |
| ---> tag | 标签标识 | true | string |
| ---> riskLevel | 风险等级 | true | string |
| ---> zhCn | 中文描述 | true | string |
| stats | 开发者统计（needStats=true时返回） | false | object |
| -> creator | 开发者地址 | true | string |
| -> sourceTime | 资金来源时间 | false | number |
| -> sourceAddress | 资金来源地址 | false | string |
| -> total | 创建代币总数 | false | number |
| -> migrated | 已迁移数量 | false | number |
| -> nonMigrated | 未迁移数量 | false | number |
| -> topMarketCap | 市值最高的代币 | false | object |
| -> lastCreateCoin | 最新创建的代币 | false | object |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": "1777522397000",
        "list": [
            {
                "chainName": "SOL",
                "symbol": "horboobs",
                "name": "Strait of Horboobs",
                "tokenAddressBase": "DK2UCiU6KjgfcrmxmdGtGodPsXEsRRDbfvc9xTTth1WZ",
                "icon": "https://static.dexscan.trade/images/logo/101-DK2UCiU6KjgfcrmxmdGtGodPsXEsRRDbfvc9xTTth1WZ.jpeg",
                "creator": "AV7PjXHL5JXZ1YoYRoN9Dsstg1x2UciBupMCXcJP8gUz",
                "liquid": "0.320585733583475",
                "volume": "351064647.004989",
                "value": "956.1649245589174",
                "totalSupply": "999999998.926997",
                "marketCap": "2331.2197969985941614771015",
                "holderCount": "1",
                "price": "0.0000023312197995",
                "priceChange": "-0.13688",
                "createTime": "1777522397000",
                "riskTag": {
                    "address": "DK2UCiU6KjgfcrmxmdGtGodPsXEsRRDbfvc9xTTth1WZ",
                    "chainName": "SOL",
                    "level": "NONE",
                    "riskTags": ""
                },
                "noPnl": false,
                "creatorBalance": "0",
                "top10BalanceSum": "0",
                "tradeCount": "18",
                "telegram": "",
                "twitter": "https://x.com/AutismCapital/status/2049703454780891161",
                "website": "",
                "kolCount": 1,
                "newCount": 0,
                "ondoMarketCap": "",
                "ondoPriceChange24h": "",
                "migrateFinished": false,
                "migrateProgress": "0.0001",
                "creatorBalanceRatio": "0"
            }
        ],
        "stats": ""
    },
    "msg": "操作成功",
    "reqId": "2049734014487781376"
}
```

---

## 6. 查询代币近期统计信息

**接口地址**: `POST /v3/market/coin-summary`

**接口描述**: 查询代币近期统计信息

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| bars | 时间粒度列表 | false | array |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenAddressBase | 代币合约地址 | true | string |
| symbol | 代币符号 | true | string |
| name | 代币名称 | true | string |
| icon | 代币图标 | false | string |
| price | 当前价格 | false | number |
| priceChange | 涨跌幅 | false | number |
| marketCap | 市值 | false | number |
| liquid | 流动性 | false | number |
| volume | 成交量 | false | number |
| value | 成交额 | false | number |
| buyVolume | 买入量 | false | number |
| sellVolume | 卖出量 | false | number |
| buyValue | 买入额 | false | number |
| sellValue | 卖出额 | false | number |
| buyTradeCount | 买单数 | false | number |
| sellTradeCount | 卖单数 | false | number |
| tradeCount | 总交易数 | false | number |
| buyAddressCount | 买入地址数 | false | number |
| sellAddressCount | 卖出地址数 | false | number |
| addressCount | 总活跃地址数 | false | number |
| holderCount | 持币地址数 | false | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "chainName": "SOL",
            "tokenAddressBase": "5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd",
            "symbol": "MEGAMEN",
            "icon": "https://static.dexscan.trade/images/logo/101-5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd.jpeg",
            "createTime": "1777520304000",
            "totalSupply": "999977065.842766",
            "liquid": "4091.8593300901225",
            "holderCount": "149",
            "marketCap": "2763.3956432963049637078094",
            "windowStart": "1777529190000",
            "bar": "5m",
            "openPrice": "0.0000030434918438",
            "closePrice": "0.0000027634590209",
            "priceChange": "-0.09201",
            "low": "0.0000027634590209",
            "high": "0.0000030434918438",
            "buyVolume": "0",
            "sellVolume": "34899904.340996",
            "volume": "34899904.340996",
            "buyValue": "0",
            "sellValue": "100.17907561654481",
            "value": "100.17907561654481",
            "buyTradeCount": "0",
            "sellTradeCount": "6",
            "tradeCount": "6",
            "buyAddressCount": "0",
            "sellAddressCount": "4",
            "addressCount": "4",
            "memeDex": "Pump.fun",
            "riskLevel": "NONE"
        }
    ],
    "msg": "操作成功",
    "reqId": "2049734027288797184"
}
```

---

## 7. 查询代币信息

**接口地址**: `POST /v3/market/coin-info`

**接口描述**: 查询代币详细信息

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenAddressBase | 代币合约地址 | true | string |
| symbol | 代币符号 | true | string |
| name | 代币名称 | true | string |
| decimals | 代币精度 | true | number |
| icon | 代币图标 | false | string |
| totalSupply | 总供应量 | false | number |
| owner | 所有者地址 | false | string |
| createTime | 创建时间（时间戳ms） | false | number |
| createTx | 创建交易Hash | false | string |
| creator | 创建者地址 | false | string |
| price | 当前价格 | false | number |
| priceChange | 涨跌幅 | false | number |
| marketCap | 市值 | false | number |
| liquid | 流动性 | false | number |
| volume | 成交量 | false | number |
| value | 成交额 | false | number |
| holderCount | 持币地址数 | false | number |
| kolCount | KOL持仓地址数 | false | number |
| newCount | 新钱包持仓地址数 | false | number |
| riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | false | string |
| riskTag | 风险标签信息 | false | object |
| mint | 是否为Mintable代币 | false | boolean |
| freeze | 是否为冻结代币 | false | boolean |
| transferFee | 转账费用 | false | number |
| top10HolderRatio | Top10持仓比例 | false | number |
| fundingAddress | 资金地址 | false | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "chainName": "SOL",
        "tokenAddressBase": "So11111111111111111111111111111111111111112",
        "symbol": "SOL",
        "name": "Wrapped SOL",
        "decimals": 9,
        "icon": "https://static.dexscan.trade/images/logo/sol.png",
        "totalSupply": 999999999.99,
        "createTime": 1609459200000,
        "creator": "SysvarC1ock11111111111111111111111111111111",
        "price": 138.12,
        "priceChange": 0.0199,
        "marketCap": 65000000000,
        "liquid": 980000000,
        "volume": 1234567.89,
        "value": 168999999.99,
        "holderCount": 4500000,
        "kolCount": 1280,
        "newCount": 23400,
        "riskLevel": "NONE",
        "mint": false,
        "freeze": false,
        "transferFee": 0,
        "top10HolderRatio": 0.35
    },
    "msg": "操作成功",
    "reqId": "2043948786527789063"
}
```

---

## 8. 查询K线历史数据

**接口地址**: `POST /v3/market/kline-historical`

**接口描述**: 查询代币K线历史数据

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |
| interval | K线周期（1m/5m/15m/30m/1h/4h/1d/1w） | true | string |
| begin | 起始时间戳（毫秒） | true | number |
| end | 结束时间戳（毫秒） | true | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| list | K线数据列表 | false | array |
| -> time | 时间戳 | true | number |
| -> open | 开盘价 | true | number |
| -> high | 最高价 | true | number |
| -> low | 最低价 | true | number |
| -> close | 收盘价 | true | number |
| -> volume | 成交量 | true | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "list": [
            {
                "time": 1776121200000,
                "open": 135.50,
                "high": 139.00,
                "low": 134.80,
                "close": 138.20,
                "volume": 123456.78
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789064"
}
```

---

## 9. 查询Meme代币排行列表

**接口地址**: `POST /v3/market/meme-rank`

**接口描述**: 查询Meme代币排行列表

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | false | string |
| order | 排序 | false | array |
| -> column | 排序字段 | true | string |
| -> asc | 是否正序 | true | boolean |
| page | 页数 | false | number |
| pageSize | 页大小 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| total | 总数 | true | number |
| list | 列表 | true | array |
| -> chainName | 链名 | true | string |
| -> tokenAddressBase | 代币合约地址 | true | string |
| -> symbol | 代币符号 | true | string |
| -> name | 代币名称 | true | string |
| -> icon | 代币图标 | false | string |
| -> price | 当前价格 | false | number |
| -> priceChange | 涨跌幅 | false | number |
| -> marketCap | 市值 | false | number |
| -> liquid | 流动性 | false | number |
| -> volume | 成交量 | false | number |
| -> holderCount | 持币地址数 | false | number |
| -> newHolderCount | 新地址持仓合计 | false | number |
| -> createTime | 创建时间 | false | number |
| -> riskLevel | 风险等级 | false | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 500,
        "list": [
            {
                "chainName": "SOL",
                "tokenAddressBase": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
                "symbol": "SOUL",
                "name": "Soulana",
                "icon": "https://static.dexscan.trade/images/logo/101-38Hb.webp",
                "price": 0.000002565,
                "priceChange": 0.482,
                "marketCap": 2564.59,
                "liquid": 1200.00,
                "volume": 5000000.00,
                "holderCount": 1256,
                "newHolderCount": 320,
                "createTime": 1776122379000,
                "riskLevel": "NONE"
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789065"
}
```

---

## 10. 查询Meme支持的DEX列表

**接口地址**: `POST /v3/market/meme-dexs`

**接口描述**: 查询Meme代币支持的DEX列表

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| tokenContractAddress | 代币合约地址 | true | string |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| dexEnum | DEX类型枚举 | true | number |
| dexName | DEX名称 | true | string |
| dexIcon | DEX图标 | false | string |
| dexAddress | DEX地址 | true | string |
| poolAddress | 池子地址 | false | string |
| version | 版本 | false | string |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "dexEnum": 1,
            "dexName": "Raydium",
            "dexIcon": "https://static.dexscan.trade/dex/raydium.png",
            "dexAddress": "9W959DqEETiGZocYWCQPaJ6sBmUzgfxXfqGeTEdp3aQP",
            "poolAddress": "HJPjoWUrhoZzkNfRpHuieeFk9WcZWjwy6PBjZ81ngndJ",
            "version": "v4"
        }
    ],
    "msg": "操作成功",
    "reqId": "2043948786527789066"
}
```

---

## 输出规则

### 默认输出字段

**coin-rank**：symbol, chainName, tokenAddressBase, priceChange, volume, value, marketCap, holderCount, riskLevel

**trade-scroll**：blockTime, swapType, address, baseSymbol, baseAmount, price, value, tags

**liquid-scroll**：blockTime, swapType, address, value, tokens（含 symbol、amount）

**pnl-coin-list**：address, symbol, balance, balanceValue, buyValue, sellValue, realizedPnl, realizedPnlRatio, totalPnl, totalPnlRatio, tags

**developer-scroll**：symbol, chainName, tokenAddressBase, price, priceChange, marketCap, liquid, creatorBalanceRatio, migrateFinished

**coin-summary**：输出所有字段

**coin-info**：输出所有字段

**kline-historical**：输出 list 全部字段（time, open, high, low, close, volume）

**meme-rank**：symbol, chainName, tokenAddressBase, price, priceChange, marketCap, holderCount, riskLevel

**meme-dexs**：输出所有字段

### 详细信息输出

当用户要求查看详细信息时，输出对应接口的完整响应字段，包含 tagInfo、riskTag、stats 等嵌套数据
