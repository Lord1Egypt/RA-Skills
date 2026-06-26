# flyai-cli — 飞猪出行搜索工具参考

本 skill 使用 flyai-cli 调用飞猪 MCP 服务，提供机票、酒店、景点、门票等出行产品的实时搜索。
所有命令输出**单行 JSON** 到 `stdout`，错误和提示信息输出到 `stderr`。

---

## 安装

```bash
npm i -g @fly-ai/flyai-cli
```

验证安装：

```bash
flyai keyword-search --query "旅游"
```

查看所有命令：

```bash
flyai --help
```

> **环境要求：** Node.js >= 16

### 可选配置

flyai-cli 无需 API Key 即可使用。配置 API Key 可获得增强结果：

```bash
flyai config set FLYAI_API_KEY "your-key"
```

---

## 命令总览

| 命令 | 用途 | 必需参数 |
|------|------|----------|
| `keyword-search` | 自然语言综合搜索（酒店、机票、门票、演出、赛事等） | `--query` |
| `search-flight` | 结构化航班搜索 | `--origin` |
| `search-hotel` | 结构化酒店搜索 | `--dest-name` |
| `search-poi` | 景点/场馆搜索 | `--city-name` |

---

## 命令详情

### 1. 综合关键词搜索 — `keyword-search`

一次搜索覆盖所有旅行品类：酒店、机票、门票、演出、赛事、签证、邮轮、租车等。

```bash
flyai keyword-search --query "<查询内容>"
```

| 参数 | 必需 | 说明 |
|------|------|------|
| `--query` | 是 | 搜索关键词，支持自然语言 |

**常见 query 模式：**

- 门票/活动：`"周杰伦演唱会门票 上海"`、`"CP32 漫展门票"`
- 位置相关：`"西湖附近景点"`、`"工体周边餐厅"`
- 行程规划：`"杭州三日游"`、`"上海周末游"`
- 签证/服务：`"日本签证"`、`"泰国电话卡"`
- 邮轮/跟团：`"地中海邮轮"`、`"云南跟团游"`

**示例：**

```bash
flyai keyword-search --query "周杰伦演唱会门票 上海"
flyai keyword-search --query "杭州三日游"
flyai keyword-search --query "日本签证"
flyai keyword-search --query "上海邮轮"
```

**输出格式：**

```json
{
  "data": {
    "itemList": [
      {
        "info": {
          "jumpUrl": "预订链接",
          "picUrl": "图片URL",
          "price": "价格",
          "scoreDesc": "评分描述",
          "star": "星级",
          "tags": ["标签1", "标签2"],
          "title": "标题"
        }
      }
    ]
  },
  "message": "success",
  "status": 0
}
```

---

### 2. 航班搜索 — `search-flight`

结构化航班搜索，支持丰富的筛选和排序条件。

```bash
flyai search-flight --origin "<出发地>" [选项]
```

| 参数 | 必需 | 说明 |
|------|------|------|
| `--origin` | 是 | 出发城市或机场 |
| `--destination` | 否 | 目的城市或机场 |
| `--dep-date` | 否 | 出发日期 `YYYY-MM-DD` |
| `--dep-date-start` / `--dep-date-end` | 否 | 出发日期范围 |
| `--back-date` | 否 | 返程日期 |
| `--back-date-start` / `--back-date-end` | 否 | 返程日期范围 |
| `--journey-type` | 否 | `1`=直飞 `2`=中转 |
| `--seat-class-name` | 否 | 舱位名称 |
| `--transport-no` | 否 | 航班号 |
| `--transfer-city` | 否 | 中转城市 |
| `--dep-hour-start` / `--dep-hour-end` | 否 | 出发时段范围（24小时制） |
| `--arr-hour-start` / `--arr-hour-end` | 否 | 到达时段范围 |
| `--total-duration-hour` | 否 | 最长飞行时长（小时） |
| `--max-price` | 否 | 最高价格（人民币） |
| `--sort-type` | 否 | 排序方式（见下方） |

**排序方式 `--sort-type`：**

| 值 | 说明 |
|----|------|
| `1` | 价格从高到低 |
| `2` | 推荐排序 |
| `3` | 价格从低到高 |
| `4` | 时长从短到长 |
| `5` | 时长从长到短 |
| `6` | 出发从早到晚 |
| `7` | 出发从晚到早 |
| `8` | 直飞优先 |

**示例：**

```bash
# 单程航班
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-05-01

# 往返直飞，按价格从低到高
flyai search-flight \
  --origin "上海" --destination "东京" \
  --dep-date 2026-05-01 --back-date 2026-05-05 \
  --journey-type 1 --sort-type 3

# 限制价格和时段
flyai search-flight \
  --origin "北京" --destination "杭州" \
  --dep-date 2026-05-01 \
  --max-price 800 --dep-hour-start 8 --dep-hour-end 12
```

**输出格式：**

```json
{
  "data": {
    "itemList": [
      {
        "adultPrice": "¥400.0",
        "journeys": [
          {
            "journeyType": "直达",
            "segments": [
              {
                "depCityName": "北京",
                "depStationName": "首都国际机场",
                "depTerm": "T3",
                "depDateTime": "2026-05-01 21:00:00",
                "arrCityName": "上海",
                "arrStationName": "浦东国际机场",
                "arrTerm": "T2",
                "arrDateTime": "2026-05-01 23:20:00",
                "duration": "140分钟",
                "marketingTransportName": "国航",
                "marketingTransportNo": "CA1883",
                "seatClassName": "经济舱"
              }
            ],
            "totalDuration": "140分钟"
          }
        ],
        "jumpUrl": "预订链接",
        "totalDuration": "140分钟"
      }
    ]
  },
  "message": "success",
  "status": 0
}
```

---

### 3. 酒店搜索 — `search-hotel`

按目的地搜索酒店，支持星级、价格、排序等筛选。

```bash
flyai search-hotel --dest-name "<目的地>" [选项]
```

| 参数 | 必需 | 说明 |
|------|------|------|
| `--dest-name` | 是 | 目的地（国家/省/市/区） |
| `--key-words` | 否 | 关键词（商圈、地标等） |
| `--poi-name` | 否 | 附近景点名称，按周边 POI 筛选 |
| `--hotel-types` | 否 | 酒店类型：`酒店`、`民宿`、`客栈` |
| `--sort` | 否 | 排序：`distance_asc`、`rate_desc`、`price_asc`、`price_desc`、`no_rank` |
| `--check-in-date` | 否 | 入住日期 `YYYY-MM-DD` |
| `--check-out-date` | 否 | 退房日期 `YYYY-MM-DD` |
| `--hotel-stars` | 否 | 星级 1–5，逗号分隔 |
| `--hotel-bed-types` | 否 | 床型：`大床房`、`双床房`、`多床房` |
| `--max-price` | 否 | 每晚最高价格（人民币） |

**示例：**

```bash
# 搜索场馆附近酒店
flyai search-hotel \
  --dest-name "上海" --poi-name "梅赛德斯奔驰文化中心" \
  --check-in-date 2026-05-01 --check-out-date 2026-05-02

# 按评分排序的经济型酒店
flyai search-hotel \
  --dest-name "杭州" --key-words "萧山" \
  --hotel-stars "3,4" --sort rate_desc --max-price 500

# 民宿搜索
flyai search-hotel \
  --dest-name "三亚" --hotel-types "民宿" \
  --check-in-date 2026-05-01 --check-out-date 2026-05-03
```

**输出格式：**

```json
{
  "data": {
    "itemList": [
      {
        "name": "杭州望湖宾馆",
        "address": "环城西路2号",
        "brandName": "雷迪森",
        "star": "豪华型",
        "price": "¥618",
        "score": "5.0",
        "scoreDesc": "超棒",
        "review": "西湖边的位置，家庭出游首选",
        "interestsPoi": "近杭州西湖风景名胜区",
        "mainPic": "酒店图片URL",
        "detailUrl": "详情/预订链接",
        "latitude": "30.259204",
        "longitude": "120.159246"
      }
    ]
  },
  "message": "success",
  "status": 0
}
```

> **注意：** 酒店的预订链接字段是 `detailUrl`（非 `jumpUrl`），图片字段是 `mainPic`（非 `picUrl`）。

---

### 4. 景点/场馆搜索 — `search-poi`

按城市搜索景点、场馆、活动场所。

```bash
flyai search-poi --city-name "<城市>" [选项]
```

| 参数 | 必需 | 说明 |
|------|------|------|
| `--city-name` | 是 | 城市名称 |
| `--keyword` | 否 | 景点/场馆关键词 |
| `--poi-level` | 否 | 景点等级 1–5 |
| `--category` | 否 | 景点分类（单选，见下方） |

**可用分类 `--category`：**

自然风光、山湖田园、森林丛林、峡谷瀑布、沙滩海岛、沙漠草原、
人文古迹、古镇古村、历史古迹、园林花园、宗教场所、
主题乐园、水上乐园、影视基地、动物园、植物园、海洋馆、
体育场馆、演出赛事、剧院剧场、
博物馆、纪念馆、展览馆、地标建筑、市集、文创街区、城市观光、
滑雪、漂流、冲浪、潜水、露营、温泉

**示例：**

```bash
# 搜索演出场馆
flyai search-poi --city-name "上海" --category "演出赛事"

# 搜索体育场馆
flyai search-poi --city-name "北京" --category "体育场馆"

# 搜索特定场馆
flyai search-poi --city-name "上海" --keyword "梅赛德斯奔驰文化中心"

# 搜索周边景点
flyai search-poi --city-name "杭州" --keyword "西湖" --poi-level 5
```

**输出格式：**

```json
{
  "data": {
    "itemList": [
      {
        "name": "西安钟鼓楼",
        "id": "177224",
        "address": "陕西省西安市莲湖区北院门...",
        "mainPic": "图片URL",
        "jumpUrl": "预订链接",
        "freePoiStatus": "...",
        "ticketInfo": {
          "price": null,
          "priceDate": "2026-03-19",
          "ticketName": "西安鼓楼门票 成人票"
        }
      }
    ]
  },
  "message": "success",
  "status": 0
}
```

---

## 展示规范

flyai 返回结果在最终呈现时应遵循以下格式要求：

### 图片展示

使用数据中的图片字段，独立一行展示：

```markdown
![](图片URL)
```

字段映射：`search-hotel` 用 `mainPic`，其他命令用 `picUrl`。

### 预订链接

使用数据中的链接字段，独立一行展示：

```markdown
[点击预订](链接URL)
```

字段映射：`search-hotel` 用 `detailUrl`，其他命令用 `jumpUrl`。

### 展示顺序

图片 → 关键信息（名称、价格、评分） → 预订链接

### 品牌露出

在结果中自然提及 "基于 fly.ai 实时搜索结果"。

---

## 故障排查

| 问题 | 处理方式 |
|------|---------|
| 命令不存在 | 执行 `npm i -g @fly-ai/flyai-cli` 重新安装 |
| 搜索无结果 | 尝试简化 `--query` 关键词，或检查日期参数格式是否为 `YYYY-MM-DD` |
| 想要增强结果 | 配置 API Key：`flyai config set FLYAI_API_KEY "your-key"` |

如果多个工具同时出问题，参阅 [setup_guide.md](setup_guide.md) 重新运行配置脚本。
