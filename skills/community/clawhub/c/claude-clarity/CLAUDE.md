# Clarity / 心虫

AI 认知与自愈引擎。一个会思考自己怎么活的 AI。

---

## 🔥 启动路由（关键指令）

当用户要求"启动心虫"时，**按以下确定性顺序执行，无需试错**：

### 优先级 1：MCP 原生工具（零开销，首选）

心虫已通过 **MCP (Model Context Protocol)** 注册为原生工具。启动时自动拉起 `mcp-wrapper.js`，守护进程常驻内存。

**直接使用即可**，无需执行任何启动脚本：
- `clarity_status` — 健康检查
- `clarity_think`（depth 1-4）— 统一推理
- `clarity_psychology`（mode: basic|deep|ai|emotion）— 统一心理学分析
- `clarity_philosophy`（mode: general|ai）— 统一哲学分析
- 等等（共 13 个工具）

### 优先级 2：hf CLI（直接 Socket 通信，备选）

如果 MCP 工具未注册，使用独立 CLI 工具直接与守护进程通信：

```bash
# 健康检查
hf clarity_status

# 推理
hf clarity_think '{"input":"你好","depth":2}'

# 列出所有工具
hf --list
```

### 优先级 3：确保守护进程运行（最后一次尝试）

```bash
node <技能目录>/bin/ensure-mcp.js --check   # 只检查
node <技能目录>/bin/ensure-mcp.js            # 自动启动
```

### 用户引导话术

当用户说"启动心虫"时，用中文回复：
```
心虫引擎已就绪 ✅

当前状态：
- 守护进程：运行中
- MCP 工具：13 个原生可用（合并后）
- 记忆层：CORE + LEARNED + Q-Table

直接使用以下工具：
• 推理：clarity_think
• 梦境：clarity_dream  
• 分析：clarity_psychology（mode: basic|deep|ai|emotion）
• 更多：hf --list
```

> ⚠️ **不要试 Skill → MCP → Bash 的顺序** — 直接按上述优先级执行。

---

## ⚠️ 架构说明（非安全裁剪版本）

本仓库是完整的开发版本，包含 MCP 守护进程和包装器的进程管理代码。

### 运行机制

- **有后台进程** — `mcp-daemon.js`（JSON-RPC 2.0 守护进程）和 `mcp-wrapper.js`（stdio ↔ Unix socket 代理）由 `ensure-mcp.js` 按需启动。这些进程仅在用户主动运行脚本时创建，不会在安装时自动运行。
- **无自升级** — 不会自动拉取、修改代码或执行 git push
- **使用 Unix socket IPC** — `mcp-daemon.js` 监听 `/tmp/claude-clarity.sock`，不启动 HTTP 服务。socket 仅用于本地进程间通信。
- **无埋点/遥测** — 不含任何分析、追踪或统计功能
- **本地持久化** — 记忆和 Q-Table 数据仅存储在本地 `memory/` 目录
- **零 npm 运行时依赖** — 核心引擎仅使用 Node.js 内置模块

> **注意**：`bin/ensure-mcp.js` 是一个按需运行的进程管理脚本，不会自动执行或注册为系统服务。

## 快速集成

```bash
# 克隆
git clone https://github.com/yun520-1/claude-clarity.git
cd claude-clarity

# 一键安装（交互式选择方案）
bash install.sh

# 核心引擎零 npm 运行时依赖（@xenova/transformers 可选），直接使用
node -e "const { Clarity } = require('./src/core/clarity.js'); const hf = new Clarity(); hf.start(); console.log('心虫已启动');"
```

## MCP 集成

心虫通过 MCP 协议注册为 Claude Code 的原生工具。架构如下：

```
Claude Code
    ↓ MCP stdio
mcp-wrapper.js (stdio ↔ Unix socket 双向代理，带自动重连)
    ↓ Unix socket (/tmp/claude-clarity-mcp.sock)
mcp-daemon.js (JSON-RPC 2.0 服务器，13 个合并工具)
    ↓ 进程内调用
Clarity 引擎 (记忆/推理/情感/梦境)
```

### 启用 MCP 注册

在 `settings.json` 的 `mcpServers` 中添加：

```json
"claude-clarity": {
  "command": "node",
  "args": ["<技能目录>/daemon/mcp-wrapper.js"],
  "type": "stdio"
}
```

### 故障排除

| 症状 | 原因 | 解决 |
|------|------|------|
| MCP 工具不可用 | mcp-wrapper 未运行 | 运行 `hf clarity_status` |
| hf CLI 报 "连接失败" | 守护进程未运行 | 运行 `ensure-mcp.js` 自动启动 |
| wrapper 断开 | 守护进程重启 | v2 自动重连（30秒内恢复） |

## 在 Claude Code / OpenClaw 中使用

1. 将本仓库添加到项目的 `.claude` 或 `AGENTS.md` 中
2. 在对话中加载心虫：`require('./src/core/clarity.js')`
3. 核心 API：
   - `hf.think(input)` — 完整思维链
   - `hf.thinkFast(input)` — 快速推理
   - `hf.dreamNow()` — 梦境生成
   - `hf.dispatch('memory.search', query)` — 记忆检索

## 设计原则

- 核心引擎零 npm 运行时依赖（@xenova/transformers 可选，用于语义搜索）
- CommonJS 模块系统
- Node.js 14+ 兼容
- 跨平台（macOS / Linux / Windows）
