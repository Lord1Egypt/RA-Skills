# add-siliconflow-provider

为 [OpenClaw](https://github.com/openclaw/openclaw) 配置 [硅基流动 SiliconFlow](https://siliconflow.cn) 作为模型源的 Skill。

## 🎯 功能

一键接入 SiliconFlow 的 98+ 个 AI 模型，包括：

- 🆓 **免费模型**：Qwen3-8B、DeepSeek-R1-8B 等（无限使用）
- 💰 **性价比模型**：DeepSeek V3.2、Qwen3 Coder 30B（¥0.7-3/M tokens）
- 🚀 **旗舰模型**：Kimi K2.5、Qwen3 Coder 480B、DeepSeek R1

## 📦 包含内容

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 完整配置指南：provider 注册、模型定义、别名配置、fallback 链、验证 |

## 🚀 快速开始

1. **注册 SiliconFlow**：https://cloud.siliconflow.cn/i/ihj5inat （邀请注册双方均获赠额度）
2. **获取 API Key**：控制台 → API 密钥 → 创建
3. **安装 Skill** 后让 OpenClaw agent 执行配置

## 📊 推荐模型

| 别名 | 模型 | 价格 |
|------|------|------|
| `sf-qwen3-8b` | Qwen3 8B | **免费** 🆓 |
| `sf-r1-8b` | DeepSeek R1 蒸馏 8B | **免费** 🆓 |
| `sf-qwen3-30b` | Qwen3 30B MoE | ¥0.7/¥2.8 |
| `sf-coder-30b` | Qwen3 Coder 30B | ¥0.7/¥2.8 |
| `sf-dsv3` | DeepSeek V3.2 | ¥2.0/¥3.0 |
| `sf-r1` | DeepSeek R1 | ¥4.0/¥16.0 |
| `sf-kimi` | Kimi K2.5 | ¥4.0/¥21.0 |
| `sf-coder-480b` | Qwen3 Coder 480B | ¥8.0/¥16.0 |

（价格为 ¥/百万 tokens，输入/输出）

## 🔗 链接

- **SiliconFlow 注册**：https://cloud.siliconflow.cn/i/ihj5inat
- **SiliconFlow 文档**：https://docs.siliconflow.cn
- **SiliconFlow 定价**：https://siliconflow.cn/pricing
- **OpenClaw**：https://github.com/openclaw/openclaw
- **OpenClaw 文档**：https://docs.openclaw.ai

## 📝 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|------|------|----------|--------|
| 2026-02-09 | v1.0 | 初始版本：8 个精选模型，完整配置指南 | ConfigBot (via OpenClaw with Claude Opus 4.6) |
