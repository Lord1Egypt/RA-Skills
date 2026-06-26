---
name: daily-weather-news
description: 每日天气和新闻推送技能，使用Open-Meteo API获取精确天气信息、中文国际新闻搜索、智能穿衣建议和飞书消息推送功能。适用于需要每日自动推送天气和新闻到飞书聊天场景，支持定时推送和手动查询两种模式。
---

# 每日天气新闻推送

## 概述
这个技能提供了完整的每日天气和新闻推送功能，包括天气信息获取、中文新闻搜索、智能穿衣建议和飞书消息推送。支持定时自动推送和手动查询两种模式。

## 快速开始

### 基本用法
```bash
# 测试模式（预览推送内容）
./scripts/daily_push.sh --test

# 正常执行（获取天气和新闻并推送）
./scripts/daily_push.sh

# 设置定时任务（每天早上7:30执行）
30 7 * * * /home/alanchan/.openclaw/workspace/skills/daily-weather-news/scripts/daily_push.sh
```

### 配置设置

**1. 设置环境变量（推荐）：**
```bash
# 临时设置（当前会话有效）
export TAVILY_API_KEY="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"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export TAVILY_API_KEY="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"' >> ~/.bashrc
source ~/.bashrc
```

**2. 编辑 `config/config.sh` 文件（其他配置）：**
```bash
# 目标用户ID（飞书）
TARGET_USER="ou_3a0705a4c7b5f068fff0b2b719d37978"

# 推送地点
LOCATION="黄埔"

# 日志文件路径
LOG_FILE="/home/alanchan/.openclaw/workspace/daily_push.log"
```

## 核心功能

### 1. 天气信息获取
- 使用 Open-Meteo API 获取指定地点的精确天气信息
- 通过经纬度坐标（广州：23.1291, 113.2644）精确定位
- 自动将天气代码转换为中文描述（如代码3 → "多云"）
- 提取温度、风速、风向等详细气象数据

### 2. 中文国际新闻搜索
- 使用 Tavily Search API 搜索中文国际新闻
- 优先搜索新华网、人民网等权威中文新闻源
- 提供结构化的新闻摘要和来源链接

### 3. 智能穿衣建议
- 根据Open-Meteo天气代码智能生成穿衣建议
- 考虑温度、天气类型（多云、晴朗、雨雪等）等因素
- 基于精确气象数据提供实用的穿衣指导

### 4. 飞书消息推送
- 使用OpenClaw消息API发送推送内容到飞书
- 支持丰富的emoji和格式化显示
- 自动记录推送日志和执行状态

## 工作流程

### 步骤1: 获取天气信息
```bash
weather_info=$(get_weather "$LOCATION")
# 输出: "多云 25.6°C 3.7 km/h (微风)"
```

### 步骤2: 获取国际新闻
```bash
news_info=$(get_news)
# 输出: 结构化的中文国际新闻内容
```

### 步骤3: 生成穿衣建议
```bash
clothing_advice=$(get_clothing_advice "$weather_info")
# 输出: "根据当前天气，建议穿着舒适的长袖衣物，注意早晚温差。"
```

### 步骤4: 推送消息
```bash
send_to_feishu "$push_content" "$TARGET_USER"
# 发送格式化的消息到飞书
```

## 配置选项

### config/config 关键配置
```bash
# 推送目标用户ID
TARGET_USER="ou_3a0705a4c7b5f068fff0b2b719d37978"

# 推送地点
LOCATION="广州市黄埔区"

# 广州经纬度坐标
LATITUDE="23.1291"
LONGITUDE="113.2644"

# 天气API配置
WEATHER_API_BASE="https://api.open-meteo.com/v1/forecast"

# Tavily API密钥（从环境变量读取）
# 在运行脚本前设置: export TAVILY_API_KEY="your-api-key"
TAVILY_API_KEY="${TAVILY_API_KEY:-}"

# 推送时间（cron格式）
CRON_TIME="30 7 * * *"

# 是否启用推送
ENABLE_PUSH="true"
```

## 错误处理

### 常见问题
1. **API密钥错误**
   - 检查 `TAVILY_API_KEY` 配置
   - 验证密钥有效性

2. **网络连接问题**
   - 检查网络连接
   - 验证Open-Meteo API服务可用性
   - 检查防火墙设置

3. **消息推送失败**
   - 检查 `openclaw` 命令可用性
   - 验证用户ID正确性

4. **天气数据解析失败**
   - 检查JSON数据格式
   - 验证经纬度坐标正确性
   - 确认API响应完整性

### 日志查看
```bash
# 查看推送日志
tail -f /home/alanchan/.openclaw/workspace/daily_push.log

# 查看错误日志
grep "ERROR" /home/alanchan/.openclaw/workspace/daily_push.log
```

## 参考文档

### API文档
- [weather-api.md](references/weather-api.md) - Open-Meteo 天气API文档
- [tavily-api.md](references/tavily-api.md) - Tavily搜索API文档
- [feishu-config.md](references/feishu-config.md) - 飞书推送配置

### 工作流程
- [workflow.md](references/workflow.md) - 详细工作流程和使用指南

## 扩展功能

### 自定义新闻源
修改 `NEWS_SOURCES` 配置：
```bash
NEWS_SOURCES="site:your-news-site.com 重要新闻 OR site:another-site.com 国际新闻"
```

### 多地点支持
可以扩展脚本支持多个地点的天气推送，通过添加多个经纬度坐标对实现，每个地点使用独立的API调用。

### 消息模板自定义
修改 `PUSH_TEMPLATE` 来自定义消息格式和内容结构。

### 天气代码扩展
可以根据需要扩展天气代码映射，添加更多天气类型的中文描述。

## 技术依赖
- curl: 用于HTTP请求（Open-Meteo API调用）
- node.js: 用于Tavily搜索
- openclaw: 用于飞书消息推送
- bash: 脚本执行环境（JSON解析、数据处理）
- bash: 脚本执行环境
- 标准Linux工具：grep, awk, sed（JSON数据解析）
