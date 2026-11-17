# C 方向分册 · 服务 / 记忆 / 状态内核 / 配置组合

> **文件来源**：本文件由 `10-community-casebook.md` 拆分而来，正文为原文的**逐行搬迁**，未做改写。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。总索引见 `10-community-casebook.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

---

<!-- ↓ 源：C-services-state.md （全文） -->

# C. 服务 / 记忆 / 状态内核 / 配置组合方向

> 调研员：Explore-1　｜　方向：服务式 / 记忆 / 状态内核 / 配置组合
> 读者定位：零软件工程经验的新手。本文只写**能从本地真实源码与 git 历史中核实**的内容。
> 素材根目录（生成期，**不随本 skill 发布**）：`<社区仓库快照>/src/`
> git 历史（生成期，仅 commit 元数据）：`<社区仓库快照>/repos/`
> 注意：本环境的 git 快照**只有 commit 元数据，没有文件 blob**；`git show <hash>:<path>` 与 `git show --stat` 会报 `could not fetch ... from promisor remote`。因此所有"改动文件清单"类信息无法获取，本文只引用 commit 的标题与正文。

---

## 0. 结论速览（先看这张表）

| 仓库 | 目录名 | 真实 DSH 插件位置 | 插件形态 | `dsh.bundle` | `dsh.client` | 有证据的坑数 |
|---|---|---|---|---|---|---|
| MemTensor/MemOS | `MemTensor_MemOS` | `apps/memos-local-plugin/`（DSH 适配器在 `adapters/deepseek-harness/`） | **函数式插件**：具名 `name`/`inject`/`Config`/`apply` | 有 `./adapters/deepseek-harness/cordis.patch.yml` | 无 | 7 |
| huangruiteng/loopx | `huangruiteng_loopx` | `packages/dsh-loopx-plugin/` | **函数式插件 ×3 行** + 一个纯 class 服务 `GoalBarService` | 有 `./cordis.patch.yml` | 有（`inject` 4 个客户端服务 + `platform: web`） | 7 |
| tt-a1i/archify | `tt-a1i_archify` | `integrations/deepseek-harness/` | **bundle-only**：`lib/index.js` 只是 `!!js` 里复用的路径解析助手，并不是被 Loader 加载的插件 | 有 `./cordis.patch.yml` | 无 | 5 |

### 0.1 必须先纠正一个流行误解：这三个仓库都**没有**使用「default export 服务类」写法

任务背景里提到"服务式插件 default export 服务类"。**在这三个仓库中我没有找到任何一处**：

- `grep -rn "extends Service"` → 0 命中；
- `grep -rn "export default"` → 只有 `src/client/css-modules.d.ts` 里的 `export default classes`（CSS 模块类型声明，与插件无关）；
- 三个仓库的插件入口**全部**是**具名函数式插件**：`export const name` + `export const inject` +（可选）`export const Config` + `export function apply(ctx, config)`。

因此本方向真正可抄的"服务"范本不是"继承 Service 的类"，而是三步：

1. **发布一个服务**：`ctx.reflect.provide('服务名', 值)`（loopx `init-command.ts:631`）；
2. **消费一个服务**：`ctx.get('名字')` / `inject: [...]`；
3. **类本身只是普通 class**：`GoalBarService implements GoalBarServiceHandle`，不继承任何基类（loopx `goalbar/service.ts:213`），生命周期靠 `apply()` 里的 `ctx.effect(..., '描述')` 返回 disposer 接管。

> 要"写一个自己的服务"，请把"具名导出 + inject + apply + ctx.effect 回收 + ctx.reflect.provide"当成模板；不要学着写 `export default class extends Service`——本批仓库里没有任何活例子能给你抄。

---
## C · 一、挖坑（现象 → 根因 → 怎么修）

> 每个坑都标注：**仓库 + commit 短哈希 + 提交信息原文**。凡 git 历史里查不到的，一律写"未找到"，不编造。

### 1.1 MemOS（`@memtensor/memos-local-plugin`，DSH 适配器 `adapters/deepseek-harness/`）

#### 坑 M1 ★★★：启动恢复没有超时，把关机流程扣成人质 10 分钟

- **仓库 + commit**：`MemTensor_MemOS` + `ecf1092`（2026-08-26）`fix(core): bound startup recovery wait in shutdown to 15s (#2252)`
- **提交正文原文（节选）**：
  > `core.shutdown()` awaited `startupRecoveryPromise` with **no timeout**. With a large dirty episode and a slow/flaky LLM, the startup-recovery reflect chain (up to 163 sequential LLM calls at ~2min each) can take minutes — holding shutdown hostage until the systemd kill timer fires.
  > Observed 15 Aug 2026 on a production bridge: SIGTERM at 08:00:23, daemon stuck mid-recovery, systemd `TimeoutStopSec=600` expired, SIGKILL at 08:10:23. A 10-minute stop-sigterm wedge from a single unguarded await.
- **现象**：发一个 `SIGTERM`（Ctrl+C / 进程管理器停止）后，进程卡在启动恢复流程里，10 分钟后被 systemd 强杀。
- **根因**：`shutdown()` 里 `await startupRecoveryPromise` 没有超时保护；启动恢复会串行发起最多 163 次 LLM 调用，慢/抖动的 LLM 让这个 await 变成无界等待。
- **修复（逐字）**：
  ```ts
  await withTimeout(startupRecoveryPromise, 15_000, "startup_recovery_shutdown_timeout");
  ```
  提交正文解释了"为什么 15 秒是安全的"：
  - 这个 await 最初是为 issue #1808 加的，防止 `init → shutdown` 太快导致 SQLite 在刷盘中途被关；15 秒仍足以覆盖"0–1 个 episode"的恢复（毫秒级完成）。
  - 恢复是**设计上可续跑**的：脏 episode 带 `rewardDirty.failedAttempts`，周期性的 10 分钟重打分（rescore）会重跑它们，因此超时后放行**不丢数据**。
  - 超时后 `handle.shutdown()` 摘掉订阅者，daemon 的 `process.exit(0)` 触发，残留 LLM 调用再也无法扣住进程。
- **给新手的教训**：**任何"等待后台任务"的 await 都必须包一层超时**；同时要能说清"超时后到底丢没丢数据"。

#### 坑 M2 ★★：Viewer 静态根目录解析，在"干净构建"里选错目录

- **仓库 + commit**：`MemTensor_MemOS` + `b41c899`（2026-08-16）`fix(plugin): resolve DSH Viewer assets in clean builds (#2257)`
- **提交正文原文（节选）**：
  > Fix the DSH Viewer static-root resolution exposed by the 2.0.16 release dry run. In a clean checkout, the test job runs before `prepack` builds `viewer/dist`; the previous existence-based fallback therefore selected `apps/viewer/dist` instead of the plugin-owned Viewer directory.
  > The resolver now identifies the package root through its stable `package.json` marker, so both source (`adapters/deepseek-harness`) and packed (`dist/adapters/deepseek-harness`) layouts resolve to `<package>/viewer/dist` even before Viewer assets are built. A regression test covers both clean layouts, including a package root itself named `dist`.
- **现象**：2.0.16 的 GitHub release dry run 失败；本地干净 checkout 下找不到正确的 Viewer 静态目录。
- **根因**：用"目录是否存在"（`existsSync`）来猜包根；但干净构建时 Viewer 产物 `viewer/dist` 还没生成，于是 fallback 选到了错误的 `apps/viewer/dist`。
- **修复**：改用稳定的 `package.json` 标记来识别包根，而不是猜存在性。对应源码即 §2.4 的 `resolveDeepSeekHarnessViewerStaticRoot()`：先试 `runtimeRoot/package.json`，否则上跳一层。
- **给新手的教训**：**不要用"某目录存不存在"当作路径推导依据**——它在 dev 能用、在 CI/打包后必坏。用版本稳定的锚点文件（这里是 `package.json`）。

#### 坑 M3 ★★：Viewer 端口被占用（EADDRINUSE）时，宿主快速重启会把插件搞崩

- **证据**：源码 `adapters/deepseek-harness/index.ts`（第 300–373 行）+ 该插件 `README.md`：`Quick Viewer restarts are self-healing. If viewerPort is still transiently busy, recall, capture, and tools become available immediately while the adapter retries the Viewer bind five times over about 5.75 seconds.`
- **现象**：DSH 快速重启时，旧进程的 Cordis 回收（disposal）还没走完，新进程绑同一个 `viewerPort` → `EADDRINUSE` → 整个插件启动失败。
- **根因**：一次性 `await startViewer()` 绑定，没有区分"**临时**占用（旧进程正在退出）"和"**永久**错误（端口被别的程序占用 / bindHost 非法）"。
- **修复**（源码原文，逐字）：
  ```ts
  export const DEEPSEEK_HARNESS_VIEWER_RETRY_DELAYS_MS = [
    250,
    500,
    1_000,
    2_000,
    2_000,
  ] as const;
  ```
  只对 `EADDRINUSE` 做 5 次退避自愈（合计约 5.75s）；永久错误 fail-open、不做无限重试。并且重试**可被 Cordis 的 abort 取消**——`startViewerRetryAttempt()` 专门处理"abort 赢得了 race，但延迟的 bind 稍后成功了"这种 late success，把它关掉，避免泄漏 listener 或产生未处理的 rejection：
  ```ts
  // Abort won the race. Consume either eventual outcome so a delayed bind
  // cannot leak a listener or produce an unhandled rejection after disposal.
  void pending.then(async (lateViewer) => {
    try {
      await lateViewer.close();
    } catch {
      /* best-effort cleanup after an uncancellable late listen */
    }
  }).catch(() => undefined);
  ```
- **给新手的教训**：重试要有上限、要能被取消；**"取消之后迟到的成功"必须主动清理**，否则就是内存/端口泄漏。

#### 坑 M4 ★：原生依赖 onnxruntime 在 macOS 上析构崩溃

- **证据**：该插件 `README.md`（引用了上游 issue）
- **现象**：本机 embedding（Transformers.js + ONNX Runtime）在推理结束后，宿主调用 `process.exit()` 时崩溃；DSH 的优雅退出路径恰好会这么做。
- **根因**：旧的 Transformers.js 3.x / ONNX Runtime 1.21 组合存在 known macOS destructor crash（microsoft/onnxruntime#24579），由上游 environment-lifetime 改动修复。
- **修复**：把 Transformers.js 钉在 `4.2.0`、onnxruntime-node 钉在 `1.24.3`。README 原文：`Do not downgrade this dependency in a DSH profile that uses local embeddings.`
- **给新手的教训**：**原生依赖（.node/.dll/.so）版本不能随手降**；升级平台时优先核对上游 issue。

#### 坑 M5 ★★：pnpm 11 默认拦截构建脚本，首次安装报 `ERR_PNPM_IGNORED_BUILDS`

- **证据**：该插件 `README.md`：`A first tarball or registry install can therefore stop with ERR_PNPM_IGNORED_BUILDS even though the adapter itself is prebuilt.`
- **现象**：首次从 tarball 或 npm registry 安装，卡在 `ERR_PNPM_IGNORED_BUILDS`，**即使 adapter 本体已经预编译**。
- **根因**：`better-sqlite3` / `sharp` / `onnxruntime-node` / `esbuild` 等依赖自带 install script，pnpm 11 出于安全默认 block，必须由 profile 所有者逐个批准。
- **修复**：`dsh plugin --profile web approve-builds` 逐项审查后批准；**不要** `approve-builds --all`，**不要**盲目复制 allowlist（README 明确写了 `do not use approve-builds --all or copy this allowlist blindly`）。实测策略示例：
  ```yaml
  # $DSH_HOME/profiles/web/pnpm-workspace.yaml
  allowBuilds:
    '@memtensor/memos-local-plugin': false
    better-sqlite3: true
    esbuild: true
    onnxruntime-node: true
    protobufjs: false
    sharp: true
  ```
- **给新手的教训**：安装脚本以**当前用户权限**运行，且在 agent 工具沙箱之外。只批准你信得过的依赖。

#### 坑 M6 ★★：DSH 辅助推理能力快照在 adapter 更新 / HMR 后过期

- **仓库 + commit**：`MemTensor_MemOS` + `db4717e`（2026-08-28）`fix(plugin): consolidate local runtime hardening (#2286)`
- **提交正文原文（节选）**：
  > resolves DeepSeek Harness auxiliary reasoning capability from exact model metadata, with per-route TTL caching, concurrent lookup coalescing, adapter-update invalidation, and registration-bound race fallback.
- **现象**：辅助 LLM 调用会请求"关掉推理（off）"，但 adapter 拓扑变化后旧的"该模型不支持 off"结论仍然生效（或反之），行为错乱。
- **根因**：能力结论被缓存后，没有跟随 DSH adapter 更新失效。
- **修复**：按 route 做 TTL 缓存 + 并发查询合并 + 监听 adapter 更新失效 + 绑定 registration 的 race fallback。源码对应：
  ```ts
  /** Refresh exact-model capability snapshots whenever DSH replaces an adapter. */
  export function registerDeepSeekHarnessHostLlmCapabilityInvalidation(
    ctx: Context,
    bridge: DeepSeekHarnessHostLlmBridge,
  ): () => void {
    return ctx.on("llm/adapters-updated", () => {
      bridge.invalidateModelCapabilities();
    });
  }
  ```
- **给新手的教训**：任何跨 HMR 存活的缓存，都必须挂一个失效钩子（`ctx.on(...)`）。

#### 坑 M7 ★：Hermes bridge 状态过期 / PID 被复用

- **仓库 + commit**：`MemTensor_MemOS` + `068a701`（2026-08-26）`fix(plugin): reconcile stale Hermes bridge status`；`9119efe`（2026-08-24）正文提到 `preserves the OpenClaw stale/recycled PID lock fix from #2099`
- **现象**：bridge 守护进程已经死了/被系统回收，插件仍认为它在跑；或 PID 被别的进程复用时误判。
- **根因**：状态文件（PID/status）与真实进程不同步。
- **修复**：主动 reconcile（对账）状态；对 PID 复用做防护。
- **给新手的教训**：**用 PID 文件判断"进程还活着"不可靠**，必须二次校验（启动时间 / 命令行 / 文件锁）。

---

### 1.2 loopx（`dsh-loopx-plugin`）

#### 坑 L1 ★★★：DSH 升级到 0.1.5 后 GoalBar"载体"失效

- **仓库 + commit**：`huangruiteng_loopx` + `04fc3879`（2026-09-11）`fix(dsh): restore GoalBar on DSH 0.1.5 (#4209)`
- **提交正文原文**：
  > * fix(dsh): support the 0.1.5 GoalBar carrier
  > * test(dsh): pin the 0.1.5 GoalBar regression
- **现象**：升级到 DSH 0.1.5 后，GoalBar（浏览器里的目标条）不再工作/不再显示。
- **根因**：DSH 的 **Connection RPC 载体（carrier）**在 0.1.5 变了。旧代码固定用 `/loopx` 通道；新版本要走 DSH 的 shared API 通道 `/api`，端点也更名。
- **修复**（源码 `src/client/index.tsx:44-47` + `src/client/rpc.ts`，逐字）：
  ```ts
  const rpc = createGoalBarRpc(
    ctx.connection.rpc,
    Reflect.has(ctx.connection, 'generation'),
  )
  ```
  ```ts
  const GOALBAR_CHANNEL = '/loopx'
  const GOALBAR_SHARED_API_CHANNEL = '/api'
  const GOALBAR_SHARED_API_ENDPOINT = 'loopx.goalbar'
  // ...
  const carrier = await caller.call(
    sharedApi ? GOALBAR_SHARED_API_CHANNEL : GOALBAR_CHANNEL,
    sharedApi ? GOALBAR_SHARED_API_ENDPOINT : endpoint,
    request,
    signal,
  )
  ```
  即：用**能力探测**（`Reflect.has(ctx.connection, 'generation')`）而不是"读版本号"来决定走哪条通道。
- **给新手的教训**：跨版本兼容要用**能力探测**，不要硬编码版本号判断；并且为老/新载体各留一条路。

#### 坑 L2 ★★：peer 依赖范围把"自己实测的预发布版本"排除在外

- **证据**：`packages/dsh-loopx-plugin/package.json` + `smoke/dsh-peer-range-smoke.mjs`（逐字）
  ```js
  for (const [name, range] of Object.entries(manifest.peerDependencies ?? {})) {
    if (!name.startsWith('@deepseek-ai/')) continue
    const testedVersion = manifest.devDependencies?.[name]
    assert(testedVersion, `missing tested version for official peer ${name}`)
    assert(
      supportsPrerelease(range, testedVersion),
      `${name} tested version ${testedVersion} is excluded by peer range ${range}`,
    )
  }
  ```
  其中 `supportsPrerelease` 会逐 `||` 分支检查预发布 `tuplePrefix`（`1.2.3-`）。
- **现象**：插件在实测过的 DSH 预发布版本上装不上 / peer 报警。
- **根因**：DSH 用大量预发布版本（`0.1.0-rc.7`、`0.1.1-rc.1` …），peer range 必须显式列出每个预发布分支，很容易漏。
- **修复/防御**：写一个小脚本，断言"devDependencies 里记录的实测版本"一定被 peer range 覆盖。
- **给新手的教训**：**预发布版本不遵循普通 semver 区间**，必须在 peer range 里逐条写清；用脚本自证，别靠肉眼。

#### 坑 L3 ★★：发版产物不可从 GitHub Release 安装

- **仓库 + commit**：
  - `huangruiteng_loopx` + `d6e4691b`（2026-09-01）`fix(dsh): make plugin release-installable (#3784)`
  - `98183980`（2026-09-03）`fix(dsh): require target-install compatible LoopX (#3890)`
  - `ac3fd88d`（2026-09-07）`fix(dsh): declare canonical plugin repository metadata`
- **现象**：从 GitHub Release 的 `.tgz` 安装失败；或安装成功但启动即坏。
- **根因**：包清单/入口（`exports`/`files`）或 `repository` 元数据不完整；且依赖的 LoopX 版本不满足"DSH 管理的 `pip --target` 安装后还能发现 workflow skill 文件"。
- **修复**：补齐 `exports`/`files`/`repository`；要求 `loopx>=0.5.4`。README 原文：`Although 0.5.3 carried the workflow-skill files, 0.5.4 is the first release that discovers them after the plugin's Linux pip --target managed-runtime install.`
- **给新手的教训**：**发布物要真的拿 tarball 装一遍**；"我本地能跑"不等于"装得上"。

#### 坑 L4 ★★：会话身份不唯一 → 绑定歧义，GoalBar 静默消失

- **仓库 + commit**：`huangruiteng_loopx` + `30a6e05e`（2026-09-08）`fix(dsh): derive unambiguous local session identities`
- **证据（源码）**：`src/goalbar/service.ts:41` `const AMBIGUOUS_LOG_CODE = 'dsh_loopx_goalbar_binding_ambiguous'`，以及 `capture()` / `captureIsCurrent()`（第 284–314 行）
- **现象**：某个 Session 匹配到多个绑定 → 行被隐藏、动作被拒。
- **根因**：会话身份派生不唯一（同一 sessionId 关联到多个 agent/session 引用）。
- **修复**：严格校验——`String(agent.id) === sessionId && String(session.id) === sessionId && agent.session === session`（**同一对象引用**）且 `agent.status ∈ {idle, running}` 且 `cwd` 非空；歧义时记 `binding_ambiguous` 并 **fail closed（隐藏）**。
- **给新手的教训**：**ID 相等不等于对象是同一个**；状态内核里要同时校验"ID 相等 + 引用相等 + 状态合法"。

#### 坑 L5 ★★：重复动作 / 双击 Start 触发两次可变变更

- **证据（源码）**：
  - 服务端 `src/goalbar/service.ts:584-591`：`if (this.activeAction !== undefined) return { kind: 'rejected', code: 'action_in_flight' }`
  - 客户端 `src/client/useGoalBar.ts:253`：`actionGuardRef.current = true`，注释写着 `This ref closes the pre-render/same-frame duplicate-click window.`
- **现象**：用户连点两下 `Start`，发起两次 LoopX 生命周期变更。
- **根因**：没有"进行中"闸门。
- **修复**：服务端用 `activeAction: ActionAdmission` 拒绝第二个请求；客户端用 `actionGuardRef` 关闭渲染前的同帧重复点击窗口，且**只有显式 Refresh（或 Session generation 切换）才解锁**（拒绝/结果不确定时故意保持锁）。
- **给新手的教训**：任何会改状态的按钮，**前端锁 + 后端锁都要有**。

#### 坑 L6 ★★：HMR / 同页插件重挂后 CSS 残留

- **证据（源码，逐字注释）**：`src/client/index.tsx:26-37`
  ```tsx
  // Client module exports are cached across a same-page plugin reapply, so CSS
  // installation must be an explicit, idempotent apply-time operation.
  ensurePluginStyle()

  // Register ownership immediately after installation, before any later apply
  // step can fail, so Cordis rollback and ordinary unload both remove the tag.
  ctx.effect(() => () => {
    if (typeof document === 'undefined') return
    for (const style of document.querySelectorAll('style[data-plugin]')) {
      if (style.getAttribute('data-plugin') === PACKAGE_ID) style.remove()
    }
  }, 'dsh-loopx-plugin CSS ownership')
  ```
- **现象**：热重载后样式重复叠加或丢失。
- **根因**：客户端模块导出在"同页插件重挂"之间被缓存；`apply` 会被再次调用。
- **修复**：安装要**幂等**；卸载要**在 apply 早期就登记所有权**（早于任何后续可能失败的步骤），这样 Cordis 回滚和普通卸载都会清理。
- **给新手的教训**：客户端 `apply` 可能被调用多次——一切副作用都必须幂等 + 可回收。

#### 坑 L7 ★：监听器 / 订阅忘记回收

- **证据（源码）**：`src/client/index.tsx:39-42` 用 `ctx.effect(() => ctx.locale.register(...))`；`subscribeConnectionReset: listener => ctx.on('connection/reset', listener)`；`driver.ts:1169` 与 `observer.ts:608` 都用 `ctx.effect(function* () { ... yield async () => { await dispose() } })`
- **现象**：HMR 或卸载后监听器叠加，事件触发多次，或老对象不被回收。
- **根因**：手动 `ctx.on` 若不在 `ctx.effect` 内，卸载时不会被自动清理。
- **修复**：所有注册都放进 `ctx.effect(...)`，并在生成器末尾 `yield` 一个清理函数。
- **给新手的教训**：**每一个 `ctx.on` / 注册调用都要有人负责回收**，首选 `ctx.effect`。

### 1.3 archify（`@tt-a1i/archify-dsh`）

#### 坑 A1 ★★★：用仓库根安装插件，必失败

- **证据**：`integrations/deepseek-harness/README.md`（逐字）
  > Do **not** use `dsh plugin add tt-a1i/archify`: the repository root is not a DSH package and has no bundle metadata (see [#341](https://github.com/tt-a1i/archify/issues/341)).
- **现象**：`dsh plugin add tt-a1i/archify` 失败。
- **根因**：DSH 包在**子目录** `integrations/deepseek-harness/`（`package.json` 里的 `repository.directory` 指向它）；仓库根没有 `dsh.bundle` 元数据。
- **修复**：只装发布好的 npm 包并锁死版本：`dsh plugin --profile web add @tt-a1i/archify-dsh@0.1.0`；或传本地 `.tgz`。
- **给新手的教训**：**monorepo 里插件常常不在仓库根**；安装前先确认哪个 `package.json` 里写了 `dsh.bundle`。

#### 坑 A2 ★★★：在 `!!js` 里把包根当字符串拼到 `baseUrl` 上

- **证据（源码，逐字注释）**：`integrations/deepseek-harness/cordis.patch.yml`
  ```yaml
  # Opt-in Archify filesystem Skill provider for DeepSeek Harness.
  # Resolves the packaged Skill root from the installed npm identity anchored at
  # the DSH profile (Loader baseUrl), never as a path concatenated onto baseUrl.
  - insert:
      - id: archify-skill-filesystem
        name: '@deepseek-ai/dsh-skill-filesystem'
        config:
          providerName: archify-plugin
          includeDefaultRoots: false
          bundledSkillDir: !!js process.getBuiltinModule('node:path').join(process.getBuiltinModule('node:path').dirname(process.getBuiltinModule('node:module').createRequire(baseUrl).resolve('@tt-a1i/archify-dsh/package.json')), 'skills')
  ```
- **现象**：`bundledSkillDir` 解析不到，skill 加载失败。
- **根因**：`baseUrl` 是 DSH profile 的模块解析锚点，不是一个"包目录"；直接字符串拼接会拼错。
- **修复**：用 `createRequire(baseUrl).resolve('<包名>/package.json')` 走 Node 模块解析，再取 `dirname`，最后 `join(..., 'skills')`。同一套逻辑在 `lib/index.js` 里有一份可测试的复制：
  ```js
  export function resolveArchifySkillRoot(profileBaseUrl) {
    if (!profileBaseUrl) {
      throw new Error('archify-dsh: missing DSH profile baseUrl for package resolution');
    }
    let manifestPath;
    try {
      manifestPath = createRequire(profileBaseUrl).resolve(`${PACKAGE_NAME}/package.json`);
    } catch (error) {
      throw new Error(
        `archify-dsh: cannot resolve ${PACKAGE_NAME}/package.json from the DSH profile`,
        { cause: error },
      );
    }
    return join(dirname(manifestPath), 'skills');
  }
  ```
  并且有测试断言解析失败要"响亮地抛错，而不是猜一个 root"（`test/adapter-security.test.mjs:24-28`）。
- **给新手的教训**：**要定位"已安装的包"，永远走模块解析（`createRequire().resolve`），不要拼路径。**

#### 坑 A3 ★★：Windows 上打包不可移植

- **仓库 + commit**：`tt-a1i_archify` + `fc6e8ac`（2026-08-14）`fix: make DSH packaging portable on Windows (#70)`
- **现象**：Windows 上打包/安装失败。
- **根因**：路径分隔符 / 行尾（CRLF）处理不统一。
- **修复**：规范化。同目录还留有 Linux/macOS/Windows 三平台跑的发布验收 CI（`README.md`：`Release CI runs this on Linux, macOS, and Windows.`）。
- **给新手的教训**：**路径一律用 `node:path` 处理，别手写 `/` 或 `\`。**

#### 坑 A4 ★★：从"工作区未提交的改动"打包，产物与发布不符

- **证据**：`README.md`（逐字）
  > The pack command reads adapter files and release metadata from the current adapter Git HEAD blob: commit those changes before packing; working-tree edits are not package inputs.
- **相关 commit**：`2ead014`（2026-09-08）`fix(dsh): prepare reproducible 0.2.0 adapter with current Skill snapshot (#345)`
- **现象**：本地打包出来的包，内容和已提交的版本不一致；发布不可复现。
- **根因**：打包脚本从 Git **HEAD blob** 取文件，而不是工作区文件。
- **修复**：先 commit 再 pack；发布用 tag + 记录的 Skill commit，"不是移动的分支"。
- **给新手的教训**：**先提交、再打包**；"打包源是 git 而不是磁盘"是很常见的设计。

#### 坑 A5 ★：shell 产生的文件不会自动进 Web 的 Produced Files

- **证据**：`README.md`「Produced Files limitation」（逐字）
  > Files created by shell commands do **not** automatically appear in the Web Produced Files strip. Ask the agent to return the **exact workspace paths** of the specification JSON and the HTML artifact, then open those files from the workspace.
- **现象**：工具生成了 JSON/HTML，但 Web UI 的"产出文件"条里看不到。
- **根因**：DSH 的 Produced Files 只跟踪它自己认识的文件，shell 命令产出的不算。
- **修复**：让 agent 返回精确的工作区绝对路径，用户自行打开。
- **给新手的教训**：**"文件生成了"和"UI 里看得到"是两件事**，要在提示词里显式要求返回路径。

### 1.4 未找到 / 明确不存在的坑

- **服务重复注册冲突**：三个仓库均未找到"同一服务被注册两次"的修复提交。
- **配置校验失败导致插件不加载**：无专门修复提交；MemOS 用 fail-open（见 §2.1）而非"不加载"，loopx 的 observer 用"配置不全就完全 off"（见 §2.2）。
- **`ctx.provide` 时机问题（服务冲突）**：无修复提交；loopx 反而**刻意**用 `ctx.reflect.provide` 在 boot 后才发布（见 §2.2）。
- 声明：以上写"未找到"，**不代表没有**，只代表在这三仓库的 commit 元数据里没查到。

---

## C · 二、可抄代码模板（逐字照抄，超长标 `…(略)`）

### 2.0 三个插件的完整目录树

#### 2.0.1 MemOS —— `apps/memos-local-plugin/`（全仓 673 个文件；DSH 入口在 `adapters/deepseek-harness/`）

```
apps/memos-local-plugin/
├── .gitignore
├── .npmignore
├── ARCHITECTURE.md
├── CHANGELOG.md
├── README.md
├── adapters/                      # 每个宿主一个适配器
│   ├── ALGORITHMS.md
│   ├── README.md
│   ├── deepseek-harness/          ← DSH 适配器（本次重点）
│   │   ├── README.md
│   │   ├── bridge.ts
│   │   ├── cordis.patch.yml       ← dsh.bundle.patch
│   │   ├── deadline.ts
│   │   ├── host-llm.ts
│   │   ├── index.ts               ← 插件入口（name/inject/Config/apply）
│   │   └── tools.ts               ← 6 个 memos_* 工具
│   ├── hermes/                    # Python provider + 安装脚本
│   └── openclaw/                  # index.ts / bridge.ts / tools.ts
├── agent-contract/                # 跨适配器共享的 DTO / 事件 / 错误 / JSON-RPC
├── bridge/                        # JSON-RPC bridge（DSH 不用；OpenClaw/Hermes 用）
├── bridge.cts
├── bridge.mts
├── core/                          # 记忆内核：capture/embedding/llm/memory/storage/config…
├── docs/
├── install.sh
├── openclaw.plugin.json
├── package-lock.json
├── package.json
├── pnpm-lock.yaml
├── scripts/
├── server/                        # 进程内 HTTP/SSE Viewer 后端
├── templates/                     # config.<agent>.yaml
├── tests/                         # 205 个文件（unit/integration/e2e/python 等）
├── tsconfig.build.json
├── tsconfig.json
├── tsconfig.viewer.json
├── viewer/                        # 64 个文件，Preact Viewer 前端
├── vite.config.ts
├── vitest.config.ts
└── website/
```

注：插件根另有 Windows 版安装脚本（与 `install.sh` 同名不同扩展名）。`adapters/deepseek-harness/` 只有 **7 个文件**，其余 660+ 是共享内核 / 测试 / Viewer。**新手只需盯住这 7 个文件的入口约定**。

#### 2.0.2 loopx —— `packages/dsh-loopx-plugin/`（全仓 51 个文件，`find ... | sort` 原始结果）

```
packages/dsh-loopx-plugin/
├── .gitignore
├── LICENSE
├── NOTICE
├── README.md
├── cordis.patch.yml
├── install.sh
├── package.json
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
├── scripts/build.mjs
├── smoke/Dockerfile.clean
├── smoke/dsh-clean-docker-probe.mjs
├── smoke/dsh-clean-docker-smoke.sh
├── smoke/dsh-client-artifact-smoke.mjs
├── smoke/dsh-goalbar-runtime-smoke.mjs
├── smoke/dsh-peer-range-smoke.mjs
├── smoke/dsh-profile-smoke.mjs
├── src/cli.ts
├── src/client/LoopXGoalBar.tsx
├── src/client/css-modules.d.ts
├── src/client/goalbar.module.css
├── src/client/index.tsx
├── src/client/locale.ts
├── src/client/rpc.ts
├── src/client/useGoalBar.ts
├── src/driver.ts
├── src/goalbar/connection-rpc.ts
├── src/goalbar/events.ts
├── src/goalbar/protocol.ts
├── src/goalbar/read-model.ts
├── src/goalbar/service.ts
├── src/index.ts
├── src/init-command.ts
├── src/managed-runtime.ts
├── src/observer.ts
├── tests/admission-closeout.integration.spec.ts
├── tests/cli.spec.ts
├── tests/driver.spec.ts
├── tests/goalbar-client.spec.tsx
├── tests/goalbar-connection.spec.ts
├── tests/goalbar-protocol.spec.ts
├── tests/goalbar-read-model.spec.ts
├── tests/goalbar-service.spec.ts
├── tests/init-command.spec.ts
├── tests/observer.spec.ts
├── tsconfig.client.json
├── tsconfig.host.json
├── tsconfig.json
├── tsconfig.tests.json
├── tsdown.client.config.ts
└── tsdown.config.ts
```

#### 2.0.3 archify —— `integrations/deepseek-harness/`（全仓 21 个文件，`find ... | sort` 原始结果）

```
integrations/deepseek-harness/
├── .gitignore
├── README.md
├── cordis.patch.yml
├── lib/index.js
├── package.json
├── release.json
├── scripts/distribution-acceptance.mjs
├── scripts/pack.mjs
├── scripts/release-source.mjs
├── scripts/resolve-cli.mjs
├── scripts/transient-retry.mjs
├── test/adapter-security.test.mjs
├── test/adapter-staging.test.mjs
├── test/docs-contract.test.mjs
├── test/package-contract.test.mjs
├── test/probe-skills.mjs
├── test/probe-skills.test.mjs
├── test/resolve-cli.test.mjs
├── test/tarball-contract.test.mjs
├── test/transient-retry.test.mjs
└── test/zero-regression.test.mjs
```

⚠️ 注意：**这个目录里没有 `src/`，也没有客户端半侧**。它的 `lib/index.js` 不是被 Loader 加载的插件，而是给 `cordis.patch.yml` 的 `!!js` 表达式做同构的、可测试的路径解析助手（见坑 A2）。`dsh.bundle` 指向的 patch 里插入的是 DSH 自带的 `@deepseek-ai/dsh-skill-filesystem`。

### 2.1 archify `package.json`（全文）

```json
{
  "name": "@tt-a1i/archify-dsh",
  "version": "0.2.0",
  "description": "Opt-in DeepSeek Harness Skill-only bundle for the Archify architecture-diagram skill.",
  "license": "MIT",
  "type": "module",
  "main": "./lib/index.js",
  "exports": {
    ".": "./lib/index.js",
    "./package.json": "./package.json"
  },
  "files": [
    "lib",
    "cordis.patch.yml",
    "skills",
    "README.md",
    "LICENSE",
    "release.json"
  ],
  "keywords": [
    "dsh-plugin",
    "deepseek-harness",
    "agent-skill",
    "architecture-diagram"
  ],
  "engines": {
    "node": "^22.19.0 || >=24.0.0"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/tt-a1i/archify.git",
    "directory": "integrations/deepseek-harness"
  },
  "homepage": "https://github.com/tt-a1i/archify/tree/main/integrations/deepseek-harness",
  "bugs": "https://github.com/tt-a1i/archify/issues",
  "publishConfig": {
    "access": "public"
  },
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    }
  }
}
```

### 2.2 MemOS `package.json`（全文；此处为前半段，后半段见 2.2b）

```json
{
  "name": "@memtensor/memos-local-plugin",
  "version": "2.0.16-beta.1",
  "description": "Reflect2Evolve memory plugin: layered L1/L2/L3 memory, reflection-weighted value backprop, cross-task policy induction, skill crystallization, and three-tier retrieval for OpenClaw, Hermes Agent, and DeepSeek Harness.",
  "type": "module",
  "main": "dist/core/index.js",
  "types": "dist/core/index.d.ts",
  "openclaw": {
    "id": "memos-local-plugin",
    "kind": "memory",
    "extensions": [
      "./dist/adapters/openclaw/index.js"
    ],
    "installDependencies": true
  },
  "dsh": {
    "bundle": {
      "patch": "./adapters/deepseek-harness/cordis.patch.yml"
    }
  },
  "files": [
    "dist",
    "telemetry.credentials.json",
    "openclaw.plugin.json",
    "bridge.cts",
    "bridge.mts",
    "bridge/**/*.ts",
    "core/**/*.ts",
    "core/storage/migrations/*.sql",
    "agent-contract/**/*.ts",
    "server/**/*.ts",
    "adapters/openclaw/**/*.ts",
    "adapters/openclaw/*.sh",
    "adapters/deepseek-harness/cordis.patch.yml",
    "adapters/hermes/*.sh",
    "adapters/hermes/plugin.yaml",
    "adapters/hermes/memos_provider/*.py",
    "templates/*.yaml",
    "templates/README.user.md",
    "viewer/dist",
    "scripts/postinstall.cjs",
    "scripts/sync-hermes-version.cjs",
    "install.sh",
    "...(安装脚本与其余 files 条目略)",
    "!**/ALGORITHMS.md",
    "!**/README.md",
    "adapters/deepseek-harness/README.md",
    "!**/__pycache__",
    "!**/*.pyc",
    "!**/.gitkeep",
    "!**/*.map",
    "!dist/tests",
    "!dist/tests/**"
  ],
  "scripts": {
    "build": "tsc -p tsconfig.build.json && node scripts/copy-runtime-assets.cjs",
    "build:viewer": "vite build --config vite.config.ts",
    "build:package": "npm run build && npm run build:viewer",
    "prepack": "npm run check:hermes-version && npm run build:package",
    "sync:hermes-version": "node scripts/sync-hermes-version.cjs",
    "check:hermes-version": "node scripts/sync-hermes-version.cjs --check",
    "release:validate": "npm run check:hermes-version && npm run lint && npm test",
    "dev": "tsc -p tsconfig.json --watch",
    "viewer:dev": "vite --config vite.config.ts",
    "bridge": "tsx bridge.cts",
    "bridge:daemon": "tsx bridge.cts --daemon",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:e2e": "vitest run tests/e2e",
    "lint": "tsc -p tsconfig.json --noEmit",
    "postinstall": "node scripts/postinstall.cjs"
  },
  "keywords": [
    "memory",
    "agent",
    "reflect2evolve",
    "self-evolution",
    "skill-crystallization",
    "openclaw",
    "hermes",
    "deepseek-harness",
    "dsh-plugin"
  ],
  "license": "MIT",
  "engines": {
    "node": ">=20.0.0"
  },
```
  "dependencies": {
    "@huggingface/transformers": "4.2.0",
    "@preact/signals": "^2.9.0",
    "@sinclair/typebox": "^0.34.48",
    "better-sqlite3": "^12.10.0",
    "preact": "^10.29.1",
    "tsx": "^4.21.0",
    "uuid": "^10.0.0",
    "yaml": "^2.6.0"
  },
  "peerDependencies": {
    "@deepseek-ai/cordis": "^4.0.1",
    "@deepseek-ai/dsh-agent": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/dsh-llm": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/dsh-session": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/dsh-system-prompt": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/dsh-timeout": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/dsh-tools": ">=0.1.0-rc.5 <0.2.0",
    "@deepseek-ai/schemastery": "^3.18.1"
  },
  "peerDependenciesMeta": {
    "@deepseek-ai/cordis": { "optional": true },
    "@deepseek-ai/dsh-agent": { "optional": true },
    "@deepseek-ai/dsh-llm": { "optional": true },
    "@deepseek-ai/dsh-session": { "optional": true },
    "@deepseek-ai/dsh-system-prompt": { "optional": true },
    "@deepseek-ai/dsh-timeout": { "optional": true },
    "@deepseek-ai/dsh-tools": { "optional": true },
    "@deepseek-ai/schemastery": { "optional": true }
  },
  "devDependencies": {
    "@deepseek-ai/cordis": "^4.0.1",
    "@deepseek-ai/dsh-agent": "0.1.0-rc.6",
    "@deepseek-ai/dsh-llm": "0.1.0-rc.6",
    "@deepseek-ai/dsh-session": "0.1.0-rc.6",
    "@deepseek-ai/dsh-system-prompt": "0.1.0-rc.6",
    "@deepseek-ai/dsh-timeout": "0.1.0-rc.6",
    "@deepseek-ai/dsh-tools": "0.1.0-rc.6",
    "@deepseek-ai/schemastery": "^3.18.1",
    "@preact/preset-vite": "^2.10.5",
    "@types/better-sqlite3": "^7.6.12",
    "@types/node": "^22.10.0",
    "@types/uuid": "^10.0.0",
    "typescript": "^5.7.0",
    "vite": "^5.4.10",
    "vitest": "^2.1.9"
  }
}
```

### 2.2b MemOS `cordis.patch.yml`（全文，逐字）

```yaml
- insert:
    - id: memos-local-memory
      name: '@memtensor/memos-local-plugin/dist/adapters/deepseek-harness/index.js'
      config:
        enabled: true
        profileId: default
        home: ''
        recallEnabled: true
        captureEnabled: true
        toolsEnabled: true
        hostLlmEnabled: true
        viewerEnabled: true
        viewerPort: 18801
        recallTimeoutMs: 3000
        contextMaxChars: 6000
        toolResultMaxChars: 1200
        failOnStartupError: false
```

要点：patch 里用的是**编译后**路径 `dist/adapters/deepseek-harness/index.js`（不是 `src`）；`name` 是包内相对导出，`config` 与插件 `Config` 的字段一一对应。

### 2.3 【核心范本·服务生命周期】MemOS DSH 适配器插件头 + Config（`adapters/deepseek-harness/index.ts`，逐字）

```ts
/** Native Cordis adapter for DeepSeek Harness. */

import type { Context } from "@deepseek-ai/cordis";
import type { PreStepDecision } from "@deepseek-ai/dsh-agent";
import { createUserMessage } from "@deepseek-ai/dsh-llm";
import type { Session, SessionEvent } from "@deepseek-ai/dsh-session";
import type {} from "@deepseek-ai/dsh-system-prompt";
import Schema from "@deepseek-ai/schemastery";
// …(其余 import 略)

export const name = DEEPSEEK_HARNESS_PLUGIN;
export const inject = ["systemPrompt", "tools", "llm"];
export const DEEPSEEK_HARNESS_VIEWER_PORT = 18_801;
export const DEEPSEEK_HARNESS_VIEWER_RETRY_DELAYS_MS = [
  250,
  500,
  1_000,
  2_000,
  2_000,
] as const;
export const DEEPSEEK_HARNESS_MAX_FOREGROUND_SEARCH_MS = 3_000;

export interface Config {
  enabled: boolean;
  profileId: string;
  home: string;
  recallEnabled: boolean;
  captureEnabled: boolean;
  toolsEnabled: boolean;
  hostLlmEnabled: boolean;
  viewerEnabled: boolean;
  viewerPort: number;
  recallTimeoutMs: number;
  contextMaxChars: number;
  toolResultMaxChars: number;
  failOnStartupError: boolean;
}

export const Config: Schema<Config> = Schema.object({
  enabled: Schema.boolean().default(true),
  profileId: Schema.string().default("default"),
  home: Schema.string().default(""),
  recallEnabled: Schema.boolean().default(true),
  captureEnabled: Schema.boolean().default(true),
  toolsEnabled: Schema.boolean().default(true),
  hostLlmEnabled: Schema.boolean().default(true),
  viewerEnabled: Schema.boolean().default(true),
  viewerPort: Schema.number().step(1).min(1).max(65_535).default(
    DEEPSEEK_HARNESS_VIEWER_PORT,
  ),
  recallTimeoutMs: Schema.number().min(100).default(3_000),
  contextMaxChars: Schema.number().min(256).default(6_000),
  toolResultMaxChars: Schema.number().min(128).default(1_200),
  failOnStartupError: Schema.boolean().default(false),
});
```

**可抄点**：
1. `name` / `inject` / `Config` **全部具名导出**，`inject` 是**字符串数组**，列出本插件要用到的 DSH 服务；
2. `interface Config` 与 `const Config: Schema<Config>` **同名共存**（TS 里接口与值可同名）；
3. `Schema.boolean().default(true)` 用 schemastery **给每个字段默认值**，并可用 `.min/.max/.step` 约束数值。

### 2.4 【核心范本·副作用回收】MemOS `apply()` 的"注册表 + 统一回滚 + 卸载 disposer"（逐字，中间略）

```ts
/** Bootstrap MemOS and register all lifecycle hooks as one Cordis plugin. */
export async function apply(
  ctx: Context,
  config: Config,
): Promise<() => Promise<void>> {
  if (!config.enabled) return async () => undefined;

  const configuredHome = defaultDeepSeekHarnessHome(config.home);

  let core: MemoryCore | undefined;
  let bridge: ReturnType<typeof createDeepSeekHarnessBridge> | undefined;
  let viewer: ServerHandle | undefined;
  let viewerRetryController: AbortController | undefined;
  let viewerRetryTask: Promise<void> | undefined;
  let disposing = false;
  const registrations: Array<() => void> = [];
  const unregisterAll = (): void => {
    for (const unregister of registrations.splice(0).reverse()) {
      try {
        unregister();
      } catch (error) {
        ctx.logger.warn(`memos-local-memory: registration rollback failed: ${String(error)}`);
      }
    }
  };
  try {
    // …(第 248–400 行：解析 home、loadConfig、建 hostLlmBridge、bootstrapMemoryCore、启动 Viewer 略)

    registrations.push(ctx.systemPrompt.section({
      name: "tool:memos-local-memory",
      order: 114,
      text: deepSeekHarnessMemoryGuidance(config.toolsEnabled),
    }));

    registrations.push(ctx.on("agent/pre-step", async (payload, next): Promise<PreStepDecision> => {
      return bridge!.beforeStep(
        payload as unknown as DshPreStepPayloadLike,
        next as unknown as () => Promise<DshPreStepDecisionLike>,
      ) as unknown as Promise<PreStepDecision>;
    }));

    registrations.push(ctx.on("session/event", (session: Session, event: SessionEvent): void => {
      bridge!.onSessionEvent(
        session as unknown as DshSessionLike,
        event as unknown as DshSessionEventLike,
      );
    }));

    registrations.push(ctx.on("session/disposed", (session: Session): void => {
      // Session disposal is intentionally detached from DSH's request path.
      // The bridge serializes close after this session's queued lifecycle work;
      // Cordis disposal remains the one place that drains all queues.
      void bridge!.closeSession(session as unknown as DshSessionLike).catch((error) => {
        ctx.logger.warn(
          `memos-local-memory: detached session cleanup failed: ${String(error)}`,
        );
      });
    }));

    if (config.toolsEnabled) {
      registrations.push(registerDeepSeekHarnessTools(ctx, {
        core,
        profileId: config.profileId,
        maxBodyChars: config.toolResultMaxChars,
        searchTimeoutMs: foregroundSearchTimeoutMs,
        currentEpisode: (session) => bridge!.currentEpisode(session),
        runWithLlmRoute: (route, operation) => routes.run(route, operation),
      }));
    }

    ctx.logger.info(
      `memos-local-memory: ready (home=${home.root}, recall=${String(config.recallEnabled)}, ` +
      // …(日志其余略)
    );
  } catch (error) {
    disposing = true;
    unregisterAll();
    viewerRetryController?.abort();
    if (viewerRetryTask) await viewerRetryTask;
    if (viewer) {
      try {
        await viewer.close();
      } catch {
        /* best-effort cleanup after failed bootstrap */
      }
    }
    if (bridge) await bridge.dispose();
    else if (core) await core.shutdown();
    const message = error instanceof Error ? error.message : String(error);
    ctx.logger.warn(`memos-local-memory: startup failed: ${message}`);
    if (config.failOnStartupError) throw error;
    return async () => undefined;
  }

  return async () => {
    disposing = true;
    unregisterAll();
    viewerRetryController?.abort();
    if (viewerRetryTask) await viewerRetryTask;
    if (viewer) {
      try {
        await viewer.close();
      } catch (error) {
        ctx.logger.warn(`memos-local-memory: viewer close failed: ${String(error)}`);
      }
    }
    await bridge!.dispose();
    ctx.logger.info("memos-local-memory: stopped");
  };
}
```

**可抄点（这是"服务/内存密级插件"的标准骨架）**：
1. `apply` 是 `async`，**返回一个卸载函数** `() => Promise<void>`；
2. 所有注册（`ctx.on` / `ctx.systemPrompt.section` / `ctx.tools.register` / 自定义 `register*`）的返回值都 `push` 进一个 `registrations` 数组，**每个注册函数都返回自己的 disposer**；
3. `unregisterAll()` **倒序** `splice(0).reverse()` 逐个调用，且**每个都 try/catch**（一个回滚失败不能挡住其余）；
4. `catch` 里做**全量回滚**（`unregisterAll` + abort 重试 + close viewer + dispose bridge / shutdown core），再按 `failOnStartupError` 决定"抛出"还是"返回空卸载函数、让宿主继续跑"；
5. `disposing` 标志位让"重试中迟到的成功"知道自己该收尾。

### 2.5 MemOS 工具模板：`parameters`（DSH DSL）与 `output.schema`（标准 JSON Schema）（逐字，节选）

```ts
/** Read-oriented MemOS tools exposed through DeepSeek Harness. */

import type { Context } from "@deepseek-ai/cordis";
import { defineTool, type JsonValue } from "@deepseek-ai/dsh-tools";
// …(import 略)

const JSON_OUTPUT = {
  schema: {
    type: "object" as const,
    additionalProperties: true,
    properties: {
      text: { type: "string" as const, required: true },
    },
  },
  render: (_args: unknown, value: Record<string, unknown>) => [{
    type: "text" as const,
    text: typeof value["text"] === "string"
      ? value["text"]
      : JSON.stringify(value),
  }],
} as const;

export function registerDeepSeekHarnessTools(
  ctx: Context,
  options: DeepSeekHarnessToolsOptions,
): () => void {
  const bodyCap = options.maxBodyChars;
  const searchTimeoutMs = options.searchTimeoutMs ?? 3_000;
  const now = options.now ?? (() => Date.now());
  const disposers: Array<() => void> = [];

  try {
    disposers.push(ctx.tools.register(defineTool({
      name: "memos_search",
      description:
        "Search long-term MemOS memory across prior traces, learned policies, world models, and skills. " +
        "Use this before claiming that earlier user context is unavailable.",
      parameters: {
        query: {
          type: "string",
          required: true,
          description: "A concise free-text memory query.",
        },
        maxResults: {
          type: "integer",
          description: "Maximum results per tier (1-50).",
        },
        tier1topK: { type: "integer", description: "Skill result limit (0-100)." },
        tier2topK: { type: "integer", description: "Trace/policy result limit (0-100)." },
        tier3topK: { type: "integer", description: "World-model result limit (0-100)." },
        sessionScope: {
          type: "boolean",
          description: "Restrict results to the current DSH session.",
        },
      },
      output: JSON_OUTPUT,
      isConcurrencySafe: () => true,
      async execute(args, exec) {
        const query = requireText(args.query, "query");
        // …(execute 主体略)
      },
    })));
    // …(其余 5 个工具同样 disposers.push(ctx.tools.register(defineTool({ ... }))) 略)
  } catch (error) {
    disposeAll(disposers);
    throw error;
  }

  return () => disposeAll(disposers);
}

function disposeAll(disposers: Array<() => void>): void {
  for (const dispose of disposers.splice(0).reverse()) dispose();
}
```

**可抄点 1 —— 两种 `required` 写法千万别混**（本手册的硬规则）：
- **`parameters` 用 DSH 自研 DSL**：必需参数写在**属性级** `required: true`（见上面 `query`）。
- **`output.schema` 用标准 JSON Schema**：对象级 `required: ['a','b']` 数组。
- 从源码可确认：`parameters.query.required: true`（属性级）、`output.schema.properties.text.required: true`（也是属性级，因为它走的是另一种渲染 DSL）；而标准 JSON Schema 对象级的 `required` 是**数组**，两者语法语义不同，**不可互相搬用**。

**可抄点 2 —— 工具注册的失败安全**：`register*` 函数内部维护 `disposers` 数组，整个注册包在 `try/catch` 里；任何一个工具注册失败就 `disposeAll` 已注册的、再把错误抛出去；成功则返回 `() => disposeAll(disposers)`。这与 §2.4 的 `registrations` 是**同一个模式**，只是作用域更小。

### 2.6 【最小范本·服务生命周期】loopx 包根 Host 插件（`src/index.ts` 全文，逐字，共 29 行；⚠️ **该快照取自 loopx `e602dd9273`** —— 上游已前移到 `26eaefc214`，**同一文件现为 75 行**（已重写）。下面的逐字全文是**当时**的形态，抄之前请先取上游最新）

```ts
import type { Context } from '@deepseek-ai/cordis'
import type { Agent } from '@deepseek-ai/dsh-agent'
import {
  registerGoalBarConnectionTransport,
} from './goalbar/connection-rpc.ts'
import { goalBarCoordinator } from './goalbar/events.ts'
import { createGoalBarService } from './goalbar/service.ts'
import { resolvePluginLoopXCommand } from './managed-runtime.ts'

export const name = 'dsh-loopx-plugin'
export const inject = ['agents', 'connection', 'loopxBootstrap']

/** Package-root Host plugin: one GoalBar service, never a second Driver. */
export function apply(ctx: Context): void {
  ctx.effect(() => {
    const service = createGoalBarService({
      getAgent: sessionId => ctx.agents.get(sessionId as Agent['id']),
      coordinator: goalBarCoordinator,
      resolveCommand: signal => resolvePluginLoopXCommand({ signal }),
      warn: message => { ctx.logger.warn(message) },
    })
    const disposeRpc = registerGoalBarConnectionTransport(ctx.connection, service)
    return async () => {
      await service.dispose()
      await disposeRpc()
    }
  }, 'dsh-loopx GoalBar Host service')
}
```

**为什么它是最佳"服务"起手范本**：
- 只有 `name` + `inject` + `apply` 三件套，**没有 Config**（loopx 这个包不读 Cordis config，见 §三）；
- `apply` 是**同步**的（`(): void`），所有异步初始化都封在 `ctx.effect` 的回调里；
- `ctx.effect(() => { ...; return async () => { await service.dispose(); await disposeRpc() } }, '描述')` —— **effect 回调返回 disposer**，Cordis 卸载时自动调用；
- `inject: ['agents', 'connection', 'loopxBootstrap']` 一眼看出依赖 3 个服务，其中 `loopxBootstrap` 是**自家**在其他行 `provide` 出来的。

### 2.7 【最小范本·条件关闭】loopx 影子观察者入口（`src/observer.ts` 末尾，逐字）

```ts
/** Cordis entrypoint. Partial configuration is the exact feature-off path. */
export function apply(ctx: Context): void {
  const config = resolveShadowObserverConfig()
  if (config === undefined) return
  registerShadowObserver(ctx, config)
}
```

```ts
/** Register only the session log's read-only publication hooks. */
export function registerShadowObserver(ctx: Context, config: ShadowObserverConfig): ShadowObserver {
  const observer = new ShadowObserver({
    config,
    warn: message => { ctx.logger.warn(message) },
  })
  ctx.effect(function* () {
    ctx.on('session/created', session => { observer.observeSessionCreated(session) })
    ctx.on('session/event', (session, event) => { observer.observeSessionEvent(session, event) })
    ctx.on('session/disposed', session => { observer.observeSessionDisposed(session) })
    yield async () => {
      await observer.dispose()
    }
  }, 'dsh-loopx shadow observer lifecycle')
  return observer
}
```

**可抄点**：
- **配置不全就彻底 off**：`if (config === undefined) return`——比"报错不加载"更友好，也不会留下半个插件；
- `ctx.effect(function* () { ...; yield async () => {...} })` 是**生成器写法**：`yield` 出来的函数就是 disposer，与返回函数的写法等价，适合"注册很多行 + 末尾统一清理"。

### 2.8 【核心范本·发布服务】loopx `init-command.ts` 的 `ctx.reflect.provide`（逐字）

```ts
/** Register the explicit repair command without changing LoopX readiness. */
export function registerLoopXInitCommand(
  ctx: Context,
  options: LoopXInitOptions = {},
): void {
  ctx.commands.register({
    name: 'loopx-init',
    description: 'install or upgrade LoopX and install the DSH LoopX skills',
    recordInput: false,
    async handler(invocation): Promise<CommandResult> {
      if (invocation.rawInput.trim().length > 0) {
        return { kind: 'error', text: 'Usage: /loopx-init' }
      }
      const warn = (message: string): void => { ctx.logger.warn(message) }
      queueFollowup(invocation.agent, startFollowup(), 'start', warn)
      try {
        const result = await initializeLoopX({ ...options, signal: invocation.signal })
        const commandResult = successResult(result)
        if (!invocation.signal.aborted) {
          queueFollowup(invocation.agent, successFollowup(result), 'complete', warn)
        }
        return commandResult
      } catch (error: unknown) {
        const commandResult = commandFailure(error)
        if (!cancelled(error, invocation.signal)) {
          queueFollowup(invocation.agent, failureFollowup(error), 'complete', warn)
        }
        return commandResult
      }
    },
  })
}
```

```ts
/**
 * Make the installed plugin ready before DSH finishes loading this row.
 *
 * Startup failures are isolated to LoopX: DSH still boots and the registered
 * command remains as an explicit retry surface. The awaited happy path keeps a
 * freshly installed profile from racing its first `skill.list` readback.
 */
export async function apply(ctx: Context, options: LoopXInitOptions = {}): Promise<void> {
  registerLoopXInitCommand(ctx, options)
  let status: LoopXBootstrapStatus
  try {
    await initializeLoopX(options)
    status = Object.freeze({ state: 'ready' })
  } catch (error: unknown) {
    status = bootstrapFailureStatus(error)
    try {
      ctx.logger.warn(automaticFailure(error))
    } catch {
      // Diagnostics must never turn an isolated LoopX bootstrap failure into a DSH startup failure.
    }
  }
  ctx.reflect.provide('loopxBootstrap', status)
}
```

**可抄点（怎么"提供"一个服务）**：
1. **服务名是字符串**：`ctx.reflect.provide('loopxBootstrap', status)`；别的行用 `inject: ['loopxBootstrap']` 或 `ctx.get('loopxBootstrap')` 消费；
2. **无论成功还是"安全失败"都要 provide**——否则依赖它的行（Web server / web runtime）会被一直挂起，DSH 的 Web URL 永远发不出来；
3. **失败降级成类型化的状态对象**（`{ state: 'failed', stage, causeKind }`），而不是抛异常；这样宿主可继续启动，`/loopx-init` 还能修复；
4. `Object.freeze(...)` 冻结状态，防止下游误改。

### 2.9 loopx 状态内核：`driver.ts` 的 `apply`（逐字，多监听 + 生成器清理）

```ts
export function apply(ctx: Context): void {
  const driver = new LoopXContinuationDriver({
    isLiveAgent: agent => ctx.agents.get(agent.id) === agent,
    resolveCommand: signal => resolvePluginLoopXCommand({ signal }),
    runDetached: operation => ctx.agents.withoutInitiator(operation),
    warn: message => { ctx.logger.warn(message) },
  })

  ctx.effect(function* () {
    const unregisterDriverBridge = goalBarCoordinator.registerDriverBridge(driver)
    ctx.on('agent/created', ({ agent }) => { driver.observeAgent(agent) })
    ctx.on('agent/disposed', ({ agent }) => {
      goalBarCoordinator.invalidateSession(agent.session)
      driver.onAgentDisposed(agent)
    })
    ctx.on('session/disposed', session => {
      goalBarCoordinator.invalidateSession(session)
    })
    ctx.on('agent/session-start', ({ agent }) => { driver.onSessionStart(agent) })
    ctx.on('agent/status', ({ agent, status }) => {
      if (status === 'idle' || status === 'running') {
        goalBarCoordinator.publishAgentStatus(agent.session, status)
      }
      driver.onAgentStatus(agent, status)
    })
    ctx.on('agent/inbox/inserted', ({ agent, message }) => driver.onInboxInserted(agent, message))
    ctx.on('agent/inbox/claimed', ({ agent, message }) => driver.onInboxClaimed(agent, message))
    ctx.on('agent/inbox/discarded', ({ agent, message }) => driver.onInboxDiscarded(agent, message))
    ctx.on('agent/error', ({ agent }) => { driver.onAgentError(agent) })
    ctx.on('agent/pre-step', ({ agent, messages, signal }, next) => (
      driver.onPreStep(agent, messages, signal, next)
    ))
    ctx.on('session/event', (session, event) => {
      if (event.type === 'step/end' || event.type === 'turn/end') {
        goalBarCoordinator.publishSessionCandidate(session, event)
      }
      const agent = ctx.agents.get(session.id)
      if (agent?.session === session) driver.onSessionEvent(agent, event)
    })
    for (const agent of ctx.agents.list()) driver.observeAgent(agent)
    yield async () => {
      unregisterDriverBridge()
      await driver.dispose()
    }
  }, 'dsh-loopx-driver lifecycle')
}
```

**可抄点**：
- **"全局一个 Driver，按会话激活"** 的状态内核模式：Driver 实例只建一次，把"DSh 的 agent 事件"翻译成 driver 内部状态；卸载时 `yield` 一个函数统一 `dispose()`；
- `ctx.agents.list()` 在 apply 时对**已存在**的 agent 补一遍 `observeAgent`，避免"插件比 agent 晚加载"时漏掉；
- `if (agent?.session === session)` 用**引用相等**确认事件属于当前 agent（呼应坑 L4）。

### 2.10 loopx 服务类骨架：不继承任何基类，自己管生命周期（`src/goalbar/service.ts` 节选，逐字）

```ts
export interface GoalBarServiceHandle {
  handle(
    request: GoalBarRequestV1,
    signal: AbortSignal,
  ): Promise<GoalBarResponseV1>
  dispose(): Promise<void>
}

export class GoalBarService implements GoalBarServiceHandle {
  private readonly disposal = new AbortController()
  private activeAction?: ActionAdmission | undefined
  private disposed = false

  constructor(options: GoalBarServiceOptions) {
    // …(字段赋值略)
  }

  async handle(
    request: GoalBarRequestV1,
    signal: AbortSignal,
  ): Promise<GoalBarResponseV1> {
    try {
      if (request.op === 'read') return await this.readResponse(request, signal)
      if (request.op === 'watch') return await this.watchResponse(request, signal)
      return await this.actionResponse(request, signal)
    } catch {
      return fixedGoalBarFailureResponseV1(request)
    }
  }

  async dispose(): Promise<void> {
    if (!this.disposed) {
      this.disposed = true
      this.disposal.abort()
      this.watchService.dispose()
    }
    await this.activeAction?.completion
  }
}

export function createGoalBarService(
  options: GoalBarServiceOptions,
): GoalBarService {
  return new GoalBarService(options)
}
```

**可抄点（"类式服务"的正确姿势）**：
1. **先定义 `interface XxxHandle`**（对外契约），`class` 只 `implements` 它——**不 extends Cordis 的 Service**；
2. 服务类自己持有一个 `AbortController` 作 `disposal`，`dispose()` **幂等**（`if (!this.disposed)`）；
3. `dispose()` 结束后 `await this.activeAction?.completion`，**等待进行中的动作收尾**，避免"卸载时还在改状态"；
4. 对外暴露一个 `createXxxService(options)` 工厂函数，而不是让调用方 `new`；
5. `handle()` 顶层 `try/catch`，任何意外都翻译成**类型化的失败响应**返回，而不是把异常抛给 RPC 边界。

### 2.11 loopx 客户端半侧入口（`src/client/index.tsx` 全文，逐字）

```tsx
import type { Context } from '@deepseek-ai/cordis'
import type { ConnectionHandle } from '@deepseek-ai/dsh-client-connection/client'
import type {} from '@deepseek-ai/dsh-client-locale/client'
import type {} from '@deepseek-ai/dsh-client-runtime/client'
import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'

import { LoopXGoalBar } from './LoopXGoalBar.tsx'
import { ensurePluginStyle } from './goalbar.module.css'
import {
  GOALBAR_LOCALES,
  GOALBAR_LOCALE_NAMESPACE,
} from './locale.ts'
import { createGoalBarRpc } from './rpc.ts'

const PACKAGE_ID = 'dsh-loopx-plugin'

/** Cordis service names required before the materialized Client plugin applies. */
export const inject = ['connection', 'locale', 'slots'] as const

type GoalBarClientContext = Context & {
  readonly connection: ConnectionHandle
}

/** Register the exact-Session LoopX GoalBar contribution and its owned copy. */
export function apply(ctx: GoalBarClientContext): void {
  // Client module exports are cached across a same-page plugin reapply, so CSS
  // installation must be an explicit, idempotent apply-time operation.
  ensurePluginStyle()

  // Register ownership immediately after installation, before any later apply
  // step can fail, so Cordis rollback and ordinary unload both remove the tag.
  ctx.effect(() => () => {
    if (typeof document === 'undefined') return
    for (const style of document.querySelectorAll('style[data-plugin]')) {
      if (style.getAttribute('data-plugin') === PACKAGE_ID) style.remove()
    }
  }, 'dsh-loopx-plugin CSS ownership')

  ctx.effect(
    () => ctx.locale.register(GOALBAR_LOCALE_NAMESPACE, GOALBAR_LOCALES),
    'dsh-loopx-plugin GoalBar locale',
  )

  const rpc = createGoalBarRpc(
    ctx.connection.rpc,
    Reflect.has(ctx.connection, 'generation'),
  )
  ctx.slots.inject('conversation.input.dock', () => ctx.slots.register({
    name: 'conversation.input.dock',
    id: 'loopx-goal',
    order: 15,
    locale: GOALBAR_LOCALE_NAMESPACE,
    inject: sessionId => ({
      rpcSessionId: String(sessionId),
      rpc,
      subscribeConnectionReset: (listener: () => void) => (
        ctx.on('connection/reset', listener)
      ),
    }),
  }, LoopXGoalBar))
}
```

**可抄点（客户端半侧）**：
- 客户端入口同样是**具名** `inject` + `apply`，但 `inject` 是**客户端服务名**（`connection`/`locale`/`slots`），与宿主侧同名不同义；
- 通过 `ctx.slots.inject('conversation.input.dock', ...)` 往 DSH 对话输入区的 dock 里**插一个 React 组件**（`LoopXGoalBar`），用 `order` 控制排序；
- 组件的 `inject: sessionId => ({...})` 把**当前会话 id** 注入组件，同时把 `ctx.on` 的订阅能力传下去；
- 所有 `ctx.effect` 都带**第二个字符串参数**（用途描述），方便日志与排查。

### 2.12 loopx `cordis.patch.yml`（全文，逐字）

```yaml
# LoopX owns Goal, Todo, quota, and thread-binding authority.
- insert:
    # The package-root Host row is also the discovery anchor for dsh.client.
    - id: loopx-goalbar
      name: dsh-loopx-plugin

    - id: loopx-init-command
      name: dsh-loopx-plugin/init-command

    - id: loopx-driver
      name: dsh-loopx-plugin/driver

    # Loaded as its own default-off Cordis row. It has no Driver or Agent
    # injection and registers only session publication hooks when fully pinned.
    - id: loopx-shadow-observer
      name: dsh-loopx-plugin/observer

# The browser must not advertise readiness while first-run skill bootstrap is
# still in flight. A safe bootstrap failure also publishes the service, so DSH
# remains usable and /loopx-init can repair it.
- id: webserver
  name: '@deepseek-ai/dsh-host-webserver'
  inject: [webStartup, loopxBootstrap]

- id: web-runtime
  name: '@deepseek-ai/dsh-web-app'
  inject: [webStartup, loopxBootstrap]
```

**可抄点（patch 语法）**：
- `- insert:` 下面是一个**列表**，每行有 `id` 和 `name`；`name` 既可以是**包名**（`dsh-loopx-plugin`），也可以是**包的子导出**（`dsh-loopx-plugin/driver`、`dsh-loopx-plugin/observer`），与 `package.json` 的 `exports` 对应；
- 已存在的行（`webserver` / `web-runtime`）用**顶层** `- id/name/inject` 覆写，`inject` 列表里加上自家的 `loopxBootstrap`，从而把"Web 就绪"**挂到** LoopX 引导完成的边界上；
- 注释里点明了关键次序约束：依赖服务未 provide 前，被 inject 的行不会激活。

### 2.13 loopx `package.json`（全文；此处为前半段，后半段见 2.13b）

```json
{
  "name": "dsh-loopx-plugin",
  "version": "0.1.1-beta.5",
  "description": "One-step LoopX bootstrap, same-session driver, and local GoalBar for DeepSeek Harness",
  "type": "module",
  "main": "./lib/index.js",
  "types": "./lib/types/index.d.ts",
  "exports": {
    ".": {
      "types": "./lib/types/index.d.ts",
      "default": "./lib/index.js"
    },
    "./init-command": {
      "types": "./lib/types/init-command.d.ts",
      "default": "./lib/init-command.js"
    },
    "./driver": {
      "types": "./lib/types/driver.d.ts",
      "default": "./lib/driver.js"
    },
    "./observer": {
      "types": "./lib/types/observer.d.ts",
      "default": "./lib/observer.js"
    },
    "./client": {
      "types": "./lib/types/client/index.d.ts",
      "default": "./lib/client.js"
    },
    "./cordis.patch.yml": "./cordis.patch.yml",
    "./package.json": "./package.json"
  },
  "files": [
    "lib/*.js",
    "lib/types/**/*.d.ts",
    "cordis.patch.yml",
    "README.md",
    "LICENSE",
    "NOTICE"
  ],
  "engines": {
    "node": "^22.19.0 || >=24.0.0"
  },
  "scripts": {
    "build": "node scripts/build.mjs",
    "typecheck": "tsc -p tsconfig.host.json --noEmit && tsc -p tsconfig.client.json --noEmit && tsc -p tsconfig.tests.json",
    "test": "vitest run",
    "prepack": "pnpm build",
    "smoke:artifact": "node smoke/dsh-client-artifact-smoke.mjs",
    "smoke:peer-range": "node smoke/dsh-peer-range-smoke.mjs",
    "smoke:profile": "node smoke/dsh-profile-smoke.mjs",
    "smoke:runtime": "node smoke/dsh-goalbar-runtime-smoke.mjs",
    "smoke:docker": "bash smoke/dsh-clean-docker-smoke.sh"
  },
  "dsh": {
    "bundle": {
      "patch": "./cordis.patch.yml"
    },
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-connection",
        "@deepseek-ai/dsh-client-locale",
        "@deepseek-ai/dsh-client-runtime",
        "@deepseek-ai/dsh-client-ui-conversation"
      ],
      "platform": "web"
    }
  },
```
  "peerDependencies": {
    "@deepseek-ai/cordis": "^4.0.1",
    "@deepseek-ai/dsh": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-connection": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-locale": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-runtime": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-ui-conversation": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-ui-primitives": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "@deepseek-ai/dsh-client-ui-slots": ">=0.1.0-rc.7 <0.1.1 || >=0.1.1-rc.1 <0.2.0-0",
    "react": "^18.2.0"
  },
  "peerDependenciesMeta": {
    "@deepseek-ai/cordis": { "optional": true },
    "@deepseek-ai/dsh": { "optional": true },
    "@deepseek-ai/dsh-client-connection": { "optional": true },
    "@deepseek-ai/dsh-client-locale": { "optional": true },
    "@deepseek-ai/dsh-client-runtime": { "optional": true },
    "@deepseek-ai/dsh-client-ui-conversation": { "optional": true },
    "@deepseek-ai/dsh-client-ui-primitives": { "optional": true },
    "@deepseek-ai/dsh-client-ui-slots": { "optional": true },
    "react": { "optional": true }
  },
  "devDependencies": {
    "@deepseek-ai/cordis": "4.0.1",
    "@deepseek-ai/dsh": "0.1.1-rc.2",
    "@deepseek-ai/dsh-agent": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-connection": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-locale": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-runtime": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-ui-conversation": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-ui-primitives": "0.1.1-rc.2",
    "@deepseek-ai/dsh-client-ui-slots": "0.1.1-rc.2",
    "@deepseek-ai/dsh-commands": "0.1.1-rc.2",
    "@deepseek-ai/dsh-llm": "0.1.1-rc.2",
    "@deepseek-ai/dsh-session": "0.1.1-rc.2",
    "@types/node": "^22.19.0",
    "@types/react": "~18.3.1",
    "@types/react-dom": "~18.3.1",
    "jsdom": "^26.1.0",
    "lightningcss": "1.33.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tsdown": "0.22.2",
    "typescript": "^6.0.3",
    "vitest": "^4.1.8"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/huangruiteng/loopx.git",
    "directory": "packages/dsh-loopx-plugin"
  },
  "license": "Apache-2.0",
  "publishConfig": {
    "access": "public"
  }
}
```

**可抄点**：
- `dsh.client.inject` 列出**客户端模块名**（`@deepseek-ai/dsh-client-*`），`platform: "web"` 表示只在 Web 表面挂载；**这是与 MemOS/archify 的关键差异**：只有 loopx 同时声明了 `dsh.bundle` + `dsh.client`；
- `exports` 里为宿主多行（`./init-command`、`./driver`、`./observer`、`./client`）各开一个子导出，**patch 的 `name` 正好引用它们**；
- peer 全是 `optional: true` + `peerDependenciesMeta`，通过 `smoke:peer-range` 脚本自证"实测版本落在 peer 范围内"（坑 L2）。

### 2.14 【同类里最小的服务定义 / 插件入口】横向对比

| 角色 | 文件 | 行数 | 是否有 `apply` | 是否有 `inject` | 生命周期 |
|---|---|---|---|---|---|
| **最小"路径解析助手"**（严格说不是插件，但可当"入口模块"最小样板） | archify `integrations/deepseek-harness/lib/index.js` | 22 | 无 | 无 | 无 |
| **最小"服务生命周期"插件** | loopx `packages/dsh-loopx-plugin/src/index.ts` | 29 | 有 | 有（3 个） | `ctx.effect` 返回 async disposer |
| 中等"条件关闭"插件 | loopx `src/observer.ts` 的 `apply` | 6（apply 本体） | 有 | 无 | `if (config===undefined) return` |
| 大型"记忆服务"插件 | MemOS `adapters/deepseek-harness/index.ts` | 487 | 有（async） | 有（3 个） | `registrations[]` + 回滚 + 返回卸载函数 |

**结论：教学首选 loopx `src/index.ts`（29 行）作为"怎么写一个有生命周期的服务插件"的最小范本。**
它完整演示了：具名 `name`/`inject`、`ctx.effect` 建服务与 RPC、返回 disposer 卸载、以及"inject 一个自家 provide 的服务名"。想看"全量工程化"再升级到 MemOS 的 487 行版本。

**绝对最小的入口模块范本**（archify `lib/index.js` 全文，逐字，22 行）——注意它**没有 `apply`**，因为 archify 的 `cordis.patch.yml` 插入的是 DSH 内置 provider，这个文件只被测试直接 import：

```js
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';

export const name = 'archify-dsh';
export const PACKAGE_NAME = '@tt-a1i/archify-dsh';

export function resolveArchifySkillRoot(profileBaseUrl) {
  if (!profileBaseUrl) {
    throw new Error('archify-dsh: missing DSH profile baseUrl for package resolution');
  }
  let manifestPath;
  try {
    manifestPath = createRequire(profileBaseUrl).resolve(`${PACKAGE_NAME}/package.json`);
  } catch (error) {
    throw new Error(
      `archify-dsh: cannot resolve ${PACKAGE_NAME}/package.json from the DSH profile`,
      { cause: error },
    );
  }
  return join(dirname(manifestPath), 'skills');
}
```

**重要提醒**：archify 的 `package.json` 里 `"main": "./lib/index.js"`，但**patch 从未引用它**；Loader 加载的是 patch 里 `name: '@deepseek-ai/dsh-skill-filesystem'`。所以"包有 `main`/`exports`" ≠ "它会被当插件加载"，**真正的装配入口由 `cordis.patch.yml` 的 `name` 决定**。

---

## C · 三、该方向的开发规范（只在多家都这么做时才归纳）

> 每条规范都标注**依据**（哪几个仓库、哪几个文件）。只有"多家共识"才写"规范"；单家独有写"某仓库的做法"。

### 规范 1：插件入口一律**具名**导出 `name` / `inject` / `Config` / `apply`；**不要 default export**

- **依据（3/3 家）**：
  - MemOS：`adapters/deepseek-harness/index.ts` → `export const name`、`export const inject = ["systemPrompt","tools","llm"]`、`export const Config`、`export async function apply`；
  - loopx：`src/index.ts` / `src/driver.ts` / `src/observer.ts` / `src/init-command.ts` / `src/client/index.tsx` 全部具名 `name`/`inject`/`apply`；
  - archify：`lib/index.js` 也是具名 `name`。
- 补充：`grep -rn "export default"` 在三个仓库的插件代码里**只**命中一个与插件无关的 `css-modules.d.ts`。这与手册背景"绝不能有 default export（官方复盘 0001）"一致。

### 规范 2：生命周期/副作用统一用 `ctx.effect(...)` 或"注册函数返回 disposer + 数组统一回收"

- **依据（3/3 家）**：
  - loopx：`ctx.effect(() => {...; return async () => {...}}, '描述')`（`src/index.ts`）、`ctx.effect(function* () {...; yield async () => {...}}, '描述')`（`src/driver.ts`、`src/observer.ts`）、客户端同样 `ctx.effect(...)`（`src/client/index.tsx`）；
  - MemOS：`registrations.push(ctx.on(...))` + `unregisterAll()` 倒序回收（`adapters/deepseek-harness/index.ts`）；工具侧同样的 `disposers` 数组（`tools.ts`）；
  - archify：无副作用（README 明确"no background service / no telemetry / no install hooks"），是"零副作用"的另一种合规姿态。
- 描述字符串：loopx 所有 `ctx.effect` 都带第二个参数（用途），建议照抄这个习惯。

### 规范 3：发布服务的名字用**字符串**，消费方用 `inject: [...]` 或 `ctx.get('...')`

- **依据**：loopx `init-command.ts` 用 `ctx.reflect.provide('loopxBootstrap', status)`；同包 3 个插件用 `inject: ['agents','connection','loopxBootstrap']` 消费；patch 里 `inject: [webStartup, loopxBootstrap]`。
- **只有 1 家**做"provide + inject"，但它是本方向唯一的服务发布活例，建议作为该方向的样板。

### 规范 4：配置定义二选一，且都要有默认值

- **依据（2 家做法不同）**：
  - MemOS（DSH 插件层）：用 **schemastery** `export const Config: Schema<Config> = Schema.object({ ... .default(...) })`，且在 `interface Config` 里给类型（`adapters/deepseek-harness/index.ts`）；
  - MemOS（内核层 `core/config/schema.ts`）：用 **@sinclair/typebox** `Type.Object({...})`，并且"每个字段必须有 default，旧配置才能升级"（`core/config/README.md` 原文：`Adding fields: provide a default in defaults.ts (so old configs upgrade). Removing fields: log a warning at load time; don't crash.`）；
  - loopx：**完全不声明 `Config`**，配置走环境变量 + `resolve*Config()`（`src/observer.ts` 的 `resolveShadowObserverConfig()`），配置不完整就整体 off。
- 共识：**没有默认值 / 校验失败的路径必须有明确降级策略**（MemOS 缺失配置文件→用 defaults + 警告；loopx 配置不全→off）。

### 规范 5：`cordis.patch.yml` 用 `- insert:` 列表；`name` 指向"包名或包子导出"，与 `package.json` 的 `exports` 对齐

- **依据（3/3 家）**：三家都写 `dsh.bundle.patch`；loopx 的 patch `name` 直接用子导出（`dsh-loopx-plugin/driver` 等），并与其 `exports` 字段严格对应；MemOS 用**编译后**路径（`dist/adapters/deepseek-harness/index.js`）；archify 用 `!!js` 内联解析。
- 覆写已存在行时用**顶层** `- id/name/inject`（loopx 对 `webserver`/`web-runtime` 的做法）。
- 关于 `!!js`：只有 archify 用它（在插件 `config` 内），与手册背景"`!!js` 只在插件 config 与 entry 的 disabled 内被求值"一致。

### 规范 6：要写测试，且测试要覆盖"干净构建 / 打包产物"

- **依据（2/3 家做得很足）**：
  - MemOS：`tests/` 有 205 个文件，含 `deepseek-harness-*.test.ts` 6 个；提交 `b41c899` 明确"新增回归测试覆盖两种干净布局，包括包根本身名为 dist 的情况"；
  - archify：`test/` 10 个 `.test.mjs`，含 `package-contract.test.mjs`（断言必须有 `dsh.bundle.patch`、**不得**有 install 生命周期脚本、不得有 dependencies）、`tarball-contract.test.mjs`、`zero-regression.test.mjs`；
  - loopx：`tests/` 10 个 `*.spec.ts` + `smoke/` 5 个冒烟脚本（artifact/profile/runtime/docker/peer-range）。
- 共识：**测试要跑"打包后的产物"**，而不只是源码（呼应坑 A4/M2）。

### 规范 7：README 要写清"安装 / 升级 / 卸载 / 失败行为 / 已知限制 / 安全边界"，并诚实标注"非官方"

- **依据（3/3 家）**：
  - MemOS `adapters/deepseek-harness/README.md` 有 `Install` / `Uninstall` / `Failure behavior` / `Known limitations`(7 条) / `Privacy and security`，并给了**字段表**；
  - loopx `README.md` 有 `Install` / `Uninstall` / `Shadow observer` / 权限与隐私边界 / `Maintainer release and marketplace handoff`；
  - archify `README.md` 第一行就写 `This is **not** an official DeepSeek product and does not imply DeepSeek endorsement.`，并单列 `Security posture`。

### 规范 8（弱共识，仅供注意）：`inject` 是**数组**；`name` 用**包名或短横线命名**

- **依据（3/3 家的宿主侧入口）**：MemOS `inject = ["systemPrompt","tools","llm"]`；loopx `inject = ['agents','connection','loopxBootstrap']`；archify 无 inject（不适用）。客户端 loopx `inject = ['connection','locale','slots']`。
- 命名：包名 `dsh-loopx-plugin` / `@tt-a1i/archify-dsh`，插件 `name` 与之对应（`dsh-loopx-plugin`、`archify-dsh`）。

### 明确**没有**形成规范的点（提示手册不要写死）

- **是否用 `default export 服务类`**：3 家都没有 → 本方向**不要**把它写成规范，反而应写"本批真实仓库不使用该写法"。
- **是否继承某个 `Service` 基类**：0 家 → 类式服务（loopx `GoalBarService`）只是**普通 class + interface + AbortController 自管理**。
- **是否写 `Config`**：2/3 家写、1 家不写 → 不是硬性规范。

---

## C · 四、新手最容易卡住的 5 个点（附一句可执行建议）

> 全部来自上面的真实坑，按"对零经验者的致命程度"排序。

### 卡点 1：以为用了 `default export` 也没关系 —— 结果 `inject` 被静默丢弃

- **为什么致命**：官方复盘 0001 已确认 default export 会让 Loader 丢掉 `inject`；插件看似加载了，但服务依赖全没注入，行为诡异且不报错。新手最容易在 e2e 里写 `export default` 图省事。
- **建议**：入口**只写具名导出** `export const name` / `export const inject` / `export function apply`，提交前 `grep -n "export default"` 自查必须为空。

### 卡点 2：卸载/热重载时副作用没回收 —— 监听器叠加、样式重复、端口占用

- **为什么致命**：HMR 会**再次调用** `apply`；客户端模块导出还会被缓存（loopx 源码注释原话）。没回收就是"重载越多次越坏"，且常表现为"偶尔"。
- **建议**：**每写一个 `ctx.on`/注册调用，就立刻放进 `ctx.effect(...)`**（或 push 进数组并返回 disposer）；`apply` 里的副作用必须**幂等**。

### 卡点 3：任何"等后台任务"的 await 不设超时 —— 卸载/关整天卡死

- **为什么致命**：MemOS 真实事故：一个无超时的 `await` 让 `SIGTERM` 后卡 10 分钟被强杀（坑 M1）。新手不知道"后台 LLM 有 163 次串行调用"这种事。
- **建议**：**给每个等待后台工作的 await 都套 `withTimeout(promise, ms, "名字")`**，并在代码注释里写清"超时后丢不丢数据"。

### 卡点 4：路径靠"猜"或"拼" —— dev 能跑、打包/CI 必坏

- **为什么致命**：用 `existsSync` 猜包根（坑 M2）、把包名拼到 `baseUrl` 上（坑 A2）都会在干净构建或换机器时崩。新手无法复现"CI 才失败"。
- **建议**：**定位已安装的包一律用 `createRequire(锚点).resolve('<包名>/package.json')`**；路径拼接一律用 `node:path`，绝不用字符串手动拼 `/` 或 `\`。

### 卡点 5：把"能改状态的动作"当成普通函数 —— 双击/重复请求导致状态被改两次

- **为什么致命**：状态内核里 `Start`/`Pause` 这类动作真的会改权威数据；新手的按钮没有锁，连点两次就发起两次变更（坑 L5）。而且"拒绝/结果不确定"时如果解锁，用户会重复点，越点越乱。
- **建议**：**前端锁（`xxxGuardRef`）+ 后端锁（`activeAction`）双保险**；只有"显式刷新"或"会话切换"才解锁，拒绝与不确定结果**故意保持锁定**。

---

## C · 五、给手册写作的提醒（本方向特有）

1. **不要写"服务式插件用 default export 服务类"** —— 本批 3 个真实仓库**都不是**，会误导读者。可写"DSH 历史上存在该写法，但本批实战仓库统一用函数式具名导出 + `ctx.reflect.provide`"。若需引用 default export 服务类，需另找官方模板（不在本次素材内）。
2. **两种 `required` 的对照表一定要做成醒目小卡**：`parameters` 属性级 `required: true`（DSH DSL）vs `output.schema` 对象级 `required: ['a','b']`（标准 JSON Schema），不可混用。
3. **`!!js` 只出现在插件 config 内**：本批只有 archify 用它，且用于"解析已安装包路径"，是很好的正例。
4. **"行顺序不影响加载顺序"** 在 loopx 的 patch 里有旁证：`webserver`/`web-runtime` 靠 `inject: [..., loopxBootstrap]` 决定激活时机，而不是靠行序。

---

## 附：本文实际读取的源码/测试/文档文件清单（30 项）

1. `MemTensor_MemOS/apps/memos-local-plugin/adapters/deepseek-harness/index.ts`（全文 487 行）
2. `MemTensor_MemOS/apps/memos-local-plugin/adapters/deepseek-harness/tools.ts`（节选：头部 + 参数 DSL + 尾部回收）
3. `MemTensor_MemOS/apps/memos-local-plugin/adapters/deepseek-harness/host-llm.ts`（头部）
4. `MemTensor_MemOS/apps/memos-local-plugin/adapters/deepseek-harness/cordis.patch.yml`（全文）
5. `MemTensor_MemOS/apps/memos-local-plugin/adapters/deepseek-harness/README.md`（全文）
6. `MemTensor_MemOS/apps/memos-local-plugin/package.json`（全文）
7. `MemTensor_MemOS/apps/memos-local-plugin/CHANGELOG.md`（头部）
8. `MemTensor_MemOS/apps/memos-local-plugin/core/config/README.md`（全文）
9. `MemTensor_MemOS/apps/memos-local-plugin/core/config/schema.ts`（头部）
10. `MemTensor_MemOS/AGENTS.md`（grep）
11. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/index.ts`（全文 29 行）
12. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/driver.ts`（第 1130–1206 行）
13. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/observer.ts`（第 585–624 行）
14. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/init-command.ts`（第 530–632 行）
15. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/goalbar/service.ts`（全文 745 行）
16. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/client/index.tsx`（全文 61 行）
17. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/client/rpc.ts`（全文）
18. `huangruiteng_loopx/packages/dsh-loopx-plugin/src/client/useGoalBar.ts`（全文 392 行）
19. `huangruiteng_loopx/packages/dsh-loopx-plugin/cordis.patch.yml`（全文）
20. `huangruiteng_loopx/packages/dsh-loopx-plugin/package.json`（全文）
21. `huangruiteng_loopx/packages/dsh-loopx-plugin/smoke/dsh-peer-range-smoke.mjs`（全文）
22. `huangruiteng_loopx/packages/dsh-loopx-plugin/README.md`（全文）
23. `huangruiteng_loopx/docs/plans/2026-08-20-dsh-native-skill-driver.md`（头部 130 行）
24. `huangruiteng_loopx/AGENTS.md`（grep）
25. `tt-a1i_archify/integrations/deepseek-harness/lib/index.js`（全文 22 行）
26. `tt-a1i_archify/integrations/deepseek-harness/cordis.patch.yml`（全文）
27. `tt-a1i_archify/integrations/deepseek-harness/package.json`（全文）
28. `tt-a1i_archify/integrations/deepseek-harness/README.md`（全文）
29. `tt-a1i_archify/integrations/deepseek-harness/test/package-contract.test.mjs`（头部）
30. `tt-a1i_archify/integrations/deepseek-harness/test/adapter-security.test.mjs`（全文）

（另：git 历史读取 3 个仓库的 `git log` / `git show -s`，共核实 20+ 条 commit 元数据。）

> 全文完。所有代码块逐字来自本地源码快照；所有坑均有 commit 哈希或源码行号佐证；查不到的已明确标注"未找到"。

---

