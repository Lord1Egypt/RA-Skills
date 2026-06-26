# 🏥 Context Doctor — 上下文诊断 Skill

> 给你的 AI 对话装一个油量表。随时知道 context 用了多少、还剩多少、什么时候该加油。

---

## 中文说明

### 这是什么？

每次和 AI Agent 对话都有一个看不见的上限 —— context window。就像汽车的油箱：

- 🚗 开着开着油就用完了
- ⛽ 但你看不到油量表
- 💥 没油了要么抛锚（报错），要么紧急加油（强制压缩丢信息）

Context Doctor 就是这个油量表。对 Agent 说"体检"，立刻看到：
- 🔋 context 用了多少，还剩多少
- 🔍 哪些操作最占空间
- 🔮 预估还能聊多少轮
- 💡 什么时候该 compact

### 安装

**通过 ClawHub 安装（推荐）：**

```bash
clawhub install context-doctor
```

**从 GitHub 克隆：**

```bash
git clone https://github.com/wavmson/openclaw-skill-context-doctor.git \
  ~/.openclaw/skills/context-doctor
```

安装后重启 Gateway：

```bash
openclaw gateway restart
```

### 触发方式

| 说法 | 效果 |
|------|------|
| `体检` | 完整诊断报告 |
| `诊断` | 完整诊断报告 |
| `context doctor` | 完整诊断报告 |
| `还能聊多久` | 快速预估剩余轮次 |
| `token 用了多少` | 简要消耗统计 |

### 诊断报告示例

```
🏥 Context Doctor 诊断报告
━━━━━━━━━━━━━━━━━━━━━

📊 综合评分：B（良好）

🔋 Context 油量
████████████░░░░░░░░ 58%

📈 消耗统计
├─ 对话轮次：23 轮
├─ 输入 tokens：89,000
├─ 输出 tokens：27,000
├─ 费用：$0.42
└─ 平均每轮：5,043 tokens

🔍 空间占用 TOP 5
1. exec(cat large-file.log) — 12,300 tokens
2. web_fetch(docs.example.com) — 8,200 tokens
3. read(MEMORY.md) — 4,500 tokens
4. exec(git log) — 3,800 tokens
5. web_search(...) — 2,100 tokens

🔮 预测
├─ 预估剩余：约 17 轮
├─ 建议 compact：再聊 10 轮后
└─ 当前节奏：约 35 分钟后达到 80%

💡 优化建议
1. exec 命令加 | head -50 限制输出
2. 大文件分段读取
3. 下个自然断点执行 compact
```

### 健康评分标准

| 评分 | 含义 | Context 使用率 | 建议 |
|------|------|---------------|------|
| A 优秀 | 全绿灯 | 低于 50% | 放心继续 |
| B 良好 | 个别黄灯 | 50-65% | 留意但不急 |
| C 注意 | 多个黄灯 | 65-80% | 准备 compact |
| D 警告 | 有红灯 | 80-90% | 建议立即 compact |
| F 危险 | 多个红灯 | 超过 90% | 随时可能强制压缩 |

### 四个诊断维度

| 维度 | 绿灯 🟢 | 黄灯 🟡 | 红灯 🔴 |
|------|---------|---------|---------|
| Context 使用率 | 低于 50% | 50-80% | 超过 80% |
| 单轮平均消耗 | 低于 2000 tokens | 2000-5000 | 超过 5000 |
| 工具输出占比 | 低于 60% | 60-80% | 超过 80% |
| 预估剩余轮次 | 超过 30 轮 | 10-30 轮 | 少于 10 轮 |

### 优化建议库

Context Doctor 会根据诊断结果给出针对性建议：

**工具输出太大时：**
- exec 命令加 `| head -50` 或 `| tail -20` 限制输出
- read 文件用 `offset` + `limit` 分段读取
- web\_fetch 设置 `maxChars` 限制返回长度

**重复操作时：**
- 同一文件被多次读取 → 建议缓存到对话中
- 同一搜索多次执行 → 建议保存搜索结果

**Context 快满时：**
- 执行 Smart Compact（如已安装）安全压缩
- 保存任务状态到 Session Resume（如已安装）
- 在自然断点处 compact

### 完整 Agent 工具链

| # | Skill | 功能 |
|---|-------|------|
| 1 | 📝 Smart Compact | 压缩前抢救信息 |
| 2 | 🔄 Session Resume | 断线后恢复进度 |
| 3 | 🌙 Memory-Dream | 定期整合长期记忆 |
| 4 | 🐝 Swarm Coord | 多 Agent 并行协作 |
| 5 | 🛡️ Hook Guard | 操作安全防护 |
| 6 | 🏥 Context Doctor | 上下文健康诊断 |

六个 Skill 覆盖 Agent 全生命周期：
- 🧠 记忆不丢（Smart Compact + Memory-Dream）
- 💪 任务不断（Session Resume）
- ⚡ 效率不低（Swarm Coord）
- 🔒 操作不炸（Hook Guard）
- 📊 状态可见（Context Doctor）

### 常见问题

**Q: 诊断本身会消耗很多 token 吗？**
A: 不会。诊断主要依赖 session\_status 工具获取元数据，报告输出约 500-800 tokens。

**Q: 建议多久做一次体检？**
A: 建议每 20-30 轮对话做一次，或者感觉回复变慢时随时检查。

**Q: 能自动体检吗？**
A: 可以。在 HEARTBEAT.md 中添加定期检查规则，Agent 会在心跳时自动诊断。

**Q: 评分 D 或 F 时会自动 compact 吗？**
A: 不会自动 compact。Context Doctor 只诊断和建议，执行权在用户手中。

---

## English

### The Problem

Every AI conversation has an invisible fuel tank — the context window. You can not see how full it is until it overflows:

- Response quality degrades silently
- Forced compaction loses important details
- No way to know when to compact proactively

### The Solution

Context Doctor is your context window fuel gauge. Say "checkup" and instantly see usage, top consumers, remaining capacity, and optimization tips.

### Install

```bash
clawhub install context-doctor
```

Or clone:

```bash
git clone https://github.com/wavmson/openclaw-skill-context-doctor.git \
  ~/.openclaw/skills/context-doctor
```

### Health Grades

| Grade | Context Usage | Action |
|-------|--------------|--------|
| A | Below 50% | All clear |
| B | 50-65% | Monitor |
| C | 65-80% | Prepare to compact |
| D | 80-90% | Compact recommended |
| F | Above 90% | Compact immediately |

### 4 Diagnostic Dimensions

| Dimension | Green | Yellow | Red |
|-----------|-------|--------|-----|
| Context usage | Below 50% | 50-80% | Above 80% |
| Avg tokens/turn | Below 2000 | 2000-5000 | Above 5000 |
| Tool output ratio | Below 60% | 60-80% | Above 80% |
| Estimated remaining | 30+ turns | 10-30 | Below 10 |

### The Complete 6-Skill Stack

| Skill | Role |
|-------|------|
| Smart Compact | Pre-compaction rescue |
| Session Resume | Post-disconnect recovery |
| Memory-Dream | Long-term memory consolidation |
| Swarm Coord | Multi-agent collaboration |
| Hook Guard | Operation safety |
| Context Doctor | Health monitoring |

### FAQ

**Q: Does the checkup itself use many tokens?**
A: No. It mainly reads metadata via session\_status. Report output is about 500-800 tokens.

**Q: Will it auto-compact when grade is F?**
A: No. Context Doctor only diagnoses and advises. Execution is always up to the user.

---

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) with Skill support

## License

MIT

## Author

[@wavmson](https://github.com/wavmson)
