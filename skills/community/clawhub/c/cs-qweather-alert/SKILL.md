---
name: 和风天气 - 天气和预警查询
description: 和风天气查询工具集，支持实时天气查询和天气预警查询。当用户询问城市天气、气温、湿度、刮风下雨等天气状况，或需要查询预警时触发。
---

# 和风天气-天气查询与天气预警查询

**和风天气查询工具集** — 支持实时天气查询和天气预警查询两个功能。

---

## 技能职责

当需要查询某个城市的**实时天气**、**每日天气预报**或**天气预警**时使用此 skill。

---

## 脚本清单

| 脚本 | 功能 |
|------|------|
| `qweather-get-weather-now.py` | 实时天气查询 |
| `qweather-get-weather-alert.py` | 天气预警查询 |
| `qweather-get-weather-daily.py` | 每日天气预报（3/7/10/15/30天） |
| `qweather_utils.py` | 公共工具库（供上述脚本调用） |

---

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `QWEATHER_API_HOST` | ✅ | 和风 API Host，格式为 `https://xxx.re.qweatherapi.com` |
| `QWEATHER_CITY` | 否 | 默认城市名，作为命令行参数的备用 |

> **环境变量加载**：脚本使用 `dotenv` 库自动从 `~/.openclaw/.env` 加载变量（`override=True`，强制读取最新值避免旧进程缓存干扰），在 OpenClaw 环境下无需手动配置即可使用。
>
> **Token 配置**：JWT Token 默认从 `~/.myjwtkey/last-token.dat` 读取，也可通过 `--token` 参数显式传入。

---

## qweather-get-weather-now.py — 实时天气

查询城市当前天气状况，包括温度、湿度、风力、气压等详细信息。

### 命令

```bash
python3 cs-qweather-alert/scripts/qweather-get-weather-now.py <城市名> [--host API_HOST] [--token TOKEN]
```

### 示例

```bash
# 查询北京实时天气
python3 cs-qweather-alert/scripts/qweather-get-weather-now.py 北京

# 指定 API Host
python3 cs-qweather-alert/scripts/qweather-get-weather-now.py 上海 --host https://md78m2kdwa.re.qweatherapi.com

# 通过环境变量设置默认城市
export QWEATHER_CITY=南京
python3 cs-qweather-alert/scripts/qweather-get-weather-now.py
```

### 输出字段

| 字段 | 说明 |
|------|------|
| `obsTime` | 数据观测时间 |
| `temp` | 温度（°C） |
| `feelsLike` | 体感温度（°C） |
| `text` | 天气状况文字 |
| `windDir / windScale / windSpeed` | 风向 / 风力等级 / 风速（km/h） |
| `humidity` | 相对湿度（%） |
| `precip` | 过去1小时降水量（mm） |
| `pressure` | 大气压强（hPa） |
| `vis` | 能见度（km） |
| `cloud` | 云量（%） |
| `dew` | 露点温度（°C） |

### 示例输出

```
🌤️  北京 实时天气
🕐 2026-04-09 22:48  🌫️ 雾  10°C（体感 8°C）
────────────────────────────────────────
💨 风力 ······ 西南风 1级 (4 km/h)
💧 湿度 ······ 96%
🌧️  降水量 ···· 0 mm
🌡️  气压 ······ 999 hPa
👁️  能见度 ···· 3 km
☁️  云量 ······ 91%
🌫️  露点 ······ 8°C
────────────────────────────────────────
📡 QWeather | 2026-04-09 22:52
```

---

## qweather-get-weather-daily.py — 每日天气预报

查询城市未来 3-30 天天气预报，包含最高/最低温度、天气状况、风力风向、降水概率、紫外线指数、日出日落、月相等信息。

### 命令

```bash
python3 cs-qweather-alert/scripts/qweather-get-weather-daily.py <城市名> [--days 7] [--host API_HOST] [--token TOKEN]
```

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--days` | 7 | 预报天数，支持 3/7/10/15/30 天 |

### 示例

```bash
# 查询北京 7 天预报（默认）
python3 cs-qweather-alert/scripts/qweather-get-weather-daily.py 北京

# 查询上海 15 天预报
python3 cs-qweather-alert/scripts/qweather-get-weather-daily.py 上海 --days 15

# 查询广州 30 天预报
python3 cs-qweather-alert/scripts/qweather-get-weather-daily.py 广州 --days 30
```

### 输出字段

| 字段 | 说明 |
|------|------|
| `fxDate` | 预报日期 |
| `tempMax / tempMin` | 最高 / 最低温度（°C） |
| `textDay / textNight` | 白天 / 夜间天气文字 |
| `iconDay / iconNight` | 白天 / 夜间天气图标 |
| `windDirDay / windScaleDay` | 白天风向 / 风力等级 |
| `precip` | 预报当天总降水量（mm） |
| `uvIndex` | 紫外线指数 |
| `sunrise / sunset` | 日出 / 日落时间 |
| `moonPhase / moonrise / moonset` | 月相 / 月升 / 月落 |
| `humidity` | 相对湿度（%） |

### 示例输出

```
📅 北京 7天天气预报
────────────────────────────────────────────────────────────
今天 04-27 | ⛅多云 | 9°C~22°C | 北风1-3级 | 💧无降水 | 紫外线: 8(极强)
明天 04-28 | ☀️晴 | 9°C~22°C | 北风1-3级 | 💧无降水 | 紫外线: 9(极强)
后天 04-29 | ☀️晴 | 10°C~25°C | 西南风1-3级 | 💧无降水 | 紫外线: 9(极强)
周四 04-30 | ☀️晴 | 15°C~29°C | 西南风1-3级 | 💧无降水 | 紫外线: 9(极强)
周五 05-01 | ⛅多云→☁️阴 | 14°C~25°C | 南风1-3级 | 💧无降水 | 紫外线: 4(较强)
周六 05-02 | ☀️晴 | 12°C~25°C | 西南风1-3级 | 💧无降水 | 紫外线: 9(极强)
周日 05-03 | ☀️晴→☁️阴 | 15°C~28°C | 西南风1-3级 | 💧无降水 | 紫外线: 9(极强)
────────────────────────────────────────────────────────────
🌅 日出 05:21 / 日落 19:04  🌙 盈凸月     月升 14:46 / 月落 03:11
────────────────────────────────────────────────────────────
📡 QWeather | 更新于 2026-04-27 00:04
```

### 紫外线指数等级

| 指数 | 描述 |
|------|------|
| 0-2 | 很弱 / 弱 |
| 3-4 | 中等 / 较强 |
| 5-6 | 强 / 很强 |
| 7-9 | 很强 / 极强 |
| 10-12 | 极强（极高） |

---

## qweather-get-weather-alert.py — 天气预警

查询城市当前生效的天气预警信息。

### 命令

```bash
python3 cs-qweather-alert/scripts/qweather-get-weather-alert.py <城市名> [--host API_HOST] [--token TOKEN]
```

### 示例

```bash
# 查询北京天气预警
python3 cs-qweather-alert/scripts/qweather-get-weather-alert.py 北京

# 查询多个城市
python3 cs-qweather-alert/scripts/qweather-get-weather-alert.py 上海
```

### 预警级别

| 级别 | Emoji |
|------|-------|
| 极严重（extreme） | 🔴 |
| 严重（severe） | 🟠 |
| 中等（moderate） | 🟡 |
| 轻微（minor） | 🔵 |

### 示例输出

```
🌤️  北京 天气预警
坐标: 39.90499, 116.40529
────────────────────────────────────────
✅ 目前没有天气预警
```

---

## 公共机制

### 城市经纬度缓存

- **位置**：`scripts/data/location.json`（脚本同目录下）
- **命中**：查询过的城市直接从缓存读取，不调 API
- **失效**：永久缓存，人工手动清理文件即可

### 日志

- **位置**：`/tmp/cslog/`
- **命名规则**：`qweather-get-weather-now-YYYYMMDD.log`、`qweather-get-weather-alert-YYYYMMDD.log`、`qweather-get-weather-daily-YYYYMMDD.log`
- **脱敏**：JWT Token 只显示前8后4位，其余用 `***` 替代

### 共享常量

`qweather_utils.py` 中定义了以下共享常量，供所有脚本使用：

| 常量 | 说明 |
|------|------|
| `WEATHER_ICON_EMOJI` | 天气图标代码 → emoji 映射表 |
| `DEFAULT_WEATHER_EMOJI` | 未识别图标代码时的默认 emoji |
| `UV_DESCRIPTION` | 紫外线指数 → 描述文字映射表 |
| `get_weather_emoji(icon_code)` | 根据图标代码返回对应 emoji |
| `uv_description(uv_index)` | 根据紫外线指数返回描述文字 |

### 城市名称规则

- 直辖市（如北京、上海）：直接显示城市名
- 省会/地级市（如南京）：直接显示城市名
- 县级市/区县（如浦东新区）：显示「省市区」格式，自动去重

---

## 依赖

- Python 3（标准库，无需 pip）
