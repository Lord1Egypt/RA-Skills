---
name: code-review-assistant
description: 代码审查助手 - 自动分析代码，提供审查意见、性能优化建议、安全漏洞检测。支持多种编程语言，生成详细的代码审查报告。
homepage: https://github.com/openclaw/code-review-assistant
metadata:
  openclaw:
    emoji: 🔍
    requires:
      bins: ["node"]
---

# 代码审查助手

自动代码审查，提升代码质量。

## 功能特点

- 🔍 **自动审查** - 分析代码结构和风格
- ⚡ **性能优化** - 识别性能瓶颈
- 🔒 **安全检测** - 发现潜在安全漏洞
- 📊 **质量报告** - 生成详细审查报告
- 🛠️ **多语言支持** - 支持 JS/Python/Go/Java 等

## 使用方法

```bash
node scripts/review.mjs --file ./src/app.js
```

## License

MIT
