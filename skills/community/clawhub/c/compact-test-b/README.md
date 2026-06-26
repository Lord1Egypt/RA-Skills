# 🔍 Smart Compact — 智能压缩增强

> 让 OpenClaw 的 /compact 不再丢失重要信息。先救后压，四阶段智能上下文管理。

---

## 中文说明

### 这是什么？

AI Agent 对话越长，上下文越大，token 消耗越快。压缩上下文是必须的，但 OpenClaw 原生的 `/compact` 是一步到位的压缩——整个对话被浓缩成一段摘要，过程中**大量细节会丢失**。

你有没有遇到过这些情况？
- Agent 压缩后忘了刚才调试好的 API 端点
- 配置文件的路径、IP、端口信息全部丢失
- 之前踩过的坑，压缩后又要重新踩一遍
- 做了某个决策，压缩后连原因都想不起来了

**Smart Compact** 在 `/compact` 之前插入一个"预处理"阶段：**先把重要信息救出来，写入记忆文件，确认安全后再压缩**。

### 核心理念：先救后压

传统压缩是一刀切，Smart Compact 采用**四阶段渐进式**策略：

```
阶段一「扫描」 → 阶段二「提取」 → 阶段三「检查」 → 阶段四「压缩」
```

每个阶段都有明确的职责，确保信息不会在压缩中意外丢失。

### 安装

**方式一（推荐）：通过 ClawHub**

```bash
clawhub install smart-compact
```

**方式二：从 GitHub 克隆**

```bash
git clone https://github.com/wavmson/openclaw-skill-smart-compact.git \
  ~/.openclaw/skills/smart-compact
```

**方式三：只复制核心文件**

```bash
mkdir -p ~/.openclaw/skills/smart-compact
curl -o ~/.openclaw/skills/smart-compact/SKILL.md \
  https://raw.githubusercontent.com/wavmson/openclaw-skill-smart-compact/main/SKILL.md
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 使用方法
