# 📝 智能摘要助手 (Smart Summarizer)

> 🔍 一键提取长文本核心要点，告别信息过载

![Demo](https://img.shields.io/badge/trigger-keyword%20%7C%20length-blue)
![Model](https://img.shields.io/badge/model-any%20LLM-green)
![Lang](https://img.shields.io/badge/lang-ZH%2FEN-brightgreen)

---

## 🌟 核心能力

### ✅ 智能触发机制
- 🔑 **关键词触发**：消息包含 `总结`、`摘要`、`summarize`、`brief` 时自动激活
- 📏 **长度触发**：纯文本超过 100 字符时，即使无关键词也会尝试摘要
- 🎯 **精准匹配**：正则表达式 `/总结|摘要|summarize|brief/i`，不误触日常聊天

### ✅ 专业摘要输出
- 📋 **结构化列表**：自动使用 bullet points 格式，层次清晰
- 🌐 **语言自适应**：输入中文输出中文，输入英文输出英文，混合内容智能处理
- ✂️ **去噪精简**：自动过滤寒暄、重复、无关内容，只保留干货
- ⚡ **快速响应**：温度参数 0.3，确保输出稳定一致

### ✅ 场景全覆盖
| 场景 | 示例输入 | 输出效果 |
|-----|---------|---------|
| 📧 邮件摘要 | 长邮件正文 | 3-5 条核心事项 + 行动点 |
| 🗣️ 会议记录 | 讨论纪要文本 | 议题列表 + 决策结论 + 待办 |
| 📰 文章提炼 | 新闻/博客全文 | 核心观点 + 关键数据 + 结论 |
| 💬 聊天记录 | 群聊长篇讨论 | 争议点 + 共识 + 下一步 |

---

## 🚀 快速开始

### 1️⃣ 安装技能
```bash
openclaw skills install smart-summarizer