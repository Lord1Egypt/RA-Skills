# 每日天气新闻推送技能

## 概述
这个技能提供了完整的每日天气和新闻推送功能，包括天气信息获取、中文新闻搜索、智能穿衣建议和飞书消息推送。

## 功能特性
- 🌦️ 实时天气信息获取
- 🌍 中文国际新闻搜索
- 👔 智能穿衣建议
- 📱 飞书消息推送
- ⚙️ 灵活的配置管理
- 🧪 测试模式支持

## 使用场景
- **日常推送**: 每天早上7:30自动推送天气和新闻
- **手动查询**: 随时查询当前天气和最新新闻
- **测试验证**: 使用测试模式验证推送内容
- **自定义配置**: 修改配置文件适应不同需求

## 快速开始

### 1. 配置设置
编辑 `config/config.sh` 文件，设置：
```bash
TARGET_USER="你的飞书用户ID"
LOCATION="黄埔"
TAVILY_API_KEY="你的API密钥"
```

### 2. 手动执行测试
```bash
# 测试模式
./scripts/daily_push.sh --test

# 正常执行
./scripts/daily_push.sh
```

### 3. 设置定时任务
```bash
# 添加到crontab
crontab -e

# 每天早上7:30执行
30 7 * * * /home/alanchan/.openclaw/workspace/skills/daily-weather-news/scripts/daily_push.sh
```

## 工作流程

### 步骤1: 获取天气信息
- 使用 wttr.in API 获取指定地点的天气
- 自动将英文天气描述转换为中文
- 提取温度、风速、湿度等关键信息

### 步骤2: 获取国际新闻
- 使用 Tavily Search API 搜索中文国际新闻
- 优先搜索新华网、人民网等权威中文新闻源
- 提供结构化的新闻摘要和来源链接

### 步骤3: 生成穿衣建议
- 根据天气状况智能生成穿衣建议
- 考虑温度、天气类型等因素
- 提供实用的穿衣指导

### 步骤4: 推送消息
- 使用飞书消息API发送推送内容
- 支持Markdown格式美化显示
- 自动记录推送日志

## 配置文件详解

### config/config.sh
```bash
# 目标用户ID
TARGET_USER="ou_3a0705a4c7b5f068fff0b2b719d37978"

# 推送地点
LOCATION="广州市黄埔区"

# API密钥
TAVILY_API_KEY="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"

# 日志文件路径
LOG_FILE="/home/alanchan/.openclaw/workspace/daily_push.log"

# 推送时间 (cron格式)
CRON_TIME="30 7 * * *"
```

## 脚本功能

### scripts/daily_push.sh
主要功能模块：
- `get_weather()`: 获取天气信息
- `get_news()`: 获取国际新闻
- `get_clothing_advice()`: 生成穿衣建议
- `send_to_feishu()`: 推送消息到飞书
- `main()`: 主函数协调各模块

### 参数支持
```bash
# 测试模式
./scripts/daily_push.sh --test

# 正常执行
./scripts/daily_push.sh
```

## 错误处理

### 常见问题
1. **API密钥错误**
   - 检查 TAVILY_API_KEY 配置
   - 验证密钥有效性

2. **网络连接问题**
   - 检查网络连接
   - 验证API服务可用性

3. **消息推送失败**
   - 检查 openclaw 命令可用性
   - 验证用户ID正确性

### 日志查看
```bash
# 查看推送日志
tail -f /home/alanchan/.openclaw/workspace/daily_push.log

# 查看错误日志
grep "ERROR" /home/alanchan/.openclaw/workspace/daily_push.log
```

## 扩展功能

### 自定义新闻源
修改 `config/config.sh` 中的 `NEWS_SOURCES`：
```bash
NEWS_SOURCES="site:your-news-site.com 重要新闻 OR site:another-site.com 国际新闻"
```

### 多地点支持
可以扩展脚本支持多个地点的天气推送：
```bash
# 在config.sh中添加多个地点
LOCATIONS=("黄埔" "天河" "越秀")
```

### 消息模板自定义
修改 `PUSH_TEMPLATE` 来自定义消息格式：
```bash
PUSH_TEMPLATE="自定义模板 {date} {weather} {news}"
```

## 相关文档
- [weather-api.md](references/weather-api.md) - 天气API文档
- [tavily-api.md](references/tavily-api.md) - Tavily搜索API文档
- [feishu-config.md](references/feishu-config.md) - 飞书推送配置

## 技术依赖
- curl: 用于HTTP请求
- node.js: 用于Tavily搜索
- openclaw: 用于飞书消息推送
- bash: 脚本执行环境