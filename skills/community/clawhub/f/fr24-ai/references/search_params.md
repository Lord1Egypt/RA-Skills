# Skill 搜索参数说明（对应 ApiSearchRq）

## searchLegs[]

| 字段 | 必填 | 格式 |
|------|------|------|
| origin | 是 | IATA 三字码 |
| destination | 是 | IATA 三字码 |
| depDate | 是 | `YYYY-MM-DD` |
| typeO / typeD | 否 | `airportcode` 或 `airportgroup` |

## 行程类型

- 1 段 → 单程
- 2 段且 A→B、B→A → 往返
- 其他 → Skill 拒绝（307902）

## 乘客

- adultNum ≥ 1
- 成人+儿童 ≤ 9；儿童 ≤ 成人×2

## preferences

| 字段 | 默认 |
|------|------|
| cabin | Y |
| stops | 2（直飞填 0） |
| resultCtrl | 15（≤20） |
| preferredCarrier | 可选，IATA 列表，如 `["CA"]`（export 搜索时过滤） |
| prohibitedCarrier | 可选，排除航司 |
| depTimeWindow | 可选，`{"from":"11:00","to":"13:00"}`，仅客户端汇总时按首段起飞时间过滤 |
| depTimeLabel | 可选，展示用，如「约12点起飞」 |

## 重新搜索（refine）

用户对结果不满意时：

```bash
python scripts/nl_to_search.py refine --text "要国航，中午12点左右起飞"
python scripts/skill_search_client.py search --payload-file .cache/pending_search.json
```

`refine` 不扣配额；`search` 扣 1 次。
