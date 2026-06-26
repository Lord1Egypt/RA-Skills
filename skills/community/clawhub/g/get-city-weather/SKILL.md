---
name: get-weather
description: 获取指定城市的天气信息，包括温度、天气状况、风力、空气质量等。当用户询问天气、需要天气数据或提到城市天气时使用此技能。
---

# 获取天气信息

## 功能概述

此技能用于获取中国各城市的实时天气信息，包括：
- 当前温度和天气状况
- 风向和风力
- 空气质量指数(AQI)
- 生活指数建议

## 使用方法

### 1. 获取天气信息

在技能目录下运行天气获取脚本：

```bash
python scripts/get_weather.py [城市名]
```

Windows PowerShell 如遇控制台编码问题，可直接运行：

```powershell
$env:PYTHONIOENCODING="utf-8"
python .\scripts\get_weather.py 深圳
```

如果从其他目录调用，可先切换到技能目录，或使用相对路径：

```powershell
python .\get-weather\scripts\get_weather.py 深圳
```

示例：
```bash
python scripts/get_weather.py 北京
python scripts/get_weather.py 上海
```

### 2. 查看天气报告

脚本执行后会生成天气报告文件：
- 位置：`./get-weather/output/weather_report_[城市]_[日期].txt`
- 包含完整的天气信息和生活建议

## 实现方式

本技能通过聚合数据 `simpleWeather/query` 接口获取实时天气，并从环境变量或 `.env` 读取 API Key。脚本启动时会主动将 `stdout/stderr` 配置为 UTF-8，减少 Windows 控制台输出中文和 emoji 时的编码错误。

## 配置说明

### API 密钥配置（必填）

脚本会按以下顺序读取 API Key：

1. 环境变量 `JUHE_WEATHER_API_KEY`
2. 环境变量 `WEATHER_API_KEY`
3. 技能目录下的 `.env` 文件

`.env` 示例：

```env
JUHE_WEATHER_API_KEY=your_api_key_here
```

PowerShell 示例：

```powershell
$env:JUHE_WEATHER_API_KEY="your_api_key_here"
python .\scripts\get_weather.py 深圳
```

接口信息：

- 地址：`http://apis.juhe.cn/simpleWeather/query`
- 方法：`GET`
- 参数：`city`、`key`

未配置 API Key 或接口请求失败时，脚本会直接报错退出。

## 输出示例

```
========================================
          北京市 今日天气报告
========================================

📅 日期：2026年03月17日 星期二

🌡️  温度：15°C ~ 22°C
    当前：18°C

☁️  天气：多云

💨 风力：东南风 3级

🌫️ 空气质量：良 (AQI: 65)

💡 生活指数：
    • 穿衣：建议穿薄外套
    • 运动：适宜户外运动
    • 洗车：适宜洗车
    • 感冒：较易发，注意防护

========================================
```

## 依赖要求

- Python 3.6+
- requests

安装依赖：
```bash
pip install requests
```
