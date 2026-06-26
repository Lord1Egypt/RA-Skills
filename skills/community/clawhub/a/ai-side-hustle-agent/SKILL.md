---
name: side-hustle-agent
version: 1.0.0
description: AI 副业顾问 - 自动扫描接单平台，分析项目可行性，推荐最适合的赚钱机会。适合：想在网上接单赚钱但不知道从哪开始的人。
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["curl"]
---

# AI 副业顾问 Skill

自动扫描接单平台，分析项目可行性，推荐赚钱机会。

## 核心功能

### 1. 平台扫描
自动扫描以下平台：
- Upwork（国际）
- Fiverr（国际）
- 掘金沸点（国内）
- 猪八戒（国内）
- 程序员客栈（国内）

### 2. 项目分析
对每个项目自动分析：
- 预算范围
- 技术要求
- 竞争程度
- 时间成本
- 成功率预估

### 3. 机会推荐
根据你的技能栈，推荐：
- 最适合的项目
- 报价建议
- 提案模板
- 注意事项

## 使用方法

### 扫描今日机会

```
扫描今天适合我的接单机会
```

Agent 会：
1. 访问主要平台
2. 筛选符合条件的项目
3. 按收益/难度排序
4. 给出行动建议

### 分析特定项目

```
分析这个项目：[项目链接]
```

返回：
- 可行性评分（1-10）
- 预计收益
- 时间成本
- 竞争分析
- 报价建议

### 生成提案

```
为这个项目写提案：[项目链接]
```

自动生成：
- 专业提案
- 报价策略
- 时间规划

## 配置文件

### ~/.openclaw/workspace/HUSTLE.md

```yaml
# 你的技能栈
skills:
  - Python
  - Node.js
  - React
  - 微信小程序

# 感兴趣的领域
interests:
  - AI 应用开发
  - 自动化脚本
  - 数据分析
  - 网站开发

# 期望收入（元/月）
target_income: 5000

# 可投入时间（小时/周）
available_hours: 20
```

## 快速命令

### Upwork 扫描

```bash
curl -s "https://www.upwork.com/search/jobs/?q=python" | grep -oP '(?<=title">)[^<]+' | head -10
```

### 掘金沸点

```bash
curl -s "https://api.juejin.cn/recommend_api/v1/short_msg/recommend" \
  -H "Content-Type: application/json" \
  -d '{"id_type":2,"sort_type":200,"cursor":"0","limit":20}' \
  | jq '.data[].msg_Info.content' | head -10
```

## 输出格式

### 机会卡片

```
🎯 [平台] 项目标题
💰 预算：$500-1000
⏰ 截止：3天
📊 匹配度：85%
💡 建议：你的 Python 技能很适合，建议报价 $800
```

### 分析报告

```
📋 项目分析
━━━━━━━━━━━━━━━━
✅ 优势：
  - 技术栈匹配
  - 预算合理

⚠️ 风险：
  - 竞争激烈
  - 时间紧张

💰 建议：报价 $900，3天交付
```

## 注意事项

- 免费平台有限流，建议配合 API Key
- 项目信息实时变化，以平台为准
- 提案发送前人工审核

---

创建：2026-03-11
版本：1.0
