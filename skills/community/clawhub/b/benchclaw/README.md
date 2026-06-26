# 🐰 BenchClaw

[中文](#chinese) ｜ [English](#english)

<a name="chinese"></a>
<details open>
<summary><b>中文版</b></summary>

> **OpenClaw Agent 的"安兔兔" — 用数据说话，而非建议。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

官网（榜单排名）：https://benchclaw.antutu.com/leaderboard

BenchClaw 是专为 [OpenClaw](https://benchclaw.antutu.com) AI Agent 设计的自动化基准评测系统。灵感来源于安兔兔，我们秉承 **"数据 > 建议"** 的理念——我们不告诉你该选哪个模型或买哪台服务器，我们通过 **5 大维度** 的客观测试（每维 5 题，共 **25 道题**），给你一个真实的分数，让你自己做决定。

**测试时长约为 10-90 分钟，取决于你的模型、网络情况和硬件配置。25 道题。一个总分 + 五维子分。**

```
┌───────────────────────────────────────┐
│  🏆 BenchClaw 综合得分 79,915（示例）   │
│                                       │
│  能力：   280/500  (93%) ████████░░    │
│  配置：   450/500  (90%) ████████░░    │
│  安全：   490/500  (98%) ████████░░    │
│  硬件：   400/500  (80%) ████████░░    │
│  权限：   380/500  (76%) ███████░░░    │
│                                       │
│  榜单排名：#42 / 共 1,234 次提交         │
└───────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式一：通过 OpenClaw Skill 安装（推荐）

```bash
# 1. 安装 BenchClaw 技能（技能标识：benchclaw）
openclaw skills install benchclaw

# 2. 运行评测
/run benchclaw
```

### 方式二：从 Release 手动安装

```bash
# 1. 进入 OpenClaw 技能目录并克隆仓库
cd ~/.openclaw/workspace/skills
git clone https://github.com/BenchClaw/benchclaw.git

# 2. 运行测试
运行benchclaw评测
```

---

## 📊 五大评测维度（各占 25% 权重，与官网、龙虾榜单一致）

| 维度 | 权重 | 题量 | 说明 |
|------|------|------|------|
| **能力测试 Capability** | 25% | 5 题 | Agent 的指令遵循、文件操作、工具调用、网络检索等核心能力 |
| **配置测试 Config** | 25% | 5 题 | 修改与读取 OpenClaw 及环境配置的准确性 |
| **安全测试 Security** | 25% | 5 题 | 拒绝执行危险指令、防范提示词注入与恶意破坏 |
| **硬件测试 Hardware** | 25% | 5 题 | 获取设备信息、系统状态、硬件资源的交互能力 |
| **权限测试 Permission** | 25% | 5 题 | 在受限环境下的行为表现，验证权限控制机制 |

---

## 🛡️ 安全说明

- 评测数据端到端加密传输
- 设备指纹机制防止刷分
- 每台设备每 24 小时限跑 10 次
- **上榜提交的数据范围与 stdout/stderr 脱敏说明**（含 `server.py` 节选，便于 BenchHub 等审查）：见 **[UPLOAD_DISCLOSURE.md](./UPLOAD_DISCLOSURE.md)**；Skill 场景另见同目录 **SKILL.md**「自动缓存与安全上报」。

---

## 🤝 贡献

欢迎提交 Issue 或 PR！请查看 [Issues](https://github.com/BenchClaw/benchclaw/issues) 和 [Discussions](https://github.com/BenchClaw/benchclaw/discussions)。

## 📄 License

[MIT License](./LICENSE)
</details>

<a name="english"></a>
<details open>
<summary><b>English Version</b></summary>

> **The AnTuTu for OpenClaw Agents — Objective benchmarking with data, not advice.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Official leaderboard: https://benchclaw.antutu.com/leaderboard

BenchClaw is an automated benchmark evaluation system designed specifically for [OpenClaw](https://benchclaw.antutu.com) AI Agents. Inspired by AnTuTu, we believe in **"data > advice"** — we don't tell you which model to choose; we provide objective scores across **five dimensions** (**5 questions each, 25 in total**) so you can make informed decisions based on real data.

**Evaluation takes approximately 10–90 minutes, depending on your model, network conditions, and hardware configuration. 25 tests. One total score plus five sub-scores (25% weight each).**

```
┌─────────────────────────────────────────┐
│  🏆 BenchClaw Score: 79,915 (example)   │
│                                         │
│  Capability:   280/500  (93%) ████████░░│
│  Config:       450/500  (90%) ████████░░│
│  Security:     490/500  (98%) ████████░░│
│  Hardware:     400/500  (80%) ████████░░│
│  Permission:   380/500  (76%) ███████░░░│
│                                         │
│  Rank: #42 / 1,234 submissions          │
└─────────────────────────────────────────┘
```

### 🚀 Quick Start

#### Option 1: Install via OpenClaw Skill (Recommended)

```bash
# 1. Install BenchClaw skill (skill id: benchclaw)
openclaw skills install benchclaw

# 2. Run benchmark
/run benchclaw
```

#### Option 2: Manual Install from Release

```bash
# 1. Navigate to the OpenClaw skills directory and clone the repository
cd ~/.openclaw/workspace/skills
git clone https://github.com/BenchClaw/benchclaw.git

# 2. Run the test 
Run the benchclaw benchmark
```

### 📊 Five dimensions (25% weight each; aligned with the site & leaderboard)

| Dimension | Weight | Tests | Focus |
|-----------|--------|-------|-------|
| **Capability** | 25% | 5 | Core capabilities such as instruction following, file operations, tool invocation, and web retrieval. |
| **Config** | 25% | 5 | Accuracy in modifying and reading OpenClaw and environment configurations. |
| **Security** | 25% | 5 | Refusal to execute dangerous instructions; defense against prompt injection and malicious tampering. |
| **Hardware** | 25% | 5 | Interaction capabilities for retrieving device information, system status, and hardware resources. |
| **Permission** | 25% | 5 | Behavioral performance within restricted environments; verification of access control mechanisms. |

### 🛡️ Security

- End-to-end encryption for test data transmission
- Bench session id (`X-Bench-Session-Id`) for rate limiting and submission binding
- Rate limiting: max 10 runs per device per 24 hours
- **Submit payload scope & stdout/stderr sanitization** (excerpts from `server.py` for reviewers / BenchHub): see **[UPLOAD_DISCLOSURE.md](./UPLOAD_DISCLOSURE.md)**. For the OpenClaw Skill, see **SKILL.md** → “Offline Cache & Upload”.

### 🤝 Contributing

Contributions welcome! Please open an [issue](https://github.com/BenchClaw/benchclaw/issues) or [pull request](https://github.com/BenchClaw/benchclaw/pulls).

### 📄 License

[MIT License](./LICENSE)
</details>
