# 🤖 AI 模型智能管家 (AI Model Steward)

### 全自动 AI 模型监控、情报搜集与智能部署建议系统

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-blue.svg)](https://github.com/openclaw/openclaw)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

---

## 一句话介绍

每天自动搜集网上最新 AI 模型资讯和免费 tokens 领取信息，每周生成部署建议报告，支持一键审批加入模型切换链。

## 功能概览

### 📡 每日模型情报（Daily Intelligence）

- 自动监控 OpenRouter、阿里云、腾讯云、百度等平台的免费模型动态
- 追踪各大厂商（OpenAI、Google、DeepSeek、Qwen、MiniMax、NVIDIA 等）的新模型发布
- 汇总免费 tokens 领取渠道和限时优惠活动
- 存储到飞书多维表格，方便回溯查询

### 📊 周度部署建议（Weekly Deployment Report）

- 基于本周情报数据，AI 自动生成部署建议报告
- 对比新旧模型质量、价格、上下文长度
- 给出"建议新增"、"建议替换"、"建议保留"的明确建议
- 飞书文档呈现，等你一键审批

### 🔌 一键部署到 OpenClaw

- 审批同意后，自动将新模型加入 fallback 链
- 安全回滚机制
- 配置备份

---

## 架构设计

```
┌─────────────┐
│  数据源层    │
│  • 网页抓取  │
│  • API 查询 │
│  • RSS 订阅 │
└──────┬──────┘
       ▼
┌─────────────┐
│  情报处理层  │
│  • 信息提取  │
│  • 去重去噪  │
│  • 质量评分  │
└──────┬──────┘
       ▼
┌─────────────┐
│  存储层      │
│  • 多维表格  │
│  • 本地缓存  │
└──────┬──────┘
       ▼
┌─────────────┐
│  报告生成层  │
│  • AI 分析   │
│  • 模板渲染  │
│  • 飞书文档  │
└──────┬──────┘
       ▼
┌─────────────┐
│  部署层      │
│  • 审批流程  │
│  • 配置更新  │
│  • 安全回滚  │
└─────────────┘
```

---

## 快速开始

### 前置要求

- Python 3.8+
- OpenClaw 已安装
- 飞书 OAuth 已授权（多维表格操作）
- OpenRouter API Key
- `requests` 库

### 安装

```bash
cd ~/.openclaw/workspace/projects/ai-model-steward
pip install -e .
```

### 基础使用

```bash
# 执行今日情报搜集
python -m ai_model_steward daily

# 生成本周部署建议
python -m ai_model_steward weekly

# 查看情报历史
python -m ai_model_steward history

# 手动审批模型
python -m ai_model_steward approve <model_name>

# 部署到 OpenClaw
python -m ai_model_steward deploy
```

---

## 数据源

我们监控以下信息源：

| 来源 | 频率 | 类型 |
|------|------|------|
| OpenRouter Model List | 实时 | API |
| OpenRouter Blog | 每日 | 网页 |
| 机器之心 | 每日 | 网页 |
| 量子位 | 每日 | 网页 |
| HuggingFace Blog | 每日 | RSS |
| 各厂商官方 Twitter/公众号 | 每日 | 网页 |
| Vercel AI SDK Blog | 每周 | 网页 |

---

## 发布平台

| 平台 | 类型 | 链接 |
|------|------|------|
| GitHub | 开源 | https://github.com/<你的 ID>/ai-model-steward |
| DeskHub | 技能市场 | skills.deskclaw.me |
| ClawHub | OpenClaw 官方 | clawhub.com |

---

## License & 赞助

MIT License - 自由使用、修改、分发

如果这个项目帮到你了，欢迎赞助支持开发 ❤️

### 赞助方式

| 方式 | 链接/说明 |
|------|----------|
| **GitHub Sponsors** | <https://github.com/sponsors/HHBB2221> ✅ 已开通 |
| **微信打赏** | 见 [SPONSOR.md](SPONSOR.md)（收款码待上传） |
| **支付宝打赏** | 见 [SPONSOR.md](SPONSOR.md)（收款码待上传） |

---

**所有赞助将用于**:
- 服务器和 API 费用
- 持续开发维护
- 社区支持

感谢每一位支持者！🙏

---

## 变更日志

- **0.1.0** (2025-03-31) - 初始版本，核心框架

---

<p align="center">
  <b>让 AI 管理 AI，人类只管审批</b>
  <br>
  <br>
  <a href="https://github.com">⭐ Star us on GitHub</a>
  ·
  <a href="mailto:your@email.com">📧 联系作者</a>
</p>
