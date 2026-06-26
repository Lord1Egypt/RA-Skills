---
name: china-weather
description: 查询中国任意城市的实时天气、多日预报和生活指数。数据来源中国天气网（weather.com.cn）。当用户询问中国城市天气、气温、降雨、空气质量、穿衣建议、出行建议等天气相关问题时使用。支持全国 350 个城市。
---

# 中国天气查询

## 使用方法

运行查询脚本：

```bash
python3 <skill_dir>/scripts/weather_query.py <城市名> [--days N] [--detail] [--json]
```

### 参数

- `城市名` — 城市名称，支持模糊匹配（如"杭"、"杭州"都能匹配）
- `--days N` — 预报天数，默认 1 天，最大 5 天
- `--detail` — 显示生活指数（穿衣、紫外线、雨伞、洗车等）
- `--json` — 输出原始 JSON 数据

### 示例

```bash
# 上海实时天气
python3 scripts/weather_query.py 上海

# 北京 3 天预报
python3 scripts/weather_query.py 北京 --days 3

# 成都详细天气（含生活指数）
python3 scripts/weather_query.py 成都 --days 2 --detail

# 输出 JSON
python3 scripts/weather_query.py 广州 --json
```

## 数据内容

- **实况**：气温、天气、风力、湿度、AQI、PM2.5、能见度、气压
- **预报**：5 天内天气趋势（白天/夜间天气、最高/最低温、风向风力）
- **生活指数**：穿衣、紫外线、雨伞、洗车、感冒、旅游、运动、空调、舒适度、晾晒
- **预警**：气象预警信号（蓝色/黄色/橙色/红色）

## 覆盖范围

全国 34 个省级区划，350 个城市。编码表见 `references/cities.json`。

## 数据来源

中国天气网（weather.com.cn）→ 中央气象台，每日 06/08/12/16/20 时更新。

## 注意

- 需要网络访问 `d1.weather.com.cn`
- HTTP 接口需设置 `Referer: http://www.weather.com.cn/`
