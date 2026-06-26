# 代币信号接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 信号列表查询

**接口地址**: `POST /v3/coin-signal-scroll`

**接口描述**: 查询24小时信号，支持游标分页，每页返回20条

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名称 | false | string |
| cursor | 游标 | false | object |
| -> address | 代币地址 | true | string |
| -> signalTime | 最新信号时间 | true | number |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| cursor | 游标 | false | object |
| -> address | 代币地址 | true | string |
| -> signalTime | 最新信号时间 | true | number |
| list | 列表 | false | array |
| -> chainName | 链名称 | true | string |
| -> address | 代币地址 | true | string |
| -> symbol | 代币symbol | true | string |
| -> name | 代币名称 | true | string |
| -> icon | 代币图标 | true | string |
| -> riskTag | 风险信息 | false | object |
| --> address | 代币地址 | true | string |
| --> chainName | 链名称 | true | string |
| --> level | 风险等级，NONE、LOW、MEDIUM、HIGH | true | string |
| --> riskTags | 风险标签 | false | array |
| ---> id | id | true | number |
| ---> tag | 风险标签 | true | string |
| ---> riskLevel | 风险等级，NONE、LOW、MEDIUM、HIGH | true | string |
| ---> zhCn | 风险描述 | true | string |
| -> top10BalanceSum | top10持仓 | false | string |
| -> signalPrice | 最新信号推送价格 | true | string |
| -> signalMarketCap | 最新信号推送市值 | true | string |
| -> signalHolder | 最新信号推送持币地址数量 | true | number |
| -> price | 当前价格 | true | string |
| -> marketCap | 当前市值 | true | string |
| -> holder | 当前持币地址数量 | true | number |
| -> score | 最新信号评分 | true | number |
| -> maxPriceChange | 最新信号最大价格涨幅 | true | number |
| -> signalTime | 最新信号推送时间 | true | number |
| -> totalSupply | 供应量 | false | string |
| -> chartList | 图表数据 | false | array |
| --> time | 时间窗口 | true | number |
| --> price | 时间窗口价格 | true | string |
| --> hot | 时间窗口热力值 | false | string |
| --> tagInfo | 时间窗口成交额最大的kol标签 | false | object |
| ---> address | 地址 | true | string |
| ---> name | 地址名称 | true | string |
| ---> url | 地址官网 | true | string |
| ---> icon | 地址头像 | true | string |
| ---> fans | 粉丝数量 | true | number |
| ---> tag | 地址标签 | true | string |
| --> value | 时间窗口kol最大成交额 | false | string |
| --> kolComment | 时间窗口评论影响最大kol | false | object |
| ---> userId | 评论KOL用户ID | true | number |
| ---> username | 评论KOL名称 | false | string |
| ---> url | 地址官网 | false | string |
| ---> icon | 地址头像 | true | string |
| ---> score | 评论KOL评分 | false | string |
| --> signal | 信号推送 | true | boolean |
| -> hisList | 历史信号数据 | true | array |
| --> signalTime | 信号推送时间 | true | number |
| --> score | 信号评分 | true | string |
| --> marketCap | 信号推送市值 | true | string |
| -> createTime | 代币创建时间 | false | number |
| -> firstMaxPriceChange | 首次信号最大涨幅 | true | string |
| -> firstCreateTime | 首次信号推送时间 | true | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "cursor": {
            "address": "CpmiJvsPHnK7suAfe5jZGQJQEbxEAVh65wJ1RT1Fpump",
            "signalTime": 1777482160000
        },
        "list": [
            {
                "chainName": "SOL",
                "address": "5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd",
                "symbol": "MEGAMEN",
                "name": "MegaMen",
                "icon": "https://static.dexscan.trade/images/logo/101-5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd.jpeg",
                "riskTag": {
                    "address": "5BWhSnQbangtYqPKmQjnt8Kux2rHnUzvW6FcvHjv5WGd",
                    "chainName": "SOL",
                    "level": "NONE",
                    "riskTags": []
                },
                "top10BalanceSum": "146170257.23356401920318603515625",
                "signalPrice": "0.0000531437210105",
                "signalMarketCap": "53143.7210105",
                "signalHolder": "308",
                "price": "0.0000030434918438",
                "marketCap": "3043.4220438795138942319508",
                "holder": "153",
                "score": 61,
                "maxPriceChange": "0.303",
                "signalTime": 1777520343000,
                "totalSupply": "999977065.842766",
                "chartList": [
                    {
                        "time": 1777520340000,
                        "price": "0.0000692439754826",
                        "hot": "",
                        "tagInfo": {
                            "address": "FajxNukkjDLGXfB5V3L1msrU9qgzuzhN4s4YQfefSCKp",
                            "name": "Divix",
                            "url": "https://x.com/cryptodivix",
                            "icon": "https://static.dexscan.trade/kol/cryptodivix.png",
                            "fans": 80713,
                            "tag": "kol"
                        },
                        "value": "308.06155562842645",
                        "kolComment": "",
                        "signal": true
                    }
                ],
                "hisList": [
                    {
                        "signalTime": 1777520343000,
                        "score": 61,
                        "marketCap": "53143.7210105"
                    }
                ],
                "createTime": 1777520304000,
                "firstMaxPriceChange": "0.303",
                "firstCreateTime": 1777520343000
            }
        ]
    },
    "msg": "操作成功",
    "reqId": "2049732973264396288"
}
```

---

## 2. 信号排行榜

**接口地址**: `POST /v3/coin-signal-rank`

**接口描述**: 查询24小时信号排行榜TOP10，基于首次信号最大涨幅降序，最新信号推送时间降序。

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | false | string |

**响应参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | false | string |
| address | 代币地址 | false | string |
| symbol | 代币symbol | true | string |
| name | 代币名称 | true | string |
| icon | 代币图标 | true | string |
| marketCap | 最新信号推送市值 | true | string |
| score | 最新信号评分 | true | number |
| maxPriceChange | 最新信号价格最大涨幅 | true | string |
| signalTime | 最新信号推送时间 | true | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "chainName": "SOL",
            "address": "2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump",
            "symbol": "Wish",
            "name": "Make A Wish",
            "icon": "https://static.dexscan.trade/images/logo/101-2ssMotVbTUfRJev2UnibHzHsoeszPzgwbfsTZPSHpump.jpeg",
            "marketCap": "2252716.2728507410401950835774",
            "score": 66,
            "maxPriceChange": "0.8151",
            "signalTime": 1777514626000
        }
    ],
    "msg": "操作成功",
    "reqId": "2049732973738352640"
}
```

---

## 输出规则

### 默认输出字段

**coin-signal-scroll**：symbol, chainName, address, price, holder, marketCap, score, signalTime, firstMaxPriceChange, firstCreateTime

**coin-signal-rank**：symbol, chainName, address, marketCap, score, maxPriceChange, signalTime

### 详细信息输出

当用户要求查看详细信息时，输出对应接口的完整响应字段，包含 riskTag、chartList、hisList 等嵌套数据
