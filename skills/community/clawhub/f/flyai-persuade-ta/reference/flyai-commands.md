# FlyAI 命令参考

> ⚠️ **重要**：所有命令需加 `NODE_TLS_REJECT_UNAUTHORIZED=0` 前缀绕过 SSL 验证

## search-flight — 搜索机票

查询航班信息，用于获取真实机票价格。

### 基础用法

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "巴厘岛" \
  --dep-date 2026-04-15 --back-date 2026-04-20 \
  --sort-type 3
```

### 完整参数

| 参数 | 说明 | 示例 |
|-----|------|------|
| --origin | 出发城市（必填） | "上海"、"北京" |
| --destination | 目的地城市 | "巴厘岛"、"东京" |
| --dep-date | 出发日期（YYYY-MM-DD） | 2026-04-15 |
| --back-date | 返回日期 | 2026-04-20 |
| --journey-type | 1=直飞，2=转机 | 1 |
| --max-price | 价格上限 | 3000 |
| --sort-type | 1=价格降序，3=价格升序，6=早出发 | 3 |

### 说服场景应用

```bash
# 证明"其实机票没那么贵"
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "曼谷" \
  --dep-date 2026-05-01 --sort-type 3 --max-price 2000
```

---

## search-hotel — 搜索酒店

查询酒店信息，用于获取真实住宿价格。

### 基础用法

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "巴厘岛" \
  --check-in-date 2026-04-15 --check-out-date 2026-04-18 \
  --sort price_asc
```

### 完整参数

| 参数 | 说明 | 示例 |
|-----|------|------|
| --dest-name | 目的地（必填） | "巴厘岛"、"三亚" |
| --check-in-date | 入住日期 | 2026-04-15 |
| --check-out-date | 退房日期 | 2026-04-18 |
| --hotel-stars | 星级（1-5） | "4,5" |
| --max-price | 每晚价格上限 | 500 |
| --sort | 排序方式 | price_asc / rate_desc |
| --poi-name | 附近景点 | "海神庙" |

### 说服场景应用

```bash
# 证明"泳池别墅也不贵"
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "巴厘岛" --key-words "泳池别墅" \
  --check-in-date 2026-04-15 --check-out-date 2026-04-18 \
  --sort price_asc --max-price 800
```

---

## search-poi — 搜索景点

查询目的地景点信息。

### 基础用法

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "巴厘岛"
```

### 完整参数

| 参数 | 说明 | 示例 |
|-----|------|------|
| --city-name | 城市名（必填） | "巴厘岛"、"东京" |
| --keyword | 关键词 | "寺庙"、"海滩" |
| --category | 分类 | "自然风光"、"历史古迹" |
| --poi-level | 等级（1-5） | 5 |

### 景点分类选项

- 自然风光：山湖田园、森林丛林、峡谷瀑布、沙滩海岛、沙漠草原
- 人文古迹：古镇古村、历史古迹、园林花园、宗教场所
- 主题乐园：水上乐园、影视基地、动物园、海洋馆
- 演出赛事：剧院剧场、博物馆、纪念馆
- 户外活动：滑雪、漂流、冲浪、潜水、露营、温泉

---

## keyword-search — 通用搜索

自然语言搜索，适合获取综合信息。

### 基础用法

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search \
  --query "巴厘岛5天4晚攻略"
```

### 说服场景应用

```bash
# 获取签证信息（回应"签证麻烦"顾虑）
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search \
  --query "巴厘岛签证 中国免签"

# 获取安全信息（回应"不安全"顾虑）
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search \
  --query "巴厘岛 安全 治安"
```

---

## 命令组合策略

### 场景：证明"巴厘岛其实不贵"

```bash
# 1. 搜索低价机票
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "巴厘岛" \
  --dep-date 2026-08-14 --back-date 2026-08-18 \
  --sort-type 3

# 2. 搜索经济型酒店
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "巴厘岛" \
  --check-in-date 2026-08-14 --check-out-date 2026-08-18 \
  --sort price_asc

# 3. 搜索景点门票
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi \
  --city-name "巴厘岛"
```

### 场景：证明"只请2天能玩5天"

```bash
# 搜索周五出发周二回的航班（请假周一周二）
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "曼谷" \
  --dep-date 2026-05-01 --back-date 2026-05-05 \
  --sort-type 3
```
