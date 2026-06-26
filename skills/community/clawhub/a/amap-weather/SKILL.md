---
name: amap-weather
description: >
  Query weather via Amap (高德) Weather API — China's most accurate location-based weather service.
  Use when user asks about weather in Chinese cities, mentions 高德/amap weather, or needs weather
  data for China locations. Supports real-time conditions and 4-day forecasts. Requires AMAP_API_KEY
  env var. Trigger phrases: 天气, weather in Beijing/Shanghai/etc, 高德天气, 今天天气怎么样,
  明天下雨吗, 未来几天天气.
---

# Amap Weather (高德天气)

## Prerequisites

- `AMAP_API_KEY` environment variable (高德 Web 服务 API Key)
- Apply at https://lbs.amap.com → 控制台 → 应用管理 → 创建应用 → 添加 Key (Web服务类型)

## Quick Usage

Run the bundled script:

```bash
# Real-time weather (实况)
python3 scripts/amap_weather.py 北京

# 4-day forecast (预报)
python3 scripts/amap_weather.py 杭州 --forecast

# By adcode (区县级精度)
python3 scripts/amap_weather.py 110108 --forecast   # 海淀区

# Raw JSON output
python3 scripts/amap_weather.py 上海 --json
```

The script accepts city names (中文) or 6-digit adcodes. It has a built-in lookup table for 40+ major cities. For districts or less common cities, use adcodes directly.

## Direct API Call (without script)

```bash
# Real-time
curl -s "https://restapi.amap.com/v3/weather/weatherInfo?key=${AMAP_API_KEY}&city=110000&extensions=base"

# Forecast
curl -s "https://restapi.amap.com/v3/weather/weatherInfo?key=${AMAP_API_KEY}&city=110000&extensions=all"
```

Parse the JSON: `lives[0]` for real-time, `forecasts[0].casts[]` for forecast (4 days).

## Key Details

- **extensions=base** → real-time → `lives[]` (temperature, weather, humidity, wind)
- **extensions=all** → forecast → `forecasts[].casts[]` (4 days, day/night split)
- adcode 6-digit code required (not city name in API). Script handles name→adcode mapping.
- Updates: real-time hourly, forecast at ~8:00/11:00/18:00 CST
- Free quota: 300k calls/day

## Formatting Output

When presenting weather to users:
- Use weather emoji (☀️晴 ⛅多云 🌧雨 ❄️雪 🌫雾 😷霾)
- Temperature in °C
- Include wind and humidity for real-time
- For forecast, show day/night separately with high/low temps

## API Reference

For complete field definitions, error codes, and adcode list: see [references/api-docs.md](references/api-docs.md).
