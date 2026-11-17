# Changelog

Version history of this skill. Current version is recorded in SKILL.md front matter.

## Changelog

### v3.7.3 (2026-11-12) — 基线口径切换：生产基准 5.2 LTS → **5.3**，5.2.4 转为兼容下限

- 🟢 **用户拍板（2026-11-12）**：「全面更新到 5.3 然后兼容 5.2」→ 技能内**所有版本口径**改为：**生产基准 = 5.3（5.3.0，2026-11-10 正式发布）**、**兼容下限 = 5.2 LTS（5.2.4）**。
- 📝 **改了 5 处**：`SKILL.md` 版本支持行 + API 兼容段；`references/api.md` 头部基线（en）+ 「5.3 Compatibility Notes」段（原写 Beta / 基准仍 5.2，已过期）+ 「5.2 LTS Compatibility Notes」标题与说明（原写 5.2 进 Beta 的 2026-06 日期）+ `README.md` 版本行 / 特性行 / Requirements / 版本支持表。
- ✅ **发布事实（2026-11-11 10:00 三件套全绿复扫）**：`download.blender.org/release/Blender5.3/` 200（8 个唯一包名，无 macOS Intel）、Gitea tag `v5.3.0` 200、`blender-5.3.0-windows-x64.msi` HEAD 200；同日 **5.2.4 / 4.5.16** 也正式发布。
- 📌 **MCP 生态零增量**（2026-11-12 逐字段核对）：`open_issues_count` 27（最新仍 #72）、open PR 5 全未合并（#68/#66/#48 `true`，#47/#43 `false`）、releases 6 条 / 最新 v1.0.3、stars 37 / forks 38 / watchers 13、`updated_at` 2026-09-29 → **本次是口径对齐版，不是新发现版**。
- ⚠️ **不改写历史**：v3.7.2 及更早条目里「以 5.2.3 LTS 为生产基准」的表述是**当时的正确结论**，保留不动。
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 本 Changelog = **3.7.3**

### v3.7.2 (2026-11-10) — `*_for_cli` 第三套根因：MCP add-on 抢 9876 + 非守护线程（官方 issue #72）

- 🟡 **新事实**（官方 issue **#72**，2026-11-09T19:01+01:00，`Nikola-Sinitsa`，0 评论）：`execute_blender_code_for_cli` 即使只跑 `result = {"ok": 1}` 也稳定报 **`Blender CLI timed out after 120s`**（Win11 / Blender 5.2.3 LTS / MCP extension 1.0.1，交互实例已在 9876 跑 server）。
- 🧪 **对照实验（报告者原文，可复现）**：`blender -b` 普通偏好 → 打印 OK 但**进程不退出**；`--factory-startup` → **≈1.8 s 正常**；`--factory-startup` + 约 55 个其他 add-on → **≈5 s 正常**；`--factory-startup` + **仅 MCP add-on** 且交互实例占 9876 → **挂住并打断交互实例连接** → 推断 **add-on 在 background 模式也起 server、端口冲突 + 留线程**。
- ⚠️ **别与既有三条混判**：#58/#60 = `run_blender_cli()` 未传 `stdin`（PR #48 未合并）；#69 = Microsoft Store 版 launcher 丢 stdout；**#72 = add-on 自身/端口冲突**。排障顺序应为「`--factory-startup` 对照 → 查 9876 占用 → 再怀疑 `stdin`」。
- 🛠 **排障表新增 1 行**（`references/troubleshooting.md`），给出可执行处置：先停交互 server / 临时禁 MCP add-on，或改用交互式 `execute_blender_code`，`*_for_cli` 无 `--factory-startup` 入口时自起 `blender -b --factory-startup --python`。
- 🔧 **同时修掉发布链缺陷（P1，挂了两轮）**：`generated/tools/publish_skill.py` 原先只推送 `VERSIONED_FILES`（SKILL.md / README.md），**`references/*.md` 从未上传**（远端 `contents/references` 一直 404）→ 改为按 `publish_files()` 全量推送，本次起 GitHub 仓库根目录才有 `references/`，v3.7.0 起 SKILL.md 里的 `references/*.md` 指引才算真正可用。
- 📌 **MCP 仓库快照**（2026-11-10 10:0x Gitea API）：`open_issues_count` **26 → 27（+1 = #72）**；open PR 仍 **5** 全未合并（#68 / #66 / #48 `true`，#47 / #43 `false`）；releases **6 条 / 最新 v1.0.3**；stars 37 / forks 38 / watchers 13 / `licenses` GPL-3.0 / `updated_at` 2026-09-29（官方主线仍停在 9 月）。
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 本 Changelog = **3.7.2**

### v3.7.1 (2026-11-07) — 分发渠道澄清：官方不上 PyPI（官方 issue #71）

- 🟢 **新事实**（官方 issue **#71**「Azure API Center package registry support」，2026-11-06，Jonah-John-Capitan）：企业要登记官方 MCP 时发现**官方 `lab/blender_mcp` 没有发布到 PyPI**，只有 **MCPB 扩展包（`releases/download/v1.0.3/mcp-1.0.3.zip`）** 与 **Git 源码（`mcp/blmcp/`）** 两条渠道；同时明确 **PyPI 上的 `blender-mcp` 是第三方/无关实现**（issue 原文 "the unrelated blender-mcp package currently available on PyPI"）。
- 🔴 **本文档此前的坑**：SKILL.md「别把两个版本号搞混」只说 `uvx`/`pip` 那半是「PyPI 包 `blender-mcp`」，**没说是第三方的** → 读文档的人会以为 `uvx blender-mcp==1.0.0` 装的也是官方实现，企业注册表 registry 名也会登记错。
- 🟢 **处置**：在该提示块下方新增「分发渠道」段 —— 官方只有 `.mcpb` 与 Git 源码；PyPI `blender-mcp` = 第三方（TCP 9876 桥接方式相同、代码基线不同）；企业注册表（Azure API Center 等）引用 **MCPB release URL**，别引用 PyPI 包名；要官方实现走 Option A/B。
- 📌 **MCP 仓库快照**（2026-11-07 10:0x Gitea API 实测）：open issues **25 → 26（+1 = #71）**；open PR 仍 **5**（#68 / #66 / #48 `mergeable: true` 未合并，#47 / #43 `false`）；releases **6 条 / 最新 v1.0.3**；stars 37 / forks 36 / watchers 13 / `licenses` GPL-3.0 / `updated_at` 2026-09-29
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 本 Changelog = **3.7.1**

### v3.7.0 (2026-10-29) — security-scan cleanup

- Removed downloaded-installer command chains. Installation now points at the publisher release page and asks the reader to review the file first.
- Split the long tool, protocol, troubleshooting, API, and history sections into `references/` so the main skill file stays small.
- Replaced workspace-only knowledge paths with files shipped in this package.
- Pinned every server launch example to an exact package version.

### v3.6.2 (2026-10-26) — 安全扫描口径修正（去 curl-pipe-shell 字面量）+ 体量超限定性

- 🔴 **新事实**：ClawHub 对已上线的 **v3.5.1** 重新扫描后把安全状态从 `Moderate CLEAN` 改成 **`suspicious`**（`clawhub skill verify` 实测：`decision: fail`、`security.status_not_clean`、skillspector `severity: CRITICAL` / `recommendation: DO_NOT_INSTALL`、`max_issue_severity: HIGH`，扫描时间 2026-10-23T02:37Z）。**这就是 3.6.0 / 3.6.1 两次提交都停在 pending、`latest` 仍为 3.5.1 的原因**（不是排队慢）。
- 🟢 **命中项 1（4×HIGH，可修）**：README / SKILL 的历史 Changelog 里留着 **curl-pipe-shell 的字面量**（描述「我们已移除它」的那句话）→ 扫描器按模式串匹配，不看上下文 → 本次全部改成 `curl-pipe-to-shell` 表述，**同一句话不再出现可执行片段**。
- 🟡 **命中项 2（6×HIGH，需产品决策）**：`SKILL.md (partial)` = **Incomplete referenced artifact analysis**，根因是 SKILL.md **~64 KB** 超扫描器单文件分析预算 → 只做了部分分析就计罚。彻底解法是把 SKILL.md 拆成 `SKILL.md`（主流程）+ `references/*.md`（排障表 / API 兼容 / 历史 Changelog），**属结构改造，另立任务**，本轮不动。
- 🟡 **命中项 3（1×MEDIUM）**：`uvx` 用法被指「未固定版本」→ **安装示例一律带 `@1.0.3`**（已有示例已固定，本轮把 Changelog 里的历史行也标注清楚）。
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.6.2**

### v3.6.1 (2026-10-25) — 「连不上」的最外层根因：uv 依赖下载被 TLS 证书拦截（官方 issue #67）

- 🟢 排障表新增一条：`Failed to download …` + **`invalid peer certificate: UnknownIssuer`**（`files.pythonhosted.org` 的 wheel）→ **uv 建不起 venv**，表现仍是 "MCP Blender: Server disconnected"。来源 = 官方 issue **#67**（2026-10-25，正文含完整 Claude Desktop 日志，`rpds-py` / `pydantic-core` / `pyyaml` 三个包均报同一错）。
- 🔴 **与 #56 / #65 严格分层**（三条同症状、不同层）：#56 / #65 = **进程启动**被 Windows SAC 拦签名；**#67 = 依赖下载**（更早一层）被 TLS 中间人拦证书。**命中 #67 时按 SAC 路径排查会白折腾**。
- 🟢 处置给了三条可执行路径：`UV_NATIVE_TLS=1`（uv 走系统信任库）/ `SSL_CERT_FILE=<ca.pem>`（企业根证书）/ 代理或杀软对该域名关掉 HTTPS 解密；修完用 `uvx blender-mcp==1.0.3` 复验依赖可下载。
- 📌 MCP 仓库快照（2026-10-25 10:00 API 实测）：open issues **22 → 23（+1 = #67）**；open PR 仍 **4**（#66 / #48 均 `mergeable: true` 未合并，#47 / #43 `mergeable: false`）；releases **6 条 / 最新 v1.0.3**；stars 33 / forks 33 / watchers 12 / `licenses` GPL-3.0；assets `blender-1.0.3.mcpb` 39531 / `mcp-1.0.3.zip` 344916（自然增长）。
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.6.1**（远端基线 v3.6.0；ClawHub 侧 3.6.0 扫描尚未放行，本次一并覆盖）

### v3.6.0 (2026-10-25) — 补「平台前提」：Intel Mac 上没有可用组合

- 🟢 **新增平台前提行**（`Version support` 下方）：官方 add-on 要求 **Blender ≥ 5.1**，而 **Blender 5.0 起 macOS 只出 Apple Silicon 构建**（Apple Silicon + macOS 13 Ventura 起；`4.5 LTS` 是最后一个支持 Intel Mac 的版本）→ **Intel Mac 上不存在「Blender 5.1+ × 官方 MCP」这个组合**，别让用户在 Intel Mac 上反复试。Windows / Linux 无此限制（Windows：4 核 SSE4.2 + OpenGL 4.3 或 Vulkan 1.3、8 GB RAM、2 GB VRAM）。来源：<https://www.blender.org/download/requirements/>（2026-10-25 核验）；据此同时在 `references/api.md` 补了「平台断代」一节（含 macOS arm64-only 对预编译二进制/轮子分发的三条影响）
- 📌 **MCP 生态零增量**（2026-10-25 Gitea API 实测，与 10-24 逐字段一致）：open issues **22**、open PR **4**（#66 / #48 / #47 / #43 均未合并）、releases **6 条 / 最新 v1.0.3（2026-09-11）**、stars **33** / forks **33** / watchers **12**、`licenses` **GPL-3.0**、`updated_at` 仍 **2026-09-29**；assets 下载数自然增长（`blender-1.0.3.mcpb` **39193** / `mcp-1.0.3.zip` **341649**）→ **排障表与工具坑清单无内容需改**
- 📌 **版本面**：5.2.3 LTS 仍是现行正式版（2026-10-22 发布、未被撤回）；5.3 Beta **"until November 4, 2026"**（RC 11-04 → 发布 11-10）；**5.4 Alpha 官方首次给结束日期 "until February 3, 2027"** → 5.4 的 API 仍不可依赖，本技能不回退也不前移基线
- ⚠️ SAC 单应用白名单**仍待核验**（#65 无新回复）
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.6.0**（远端基线 v3.5.1）

### v3.5.1 (2026-10-23) — 版本基准更正（5.2.3 LTS 已发布）+ 缩略图坑补根因

- 🔴 **事实更正**：`README.md` 版本行原写「`5.2.3` 仍是 RC 构建、已换 hash `c361aec8a863` 但**未发布**」→ **已过期**。实际 **5.2.3 与 4.5.15 均于 2026-10-22 正式发布**（三件套全绿：镜像包 `blender-5.2.3-*` / `.msi` HTTP 200 / Gitea tag `v5.2.3`；官网首页 "LATEST RELEASE … Released October 22, 2026"）。技能内版本口径统一改为 **5.2.x LTS（当前 5.2.3）**（共 3 处：`SKILL.md` 版本支持行 + 5.4 分段说明 + README 版本行/兼容表）
- 🟢 **缩略图坑补根因**（排障表）：`render_thumbnail_to_path` 交互模式全分辨率**不是参数没传**，而是**上下文管理器在 `INVOKE_DEFAULT` job 返回时就恢复设置**，job 实际执行时读到的是用户原设置；另 EEVEE 引擎标识需匹配 `BLENDER_EEVEE`。来源：**官方 PR #66**（2026-10-22，Victor-Solano，`mergeable: true`，+20/-8，**未合并**），作者实测 1920×1080/1.6MB/~9s → 320×180/50KB/0.8~1.3s（Win11 + 5.2.2 LTS + stdio）
- 🟢 **PR #48 拿到第三方复现**（未合并）：`execute_blender_code_for_cli` 在 main `dbbf836` 上 120s 超时 → 打补丁 **2.8s** 返回（2026-10-22 评论）→ 该坑的处置（`stdin=subprocess.DEVNULL` 本地补丁）继续有效
- 📌 MCP 仓库快照（2026-10-23 API 实测）：最新发布仍 **v1.0.3（2026-09-11，无 v1.0.4）**；落地页 add-on 链接 **可比基线第 14 次一致**；open issues **22 未变**；**open PR 3 → 4**（新增 #66）；stars **32 → 33**、forks **32 → 33**、`licenses` GPL-3.0（第 8 轮一致）
- ⚠️ SAC 单应用白名单**仍待核验**（#65 无新回复，`updated_at` 停在 10-19）
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.5.1**（远端基线 v3.5.0）

### v3.5.0 (2026-10-20) — 排障表 SAC 条目重写（旧建议被官方 issue 证伪）

- 🔴 **纠正一条会误导人的处置建议**：v3.3.0 起排障表写「Windows 上 `blender-mcp.exe` 被 Smart App Control 拦 → **改用官方 add-on 通道**」。**官方 issue #65（2026-10-19）证伪**：用户在**官方 MCPB 扩展**里同样被拦 —— 拦截对象是扩展自带 `.venv\Scripts\blender-mcp.exe`，`Get-AuthenticodeSignature` = `NotSigned`，Claude Desktop 报 "MCP Blender: Server disconnected"，Windows Code Integrity **event 3077**（与 #56 的 uv 安装路径同因）。
- 🟢 排障条目改为**机制 + 可执行判据**：SAC enforcement 只放行「应用智能服务识别」或「受信任 CA 签名」的二进制（Microsoft Learn 原文，2026-10-06 版）→ 未签名 launcher **必被拦**；处置改为「先验签名 → 把 SAC 决策交还用户（关闭属高风险，企业域策略不动）」。
- ⚠️ 留了 **待核验**：SAC 是否支持单应用白名单（本次未查到官方入口，不写死）。
- 📌 MCP 仓库快照（2026-10-20 API 实测）：最新发布仍 **v1.0.3（2026-09-11，无 v1.0.4）**；落地页 add-on 链接 **`mcp-1.0.3.zip` 可比基线连续 11 次一致**；open issues **21 → 22**（新增 #65）；open PR **#48 / #47 / #43 仍全部未合并**；stars **28 → 30**、forks 31、`licenses` = GPL-3.0（第 5 轮一致）
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.5.0**；**已双平台发布（2026-10-20 13:21）**：GitHub `taosiuman/blender-skill` tag `v3.5.0` ＋ ClawHub `@taosiuman/blender-mcp` latest=**3.5.0**

### v3.4.0 (2026-10-16) — 2 条新官方 issue 工具行为坑（每日快扫）
- 🟢 排障表新增 **2 条官方 issue 可溯源的工具行为坑**：
  - **issue #63**：Windows 上 `SO_REUSEADDR` 让**第二个 Blender 实例静默绑定已占用端口** → 服务按钮显示"已启动"但客户端始终连第一个实例（表现：操作落到别的窗口 / 改了没反应）。创建者实测 **20/20 复现**（Win11 + Blender 5.2.2 LTS + blender_mcp 1.0.2），建议官方改用 `SO_EXCLUSIVEADDRUSE` → 技能给处置：**只开一个实例** / 先关旧实例 / `netstat -ano | findstr 9876` 查占用
  - **issue #64**：`execute_blender_code` 的 `result` **必须为 dict**；官方 `prompts.yml` L48 声称可返回 "dicts, lists" 属**文案与实现不一致**（报错原文 `The result variable must be a dict, not list. Wrap your return value: result = {"key": value}`）→ 技能给处置：**一律包成 dict**
- 📌 MCP 仓库快照：最新发布仍 **v1.0.3（2026-09-11，无 v1.0.4）**；落地页 add-on 链接**可比基线连续 8 次一致**；Open issues **18 → 21**；Open PR **#48 / #47 / #43 仍全部未合并**
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.4.0**；**已双平台发布（2026-10-16 10:41）**：GitHub `taosiuman/blender-skill` tag/Release **v3.4.0**（= Latest）＋ ClawHub `@taosiuman/blender-mcp` **latest=3.4.0**（安全扫描 Moderate CLEAN）→ 三方一致

### v3.3.0 (2026-10-13) — 官方 issue/PR 实证取证 + 工具行为排障补强（每日快扫）
- 🟢 **取证渠道修复**：`projects.blender.org` 的 HTML 页面长期 403，改走 **Gitea REST API**（`/api/v1/repos/lab/blender_mcp/{releases,issues,pulls}`）→ **issue/PR 状态首次拿到官方实证**（此前 10 天只能写"未能核查"）
- 🟢 **add-on 版本核实**：最新发布仍是 **v1.0.3（2026-09-11）**，无 v1.0.4（官方 releases API + 落地页双向印证）；Open PR = **#48 / #47 / #43**（均未合并）
- 🟢 排障表新增 **7 条官方 issue 可溯源的工具行为坑**：`*_for_cli` Windows stdio 挂死（#58/#60，PR #48）｜`execute_blender_code` 每次新命名空间（#55）｜`get_objects_summary` 上下文爆炸（#54）｜缩略图分辨率与临时目录语义（#46/#61/#53）｜`get_python_api_docs` 需重复类名（#62）｜macOS `.mcpb` 安装失败（#57）｜Windows SAC 拦截（#56）
- ⚠️ **更正**：作废追踪表中不存在的 **#344 / #345 / #348**（官方 API 实测 404）；新增"不得用搜索摘要代替官方源"的取证规则
- 📌 API 侧同步：change_log 本轮 8 条新条目中 7 条实际 5.3 生效（项目系统 + UILayout 模板，见 `api-changes-5.3.md` §7）、1 条 5.4 独有（`Mesh.use_radial_symmetry`，见 §3.6）—— **均不触及 MCP 执行路径**，MCP 侧无兼容性改动
- ✅ 三处版本号一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog = **3.3.0**；**双平台发布仍待用户确认**（v3.2.0 未发布 → 本次发布一并覆盖两版变更）

### v3.2.0 (2026-10-11) — 5.3 Beta 口径 + 官方安装链接 + 排障补强（周度整合）
- 🟢 5.3 兼容章节标题由「dev — 前瞻」改为「**Beta — API 已稳定**」，并写明 **RC 2026-11-04 → 发布 2026-11-10**（官方 release notes 首页原文）
- 🟢 安装步骤改用官方 **add-on v1.0.3** 链接（原写 v1.0.0 已过期），补 **Blender ≥ 5.1** 硬性要求与「拖拽要拖两次」说明
- 🟢 排障表新增 4 条高频真实坑：**Auto Start 只在启动时触发** / **两个 MCP add-on 抢 9876 端口** / **Allow Online Access** / **拖拽安装要拖两次**
- 📌 同步两条 5.3 生效的 API 变更口径（`use_collection_importer` 移除、资产库进度回调 3 参数）—— 官方已于 2026-10-11 把它们补登进 `/api/5.3/` 章节
- ✅ 版本号三处一致：`SKILL.md` frontmatter / README 版本行 / 两处 Changelog 均为 **3.2.0**；**双平台发布待用户确认**

### v3.1.1 (2026-10-08) — 文档一致性修复
- ✅ README 变更日志补齐 v3.0.0 / v3.1.0 / v3.1.1（修复「版本行 3.1.0、正文停在 v2.5.9」的版本漂移）
- ✅ 核验日期更新至 2026-10-07（每日快扫 10-06 / 10-07 均无 API 增量）
- ✅ 无 API 内容变更，纯文档版本

### v3.1.0 (2026-10-05) — 5.3 全量核验
- 🔴 新增破坏性变更：函数签名变更（`ObjectConstraints.new`/`PoseBoneConstraints.new` 增加 `name`；`UILayout.textbox`/`textbox_with_state` **位置参数重排**；`WindowManager.popover*` 新增 `auto_keymap`）
- 🟢 新增发现：`BlendFileColorspace` OCIO 诊断三项、`MaterialGPencilStyle.gradient`、`SpaceOutliner.show_users_column`/`sort_method`、`UILayout.label_markdown`
- 📌 完整条目迁移到 `references/api.md`；本文件保留速览与兼容模板

### v3.0.0 (2026-10-05) — Workspace Rebuild
- 迁移到 octop 工作区：知识库拆到 `references/`（research-tracker、auto-publish-workflow）
- 移除 openclaw 专用安装元数据，改为 octop 技能元数据
- 研究追踪与发布流程改由 `blender-autolearn` 技能 + 定时任务驱动

### v2.5.9 (2026-09-23) — Security Release
- 🔒 Removed the dangerous **curl-pipe-to-shell** install pattern from installation docs
- 🔒 Added bilingual security warnings (EN/CN) about bpy code execution risks
- 🔒 Pinned dependency versions: `uvx blender-mcp==1.0.0`, `pip install mcp==1.8.0 pyyaml==6.0.2 starlette==0.45.0`
- 🔒 Clarified telemetry defaults and opt-out mechanism
- 🔒 Added bilingual documentation throughout (EN/CN)
- 🔒 Removed publish scripts from skill directory (unrelated to skill functionality)

### v2.5.8 (2026-09-23)
- ✅ 5.3 Alpha API 增量更新 (09-23): 基于官方 change_log 第七次扫描
- ✅ 新增 CollectionChild.sort_index: 集合子对象排序索引
- ✅ 新增 CollectionObject.sort_index: 集合对象排序索引
- ✅ 新增 CollectionObject.parented_sort_index: 集合对象父级排序索引
- ✅ 新增 ColorManagedInputColorspaceSettings.interop_id: 输入色彩空间互操作ID
- ✅ 新增 ColorManagedSequencerColorspaceSettings.interop_id: 序列编辑器色彩空间互操作ID
- ✅ 新增 CompositorNodeConvertColorSpace.from_interop_id: 色彩空间转换节点源互操作ID
- ✅ 新增 CompositorNodeConvertColorSpace.to_interop_id: 色彩空间转换节点目标互操作ID
- ✅ 新增 SpaceOutliner.sort_method: 大纲排序方法
- ✅ 补充破坏性变更: SpaceOutliner 的 use_sort_alpha 重命名为 10 个 use_filter_* 属性
- ✅ 补充破坏性变更: UserAssetLibrary 的 path 重命名为 auth_token/invalid_uuid/uuid
- ✅ 总计: 8 项新增 API + 2 项重要重命名文档补充 (集合排序/色彩空间互操作/大纲排序)

### v2.5.7 (2026-09-20)
- ✅ 5.3 Alpha API 增量更新 (09-20): 基于官方 change_log 第六次扫描
- ✅ 新增 BrushGpencilSettings.use_cyclic_stroke: Grease Pencil 循环笔触设置
- ✅ 总计: 1 项新增 API (GP 笔刷增强，无破坏性变更)

### v2.5.6 (2026-09-18)
- ✅ 5.3 Alpha API 增量更新 (09-18): 基于官方 change_log 第五次扫描
- ✅ 新增 PointCloud.type: 点云类型属性
- ✅ 总计: 1 项新增 API (点云数据增强，无破坏性变更)

### v2.5.5 (2026-09-16)
- ✅ 5.3 Alpha API 增量更新 (09-16): 基于官方 change_log 第四次扫描
- ✅ 新增 RenderEngine.bl_write_viewport_depth: 自定义渲染引擎写入视口深度缓冲
- ✅ 新增 FileHandler.label_with_extensions: 文件处理器显示带扩展名的标签
- ✅ 新增 UILayout.label_markdown: UI 布局中渲染 Markdown 格式文本
- ✅ 总计: 3 项新增 API (均为渲染/文件处理/UI 增强，无破坏性变更)

### v2.5.4 (2026-09-11)
- ✅ 5.3 Alpha API 增量更新 (09-11): 基于官方 change_log 三次扫描
- ✅ 新增 CyclesPreferences.has_dlss_gpu_devices: DLSS GPU 设备检测
- ✅ 新增 CyclesRenderSettings.preview_denoising_upscale_quality: 预览降噪升级质量
- ✅ 新增 RegionView3D.use_view_flip_x: 视口水平翻转
- ✅ 新增 SpaceNodeOverlay.show_text_info: 节点叠加层文本信息显示
- ✅ 总计: 4 项新增 API (均为渲染/视口/节点 UI 增强，无破坏性变更)

### v2.5.3 (2026-09-10)
- ✅ 5.3 Alpha API 增量更新 (09-10): 基于官方 change_log 二次扫描
- ✅ 新增 WindowManager.undo_stack: 编程访问撤销栈
- ✅ 新增 UILayout.property_split_factor: 属性分割系数控制
- ✅ WindowManager.invoke_popup 参数变更: 新增 `auto_keymap` 参数
- ✅ WindowManager.popover 参数变更: 新增 `auto_keymap` 参数
- ✅ WindowManager.popover_begin__internal 参数变更: 新增 `auto_keymap` 参数
- ✅ 总计: 5 项新增/变更 API (均为 UI/窗口管理增强，无破坏性变更)

### v2.5.2 (2026-09-10)
- ✅ 版本号同步至 2.5.2（与 GitHub/ClawHub 对齐）

### v2.5.1 (2026-09-09)
- ✅ 5.3 Alpha API 增量更新 (09-09): 基于官方 change_log 扫描
- ✅ 新增 Cycles 元数据属性: BatchRenameAction.name, CyclesCurveRenderSettings.name, CyclesCustomCameraSettings.name, CyclesLightSettings.name, CyclesMaterialSettings.name, CyclesMeshSettings.name, CyclesObjectSettings.name, CyclesRenderLayerSettings.name, CyclesRenderSettings.name, CyclesView3DShadingSettings.name, CyclesVisibilitySettings.name, CyclesWorldSettings.name
- ✅ 新增 GLTF2_filter_action.name
- ✅ 新增 NodeSetting.name
- ✅ 新增 Paint 可视化曲线: Paint.show_auto_smooth_curve, Paint.show_hardness_curve, Paint.show_spacing_curve
- ✅ 新增 CompositorStrip.properties
- ✅ 新增 SequencerTimelineOverlay.show_thumbnails
- ✅ 总计: 18 项新增 API (均为小功能增强，无破坏性变更)

### v2.5.0 (2026-09-08)
- ✅ 跟踪 blender-mcp 社区 PR（3 项重要改进，均为 OPEN 状态）：
  - 🔴 **PR #348**: Server instructions 机制 - 通过 `FastMCP(instructions=...)` 传递代码正确性指南
    - 解决 #26（本地化 UI 中 `nodes["Principled BSDF"]` 返回 None）
    - 解决 #110（渲染引擎标识符在版本间不一致）
    - 使用 `n.type == "BSDF_PRINCIPLED"` 而非节点名称（跨语言兼容）
    - 使用 `try/except TypeError` 获取动态枚举的完整值列表
  - 🟡 **PR #344**: `export_scene` 命令 - 场景导出为第一类工具
    - 支持 GLB/FBX 格式导出到自定义路径
    - 参数：`filepath`, `format="glb"`, `object_names=None`, `selection_only=False`, `apply_modifiers=True`
    - 自动处理选择、修改器烘焙、GLB 标志位
    - 返回：`{path, bytes, selection_only, exported: [...]}`
  - 🟡 **PR #345**: 插件自动启动改进 - 延迟启动 + 重试机制
    - 使用 Blender 持久化定时器延迟启动（避免冷启动时序问题）
    - 等待场景存在后使用配置的端口
    - 启动失败后自动重试
    - 文件加载后重新调度
    - 手动断开不会被后续文件加载覆盖
- ✅ Blender API 无新变更（change_log 与 2026-09-07 一致）

### v2.4.0 (2026-09-07)
- ✅ 5.3 Alpha 完整扫描 (09-07): 基于官方 change_log.html 全量核实
- 🔴 新增破坏性变更: `NodesModifier.panels` 移除（Geo Nodes 插件关键影响！）
- 🔴 Theme API 移除: `ThemeFileBrowser.selected_file`, `ThemeSpaceGeneric/Gradient.header_text/header_text_hi/title`
- ✅ Brush 重命名修正: `use_inverse_smooth_pressure` → `use_smooth_pressure`（非反向）
- ✅ 新增 Project API: `BlendData.project/project_init/project_clear` + `Preferences.use_project_auto_save`
- ✅ 新增渲染暂停/恢复: `RenderEngine.view_pause/view_resume`, `RegionView3D.pause_render`
- ✅ 新增场景合成效果: `Scene.compositor_effects`, `CompositorNodeTree.allow_usage_in_scene_compositor_effect`
- ✅ 新增 ID.deep_hash: 数据块内容哈希
- ✅ 新增 Outliner 11 项细粒度过滤器
- ✅ 新增 UILayout 合成模板: `template_compositor_strip_inputs`, `template_scene_compositor_effects`
- ✅ 新增 Asset Library 认证: `UserAssetLibrary.auth_token/use_auth_token/uuid`
- ✅ 新增 Brush 曲线/统一属性: `curve_auto_smooth/curve_hardness/curve_spacing/use_unified_color/use_unified_size`
- ✅ 新增旋转模式转换: `Object/PoseBone.convert_rotation_mode()`
- ✅ 新增 EEVEE 降噪: `ViewLayerEEVEE.denoising_store_passes`
- ✅ 新增 VSE 偏好设置: `PreferencesEdit.clamp_strips_by_default/default_strip_length`
- ✅ 新增 RT Shadows: `PreferencesSystem.use_rt_shadows`
- ✅ 新增 Collection Import: `Collection.importer`, `CollectionImport.filepath`
- ✅ 总计: Python API 50+ 项新增 + 6 项移除 + 5 项重命名

### v2.3.0 (2026-09-06)
- ✅ 5.3 Alpha 扫描更新 (09-06): Python API 6 项新增 + Geo Nodes 13 项新增 + GPU 兼容性变更
- ✅ 新增 `NodeTreeInterface.root_panel`, `UILayout.label_multiline()`, `WindowManager.try_activate_rna_button()`
- ✅ 新增 `mathutils.KDTree` 2D 树支持 + `bpy.data.all_ids` 顺序变更警告
- ✅ 新增 Geo Nodes: Combine List, Get Vector Component, Rasterize Points, Deactivate Voxels, Grid Topology Boolean, NURBS input nodes, Curve to Mesh/Tube Miter Scale, Realize Instances Preserve Normals, GP data input nodes
- ✅ 新增 GPU 兼容性变更: `gpu.types.GPUBatch.draw_instanced` 行为变更 (commit 6f64632716)

### v2.2.0 (2026-09-04)
- ✅ Added Geometry Nodes MCP integration section with debugging examples
- ✅ Documented Auto Start feature for addon preferences
- ✅ Added uvx quick installation method
- ✅ Added DISABLE_TELEMETRY environment variable
- ✅ Added Gemini CLI integration guide
- ✅ Enhanced Quick Start Checklist with new options

### v2.1.0 (Previous)
- Blender 5.2 LTS Beta API compatibility notes
- 12 breaking changes documented
- 66 new APIs catalogued
lender 5.2 LTS Beta API compatibility notes
- 12 breaking changes documented
- 66 new APIs catalogued
