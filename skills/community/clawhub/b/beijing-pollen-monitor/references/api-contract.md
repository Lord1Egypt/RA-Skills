# 北京花粉监测 API 约定

封装北京公共花粉监测 API，提供统一的 shell 入口：

```bash
./scripts/beijing-pollen-query.sh query --mode <report|overview|stations|history|forecast|daily> [options]
```

## 依赖

运行时需要：`bash`、`curl`、`jq`

缺少 `jq` 时脚本以退出码 `1` 退出并输出 JSON 错误信息。

## 上游 API

- `GET /v1/weatherPollen/pollens` — 北京区域概览（16 个区）
- `GET /api/pollen/obs/latestPollenLevels` — 全部站点实时读数（16 个站点，每区一个）
- `GET /api/pollen/obs/history24?staId=...` — 单站点 24 小时序列
- `GET /v1/pollen/forecast?plantCode=zongleibie` — 北京区级总量等级预报
- `GET /v2/pollen/classify/forecast?areaCode=...` — 目标区分类花粉预报
- `GET /v1/pollen/legends` — 北京区级浓度等级说明

## 命令

晨报（推荐）：

```bash
./scripts/beijing-pollen-query.sh query --mode daily --district 朝阳
./scripts/beijing-pollen-query.sh query --mode daily --district 朝阳 --format text
```

即时查询简报：

```bash
./scripts/beijing-pollen-query.sh query --mode report --district 海淀
./scripts/beijing-pollen-query.sh query --mode report --district 海淀 --format text
```

概览：

```bash
./scripts/beijing-pollen-query.sh query --mode overview
```

站点：

```bash
./scripts/beijing-pollen-query.sh query --mode stations
```

历史：

```bash
./scripts/beijing-pollen-query.sh query --mode history --district 朝阳
./scripts/beijing-pollen-query.sh query --mode history --station-id 54398
```

预报：

```bash
./scripts/beijing-pollen-query.sh query --mode forecast --district 海淀
./scripts/beijing-pollen-query.sh query --mode forecast --district 海淀 --format text
```

## 参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--mode` | `report`、`overview`、`stations`、`history`、`forecast`、`daily` | `overview` |
| `--district` | 区名，模糊匹配（report/history/forecast/daily 必填） | — |
| `--station-id` | 站点 ID（history 替代方式） | — |
| `--format` | `json` 或 `text` | `json` |
| `--limit` | 热点站点数量上限 | `5` |
| `--timeout-ms` | HTTP 超时毫秒数 | `8000` |

可用区名：东城 西城 朝阳 海淀 丰台 石景山 门头沟 房山 通州 顺义 昌平 大兴 怀柔 平谷 密云 延庆

## 退出码

| 码 | 含义 |
|---|---|
| `0` | 成功 |
| `1` | 缺少依赖 |
| `2` | 参数错误（含 `district_not_found`） |
| `3` | 上游请求失败或业务错误 |
| `4` | 返回数据为空 |

## JSON 顶层结构

成功：

```json
{
  "ok": true,
  "mode": "daily",
  "generated_at": "2026-03-30T06:00:00Z",
  "query": { "mode": "daily", "district": "朝阳", "format": "json", "limit": 5 },
  "data": {},
  "warnings": []
}
```

失败：

```json
{
  "ok": false,
  "mode": null,
  "generated_at": "2026-03-30T06:00:00Z",
  "query": {},
  "warnings": [],
  "error": { "code": "district_not_found", "message": "No station found matching district: 成都. Available: ..." }
}
```

text 格式：

```json
{
  "ok": true,
  "mode": "daily",
  "format": "text",
  "generated_at": "...",
  "query": {},
  "data": { "text": "朝阳区花粉晨报（2026-03-30 08:00）\n\n当前监测：...\n..." },
  "warnings": []
}
```

## 模式约定

### `report`

自动完成：全市概览 + 目标站点 + 24h 历史。需要 `--district`。

`data` 字段：

```json
{
  "city_summary": {
    "area_count": 16,
    "avg_level_code": 2,
    "avg_level_text": "较低",
    "hotspots": [{ "station_id", "station_name", "display_value", "level_code", "level_text" }],
    "alerts": [{ "source", "name", "level_text", "display_value" }]
  },
  "target_station": {
    "station_id": "54399",
    "station_name": "海淀区",
    "current": {
      "display_value": "156",
      "level_code": 2,
      "level_text": "较低",
      "observed_at": "2026-03-30 08:00:00",
      "advice": "..."
    },
    "trend_24h": {
      "delta": -30,
      "direction": "falling",
      "min": 120,
      "max": 210,
      "series_points": 24,
      "latest_advice": "..."
    }
  }
}
```

`target_station.current` 追加：
- `value_family` — 固定为 `station_observation`
- `meaning` — summary_text, detail_text, source

### `overview`

`data` 字段：
- `beijing_areas[]` — area_id, name, raw_pollen, display_value, level_code, level_text, value_family, meaning, observed_at
- `stations[]` — station_id, station_name, raw_pollen, display_value, level_code, level_text, value_family, meaning, observed_at, advice
- `hotspots[]` — stations 的高风险子集，按等级和数值排序，受 `--limit` 限制
- `alerts[]` — source, entity_id, name, severity, level_code, level_text, display_value, observed_at, advice（可选）

### `stations`

`data` 字段：
- `stations[]` — 同 overview
- `alerts[]` — 同 overview

### `history`

`data` 字段：
- `station` — station_id, station_name
- `series[]` — timestamp, raw_pollen, display_value, numeric_value, level_code, level_text, value_family, meaning, advice
- `summary` — latest_value, latest_level.code/text/meaning, latest_advice, min, max, delta_24h, trend

### `forecast`

自动完成：解析目标区 → 拉取总量预报 → 拉取分类预报。需要 `--district`。

`data` 字段：
- `target_area` — area_id, name
- `total_forecast.series[]` — forecast_time, base_time, level_code, level_text, value_family, meaning
- `classify_forecast.categories[]` — plant_code, plant_name, forecast_time, level_code, display_text, min_value, max_value, description, value_family, meaning
- `summary.next_level` — code, text, meaning
- `summary.primary_category` — plant_code, plant_name, display_text, meaning

### `daily`

自动完成：目标区实时站点 + 24h 变化 + 今天总量预报 + 后续两天趋势 + 分类提示。需要 `--district`。

`data` 字段：
- `target` — area_id, area_name, station_id, station_name
- `current` — display_value, level_code, level_text, value_family, meaning, observed_at
- `change_24h` — delta, direction, min, max
- `today_outlook` — forecast_time, base_time, level_code, level_text, value_family, meaning, relative_to_current
- `forecast_series[]` — forecast_time, base_time, level_code, level_text, value_family, meaning
- `forecast_change.today_vs_current` — relation, summary_text, detail_text, source
- `forecast_change.tomorrow_vs_today` — 同上，可能为 null
- `forecast_change.day_after_vs_tomorrow` — 同上，可能为 null
- `category_hint` — plant_code, plant_name, forecast_time, display_text, description, value_family, meaning
- `advice` — 当前建议文案

趋势逻辑：
- `rising`：最新 - 最早 > 10
- `falling`：最新 - 最早 < -10
- `steady`：其他
- `unknown`：数值不可用

## 解释层规则

所有主结果对象都会追加：
- `value_family` — `area_realtime`、`station_observation`、`total_forecast`、`classify_forecast`
- `meaning` — summary_text, detail_text, source

`source` 可能取值：
- `legend`
- `upstream_level`
- `upstream_description`
- `local_mapping`

## 归一化规则

区域概览值（`area_realtime`）：
- 空/null → level_code=0，level_text="暂无"
- `>= 99999` → display_value=">800"，level_code=5，level_text="很高"，发出 warning
- `> 800` → display_value=">800"，level_code=5
- 阈值：`<=100` → 1/低，`101-250` → 2/较低，`251-400` → 3/中等，`401-800` → 4/高

站点和历史值（`station_observation`）：
- display_value 同样将 `>= 99999` 归一化为 ">800"
- level_code 优先使用源字段 `hfHLv`
- `hfHLv` 缺失或无效时回退到与区域概览相同的阈值规则

总量预报（`total_forecast`）：
- `1` → 低
- `2` → 较低
- `3` → 中等
- `4` → 高
- `5/6` → 很高
- 解释为等级预报，不解释为浓度值范围

分类预报（`classify_forecast`）：
- `display_text` 优先使用上游 `description`
- `meaning.source` 优先为 `upstream_description`
- 不直接把 `level=2` 套用成“较低”

## 警告

`warnings[]` 包含结构化警告对象：
- `pollen_value_capped` — 检测到封顶或哨兵值
- `legend_fallback_used` — legends 接口不可用，回退本地阈值解释
- `classify_forecast_empty` — 分类预报为空，但总量预报仍成功

## 冒烟测试

```bash
# 简报
./scripts/beijing-pollen-query.sh query --mode report --district 海淀 | jq '.ok, .data.target_station.station_name'
./scripts/beijing-pollen-query.sh query --mode report --district 海淀 --format text | jq -r '.data.text'

# 概览
./scripts/beijing-pollen-query.sh query --mode overview | jq '.ok, (.data.beijing_areas | length), (.data.stations | length)'

# 站点
./scripts/beijing-pollen-query.sh query --mode stations | jq '.data.alerts | length'

# 历史
./scripts/beijing-pollen-query.sh query --mode history --district 朝阳 | jq '.data.summary'

# 预报
./scripts/beijing-pollen-query.sh query --mode forecast --district 海淀 | jq '.data.summary.next_level'
./scripts/beijing-pollen-query.sh query --mode forecast --district 海淀 --format text | jq -r '.data.text'

# 晨报
./scripts/beijing-pollen-query.sh query --mode daily --district 朝阳 | jq '.data.today_outlook.level_text'
./scripts/beijing-pollen-query.sh query --mode daily --district 朝阳 --format text | jq -r '.data.text'

# 错误处理
./scripts/beijing-pollen-query.sh query --mode report 2>&1 | jq '.error'
./scripts/beijing-pollen-query.sh query --mode report --district 成都 2>&1 | jq '.error'
```
