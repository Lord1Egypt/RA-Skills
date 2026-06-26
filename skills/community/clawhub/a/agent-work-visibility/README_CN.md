# Agent Work Visibility v3.0.4

**系统级任务透明层 - 安装即用**

> 让长任务不再黑箱，让用户更安心。
> 
> 这不是一个技能，而是 Agent 的职业本能。

---

## 🚀 快速开始

### 1. 安装

```bash
clawhub install agent-work-visibility
```

### 2. 激活

```bash
# 运行激活脚本（注入协议到 SOUL.md）
node ~/.openclaw/skills/agent-work-visibility/activate.js
```

### 3. 使用

**开启新会话**，然后发送任意长任务指令：

```
查询 bnb memecoin top3
```

**预期输出：**
```
🟢 查询 BNB MemeCoin Top3
━━━━━━━━━━━━━━━━━━━
进度：[█████░░░░░░░░░░░░░░░] 25% (1/4)
━━━━━━━━━━━━━━━━━━━
健康度：🟢 健康 (100/100)
当前阶段：连接 API
正在做什么：正在获取 BNB 链 MemeCoin 数据
已运行：0 分钟
```

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **自动触发** | 基于任务属性（API/联网/多步），不依赖用户措辞 |
| **进度条展示** | `[████████████░░░░░░░░] 60%` 直观展示完成度 |
| **每分钟更新** | 即使无进展也自动刷新状态 |
| **健康度指标** | 🟢🟡🟠 根据任务状态动态变化 |
| **具体动作描述** | 拒绝"正在处理"，显示"正在比较 3 个数据源" |

---

## 📋 触发条件

只要任务涉及以下任一属性，**自动启动透明层**：

- 🔌 外部 API 调用 (crypto-market-rank, web_search, 等)
- ⛓️ 链上数据抓取 (query-address-info, query-token-info, 等)
- 🌐 联网操作 (web_fetch, browser, 等)
- 🧩 多步推理 (步骤≥3 的分析/比较/调研)
- 🤖 子 Agent 协作 (调用其他 bot/skill)
- ⏱️ 预计耗时>10 秒

---

## 🔧 CLI 使用指南

### 创建任务

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js create task-001 "查询 BNB MemeCoin Top3" api
```

### 更新进度

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "连接 API" 25 "正在获取数据"
```

### 完成任务

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js complete task-001
```

### 查看状态

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js status task-001
```

### 报告阻塞

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js block task-001 "API 响应超时"
```

---

## 🧪 测试用例

### 测试 1：Crypto 排行榜

```bash
# 创建
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js create task-001 "查询 BNB MemeCoin Top3" api

# 更新
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "连接 API" 25 "正在获取数据"
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "数据处理" 50 "正在解析结果"
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-001 "生成结果" 75 "正在整理输出"

# 完成
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js complete task-001
```

### 测试 2：链上查询

```bash
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js create task-002 "查询地址持仓" onchain
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js update task-002 "连接 RPC" 30 "正在读取链上数据"
node ~/.openclaw/skills/agent-work-visibility/bin/agent-visibility-v3.js complete task-002
```

---

## 📄 文件结构

```
agent-work-visibility/
├── SKILL.md                  # 技能规范
├── activate.js               # 激活脚本
├── README.md                 # 英文文档
├── README_CN.md              # 中文文档
└── bin/
    ├── agent-visibility-v3.js  # v3 CLI（简化版）
    └── monitor.js              # v2 CLI（完整版）
```

---

## ❓ FAQ

### Q: 为什么需要手动运行 activate.js？

A: OpenClaw 技能系统目前不支持完全自动激活。激活脚本确保协议注入到 Agent 的核心身份（SOUL.md）中。

### Q: 激活后多久生效？

A: **下次会话**生效。需要开启新会话让 Agent 重新读取 SOUL.md。

### Q: 可以禁用吗？

A: 可以。从 SOUL.md 或 AGENTS.md 中删除"强制协议：任务透明层"部分即可。

### Q: 会影响简单任务吗？

A: 不会。只有涉及外部 API、联网、多步推理的任务才会触发。

---

## 📋 版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| v0.1.0 | 2026-03-18 | MVP 初始版本 |
| v0.2.0 | 2026-03-18 | Phase 2 验证 |
| v2.0.0 | 2026-03-18 | 主动工作协议重构 |
| v2.1.0 | 2026-03-19 | 进度条展示 + 每分钟自动更新 |
| v3.0.0 | 2026-03-19 | **系统级透明层 + CLI v3** |

---

## 🤝 Contributing

欢迎贡献！Issues & PRs 都是欢迎的。

**License:** MIT

---

**让长任务不再黑箱，让用户更安心。**

**This is not a skill. This is professional conduct.**
