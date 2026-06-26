---
slug: ai-model-steward
name: ai-model-steward
version: 0.1.0
displayName: AI 模型智能管家
summary: 全自动 AI 模型监控、情报搜集与智能部署建议系统
tags: ai, models, monitoring, intelligence, deployment, openrouter
---

# AI 模型智能管家

全自动监控最新 AI 模型动态，每日搜集免费 tokens 信息，每周生成部署建议，支持一键审批上线。

## 功能

- 📡 **每日情报**: 自动监控 OpenRouter、机器之心、量子位、HuggingFace 等平台
- 🎁 **免费追踪**: 汇总免费 tokens 领取渠道和限时优惠
- 📊 **周报分析**: AI 生成周度部署建议，对比模型质量/价格
- 🔌 **一键部署**: 审批通过后自动加入模型切换链
- 🔄 **安全回滚**: 每次部署自动备份，支持一键回滚

## 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/projects/ai-model-steward
pip install -e .
```

### 手动执行

```bash
# 每日情报
ai-model-steward daily

# 周报
ai-model-steward weekly

# 查看历史
ai-model-steward history

# 审批模型
ai-model-steward approve openrouter/qwen/qwen3-coder:free

# 移除模型
ai-model-steward reject openrouter/qwen/qwen3-coder:free

# 查看当前切换链
ai-model-steward deploy list
```

### 定时任务（自动）

已内置 2 个定时任务：
- **每天 9:00** 执行情报搜集
- **每周一 10:00** 生成周报

## 开源协议

MIT

## 赞助支持

如果这个项目帮到你，欢迎赞助 ❤️

- GitHub Sponsor
- 微信赞赏码
- 支付宝

## 作者

老徐

## 更新日志

- **0.1.0** (2026-03-31) - 初始版本
