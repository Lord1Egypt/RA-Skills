# 🧠 First Principles — 第一性原理思维框架

> 让 AI Agent 从问题本质出发，不从惯例或模板出发。

---

## 中文说明

### 这是什么？

AI Agent 最常见的问题不是能力不够，而是**思维方式不对**：

- 🤖 用户说啥就做啥，不质疑方案是否最优
- 📋 套模板，不管具体场景适不适合
- 🩹 出问题打补丁，不追根因
- 💬 输出一堆废话，重点淹没在客套里

First Principles 是一个**始终生效的思维框架 Skill**，改变 Agent 的决策方式。

### 四条铁律

| # | 铁律 | 含义 |
|---|------|------|
| 1 | **不假设** | 动机或目标不清晰时，停下来讨论，不猜 |
| 2 | **不绕路** | 路径不是最短的，直接告诉用户并建议更好方案 |
| 3 | **不补丁** | 遇到问题追根因，不打表面补丁 |
| 4 | **不废话** | 砍掉一切不改变决策的信息 |

### 安装

**通过 ClawHub 安装（推荐）：**

```bash
clawhub install first-principles
```

**从 GitHub 克隆：**

```bash
git clone https://github.com/wavmson/openclaw-skill-first-principles.git \
  ~/.openclaw/skills/first-principles
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 效果对比

**没有 First Principles：**
```
用户：帮我写个脚本监控服务器
Agent：好的！我来帮你写一个服务器监控脚本。首先我们需要...（洋洋洒洒500字）
```

**有 First Principles：**
```
用户：帮我写个脚本监控服务器
Agent：监控什么指标？CPU/内存/磁盘/网络？异常时怎么通知你？
      另外，如果只是基础监控，直接用 uptime-kuma 比写脚本快10倍。你的场景需要自定义吗？
```

### 特性

- ✅ `alwaysLoad: true` — 自动生效，无需手动触发
- ✅ 反模式检测 — 自动识别模板思维、过度工程、表面修复等
- ✅ 决策日志 — 非显而易见的决策自动记录原因
- ✅ 零依赖 — 纯思维框架，不需要任何外部工具

---

## English

### What is this?

A thinking framework Skill that forces AI Agents to reason from first principles — starting from the actual problem, not from conventions or templates.

### Four Rules

1. **Don't assume** — If motivation or goals are unclear, stop and ask
2. **Don't detour** — If there's a shorter path, say so directly
3. **Don't patch** — Chase root causes, not symptoms
4. **Don't ramble** — Cut everything that doesn't change the decision

### Install

```bash
clawhub install first-principles
```

Or clone from GitHub:

```bash
git clone https://github.com/wavmson/openclaw-skill-first-principles.git \
  ~/.openclaw/skills/first-principles
```

---

## Part of the OpenClaw Agent Safety & Ops Series

| # | Skill | Purpose |
|---|-------|---------|
| 1 | 🌙 Memory Dream | Memory consolidation during sleep |
| 2 | 📝 Smart Compact | Context compression before overflow |
| 3 | 🔄 Session Resume | Task recovery after disconnection |
| 4 | 🐝 Swarm Coord | Multi-agent parallel task dispatch |
| 5 | 🛡️ Hook Guard | Safety hooks for dangerous operations |
| 6 | 🏥 Context Doctor | Session health diagnostics |
| 7 | 🧠 **First Principles** | **First-principles thinking framework** |

## License

MIT
