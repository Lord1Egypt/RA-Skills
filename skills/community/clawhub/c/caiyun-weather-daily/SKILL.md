---
name: caiyun-weather-daily
description: 彩云天气每日推送。每天定时查询天气并通过微信/消息渠道推送天气早报。支持自定义位置、推送时间和推送渠道。Use when user wants to set up daily weather notifications.
---

# 彩云天气每日推送

定时查询彩云天气 API，生成天气早报并推送到指定渠道。

## 功能

- 🌤️ 实时天气数据（气温、体感、湿度、风速）
- 📅 今日气温范围（最高/最低）
- 🌧️ 降雨预测（今日是否降雨、2小时内降雨概率）
- ⏰ 定时推送（可配置推送时间）
- 📱 多渠道推送（微信、Telegram、Discord 等）

## 配置

### 必需配置

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `CAIYUN_TOKEN` | 彩云天气 API Token | [彩云开发者平台](https://www.caiyunapp.com/h5/) |
| `LNG` | 经度 | 地图工具获取 |
| `LAT` | 纬度 | 地图工具获取 |

### 可选配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `PUSH_TIME` | 推送时间（cron 表达式） | `0 7 * * *`（每天 7:00） |
| `PUSH_CHANNEL` | 推送渠道 | `wechat` |
| `LOCATION_NAME` | 位置名称（显示用） | `当前位置` |

## 使用方式

### 方式 1：通过 OpenClaw Cron 配置

在 OpenClaw 的 cron 配置中添加：

```json
{
  "name": "每日天气推送",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "调用彩云天气脚本推送今日天气"
  },
  "delivery": { "mode": "announce", "channel": "wechat" }
}
```

### 方式 2：直接运行脚本

```bash
# 设置环境变量
export CAIYUN_TOKEN="your_token"
export LNG="116.4"   # 你的经度
export LAT="39.9"    # 你的纬度

# 运行
python3 weather_push.py
```

### 方式 3：手动查询

```bash
# 快速查询当前天气
curl -s "https://api.caiyunapp.com/v2.6/${CAIYUN_TOKEN}/${LNG},${LAT}/realtime?lang=zh_CN" | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d['result']['realtime']
print(f\"气温: {r['temperature']}°C, 体感: {r['apparent_temperature']}°C, 湿度: {int(r['humidity']*100)}%\")
"
```

## 输出格式

```
🌤 当前位置 今日天气

🌡 气温：18°C ~ 25°C
🤔 体感：23°C
💧 湿度：65%
🌧 今日降雨：否
⏱ 2小时内降雨：否
```

## 彩云天气 API

### 获取 Token

1. 访问 [彩云天气开发者平台](https://www.caiyunapp.com/h5/)
2. 注册账号并创建应用
3. 获取 API Token

### API 端点

| 端点 | 说明 |
|------|------|
| `/realtime` | 实时天气 |
| `/daily` | 日级预报（最多 5 天） |
| `/minutely` | 分钟级降水（2 小时） |
| `/hourly` | 小时级预报（48 小时） |
| `/weather` | 综合接口（包含以上全部） |

### 示例请求

```bash
# 综合天气数据
curl -s "https://api.caiyunapp.com/v2.6/YOUR_TOKEN/LNG,LAT/weather?lang=zh_CN&unit=metric&alert=true"
```

## 依赖

- Python 3.7+
- curl
- OpenClaw（用于定时任务和消息推送）

## 扩展

### 添加天气预警

修改脚本，解析 `alert=true` 返回的预警数据：

```python
alerts = data.get('result', {}).get('alert', {}).get('content', [])
for alert in alerts:
    print(f"⚠️ {alert['title']}: {alert['description']}")
```

### 多地点推送

在脚本中添加多个位置：

```python
LOCATIONS = [
    {"name": "北京", "lng": "116.4", "lat": "39.9"},
    {"name": "上海", "lng": "121.4", "lat": "31.2"},
]
```

### 条件推送

只在特定天气条件下推送：

```python
# 只在今日有雨时推送
if has_rain_today:
    send_weather_push()
```
