---
name: ClawHub Market Analyzer
description: Analyze the ClawHub marketplace to identify money-making opportunities, competition, and pricing strategies for skill creators.
version: 0.1.0
tags:
  - market-research
  - clawhub
  - skill-creation
  - monetization
---

# ClawHub Market Analyzer

## 🎯 概述

为想在 ClawHub 上发布技能（skills）并赚钱的创作者提供市场分析工具。通过分析搜索结果、趋势数据和竞争格局，帮你找到蓝海市场、制定定价策略、优化技能 SEO。

## 🔧 功能

- **analyze <keyword>** - 分析关键词在 ClawHub 上的竞争情况，返回：
  - 相关技能数量
  - 平均评分（近似）
  - 定价策略（若描述中包含 SkillPay 等信息）
  - 入场难度评估
  - 具体建议

- **trends** - 分析近期更新技能的热门类别，识别上升趋势

- **niche-finder** - 自动推荐需求高、竞争少的潜在技能方向

## 📦 安装

```bash
clawhub install clawhub-market-analyzer
```

## 🚀 使用示例

```bash
# 分析 "小红书自动化" 市场
clawhub-market-analyzer analyze "小红书自动化"

# 查看热门类别
clawhub-market-analyzer trends

# 寻找蓝海机会
clawhub-market-analyzer niche-finder
```

## 📋 输出示例

### analyze 输出

```
=== ClawHub 市场分析: 小红书自动化 ===

🔍 发现 8 个相关技能
📈 平均评分: 3.42 (中等竞争)
💰 付费技能比例: 25%
📝 常见关键词: AI, 一键生成, 内容, 笔记

✅ 入场建议: 机会良好
- 竞争适中，仍有空间
- 建议聚焦于"数据分析"或"多平台同步"细分
- 定价参考: $5-15 或 SkillPay订阅模式
- 差异化点: 提供详细的数据可视化、历史趋势对比
```

### trends 输出

```
=== ClawHub 热门类别 (基于最近100个更新) ===

1. 自动化工作流 (12 个技能) - 持续热门
2. 内容生成 (9 个技能) - 稳定增长
3. 合规与安全 (7 个技能) - 新兴
4. 金融与交易 (6 个技能) - 成熟
5. 健康监测 (4 个技能) - 新赛道

🔑 建议: 考虑"合规+自动化"交叉方向
```

### niche-finder 输出

```
=== 推荐蓝海技能方向 ===

1. [高潜力] GDPR 合规自动化
   - 需求: 高 (企业刚需)
   - 竞争: 低 (仅 2 个技能)
   - 预估评分: 3.8+
   - 建议定价: $20-50

2. [稳定] Notion 数据同步专家
   - 需求: 中高
   - 竞争: 中 (5 个技能)
   - 预估评分: 3.5+
   - 建议定价: $10-20

...
```

## 🛠️ 技术实现

- 使用 ClawHub CLI 进行搜索和数据采集
- 本地缓存减少重复查询
- 智能关键词匹配（支持中文分词）
- 可扩展的分析模块

## 📊 数据来源

- `clawhub search` 实时结果
- 本地缓存的 `clawhub explore` 趋势数据

## 🧠 使用场景

- 你有一个技能点子，但不确定市场竞争如何？
- 你想在 ClawHub 上赚第一桶金，但不知道从何入手？
- 你想优化现有技能的标签和描述以获得更多曝光？

本 skill 提供数据驱动的决策支持。

## 🧩 示例工作流

```bash
# 1. 想做一个"小红书数据分析"技能
clawhub-market-analyzer analyze "小红书数据"

# 2. 发现竞争激烈，调整方向为"小红书竞品分析"
clawhub-market-analyzer analyze "小红书竞品"

# 3. 发现机会不错，开始开发

# 4. 定期查看 trends 调整策略
clawhub-market-analyzer trends
```

## 🔐 隐私说明

本 skill 仅使用公开的 ClawHub 数据，不收集个人隐私。

## 📄 许可证

MIT

---

## 开发说明

本 skill 由 AI 助手创建，旨在帮助更多创作者在 ClawHub 生态中成功。
