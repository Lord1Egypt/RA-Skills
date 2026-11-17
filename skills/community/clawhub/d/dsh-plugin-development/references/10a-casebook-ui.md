# A 方向分册 · DSH UI 插件

> **文件来源**：本文件由 `10-community-casebook.md` 拆分而来，正文为原文的**逐行搬迁**，未做改写。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。总索引见 `10-community-casebook.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。

---

<!-- ↓ 源：A-ui-plugins.md （全文） -->

# A. DSH UI 插件方向 —— 真实踩坑记录 + 可复用骨架（原始素材）

> 面向《DSH 插件开发实战手册》。读者设定：**零软件工程经验的新手**。
> 每一条都标注来源：`仓库 + commit 短哈希 + 提交信息原文`，或 `仓库 + 文件路径`。
> 查不到的明确写 **「未找到」**，不编造。

---

## 0. 材料与方法（先读，决定你能从这个文件里信多少）

### 0.1 三个仓库的本地可用性（实测）

| 仓库 | commits | trees | **本地 blobs** |
|---|---|---|---|
| `zhu1090093659_dsh-web` | 2444 | 19098 | **365**（全部是 `.agents/notes/**` 笔记） |
| `omdsh-dev_DSH-better-sidebar` | 644 | 2044 | **0** |
| `dsh-market_dsh-market` | 491 | 1685 | **0** |

三仓均为 `--filter=blob:none --no-checkout` 部分克隆，工作区为空（`find . -type f -not -path './.git/*'` 返回 0）。
复现命令：

```bash
cd <repo>
git cat-file --batch-check --batch-all-objects | awk '$2=="blob"' | wc -l   # 本地 blob 数
git ls-tree -r HEAD                                                          # 全部路径+哈希（不需要 blob）
```

### 0.2 读文件内容的正确姿势

```bash
cd <repo>
GIT_NO_LAZY_FETCH=1 git show HEAD:<路径>
# 不加 GIT_NO_LAZY_FETCH=1 时会尝试联网 fetch，环境无网，报：
#   fatal: unable to access 'https://github.com/...': Could not connect to server
#   fatal: could not fetch <hash> from promisor remote
# 即使加了，blob 不在本地时仍报：fatal: bad object HEAD:<路径>
```

**结论（对写手册至关重要）：**

1. **本文件无法提供任何 `.ts` / `.tsx` / `package.json` / `cordis.patch.yml` 的源码逐字照抄** —— 这些 blob 不在本地，任务书里 `git show HEAD:<源码路径>` 会直接 `bad object`。凡涉及源码正文，本文件一律标注 **「未找到（blob 不可用）」**，只给出**路径与目录树**这两个确实可读到的事实。
2. 但 `dsh-web` 把 **245 篇 Agent Notes**（中文/英文成对）提交进了仓库，且这 365 个 blob 全部可用。这些 Notes 是**维护者自己写的 RFC/事故报告**，格式固定为 `## Problem` / `## Decision` / `## Alternatives considered` / `## Consequences` / `## Testing`，信息密度远高于源码注释，是本次最有价值的坑源。
3. `omdsh-dev_DSH-better-sidebar` 与 `dsh-market_dsh-market` 的提交信息**写得极长**（正文常含「诊断 / 根因 / 修复 / 测试」四段），弥补了 blob 缺失。
4. 三个仓库文件树完整，可读到：包边界、`exports` 相关文件是否存在、`src/{host,client,core}` 分层、`tests/` 命名等**结构性事实**。

### 0.3 本文件引用的 dsh-web 笔记

- Bug-fix 笔记：`.agents/notes/implemented/bug-fix/`（全仓 83 篇可读 / 该目录下 245 篇已实现笔记共存）
- Architecture 笔记：`.agents/notes/implemented/architecture/`（可读 18 篇）
- 权威规范：`packages/AGENTS.md`（**逐字可读**，见 §二 与 §三）
- 笔记写作规范：`.agents/notes/README.md`、`.agents/notes/AGENTS.md`

---

# A · 一、坑点清单：现象 → 根因 → 怎么修

> 记法：`[仓库] <commit 短哈希> <提交信息原文>`。
> 「提交信息原文」保留原始措辞（含中英混排、原文错别字）。

## 1.1 zhu1090093659_dsh-web（2444 commits，1032 次修复；坑矿最富）

### A 组：客户端半 / 宿主半通信与线协议

#### 坑 D1　客户端 bundle 硬 require `dsh-client-store`，宿主换 cohort 后整个家族客户端全不加载

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-28-client-store-dual-cohort-engine-shim.md`
  （笔记标题逐字：`Agent Note: dual-cohort client compatibility repair (store engine, injected faces)`）
- **现象**（笔记逐字）：
  ```
  failed to import loader entry 47c06ebb (@linxin666/dsh-client-ui-web-ui-settings):
  client-modules: require("@deepseek-ai/dsh-client-store") missed the module table —
  not a platform seed word, not a materialized module, and no registered package factory
  ```
  以及：task-board 条目永远停在 `pending (waiting for service: remote.agentPresets)`，启动审计报「一个条目未激活」。
- **根因**（笔记逐字）：
  1. 0.1.2-alpha.1 迁移把 `dsh-client-store` 变成「冻结平台模块」，共享客户端预设把它 external 化，于是每个重建的客户端 bundle 在求值期硬 require 它；但运行中的 0.1.1-rc.2 宿主没有这个包 —— `require` 落到模块表外。
  2. Typert-gateway 迁移把 `'remote.agentPresets'` 加进了客户端条目的**硬 inject 列表**；这个服务只在 0.1.2 宿主上注册，rc.2 宿主永远不满足 → 条目 pending。
- **修复**（笔记逐字要点）：
  - 不再 external `@deepseek-ai/dsh-client-store` 的 value import；预设把这类导入重定向到一个**生成 shim**，在 bundle 求值期通过 loader 注入的 `require` 解析引擎：**先试平台模块，再退到旧面 `@deepseek-ai/dsh-client-runtime/client`**。shim 的 specifier 用 `join('')` 拼，让静态解析器看不见，从而把 require 原样 emit 进 factory scope。
  - shim **只转发两个引擎共同的值面**：`notifySubscribers` 只在 cohort 包里存在，**绝不能再导出**——未来再 value import 它会以 missing-export 构建失败，而不是静默破坏 rc.2。
  - task-board 客户端：`remote.agentPresets` 从硬 inject 列表移除；改为**使用时探测**：注册了就用 `remote.agentPresets`，否则退到 `connection.api.agentPresets`（迁移前的 rc.2 面）。
  - 笔记明确否决「用 cordis 的软等待」：*"an inject wait either blocks activation (hard) or cannot express 'continue without it' (cordis inject has no optional flag here)"*。
- **给新手的教训**：宿主 SDK 大版本迁移时，**客户端 bundle 的 external/require 是最先炸的地方**；且 **inject 列表是硬门**，多写一个不存在的面（见市场坑 M1）或写少了都会挂。

#### 坑 D2　线协议参数形状与 descriptor 不一致，测试全绿但功能全死

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-28-descriptor-faithful-wire-contracts.md`
- **现象**（笔记逐字）：`session/list` 用 `{request}` 调用，但它的单参数在线上是 `_request`（task-board 结算循环死、手机会话列表死）；`directoryPicker/list` 发 `{request: body}`，但它声明的是一个扁平的可选 `path`（手机浏览死）；业务错误码从 `error.code` 读，但 `TypertRemoteFailure` 把它放在 `error.failure`（配对模型目录返回 502 而不是 409/422）；`CardForm.save()` 把「resolved 的 scope.mutate」当成成功，但 0.1.2 的 scope 在**拒绝后会先做一次恢复性 reload 再 resolve**（被拒绝的保存丢用户草稿）；git-graph 以为 `ISessions.create` 会导航，其实只有 `open()` 才选中（worktree 会话被隐形创建）；手机历史分页重复同一页，因为 `beforeSeq` 从不前进。
- **根因**：调用点把「自己以为的」线协议写进代码，**测试替身也带着同样的错误假设**，所以所有门禁全绿覆盖着静默损坏的路径。
- **修复**（笔记逐字要点）：新增 `invokeWireArgs()` helper 把 invoke 参数按 descriptor 的线布局键：`session/list -> { _request }`、`directoryPicker/list -> 扁平可选 path`、`agentPresets/list` 与 `session/modelCatalog -> {}`、**其余 -> `{ request }`**；测试 fake 也用同一套 descriptor 表，并像网关的 `assertExactArguments` 一样**拒绝多余/缺失的键**；BFF 从 `error.failure` 取业务失败，再退到 `error.code`，并把真实 wire code 映射（`settings-conflict -> 409`、`settings-rejected -> 422`）；`CardForm.save()` 保留单次原子 mutate，但**按「结算后的快照读回」判定**每次计划写入（set：用户层存有该值；unset：字段消失；一次 miss 即整批失败并保留草稿）。
- **给新手的教训**：DSH 的 RPC 参数形状不是「统一 `{request}`」，**要照 descriptor 表**；错误信息在 `error.failure` 不在 `error.code`；测试替身必须和线上同形，否则测试是自我安慰。

#### 坑 D3　把 `ctx.settings` 的 prototype 方法裸引用交给 `useSyncExternalStore`，设置区块首屏必崩

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-09-01-settings-scope-useSyncExternalStore-binding.md`
- **现象**（笔记逐字，含报错）：
  ```
  TypeError: Cannot read properties of undefined (reading 'store')
      at getSnapshot (client.js:998)        <- official dsh-client-ui-settings bundle
      at useSyncExternalStore (frontend bundle)
      at AutoSettingsPanel (AutoSettings.tsx:76)
  slot entry crashed in 'settings.section'
  ```
  每次安装，这个区块首次渲染就崩（v0.3.11 起）。
- **根因**：`AutoSettings.tsx` 把 `props.settings.subscribe` / `props.settings.getSnapshot` 当裸引用传给 `useSyncExternalStore`。settings prop 是官方 `SettingsScope` 实例，这两个方法**是读 `this.store` 的 prototype 方法**；React 以裸函数调用它们，`this` 是 `undefined`。（⚠️ **时效**：该 `SettingsScope` 与手写卡片族已在 `dsh-v0.1.7-rc.1` 移除；本坑按**通用教训**保留。）
- **修复**：用 `useMemo` 绑定：`settings.subscribe.bind(settings)`（保持 hook 身份稳定；scope 对象每个条目身份稳定，不会引起重复订阅）。并**审计全仓所有 `useSyncExternalStore`**，确认只有 settings scope 是 prototype-方法面；补一个「故意用 prototype 方法 fake」的回归测试 + 一个断言「裸调用该 fake 会崩」的前提守卫。
- **给新手的教训**：`ctx.*` / service 上的方法是**带 `this` 的方法**；解构或当回调传出去前先 `bind`。这条和「`ctx.slots.register` 丢 this」（坑 C1）是**同一类事故**，在 DSH 里反复出现。

#### 坑 D4　`ctx.get('xxx')` vs `ctx.xxx`：直接属性读会抛 `cannot get property ... without inject`

- 来源：`omdsh-dev_DSH-better-sidebar` `c81de33`
- 提交信息原文：
  ```
  fix: @-reference button no-ops — read conversation via ctx.get, not the ctx property

  Cordis only grants property reads for services declared in the plugin's
  inject list; every other read throws "cannot get property X without inject"
  (the app's own plugins read 'conversation' through ctx.get for this reason).
  referenceInChat now resolves the conversation service lazily via
  ctx.get('conversation') and no-ops when absent.
  ```
- 来源：`omdsh-dev_DSH-better-sidebar` `197b10a`
- 提交信息原文（更完整，含死锁说明）：
  ```
  fix(sidebar): read betterSidebar via ctx.get() in all internal consumers

  ... the Cordis plugin loader registers the provided betterSidebar impl on a
  neighboring fiber that is not on the rendering fiber parent chain, so every
  direct ctx.betterSidebar read inside the plugin own tree throws

    cannot get property "betterSidebar" without inject

  and the panel dies inside RenderBoundary on page load ... declaring
  betterSidebar in the plugin own inject would deadlock the fiber (it
  waits for the service before running apply, but the service is only
  provided inside apply).

  ctx.get() resolves through the root reflect store and is unaffected by
  the fiber chain, so all 26 internal reads switch to it. External
  consumers keep using ctx.betterSidebar after injecting it, unchanged.
  ```
- **现象**：`@` 引用按钮点了没反应；侧栏面板加载即白屏。
- **根因**：cordis 只允许读 **inject 列表里声明过的**服务属性，其余一律抛错；而**自己 `ctx.provide()` 的服务又不能在 apply 前 inject**（会死锁）。
- **修复**：插件**内部**用 `ctx.get('服务名')`（走 root reflect store，不受 fiber 链影响），取不到就 no-op；**外部消费者**仍照常 `inject` 后 `ctx.服务名`。
- **给新手的教训**：这是 DSH 新手第一个必踩的坑。一句话记住：**自己 provide 的服务，自己读要用 `ctx.get()`；读别人的服务，先在 `inject` 里声明。**

### B 组：热更新 / HMR / 重新挂载

#### 坑 H1　HMR 原地替换 DOM 节点后，观察器挂在已分离节点上永久失效（底栏空白 / 输入框位移）

- 来源：`omdsh-dev_DSH-better-sidebar` `e8d0498`
- 提交信息原文（截断）：
  ```
  fix(drag): 中断/快速释放不再回滚，HMR 后中心列重定位兜底 (#247 #248) (#249)

  #248 HMR 后底栏空白/输入框位移：
  - #root 观察改为 childList+subtree：HMR 原地替换 centerCol 节点时
    childList-only 观察器不触发，ref/RO 挂在已分离节点上永久失效
  - locate 只在列节点身份变化时测量（同节点缩放交给 ResizeObserver），
    rAF 防抖避免流式渲染 mutation 突发强制布局
  - 列节点断开（isConnected=false）时丢弃引用，下次 tick 重新定位
  - 1.5s 兜底重定位 interval：任何 HMR teardown/setup 时序都能在数秒内
    收敛（style 属性字节相同、观察器尚未挂上等盲区全部覆盖）
  ```
- **现象**：改完前端热更新后，底部面板空白、输入框位置漂移。
- **根因**：HMR 会**原地替换** React 树里的 DOM 节点；`childList`-only 的 MutationObserver 对「同一父节点下子树被换」不敏感，`ref`/`ResizeObserver` 还挂在**已分离**的旧节点上，永久失效。
- **修复**：`childList+subtree` 观察；**只在列节点身份变化时**重新测量（同节点缩放交给 ResizeObserver）；`isConnected === false` 时丢弃引用，下个 tick 重新定位；加一个 1.5s 兜底重定位 interval 覆盖所有 HMR 时序盲区。
- **给新手的教训**：任何时候拿到 DOM 引用都要用 `node.isConnected` 兜底；**HMR 下没有「一直有效」的 DOM 引用**。

#### 坑 H2　构建期给产物打补丁不具持久性，任何别的构建路径都能让它复发

- 来源：`omdsh-dev_DSH-better-sidebar` `7eccc49`（revert）
- 提交信息原文：
  ```
  revert: 移除构建期 IME 守卫补丁 — 补丁打在产物上不具持久性

  taekchef 的 apply-ime-guard.mjs 在每次 build/prepare/bundle 后把守卫
  字符串注入 lib/client.js，但补丁对象是构建产物而非源码：
  - 裸 tsdown 重建 / 其他构建路径产出无守卫的 bundle（#562 复发根因）
  - 守卫逻辑游离于源码之外，难以测试与维护

  运行时方案（src/client/ime-guard.ts + tests/ime-guard.spec.ts）已在
  源码内实现同等守卫 ... 任何构建方式产物都自带守卫。
  ```
- **现象**：某个修复「明明提交了」，换个构建命令就复发。
- **根因**：补丁打在**产物**（`lib/client.js`）而不是源码；产物可被任意构建路径覆盖。
- **修复**：把逻辑搬进源码（`src/client/ime-guard.ts`）并带测试，删除构建期注入脚本。
- **给新手的教训**：**永远不要手动改 `lib/`、`dist/` 里的产物**。改源码，重新 build。

#### 坑 H3　「用完不清理」的全局副作用：卸载后样式/变量残留

- 来源：`omdsh-dev_DSH-better-sidebar` `9aeb046`
- 提交信息原文（截断）：
  ```
  fix: sidebar crash #31 — layout-push CSS-variable leak + per-tab error containment

  1. Layout-push leak (root cause): the layout-push effect wrote
     --dsh-sidebar-width/--dsh-sidebar-height on document.documentElement
     without a cleanup, so ANY unmount of the Sidebar (error-boundary swap,
     plugin disable, HMR) left the variables behind and layout.css kept
     squeezing #root with a stale margin — "the sidebar cannot be hidden"
     until a full reload. The effect now removes both properties on cleanup
     (the CSS fallback 0px restores the layout).

  2. Crash containment (UX): the root error boundary previously replaced the
     WHOLE sidebar — toggle cluster included — with an error strip on any tab
     crash. A new shared RenderBoundary (src/client/RenderBoundary.tsx) now
     scopes containment per tab ...
  ```
- **现象**：侧栏「关不掉」，必须整页刷新；任一个 tab 崩溃会把整个侧栏（连开关）换成错误条。
- **根因**：① 往 `document.documentElement` 写 CSS 变量却没 cleanup，卸载（错误边界切换 / 插件禁用 / HMR）后残留；② 错误边界粒度太粗。
- **修复**：effect cleanup 里 `removeProperty`；错误边界**按 tab 收敛**（`src/client/RenderBoundary.tsx`），用 `createElement` 渲染 descriptor 让顶层组件 throw 也能落进边界。
- **给新手的教训**：往 `html`/`body` 写 token/变量/属性，**必须成对写 cleanup**；否则用户唯一的自救方法是刷新页面。dsh-web 也有一条同源坑：skin 锁 `html,body` 的 `overflow` 后必须自己成对清理（见坑 S1）。
### C 组：插槽 slots

#### 坑 C1　把 `ctx.slots.register` 解构成裸函数调用，丢 `this` 后抛 `reading 'effect'`，且被空 catch 吞掉

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-26-dsh-perf-render-shadow-rework.md`
- **现象**（笔记逐字）：
  > **P1 assistant-step shadow never registered**: `registerAny = ctx.slots.register; registerAny(...)` strips the service instance (`this`), so `register` threw `Cannot read properties of undefined (reading 'effect')`. The original catch was empty, hiding the failure; the fiber chain proved the official `AssistantNodeView` always rendered.
- **根因**：① 解构丢 `this`；② **空的 catch 把失败藏了**（日志里什么都看不到）。
- **修复**（笔记逐字）：*"registration uses the lowest existing priority minus one to win the keyed cell, and the register call is bound to the slot service instance"*；并且 *"All three shadow/enable failure paths now log (warn) instead of swallowing silently, plus one per-page diagnostic line reporting the registered priority and the projected cell winner."*
- **给新手的教训**：**不要解构 `ctx.xxx` 上的方法**；**不要写空 catch**。

#### 坑 C2　直接 `slots.register` 会早于宿主的子插槽声明，抛 "not declared"

- 来源：`omdsh-dev_DSH-better-sidebar` `0f9af85`
- 提交信息原文（逐字）：
  ```
  fix: 聊天产出文件行拦截改用 slots.inject 延迟注册（issue #15）

  conversation.chat.turnTail 是宿主 ui-conversation 在 conversation.chat.node
  children 表中声明的子插槽，直接 slots.register 会早于声明而抛
  "not declared (a parent entry's children table must declare it)"，
  导致拦截注册失败回退默认 deliverables 行为并弹诊断条。

  改用 ctx.slots.inject 等待声明落账后再注册（与官方
  dsh-client-ui-deliverables 同款写法）：已声明则同步注册，未声明则
  在声明提交时注册，声明撤销自动卸载、重声明重新注册，fiber 卸载
  幂等清理。
  ```
- **现象**：往 `conversation.chat.turnTail` 注册拦截「注册了但没生效」，回退默认行为并弹诊断条。
- **根因**：该插槽是宿主的**子插槽**（父条目 `conversation.chat.node` 的 children 表里声明的），**声明时机晚于**你的 apply。
- **修复**：用 `ctx.slots.inject`（等声明后再注册；已声明则同步注册；声明撤销自动卸载；重声明重新注册；fiber 卸载幂等清理）。这正是官方 `dsh-client-ui-deliverables` 的写法。
- **给新手的教训**：**注册插槽先用 `slots.inject`，不要用 `slots.register` 硬怼**；DSH 里「注册了但没显示」九成是插槽名写错（要用宿主的**全名**如 `conversation.chat.turnTail`）或注册时机太早。

#### 坑 C3　keyed slot 的 `(key, priority)` 唯一性：两个插件都算 `-1` → 后 apply 的那个直接抛错

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-27-perf-shadow-priority-headroom.md`
- **现象**（笔记逐字）：
  > The keyed client slot `conversation.chat.node` enforces uniqueness per `(key, priority)` pair: registering an entry that collides on both throws, and the throwing plugin fails to apply ("keyed slot ... already has an entry ... registered by ...").
  > Loading the family bundle together with better-session therefore failed client boot: dsh-perf claimed `assistant-step` at `-1` first (registration order depends on apply order), and message-actions then threw on the same `(key, priority)`. Whichever order the two apply in, one of them dies while both compute or pin exactly `-1`.
- **根因**：`conversation.chat.node` 是 keyed slot，按 `(key, priority)` 去重；`dsh-perf` 用 `min(existing) - 1`（当时算出 `-1`），第三方 `@morlay/ui-conversation-message-actions@0.0.11` 硬编码 `-1`，两者撞车；**谁先 apply 谁活**，与顺序相关。
- **修复**（笔记逐字代码块，**逐字照抄**）：
  ```ts
  const SHADOW_PRIORITY_HEADROOM = 8
  const floor = (existing.length === 0 ? 0 : Math.min(...existing)) - 1 - SHADOW_PRIORITY_HEADROOM
  ```
  即从「紧贴最小值的 `-1`」改为「留 8 格安全带」：官方渲染器在 0 时影子落在 `-9`；若别人先在 `-1`，影子落到 `-10`。**顺序无关**。
- **给新手的教训**：往 keyed slot 注册时**不要用 `-1`、`0` 这类常见值**，留安全带；插槽投影规则（这里是「lowest renders」= 数值小的先渲染）要去宿主文档/官方包里确认。

#### 坑 C4　插槽宿主 DOM 结构变了（0.1.x 把 slot 包进 `[data-slot]`），靠 `nth-child` 的选择器全失效

- 来源：`omdsh-dev_DSH-better-sidebar` `0a07cff`
- 提交信息原文（逐字）：
  ```
  fix: 适配 DSH 0.1.x 的 [data-slot] DOM 结构，恢复 Session log 挤压与布局

  DSH 0.1.x 把 slot 宿主包进 [data-slot] 容器：
  #root > div[data-slot=root] > div.frame > div.centerCol
    > div[data-slot=conversation] > div.root[data-phase]
      > div[data-slot=conversation.session.header] > header

  旧选择器 #root > div > div:nth-child(2) 选中的是 data-slot=root 包装
  层的第 2 子元素（不存在，其唯一子元素是 frame），导致：
  - 折叠态 header 右 padding 挤压失效（Session log 胶囊被按钮簇盖住）
  - 底部面板纵向挤压 / 拖动过渡 / 减少动效全部失效
  - Sidebar.tsx 中间列定位器（#root > div 的 children[1]）失效，
    底部面板宽度测量回退为 0

  修复：全部改用 [data-slot] 语义锚点——
  - 中间列：#root > div[data-slot=root] > div > div:nth-child(2)
  - header：body[data-dsh-sidebar-collapsed]
    [data-slot=conversation.session.header] > header
  - Sidebar.tsx 定位器：#root [data-slot=conversation] 的 parentElement
    （= centerCol，探针实测确认）
  ```
- **现象**：升级宿主后，自己的定位/挤压样式**静默失效**（不报错，只是不对）。
- **根因**：宿主 0.1.x 给每个 slot 包了 `[data-slot=<插槽全名>]` 容器，改变了 DOM 层级；`nth-child` 这类位置选择器全部错位。
- **修复**：改用 `[data-slot="<插槽全名>"]` 语义锚点 + 属性锚点，而不是位置。
- **给新手的教训**：**不要用 `nth-child` 锚定宿主 DOM**；用 `[data-slot="..."]`、`[data-dsh-plugin]`、`[data-dsh-part]` 等语义属性（§三 有 dsh-web 的强制规范）。

#### 坑 C5　插槽 host 里「像自己」的 DOM 是别人的：宿主 slot 内已有官方组件，叠加成三层

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-24-wallpaper-exclusive-queue-dock-chrome.md`
- **现象**（笔记逐字）：
  > The native queue dock (the `data-queue-dock` element rendered by QueueDock in dsh-client-ui-conversation) stacks two boxes inside the conversation.input.dock slot: a root whose class contains `_dock` and therefore receives the skin input-card material, whose horizontal padding reads as a halo ring around the content, and an inner panel that paints its own near-opaque `--dsw-specific-tip` fill with a top-only border radius plus an ::after bottom highlight that reads as a bright seam above the composer card. With wallpaper-exclusive active the queued message renders as three visible layers instead of one.
- **根因**：`conversation.input.dock` 插槽里已经有官方组件自己的两层盒子；皮肤再叠一层材质，视觉上成了三层。注意：**官方组件的类名是带哈希前缀的**（如 `_dock`），且随版本变化。
- **修复**：用**属性锚点** `[data-queue-dock]`（而不是类名）收窄作用域；并明确否决「全局重映射 `--dsw-specific-tip`」（*"a global token remap would leak into unrelated consumers of that token"*）。
- **给新手的教训**：**不要用宿主组件的哈希类名做选择器**；用 `data-*` 属性或 `[class$="_xxx"]` 尾匹配（dsh-web 多处用 `[class$="_frame"]` / `[class$="_centerCol"]` 这种写法）。另注意：宿主 patch 里出现的 `[data-phase="active"]` 可能是**死代码**（该笔记原文：*"The `[data-phase="active"]` gate from the earlier round matched no shipped shell build and is removed as dead code"*）。
### D 组：样式 / 主题

#### 坑 S1　给 `#root` 加 `width: 100% !important` 直接顶死第三方侧栏

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-27-skin-center-root-width-lock.md`
- **现象**（笔记逐字）：
  > Skin Center 0.3.5 added viewport and root lock rules ... However, it placed `width: 100% !important;` on `[id="root"]`. This broke third-party sidebar plugins like `dsh-better-sidebar` (#1222), which resize `#root` via `#root { width: calc(100% - var(--dsh-sidebar-width, 0px)) }` ... the `!important` rule forced `#root` to remain at 100% width, causing the right sidebar panel to float over and obscure chat messages.
- **根因**：为了防外层滚动条，给 `#root` 上了 `width !important`，**把「别人要靠改 `#root` 宽度来推挤布局」这条契约踩死了**。
- **修复**：`width: 100% !important` → **`max-width: 100% !important`**；保留 `height/max-height/overflow/box-sizing`。
- **给新手的教训**：`!important` 在插件生态里是**跨插件事故**。要用就说清「我要锁的是什么、不锁什么」。

#### 坑 S2　CSS Modules 同名哈希撞车：8 个包都叫 `settings-card.module.css`，7 个的样式被去重守卫吃掉

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-09-02-css-module-style-tag-collision.md`
- **现象**（笔记逐字）：
  > In the deployed web GUI every family settings card except the first-processed one rendered as bare UA defaults: collapsed cards were fit-content inline buttons instead of full-width disclosure rows, and the pet / doctor / task-board / remote / describe-image / desktop-launcher fields had no styling at all, under every appearance skin.
- **根因**（笔记逐字）：
  1. 共享客户端预设（`shared/tsdown.client.ts`）用 `data-plugin-css = "<bundle id>/<basename>"` 给注入的样式表打 tag。聚合构建内联了 8 个包，每个都带自己的 `settings-card.module.css`，**8 个 tag id 相同**，幂等守卫让第一个 tag 压制了其余 7 个；而每个包的 class map 带**基于路径**的 CSS-modules 哈希 → 7 份 class map 指向从未注入的样式。
  2. `scripts/sync-shared.mjs` 的 `SETTINGS_CONSUMERS` 漏了 `dsh-perf`，它的卡壳副本漂移。
- **修复**：预设改用**完整 repo 相对文件 id** 作为 tag key（`<bundle id>/packages/<pkg>/src/client/<file>.module.css`），同名不同包的模块不再互相压制；`data-plugin`（卸载清理键）不变。并给 `sync-shared` 增加 `SETTINGS_CARD_ONLY_CONSUMERS` 分层。笔记明确否决替代方案：*"Content-hash dedupe of identical stylesheets: rejected — CSS-modules hashes derive from the file path, so identical copies still produce different class maps and cannot share one tag."*
- **给新手的教训**：多个插件被同一 bundle 内联时，**样式注入的去重键不能用文件名**；这也是「CSS Modules 哈希由路径决定」这一事实的实战后果。

#### 坑 S3　`backdrop-filter: blur()` 挂在根容器上，流式输出时 GPU/CPU 爆 80%

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-09-03-blue-fantasy-backdrop-filter-perf.md`
- **现象**（笔记逐字）：*"When using the Blue Fantasy skin with a background image ... during session task runs with continuous streaming token output, the GPU and CPU load reached over 80% (issue #1358)."*
- **根因**：`patches.css` 把 `backdrop-filter: blur(12px)` 挂在根视口容器 `.aionui-root` 上；**聊天气泡每追加一个 token 都触发整视口重绘 + 对壁纸做昂贵的高斯模糊重采样**。
- **修复**：把 `.aionui-root` 从 blur 规则里去掉，blur 只留在侧栏列；给侧栏列加 `contain: paint`，让聊天区的 DOM 变更不再让侧栏图层失效。笔记明确否决「去全局 blur」和「节流 React 流式更新」。
- **给新手的教训**：**`backdrop-filter` 永远不要挂在滚动/流式更新的容器上**；用 `contain: paint` 把重绘关在局部。

#### 坑 S4　暗色/亮色双方案：卡片故意保持深色，但亮色下没设文字色 → 深底深字看不见

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-24-maid-atelier-light-composer-contrast.md`
- **现象**（笔记逐字）：*"with the maid-atelier (Abyssal Maid Atelier) skin active in the light scheme, text typed into the conversation composer is unreadable."*
- **根因**：composer 卡片在**两种方案下都故意保持深蓝**；壳层通过卡片里一个高亮背板 div 画输入文字（textarea 用透明 `-webkit-text-fill-color` 叠在上面，只贡献光标和选区；`[data-input-mirror]` 是 `visibility:hidden` 的测量副本），而**亮色覆盖没设背板颜色** → 继承了亮色墨色 `#172347`，深蓝底 + 深蓝字。亮色光标 `#405a99`、placeholder `#4d5d7f` 同病。
- **修复**：把 composer 卡片当作「方案无关的深色面」，把背板/镜像文字 `#eef3fc`、光标 `#bcd2ff`、placeholder `#b6c2e0` 在两种方案下都钉死；删掉多余的 `body[data-ds-dark-theme]` 覆盖。skin 版本 bump 0.3.0→0.3.1。
- **给新手的教训**：暗色/亮色不是「只调背景色」；**只要有一处背景不随方案变，那里的文字色/光标色/placeholder 就都不能继承默认墨色**。

#### 坑 S5　token 误用：把品牌色当填充色 → 官方主题下黑底黑字/白底白字

- 来源：`dsh-web`　`packages/AGENTS.md`（**逐字可读**，原文引用）：
  > 填充主按钮一律用主按钮三件套（`--dsw-alias-button-primary-fill` / `--dsw-alias-button-primary-hover` / `--dsw-alias-label-primary-foreground`，明暗两组），不得把 `--dsw-alias-brand-primary` 当填充色（官方主题下它与前景同值，会出现黑底黑字/白底白字）
- **给新手的教训**：**颜色只用语义 token，不要用品牌色当填充**；这是被写进包级规范的血泪条款。

#### 坑 S6　skin 覆写 `--dsw-skin-scrim` 与背景显隐互相踩：拖动宠物/切模型把背景不透明度重置成 0

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-24-skin-background-scope-reset.md`
- **现象**（笔记逐字）：*"moving the whale pet or switching models can reset the Skin Center background occlusion to 0%."*
- **根因**：旧的 `skin-background` settings scope 在**任何 settings 文档变化**时都会发布一份 schema 解析后的 section，而 Skin Center v2 的 active-state 文档才是背景的权威存储。把「解析后的 section」当成完整替换，会让 schema 默认值 `backgroundOpacity: 0` 覆盖已持久化的值（如 100）。
- **修复**：把旧 scope 当成**带 revision 围栏的原始用户字段补丁**——没有 namespace revision 或 revision 相同的发布一律忽略；只读取 `snapshot.user`，过滤并归一化「已知且显式存储」的字段，合并进 v2 背景，**绝不用 schema 默认值替换缺失字段**。相关同源坑：`2026-08-26-skin-center-scrim-and-scope-guard.md`（*"removed all hardcoded scrim variable overwrites in `setBackgroundLayer`, keeping `--dsw-skin-scrim` under the sole authority of `BackgroundController`"*）。
- **给新手的教训**：**两个东西都想当「唯一事实源」时必然打架**。settings 的多源合并要按「显式用户字段」而不是「schema 解析结果」合并。

#### 坑 S7　解析 CSS 做审计时 at-rule 递归爆炸，skin 校验跑 ~126 秒

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-25-token-audit-at-rule-recursion.md`
- **现象**（笔记逐字）：*"`auditTokenContract` ... at-rule branch recursed with `visit(open + 1)` and no block boundary ... on nested at-rule chains (`@media` > `@supports` > `@container` > `@keyframes`, the shape a v1 CSS-modules bundle keeps after migration) the traversal became exponential — auditing the migrated orca-link patches.css took ~126 s and the `dsh-skin validate` / check gates hang on any such skin."*
- **根因**：递归没有 **block 边界**，每个 at-rule 都重扫剩余全部块 → 嵌套 at-rule 下指数级。
- **修复**：把 at-rule 递归限制到它自己的闭合花括号内：`visit(start, limit, ...)`，`limit` 封顶在外层 close。
- **给新手的教训**：解析 CSS（而不是直接交给浏览器）时，**嵌套结构必须有边界**；lightningcss 会产出嵌套 `@media`，这类输入是常态。

#### 坑 S8　宿主锁住 `html,body` 的 `overflow` / `height` 后，第三方布局推挤配套失效

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-26-viewport-scroll-lock-on-workspace-select.md`
- **现象**（笔记逐字）：*"When selecting or switching a workspace ... the page viewport scrolled downward unexpectedly. The top titlebar and sidebar top were displaced offscreen, `#root`'s bottom border moved to the middle of the viewport, and a large black void appeared at the bottom with a global window scrollbar."*
- **根因**：`html` / `body` 没有 `overflow: hidden`，而 `#root` 在某些皮肤下有 `border: 1px solid` 而没有 `box-sizing: border-box`，产生轻微溢出，浏览器 `focus()` / `scrollIntoView()` 把它滚到了底部。
- **修复**：`html, body` 锁 `height/width/overflow/margin/padding`；`[id="root"]` 锁 `box-sizing: border-box / height / max-height / overflow`（注意**用 max-width 不用 width**，见坑 S1）；`installShellRenderingAdapter()` 里调用 `doc.defaultView?.scrollTo?.(0, 0)` 复位已有滚动偏移；并修皮肤自己的 `box-sizing`。
- **给新手的教训**：**「锁视口」和「让别人推挤布局」是一对矛盾**；锁的时候只锁 `max-*`，把可变更的自由留给别人。
### E 组：插件启用/禁用 / 启停

#### 坑 P1　禁用「载体 bundle」只写了 insert 行的 `disabled: true`，它的顶层副作用行照样生效 → 启动断链

- 来源：`dsh-market_dsh-market` `263665c`
- 提交信息原文（逐字，截断）：
  ```
  fix: 禁用载体 bundle 时连同其 patch 副作用一起回滚 (#224) (#225)

  禁用一个"载体 bundle"（cordis.patch.yml 既 insert 自己的插件、又有顶层行
  修改其他插件的包）时，市场只往 user-patch 写 inserted 行的 disabled: true
  （#147 的结构归属），但 bundle 仍留在 dsh.profile.bundles，其副作用行
  （禁用官方后端 / 改其他插件 config）每次启动照样应用，导致启动断链。
  真实案例 dsh-postgres-backends：禁用后 session-persistence-jsonl 仍被禁、
  storage-domain 仍路由到已禁用的 postgres，sessionPersistence 无提供者。

  修复：toggle 检测到载体 bundle（carrierSideEffectIds = 全部 entry id 减去
  inserted id）时，禁用则把它移出 dsh.profile.bundles、启用则加回---
  bundle patch 整体不再应用，两类副作用同时消失。纯 insert 插件维持原 HMR
  快路径。载体 toggle 需要重启（bundles 为启动期读取）。
  ```
  以及同 PR 的第二段修正（**判据过宽**的教训）：
  ```
  fix: 载体判定收窄为"禁用其他插件"，修复 fixture-cross 重新启用失败 (#224)

  ... 首版 carrierSideEffectIds 把任何顶层副作用行都判为载体，而 e2e 的
  fixture-cross 只是改邻居 dshm-fixture-b 的 config（无 disabled），被误判后
  移出 dsh.profile.bundles，破坏了重新启用 ... 收窄判据：carrierDisableIds
  只识别顶层 `disabled: true` 行（禁用其他插件）。
  ```
- **给新手的教训**：**`cordis.patch.yml` 里「插自己」和「改别人」是两类行**：`- insert:`（自己）与顶层 `- id:`（改已有的别人）。禁用插件时**两类都要处理**，否则会留下幽灵副作用。

#### 坑 P2　把「最后一个 patch 行」删干净后，user patch 层变成纯注释，宿主直接拒启

- 来源：`dsh-market_dsh-market` `bb260cb`
- 提交信息原文（逐字）：
  ```
  fix: never leave the user patch layer without a top-level array

  Disable a plugin, then enable it again, and dsh refuses to start the profile:

    dsh: overlay .../cordis.patch.yml must be a top-level YAML array of
         loader patch entries

  Appending the first row comments the dsh template's `[]` placeholder out (it
  has to — appending after it would put two elements in one document), so
  removing the LAST row left a file of pure comments. yaml.load returns
  undefined for that, dsh's parsePatchList rejects anything that is not an
  array, and the profile will not boot at all. An emptied file has the same
  problem: yaml.load('') is undefined too, and one existing spec asserted
  exactly that empty result — it had encoded the bug as the expectation.
  ```
- **给新手的教训**：**动别人的 YAML 要保证「顶层永远是数组」**；同时注意「一个测试把 bug 编码成了期望」（把 bug 写进了断言）。

#### 坑 P3　装上市集后宿主起不来：ESM 具名导入一个已被删除的 export，任何兜底都来不及跑

- 来源：`dsh-market_dsh-market` `a99a205`
- 提交信息原文（逐字，截断）：
  ```
  fix: installing the market no longer stops dsh 0.1.2-alpha from booting (#437)

  dsh 0.1.2-alpha.2 reached npm today. With the market installed, the host
  does not start:

    SyntaxError: The requested module '@deepseek-ai/dsh-settings' does not
    provide an export named 'installSettingsSection'
    ... dsh exited 1

  0.1.2-alpha.1 deleted `installSettingsSection` and moved `settingsNamespace`
  to another package. src/settings.ts imported both by name.

  The distinction that matters is between a missing SERVICE and a missing
  EXPORT. This module was written for the first: its comment explains that the
  wiring rides a scoped fiber, so a host without a settings service simply
  never runs it. That is true, and `ctx.inject` still does exactly that. But an
  ESM named import of an export that no longer exists cannot degrade — it
  throws while the module is being evaluated, cordis records a failed entry,
  and the host exits 1. The graceful path never got a chance to run. A plugin
  must not be able to stop the host from starting.

  The service itself never changed. `settings.register(ns, schema, { base })`
  is identical in 0.1.0-rc.7 and 0.1.2-alpha.2; only the two convenience
  wrappers went away. So this inlines what the wrapper did ...
  ```
- **给新手的教训**：**「服务缺失」可以优雅降级；「ESM 具名导出缺失」是模块求值期就炸，会带着整个宿主 exit 1**。核心 SDK 只依赖**稳定的 service seam**，不要依赖便利包装函数。

#### 坑 P4　启动期隔离：一个坏插件会拖垮整个家族（甚至整个 `dsh web`）

- 来源：`dsh-web`　`.agents/notes/implemented/architecture/2026-09-01-aggregate-plugin-fault-isolation-shell.md`
- **现象**（笔记逐字）：*"The loader treats all rows as one transactional group (`EntryGroup.update` in the vendored cordis loader): any entry that fails to import or start rolls the whole group back, and the boot audit (`assertEntriesActivated` in `@deepseek-ai/dsh-app-boot`) then aborts the entire `dsh web` process. One broken plugin — an SDK drift, a bad release, a third-party import — took every plugin down"*
- **修复**：每个家族 insert 行的 `name` 改为聚合包的**按家族子路径导出** `@linxin666/dsh-web-all/<family>`，真包名放进 row config 的 `config.plugin`；shell（`packages/dsh-web-all/src/shell.ts`）在 start 时 import 真模块，导入失败/形状不可用/激活失败都被**捕获、记录**，shell 条目本身保持 ACTIVE。另加 `shared/host/run-guarded.ts` 把 fire-and-forget rejection 变成 logged error（因为宿主的 `installFailLoud` 会把**任何** unhandled rejection 变成整进程退出）。
- **给新手的教训**：宿主 loader 把一次 boot 里所有 row 当**一个事务组**；写插件要假设「我挂了不能连累别人」，并且**绝不允许 unhandled rejection 逃逸**（宿主会直接 exit）。

#### 坑 P5　菜单/开关状态与宿主不同步：宿主已禁用的插件，行里还让它显示可点开关

- 来源：`dsh-market_dsh-market` `a40d2d0`
  `fix: market row shows a disabled switch with a tooltip instead of a server-rejected toggle (#99)`
- 相关：`dsh-market_dsh-market` `334965a` `feat: universal plugin enable/disable, catalog-driven deprecation, and custom groups (#60, #11, #59) (#94)`
- **给新手的教训**：**宿主拒绝的开关不要让它「看起来能点」**；失败要显性化。

#### 坑 P6　改了开关要重启，但用户以为已生效

- 来源：`dsh-market_dsh-market` `53c0956` `fix: clear pending restart after successful hot mount (#75)`
- 相关：`dsh-market_dsh-market` `946d765` `fix: an update of a running plugin reads as "restart", not "live" (#172)`；`dsh-market_dsh-market` `a3e7141` `fix: a standing, dismissible restart notice for host-reported pending plugins (#146)`
- **给新手的教训**：**「已生效」和「待重启」必须区分得很清楚**，并在热挂载成功后清掉 pending 标记。

### F 组：构建 / 打包 / `exports` / client bundle

#### 坑 B1　声明了 `dsh.client.platform: "web"` 但 `package.json` 没导出 `./client` → 整个 profile 组合失败

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-26-dsh-perf-client-export.md`
- **现象**（笔记逐字）：
  > `dsh --profile web` fails before the Web UI starts with `client-modules: 1 client package failed to compose`: `@linxin666/dsh-perf` declares `dsh.client.platform: "web"` but its `package.json` does not export `./client`. The official client-modules loader resolves the declared browser half through `exports["./client"]`, so the missing subpath is treated as a plugin composition error even though `lib/client.js` already exists.
- **修复**：`packages/dsh-perf/package.json` 加标准客户端子路径：`"./client"` 的 types 指 `./lib/types/client/index.d.ts`，runtime 指 `./lib/client.js`；保留原 `dsh.client` 声明。笔记明确否决「用纯字符串 export」：*"the repository family convention uses the conditional object with a `types` entry, and the loader accepts that form directly."*
- **给新手的教训**：**`dsh.client` 声明与 `exports["./client"]` 必须配对**；只有其中一个，客户端半就不进引导清单。

#### 坑 B2　`dsh.client` 字段名写错（旧字段 `dshClient`）→ 浏览器根本不加载插件

- 来源：`omdsh-dev_DSH-better-sidebar` `53a9ced`
- 提交信息原文（逐字）：
  ```
  fix(client-modules): package.json 补 dsh.client 声明 — client 半未进引导清单的根因修复

  诊断（2026-08-11 重启后侧边栏不显示）：host 半正常（/sidebar/api 路由
  200），但页面 window.__DSH_BOOT__ 引导清单 30 个 client 插件中没有
  dsh-better-sidebar。client-modules 扫描器（packages/client/modules）读
  package.json 的 pkg.dsh.client 声明 + exports["./client"] 组合 bundle；
  插件只声明了旧字段 dshClient（dsH 新版本约定改为 dsh.client，工作正常的
  ui-genui 两者并存）。旧字段缺失 → 负判定缓存 → 无 client 入口 → 浏览器
  不加载侧边栏。

  修复：package.json 新增 "dsh": { "client": { inject, platform } }
  与 dshClient 并存（兼容新旧 dsh）
  ```
  相关：`omdsh-dev_DSH-better-sidebar` `7c792c2` `chore: 移除旧字段 dshClient — 只适配新 dsh 版本（dsh.client 声明）`
- **给新手的教训**：**`dsh.client`（点号），不是 `dshClient`**。验证方法（提交原文给的思路）：看页面 `window.__DSH_BOOT__` 的 client 插件清单里有没有你的包。

#### 坑 B3　`exports` 缺子路径别名（`./client/api`、`./client/service`）

- 来源：`omdsh-dev_DSH-better-sidebar` `39455ff`
  `docs+fix: exports 加 ./client/api 别名；catch-all+detect 纯嗅探规则；设计文档偏差记录`
- 相关：`omdsh-dev_DSH-better-sidebar` `291158a`
  `package.json: 加 ./client/service exports 子路径，version 0.4.0`
- **给新手的教训**：`exports` 是**白名单**；你要让外部 import 的每个子路径都得显式列出来（`.`, `./client`, `./client/service`, `./invariant`, `./src/*` 测试用）。

#### 坑 B4　客户端 bundle 不可复现 / 泄漏构建者绝对路径

- 来源：`dsh-market_dsh-market` `1391ada`
- 提交信息原文（逐字）：
  ```
  build: strip the builder's absolute path from the published client artifact (#121)

  client/client.js is committed AND published, so it must be byte-identical
  regardless of whose machine built it. tsdown names the CSS module's
  virtual chunk by absolute path, so the builder's checkout leaked into a
  region comment: main currently ships /Users/<me>/work/dsh-market/… to
  npm, and #99 arrived carrying D:\Github\… — every contributor's artifact
  diff churned on the path plus every hashed class name.

  normalize-client-banner now rewrites those virtual ids to a stable
  repo-relative form (Windows separators included, so a Windows build
  produces the same bytes) and fails the build if this builder's checkout
  path survives anywhere else.
  ```
- 相关：`dsh-market_dsh-market` `9f15747`：
  ```
  build: make the client bundle byte-reproducible (#171)

  ... The CSS module class map was a hole in that: tsdown emits its keys in an
  unstable order, so two consecutive builds of identical source differed by
  ~265 lines. ... Sorting the map fixes it. ... Four consecutive builds now
  produce identical sha256 for both client.js and client.js.map.
  ```
  以及 `8830b8b`：`chore: stop committing client.js.map, which is where the conflicts were (#533) (#539)`
- **给新手的教训**：客户端 bundle 若**提交进仓库或发布到 npm**，必须**可复现**（路径、CSS Modules class map 的 key 顺序都会被 tsdown 带进来）；否则每个人 `npm install` 都会拿到一个 diff，PR 之间在生成文件上冲突。

#### 坑 B5　聚合包把 8 个包的客户端内联成一个 2.5 MB 产物

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-09-02-aggregate-client-children-mount.md`
- 原文：*"`@linxin666/dsh-web-all`'s `lib/client.js` grows from ~14 KB to ~2.5 MB (the family's client code rides one artifact; the loader serves it as a single entry)."*
- 根因：客户端模块扫描器 `@deepseek-ai/dsh-client-modules` 是**从 loader 的 entries 组合浏览器 bundle 图**的；它**看不到 shell 的 apply 里创建的 cordis 子插件**，所以子插件的客户端 bundle 永远到不了浏览器。修法是让聚合的客户端 bundle**静态 import 每个子插件的 `./client`**（生成 `children.specifiers.json` / `children.generated.ts` / `children.modules.d.ts`），并 `mount-children.ts` 把每个子插件当**嵌套客户端插件**挂载。
- **给新手的教训**：**「宿主半能看到」≠「浏览器半能看到」**。客户端 bundle 的图只由 loader entries 决定；动态 create 的子插件必须显式带进客户端图。

#### 坑 B6　最近邻 `package.json` 规则：多一层子路径导出把扫描器引到错误的清单上

- 来源：`dsh-web`　`.agents/notes/implemented/architecture/2026-09-02-aggregate-family-row-display-names.md`
- **原文要点（逐字）**：*"A marker manifest (`src/shells/package.json`, built into `lib/shells/`) sits beside the re-export: the client module scanner resolves a row's module URL and walks up to the nearest package.json, and the marker (string `name`, `type: "module"`, no `dsh` field) stops that walk before it reaches the package root. Without it, every family row would resolve to the aggregate's own manifest and its `dsh.client` face — `reconcilePackage` then throws "resolves from multiple active Loader sources" ... `type: "module"` is required by the same nearest-manifest rule: without it Node parses the re-export as CJS."*
- **给新手的教训**：**客户端扫描器按「最近的 package.json」判定归属**。你若在包内再造一层子目录导出，务必放一个「标记清单」阻挡向上查找，并带 `type: "module"`。

#### 坑 B7　打包/构建杂项（同一类）

- 来源（提交信息原文）：
  - `dsh-web` `scripts/aggregate.mjs`：手写 YAML 子集扫描器，无 js-yaml 依赖（`2026-08-26-aggregate-harness-row-patches.md` 原文：*"Switch the generator's parser to a general YAML library: rejected — the repository has no js-yaml/yaml dependency, and the existing `parseManifest` already establishes the hand-rolled YAML-subset scanning style"*）
  - `omdsh-dev_DSH-better-sidebar` `61c9c55`：`fix(registry): registry 打包补上 mermaid 懒加载 chunk` —— **懒加载 chunk 要显式补进产物清单**
  - `omdsh-dev_DSH-better-sidebar` `4af8d31`：`fix: devDependency 改用 npm registry 版本，去掉本机 link 路径` —— **不可把本机 link 路径提交进清单**
  - `omdsh-dev_DSH-better-sidebar` `3d23ceb`：`fix(ci): pnpm 版本统一由 packageManager 字段供版，移除 action 显式 version 输入`
  - `dsh-web` `3a645bef`：`fix(pet): bound the frames2d warm pass behind a fetch pool` —— **预热/预取要有界**
  - `dsh-web` `2026-09-10-pet-frames2d-fetch-storm.md`（笔记，文件在但 blob 未本地）：**fetch 风暴**主题
- **给新手的教训**：懒加载/预取/生成物都要有**显式清单 + 一致性门禁**（`--check`）。

DSH_EOF_MARKER
### G 组：时序竞态

#### 坑 R1　启动竞态：host service 还没注册，首次轮询就报错（每次启动都打堆栈级 console.error）

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-28-taREDACTED-SECRET.md`
- **现象**（笔记逐字）：*"the session tree activates `sessionController` only after its nine inject services resolve ... while `TaskBoardHostService.start()` fires the first roster poll immediately during plugin start. The first `session/list` therefore fails with the gateway's `service-unavailable` and every boot printed a stack-trace-level `console.error` ... even though the 5-second poll recovered on its next tick."*
- **修复**：`listRunning` 在网关报 `code: 'service-unavailable'` 时重试（5 次 × 2s 退避，可通过构造参数覆盖）；**只对这一个错误码重试**，其他错误保持单发语义；耗尽后只打一次同样的错误并返回 `{ known: false }`。笔记明确否决「按固定秒数延迟首轮」（*"a blind wait that still races on slow machines"*）和「inject 等 `sessionController`」（*"a hard wait pends the whole entry forever on hosts that never activate the service"*）。
- **给新手的教训**：**插件 start() 时别假设别人的 service 已就绪**；遇到 `service-unavailable` 要**有限重试**，不要硬 inject、也不要盲等固定时间。

#### 坑 R2　会话列表瞬时 `current = undefined` 把看板误关

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-26-taREDACTED-SECRET.md`
- **现象**（笔记逐字）：*"the session list snapshot momentarily emitted `current = undefined`. The controller's `onSessionsChanged()` checked `current !== this.lastCurrent` and immediately called `this.closeBoard()`, closing the task board on click."*
- **修复**：只在「两个有效且不同的 session id 之间导航」时才关：`this.lastCurrent !== undefined && current !== undefined && current !== this.lastCurrent`。同一天的后续笔记干脆**移除了隐式关闭**（`2026-08-26-taREDACTED-SECRET.md`）：看板只由显式用户动作关闭。
- **给新手的教训**：**列表快照会瞬时缺字段**（子代理链初始化、视图挂载时都会）。不要用「值变了就关/就重置」；加 `undefined` 守卫，或干脆别隐式动作。

#### 坑 R3　DOM 被换掉后挂载点不 `isConnected`，返回按钮永久失效

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-27-taREDACTED-SECRET.md`
- **现象**（笔记逐字）：
  > In DSH WebView2 desktop and web environments, clicking the "Return to session" (`返回会话`) button on top of the task board had no response and left the user stuck on the task board view.
- **根因**（笔记逐字）：
  - `BoardController.closeBoard()` had an early-return guard `if (!this.boardOpen) return`, preventing cleanup notification when internal state drifted or needed active attribute teardown.
  - `openSession()` in `controller.ts` navigated to the execution session but did not explicitly invoke `this.closeBoard()`.
  - `board-mount.tsx` had `if (container !== undefined) return;` which did not verify `container.isConnected`. When DSH React re-rendered or swapped the center conversation column, the container disconnected and could not self-heal/remount.
- **修复**：`closeBoard()` 无条件置 `boardOpen = false` 并 `notify()`；`openSession()` 先 `closeBoard()`；`ensure()` 检查 `container.isConnected`，断开则卸载旧 root、移除分离元素、重新挂到当前会话列。
- **给新手的教训**：**「容器已存在就直接 return」是错的**——必须检查 `isConnected`；幂等的 close/cleanup 不要加早退守卫。

#### 坑 R4　面板/布局「推挤」的变量在挂载期不持续有效，拖拽松手后闪一下全宽

- 来源：`omdsh-dev_DSH-better-sidebar` `5cc1a4b`
  `fix(layout): 推挤变量挂载期持续有效，拖拽松手后底边栏不再闪全宽 (#258) (#259)`
- 相关：`omdsh-dev_DSH-better-sidebar` `a2bb04b` `fix: 底栏宽度直测中间列，修复启动竞态下底栏跑到最左边`
- **给新手的教训**：**布局推挤类 CSS 变量要在挂载期持续有效**，不能「设置一次就完」；启动竞态下测量要落到真实列而不是默认值。

#### 坑 R5　子代理实时预览 O(N²) 请求风暴

- 来源：`omdsh-dev_DSH-better-sidebar` `6cea4bd`
- 提交信息原文（逐字，截断）：
  ```
  fix(subagent): 子代理页实时预览改为批量接口，避免 O(N²) history 请求风暴 (#298)
  ...
  旧实现中，每个 running 子代理卡片都独立轮询 subagents.history：
  - N 个 running 子代理 → 每 3 秒产生 N 次 subagents.history 请求；
  - 每次 subagents.history 都会在 host 侧触发一次完整的 listChildren 全量
    子代理目录枚举；
  - 子代理数量越多，服务端重复扫描越严重，近似 O(N²) 放大；
  - 请求超过 3 秒时，客户端还会 abort 旧请求并重发，进一步形成请求风暴。
  改动：① 新增 host 批量接口 POST /sidebar/api/subagents.live；② 客户端改
  为单轮询 + 单飞行请求（递归 setTimeout，慢请求不再被 abort/重发，页面隐藏
  或 root 变化时停止轮询并中止在途请求）；③ 解析器从事件尾部反向扫描、命中
  即停；④ UI 不变。
  ```
  后续 CR 修正（同 PR 第三段）还加了 **12 条消息窗口**：*"lastActivity 增加可选 maxMessages 参数：反向扫描按表面消息计数，窗口满后更老事件一律跳过；路由传 LIVE_WINDOW_MESSAGES = 12（导出常量）"* —— 否则长会话会显示陈旧 tool，且每次轮询反向扫描整个事件数组。
- **给新手的教训**：**列表页不要「每个卡片一个定时器」**；合并成一个轮询 + 单在途请求 + 隐藏页面停止 + 有界窗口。

#### 坑 R6　`getBoundingClientRect` 绝对定位法在皮肤/滚动/动态加载下必错

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-31-git-graph-branch-chip-hero-portal.md`
- **现象**（笔记逐字）：*"In blank sessions, the Git branch selector (`BranchChip`) detached and floated high above the conversation area / hero whale illustration rather than sitting in the row alongside `WorkspaceChip` and `AgentPresetSeat`."*
- **根因**（笔记逐字）：*"`BranchChip` calculated `top = rowRect.top - stackRect.top + ...` (coordinates relative to `div.wSkVaW_composerStack`) and applied `position: absolute; left: ${left}px; top: ${top}px` (`css.anchorHero`). However, `composerStack` and `heroWorkspaceRow` are `position: static` flex containers without an established containing block; the nearest positioned ancestor establishing a containing block was `div.wSkVaW_body` at the top of the conversation view (`y = 0`)."* → 相对 A 算坐标、相对 B 定位，偏几百像素。
- **修复**：不再算坐标，直接 `createPortal(chipNode, heroRow)` 把组件**门户**进官方 `heroWorkspaceRow` flex 容器；隐藏一个零尺寸占位留在 `conversation.input.dock`；`.anchorHero` 用 `display: inline-flex; align-items: center;`，**不用 `position: absolute`**，让 chip 成为原生 flex 子项，继承官方的 2px gap 与响应式流。
- **给新手的教训**：**要做「塞进宿主某一行」的效果，就 portal 进去，别用 `getBoundingClientRect` 算绝对坐标**（跨滚动、视口变化、动态加载、不同皮肤的 containing block 都会错）。

### H 组：跨平台（Windows / 换行符 / 大小写）

#### 坑 W1　`{...process.env}` 展开后 `Path` 与 `PATH` 并存，子进程丢失全部系统目录

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-09-04-desktop-child-env-path-normalization.md`（提交 `7d810121`）
- **现象**（笔记逐字）：*"Plugins relying on Windows DPAPI credential decryption (such as `dsh-chatgpt-subscription`) failed when calling `spawn('powershell.exe', ...)` with `Error: spawnSync powershell.exe ENOENT` ... Any external tools invoked by plugins (such as `codegraph`) failed to resolve"*
- **根因**（笔记逐字，含代码）：
  ```javascript
  const env = { ...process.env, DSH_HOME: home };
  const nodeBinDir = process.platform === 'win32' ? nodeHome : path.join(nodeHome, 'bin');
  env.PATH = nodeBinDir + path.delimiter + (env.PATH ?? '');
  ```
  *"On Windows, the operating system exposes the environment variable as `Path` (mixed-case) rather than `PATH`. When `process.env` (a case-insensitive Proxy in Node) is spread into a plain JavaScript object, the property is stored with its exact key `'Path'`. Because `env.PATH` was undefined before the assignment, `env.PATH` was set to *only* `nodeBinDir`. This left two distinct keys in the environment object: `Path` ... and `PATH` ... When Node.js and libuv serialized the environment block for `CreateProcessW`, `PATH` took precedence or collided, causing child processes to lose all standard Windows system directories (`C:\Windows\System32`, ...)."*
- **修复**：找 `process.env` 里 **PATH 的所有大小写变体**（`Path`/`PATH`…）→ 全删 → 只设一个规范化的 `env.PATH`。并把 `childEnv` 抽出到 `desktop/src/runtime.cjs` 以便单测。
- **给新手的教训**：**Windows 上是 `Path` 不是 `PATH`**；`{...process.env}` 会把这个大小写差异固化，之后写 `env.PATH` 等于**丢掉系统 PATH**。

#### 坑 W2　Windows 上只发 `.cmd` shim，`spawn` 不带 shell → ENOENT / EINVAL

- 来源：`dsh-market_dsh-market` `18abcd3`
- 提交信息原文（逐字）：
  ```
  fix: spawn pnpm/corepack/npm via a shell on Windows (#4)

  Windows only ships .cmd shims for these commands. Node spawn without a
  shell fails with ENOENT (bare name) or EINVAL (.cmd), so probePnpm and
  setup-pnpm always fail and the market UI stays blocked.

  Match dsh's plugin forwarder: shell: process.platform === "win32".
  ```
- 相关：`dsh-web` `404f0c4a` `fix(desktop): run pnpm install through a shell on windows`；`dsh-market_dsh-market` `237e8f5` `fix(cli): avoid Node DEP0190 shell+argv spawn on Windows (#80)`
- **给新手的教训**：**在 Windows 上 spawn `pnpm`/`npm`/`corepack` 要 `{ shell: true }`**（或直接找 `.cmd` 全路径）。

#### 坑 W3　CRLF 让注释剥离正则失效 → Windows 上写的 `cordis.patch.yml` 在**任何平台**都无法热挂载

- 来源：`dsh-market_dsh-market` `01b3c28`
- 提交信息原文（逐字）：
  ```
  fix: a Windows-authored bundle patch can be hot-mounted

  Running layer 3 on Windows turned up a real product bug, not a CI one: with
  CRLF line endings, parseSimplePatch refused a patch that is a plain insert
  list, so the market told the user to restart for a plugin it could have
  mounted immediately.

  The mechanism is a nasty little JS detail. Comments are stripped with
  `raw.replace(/#.*$/, '')`, and `\r` is a LINE TERMINATOR in JavaScript: `.`
  will not cross it, and `$` without /m anchors only at the very end of the
  string. So on `# comment\r` the pattern never matches, the comment survives,
  matches none of the row shapes, and hits the parser's `return null` — which
  the caller reports as "the bundle patch contains config/expression rows".

  The user-visible effect: any plugin whose cordis.patch.yml was authored on
  Windows could never hot-mount, on ANY platform, and always demanded a
  restart. Both parsers now split on /\r?\n/.
  ```
- **给新手的教训**：解析文本一定要 `split(/\r?\n/)`；**JS 里 `\r` 是行终止符**，`$`（无 `/m`）只匹配字符串末尾，`#.*$` 对 `# comment\r` 永不匹配。

#### 坑 W4　`import.meta.url` 与 `process.argv[1]` 的直接入口判断在 Windows 永远为 false（CLI 静默退出 0）

- 来源：`dsh-web`　`.agents/notes/implemented/bug-fix/2026-08-27-doctor-windows-supervisor-lifecycle.md`
- **现象**（笔记逐字）：*"src/cli.ts compared `import.meta.url === new URL(process.argv[1] ?? '', 'file:').href`. On Windows, drive letters in `process.argv[1]` (e.g. `C:\...`) produced malformed file URLs when constructed with `new URL(..., 'file:')`, causing the equality check to always evaluate to false. CLI commands exited silently with code 0 without executing main()."*
- 同笔记另两条 Windows 坑：
  - *"`service.ts` mistakenly imported path helpers from `node:path/posix`, corrupting Windows absolute paths."*
  - *"`runCommand` passed `{ shell: true }` on Windows, causing cmd.exe to break paths containing spaces (e.g. `DSH Doctor`) into multiple arguments and failing `schtasks /Create`"* —— **与坑 W2 相反**：这里 `shell: true` 反而害事（该传精确 argv 给 `schtasks.exe`）。
- **修复**：入口判断改为 `fileURLToPath(import.meta.url)` + `resolve(entryArg)`，Windows 下大小写不敏感归一；按目标平台选 `win32` 或 `posix` path 模块；`/TR` 目标路径加引号；去掉 `shell: true`。
- **给新手的教训**：**「要不要 shell」取决于具体可执行文件**——`.cmd` shim 要 shell，`.exe` 精确参数不要 shell；路径比较用 `fileURLToPath` + `resolve`，别手拼 `file:` URL。

#### 坑 W5　Windows 盘符路径解码多/少前导斜杠被拒

- 来源：`omdsh-dev_DSH-better-sidebar` `6b4fed1`
  `fix(html): Windows 盘符路径解码去掉前导斜杠，修复 html 预览被 isWithin 拒绝`
- 相关：`omdsh-dev_DSH-better-sidebar` `180b16d` `fix: 修复 WSL 会话 Linux 路径解析 (#399)`；`81ab0c5` `fix: cross-platform path handling and tests`；`db189e3` `feat: 统一路径处理——UNC/软链接分类/html 路由平台守卫`
- **给新手的教训**：路径要**统一入口归一化**（UNC、盘符、大小写、正/反斜杠、软链接），不要在几十处各写一遍解析。

#### 坑 W6　Windows 更新/解压/子进程/安装脚本杂项

- 来源（提交信息原文）：
  - `dsh-web` `36de9e36` `fix(desktop): extract runtime archives with windows-safe bsdtar`
  - `dsh-web` `00251900`：`fix(desktop): stage the windows cloudflared binary and self-heal wrong-arch ones` —— 原文要点：*"The payload's cloudflared postinstall only fetches the build machine's platform binary, so Windows installers shipped a macOS arm64 cloudflared"*
  - `dsh-market_dsh-market` `9f0ac8c` `fix: hide Windows child process consoles (#536)`（无正文）
  - `dsh-market_dsh-market` `33a5153` `fix: explain a Windows locked-file rename instead of showing pnpm's stack (#394)`
  - `dsh-market_dsh-market` `99ab687` `fix: honor Windows npm global prefix (#413)`
  - `omdsh-dev_DSH-better-sidebar` `9642e95` `fix: install.ps1 兼容 PowerShell 5.1（node -e 改临时文件，补 UTF-8 BOM）`
  - `omdsh-dev_DSH-better-sidebar` `d94465c` `fix: install.sh 变量加花括号（$WS_YML：→ ${WS_YML}），修复 macOS bash 3.2 下 unbound variable（#23）`
  - `omdsh-dev_DSH-better-sidebar` `71c5413` `fix(git): hide spawned git windows on Windows (#301)`
  - `omdsh-dev_DSH-better-sidebar` `7499383` `fix(terminal): resolve Windows custom shell executables (#487)`
  - `omdsh-dev_DSH-better-sidebar` `ac02598` `fix: preserve Windows explorer reveal selection`
  - `omdsh-dev_DSH-better-sidebar` `ddd3bed` `merge #47: fix PowerShell installer BOM parse and pnpm version check`
  - `omdsh-dev_DSH-better-sidebar` `24db20a` `test: make five suites Windows-runner clean`
- **给新手的教训**：Windows 相关坑**必须真机跑 CI**。市场那条说得很直白（`01b3c28`）：*"the whole suite was green on Linux and macOS throughout, and it would have kept hiding there."*

---

## 一-I 组：其它高频坑（跨主题，dsh-web 为主）

#### 坑 X1　z-index 层级：宿主的 shell.overlay 是 absolute inset:0 / z-index 20，插件面板默认被压在下面

- **来源**：zhu1090093659_dsh-web 08ea9de3 fix(aionui-panel): lift panel columns above shell.overlay layer (#195)；a36f60f6 fix(task-board): raise board container and modal z-index above panel overlays (#54)；40e15c77 fix(dsh-aionui-panel): keep panel frame chrome below the shell overlay layer (#234) (#259)
- **现象**：插件面板/看板/弹窗被宿主的 overlay 图层盖住，点不到、看不清；右下角区域尤其容易被盖。
- **根因**（提交原文）："The core AppFrame renders the shell.overlay slot as an absolute inset:0 layer at z-index 20 over the whole frame grid. With the aionui panel tracks appended as grid columns (4/5), right-edge overlay plugins painted on top of the Explorer / Preview content."
- **修复**：给插件自己的列/容器显式 z-index: 30 —— "above the overlay, below dialogs 1000+"，并沿用既有的 "tab-bar z-index 30 convention"；同时外壳 chrome 要低于 overlay（40e15c77），所以是分层而非一味抬高。
- **给新手的教训**：DSH 宿主自有一套 z-index 常量（shell.overlay = 20，对话框 = 1000+）。插件不要用 9999 一把梭，先在自己的层（20~30）里解决；抬得比对话框还高会盖住系统的确认框。

#### 坑 X2　不要把 React 拥有的 DOM 节点「搬家」——insertBefore / removeChild 锚点会失效

- **来源**：zhu1090093659_dsh-web baa711b4 perf(remote-web-ui): stop re-parenting the header actions and cut per-tick layout reads
- **现象**：把宿主已有的 React 节点搬到自己的容器里，界面上"看着没坏"，但后续 React 更新报错/错位；节点里的实时按钮（如后台任务徽标）变成点了没反应的死按钮。
- **根因**（提交原文）："The seated header actions were moved into the tabs row, which makes React's later insertBefore/removeChild anchors point at a node that is no longer a child of its recorded parent, and the background-task badge inside the node is a live React button a clone could not keep."
- **修复**：节点留在 React 原来的位置，改用「注入 CSS 把它移出文档流 + 用一个收敛的 transform 画到目标位置」，目标位置用 padding-right 预留被画上去的宽度。（同一提交还修了两个相邻坑：600ms 定时器每 tick 强制同步布局读取；以及靠匹配官方按钮文案来"下钻"选择器，在别的语言下永远不触发，改为结构化回退。）
- **给新手的教训**：宿主渲染出来的 DOM 属于 React。你可以改它的 class/样式，**不要改它的父子关系**。要"搬"就用视觉手段（CSS transform / position），不要用 DOM 手段。官方节点里的按钮可能是活的 React 组件，clone 出来的只是空壳。

#### 坑 X3　浏览器自动翻译会替换 React 底下的 text node，React 抛 NotFoundError，整段 UI 卸载变空白

- **来源**：dsh-market_dsh-market 43d5768 fix: a translated page can no longer blank the market (#293) (#513)；7133ed3 release 1.43.0: the blank market, and four failures that described themselves wrong
- **现象**：用户开了 Chrome/Edge 的整页翻译之后，市场面板**整块变空白**——连「导出日志」按钮都一起消失，所以从那个状态导出的日志永远是空的，导致这个 bug 在 #286 / #241 / #293 上挂了几个月、始终无法在身边复现。
- **根因**（提交原文）："Chrome and Edge translate by replacing text nodes underneath React; React then tries to remove a node its parent no longer has, throws NotFoundError, and the whole section unmounts."
- **修复**（逐条照抄要点）：
  1. 在市场根节点**以及 portal 宿主**上加 `translate="no"` 与 `notranslate`。**portal 宿主也必须加**，因为对话框和 lightbox 从那里渲染——"a translated dialog crashes React exactly the same way"。
  2. 只对自己子树生效："Scoped to this subtree: the host page around it still translates."
  3. 导出的日志里读 html 元素上 Chrome/Edge 留下的标记，写明"本页是否被浏览器翻译过"——"A fact, not a verdict — a translated page is not by itself a fault"，但这正是用户永远不会主动提供的线索。
- **代价**（作者自己写明）："The cost is that machine translation stops inside the market. That is a fair trade against a panel that cannot render at all, and the market ships its own 中文 and English rather than relying on the browser."
- **给新手的教训**：**任何挂在 React 树里的 DSH 插件，根节点都该加 `translate="no"` 与 `notranslate`**。这不是可选优化，是防止整块 UI 崩掉；凡有 portal 的（弹窗、右键菜单、浮层），portal 容器也要加。

#### 坑 X4　dsh.bundle.patch 型插件被当成普通插件写进 insert 行，loader 导入不存在的模块，dsh web 起不来

- **来源**：zhu1090093659_dsh-web d05bf033 fix(web-ui-all): expand external plugin bundles and restore better-session 0.0.11；63a8d3a7 fix(skins): drop dsh.bundle.patch from home-inserted skins (#381)；1e816872 feat(plugin-manager): strip duplicate-mount bundles entries after CLI mutations
- **现象**：`dsh web` 直接 boot 失败（宿主启动即崩，不是界面坏掉）。
- **根因**（提交原文）："@morlay/better-session ships as a profile bundle (dsh.bundle.patch), so writing its package name into an insert row made the loader import a module that does not exist and dsh web failed to boot."
- **修复**：聚合生成器 parsePatchBlocks **展开 bundle 行**——"accepts name-less harness patch rows (preserving extra lines such as disabled flags), insert ids stay namespaced, later bundle patches override earlier same-id rows, and external children are resolved from the aggregate package"；link-profile.mjs 把 bundle 子包也 link 到 profile 根，让 profile-root import 能解析。
- **反向坑**（63a8d3a7）：反过来，"Declaring dsh.bundle.patch lets reconcile put them back on dsh.profile.bundles and recreate duplicate loader entries."——一个已经被宿主层面插入的皮肤（`bundleWired: false`，由 dsh-skin 在 home 层插入），**不该**再声明 `dsh.bundle.patch`，否则 reconcile 会把它放回 `dsh.profile.bundles`、重建重复的 loader entries。
- **给新手的教训**：一个包**要么**是 `dsh.bundle.patch` 型（自己带 patch 文件、由 `bundles` 拉起），**要么**是被别人 `insert:` 的普通插件，不要两头都占。动完配置先 `dsh dump-config` 看**真实的 loader entries**，别只看自己的 package.json。

#### 坑 X5　异步 apply 里抛错，unhandled rejection 被宿主 installFailLoud 抓住，整个 dsh web 进程死掉

- **来源**：zhu1090093659_dsh-web ed3be967 fix(dsh-web-all): config-less self row mounts as a no-op; shell never throws；对照 8d4441ca fix(web-all): make degraded route a ref-counted singleton across shell entries (#1363)；4b25dd77 feat(aggregate): isolate per-plugin boot failures behind the dsh-web-all shell
- **现象**：一个配置形状不对的行（SELF 行用**空 config** 挂载本包）让 shell 抛错；抛错发生在 **async apply** 里，rejection 逃出 loader 生命周期变成 unhandled rejection，宿主 installFailLoud 直接把整个 `dsh web` 干掉——"the exact failure the shell exists to prevent"。
- **根因 + 修复要点**（逐条照抄）：
  - "a config-less row (self shape: `undefined` or `{}`) mounts as the original no-op compat behavior"
  - "a row WITH config but no plugin name no longer throws either: it records a degraded entry and returns."
  - "Loudness lives in the log and the degraded ledger, never in process death."
- **背景**（4b25dd77 原文）：宿主 loader 把整组行当成**一个事务组**（EntryGroup.update）——"any entry that fails to import or start rolls the whole group back, and the boot audit (assertEntriesActivated in @deepseek-ai/dsh-app-boot) then aborts the entire dsh web process." 所以家族把每条行包进 fault-isolation shell，一条坏插件只降级它自己，并提供 `GET /api/dsh-web-all/degraded` 路由报告降级台账。
- **给新手的教训**：DSH 宿主有 installFailLoud——**任何未处理的 promise rejection 都会终止整个 host 进程**。插件 apply() 里凡是异步的都要 try/catch；捕获后记日志 + 降级，绝不让 rejection 逃出去。测试要覆盖"启动失败"和"导入失败"两条路径（先例：`packages/dsh-web-all/tests/shell-isolation.spec.ts`）。

---

## 1.2　omdsh-dev_DSH-better-sidebar 分仓坑点汇总（第三方侧栏底座）

**仓库事实**：644 commits / 12 tags；根目录共 383 个文件。**0 个 blob 可用**（只读得到目录树 + 提交信息）。
技术栈：`package.json` / `pnpm-workspace.yaml` / `cordis.patch.yml` / `dsh.plugin.json`（根目录另有一份插件清单）/ `Makefile` / `eslint.config.js` / `playwright.config.ts`。
源码分区与 dsh-web 同一套约定：`src/`（host：agent-pty、bundle-route、browser-probe…）+ `src/client/`（browser：BrowserView.tsx、DiffTab.tsx、EditorHost.tsx…）。
最有价值的可读线索：`docs/plans/*.md`（50+ 篇设计文档，如 `2026-08-19-sidebar-injection-unified-host-design.md`、`2026-08-12-lazy-chunks-design.md`、`2026-08-14-terminal-font-design.md`、`2026-09-08-terminal-shell-config-hardening-design.md`）与 `docs/external-plugin-guide.md`（第三方注册新页面的官方指南）、`AGENTS.md`。
注意：这些 md 的 **blob 同样不可用**，只能从文件名与提交信息推断主题；正文无法逐字引用。

#### 坑 SB1　终端自定义字体栈不以通用族收尾，浏览器落到比例字体，整张网格崩掉

- **来源**：omdsh-dev_DSH-better-sidebar 0504e39 fix(terminal): 自定义字体解析失败时兜底到等宽，避免掉进比例字体毁掉网格
- **现象**（提交原文，含实测表）：macOS + Chrome 填 `Maple Mono NF CN` → DevTools Rendered Fonts 显示 **PingFang SC**，cell 12.09px @ 13px 字号（0.93em，等宽字体应为 0.6em），字符间距被撑开、字形变比例、Nerd Font 图标全消失。改成 `Maple Mono NF CN, monospace` → Rendered Fonts 变成 **Menlo**，恢复正常。
- **根因**：“字体栈若不以通用族收尾，浏览器解析不到任何具名字体时会落到**标准字体**（macOS 中文环境是 PingFang SC）——它是**比例字体**。xterm 用它的推进宽度量 cell，网格随即失真。” 并且“终端里跑的 shell 在 host 上，字体却由**浏览器所在机器**提供，两者不同机时（远程/容器化的 DSH）用户按 host 侧装的字体填名字必然解析失败。”
- **修复**：新增 `withMonospaceFallback()`，在 `resolveTerminalFont` 出口保证字体栈以通用族收尾；主题 token `--ds-font-family-code` 的值同样兜底。**不做字体嗅探**（设计文档把"字体合法性嗅探"列为非目标）；用户已写通用族则原样保留。
- **给新手的教训**：任何自定义字体栈都要以通用族（`monospace` / `sans-serif`）收尾，否则远端机器上一定落到比例字体。终端的字体来自**用户浏览器**，不是 host。

#### 坑 SB2　收起的面板用 transform 滑出屏幕，仍计入祖先滚动溢出区，整页可双向拖拽

- **来源**：omdsh-dev_DSH-better-sidebar ffcd695 fix(layout): 面板宿主裁剪视口边缘，收起的面板不再撑出文档双向滚动 (#277)
- **现象**：面板收起后整个页面可以左右/上下拖动。
- **根因**：“收起的面板以 `transform: translate(102%)` 滑出屏幕，但 transform 后的元素仍计入祖先滚动溢出区。”
- **修复**：面板宿主 `[data-dsh-panel-host]` 是视口尺寸的 `fixed` 容器，补上 `overflow: hidden`，裁剪点恰在视口边缘；开合滑入动画、内部滚动容器与 fixed 弹层均不受影响。e2e 增加回归断言：面板收起时文档 scrollWidth/Height 不得超出视口。
- **给新手的教训**：`transform` 移出可视区**不等于**移出溢出区。侧栏/抽屉类插件要在宿主容器上 `overflow: hidden`，并写一条"文档不产生滚动条"的 e2e 断言。

#### 坑 SB3　宿主 markdown 原语泄漏进文件预览：sticky 代码块 banner 钉在视口顶，TOC 浮层被压在它下面

- **来源**：omdsh-dev_DSH-better-sidebar a2a2690 fix(markdown): preview TOC dismiss-on-outside-click, popover z-index, code-block banner stickiness
- **现象**：预览里每个代码块的头像"浮动标题"一样钉在视口顶部，直到整块滚过去；TOC 目录面板被代码块 header 盖住；TOC 只能再点一次开关才关。
- **根因**：“DSH 的 `bannerWrap` 是 `position:sticky`（`top:0`，`z-index:6`）以便每条消息的代码块保留复制按钮。预览里每个 fence 共用同一个 `.editorMd` 滚动容器，banner 因此钉到视口顶。” 而 “`.tocBar` 是 `z-index:3`，低于代码 banner 的 6，所以目录面板画在 sticky fence header 下面。”
- **修复**：对预览里非 mermaid 的 fence 中和 stickiness（mermaid chrome 会替换 banner，用 `data-mermaid-processed` 排除）；TOC bar 抬到 `z-index:7`；给 TOC 加 `document` 级 `pointerdown` 监听做 outside-click 关闭（豁免按钮与面板本身）。
- **给新手的教训**：**宿主的组件按上下文做了 `position: sticky` / z-index，搬到别的滚动容器里语义就变了**。复用官方 markdown 原语时，要么中和它的定位，要么显式重排层级。

#### 坑 SB4　portal 出去的 fixed 弹窗，在它依附的编辑面离开视口后仍然存在

- **来源**：omdsh-dev_DSH-better-sidebar d258f3f fix(editor): dismiss the selection popup when its surface leaves the viewport (#425)
- **现象**：触发选区弹出层的编辑面已经不可见了，弹层还钉在屏幕上。
- **根因**：“侧栏让每个 tab 常驻挂载（切 tab 只设 `display:none`；收起面板是把整体 translate 出屏），所以 portal 的 `position:fixed` 按钮会活得比它的编辑面更久。”
- **修复**：抽出 `useSelectionPopup`，在按钮外任何 `mousedown`、Escape、`document` hidden、`window` blur，以及——关键——**用 `IntersectionObserver` 报告编辑面离开视口**时关闭。
- **给新手的教训**：portal 的浮层脱离了父级的显示状态。父面用 `display:none` / `transform` 隐藏时，浮层不会自动消失，必须显式监听（IntersectionObserver / visibilitychange / blur）。
- **来源**：omdsh-dev_DSH-better-sidebar c7d58c9 把 19 个非中英词典移进懒加载 chunk
- **现象**：核心 client bundle 体积过大（1.46MB）。
- **根因**（中文转述）：核心 client bundle 静态 import 了每一个第三语言词典（约 640KB 源码，差不多是 bundle 的一半），而大多数会话根本不会走这条路径：侧栏自己的翻译函数只查中英文加 better-locale override store，词典的唯一消费者是那个 store 的注册调用。
- **修复**：把词典挪进既有的 lazy-chunk 机制（单独打成一个懒加载 js，只在真的装了 better-locale 时按需取；用一个 generation counter 让异步注册在 effect 重跑或中途 dispose 时变得无关紧要）。chunk 落地前翻译函数继续走中英文链；store 在注册时 bump 自身 revision，词典到达后重渲染 chrome。**core client.js：1.46MB 降到 822KB，减少 44%**。词典 chunk 边界的 key-set 检查移到既有运行时测试（每个已发布词典必须与中文 key-set 相等）。
- **给新手的教训**：客户端 bundle 会被整包推给浏览器，**静态 import 就是全量下载**。翻译词典、图标集、大 JSON 一律走 lazy chunk；异步注册要配一个 generation counter 处理"还没到就卸载"。

#### 坑 SB6　桌面壳兼容硬编码在核心里会互相打架；正确做法是把壳适配下沉到用户空间

- **来源**：omdsh-dev_DSH-better-sidebar 50a8888 侧边栏桌面兼容三方案：自动检测（WCO 标准几何）、壳预设、自定义 CSS
- **现象**：为某个桌面壳（Electron 套壳）加的标题栏 offset，在另一个壳上就坏。
- **根因 + 决策**（提交原文，中文部分逐字）：提交原文写的是「核心只保留 Web 标准机制，壳专属适配全部下沉到用户空间（KISS）」，以及「核心 grep 无壳专属类名；为某壳做的兼容在另一壳会再坏——预设与自定义 CSS 是唯一出路（AGENTS.md §8 契约已更新）」。
- **修复**：`prefs` 新增 `titleBarScheme`（auto、preset、custom 三态，旧布尔 `titleBarCompat` 自动迁移）；`wco.ts` 用 `navigator.windowControlsOverlay` 做反应式几何（`geometrychange` 实时更新；`visible=false` 的幽灵 API 视为缺失）；`titlebar-strip.ts` 收敛出唯一 strip 取值链：WCO → `dsh-desktop-titlebar-inset` 契约参数 → 预设 → 手动 px → 0；移除 `desktop-env.ts` 里 win32 32px 硬编码；预设与自定义 CSS 通过 `data-dsh-preset-css`、`data-dsh-custom-css` 标签注入，并补稳定寻址面 `data-dsh-toggle-cluster`、`data-dsh-panel`；交互 chrome 统一 `-webkit-app-region: no-drag`。
- **给新手的教训**：**不要往核心里写"某壳"的类名或像素**。优先用 Web 标准 API（`navigator.windowControlsOverlay`）自动检测；检测不到就做成数据驱动的预设加用户可写 CSS，不要硬编码。

#### 坑 SB7　安装脚本的跨平台与内嵌 Node 版本细节

- **来源**：omdsh-dev_DSH-better-sidebar 9642e95 修 install.ps1 兼容 PowerShell 5.1（node -e 改临时文件，补 UTF-8 BOM）；d94465c 修 install.sh 变量加花括号，修复 macOS bash 3.2 下 unbound variable（#23）；ddd3bed 合并 #47 修 PowerShell 安装器 BOM 解析与 pnpm 版本检查
- **现象**：Windows 上安装脚本解析失败 / macOS 上安装脚本报 "unbound variable" / 中文输出乱码。
- **根因**：Windows PowerShell 5.1（`powershell.exe`，不是 `pwsh`）默认用非 UTF-8 读脚本；bash 3.2（macOS 自带）在 `set -u` 下对 `$VAR` 紧邻中文/标点时会做变量名扩展。
- **修复**：`.ps1` 补 UTF-8 BOM；避免 `node -e` 内联长脚本、改写成临时文件；`.sh` 里所有变量引用统一加花括号 `${VAR}`。
- **给新手的教训**：Windows 侧脚本要当 PowerShell 5.1（不是 7）来写，并保存成 **UTF-8 with BOM**；shell 脚本里变量一律写 `${VAR}`，别写 `$VAR` 后面紧跟其他字符。

#### 坑 SB8　"隐形齿轮"式的二级设置入口：可发现性不足，且容易踩到无边框按钮的可见性契约

- **来源**：omdsh-dev_DSH-better-sidebar 0fdf63b 侧边卡片设置页 UI/UX 现代化——卡片底部设置条替代隐形齿轮，协调双色启用态（#300）
- **现象**：插件设置卡片右下角 16px 的幽灵齿轮，用户找不到入口，以为这个插件没有设置页。
- **根因**：入口只有图标、没有文字标签、位置在角落，常态下几乎不可见。
- **修复**：把齿轮改成**卡片底缘全宽设置条**（hairline 分隔 + 齿轮图标 + 「功能设置」文字标签），常态可发现，hover 用品牌淡底加 brand 字色引导；**可见性条件与 `aria-label` 契约保持不变**（仅父级启用且声明 settings 时才出现）；动效纪律：全部过渡 ≤160ms 且只动颜色属性、`prefers-reduced-motion` 全覆盖。
- **给新手的教训**：给插件做设置页，**入口要有文字标签、要能被一眼看到**。改视觉时不要动 `aria-label` 和可见性条件——那是无障碍与逻辑契约。

---

## 1.3　dsh-market_dsh-market 分仓坑点汇总（设置页内的可视化插件市场）

**仓库事实**：491 commits / 12 tags；HEAD 树 213 个文件；**0 个 blob 可用**。
分层：`src/`（host：install.ts、patch.ts、hot.ts、profile.ts、restart.ts、routes.ts、settings.ts、pnpm-compat.ts、update-api-v1.ts…）+ `src/client/`（browser：MarketSection.tsx、SettingsCard.tsx、OperationsPanel.tsx、ErrorBoundary.tsx、Diagnostics.tsx、comments.ts、market-data.ts…）+ 预构建的 `client/client.js`（提交进仓库的 browser bundle）+ `cordis.patch.yml`。
测试结构值得新手照抄：`tests/` 平铺宿主单测 + `tests/client/*.client.spec.tsx`（浏览器半测）+ `tests/web/*.e2e.ts`（Playwright）+ **`tests/web/fixtures/fixture-a|b|carrier|clash|cross/`（每个都是含 `package.json` + `cordis.patch.yml` + `index.js` 的最小插件样例）** + `vitest.compat.config.ts`（真 pnpm 兼容车道）。
另注：根目录是 `package-lock.json`（npm），不是 pnpm lock —— 第三方独立插件不必强求 pnpm。

#### 坑 MK1　一个已删除的本地 .tgz 依赖会阻塞该 profile 的所有安装与卸载，而报错只给路径不给包名

- **来源**：dsh-market_dsh-market 7133ed3 release 1.43.0（#436，by @screamff）
- **现象**：一份"插件页面全坏"的报告；但实际是**安装/卸载全部失败**。
- **根因**（提交原文）："A plugin installed from a .tgz that has since been deleted blocks EVERY install and uninstall in the profile, because pnpm re-resolves all direct dependencies before any change." 用户看到的是 pnpm 原始的 ENOENT，**只给路径、不给包名**，读起来跟用户想做的事毫无关系。
- **修复**：抓出死掉的本地依赖并**点名那个包**；对照真实 pnpm 10 与 11 量化，并在 compat 车道里钉住。
- **给新手的教训**：报错信息要**点名用户能识别的对象**（插件名），不要透传包管理器的原始错误（只说路径）。另外：profile 里的**任何一条**直接依赖坏掉，都会让整条依赖操作失败——排查"我怎么装都装不上"时，先怀疑 profile 里已有的坏依赖。

#### 坑 MK2　原生 .node 插件无法 dlclose，卸载后报 "hot（刷新即可）" 是错的；Windows 上还会报 EPERM

- **来源**：dsh-market_dsh-market 7133ed3 release 1.43.0（#441，by @yandidan1）
- **现象**：卸载一个带 native addon 的插件后提示"刷新一下就够"，但刷新后仍然失败；Windows 上后续安装报 EPERM，且文案是写给**更新**场景的，让用户去禁用一个已经删掉的插件。
- **根因**（提交原文）："Node has no dlclose: once a `.node` is loaded the process holds it until it exits, so unmounting or even uninstalling the plugin does not free the file, and on Windows the next install fails renaming over it."
- **修复**：卸载对这类插件**明确说明**需要重启进程；EPERM 文案按场景区分安装/更新/卸载。
- **给新手的教训**：装了原生模块（`.node`）的插件，**热卸载是不成立的**，必须整进程重启。别把"刷新页面"当成万能解法。

#### 坑 MK3　pnpm 起不来时，用户看到的是 Node 的原始错误对象和一段 argv dump

- **来源**：dsh-market_dsh-market 7133ed3 release 1.43.0（#509 by @awslmowms；#502 by @Ztyss）
- **现象**：Ubuntu 上 spawn 直接被拒，界面显示 Node 的原始 error 对象 + argv dump；更新路径还谎称"回滚无法验证"——而 pnpm 根本没跑、什么都没写。
- **修复**：每种原因**配一条对应的修复指引**——EACCES、ENOENT，以及 Windows 的 exit 9009。
- **给新手的教训**：调用外部进程时，对**每个已知退出码/errno 写人话**，并且**没执行就别说"回滚失败"**。把 `err.code` 映射成用户能做的下一步动作。

#### 坑 MK4　「立即更新」看起来不像按钮——它用了宿主默认 variant，被塞在红色 12px 错误 banner 里

- **来源**：dsh-market_dsh-market 7133ed3 release 1.43.0（#410，由用户 @Dave-12138 在自己的截图里发现）
- **现象**：按钮一直都在，但用户找不到。
- **根因**："It was there the whole time, taking the host default variant inside a red 12px error banner."
- **修复**：给主操作显式使用主按钮三件套 token，让它在错误语境里仍是明确的按钮。
- **给新手的教训**：**不要把关键操作按钮放在错误 banner 里还依赖默认样式**。主按钮必须显式用 `--dsw-alias-button-primary-fill` 三件套（详见 §三）。

#### 坑 MK5　代理到不了 pnpm：catalog 能加载，安装却全部卡死

- **来源**：dsh-market_dsh-market 2c5a32b fix: a proxy reaches pnpm, a CRLF workspace file stays valid, and a long tag stops wrapping the row（#148 #161 #188 #232）
- **现象**：在有代理的网络里，市场自己的 catalog 拉得好好的，但每一次安装都卡住。
- **根因**（提交原文）："The market's own catalog fetches have gone through undici's EnvHttpProxyAgent since 1.14.0 … pnpm reads none of HTTPS_PROXY/http_proxy; it reads npm config, so a proxy reaches it only as npm_config_https_proxy / npm_config_proxy."
- **修复**：`spawnEnv()` 做翻译，**镜像 undici 自己的优先级**（小写覆盖大写，https 回退到 http）；`NO_PROXY` 也要转发；调用方已设置的 `npm_config_*` 永远优先，且**大小写不敏感**（因为 Windows 环境变量键就是大小写不敏感的）。
- **给新手的教训**：插件自己做 HTTP 和插件调用 pnpm，走的是**两套不同的代理配置**。给子进程传代理时，要同时写 `npm_config_https_proxy` / `npm_config_proxy`，并保留大小写两种拼写。

#### 坑 MK6　CRLF 的 pnpm-workspace.yaml 让 allowBuilds 块匹配失败、追加出第二个块 → 非法 YAML → 该 profile 所有安装失败

- **来源**：dsh-market_dsh-market 2c5a32b（#231 by @MichengAI）
- **现象**：Windows 上（或任何 `core.autocrlf=true` 的检出）该 profile 里**每一次**安装都失败。
- **根因**（提交原文）："The allowBuilds block pattern required a `\n` immediately after the key. A CRLF file … has `\r` there, so an EXISTING block was never found and a second one got appended. Two top-level allowBuilds keys is invalid YAML."
- **修复**：正则容忍 `\r`；**合并所有块**（而不是只处理第一个，这样可以修好已坏掉的文件，而不是静默撤销第二个块里的审批）；重写时保持文件自己的换行符，不留下混合换行。
- **给新手的教训**：**插件写用户的 YAML/JSON 配置时，正则必须容忍 `\r`**。改完要保持原文件换行风格；块匹配要用"合并"语义，不要用"找不到就再追加一个"。

#### 坑 MK7　行内唯一的可变长文案用了 nowrap + flex-shrink:0，把整个操作行挤下去

- **来源**：dsh-market_dsh-market 2c5a32b（#234 by @Ztyss）
- **现象**：`.metaTag`（本地开发 link）把 Uninstall 按钮挤到了单独一行。
- **根因**："`.metaTag` holds the row's only variable-length copy and was nowrap with flex-shrink:0, so the longest of them wrapped the whole action row."
- **修复**：文案这半边允许收缩/换行，按钮那半边保持可操作。
- **给新手的教训**：flex 行里**唯一可变长的那一段**不要用 `flex-shrink: 0` + `nowrap`，否则最长的数据会把按钮挤出去。可变长的给 `flex: 1; min-width: 0`，按钮给 `flex: none`。

#### 坑 MK8　插件自己的自动折叠，与 Chrome 的 scroll anchoring 互搏成无限抖动

- **来源**：dsh-market_dsh-market a56c5e9 fix: the category row stops fighting the scroll it triggered（#395 #403）；d590242 release 1.36.0
- **现象**：分类列表展开时滚动插件列表，画面**持续闪烁**。
- **根因**（提交原文）："Scroll anchoring picks a node below the viewport and rewrites scrollTop whenever content ABOVE it changes height, which is exactly what collapsing ~120px of category row does. So the browser undid the scroll that had caused the collapse, that put the viewport back above the sentinel, the row re-expanded, and the next scroll event started it again." 实测：*"one synthetic 8px/frame scroll drove scrollTop 8 → 134 → 24 inside 30ms while the row flipped 146px ↔ 26px; parking at scrollTop 20 with no further input was yanked straight back to 0."*
- **修复**：滚动容器上 `overflow-anchor: none`（*"With overflow-anchor:none … the same gesture collapses once and scrollTop stays where it was put."*）。放弃锚定在本列表没有代价——*"Every image it renders is sized in CSS (`.shot`, `.cardShot`, `.av`), so nothing above the viewport resizes on load."*
- **给新手的教训**：**当滚动本身会改变视口上方内容高度时，一定要关掉 `overflow-anchor`**，否则浏览器会"帮你"把滚动位置改回去，和你自己的逻辑打架成死循环。关闭的前提是：列表里没有"先占位后撑高"的图片。

#### 坑 MK9　每张卡片每次渲染都全量重扫 catalog：`O(cards × installed × catalog)`，占掉整个录制 28.4% 的 CPU

- **来源**：dsh-market_dsh-market 6ddc691 perf: stop rescanning the whole catalog once per card, per render（#262 #264）；b9323cc release 1.18.0
- **现象**："插件页面非常卡"，附了 Chrome trace。
- **根因**（提交原文）："`looseMatchCount` answers 'how many catalog entries could this installed dependency be?', which depends only on the catalog and the dependency name. It has nothing to do with the card being drawn. But it sat inside `matchInstalledName`, which runs once per installed dependency, which runs once per rendered card — so every render cost `cards × installed × catalog` with a full scan of ~1800 entries each time, allocating a fresh identity Set per entry along the way." CPU profile：*"looseMatches, 2918ms self time, 28.4% of the entire recording — the largest non-idle entry by a wide margin."*
- **修复**：按 **catalog 数组的 identity** 做 memo（重新拉取 catalog 自然拿到新 map，旧的变成可回收）；`entryIdentities` 按 entry 对象 memo（catalog entry 解析一次、之后不再 mutate）；`depIdentities` 移出扫描循环（原本每次调用重建约 1800 次）。实测：*"24 cards: 48.1ms → 1.8ms; 96 cards: 223.6ms → 0.8ms per render."*（线上 catalog 1800+，大约是实测的两倍。）
- **给新手的教训**：**渲染函数里任何"只跟数据有关、跟这一行无关"的计算，都要 memo**。看到三层嵌套循环 `cards × installed × catalog` 就是它在报警。用数组 identity 当 memo key。

#### 坑 MK10　把 `settingsScope` 写进模块级 `inject` 会让整个插件在旧宿主上不挂载

- **来源**：dsh-market_dsh-market 53ea53d feat: allowRestart is a switch on the settings page, not a YAML edit
- **背景**：市场要在 dsh 0.1.0-rc.7 开放的"插件配置页"上放一张设置卡（host 半在 `src/settings.ts` 注册命名空间，browser 半在 `src/client/SettingsCard.tsx` 出卡片）。
- **坑**（提交原文）："The browser side does need care, and takes it through a NESTED inject: naming `settingsScope` in the module-level `inject` would leave the whole plugin unmounted on rc.6 — trading the market's own page for a card that host cannot render. Nested, the card is simply absent there."
- **兼容性设计**（照抄）："Compatibility needs no version check on the Host side: `installSettingsSection` rides its own scoped fiber, so a dsh without a settings service never runs any of it and the composed entry stands."
- **另两条决策**：只暴露 `allowRestart`（`profile` 在挂载时决定、运行中换不了，提供了也是空承诺）；Desktop 分支根本不注册（那里由壳掌管进程生命周期，值被强制 false）。
- **给新手的教训**：**新 API 的依赖要放在"嵌套 inject"里，不要写进模块级 `inject`**。写进模块级意味着旧宿主上整个插件都不加载；嵌套注入则只是那张卡片不存在，插件本体照常工作。

#### 坑 MK11　插件不能通过通用卸载路径卸载自己：要独立路由、显式 confirm，且"热禁用"写下的行会活得更久

- **来源**：dsh-market_dsh-market b36f2ee feat: manage the market itself from its plugin-configuration card（#173）
- **要点**（提交原文逐条）：
  - 通用卸载路由**拒绝**卸载市场自己：*"a destructive action on the plugin serving the request should not be reachable as a stray `{ name: "dshmarket" }` on the ordinary path."* 需要单独的 `self-uninstall` 路由 + 显式 `confirm`，并走与重启相同的 loopback 门。
  - 已被 import 的模块**不会随文件消失**：*"an already-imported module does not vanish with its files, so the process keeps serving and the response completes; the profile boots clean afterwards. What DOES break is a refresh — the host 404s on the removed client bundle while the loader entry is still live … so the market disables its own entry after responding."*
  - "热禁用"写下的 `disabled: true` 行会**活过**这次操作：*"the market's hot-disable writes `disabled: true` rows into the profile's user patch layer, and those OUTLIVE …"* —— 所以设置页提供一个**默认关闭**的 cleanup 复选框来收拾它们。
- **给新手的教训**：插件**不要**给自己提供一条"普通路径就能触发"的自毁接口；要单独路由 + 显式确认。卸载/禁用后"刷新页面"必然 404（bundle 没了、loader entry 还在），要**在响应完成后先把自己的 entry 禁掉**。热禁用会在用户的 patch 层留下 `disabled: true` 行，考虑提供清理入口。

#### 坑 MK12　Windows 三连：CRLF 让热挂载失效、锁定文件改名被拒、重启给 PowerShell 一个 `.ps1` 被策略拒绝

- **来源**：dsh-market_dsh-market 01b3c28 fix: a Windows-authored bundle patch can be hot-mounted；33a5153 fix: explain a Windows locked-file rename instead of showing pnpm's stack（#394 #389）；d590242 release 1.36.0（#397 #398）
- **坑 12-a（CRLF + JS 的 `\r` 是行终止符）**（提交原文）：*"Comments are stripped with `raw.replace(/#.*$/, '')`, and `\r` is a LINE TERMINATOR in JavaScript: `.` will not cross it, and `$` without `/m` anchors only at the very end of the string. So on `# comment\r` the pattern never matches, the comment survives, matches none of the row shapes, and hits the parser's `return null` — which the caller reports as 'the bundle patch contains config/expression rows'."* 用户可见后果：*"any plugin whose `cordis.patch.yml` was authored on Windows could never hot-mount, on ANY platform, and always demanded a restart."* 修复：两个解析器都改成按 `/\r?\n/` 切分。**注意**：作者还写明 profile.ts 里"等价的那处改动是故意不覆盖的"，并**删掉了自己先写的那条测试**——因为那里的模式都是 `^` 锚定、注释行必以 `#` 开头，不剥离注释的结果完全相同；*"The test passed with and without the fix — it tested nothing."*
- **坑 12-b（Windows 锁定文件改名）**：pnpm 把新版本 stage 在同级 `<name>_tmp_<pid>_<n>` 目录再 rename 覆盖旧的，Windows 在目标下任何文件被打开时拒绝 rename。*"For an UPDATE the target is a plugin the running dsh has loaded — its own files are the ones held open. On POSIX this never comes up, because replacing an open file leaves the old inode alive for whoever still holds it."* 修复：报错点名插件、说明旧版本完好、给出两条出路（退出 harness 从命令行更新；或禁用插件→重启→更新），并点名杀毒软件/文件索引器。**故意不做自动重试**：*"the process that would retry is the one holding the handles, so a retry cannot win."*
- **坑 12-c（重启用 `dsh.ps1` 被 Restricted 执行策略拒）**：#397 报告 Windows 上点"立即重启"，宿主关掉后再也没回来。根因：*"The relaunch handed a bare `dsh` to a hidden PowerShell, PowerShell prefers `dsh.ps1`, and the default Restricted execution policy refuses it — after the old host has already exited. So the button did the destructive half of its job and not the other half, with no way back from inside the UI."* 修复：显式用 `dsh.cmd`（npm 同时安装、不受脚本策略管）。
- **给新手的教训**：Windows 上（1）一切按行切分都用 `/\r?\n/`，别用 `$`（JS 里 `\r` 是行终止符）；（2）文件被占用时的 rename 会失败，报错要说清"这个版本还在跑，先退出再更新"；（3）**重启/拉起子进程显式用 `.cmd`**，不要只给一个裸命令名让 PowerShell 去猜 `.ps1`。这些坑在 Linux/macOS 上 100% 不复现——*"the whole suite was green on Linux and macOS throughout, and it would have kept hiding there."*

---

# A · 二、插件骨架与可复用代码（含"能不能照抄"的诚实结论）

## 二.0　前置声明：源码 blob 不可用，因此**无法逐字照抄源码**

必须先把边界说清楚，否则这本手册会教错人。

三个仓库都是**部分克隆**（`--filter=blob:none --no-checkout`），本地只落了 commit/tree 对象，**blob（文件内容）在需要时才会 lazy fetch**。而当前环境没有网络，所以：

```text
$ git -C zhu1090093659_dsh-web show HEAD:packages/dsh-session-id/package.json
fatal: bad object HEAD:packages/dsh-session-id/package.json

$ GIT_NO_LAZY_FETCH=1 git -C zhu1090093659_dsh-web show HEAD:packages/dsh-session-id/src/index.ts
fatal: bad object HEAD:packages/dsh-session-id/src/index.ts
```

**实际 blob 计数**（`git cat-file --batch-check --batch-all-objects`）：

| 仓库 | commit | tag | tree | **可用 blob** | 说明 |
| --- | --- | --- | --- | --- | --- |
| zhu1090093659_dsh-web | 2444 | 15 | 19098 | **365** | 只有 `.agents/notes/**` 的笔记正文 + `packages/AGENTS.md` |
| omdsh-dev_DSH-better-sidebar | 644 | 12 | 2044 | **0** | 一个文件内容都读不到 |
| dsh-market_dsh-market | 491 | 12 | 1685 | **0** | 一个文件内容都读不到 |

**结论**：用户点名要"逐字照抄"的 `package.json` 全文、`src/index.ts`、客户端入口文件、`cordis.patch.yml`、调用 slots API 的代码、设置卡片代码、CSS——**在物理上拿不到**。本节不会伪造任何一行源码。

下面给出的是**确实读得到**的三类事实：

1. **权威契约文本**：`zhu1090093659_dsh-web` 的 `packages/AGENTS.md`（**逐字可读**，365 个可用 blob 之一）——它规定了包形态、分层、exports、样式、测试纪律。这是本节最有价值的部分。
2. **完整目录树**：`git ls-tree -r --name-only HEAD <路径>`（真实、完整），用来照抄"文件该放哪、叫什么名字"。
3. **确切的 API 名 / 字段名 / 报错字符串**：来自维护者笔记（`.agents/notes/**`，逐字可读）与提交信息。

凡用户要求"逐字照抄"而我拿不到的，一律写 **「未找到（blob 不可用）」**。

## 二.1　最小 UI 插件范本

### 二.1.1 判定方法（为什么不用 `wc -l`）

用户建议用 `find` + `wc -l` 找代码量最小的插件——但 blob 不可用，`wc -l` 无从下手。改用**文件数**做近似（`git ls-tree -r --name-only HEAD <包目录> | wc -l`），并在同等文件数下优先选"纯客户端 UI、无 host 逻辑"的包。

### 二.1.2 家族内文件数排行（越小越简单）

| 包 | 总文件数 | 其中 src 下 ts/tsx | 备注 |
| --- | --- | --- | --- |
| `packages/dsh-session-id` | **24** | 14 | **最小、最干净的纯客户端 UI 插件**，含 2 个测试 |
| `packages/dsh-model-capabilities` | 28 | 17 | 次小 |
| `packages/dsh-web-settings` | 34 | 25 | 含设置桥 |
| `packages/dsh-web-all` | 41 | 17 | 聚合载具，非普通插件 |
| `packages/dsh-usage` | 40 | 29 | |
| `packages/dsh-skill-explorer` | 48 | 36 | |
| `packages/dsh-session-archive` | 51 | 39 | 唯一把 "settings token 契约" 做进 UI 的包 |

### 二.1.3 范本 A（推荐）：`packages/dsh-session-id/` —— 家族内最小的纯客户端 UI 插件

**完整目录树（`git ls-tree -r --name-only HEAD packages/dsh-session-id/`，真实完整）**：

```text
packages/dsh-session-id/.gitignore
packages/dsh-session-id/AGENTS.md
packages/dsh-session-id/LICENSE
packages/dsh-session-id/README.i18n.yaml
packages/dsh-session-id/README.md
packages/dsh-session-id/README.zh.md
packages/dsh-session-id/cordis.patch.yml
packages/dsh-session-id/package.json
packages/dsh-session-id/src/client/SessionIdEntry.tsx
packages/dsh-session-id/src/client/SessionIdPanel.tsx
packages/dsh-session-id/src/client/css-modules.d.ts
packages/dsh-session-id/src/client/icons.tsx
packages/dsh-session-id/src/client/index.ts
packages/dsh-session-id/src/client/locales.ts
packages/dsh-session-id/src/client/semantic.ts
packages/dsh-session-id/src/client/session-id.module.css
packages/dsh-session-id/src/client/telemetry.ts
packages/dsh-session-id/src/index.ts
packages/dsh-session-id/src/invariant.ts
packages/dsh-session-id/tests/session-id-entry.spec.tsx
packages/dsh-session-id/tests/session-id-panel.spec.tsx
packages/dsh-session-id/tsconfig.build.json
packages/dsh-session-id/tsconfig.json
packages/dsh-session-id/tsdown.config.ts
packages/dsh-session-id/vitest.config.ts
```

**从这棵树能直接学到的事实（真实、可照抄的结构）**：

- 一个完整插件**必须有**：`package.json`、`cordis.patch.yml`、`src/index.ts`（host 半区，**可以为空函数**）、`tsconfig.json` + `tsconfig.build.json`、`tsdown.config.ts`、`vitest.config.ts`、`README.md` + `README.zh.md` + `README.i18n.yaml`（双语三件套）、`AGENTS.md`（包级规则）、`.gitignore`、`LICENSE`。
- 浏览器半区**全部**放 `src/client/`：入口 `index.ts`、组件 `*.tsx`、i18n `locales.ts`、语义属性 `semantic.ts`、遥测 `telemetry.ts`、CSS Modules `*.module.css`、以及 **`css-modules.d.ts`**（CSS Modules 的类型声明——没有它 TS 会报找不到 `*.module.css` 模块）。
- **`src/invariant.ts`**：本包特有的"不变量"声明（供 `exports["./invariant"]` 用）。⚠️ 这是**仓库内既有包的现状**，不是对新插件的要求 —— `0.2.1-alpha.1` 起 `packages/AGENTS.md` 已**删除**这条约定。
- 测试放 `tests/`，且是 `.spec.tsx`（用 vitest + 组件挂载）。

**`package.json` 全文：未找到（blob 不可用）。** 只能给出**必须包含的字段清单**，以及每个字段的**形状依据**：

| 字段 | 形状 | 依据（可读来源） |
| --- | --- | --- |
| `"type"` | `"module"` | `packages/AGENTS.md` 逐字："独立 cordis bundle 包：`"type": "module"`" |
| `"dsh"."bundle"."patch"` | `"./cordis.patch.yml"` | `packages/AGENTS.md` 逐字 |
| `"dsh"."client"."platform"` | `"web"` | `packages/AGENTS.md` 逐字（形态参照 `packages/dsh-task-board/`） |
| `"dsh"."client"."inject"` | 服务名数组 | 见 §二.2.3 与坑 D1 的车祸现场（`remote.agentPresets` 就在这个数组里） |
| `"exports"."."` | host 半区入口 | `packages/AGENTS.md` 逐字 |
| `"exports"["./client"]` | 浏览器半区入口（**条件对象**，含 `types` + 运行时） | dsh-web 笔记 `2026-08-26-dsh-perf-client-export.md` 专讲这个（坑 B1/B2） |
| `"exports"["./invariant"]` | 可选（**`0.2.1-alpha.1` 起 `packages/AGENTS.md` 已删除该约定**，仅仓库内既有包在用；**新插件不必提供**） | ~~`packages/AGENTS.md` 逐字~~ **依据已失效**（见 `02b-official-templates.md` §附） |
| `"exports"["./src/*"]` | 测试引用的源码直出 | `packages/AGENTS.md` 逐字："`./src/*` 用于测试引用" |
| `"engines"."node"` | `"^22.19 \|\| >=24"` | `packages/AGENTS.md` 逐字 |
| `"peerDependencies"` | 运行时注入的服务 | `packages/AGENTS.md` 逐字："peerDependencies 声明运行时注入的服务" |
| `"files"` | **未找到** | 三个仓库都读不到（dsh-web 的 AGENTS.md 未提 `files` 字段） |

**注意**：用户点名要的 `files`、`peerDependencies` 具体内容、`dsh` 字段的完整 JSON，**全部未找到（blob 不可用）**。`peerDependencies` 只能确定"**声明运行时注入的服务**"这一**语义**（AGENTS.md 逐字），具体依赖名无法给出。市场上有一条相关证据：`dsh-market` 的 `ddb66c9 fix(market): 移除公开版 cordis peer 并迁移类型基底到 @deepseek-ai/cordis` —— 说明第三方独立插件把 cordis 从 `peerDependencies` 移到类型基底也是实际情况，**不要照抄 dsh-web 家族的 peer 清单**。

### 二.1.4 范本 B：`scripts/plugin-template/` —— 仓库自带的官方脚手架（最小形态）

**完整目录树（真实完整）**：

```text
scripts/plugin-template/.gitignore
scripts/plugin-template/AGENTS.md
scripts/plugin-template/README.i18n.yaml
scripts/plugin-template/README.md
scripts/plugin-template/README.zh.md
scripts/plugin-template/cordis.patch.yml
scripts/plugin-template/package.json
scripts/plugin-template/src/client/index.ts
scripts/plugin-template/src/index.ts
scripts/plugin-template/tsconfig.build.json
scripts/plugin-template/tsconfig.json
scripts/plugin-template/tsdown.config.ts
```

**这是三个仓库里能找到的、文件数最少的 UI 插件骨架（12 个文件）**。它比 `dsh-session-id` 更小，因为它是模板：没有测试、没有 LICENSE、没有 locales/telemetry/invariant。

**新手应当照抄这个结构**：`src/index.ts`（host，可为空）+ `src/client/index.ts`（browser，写 UI）+ `package.json` + `cordis.patch.yml` + 两个 tsconfig + 一个 tsdown 配置 + 双语 README 三件套。

**同样：所有文件内容「未找到（blob 不可用）」。** 无法给出 `src/client/index.ts` 的实际写法。

### 二.1.5 第三方仓库里的最小插件样例（dsh-market 的测试 fixture）

如果想知道"一个能装进 profile 的插件包长什么样"，`dsh-market_dsh-market` 的测试目录里有**五个最小样例**，每个都只有三个文件：

```text
dsh-market_dsh-market/tests/web/fixtures/fixture-a/cordis.patch.yml
dsh-market_dsh-market/tests/web/fixtures/fixture-a/index.js
dsh-market_dsh-market/tests/web/fixtures/fixture-a/package.json
dsh-market_dsh-market/tests/web/fixtures/fixture-b/{cordis.patch.yml, index.js, package.json}
dsh-market_dsh-market/tests/web/fixtures/fixture-carrier/{cordis.patch.yml, package.json}       # 注意：没有 index.js
dsh-market_dsh-market/tests/web/fixtures/fixture-clash/{cordis.patch.yml, index.js, package.json}
dsh-market_dsh-market/tests/web/fixtures/fixture-cross/{cordis.patch.yml, index.js, package.json}
```

**能直接确认的事实**：一个最小的可安装插件 = `package.json` + `cordis.patch.yml` + 一个 JS 入口（`index.js`，说明**不必是 TypeScript**）；`fixture-carrier` 只有 `package.json` + `cordis.patch.yml` 没有 `index.js`，对应坑 X4 里"bundle 载体"的形态。**文件内容未找到（blob 不可用）。**

## 二.2　如何往 slots 塞 UI

**没有一行可照抄的 slots 调用代码（blob 不可用）。** 但笔记与提交里给了**确切的 API 名、参数形状和踩坑报错**，这些是真实读到的：

### 二.2.1 已知的 slots API 表面

- `ctx.slots` —— `packages/AGENTS.md` 逐字点名它是"跨插件协作的 cordis 服务"之一（原文："跨插件协作走 cordis 服务（`ctx.slots` / `ctx.sessions` / `ctx.workspaces`）或 slot，不走 value import"）。
- `ctx.slots.register(...)` / `ctx.slots.inject(...)` —— 见坑 C1/C2 的车祸现场笔记。
- **插槽名（slot name）是字符串**，宿主在 DOM 上以 `[data-slot="<插槽全名>"]` 暴露锚点 —— 见坑 C4。
- **keyed slot** 的优先级是二元组 `(key, priority)`，且有一个保留常量 `SHADOW_PRIORITY_HEADROOM = 8` —— 见坑 C3（笔记 `2026-08-27-perf-shadow-priority-headroom.md`，逐字可读）。

### 二.2.2 三条硬约束（都是真实报错换来的）

1. **`register` 必须保留 `this`**：解构 `const { register } = ctx.slots` 会丢 `this`，报 `TypeError: Cannot read properties of undefined (reading 'effect')`（坑 C1）。→ 写 `ctx.slots.register(...)`，不要解构。
2. **注册时机**：`ctx.slots.inject` 是延迟注册（坑 C2）——在依赖服务就绪后再挂 UI，不要假设 `apply()` 一开始就能注册。
3. **keyed slot 的 `(key, priority)` 必须唯一**，撞车会互相覆盖；官方组件用 `priority` 的保留区间，插件要留 headroom（坑 C3）。

### 二.2.3 客户端 inject 是硬约束，不是提示

`package.json` 的 `dsh.client.inject`（或客户端 entry 的 `inject` 数组）里写了某个服务名，宿主上**没有**这个服务，entry 会**永远 pending**，boot 报"一个 entry 未激活"。原文（笔记 `2026-08-28-client-store-dual-cohort-engine-shim.md`，逐字）：

```text
pending (waiting for service: remote.agentPresets)
```

**修复模式**（照抄思路）：把版本相关的服务**从硬 inject 里拿掉**，改成"使用时探测"：

- *"The preset roster is read at use time through whichever face the running host serves — `remote.agentPresets` when registered, else `connection.api.agentPresets` (the pre-migration rc.2 face)"*
- *"probing at use time is the same mechanism the bridge-fallback compat binder already uses"*
- 理由（原文）：*"an inject wait either blocks activation (hard) or cannot express 'continue without it' (cordis inject has no optional flag here)"* —— **cordis 没有"可选 inject"**，所以兼容写法只能在**使用时探测**。

## 二.3　如何在设置页加一张卡片

**调用代码：未找到（blob 不可用）。** 以下是确切读到的 API 名与两个真实车祸现场。

### 二.3.1 两端分工（dsh-market 的做法，提交 53ea53d 原文）

> "dsh 0.1.0-rc.7 opened the plugin configuration page to plugins outside its own repository: the Host serves every registered settings namespace, and the tab pairs a namespace with the card keyed to it. **Both halves ship here** — the namespace in `src/settings.ts`, the card in `src/client/SettingsCard.tsx`."

→ **host 半区**：`src/settings.ts` 注册一个 settings **namespace**。
→ **browser 半区**：`src/client/SettingsCard.tsx` 渲染 keyed 到该 namespace 的**卡片**。
→ **host 侧注册 API 确认为 `installSettingsSection`**（`packages/AGENTS.md` 逐字与提交 53ea53d 都点名）。

### 二.3.2 插槽名确认为 `settings.section`

笔记 `2026-09-01-settings-scope-useSyncExternalStore-binding.md` 里有一条真实的 slot 崩溃栈（逐字）：

```text
TypeError: Cannot read properties of undefined (reading 'store')
    at getSnapshot (client.js:998)        <- official dsh-client-ui-settings bundle
    at useSyncExternalStore (frontend bundle)
    at AutoSettingsPanel (AutoSettings.tsx:76)
slot entry crashed in 'settings.section'
```

→ **崩溃日志会带插槽名 `settings.section`**，这是排查"卡片没显示/卡片崩了"的第一手线索。

### 二.3.3 必须照抄的一条：拿到官方 `SettingsScope` 后要 **bind**

> ⚠️ **时效（2026-09-23）**：`SettingsScope` 本体与手写设置卡片族已在 `dsh-v0.1.7-rc.1` **整体移除**。本节的**具体 API** 已不适用，**通用教训**（类实例方法交给 React 前先 `bind`）仍然成立。

- 卡片组件收到的 `props.settings` 是官方的 `SettingsScope` **实例**，它的 `subscribe` / `getSnapshot` 是**读 `this.store` 的原型方法**。
- React 的 `useSyncExternalStore` 会把回调**当裸函数调用**，`this` 变成 `undefined`，第一次 `getSnapshot()` 就抛。
- **正确写法**（提交原文）：*"`AutoSettingsPanel` now binds both methods to the scope with `useMemo` (`settings.subscribe.bind(settings)`), keeping stable hook identities across renders (the scope object itself is identity-stable per entry, so no resubscribe churn)."*
- 维护者还做了全仓审计（doctor、market、pet、session-id、session-archive、ssh、usage）：*"all other stores are closure-based (`createSnapshotStore` instances or object literals with arrow methods) and are safe unbound; the settings scope was the only prototype-method surface passed as a callback."*
- **给新手的教训**：凡是把**类实例的方法**交给 React 当回调，一律 `.bind(instance)`。`createSnapshotStore` 之类闭包 store 不用 bind。

### 二.3.4 先例与契约

- 唯一把"settings token 契约"做进 UI 的家族包是 `packages/dsh-session-archive`（笔记 `2026-09-01-session-archive-token-contract-ui.md`）。
- 卡片上要放"主操作"时，**必须用主按钮三件套 token**（见 §二.5 与坑 MK4）。
- 设置卡片"长列表"要用内部滚动（提交 0fdf63b 原文：*"popupRows 内部滚动 max-height min(52vh,440px) + 细滚动条（`--dsw-alias-scrollbar-*` 令牌）"*），并且要处理 `prefers-reduced-motion`。

## 二.4　客户端插件如何拿宿主侧数据

**调用代码：未找到（blob 不可用）。** 但这一节的**接口表是逐字读到的**，可以直接当契约用。

### 二.4.1 `invokeWireArgs()` 参数形状表（逐字，来自笔记 `2026-08-28-descriptor-faithful-wire-contracts.md`）

网关方法的参数**不能随便包 `{ request }`**，每个方法的线上形状由 SDK 生成的 descriptor 表决定：

| 调用 | 线上参数形状 |
| --- | --- |
| `session/list` | `{ _request }`（**注意下划线**） |
| `directoryPicker/list` | 扁平的、可选的 path（**不是** `{ request: body }`） |
| `agentPresets/list` | `{}` |
| `session/modelCatalog` | `{}` |
| 其余一切 | `{ request }` |

实测翻车记录（逐字）：*"session/list was invoked with args `{request}` although its single parameter wires as `_request` (task-board settlement loop dead, phone session list dead); directoryPicker/list was sent `{request: body}` although it declares one flat optional path (phone browsing dead)"*。

网关侧有 `assertExactArguments` —— 多传/少传 key 会**直接报错**（原文：*"the fakes … reject extra/missing keys exactly like the gateway's `assertExactArguments`"*）。

**给新手的教训**：**不要凭直觉包 `{ request }`**。要么查 descriptor 表，要么照抄 `invokeWireArgs()` 这个 helper 的做法（按方法名分派），并且**让测试 fake 也用同一张表**——否则真机上一条路径静默死掉、测试全绿。

### 二.4.2 业务错误码在 `error.failure`，不在 `error.code`

- `TypertRemoteFailure` **把业务错误码挂在 `error.failure` 上**；`error.code` 不是它。
- 实测翻车：*"business error codes were read from `error.code` although `TypertRemoteFailure` carries them on `error.failure` (paired-model-catalog answered 502 instead of 409/422)"*。
- 正确映射（逐字）：*"`settings-conflict` -> 409, `settings-rejected` -> 422"*，**不要用 message 正则去猜**。
- 兼容写法：*"extracts business failures from `error.failure` before falling back to `error.code`"*。

### 二.4.3 `ctx.get()` 与 `ctx.<service>` 的区别（坑 D4）

- 在 host 半区，`ctx.get('service.name')` 与 `ctx.serviceName` 的语义差别是真实踩过的坑（见坑 D4）。
- **给新手的教训**：取服务用 `ctx.get(...)`（可判空、不触发注入约束），直接用 `ctx.xxx` 容易拿到 undefined 或踩 inject 约束。

### 二.4.4 客户端 store 引擎的确切导出名

笔记 `2026-08-28-client-store-dual-cohort-engine-shim.md` 逐字给出（两个 cohort 的契约完全相同）：

```text
createSnapshotStore / defineStore / shallowEqual
```

- 来源面：`@deepseek-ai/dsh-client-store`（0.1.2+ 的冻结平台模块）或 `@deepseek-ai/dsh-client-runtime/client`（rc.2 的 inject module 的 `./client` face）。
- **`notifySubscribers` 只在 cohort 包里有，绝不能 re-export**——*"a future value import of it fails the build with a missing-export error instead of silently breaking rc.2"*。
- 真实报错（逐字，非常重要，新手一定会遇到这个形状）：

```text
failed to import loader entry 47c06ebb (@linxin666/dsh-client-ui-web-ui-settings):
client-modules: require("@deepseek-ai/dsh-client-store") missed the module table —
not a platform seed word, not a materialized module, and no registered package factory
```

→ 遇到"missed the module table"就是**在浏览器 bundle 里 import 了一个平台没允许的包**（平台种子表见 §三与 `shared/web-platform.ts`）。

### 二.4.5 `stream()` 与 `invoke()` 是两种网关调用

- 网关有 `stream()`（流式）与 `invoke()`（一次性）两种；RPC 方法名与调用方式必须配对（见坑 D2）。
- 具体方法名清单**未找到**（blob 不可用）；只能从笔记确认"`stream()` vs `invoke()` 用错会静默拿不到数据"这一模式。

## 二.5　样式与主题怎么写（事实，不猜测）

### 二.5.1 官方契约原文（`zhu1090093659_dsh-web` 的 `packages/AGENTS.md`，逐字引用）

> - **样式**：CSS Modules（`*.module.css`）经 lightningcss 编译进 bundle；不引入
>   UI 框架样式库。填充主按钮一律用主按钮三件套
>   （`--dsw-alias-button-primary-fill` / `--dsw-alias-button-primary-hover` /
>   `--dsw-alias-label-primary-foreground`，明暗两组），不得把
>   `--dsw-alias-brand-primary` 当填充色（官方主题下它与前景同值，会出现
>   黑底黑字/白底白字），契约见
>   [skins/skin-center/contracts/primary-action-tokens-v1.md](skins/skin-center/contracts/primary-action-tokens-v1.md)。

**结论（可直接照抄的规范）**：

1. **样式方案就是 CSS Modules**：文件名 `*.module.css`，通过 `import styles from './x.module.css'` 用。**不是** CSS-in-JS，**不是** Tailwind，**不是** UI 框架样式库。
2. **编译器是 lightningcss**，产物打进浏览器 bundle。
3. **主按钮三件套 token**（明暗各一组，都要出）：
   - 填充：`--dsw-alias-button-primary-fill`
   - 悬停：`--dsw-alias-button-primary-hover`
   - 前景文字：`--dsw-alias-label-primary-foreground`
4. **禁止**：把 `--dsw-alias-brand-primary` 当填充色。**原因官方写明**：官方主题下它与前景同值，会造成"黑底黑字/白底白字"。
5. 需要 TypeScript 认识 `*.module.css`，就要有 `src/client/css-modules.d.ts`（`dsh-session-id` 树里有这个文件）。

### 二.5.2 其余在设计 token 与宿主契约里出现过、可确认存在的变量

从笔记与提交里读到的 token / 属性名（**都是真实字符串**）：

- 语义 token：`--dsw-alias-label-secondary`、`--dsw-alias-label-tertiary`、`--dsw-alias-state-error-primary`、`--dsw-alias-state-success-primary`、`--dsw-alias-brand-primary`、`--dsw-alias-scrollbar-*`、`--dsw-skin-scrim`
- 插件自有 token：`--dsh-sidebar-width`、`--dsh-composer-accessory-*`、`--ds-font-family-code`（终端字体，见坑 SB1）
- 语义属性（L2，`packages/AGENTS.md` 逐字）：插件根容器打 `data-dsh-plugin="<插件短名>"`；部件打**裸值** `data-dsh-part`（例如 `column`，**不是** `task-board-column`）；**不复用官方的 `data-plugin`**（它标注 style 标签归属，语义不同）。
- 宿主 DOM 锚点：`[data-slot="<插槽全名>"]`、`[data-dsh-plugin]`、`[class$="_xxx"]` 尾匹配（官方组件类名是哈希的，如 `_dock`）。

### 二.5.3 CSS Modules 注入机制（坑 S2 的真实机制，必须知道）

- 插件样式以 `<style data-plugin-css="...">` 标签注入，tag key 用于去重。
- **class map 的哈希由"文件路径"决定**——所以 8 个不同的包各自有一个同名 `settings-card.module.css` 时，去重会把其中 7 个吃掉（坑 S2 就是这么炸的）。
- 卸载清理用 `data-plugin` 键。

**给新手的教训**：CSS Modules 的类名要**按包命名空间化**（例如 `session-id.module.css` 而不是 `settings-card.module.css`），否则跨包同名会互相吞掉。

## 二.6　完整插件目录树

### 二.6.1 `packages/dsh-session-id/`（最小纯客户端 UI 插件）

见 §二.1.3（24 个文件，已给完整树）。

### 二.6.2 `packages/dsh-web-all/`（聚合载具，含"客户端要携带子插件"的架构）

```text
packages/dsh-web-all/aggregate.yml
packages/dsh-web-all/lib/shells/package.json
packages/dsh-web-all/package.json
packages/dsh-web-all/src/client/children.generated.ts
packages/dsh-web-all/src/client/children.modules.d.ts
packages/dsh-web-all/src/client/children.specifiers.json
packages/dsh-web-all/src/client/index.ts
packages/dsh-web-all/src/client/mount-children.ts
packages/dsh-web-all/src/degraded.ts
packages/dsh-web-all/src/index.ts
packages/dsh-web-all/src/rows.ts
packages/dsh-web-all/src/shell.ts
packages/dsh-web-all/src/shells/package.json
packages/dsh-web-all/src/shells/shell.ts
packages/dsh-web-all/src/state.ts
packages/dsh-web-all/src/shells/...   （tests 见下）
```
（注：`tests/` 下 6 个测试文件，含 `shell-isolation.spec.ts`、`client-children-mount.spec.ts`；`src/state.ts`、`src/degraded.ts`、`src/rows.ts` 是 shell 的台账/行生成。）

**这张树讲清了一件关键事**：客户端 bundle 图由 **loader entries** 决定，不是由 `import` 决定。所以聚合包必须：
1. 由生成器产出 `src/client/children.specifiers.json` / `children.generated.ts` / `children.modules.d.ts`；
2. 在 `src/client/mount-children.ts` 里**在浏览器侧把每个子插件的 `./client` 当作嵌套客户端插件挂载**；
3. 生成的 `./client` 产物是 **loader factory 文件**（*"they call `window.__ModuleLoader__.load` on evaluation"*），所以 tsdown 要把这些 specifier **alias 到子包的源码**，tsc 则读生成的 ambient 声明。
（全部依据笔记 `2026-09-02-aggregate-client-children-mount.md`，逐字可读；代价是 `lib/client.js` 从 ~14KB 涨到 ~2.5MB。）

### 二.6.3 `scripts/plugin-template/`（官方脚手架）

见 §二.1.4（12 个文件，已给完整树）。

### 二.6.4 三方仓库的目录树（用于对照"第三方插件长什么样"）

**`omdsh-dev_DSH-better-sidebar`（383 文件，根目录）**：`.editorconfig`、`.github/`、`.gitignore`、`AGENTS.md`、`LICENSE`、`Makefile`、`README.md`、`README_EN.md`、`cordis.patch.yml`、`dsh.plugin.json`、`docs/`（`external-plugin-guide.md` + `plans/` 50+ 篇 + `screenshots/`）、`eslint.config.js`、`package.json`、`playwright.config.ts`、`pnpm-lock.yaml`、`pnpm-workspace.yaml`、`scripts/`（`install.ps1`、`install.sh`、`check-consumer-types.sh`、`e2e-*.sh`、`package-registry.mjs`）、`src/`（host：`agent-opens.ts`、`agent-pty.ts`、`assistant-live.ts`、`browser-probe.ts`、`bundle-route.ts`…）+ `src/client/`（`BrowserView.tsx`、`DiffTab.tsx`、`EditorHost.tsx`…）。

**`dsh-market_dsh-market`（213 文件，根目录）**：`.gitattributes`、`.github/`、`IMPROVEMENT-PLAN.md`、`LICENSE`、`README.md`、`README.zh.md`、`TESTING.md`、`UPDATE-API-V1.md`、`assets/`、**`client/client.js`（提交进仓库的浏览器 bundle）**、`cordis.patch.yml`、`package.json`、**`package-lock.json`（npm，不是 pnpm）**、`scripts/`（`build-site.mjs`、`preflight.mjs`、`restart-smoke.mjs`、`smoke-spawn.mjs`、`validate-registry.mjs`…）、`site/`（静态站）、`src/`（host）+ `src/client/`（browser）、`tests/`（宿主单测）+ `tests/client/`（浏览器半测）+ `tests/web/`（Playwright e2e + 5 个 fixture 插件）、`tsdown.config.ts`、`tsconfig*.json`、`vitest*.config.ts`（3 个 vitest 配置：默认、compat、web）。

---

# A · 三、开发规范（只归纳三仓共识，并标注依据）

**归纳规则**：只有当**三个仓库都这么做**，或**多个提交在反复修同一个问题**时，才写成"规范"，并注明依据。单仓独有的约定会明确标注"（仅 dsh-web）"。

## 三.1　目录怎么放

**三仓共识（依据：三仓 HEAD 目录树都在 `git ls-tree -r --name-only HEAD` 里可见）**：

```text
<插件根>/
  package.json          # 三仓都有
  cordis.patch.yml      # 三仓都有
  tsconfig.json         # 三仓都有
  tsconfig.build.json   # 三仓都有
  tsdown.config.ts      # 三仓都有
  vitest.config.ts      # 三仓都有
  README.md             # 三仓都有
  AGENTS.md             # 三仓根目录都有
  LICENSE               # 三仓都有
  src/                  # host 半区（跑在 dsh host 进程）
  src/client/           # browser 半区（跑在 Web GUI）：*.tsx / *.module.css / index.ts
  tests/                # 三仓都有；dsh-web 用 *.spec.tsx、market 分 tests/ + tests/client/ + tests/web/
```

**三仓共识的三条**：

1. **`src/` = host，`src/client/` = browser**。三仓都严格这么分（dsh-web 的 `packages/AGENTS.md` 把它写成硬规则；sidebar 与 market 的树里也是 `src/**` 放 host、`src/client/**` 放 browser）。
2. **测试全部放 `tests/`**（三仓一致；market 进一步按宿主/浏览器/web e2e 分三个子目录，sidebar 有 `tests/e2e/`，并可带 `tests/fixtures/<名字>/{package.json,cordis.patch.yml,index.js}` 作为**最小插件 fixture**——sidebar 与 market 都这么做了）。
3. **一个插件包 = 一个独立可安装的 npm 包**，不是 monorepo 里的一个源文件夹（三仓一致）。

**仅 dsh-web 独有的约定（不要当通用规范）**：
- `src/core/`（两侧共享的纯逻辑，两个 program 都编译）——只有 dsh-web 的 `packages/AGENTS.md` 规定。
- `src/invariant.ts` + `exports["./invariant"]`——只有 dsh-web 用。
- `README.i18n.yaml`（双语配对一致性记录）——只有 dsh-web 的 `packages/AGENTS.md` 要求；market 只有 `README.md` + `README.zh.md`，sidebar 用 `README.md` + `README_EN.md`。
- 插件清单写在哪里**不统一**：dsh-web 与 market 写在 `package.json` 的 `dsh` 字段（AGENTS.md 与提交信息可证）；**sidebar 在根目录另放一份 `dsh.plugin.json`**。→ 新手册应以 `dsh` 字段为主（dsh-web 家族 + market 的做法），但要知道存在 `dsh.plugin.json` 形态。

## 三.2　命名怎么起

**多提交共同修正得出的规律**：

1. **CSS Module 文件名必须按包命名空间化**。依据：坑 S2（8 个包同名 `settings-card.module.css` 互相吞掉）+ 三仓实际命名（sidebar 用 `sidebar.module.css` / `SubagentView.module.css` / `changes.module.css`；market 用 `Market.module.css`；dsh-web 的 AGENTS.md 要求 `*.module.css`）。→ **文件名 = 模块名，不要用 `index.module.css` / `settings-card.module.css` 这种通用名。**
2. **语义属性用裸值**：`data-dsh-plugin="<短名>"` + `data-dsh-part="column"`（**不是** `task-board-column`）。依据：`packages/AGENTS.md` 逐字；且 dsh-web 的 `dsk-session-id/src/client/semantic.ts` 文件存在，说明这是每包一个文件的落地方式。
3. **host 侧服务名用点分命名空间**（如 `remote.agentPresets`、`settings.section`、`session.list`、`directoryPicker.list`）。依据：笔记与提交信息里出现的全部服务/方法名都是这个形状。
4. **patch 行 id 要带命名空间**：dsh-web 的聚合生成器把子插件行 id 统一改成 `web-ui-*`（剥掉子包 `ui-` 前缀）；market 也有一条 `fix(market): namespace market identifiers as dsh-web-ui-market`（d05bf033 附近）。依据：`packages/AGENTS.md` 逐字 + 提交 a7843022。→ **理由（逐字）**："与独立包安装共存，不再触发 loader 的 duplicate entry id"。
5. **测试文件与源码同名 + `.spec`**：三仓一致（`session-id-panel.spec.tsx` 对 `SessionIdPanel.tsx`；`agent-pty.spec.ts` 对 `agent-pty.ts`；`MarketSection.tsx` 对 `tests/client/market-section.client.spec.tsx`）。

## 三.3　类型怎么定义

**三仓共识**（依据：`packages/AGENTS.md` 逐字 + 三仓都有 `tsconfig.json` + `tsconfig.build.json`）：

1. **类型只来自官方 SDK 的 npm 包**，不指向任何 DSH 源码 checkout。原文（`packages/AGENTS.md` 逐字）："只基于官方 NPM SDK：类型来自 `@deepseek-ai/*` devDependencies（node_modules 解析）；peerDependencies 声明运行时注入的服务；**禁止 tsconfig 指向任何 DSH 源码 checkout**。"
2. **tsconfig 分层**：solution + host/client 各自 program（`tsconfig.json` + `tsconfig.build.json` + 有时还有 `tsconfig.client.json` / `tsconfig.tests.json`；market 就有 4 个 tsconfig）。
3. **CSS Modules 要有类型声明**：`src/client/css-modules.d.ts`（dsh-web 的 `dsh-session-id` 有此文件）；market 有 `src/client/globals.d.ts` 与 `src/client/primitives.d.ts`。→ **每个 browser 半区都要有 `.d.ts` 声明环境类型。**
4. **浏览器 bundle 的纯度门（仅 dsh-web，但建议照抄）**：`@deepseek-ai/*` **只能 type-only 导入**；值导入只允许平台种子表成员（react / cordis / ui-slots / ui-primitives，见 `shared/web-platform.ts`）；跨插件协作走 cordis 服务或 slot，不走 value import。依据：`packages/AGENTS.md` 逐字 + 坑 B1/B2 的真实报错。

## 三.4　错误怎么处理

**多提交反复修同一个问题累积出的规范（每条都有多次提交证据）**：

1. **绝不让 promise rejection 逃出去**。证据：坑 X5（`ed3be967`：config-less row 抛错 → unhandled rejection → `installFailLoud` 杀进程）+ 坑 P4（loader 事务组回滚）。→ 插件 `apply()` 的异步逻辑一律 `try/catch`，捕获后**记日志 + 降级**。
2. **报错要解释，不要透传**。证据（多条）：market 的 pnpm ENOENT 只说路径（MK1）、Windows 锁文件 rename 的 pnpm stack（MK12-b）、pnpm 起不来的 argv dump（MK3）、host boot 失败只给一个 entry hash（坑 B1）。→ 报错**点名用户能识别的对象**（插件名/服务名），并给出**下一步动作**。
3. **"能说出来"比"静默失败"重要**。证据：market 的 `ErrorBoundary.tsx`（browser 半区专门的错误边界文件）；dsh-web 的 degraded 台账 + `GET /api/dsh-web-all/degraded` 路由（坑 X5）；提交 `7c9b3941 feat(doctor): boot self-heal attributes the failing plugin row and quarantines it`。→ 崩溃/降级要有**出口**：错误边界、降级台账、日志。
4. **运行期依赖要"使用时探测"，不要写死在硬 inject 里**。证据：坑 D1（`dsh-client-store` 硬 require + `remote.agentPresets` 硬 inject 让 entry 永远 pending）+ 坑 MK10（`settingsScope` 写进模块级 inject 会让整个插件在旧宿主不挂载）。→ cordis **没有可选 inject**，兼容只能靠嵌套 inject / 使用时探测。

## 三.5　要不要写测试

**三仓共识：要，且是硬门禁。**

- 依据 1（`packages/AGENTS.md` 逐字）："每个包必须有 `vitest run` 可通过的测试（`pnpm test` 全仓门禁）。**行为变化必须带测试**；纯 UI 展示层的冒烟测试可放宽为轻量挂载断言。""`tests/` 放测试，**测试文件不得依赖 DSH 源码 checkout 的 fixture**。"
- 依据 2（三仓都有 `vitest.config.ts` 与 `tests/` 目录）。
- 依据 3（多提交反复修同一问题）：几乎每条坑的"修复"段落都带一句测试变化——`shell-isolation.spec.ts`（14→19 用例）、`mobile-adapt.spec.ts`（11 用例）、`md-toc` 单测、`client-children-mount.spec.ts`、`tests/auto-settings.spec.tsx`（对"故意原型方法 fake"渲染）、market 的 `vitest.compat.config.ts`（真 pnpm 兼容车道）。

**从提交里能提炼的两条测试纪律（都是真实教训）**：

1. **测试要让"契约漂移"直接红**。market 与 dsh-web 都用这招：*"the test fakes encode the same descriptor tables so drift fails the suite"*（坑 D2）；*"the fakes … reject extra/missing keys exactly like the gateway's `assertExactArguments`"*。→ **fake 要跟真实契约一样严格**，否则测试全绿、真机死掉。
2. **删掉"测不到东西"的测试**。market 的作者在 `01b3c28` 里逐字写道：*"The test passed with and without the fix — it tested nothing, which is the one thing…"*（他把这条没意义的测试删了）。→ **测试必须能失败**；一个在修复前后都通过的测试是负债。

## 三.6　一句话总结（写进手册的规范清单）

> 目录：`src/`（host）+ `src/client/`（browser）+ `tests/`；根目录必有 `package.json`、`cordis.patch.yml`、两个 tsconfig、`tsdown.config.ts`、`vitest.config.ts`、`README`（双语）、`AGENTS.md`、`LICENSE`。
> 命名：CSS Module 与 patch 行 id 都要带包命名空间；语义属性用 `data-dsh-plugin` + 裸值 `data-dsh-part`。
> 类型：只依赖官方 `@deepseek-ai/*` npm 类型；browser 半区要有 `.d.ts`；`@deepseek-ai/*` 在 browser 里只能 type-only。
> 错误：异步一律 try/catch，绝不放走 rejection；报错要点名对象 + 给下一步；要有错误边界与降级出口。
> 测试：每包必须有 vitest；行为变化必带测试；fake 要和真实契约一样严格；测不到东西的测试要删。

---

# A · 四、新手最容易卡住的 5 个点（每个一句可执行建议）

> 挑选依据：这 5 条在三个仓库里都留下了**反复出现的修复提交**，且都是"猜不到、必须踩过才知道"的类型。

### 1. 改完前端不生效，以为是 HMR，其实是 bundle 没重建 / 没配 `exports["./client"]`

现象：改了一行 UI，刷新页面没变化；或者 host 报 `1 client package failed to compose` / `failed to import loader entry <hash>`。
**可执行建议**：**先确认两件事，再怀疑 HMR**——(a) `package.json` 里 `dsh.client` 声明与 `exports["./client"]` **必须成对存在**（缺一个就 compose 失败，见坑 B1/B2）；(b) 用 `window.__DSH_BOOT__`（或 boot 日志里的 entry id）确认浏览器**真的加载了你的新 bundle**，而不是旧产物。**改了 bundle 层的任何东西，重启 `dsh web`；只改了被按需服务的 `lib/client.js`，刷新页面即可。**

### 2. 插槽注册了却没显示：不是插槽名写错，就是注册时机不对

现象：`ctx.slots.register` 调了，界面什么都没有；控制台可能只有一行被你自己 `catch` 吞掉的东西。
**可执行建议**：**三步排查**——(a) 写成 `ctx.slots.register(...)`，**绝不写成 `const { register } = ctx.slots`**（解构丢 `this`，报 `Cannot read properties of undefined (reading 'effect')`，见坑 C1）；(b) 用 `ctx.slots.inject` 做**延迟注册**，别在 `apply()` 一开始就注册（坑 C2）；(c) 在浏览器里 `document.querySelector('[data-slot="<你的插槽全名>"]')` 看锚点在不在——**不在就是插槽名错了，在就是渲染/优先级问题**（坑 C4）。另外：`catch(e) {}` 空捕获是这类 bug 的头号帮凶。

### 3. 主按钮变"黑底黑字/白底白字"或看不见

现象：按钮在浅色主题下文字和背景同色，或者按钮压根不像按钮。
**可执行建议**：**主按钮只用三件套 token，永远不要把 `--dsw-alias-brand-primary` 当填充色**——官方写明它在官方主题下与前景同值（见 §二.5.1 与坑 MK4）。三件套是 `--dsw-alias-button-primary-fill`（填充）、`--dsw-alias-button-primary-hover`（悬停）、`--dsw-alias-label-primary-foreground`（前景），**明暗两组都要给**。

### 4. 卸载/改开关后"刷新一下就好"——其实根本没生效

现象：卸载插件提示"hot，刷新即可"，刷新后还是坏的；或者改了启用开关，界面看着变了但功能没变。
**可执行建议**：**先问"这个动作天然是热生效的吗"**——(a) 带原生 `.node` 的插件**不能热卸载**，必须整进程重启（坑 MK2）；(b) 卸载后"刷新页面"**必然** 404（bundle 没了、loader entry 还在），要在响应完成后**先禁掉自己的 entry**（坑 MK11）；(c) 改完**明确告诉用户"已生效"还是"待重启"**（坑 P6），`dsh.bundle.patch` 层的改动一律待重启。

### 5. 在浏览器半区 import 了不该 import 的包，bundle 直接不加载

现象：控制台报 `client-modules: require("...") missed the module table — not a platform seed word, not a materialized module, and no registered package factory`。
**可执行建议**：**浏览器半区里 `@deepseek-ai/*` 只能写 `import type`**；要用值只允许**平台种子表**里的那 9 个 specifier（react 四件套 + `@deepseek-ai/cordis` + `dsh-client-store` + `dsh-client-ui-slots` + `dsh-client-ui-primitives` + `dsh-client-ui-dockkit`；权威来源 `packages/client/web/src/platform.ts:8-14`）。需要别的插件的功能时，**不要 `import` 它**，改用 **cordis 服务**（`ctx.slots` / `ctx.sessions` / `ctx.workspaces`）或插槽（见 §二.4.4 与 `packages/AGENTS.md` 的"浏览器 bundle 纯度门"）。

> 🔧 **校正（2026-09-11）**：本节原文写「只用平台种子表允许的**四个**（react / cordis / ui-slots / ui-primitives）」——那是**低估**，且写的是简写名而非真实 specifier。已按源码改为 9 个全名。见 `14-inbound-http-and-timers.md` §17.3。

---

# 附：本报告的素材边界（务必随报告一起读）

1. 三个仓库都是 `--filter=blob:none` 的部分克隆。dsh-web 有 365 个可用 blob（`.agents/notes/**` + `packages/AGENTS.md`），**sidebar 与 market 为 0**。因此：
   - 所有"坑"都来自**提交信息 + 维护者笔记 + 目录树**这三类**真实可读**证据，每条都标了 `仓库 + commit 短哈希`或`仓库 + 文件路径`。
   - 所有"照抄代码"需求中拿不到的部分，都明确标注 **未找到（blob 不可用）**，**没有一行虚构代码**。
2. dsh-web 的 `.agents/notes/**` 是本次最有价值的素材源：365 个 blob 全部可读，共 786 个笔记文件（含 zh 与 i18n 配对），形态是维护者自写的 RFC/事故报告，正文骨骼固定为 `## Problem` / `## Decision` / `## Alternatives considered` / `## Consequences` / `## Testing`，含真实报错字符串、根因、权衡与否决方案、验证步骤。
3. 若要补齐"逐字源码"，只有一条路：给能联网的环境，对三仓执行 `git fetch`（补 blob），或改用 `git clone`（不带 `--filter`）。在那之前，本报告是本任务能达到的**事实上限**。

---

