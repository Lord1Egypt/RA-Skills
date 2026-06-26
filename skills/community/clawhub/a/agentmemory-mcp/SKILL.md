---
name: agentmemory
description: |
  Persistent cross-session memory for OpenClaw via agentmemory.
  
  Use when:
  - User asks to install/configure agentmemory for OpenClaw
  - Agent needs to remember project context, decisions, or workflows across sessions
  - Setting up long-term memory for OpenClaw (MCP mode)
  - Integrating agentmemory with existing MEMORY.md system
  - Troubleshooting agentmemory connection issues
  - Upgrading or removing agentmemory

  ───────────────────────────────
  
  基于 agentmemory 的跨会话持久化记忆系统，适用于 OpenClaw。
  
  适用场景：
  - 用户要求安装/配置 agentmemory
  - Agent 需要记住项目背景、决策或工作流程
  - 为 OpenClaw 设置长期记忆（MCP 模式）
  - 与现有 MEMORY.md 系统集成
  - 排查 agentmemory 连接问题
  - 升级或移除 agentmemory
---

# agentmemory Integration for OpenClaw

> **Status**: ✅ Verified working with OpenClaw v2026.5.4
> **Version**: agentmemory npm v0.9.11 · iii-engine Docker v0.11.6
> **MCP Tools**: 107 REST + 51 MCP tools available

Persistent memory server giving OpenClaw agents cross-session semantic recall via BM25+Vector+Graph RRF hybrid search.

## Architecture

```
OpenClaw Agent ←→ Gateway (MCP) ←→ agentmemory MCP Server (localhost:3111)
                                              ↓
                                         SQLite/KV Store
                                              ↓
                                      Viewer (localhost:3113)
```

## Quick Start (MCP Mode — 5 minutes)

### Step 1: Install and start memory server

```bash
# Server runs on localhost:3111, viewer at localhost:3113
npx @agentmemory/agentmemory
```

### Step 2: Configure OpenClaw MCP

Add to `~/.openclaw/openclaw.json` under `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "agentmemory": {
        "command": "npx",
        "args": ["-y", "@agentmemory/mcp"]
      }
    }
  }
}
```

### Step 3: Restart Gateway

```bash
openclaw gateway restart
```

### Step 4: Verify

```bash
curl http://localhost:3111/agentmemory/health
# → {"status":"healthy","version":"0.9.11"}

# View memory dashboard
open http://localhost:3113
```

---

## systemd Service (Production)

For auto-start and reliable background operation:

### Install service

```bash
mkdir -p ~/.config/systemd/user
cp ./scripts/agentmemory.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable agentmemory
systemctl --user start agentmemory

# Enable linger (boot without login)
loginctl enable-linger $(whoami)
```

### Service commands

```bash
systemctl --user status agentmemory   # Check status
journalctl --user -u agentmemory -f   # View logs
systemctl --user restart agentmemory  # Restart
```

### Service environment variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `NODE_ENV` | `production` | Production mode |
| `AGENTMEMORY_PORT` | `3111` | MCP API port |
| `AGENTMEMORY_VIEWER_PORT` | `3113` | Dashboard port |
| `AGENTMEMORY_III_VERSION` | `latest` | iii-engine Docker image tag |

> **Important**: `AGENTMEMORY_III_VERSION=latest` overrides the npm CLI's hardcoded `IIPINNED_VERSION=0.11.2`, ensuring the latest stable iii-engine (v0.11.6) is used instead of the older pinned version.

### Docker socket

The service uses the system Docker socket at `/var/run/docker.sock` (owned by `root:docker`). Do NOT set `DOCKER_HOST` — the default socket path is correct.

---

## Search Mode: BM25 vs Vector

agentmemory supports two search modes:

| Mode | Description | Use when |
|------|-------------|----------|
| **BM25-only** | Keyword-based full-text search | Default, no API key needed |
| **Hybrid (BM25+Vector)** | BM25 + semantic embeddings | Need semantic/synonym search |

### Default: BM25-only (no configuration needed)

BM25 covers 90%+ of searches for known terms (skill names, config keys, decision labels). Current status after setup:

```
[agentmemory] Embedding provider: none (BM25-only mode)
```

### Want vector search? Choose your embedding provider

When you're ready to upgrade, choose from these free-tier options:

| Provider | Free tier | Chinese | Setup |
|----------|-----------|---------|-------|
| **VoyageAI** | 50k tokens/month | ✅ Good | `VOYAGE_API_KEY` + `EMBEDDING_PROVIDER=voyageai` |
| **Cohere** | 50k tokens/month | ✅ Good | `COHERE_API_KEY` + `EMBEDDING_PROVIDER=cohere` |
| **阿里云百炼 Qwen/E5** | ~$0.1/1M tokens | ✅ Excellent | `OPENAI_API_KEY` + `OPENAI_BASE_URL` + `EMBEDDING_PROVIDER=openai` |

**When user wants vector search**, ask them to choose one of the three, then configure accordingly:

#### Option A: VoyageAI
```ini
Environment=EMBEDDING_PROVIDER=voyageai
Environment=VOYAGE_API_KEY=your_voyage_key
```

#### Option B: Cohere
```ini
Environment=EMBEDDING_PROVIDER=cohere
Environment=COHERE_API_KEY=your_cohere_key
```

#### Option C: 阿里云百炼 (Bailian)
```ini
Environment=EMBEDDING_PROVIDER=openai
Environment=OPENAI_API_KEY=your_bailian_key
Environment=OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
Environment=OPENAI_EMBEDDING_MODEL=text-embedding-v4
Environment=OPENAI_EMBEDDING_DIMENSIONS=1024
```

After configuring, reload and restart:
```bash
systemctl --user daemon-reload
systemctl --user restart agentmemory
```

Verify embedding is active:
```bash
journalctl --user -u agentmemory -n 5 --no-pager | grep "Embedding provider"
# → [agentmemory] Embedding provider: openai (1024 dims)  ← example for Bailian
```

---

## Integration with MEMORY.md

agentmemory and MEMORY.md serve different purposes — they coexist:

| Layer | System | Purpose | Management |
|-------|--------|---------|------------|
| **Experience** | agentmemory | Manual save, semantic recall, cross-agent | `memory_save` (manual) |
| **Knowledge** | MEMORY.md | Curated decisions, preferences, rules | Manual |

### Coordination rules

- **Before major tasks**: Call `memory_recall` to retrieve relevant experiences
- **After important decisions**: Call `memory_save` with result
- **Curated knowledge**: Stays in MEMORY.md (survives compaction)
- **Session start**: Both systems loaded; no conflicts

### After installation: migrate MEMORY.md (important!)

After completing installation, migrate MEMORY.md content into agentmemory:

1. **Open the dashboard to view current state**
   ```bash
   open http://localhost:3113
   ```
   Initially empty — migration populates it with searchable data.

2. **Migrate MEMORY.md content**
   Use the CLI migrate command:
   ```bash
   agentmemory migrate --from-file ~/.openclaw/workspace/MEMORY.md --verbose
   ```

3. **Verify migration results**
   After migration, reopen http://localhost:3113 to confirm data is stored.

> Note: MEMORY.md stays intact — both systems coexist. agentmemory handles semantic search; MEMORY.md holds curated knowledge.

---

## Verification

Run the verification script:
```bash
bash ./scripts/verify.sh
```

Expected output:
- ✅ Memory server on port 3111
- ✅ Health endpoint responding
- ✅ Viewer available on port 3113
- ✅ OpenClaw MCP configured
- ✅ systemd service active

### Manual health check

```bash
curl http://127.0.0.1:3111/agentmemory/health | python3 -m json.tool
```

Healthy response shows: `{"status":"healthy","uptimeSeconds":...,"workers":[...]}`

---

## MCP Tools (Key ones for OpenClaw)

| Tool | Purpose |
|------|---------|
| `memory_recall` | Semantic search across all memories |
| `memory_save` | Store new memories with type/tags |
| `memory_smart_search` | Hybrid BM25+vector search |
| `memory_timeline` | View memories chronologically |
| `memory_profile` | Agent's memory usage stats |
| `memory_snapshot` | Full memory export as JSON |
| `memory_forget` | Delete specific memories |
| `memory_context` | Get context for current session |
| `memory_lesson_save` | Record lessons learned from errors |
| `memory_reflect` | Cluster knowledge graph for insights |

See `references/mcp-tools.md` for full list of 51 tools.

---

## Uninstall

### MCP mode removal

1. Remove from `openclaw.json` mcp.servers section
2. `openclaw gateway restart`

### Full removal

```bash
systemctl --user stop agentmemory
systemctl --user disable agentmemory
rm ~/.config/systemd/user/agentmemory.service
pkill -f "agentmemory"
```

---

## Troubleshooting

### "Connection refused on port 3111"
Memory server not running. Start it:
```bash
systemctl --user start agentmemory
# Or manually: npx @agentmemory/agentmemory
```

### "Config invalid" after editing openclaw.json
Ensure `mcp.servers` path (not `mcpServers`). Run:
```bash
openclaw status  # Should show "Config valid"
```

### View real-time logs
```bash
journalctl --user -u agentmemory -f --since "1 hour ago"
```

### iii-engine version mismatch
If `api::graph-stats` and other v0.11.6 functions are not registered:
```bash
# Check current iii-engine version
curl -s http://127.0.0.1:3111/agentmemory/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
for w in d['health']['workers']:
    print(w['name'], '→', w['version'])
"

# Ensure AGENTMEMORY_III_VERSION=latest is set in systemd service
systemctl --user status agentmemory
grep AGENTMEMORY_III_VERSION ~/.config/systemd/user/agentmemory.service
```

### WebSocket disconnected (1006)
This is typically a client-side event (browser tab switch, network glitch), not a Gateway failure. Check:
```bash
journalctl --user -u openclaw-gateway --since "5 minutes ago" | grep -E "connected|disconnected"
```
If Gateway shows `webchat connected` after the disconnect, the service is fine.

---

---

## 中文版 Chinese Version

### agentmemory × OpenClaw 集成

> **状态**: ✅ 已验证兼容 OpenClaw v2026.5.4
> **版本**: agentmemory npm v0.9.11 · iii-engine Docker v0.11.6
> **MCP 工具**: 107 个 REST + 51 个 MCP 工具

持久化记忆服务，为 OpenClaw Agent 提供跨会话语义召回能力，基于 BM25+向量+图谱混合搜索。

### 系统架构

```
OpenClaw Agent ←→ Gateway (MCP) ←→ agentmemory MCP 服务器 (localhost:3111)
                                              ↓
                                          SQLite/KV 存储
                                              ↓
                                        浏览器仪表板 (localhost:3113)
```

### 快速开始（MCP 模式 — 5 分钟）

**第一步：启动记忆服务器**

```bash
npx @agentmemory/agentmemory
# 服务器端口：3111（API）、3113（浏览器仪表板）
```

**第二步：配置 OpenClaw MCP**

在 `~/.openclaw/openclaw.json` 中加入：

```json
{
  "mcp": {
    "servers": {
      "agentmemory": {
        "command": "npx",
        "args": ["-y", "@agentmemory/mcp"]
      }
    }
  }
}
```

**第三步：重启 Gateway**

```bash
openclaw gateway restart
```

**第四步：验证**

```bash
curl http://localhost:3111/agentmemory/health
# → {"status":"healthy","version":"0.9.11"}

# 打开记忆仪表板
open http://localhost:3113
```

---

### 搜索模式：BM25 vs 向量

agentmemory 支持两种搜索模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **仅 BM25** | 基于关键词的全文搜索 | 默认，无需 API key |
| **混合搜索 (BM25+向量)** | BM25 + 语义 embeddings | 需要同义词/语义搜索时 |

### 默认：仅 BM25（无需配置）

BM25 对已知术语（技能名、配置键、决策标签）的搜索已覆盖 90%+ 需求。安装后的状态：

```
[agentmemory] Embedding provider: none (BM25-only mode)
```

### 需要向量搜索？从三个免费选项中选择

准备好后再升级，从以下免费额度选项中选择：

| 提供商 | 免费额度 | 中文支持 | 配置方式 |
|--------|----------|----------|----------|
| **VoyageAI** | 50k tokens/月 | ✅ 良好 | `VOYAGE_API_KEY` + `EMBEDDING_PROVIDER=voyageai` |
| **Cohere** | 50k tokens/月 | ✅ 良好 | `COHERE_API_KEY` + `EMBEDDING_PROVIDER=cohere` |
| **阿里云百炼 Qwen/E5** | ~$0.1/1M tokens | ✅ 优秀 | `OPENAI_API_KEY` + `OPENAI_BASE_URL` + `EMBEDDING_PROVIDER=openai` |

**当用户需要向量搜索时**，先让他们从三个选项中选择，然后再配置：

#### 选项 A: VoyageAI
```ini
Environment=EMBEDDING_PROVIDER=voyageai
Environment=VOYAGE_API_KEY=your_voyage_key
```

#### 选项 B: Cohere
```ini
Environment=EMBEDDING_PROVIDER=cohere
Environment=COHERE_API_KEY=your_cohere_key
```

#### 选项 C: 阿里云百炼 (Bailian)
```ini
Environment=EMBEDDING_PROVIDER=openai
Environment=OPENAI_API_KEY=your_bailian_key
Environment=OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
Environment=OPENAI_EMBEDDING_MODEL=text-embedding-v4
Environment=OPENAI_EMBEDDING_DIMENSIONS=1024
```

配置完成后，重载并重启服务：
```bash
systemctl --user daemon-reload
systemctl --user restart agentmemory
```

验证 embedding 已启用：
```bash
journalctl --user -u agentmemory -n 5 --no-pager | grep "Embedding provider"
# → [agentmemory] Embedding provider: openai (1024 dims)  ← Bailian 配置示例
```

---

### systemd 服务（生产环境推荐）

**安装服务：**

```bash
mkdir -p ~/.config/systemd/user
cp ./scripts/agentmemory.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable agentmemory
systemctl --user start agentmemory

# 启用 linger（开机免登录自动启动）
loginctl enable-linger $(whoami)
```

**服务环境变量：**

| 变量 | 值 | 说明 |
|------|-----|------|
| `NODE_ENV` | `production` | 生产模式 |
| `AGENTMEMORY_PORT` | `3111` | MCP API 端口 |
| `AGENTMEMORY_VIEWER_PORT` | `3113` | 仪表板端口 |
| `AGENTMEMORY_III_VERSION` | `latest` | iii-engine Docker 镜像标签 |

> **重要**：`AGENTMEMORY_III_VERSION=latest` 用于绕过 npm CLI 硬编码的 `IIPINNED_VERSION=0.11.2`，确保使用最新的稳定版 iii-engine（v0.11.6）。

**Docker socket**：服务使用系统 Docker socket `/var/run/docker.sock`（属于 `root:docker` 组）。不要设置 `DOCKER_HOST` 环境变量，默认 socket 路径已正确。

---

### 与 MEMORY.md 的协同

两个系统分工不同，共存互补：

| 层级 | 系统 | 用途 | 管理方式 |
|------|------|------|----------|
| **经验层** | agentmemory | 手动保存重要内容、语义召回、跨 Agent 共享 | `memory_save`（手动调用） |
| **知识层** | MEMORY.md | 精心整理的决策、偏好、规则 | 手工维护 |

**协调规则：**

- **任务开始前** → 调用 `memory_recall` 检索相关经验
- **重要决策后** → 调用 `memory_save` 保存结果
- **精选知识** → 留在 MEMORY.md（不受会话压缩影响）
- **会话启动时** → 两个系统同时加载，无冲突

### 首次安装后：迁移 MEMORY.md（重要！）

安装完成后，将 MEMORY.md 的核心内容迁移到 agentmemory：

1. **打开仪表板查看当前状态**
   ```bash
   open http://localhost:3113
   ```
   初始是空的，迁移后才有数据可搜。

2. **迁移 MEMORY.md 内容**
   使用 CLI migrate 命令：
   ```bash
   agentmemory migrate --from-file ~/.openclaw/workspace/MEMORY.md --verbose
   ```

3. **验证迁移结果**
   迁移完成后，再次打开 http://localhost:3113 查看记忆仪表板，确认数据已入库。

> 注意：MEMORY.md 本身保留不动，两套系统共存 — agentmemory 负责语义搜索，MEMORY.md 负责手工精修知识。

---

### 核心 MCP 工具

| 工具 | 用途 |
|------|------|
| `memory_recall` | 跨所有记忆的语义搜索 |
| `memory_save` | 以类型/标签存储新记忆 |
| `memory_smart_search` | BM25+向量混合搜索 |
| `memory_timeline` | 按时间线查看记忆 |
| `memory_profile` | Agent 记忆使用统计 |
| `memory_snapshot` | 完整记忆导出 JSON |
| `memory_forget` | 删除指定记忆 |
| `memory_context` | 获取当前会话上下文 |
| `memory_lesson_save` | 记录从错误中学到的教训 |
| `memory_reflect` | 聚类知识图谱提炼洞察 |

完整 51 个工具列表见 `references/mcp-tools.md`。

---

### 验证

```bash
bash ./scripts/verify.sh
```

预期结果：
- ✅ 记忆服务器在 3111 端口运行
- ✅ Health 端点正常响应
- ✅ 仪表板在 3113 端口可访问
- ✅ OpenClaw MCP 已配置
- ✅ systemd 服务已激活

### 手动健康检查

```bash
curl http://127.0.0.1:3111/agentmemory/health | python3 -m json.tool
```

健康响应包含：`{"status":"healthy","uptimeSeconds":...,"workers":[...]}`

---

### 卸载

**仅移除 MCP 模式：**

1. 从 `openclaw.json` 的 `mcp.servers` 中删除 agentmemory 条目
2. 执行 `openclaw gateway restart`

**完全移除：**

```bash
systemctl --user stop agentmemory
systemctl --user disable agentmemory
rm ~/.config/systemd/user/agentmemory.service
pkill -f "agentmemory"
```

---

### 故障排查

**"Connection refused on port 3111"**
服务器未启动，启动它：
```bash
systemctl --user start agentmemory
# 或手动：npx @agentmemory/agentmemory
```

**修改 openclaw.json 后提示 "Config invalid"**
确保路径是 `mcp.servers`（不是 `mcpServers`）：
```bash
openclaw status  # 应显示 "Config valid"
```

**查看实时日志：**
```bash
journalctl --user -u agentmemory -f --since "1 hour ago"
```

**iii-engine 版本不匹配**
如果 `api::graph-stats` 等 v0.11.6 函数未注册：
```bash
# 检查当前 iii-engine 版本
curl -s http://127.0.0.1:3111/agentmemory/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
for w in d['health']['workers']:
    print(w['name'], '→', w['version'])
"

# 确认 systemd service 中设置了 AGENTMEMORY_III_VERSION=latest
systemctl --user status agentmemory
grep AGENTMEMORY_III_VERSION ~/.config/systemd/user/agentmemory.service

**WebSocket 断连 (1006)**
这通常是客户端事件（浏览器切页、网络抖动），非 Gateway 故障。检查：
```bash
journalctl --user -u openclaw-gateway --since "5 minutes ago" | grep -E "connected|disconnected"
```
如果 Gateway 在断连后显示 `webchat connected`，说明服务正常。

---

*🦞 Skill by 龙虾 — agentmemory-mcp on ClawHub: https://clawhub.ai/lufei4/agentmemory-mcp*