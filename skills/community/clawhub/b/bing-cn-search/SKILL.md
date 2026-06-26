---
name: bing-search
description: |
  使用必应中文搜索(Bing CN)获取互联网信息。当用户询问新闻、时事、需要搜索互联网内容、或提到"搜索一下"、"查一下"、"网上说"等场景时触发。
triggers:
  - 新闻
  - 最新
  - 搜索
  - 查一下
  - 网上
  - 百度一下
  - 谷歌一下
  - 搜一下
  - 什么消息
  - 发生了什么
  - 时事
  - 热点
  - 热搜
---

# Bing Search Skill

使用必应中文搜索引擎(Bing CN)获取互联网实时信息。

## 前置条件

### 1. 安装 mcporter CLI

```bash
npm install -g mcporter
```

### 2. 安装 bing-cn-mcp

```bash
mkdir -p ~/bing-mcp-test && cd ~/bing-mcp-test
npm init -y
npm install bing-cn-mcp
```

### 3. 配置 MCP 服务器

```bash
mcporter config add bing-cn --command "node ~/bing-mcp-test/node_modules/bing-cn-mcp/build/index.js"
```

### 4. 验证安装

```bash
mcporter list bing-cn
```

## 触发条件

当用户输入包含以下意图时触发此 skill：

- "搜索一下..."
- "查一下..."
- "网上说..."
- "有什么新闻"
- "最近发生了什么"
- "...的最新消息"

## 工作流程

### Step 1: 提取搜索关键词

从用户输入中提取核心搜索词。

### Step 2: 调用 Bing 搜索

```bash
mcporter call bing-cn.bing_search query="<关键词>" count=10
```

### Step 3: 处理搜索结果

阅读搜索结果的标题和摘要，理解并归纳信息，用自己的语言整理输出。

### Step 4: 输出格式

直接给出整理后的内容，文末添加 "**信息来源：**" 列出引用的网站。

**格式：**
```
[根据搜索结果整理的内容，用自己的语言表达]

---
**信息来源：**
- [网站名称] (域名)
- [网站名称] (域名)
```

## 限制说明

- **不适用于**：个人隐私查询、本地文件搜索、已知的常识性问题
- **搜索结果时效性**：来自必应索引，可能存在数小时至数天的延迟
- **内容准确性**：搜索结果由第三方网站提供，需用户自行判断
