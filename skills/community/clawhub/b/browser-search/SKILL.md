---
name: browser-search
description: |
  浏览器搜索技能 - 安全的网页搜索工具
  使用本地浏览器进行自动化搜索和内容提取
  支持 Bing、Google、Baidu、DuckDuckGo 等公开搜索引擎
  无需 API 配置，路径输出受限
---

# Browser Search 技能

使用本地浏览器进行安全的网页搜索和内容提取。

## 安全说明

**仅用于合法用途**，严格遵守以下限制：

- ✅ **仅访问公开搜索引擎**：Bing、Google、Baidu、DuckDuckGo
- ✅ **路径输出受限**：结果文件只能保存到用户主目录
- ✅ **无危险函数**：不使用 eval/exec 等危险函数
- ✅ **严格的超时控制**：防止无限等待
- ❌ **禁止访问敏感站点**：仅支持公开搜索引擎
- ❌ **禁止爬取私有内容**：仅提取搜索结果摘要

## 核心功能

- 🔍 **多搜索引擎支持**：Bing、Google、Baidu、DuckDuckGo
- 📄 **内容提取**：自动提取搜索结果标题和链接
- 💾 **结果保存**：保存到 JSON/TXT/MD 文件（路径受限）

## 使用场景

- 查找最新新闻和资讯
- 搜索技术文档和教程
- 市场调研（仅限公开信息）

## 触发词

- "搜索..."
- "查找..."
- "用浏览器搜索..."
- "帮我找..."

## 快速开始

```bash
# 基本搜索
browser-search "人工智能 2026"

# 指定引擎
browser-search "AI 趋势" --engine bing

# 保存结果
browser-search "Python 教程" --output ~/results.json --max 5
```

## 注意事项

- 需要本地 Chromium 浏览器
- 结果可能受地区限制
- 仅用于合法合规用途
- 输出文件路径必须在用户主目录
