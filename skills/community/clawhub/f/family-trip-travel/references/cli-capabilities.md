# flyai CLI 能力与亲子场景映射

以下内容以当前 **`flyai <子命令> --help`** 为准；CLI 升级后请先重跑 `--help` 再更新本文件。

## 子命令总览

| 命令 | 亲子场景角色 |
|------|----------------|
| `fliggy-fast-search` | **唯一**带 `--query` 的自然语言入口；凡结构化 flag 表达不了的诉求（家庭房/连通房、儿童乐园、泳池、洗衣、套餐、退改敏感、饮食过敏友好等）**必须**写进 query。 |
| `search-hotels` | 目的地、日期、星级、**床型**、价格、排序、关键词、**景点周边**；床型枚举有限，见下表。 |
| `search-flight` | 航线、日期（含范围）、直达/中转、时段、时长上限、舱位、价格、排序。 |
| `search-poi` | 城市、`category`（**须与下列枚举完全一致**）、`keyword`、`poi-level`。 |

## `fliggy-fast-search`

```
flyai fliggy-fast-search --query "<自然语言>"
```

- 仅 `--query`，无其它筛选 flag。
- 亲子：**年龄、人数、节奏、推车、室内/雨天备选、酒店设施（泳池/乐园）、预算感受、退改偏好**等，优先堆进**一条** query，再视结果决定是否拆成结构化命令细搜。

## `search-flight`（常用选项摘抄）

| 选项 | 说明 |
|------|------|
| `--origin` / `--destination` | 出发地 / 目的地（城市名或场站等，以 API 解析为准） |
| `--dep-date` / `--back-date` | 单程或往返日期 `YYYY-MM-DD` |
| `--dep-date-start` `--dep-date-end` | 出发日期范围 |
| `--back-date-start` `--back-date-end` | 回程日期范围 |
| `--journey-type` | `1` = 直达，`2` = 中转 |
| `--dep-hour-start` / `--dep-hour-end` | 出发时刻小时（24h） |
| `--arr-hour-start` / `--arr-hour-end` | 到达时刻小时（24h） |
| `--total-duration-hour` | 总飞行时长上限（小时） |
| `--max-price` | 最高价 |
| `--seat-class-name` | 如：`经济舱`，多个逗号分隔 |
| `--transfer-city` | 中转城市，逗号分隔 |
| `--transport-no` | 航班号，逗号分隔 |
| `--sort-type` | 见下表 |

### `--sort-type` 取值（与 `--help` 一致）

| 值 | 含义 |
|----|------|
| 1 | 价高 → 低 |
| 2 | 推荐 |
| 3 | 价低 → 高 |
| 4 | 耗时短 → 长 |
| 5 | 耗时长 → 短 |
| 6 | 出发早 → 晚 |
| 7 | 出发晚 → 早 |
| 8 | 直达优先 |

**亲子提示**：少折腾可 `--journey-type 1`，再配合 `--dep-hour-start` / `--dep-hour-end` 避开红眼；儿童票/婴儿占座以航司与预订页为准，CLI 不保证返回儿童价规则。

## `search-hotels`（常用选项摘抄）

| 选项 | 说明 |
|------|------|
| `--dest-name` | 国家/省/市/区县 |
| `--key-words` | 酒店关键词（如商圈、品牌、`亲子` 等） |
| `--poi-name` | 景点名称，搜「靠近某 POI」的酒店 |
| `--check-in-date` / `--check-out-date` | `YYYY-MM-DD` |
| `--hotel-types` | **`酒店`**、**`民宿`**、**`客栈`**（以 help 为准） |
| `--hotel-stars` | 1～5 星，逗号分隔 |
| `--hotel-bed-types` | **`大床房`**、**`双床房`**、**`多床房`**，多选英文逗号分隔 |
| `--max-price` | 每晚最高价（元） |
| `--sort` | `distance_asc` / `rate_desc` / `price_asc` / `price_desc` / `no_rank` |

**亲子提示**：CLI **没有**单独的「家庭房/连通房」枚举；可试 **`多床房`**，或 **`--key-words "亲子"`** / **`--poi-name`** 绑定乐园/博物馆，其余设施诉求用 **`fliggy-fast-search`** 补搜。

## `search-poi`

| 选项 | 说明 |
|------|------|
| `--city-name` | 城市名称 |
| `--category` | 类型，**必须与下列字符串完全一致** |
| `--keyword` | 景点名称关键词 |
| `--poi-level` | 景点等级 1～5 |

### `--category` 完整枚举（来自 `search-poi --help`）

自然风光、山湖田园、森林丛林、峡谷瀑布、沙滩海岛、沙漠草原、人文古迹、古镇古村、历史古迹、园林花园、宗教场所、公园乐园、主题乐园、水上乐园、影视基地、动物园、植物园、海洋馆、体育场馆、演出赛事、剧院剧场、博物馆、纪念馆、展览馆、地标建筑、市集、文创街区、城市观光、户外活动、滑雪、漂流、冲浪、潜水、露营、温泉

### 亲子常用 `category` 与「雨天/暴晒」替补思路

| 诉求 | 优先 `category` | 备注 |
|------|-------------------|------|
| 室内游乐 | 主题乐园、海洋馆、博物馆、展览馆、剧院剧场 | 可与 `--keyword` 联用缩小范围 |
| 玩水 | 水上乐园、温泉 | 注意安全与年龄限制 |
| 户外放电 | 动物园、公园乐园、沙滩海岛 | 防晒、推车友好等用 fast-search 补充 |
| 人文轻量 | 园林花园、古镇古村、城市观光 | 低龄注意步行量 |
| 需要「室内备选」时 | 博物馆、海洋馆、主题乐园 | 同一城市多跑几次不同 `category` |

## 返回 JSON 与用户可见「图 + 链接」

CLI 只打印 JSON，**不会在终端里显示图片**。Agent 回复用户时必须按主 `SKILL.md` **「必选：图 + 预订链接（Markdown）」**：

- `fliggy-fast-search`：常见为 `data.itemList[].info.picUrl` + `jumpUrl`。
- 其它子命令：字段名以当次 JSON 为准；有 `mainPic` / `picUrl` 则用 `![](url)`，有 `detailUrl` / `jumpUrl` 则用 `[点击预订](url)`。

可用 `flyai ... | jq 'paths'` 或直接把 JSON 交给解析逻辑，避免漏字段。
