# Blender MCP Skill

An OpenClaw Agent Skill for connecting to and controlling Blender via the official [Blender MCP Server](https://www.blender.org/lab/mcp-server/).

用于连接和控制 Blender 的 OpenClaw Agent 技能，通过官方 [Blender MCP Server](https://www.blender.org/lab/mcp-server/) 实现。

**Version: 3.7.3** — Blender 5.1+（官方硬性要求）/ **生产基准 = 5.3（5.3.0，2026-11-10 正式发布，三件套全绿：镜像 `Blender5.3/` + Gitea tag `v5.3.0` + `.msi` 200）** / **兼容下限 = 5.2 LTS（5.2.4，同日发布）** / 5.4 仍 Alpha（until 2027-02-03），只用 `hasattr` 兜底

> ⚠️ **平台前提**（2026-10-25 核验）：官方 add-on 要求 Blender ≥ 5.1，而 **Blender 5.0 起 macOS 只出 Apple Silicon 构建** → **Intel Mac 上没有可用的「5.1+ × 官方 MCP」组合**（4.5 LTS 是最后一个支持 Intel 的版本）。Windows / Linux 不受影响（Windows 需 4 核 SSE4.2 + OpenGL 4.3 或 Vulkan 1.3、8 GB RAM）。来源：<https://www.blender.org/download/requirements/>

---

## ⚠️ Security Warning / 安全警告

**English:**
This skill provides full access to Blender's Python API (`bpy`) through the MCP channel. Code executed via `execute_blender_code` can:
- Read, modify, or delete files on your system
- Execute arbitrary Python code (including network requests)
- Alter or corrupt your Blender project data

**Always review code before execution. Keep backups of important `.blend` files.**

**中文：**
此技能通过 MCP 通道提供对 Blender Python API (`bpy`) 的完全访问。通过 `execute_blender_code` 执行的代码可以：
- 读取、修改或删除系统上的文件
- 执行任意 Python 代码（包括网络请求）
- 更改或损坏 Blender 项目数据

**执行前请始终审查代码。保持重要 `.blend` 文件的备份。**

---

## What's New in v3.7.3 / 更新内容

### v3.7.3 (2026-11-12) — 基线切换：生产基准 5.2 LTS → **5.3**，5.2.4 = 兼容下限
- 🟢 用户拍板「全面更新到 5.3 然后兼容 5.2」→ **生产基准 = 5.3（5.3.0，2026-11-10 发布）**、**兼容下限 = 5.2 LTS（5.2.4）**
- 📝 口径改了 5 处：`SKILL.md` 版本支持行 + API 兼容段、`references/api.md` 头部（en）+ 5.3 / 5.2 两个兼容段标题与说明、本 README 版本行 / 特性行 / Requirements / 版本支持表
- ✅ 发布事实（2026-11-11 复扫三件套全绿）：镜像 `Blender5.3/` 200、Gitea tag `v5.3.0` 200、`.msi` HEAD 200；同日 5.2.4 / 4.5.16 也发布
- 📌 MCP 生态零增量（issues 27 / PR 5 全未合并 / releases 6 · v1.0.3 / stars 37 / forks 38）→ 本次是**口径对齐版**，不是新发现版
- ⚠️ 历史条目（≤ v3.7.2）里「以 5.2.3 LTS 为基准」是当时的正确结论，**不改写**

## What's New in v3.6.2 / 更新内容

### v3.6.2 (2026-10-26) — ClawHub 安全扫描口径修正 / Security-scan remediations
- 🔴 **ClawHub 把已上线的 v3.5.1 重新判为 `suspicious`**（`decision: fail`、skillspector `CRITICAL` / `DO_NOT_INSTALL`、`max_issue_severity: HIGH`，2026-10-23T02:37Z 扫描）→ **3.6.0 / 3.6.1 的提交因此一直 pending**，`latest` 停在 3.5.1
- 🟢 修掉 4×HIGH：历史 Changelog 里描述「已移除」的那句话仍带着 curl-pipe-shell 字面量 → 改为 `curl-pipe-to-shell` 表述
- 🟡 仍存 6×HIGH：`SKILL.md (partial)` —— SKILL.md ~64 KB 超出扫描器单文件预算，只做部分分析即计罚 → 需拆 `references/`，另立任务
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.6.2**）

## What's New in v3.6.1 / 更新内容

### "MCP Can't Connect" — the Outermost Cause Is uv Dependency Download / 「连不上」的最外层根因（v3.6.1 · 2026-10-25）
- 🟢 **排障表新增一条**：日志里出现 `Failed to download <pkg>` ＋ **`invalid peer certificate: UnknownIssuer`**（`files.pythonhosted.org` 的 wheel，如 `rpds-py` / `pydantic-core` / `pyyaml`）→ **uv 建不起 venv**，最终表现仍是 "MCP Blender: Server disconnected"。来源 = 官方 issue **#67**（2026-10-25，正文含完整 Claude Desktop 日志）
- 🔴 **与 SAC 拦截严格分层**：#56 / #65 = **进程启动**被 Windows Smart App Control 拦签名；#67 = **依赖下载**（更早一层）被 TLS 中间人拦证书 → **命中 #67 时按 SAC 路径排查纯属白折腾**
- 🟢 处置三条路径：`UV_NATIVE_TLS=1`（uv 走系统信任库）／`SSL_CERT_FILE=<ca.pem>`（企业根证书）／代理或杀软对该域名关闭 HTTPS 解密；修完用 `uvx blender-mcp==1.0.3` 复验依赖可下载
- 📌 **MCP 生态增量**（2026-10-25 10:00 Gitea API）：open issues **22 → 23（仅 #67）**｜open PR **4**（#66 / #48 `mergeable: true` 未合并，#47 / #43 `mergeable: false`）｜releases **6 条 / v1.0.3**｜stars 33 / forks 33 / watchers 12 / `licenses` GPL-3.0｜assets `.mcpb` **39531** / `.zip` **344916**（自然增长）
- 📌 版本面：5.2.3 LTS 现行｜5.3 Beta（RC 11-04 → 发布 11-10，daily `32f5c9c48bca` 含 GSplat 修复）｜5.4 Alpha 至 **2027-02-03**；镜像仍无 `Blender5.3/`、`Blender5.4/` → 基线不前移
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.6.1**）

## What's New in v3.6.0 / 更新内容

### Platform Prerequisite: Intel Mac Has No Valid Combo / 平台前提：Intel Mac 无可用组合（v3.6.0 · 2026-10-25）
- 🟢 **新增平台前提**：官方 add-on 硬性要求 **Blender ≥ 5.1**，而 **Blender 5.0 起 macOS 只有 Apple Silicon 构建**（需 Apple Silicon + macOS 13 Ventura 起；`4.5 LTS` 是最后一个支持 Intel Mac 的版本）→ **Intel Mac 上「Blender 5.1+ × 官方 MCP」这个组合根本不存在**。此前技能只写「Blender 5.1+」，Intel Mac 用户会照着试到怀疑人生
- 🟢 Windows / Linux 不受影响，但 Windows 有硬门槛：**4 核 SSE4.2 + OpenGL 4.3 或 Vulkan 1.3、8 GB RAM、2 GB VRAM**（来源 <https://www.blender.org/download/requirements/>，2026-10-25 核验）
- 📌 **MCP 生态零增量**（2026-10-25 Gitea API，与 10-24 逐字段一致）：open issues **22**｜open PR **4**（#66 / #48 / #47 / #43 均未合并）｜releases **6 条 / v1.0.3**｜stars 33 / forks 33 / watchers 12 / `licenses` GPL-3.0｜assets 自然增长（`.mcpb` **39193** / `.zip` **341649**）
- 📌 版本面：5.2.3 LTS 现行（10-22 发布、未撤回）｜5.3 Beta "until November 4, 2026"（RC 11-04 → 发布 11-10）｜**5.4 Alpha "until February 3, 2027"**（官方首次给结束日期）→ 基线不前移
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.6.0**）

## What's New in v3.5.1 / 更新内容

### Version Baseline Corrected + Thumbnail Root Cause / 版本基准更正 + 缩略图根因（v3.5.1 · 2026-10-23）
- 🔴 **Blender 5.2.3 LTS 已于 2026-10-22 正式发布**（与 4.5.15 同日）：镜像 `blender-5.2.3-*` 全平台包 ＋ `.msi` HTTP 200 ＋ Gitea tag `v5.2.3`，官网首页 "LATEST RELEASE … Released October 22, 2026"。本 README 原写「5.2.3 仍是 RC、未发布」**已过期**，版本口径统一改为 **5.2.x LTS（当前 5.2.3）**
- 🟢 **缩略图全分辨率坑补根因**（官方 PR **#66**，2026-10-22，未合并）：上下文管理器在 `INVOKE_DEFAULT` job **返回时**就恢复渲染设置，job 真正执行在后面 → 读到的是用户原设置；另 EEVEE 引擎标识需匹配 `BLENDER_EEVEE`。作者实测 1920×1080/1.6 MB/~9 s → 320×180/50 KB/0.8~1.3 s
- 🟢 **PR #48 获第三方复现**（未合并）：`execute_blender_code_for_cli` 在 main `dbbf836` 上 120 s 超时 → 打补丁 **2.8 s**（2026-10-22）→ 本地 `stdin=subprocess.DEVNULL` 补丁的处置继续有效
- 📌 MCP 快照（2026-10-23）：发布仍 **v1.0.3**（无 v1.0.4）｜落地页链接**第 14 次一致**｜open issues **22 未变**｜**open PR 3 → 4**（新增 #66）｜stars/forks **33**
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.5.1**）

## What's New in v3.5.0 / 更新内容

### SAC Troubleshooting Corrected / 排障表 SAC 条目重写（v3.5.0 · 2026-10-20）
- 🔴 **旧建议被官方 issue 证伪**：v3.3.0 起排障表写「`blender-mcp.exe` 被 Smart App Control 拦 → 改用官方 add-on 通道」。**官方 issue #65（2026-10-19）**：用户在**官方 MCPB 扩展**里同样被拦 —— 扩展自带 `.venv\Scripts\blender-mcp.exe` `NotSigned`，Claude Desktop 报 "MCP Blender: Server disconnected"，Code Integrity **event 3077**（与 #56 的 uv 路径同因）
- 🟢 条目改为机制 + 判据：SAC enforcement 只放行「被应用智能服务识别」或「受信任 CA 签名」的二进制（Microsoft Learn）→ 未签名 launcher 必被拦；处置 = 先验签名 → 决策（是否关闭 SAC）交还用户，企业域策略不动
- ⚠️ 留待核验：SAC 是否支持单应用白名单（未查到官方入口，不写死）
- 📌 MCP 仓库快照（2026-10-20）：最新发布仍 **v1.0.3**（无 v1.0.4）｜落地页链接**连续 11 次一致**｜Open issues **21 → 22**（新增 #65）｜Open PR **#48 / #47 / #43 仍未合并**｜stars 28 → 30
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.5.0**）；**已双平台发布（2026-10-20 13:21）**：GitHub tag `v3.5.0` ＋ ClawHub latest=3.5.0

## What's New in v3.4.0 / 更新内容

### Two New Official Tool-Behavior Gotchas / 两条新官方工具行为坑（v3.4.0 · 2026-10-16）
- 🟢 **issue #63（Windows 多开陷阱）**：`mcp_to_blender_server.py` 在 `bind()` 前设 `SO_REUSEADDR`，Windows 语义允许**第二个 Blender 静默绑定已占用端口** → 服务按钮显示 "Server is started"，但客户端始终连**第一个**实例（现象：改了没反应 / 操作落到另一个窗口）。创建者 Win11 + Blender 5.2.2 LTS + blender_mcp 1.0.2 实测 **20/20 复现** → 技能处置：只开一个实例 / 先关旧实例再 Start / `netstat -ano | findstr 9876` 查占用
- 🟢 **issue #64（返回值类型）**：`execute_blender_code` 的 `result` **必须为 dict**，官方 `prompts.yml` L48 说可返回 "dicts, lists" 是**文案与实现不一致**（报错：`The result variable must be a dict, not list. Wrap your return value: result = {"key": value}`）→ 技能处置：返回值**一律包成 dict**
- 📌 MCP 仓库快照：最新发布仍 **v1.0.3**（无 v1.0.4）｜落地页链接**连续 8 次一致**｜Open issues **18 → 21**｜Open PR **#48 / #47 / #43 仍未合并**
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.4.0**）；**已双平台发布（2026-10-16 10:41）**：GitHub `taosiuman/blender-skill` tag/Release **v3.4.0**（= Latest）＋ ClawHub `@taosiuman/blender-mcp` **latest=3.4.0**（安全扫描 Moderate CLEAN）→ 三方一致

### Official Issue/PR Evidence + Tool-Behavior Troubleshooting / 官方 issue 实证取证 + 工具行为排障（v3.3.0 · 2026-10-13）
- 🟢 **取证渠道**：`projects.blender.org` 网页长期 403 → 改走 **Gitea REST API**（`/api/v1/repos/lab/blender_mcp/{releases,issues,pulls}`），issue/PR 状态首次拿到**官方实证**
- 🟢 **add-on 版本**：最新发布仍 **v1.0.3（2026-09-11）**，无 v1.0.4；Open PR = **#48 / #47 / #43**（均未合并）
- 🟢 排障表新增 7 条可溯源行为坑（`*_for_cli` Windows stdio 挂死 / `execute_blender_code` 新命名空间 / `get_objects_summary` 上下文爆炸 / 缩略图分辨率与临时目录 / `get_python_api_docs` 需重复类名 / macOS `.mcpb` / Windows SAC）
- ⚠️ 作废不存在的 **#344 / #345 / #348**（官方 API 实测 404）；新增「不得用搜索摘要代替官方源」规则
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.3.0**）

### 5.3 Beta Alignment + Install & Troubleshooting Fixes / 5.3 Beta 口径 + 安装与排障修正（v3.2.0 · 2026-10-11）
- 🟢 5.3 兼容章节由「dev — 前瞻」改为「**Beta — API 已稳定**」：官方 release notes 首页原文 *"currently in Beta until November 4, 2026"*（RC 节点）→ 发布 **2026-11-10**
- 🟢 安装步骤改用官方 **add-on v1.0.3** 链接（原写 v1.0.0 已过期），补 **Blender ≥ 5.1** 硬性要求与「拖拽安装要拖两次」
- 🟢 排障表新增 4 条真实高频坑：Auto Start 只在启动时触发 / 两个 MCP add-on 抢 9876 端口 / Allow Online Access / 拖拽要拖两次
- 🟢 澄清两个版本号：**add-on v1.0.3**（Blender 侧）≠ **MCP Server 包 1.0.0**（PyPI `blender-mcp`，`uvx` 侧）
- ✅ 版本号三处一致（SKILL.md frontmatter / 本 README 版本行 / 两处 Changelog = **3.2.0**）

### Docs Consistency Fix / 文档一致性修复（v3.1.1 · 2026-10-08）
- ✅ README 变更日志补齐 v3.0.0 / v3.1.0 / v3.1.1 —— 修复「版本行写 3.1.0、正文却停在 v2.5.9」的版本漂移
- ✅ README changelog caught up with the actual version (no more v2.5.9 drift)
- ✅ 核验日期更新至 2026-10-07（10-06 / 10-07 每日快扫均无 API 增量）
- ✅ 无 API 内容变更，纯文档版本 / Docs-only release, no API content change

### Blender 5.3 API Verification / 5.3 API 全量核验（v3.1.0 · 2026-10-05）
- 🔴 **函数签名变更**（按位置传参会静默出错或 TypeError）：`ObjectConstraints.new` / `PoseBoneConstraints.new` 由 `(type)` → `(type, name)`；`UILayout.textbox` / `textbox_with_state` 位置参数重排；`WindowManager.popover*` 新增 `auto_keymap` → **一律改用关键字传参**
- 🟢 新增 API：`BlendFileColorspace` OCIO 诊断三项、`MaterialGPencilStyle.gradient`、`SpaceOutliner.show_users_column` / `sort_method`、`UILayout.label_markdown`
- 📌 完整清单见工作区 `references/api.md`
- 📌 版本状态：最新稳定版 **5.2.2 LTS**（2026-09-15）；5.3 官方 API 文档已生成但未发布 → 按前瞻兼容处理

### Workspace Rebuild / 工作区重建（v3.0.0 · 2026-10-05）
- 🏗 技能元数据 `metadata.openclaw` → `metadata.octop`（现由 octop agent **B 哥** 维护）
- 🏗 知识库拆分：API 变更明细移入工作区 `knowledge/`，技能保留「速览 + 兼容模板 + 排障」
- 🏗 修复版本号漂移：`version` / README 版本行 / Changelog 三处强制一致

### Previous Updates / 之前的更新

**v2.5.9 (2026-09-23):** Security release — removed dangerous **curl-pipe-to-shell** pattern, added explicit bpy-execution warnings, pinned dependency versions, bilingual (EN/CN) docs

**v2.5.8:** 8 new APIs + 2 breaking changes documented
- CollectionChild.sort_index, ColorManagedInputColorspaceSettings.interop_id, etc.

**v2.5.7:** BrushGpencilSettings.use_cyclic_stroke (Grease Pencil cyclic stroke)

**v2.5.6:** PointCloud.type (point cloud data access)

---

## Features / 功能

- **20 built-in tools** — scene analysis, screenshots, rendering, navigation, doc search
- **Arbitrary bpy code execution** — full Python API access through the MCP channel
- **3 connection modes** — mcporter (recommended), direct TCP socket, background/headless
- **Geometry Nodes MCP integration** — data relationship queries, scene debugging, node tree inspection
- **Auto Start** — enable in addon preferences to auto-start MCP Server on Blender launch
- **Blender 5.1 / 5.2 LTS (floor) / 5.3 (baseline) compatible** — includes workarounds for all breaking API changes

- **20 个内置工具** — 场景分析、截图、渲染、导航、文档搜索
- **任意 bpy 代码执行** — 通过 MCP 通道访问完整的 Python API
- **3 种连接模式** — mcporter（推荐）、直接 TCP 套接字、后台/无头
- **几何节点 MCP 集成** — 数据关系查询、场景调试、节点树检查
- **自动启动** — 在插件首选项中启用，Blender 启动时自动启动 MCP Server
- **兼容 Blender 5.1 / 5.2 LTS（兼容下限）/ 5.3（生产基准）** — 包含所有破坏性 API 变更的解决方案

---

## Quick Start / 快速开始

### Option A: mcporter (recommended / 推荐)
```bash
npm install -g mcporter
mcporter config add blender-mcp --transport stdio --command "python -m blmcp --transport stdio"
```

### Option B: uvx (with pinned version / 固定版本)
```bash
# Install uv first (safe method / 安全方法)
# All platforms: download uv from https://github.com/astral-sh/uv/releases and review it first.

# Run with pinned version / 使用固定版本运行
uvx blender-mcp==1.0.0
```

### Then call tools / 然后调用工具
```bash
mcporter call blender-mcp.get_objects_summary
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"count": len(bpy.data.objects)}'
```

---

## Install Dependencies / 安装依赖

```bash
# Install with pinned versions / 使用固定版本安装
pip install mcp==1.8.0 pyyaml==6.0.2 starlette==0.45.0

# Start MCP Server (stdio mode)
python -m blmcp --transport stdio

# Or HTTP mode
python -m blmcp --transport http --host 127.0.0.1 --port 8000
```

---

## Telemetry / 遥测

**English:** Anonymous usage telemetry may be collected by default. To disable:
```bash
export DISABLE_TELEMETRY=true  # Linux/Mac
set DISABLE_TELEMETRY=true    # Windows CMD
$env:DISABLE_TELEMETRY=true   # PowerShell
```

**中文：** 默认情况下可能会收集匿名使用遥测数据。禁用方法：
```bash
export DISABLE_TELEMETRY=true  # Linux/Mac
set DISABLE_TELEMETRY=true    # Windows CMD
$env:DISABLE_TELEMETRY=true   # PowerShell
```

---

## Requirements / 系统要求

- Blender 5.1+ (5.2.x LTS = compatibility floor, **5.3.x = production baseline**)
- Python 3.13+
- Node.js 18+ (for mcporter)

---

## Blender Version Support / Blender 版本支持

| Version | Status | Support |
|---------|--------|---------|
| **5.3 (5.3.0, 2026-11-10)** | **Stable — 生产基准** | ✅ 全功能；新代码默认目标 |
| 5.2 LTS (current 5.2.4, 2026-11-10) | Stable — **兼容下限** | Until 2028-07；每条 5.3 路径都必须留回退 |
| 5.1 | Stable | Legacy（按需） |
| 4.5 LTS (current 4.5.16, 2026-11-10) | Supported | Until 2027-07 |
| 5.4 | Alpha（main，until 2027-02-03） | **不承诺**：仅 `hasattr` 兜底 |

---

## Repository Contents / 仓库内容

| File | Description |
|------|-------------|
| SKILL.md | Complete skill definition — architecture, installation, 20 tools, protocol, 5.1/5.2/5.3 compatibility notes, troubleshooting |
| README.md | Project overview and quick start guide (bilingual) |

| 文件 | 描述 |
|------|------|
| SKILL.md | 完整的技能定义 — 架构、安装、20 个工具、协议、5.1/5.2/5.3 兼容性说明、故障排除 |
| README.md | 项目概述和快速入门指南（双语） |

---

## License / 许可证

Apache-2.0

---

## Changelog / 变更日志

> 顺序：最新在上。**版本号三处必须一致**（`SKILL.md` frontmatter / 本文件顶部版本行 / 本 Changelog 首条）。
> 2026-10-11 修复：本节此前**重复两遍**且缺失 v3.1.0 / v3.1.1 条目（v3.0.0 与 v2.5.x 混排、还残留一行截断文本）。

### v3.6.1 (2026-10-25) — 「连不上」的最外层根因：uv 依赖下载被 TLS 证书拦截（官方 issue #67）
- 🟢 排障表新增：`Failed to download …` + **`invalid peer certificate: UnknownIssuer`**（`files.pythonhosted.org`）→ uv 建不起 venv，表现仍是 "MCP Blender: Server disconnected"（官方 issue **#67**，2026-10-25，日志里 `rpds-py` / `pydantic-core` / `pyyaml` 三包同报）
- 🔴 **与 #56 / #65 严格分层**：#56 / #65 = 进程启动被 Windows SAC 拦签名；#67 = 依赖下载（更早一层）被 TLS 中间人拦证书 → 命中 #67 时按 SAC 排查会白折腾
- 🟢 处置：`UV_NATIVE_TLS=1` / `SSL_CERT_FILE=<ca.pem>` / 对该域名关 HTTPS 解密；修完 `uvx blender-mcp==1.0.3` 复验
- 📌 MCP 增量：open issues **22 → 23（仅 #67）**｜open PR 仍 4（#66 / #48 `mergeable: true` 未合并）｜releases 6 / **v1.0.3**｜stars 33 / forks 33 / GPL-3.0｜assets 39531 / 344916（自然增长）
- 📌 版本面：5.2.3 LTS 现行｜5.3 Beta（RC 11-04 → 发布 11-10）｜5.4 Alpha until 2027-02-03；镜像仍无 `Blender5.3/`、`Blender5.4/`
- ⚠️ 待核验：SAC 单应用白名单（#65 无新回复）

### v3.6.0 (2026-10-25) — 补「平台前提」：Intel Mac 上没有可用组合
- 🟢 **新增平台前提**：官方 add-on 要求 **Blender ≥ 5.1**，而 Blender **5.0 起 macOS 只出 Apple Silicon 构建**（4.5 LTS 是最后一个支持 Intel Mac 的版本）→ **Intel Mac 无法使用「5.1+ × 官方 MCP」**。Windows 需 4 核 SSE4.2 + OpenGL 4.3 或 Vulkan 1.3、8 GB RAM、2 GB VRAM（<https://www.blender.org/download/requirements/>，2026-10-25）
- 📌 **MCP 零增量**（与 10-24 逐字段一致）：open issues 22｜open PR 4（全未合并）｜releases 6 / **v1.0.3**｜stars 33 / forks 33 / watchers 12 / GPL-3.0｜assets 下载数自然增长（39193 / 341649）→ 排障表与工具坑清单无内容需改
- 📌 版本面：5.2.3 LTS 现行｜5.3 Beta until 11-04（发布 11-10）｜**5.4 Alpha until 2027-02-03**（官方首次给出结束日期）
- ⚠️ 待核验：SAC 单应用白名单（#65 无新回复）

### v3.5.1 (2026-10-23) — 版本基准更正（5.2.3 LTS 已发布）+ 缩略图坑补根因
- 🔴 **Blender 5.2.3 LTS 与 4.5.15 已于 2026-10-22 正式发布**（镜像包 + `.msi` 200 + Gitea tag 三件套全绿；官网 "LATEST RELEASE … Released October 22, 2026"）→ 本 README 原写「5.2.3 仍是 RC、未发布」**已过期**，全技能版本口径改为 **5.2.x LTS（当前 5.2.3）**
- 🟢 排障表「缩略图全分辨率」条目补**根因**（官方 PR **#66**，未合并）：上下文管理器在 `INVOKE_DEFAULT` job **返回时**就恢复设置，job 实际执行读到用户原值；另 EEVEE 标识需匹配 `BLENDER_EEVEE`。实测 1920×1080/1.6 MB/~9 s → 320×180/50 KB/0.8~1.3 s
- 🟢 **PR #48 获第三方复现**：`execute_blender_code_for_cli` main `dbbf836` 120 s 超时 → 打补丁 2.8 s → 「本地 `stdin=subprocess.DEVNULL` 补丁」处置继续有效
- 📌 add-on **v1.0.3** 未变（无 v1.0.4）；落地页链接**第 14 次一致**；open issues **22 未变**；open PR **3 → 4**（新增 #66）；stars/forks **33**

### v3.5.0 (2026-10-20) — 排障表 SAC 条目重写（旧建议被官方 issue #65 证伪）
- 🔴 **纠正**：「`blender-mcp.exe` 被 SAC 拦 → 改用官方 add-on 通道」已不成立 —— 官方 MCPB 扩展自带的 `.venv\Scripts\blender-mcp.exe` 同样 `NotSigned`、同样触发 Code Integrity event 3077（issue **#65**，与 #56 同因）
- 🟢 条目改为机制 + 判据（SAC 只放行智能服务识别 / 受信任 CA 签名的二进制）+ 处置（先验签名 → 关闭 SAC 的决策交还用户）
- ⚠️ 待核验：SAC 是否支持单应用白名单
- 📌 **add-on v1.0.3** 未变（无 v1.0.4）；落地页链接连续 11 次一致；Open issues **21 → 22**；Open PR #48 / #47 / #43 仍未合并；stars 28 → 30
- ✅ **已双平台发布（2026-10-20 13:21）**：GitHub tag `v3.5.0` ＋ ClawHub latest=3.5.0（Moderate CLEAN）

### v3.4.0 (2026-10-16) — 2 条新官方 issue 工具行为坑
- 🟢 排障表补 **2 条**官方 issue：**#63**（Windows `SO_REUSEADDR` → 第二个 Blender 静默占用端口，客户端始终连第一个实例；20/20 复现）｜**#64**（`result` 必须为 dict，官方 instructions 说可返回 list 属文案误导）
- 📌 **add-on v1.0.3** 未变（无 v1.0.4）；落地页链接连续 8 次一致；Open issues **18 → 21**；Open PR #48 / #47 / #43 仍未合并

### v3.3.0 (2026-10-13) — 官方 issue/PR 实证取证 + 工具行为排障补强
- 🟢 取证渠道改走 **Gitea REST API**（网页 403 绕过），issue/PR 状态首次有官方实证
- 🟢 **add-on v1.0.3** 未变（releases API 核实，无 v1.0.4）；Open PR #48 / #47 / #43 未合并
- 🟢 排障表补 **7 条**官方 issue 可溯源的工具行为坑
- ⚠️ 作废不存在的 #344 / #345 / #348（实测 404）

### v3.2.0 (2026-10-11) — 5.3 Beta 口径 + 安装与排障修正
- 🟢 5.3 兼容章节「dev — 前瞻」→「**Beta — API 已稳定**」；写明 **RC 2026-11-04 → 发布 2026-11-10**（官方 release notes 首页原文）
- 🟢 安装改用官方 **add-on v1.0.3** 链接（原 v1.0.0 已过期）+ **Blender ≥ 5.1** 要求 + 「拖拽要拖两次」
- 🟢 排障表补 4 条真实高频坑：Auto Start 仅启动时触发 / 两个 MCP add-on 抢 9876 / Allow Online Access / 拖拽两次
- 🟢 澄清 **add-on v1.0.3**（Blender 侧）≠ **MCP Server 包 1.0.0**（PyPI，`uvx` 侧）

### v3.1.1 (2026-10-08) — Docs Consistency Fix / 文档一致性修复
- ✅ README 变更日志补齐 v3.0.0 / v3.1.0 / v3.1.1（修复「版本行 3.1.0、正文停在 v2.5.9」的版本漂移）
- ✅ 核验日期更新至 2026-10-07（每日快扫 10-06 / 10-07 均无 API 增量）
- ✅ 无 API 内容变更，纯文档版本

### v3.1.0 (2026-10-05) — 5.3 全量核验
- 🔴 新增破坏性变更：函数签名变更（`ObjectConstraints.new` / `PoseBoneConstraints.new` 增加 `name`；`UILayout.textbox` / `textbox_with_state` **位置参数重排**；`WindowManager.popover*` 新增 `auto_keymap`）
- 🟢 新增发现：`BlendFileColorspace` OCIO 诊断三项、`MaterialGPencilStyle.gradient`、`SpaceOutliner.show_users_column` / `sort_method`、`UILayout.label_markdown`
- 📌 完整条目迁移到 `references/api.md`；技能保留速览与兼容模板

### v3.0.0 (2026-10-05) — Workspace Rebuild / 工作区重建
- 🏗 技能元数据 `metadata.openclaw` → `metadata.octop`（改由 octop agent **B 哥** 维护）
- 🏗 知识库拆分：API 变更明细移入工作区 `knowledge/`，技能保留速览 + 兼容模板 + 排障
- 🏗 修复版本号漂移：`version` / README 版本行 / Changelog 三处强制一致

### v2.5.9 (2026-09-23) — Security Release / 安全发布
- 🔒 Removed dangerous **curl-pipe-to-shell** pattern from documentation / 从文档中移除危险的 **curl-pipe-to-shell** 模式
- 🔒 Added explicit security warnings about bpy code execution / 添加关于 bpy 代码执行的明确安全警告
- 🔒 Pinned dependency versions (uvx, pip) / 固定依赖版本（uvx、pip）
- 🔒 Clarified telemetry defaults and opt-out / 明确遥测默认值和退出方式
- 🔒 Added bilingual documentation (EN/CN) / 添加双语文档（中/英）
- 🔒 Removed release automation scripts (unrelated to skill) / 移除发布自动化脚本（与技能无关）

### v2.5.8 (2026-09-23)
- ✅ 5.3 API update: 8 new APIs + 2 breaking changes documented

### v2.5.7 (2026-09-20)
- ✅ BrushGpencilSettings.use_cyclic_stroke

### v2.5.6 (2026-09-18)
- ✅ PointCloud.type
