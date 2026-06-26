# FlyAI 命令参考

> ⚠️ SSL 证书问题：执行 flyai 命令时，需在命令前添加环境变量绕过 SSL 验证：
> ```bash
> NODE_TLS_REJECT_UNAUTHORIZED=0 flyai <command>
> ```

## fliggy-fast-search

自然语言全品类搜索，一次查询覆盖机票、酒店、门票、旅游等所有品类。

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai fliggy-fast-search --query "[自然语言查询]"
```

**示例**：
```bash
flyai fliggy-fast-search --query "杭州3日游"
flyai fliggy-fast-search --query "法国签证"
flyai fliggy-fast-search --query "上海邮轮"
```

---

## search-flight

结构化机票搜索，支持深度筛选。

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "[出发城市]" \
  --destination "[目的地]" \
  --dep-date [出发日期] \
  --back-date [返回日期]
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--origin` | 出发城市或机场 | ✅ |
| `--destination` | 到达城市或机场 | |
| `--dep-date` | 出发日期 YYYY-MM-DD | |
| `--dep-date-start/end` | 出发日期范围 | |
| `--back-date` | 返回日期 | |
| `--back-date-start/end` | 返回日期范围 | |
| `--journey-type` | 1=直飞 2=中转 | |
| `--seat-class-name` | 舱位等级 | |
| `--transport-no` | 航班号 | |
| `--transfer-city` | 中转城市 | |
| `--dep-hour-start/end` | 出发时间范围 (0-23) | |
| `--arr-hour-start/end` | 到达时间范围 (0-23) | |
| `--total-duration-hour` | 最长飞行时长（小时） | |
| `--max-price` | 价格上限 | |
| `--sort-type` | 排序方式（见下表） | |

### 排序方式 (sort-type)

| 值 | 说明 |
|----|------|
| 1 | 价格降序 |
| 2 | 推荐排序 |
| 3 | 价格升序 |
| 4 | 时长升序 |
| 5 | 时长降序 |
| 6 | 早班优先 |
| 7 | 晚班优先 |
| 8 | 直飞优先 |

---

## search-hotels

结构化酒店搜索，支持星级、价格、位置筛选。

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotels \
  --dest-name "[目的地]" \
  --check-in-date [入住日期] \
  --check-out-date [退房日期]
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--dest-name` | 目的地（国家/省/城市/区） | ✅ |
| `--key-words` | 搜索关键词 | |
| `--poi-name` | 附近景点名称 | |
| `--hotel-types` | 酒店/民宿/客栈 | |
| `--sort` | 排序方式（见下表） | |
| `--check-in-date` | 入住日期 YYYY-MM-DD | |
| `--check-out-date` | 退房日期 YYYY-MM-DD | |
| `--hotel-stars` | 星级筛选，逗号分隔 "4,5" | |
| `--hotel-bed-types` | 大床房/双床房/多床房 | |
| `--max-price` | 每晚最高价格（CNY） | |

### 排序方式 (sort)

| 值 | 说明 |
|----|------|
| distance_asc | 距离近优先 |
| rate_desc | 评分高优先 |
| price_asc | 价格低优先 |
| price_desc | 价格高优先 |
| no_rank | 不排序 |

---

## search-poi

景点/活动搜索，支持类别和等级筛选。

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "[城市]"
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--city-name` | 城市名称 | ✅ |
| `--keyword` | 景点名称关键词 | |
| `--poi-level` | 景点等级 1-5 | |
| `--category` | 景点类别（见下方） | |

### 景点类别 (category)

**自然风光**：
- 自然风光、山湖田园、森林丛林、峡谷瀑布、沙滩海岛、沙漠草原

**人文古迹**：
- 人文古迹、古镇古村、历史古迹、园林花园、宗教场所

**主题乐园**：
- 主题乐园、水上乐园、影视基地、动物园、植物园、海洋馆

**文化场馆**：
- 体育场馆、演出赛事、剧院剧场、博物馆、纪念馆、展览馆

**城市休闲**：
- 地标建筑、市集、文创街区、城市观光

**户外活动**：
- 滑雪、漂流、冲浪、潜水、露营、温泉
