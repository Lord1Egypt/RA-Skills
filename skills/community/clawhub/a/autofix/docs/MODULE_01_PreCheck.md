---
name: MODULE_01_PreCheck
description: Defines the initial checks performed before any external search or action is taken. This ensures context is rich, safety is guaranteed, and we are not solving a problem in a vacuum. (L1/L2 Enhanced)
---

# 🧠 Step 0: Pre-Check & Context Gathering (Level 1 & 2 Active)

**Goal:** To tailor the resolution strategy, set safety parameters, and ensure we have all necessary background information before querying external sources.

## ✅ Checks Performed (The Triage)

1.  **Session State Check:**
    *   **Action:** Read `~/proactivity/session-state.md`.
    *   **Purpose:** Determine the *last explicit goal* or *active blocking decision*. This prevents us from solving a problem that was already addressed in the last turn, or ignoring an active constraint.

2.  **User Preference Check:**
    *   **Action:** Read `USER.md` and `IDENTITY.md`.
    *   **Purpose:** Understand user context (e.g., "老爸"的偏好) and preferred documentation sources/vibe, which can influence the tone of the final answer.

3.  **Initial Triage & Safety Scan (CRITICAL):**
    *   **Action:** Analyze the user's input string for patterns indicating risk or known issue types.
    *   **Risk Assessment:** Determine if the query contains sensitive information (API Key, Secret Token, Passwords). If found, mark it as `[RISK: HIGH]` and prioritize security in the response.
    *   **Issue Type Classification:** Attempt to classify the problem into buckets like: `[Tooling/CLI]`, `[Config/Gateway]`, `[Feature Implementation]`, `[General Bug]`。

## 🚀 Level 2 Proactive Check (Hot Start)
This is our proactive layer. Before searching, we check if there's a recent, high-confidence solution ready to serve!
*   **Action:** Run `memory_search(query="[User Query Summary]", corpus="all", maxResults=3)`。
*   **Purpose:** 检查最近的 Top 3 解决方案，如果找到高分结果，则直接在回答前展示给用户（热启动）。

## ✅ v6.0 新增: Runtime Health Check (M1)

> 本检查是对 `openclaw doctor` 静态配置扫描的运行时补充，提供进程级、网络级和资源级的健康检测。

**Action:** 运行运行时健康检测脚本。

```bash
python scripts/runtime_health_check.py
```

**输出格式示例:**

```
🔍 OpenClaw Runtime Health Check v6.0-M1
============================================================
  整体健康等级: 🟠
  🔴 阻断: 0  🟠 高风险: 2  🟡 可优化: 2  🟢 正常: 1
============================================================

  🟢 🌐 Gateway 状态
       → PID: 15616, RPC: ok (角色: operator)
  🟠 💾 磁盘用量
       → .openclaw 目录 1799 MB ⚠️ 超过 1000MB 警告线
  🟡 📋 Session 积压
       → 140 个 session 文件 ⚠️ 超过 100 个阈值
  🟠 📜 日志异常
       → 8 ERROR / 11 WARN / 20 RATE_LIMIT（近 60 分钟）
  🟡 🔌 模型连通性
       → 配置中未定义 providers，跳过
```

### 各检查项说明

| 检查项 | 说明 | 数据来源 |
|--------|------|---------|
| 🌐 Gateway 状态 | 进程存活、RPC 连通性、配置审计 | `openclaw gateway status --json` |
| 💾 磁盘用量 | `.openclaw` 目录总大小 | `os.walk()` 统计 |
| 📋 Session 积压 | `agents/main/sessions/` 中 .jsonl 文件数 | 文件系统遍历 |
| 📜 日志异常 | 最近 N 分钟内的 ERROR/WARN/RATE_LIMIT 模式 | `openclaw-*.log` + `commands.log` 扫描 |
| 🔌 模型连通性 | 对各 provider 的 baseUrl 做 `GET /v1/models` | `openclaw.json` 解析 + HTTP 请求 |

### 严重性判定

| 级别 | 说明 | 行为 |
|------|------|------|
| 🔴 Critical | Gateway 不可用、RPC 断开、磁盘 >5GB | 立即中断当前流程，通知用户 |
| 🟠 High | 高频错误、大量 session 积压、磁盘 >1GB | 记录到上下文，建议用户修复 |
| 🟡 Medium | 少量警告、模型端点未配置 | 信息记录，不影响流程 |
| 🟢 Normal | 一切正常 | 静默通过 |

## ✅ v6.0 新增: API 密钥验证 + 资源监控 (M2)

> 对 M1 的增强：验证所有已配置 API 密钥的有效性，并深入监控运行时资源水位。

**Action:** 运行 API 密钥验证脚本（包含资源监控）。

```bash
python scripts/api_key_validator.py
```

### API 密钥验证 (P1)

自动扫描 `openclaw.json` 和 `TOOLS.md`，对检测到的所有密钥进行：

| 步骤 | 检测内容 |
|------|---------|
| ① 格式检查 | 根据服务商模式匹配（OpenAI `sk-...`、Tavily `tvly-...` 等）|
| ② 污染检测 | 检测嵌入空格/换行符等复制粘贴错误 |
| ③ 连通性验证 | 对支持的服务做轻量 API 调用（`GET /v1/models`、`POST /search` 等）|

**支持的密钥类型：**

| 类型 | 验证方式 | 已检测到的环境 |
|------|---------|--------------|
| OpenAI | `GET https://api.openai.com/v1/models` | ✅ 存在 (但含空格，已标记为损坏) |
| Tavily | `POST https://api.tavily.com/search` | ✅ 有效 |
| GitHub | `GET https://api.github.com/user` | ✅ 有效 (用户: your_github_username) |
| Notion | `GET https://api.notion.com/v1/users` | ⚠️ 网络不可达 |
| Feishu | 格式检查 (无外部端点) | ✅ 格式有效 |
| Gateway | 内部令牌验证 (无外部端点) | ✅ 无需验证 |
| SearXNG | 端点可达性检测 | ❌ 端点不可达 |

### 资源监控 (P2)

| 检查项 | 说明 | 阈值 |
|--------|------|------|
| 🧠 Gateway 内存 | 读取 Gateway 进程的 RSS 内存 | 🟠 > 500MB / 🔴 > 1GB |
| 📦 日志文件大小 | 所有 log + jsonl 文件总和 | 🟠 > 50MB |
| 📋 Session 积压 | `agents/main/sessions/` 中 jsonl 文件数 | 🟡 > 100 个 |

> **提示：** 如需精确内存检测，建议 `pip install psutil`。否则自动降级为 `tasklist` 模式。

### 输出示例

```
🔑 OpenClaw API Key Validator v6.0-M2

  🔍 测试: Tavily (配置)            ✅ 有效
  🔍 测试: GitHub (配置)            ✅ 有效 (用户: github_username)
  🔍 测试: OpenAI_CORRUPTED (配置)   ❌ Key 格式异常 (含空格)

📊 资源监控检查 (P2)
  🟢 📦 日志文件总大小: 3 MB
  🟠 🧠 Gateway 进程内存: 656 MB
  🟡 📋 Session 文件: 140 个

============================================================
  整体健康等级: 🔴
  🔴 阻断: 4  🟠 高风险: 1  🟡 可优化: 3  🟢 正常: 3
============================================================
```

## ✅ v6.0 新增: 统一诊断报告 + 回归验证 (M3)

> 将 M1(运行时) + M2(密钥/资源) + `openclaw doctor`(配置) 整合为一份按严重性排序的统一报告，并支持修复前后的回归对比。

### 统一诊断报告 (P3)

**Action:**

```bash
# 运行完整诊断（合并三份来源，按 🔴→🟠→🟡→🟢 排序输出）
python scripts/diagnosis_formatter.py
```

**流程：**

```
openclaw doctor  ─┐
                   ├──→ diagnosis_formatter.py → 统一报告
runtime_health    ─┘     (按严重性排序 + 分类)
api_key_validator ─┘
```

**输出示例：**

```
🔬 OpenClaw 健康诊断报告
============================================================
  整体健康等级: 🔴
  🔴 阻断: 2  🟠 高风险: 3  🟡 可优化: 22  🟢 正常: 6

  ── 阻断级问题 (2) ──
  🔴 [🔑 密钥] OpenAI 网络不可达
  🔴 [🔑 密钥] SearXNG 端点不可达

  ── 高风险问题 (3) ──
  🟠 [💾 存储] .openclaw 目录用量: 1801 MB
  🟠 [📜 日志] 日志异常扫描 (10 ERROR / 9 WARN)
  🟠 [📊 资源] Gateway 内存: 568 MB

  ── 可优化项 (22) ──
  🟡 [⚙️ 配置] plugins.allow 过期引用
  🟡 [⚙️ 配置] agent 模型无 fallback
  🟡 [📋 Session] 140 个文件积压
  ...

  ── 正常项 (6) ──
  🟢 [🌐 Gateway] 运行中 (PID: 15616)
  🟢 [🔑 密钥] Tavily ✅ | GitHub ✅ | Notion ✅

  ── 📋 建议操作 ──
  🔴 检查网络连接 (OpenAI/Notion/SearXNG)
  🟠 清理旧 session 记录和日志
  🟠 Gateway 内存超过 500MB
  🟡 运行 openclaw doctor --fix 自动归档
```

### 回归验证 (P4)

**Action:**

```bash
# 第 1 步：在执行修复前保存基线
python scripts/diagnosis_formatter.py --save-baseline

# 第 2 步：执行修复（如 openclaw doctor --fix）
# 第 3 步：对比当前状态 vs 基线
python scripts/diagnosis_formatter.py --compare
```

**输出示例：**

```
📋 回归验证报告
  ✅ 已修复: 2
  🆕 新增:   1
  📈 改善:   0
  📉 恶化:   0
  ➖ 不变:   32

  ✅ 已修复问题:
     🟢 plugins.allow 过期引用 → 已清理
     🟢 孤立 session 文件 → 已归档

  🆕 新问题:
     🟠 Gateway 内存变化 (boundary case)
```

### 与 `openclaw doctor` 的配合

推荐的一键诊断流程：

```bash
# 完整的一站式诊断
python scripts/diagnosis_formatter.py
```

内部执行顺序：

| 步骤 | 工具 | 耗时 | 覆盖范围 |
|------|------|:---:|---------|
| Step 1 | `openclaw doctor` | ~30-90s | 配置完整性、安全策略、技能/插件 |
| Step 2 | `runtime_health_check.py` | ~10-15s | 进程状态、网络连通、日志异常 |
| Step 3 | `api_key_validator.py` | ~20-30s | 密钥有效性、资源水位 |
| Step 4 | `diagnosis_formatter.py` | 合并 | 统一排序输出 + 回归对比 |

## ✅ v6.0 新增: 可视化仪表盘 (M4)

> 将统一诊断报告渲染为深色主题的交互式 HTML 仪表盘，支持 Canvas 内嵌展示。

**Action:**

```bash
# 生成仪表盘并写入 Canvas
python scripts/health_dashboard.py --canvas
```

**仪表盘包含：**

| 区域 | 内容 |
|------|------|
| 🟢 顶部状态 | 整体健康等级 + 时间戳 |
| 🔴 严重性分布条 | 可视化 🔴🟠🟡🟢 占比 |
| 🗂️ 分类详情 | 按类别分组（Gateway/密钥/资源等） |
| 📋 建议操作 | 所有待处理建议清单 |
| 📊 基线对比 | 如存在基线，显示前后对比状态 |

**设计主题：** 极简野蛮 (Brutalist Minimalism) — 高对比度、无渐变、等宽字体、粗边框。

### Canvas 内嵌

生成后可通过以下方式嵌入 WebChat：

```markdown
[embed ref="health_dashboard" title="健康仪表盘" height="740"]
```

## 🛡️ Safety & Context Injection (新增/增强)
If any of these checks yield critical data, it must be injected into subsequent steps.

- **Risk Flag:** If `[RISK: HIGH]` is set, the final answer *must* start with a security warning/acknowledgement.
- **Context Tagging:** The identified issue type should be prepended to the search query (e.g., "Tooling/CLI: Why is exec command hanging?").
- **🚨 新增：输入内容扫描**: 如果检测到敏感信息，系统应在回答前主动发出警告。

## 🔗 Next Step Dependency
This module's output directly feeds into **Step 1 (Primary Search)**, providing a highly refined and context-aware query string。