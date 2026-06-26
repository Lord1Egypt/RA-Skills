---
name: chatgpt-search
description: 使用浏览器自动化在 ChatGPT 上搜索问题，获取 AI 回答。无需登录即可使用基础功能。
version: 1.0.0
author: Felix
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["node"]}}}
---

# ChatGPT 搜索 Skill

通过浏览器自动化在 ChatGPT 上提问并获取回答。支持各种查询问题，无需 API Key。

---

## 🚀 快速使用

### 直接使用浏览器工具

在 OpenClaw 会话中直接说：

```
使用 ChatGPT 搜索：[你的问题]
```

例如：
- "使用 ChatGPT 搜索：OpenClaw 最新版本是多少？"
- "使用 ChatGPT 搜索：如何配置 VPS 安全？"
- "使用 ChatGPT 搜索：解释量子计算原理"

### 自动关闭标签页

搜索完成后会**自动关闭**打开的 ChatGPT 标签页，保持浏览器整洁。

---

## 📦 脚本使用

### 基础搜索

```bash
node scripts/chatgpt-search.js "你的问题"
```

### 带上下文搜索

```bash
node scripts/chatgpt-search.js "你的问题" --context "额外背景信息"
```

---

## 🔧 脚本参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索问题（必需） | - |
| `--context` | 额外上下文信息 | 无 |
| `--timeout` | 超时时间（毫秒） | 30000 |
| `--output` | 输出格式（json/text） | text |
| `--keep-open` | 搜索后保持标签页打开 | false（自动关闭） |

---

## 💡 使用场景

| 场景 | 示例 |
|------|------|
| **知识查询** | "Python 异步编程的最佳实践" |
| **代码解释** | "解释这段代码的工作原理" |
| **概念理解** | "什么是区块链？" |
| **问题解决** | "如何调试内存泄漏？" |
| **最新信息** | "2026 年 AI 发展趋势" |

---

## 📝 输出格式

### 文本模式（默认）

```
ChatGPT 回复：

[回答内容]

---
搜索时间：3.2 秒
```

### JSON 模式

```json
{
  "query": "你的问题",
  "answer": "ChatGPT 的回答",
  "elapsedSeconds": "3.2",
  "timestamp": "2026-03-17T23:47:00Z"
}
```

---

## ⚠️ 注意事项

1. **无需登录**：基础功能无需 ChatGPT 账号
2. **登录限制**：部分高级功能可能需要登录
3. **速率限制**：避免频繁请求，建议间隔 5-10 秒
4. **浏览器依赖**：需要 Chromium 浏览器和 18800 调试端口

---

## 🔍 故障排查

### 问题：浏览器超时

**解决方案：**
```bash
# 检查浏览器是否运行
ps aux | grep chromium

# 重启浏览器
/snap/bin/chromium --remote-debugging-port=18800 --user-data-dir=/tmp/openclaw-chrome &
```

### 问题：ChatGPT 要求登录

**解决方案：**
- 简单问题通常无需登录
- 复杂问题可能需要手动登录
- 考虑使用其他搜索方式（web_search）

### 问题：回答被截断

**解决方案：**
- 增加 `--timeout` 参数
- 拆分复杂问题为多个小问题
- 使用 `--output json` 获取完整内容

---

## 🆚 与其他搜索方式对比

| 方式 | 优势 | 劣势 | 适用场景 |
|------|------|------|---------|
| **chatgpt-search** | AI 整合答案，易于理解 | 速度较慢，需浏览器 | 复杂问题、需要解释 |
| **web_search** | 快速，多来源 | 需要自己整合信息 | 新闻、事实查询 |
| **web_fetch** | 获取特定页面内容 | 仅限单个 URL | 读取已知文章 |

---

## 📋 最佳实践

1. **问题清晰**：明确表达你的问题
2. **提供上下文**：使用 `--context` 添加背景信息
3. **验证答案**：重要信息建议交叉验证
4. **合理使用**：简单问题优先使用 web_search

---

## 🔗 相关 Skill

- `web_search` - 传统搜索引擎
- `web_fetch` - 网页内容提取
- `tavily-search` - AI 优化搜索
- `agent-reach` - 多平台搜索

---

## 📖 示例

### 示例 1：查询技术信息

```bash
node scripts/chatgpt-search.js "OpenClaw 最新版本特性"
```

### 示例 2：代码解释

```bash
node scripts/chatgpt-search.js "解释 async/await 的工作原理" --context "JavaScript 编程"
```

### 示例 3：概念学习

```bash
node scripts/chatgpt-search.js "什么是向量数据库？" --output json
```

---

## 📅 更新日志

### v1.0.0 (2026-03-17)
- 初始版本
- 支持基础问答功能
- 支持文本和 JSON 输出格式
- 浏览器自动化集成
