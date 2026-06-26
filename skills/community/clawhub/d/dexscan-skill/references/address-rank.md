# 地址牛人榜接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 接口信息

**接口地址**: `POST /v3/address/address-rank-page`

**接口描述**: 查询地址盈亏排行榜，支持多条件筛选和排序

## 请求参数

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| chainName | 链名 | true | string |
| bar | 时间枚举（7d、30d、90d） | true | string |
| page | 页数 | true | string |
| pageSize | 页大小 | true | string |
| order | 排序 | false | array |
| -> column | 排序字段 | true | string |
| -> asc | 是否正序 | true | boolean |
| tag | 标签枚举（KOL） | false | string |
| minPnl | 收益额最小值 | false | number |
| maxPnl | 收益额最大值 | false | number |
| minWinRatio | 胜率最小值 | false | number |
| maxWinRatio | 胜率最大值 | false | number |
| minNumber | 交易笔数最小值 | false | number |
| maxNumber | 交易笔数最大值 | false | number |
| maxValue | 成交额最大值 | false | number |
| minValue | 成交额最小值 | false | number |

## 响应参数

| 参数名称 | 字段说明 | 数据类型 |
|----------|----------|----------|
| total | 总记录数 | number |
| list | 地址列表 | array |
| -> address | 地址 | string |
| -> chainName | 链名 | string |
| -> bar | 时间范围 | string |
| -> pnl | 盈亏金额 | number |
| -> pnlRatio | 收益率 | number |
| -> buyValue | 买入成交额 | number |
| -> sellValue | 卖出成交额 | number |
| -> buyNumber | 买入笔数 | number |
| -> sellNumber | 卖出笔数 | number |
| -> winRatio | 胜率 | number |
| -> lastTransTime | 最后交易时间 | string |
| -> pnlTrend | 盈亏趋势 | object |
| -> highPnlCoins | 高收益代币列表 | array |
| --> icon | 代币图标 | string |
| --> symbol | 代币符号 | string |
| --> pnl | 收益金额 | string |
| --> pnlRatio | 收益率 | string |
| --> caddress | 代币地址 | string |
| -> number | 交易笔数 | number |
| -> value | 成交额 | number |
| -> buyAvgPrice | 平均买入价 | number |
| -> tagInfo | 地址标签信息 | object |
| --> name | 地址名称 | string |
| --> url | X地址 | string |
| --> icon | 地址头像 | string |
| --> fans | 粉丝数量 | number |
| --> tag | 地址标签 | string |
| -> aiLabel | AI标签分析 | object |
| --> evidence | 证据列表 | array |
| --> summary | AI总结 | string |
| --> label | 标签列表 | array |
| --> score | AI评分 | number |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 1089,
        "list": [
            {
                "address": "CyaE1VxvBrahnPWkqm5VsdCvyS2QmNht2UFrKJHga54o",
                "chainName": "SOL",
                "bar": "7d",
                "pnl": 206389.5398410519,
                "pnlRatio": 0.26890182193926954,
                "buyValue": 768478.369521926,
                "sellValue": 973917.0275784321,
                "buyNumber": 5671,
                "sellNumber": 2223,
                "winRatio": 0.6333030027297544,
                "lastTransTime": "2026-04-30 13:21:47",
                "pnlTrend": {
                    "2026-04-24": "13966.97050299",
                    "2026-04-25": "18302.45783004",
                    "2026-04-26": "37975.32633631",
                    "2026-04-27": "23217.89264893",
                    "2026-04-28": "61519.51746461",
                    "2026-04-29": "42900.49942334",
                    "2026-04-30": "8506.87563482"
                },
                "highPnlCoins": [
                    {
                        "icon": "https://static.dexscan.trade/images/logo/101-4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump.webp",
                        "symbol": "CREATURES",
                        "pnl": "22017.9327792186",
                        "pnlRatio": "1.51895",
                        "caddress": "4y1gkKzCb4qAiH8pH8ft2xvezf6sazurmYDajWXwpump"
                    }
                ],
                "updateTime": "2026-04-30 13:59:53",
                "number": 7894,
                "value": 1742395.3971003583,
                "buyAvgPrice": 135.51020446516065,
                "tagInfo": {
                    "address": "CyaE1VxvBrahnPWkqm5VsdCvyS2QmNht2UFrKJHga54o",
                    "name": "CENTED",
                    "url": "https://x.com/Cented7",
                    "icon": "https://static.dexscan.trade/kol/Cented7.png",
                    "fans": 494140,
                    "tag": "kol"
                },
                "aiLabel": ""
            }
        ],
        "extend": ""
    },
    "msg": "操作成功",
    "reqId": "2049732977899102208"
}
```

## 输出规则

### 默认输出字段

**address-rank-page**：address, chainName, pnl, pnlRatio, winRatio, number, value, lastTransTime

### 详细信息输出

当用户要求查看详细信息时，输出 list 下一层级所有字段，包含 tagInfo、aiLabel、highPnlCoins 等嵌套数据
