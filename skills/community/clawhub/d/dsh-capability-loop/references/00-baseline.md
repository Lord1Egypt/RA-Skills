# 00 · 环境事实基线（Baseline）

> 用途：开工前核对，避免拿上周的结论当今天的事实。
> 源环境快照：**2026-11-12**，DSH `0.2.1-rc.5`、Node `22.23.4`、Windows x64、provider `dxxc-token-hub` / `deepseek-v4.1-flash-1017`（1M 上下文）。
> 复核命令：`scripts/capability-audit.ps1`（只读，自动覆盖下表大部分项）。

## 1. 路径与运行时

| 项 | 源环境值 | 复核方式 |
|---|---|---|
| `DSH_HOME` | `%USERPROFILE%\.dsh`（默认 `%USERPROFILE%\.dsh`） | `$env:DSH_HOME` / 目录存在性 |
| Profile | `%USERPROFILE%\.dsh\profiles\web`（配置在 `cordis.patch.yml` + `package.json`） | 读文件 |
| Skills（活动） | `%USERPROFILE%\.dsh\skills\<name>\SKILL.md`，**只扫一层目录** | 目录计数 |
| Skills（停用） | `%USERPROFILE%\.dsh\skills-disabled\`（同结构，不被加载） | 目录计数 |
| 角色 prompt | `%USERPROFILE%\.dsh\agents\*.md`（spawn 时手工粘进 prompt；子代理不会自动读） | 文件列表 |
| 桌面壳 | `D:\DeepSeek Harness\resources\app\src\main.js`（Electron 主进程，**升级会覆盖**） | 文件存在 + 锚点 |
| DSH CLI | `D:\DeepSeek Harness\resources\app\dsh-local\node_modules\@deepseek-ai\dsh\lib\bin.js` | 运行 `--version` |
| 会话存储 | `%USERPROFILE%\.dsh\sessions\<cwd-hash>\<id>\session.v4.jsonl.zstd`（多帧 zstd，需逐帧解压） | 目录统计 |
| 会话索引 | `%USERPROFILE%\.dsh\session-index.sqlite`（+`-wal`/`-shm`） | 文件大小/时间 |
| 桌面日志 | `%APPDATA%\DeepSeek Harness\desktop.log` / `error.log` | 读尾部 |
| Trae（CN 3.4.x） | `D:\Trae CN`；CLI `D:\Trae CN\bin\trae-cn.cmd`；**当前打开工程**：`%APPDATA%\Trae CN\User\globalStorage\storage.json` → `windowsState.lastActiveWindow.folder`（file URI）；近期工程见 `backupWorkspaces.folders` 与 `User\workspaceStorage\*\workspace.json` | `trae-status.ps1` 只读比对 |
| 技能市场数据 | `%USERPROFILE%\.dsh\storages\@montersy123\dsh-skill-market\data\{panel.json,installed.json}`；安装目录 `<handle>--<slug>`；`origin=market/manual` | `skill-status.ps1` 读记录 |
| 浏览器（视觉 QA） | `C:\Program Files\Google\Chrome\Application\chrome.exe`；`workspace-write` 下 agent-browser 因 crashpad 被拒；`danger-full-access` 下 Chrome headless `--screenshot` 可出图（2026-11-13 实测）；agent-browser `open` 会挂起，需后台+超时 | 截图 + 像素抽查 |

**PowerShell 事实（既定，不再探测/不再提醒）**：本机只有 **Windows PowerShell 5.1**，DSH 的 `pwsh` 工具/持久终端会自动兜底到 5.1。脚本按 5.1 语法写；需要 PS7 专属能力时只写「未实测 + 补测路径」。

## 2. 关键配置锚点（源环境实测值）

`cordis.patch.yml`（约 160 行，行号会随改动漂移，**按内容匹配，不按行号**）：

```yaml
- id: optional-session-query-sqlite
  config:
    path: !!js dshHomePath('session-index.sqlite')   # 持久化，非 :memory:
    openAt: first-search                               # 不拖慢启动，首次搜索建库
    journalMode: wal
- id: optional-tool-session-query
  config:
    searchTimeoutMs: 600000                            # 首次建库保护（稳定后可回默认 30s）
```

- 已移除：`dsh-token-insights`（patch 插入段 + disabled 行 + pnpm 包 + storage 四处一起清，顺序不能反）；`dshmarket`（自重启抢 3080，是 `EADDRINUSE` 的直接来源）。
- 保留：`@montersy123/dsh-skill-market`（技能市场）；`dsh-cost-meter`、`dsh-context`、`dsh-video-skin`、`modlens`；官方 plugin-market 保留但 `indexes: []` 为空壳。

`main.js` 健康检查锚点（补丁版源环境实测值）：

| 常量/函数 | 旧版（未打补丁） | 补丁版 |
|---|---|---|
| `HEALTH_PROBE_TIMEOUT` | 8000 | **12000** |
| 探活间隔 | 5000 | **8000** |
| `HEALTH_FAILURE_LIMIT` | 3 | **6** |
| `HEALTH_DOWN_WINDOW_MS` | 无（≈23s 即 kill） | **60000**（连续失败 ≥60s 才 kill） |
| 忙判定 | 无 | `isTcpAccepting(port)`：端口可 accept 视为「服务器忙」，只告警 |
| kill 前复核 | 无 | 复核 5s，已恢复则取消重启 |
| 崩溃退避 | 无 | `CRASH_RESTART_BACKOFF_MS = 3000` |
| 服务器 stderr | 无 | 尾部落 `desktop.log` |

判定「补丁是否在位」= 上述锚点存在且值匹配；**哈希不匹配不要强刷**（DSH 升级后 main.js 变了，按 diff 重做补丁，见 `20-runtime-fix.md`）。

## 3. 能力资产地图（工作区）

| 资产 | 位置 | 作用 |
|---|---|---|
| 协作契约 | `<ws>/AGENTS.md` | 自动加载的 workspace instructions：角色/评审门/自动路由/门禁 |
| 记忆落盘 | `<ws>/memory/{rules,team-learnings,design-learnings,decisions}.md` | 能力累积闭环；rules ≤60 条 |
| 需求规范 | `<ws>/standards/` | SRS 标准/模板、L0 入口、迁移指南、系统证据驱动、旅程/缺口/通关 |
| 系统事实采集 | `<ws>/tools/system-facts/extract-frontend.mjs` | 从源码 AST 生成菜单树/接口清单/ mock 缺口 |
| 文档总览构建 | `<ws>/tools/build-docs-html.py` | Markdown → 单文件 HTML（搜索/目录/双主题/打印） |
| 升级包 | `<ws>/upgrade/{config,shell,design,team,tools,backup}` | apply/rollback/verify + 门禁脚本 |
| 门禁脚本 | `upgrade/team/{gate-check,requirement-doc-check,test-traceability}.ps1`、`upgrade/post-restart-check.ps1` | 设计/需求/测试/环境四类验收 |
| 示例项目 | `<ws>/projects/<模块>/` | README-需求入口 + SRS + 事实 + 旅程 + 缺口 + 规则 + 用例 + HTML |
| 交接方法 | skill `feature-handoff` + `<ws>/tools/trae-handoff/` | DSH↔Trae 四件套与四脚本 |
| 能力闭环 | `~/.dsh/skills/dsh-capability-loop/`（源 `<ws>/tools/capability-loop/`） | 七阶段闭环、九组体检、聚合门禁、产品/设计上下文、grill、更新提示；快照 `<ws>/.tmp/capability-loop/audit-state.json` |
| 迁移交付 | `<ws>/handover/` + `<ws>/dist/*.zip` | 01–07 文档、install 变体、CHANGELOG/LICENSE |

## 4. 版本差异与降级

- **同事环境路径/端口/模型/DSH 版本不同**：脚本一律用参数（`-DshHome/-Workspace/-AppSrc`），不要硬编码源路径。
- **没有 `dsh-version-panel` 本地包**：用 `handover/install/` 的 colleague 变体（移除 file: 依赖与 patch 插入段）再 apply。
- **完全离线**：`apply.ps1 -Scheme B -SkipPnpm`，手工删掉不用的依赖与 bundle 行（保留 base/web-app 即可启动）。
- **桌面壳版本已升级**：`main.js` 哈希/锚点不匹配 → 跳过补丁（记录「未实测」），按 diff 重做后再施加，绝不强制覆盖。
- **本 skill 自身**：版本看 `version.json`，差异看 `CHANGELOG.md`；对方修改不回传、不合并。
