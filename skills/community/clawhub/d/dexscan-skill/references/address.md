# 地址情况接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 游标查询地址交易历史列表

**接口地址**: `POST /v3/address/address-trade-scroll`

**接口描述**: 游标分页查询指定钱包地址的历史交易盈亏记录

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| address | 钱包地址 | true | string |
| tokenContractAddress | 代币合约地址，传入时只查询该代币的交易记录 | false | string |
| swapTypes | 交易类型（1-买入，2-卖出） | false | array |
| cursor | 游标，首次不传 | false | object |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| size | 每次返回数量，默认30 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| cursor | 下一页游标 | false | object |
| -> blockTime | 区块时间戳（毫秒） | true | number |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| list | 交易记录列表 | false | array |
| -> address | 钱包地址 | true | string |
| -> blockTime | 交易时间 | true | string |
| -> blockHeight | 区块高度 | true | number |
| -> transIndex | 交易内事件索引 | true | number |
| -> instIndex | 指令索引 | true | number |
| -> baseAddress | 代币合约地址 | true | string |
| -> swapType | 交易类型（1-买入，2-卖出） | true | number |
| -> amount | 交易数量 | true | number |
| -> amountPnl | 盈亏关联数量 | false | number |
| -> price | 交易价格 | true | number |
| -> value | 交易金额（USD） | true | number |
| -> pnl | 本次交易盈亏（USD） | false | number |
| -> symbol | 代币符号 | false | string |
| -> icon | 代币图标 | false | string |
| -> nativePrice | 原生代币价格 | false | number |
| -> marketCap | 市值 | false | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "blockTime": "2026-04-30 13:21:47",
            "blockHeight": "416591907",
            "transIndex": 362,
            "instIndex": 4001000,
            "externalCursor": ""
        },
        "list": [
            {
                "address": "CyaE1VxvBrahnPWkqm5VsdCvyS2QmNht2UFrKJHga54o",
                "blockTime": "2026-04-30 13:21:47",
                "blockHeight": "416591907",
                "transIndex": 362,
                "instIndex": 4001000,
                "baseAddress": "CuaDFXcxt7MV5awapFuQvfQwThA743Cs7e53b1cZpump",
                "swapType": 2,
                "amount": 41644603.837879,
                "amountPnl": 41644603.837879,
                "price": 0.0000089075276332,
                "value": 370.95045946155534,
                "pnl": 108.95635579654717,
                "symbol": "OpenGithub",
                "icon": "https://static.dexscan.trade/images/logo/101-CuaDFXcxt7MV5awapFuQvfQwThA743Cs7e53b1cZpump.webp",
                "nativePrice": 82.60562764263332,
                "marketCap": 3934.3972518874343
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2049732977806827520"
}
```

---

## 2. 分页查询地址盈亏分析列表

**接口地址**: `POST /v3/address/address-list`

**接口描述**: 分页查询钱包地址的各代币持仓盈亏情况，支持多维度过滤和排序

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| address | 钱包地址 | true | string |
| page | 页数，默认1 | false | number |
| pageSize | 页大小，默认20 | false | number |
| order | 排序 | false | array |
| -> column | 排序字段（latestTime/realizedPnl/totalPnl/unrealizedPnl/balance/sellValue/buyValue/realizedPnlRatio/unrealizedPnlRatio/totalPnlRatio） | true | string |
| -> asc | 是否正序 | true | boolean |
| baseAddress | 代币合约地址，传入时只查询该代币 | false | string |
| hideHighRisk | 是否隐藏高风险代币 | false | boolean |
| hideClearance | 是否隐藏已清仓代币 | false | boolean |
| hideLowValue | 是否隐藏持仓价值低于$1的代币 | false | boolean |
| minRealizedPnlRatio | 已实现盈利比例最小值 | false | number |
| maxRealizedPnlRatio | 已实现盈利比例最大值 | false | number |
| minUnrealizedPnlRatio | 未实现盈利比例最小值 | false | number |
| maxUnrealizedPnlRatio | 未实现盈利比例最大值 | false | number |
| minTotalPnlRatio | 总盈利比例最小值 | false | number |
| maxTotalPnlRatio | 总盈利比例最大值 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| total | 总数 | true | number |
| list | 盈亏列表 | true | array |
| -> address | 钱包地址 | true | string |
| -> baseAddress | 代币合约地址 | true | string |
| -> chainName | 链名 | false | string |
| -> symbol | 代币符号 | false | string |
| -> icon | 代币图标 | false | string |
| -> price | 当前价格 | false | number |
| -> balance | 当前持仓数量 | false | number |
| -> balanceValue | 当前持仓价值（USD） | false | number |
| -> beginTime | 首次买入时间戳 | false | number |
| -> latestBeginTime | 最近一次买入时间戳 | false | number |
| -> latestTime | 最近交易时间戳 | false | number |
| -> buyAmount | 总买入数量 | false | number |
| -> buyValue | 总买入金额（USD） | false | number |
| -> buyNumber | 买入次数 | false | number |
| -> buyAvgPrice | 平均买入价格 | false | number |
| -> sellAmount | 总卖出数量 | false | number |
| -> sellValue | 总卖出金额（USD） | false | number |
| -> sellNumber | 卖出次数 | false | number |
| -> sellAvgPrice | 平均卖出价格 | false | number |
| -> realizedPnl | 已实现盈亏（USD） | false | number |
| -> realizedPnlRatio | 已实现盈亏比例 | false | number |
| -> unrealizedPnl | 未实现盈亏（USD） | false | number |
| -> unrealizedPnlRatio | 未实现盈亏比例 | false | number |
| -> totalPnl | 总盈亏（USD） | false | number |
| -> totalPnlRatio | 总盈亏比例 | false | number |
| -> riskLevel | 风险等级（NONE/LOW/MEDIUM/HIGH） | false | string |
| -> holdingPeriod | 持仓时长（毫秒） | false | number |
| -> tagInfo | 地址标签信息 | false | object |
| --> address | 地址 | true | string |
| --> name | 名称 | true | string |
| --> url | 主页链接 | true | string |
| --> icon | 头像 | true | string |
| --> fans | 粉丝数 | true | number |
| --> tag | 标签 | true | string |
| -> tags | 地址类型标签（DEV/KOL/TOP10/SNIPER/NEW） | false | array |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 58,
        "list": [
            {
                "address": "AoTXYoy7kPLCx2DHJq35wiPV8aLKVYF2ShhcZS3XYk9H",
                "baseAddress": "So11111111111111111111111111111111111111112",
                "chainName": "SOL",
                "symbol": "SOL",
                "icon": "https://static.dexscan.trade/images/logo/sol.png",
                "price": 138.12,
                "balance": 1500.0,
                "balanceValue": 207180.0,
                "beginTime": 1700000000000,
                "latestTime": 1776124900000,
                "buyAmount": 2000.0,
                "buyValue": 250000.0,
                "buyNumber": 5,
                "buyAvgPrice": 125.0,
                "sellAmount": 500.0,
                "sellValue": 65000.0,
                "sellNumber": 2,
                "sellAvgPrice": 130.0,
                "realizedPnl": 2500.0,
                "realizedPnlRatio": 0.04,
                "unrealizedPnl": 19680.0,
                "unrealizedPnlRatio": 0.105,
                "totalPnl": 22180.0,
                "totalPnlRatio": 0.1,
                "riskLevel": "NONE",
                "holdingPeriod": 76124900000,
                "tags": ["KOL"]
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789068"
}
```

---

## 3. 分页查询地址资产组合列表

**接口地址**: `POST /v3/address/address-asset-top`

**接口描述**: 分页查询钱包地址的持仓资产列表，按持仓价值降序排列

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| address | 钱包地址 | true | string |
| page | 页数，默认1 | false | number |
| pageSize | 页大小，默认10 | false | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| total | 总数 | true | number |
| list | 资产列表 | true | array |
| -> chainName | 链名 | true | string |
| -> tokenContractAddress | 代币合约地址 | true | string |
| -> symbol | 代币符号 | true | string |
| -> icon | 代币图标 | false | string |
| -> price | 当前价格 | false | number |
| -> priceChange24h | 24h涨跌幅 | false | number |
| -> address | 钱包地址 | true | string |
| -> balance | 持仓数量 | false | number |
| -> value | 持仓价值（USD） | false | number |
| -> ratio | 该代币占总资产比例（0~1） | false | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 25,
        "list": [
            {
                "chainName": "SOL",
                "tokenContractAddress": "So11111111111111111111111111111111111111112",
                "symbol": "SOL",
                "icon": "https://static.dexscan.trade/images/logo/sol.png",
                "price": 138.12,
                "priceChange24h": 0.052,
                "address": "AoTXYoy7kPLCx2DHJq35wiPV8aLKVYF2ShhcZS3XYk9H",
                "balance": 1500.0,
                "value": 207180.0,
                "ratio": 0.65
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789069"
}
```

---

## 4. 分页查询地址开发者代币列表

**接口地址**: `POST /v3/address/developer-page`

**接口描述**: 分页查询指定开发者地址创建的代币列表，支持排序

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| addressDev | 开发者钱包地址 | true | string |
| page | 页数，默认1 | false | number |
| pageSize | 页大小，默认20 | false | number |
| order | 排序 | false | array |
| -> column | 排序字段（createTime/marketCap/liquid/value/creatorBalanceRatio） | true | string |
| -> asc | 是否正序 | true | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| total | 总数 | true | number |
| list | 代币列表 | true | array |
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
| -> noPnl | 是否存在无PNL数据 | false | boolean |
| -> riskTag | 风险标签信息 | false | object |
| --> address | 代币地址 | true | string |
| --> chainName | 链名 | true | string |
| --> level | 风险等级（NONE/LOW/MEDIUM/HIGH） | true | string |
| --> riskTags | 风险标签列表 | false | array |
| ---> id | 标签ID | true | number |
| ---> tag | 标签标识 | true | string |
| ---> riskLevel | 风险等级 | true | string |
| ---> zhCn | 中文描述 | true | string |

**响应示例（developer-page）**:

```json
{
    "code": 200,
    "data": {
        "total": 15,
        "list": [
            {
                "chainName": "SOL",
                "tokenAddressBase": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
                "symbol": "SOUL",
                "name": "Soulana",
                "icon": "https://static.dexscan.trade/images/logo/101-38Hb.webp",
                "creator": "DevAddressXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "price": 0.0000025651230023,
                "priceChange": -0.891,
                "marketCap": 2564.59,
                "liquid": 1200.0,
                "value": 8900.0,
                "createTime": 1776122379000,
                "creatorBalance": 50000000.0,
                "creatorBalanceRatio": 0.05,
                "migrateFinished": false,
                "migrateProgress": 0.32,
                "riskTag": {
                    "address": "38Hb8v9yFen5fN3FJUSuf8SuiVbzGYcTgkmsjqkKpump",
                    "chainName": "SOL",
                    "level": "NONE",
                    "riskTags": []
                }
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2043948786527789070"
}
```

---

## 输出规则

### 默认输出字段

**address-trade-scroll**：blockTime, symbol, swapType, amount, price, value, pnl

**address-list**：symbol, baseAddress, balance, balanceValue, buyValue, sellValue, realizedPnl, realizedPnlRatio, unrealizedPnl, unrealizedPnlRatio, totalPnl, totalPnlRatio, riskLevel

**address-asset-top**：symbol, tokenContractAddress, price, priceChange24h, balance, value, ratio

**developer-page**：symbol, tokenAddressBase, price, priceChange, marketCap, liquid, createTime, creatorBalanceRatio, migrateFinished

### 详细信息输出

当用户要求查看详细信息时，输出对应接口的完整响应字段，包含 tagInfo、riskTag、tags 等嵌套数据
