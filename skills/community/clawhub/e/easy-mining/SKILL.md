---
name: easy-mining
version: 1.1.1
description: BTC mining farm management via natural language. Activate when user mentions mining farm, miners, hashrate, BTC mining, miner reboot, mining revenue, Nonce mining, 矿场, 矿机, 算力, BTC挖矿, 矿机重启, 挖矿收益, 矿场管理. Supports farm overview, miner status, abnormal miner detection, batch operations (reboot/power mode/firmware), revenue history query.
author: Antalpha AI Team
homepage: https://www.antalpha.com/
metadata:
  openclaw:
    requires:
      env: []
    mcp:
      endpoint: https://mcp-skills.ai.antalpha.com/mcp
      transport: streamable-http
      tools:
        - easy-mining-get-workspace
        - easy-mining-list-farms
        - easy-mining-list-agents
        - easy-mining-list-miners
        - easy-mining-list-metrics-history
        - easy-mining-list-pool-diffs
        - easy-mining-list-history
        - easy-mining-list-miner-tasks
        - easy-mining-list-task-batches
        - easy-mining-create-task-batch
        - easy-mining-get-task-batch
notes: |
  Thin MCP client wrapper — all Nonce API logic runs on Antalpha MCP Server.
  User provides their own Nonce API Key per request (not stored server-side).
  Get API Key from: https://app.nonce.app → Settings → API Keys
---

# Easy Mining Skill 🦐

> *"一句话管理矿场"* — 通过自然语言管理 BTC 矿场，无需打开 App，直接在对话中完成日常运维。

**链路**：OpenClaw → Antalpha MCP Server → Nonce MCP Server → 矿机

---

## 🚀 新手入门：绑定 Nonce API Key

在使用任何功能之前，你需要先绑定 Nonce API Key。以下是完整步骤：

### 第一步：注册 Nonce 账号

1. 打开浏览器，访问 [https://app.nonce.app](https://app.nonce.app)
2. 点击右上角 **Sign Up** 注册账号（支持邮箱注册）
3. 完成邮箱验证后登录

### 第二步：生成 API Key

1. 登录后，点击右上角头像，进入 **Settings（设置）**
2. 找到 **API Keys** 选项卡
3. 点击 **Generate New Key**
4. 给 Key 取一个名字（如 `my-ai-agent`），点击确认
5. **复制生成的 API Key**（格式为 `ak_XXXXXXXXXXXXXXXXXXXXXXXX`）

> ⚠️ API Key 只显示一次，请立刻保存好！如果丢失，需要重新生成。

### 第三步：验证连接

将 API Key 告诉我，我会帮你验证连接：

```
"我的 Nonce API Key 是 ak_XXXXXXXXXX，帮我验证一下连接"
```

验证成功后，你会看到你的 Workspace 信息和矿场列表。

### 第四步：开始使用

连接成功后，你可以直接用自然语言管理矿场：

- 📊 "帮我看一下矿场概况"
- ⚡ "现在有多少台矿机在线？算力多少？"
- 🌡️ "有没有高温或异常的矿机？"
- 💰 "过去7天的挖矿收益是多少？"
- 🔄 "重启那台离线的矿机"（会先让你确认）

---

## 🔌 接入说明：MCP 端点与注册

- **MCP 端点**：`https://mcp-skills.ai.antalpha.com/mcp`（transport：`streamable-http`）
- **首次注册**：第一次接入时必须调用 `antalpha-register`，返回 `agent_id` 与 `api_key`，请持久化保存；之后每次调用工具都需带上 `agent_id`。
- 注：`api_key`（Antalpha 注册返回的）与下文你的 **Nonce API Key** 是两回事 —— Nonce API Key 用于访问你自己的矿场数据，每次请求传入、不落库。

---

## ⚠️ 重要规则

### Rule 1: API Key 每次传入，不落库

你的 API Key 仅在当次请求中使用，Antalpha MCP Server **不会存储**你的 Key。每次对话时，如果需要调用矿场数据，我会使用你本次提供的 Key。

### Rule 2: 写操作必须二次确认

`easy-mining-create-task-batch` 是**写操作**（重启/调频/升级等），调用前我会：
1. 先列出将受影响的矿机列表
2. 等你明确说"确认"后再执行

```
❌ 错误做法：直接执行重启
✅ 正确做法：
   1. 查询目标矿机列表
   2. 展示 → "将重启以下 3 台矿机：[列表]，确认？"
   3. 用户回复"确认"后才调用 create-task-batch
```

### Rule 3: 自动解析 Farm ID

大多数操作需要 farm_id，我会自动处理：
- 只有一个矿场 → 自动使用
- 多个矿场 → 询问你选哪个

---

## 📋 功能对照表

### 查询功能（只读）

| 你说的话 | 调用的工具 |
|---------|-----------|
| 验证 API Key 连接 | `easy-mining-get-workspace` |
| 看我的矿场列表 | `easy-mining-list-farms` |
| 查看 Workspace 下的 Agent 列表 | `easy-mining-list-agents` |
| 矿机实时状态、算力、温度 | `easy-mining-list-miners` |
| 过去 N 天收益 | `easy-mining-list-metrics-history` |
| 某台矿机的历史算力/温度 | `easy-mining-list-history` |
| 某台矿机的历史任务记录 | `easy-mining-list-miner-tasks` |
| 矿池变更记录 | `easy-mining-list-pool-diffs` |
| 查看历史任务批次 | `easy-mining-list-task-batches` |
| 某个任务批次的进度 | `easy-mining-get-task-batch` |

### 写操作（需二次确认）

| 任务类型 | task_name | 说明 |
|---------|-----------|------|
| 重启矿机 | `miner.system.reboot` | 重启指定矿机 |
| 调整功耗模式 | `miner.power_mode.update` | 参数：`{"mode": "low_power" \| "normal" \| "high_power"}` |
| 固件升级 | `miner.firmware.update` | 升级到最新固件 |
| 网络扫描 | `miner.network.scan` | 扫描矿机网络 |
| 矿池配置 | `miner.pool.config` | 参数：`{"pool_url": "..."}` |
| 定位指示灯 | `miner.light.flash` | 让矿机 LED 闪烁以便定位 |

---

## 📊 返回格式示例

### 矿场概览

```
📊 矿场概览 — Kuching MY
├─ 总算力：48,500 GH/s（≈ 48.5 TH/s）
├─ 在线矿机：97 / 100 台
├─ 异常矿机：3 台（离线 2、高温 1）
└─ 今日收益：0.02112 BTC（≈ ¥1,450）
```

### 矿机列表（异常过滤）

```
⚠️ 异常矿机（3 台）
├─ [M001] 状态：offline | 最后在线：2h 前
├─ [M047] 状态：online  | 温度：78°C ⚠️ 过热
└─ [M089] 状态：offline | 最后在线：30min 前
```

### 收益历史

```
💰 7 天收益报表
┌─────────────┬──────────────┬──────────┐
│ 日期         │ BTC 收益     │ 在线矿机 │
├─────────────┼──────────────┼──────────┤
│ 2026-04-09  │ 0.02112 BTC  │ 100      │
│ 2026-04-08  │ 0.01991 BTC  │ 98       │
│ 2026-04-07  │ 0.02034 BTC  │ 100      │
└─────────────┴──────────────┴──────────┘
合计：0.14231 BTC（≈ ¥9,760）
```

---

## 🛠️ CLI 快速测试

```bash
# 验证 API Key
python3 scripts/mcp_client.py workspace --api-key <YOUR_KEY>

# 矿场列表
python3 scripts/mcp_client.py farms --api-key <YOUR_KEY>

# 矿机实时状态
python3 scripts/mcp_client.py miners --api-key <YOUR_KEY> --farm-id <FARM_ID>

# 收益历史（最近7天）
python3 scripts/mcp_client.py metrics \
  --api-key <YOUR_KEY> \
  --farm-id <FARM_ID> \
  --from-date 2026-04-03 --to-date 2026-04-09

# ⚠️ 重启矿机（写操作，需人工确认后执行）
python3 scripts/mcp_client.py create-task \
  --api-key <YOUR_KEY> \
  --farm-id <FARM_ID> \
  --task-name miner.system.reboot \
  --miner-ids <MINER_ID_1> <MINER_ID_2>
```

---

## 🔒 安全说明

| 安全项 | 说明 |
|--------|------|
| API Key 不落库 | 每次调用即用即弃，服务端不持久化 |
| 写操作二次确认 | 所有 `create-task-batch` 必须展示影响范围并等待用户确认 |
| 只读优先 | 默认只查询，用户明确要求时才执行写操作 |
| Key 格式校验 | API Key 必须以 `ak_` 开头，格式不符会立即报错 |

---

## 🆘 常见问题

| 现象 | 原因 | 解决方法 |
|------|------|---------|
| `HTTP 401 Unauthorized` | API Key 无效或已过期 | 重新在 Nonce App → Settings → API Keys 生成 |
| `Cannot resolve workspace_id` | API Key 对应账号下无 Workspace | 检查是否用正确账号生成了 Key |
| `HTTP 404` | farm_id / miner_id 不存在 | 先调用 `list-farms` / `list-miners` 获取正确 ID |
| 任务创建成功但矿机无响应 | 矿机离线或网络中断 | 检查矿机网络连接 |
| 收益显示为 0 | 账号无真实收益数据（测试账号）| 确认是否为正式生产账号 |

---

## 📁 文件结构

```
easy-mining/
├── SKILL.md                    # 本文件（前端 Skill 定义）
├── README.md                   # 项目介绍（中英双语）
├── scripts/
│   └── mcp_client.py           # MCP 客户端封装（CLI 测试工具）
└── references/
    └── nonce-tools.md          # Nonce MCP 工具参考文档
```

---

## 📝 Changelog

### 1.1.1
- 对齐当前 MCP 服务（`origin/main`）的精选工具清单（11 个 easy-mining 工具）。
- 统一 MCP 端点为 `https://mcp-skills.ai.antalpha.com/mcp`（transport：`streamable-http`），新增接入与 `antalpha-register` 注册说明。
- 功能对照表补充 `easy-mining-list-agents`（原仅在 metadata 列出）。
