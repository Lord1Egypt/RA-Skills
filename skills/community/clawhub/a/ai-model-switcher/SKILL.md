---
name: ai-model-switcher
description: "AI模型切换器：日常本地模型 + 复杂任务云模型的混合使用方案。根据任务类型自动选择最优模型，最大化利用本地模型（零token成本），最小化云模型token消耗。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎩",
        "author": "小六管家",
        "version": "1.0.0",
        "created": "2026-03-27",
        "category": "productivity",
        "tags": ["model-switching", "cost-optimization", "hybrid-ai", "local-ai", "cloud-ai"],
        "requires": { "bins": ["openclaw"] },
        "recommends": { "bins": ["ollama"] }
      },
  }
---

# 🎩 AI模型切换器

## 概述

**AI模型切换器**是一个为OpenClaw用户设计的智能模型切换工具。采用**日常本地模型 + 复杂任务云模型**的混合使用策略，根据任务类型自动选择最优模型，实现成本优化和性能平衡。

### 核心价值
- **零成本日常使用**：最大化利用本地模型（Ollama）
- **智能任务识别**：7种任务类型自动匹配最优模型
- **成本透明化**：详细的token消耗和成本统计
- **易于使用**：简单的OpenClaw命令接口

## 快速开始

### 安装后使用
```bash
# 查看系统状态
openclaw skill ai-model-switcher status

# 日常对话模式（本地模型，零成本）
openclaw skill ai-model-switcher chat

# 研究模式（推理云模型）
openclaw skill ai-model-switcher research

# 编程模式（云模型）
openclaw skill ai-model-switcher code

# 查看使用统计
openclaw skill ai-model-switcher stats
```

## 功能特性

### 1. 智能任务识别
| 任务类型 | 命令 | 推荐模型 | 描述 |
|---------|------|---------|------|
| 日常对话 | `chat` | 本地模型 | 日常聊天、简单问答 |
| 简单问答 | `simple` | 本地模型 | 信息查询、基础问题 |
| 研究分析 | `research` | 推理云模型 | 复杂推理、研究任务 |
| 长文档处理 | `longdoc` | Kimi云模型 | 长文本分析、多文件处理 |
| 编程开发 | `code` | DeepSeek云模型 | 代码生成、技术问题 |
| 数据分析 | `analysis` | 推理云模型 | 数据分析、统计计算 |
| 创意写作 | `creative` | DeepSeek云模型 | 创意写作、内容生成 |

### 2. 成本优化策略
- **激进模式**：尽可能使用本地模型，最小化成本
- **平衡模式**：智能平衡本地和云模型使用（默认）
- **性能模式**：优先使用高性能云模型

### 3. 支持的模型
- **本地模型**：`ollama:deepseek-r1:14b`（零成本）
- **DeepSeek通用模型**：`deepseek/deepseek-chat`
- **DeepSeek推理模型**：`deepseek/deepseek-reasoner`
- **Kimi长文本模型**：`moonshot/kimi-k2.5`

## 配置文件

技能使用JSON配置文件，支持完全自定义：
- 添加新模型
- 定义新任务类型
- 调整成本策略
- 启用/禁用功能

## 使用统计

技能记录详细的使用信息：
- 模型切换次数
- Token消耗统计
- 成本计算
- 切换历史记录

## 故障排除

### 常见问题
1. **技能无法安装**：检查OpenClaw版本和网络连接
2. **命令不工作**：确保技能已正确安装和加载
3. **模型切换失败**：检查模型配置和API密钥

### 获取帮助
- 查看详细文档：`docs/README.md`
- 报告问题：通过OpenClaw社区
- 功能建议：欢迎提出改进建议

## 许可证

本项目采用 **MIT-0 License**，允许商业使用、修改和分发。

## 关于作者

**小六管家** - OpenClaw智能助手开发者

### 开发理念
- **用户至上**：以用户需求为核心
- **技术实用**：注重实际使用效果
- **持续改进**：根据反馈不断优化
- **开源共享**：促进技术交流和进步