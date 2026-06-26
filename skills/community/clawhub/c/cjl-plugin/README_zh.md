---
languages:
  - en
  - zh
  - ja
---

# CJL 技能集合

个人 Claude Code 插件，提供 17 个可用于生产环境的技能，涵盖研究、内容创作、演示文稿设计和工作流自动化。

**English** | [简体中文](./README_zh.md) | [日本語](./README_ja.md)

---

## 技能一览

| 技能 | 命令 | 说明 |
|------|------|------|
| `cjl-card` | `/cjl-card` | 内容 → PNG 可视化（长图、信息图、海报） |
| `cjl-paper` | `/cjl-paper` | 学术论文分析流程 |
| `cjl-paper-flow` | `/cjl-paper-flow` | 论文分析 + PNG 卡片组合工作流 |
| `cjl-paper-river` | `/cjl-paper-river` | 学术论文溯源 / 引用关系追踪 |
| `cjl-plain` | `/cjl-plain` | 简明语言重写器 |
| `cjl-rank` | `/cjl-rank` | 降维分析 |
| `cjl-relationship` | `/cjl-relationship` | 关系分析 |
| `cjl-roundtable` | `/cjl-roundtable` | 多视角圆桌讨论 |
| `cjl-skill-map` | `/cjl-skill-map` | 已安装技能可视化总览 |
| `cjl-travel` | `/cjl-travel` | 城市旅行研究工作流 |
| `cjl-word` | `/cjl-word` | 英语单词深度学习（含词源） |
| `cjl-word-flow` | `/cjl-word-flow` | 单词分析 → 信息图卡片 |
| `cjl-writes` | `/cjl-writes` | 写作引擎，梳理思路 |
| `cjl-x-download` | `/cjl-x-download` | X/Twitter 媒体下载器 |
| `cjl-learn` | `/cjl-learn` | 概念拆解与学习 |
| `cjl-invest` | `/cjl-invest` | 投资研究与分析 |
| `cjl-slides` | `/cjl-slides` | HTML 演示文稿，24 种国际设计风格 |

---

## 设计理念

每个技能遵循以下原则：

- **原子化**：一个技能，一个职责
- **可观测**：输入 → 输出合约清晰
- **自包含**：无外部状态依赖
- **用户可触发**：通过 `/技能名` 或自然语言激活

---

## 使用方法

### 插件方式安装

```bash
/install-plugin https://github.com/0xcjl/cjl-plugin
```

### 手动安装

```bash
git clone https://github.com/0xcjl/cjl-plugin ~/.claude/plugins/cjl-plugin
```

### 激活技能

```
/cjl-paper
/cjl-slides
/cjl-card
```

---

## 依赖

| 技能 | 依赖 | 安装方式 |
|------|------|---------|
| `cjl-card` | Node.js + Playwright | 参见 [cjl-card 文档](https://github.com/0xcjl/cjl-plugin/tree/main/skills/cjl-card) |

---

## 开发指南

详见 [CLAUDE.md](./CLAUDE_zh.md)。

---

## 致谢

本集合技能改编自 [lijigang/ljg-skills](https://github.com/lijigang/ljg-skills)，已完成技能重命名（`ljg-` → `cjl-`），并新增 `cjl-slides` 技能。

---

## 许可证

MIT
