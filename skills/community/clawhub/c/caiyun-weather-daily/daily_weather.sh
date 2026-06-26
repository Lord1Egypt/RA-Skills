#!/bin/bash
# 彩云天气每日早报推送
# 用法: ./daily_weather.sh [channel]
# channel: wechat (默认), telegram, discord 等

set -e

# 配置（通过环境变量设置，必须提供）
# 示例: export CAIYUN_TOKEN="your_token" LNG="116.4" LAT="39.9"
TOKEN="${CAIYUN_TOKEN:-}"
LNG="${LNG:-}"
LAT="${LAT:-}"

# 检查配置
if [ -z "$TOKEN" ] || [ -z "$LNG" ] || [ -z "$LAT" ]; then
    echo "❌ 错误: 请设置环境变量 CAIYUN_TOKEN, LNG, LAT"
    echo "示例: export CAIYUN_TOKEN='your_token' LNG='116.4' LAT='39.9'"
    exit 1
fi

LOCATION="${LOCATION_NAME:-当前位置}"
CHANNEL="${1:-wechat}"

API_URL="https://api.caiyunapp.com/v2.6/${TOKEN}/${LNG},${LAT}"

echo "🔄 获取天气数据..."

# 获取综合天气数据
WEATHER=$(curl -s "${API_URL}/weather?lang=zh_CN&unit=metric&alert=true" --max-time 15)

# 解析数据
TEMP=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['result']['realtime']['temperature'])
" 2>/dev/null || echo "--")

FEELS=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['result']['realtime']['apparent_temperature'])
" 2>/dev/null || echo "--")

HUMIDITY=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(int(d['result']['realtime']['humidity']*100))
" 2>/dev/null || echo "--")

WIND=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['result']['realtime']['wind']['speed'])
" 2>/dev/null || echo "--")

TEMP_MAX=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['result']['daily']['temperature'][0]['max'])
" 2>/dev/null || echo "--")

TEMP_MIN=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(d['result']['daily']['temperature'][0]['min'])
" 2>/dev/null || echo "--")

SKYCON=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
skycons = {
    'CLEAR':'晴','CLEAR_DAY':'晴','CLEAR_NIGHT':'晴',
    'PARTLY_CLOUDY':'多云','PARTLY_CLOUDY_DAY':'多云','PARTLY_CLOUDY_NIGHT':'多云',
    'CLOUDY':'阴',
    'LIGHT_RAIN':'小雨','MODERATE_RAIN':'中雨','HEAVY_RAIN':'大雨',
    'RAIN':'雨','STORM_RAIN':'暴雨','DRIZZLE_RAIN':'毛毛雨',
    'SNOW':'雪','LIGHT_SNOW':'小雪','MODERATE_SNOW':'中雪','HEAVY_SNOW':'大雪',
    'FOG':'雾','HAZE':'霾','SAND':'沙尘'
}
s = d['result']['realtime']['skycon']
print(skycons.get(s, s))
" 2>/dev/null || echo "--")

RAIN_TODAY=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
skycon = d['result']['daily']['skycon'][0]['value']
rain_types = ['RAIN','LIGHT_RAIN','MODERATE_RAIN','HEAVY_RAIN','STORM_RAIN','DRIZZLE_RAIN']
print('是 ⚠️' if any(r in skycon for r in rain_types) else '否')
" 2>/dev/null || echo "否")

RAIN_2H=$(echo "$WEATHER" | python3 -c "
import sys,json
d=json.load(sys.stdin)
prob = d['result'].get('minutely',{}).get('precipitation_2h',[])
has_rain = any(p > 0.03 for p in prob) if prob else False
print('是 ⚠️' if has_rain else '否')
" 2>/dev/null || echo "否")

NOW=$(date "+%Y-%m-%d %H:%M")

# 组装消息
MSG="🌤 ${LOCATION} 今日天气

🌡 气温：${TEMP_MIN}°C ~ ${TEMP_MAX}°C
🤔 体感：${FEELS}°C
💧 湿度：${HUMIDITY}%
🌬 风速：${WIND} m/s
☁ 天气：${SKYCON}
🌧 今日降雨：${RAIN_TODAY}
⏱ 2小时内降雨：${RAIN_2H}

📅 ${NOW}"

echo "$MSG"

# 发送消息（如果安装了 OpenClaw CLI）
if command -v openclaw &> /dev/null; then
    echo ""
    echo "📤 发送到 ${CHANNEL}..."
    openclaw message send --channel "$CHANNEL" "$MSG" && echo "✅ 已发送"
elif [ -f "/Applications/QClaw.app/Contents/Resources/openclaw/bin/openclaw" ]; then
    echo ""
    echo "📤 发送到 ${CHANNEL}..."
    /Applications/QClaw.app/Contents/Resources/openclaw/bin/openclaw message send --channel "$CHANNEL" "$MSG" && echo "✅ 已发送"
else
    echo ""
    echo "ℹ️ OpenClaw CLI 未安装，消息已打印到终端"
fi
