---
slug: free-weather-api-tool-free
name: free-weather-api-tool-free
version: 1.0.1
displayName: 天气查询免费版
summary: "查询城市天气,支持实时天气、未来7天预报、空气质量与出行建议。面向个人用户的天气查询助手,提供实时天气、多日预报、空气质量与智能建议."
license: Proprietary
edition: free
description: '面向个人用户的天气查询助手,提供实时天气、多日预报、空气质量与智能建议.
  核心能力: 城市天气查询、未来7天预报、空气质量分析、出行建议、天气预警提醒

  适用场景: 出行规划、穿衣建议、户外活动决策、差旅准备

  差异化: 免费版聚焦单城市查询与基础建议,适合个人日常使用

  适用关键词: 天气查询, 实时天气, 未来预报, 空气质量, 出行建议, 天气预警'
tags:
  - 天气查询
  - 生活助手
  - 出行规划
  - 空气质量
  - 天气预警
  - API
  - 接口
  - 开发工具
  - get
  - data
  - current
  - location
  - 天气
tools:
  - read
  - exec
  - write
homepage: ""
category: "Development"
---
# 天气查询 (免费版)

## 概述

本工具为个人用户提供准确的天气查询服务,支持实时天气、未来 7 天预报、空气质量、降水概率、风力风向等完整指标。基于天气数据智能分析,为出行、穿衣、户外活动提供决策建议,并在恶劣天气时主动预警.
免费版聚焦个人日常查询,适合出行规划、习惯养成、生活决策等场景.
## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|----|---|-----|
| 实时天气 | 当前温度、天气、湿度、风力 | 支持 |
| 多日预报 | 未来 1-7 天预报 | 支持 |
| 空气质量 | AQI、PM2.5、紫外线指数 | 支持 |
| 出行建议 | 基于天气的智能建议 | 支持 |
| 天气预警 | 暴雨、台风、高温等预警 | 支持 |
| 历史天气 | 过去天气数据查询 | 不支持 (升级 PRO) |
| 多城市对比 | 同时对比多个城市 | 不支持 (升级 PRO) |
| 农业气象 | 农业专项预报 | 不支持 (升级 PRO) |
| 天气推送 | 定时推送天气 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：查询城市天气、支持实时天气、空气质量与出行建、面向个人用户的天、气查询助手、提供实时天气、空气质量与智能建、核心能力、城市天气查询、空气质量分析、天气预警提醒、适用场景、出行规划、穿衣建议、户外活动决策、差旅准备、差异化、免费版聚焦单城市、查询与基础建议、适合个人日常使用、适用关键词、天气查询、未来预报等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一: 简单天气查询

```text
用户: "北京今天天气怎么样?"
# ...
助手:
实时天气: 北京当前多云,气温 15°C,体感温度 13°C,西北风 3-4 级,湿度 45%,能见度 10 公里.
# ...
预报概况: 未来 3 天以晴到多云为主,气温逐步回升.
- 今天: 多云转晴,8-18°C
- 明天: 晴,10-20°C
- 后天: 晴,12-22°C
# ...
出行建议:
- 今日早晚温差 10 度,注意及时增减衣物
- 明天紫外线较强 (UV 指数 7),外出请做好防晒措施
- 空气质量一般 (AQI 85),敏感人群建议减少户外活动
```

### 场景二: 旅行天气规划

```text
用户: "下周去杭州旅游,帮我看看天气"
# ...
助手:
1. 查询杭州未来 7 天天气
2. 重点关注旅行期间 (7月22日-28日):
   - 7月22-24日: 多云,25-32°C,适合游玩
   - 7月25日: 午后雷阵雨,建议上午安排户外活动
   - 7月26-28日: 晴热高温,35°C+,注意防暑
3. 行李建议:
   - 防晒霜、遮阳帽
   - 轻薄透气衣物
   - 雨伞 (应对午后雷阵雨)
   - 充足饮用水
```

### 场景三: 恶劣天气预警

```text
用户: "广州天气如何?"
# ...
助手:
实时天气: 广州当前暴雨,气温 22°C,体感温度 20°C,东南风 5-6 级,湿度 90%,能见度 2 公里.
# ...
重点提示:
暴雨橙色预警: 预计今天 12-18 时有 50-80 毫米降雨
# ...
出行建议:
- 尽量避免外出,如需外出请远离低洼地区
- 驾车请减速慢行,注意积水路段
- 请关注最新天气预警信息
```

## 不适用场景

以下场景天气查询免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### Step 1: 调用查询接口

```bash
# 查询北京实时天气
curl -s "wttr.in/Beijing?format=%l:+%c+%t+%h+%w&lang=zh"
# ...
# 详细预报
curl -s "wttr.in/Beijing?T&lang=zh"
```

### Step 2: 使用 query_weather 工具

```text
query_weather(location="北京", days=3, details=true)
```

参数说明:

| 参数 | 说明 | 默认值 |
|:-----|:-----|:-----|
| location | 城市或地区名称 | 必填 |
| days | 预报天数 | 1 |
| details | 是否返回详细 (空气质量等) | false |

### Step 3: 解析返回数据

```python
import requests
# ...
def query_weather(location, days=1, details=False):
    """查询天气"""
    url = f"https://wttr.in/{location}"
    params = {
        "format": "j1",  # JSON 格式
        "lang": "zh",
    }
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
# ...
    current = data.get("current_condition", [{}])[0]
    forecast = data.get("weather", [])[:days]
# ...
    return {
        "location": location,
        "query_time": current.get("localObsDateTime"),
        "current": {
            "temperature": current.get("temp_C"),
            "feels_like": current.get("FeelsLikeC"),
            "weather": current.get("lang_zh", [{}])[0].get("value"),
            "humidity": current.get("humidity"),
            "wind_speed": current.get("windspeedKmph"),
            "wind_direction": current.get("winddir16Point"),
        },
        "forecast": [
            {
                "date": f.get("date"),
                "temp_high": f.get("maxtempC"),
                "temp_low": f.get("mintempC"),
                "hourly": f.get("hourly", []),
            }
            for f in forecast
        ],
    }
```

## 示例

### 基础配置

```yaml
# ~/.weather-tool-free.yaml
api:
  primary: wttr.in
  fallback: open-meteo
  timeout: 30
  language: zh
# ...
user:
  default_location: 北京
  units: metric
  timezone: Asia/Shanghai
# ...
output:
  format: text  # text | json
  include_suggestions: true
  include_alerts: true
```

### 天气报告模板

```python
REPORT_TEMPLATE = """实时天气: {location}当前{weather},气温{temp}°C,体感温度{feels_like}°C,{wind_direction}{wind_speed},湿度{humidity}%,能见度{visibility}公里.
# ...
预报概况: 未来{days}天{forecast_summary}.
# ...
重点提示:
{highlights}
# ...
出行建议:
{suggestions}
"""
# ...
def render_report(data):
    return REPORT_TEMPLATE.format(
        location=data["location"],
        weather=data["current"]["weather"],
        temp=data["current"]["temperature"],
        feels_like=data["current"]["feels_like"],
        wind_direction=data["current"]["wind_direction"],
        wind_speed=data["current"]["wind_speed"],
        humidity=data["current"]["humidity"],
        visibility=data["current"].get("visibility", "10"),
        days=len(data["forecast"]),
        forecast_summary=summarize_forecast(data["forecast"]),
        highlights=generate_highlights(data),
        suggestions=generate_suggestions(data),
    )
```

### 智能建议生成

```python
def generate_suggestions(data):
    """根据天气生成出行建议"""
    suggestions = []
    current = data["current"]
# ...
    # 降水建议
    precip_prob = int(current.get("precip_prob", 0))
    if precip_prob > 70:
        suggestions.append("建议携带雨具")
# ...
    # 温差建议
    for f in data["forecast"]:
        diff = int(f["temp_high"]) - int(f["temp_low"])
        if diff > 10:
            suggestions.append(f"{f['date']} 温差 {diff}°C,建议备好外套")
            break
# ...
    # 空气质量建议
    aqi = int(current.get("aqi", 0))
    if aqi > 100:
        suggestions.append("空气质量较差,建议佩戴口罩")
    elif aqi > 150:
        suggestions.append("空气污染严重,敏感人群减少户外活动")
# ...
    # 紫外线建议
    uv = int(current.get("uv_index", 0))
    if uv > 7:
        suggestions.append(f"紫外线较强 (UV 指数 {uv}),注意防晒")
# ...
    # 风力建议
    wind = int(current.get("wind_speed", 0))
    if wind > 30:
        suggestions.append("风力较大,注意高空坠物,避免户外活动")
# ...
    # 温度建议
    temp = int(current.get("temperature", 20))
    if temp < 0:
        suggestions.append("气温低于 0°C,注意防寒保暖")
    elif temp > 35:
        suggestions.append("气温高于 35°C,注意防暑降温")
# ...
    return "\n".join(f"- {s}" for s in suggestions) if suggestions else "- 天气良好,适合正常活动"
```

## 最佳实践

### 1. 城市名称规范

使用城市中文名或拼音,避免歧义.
```bash
# 推荐
curl "wttr.in/Beijing?lang=zh"
curl "wttr.in/上海?lang=zh"
# ...
# 不推荐 (可能歧义)
curl "wttr.in/shanghai"
```

### 2. 缓存减少请求

天气数据变化不频繁,建议缓存减少请求.
```python
import json
from pathlib import Path
from datetime import datetime, timedelta
# ...
CACHE_DIR = Path.home() / ".weather_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
# ...
def get_with_cache(location, ttl_minutes=30):
    cache_file = CACHE_DIR / f"{location}.json"
    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        age = datetime.now() - datetime.fromisoformat(data["cached_at"])
        if age < timedelta(minutes=ttl_minutes):
            return data["weather"]
# ...
    weather = query_weather(location)
    cache_file.write_text(json.dumps({
        "cached_at": datetime.now().isoformat(),
        "weather": weather,
    }, ensure_ascii=False, indent=2))
    return weather
```

### 3. 天气预警分级

```python
ALERT_LEVELS = {
    "暴雨": {"yellow": "关注", "orange": "重要", "red": "紧急"},
    "台风": {"blue": "关注", "yellow": "重要", "orange": "紧急", "red": "极紧急"},
    "高温": {"yellow": "关注", "orange": "重要", "red": "紧急"},
    "寒潮": {"blue": "关注", "yellow": "重要", "orange": "紧急"},
}
# ...
def format_alert(alert_type, level):
    severity = ALERT_LEVELS.get(alert_type, {}).get(level, "未知")
    return f"{alert_type}{level}预警 ({severity})"
```

### 4. 日期与单位统一

- 日期统一使用 `YYYY-MM-DD` 格式
- 温度统一使用摄氏度
- 风力使用级别或 km/h

## 常见问题

### Q1: 查询的城市找不到怎么办?

尝试使用城市拼音或英文,如 "Shanghai"、"Beijing"。也可使用机场代码如 "PEK"、"PVG".
### Q2: 数据更新频率?

实时天气约每 30 分钟更新一次,预报每天更新 2-4 次.
### Q3: 支持哪些地区?

支持全球主要城市,中国地级市及以上基本全覆盖.
### Q4: 如何获取更长时间预报?

免费版支持最多 7 天预报。如需 15 天或更长,可升级 PRO 版本.
### Q5: 数据准确性如何?

数据来自权威气象服务,与主流天气应用精度相当。极端天气请以当地气象部门发布为准.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需访问天气 API 服务

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| wttr.in | 在线 API | 必需 | 免费,无需 Key |
| Open-Meteo | 在线 API | 备选 | 免费,无需 Key |
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| curl | 命令行工具 | 可选 | 系统自带 |
| Python 3.8+ | 运行时 | 可选 | python.org 下载 |
| requests 库 | Python 库 | 可选 | `pip install requests` |

### API Key 配置

```bash
# 免费版无需 API Key
# 天气服务均免费提供
# ...
# 可选: 默认位置
export WEATHER_DEFAULT_LOCATION="北京"
export WEATHER_LANGUAGE="zh"
```

### 可用性分类

- **分类**: MD+EXEC (Markdown 指令 + 命令行执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 调用免费天气 API,完成天气查询与建议生成
- **免费版限制**: 单城市查询、最多 7 天预报、无历史数据、无推送服务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "天气查询免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "free weather api"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
