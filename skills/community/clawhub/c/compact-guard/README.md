# Smart Compact

智能压缩增强。在压缩对话上下文前，先扫描工具输出、提取重要信息到记忆文件、生成检查清单，确保不丢失关键内容。

## 安装

```bash
clawhub install smart-compact
```

```bash
git clone https://github.com/wavmson/openclaw-skill-smart-compact.git ~/.openclaw/skills/smart-compact
```

## 使用

对 Agent 说"智能压缩"或"smart-compact"即可触发。

四个阶段：扫描工具输出 → 提取重要信息到记忆文件 → 生成压缩前检查清单 → 用户确认后压缩。

## 设计原则

- 先救后压，宁可多存也不能漏存
- 只追加记忆文件，绝不覆盖已有内容
- 必须用户确认才执行压缩操作
- 每一步操作都有详细报告
- 重复执行不会产生副作用

## 与 Memory-Dream 搭配

Smart Compact 负责实时保护，Memory-Dream 负责定期整合。两者互补。

## 许可

MIT
