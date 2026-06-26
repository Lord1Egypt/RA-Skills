# FlyAI 命令参考

> ⚠️ **重要**：所有命令执行前需加 `NODE_TLS_REJECT_UNAUTHORIZED=0` 解决 SSL 证书验证问题

## 目录

1. [keyword-search - 自然语言搜索](#keyword-search)
2. [search-flight - 机票搜索](#search-flight)
3. [search-hotel - 酒店搜索](#search-hotel)
4. [search-poi - 景点搜索](#search-poi)

---

## keyword-search

自然语言搜索，跨所有旅行类别（酒店、机票、门票、签证、邮轮等）。

**适用场景**：
- 攻略中模糊描述的信息匹配（如"洱海边那家网红民宿"）
- 快速探索某个目的地的综合信息
- 不确定具体分类时的通用搜索

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "[搜索词]"
```

**示例**：
```bash
# 搜索大理的无边泳池民宿
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "大理洱海边无边泳池民宿"

# 搜索云南的旅行产品
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "云南5天4晚跟团游"
```

---

## search-flight

结构化机票搜索，支持丰富的筛选条件。

**适用场景**：
- 替换攻略中的航班信息（不同出发城市）
- 比较多个日期的机票价格
- 筛选特定条件的航班（直飞、时段、舱位等）

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "[出发城市]" \
  --destination "[目的地城市]" \
  --dep-date [出发日期] \
  [其他可选参数]
```

**完整参数列表**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--origin` | 出发城市（必填） | "上海" |
| `--destination` | 目的地城市 | "大理" |
| `--dep-date` | 出发日期 (YYYY-MM-DD) | 2026-08-10 |
| `--dep-date-start` | 出发日期范围起始 | 2026-08-01 |
| `--dep-date-end` | 出发日期范围结束 | 2026-08-31 |
| `--back-date` | 返程日期 | 2026-08-14 |
| `--back-date-start` | 返程日期范围起始 | 2026-08-13 |
| `--back-date-end` | 返程日期范围结束 | 2026-08-15 |
| `--journey-type` | 1=直飞, 2=中转 | 1 |
| `--seat-class-name` | 舱位名称 | "经济舱" |
| `--transport-no` | 航班号 | "MU5819" |
| `--transfer-city` | 中转城市 | "昆明" |
| `--dep-hour-start` | 出发时间起始（小时） | 6 |
| `--dep-hour-end` | 出发时间结束（小时） | 12 |
| `--arr-hour-start` | 到达时间起始 | 14 |
| `--arr-hour-end` | 到达时间结束 | 22 |
| `--total-duration-hour` | 最大飞行时长（小时） | 5 |
| `--max-price` | 最高价格（元） | 1500 |
| `--sort-type` | 排序方式（见下表） | 3 |

**排序类型**：
| sort-type | 说明 |
|-----------|------|
| 1 | 价格降序（贵→便宜） |
| 2 | 推荐排序 |
| 3 | 价格升序（便宜→贵）✅ 常用 |
| 4 | 时长升序（短→长） |
| 5 | 时长降序 |
| 6 | 起飞早→晚 |
| 7 | 起飞晚→早 |
| 8 | 直飞优先 |

**常用示例**：
```bash
# 基础往返搜索，按价格排序
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "大理" \
  --dep-date 2026-08-10 --back-date 2026-08-14 \
  --sort-type 3

# 只要直飞，早上出发
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "北京" --destination "三亚" \
  --dep-date 2026-08-10 \
  --journey-type 1 --dep-hour-start 6 --dep-hour-end 12

# 预算有限，最高1000元
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "杭州" --destination "成都" \
  --dep-date 2026-08-10 \
  --max-price 1000 --sort-type 3
```

---

## search-hotel

结构化酒店搜索，支持位置、星级、价格等筛选。

**适用场景**：
- 验证攻略中推荐的酒店是否有房
- 搜索同区域的替代酒店
- 按特定条件筛选酒店（星级、房型、价格等）

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "[目的地]" \
  [其他可选参数]
```

**完整参数列表**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--dest-name` | 目的地（必填） | "大理" |
| `--key-words` | 搜索关键词 | "云隐山房" |
| `--poi-name` | 附近景点名 | "洱海" |
| `--hotel-types` | 酒店类型 | "民宿" |
| `--sort` | 排序方式 | "rate_desc" |
| `--check-in-date` | 入住日期 | 2026-08-10 |
| `--check-out-date` | 退房日期 | 2026-08-12 |
| `--hotel-stars` | 星级（逗号分隔） | "4,5" |
| `--hotel-bed-types` | 房型 | "大床房" |
| `--max-price` | 最高价格/晚 | 800 |

**酒店类型**：
- `酒店` - 标准酒店
- `民宿` - 民宿/客栈
- `客栈` - 传统客栈

**排序方式**：
- `distance_asc` - 距离近→远
- `rate_desc` - 评分高→低 ✅ 常用
- `price_asc` - 价格低→高
- `price_desc` - 价格高→低
- `no_rank` - 默认排序

**房型**：
- `大床房` - 大床
- `双床房` - 双床
- `多床房` - 多床

**常用示例**：
```bash
# 验证原攻略推荐的酒店
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "大理" --key-words "云隐山房" \
  --check-in-date 2026-08-10 --check-out-date 2026-08-12

# 搜索洱海边的高评分民宿
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "大理" --poi-name "洱海" \
  --hotel-types "民宿" --sort rate_desc \
  --check-in-date 2026-08-10 --check-out-date 2026-08-12

# 预算有限，找500以内的
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "丽江" --max-price 500 \
  --sort price_asc \
  --check-in-date 2026-08-12 --check-out-date 2026-08-14
```

---

## search-poi

景点/活动搜索，支持分类和等级筛选。

**适用场景**：
- 验证攻略中提到的景点是否存在
- 补充景点的门票、开放时间等信息
- 发现攻略中未提到的当地景点

**命令格式**：
```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "[城市]" \
  [其他可选参数]
```

**完整参数列表**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--city-name` | 城市（必填） | "大理" |
| `--keyword` | 景点关键词 | "洱海" |
| `--poi-level` | 景点等级 (1-5) | 5 |
| `--category` | 景点分类 | "自然风光" |

**景点分类**：
- 自然风光：`自然风光`、`山湖田园`、`森林丛林`、`峡谷瀑布`、`沙滩海岛`、`沙漠草原`
- 人文古迹：`人文古迹`、`古镇古村`、`历史古迹`、`园林花园`、`宗教场所`
- 主题乐园：`主题乐园`、`水上乐园`、`影视基地`、`动物园`、`植物园`、`海洋馆`
- 文化场馆：`博物馆`、`纪念馆`、`展览馆`、`体育场馆`
- 演出活动：`演出赛事`、`剧院剧场`
- 城市观光：`地标建筑`、`市集`、`文创街区`、`城市观光`
- 户外运动：`滑雪`、`漂流`、`冲浪`、`潜水`、`露营`、`温泉`

**常用示例**：
```bash
# 搜索大理的所有景点
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi --city-name "大理"

# 搜索指定景点验证信息
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "大理" --keyword "苍山感通索道"

# 搜索5A级景点
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "丽江" --poi-level 5

# 按分类搜索
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "西安" --category "历史古迹"
```

---

## 返回数据提取

FlyAI 返回 JSON 格式数据，关键字段：

### 机票数据
```json
{
  "flightNo": "MU5819",        // 航班号
  "depTime": "07:30",          // 出发时间
  "arrTime": "11:20",          // 到达时间
  "price": 1080,               // 价格
  "jumpUrl": "https://..."     // 飞猪预订链接
}
```

### 酒店数据
```json
{
  "hotelName": "云隐山房",     // 酒店名
  "star": 4,                   // 星级
  "score": 4.8,                // 评分
  "price": 580,                // 价格
  "jumpUrl": "https://..."     // 飞猪预订链接
}
```

### 景点数据
```json
{
  "poiName": "苍山感通索道",   // 景点名
  "level": "4A",               // 等级
  "ticketPrice": 115,          // 门票价格
  "openTime": "08:30-17:00",   // 开放时间
  "jumpUrl": "https://..."     // 购票链接
}
```

**提取预订链接**：从返回数据的 `jumpUrl` 字段获取飞猪直接预订链接。
