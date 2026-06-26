---
name: ai-trends-reporter
description: AI前沿动态和ClawHub技能推荐报告生成器。自动搜索最新AI新闻、对比ClawHub上用户未安装的Skills，生成结构化报告。支持web search和ClawHub搜索。
metadata: {"openclaw":{"emoji":"📊","requires":{"env":["BRAVE_API_KEY"]},"optional":{"env":["CLAWHUB_TOKEN"]}}}
---

# AI Trends Reporter

> AI前沿动态 + ClawHub好物推荐，一键生成报告

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com)

## 🎯 功能特性

1. **AI前沿动态搜索** - 搜索最新AI新闻和趋势（需要 Brave Search API）
2. **ClawHub Skills推荐** - 对比用户已安装的Skills，推荐未安装的高评分Skills
3. **结构化报告** - 生成易于阅读的报告格式
4. **个性化推荐** - 根据用户已有Skills推断需求，精准推荐

## 📋 使用场景

- 📰 每日/每周AI资讯简报
- 🔍 发现新的ClawHub Skills
- 📈 了解AI行业最新动态
- 🎁 获取新Tools和Skills安装建议

## 🚀 快速开始

### 基础命令

```
请帮我生成AI前沿动态和技能推荐报告
```

### 可选参数

```
- 报告类型：每日简报 / 每周总结 / 专题分析
- 关注领域：大模型 / AI Agent / 开发工具 / 自动化
- 推荐数量：少量(3-5) / 中等(8-10) / 大量(15+)
```

## 📊 报告内容

生成的报告包含以下板块：

### 1. AI前沿动态
- 最新AI新闻和模型更新
- 行业趋势分析
- 重点技术突破

### 2. ClawHub Skills推荐
- 高评分但未安装的Skills
- 按类别分组（自动化、开发、媒体、社媒等）
- 简明简介和用途说明

### 3. 安装建议
- 针对用户需求的推荐
- 优先级排序
- 简要安装指引

## ⚙️ 配置说明

### Brave Search API（必需）

用于搜索AI新闻，需要配置 API Key：

```bash
openclaw configure --section web
```

或设置环境变量：
```bash
export BRAVE_API_KEY="your_api_key"
```

获取 API Key：https://brave.com/search/api/

### ClawHub Token（可选）

用于获取更准确的Skills排名：

```bash
export CLAWHUB_TOKEN="your_token"
```

## 📝 使用示例

### 示例1：生成每日简报
```
生成一份AI前沿动态报告
```

### 示例2：定制化报告
```
帮我生成一份本周AI动态报告，重点关注AI Agent和自动化领域的新Skills
```

### 示例3：定期任务
```
每天早上9点自动生成AI前沿动态报告发给我
```

## 🔧 工作原理

1. **获取已安装Skills列表** - 扫描用户的Skills目录
2. **搜索AI新闻** - 调用 Brave Search API 获取最新AI资讯
3. **获取ClawHub热门Skills** - 通过 ClawHub API 获取高评分Skills
4. **智能过滤** - 排除用户已安装的Skills
5. **生成报告** - 整理成结构化的markdown报告

## ⚠️ 注意事项

- 不配置 Brave Search API 也能获取ClawHub Skills推荐
- 报告生成需要网络连接
- 首次使用建议查看完整报告了解推荐逻辑

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License
