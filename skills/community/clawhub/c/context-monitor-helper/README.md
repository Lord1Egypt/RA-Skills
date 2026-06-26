# context-monitor ⚡

实时监控会话上下文使用率，在消息底部显示占用百分比，超过阈值时主动提醒用户清理上下文。

## 🎯 功能特性

- **实时显示**：每次回复自动附加上下文使用百分比
- **进度条可视化**：直观的进度条展示使用率
- **智能预警**：超过 70% 时提醒使用 `/new` 或 `/compact`
- **多模型支持**：自动识别不同模型的上下文窗口大小
- **零配置**：安装即用，无需额外设置

## 📦 快速开始

### 安装

```bash
claw skill install context-monitor
```

### 效果预览

**正常使用（<70%）：**
```
[你的回复内容]

---
📊 上下文使用：45% ▓▓▓▓▓▓▓▓░░░░░░░░░ (4500/10000 tokens)
```

**警告状态（≥70%）：**
```
[你的回复内容]

---
⚠️ 上下文使用：78% ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░ (7800/10000 tokens)
💡 建议：使用 /new 开启新会话 或 /compact 压缩上下文
```

**严重警告（≥90%）：**
```
[你的回复内容]

---
🚨 上下文使用：95% ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ (9500/10000 tokens)
⚠️ 严重：上下文即将超限！建议立即使用 /new 开启新会话
```

## 🔧 配置选项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `warningThreshold` | 70 | 警告阈值（百分比） |
| `criticalThreshold` | 90 | 严重警告阈值（百分比） |
| `showProgressBar` | true | 是否显示进度条 |
| `showTokenCount` | true | 是否显示具体 Token 数 |
| `enabled` | true | 是否启用监控 |

## 💡 使用场景

### 1. 长对话管理
避免上下文超限导致 AI 遗忘早期内容，在达到限制前主动清理。

### 2. 多轮调试
监控 Token 消耗，优化对话策略，减少不必要的上下文占用。

### 3. 成本控制
了解每次对话的 Token 使用情况，合理规划使用量。

### 4. 主动清理
在达到限制前及时使用 `/new` 或 `/compact`，保持对话流畅。

## 📋 命令

| 命令 | 说明 |
|------|------|
| `/context` | 查看当前上下文状态 |
| `/context on` | 启用上下文监控 |
| `/context off` | 禁用上下文监控 |
| `/new` | 开启全新会话（清空上下文） |
| `/compact` | 压缩上下文（保留核心信息） |

## 🏗️ 开发

### 环境要求

- Node.js >= 18.0.0
- npm >= 9.0.0

### 安装依赖

```bash
cd context-monitor
npm install
```

### 构建

```bash
npm run build
```

### 测试

```bash
npm test
npm run test:coverage
```

### 发布

```bash
npm run publish
# 或
claw skill publish
```

## 📊 支持的模型

| 模型 | 上下文窗口 |
|------|-----------|
| Qwen3.5-Plus | 256,000 tokens |
| Qwen-Max | 32,000 tokens |
| Claude-3-5-Sonnet | 200,000 tokens |
| Claude-3-Opus | 200,000 tokens |
| GPT-4-Turbo | 128,000 tokens |
| GPT-4o | 128,000 tokens |
| GPT-3.5-Turbo | 16,385 tokens |
| Gemini-Pro | 128,000 tokens |
| 其他模型 | 128,000 tokens (默认) |

## 🐛 常见问题

### Q: 为什么显示的 Token 数和平台统计不一致？

A: 本 Skill 使用估算算法（中文约 1.5 字符/Token，英文约 4 字符/Token），实际 Token 数以平台为准。误差通常在±5% 内。

### Q: 可以关闭上下文显示吗？

A: 可以，使用 `/context off` 临时关闭，`/context on` 重新开启。

### Q: 支持哪些模型？

A: 支持所有 OpenClaw 集成的模型，自动识别上下文窗口大小。未识别的模型使用默认值 128,000 tokens。

### Q: 会影响性能吗？

A: 每次回复增加约 10-20ms 处理时间，对用户体验影响可忽略不计。

### Q: 会存储我的对话内容吗？

A: 不会。本 Skill 仅实时计算 Token 使用量，不存储任何对话内容。

## 📝 更新日志

### v1.0.0 (2026-04-05)
- ✨ 初始版本发布
- ✨ 实时上下文使用率监控
- ✨ 进度条可视化
- ✨ 智能预警系统
- ✨ 多模型支持
- ✨ `/context` 命令支持

## 📄 许可证

MIT License

## 🔗 相关链接

- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills/tree/main/context-monitor)
- [ClawHub 页面](https://clawhub.ai/skills/context-monitor)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [问题反馈](https://github.com/rfdiosuao/openclaw-skills/issues)

## 👨‍💻 作者

**Spark** - OpenClaw Skill 开发专家

---

_让每一次对话都清晰可控 ⚡_
