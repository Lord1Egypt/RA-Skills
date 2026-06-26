# auto-context

> 智能上下文卫生检查器

[English](./README.md) · [日本語](./README_ja.md) · [Español](./README_es.md)

## 概述

**auto-context** 是专为 AI 编码助手设计的智能上下文健康检查器。它分析会话的上下文污染程度（长对话、主题漂移、噪声累积），并建议操作：continue、/fork、/btw 或新会话。

## 为什么需要这个技能？

上下文管理对 AI 代理至关重要。随着对话变长，上下文污染（主题漂移、噪声累积、冗余工具调用）会降低响应质量。传统解决方案（如压缩或会话重置）是响应式的——AutoContext 提供**主动建议**，在问题发生前预防。

### 研究基础
- 上下文窗口管理相关 ArXiv 论文
- 认知负荷理论（心理学）
- 人机交互中工作记忆的局限性

## 功能特性

### 多维度评估（5维度）

| 维度 | 指标 | 阈值 | 权重 |
|------|------|------|------|
| 对话长度 | 连续轮数 | >30 轮 | 20% |
| 主题连贯性 | 漂移次数 | 2+ 次 | 25% |
| 信息密度 | 字/轮 | <50 | 15% |
| 工具效率 | 有效产出 | <10% | 20% |
| 压缩次数 | 压缩触发 | 2+ 次 | 20% |

### 健康等级

- 🟢 **HEALTHY** (80-100): 继续当前话题
- 🟡 **NOISY** (60-79): 可继续但注意效率
- 🔴 **POLLUTED** (40-59): 建议 /fork 或 /btw
- ⛔ **CRITICAL** (<40): 建议新会话

### 双触发模式

1. **手动**: `/auto-context` 获取完整健康报告
2. **自动**: 响应层检测到信号时触发

### 自动触发信号

- 连续 20+ 轮无明显进展
- 主题漂移（当前话题与 5 轮前话题无关）
- 噪声累积（连续 3 轮用户输入 < 10 字）
- 工具重复（相同工具连续调用 5+ 次无有效产出）
- 记忆模糊（开始混淆之前会话内容）
- 频繁压缩（已执行 2+ 次压缩）

## 安装

### Hermes Agent
```bash
# 手动触发
/auto-context

# 自动模式默认启用
```

### Claude Code / OpenClaw
```bash
# 通过 Skill 市场或手动克隆
git clone https://github.com/0xcjl/auto-context.git ~/.claude/skills/auto-context
```

## 使用方法

### 手动模式
```
/auto-context
```

输出：
```
🧠 上下文健康报告
  • 32轮对话，1次主题漂移，信息密度中
  • 等级：🟡 NOISY
  • 建议：可继续，但考虑用 /btw 聚焦新话题
```

### 自动模式
检测到信号时自动触发。示例：
- "会话有点长，建议 /fork 保持效率"

## 与现有系统的集成

| 系统 | 角色 | 集成方式 |
|------|------|----------|
| MEMORY.md | 长期记忆 | 互补 |
| compression | 自动压缩 | 压缩前主动建议 |
| session_reset | 定时重置 | 智能提醒补充 |

## 致谢

- **原始版本**: [lovstudio/auto-context](https://github.com/lovstudio/skills/tree/main/skills/lovstudio-auto-context)
- **Hermes 适配**: [0xcjl/auto-context](https://github.com/0xcjl/auto-context)
- **研究参考**: 上下文管理 ArXiv 论文、认知心理学

## 许可证

MIT
