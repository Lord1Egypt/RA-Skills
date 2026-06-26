# 热度接口

> **认证说明**：所有接口认证信息详见 SKILL.md 文档

## 1. 社交热度列表

**接口地址**: `POST /v3/coin-heat-page`

**接口描述**: 社交热度列表，支持分页和排序

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| page | 页数 | true | integer |
| pageSize | 页大小 | true | integer |
| order | 排序 | false | array |
| -> column | 排序字段 | true | string |
| -> asc | 是否正序 | true | boolean |
| chainName | 链名 | true | string |
| heatDate | 热度时间戳 | false | number |
| onlyLookNewCoin | 是否新币 | false | boolean |
| filtrationBlueChipCoin | 是否过滤蓝筹币 | false | boolean |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|----------|----------|----------|
| chainName | 链名 | string |
| icon | 代币图标 | string |
| address | 代币地址 | string |
| symbol | 代币符号 | string |
| heatTime | 热度时间 | number |
| displayHeat | 展示热度 | number |
| marketCap | 市值 | number |
| priceFluctuationRatio | 24小时涨跌幅 | number |
| heatTopKol | 热度贡献前5kol | array |
| -> username | kol名 | string |
| -> url | X地址 | string |
| -> icon | 图标 | string |
| buyTopKol | 交易买入top5kol | array |
| -> username | kol名 | string |
| -> url | X地址 | string |
| -> icon | 图标 | string |
| heatFluctuation | 热度涨跌值 | number |
| heatFluctuationRatio | 热度涨跌幅 | number |
| priceTrend | 24h价格走势 | array |
| aiSummary | 推文AI总结 | object |
| -> tweetAiSummaryList | 总结列表 | array |
| --> title | 标题 | string |
| --> content | 总结内容 | string |

**响应示例**:

```json
{
    "code": 200,
    "data": {
        "total": 140,
        "list": [
            {
                "chainName": "SOL",
                "icon": "https://static.dexscan.trade/images/logo/101-4UeLCRqARmfb6e6KQijtiktqqXUxbfk6jZng7DhuBAGS.webp",
                "address": "4UeLCRqARmfb6e6KQijtiktqqXUxbfk6jZng7DhuBAGS",
                "symbol": "ASTEROID",
                "heatTime": 1777521600000,
                "displayHeat": 4282341.622794999,
                "marketCap": 3826759.96922065,
                "priceFluctuationRatio": -0.0104,
                "heatTopKol": [
                    {
                        "userId": "879561144251195392",
                        "username": "@phamduydong179",
                        "url": "https://x.com/phamduydong179",
                        "icon": "https://static.dexscan.trade/kol/phamduydong179.png"
                    }
                ],
                "buyTopKol": [
                    {
                        "userId": "",
                        "username": "Nach",
                        "url": "https://x.com/NachSOL",
                        "icon": "https://static.dexscan.trade/kol/NachSOL.png"
                    }
                ],
                "heatFluctuation": 0,
                "heatFluctuationRatio": 0,
                "priceTrend": [
                    0.004246863874224
                ],
                "aiSummary": {
                    "tweetAiSummaryList": [
                        {
                            "title": "ASTEROID 多链叙事撕裂与SpaceX官方背书下的 meme 暴涨周期",
                            "content": "$ASTEROID 多链生态剧烈分化：SOL链Bags平台主打高税手续费分发与慈善叙事，ETH主网强调OG社区自治、零预挖、真实捐赠（21亿代币/0.5%总量捐予St. Jude），二者因分发公平性、筹码结构及信息透明度爆发激烈论战，形成"大小写纷争"与阵营站队。社区普遍警告FOMO风险，强调"无人为你的钱包负责"，但亦有用户宣称ETH版本已确认庄家控盘，市值稳守1M–1.8M区间为关键信号。\n\nSpaceX官方邮件确认"Asteroid Plush Toy Restock"，标题直指「Inquiry about Asteroid Plush Toy Restock」，并将Asteroid Shiba Inu明确定义为"零重力指示器"，构成罕见链下强背书；叠加马斯克近期高频提及太空主题meme（$SCAM、$FLORK），市场强烈预期其将直接助推$ASTEROID——尤其Bags版有望复制$SCAM单日暴涨逻辑。Jucom Launchpad第10期已启动（4月27日–29日），绑定"登月+SpaceX吉祥物"叙事，打新热度持续攀升，被视作短期情绪放大器。\n\n链上动态两极分化：VitalikButerin单日抛售4000万枚$ASTEROID-2换得11.4万美元USDC，引发E卫兵对信仰动摇与熊市阶段的深度讨论；与此同时，SOL链大户出现单地址清仓5280万枚（获利8.37万美元）后转向$SCAN，而ETH链交易量从4000万刀骤降至600万刀，活跃度明显冷却，但持币地址数稳定在23,800+，未现大规模抛压。商标已提交USPTO注册，法律层面强化IP护城河，社区共识正从"土狗投机"向"太空文化符号"加速迁移。"
                        }
                    ]
                },
                "coinCreateTime": 1754936983000,
                "heatRaw": 428.23416227949986,
                "heatEma": 428.23416227949986,
                "createTime": "2026-04-30 12:01:02",
                "tweetIdList": [
                    "2048614663433425050"
                ],
                "coinKey": "SOL_4UeLCRqARmfb6e6KQijtiktqqXUxbfk6jZng7DhuBAGS"
            }
        ],
        "extend": ""
    },
    "msg": "操作成功",
    "reqId": "2049732978247229440"
}
```

---

## 2. 推文热度数据

**接口地址**: `POST /v3/twitter-tweets-heat`

**接口描述**: 查询推文热度数据

**请求参数**:

| 参数名称 | 字段说明 | 是否必须 | 数据类型 |
|----------|----------|----------|----------|
| | 推文id列表 | true | array |

**响应参数**:

| 参数名称 | 字段说明 | 数据类型 |
|----------|----------|----------|
| snapshootTime | 快照时间 | string |
| tweetId | 推文ID | string |
| userId | 用户ID | string |
| keyword | 搜索关键词 | string |
| tweetText | 推文内容 | string |
| tweetTime | 推文时间 | string |
| views | 浏览数量 | number |
| replies | 回复数量 | number |
| retweets | 转发数量 | number |
| likes | 点赞数量 | number |

**响应示例**:

```json
{
    "code": 200,
    "data": [
        {
            "snapshootTime": "2026-04-17 16:00:00",
            "tweetId": "1780000000000000001",
            "userId": "123456789",
            "keyword": "SOUL",
            "tweetText": "Just bought some $SOUL, this is going to moon! #SOL #DeFi",
            "tweetTime": "2026-04-17 15:30:00",
            "views": 15823,
            "replies": 42,
            "retweets": 128,
            "likes": 356
        }
    ],
    "msg": "操作成功",
    "reqId": "2043948786527789005"
}
```

---

## 输出规则

### 默认输出字段

**coin-heat-page**：address, symbol, displayHeat, priceFluctuationRatio, heatFluctuation, heatFluctuationRatio

**twitter-tweets-heat**：tweetId, userId, tweetText, tweetTime, views, replies, retweets, likes

### 详细信息输出

当用户要求查看详细信息时，输出完整响应字段，包含 aiSummary、heatTopKol、priceTrend 等嵌套数据
