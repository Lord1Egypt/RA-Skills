# Agent Memory Protocol

<p align="center">
  <strong>OpenClaw agent 结构化记忆管理 skill — 三层密度结构、会话反思与冲写协议</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/clawhub-agent--memory--protocol-brightgreen?style=for-the-badge" alt="ClawHub">
  <img src="https://img.shields.io/badge/OpenClaw-skill-orange?style=for-the-badge" alt="Skill">
  <img src="https://img.shields.io/badge/许可证-MIT-blue?style=for-the-badge" alt="License">
</p>

[OpenClaw](https://github.com/openclaw/openclaw) 的记忆管理 skill，为 agent 建立一套一致、结构化的记忆体系。定义信息该写到哪里、如何高效检索、何时冲写以避免上下文丢失 — 所有 agent 都可以遵循同一套协议。

## 为什么需要它

随着 agent 处理的任务增多、session 不断积累，记忆会变得碎片化。没有协议时：
- 同一事实被写在多处，逐渐不同步
- 重要决策被埋在 session 日志里，压缩后丢失
- Agent 浪费 token 通读所有内容，而不是直接定位到正确的文件

这个 skill 解决上述三个问题。

## 包含内容

### 三层密度结构

| 层级 | 文件 | 作用 |
|------|------|------|
| **L0** | `MEMORY.md` | 极简索引 — 每类 1-3 句 + 路径指针。永远先读这里。 |
| **L1** | `memory/INDEX.md` | 各分类概览导航（约 500-1000 字）。 |
| **L2** | `memory/user/` `memory/agent/` | 完整详情，按需读取。 |

检索成本按需扩展：L0 始终快速；只在需要细节时才深入 L2。

### 六分类写入规范

```
新信息 → 分类判断
  ├── 用户身份/背景 → user/profile.md
  ├── 偏好/习惯 → user/preferences/[主题].md
  ├── 项目/工具/人物 → user/entities/[类型].md
  ├── 重要决策/事件 → user/events/YYYY-MM-[名称].md  （只增不改）
  ├── 首次处理的新类型任务 → agent/cases/[名称].md    （只增不改）
  └── 发现可复用规律 → agent/patterns/[名称].md
```

### 会话反思

session 结束时，如果包含纠正、失败或发现更优方案，提炼一条 pattern。同一条目被触发 ≥3 次后升级为 instinct。

### Flush Checklist

session 结束或压缩前扫描的 6 项检查 — 防止容易遗漏的内容丢失：偏好、项目进度、决策、实体更新、规律、纠正。

### 上下文压力协议

在 50 / 70 / 85% 上下文用量设置阈值，对应逐级升高的冲写紧迫度。

### 子代理写入规则

明确哪个 agent 写什么内容，以及编排 agent 如何同步 L0/L1 索引。

## 安装

```bash
clawhub install agent-memory-protocol
```

或直接克隆：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OttoPrua/openclaw-memory-manager.git memory-manager
```

## 使用

Skill 在触发记忆相关操作时自动激活。也可手动加载：

```
读取 memory-manager skill 并按协议执行本次写入。
```

触发词：`记住这个`、`更新记忆`、`memory write`、`flush memory`

## 目录结构（初始化后）

```
memory/
├── INDEX.md                    ← L1 导航
├── user/
│   ├── profile.md
│   ├── preferences/
│   │   ├── learning.md
│   │   ├── lifestyle.md
│   │   ├── tech.md
│   │   └── communication.md
│   ├── entities/
│   │   ├── tools.md
│   │   └── people.md
│   └── events/
└── agent/
    ├── cases/
    └── patterns/
```

## 外部工具与集成

Skill 协议定义写入/读取规则。实际检索基础设施使用两个外部工具：

- **[qmd](https://github.com/tobilen/qmd)** — 对 `memory/` 和 `blackboard/` Markdown 文件做本地语义搜索（驱动 `memory_search`）
- **[LosslessClaw](https://github.com/martian-engineering/lossless-claw)** — DAG 分层上下文压缩；将历史 session 压缩为可恢复的摘要，通过 `lcm_grep` / `lcm_expand` 访问

完整配置指南 → **[MEMORY-STACK.zh-CN.md](MEMORY-STACK.zh-CN.md)**

## 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw) — 核心 Gateway
- [OpenClaw 文档](https://docs.openclaw.ai) — 完整文档
- [ClawHub: agent-memory-protocol](https://clawhub.ai/OttoPrua/agent-memory-protocol) — 从 ClawHub 安装
- [Discord](https://discord.gg/clawd) — 社区

## 许可证

MIT
