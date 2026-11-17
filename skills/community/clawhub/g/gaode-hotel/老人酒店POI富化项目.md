# 老人酒店 POI 富化项目

## 背景

高德 POI 库里的酒店数据目前缺乏适老化维度的标签。老人订酒店的三大核心需求是：别摔着、别累着、别饿着。数据来源：2026年调研，超过40%老年旅行者选四五星酒店，平均行程5.5–12.6天，偏好山岳风光和人文历史景区。

## 第一阶段：MVP 标签（可自动化，立即落地）

两个标签，完全依赖高德 `/nearby` 接口，无需人工介入：

| 标签字段 | 含义 | 打标逻辑 |
|---------|------|---------|
| `near_hospital` | 500m 内有医院或诊所 | 以酒店坐标调 `/nearby?category=医疗保健服务&radius_m=500`，有结果则打 `true` |
| `near_pharmacy` | 500m 内有药店 | 以酒店坐标调 `/nearby?category=购物服务&radius_m=500`，关键词匹配"药店/药房/大药房"，有结果则打 `true` |

数据写入目标：**独立表 `poi_elderly_tags`**，不写回 poi 主表。理由：一店多源可留版本、Phase 2 加 NLP 列不用 ALTER 4.9GB 主表、不影响线上 MCP 读主表。

```sql
CREATE TABLE poi_elderly_tags (
    poi_id        TEXT PRIMARY KEY,
    near_hospital BOOLEAN,
    near_pharmacy BOOLEAN,
    enriched_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

查询走 LEFT JOIN，主键扫描性能没问题。Phase 2 来了直接 `ALTER TABLE poi_elderly_tags ADD COLUMN has_elevator BOOLEAN`——只动这张小表。

## 第二阶段：NLP 解析标签（需解析酒店描述文本）

待飞猪或其他渠道能拿到酒店描述字段后，用 NLP 提取：

| 标签字段 | 关键词 |
|---------|-------|
| `has_elevator` | 电梯、直达 |
| `has_accessible` | 无障碍、坡道、轮椅、扶手 |
| `bathroom_antislip` | 防滑、扶手、浴室安全 |
| `has_emergency_call` | 紧急呼叫、SOS |
| `breakfast_chinese_hot` | 中式早餐、热食、粥 |

## 第三阶段：结构化筛选能力

在 travel_agent.py 里新增 `--senior-friendly` 开关，自动加上 `near_hospital=true OR near_pharmacy=true` 过滤条件，输出结果额外展示步行距离最近的医院和药店。

## 实施路径

1. 写一个批处理脚本，遍历 poi.sqlite 里 `cat='住宿服务'` 的记录，调 `/nearby` 写两列——预计半天完成
2. 在 travel_agent.py 加 `--senior-friendly` 参数，查询时读两列过滤
3. Hackathon 演示时作为差异化卖点：别家只有位置锚定，我们还有适老化筛选

## 关联项目

- `travel_agent.py`：当前 v1.0.1，位于 `飞猪联动/`
- POI 数据库：`poi.sqlite`（4.9GB），102城 995万条
- 高德 `/nearby` API：`http://82.156.169.110/poi/v1/nearby`
