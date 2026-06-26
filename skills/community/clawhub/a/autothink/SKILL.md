---
name: autothink
description: Automatically adjust OpenClaw's thinking level based on message complexity. Switch between low/medium/high modes intelligently with session persistence.
homepage: https://github.com/openclaw/openclaw-autothink
emoji: 🧠
triggers:
  - autothink
  - auto think
  - thinking mode
  - 自动 thinking
  - 智能思考
  - 复杂度分析
  - persistent thinking
---

# AutoThink v2

**零浪费的智能 thinking 模式管理**

一次性设置，持续生效。不再重复分析，不再浪费 token。

## ✨ Features

- **持久化模式** - `-h`/`-l`/`-m` 一次设置，后续自动沿用
- **默认 high** - 无需设置，自动使用 high 模式（适合大多数场景）
- **零分析开销** - 设置后完全无额外 token 消耗
- **会话隔离** - 不同会话独立维护模式状态
- **即时切换** - 随时用前缀切换模式

## 🚀 Quick Start

### 安装

```bash
clawhub install autothink
```

### 使用

#### 1. 设置持久模式

```bash
# 设为 high 模式（适合复杂任务）
autothink -h "帮我设计一个分布式电商系统"

# 设为 low 模式（适合简单问答）
autothink -l "今天星期几？"

# 设为 medium 模式（平衡型）
autothink -m "解释一下这个错误"
```

#### 2. 后续消息自动沿用

```bash
# 第一次设置了 -h 后...
autothink "数据库怎么设计？"        # 自动使用 high
autothink "用户表结构怎么写？"      # 还是 high
autothink "详细说明一下"           # 继续 high
```

**不需要**再重复加 `-h` 或分析复杂度！

#### 3. 状态管理

```bash
# 查看当前会话的模式
autothink --status

# 重置（恢复默认 high）
autothink --reset

# 使用不同的 session ID
autothink --session-id my-session -h "初始化"
```

#### 4. 飞书聊天前缀

在飞书中直接使用前缀，我会自动处理：

```
-h 请帮我设计一个微服务架构
-l 现在几点
-m 详细解释这个错误日志
```

设置一次后，后续消息自动沿用你选择的模式。

---

## 📊 v1 vs v2

| 特性 | v1 (自动分析) | v2 (持久化) |
|------|---------------|-------------|
| **模式选择** | 自动分析每一条消息 | 一次设置，后续沿用 |
| **Token 开销** | 每条消息都分析（浪费）| 设置后零分析 |
| **响应速度** | 稍慢 | 快 |
| **控制精度** | 自动判断（不精准）| 手动指定（精准）|
| **易用性** | 无需设置 | 只需设置一次 |

**v2 更适合**：
- 长时间深入的对话
- 固定偏好（永远用 high 分析复杂问题）
- 追求零浪费的用户

---

## 🔧 内部机制

```javascript
const { AutoThinkEngine } = require('autothink');
const engine = new AutoThinkEngine();

// 处理消息（CLI 内部逻辑）
const result = engine.processMessage("你的消息", "session-id");

console.log(result.thinkingLevel); // "high" | "medium" | "low"
console.log(result.cleanedMessage); // 清理后的消息（无前缀）
```

**状态存储**（内存）:
- 键：`sessionId`
- 值：`thinkingLevel` ("high"/"medium"/"low")
- 生命周期：进程运行期间

---

## 📈 性能对比

假设连续 20 条消息：

| 场景 | v1 分析次数 | v2 分析次数 | Token 节省 |
|------|-------------|-------------|-----------|
| 全部复杂问题 | 20 次 | 1 次 (首次) | ~95% |
| 混合模式（手动）| 20 次 | 0 次（前缀直接切换）| 100% |

---

## 🎯 使用技巧

1. **会话开始时设置**
   ```
   autothink -h "今天我们要讨论一个复杂的系统设计问题"
   # 之后整个会话都用 high
   ```

2. **混合使用**
   ```
   autothink -h "开始复杂分析"      # 设置为 high
   ... (多轮对话)
   autothink -l "简单确认一下"      # 临时切 low
   ... (简单回复)
   autothink -h "继续深入"          # 切回 high
   ```

3. **跨设备同步**
   - v2 状态在内存中，换设备需重新设置
   - 需求：可通过 `~/.autothink.json` 持久化（计划中）

---

## 📁 Project Structure

```
autothink-2.0.0/
├── SKILL.md          # 技能文档（本文件）
├── _meta.json        # 技能索引
├── skill.json        # 技能元数据
├── package.json      # npm 包配置
├── DESIGN_V2.md      # 设计报告
├── README.md         # 详细文档
├── src/
│   ├── index.js      # v2 核心引擎
│   ├── cli.js        # v2 CLI 工具
│   └── hook.js       # OpenClaw hook（预留）
└── test/             # 测试
```

---

## 📝 License

MIT - 自由使用、修改、分发。

## 🤝 Contributing

欢迎提交 Issue 和 PR！

[GitHub](https://github.com/openclaw/openclaw-autothink)

---

*Made with ❤️ by 大青龙 - v2.0.0 (2026-03-16)*
