# 天气API文档

## Open-Meteo API

### 基本用法
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=LATITUDE&longitude=LONGITUDE&current_weather=true&hourly=PARAMETERS"
```

### 支持的参数
- `latitude`: 纬度坐标
- `longitude`: 经度坐标
- `current_weather`: 是否获取当前天气 (true/false)
- `hourly`: 每小时数据参数
- `timezone`: 时区设置 (auto/Asia/Shanghai等)

### 输出格式选项
- JSON格式，包含以下主要字段：
  - `current_weather`: 当前天气信息
    - `weathercode`: 天气代码
    - `temperature`: 温度 (°C)
    - `windspeed`: 风速 (km/h)
    - `winddirection`: 风向 (度)
    - `is_day`: 是否白天 (0/1)
  - `hourly`: 每小时数据
    - `temperature_2m`: 2米高度温度
    - `windspeed_10m`: 10米高度风速
    - `weathercode`: 天气代码

### 示例
```bash
# 获取广州黄埔天气
curl -s "https://api.open-meteo.com/v1/forecast?latitude=23.1291&longitude=113.2644&current_weather=true"

# 获取详细天气信息
curl -s "https://api.open-meteo.com/v1/forecast?latitude=23.1291&longitude=113.2644&current_weather=true&hourly=temperature_2m,windspeed_10m,weathercode"

# 设置时区为亚洲/上海
curl -s "https://api.open-meteo.com/v1/forecast?latitude=23.1291&longitude=113.2644&current_weather=true&timezone=Asia/Shanghai"
```

### 中文天气描述映射
根据Open-Meteo天气代码：

| 代码 | 天气类型 | 中文描述 |
|------|----------|----------|
| 0-1 | 晴天 | 晴朗 |
| 2 | 部分多云 | 部分多云 |
| 3 | 多云 | 多云 |
| 45 | 雾 | 雾 |
| 48 | 冻雾 | 冻雾 |
| 51-57 | 毛毛雨 | 毛毛雨/冻毛毛雨 |
| 61-63 | 雨 | 雨 |
| 65 | 大雨 | 大雨 |
| 66-67 | 冻雨 | 冻雨 |
| 71-77 | 雪 | 雪 |
| 80-82 | 阵雨 | 阵雨 |
| 85-86 | 阵雪 | 阵雪 |
| 95-99 | 雷暴 | 雷暴 |

### 数据解析示例
```bash
# 解析JSON响应
response=$(curl -s "https://api.open-meteo.com/v1/forecast?latitude=23.1291&longitude=113.2644&current_weather=true")

# 提取天气数据
weather_code=$(echo "$response" | sed 's/.*"current_weather":{//; s/}.*//' | grep -o '"weathercode":[0-9]*' | awk -F: '{print $2}')
temperature=$(echo "$response" | sed 's/.*"current_weather":{//; s/}.*//' | grep -o '"temperature":[0-9.]*' | awk -F: '{print $2}')
wind_speed=$(echo "$response" | sed 's/.*"current_weather":{//; s/}.*//' | grep -o '"windspeed":[0-9.]*' | awk -F: '{print $2}')

# 风速描述映射
wind_desc="未知"
wind_int=$(echo "$wind_speed" | awk '{printf "%.0f", $1}')
if [ "$wind_int" -lt 5 ]; then
    wind_desc="微风"
elif [ "$wind_int" -lt 15 ]; then
    wind_desc="和风"
elif [ "$wind_int" -lt 25 ]; then
    wind_desc="强风"
else
    wind_desc="狂风"
fi

echo "天气: ${weather_code} ${temperature}°C ${wind_speed} km/h (${wind_desc})"
```

### API优势
- ✅ 完全免费，无请求频率限制
- ✅ 开源可靠，数据质量高
- ✅ 精确的经纬度定位
- ✅ 结构化的JSON数据格式
- ✅ 支持多种气象参数
- ✅ 全球覆盖，支持时区设置
- ✅ 详细的天气代码系统

### API限制
- 需要网络连接
- 建议添加错误处理和重试机制
- 响应数据较大，建议按需请求参数
- 天气代码需要映射到中文描述