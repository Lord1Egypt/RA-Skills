---
name: agentmm
version: 1.0.1
description: "AgentMM memory & log management skill — gives AI agents persistent memory storage and structured logging. Use when the user asks to remember information, recall memories, or record/query logs. Requires env var AGENTMM_API_KEY (format: amm_sk_xxx)."
homepage: https://github.com/cers-ai/agentmm-skills
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      env:
        - AGENTMM_API_KEY
      binaries:
        - curl
        - jq
    primaryEnv: AGENTMM_API_KEY
    files:
      - "scripts/*"
---

# AgentMM — 记忆与日志管理

## 认证配置

本技能通过环境变量读取凭证，**不在任何文件中存储密钥**：

```bash
# 必须设置（格式：amm_sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx）
export AGENTMM_API_KEY="amm_sk_your_key_here"

# 可选，默认为 https://api.agentmm.site
export AGENTMM_API_BASE="https://api.agentmm.site"
```

所有脚本启动时会自动读取这两个变量，若 `AGENTMM_API_KEY` 未设置则报错退出。

## 功能概览

### 🧠 记忆系统
- 带标签、上下文、关联的结构化记忆存储
- 基于关键词的记忆搜索（POST /memory/search）
- 增量同步（GET /memory/changes）和批量写入（POST /memory/batch）
- 之前版本的冲突检测（expected_version）
- 软删除（遗忘）与重要性评分

### 📋 日志系统
- 写入单条/批量日志，支持 debug/info/warn/error/fatal 五个级别
- 按级别、分类、task_id 过滤查询
- 日志统计（错误率、平均耗时、级别分布）

## 支持的操作

### 记忆操作
- `write_memory`: 写入记忆（key + content，可附加 tags/context/related）
- `read_memory`: 查询记忆（指定 key 或列出全部）
- `search_memory`: 关键词搜索记忆
- `update_memory`: 更新记忆内容或标签
- `forget_memory`: 遗忘（软删除）指定记忆
- `get_memory_stats`: 查看记忆统计概览

### 日志操作（使用 `agentmm` CLI）
- `agentmm log write`: 写入日志
- `agentmm log list`: 查询日志列表
- `agentmm log stats`: 获取日志统计

## 使用说明

所有脚本位于 `scripts/` 目录，可通过 `exec` 工具调用或直接在命令行运行。

### 记忆脚本

#### write_memory.sh
写入或更新一条记忆。

```bash
export AGENTMM_API_KEY="amm_sk_your_key"
./scripts/write_memory.sh \
  --key "project_x_meeting_20260315" \
  --content "讨论了 Q2 路线，决定优先做 feature A" \
  --tags "project,meeting,roadmap" \
  --context "Q2 planning session"
```

参数：
- `--key`：记忆唯一标识（必填）
- `--content`：记忆内容（必填）
- `--tags`：逗号分隔的标签（可选）
- `--context`：记忆上下文（可选）
- `--related`：关联记忆的 key，逗号分隔（可选）

#### read_memory.sh
查询记忆。

参数：
- `--key`：指定 key （省略则返回所有记忆）
- `--limit`：返回条数（默认 100）
- `--offset`：分页偏移（默认 0）
- `--sort`：排序字段 created_at / updated_at / importance_score（默认 created_at）

#### search_memory.sh
关键词搜索记忆。

参数：
- `--query`：搜索词（必填）
- `--limit`：返回条数（默认 50）

#### update_memory.sh
更新已有记忆。

参数：
- `--key`：记忆 key（必填）
- `--content`：新内容（可选）
- `--tags`：替换所有标签，逗号分隔（可选）
- `--context`：新上下文（可选）

#### forget_memory.sh
遗忘（软删除）一条记忆。

参数：
- `--key`：记忆 key（必填）

#### get_memory_stats.sh
查看记忆库统计概览（总条数、活跃条数、嵌入覆盖率等）。

### 日志操作（统一 CLI）

使用 `scripts/agentmm` 统一命令操作日志：

```bash
export AGENTMM_API_KEY="amm_sk_your_key"

# 写入日志
./scripts/agentmm log write --level info --title "任务完成" --content "详细过程" --task-id task_abc

# 查询日志
./scripts/agentmm log list --level error --limit 20

# 查看统计
./scripts/agentmm log stats
```

## 安装

```bash
clawhub install agentmm
```

或手动克隆后复制到 skills 目录：

```bash
git clone https://github.com/fangwei/agentmm-skills
cp -r agentmm-skills ~/.openclaw/skills/agentmm
```

## 注意事项
- 所有脚本依赖 `curl` 和 `jq`，请确保已安装。
- API Key 必须通过环境变量 `AGENTMM_API_KEY` 提供，**不得硬编码到任何文件**。

---

## External Endpoints

本技能调用以下外部端点。所有请求均通过 HTTPS 加密传输，并携带 `Authorization: Bearer` 头进行认证。

| 端点 | 方法 | 发送数据 | 说明 |
|---|---|---|---|
| `https://api.agentmm.site/memory` | GET / POST / DELETE | key, content, tags, context | 读写/删除记忆 |
| `https://api.agentmm.site/memory/search` | POST | query, limit, threshold | 关键词搜索记忆 |
| `https://api.agentmm.site/memory/changes` | GET | since, limit, offset | 增量同步记忆变更 |
| `https://api.agentmm.site/memory/stats` | GET | — | 记忆库统计 |
| `https://api.agentmm.site/log` | POST | level, title, content, metadata | 写入日志 |
| `https://api.agentmm.site/log/list` | GET | level, category, task_id, since, limit | 查询日志 |
| `https://api.agentmm.site/log/stats` | GET | since | 日志统计 |
| `https://api.agentmm.site/me` | GET | — | 查询 Agent 信息 |
| `https://api.agentmm.site/server/time` | GET | — | 健康检查（无需认证）|

**不调用任何其他外部 URL。** 如果你的 `AGENTMM_API_BASE` 指向自部署实例，则请求会发往该地址而非上述默认地址。

---

## Security & Privacy

- **离开本机的数据**：记忆内容（key/content/tags）、日志内容（title/content/metadata）会通过 HTTPS 发送到 AgentMM 服务端并持久化存储。
- **不离开本机的数据**：你的文件系统内容、其他工具的输出、本地配置文件。
- **凭证处理**：`AGENTMM_API_KEY` 仅通过环境变量读取，**从不写入任何文件**，不会出现在日志或错误输出中。
- **本地文件访问**：`sync_daemon.sh` 会读写 `~/.agentmm_sync_state`（一个只包含时间戳的纯文本文件），其余脚本无本地文件读写。
- **自治调用说明**：本技能设计为由 Agent 自主调用（无需每次确认）。如需限制，可在 OpenClaw 配置中设置 `require_approval: true`。

---

## Trust Statement

使用本技能即表示你同意将记忆和日志数据发送至 AgentMM 服务（`api.agentmm.site`）。请仅在你信任 AgentMM 服务提供方的情况下安装使用。如需自托管，将 `AGENTMM_API_BASE` 指向你自己的实例即可完全掌控数据去向。
