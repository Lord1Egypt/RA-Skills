# 多渠道聊天纪要助手

> 将来自 Telegram、Slack、企业微信、Discord、钉钉等多个聊天平台的消息，自动整理成结构化纪要，提取摘要、决策、行动项和风险。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-blue.svg)](https://clawhub.com)

## ✨ 特性

- 🔄 **多平台支持** - Telegram、Slack、企业微信、Discord、钉钉、邮件线程
- 🧠 **智能分析** - 自动识别主题、决策、行动项、风险和待跟进问题
- 📊 **结构化输出** - 生成包含摘要、讨论、决策、行动项的完整纪要
- 🎯 **多场景适配** - 站会日报、项目同步、客户反馈、管理层简报
- 🔒 **隐私优先** - 仅处理用户主动提供的内容，不自动连接任何平台
- 🌐 **多语言** - 默认中文，支持英文和其他语言

## 🚀 快速开始

### 最简单的使用方式

```
使用 $multi-channel-chat-minutes

[粘贴你的聊天记录]
```

### 常见场景

**每日站会纪要：**
```
使用 $multi-channel-chat-minutes，整理昨天的项目群聊天，生成站会纪要

[Telegram 群聊记录]
[Slack 频道记录]
```

**客户反馈汇总：**
```
使用 $multi-channel-chat-minutes，把这些客服群消息整理成客户反馈摘要

[客服群聊天记录]
```

**管理层周报：**
```
使用 $multi-channel-chat-minutes，汇总本周所有项目群讨论，输出管理层周报

[多个群的聊天记录]
```

## 📋 输出内容

默认包含以下部分：

- **📊 核心摘要** - 3-5 条关键结论
- **💬 关键讨论** - 按主题分组的详细内容
- **✅ 决策记录** - 明确的决策和结论
- **📋 行动项** - 任务/负责人/截止时间/状态
- **⚠️ 风险与阻塞** - 需要关注的问题
- **❓ 待跟进问题** - 未解决的疑问

## 📖 文档

- [快速开始](QUICKSTART.md) - 5 分钟上手指南
- [SKILL.md](SKILL.md) - 完整的 Skill 说明
- [配置参考](references/config-schema.md) - 高级配置选项
- [输出示例](references/output-examples.md) - 真实场景示例

## 🎯 适用场景

| 场景 | 说明 | 推荐配置 |
|------|------|----------|
| 每日站会 | 汇总昨天的讨论，生成今日站会纪要 | `objective: standup` |
| 项目同步 | 整理多群讨论，同步项目进展 | `summary_level: detailed` |
| 客户反馈 | 汇总客服群消息，提取客户反馈 | `objective: customer_feedback` |
| 管理层简报 | 生成周报或月报，供管理层阅读 | `objective: exec_brief` |

## 🔐 隐私与安全

- ✅ 仅处理用户主动提供的聊天内容
- ✅ 不会自动连接或登录任何聊天平台
- ✅ 自动过滤敏感信息（token、密码、内部链接）
- ✅ 不存储或传输用户数据
- ✅ 拒绝处理无权访问的渠道内容

## 🛠️ 支持的输入格式

- ✅ 直接粘贴的文本
- ✅ 平台导出的聊天记录（TXT、JSON、CSV）
- ✅ OCR 识别后的截图文本
- ✅ 已经整理好的结构化数据

## 📊 输出格式

- **Markdown**（默认）- 适合人类阅读
- **JSON** - 适合程序处理
- **HTML** - 适合网页展示
- **Plain Text** - 适合纯文本环境

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢 OpenClaw 社区的支持和反馈！

---

**Made with ❤️ for the OpenClaw community**
