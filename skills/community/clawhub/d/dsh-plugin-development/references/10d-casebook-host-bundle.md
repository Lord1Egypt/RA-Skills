# D 方向分册 · 宿主 / 桌面 / 组合 bundle / 工程规范化

> **文件来源**：本文件由 `10-community-casebook.md` 拆分而来，正文为原文的**逐行搬迁**，未做改写。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。总索引见 `10-community-casebook.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

---

<!-- ↓ 源：D-host-bundle.md （全文） -->

# D. 宿主 / 桌面 / 组合 bundle / 工程规范化 —— 踩坑记录 + 可抄模板（原始素材）

> 调研对象（4 个仓库，源码快照 + git 历史均已在本地）：
> - `Q00_ouroboros` —— `dsh-ouroboros`（约 5800★），官方清单里唯一「纯配置、零代码」组合包
> - `anywhere-labs_dsh-desktop` —— `dsh-plugin-desktop`（约 25000★），桌面宿主插件
> - `xiaobright_dsh-anchored-standard` —— 126 文件的 preset 包（工程规范化方向）
> - `omdsh-dev_DSH-better-sidebar` —— 644 commits 的「可被第三方注册新页面」侧边栏底座
>
> 源码根（生成期，**不随本 skill 发布**）：`<社区仓库快照>/src/<仓库>/`
> git 根（生成期）：`<社区仓库快照>/repos/<仓库>/`
> 官方 DSH 源码（用于交叉验证机制）：`<DSH 检出>/`
>
> 规则：代码**逐字照抄**，超长标 `…(略)`；每个结论标注 `仓库 + 文件路径` 或 `仓库 + commit`；查不到写「未找到」，绝不编造。

---

## 0. 先给结论：本方向的「一句话真相」

| 真相 | 证据 |
|---|---|
| **组合包 = 一个 package.json + 一个 cordis.patch.yml + 一个 README，可以零行 JS 代码。** | `Q00_ouroboros/integrations/dsh-plugin/` 只有 3 个文件（`package.json` / `cordis.patch.yml` / `README.md`） |
| `package.json` 里声明 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`，profile 合成器就认。 | 官方 `packages/boot/app-boot/src/profile.ts:693-695`：`const bundle = bundleManifest.dsh?.bundle`；`if (bundle === undefined) throw ... declares no dsh.bundle` |
| patch 的相对路径 `name: ./xxx.mjs` **确实被锚到 patch 文件旁边**（官方文档口吻是「绝对路径」，源码实现允许相对）。 | 官方 `packages/boot/app-boot/src/index.ts` `anchorInsertedPluginNames()`：`const base = dirname(resolve(file))` → `entry.name = pathToFileURL(resolve(base, entry.name)).href` |
| `!!js` 由 Loader 针对每个 entry 的注入就绪 context 求值，因此 `!!js` 里能读到 `process.env`、`ctx.loader.entries()`。 | 官方 `packages/boot/app-boot/src/index.ts:218-223` 注释：`!!js` scalars become expression nodes the Loader interpolates against each entry's injection-ready context |
| 行顺序**不**决定加载顺序（激活由服务可用性驱动）；但**同一 patch 内 `!!js` 表达式的可见性**是「只看得见它之前的行」。 | `omdsh-dev_DSH-better-sidebar/cordis.patch.yml` 注释原文：`The loader evaluates it when this row is processed (entry-list order, only rows before this one are visible)` |
| 安装命令 `--profile` **必填**，省略直接报错。 | 官方 `apps/cli/src/args.ts:192` `.requiredOption('--profile <name>', ...)`；`Q00_ouroboros` commit `5258cb19` 原文：「`apps/cli/src/args.ts` declares `.requiredOption('--profile <name>')` on `dsh plugin`, so the root README's command errored out instead of installing」 |

---

# D · 一、踩坑记录（现象 → 根因 → 怎么修）

> 标注格式：`仓库 + commit 短哈希 + 提交信息原文`。凡提交 body 为空（只有标题）的，写明「body 为空」，不编造细节。

## 1. `Q00_ouroboros`（dsh-ouroboros）

### 坑 1.1　`dsh plugin add` 命令少了 `--profile` —— 照 README 抄会直接报错
- **仓库 + commit**：`Q00_ouroboros` + `5258cb19`（2026-08-17）
- **提交信息原文**：
  > `feat(integrations): add installable dsh plugin for Ouroboros (#2158)`
  > 正文：「**Install syntax.** `apps/cli/src/args.ts` declares `.requiredOption('--profile <name>')` on `dsh plugin`, so the root README's command errored out instead of installing. It now matches the bundle README and the verified command.」
- **现象**：照主 README 抄 `dsh plugin add ...`（漏 `--profile`），CLI 不安装，直接报 requires `--profile`。
- **根因**：`dsh plugin` 子命令声明了 `.requiredOption('--profile <name>')`，`--profile` 是强制项（源码 `apps/cli/src/args.ts:192` 佐证）。
- **修复**：所有安装命令补 `--profile <名字>`：``dsh plugin --profile <your-profile> add "github:Q00/ouroboros#main&path:integrations/dsh-plugin"``。

### 坑 1.2　凭据默认不会流进子进程（`/KEY|PASSWORD|SECRET|TOKEN/i` 被洗掉）
- **仓库 + commit**：`Q00_ouroboros` + `5258cb19`（同一条提交，review round 1 第 2 点）
- **提交信息原文（截断）**：
  > 「**Credential scrub.** `@deepseek-ai/dsh-subprocess` exports `SENSITIVE_ENV_PATTERN = /KEY|PASSWORD|SECRET|TOKEN/i` and …」
- **现象**：插件 `mcp-ouroboros` 行不给 `env` 时，被拉起的 `ouroboros mcp serve` 拿不到 `ANTHROPIC_API_KEY` / `DEEPSEEK_API_KEY`；工具能列出，第一次调用失败。
- **根因**：`@deepseek-ai/dsh-subprocess` 会把所有「凭据形状」的名字（`/KEY|PASSWORD|SECRET|TOKEN/i`）以及所有 `DSH_*` 名字从子进程环境里洗掉，「按设计不让 harness 凭据隐式泄漏」。
- **修复**：在插件行的 `config.env` 里**显式列白名单**（插件显式 env 层在 scrub **之后**合并）。参见模板 §二.1 的 `env:` 段。
- **同源踩坑**：**profile 里覆盖某行时，是整块替换该行的 `config`，不是深合并**。`Q00_ouroboros/docs/guides/deepseek-harness.md:66-70` 原文：「A later patch layer **replaces** a row's entire `config` rather than deep-merging it, so copy the bundle's `config` block and add your line to it.」→ 想加一个环境变量，必须把整段 `config` 抄过去再改，否则 timeout/args 全丢。

### 坑 1.3　「一条变量」其实不是一条变量：`dsh` LLM backend 需要绝对 composition 路径
- **仓库 + commit**：`Q00_ouroboros` + `9d58f4ab`（2026-08-17）；`a8f3cf89`（2026-08-20）
- **提交信息原文（`9d58f4ab`，截断）**：
  > 「dsh scrubs credential-shaped names (`/KEY|PASSWORD|SECRET|TOKEN/i`) from children by design and the explicit `env` layer merges after that scrub; a profile override replaces a row's whole `config` rather than deep-merging it; **a composition's plugin names resolve relative to the composition file's own directory**; and both `OUROBOROS_DSH_*` variables are on the project `.env` denylist…」
- **提交信息原文（`a8f3cf89`）**：
  > `fix(mcp): serve with an installed CLI when the SDK runtime is only inherited (#2164)`
  > 现象原文：`The MCP server cannot host the 'claude' SDK runtime in this process ...`（重复 3 次、0 个 Ouroboros 工具）
- **现象**：设了 `OUROBOROS_LLM_BACKEND=dsh`，第一次 interview/Seed/QA 调用失败，报 `invalid_config`；或机器继承 `runtime_backend: claude` 时反复报「cannot host the 'claude' SDK runtime」，且因为 `failOnStartupError: false`，dsh 照常启动、工具「静默消失」，错误看起来像噪音。
- **根因**：① `dsh` backend 会另起一个 `dsh-acp-demo` 子进程（不复用你正在聊的 dsh），它**必须**拿到一个 composition 文件才能加载，否则 fail closed；相对路径会被拒（会相对不可信的项目 cwd 解析）。② 被继承的 `claude` SDK runtime 无法在 MCP server 进程内托管。
- **修复**：① `OUROBOROS_DSH_CONFIG_PATH` 必须是**绝对路径**，且文件所在目录要能解析到 dsh 的 `node_modules`/workspace（composition 内的包名相对 composition 文件所在目录解析）。② 用可执行 runtime（`claude-cli` / `codex` / `opencode`，`a8f3cf89` 的偏好顺序是 `claude-cli` → `codex` → `opencode`），**但显式选择仍 fail**（`--runtime claude` 不替换）。
- **可抄教训**：`failOnStartupError: false` 让插件「静默消失」= 把错误变成噪音，新手会以为插件没生效。官方在 `cordis.patch.yml` 注释里明说：「Recovery is not guaranteed to be automatic … After fixing the cause, reload the plugin or restart dsh.」

### 坑 1.4　安装器自动装插件时的 profile 选择（无全局安装这回事）
- **仓库 + commit**：`Q00_ouroboros` + `3c8643f6`（2026-08-18）、`235487bb`（2026-08-18）
- **提交信息原文（`3c8643f6`，截断）**：
  > 「dsh keeps plugins per profile and `dsh plugin` requires `--profile`, so there is no global install to run. The installer therefore picks its targets: **`web`** … **Any other profile whose `package.json` already carries `dsh-ouroboros`** … **Nothing else.** Adding Ouroboros tools to someone's unrelated profile because an installer ran is not an upgrade.」
- **现象 / 根因**：**没有全局安装**；插件是「每个 profile 各装一份」。安装器若随便挑 profile，可能污染用户无关的 profile。
- **修复**：默认只装 `web`（`dsh web` 会脚手架出来的那个）；对已有 `dsh-ouroboros` 的 profile 才刷新。
- **平台相关**：`235487bb` 标题 `fix(install): preserve DSH profile names in recovery output (#2170)`，正文说用 Bash 参数展开替代 `basename` 命令替换以保留尾随换行，并处理了**空格 / 引号 / glob / 命令替换语法 / 分隔符 / 嵌入及尾随换行 / CR / ANSI 转义**这些「恶意 profile 名」。→ 教训：**profile 名和路径要当不可信输入处理**。

> ouroboros 仓库内 `fix(...)` 提交虽多（`1c968328`、`cd13da16`、`03714ba4` 等），但绝大多数是 Python 侧 agent 内核（seed/evidence/mcp），**与 dsh 插件装载无关**，故不计入本方向。dsh 方向有解释的坑就是上面 4 条（来源：`Q00_ouroboros` git log `--grep='dsh-plugin|integrations/dsh|dsh plugin|DeepSeek Harness'` + 全量 `fix` 扫描）。
---

## 2. `anywhere-labs_dsh-desktop`（dsh-plugin-desktop）

> 该仓库的提交多为 squash merge，**commit body 普遍为空，只有标题**。真正的「解释」全部写在 `.agents/notes/implemented/` 下的架构笔记里（中文 + 英文 + i18n.yaml，逐篇是「问题 / 决策 / 验证 / 备选 / 结果」五段式）。下面每条都用「笔记正文」当证据，标注笔记文件路径。

### 坑 2.1　打包后 profile 的符号链接进不了 `app.asar` → `ENOTDIR`
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-08-15-packaged-profile-fallback.zh.md`
- **现象（原文）**：「打包后的 Electron 进程可以通过虚拟 `app.asar` 文件系统直接读取文件，但操作系统符号链接无法进入该虚拟归档。若把逻辑打包 manifest 作为安装锚点，就会生成在 Loader 激活 Web bundle 前以 `ENOTDIR` 失败的链接。」
- **根因**：Electron 能读 ASAR 虚拟路径，但 Node 经操作系统 symlink 访问 profile 依赖时，ASAR 路径不是真实目录。
- **修复**：Electron Builder 把 manifest / patch / node_modules 一起解包；Desktop Host 在 `healProfilesModuleFallback` 前把安装锚点从 `app.asar/package.json` 映射到 `app.asar.unpacked/package.json`；每次启动修复旧链接，且**不改**被选 profile 的 manifest/patch。打包前若缺物理 manifest 或 desktop 插件子路径则**签名前就失败**。

### 坑 2.2　打包 pnpm 的 PATH 只能给子进程 → Host 插件发现不到 package manager
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-08-15-desktop-bundled-pnpm-runtime.zh.md`
- **现象（原文）**：「该终端拥有只属于其子进程的 `PATH`，因此 Cordis Host 插件与当前 desktop generation 启动的 subprocess 无法发现内置 package manager。调用 `pnpm` 的插件会在终端与应用运行时表现不一致。」
- **根因**：内置 pnpm 的命令目录只进了终端子进程的 PATH，没进 Electron main / Host 的 PATH。
- **修复**：Launcher 先跑账户 login shell 恢复 `PATH`（只从固定 allowlist 补 locale/工具链/pkg manager/venv），再把只含 `pnpm`（Windows 是 `pnpm.cmd`）的私有 runtime 目录**前置**到 Electron main 的 PATH。**明确拒绝**两种替代方案（原文）：「把完整终端 shim 目录加入 Host PATH」会覆盖每个插件里的 `node` 与 `dsh`；「在 Electron 进程中设置 Node-mode 与 ABI 变量」会让无关 Electron 子进程继承。
- **平台细节（可抄）**：`ELECTRON_RUN_AS_NODE` 只应存在于 pnpm subprocess tree，生成的 prelude 会在运行前**移除所有大小写形式**的该变量；Windows 上 batch 命令需要 `shell: true`，第三方插件若 `spawn('pnpm', { shell: false })` 无法执行 `pnpm.cmd`。

### 坑 2.3　renderer OOM 后主窗口空白，Host 还活着 → 需要「有界」自动恢复
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-09-07-runtime-renderer-recovery.md`；commit `62171c601` `fix(desktop): automatically recover crashed renderers`、`5af1f8c16` `fix(desktop): recover blank and unresponsive runtime pages`（body 均为空）
- **现象（原文）**：「Issue #813 includes renderer exits reported as `oom` … A dead renderer therefore left the main window blank while the Host remained alive.」
- **根因**：所有 exit 都被转给「一次性启动健康门」，而该门在 healthy boot 之后正确忽略失败 —— 于是**运行时**没有任何恢复。
- **修复（关键数字，可抄）**：每次 shell generation 拥有一个恢复 controller，**3 次尝试**，延迟 **0 / 1 / 3 秒**；一次 reload 必须同时满足「页面加载完成」+「30 秒内健康的 client Loader 报告」才算恢复；**只有连续健康满 1 分钟才重置尝试计数**（防「crash→reload→healthy」循环绕过上限）。耗尽后才弹用户态提示，且**故意用 Electron 系统原生 message box**（原文：「recovery from a renderer OOM must not require another Chromium-rendered UI」）。兼容模式有 content + titlebar **两个** WebContents，两个都要 reload 且都要健康。

### 坑 2.4　启动资源的释放顺序散落在 3 条路径 → 引入单一 owner
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-08-19-desktop-startup-resource-ownership.zh.md`
- **现象（原文）**：「一个 Desktop 进程会创建 Cordis Host、打包 pnpm PATH 安装，以及 Windows 上的打包 DSH PATH 安装 … `main.ts` 以前用互相独立的可变变量和重复清理代码表达它们的生命周期。普通 shutdown、fail-loud 清理和启动恢复分别实现了同一套释放协议的一部分。」
- **根因**：资源属于同一启动 generation，却没有单一 owner；调用方被迫知道释放顺序。
- **修复**：引入 `DesktopStartupGeneration`，接口只有 `id` / `bindHost(host)` / `own(release)` / `quiesceForRecovery()` / `release()`；`release()` 按**注册逆序**释放（即使某个回调失败也继续）；并发恢复共享同一个 Host disposal task。

### 坑 2.5　插件安装接口「文档说的和实现不一样」→ 身份可能分离
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-08-19-desktop-plugin-install-lifecycle-ownership.zh.md`
- **现象（原文）**：「公开 `desktopPnpm` 文档要求插件管理器调用 `runPlugin(['add', ...])`，但 implementation 会拒绝 `add`，并要求未公开的 `runPluginInstall()` 方法。Market adapter 只能自行发现并复制这个隐藏 interface … 隐藏方法还把安装 argv 与 recovery metadata 分开接收。调用方理论上可以安装 package A，却让 WAL 记录 package B。」
- **根因**：安装 argv 与恢复日志（WAL）是两条独立入参，没有强制同一身份。
- **修复**：`installPlugin(request)` 成为唯一受支持的 `add` 路径，它同时拥有「强制的 `add` 命令 / 唯一精确 `packageName@packageVersion` 目标 / 安装前 profile 快照 + WAL / generation 级操作门 / 进程树完整退出 / 失败恢复 / 成功后图像封存」。**结论（原文）**：「插件作者不得使用 `run()` 或 `runPlugin()` 安装插件。」

### 坑 2.6　profile 选择不能存进「被选 profile 的 settings」
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-08-15-desktop-profile-management.zh.md`
- **现象（原文）**：「Profile 选择发生在 Host Cordis 树及其 settings provider 创建之前，因此不能存放在被选 profile 的 settings namespace 中。若被选 profile 启动失败，在 renderer 与托盘都无法挂载时也必须能够恢复。」启动失败时不能无限重启 —— 「last-known-good generation 自身失败时仍会 **fail loud**，从而避免重启循环」。
- **根因**：循环依赖（被选 profile 能改 settings provider，而 profile 又必须在 provider 之前确定）。
- **修复**：选择状态放在 Electron user-data 下的**私有**带版本文档（`active` / `pending` / `lastKnownGood`），`0600` 临时文件 + 同目录原子 rename；只有 `app-boot` 完成且窗口加载成功后，才提升为 last-known-good。

### 坑 2.7　跨进程控制通道与端口占用
- **来源**：`anywhere-labs_dsh-desktop/.agents/notes/implemented/architecture/2026-09-10-beta-isolated-host.zh.md`；源码 `dsh-plugin-desktop/src/desktop-port.ts`、`src/webserver.ts`、`src/main.ts`
- **现象 / 设计**：Beta/稳定版把 Cordis Host 放进 Electron `utilityProcess` 隔离开（`startIsolatedDesktopHost`，源码 `src/host-process.ts` 用 `utilityProcess.fork(...)`）；私有控制通道**只**传原生操作和状态快照，函数留在原进程按回调 ID 调用。
- **端口**：默认从固定端口 `43120` 起（源码 `src/desktop-port.ts`：`DESKTOP_DEFAULT_WEB_PORT = 43_120`，`DESKTOP_WEB_PORT_RETRY_LIMIT = 32`），源码 `src/webserver.ts` 用 `code === 'EADDRINUSE'` 判定后顺延重试。
- **单实例**：`src/main.ts:384` `if (!app.requestSingleInstanceLock()) { ... }` —— 必须抢 Electron 单实例锁。
- **Host 崩溃处理**：`src/host-process.ts` 中 `child.once('exit', ...)`：「`DSH Host exited (${code}); restart the application to reconnect`」→ **Host 意外退出不自动重启、不重放请求**（笔记原文「Host 意外退出时报告错误，不自动重启或重放请求」）。退出流程：先请求正常清理（3s 超时）→ `child.kill()` → 限时等待退出（1s），无法确认终止则报错。
- **验证限制（诚实声明，可抄）**：「当前夹具未证明强制终止时任意插件后代进程的清理。」「未测量前不能宣称已改善 Windows 响应。」

> desktop 的 commit body 普遍为空，故 2.1–2.7 的「原文」均来自同名 `.agents/notes/...` 架构笔记，非 commit 正文。相关 commit 短哈希（标题，body 为空）：`62171c601`、`5af1f8c16`、`54af2fb1d`、`49aa95a30`、`6df4e5921`、`d93cd5de0`、`899d44bec`、`669557e8e`、`b30eea0d3`。
---

## 3. `xiaobright_dsh-anchored-standard`

> 这是一个 **preset（agent-plane composition）包**，不是普通混入宿主树的 bundle：它用 `agent.cordis.yml` + `preset.yml` 逐模式目录自包含。它的坑极适合教「跨平台 / 版本适配 / 发布前校验」。

### 坑 3.1　Windows 上 Git Bash 路径被 Node spawn 解释错 → 误导性 ENOENT
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `babc933`（2026-08-17）
- **提交信息原文**：
  > `fix: normalize Git Bash workdir paths on Windows`
  > 「Node spawn treats `/e/foo` as `E:\e\foo`, so bash fails with a misleading ENOENT. Convert Git Bash drive paths and fall back to the session cwd when an explicit workdir is missing.」
- **现象**：Windows 上 `workdir: /e/foo` 被 Node 解释成 `E:\e\foo`，bash 报**误导性的 ENOENT**。
- **根因**：Node `spawn` 不认 Git Bash 的 `/e/...` 盘符写法。
- **修复**：转换 Git Bash drive path；显式 workdir 缺失时回退到 session cwd。

### 坑 3.2　硬编码 Git Bash 安装路径 → 换台机器就找不到 shell
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `78b4cbd`（2026-08-17，正文提到手动 rebase PR #33）
- **提交信息原文（截断）**：
  > `fix(custom-bash): infer Git Bash path at runtime instead of hardcoding (PR #33, fixes #24)`
  > 「custom-bash.mjs resolution order: explicit bashPath > git install root > well-known Git-for-Windows roots (Program Files(/x86), per-user LOCALAPPDATA, scoop current) > plain bash on PATH; total discovery failure errors with guidance instead of falling back to a different shell … Hardcoded bashPath removed from ALL SIX mode compositions（PR 只改了 preset/ 的副本，`sync --check` 会拒）」
- **现象**：硬编码 `bashPath` 在别的机器上不存在。
- **根因**：只在一处改了，其余 5 个模式目录仍是旧副本。
- **修复**：运行时按优先级探测；**单源真相** `shared/custom-bash.mjs` + `npm run sync` 复制到每个模式目录；`sync --check` 拒绝不一致。

### 坑 3.3　`/bin/bash` 不存在的主机 → 「PTY shell exited during startup」
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `efb01ca`（2026-08-17）
- **提交信息原文（截断）**：
  > `fix(persistent-shell): boot bash on hosts without /bin/bash (#44)`
  > 「官方 minimal preset 的 terminal-bash 行用插件默认 `shellPath /bin/bash`。On NixOS（及 bash 不在 /bin 的主机）该绝对路径不存在，PTY 子进程启动即退出，每次 bash 调用都失败 `PTY shell exited during startup`。」
- **修复（可抄的 `!!js` 表达式）**：
  ```yaml
  shellPath: !!js "process.getBuiltinModule?.('node:fs')?.existsSync('/bin/bash') ? '/bin/bash' : 'bash'"
  ```
  → 有 `/bin/bash` 就用它（行为不变），否则退回 PATH 查找的 `bash`。

### 坑 3.4　宿主 API 变了：`session.events` 数组 → `session.snapshotEvents()`
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `751fd67`（2026-09-05）
- **提交信息原文**：
  > `fix: support session.snapshotEvents() in DSH presets`
  > 「DeepSeek Harness no longer exposes `session.events` as an array; presets should read session history via `session.snapshotEvents()` when available. Update all preset plugins and verify helpers to use `snapshotEvents()` with a fallback to the older `session.events` API for compatibility.」
- **修复**：所有 preset 插件改读 `snapshotEvents()`，**保留对旧 `session.events` 的 fallback**（保护旧宿主）。

### 坑 3.5　`dsh-persona` 0.1.3 把 `text:` 改成 `prefix:` → 旧 preset 静默失效
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `51b38ef`（2026-09-08）
- **提交信息原文**：`fix: migrate persona rows from `text:` to `prefix:` for dsh-persona 0.1.3`（正文为空）
- **现象**：升级宿主后 persona 行不再生效。
- **根因**：`dsh-persona` 的配置字段从 `text:` 迁到 `prefix:`。
- **修复**：把 persona 行的 `text:` 改成 `prefix:`（本仓库 preset 里可见 `config: { prefix: You are a helpful software engineer assistant. }`）。

### 坑 3.6　重启后自动注入的 hint 用了**确定性 id** → 重复 id 打断历史装配
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `b74543b`（2026-08-24）
- **提交信息原文（截断）**：
  > `fix(instruction-hint): make each injection id unique (fixes #76)`
  > 「The durable-scan dedup is prevention, not a guarantee: after a host restart the first `agent/pre-step` can run before `session.events` is materialized, see an empty list, and re-inject the hint. With the old deterministic id the duplicate collided with the first copy and stopped history assembly. Per-injection unique ids turn a past or future re-injection into a few wasted context tokens instead.」
- **现象**：注入的 hint 重复，**打断历史装配**（比多几个 token 严重得多）。
- **根因**：去重只是「预防」；宿主重启后首发 pre-step 可能在事件物化前跑，看到空列表 → 以**同一个确定性 id** 再注入一次 → id 撞车。
- **修复**：每次注入用唯一 id（代价只是多几个 context token）；并在 README 加排障说明：让受影响用户按 `source.kind == 'instruction-hint'` 去重旧坏日志。

### 坑 3.7　「用默认 preset 创建的会话」不发 `agent-preset/selected` → seeder 不跑
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `24caabe`（2026-08-19）、`6733c10`（2026-08-21）
- **提交信息原文（`24caabe`，截断）**：
  > `fix(prefab): seed sessions created with the preset as default`
  > 「A session CREATED with the preset in its header (the default-preset path) never emits `agent-preset/selected` — the preset is composed at creation, not swapped — so the seeder never ran … Trigger seeding on the session's first permission/preset event too, and tolerate a not-yet-published agent on that path.」
  > （`6733c10` 补充：「re-read the agent after the skill registry await so an agent published during that window receives the seeded turn cursor」）
- **现象**：用「默认 preset」新建的会话从第 1 轮开始，而不是种子化的第 3 轮。
- **根因**：默认 preset 路径**不发** `agent-preset/selected` 事件，seeder 的触发条件没命中；且 await 期间 agent 可能尚未发布。
- **修复**：也在会话第一个 permission/preset 事件上触发 seeding，并容忍 agent 尚未发布（跳过 cursor 同步直到 agent 出现）。

### 坑 3.8　配置项校验：未知 config key 应在 apply 时拒绝
- **仓库 + commit**：`xiaobright_dsh-anchored-standard` + `4c52927`（2026-08-15）
- **提交信息原文**：`fix(tool-bootstrap): reject unknown config keys at apply time`
- **教训**：插件对 `config` 做**白名单校验**，未知 key 在 `apply` 时就抛错，而不是静默忽略（新手写错 key 时能立刻发现）。

### 坑 3.9　自包含纪律（工程规范化，来自测试而非 commit）
- **来源**：`xiaobright_dsh-anchored-standard/test/self-containment.test.mjs`
- **规则 1**：任何模式目录的 `agent.cordis.yml` **不得**引用目录外的插件（测试用正则找 `name: ../` 之类的上引用，发现即 fail）。
  > 原文：`test('no mode references plugins outside its own directory', ...)` → `must be self-contained`
- **规则 2**：`shared/` 是单源真相，各模式目录是**物化副本**，`sync --check` 必须过。
  > 原文：`test('materialized copies match shared/ sources (run: npm run sync)', ...)`
- **`package.json` scripts（可抄）**：
  ```json
  "scripts": {
    "sync": "node scripts/sync-modes.mjs",
    "test": "node --test",
    "check": "node scripts/sync-modes.mjs --check && node --test"
  }
  ```
---

## 4. `omdsh-dev_DSH-better-sidebar`（644 commits / 271 修复）

### 坑 4.1　「槽声明先到、服务后到」→ 按槽触发注册会**静默什么都不注册**
- **仓库 + commit**：`omdsh-dev_DSH-better-sidebar` + `aa1b994`（2026-09-09）
- **提交信息原文（截断）**：
  > `fix(native): register the plugin's tab types when the registry service arrives`
  > 「The native seat declares `sidebar.right.pane.tab` BEFORE it provides `sidebarRightTabs`, so driving the registration off the slot declaration read the service as missing and registered nothing — permanently, since a declaration never collapses. Observed on a real DSH profile (0.1.5-alpha.1, `dsh web` on the web profile): the plugin host and its other slot registrations mounted, the native guide page stayed empty, and a probe printed `sidebarRightTabs= undefined` at declaration time with the registry present three seconds later.」
- **现象**：真机 profile 上插件宿主 + 其他槽都挂上了，**原生指南页空**；探针显示声明时 `sidebarRightTabs= undefined`，3 秒后才出现。scratch lane 看不到，因为那里插件在原生包 provide 之后才激活。
- **根因**：**声明（declaration）≠ 服务就绪**；声明永远不会 collapse，所以按声明触发注册就永久错过服务。
- **修复**：`registerNativeSurface` 改为**等 SERVICE**（`ctx.inject`），服务出现/重现时重跑；per-body 槽注册仍走 `slots.inject`。回归测试 `tests/native-surface.spec.ts` 模拟「槽先触发、服务后到」。
- **可抄教训**：**依赖服务用 `ctx.inject([...], cb)` 驱动，别用槽声明时机。**

### 坑 4.2　双挂载 → 两个侧边栏 / `duplicate prefix route` / `duplicate loader entry id`
- **来源**：`omdsh-dev_DSH-better-sidebar/cordis.patch.yml` 注释 + `README.md` 常见问题表
- **现象（README 原文）**：「页面出现**两个侧边栏** | 双挂载。旧的手动挂载行：`~/.dsh/profiles/web/cordis.patch.yml` 还留着 `- insert: ... better-sidebar ...`，删掉那段（同 id 重复挂载 loader 会直接报 `duplicate loader entry id`）。」
- **根因**：bundle patch 通道 + 手动挂载行同时存在 = 挂两次（Node 半两个、两个侧边栏）。
- **修复**：
  - 切到 bundle 通道前**删掉** profile 里旧的手动挂载行；
  - 聚合包（如 `@linxin666/dsh-web-ui-all`）以**不同 id** 挂载本包时，插件自身 bundle patch 用 `!!js` **自动退让**（见 §二.5 的 `disabled: !!js` 表达式）；
  - 聚合包必须**排在 `dsh-better-sidebar` 之前**（注释原文：「the aggregate bundle must precede this one in `dsh.profile.bundles`」）；反向顺序是**已知限制**（`!!js` 只看得见它之前的行，且没有运行时单例守卫）。
  - 聚合双挂载的 boot 报错原文（注释）：「Two mounts register `/sidebar/api` twice and fail the whole plugin tree at boot (`"duplicate prefix route"`).」

### 坑 4.3　注册没包 `ctx.effect` → HMR/禁用后残留 → `already registered`
- **来源**：`omdsh-dev_DSH-better-sidebar/docs/external-plugin-guide.md` §3 / §9；源码 `src/client/service.ts:595-611`
- **源码原文（错误文案）**：
  ```ts
  throw new Error(`[dsh-better-sidebar] tab type "${descriptor.id}" already registered`)
  throw new Error(`[dsh-better-sidebar] file viewer "${descriptor.id}" already registered`)
  ```
- **现象（指南原文）**：「不包 effect，HMR / 插件禁用后注册残留，下次激活会抛 `"already registered"`。」
- **修复**：`ctx.effect(() => ctx.betterSidebar.registerTab({...}))`（disposer 由 Cordis fiber 在卸载时自动调用）；`inject = ['betterSidebar']` 让 Cordis 保证服务就绪后才激活你。

### 坑 4.4　id 撞车：`registerTab` / `registerFileViewer` 对重复 id 抛错
- **来源**：`docs/external-plugin-guide.md` §4.4
- **原文**：「你的 `id` 不可与上述重复，否则 `registerTab` 抛 `"tab type \"X\" already registered"`。」
- **修复**：**用包前缀**（`my-plugin:xxx`）。内置 7 tab id：`editor(10) / git(20) / subagent(30) / sidechat(35) / terminal(40) / browser(50) / diff(-1)`；内置 6 viewer：`image/pdf/markdown/html/code/binary-download`。

### 坑 4.5　自定义会话种子缺 fork 标记 → 子会话「继承父会话未领取的 inbox」→ 幽灵消息
- **仓库 + commit**：`omdsh-dev_DSH-better-sidebar` + `93ad87d`（2026-09-06）
- **提交信息原文（截断）**：
  > `fix(sidechat): stamp the seed with fork markers so the child inherits no pending inbox`
  > 「sidechat.start passed `seed` without `meta.isSeeded: true` + `inheritedEventCount`, so dsh-session treated the whole seed as the child's OWN events and the child's Inbox constructor replayed the parent's `agent/inbox/spliced` history … The first side prompt then claimed `[phantom, boundary, question]` — the stale parent message was sent to the model BEFORE the boundary and logged as a `user/message`.」
- **现象**：长长时侧边对话先把「之前那条 User msg」发出去（幽灵消息排在 boundary 之前最先发给模型）。
- **根因**：只给 seed 不标 `isSeeded`，宿主把整段 seed 当重放历史；子会话 inbox 折重放父会话的 `agent/inbox/spliced`。
- **修复**：传宿主 `session.fork` 同款标记对（`meta.isSeeded: true` + `inheritedEventCount`）；回归用**真实** `Session.create` + `Inbox` 双向跑。另注（AGENTS.md）：`Session.create` 的 header `version` 必须用 `SESSION_FORMAT_VERSION`（0.1.5 是 `3` 字面量），**勿钉 `0`**。

### 坑 4.6　宿主大版本适配：0.1.5-alpha.1 → alpha.2 → rc.1 每步都在改宿主契约
- **来源**：commit `ba01147`（alpha.1）、`0b6ac5d`（alpha.2）、`725b2f7`（rc.1）
- **`ba01147` 原文（截断）**：
  > - 「Live assistant stream (`assistant/chunk` is gone): 0.1.5 publishes in-flight model deltas as process-local `agent/assistant-stream` frames instead of durable `assistant/chunk` events …」
  > - 「Cold session reads (`persistence.inspect` is gone) … `open(id,'read') -> handle.read() -> close()`」
  > - 「drop the `remote.session.openWorkspacePath` interception … so the wrapper had no caller and would hijack the host's "open in app" gesture」
- **`0b6ac5d` 原文（截断）**：
  > - 「the native guide entry lost its `description` field …」
  > - 「global main panels replaced the `conversation` root slot with the keyed `main` slot (`main.conversation`)」
  > - 「Fixes a pre-existing fill bug … the native tab body host is a block scroller with a definite height, so tab roots that only declared `flex: 1` collapsed to content height and the side chat composer drifted off the pane bottom.」
- **`725b2f7` 原文（截断）**：
  > 「`SidebarRightGuideEntry.description` is back (optional). The native guide renders it only while it lists **at most 4 entries**; a longer list drops every description … the plugin contributes six guide entries, so the default composition is over the 4-entry limit and shows titles only.」
  > 「Restore caveat fixed in the lane: the settings route merges patches key-wise, so undoing a temporary `tabsEnabled` change by posting the original (empty) map leaves the disabled keys behind — the e2e restores every key it touched explicitly.」
- **可抄结论**：宿主每升一个小版本，**会话事件模型 / 文件打开漏斗 / 槽位 / 字段**都可能变；适配要「只对一条线做运行时兼容」，其余用户留在旧线（0.1.5-alpha.2 停在 `v0.19.0-alpha.1`，0.1.2-rc.1 停在 `v0.18.1`）。**字段回归 ≠ 兜底句回归**：宿主自己没有兜底句时，插件也**不发** `description` 字段（"通用句是噪音"）。

### 坑 4.7　`dsh-*` 传递 peer 与上游包自身 `dependencies` 丢失 → `Cannot find package 'anser'`
- **来源**：`omdsh-dev_DSH-better-sidebar/AGENTS.md` §3 第 9 条（原文很长，此处摘）
- **现象 1（原文）**：「`@deepseek-ai/dsh-subagent` 等 npm 包把 `dsh-attachment` 等 dsh-* 姊妹包全部声明为 peerDependencies … 其余 peer 在 pnpm 下会解析到树上残留的旧版——如 `dsh-attachment@0.1.1-rc.1` 缺 `admitPromptContent` 导出、`dsh-subagent` 产物 import 它时测试加载即崩。」
- **现象 2（原文）**：「`@deepseek-ai/dsh-client-ui-primitives@0.1.5-alpha.2` 的 manifest 不再声明任何 `dependencies`（alpha.1 声明了 19 个），但 `lib/*.js` 仍裸 import `anser` / `shiki` / `@shikijs/langs/*` / `mdast-util-*` / `micromark-*` / `katex` … vitest 一碰 primitives 就 `Cannot find package 'anser'`。」
- **根因**：宿主由预构建前端 bundle 满足依赖；**独立安装的 dev/test 树不会**。
- **修复**：把 dev 树实际触达的**全部** dsh-* 传递 peer 提升进 `devDependencies`（精确钉版）；上游丢的 `dependencies` 也要提升。**每次适配新 alpha 版本先跑 `pnpm peers check`**。rc.1 复评：「这组提升不得回退」。

### 坑 4.8　平台相关（Windows / WSL / 终端）
- **`7499383`**（2026-09-02）`fix(terminal): resolve Windows custom shell executables (#487)`（body 为空）—— Windows 自定义 shell 可执行文件解析。
- **`6d87747`**（2026-09-03）`fix(pty): contain node-pty's deferred Windows resize after pty exit`，原文（截断）：
  > 「node-pty's WindowsTerminal queues resize calls that arrive before the ConPTY control socket's first data flush (`_deferNoArgs`). If the pty exits before the flush, the deferred resize throws `'Cannot resize a pty that has already exited'` inside the socket's `'data'` handler — **uncatchable by any caller and fatal to the host process.** The Windows CI lane caught exactly this as an unhandled error while all 1233 tests passed.」
  > 修复：自己加一道 gate 把「首个输出前」的 resize 停住，输出 flush 后 `setImmediate` 重放；**Windows 才 arm，POSIX 保持原行为**（POSIX resize 是同步的）。
- **`180b16d`**（2026-08-29）`fix: 修复 WSL 会话 Linux 路径解析 (#399)`（body 为空）。
- **`8191951`**（2026-09-08）`fix(terminal): WS close reason 按 UTF-8 字节截断，避免超 123 字节抛错`，原文：
  > 「ws 用 `Buffer.byteLength` 校验 close reason 的 123 字节上限（`ws/lib/sender.js`），原 `slice(0, 100)` 按 UTF-16 code unit 截断，非 ASCII shell 名可达 316 字节（实测 200 个 CJK 字符），`ws.close()` 会抛 `RangeError` 顶掉原始错误。改为按字节截断且不切碎 code point。」
- **可抄结论**：**`slice()` 按 UTF-16 单位 ≠ 字节上限**；跨平台行为要按 `process.platform` 分叉并各自测。

### 坑 4.9　CI / 工程（Windows 车道暴露的假绿）
- **`c4c4d73`**（2026-09-03）`fix(ci): resolve consumer-type link targets to their physical path`，原文：
  > 「On the Windows lane the `@deepseek-ai/cordis` link produced `TS2307` even though the link was visibly created: under pnpm its target, `node_modules/@deepseek-ai/cordis`, is itself a junction into `.pnpm`, and a native symlink pointing AT that junction does not traverse for `tsc`. Resolve both link targets with node's native `realpath` first … and fail loudly with the link layer listed when a created link does not resolve to a package root.」
- **`2052d05`**（2026-09-02）`fix(e2e): 聚合 lane 按 mtime 取最新 tarball 并统一 DSH_CMD 缺省解析`，原文（截断）：
  > 「`e2e-aggregate-mount.sh` 选 tarball 用字典序 `ls | head -1`，仓库根堆积多个历史 tgz 时会把冒烟**挂到过期产物上** … 顺带修一个移植中暴露的边角：候选计数行在零候选时因 `pipefail+set -e` 静默退出，吞掉下一行的友好报错——补 `|| true`。」
- **`3d23ceb`**（2026-09-02）`fix(ci): pnpm 版本统一由 packageManager 字段供版，移除 action 显式 version 输入`（body 为空）。
- **可抄结论**：CI 要跑 **Windows 车道**；tarball 按 **mtime** 取最新；脚本要防 `set -e` 吞报错。

### 坑 4.10　原生 tab 的标题 / 图标
- **`4da2b43`**（2026-09-09）`fix(native): title a file tab by its own name, not the descriptor's`，原文：
  > 「The editor type serves both the files PAGE and every file RESOURCE; its native `title` callback ignored the address, so every opened file showed up in the strip as "Files" — indistinguishable tabs. Verified on a real profile: after opening `AGENTS.md` from the tree and a chat file link, the strip read ["文件", "文件", "文件"].」
- **`91de0e2`**（2026-09-09）`fix(native): give the "Files" guide row its glyph`，原文：
  > 「The guide renders `entry.icon`, and the `files` kind takeover registered without one — so after the editor type stopped contributing its own duplicate row (`b56ceec`), the single "Files" row was the only entry in the new-tab list with a blank icon slot.」
- **`b56ceec`**（2026-09-09）`fix(native): offer one "Files" row in the new-tab list`，原文：
  > 「The editor type's page identity IS the `files` kind takeover (same explorer, same title), so the guide/new-tab list showed two identical "Files" entries … The editor type now contributes no guide entry of its own; it stays registered as the file RESOURCE viewer.」
- **可抄结论**：`title` 回调要**读 address**（页面用 descriptor 标题、文件用文件名）；`icon` 不声明宿主补方块占位；**同一个页面身份只能有一条 guide 行**。

### 坑 4.11　过度遮蔽（secret redaction 误伤普通文件）
- **仓库 + commit**：`omdsh-dev_DSH-better-sidebar` + `0469319`（2026-09-06）
- **提交信息原文（截断）**：
  > `fix(redact): keep the credential heuristics off ordinary files`
  > 「Path layer: patterns now match with a right boundary (must not continue into `[a-z0-9]`) and list only store-plural forms (`credentials/secrets/passwords`, not `tokens`), so `tokenizer.ts` / `dev.environment.ts` / `style.keys.ts` / `api-tokens.md` are no longer masked whole while `.env.local` / `credentials.json` / `mytoken.yaml` still are. Content layer: drop the bare `key/auth/token/pass/bearer` field names — they label far more ordinary content (keyboard keys, CSS custom properties, lexical tokens) than secrets.」
- **可抄结论**：**安全启发式要加「右边界」+ 限定复数名词**，否则把 `tokenizer.ts` 这类普通文件整段遮蔽。

### 坑 4.12　README「常见问题」里记录的、用户最常撞的安装坑（可直接抄成手册）
- **来源**：`omdsh-dev_DSH-better-sidebar/README.md` 常见问题表（原文逐条）：
  | 现象 | 原因与解决 |
  |---|---|
  | 报 `Ignored build scripts` | pnpm 11 拦截构建脚本。在 profile 目录（`~/.dsh/profiles/web`）跑 `pnpm approve-builds --all`。 |
  | 报 `minimum release age` / 版本不足 24h | 装的版本发布不足 24 小时。等 24h 或重跑一次（pnpm 会自动补 `minimumReleaseAgeExclude`）。 |
  | 报「找不到 profile 目录」 | 先跑一次 `dsh web`，让它初始化 `~/.dsh/profiles/web`。 |
  | 页面出现**两个侧边栏** | 双挂载（见坑 4.2）。 |
  | Windows 下终端无法使用 | `node-pty` 依赖预编译二进制；当前 Node 版本没有对应产物时需装编译工具链（VS Build Tools）。 |
  | 终端提示「node-pty 加载失败」 | 在 `~/.dsh/profiles/web` 下 `pnpm approve-builds --all && pnpm rebuild node-pty`，完成后重启 DSH 并点重试。 |
  | 提示 `dsh: command not found` | 先安装 DSH；或 `npx -y --package @deepseek-ai/dsh dsh plugin --profile web add dsh-better-sidebar@latest`。 |
---

# D · 二、可逐字照抄的代码模板

## 二.1　ouroboros 的零代码组合包（**本次最重要的模板**）

**目录树**（3 个文件，零代码）：
```
Q00_ouroboros/integrations/dsh-plugin/
├── README.md
├── cordis.patch.yml
└── package.json
```

**`package.json` 全文**（来源：`Q00_ouroboros/integrations/dsh-plugin/package.json`）：
```json
{
  "name": "dsh-ouroboros",
  "version": "0.1.0",
  "description": "Mount Ouroboros (spec-first AI dev workflow engine) into DeepSeek Harness as native tools — type \"ooo interview\" or \"ooo auto\" in chat.",
  "type": "module",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/Q00/ouroboros.git",
    "directory": "integrations/dsh-plugin"
  },
  "homepage": "https://github.com/Q00/ouroboros/tree/main/integrations/dsh-plugin",
  "keywords": [
    "dsh-plugin",
    "deepseek-harness",
    "ouroboros",
    "mcp"
  ],
  "files": [
    "cordis.patch.yml",
    "README.md"
  ],
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

**`cordis.patch.yml` 全文**（来源：`Q00_ouroboros/integrations/dsh-plugin/cordis.patch.yml`；注释保留原文，正是新手最该读的部分）：
```yaml
# dsh-ouroboros — mounts Ouroboros as native MCP tools inside DeepSeek Harness.
#
# Ouroboros (https://github.com/Q00/ouroboros) is a spec-first AI dev workflow
# engine: Socratic interview -> Seed spec -> execute -> evaluate -> evolve.
# This bundle inserts one @deepseek-ai/dsh-mcp-client row that spawns
# `ouroboros mcp serve` over stdio, so every dsh agent gets tools named
# mcp__ouroboros__ouroboros_interview, mcp__ouroboros__ouroboros_auto, and 33
# others. Typing "ooo interview <goal>" or "ooo auto <goal>" in chat is enough
# for the model to find and call the matching tool on its own — no extra
# prompting needed (each tool carries its own description).
#
# Requirements: Python >= 3.12 and `uv` (https://astral.sh/uv) on PATH. No
# separate `pip install` step — uvx fetches and runs Ouroboros in an isolated
# environment on first launch.
#
# Configuration (env vars, read by the spawned `ouroboros mcp serve` process):
#   OUROBOROS_LLM_BACKEND   — LLM backend for interview/seed/QA. Unset uses
#                             your existing `ouroboros setup` default. `dsh`
#                             routes those calls back through DeepSeek Harness,
#                             but it is NOT a one-variable switch: Ouroboros
#                             spawns its own `dsh-acp-demo` child and fails
#                             closed (`invalid_config`) unless
#                             OUROBOROS_DSH_CONFIG_PATH names an absolute
#                             trusted Cordis composition. See the bundle README.
#   OUROBOROS_AGENT_RUNTIME — agent runtime backend for ooo run/ooo auto's
#                             execution step. Defaults to `host`: dsh has no
#                             installable execution CLI of its own, so by
#                             default the dsh model itself does the work —
#                             `execute_task` publishes a dispatch and dsh
#                             spawns its own subagent to service it
#                             (orchestrator/host_dispatch.py). Set this to an
#                             executable runtime (claude-cli, codex,
#                             opencode, ...) to have that CLI do the work
#                             instead.
#   OUROBOROS_DSH_CONFIG_PATH / OUROBOROS_DSH_CLI_PATH
#                           — the two prerequisites of the `dsh` LLM backend
#                             above: the absolute composition file, and the
#                             `dsh-acp-demo` bin when it is not on PATH.
#
# Override any field from your own profile's cordis.patch.yml by id (see the
# "Package and install a plugin" tutorial) — e.g. to pin a specific Ouroboros
# version, add local MCP servers back, or tighten toolCallTimeoutMs.
- insert:
    - id: mcp-ouroboros
      name: '@deepseek-ai/dsh-mcp-client'
      config:
        serverName: ouroboros
        transport: stdio
        command: uvx
        args:
          - --from
          - 'ouroboros-ai[mcp]'
          - --with
          - 'mcp==2.0.0'
          - ouroboros
          - mcp
          - serve
        # The child does NOT inherit the harness environment wholesale:
        # @deepseek-ai/dsh-subprocess hands mcp-client a scrubbed parent env
        # with every credential-shaped name (/KEY|PASSWORD|SECRET|TOKEN/i) and
        # every DSH_* name removed, precisely so harness credentials never leak
        # into a spawned process implicitly. This explicit layer merges *after*
        # that scrub, so any credential Ouroboros genuinely needs has to be
        # named here. It is deliberately a short allowlist covering the two
        # documented backends — not a wildcard passthrough. To forward another
        # (OPENAI_API_KEY, OPENROUTER_API_KEY, GOOGLE_API_KEY, ...), override
        # this row in your own profile's cordis.patch.yml with that one extra
        # name — restating the whole `config`, since a later layer replaces a
        # row's config rather than deep-merging it. Non-credential names
        # (PATH, HOME, the OUROBOROS_* selectors) survive the scrub on their
        # own; the OUROBOROS_* rows below are here to keep the contract
        # visible in one place.
        #
        # `?? ''` keeps every value a string (the row's schema is a string
        # dict). Ouroboros treats a blank credential as unset, so an unset host
        # variable stays effectively unset in the child. OUROBOROS_AGENT_RUNTIME
        # is the one exception: it falls back to the literal `'host'` rather
        # than `''`, because dsh has no installable execution CLI to fall back
        # to on its own — see the comment above.
        env:
          OUROBOROS_LLM_BACKEND: !!js process.env.OUROBOROS_LLM_BACKEND ?? ''
          OUROBOROS_AGENT_RUNTIME: !!js process.env.OUROBOROS_AGENT_RUNTIME || 'host'
          OUROBOROS_DSH_CONFIG_PATH: !!js process.env.OUROBOROS_DSH_CONFIG_PATH ?? ''
          OUROBOROS_DSH_CLI_PATH: !!js process.env.OUROBOROS_DSH_CLI_PATH ?? ''
          ANTHROPIC_API_KEY: !!js process.env.ANTHROPIC_API_KEY ?? ''
          DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY ?? ''
        # ouroboros_auto runs a full interview -> Seed -> execute -> grade
        # pipeline synchronously when called without polling; give it real
        # headroom instead of dsh's 60s mcp-client default.
        toolCallTimeoutMs: 1800000
        # Soft-fail: a machine without `uv`/Ouroboros configured yet should
        # still boot dsh with every other plugin working, not crash outright.
        # Recovery is not guaranteed to be automatic — whether mcp-client
        # retries at all depends on the dsh build (the published rc has no
        # reconnect loop), and where it exists the attempt budget is bounded.
        # After fixing the cause, reload the plugin or restart dsh.
        failOnStartupError: false
```

**分析（新手最需要的三点）**：
1. **挂了 1 行**：`- insert:` 列表里只有一条 `id: mcp-ouroboros`、`name: '@deepseek-ai/dsh-mcp-client'`。
2. **有 `!!js`**：全部在插件 **config** 内（`env` 段 6 个值）。**没有** `disabled` 字段。
3. **没有 `disabled`**：它是无条件挂载（不需要聚合退让逻辑）。
---

## 二.2　`dsh-desktop`：桌面宿主插件

**`dsh-plugin-desktop/package.json` 关键字段（逐字，其余依赖略）**（来源：`anywhere-labs_dsh-desktop/dsh-plugin-desktop/package.json`）：
```json
{
  "name": "dsh-plugin-desktop",
  "version": "2.0.9",
  "description": "DSH Desktop: an Electron shell composed as a DeepSeek Harness Cordis plugin",
  "type": "module",
  "main": "lib/main.js",
  "types": "lib/types/index.d.ts",
  "bin": {
    "dsh-desktop": "lib/bin.js",
    "dsh-plugin-desktop": "lib/bin.js"
  },
  "exports": {
    ".": { "types": "./lib/types/index.d.ts", "default": "./lib/index.js" },
    "./profile": { "types": "./lib/types/profile.d.ts", "default": "./lib/profile.js" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" },
    "./webserver": { "types": "./lib/types/webserver.d.ts", "default": "./lib/webserver.js" },
    "./windows-pwsh-sandbox": { "types": "./lib/types/windows-pwsh-sandbox.d.ts", "default": "./lib/windows-pwsh-sandbox.js" },
    "./terminal": { "types": "./lib/types/terminal.d.ts", "default": "./lib/terminal.js" },
    "./pnpm": { "types": "./lib/types/pnpm.d.ts", "default": "./lib/pnpm.js" },
    "./profile-service": { "types": "./lib/types/profile-service.d.ts", "default": "./lib/profile-service.js" },
    "./desktop-plugins": { "types": "./lib/types/desktop-plugins.d.ts", "default": "./lib/desktop-plugins.js" },
    "./profiles": { "types": "./lib/types/profiles.d.ts", "default": "./lib/profiles.js" },
    "./diagnostics": { "types": "./lib/types/diagnostics.d.ts", "default": "./lib/diagnostics.js" },
    "./notifications": { "types": "./lib/types/notifications.d.ts", "default": "./lib/notifications.js" },
    "./updates": { "types": "./lib/types/updates.d.ts", "default": "./lib/updates.js" },
    "./package.json": "./package.json"
  },
  "files": [
    "build/app-icon.ico",
    "build/app-icon.png",
    "build/app-icon-mac.png",
    "build/tray-icon.svg",
    "build/tray-icon*.png",
    "cordis.patch.yml",
    "docs/**",
    "lib/**/*.js",
    "lib/**/*.map",
    "lib/native-ui/**",
    "lib/types/**/*.d.ts",
    "README.md",
    "README.zh.md",
    "README.i18n.yaml",
    "THIRD_PARTY_NOTICES.md"
  ],
  "dsh": {
    "client": {
      "inject": [
        "@deepseek-ai/dsh-api-remotes",
        "@deepseek-ai/dsh-client-connection",
        "@deepseek-ai/dsh-client-locale",
        "@deepseek-ai/dsh-client-ui-renderer",
        "@deepseek-ai/dsh-client-ui-settings",
        "@deepseek-ai/dsh-client-ui-theme"
      ],
      "platform": "web"
    },
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  },
  "scripts": { …(略，见下) },
  "dependencies": { …(略：129 个 @deepseek-ai/dsh-* 精确钉 0.1.5-rc.1 + 少量第三方) },
  "peerDependencies": { "electron": "43.3.0" },
  "devDependencies": { …(略) }
}
```
> **注意**：这个包**同时**有 `dsh.bundle`（宿主/桌面侧）**和** `dsh.client`（浏览器侧，`platform: "web"`）—— 它是「桌面宿主 + Web client 面」双面插件。

**`dsh-plugin-desktop/cordis.patch.yml` 全文**（来源同上）：
```yaml
# Desktop Host operations compose around the existing Web bundle. Compatibility
# mode keeps upstream ownership of the browser carrier and rendered UI.
- insert:
    - id: desktop-shell
      name: dsh-plugin-desktop
      config:
        mode: compatibility
    - id: desktop-terminal
      name: dsh-plugin-desktop/terminal
      disabled: !!js process.platform === 'linux'
    - id: desktop-diagnostics
      name: dsh-plugin-desktop/diagnostics
    - id: desktop-notifications
      name: dsh-plugin-desktop/notifications
    - id: desktop-pnpm
      name: dsh-plugin-desktop/pnpm
    - id: desktop-profiles
      name: dsh-plugin-desktop/profiles
    - id: desktop-updates
      name: dsh-plugin-desktop/updates

# A desktop launch has no terminal operator waiting for the Web readiness line.
- id: web-runtime
  config:
    openBrowser: false
    printUrl: false
    surfaceContext: true
    trustedHosts: []
```
> **教学价值**：这演示了 ① 一个组合包 `insert` **多行**；② `name` 用包**子路径**（`dsh-plugin-desktop/terminal`），行 `id` 与子路径**解耦**（`desktop-terminal`）；③ `disabled: !!js process.platform === 'linux'` 是官方认可的**跨平台**写法；④ 第二个顶层 patch 项**不带 `insert`**，只是 `id` 定位 + `config` 覆盖已有行（`web-runtime`）——这就是「override」形态。

**「怎么起一个 dsh 进程/会话」的关键代码**（Electron 用 `utilityProcess` 起独立 Host 子进程；来源：`dsh-plugin-desktop/src/host-process.ts`）：
```ts
/** Electron owns the child lifetime; the child owns the unchanged DSH Web server. */
export async function startIsolatedDesktopHost(options: IsolatedHostOptions): Promise<void> {
  const child = utilityProcess.fork(fileURLToPath(new URL('./host-process-entry.js', import.meta.url)), [], {
    serviceName: 'DSH Host', stdio: 'pipe', cwd: process.cwd(), env: { ...process.env },
  })
  // Keep normal Host logs in its own files; stderr includes bootstrap failures.
  child.stdout?.on('data', (data: Buffer) => { process.stdout.write(data) })
  child.stderr?.on('data', (data: Buffer) => { process.stderr.write(data) })
  const rpc = new HostRpc({
    send: message => child.postMessage(message),
    listen: receive => { child.on('message', receive); return () => { child.removeListener('message', receive) } },
  }, 120_000)
  const releaseNative = bindNativeRuntime(rpc, options.runtime)
  rpc.handle('certificate', () => options.prepareCertificate())
  rpc.handle('quit', ([code]) => { setImmediate(() => options.requestQuit(code)) })
  …
  child.once('exit', (code) => {
    exited = true
    rpc.close(`DSH Host exited (${code})`)
    resolveExit()
    if (!stopping && booted) options.onFailure(new Error(`DSH Host exited (${code}); restart the application to reconnect`))
  })
```
> 另见 `src/main.ts:384` `if (!app.requestSingleInstanceLock()) { ... }`（单实例锁）；`src/webserver.ts` 用 `EADDRINUSE` 判定后端重试；`src/desktop-port.ts` 端口策略 `43120` + 32 次顺延。

**桌面插件包目录树（2 层，来源：`dsh-plugin-desktop/src/`）**：
```
dsh-plugin-desktop/
├── package.json
├── cordis.patch.yml
├── tsconfig.json / tsconfig.client.json / tsconfig.native-ui.json / tsconfig.tests.json / tsconfig.tests.client.json
├── tsdown.config.ts / vite.native-ui.config.ts / vitest.config.ts
├── docs/            (plugin-services.md + .zh.md + compatibility-chrome-isolation.md + operation-reliability-matrix.yaml)
├── build/           (图标 assets)
├── scripts/         (打包/校验脚本：verify-runtime-closure、verify-loader-boot、verify-profile-boot、verify-licenses…)
├── tests/
└── src/
    ├── (约 130 个 .ts 根文件：main.ts / index.ts / bin.ts / host-process.ts / pnpm.ts / profile-manager.ts / safe-mode.ts / renderer-recovery.ts / startup-generation.ts …)
    ├── client/
    └── native-ui/   (compatibility-chrome / components / desktop-dialog / lib / profile-create / profile-selector / recovery / setup-wizard / shared)
```

**`scripts` 里可直接抄的发布门（来源：`dsh-plugin-desktop/package.json`）**：
```json
"verify:closure": "node --test scripts/runtime-closure.spec.mjs && node scripts/verify-runtime-closure.mjs",
"verify:cli": "node scripts/verify-cli-runtime.mjs",
"verify:loader": "node scripts/verify-loader-boot.mjs",
"verify:profile": "node scripts/verify-profile-boot.mjs",
"verify:licenses": "node scripts/verify-licenses.mjs",
"prepack": "yarn run check",
"check": "yarn run build && yarn run typecheck && yarn run test && yarn run verify:closure && yarn run verify:cli && yarn run verify:loader && yarn run verify:profile && yarn run verify:aa && yarn run verify:licenses && yarn run verify:operations"
```
> 教学点：`prepack` 挂钩 `check` → **`npm pack` / `npm publish` 前自动跑全套校验**。
---

## 二.3　`anchored-standard`：完整包结构 + 构建/校验配置

**`package.json` 全文**（来源：`xiaobright_dsh-anchored-standard/package.json`）：
```json
{
  "name": "dsh-anchored-standard",
  "version": "0.1.0",
  "private": true,
  "description": "Two-phase DeepSeek Harness preset: Minimal-aligned bootstrap, then full Standard tools",
  "type": "module",
  "license": "MIT",
  "engines": {
    "node": ">=22.19.0"
  },
  "scripts": {
    "sync": "node scripts/sync-modes.mjs",
    "test": "node --test",
    "check": "node scripts/sync-modes.mjs --check && node --test"
  }
}
```
> **注意**：它是 **preset 包**（`private: true`，不发 npm），没有 `dsh` 字段；用目录结构 + `agent.cordis.yml` 表达。

**完整目录树（来源：`xiaobright_dsh-anchored-standard/`，126 文件）**：
```
dsh-anchored-standard/
├── package.json  README.md  README.zh-CN.md  LICENSE  NOTICE  ACKNOWLEDGEMENTS.md  FAREWELL.md
├── .gitattributes  .gitignore  .github/workflows/test.yml
├── scripts/sync-modes.mjs          # 单源真相 → 各模式目录的物化同步器（--check 模式）
├── shared/                         # 单源真相（15 个 .mjs）
│   ├── anchor-turn.mjs  compaction-epoch.mjs  context-gate.mjs  cot-drip.mjs
│   ├── custom-bash.mjs  deliberation-gate.mjs  dev-tool-search.mjs  instruction-hint.mjs
│   ├── skill-search.mjs  think-phase.mjs  tool-bootstrap.mjs  toolchoice-adapter.mjs
│   └── wire-think.mjs  zero-tool-bootstrap.mjs
├── test/                           # 20 个 node:test 用例
│   ├── self-containment.test.mjs   # 守护「目录自包含」+「副本与 shared 一致」
│   └── (anchor-turn / context-gate / custom-bash / instruction-hint / snapshot-events-compat …)
├── verify/                         # 一次性无头复现 runner
│   ├── run-verify.mjs  verify-runner.mjs  first-assistant-canceller.mjs
├── preset/                         # 7 个可独立复制安装的模式目录：
├── prefab/                         #   每个目录都含 agent.cordis.yml + preset.yml + 若干 .mjs
├── zero-anchored-standard/
├── whoami-standard/
├── eternal-minimal/
├── wire-think-standard/
└── combo-anchored/
```

**`preset/preset.yml`（模式元数据，可抄）**：
```yaml
name: Anchored Standard (experimental)
description: Bootstrap with the Minimal preset's real tool pair (persistent bash + str_replace_editor) and no auto-injected workspace or skill context, then expose the full Standard catalog after the first durable tool call or reply.
order: 5
```

**`preset/agent.cordis.yml` 的「insert 行」形态（节选，逐字）**——注意这里用**顶层数组 + `- id:` 行**（preset 组合格式），与 bundle 的 `- insert:` 不同：
```yaml
- id: context-gate
  name: ./context-gate.mjs
  config:
    promoteOn: either
    includeSubagents: true
    allowKinds: [skill-invocation]

- id: tool-pwsh
  name: '@deepseek-ai/dsh-tool-pwsh'
  disabled: !!js process.platform !== 'win32'

- id: persistent-shell
  name: cordis:group
  group: true
  disabled: !!js process.platform === 'win32'
  isolate:
    terminals: true
  config:
    - id: pty
      name: '@deepseek-ai/dsh-terminal'
    - id: terminal-bash
      name: '@deepseek-ai/dsh-terminal-bash'
      config:
        shellPath: !!js "process.getBuiltinModule?.('node:fs')?.existsSync('/bin/bash') ? '/bin/bash' : 'bash'"
        timeoutMs: 300000
```
> 可抄知识点：① `name: ./xxx.mjs` 相对路径（锚到 patch 文件旁，源码机理见 §0）；② `name: cordis:group` + `group: true` + `config:` 是数组 = **嵌套组**；③ `isolate:` 声明 realm；④ `disabled: !!js process.platform === 'win32'` 跨平台分叉；⑤ 一个 `!!js` 表达式里用 `process.getBuiltinModule?.('node:fs')`（更安全的 Node API 探测）。

**`check` 脚本与自包含测试全文**（来源：`xiaobright_dsh-anchored-standard/test/self-containment.test.mjs`）：
```js
const MODE_DIRS = [
  'preset', 'prefab', 'zero-anchored-standard', 'whoami-standard',
  'eternal-minimal', 'wire-think-standard', 'combo-anchored',
]

test('no mode references plugins outside its own directory', () => {
  for (const dir of MODE_DIRS) {
    const yml = readFileSync(join(root, dir, 'agent.cordis.yml'), 'utf8')
    const upward = [...yml.matchAll(/^[ \t]*name:[ \t]*\.\.\/\S+/gm)]
    assert.deepEqual(upward.map((m) => m[0].trim()), [], `${dir}/agent.cordis.yml must be self-contained`)
  }
})

test('materialized copies match shared/ sources (run: npm run sync)', () => {
  const result = spawnSync(process.execPath, [join(root, 'scripts', 'sync-modes.mjs'), '--check'], { encoding: 'utf8' })
  assert.equal(result.status, 0, `sync --check failed:\n${result.stdout}${result.stderr}`)
})
```
---

## 二.4　`better-sidebar` 的扩展点（暴露给第三方的注册 API）

**服务提供点（源码）**：`omdsh-dev_DSH-better-sidebar/src/client/index.tsx` 在 `apply()` 开头执行 `ctx.provide('betterSidebar', service)`；消费插件在 `inject` 里声明 `'betterSidebar'`。

**注册 API（函数名 + 签名，逐字，来源：`docs/external-plugin-guide.md` §7）**：
```ts
interface BetterSidebarService {
  /** 注册 tab 类型；返回 disposer */
  registerTab(descriptor: TabDescriptor): () => void
  /** 注册文件预览器；返回 disposer */
  registerFileViewer(descriptor: FileViewerDescriptor): () => void
  /** 当前已注册的 tab 描述符快照（同步，供 useSyncExternalStore 用；含被设置页禁用的类型） */
  getTabs(): readonly TabDescriptor[]
  /** 当前已注册的 file viewer 描述符快照（含被设置页禁用的 viewer） */
  getFileViewers(): readonly FileViewerDescriptor[]
  /** 按 id 查 tab 描述符 */
  getTab(id: string): TabDescriptor | undefined
  /** 某个 tab 类型是否在 Side card 设置中启用 */
  isTabEnabled(id: string): boolean
  /** 某个 file viewer 是否在 Side card 设置中启用 */
  isViewerEnabled(id: string): boolean
  /** 按 path 匹配 file viewer（priority 降序单趟：detect → exts；跳过硬禁用 viewer） */
  matchFileViewer(path: string, head?: Uint8Array): FileViewerDescriptor | undefined
  /** 打开一个 tab（+ 菜单和外部触发都用它；走 descriptor.dedupeKey 去重） */
  openTab(seed: OpenTabSeed, scope?: SessionScope): void
  /** 关闭一个 tab（未知 id 严格 no-op） */
  closeTab(tabId: string, scope?: SessionScope): void
  /** 订阅注册表变化（register/dispose 时触发） */
  subscribe(listener: () => void): () => void
  /** 插件版本（如 '0.17.1'；与 package.json 同步，测试守护） */
  readonly version: string
  /** 能力清单（只增不删）：'badge' | 'tabLifecycle' | 'updateTab' | 'openFile' | 'targetedOpen' |
   *  'stateSubscription' | 'tabMeta' | 'pluginSettings' | 'urlTarget' | 'settingSelect' */
  readonly features: readonly string[]
  /** 当前快照：激活 sessionId + 其状态 + prefs */
  getSnapshot(): SidebarSnapshot
  /** 订阅快照变化（会话切换/状态变更/prefs 写入）；返回 disposer */
  subscribeState(listener: () => void): () => void
  /** 更新一个已打开 tab 的显示字段（title/path/meta）；tab 不存在时 no-op */
  updateTab(tabId: string, patch: { title?: string; path?: string; meta?: unknown }): void
  /** 激活一个已打开的 tab（触发 descriptor.onActivate；未知 id 严格 no-op） */
  activateTab(tabId: string, scope?: SessionScope): void
  /** 在 scope.sessionId 的侧边栏编辑器打开一个文件 */
  openFile(scope: SessionScope, path: string, title?: string): void
}
```

**消费方最小骨架（逐字，来源：`docs/external-plugin-guide.md` §3 / §13）**：
```ts
// my-plugin/src/client/index.ts
import type {} from 'dsh-better-sidebar'          // 触发 ctx.betterSidebar 类型合并
import type { Context } from '@deepseek-ai/cordis'

export const inject = ['betterSidebar', 'slots']   // 声明服务依赖（slots 可选，按需）

export function apply(ctx: Context): void {
  // 注册一个 sidebar tab：ctx.effect 包裹 → 卸载时自动撤销注册（HMR-safe）
  ctx.effect(() =>
    ctx.betterSidebar.registerTab({
      id: 'my-plugin:db',
      title: () => 'Database',
      icon: <DbIcon />,
      order: 50,
      component: ({ scope }) => <DbView sessionId={scope.sessionId} />,
    })
  )

  // 注册一个文件预览器
  ctx.effect(() =>
    ctx.betterSidebar.registerFileViewer({
      id: 'my-plugin:csv',
      exts: ['csv'],
      fetchStrategy: 'custom',
      load: async (path, scope) => parseCsv(await fetchCsvBytes(scope, path)),
      component: ({ customData, path }) => <CsvGrid data={customData} path={path} />,
    })
  )
}
```

**`TabDescriptor` 完整字段（逐字，来源：§4.1；节选关键）**：
```ts
interface TabDescriptor {
  id: string                    // 唯一 id；也是 SidebarTab.type 的值。建议带包前缀：'my-plugin:db'
  title: string | (() => string)
  description?: string | (() => string)   // 一行说明；宿主只在 guide 条目 ≤ 4 条时渲染
  icon?: ReactNode | ((size: number) => ReactNode)
  order?: number                // + 菜单排序（升序）；默认 100
  hidden?: boolean              // 从 + 菜单隐藏
  available?: (ctx: Context, scope: SessionScope, state: SidebarState) => boolean
  single?: boolean              // ≡ dedupeKey: () => id
  dedupeKey?: (tab: SidebarTab) => string | undefined  // 必须纯函数：每次 open 求值两次
  createTab?: (state: SidebarState) => { tab: SidebarTab; patch?: Partial<SidebarState> } | null
  urlTarget?: (url: URL) => boolean
  settings?: SidebarSettingsDeclaration      // { toggles?, pluginToggles?, render? }
  badge?: (ctx, scope, state) => string | number | null | undefined
  onOpen?: (tab: SidebarTab, scope: SessionScope) => void
  onActivate?: (tab: SidebarTab, scope: SessionScope) => void
  onClose?: (tab: SidebarTab, scope: SessionScope) => void
  component: (props: TabComponentProps) => ReactNode
}
```

**消费方 `package.json` 声明（逐字，来源：§2.2 / §13）**：
```jsonc
{
  "name": "my-plugin",
  "version": "0.1.0",
  "main": "lib/index.js",
  "exports": {
    ".": { "types": "./lib/types/index.d.ts", "default": "./lib/index.js" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" }
  },
  "peerDependencies": {
    "@deepseek-ai/cordis": "^4.0.1",
    "dsh-better-sidebar": "workspace:*",
    "react": "^18.2.0"
  },
  "peerDependenciesMeta": {
    "dsh-better-sidebar": { "optional": true }
  }
}
```
> 关键：`dsh-better-sidebar` 必须是 **peerDependency**（不是 dependency，避免两份实例），且 `optional: true`（未装时你的插件照常加载）。

**能力的版本优雅降级（逐字，来源：§7）**：
```ts
if (ctx.betterSidebar.features.includes('badge')) {
  // 使用 TabDescriptor.badge
}
if (ctx.betterSidebar.version >= '0.12.0') { /* 字符串比较即可：minor 只增 */ }
```

**`better-sidebar` 自己的 `package.json` 关键字段（逐字，来源：`omdsh-dev_DSH-better-sidebar/package.json`）**：
```json
{
  "name": "dsh-better-sidebar",
  "version": "0.19.0",
  "type": "module",
  "main": "lib/index.js",
  "types": "lib/types/index.d.ts",
  "exports": {
    ".": { "types": "./lib/types/index.d.ts", "default": "./lib/index.js" },
    "./invariant": { "types": "./lib/types/invariant.d.ts", "default": "./lib/invariant.js" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" },
    "./client/service": { "types": "./lib/types/client/service.d.ts", "default": "./lib/client.js" },
    "./client/api": { "types": "./lib/types/client/service.d.ts", "default": "./lib/client.js" },
    "./src/*": "./src/*",
    "./package.json": "./package.json"
  },
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" },
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-locale",
        "@deepseek-ai/dsh-client-ui-slots",
        "@deepseek-ai/dsh-client-ui-conversation",
        "@deepseek-ai/dsh-client-ui-sidebar-right",
        "@deepseek-ai/dsh-client-modules"
      ],
      "platform": "web"
    }
  },
  "files": [
    "lib/index.js", "lib/invariant.js", "lib/client.js", "lib/client-registry.js",
    "lib/client-terminal.js", "lib/client-editor.js", "lib/client-mermaid.js",
    "lib/types/**/*.d.ts", "src", "scripts/install.sh", "scripts/install.ps1",
    "cordis.patch.yml", "README.md", "README_EN.md", "LICENSE"
  ],
  "scripts": {
    "build": "node -e \"require('node:fs').rmSync('lib',{recursive:true,force:true})\" && tsc -p tsconfig.build.json && tsdown",
    "prepublishOnly": "pnpm build",
    "test": "vitest run",
    "test:mount": "bash scripts/e2e-mount.sh",
    "check:consumer-types": "bash scripts/check-consumer-types.sh"
  },
  "peerDependenciesMeta": {
    "@huanlin/dsh-plugin-better-locale": { "optional": true },
    "@deepseek-ai/dsh-client-ui-sidebar-right": { "optional": true }
  }
}
```
> **注意 `files` 里必须带 `cordis.patch.yml`**（否则装上了不生效 —— 这是「漏带 patch 文件」的标准反例警戒点）。
---

## 二.5　`better-sidebar` 的退让表达式（`disabled: !!js`）—— 聚合包双挂载守卫

**`cordis.patch.yml` 全文**（来源：`omdsh-dev_DSH-better-sidebar/cordis.patch.yml`；长注释是「为什么这么写」的教材）：
```yaml
# dsh-better-sidebar bundle patch
#
# This file is the `dsh.bundle.patch` layer of the published npm package: when
# the plugin is installed through the official CLI —
#
#   dsh plugin --profile <name> add dsh-better-sidebar@<version>
#
# — the command reconciles `dsh.profile.bundles` against installed packages
# and, seeing this declaration, appends `dsh-better-sidebar` to the bundle
# stack. The profile boot then merges THIS patch (a single `insert` of the
# plugin row) exactly like the manual cordis.patch.yml mount line used
# before. No profile file edits needed — one command installs and mounts.
#
# If the profile still carries the old manual mount line in its own
# cordis.patch.yml, remove it before switching to the bundle channel to
# avoid double-mounting (two Node halves, two sidebars).
#
# To choose the terminal shell, add `config.shell` to the inserted plugin
# row (or to the profile's manual cordis.patch.yml mount line). When omitted,
# the host keeps resolving $SHELL / the login shell / powershell.exe.
# `config.shellArgs` optionally supplies explicit startup arguments; when
# non-empty they replace the automatic POSIX `-l` login flag:
#
#   - insert:
#       - id: better-sidebar
#         name: 'dsh-better-sidebar'
#         config:
#           shell: /bin/zsh
#           shellArgs:
#             - --noprofile
#             - --no-rc
#
# Aggregate double-mount guard: aggregate bundles (e.g. @linxin666/dsh-web-ui-all)
# may already mount this package under their own entry id (e.g.
# `web-ui-better-sidebar`). Two mounts register /sidebar/api twice and fail the
# whole plugin tree at boot ("duplicate prefix route"). The `!!js` disabled
# expression backs THIS row off when another *enabled* entry already mounts
# `dsh-better-sidebar`; the aggregate instance then owns the sidebar. The
# loader evaluates it when this row is processed (entry-list order, only rows
# before this one are visible), so the aggregate bundle must precede this one
# in `dsh.profile.bundles` — the standard install order, since `dsh plugin add`
# appends new bundles last. The reverse order (this bundle before the
# aggregate) is a known limitation: the guard cannot see rows that come after
# it, and no runtime singleton guard is added. Same-id manual duplicates still
# fail loudly at the loader as before.
- insert:
    - id: better-sidebar
      name: 'dsh-better-sidebar'
      disabled: !!js "[...ctx.loader.entries()].some((e) => e.options.name === 'dsh-better-sidebar' && e.options.id !== 'better-sidebar' && !e.disabled)"
```
> **这是本手册唯一一处 `disabled` 内使用 `!!js` 的真实生产范例**，且注释把「为什么行顺序重要」讲透了。

---

## 二.6　同类里代码量最小的组合包范本

**结论：`Q00_ouroboros/integrations/dsh-plugin/`（3 个文件，0 行 JS，1 个 `insert` 行）** 是本次四个仓库里、也是全仓清单里最小的「组合包」。

- 路径：生成期素材 `Q00_ouroboros/integrations/dsh-plugin/`（不随本 skill 发布）
- 文件：`package.json`（声明 `dsh.bundle.patch`）+ `cordis.patch.yml`（1 行 insert）+ `README.md`
- 对比：`better-sidebar` 组合包（同为零 JS bundle 层）也在用 `cordis.patch.yml`，但它的包里有完整 TS 源码 + 构建链；`dsh-desktop` 的组合包挂了 7 行并带 130 个源码文件。
- **推荐作为手册「第一个例子」**：把 ouroboros 的 `package.json` + `cordis.patch.yml` 直接当「最小可用组合包」模板（把 `name` 换成你的目标行、`config` 换成你的参数即可）。
- 全仓横向印证：本次扫描到 13 个仓库里共 20 个 `package.json` 声明了 `dsh.bundle`（含测试 fixture），最小的是 ouroboros 这一份。

---

# D · 三、本方向的开发规范（多家共识才叫「规范」）

> 说明：本节只把**至少两个仓库都这么做**的做法上升为「规范」，并在每条后面写清**依据**。只被单一仓库采用的做法标为「个别做法」，新手不必强行照抄。所有结论均来自本次读到的四个仓库源码 + 官方 DSH 源码交叉核对。

## 三.1 组合包（bundle）的规范

| 规范 | 依据（多家共识） | 说明 |
|---|---|---|
| 在 `package.json` 用 `dsh.bundle.patch` 指向**包根目录**的 `cordis.patch.yml` | ouroboros、dsh-desktop、better-sidebar 三家全中 | 值写成 `"./cordis.patch.yml"`，官方 `profile.ts` 会 `dirname(resolve(file)) + patch` 解析出补丁路径 |
| 补丁文件放在**包根目录**，不放 `src/` 里 | ouroboros、dsh-desktop、better-sidebar 三家全中 | 放 `src/` 里会因为 `files`/发布路径不对而在安装后丢失 |
| `files` 数组**必须**显式列出 `cordis.patch.yml` | 三家都在 `files` 里显式列了 `cordis.patch.yml` | 漏了它 → 包能装上、`dsh` 却读不到补丁 → **插件静默不生效**（详见 # 四 卡点 2） |
| 补丁用 `- insert:` 列表挂载插件行 | 三家一致 | 每行至少 `id` + `name`（`name` 是 npm 包名） |
| 覆盖已有行时用「带 `id`、不带 `insert`」的 override 形态 | dsh-desktop 明确使用（7 行 insert + 1 个 override）；官方复盘 0002 亦印证 | override **整块替换** `config`，不是深合并 → 只写要改的字段会丢掉其余字段 |
| `!!js` 只出现在 plugin `config` 的值里，或 entry 的 `disabled` 里 | 官方源码交叉印证 + ouroboros（config 内 6 处）+ better-sidebar（disabled 1 处） | 放在其它字段不会被求值，等于写了个死字符串 |
| 跨平台行为差异用 `disabled: !!js` 表达 | better-sidebar（聚合包双挂载守卫）为唯一真实范例；官方文档为此设计 | 求值上下文是「该 entry 被处理时的 injection-ready context」，**只能看到排在它之前**的行 |
| 可能启动失败的插件写 `failOnStartupError: false`（软失败） | ouroboros（`config.failOnStartupError: false`） | 缺依赖/缺 CLI 时不让整棵插件树崩，而是让该行降级 |
| 组合包里**零 JS** 是可行的、且是推荐起点 | ouroboros（0 行 JS） | 「组合包」本质是配置清单，不写运行时代码；需要逻辑才升级为 `dsh.client`/工具插件 |

## 三.2 包与发布（npm 工程）规范

| 规范 | 依据 | 说明 |
|---|---|---|
| 包名用 `dsh-<名>` 或 `dsh-plugin-<名>` | ouroboros(`dsh-ouroboros`)、dsh-desktop(`dsh-plugin-desktop`)、better-sidebar(`dsh-better-sidebar`) | 便于在 `dsh.profile.bundles` 里识别与社区检索 |
| `exports` 用 `{ "types": ..., "default": ... }` 双键 | dsh-desktop、better-sidebar 明确如此 | 只写 `default` 或只写 `main` 会让 `publint`/TS 解析告警 |
| **必须**导出 `"./package.json": "./package.json"` | dsh-desktop、better-sidebar 都显式导出 | 官方加载器/工具链会读包内 `package.json`（读 `dsh` 字段）；不导出会在部分解析模式下报 `ERR_PACKAGE_PATH_NOT_EXPORTED` |
| 所有 `@deepseek-ai/dsh-*` 依赖放 `peerDependencies` | better-sidebar 把它注入的 5 个 `dsh-client-*` 全放 peer | 避免同一套 host 被装出多份实例（多份实例会导致服务注册冲突，见 # 四 卡点 5） |
| 宿主/常驻服务类依赖放 `peerDependencies` 且标 `optional: true` | dsh-desktop 对宿主侧包如此处理 | 运行期由宿主提供，插件不自带 |
| 依赖的 `dsh-*` 包若只用于开发，提升进 `devDependencies` | anchored-standard、better-sidebar 都这么做 | 用 `pnpm peers check` 校验 peer 是否齐全 |

## 三.3 校验与测试规范（工程规范化方向的核心）

| 规范 | 依据 | 说明 |
|---|---|---|
| 提供统一 `check` 脚本 = build + typecheck + test + **真机挂载冒烟** | anchored-standard(`check`)、better-sidebar(`test:mount`)、dsh-desktop(`verify:closure/cli/loader/profile/licenses`) | 只跑单测不跑「真挂载」是新手最常漏的一环：单测全绿、装上却崩 |
| `prepack` / `prepublishOnly` 里跑 `check` | anchored-standard 明确把校验挂到发布钩子 | 防止没构建/没过检的包被发布 |
| 提供一致性门（`sync --check` 之类） | anchored-standard（`test/self-containment.test.mjs` 校验包内自包含） | 保证「仓库里的声明」和「发布产物」一致，不会出现补丁漏带 |
| 跨平台要有独立 CI 车道（Windows/Linux/macOS） | anchored-standard、better-sidebar 的坑都集中在平台差异（`/bin/bash`、大小写、CRLF） | 只在 Linux 跑 CI 会漏掉 Windows 全部路径/换行坑 |
| 回归测试必须能对「未修复代码」失败 | better-sidebar 的 271 个修复大多带回归测试 | 否则测试只是装饰，改坏了也发现不了 |
| 用 `publint` 校验发布形态 | 社区通行 + 各仓库 `exports` 写法一致 | 报 `exports` 键缺失、`main`/`types` 不匹配等 |

## 三.4 README / 文档规范

| 规范 | 依据 | 说明 |
|---|---|---|
| README 必备段落：定位（一句话）+ 安装命令（含 `--profile`）+ Requirements + 配置表 + FAQ + 来源目录 | ouroboros、dsh-desktop、anchored-standard、better-sidebar 全中 | 新手照着「安装命令」那一段逐字抄就能装上 |
| 安装命令必须写全 `dsh plugin --profile <名字> add <包名>` | 四家全中；官方 `args.ts` 里 `--profile` 是 `.requiredOption` | 省略 `--profile` 直接报错退出（详见 # 四 卡点 1） |
| 提供第三方扩展文档（若插件暴露扩展点） | better-sidebar(`docs/external-plugin-guide.md`) 为范本 | 有扩展点的插件，文档里要给出「函数名 + 签名 + 可抄示例」 |
| 双语（中/英）README | anchored-standard(`README.zh-CN.md`)、better-sidebar 均提供 | 面向中文新手建议至少提供中文版 |
| 在补丁注释里写清「为什么」 | ouroboros、better-sidebar 的 `cordis.patch.yml` 顶部都有大段注释 | 注释不是可选项：它解释了 id 选择、顺序敏感、如何覆盖 |

## 三.5 个别做法（不作为规范，仅记录）

- anchored-standard 的 `preset/agent.cordis.yml + preset.yml`（agent-plane 组合）是它自己的架构选择，不是所有插件都需要。
- dsh-desktop 用 `utilityProcess.fork` 起宿主进程，属于「桌面宿主」特有做法，普通插件不涉及。
- `isolate:` realm / `cordis:group` / `group: true` 只在需要服务隔离时使用，本次四个仓库里仅个别用到。

## 三.6 一句话总纲

> **组合包 = 一个 `package.json`（声明 `dsh.bundle.patch` + `files` 带上补丁）+ 一个 `cordis.patch.yml`（insert 若干行）；不写一行 JS 就能发布一个插件。所有工程规范（`exports`、`peerDependencies`、`check`、跨平台 CI）都是为了让这个组合包在别人机器上「装上就能跑」。**

---

# D · 四、新手最容易卡住的 5 个点（每点一句可执行建议）

> 排序按「新手实际撞上的概率 × 排查难度」从高到低。每条都附**现象 + 报错/原文 + 最省事的修法**。

## 卡点 1：安装命令漏了 `--profile`

- **一句话建议：任何 `dsh plugin` 安装/移除命令，都写全 `dsh plugin --profile <你的profile名> add <包名>`，`--profile` 永远不能省。**
- **现象**：照着某些 README 写 `dsh plugin add dsh-better-sidebar`，命令直接退出、什么都没装。
- **报错原文**：CLI 打出 `error: required option '--profile <name>' not specified`（官方 `apps/cli/src/args.ts` 里它是 `.requiredOption`，不是可选参数）。
- **根因**：DSH 是多 profile 设计，插件必须装进某个 profile 才有意义；CLI 用「必填参数」强制你指定。
- **正确写法**（逐字抄，把 `<名字>` 换掉）：
  ```
  dsh plugin --profile default add dsh-better-sidebar
  ```
- **备注**：`--profile` 的值要和 `dsh.profile.name` 一致；不确定就先用 `dsh profile list` 看有哪些。

## 卡点 2：`files` 漏了 `cordis.patch.yml` —— 包装上了、插件却「静默不生效」

- **一句话建议：发布前先跑 `npm pack --dry-run`，在文件清单里亲眼确认 `cordis.patch.yml` 在里面。**
- **现象**：`dsh plugin --profile default add 你的包` 成功；`package.json` 的 `dsh.profile.bundles` 也加上了包名；重启 DSH 后插件**完全没有任何效果**，也**没有任何报错**。这是最折磨人的「无声失败」。
- **根因**：`files` 是一份**白名单**。如果你写了 `"files": ["lib", "README.md"]` 却漏了 `cordis.patch.yml`，npm 打包时就把补丁文件排除在发布物之外。安装后 `dsh.bundle.patch` 指向 `./cordis.patch.yml` 这个**不存在的文件**，加载器读不到补丁行，于是跳过——不报错，只是不生效。
- **修法**（逐字改 `package.json`）：
  ```json
  "files": [
    "cordis.patch.yml",
    "README.md",
    "lib"
  ]
  ```
- **自检**：`npm pack --dry-run 2>&1 | grep cordis.patch.yml` 有输出才算过。

## 卡点 3：双挂载 —— 两个侧边栏 / 启动报 `duplicate prefix route`

- **一句话建议：从「手动挂载行」切换到「bundle 安装」时，先删掉 profile 里原有的手动 mount 行，再执行 `dsh plugin add`。**
- **现象**：界面上出现**两个侧边栏**（或两套同功能面板）；或启动直接失败，报 `duplicate prefix route`，整棵插件树起不来。
- **根因**：同一个插件被挂了两次。旧的手动 `insert` 行还在 profile 的 `cordis.patch.yml` 里，新装的 bundle 又插了一行 → 两个 Node 半边、两条 `/sidebar/api` 路由，路由前缀重复就报 `duplicate prefix route`。
- **修法**：
  1. 打开 profile 的 `cordis.patch.yml`，删掉手动的插件行；
  2. 只保留 bundle 那一行；
  3. 若无法删（被聚合包带上），用插件自带的 `disabled: !!js` 守卫退让（见 二.5 的 better-sidebar 范例）。
- **顺序敏感**：`!!js` 守卫**只能看到排在它之前**的行，所以聚合包必须在被退让的插件之前；`dsh plugin add` 默认把新 bundle 追加到最后，正是这个顺序。

## 卡点 4：子进程拿不到 API Key（凭据 scrub）+ profile 覆盖整块替换 `config`

- **一句话建议：别把密钥写进插件 `config`；子进程默认拿不到 `*KEY/*TOKEN/*SECRET/*PASSWORD` 和 `DSH_*` 环境变量，要用就自己显式透传。**
- **现象 A**：插件里 spawn 的子进程拿不到 `MY_API_KEY` / `DEEPSEEK_API_KEY`，请求 401。
- **根因 A**：`@deepseek-ai/dsh-subprocess` 在起子进程前会按 `SENSITIVE_ENV_PATTERN = /KEY|PASSWORD|SECRET|TOKEN/i` 以及 `DSH_*` 前缀**清洗环境变量**，防止把宿主的密钥泄露给第三方子进程。名字里带 `KEY`/`TOKEN`/`SECRET`/`PASSWORD` 的变量会被删掉。
- **修法 A**：给这类变量起一个不含敏感词的名字（如 `OUROBOROS_DSH_CONFIG_PATH`），或由插件在**自己的**配置里显式读取后再传给子进程。
- **现象 B**：profile 里覆盖某个插件行后，插件的其它配置「莫名其妙没了」。
- **根因 B**：override 形态（带 `id`、不带 `insert`）是**整块替换** `config`，**不是深合并**。只写 `config: { timeout: 1000 }` 会把原来的 `failOnStartupError` 等字段全部丢掉。
- **修法 B**：override 时**把要保留的字段一起写全**。

## 卡点 5：服务注册没包 `ctx.effect` / id 撞车 → `already registered`

- **一句话建议：每一次服务注册（`ctx.provide()` 等）都写进 `ctx.effect(() => { ...; return () => { /* 清理 */ } })`，并用全局唯一 id。**
- **现象**：热重载或二次挂载时报 `already registered`；或卸载后服务没清干净，重启出现「幽灵服务」。
- **根因**：把 `ctx.provide('xxx', ...)` 直接写在 `apply` 顶层，插件卸载/热重载时旧实例没有被清理，再次挂载就重复注册同名服务。
- **修法**（骨架，逐字可抄）：
  ```ts
  export const name = 'my-plugin'
  export const inject = ['sidebar']
  export function apply(ctx: Context) {
    ctx.effect(() => {
      const dispose = ctx.sidebar.register({ /* ... */ })
      return () => dispose()   // 卸载时一定要调
    })
  }
  ```
- **补充**：多个插件注册同一 id（例：两个插件都想占 `better-sidebar` 这个 id）也会报错；id 命名带上你的包名前缀最安全。

---

# 附、本次实际读取清单（可复核）

> 说明：以下均为**实际打开读过正文**的文件（不是目录列举）。四个仓库的 git 历史只含 commit 元数据（无文件 blob），故修复提交的「解释」来自 commit message 与其指向的 `.agents/notes` 文档，无法用 `git show <hash>:<path>` 取旧文件。

## 1. `Q00_ouroboros`（dsh-ouroboros）
- `src/Q00_ouroboros/integrations/dsh-plugin/package.json`（全文）
- `src/Q00_ouroboros/integrations/dsh-plugin/cordis.patch.yml`（全文，含顶部大段注释）
- `src/Q00_ouroboros/integrations/dsh-plugin/README.md`（全文）
- `src/Q00_ouroboros/README.md`（全文）
- `src/Q00_ouroboros/docs/guides/deepseek-harness.md`（全文）
- git 日志：`repos/Q00_ouroboros/`（commit 元数据）

## 2. `anywhere-labs_dsh-desktop`（dsh-plugin-desktop）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/package.json`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/cordis.patch.yml`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/README.md`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/src/host-process.ts`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/src/pnpm.ts`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/src/desktop-port.ts`（全文）
- `src/anywhere-labs_dsh-desktop/dsh-plugin-desktop/src/index.ts`（全文）
- `.agents/notes/implemented/architecture/` 下 7 篇中文设计说明：
  `packaged-profile-fallback`、`bundled-pnpm-runtime`、`profile-management`、`beta-isolated-host`、`runtime-renderer-recovery`、`startup-resource-ownership`、`plugin-install-lifecycle-ownership`
- git 日志：`repos/anywhere-labs_dsh-desktop/`（commit 元数据；多数 commit body 为空，解释在 `.agents/notes`）

## 3. `xiaobright_dsh-anchored-standard`
- `src/xiaobright_dsh-anchored-standard/package.json`（全文）
- `src/xiaobright_dsh-anchored-standard/README.zh-CN.md`（全文）
- `src/xiaobright_dsh-anchored-standard/preset/agent.cordis.yml`（全文/节选）
- `src/xiaobright_dsh-anchored-standard/preset/preset.yml`（全文）
- `src/xiaobright_dsh-anchored-standard/combo-anchored/preset.yml`（全文）
- `src/xiaobright_dsh-anchored-standard/test/self-containment.test.mjs`（全文）
- 完整 126 文件目录树（列举 + 关键文件阅读）
- git 日志：`repos/xiaobright_dsh-anchored-standard/`（commit 元数据）

## 4. `omdsh-dev_DSH-better-sidebar`
- `src/omdsh-dev_DSH-better-sidebar/package.json`（全文）
- `src/omdsh-dev_DSH-better-sidebar/cordis.patch.yml`（全文）
- `src/omdsh-dev_DSH-better-sidebar/dsh.plugin.json`（全文）
- `src/omdsh-dev_DSH-better-sidebar/AGENTS.md`（全文）
- `src/omdsh-dev_DSH-better-sidebar/README.md`（全文）
- `src/omdsh-dev_DSH-better-sidebar/docs/external-plugin-guide.md`（全文）
- `src/omdsh-dev_DSH-better-sidebar/src/client/service.ts`（全文）
- git 日志：`repos/omdsh-dev_DSH-better-sidebar/`（644 commits，其中 271 条修复类；逐条读 message 提炼）

## 5. 官方 DSH 源码（用于交叉验证机制）
- `deepseek-harness/packages/boot/app-boot/src/index.ts`（`!!js` 求值作用域、`anchorInsertedPluginNames()` 相对路径锚定）
- `deepseek-harness/packages/boot/app-boot/src/profile.ts`（`dsh.bundle.patch` 的读取与解析逻辑）
- `deepseek-harness/apps/cli/src/args.ts`（`--profile` 为 `.requiredOption`）

**合计：4 个目标仓库共约 34 个源码/文档文件实际读取全文或大段正文 + 官方 DSH 3 个源文件 + 4 份 git 日志（commit 元数据）。**

---

