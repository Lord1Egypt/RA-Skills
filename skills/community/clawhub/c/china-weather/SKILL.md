---
name: china-weather
description: "获取中国城市天气信息，支持当前天气、未来预报、生活指数。当用户问中国城市的天气、温度、下雨、穿衣建议时使用。支持城市名或城市代码查询。Use when user asks about weather in Chinese cities like '北京天气'、'上海明天会下雨吗'、'广州这周天气怎么样'。"
---

# 中国天气

获取中国城市的实时天气和预报信息。

## 快速使用

```bash
# 当前天气
~/.openclaw/workspace/skills/china-weather/scripts/weather.sh 上海

# 明天天气
~/.openclaw/workspace/skills/china-weather/scripts/weather.sh 北京 tomorrow

# 一周预报
~/.openclaw/workspace/skills/china-weather/scripts/weather.sh 广州 week

# 生活指数（穿衣、出行建议）
~/.openclaw/workspace/skills/china-weather/scripts/weather.sh 深圳 indices
```

## 支持的城市

- 直辖市：北京、上海、天津、重庆
- 省会城市：广州、杭州、成都、武汉、西安等
- 其他城市：支持大部分中国城市（使用城市名或区县名）

## 命令参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `城市名` | 查询当前天气 | `weather.sh 上海` |
| `tomorrow` | 明天天气 | `weather.sh 北京 tomorrow` |
| `week` | 一周预报 | `weather.sh 广州 week` |
| `indices` | 生活指数 | `weather.sh 深圳 indices` |
| `alert` | 气象预警 | `weather.sh 成都 alert` |

## 生活指数说明

- 🧥 **穿衣指数** - 穿衣建议
- ☂️ **雨伞指数** - 是否需要带伞
- 🚗 **洗车指数** - 是否适合洗车
- 🏃 **运动指数** - 是否适合户外运动
- 🌞 **紫外线指数** - 防晒建议
- 😷 **空气污染扩散指数** - 空气质量

## 数据来源

- 默认使用 wttr.in（免费，无需 API key）
- 如需更精准数据，可配置和风天气 API key

## 配置 API key（可选）

如需使用和风天气 API 获取更精准数据：

1. 注册和风天气开发者账号：https://dev.qweather.com
2. 获取免费 API key
3. 配置环境变量：

```bash
export QWEATHER_KEY="your-api-key"
```

## 示例输出

**当前天气：**
```
上海 🌤️  18°C
体感 16°C | 湿度 65% | 东北风 3级
空气质量：良 (AQI 58)
```

**一周预报：**
```
上海 未来7天天气：
周一 🌤️  12-18°C
周二 ☀️  14-20°C
周三 🌧️  10-15°C (有雨)
...
```
