# B 方向分册 · 外部调用 / 工具 / 协议集成

> **文件来源**：本文件由 `10-community-casebook.md` 拆分而来，并按**来源政策定点改写**（**不是**逐行搬迁）：私有实现类条目不收录，通用教训以「自撰建议」形式保留。其余各册 `10a` / `10c` / `10d` 仍是逐行搬迁。
> **本册性质**：**全部是上游一手素材原文** —— 性质不一：既有官方文档的**逐字摘录（属权威原文）**，也有调研期写下的**粗笔记（仅备查）**。**读某一段前，务必连带读该段开头的取材说明**，那是判断这段能信多少的依据。
> **不要整读**：先 `grep -n '^#{1,2} '` 拿小节清单，再只读需要的那一节。总索引见 `10-community-casebook.md`。
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> 🔴 **许可警示（本册特有，务必先读）**：**本册只引用 MIT / Apache-2.0 / BSD-3-Clause 三类来源，不含任何 copyleft 内容。**（三者均为 permissive；BSD-3-Clause 比 MIT 只多一条无背书条款。）
> · `Tencent/WeKnora`（§1.1）· `liustack/modlens`（§1.3）为 **MIT**；
> · `yjh051108/dsh-routing-suite`（§1.4）**许可自相矛盾**：根 `LICENSE` 是 MIT，但根 `package.json` 与 `injector/package.json` 声明 **BSD-3-Clause**（`injector/` 又**没有** LICENSE 文件），`graded/` 自带 **Apache-2.0** 全文。→ 本技能对 `injector/` 内容**按更严的 BSD-3-Clause 处理**（BSD-3 的义务严格多于 MIT），`graded/` 内容按 Apache-2.0 处理。逐包对照见随包 `NOTICE` §2；
> · `zhu1090093659/dsh-web` 为 **Apache-2.0（仓库根）**，但其**四个子包**为 **BSD-3-Clause**，另有资源目录属 **CC BY-NC-SA 4.0（非商业）** —— 本册**不引用任何资源目录内容**。
> **照抄任何第三方片段进你的项目前，都要先核对它的上游许可。** 完整来源、许可与版权声明对照见本技能根目录 `LICENSE` 末段与随包分发的 `NOTICE`。

---

<!-- ↓ 源：B-tools-external.md （全文） -->

# B · 外部调用 / 工具 / 协议集成方向 —— 踩坑原始素材与可抄模板

> 用途：《DSH 插件开发实战手册·补充篇》原始素材。读者定位：零软件工程经验。
> 调研对象（4 个仓库，均为 dsh 0.1.x 生态真实插件）：
> 1. `Tencent_WeKnora` → 包 `packages/dsh-weknora`（`@wxg-prc-cpg/dsh-weknora`）
> 3. `liustack_modlens` → 包根即插件（`@liustack/modlens`，`dsh/` 目录为 dsh 半边）
> 4. `yjh051108_dsh-routing-suite` → `injector/`（`@dsh-external/dsh-super-injector`）+ `graded/`（`@dsh-external/dsh-graded-mode`）
>
> 素材来源标注规则：`仓库 + 文件路径` 或 `仓库 + commit 短哈希 + 提交信息原文`。
> 本次实际读到源码/文档文件约 **44 个**（其中 6 个为分段读取）。git 历史只有 commit 元数据、无 blob，
> 所有修复内容均来自 **commit message 正文**，未使用 `git show <hash>:<path>`。

---

# B · 一、挖坑记录（现象 → 根因 → 怎么修）

## 1.1 Tencent_WeKnora / `packages/dsh-weknora`

该包只有 4 个相关提交，但 `feat` 提交的正文里 **自带一份完整复盘**（多次 fix 被 squash 进同一提交）。
提交时序（`git log --oneline -- packages/dsh-weknora`）：

```
d75cf72f chore: prepare v0.8.0 release notes and version bump
c1b54df7 fix(dsh-weknora): show knowledge-base figures in plugin answers (#2829) (#2895)
a68bc532 docs: link dsh-weknora to its npm package page
5b140206 feat(dsh-weknora): DeepSeek Harness plugin exposing WeKnora retrieval tools (#2759)
```

### 坑 W1（最重要）：无 scope 的检索调用 → 模型收到不透明的 HTTP 400；mock 与真实 handler 不一致导致测试测不出

- **来源**：`Tencent_WeKnora + 5b140206 + feat(dsh-weknora): DeepSeek Harness plugin exposing WeKnora retrieval tools (#2759)`，正文小节原文：

  > `* fix(dsh-weknora): demand the retrieval scope WeKnora actually requires`
  > `WeKnora rejects a knowledge-search that names no knowledge base, document or tag. The search tool told the model the opposite — that the deployment would decide the scope when a call named none — so on a deployment with no configured default, which is what the quickstart's optional WEKNORA_KNOWLEDGE_BASE_IDS leaves behind, the model's first search failed with an opaque HTTP 400.`
  > `The mock backend answered unscoped retrievals where the real handler refuses them, which is why no test caught this. Align the mock with the handler, state the requirement in the description, and reject the call inside the plugin so the model gets a message naming the argument to supply instead of a transport error.`

- **现象**：按 README 快速开始（不设 `WEKNORA_KNOWLEDGE_BASE_IDS`）装好后，模型第一次调 `weknora_search` 报 `HTTP 400`，信息里没有任何“你缺哪个参数”的提示，模型无法自救。
- **根因**：① 服务端 `POST /knowledge-search` 要求请求体必须带 `knowledge_base_ids` / `knowledge_ids` / tag 之一；② 插件工具描述却写“不指定就由部署决定”；③ 单测用的 mock 后端比真实 Go handler 宽松，放过了无 scope 调用 → 测试全绿但线上必挂。
- **怎么修**（三层一起改）：
  1. **插件内主动拦截**，抛出点名参数的错，而不是让请求打到服务端拿 400。当前源码 `packages/dsh-weknora/src/tools.ts:340-343`：

     ```ts
     // Fail here rather than let WeKnora answer 400: the model can act on a
     // message naming the argument to supply, not on a transport error.
     if (knowledgeBaseIds.length === 0 && knowledgeIds.length === 0) {
       throw new Error(`${toolName}: this WeKnora credential can see no knowledge base, so there is `
         + 'nothing to search. Check the deployment\'s API key scope.')
     }
     ```
  2. **让 mock 与真实 handler 行为一致**（mock 也拒绝无 scope 检索）。
  3. **工具描述与行为对齐**，并把 scope 解析内置化。源码 `src/tools.ts:179-184` 的 `resolveScope`：

     ```ts
     const resolveScope = async (requested: string[], knowledgeIds: string[], signal: AbortSignal): Promise<string[]> => {
       if (requested.length > 0) return requested
       if (config.knowledgeBaseIds.length > 0) return config.knowledgeBaseIds
       if (knowledgeIds.length > 0) return []
       return await allKnowledgeBaseIds(signal)
     }
     ```
     以及 `src/tools.ts:168-178` 的“可见知识库全集只解析一次并缓存”：

     ```ts
     let everyId: Promise<string[]> | undefined
     const allKnowledgeBaseIds = async (signal: AbortSignal): Promise<string[]> => {
       everyId ??= client.listKnowledgeBases(signal).then(
         bases => bases.map(kb => typeof kb.id === 'string' ? kb.id : '').filter(id => id !== ''),
         (error: unknown) => { everyId = undefined; throw error },
       )
       return await everyId
     }
     ```
- **给手册的教训**：**错误信息本身就是模型可用性的接口**。外部 API 的 400/500 要翻译成“你该改哪个参数”的话；单测的假后端必须和真后端一样“凶”。

### 坑 W2：`resource://` handle 在 dsh 里渲染不了 → 引用配图全丢

- **来源**：`Tencent_WeKnora + c1b54df7 + fix(dsh-weknora): show knowledge-base figures in plugin answers (#2829) (#2895)`，正文原文：

  > `dsh cannot load resource:// handles, and the plugin previously dropped image_info, so Q&A returned text only. Default to public URLs and emit Markdown images so the harness can render cited figures.`
  > `Refs: https://github.com/Tencent/WeKnora/issues/2829`
  > 二次修订：`Passage text already carries Markdown figures after WeKnora rewrites resource:// handles. Drop the extra images arrays and clip restoration.`

- **现象**：`weknora_ask` 返回的答案/引用里图片全部消失，只剩文字（issue #2829）。
- **根因**：WeKnora 默认返回内部句柄 `resource://…`，dsh web UI 只认识 `https://` 的 Markdown 图片，不认识内部句柄；插件又主动丢弃了 `image_info`。
- **怎么修**：
  1. 配置默认改为 `resourceUrls: 'public'`（`src/config.ts:59-67` 的 DEFAULTS 与 `src/config.ts:152-155` 校验）。
  2. 通过查询参数要求服务端把 `resource://` 改写成可直接加载的 http(s) URL。`src/client.ts:132-143`：

     ```ts
     private resourceMode(): 'handle' | 'public' {
       return this.config.resourceUrls === 'public' && !this.publicModeBlocked ? 'public' : 'handle'
     }

     private url(path: string, query?: Record<string, string | number | undefined>): string {
       const url = new URL(`${this.config.baseUrl}${path}`)
       for (const [key, value] of Object.entries(query ?? {})) {
         if (value !== undefined) url.searchParams.set(key, String(value))
       }
       if (this.resourceMode() === 'public') url.searchParams.set('resource_urls', 'public')
       return url.toString()
     }
     ```
  3. 遇到受限 API Key（服务端 403）时**自动降级并记住**，不重复付代价。`src/client.ts:113-118 / 145-165`：

     ```ts
     /**
      * A knowledge-base-restricted API key rejects `resource_urls=public` with
      * 403. After the first such refusal this client stays on handle mode so
      * later calls do not pay the same round trip.
      */
     private publicModeBlocked = false
     ```
     ```ts
     private isPublicModeForbidden(error: unknown): boolean {
       return error instanceof WeknoraApiError
         && this.config.resourceUrls === 'public'
         && !this.publicModeBlocked
         && error.status === 403
         && error.message.includes('resource_urls=public')
     }
     ```
- **给手册的教训**：跨系统传递“资源引用”时，**必须确认接收端能直接消费的 URL 形态**；对“权限受限导致的降级”要做**一次性记忆**，不要每次调用都撞一次 403。

### 坑 W3：SSE 流被截断时，把半截答案当完整答案交给模型

- **来源**：`Tencent_WeKnora + 5b140206`，正文原文（在提交正文末尾）：

  > `Added error handling for incomplete responses in the client, ensuring that truncated streams are properly managed.`

- **现象**：`weknora_ask` 偶发返回半截答案，模型据此作答。
- **根因**：WeKnora 的 `text/event-stream` 以 `response_type: "complete"` 事件结尾；网络中断/超时后流提前结束，之前累积的 `answer` 文本已经拼了一半。
- **怎么修**：用 `completed` 标志；没有收到 `complete` 事件就**抛错而不是返回半截答案**。`src/client.ts:354-433` 关键片段：

  ```ts
  let completed = false
  // ... 在 consumeLine 内：
  //   case 'complete': completed = true; break
  //   case 'error':
  //     throw new WeknoraApiError(`POST ${path} streamed an error: ${event.content ?? 'unknown error'}`)
  // ...
  // WeKnora ends every answer with a `complete` event. Without it the stream was
  // cut short, and handing the model the partial text would present a truncated
  // answer as a whole one.
  if (!completed) {
    throw new WeknoraApiError(`POST ${path} ended before WeKnora completed the answer; `
      + `${answer.join('').length} character(s) had streamed`)
  }
  ```
  同时 `finally { await reader.cancel().catch(() => undefined) }` 保证读取器不泄漏。

### 坑 W4：CI 首次安装 dsh 约 15 分钟，超过 10 分钟 job 限额

- **来源**：
  - `Tencent_WeKnora + 4e25684b + ci(dsh-weknora): cache pinned dsh install to speed up e2e`：正文 `The e2e job spends ~15 minutes downloading @deepseek-ai/dsh on every run while the actual harness scenarios finish in seconds. Cache the install directory keyed by DSH_PINNED_SPEC and enable npm dependency caching.`
  - `Tencent_WeKnora + d4f4787f + ci(dsh-weknora): restore e2e timeout for cold dsh cache`：正文 `First-run npm install of @deepseek-ai/dsh still takes ~15 minutes; the 10-minute job limit cancelled the run before the cache could warm up.`
- **根因**：`dsh plugin add` 背后是 pnpm 安装整棵 harness 依赖树，冷缓存极慢。
- **怎么修**：给 e2e job 加缓存（key 用 `DSH_PINNED_SPEC`）+ 放宽超时；工作流里还配了**每周一 03:00 UTC 用 dsh@latest 跑一次漂移检测**（允许失败），用于提前发现 harness 破坏性变更。见 `.github/workflows/dsh-plugin.yml`（`DSH_PINNED_SPEC: "@deepseek-ai/dsh@0.1.0-rc.8"`、`schedule: cron: "0 3 * * 1"`）。

### 文档线索（WeKnora）

- `packages/dsh-weknora/README.md` 有 **Compatibility** 段，明确写“Verified against dsh `0.1.0-rc.8` and WeKnora `0.8.0`…this package deliberately has **no runtime dependencies** and hands `ctx.tools.register()` a plain object, so it does not pin any harness package version.”
- 同 README “Development” 段写明：`dsh needs a Node build with zstd support (Node ≥ 22.15 or ≥ 24)…and pnpm ≥ 10 on PATH`。
- 契约测试双端锁定：`test/fixtures/api-contract.json` 记录每一次 WeKnora 调用；`test/contract.test.mjs`（插件侧）与 `contract/contract_test.go`（服务端 Go 类型侧）**两端各自断言**，“so a rename on either side fails CI instead of a user's agent”。
- 在 WeKnora 仓库内 Grep `踩坑/gotcha/pitfall/known issue`，该包文档**未命中**（即该仓库未留下这几类关键词，但上面的 commit 正文已足够详细）。

---

## 1.2 DSH 自身机制类坑（**官方一手源 · MIT**）

> **本节收录标准**：机制类坑只收录**能定位到官方 `deepseek-harness`（MIT）源码行号**的条目。
> 「怎么接某个特定第三方服务」属私有实现细节，不是「DSH 插件怎么写」——不属于本节主题，因此不收录。
> 标为「自撰建议」的条目不受此限：它们不引用任何上游代码，只给判据。

下列三条机制的权威出处都是**官方源码 + 官方单测**，而不依赖任何社区仓库：

### 坑 O1（最重要，且是“静默失效”类）：用 system prompt 注入记忆会被 persona 的 `complete: true` 整段丢弃

- **来源（已升级为一手源码，非社区二手说明）**：这条**不是**某个社区仓库的知识，而是 **DSH 自身的行为**，官方有一手记载 ——

  | # | 官方出处（MIT） | 原文/要点 |
  |---|---|---|
  | ① | `packages/preset/persona/src/index.ts:42-43` | 字段注释：`Make the prefix the complete system prompt, suppressing the suffix and every other section.`（`complete?: boolean`） |
  | ② | 同文件 `:52` / `:67` | 默认值 `complete: z.boolean().default(false)`；生效点 `...(config.complete ? { complete: true } : {})` |
  | ③ | `packages/core/system-prompt/tests/system-prompt.spec.ts:380-385` | 官方单测固定该行为：`restores one complete section after the assembly waterfall` |
  | ④ | `docs/agent-lifecycle.zh.md:29-36` | 组装顺序：`system-prompt/assemble` waterfall 先跑，`agent/pre-step` waterfall 紧随其后，返回 `authoritative reject or enter(messages)` |

  **机制**：当某个 preset 的 persona 声明了 `complete: true`（内置 `minimal` preset 即如此），组装完成后 persona 段会被还原为**唯一**的 prompt 段，其它贡献随之被静默丢弃；因此走 system prompt 的记忆插件在这类 preset 下会丢掉上下文，而且不报错。本技能引用这条机制，是为了解释下面为什么推荐 `agent/pre-step` 而非 system prompt。

  > 📌 本坑**只以官方一手出处为准**，不转述任何社区文档。

- **现象**：记忆/画像注入“看起来装好了”，但在 `minimal` 这类 preset 下完全没有生效，且**没有任何报错**。
- **根因**：dsh 的 persona 若声明 `complete: true`，组装后会用 persona 段覆盖成“唯一 prompt 段”，其它 system prompt 贡献被静默丢弃。
- **怎么修**：走 `agent/pre-step` waterfall，把注入作为**持久、带来源归属的 user 消息**追加到本步，而不是塞进 system prompt。

  waterfall 监听器**必须调用 `next()`**，不调用会短路整条流水线（官方原文：`docs/user/develop/framework/events.zh.md:64-81`）。在 `agent/pre-step` 上返回值契约是 **`enter(messages)`**（`docs/agent-lifecycle.zh.md:33`）——**追加消息才是这个钩子的用途**。

  官方自己就是这么做「向本步追加一条消息」的 —— `packages/core/agent/src/model-selection.ts:161-120`（**官方生产代码，MIT**，节选、省略了上游上下文）：

  ```ts
  // 出处：packages/core/agent/src/model-selection.ts:161-120（节选）
  const previous = agent.session.requestHeader()?.config
  if (selected === undefined || previous === undefined || sameRoute(selected, previous)) return decision
  return { ...decision, messages: [...decision.messages, modelSwitchNotice(previous, selected)] }
  }, { prepend: true })
  ```

  **要点**：`{ prepend: true }` 让**下游监听器先跑**，所以**必须先 `await next()` 拿到最终结果再追加**，不能凭空造——这样本插件才是「最后说话的人」。这个选项是官方 API，官方另有用法见 `packages/core/system-prompt/tests/system-prompt.spec.ts:391`。
  注入的消息应当用 **dsh 自己的消息构造器**生成，而不是手搓对象字面量——这样 identity、规范化与未来的 Message 不变量都由宿主保证；生成的消息带 `source: { kind: 'plugin', … }` 归属标记，下游可据此区分来源。（构造器本身的用法与契约以当前 DSH 源码为准。）
- **给手册的教训**：**“没有报错的失效”是最危险的坑**。往 system prompt 塞内容前，先确认目标 preset 的 persona 是否 `complete: true`；插件注入优先走消息通道。

- **通用结论（自撰观察，与任何上游实现无关）**：`dsh plugin` 把安装动作转发给 profile 目录下的 pnpm，所以插件必须是**真实包**；`dsh plugin add ./path/to/plugin` 这种源码链接只有在那个 checkout 自带 `node_modules` 时才行 —— 因为 Node 会从**源树的 realpath** 解析 dsh peers，而不是从 profile 目录解析。

**通用教训**（自撰建议，不引用任何上游代码）：

- **教训 1**：宿主在 `apply()` 里**已经解析好**的配置值，不要指望子进程自己再解析一遍 —— **显式写进子进程的 `env`**。凭据类配置尤其如此：继承环境里「长得像凭据」的变量会被宿主清理，而配置补丁对子进程不可见；两头都不通时，运行时表现为「凭据为空」，而不是报错。
- **教训 2**：**「锁存式失败」是长驻进程的隐形炸弹**。任何 `failed = true` 的降级开关，都必须配一条自动恢复路径（后台重放 + 状态重推导），并给定时器加 `unref()`，免得它阻止进程退出。

### 坑 O5：DSH 工具结果用 camelCase 的 `isError`，插件只认 `is_error` → 失败的调用被记成“成功”

- **来源（官方一手源码，MIT）**：这是 **DSH 自身的契约**，官方有三处记载 ——

  | # | 官方出处（MIT） | 原文/要点 |
  |---|---|---|
  | ① | `packages/llm/llm/src/message.ts:173-179` | 工具结果块 `ToolResultMessage` 里字段名就是 camelCase：`readonly isError?: boolean` |
  | ② | `packages/extensions/tool-cordis/src/api-catalog.ts`（自动生成的契约目录，`ToolResultMessage` 声明；行号随生成漂移，故不写死） | 契约全文：`export interface ToolResultMessage extends MessageBase { readonly role: 'tool'; readonly source: ToolMessageSource; readonly toolCallId: ToolCallId; readonly isError?: boolean; }` |
  | ③ | `packages/acp/acp/src/updates.ts:82` | 官方生产代码即用它判成败：`status: result.isError === true ? 'failed' : 'completed'` |

- **现象**：消费方自己写「失败判定」时按 snake_case `is_error` 去读，**永远读不到** —— 失败的调用被记成 `completed`（错误文本仍在 `tool_output` 里，只是状态字段是错的）。
- **根因**：契约字段是 camelCase `isError`，而不少 JS / Python 生态的同类字段惯例是 snake_case `is_error`；照习惯手写判定就会静默错标。
- **怎么修（自撰建议）**：判定里**两种拼写都认**（`result.isError ?? result.is_error` 一类的兼容读法），并且**给这个判定补一条测试**。这类错标只影响「看状态行事」的消费方（血缘、用量统计、工作记忆格式化、训练产物），不会当场报错，是最难发现的一类。
- **给手册的教训**：读宿主回传的结构时，**字段命名的拼写变体（snake_case vs camelCase）是一类系统性坑**。**判据永远是 DSH 自己的类型声明，不是别的生态的命名习惯。**

**通用教训**（自撰建议，不引用任何上游代码）：

- **教训 3（错误分类）**：**错误码要能区分「对方挂了」与「我们等太短」**。把「本端超时」混进 catch-all 兜底，会把健康服务报成故障，用户就去查一个根本没坏的东西。超时错误要在消息里点名：**耗时预算 + 端点 + 放宽它的那个旋钮名**。
- **教训 4（参数级校验）**：做参数级校验（例如拦截某种协议的 URI）时，先分清哪些字段是**位置**、哪些是**内容**。对「剩下的全部参数值」无差别全扫，会让**正文里恰好提到该协议**的正常写入被误拒 —— 拦截器误伤比放行更烦人。误拦时要给出「改用哪个工具 + 一个可抄的调用示例」。
- **教训 5（跨平台子进程）**：桌面宿主（Electron 一类）里 **`process.execPath` 是宿主二进制、不是 Node**。要让 Electron 以 Node 模式跑脚本，标准解法是显式设 `ELECTRON_RUN_AS_NODE=1`；且**启动子进程的方案要按宿主类型分支，不能一把梭** —— 同一处曾出现「改动 → 回滚」的往复，正是「一把梭」的代价。

**通用教训**（自撰建议，不引用任何上游代码）：

- **教训 6（幂等注入）**：任何「每会话只注入一次」的东西，都必须有**幂等判据** —— 建议直接用宿主给消息打的 `source.kind` / `plugin` / `form` 三件套，去查「本会话历史里是否已经有本插件的 instructions 消息」。**并且要同时覆盖 `session.events` 与「inbox 待发队列」两条路径**，否则会话重建（re-seed）之后会重复注入。
- **教训 7（歧义即拒绝）**：URI / 路径里出现「保留字 vs 真实名」的歧义时（例如 `scheme://user/<name>` 里的 `<name>` 既可能是保留段、也可能是真实用户名），**宁可在请求边界直接拒绝并给出正确写法，也不要猜**；配套要把历史写法做兼容归一化。
- **教训 8（前缀即命名空间）**：以固定前缀承载配置与身份（如 `XXX_` 一族环境变量）时，**API key 是最常被漏的一项**；上线前用一条「缺哪个变量」的自检把它变成可报错的事，而不是等运行时空值。

#### 一条与任何插件无关的通用事实：包版本自守

写插件包时，让「包内自报版本」与 `package.json` 的 `version` **由一个脚本守一致**（例如一条 `check:version`）。否则「装的到底是哪个版本」会在排查时变成口径打架。

---

## 1.3 liustack_modlens / `@liustack/modlens`（包根即插件，`dsh/` 是 dsh 半边）

modlens 的 dsh 相关修复提交极多（`git log --oneline -i --grep='dsh'` 有 40+ 条）。挑与“工具 / 外部调用 / 协议集成”最相关的：

### 坑 M1（最重要，安装类）：`declares no dsh.bundle — installed as a plain dependency`

- **来源**：`liustack_modlens + docs/troubleshooting.zh-CN.md`（该条标题就是 dsh 的原话），正文原文：

  > `dsh profile 装到的是旧版 modlens。`dsh.bundle` 声明从 3.9.0 起才存在，而 pnpm 11 会扣住最近 24 小时内发布的版本（`minimumReleaseAge`，自 11.0 起默认开启。`pnpm config get` 不展示这一项的内置默认值，所以查它什么都不显示）。当带声明的版本全都落在这个窗口内时，pnpm 会静默回退到更旧的版本，而旧版本没有 bundle 声明，dsh 于是正确地把它当作普通依赖，一个工具都不会出现。`
  > ``@latest` 绕不开这一层，本页早先的说法是错的。冷静期先把候选版本过滤掉，dist-tag 才在剩下的里面解析，于是它直接落到了更旧的那个上。改成写死精确版本号，pnpm 会把它当作一次明确的指定，而不是一次解析：`
  > ```sh
  > npx -y @deepseek-ai/dsh plugin --profile <name> add @liustack/modlens@3.26.1
  > ```
  > `如果你自己设过 `minimumReleaseAge`，pnpm 会把这条策略视为严格模式，转而拒绝安装并报出版本与截止时间（`ERR_PNPM_NO_MATURE_MATCHING_VERSION`）。在同一个文件里放行这一个版本：`
  > ```yaml
  > minimumReleaseAgeExclude:
  >   - '@liustack/modlens@3.26.1'
  > ```

- **现象**：插件“装上了”，但一个工具都不出现；dsh 报 `declares no dsh.bundle — installed as a plain dependency`。
- **根因**：pnpm 11 的 24 小时冷静期 + 未点名版本号 → 静默回退到**没有 `dsh.bundle` 声明的旧版**。
- **怎么修**：**安装时写死精确版本号**（并同步更新时也用 `add @版本`，而非 `update`，因为 `update` 只在已记录的 caret 范围内挪动，2.7.1 永远进不了 3.x）。同文档还给出更严格的 `minimumReleaseAgeExclude` 例外写法。
- **给手册的教训**：**“装上了但没生效”** 优先查版本：包是否声明了 `dsh` 字段、装到的是不是被冷静期回退的旧版。`dsh plugin --profile <name> list` 可以看到实际装了什么。

### 坑 M2：工具名与宿主 `read_image` 撞名 → 宿主 scoped 层静默遮蔽插件全局层

- **来源**：`liustack_modlens + docs/troubleshooting.zh-CN.md`「dsh：模型看不到 read_image 工具」：

  > `插件注册的工具名是 `modlens_read_image`，不是 `read_image`。dsh 的工具注册表是分层的，scoped 层会遮蔽全局层：宿主的 `read_image` 挂在 agent preset 作用域、插件注册在全局层，两者根本不算重名，于是注册静默成功，模型解析到的仍是宿主那个，而它对纯文本模型直接拒绝（[#34](https://github.com/liustack/modlens/issues/34)）。用自己的名字就没有东西会遮蔽它，模型是通过工具 schema 找到它的，而 schema 每次请求都会送达，与叫什么名字无关。`
  > `如果模型仍然看不到，去 harness 日志里搜 `[modlens] ... registration skipped`。`

- **现象**：注册没报错，但模型看不到/解析到的是别人的同名工具。
- **根因**：dsh 工具注册表**分层**，scoped（agent preset）层遮蔽全局层；重名不是错误，是静默遮蔽。
- **怎么修**：**给自己的工具起一个专属名字**（`modlens_read_image`）。源码注释把结论写死（`dsh/index.js:296-314`）：

  ```js
  // A name of our own rather than the host's. dsh's registry is layered and
  // a scoped tool shadows a global one, so a host `read_image` mounted in the
  // agent-preset scope and ours registered globally are not a duplicate at
  // all: the registration succeeds, nothing throws, and the model still
  // resolves the host's (issue #34). ... `toolName` still pins whatever a host
  // prefers.
  const preferred = config.toolName || 'modlens_read_image'
  try {
    ctx.tools.register(readImageTool(preferred))
  } catch (error) {
    // Same-layer duplicate of the chosen name, or a preview-era surface
    // change: degrade loudly instead of taking the whole plugin down.
    console.error(`[modlens] ${preferred} registration skipped: ${error}`)
  }
  ```
- **给手册的教训**：**注册成功 ≠ 生效**。起名要避开宿主已有工具；注册用 `try/catch` 兜住并“响一声”（`console.error`），不要静默吞掉。

### 坑 M3：harness 小版本升级改了工具定义的必填字段 → `prepareCall` 派发缺失

- **来源**：`liustack_modlens + 9199c6c + fix(dsh): serve the prepareCall dispatch dsh 0.1.1 requires`（**正文为空**，仅标题）。可印证：插件工具定义里同时提供 `presentCall`，并在 `apply()` 里为宿主预留了工具名与 schema。
- **现象**：dsh 0.1.1 下工具派发失败。
- **根因**：harness 开发者预览期**会增改工具定义契约**（0.1.1 要求 `prepareCall` 派发）。
- **怎么修**：跟随新版提供所需字段。同时插件对“预览期表面变化”统一用 `try/catch` + “degrade loudly”（见 M2 代码）。
- **给手册的教训**：dsh 处于 developer preview，**工具定义契约会变**；插件要（a）不 import 宿主包，只交普通对象（WeKnora 与 modlens 都这么做），（b）注册失败要响。

### 坑 M4：dsh 0.1.0-rc.7 把 settings slot 变成 keyed → 卡片整块不渲染

- **来源**：`liustack_modlens + f0ab04f + fix(dsh): give the settings card the key and namespace rc.7 renders by`，正文原文：

  > `dsh 0.1.0-rc.7 changed the settings page twice over. The slot the card registers into became keyed, so registering without options.key throws, which is the console error both reports carry. And a card now renders only when its key matches a settings namespace the host serves, where the old page rendered every registered card.`
  > `So the fix is two-sided. The browser half keeps its id, which rc.6's list slot requires, and adds key: 'modlens', which rc.7's keyed slot requires; one client.js serves both versions. The host half registers a 'modlens' settings namespace so the key has something to match.`

- **现象**：设置页里插件卡片消失，控制台报 keyed-slot 错误（issues #61/#65）。
- **根因**：rc.7 起 slot 需要 `key`，且卡片必须匹配宿主提供的 settings namespace。
- **怎么修**：**双版本兼容**——保留 `id`（rc.6 列表槽需要），再加 `key`（rc.7 键控槽需要）；宿主侧注册一个同名空 namespace 让 key 有东西可匹配（`dsh/index.js:207-219`）：

  ```js
  if (config.settingsCard !== false && typeof ctx.inject === 'function') {
    ctx.inject(['settings'], (scope) => {
      try {
        const passThrough = (value) => ({ ...(value ?? {}) })
        passThrough.toJSON = () => ({
          uid: 0,
          refs: { 0: { type: 'object', meta: { default: {} }, dict: {} } },
        })
        scope.settings.register('modlens', passThrough, { base: {} })
      } catch (error) {
        console.error(`[modlens] settings namespace skipped: ${error}`)
      }
    })
  }
  ```
- **给手册的教训**：UI 槽位的“注册契约”也会随 harness 版本变；**同一份 client.js 同时满足新旧两版的必填字段**是最省事的兼容法。

### 坑 M5：dsh 0.1.2-rc.1 把 composer 换成 Lexical contenteditable → 粘贴转路径“静默失败”

- **来源**：`liustack_modlens + 4b76ed4 + fix(dsh): write paste-to-path into the Lexical composer (#100)`；`CHANGELOG.md` 第 5 行原文：

  > `**dsh paste-to-path writes into the Lexical composer ([#100]).** dsh 0.1.2-rc.1 replaced the composer textarea with a Lexical contenteditable div. The paste listener still uploaded the image, then insertText returned immediately because it only accepted TEXTAREA and INPUT, so the path never landed and the console stayed quiet. Paste-to-path now resolves a writable target (textarea, input, or [data-composer-input][contenteditable=true]) before taking the event, inserts with execCommand, and logs the path if that insert fails.`

- **现象**：图片上传成功，但输入框里没有出现路径，**控制台一声不响**。
- **根因**：`insertText` 只认 `TEXTAREA`/`INPUT`；新版 composer 是 Lexical 的 `contenteditable` div。
- **怎么修**：先解析“可写目标”，插入优先用 `execCommand('insertText')`，失败再退回原型 setter；内容可编辑 div 不适用 value setter，直接放弃并**打日志**。`dsh/client.js:35-87` 原文：

  ```js
  function isTextField(el) {
    return el && (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT')
  }

  function isComposerEditable(el) {
    if (!el || typeof el.getAttribute !== 'function') return false
    if (el.getAttribute('data-composer-input') == null) return false
    return el.isContentEditable === true || el.contentEditable === 'true'
  }

  function isWritable(el) {
    return isTextField(el) || isComposerEditable(el)
  }

  function insertText(target, text) {
    if (!isWritable(target)) return false
    target.focus()
    // execCommand fires the input event React's controlled textarea needs;
    // the prototype-setter dance is the fallback for engines dropping it.
    var inserted = false
    try {
      inserted = document.execCommand('insertText', false, text)
    } catch {
      inserted = false
    }
    if (inserted) return true
    // Lexical's composer is a contenteditable div: it has no value
    // setter, and assigning innerHTML/textContent bypasses the editor.
    if (!isTextField(target)) return false
    try {
      var proto =
        target.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype
      var setter = Object.getOwnPropertyDescriptor(proto, 'value').set
      setter.call(target, target.value + text)
      target.dispatchEvent(new Event('input', { bubbles: true }))
      return true
    } catch {
      return false
    }
  }
  ```
  插入失败时明确打日志（`dsh/client.js:196-198`）：

  ```js
  if (!insertText(target, `${text} `)) {
    console.error(`[modlens] paste-to-path: could not insert into the composer (${text})`)
  }
  ```
- **给手册的教训**：浏览器端“往输入框里写字”**没有万能写法**，必须按元素类型分支；且**失败必须留下痕迹**（这里原来“console 一声不响”是最坑的部分）。

### 坑 M6：bundle loader 在等必需服务时调 `apply` → 读 `ctx.llm` 抛 “inactive context”

- **来源**：`liustack_modlens + dsh/index.js:145-160` 注释原文，并提到 issue #79：

  > `Bundle loaders can call apply while this outer context is still waiting for its required services. Reading ctx.llm here then throws "inactive context" before the first discovery sweep can register any lifecycle work (#79). Put the whole provider registry inside an injected child scope: Cordis starts it only while llm is active, and tears its listeners and registrations down with that service.`

- **现象**：加载期读可选服务直接抛 “inactive context”。
- **根因**：外层 context 还在等必需服务时 `apply` 已被调用。
- **怎么修**：把整块逻辑塞进 `ctx.inject([...], scope => ...)` 的**子作用域**，服务就绪才启动、服务下线就随之下线。`dsh/index.js:153-159`：

  ```js
  if (typeof ctx.inject === 'function') {
    ctx.inject(['llm'], (scope) => {
      return registerVisionProvider(scope, config, ownProviders, evidenceCache)
    })
  } else {
    registerVisionProvider(ctx, config, ownProviders, evidenceCache)
  }
  ```
  客户端侧同一模式（`dsh/client.js:1063-1105` 注释）：

  > `Reaching for an undeclared service throws in cordis, so each optional dependency rides a scoped ctx.inject of its own: the closure runs where the service exists and never runs where it does not… Listing it beside slots would be worse than useless: ctx.inject waits for every service named, so on a host that never provides locale the card would never register at all.`
- **给手册的教训**：**可选依赖要各自 `ctx.inject`，不要和必需依赖并列**；并列会让“一个可选服务缺席”把整块注册拖死。

### 坑 M7：包装路由丢上游状态 → 推理链（reasoning）成批丢失

- **来源（两条，都是 commit 正文原文）**：
  - `liustack_modlens + 83ab641 + fix(dsh): keep upstream replay state alive through the vision wrapper (#49)`：

    > `Reasoning blocks went missing on sessions routed through a (modlens vision) model… Measured by the reporter at ~57% of turns against a ~1% baseline on the same route… dsh strips an assistant message's adapter-private replayState whenever the provider recorded on that message belongs to a different adapter instance than the one about to run (LlmService.forAdapter, an identity comparison). This wrapper is a different instance by construction, so every turn it produced reached upstream with that state removed, and replayState is what carries reasoning continuity for these models.`
  - `liustack_modlens + c3e1f41 + fix(dsh): the vision wrapper inherits what its upstream route already had (#57)`：

    > `A user configured maxRetries 50 on their route and watched the (modlens vision) group retry twice, the harness default. The wrapper registers its own adapter, and its providerRetryPolicy() was hardcoded to return undefined. … It delegates now.`
    > `This is the second time the wrapper has been found dropping something the upstream had: #49 was the adapter-private replay state… so this went through all five methods the service calls on an adapter rather than fixing the one that was reported.`

- **现象**：走包装路由的会话里 reasoning 块丢失（报道者实测 ~57% vs 基线 ~1%）；`maxRetries` 等上游配置不生效。
- **根因**：包装器是**另一个 adapter 实例**，dsh 按“adapter 身份”比较，于是把 `replayState`（承载推理连续性）剥掉了；`providerRetryPolicy()` 又被硬编码返回 `undefined`。
- **怎么修**：包装器**把所有上游已有的东西都转发/委派**（五件事一次过，而不是只修被报道的那一件）。并明确“不复制 configurable-provider 目录”（配置仍归上游所有）。另有 `906d21a fix(dsh)!: a pinned default id encodes its upstream, like the sweep's`（**BREAKING CHANGE**：pinned 之外的默认 providerId 改为 `modlens-<upstream>`，旧会话需重选一次）。
- **给手册的教训**：**做“包装/代理层”时，宿主是按对象身份判等的**。凡是上游 adapter 提供的字段/方法，包装层都要显式转发；只修被投诉的那一个字段是治标不治本的（这里第二次才补全五处）。

### 坑 M8：Windows 下子进程弹黑框

- **来源**：`liustack_modlens + d7a2300 + fix(spawn): start every child through a wrapper that hides its console`，与 `dsh/spawnHidden.js` 全文：

  ```js
  // The only place this plugin starts a child process.
  //
  // The desktop app has no console of its own, so on Windows every child it
  // starts would be given one and shown its window: a black box per read
  // (issue #60). `windowsHide` suppresses that, defaults to false in Node, and is
  // ignored elsewhere.
  //
  // It lives in a file of its own, apart from its callers, so the rule can be
  // checked by looking at which files reach `child_process` at all rather than at
  // what each call passes. A call site cannot forget an option it never writes,
  // and writing the option after the caller's leaves nothing to override it.
  import { spawn } from 'node:child_process'

  export function spawnHidden(command, args, options) {
    return spawn(command, args, { ...options, windowsHide: true })
  }
  ```
- **根因**：Node 的 `windowsHide` 默认 false；桌面 App 每起一个子进程就闪一个黑框。
- **怎么修**：所有 spawn 收敛到**唯一一个包装函数**，并让 `windowsHide: true` 在**最后**合并（调用方无法覆盖）。文件独立，便于用“哪些文件 import 了 child_process”来审查。
- **给手册的教训**：Windows 下要加 `windowsHide: true`；并且**把跨平台差异封装到一个文件**，而不是靠每个调用点记得传。

### 坑 M9：Node 的 `fetch` 默认无视代理环境变量

- **来源**：`liustack_modlens + docs/troubleshooting.zh-CN.md`「fetch failed 或连接失败」原文：

  > `API 请求根本没离开这台机器。在要靠代理才能上网的网络里这是预期表现：Node 的 fetch 默认无视代理环境变量。你明确要求走代理后 modlens 才会遵循，两种写法任选：`
  > `HTTPS_PROXY=http://127.0.0.1:7890 modlens -i shot.png -p gemini-api   # env (NO_PROXY honored too)`
  > `modlens config set proxy http://127.0.0.1:7890                        # persistent, all API providers`
  > `modlens config set openai.proxy http://127.0.0.1:7890                 # one provider only`
  > `modlens config set openai.proxy ""                                    # 这个 provider 强制直连`
  > `provider 代理字段有三种状态。字段缺失表示继承共享配置或环境代理，空字符串表示直连，URL 表示只给该 provider 使用的代理。当外部 provider 需要共享代理，而内网端点必须直连时，这个区别很重要。`

- **现象**：`Could not connect to generativelanguage.googleapis.com (UND_ERR_CONNECT_TIMEOUT). The request never reached the network.`
- **根因**：Node 内建 fetch **不读** `HTTPS_PROXY` 等环境变量。
- **怎么修**：显式支持代理（env 或配置），并区分“缺省=继承 / 空串=直连 / URL=专用代理”三态。相关提交：`17b5373 fix: keep no-proxy API requests on same-sourced undici fetch`、`9d38558 fix(proxy): 支持 provider 直连与 DSH 代理设置`。
- **给手册的教训**：**“网络失败”先确认请求是否真的出了机器**；需要代理时必须显式配置（`undici`/`ProxyAgent`），别指望环境变量。

### 坑 M10：外部 provider 返回的 JSON 不符合声明的 schema

- **来源**：`liustack_modlens + docs/troubleshooting.zh-CN.md`「openai provider 的结果被拒绝」与 `docs/output-schema.md`：

  > 报错原文：`OpenAI-compatible API returned JSON that does not match the vision schema (wrong or missing: visual.notes, ...)`
  > `大多数 OpenAI 兼容网关在服务端什么都不强制，契约是以填好的 JSON 模板形式随提示词发过去的，能力弱一些的模型可能只答出一半，关掉思考时尤其明显。可以改成让网关自己强制执行：` `modlens config set openai.structuredOutput true`
  > `这会把契约以 response_format: json_schema 的严格形式发过去，schema 由 modlens 校验用的那份推导而来，没有需要手工同步的副本。默认关闭，因为不支持这个字段的网关会直接 400。`
  > （`docs/output-schema.md`）`Never null: a model with nothing to say there often writes one, and modlens drops the key before the result reaches you, so reading an optional field means checking whether it is there, not whether it is null.`
  > （同文档）`layout.regions[].type is a free string, not a closed list. Region kinds are an open set: a fixed enum rejected link on any web screenshot and search on a portal, and a rejected result fails the whole read over a descriptive label. The field's schema description names the common vocabulary as guidance.`

- **根因**：服务端不强制 schema；弱模型只答一半；模型爱用 `null` 填“无可说”；把描述性字段做成枚举会因“多一个合法值”而整体失败。
- **怎么修**：① 可选开关让支持 `response_format: json_schema` 的网关硬校验（默认关，因为不支持的网关会 400）；② 可选字段读“在不在”而不是“是不是 null”，`null` 直接丢键；③ **描述型字段用自由字符串 + description 引导**，不要用闭集 enum；④ 校验失败时**报出具体字段名**（`wrong or missing: visual.notes`）。
- **给手册的教训**：**模型的 JSON 输出要靠 schema 强约束 + 容错解析**；报错要能指出“哪个字段不对”。

### modlens 其它 dsh 提交（仅标题，未展开）

`0f29110 fix(dsh): a route that gains native vision says so, and says what to do`（拒绝包装自带视觉的模型时要给出人话解释）、`8962f59 fix(dsh): name a wrapped route after its upstream, and cover two untested paths`、`bfd6bbf fix(dsh): render settings card before agent discovery`、`8e711b7 fix(dsh): bind discovery to llm lifecycle`、`7546a6a fix(dsh): reuse repeated path-tool image reads`（同一图片重复读取要复用缓存）、`04e6ed1 fix(dsh): exclude vision-named ids and see through vendor prefixes`、`9085be4 fix(dsh): failed reads hold their bytes; the shared cache spares open walks`、`b95a021 fix(dsh): close paste store lifecycle gaps`、`314070c fix(dsh): canonicalise the store's parent, and never guess a paste's size`、`eccc8d2 fix(dsh): verify the paste store before trusting it, and keep the ledger honest`、`a2bb742 fix(dsh): collect pasted files instead of keeping them forever (#51)`、`c49d062 fix(dsh): require proof of ownership, not a borrowed name (#36)`、`f0c0f1e fix(dsh): follow dsh's interface language on the settings card`、`3ca7d59 fix(dsh): localize the card's load/save failure fallbacks`。

---

## 1.4 yjh051108_dsh-routing-suite / `injector`（`@dsh-external/dsh-super-injector`）+ `graded`（`@dsh-external/dsh-graded-mode`）

这个仓库的 git 只有 72 个提交，但 `injector/CHANGELOG.md` 与 `docs/SPEC.md` 把**每一条踩坑都写成了规范**。
以下坑优先选取“工具 / schema / 生命周期 / 跨平台”方向。

### 坑 R1：`parameters` 的 `required` 写法 —— **两条注册路径规则相反，必须分清** ⚠️⚠️

> ## 🔴 重要校正（2026-09-11，由主线核对官方源码后加）
>
> 本节原标题写的是「`parameters` 属性级不能有 `required` 键」——**这个结论只对一半，直接照抄会写错**。
> 官方仓库 `deepseek-harness` 源码（commit `86a402200d`）实证：
>
> ```ts
> // packages/core/tools/src/schema.ts:571-572（defineTool 实现体内）
> const parameters = parameterSchemaSpecToJsonSchema(options.parameters)
> const outputSchema = valueSchemaSpecToJsonSchema(options.output.schema)
> ```
>
> ```ts
> // packages/core/tools/src/schema.ts:97-107
> /** One implicit parameter-root property, optionally required. */
> export type ParameterPropertySpec = ValueSchemaSpec & { required?: true }
>
> /**
>  * Tool parameter schema. The map itself is an implicit open object root;
>  * requiredness remains a per-property `required: true` annotation.
>  */
> export type ParameterSchemaSpec = {
>   [key: string]: ParameterPropertySpec
>   [key: symbol]: never
> }
> ```
>
> ```ts
> // packages/core/tools/src/schema.ts:291-304（属性级 required 的收集逻辑）
> if (task.kind === 'property') {
>   if (!isJsonSchemaRecord(task.property)) authorError(`${task.path} must be a value schema object`)
>   if (Object.hasOwn(task.property, 'required') && task.property.required !== true) {
>     authorError(`${task.path}.required must be true when present`)
>   }
>   if (Object.hasOwn(task.property, 'required') && task.property.required === true) task.required.push(task.key)
>   ...
> }
> ```
>
> ```ts
> // packages/core/tools/src/schema.ts:450-459（DSL → JSON Schema 的投影）
> export function parameterSchemaSpecToJsonSchema(spec: ParameterSchemaSpec): ParameterJsonSchema {
>   const compiled = compilePropertyMap(spec, 'parameters')
>   const schema: ParameterJsonSchema = {
>     type: 'object',
>     properties: compiled.properties,
>     ...(compiled.required === undefined ? {} : { required: compiled.required }),
>   }
>   assertSupportedJsonSchema(schema)
>   return schema
> }
> ```
>
> ### 结论：DSH 有**两条**写工具的参数路径，`required` 写法正好相反
>
> | 注册方式 | `parameters` 是什么 | 必填怎么写 | 写错的后果 |
> |---|---|---|---|
> | **`defineTool({...})`**（官方推荐，从 `@deepseek-ai/dsh-tools` 导入） | **DSH 作者 DSL**（`ParameterSchemaSpec`） | **属性级** `required: true` | 写对象级 `required: ['a']` → 报错 `parameters.a.required must be true when present` 或 `parameters.x is not supported by the value schema DSL` |
> | **裸 `ctx.tools.register({...})`** | **原始 JSON Schema**（`ToolDefinition.parameters`） | **对象级** `required: ['a']` | 写属性级 `required: true` → 被 `assertSupportedJsonSchema` 拒绝（`required must be an array of strings`） |
>
> 官方仓库自带的工具插件（如 `packages/interaction/tool-ask-user/src/index.ts`）**全部走 `defineTool`**，写法是**属性级**：
>
> ```ts
>     parameters: {
>       questions: {
>         type: 'array',
>         required: true,          // ← 属性级，DSH DSL 正确写法
>         description: 'Questions to ask the user before continuing.',
>         items: {
>           type: 'object',
>           additionalProperties: true,
>           properties: {
>             id: { type: 'string', required: true, description: '...' },
>             ...
> ```
>
> **`output.schema` 同理**：走 `defineTool` 时也是 DSH DSL，用**属性级** `required: true`（官方 `tool-ask-user` 的 `output.schema.properties.answers` 就是 `required: true`）；且官方源码里 `output.schema` 的**根节点不允许 `required`**（`compileValueSchema` 以 `allowRequired: false` 起步，`schema.ts:427`）。
>
> **本笔记下方所有来自社区仓库的"对象级 `required` 数组"例子**，都是**裸 `register` + 原始 JSON Schema** 路径的写法 —— 它们本身没错，但**不能拿去填 `defineTool` 的 `parameters`**。
>
> **给手册的最终教训**：先明确你走哪条路（新手一律推荐 `defineTool`），再决定 `required` 写在哪一级。**不要混用**。
>
> ---
>
> 以下为 Agent 原始调研内容，**请带着上述校正阅读**。

### 原来的分析（保留原貌，结论已被上方校正）

- **来源**：`yjh051108_dsh-routing-suite + graded/src/tools.js:12-19` 文件头注释原文（原话“血泪坑,勿改”）：

- **来源**：`yjh051108_dsh-routing-suite + graded/src/tools.js:12-19` 文件头注释原文（原话“血泪坑,勿改”）：

  > ```
  > Schema 形态约束（血泪坑,勿改）：
  >   register() 用 assertSupportedJsonSchema 直查 output.schema 原文,发给模型的
  >   parameters 经服务端 JSON Schema 严格校验——全都只认标准 raw 形态：
  >   对象级 required 数组,属性级一律不允许 required 键。
  > ```

- **现象**：工具注册被拒（或模型侧校验失败）。
- **根因**：dsh 的工具注册器用 `assertSupportedJsonSchema` **直接读 `output.schema` 原文**；且 `parameters` 会被服务端按**标准 JSON Schema** 严格校验。它只接受“对象级 `required` 数组”，**属性节点里不允许出现 `required` 键**。
- **怎么修**：全部使用**标准 raw JSON Schema**：
  - ✅ 正确（源码里到处如此，`graded/src/tools.js:35-45`）：

    ```js
    const outputSpec = {
      schema: {
        type: 'object', additionalProperties: false, required: ['ok', 'text'],
        properties: {
          ok: { type: 'boolean' },
          text: { type: 'string' },
          warnings: { type: 'array', items: { type: 'string' }, description: '软约束提示（如概念超限），非错误' },
        },
      },
      render: (_args, value) => TEXT(value.text + (value.warnings?.length ? `\n（提示：${value.warnings.join('；')}）` : '')),
    }
    ```
  - ✅ 嵌套对象的 required 也一律放“对象级”（`graded/src/tools.js:48-59` 的 `groupItemSchema`）：

    ```js
    const groupItemSchema = {
      type: 'object', additionalProperties: false, required: ['title', 'spec', 'accept', 'do', 'verify'],
      properties: {
        title: { type: 'string', description: '小类名（纯名词短语,不要重复大类词）' },
        concepts: { type: 'array', items: { type: 'string' }, description: '...' },
        // ...
        mode: { type: 'string', enum: ['correct', 'experience', 'research'], description: '...' },
      },
    }
    ```
  - ⚠️ **反例（不要抄）**：`injector/src/index.ts` 的骨架模板里出现过属性级 `required`（`injector/src/index.ts:176-178`）：

    ```ts
    parameters: {
      name: { type: 'string', required: true, description: '谁' },
    },
    ```
    这与 `tools.js` 文件头“属性级一律不允许 required 键”的结论**互相矛盾**；两处写法不同，说明该仓库自身也存在未统一的旧写法。**教学时以 `graded/src/tools.js` 的 `required` 数组写法为准**（更严格、且是该仓库“血泪坑”注释点名的那种）。
- **给手册的教训**：工具 schema 是**发给模型的严格 JSON Schema**，不是 TypeScript 类型。`required` 只写在对象节点上、值是字符串数组；属性节点里不要写 `required: true`。

### 坑 R2：资源“裸注册”（未挂 `ctx.effect`）→ 热重载报 `duplicate / already registered`

- **来源**：`yjh051108_dsh-routing-suite + injector/docs/SPEC.md` 规范 2.2 原文：

  > `**规范 2.2**：**所有资源注册挂 ctx.effect 即获得 dispose 自动清理**——这是 cordis 的契约。裸注册（绕过 effect）在 dispose 后残留（僵尸闭包根因）。注入器自身工具必须全部走 ctx.effect（已修），插件模板同样强制。`

  以及 `injector/CHANGELOG.md` [0.2.3]/[0.1.0] 的实测记录：

  > `**强制登记守卫**：reloadPackage 重建失败若报 duplicate / already registered → 判定未登记裸注册 → 明确报错（要求插件把资源注册挂 ctx.effect）+ 自动清理残留路由`

- **现象**：热重载后报 `duplicate` / `already registered`（如 `duplicate route`）；旧 fiber 的注册没被清掉。
- **根因**：插件用“裸注册”把工具/路由/监听挂上去，没挂 `ctx.effect` → dispose 后残留。
- **怎么修**：**一切注册都包在 `ctx.effect` 里**，并保留它返回的 disposer。`injector/src/index.ts:142-186` 的官方骨架（逐字）：

  ```ts
  export function apply(ctx: Context, config: Config): void {
    // 工具注册（ctx.effect：fiber dispose 自动注销）
    ctx.effect(() => ctx.tools.register(defineTool({
      name: '${pkgName.replace(/[^a-z0-9_]/gi, '_')}_hello',
      description: ${JSON.stringify(description || '示例工具')},
      parameters: {
        name: { type: 'string', required: true, description: '谁' },
      },
      output: {
        schema: { type: 'string' },
        render: (_args: unknown, value: unknown) => [{ type: 'text', text: String(value) }],
      },
      async execute(args: { name: string }) {
        return config.greeting + '，' + args.name + '！'
      },
    })), '${pkgName}: hello tool')
  ```
  `graded/src/index.js:358-367` 是“批量注册 + 显式 disposer”的更稳写法：

  ```js
  ctx.effect(() => {
    const disposers = []
    for (const def of [editPlanDefinition(deps), lockStageDefinition(deps), markTaskDefinition(deps), commitStarDefinition(), redteamVerdictDefinition(), reviseDoDefinition()]) {
      try {
        const d = ctx.tools.register(def)
        if (d) disposers.push(d)
      } catch (e) { console.warn('[graded] global tool register failed:', def.name, e?.message || e) }
    }
    return () => { for (const d of disposers) { try { d() } catch { /* 幂等 */ } } }
  }, 'graded-mode: global tools')
  ```
- **给手册的教训**：**注册必挂 `ctx.effect`**，否则热重载/卸载必留残留；注册多个工具时逐个 `try/catch`，一个坏工具不拖垮整组。

### 坑 R3：profile patch 顶层 `[]` + 盲目 append → YAML 双顶层值，解析必炸

- **来源**：`yjh051108_dsh-routing-suite + injector/docs/SPEC.md` 规范 3.1 与 `injector/src/index.ts:715-731` 注释原文：

  > `**规范 3.1**：**profile patch 永远是单一顶层数组**——`[]` 或 `- id:` 列表，**绝不混存**（双顶层值 = YAML 解析错误 = 装配全灭）。注入器写 patch 必须解析式追加（writePatch），这是配置方言的硬性契约。`
  > `官方 patch 初始是顶层 []（空数组）；盲 append "- id:" 会产生两个顶层 YAML 值 → 解析必炸。本函数：移除顶层 [] 再追加条目，保证文件始终单一顶层值（列表）。`

- **现象**：改过 patch 后 dsh 直接装配全灭（YAML 解析错误）。
- **根因**：官方生成的 patch 初值是顶层 `[]`；直接 append `- id: …` 就变成“数组 + 新条目”两个顶层值。
- **怎么修**：**解析式写入**——先扫描现有条目 id，去重、幂等，再移除顶层 `[]` 后追加。`injector/src/index.ts:731-762` 关键片段：

  ```ts
  function writePatch(appendText: string): boolean {
    // ...
    // 1. 收集 appendText 携带的 id
    const appendIds = [...appendText.matchAll(/^\s*- id:\s*([^\s#]+)/gm)].map((m) => m[1])
    // 2. 提取现有内容里所有条目块（含注释），按 id 归组
    const blocks = extractPatchBlocks(content)
    // ... 同 id 重复：只保留最后一条
    // 3. 幂等：appendIds 全部已存在 → 不写入
    if (appendIds.length > 0 && appendIds.every((id) => existing.has(id))) {
      return false
    }
    // 4. 重写：去重后的现有块 + 追加文本
    const cleanedTop = kept.join('').replace(/^\s*\[\]\s*$/m, '')
    writeFileSync(patchFile, cleanedTop + appendText, 'utf8')
    return true
  }
  ```
- **给手册的教训**：**别用字符串拼接改 YAML/JSON 配置文件**。要么整份解析后重新序列化，要么至少做 id 去重 + 顶层值归一。

### 坑 R4：`duplicate loader entry id` → 整个 plugin tree 加载失败（启动即崩），且插件无法自愈

> 🔴 **0.1.6-alpha.1 起本条的行为已变**：加载器改回**非事务化**后，重复 `id` **不再报这个错、也不再拦截** —— 同 id 两行互相覆盖（后者胜）。下面记录的 2026-09 事故是**当时版本的真实行为**，作为「为什么 id 必须全局唯一」的历史证据保留；**当前写法的判据以 `05-pitfalls.md` 坑 P3 为准。**

- **来源**：`yjh051108_dsh-routing-suite + injector/src/index.ts:721-730` 注释原文：

  > ```
  > ═══ 幂等去重（2026-08-15 别人机器 duplicate loader entry id 教训）═══
  > 手动 patch / 重复安装 / 多路径写入都可能让同 id entry 出现两次——dsh
  > loader 装配遇同 id 直接抛 `duplicate loader entry id`，整个 plugin tree
  > 加载失败（启动即崩），且注入器自身无法自愈（鸡生蛋）。因此：
  >  1. 写入前扫描现有条目 id；若 appendText 的 id 已存在 → 不追加（幂等）；
  >  2. 对历史重复：重写文件时按 id 去重（保留最后一条，注释块保留）；
  >  3. heal/self-test 等触碰 patch 的路径全部走这里，杜绝盲 append。
  > ```

- **现象**：dsh 启动即崩，报 `duplicate loader entry id`。
- **根因**：同一个 `id` 的 entry 在 profile patch 里出现两次（手动改 / 重复安装 / 多路径写入）。
- **怎么修**：**写入前按 id 幂等去重**（见 R3 的 `writePatch`）。
- **给手册的教训**：插件行的 `id` 是**主键**；任何自动写入 patch 的代码都要先查重。

### 坑 R5：`homedir()` ≠ 真实 DSH_HOME → junction 建到错误 profile，loader 找不到包

- **来源**：`yjh051108_dsh-routing-suite + injector/src/index.ts:572-575` 注释原文：

  > ```
  > ⚠️ DSH_HOME 优先（实测踩坑）：部署的 web 进程 homedir 可能与 DSH_HOME 指向
  > 不同用户（如服务账户/另一用户 profile），homedir() 推导的路径会全部错位——
  > junction 建到错误 profile、loader 找不到包。DSH_HOME 环境变量才是权威。
  > ```
  > `const dshHome = process.env.DSH_HOME || join(homedir(), '.dsh')`

  同一修复也写进了 `injector/CHANGELOG.md` [0.3.3]：`**DSH_HOME 优先（homedir 错家）**：web 进程 homedir 与 DSH_HOME 不一致时（如服务账户/跨用户部署），registry/profileNodeModules/日志全错位…`

- **现象**：注入的插件“找不到”；写到了别的用户目录。
- **根因**：`os.homedir()` 推出的 `~/.dsh` 与真实的 `DSH_HOME` 不一致。
- **怎么修**：`process.env.DSH_HOME || join(homedir(), '.dsh')`，一切路径都由它派生。
- **给手册的教训**：**存盘/配置路径永远以 `DSH_HOME` 为准**，别硬编码 `~/.dsh`。graded 里的 `stateFile` 也遵循同一规则（`graded/src/index.js:34-39`）。

### 坑 R6：junction 路径被 tsx 模块缓存命中的旧模块 → 重载“静默失败”

- **来源**：`yjh051108_dsh-routing-suite + injector/src/index.ts:916-919` 注释原文：

  > ```
  > ⚠️ 必须 import realpath URL 而非 junction URL（实测踩坑）：tsx 按 URL
  > 缓存模块，junction 路径变化（如自检 tmpDir 迁移）后 junction URL 仍
  > 命中旧模块缓存，loadCache 不产生新 key → 匹配仍失败。realpath URL
  > 是全新 key，强制重新解析磁盘并填充缓存。
  > ```
  > 以及 `injector/CHANGELOG.md` [0.3.3]：`reloadPackage 磁盘降级改 import realpath URL（junction URL 会被 tsx 旧缓存命中，tmpDir 迁移后重载失效——实测 uid 不变）`

- **现象**：改了源码、重载了，但生效的还是旧代码（uid 不变）。
- **根因**：模块缓存按 URL 命中；junction 路径不变 → 命中旧缓存。
- **怎么修**：import **realpath** URL。`injector/src/index.ts:920-925`：

  ```ts
  const realLib = realpathSync(libPath)
  await ctx.loader.import(pathToFileURL(realLib).href, () => [])
  const real = realLib.replace(/\/g, '/')
  for (const u of loadCache.keys()) {
    if (typeof u === 'string' && decodeURIComponent(u).includes(real)) { entryUrl = u; break }
  }
  ```
- **给手册的教训**：做热重载时，**模块缓存按路径字符串命中**；走 realpath，且别忘 `decodeURIComponent`（非 ASCII 目录）与 `\` → `/`。

### 坑 R7：Windows 自带脚本宿主读不了带非 ASCII 注释的脚本 → 需 UTF-8 BOM


- **来源**：`yjh051108_dsh-routing-suite + 3f1b02e`（2026-09-03）提交信息原文：
  `fix(install): UTF-8 BOM so Windows PowerShell 5.1 parses non-ASCII comments (#16) (#87)`
- **现象**：Windows 自带的 Windows PowerShell 5.1 执行 `install-injector.ps1` 直接报语法错误（注释里的中文/中文标点被按 GBK/ANSI 解码，吃掉了引号或行尾）。
- **根因**：PS 5.1 默认按本地代码页（简体中文 Windows 是 GBK）读 `.ps1`，文件本身是无 BOM 的 UTF-8 → 中文注释乱码，某些字节序列被解释成引号导致解析失败。
- **怎么修**：把 `.ps1` 存成 **UTF-8 with BOM**（BOM 三个字节 `EF BB BF` 告诉 PS 5.1 用 UTF-8 读）。
- **给手册的教训**：给 Windows 用户发脚本时，**`.ps1` 必须带 BOM 存 UTF-8**；`.sh` 反过来要**去掉 BOM**（见 R8）。一份仓库同时装两种控制台脚本时最易踩。

### 坑 R8：`.sh` 被 CRLF 检出 → `set: pipefail: invalid option name`

- **来源**：`yjh051108_dsh-routing-suite + 5145152`（2026-09-03）提交信息原文：
  `fix: pin .sh to LF — CRLF breaks bash on Windows (#27)`，正文：
  > ```
  > With core.autocrlf=true on Windows, .sh scripts check out with CRLF line
  > endings; bash then reads "set -euo pipefail\r" and fails with
  > "set: pipefail: invalid option name" (seen when running
  > `bash scripts/build.sh` inside injector/). The repo blobs are LF — the
  > breakage is on the checkout side. Add .gitattributes (*.sh text eol=lf)
  > so .sh files stay LF regardless of autocrlf.
  > ```
- **现象**：Windows 上 `bash scripts/build.sh` 报 `set: pipefail: invalid option name`。
- **根因**：`core.autocrlf=true` 把 `.sh` 检出了 CRLF，首行 `set -euo pipefail` 末尾带了 `\r`，bash 把 `pipefail\r` 当成一个非法选项名。
- **怎么修**：仓库根加 `.gitattributes`：
  ```
  *.sh text eol=lf
  ```
  （注意：**子模块是独立仓库，各自都要自己的 `.gitattributes`**。）
- **给手册的教训**：Windows 上开发跨平台脚本，**第一时间加 `.gitattributes`**：`.sh` 强制 LF、`.ps1` 保持 CRLF/BOM、`.ts/.js/.json` 一般 `text eol=lf`。

### 坑 R9：`isHealthyLink` 把 pnpm 安装的**真实包目录**当“坏链接”删掉

- **来源**：`yjh051108_dsh-routing-suite + 1aa12ad`（2026-09-03）提交信息原文：
  `fix(injector): isHealthyLink 误删真实包目录 + 设置页 React 渲染契约 (#65)`，正文：
  > ```
  > * fix(injector): treat real (non-link) dirs as healthy in isHealthyLink
  >
  > - dev_inject_plugin: pnpm 安装的真实包目录被判为"坏链接"，被 rmSync 后替换为
  >   自指 junction--一次注入毁掉一个正常安装的包（Windows 实测）
  > - autoRestore link 自愈扫描对真实目录做无谓删除尝试；registry 包悬空警告
  >   对所有真实目录误报刷屏
  > - 真实（非链接）路径是包管理器管理的安装实体，不应进入链接校验/删除重建
  >   分支：一律视为健康
  > ```
- **现象**：执行一次“注入插件”，一个**本来好好装在 `node_modules` 里的包**被删了，换成了一个自己指向自己的 junction（自指链接），包直接废掉。
- **根因**：健康检查函数把“不是符号链接的真实目录”误判为“需要修复的坏链接”，走了 `rmSync` + 重建 junction 的分支。
- **怎么修**：判“链接健康”前先分类型——**真实（非链接）目录一律视为健康**，不进删除/重建分支。
- **给手册的教训**：任何“自动修复/自愈”逻辑，删除动作前必须**先用 `lstatSync` 判断它到底是不是链接**；`existsSync` 会跟随链接、对真实目录与悬空链接给出相反答案（见 R21）。

### 坑 R10：设置页塞普通对象 → React #130 + 整页空白

- **来源**：`yjh051108_dsh-routing-suite + 1aa12ad`（2026-09-03）提交信息原文（同上），正文：
  > ```
  > * fix(injector): settings page must use React render contract
  >
  > - 宿主 ui-settings 的 settings.section 槽期望 React 渲染函数（dsh-market 同款
  >   契约 register(descriptor, () => createElement(...))）
  > - 原 component: () => ({ render() {...} }) 普通对象在宿主渲染时抛 React #130
  >   （slot entry crashed in 'settings.section'）-> 设置页整页空白
  > - DOM 构建逻辑不变，仅改为 React 容器渲染；label「插件」与官方插件页重名，
  >   改为「插件管理」
  > ```
- **现象**：插件装上后，DSH 设置页**整页空白**，控制台 `slot entry crashed in 'settings.section'` + `React #130`（`React #130` = 返回了非合法 React 元素）。
- **根因**：`settings.section` 槽的渲染契约要的是**返回 React 元素**的函数，而插件返回了一个带 `render()` 方法的普通对象（以为要自己管 DOM）。
- **怎么修**：`register(descriptor, () => createElement(...))`，返回 React 元素；不要返回 `{ render() {} }` 这种对象。
- **给手册的教训**：UI 槽 = **React 世界**。插件的 `component` 必须返回 React 元素（JSX/`createElement`），不是自己写的 DOM 渲染器。契约可对照官方 `dsh-market` 同款写法。

### 坑 R11：同毫秒事件被“水位线”比较判成同一条 → 少推进一拍

- **来源**：`yjh051108_dsh-routing-suite + 39ee0a0`（2026-09-03）提交信息原文：
  `fix(stage): event-index watermark prevents same-millisecond double advance (#73) — port to v1.20 + sync unaliased baseline (carries sessionEvents from #85) (#86)`
- **现象**：快速连续两步（同一毫秒内）时，第二步被当成“已经处理过”。事件索引水位用**时间戳**做唯一标识，同毫秒两条事件时间戳相同 → 第二条被判为重复，双推进丢失（或反向：重复推进）。
- **根因**：用 `Date.now()`（毫秒）当事件的唯一键；毫秒内可以产生两条事件。
- **怎么修**：水位改**事件序号/索引**（单调递增整数），不用时间戳。
- **给手册的教训**：**永远不要用时间戳当唯一标识/去重键**；用数组下标或事件自带的单调 id。

### 坑 R12：agent preset 接管工具清单后，`bash` 变 `unknown tool`（注册表不匹配）

- **来源**：`yjh051108_dsh-routing-suite + 7ddeec3`（2026-09-03）提交信息原文：
  `fix(assembly): add tool-bash-posix row — POSIX bash registry mismatch (#66)`，正文：
  > ```
  > Agent presets take over the tool manifest, so the host (dsh-base) tool-bash
  > never enters a preset session: the bash claimed by STAGES stage 3 (verification)
  > fails with 'unknown tool' on macOS/Linux. Register it in the preset manifest;
  > win32 keeps using the gitbash group row (platform-mutually-exclusive, never
  > double-registered).
  > ```
- **现象**：进入某个 agent preset 会话后，提示模型用 `bash`，但模型报 `unknown tool: bash`；macOS/Linux 必现，Windows 反而正常。
- **根因**：preset **接管工具清单**（manifest）后，宿主 `dsh-base` 的 `tool-bash` 不再进入该会话；而清单里只声明了 `win32` 的 gitbash 组行，POSIX 侧没有对应行。
- **怎么修**：在 preset manifest 里补一行 POSIX 的 `tool-bash-posix`；`win32` 继续用 gitbash 组行（两者平台互斥，不会重复注册）。
- **给手册的教训**：**工具注册表是分层的**（全局层 / preset 层），preset 会整体接管工具面。写插件假设“宿主一定有某工具”就会踩空；跨平台工具名可能不同（`tool-bash` vs `tool-bash-posix`）。

### 坑 R13：`npm ci` 因引用了**未发布的包**而失败 → 锁到正式版 + 显式声明

- **来源**：`yjh051108_dsh-routing-suite + e3f00b2`（2026-09-03）提交信息原文：
  `merge: #76 fix(injector) unpin unpublished dsh-type-meta so npm ci works`，正文：
  > ```
  > - INSTALL.md：自源码构建真实经验文档（--legacy-peer-deps/分叉包重链）
  > - package-lock：rc 钉版→已发布正式版（cordis 4.0.1/cosmokit 1.8.2/TS 5.9.3）+ cordis-plugin-loader 声明
  > - package.json：devDependencies 声明 cordis-plugin-loader（锁对齐）
  > ```
- **现象**：`npm ci` 直接失败——`package-lock.json` 里钉了一个**从未发布到 registry** 的包版本（`dsh-type-meta`）。
- **根因**：锁文件里写着 registry 上不存在的版本；`npm ci` 严格按锁文件装，装不到即失败。另外 `cordis-plugin-loader` 被 `package-lock` 引用却没在 `package.json` 声明，锁与清单不一致。
- **怎么修**：把 rc 钉版改成**已发布的正式版**；`package.json` 里**显式声明**所有被锁引用的包；自源码构建的真实经验（`--legacy-peer-deps`、分叉包重链）写进 INSTALL.md。
- **给手册的教训**：**`package-lock` 引用的每个包都必须在 `package.json` 里声明**，且版本必须在 registry 真实存在；RC/未发布版本不要写进锁文件。

### 坑 R14：打包前没有先构建根 git 依赖 → 产物缺依赖

- **来源**：`yjh051108_dsh-routing-suite + a0122f3`（2026-09-03）提交信息原文：
  `fix: build root git dependency before packing (#81)`
- **现象**：`npm pack` / 发布出来的包在目标机装不上或缺文件。
- **根因**：根依赖是从 git 拉的（`git+...`），**打包时它还没被构建**，产物不完整。
- **怎么修**：在 `prepack`/`prepare` 阶段**先构建根 git 依赖再打包**。
- **给手册的教训**：`files` 白名单 + `prepare` 构建顺序要对齐：**先 build、再 pack**，`prepare` 里做构建（`npm install` 时也会跑）。

### 坑 R15：`registry.plugin` 第三参传错 → `getOuterStack is not a function`

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.1.0] 修复段原文：
  > `getOuterStack is not a function`：`registry.plugin` 第三参必须是函数（`() => []`），双路径修正
- **现象**：插件加载时报 `getOuterStack is not a function`。
- **根因**：编程式注册插件时 `registry.plugin(plugin, config, ???)` 的**第三参必须是函数**（返回依赖/配置数组的工厂），传了数组或 undefined 就炸。
- **怎么修**：第三参传 `() => []`。
- **给手册的教训**：用 `loader.create` / `ctx.plugin` 做运行时注入时，**第三个参数是函数**：`() => []`。这是最隐蔽的签名坑之一。

### 坑 R16：Windows 装了 WSL 时，`bash` 探测抢先命中 WSL → 构建必挂

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.3.3] 修复段原文：
  > **findBash 拒绝 WSL**：Windows 装 WSL 时 `System32\bash.exe` 抢先 PATH 命中，构建必挂
  > （"适用于 Linux 的 Windows 子系统没有已安装的分发版"）。修复：Git/PortableGit 路径优先，
  > PATH 探测结果含 wsl 标记即拒绝
- **现象**：Windows 上一跑构建就报 `适用于 Linux 的 Windows 子系统没有已安装的分发版`。
- **根因**：`System32\bash.exe` 是 WSL 的入口，在 PATH 探测里抢先命中；WSL 没装发行版就报错。
- **怎么修**：**Git / PortableGit 的 `bash.exe` 路径优先**；PATH 探测结果里含 `wsl` 标记（或路径在 `System32` 下）就拒绝。
- **给手册的教训**：Windows 上找 `bash`，**别只信 PATH**——显式优先 `Git\bin\bash.exe` / `PortableGit`，并排除 `System32\bash.exe`。

### 坑 R17：patch 块重写“粘连” → 顶格注释错挂到上一条目

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.3.3] 修复段原文：
  > **writePatch/extractPatchBlocks 粘连 bug（patch 串位）**：条目块后的顶格注释被并入前一块，
  > 块间重写无换行 → 注释与下一 `- id:` 粘连成一行，`disabled: true` 错挂上一条目（实测：
  > 卸载自检插件后注入器行被禁用）。修复：每块保留行尾换行、顶格注释单独成块，块间 join 不再粘连
- **现象**：卸载某个插件后，**另一个不相干的插件行被 `disabled: true` 禁用了**（自检插件被卸载 → 注入器自己那行被禁掉，注入器死了）。
- **根因**：patch 文本被切成“块”再重写时，块与块 join 没有换行；上一块末尾的顶格注释和下一块的 `- id:` 粘成一行 → 把 `disabled: true` 挂到了错误的条目上。
- **怎么修**：每块**保留行尾换行**；顶格注释**单独成块**；块间 `join` 时确保不粘连。
- **给手册的教训**：程序化改写 YAML 时，**别用字符串拼接切块**；要么用 YAML 解析器，要么每块严格带换行、注释独立成块。这坑一次就毁掉一个插件的启用状态。

### 坑 R18：官方装配不装 peers → `Cannot find package '@deepseek-ai/dsh-tools'`

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.3.3] 修复段原文：
  > **宿主自包含打包（issue #1 根治）**：tsdown 新增 host bundle，把 `@deepseek-ai/dsh-tools` /
  > schemastery 等运行时依赖打进 `lib/index.js`——官方装配（`dsh plugin add <目录>`，link: 依赖
  > 不装 peers）不再出现 `Cannot find package '@deepseek-ai/dsh-tools'`，任何装配路径均可加载
- **现象**：用官方 `dsh plugin add <目录>` 装插件，启动报 `Cannot find package '@deepseek-ai/dsh-tools'`。
- **根因**：插件把宿主包写在 `peerDependencies` 里，以为装配时装——但官方装配对 `link:` 依赖**不装 peers**，`node_modules` 里没有 `@deepseek-ai/dsh-tools`。
- **怎么修**：用 **tsdown/bundler 把运行时依赖打进产物**（host bundle），做到“自包含”，任何装配路径都能加载。
- **给手册的教训**：插件发布给新手时，**要么把宿主依赖打进 bundle，要么确保装配器会装 peers**；否则“我本地能跑，用户装了报 Cannot find package”。这与 WeKnora 的“零运行时依赖 + 结构化类型镜像”（见模板一）是同一问题的两种解法。

### 坑 R19：staging 工具转正后 `demote` 注销不掉 → 残留

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.1.1] 修复段原文：
  > `dev_stage_demote` 无法注销已转正工具：`dev_stage_promote` 注册改挂 `ctx.effect` 并保存 disposer，demote 时真正从正式工具集注销（此前只删 staging 条目，正式注册残留）
- **现象**：把工具“转正”后又撤回，工具仍留在正式工具集里，撤不掉。
- **根因**：转正注册没挂 `ctx.effect`、没保存 disposer，demote 时只删了 staging 记录，正式注册还留着。
- **怎么修**：转正注册改挂 `ctx.effect` 拿 disposer，demote 时调 disposer 真正注销。
- **给手册的教训**：**任何注册都要拿 disposer**（`ctx.effect(() => ctx.tools.register(...))` 的返回值就是注销函数）；删除逻辑必须真调用它。这是“注册成对”的纪律。

### 坑 R20：清单文件被半截写入毒化自动恢复 → 原子写（tmp + rename）

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.1.1] 修复段原文：
  > registry 原子写（tmp + rename）：中断不残留半截 JSON 毒化自动恢复
- **现象**：进程被杀在写清单中途，留下半截 JSON → 下次启动“自动恢复”读到坏 JSON 直接崩。
- **根因**：直接 `writeFileSync` 目标文件，写一半中断就损坏。
- **怎么修**：**先写临时文件（`.tmp`）再 `renameSync` 覆盖**（同目录 rename 原子）。
- **给手册的教训**：任何要“下次启动还能读”的 JSON/状态文件，都用 **tmp + rename** 原子写。

### 坑 R21：悬空 junction 用 `existsSync` 判存在返回 false → symlink EEXIST

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.2.2] 修复段原文：
  > 注入 junction 悬空重建：`existsSync` 对悬空 junction 返回 false（跟随目标）导致 symlink EEXIST——改 `lstatSync` 判断链接存在 + `rmSync` 删除重建
- **现象**：重建一个**目标已消失的 junction** 时，报 `EEXIST`（说文件已存在），但代码以为它不存在。
- **根因**：`existsSync` 会**跟随链接**；链接指向的目标没了，它就返回 `false`，于是代码走“创建”分支 → 撞上那个实际仍存在的链接 → `EEXIST`。
- **怎么修**：用 **`lstatSync`** 判断“链接本身”是否存在（不跟随），存在就 `rmSync` 删掉再建。
- **给手册的教训**：判断“链接/悬空链接是否存在”一律用 **`lstatSync`**（`existsSync` 跟随链接，答案会误导你）。与 R9 是同一根因的两面。

### 坑 R22：热重载“静默失效”——缓存丢失后自我恢复

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.2.3] 修复段原文：
  > **自重载链路断裂根治（P0）**：缓存无匹配不再 INFO 退出——降级从磁盘 URL 直接加载（junction/urlMatch 目录的 lib/index.js），`loader.import` 重新解析磁盘填充缓存后继续重载流程。此前缓存丢失（并行 build/自检交错 purge）会让自重载/热重载直接失效，只能人工 touch/重启；现链路自愈（实测：清空缓存 → 自重载直接从磁盘加载成功，审计 `cache-miss-healed`）
- **现象**：热重载/自重载**无声失效**——看着“成功”了，其实没重载；只能手动 touch 或重启。
- **根因**：缓存里找不到匹配项就 INFO 退出；而并行 build/自检会把缓存清掉（purge），于是匹配不到。
- **怎么修**：缓存无匹配时**降级为从磁盘 URL 直接 import**（`loader.import` 会重新解析磁盘、填充缓存），再继续重载流程；并打审计 `cache-miss-healed`。
- **给手册的教训**：热重载逻辑必须处理“**缓存 miss**”分支；**别在 catch/miss 路径静默 return**，否则表现为“重载没反应”。

### 坑 R23：坏 client 插件把整个 HARNESS 拖下水 → `Failed to load plugins`

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.3.1] 修复段原文：
  > **autoRestore 恢复前 client 校验**：坏 client 插件（缺 inject）恢复时**跳过 + 审计**（此前恢复路径无校验——坏插件在 registry → 新会话启动 → client apply 失败 → 整个 HARNESS "Failed to load plugins"——用户被迫手动修）
  > **校验正则兼容单双引号**：用户手修的双引号 `inject = ["slots"]` 被误判为"缺 inject"的 bug
- **现象**：一个新会话一启动，整个 Harness 报 `Failed to load plugins`，全盘不可用，用户只能手动去删坏插件。
- **根因**：坏 client 插件（`client` 部分缺 `export const inject`）在 registry 里，新会话启动时它的 client `apply` 失败 → 整个插件加载失败。
- **怎么修**：**恢复/注入前对 client 骨架做校验**（检查编译产物 `lib/client.js` + 是否声明 `inject`），不合格就**跳过 + 审计**而非硬上；校验正则要兼容单引号 `inject = ['slots']` 与双引号 `inject = ["slots"]`。
- **给手册的教训**：**client 插件用了 `ctx.slots` 就必须 `export const inject = ['slots']`**，否则 `cannot get property 'slots' without inject`，严重时拖垮整个 Harness。自动恢复类逻辑一定要“先校验后执行”。

### 坑 R24：卸载“无匹配”的统计口径 → 假失败刷屏

- **来源**：`yjh051108_dsh-routing-suite + injector/CHANGELOG.md` [0.2.3] 修复段原文：
  > **uninject 统计口径（压测②）**：无匹配 = no-op 幂等，既不计 ✓ 也不计 ✗（此前：早期计 ✗ 产生 9✗ 假失败；后改计 ✓ 高估成功）
- **现象**：卸载一个本来就没装的插件，本该无操作，但统计里刷出 9 个 ✗（假失败），吓到用户。
- **根因**：幂等 no-op 被计成“失败”。
- **怎么修**：no-op 归为幂等，**既不计成功也不计失败**。
- **给手册的教训**：日志/统计里 **no-op 与 failure 要分开**，否则“本该静默的幂等操作”会制造一堆假错误。

### 坑 R25：同一引导被反复注入“淤积”

- **来源**：`yjh051108_dsh-routing-suite + graded/CHANGELOG.md` [0.0.1-rc1] 原文：
  > 注入淤积根治：focus 幂等键去 status（状态抖动不再重注同名引导）；执行端续轮 followup→steer + 同 turn 60ms 引导合并（消除 next-turn 堆积）
- **现象**：同一段引导在会话里越堆越多（next-turn 堆积），模型被重复提示干扰。
- **根因**：幂等键里带了易变的 `status`，状态一抖动就被判为“新的引导”而重注；续轮用 followup 又制造新堆积。
- **怎么修**：幂等键**不含易变 status**；同 turn 内的引导**合并（60ms 窗口）**；续轮语义从 followup 改 steer。
- **给手册的教训**：往会话里注入文本时，**幂等键只用稳定字段**；同一轮多次触发要**去抖合并**。

### 坑 R26：设置写与读路径不一致 → 设置“改了不生效”

- **来源**：`yjh051108_dsh-routing-suite + graded/CHANGELOG.md` [0.0.1-rc1] 原文：
  > 概念上限动态化：loadConceptLimit 读路径对齐设置 API（此前写读不一致致设置失效）——phaseL2/焦点注入/schema 描述全随设置（实测 8 全链断言）
- **现象**：用户在设置面板改了数值，实际行为不变（设置像没保存）。
- **根因**：**写入走一个路径，读取走另一个路径**，两边对不上。
- **怎么修**：读写共用同一 API/同一路径，并加“全链断言”测试（从设置写入一直验到注入与 schema 描述）。
- **给手册的教训**：设置项的**写与读必须同一来源**；给“设置生效”写一条端到端断言测试，否则这类 bug 极难发现。

### 坑 R27：设置面板闪退 → effect 一次挂载 + 回调 ref 化

- **来源**：`yjh051108_dsh-routing-suite + graded/CHANGELOG.md` [0.0.1-rc1] 原文：
  > **设置面板闪退修复**（effect 一次挂载+回调 ref 化）
- **现象**：一打开设置面板就闪退/白屏。
- **根因**：effect 反复挂载、回调闭包捕获了旧值（stale closure），重渲染时崩。
- **怎么修**：**effect 只挂载一次**（空依赖数组），**回调 ref 化**（用 ref 持有最新回调，避免闭包捕获旧值）。
- **给手册的教训**：React 面板里，**副作用 effect 用空依赖只挂一次**，事件回调**用 ref 存最新函数**，避免 stale closure 导致的闪退。

### 坑 R28：agent preset 的 persona `complete: true` 会丢弃其它 system prompt 贡献

（与 O1 同类，此处补充 routing-suite 侧证据）

- **来源**：`yjh051108_dsh-routing-suite + docs/SPEC.md` 关于 `system-prompt/assemble` 的「性能引导契约」段（[0.3.2] 新增第 6 节）：Waterfall 必须 `await next()`、`agent` 判空、晋升从持久日志推导、只裁剪本插件工具。
- **现象**：插件往 system prompt 里加了引导，但在某些 preset 会话里**完全不出现**。
- **根因**：persona 的 `complete: true` 表示“本 persona 独占 system prompt”，会**静默丢弃**其它贡献者。
- **怎么修**：插件侧无法强制，只能**用 `system-prompt/assemble` waterfall 观察实际产出**；文档层提醒“别对 `complete:true` persona 期望自己的 system prompt 生效”。
- **给手册的教训**：system prompt 有“独占 persona”概念；插件加 system prompt 后**要实测是否被吞**，别假设一定生效。

---

# B · 二、可抄代码模板

> 说明：以下代码**逐字照抄**自各仓库源码快照，路径为快照绝对路径。给新手时可直接复制。
> 四个模板按“从最简单到最复杂”排序：**模板一 = 只读工具插件（推荐新手第一个照抄）** → 模板二 = 有状态服务插件 → 模板三 = UI + bundle 双声明 → 模板四 = 运行时注入器（高级）。

## 模板一：WeKnora 只读工具插件（最干净的 `defineTool` 范本）

- **快照路径**：生成期素材 `Tencent_WeKnora/packages/dsh-weknora/`（不随本 skill 发布，见 `11-glossary-and-provenance.md` §A.2）
- **为什么适合新手**：**零运行时依赖**（`dependencies` 都不需要）、不碰 UI、不写 patch 复杂结构，4 个工具全是纯只读 HTTP 调用；类型用“结构化镜像”自包含，不 import 宿主内部包，**升级 DSH 不用改代码**。
- **目录树**（实际快照文件）：

  ```
  packages/dsh-weknora/
  ├── package.json          # dsh.bundle 声明 + 零 runtime 依赖（见下）
  ├── cordis.patch.yml      # bundle 装配补丁（把本插件插入 loader）
  ├── README.md             # 英文说明（含 Compatibility 段）
  ├── README_CN.md
  ├── src/
  │   ├── index.ts          # 插件入口：name / inject / apply（63 行量级）
  │   ├── tools.ts          # 4 个工具定义（563 行，最全的 defineTool 范本）
  │   ├── client.ts         # REST 客户端 + SSE 解析（433 行）
  │   ├── config.ts         # 手写 resolveConfig()（192 行）
  │   ├── harness.ts        # 结构化类型镜像（63 行，不依赖宿主包）
  │   └── render.ts         # 工具输出的文本渲染辅助（25 行）
  ├── test/
  │   └── fixtures/api-contract.json
  └── tsconfig.build.json / tsconfig.json
  ```

- **package.json 全文（逐字照抄）**：

  ```json
  {
    "name": "@wxg-prc-cpg/dsh-weknora",
    "version": "0.1.0",
    "publishConfig": {
      "access": "public",
      "registry": "https://registry.npmjs.org/"
    },
    "description": "WeKnora knowledge retrieval tools for DeepSeek Harness (dsh): semantic search, document reading and RAG/agent answers over your own knowledge bases.",
    "keywords": [
      "dsh",
      "dsh-plugin",
      "deepseek-harness",
      "cordis",
      "weknora",
      "rag",
      "retrieval",
      "knowledge-base"
    ],
    "license": "MIT",
    "author": "WeKnora",
    "homepage": "https://github.com/Tencent/WeKnora/tree/main/packages/dsh-weknora",
    "repository": {
      "type": "git",
      "url": "git+https://github.com/Tencent/WeKnora.git",
      "directory": "packages/dsh-weknora"
    },
    "bugs": {
      "url": "https://github.com/Tencent/WeKnora/issues"
    },
    "type": "module",
    "main": "./dist/index.js",
    "types": "./dist/index.d.ts",
    "exports": {
      ".": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "./package.json": "./package.json"
    },
    "files": [
      "dist",
      "cordis.patch.yml",
      "README.md",
      "README_CN.md"
    ],
    "engines": {
      "node": ">=20.11"
    },
    "scripts": {
      "build": "tsc -p tsconfig.build.json",
      "prepare": "npm run build",
      "typecheck": "tsc -p tsconfig.json --noEmit",
      "test": "npm run build && node --test \"test/*.test.mjs\"",
      "e2e": "node test/e2e/run-in-dsh.mjs"
    },
    "dsh": {
      "bundle": {
        "patch": "./cordis.patch.yml"
      }
    },
    "devDependencies": {
      "@types/node": "^22.13.0",
      "typescript": "^5.7.3"
    }
  }
  ```
  **逐字要点（新手必看）**：① `"type": "module"` 必须有；② `exports` 里 `types` 与 `default` 都要指到编译产物；③ `files` 白名单必须包含 `cordis.patch.yml`（否则发布后没有装配补丁）；④ `dsh.bundle.patch` 指向 patch 文件；⑤ **这里没有 `dependencies`**——因为它把宿主类型做成了本地镜像（见 `harness.ts`）。

- **插件入口 `src/index.ts` 全文（逐字照抄，新手抄这个骨架）**：

  ```ts
  /**
   * dsh-weknora: a DeepSeek Harness plugin that gives the agent retrieval,
   * document reading and composed answers from a WeKnora knowledge base.
   * @module dsh-weknora
   */

  import { WeknoraClient } from './client.ts'
  import { resolveConfig } from './config.ts'
  import type { HarnessContext } from './harness.ts'
  import { createTools } from './tools.ts'

  export const name = 'dsh-weknora'

  /** Cordis waits for the tool registry before applying this plugin. */
  export const inject = ['tools'] as const

  export type { Config } from './config.ts'
  export { ConfigError, normalizeBaseUrl, resolveConfig } from './config.ts'
  export { WeknoraApiError, WeknoraClient } from './client.ts'
  export { createTools } from './tools.ts'

  /**
   * Register the configured tools. Each registration is an effect, so unloading
   * or reconfiguring the plugin withdraws the tools without a restart.
   * @param ctx - the Cordis context, with `ctx.tools` injected.
   * @param config - the plugin's `config` row; validated here so a typo fails the load.
   */
  export function apply(ctx: HarnessContext, config: unknown): void {
    const resolved = resolveConfig(config as never)
    const client = new WeknoraClient(resolved)
    const registered: string[] = []
    for (const definition of createTools(client, resolved)) {
      ctx.tools.register(definition)
      registered.push(definition.name)
    }
    ctx.logger?.info(`dsh-weknora: registered ${registered.join(', ')} against ${resolved.baseUrl}`)
  }
  ```
  **要点**：`name` / `inject` / `apply` **三个具名导出**（没有 `export default`）；配置在 `apply` 里先 `resolveConfig` 校验，**拼错立刻加载失败**（比运行到一半才报错好）。

- **`src/harness.ts` 全文（逐字照抄）——这是“不依赖宿主包”的关键**：

  ```ts
  /**
   * Structural types for the slice of the DeepSeek Harness contract this plugin
   * uses. Declaring them here keeps the package free of runtime dependencies on
   * harness internals: the shipped code only ever hands `ctx.tools.register()` a
   * plain object, so a harness release that adds optional definition fields does
   * not require a republish of this plugin.
   *
   * The shapes mirror `@deepseek-ai/dsh-tools` (`ToolDefinition`) and
   * `@deepseek-ai/dsh-llm` (`ContentBlock`, `ToolSchema`) as of dsh 0.1.0-rc.8.
   */

  /** Supported subset of JSON Schema that the harness tool registry accepts. */
  export interface JsonSchemaNode {
    type?: 'object' | 'array' | 'string' | 'number' | 'integer' | 'boolean' | 'null'
    properties?: Record<string, JsonSchemaNode>
    required?: string[]
    additionalProperties?: boolean
    items?: JsonSchemaNode
    enum?: (string | number | boolean | null)[]
    const?: string | number | boolean | null
    description?: string
    title?: string
  }

  /** Model-facing content block returned by `output.render`. */
  export interface TextContentBlock {
    type: 'text'
    text: string
  }

  /** Execution context handed to a tool body. */
  export interface ToolRunContext {
    readonly signal: AbortSignal
  }

  /** One registered model-facing tool. */
  export interface ToolDefinition {
    readonly name: string
    readonly description: string
    readonly parameters: JsonSchemaNode
    readonly output: {
      readonly schema: JsonSchemaNode
      render(args: unknown, value: unknown): TextContentBlock[]
    }
    execute(args: unknown, exec: ToolRunContext): Promise<unknown>
    readonly timeoutMs?: number
    isConcurrencySafe?(args: unknown): boolean
  }

  /** The `ctx.tools` service seam. */
  export interface ToolRegistry {
    register(definition: ToolDefinition): () => void
  }

  /** The slice of the Cordis context this plugin injects. */
  export interface HarnessContext {
    readonly tools: ToolRegistry
    readonly logger?: {
      info(...args: unknown[]): void
      warn(...args: unknown[]): void
    }
  }
  ```
  **给新手的说明**：这段不是“抄 DSH 内部”，而是**手写一份自己用到的接口**。好处：插件不 `import` 宿主包 → 不会有 R18 的 `Cannot find package`，也不用随 DSH 升级重新发布。**代价**：类型是“结构性的”，DSH 大改字段时不会报错，要靠 e2e 测试兜底。

- **最小工具范本：`list_knowledge_bases` 全文（逐字照抄，约 52 行，新手第一个工具就抄它）**
  出处：`.../dsh-weknora/src/tools.ts` 第 188–243 行。

  ```ts
  definitions.push({
    name: name('list_knowledge_bases'),
    description: 'List the WeKnora knowledge bases this deployment can retrieve from, with their ids. '
      + `${name('search')} already spans them all, so reach for this only to report what is available or to `
      + 'narrow a later search to one of them.',
    parameters: { type: 'object', properties: {}, additionalProperties: false },
    timeoutMs: config.requestTimeoutMs,
    isConcurrencySafe: () => true,
    output: {
      schema: {
        type: 'object',
        properties: {
          count: { type: 'integer' },
          knowledge_bases: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                name: { type: 'string' },
                description: { type: 'string' },
              },
              required: ['id', 'name', 'description'],
              additionalProperties: false,
            },
          },
        },
        required: ['count', 'knowledge_bases'],
        additionalProperties: false,
      },
      render: (_args, value) => {
        const result = value as KnowledgeBasesValue
        if (result.count === 0) return text('No knowledge base is available to this WeKnora credential.')
        const lines = result.knowledge_bases.map(kb => {
          const description = kb.description === '' ? '' : ` — ${kb.name} (id: ${kb.id})${description}`
          return `- ${kb.name} (id: ${kb.id})${description}`
        })
        return text(`${result.count} knowledge base(s):\n${lines.join('\n')}`)
      },
    },
    async execute(_args, exec): Promise<KnowledgeBasesValue> {
      const bases = await client.listKnowledgeBases(exec.signal)
      return {
        count: bases.length,
        knowledge_bases: bases.map(kb => ({
          id: typeof kb.id === 'string' ? kb.id : '',
          name: typeof kb.name === 'string' ? kb.name : '',
          description: typeof kb.description === 'string' ? kb.description : '',
        })),
      }
    },
  })
  ```
  **逐字要点**：① `parameters` 是标准 JSON Schema，对象级 `required` 数组；这里无参就写 `{ type: 'object', properties: {}, additionalProperties: false }`；② **`output.schema` 必须描述返回值结构**（模型看到的是它），`render` 把它变成给人/模型看的文本块；③ `execute` 只返回**纯数据**，把 `unknown` 逐字段收窄（`typeof x === 'string' ? x : ''`），保证输出是可序列化 JSON；④ `isConcurrencySafe: () => true` 表示只读、可并发。

## 模板二：有状态服务型插件（官方 `persona`，**MIT**）

> 🔴 **2026-09-16 来源政策收紧**：本模板原以一份社区记忆服务插件（**AGPL-3.0**）为载体，该来源**已移出本技能的引用集合** —— 其目录树与结构表整体删除。改用**官方一手范本**替代：更短、更权威，且是 MIT，可直接照抄。

**为什么用官方 `persona` 当范本**：它把**服务型插件的四要素**（声明依赖的服务 → 发布自己的服务 → 副作用回收 → 配置 schema）压在一份 75 行的文件里，且每一行都可照抄。出处是 DSH 自己，**不存在「版本对不上」的问题**。

- **快照路径**：官方仓库内 `packages/preset/persona/`（只读参考源，不随本 skill 发布）
- **插件形态**：TypeScript 源码（官方包，构建后发布）。若要**零构建**形态，见模板一。

### 服务型插件的通用骨架（**自撰归纳**，API 名以 `08-cheatsheet.md` 为准）

| 要素 | 服务型插件通常要做的事 |
|---|---|
| 插件形态 | 函数式三件套：`export const name` / `export const inject = [...]` / `export function apply(ctx, config)` |
| 暴露服务 | `ctx.provide('服务名', 值)` → 其它插件用 `ctx.get('服务名')` 取到 |
| 资源回收 | 每个需回收的资源挂 `ctx.effect(() => () => dispose(), "标签")`；**第二个参数是给人看的标签**，dispose 时能对上是哪一项 |
| 会话级生命周期 | 在会话开始事件里再挂一次 `ctx.effect(…)`，把回收绑定到**会话作用域**而非插件作用域 |
| 消息注入 | `ctx.on("agent/pre-step", …, { prepend: true })`，先 `await next()` 再追加（原理见坑 O1） |
| 事件捕获 | 监听会话事件与会话 flush 事件两条路径 |
| 工具前置守卫 | `ctx.on("tools/pre-execute", …)` |
| 长的子模块挂载 | **故意不 `await`** —— 阻塞式挂载会卡住它之后的所有注册 |

### 服务型插件通用的 `package.json` 字段（**DSH 官方约定**）

| 字段 | 值 / 要点 |
|---|---|
| `name` / `version` / `type` | 包名；语义化版本；`"module"`（ESM） |
| `main` / `exports` | 入口指向构建产物；`exports` 至少给出 `"."` |
| `dsh.bundle.patch` | **指向 `cordis.patch.yml`** —— 这是 `dsh plugin add` 能识别的关键声明 |
| `scripts.check` / `test` / `prepublishOnly` | 语法自检（`node --check`）+ 单测 + 发布前串联 |
| `scripts.check:version` | **断言代码里的版本常量与 `package.json` 的 `version` 一致**，防「改了代码忘改版本」 |
| `peerDependencies` | 写**区间**（如 `>=0.1.0-rc.6 <0.2.0`），不要钉死某个 rc 号 |
| `engines.dsh` | **可选，但语义很强**（`0.2.1-alpha.4` 起）：**声明了它就只有它决定兼容性** —— DSH peer 范围**不再**放宽或收窄它；写 `workspace:` 判**不兼容**；`engines` 非对象或 `engines.dsh` 非字符串 → 兼容性检查读不出清单 → **该包被拒绝（装不上）**。要么给完整范围，要么不写 |
| `engines.node` | 与宿主一致的 Node 范围 |

> 权威出处见 `07-conventions.md` 与官方包模板；本表只是导航，判据以官方 `package.json` 为准。

- **想要「官方 + 最小 + 可直接抄」的服务型插件范本，看这个（MIT）**：`packages/preset/persona/src/index.ts`（全 75 行）。
  它把**服务型插件的四要素**压到最小，且每一行都可照抄：

  ```ts
  // 出处：官方 deepseek-harness packages/preset/persona/src/index.ts（MIT），节选
  export const name = 'persona'

  /** 声明依赖的服务：Cordis 会等它就绪后再调用 apply。 */
  export const inject = ['systemPrompt']

  /** 配置的静态类型 + 运行时 schema（schemastery）；default 写在 schema 上。 */
  export interface Config {
    prefix: string
    suffix?: string
    complete?: boolean
    includeRuntimeContext?: boolean
  }
  export const Config: z<Config> = z.object({
    prefix: z.string().required(),
    suffix: z.string().default(''),
    complete: z.boolean().default(false),
    includeRuntimeContext: z.boolean().default(true),
  })

  export function apply(ctx: Context, config: Config): void {
    // 资源注册挂在 ctx.effect 下：返回值即 disposer，卸载时自动撤销。
    // 第二个参数是标签 —— dispose 时能对上是哪一项。
    ctx.effect(() => ctx.systemPrompt.section({
      name: PERSONA_PREFIX_SECTION,
      order: ctx.systemPrompt.getSectionOrder('DEPLOYMENT_PERSONA_PREFIX'),
      text: config.prefix,
      ...(config.complete ? { complete: true } : {}),   // ← 坑 O1 的机制源头
    }), 'persona.section()')
    if (!(config.includeRuntimeContext ?? true)) ctx.systemPrompt.suppressRuntimeContext()
  }
  ```

  **为什么它是最佳范本**：`name` / `inject` / `Config`（类型 + 运行时 schema）/ `apply` 四件套齐全（75 行）；
  `ctx.effect` 的**带标签写法**正是模板二要点②想教的；`complete` 字段就是坑 O1 的机制源头；且这是**官方一手代码**，永远与基线同源。

## 模板三：modlens 插件（`dsh.bundle` + `dsh.client` 双声明）

- **快照路径**：生成期素材 `liustack_modlens/`（不随本 skill 发布）
- **为什么值得看**：它是**“既有命令行、又有 DSH 插件、还有前端 UI 面板”**的复杂项目；`dsh` 字段**同时声明 bundle 与 client**；插件代码放在 `dsh/` 子目录、用 `exports` 映射，`bin` 仍是 CLI。
- **目录树（DSH 相关部分）**：

  ```
  liustack_modlens/
  ├── package.json          # dsh.bundle + dsh.client 双声明；exports 映射到 dsh/
  ├── cordis.patch.yml      # 插入 modlens 行
  ├── dsh/
  │   ├── index.js          # 插件主逻辑（后端，2199 行）
  │   ├── client.js         # 前端 UI 面板（51KB，client 入口）
  │   ├── vision-schema.json# 工具 output.schema（纯 JSON，见下）
  │   ├── spawnHidden.js    # Windows 隐藏子进程黑框（小而复用的范本）
  │   └── spawnHidden.d.ts
  ├── dist/                 # CLI 构建产物（bin 指向这里，与插件无关）
  ├── docs/
  │   └── troubleshooting.zh-CN.md   # 逐条报错排查（248 行）
  └── skills/modlens/       # 随插件分发的 skill
  ```

- **package.json 关键段（逐字照抄）**：
  ```json
  {
    "name": "@liustack/modlens",
    "version": "3.26.1",
    "type": "module",
    "bin": {
      "modlens": "./dist/main.js"
    },
    "files": [
      "dist",
      "docs",
      "skills/modlens/SKILL.md",
      "skills/modlens/scripts",
      "skills/modlens/references",
      "CHANGELOG.md",
      "SECURITY.md",
      "dsh",
      "cordis.patch.yml"
    ],
    "exports": {
      ".": "./dsh/index.js",
      "./dsh": "./dsh/index.js",
      "./package.json": "./package.json",
      "./client": "./dsh/client.js"
    },
    "dsh": {
      "bundle": {
        "patch": "./cordis.patch.yml"
      },
      "client": {
        "inject": [],
        "platform": "web",
        "immediately": true
      }
    }
  }
  ```
  **要点**：① `exports["."]` 指向插件入口 `./dsh/index.js`，`bin` 仍指向 CLI 的 `./dist/main.js`——**两种形态共存**；② `dsh.client.inject` 为空数组（本插件 UI 不依赖特定宿主服务），若用了 `ctx.slots` 必须写 `["@deepseek-ai/dsh-client-ui-slots"]` 之类（见 R23）；③ `platform: "web"`；④ `immediately: true` 表示 client 立即挂载。

- **`cordis.patch.yml` 全文（逐字照抄）**：
  ```yaml
  # dsh bundle layer: mount the modlens vision plugin (dsh/index.js via the
  # package root export; bin stays the CLI, nothing imports the root otherwise).
  - insert:
      - id: modlens
        name: '@liustack/modlens'
  ```
  **要点**：**顶层是单个数组**、`- insert:` 下再 `- id:`；entry 的 `id` 是主键（重复即崩，见 R4）；`name` 用 npm 包名，不用相对路径。

- **`dsh/spawnHidden.js` 全文（逐字照抄）——Windows “黑框”问题的通用小工具**：
  ```js
  // The only place this plugin starts a child process.
  //
  // The desktop app has no console of its own, so on Windows every child it
  // starts would be given one and shown its window: a black box per read
  // (issue #60). `windowsHide` suppresses that, defaults to false in Node, and is
  // ignored elsewhere.
  //
  // It lives in a file of its own, apart from its callers, so the rule can be
  // checked by looking at which files reach `child_process` at all rather than at
  // what each call passes. A call site cannot forget an option it never writes,
  // and writing the option after the caller's leaves nothing to override it.
  //
  // The core has its own copy in src/util/spawnHidden.ts. The duplication is on
  // purpose: this plugin ships as a unit and must not import from the CLI it
  // drives.
  import { spawn } from 'node:child_process'

  export function spawnHidden(command, args, options) {
    return spawn(command, args, { ...options, windowsHide: true })
  }
  ```
  **给手册的教训**：Windows 桌面上任何 `spawn`/`exec` 都要 `windowsHide: true`，否则**每次调用弹一个黑框**。把这件事**收进唯一一个函数**，别人就没法忘（见 M8）。

- **工具 `output.schema` 用独立 JSON 文件（逐字照抄一段）**：
  modlens 把输出的 JSON Schema 单独放 `dsh/vision-schema.json`，运行时读入。字段形态与 WeKnora 一致：对象级 `required` 数组、属性级只有 `type`/`description`/`items`/`properties`/`required`，**属性级不允许 `required: true`**（见 R1）。
  ```json
  {"type":"object","properties":{"summary":{"type":"string"},"ocr":{"type":"object","properties":{"full_text":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"text":{"type":"string"},"language":{"type":"string"}},"required":["text"]}}},"required":["full_text","lines"]}},"required":["summary","ocr"]}
  ```
  （上面为便于阅读截取了 `summary`/`ocr` 两段；完整文件在 `.../dsh/vision-schema.json`。）

## 模板四：routing-suite 运行时注入器（bundle + client + 事件拦截 + 运行时注入）

- **快照路径**：生成期素材 `yjh051108_dsh-routing-suite/injector/`（不随本 skill 发布）
- **为什么值得看**：这是**高级形态全家桶**——`bundle` + `client` 双声明、`ctx.webServer.register` 起 HTTP API、`ctx.on('llm/stream')` 拦截模型路由、`ctx.slots.inject` 挂 UI 面板、并用 `loader.create` **运行时注入其它插件**。
- **它自带的“教学模板”**：仓库里有个 `dev_scaffold_plugin` 工具，会**生成新手骨架代码**。下面是它生成的两个骨架（逐字照抄），可直接当新手模板。

- **injector 的 package.json 关键段（逐字照抄）**：
  ```json
  {
    "name": "@dsh-external/dsh-super-injector",
    "version": "0.3.3",
    "type": "module",
    "main": "./lib/index.js",
    "types": "./lib/types/index.d.ts",
    "exports": {
      ".": {
        "types": "./lib/types/index.d.ts",
        "default": "./lib/index.js"
      },
      "./client": {
        "types": "./lib/types/client/index.d.ts",
        "default": "./lib/client.js"
      },
      "./package.json": "./package.json"
    },
    "files": [
      "lib",
      "cordis.patch.yml",
      "scripts/build.sh",
      "scripts/fix-patch.mjs",
      "scripts/prepare.mjs"
    ],
    "dsh": {
      "bundle": {
        "patch": "./cordis.patch.yml"
      },
      "client": {
        "inject": [
          "@deepseek-ai/dsh-client-runtime",
          "@deepseek-ai/dsh-client-ui-slots"
        ],
        "platform": "web"
      }
    },
    "peerDependencies": {
      "@deepseek-ai/dsh-tools": ">=0.0.1-rc <2",
      "cordis": ">=4.0.0-rc <5",
      "schemastery": "^3.18.0"
    }
  }
  ```
  **要点**：① 有 client 时，`exports` 要额外暴露 `./client`（指向编译出来的 `lib/client.js`）；② `type` 的 `types` 指到 `lib/types/...`；③ `peerDependencies` 用**范围**（`>=0.0.1-rc <2`）而非钉死（见 R13）；④ `files` 要带上构建脚本，否则从 tgz 装时没法构建。

- **生成器里的“工具包形态”骨架（逐字照抄，最短的完整插件）**：
  ```ts
  /**
   * ${pkgName} — 工具包形态（由 dev_scaffold_plugin 生成）。
   * 规范：资源注册必须挂 ctx.effect（热重载/卸载自动清理——注入器踩坑记录）。
   */
  import type { Context } from 'cordis'
  import { defineTool } from '@deepseek-ai/dsh-tools'
  import z from 'schemastery'

  export const name = ${JSON.stringify(pkgName)}
  export const inject = ['tools']

  export interface Config {
    greeting: string
  }

  export const Config = z.object({
    greeting: z.string().default('你好'),
  })

  export function apply(ctx: Context, config: Config): void {
    // 工具注册（ctx.effect：fiber dispose 自动注销）
    ctx.effect(() => ctx.tools.register(defineTool({
      name: '${pkgName}_hello',
      description: '示例工具',
      parameters: {
        name: { type: 'string', required: true, description: '谁' },
      },
      output: {
        schema: { type: 'string' },
        render: (_args, value) => [{ type: 'text', text: String(value) }],
      },
      async execute(args) {
        return config.greeting + '，' + args.name + '！'
      },
    })), '${pkgName}: hello tool')
  }
  ```
  **⚠️ 重要提醒（见坑 R1）**：这个官方骨架里 `parameters` 用了**属性级 `required: true`**（`name: { type: 'string', required: true }`），但 DSH 工具 schema 实际要求的是**对象级 `required` 数组**：
  ```ts
  parameters: {
    type: 'object',
    properties: { name: { type: 'string', description: '谁' } },
    required: ['name'],
    additionalProperties: false,
  },
  ```
  **🔴 本句已被 R1 顶部校正推翻**：走官方 `defineTool()` 时，**属性级 `required: true`（第一种写法）才是正确的**；第二种（对象级 `required` 数组）只适用于裸 `register` + 原始 JSON Schema。详见 R1 顶部「重要校正」。

- **“注册守卫”写法（逐字照抄）——冲突不崩、失败降级**：
  出处：`injector/src/index.ts` 第 2356–2366 行。

  ```ts
  // ⚠️ 必须挂 ctx.effect（自己的踩坑记录自己遵守）：裸注册在 fiber 卸载
  // （自重载 dispose/卸载）时不注销 → 残留工具闭包捕获旧 fiber 状态
  // （selfReloading 等）→ 新实例注册撞 duplicate 被跳过 → 跑的是「僵尸
  // 工具的僵尸闭包」（实测：锁永久卡死、新代码永不生效的根因）。
  function safeRegister(tool: any): void {
    try {
      ctx.effect(() => ctx.tools.register(tool), `dsh-super-injector: ${tool.name ?? 'tool'}`)
    } catch (e) {
      logger.warn('[super-injector] 跳过冲突工具注册: %s', e instanceof Error ? e.message : String(e))
    }
  }
  ```
  **要点**：① 注册一律包在 `ctx.effect` 里 + 带标签；② 用 `try/catch` 把“重名冲突”降级为 warn，**不让一个工具注册失败拖垮整个插件**。

- **拦截点 1：`llm/stream` waterfall（捕获/改写模型调用）**：

  ```ts
  // 观察面：捕获主模型路由（waterfall 必须 next() 委托）
  ctx.on('llm/stream', (options, next) => {
    lastRoute = { provider: options.provider, model: options.model }
    return next()
  })
  ```
  **要点**：waterfall 里**必须调用并返回 `next()`**，否则后续监听者和真正的 LLM 调用都被你“吃掉”。

- **拦截点 2：`ctx.webServer.register`（给插件开 HTTP API）**：
  出处：`injector/src/index.ts` 第 3281 行起。

  ```ts
  ctx.effect(() => ctx.webServer.register({
    kind: 'prefix',
    path: '/super-injector/api',
    handler: async (req: any, res: any) => {
      const send = (code: number, obj: unknown): void => {
        res.writeHead(code, { 'content-type': 'application/json; charset=utf-8' })
        res.end(JSON.stringify(obj))
      }
      try {
        const url = new URL(req.url ?? '/', 'http://localhost')
        const path = url.pathname.replace(/^\/super-injector\/api/, '') || '/'
        if (req.method === 'GET' && path === '/list') {
          const entries = readRegistry().map((e) => ({ ...e, active: hasActiveEntry(e.name) }))
          return send(200, { ok: true, entries, stats: opStats })
        }
      } catch (e) {
        send(500, { ok: false, error: String(e) })
      }
    },
  }))
  ```
  **要点**：① `kind: 'prefix'` + `path` 前缀路由；② 注册也挂 `ctx.effect`（热重载时路由自动摘，免 `duplicate route`）；③ 中文响应要写 `charset=utf-8`。

- **拦截点 3：`ctx.slots.inject` 挂 UI 面板（含两个必坑注释）**：
  出处：`SCAFFOLD_UI_CLIENT` 生成模板。

  ```ts
  /**
   * ${pkgName} — client 面板（conversation.view slot）。
   * 构建：npm run build:client（tsdown，产物 lib/client.js，ModuleLoader.load 注册）。
   * ⚠️ 两个必坑（2026-08 实测）：① apply 用 ctx.slots 必须 export const inject
   * = ['slots']（服务注入声明）；② register 必须带 name 字段（= slot 名，
   * 如 conversation.view）——缺 name 报 "slot undefined is not declared"。
   */
  import type { SlotsService } from '@deepseek-ai/dsh-client-ui-slots'

  type ClientContext = {
    slots: SlotsService
  }

  export const inject = ['slots']

  export function apply(ctx: ClientContext): void {
    ctx.effect(() => ctx.slots.inject('conversation.view', () =>
      ctx.slots.register({
        name: 'conversation.view',
        id: '${pkgName}-panel',
        label: () => ${JSON.stringify(pkgName)},
        component: () => ({
          render() {
            const el = document.createElement('div')
            el.textContent = ${JSON.stringify(pkgName)} + ' 面板'
            el.style.padding = '12px'
            el.style.fontFamily = 'monospace'
            return el
          },
        }),
      }),
    ), '${pkgName}: panel')
  }
  ```
  **要点**：① client 侧 `export const inject = ['slots']` **必须写**（否则 `cannot get property 'slots' without inject`，见 R23）；② `register` 的 `name` 字段 = slot 名，**缺了报 `slot undefined is not declared`**；③ `component` 形态随槽位不同：`conversation.view` 可用 `() => ({ render() {} })` 返回 DOM，而 **`settings.section` 必须返回 React 元素**（见 R10）。

---

# B · 三、该方向的开发规范（仅在多家共识时归纳）

> 归纳原则：下面每一条**至少两家独立仓库/文档**做法一致，且给出可核对的文件出处。只有一家这么做、或只是文档声称的，一律标“单一来源/未验证”，不当“规范”。

## 规范 1：函数式插件必须具名导出 `name` / `inject` / `apply`，**禁止 default export**

- **共识证据**：
  - WeKnora `src/index.ts`：`export const name = 'dsh-weknora'`、`export const inject = ['tools'] as const`、`export function apply(ctx, config)`（无 default）。
  - injector `SCAFFOLD_TOOLKIT`：`export const name = ...`、`export const inject = ['tools']`、`export function apply(...)`。
  - modlens `dsh/index.js`（grep 见 `export const name`/`apply`）。
- **要点**：`inject` 声明你依赖的服务（`tools`/`agents`/`sessions`/`llm`/`slots`/`timer`/`systemPrompt`…），Cordis **等这些服务就绪后才 apply**；用了某服务却没在 `inject` 声明，会报 `cannot get property 'X' without inject`（见 R23）。

## 规范 2：一切资源注册必须挂 `ctx.effect`，并保存 dispose

- **共识证据**：
  - injector `injector/CHANGELOG.md` [0.1.0]：明确要求“插件把资源注册挂 `ctx.effect`”，并把它写成**强制登记守卫**（发现裸注册即报错）。
  - injector `SCAFFOLD_TOOLKIT`：注释“资源注册必须挂 ctx.effect（热重载/卸载自动清理）”。
  - WeKnora `index.ts` 注释：“Each registration is an effect, so unloading or reconfiguring the plugin withdraws the tools without a restart.”（`ctx.tools.register` 返回 disposer）。
- **要点**：裸注册（直接 `ctx.tools.register(x)` 不挂 effect）在热重载/卸载时**不注销**，导致 `duplicate`、僵尸闭包（见 R2/R19）。

## 规范 3：`package.json` 要有 `dsh.bundle.patch`，`files` 白名单必须含 patch 与产物

- **共识证据**：
  - WeKnora `dsh: { bundle: { patch: "./cordis.patch.yml" } }`；`files` 含 `dist`、`cordis.patch.yml`。
  - modlens `dsh` 同时含 `bundle` 与 `client`；`files` 含 `dsh`、`cordis.patch.yml`。
  - injector `dsh` 同时含 `bundle` 与 `client`；`files` 含 `lib`、`cordis.patch.yml`、`scripts/*`。
- **要点**：漏了 `cordis.patch.yml` 进 `files` → 发布后用户装了但**没有装配补丁**；漏了构建脚本 → 从 tgz 装时建不了依赖（见 R14、[0.2.4]）。

## 规范 4：`cordis.patch.yml` 顶层是**单个数组**，entry 靠 `id` 唯一

- **共识证据**：
  - modlens：顶层 `- insert:` → `- id: modlens`。
  - injector 根 patch：顶层 `- insert:` → `- id: dsh-super-injector`。
  - injector `writePatch` 文档：坚持“顶层 `[]` 兼容 + 幂等”，杜绝“YAML 双顶层值”（见 R3/R4）。
- **要点**：`id` 是主键，**重复即启动崩**（`duplicate loader entry id`，见 R4）；**不要盲目 append** 到顶层，否则出现两个顶层数组（YAML 解析失败）。

## 规范 5：工具 schema 有两套写法 —— **先定路径，再定 `required` 位置**（⚠️ 原结论已按官方源码校正）

- **路径 A · `defineTool()`（官方自研插件全走这条）**：`parameters` / `output.schema` 是 **DSH 作者 DSL**，必填一律**属性级** `required: true`。
  - 证据：官方 `packages/interaction/tool-ask-user/src/index.ts`；官方 `packages/core/tools/src/schema.ts:571-572`（`parameterSchemaSpecToJsonSchema(options.parameters)`）。
- **路径 B · 手写 `ToolDefinition` 后 `register`（社区插件常走这条）**：`parameters` 是**原始 JSON Schema**，必填为**对象级** `required: ['a','b']`。
  - 证据：本次实测 `Tencent_WeKnora/packages/dsh-weknora/src/tools.ts:186` —— `const definitions: ToolDefinition[] = []`，随后 push 裸对象，`parameters: { type:'object', properties:{...}, required:['query'], additionalProperties:false }`（第 251-259 行）；`output.schema` 同理（第 194、211-216 行）。
- **共识证据（路径 B 内部）**：
  - WeKnora `tools.ts` 全部 4 个工具：`parameters` 与 `output.schema` 都是对象级 `required` 数组 + `additionalProperties:false`。
  - modlens `vision-schema.json`：对象级 `required` 数组，属性级只有 `type`/`description`/`properties`/`items`/`required`。
  - `graded/src/tools.js` 注释明确“属性级不允许 `required` 键”。**⚠️ 该注释只适用于路径 B；路径 A（`defineTool`）下属性级 `required: true` 才是正确写法（见 R1 顶部校正）。**
- **两条路径都能用，但绝不可混**。新手建议：**选路径 A（`defineTool`）**，因为它自带参数校验（`validateJsonSchemaValue`）、类型推导（`InferArgs<S>`）和更友好的报错。
- **不要**把路径 A 的 DSL 当成"标准 JSON Schema"来理解：它的根是**隐式开放对象**（直接铺属性名，不用写 `type:'object'`/`properties`），且作者**不允许**写对象级 `required` 数组（写了会报 `required must be true when present`）。

## 规范 6：`peerDependencies` 用版本**范围**；宿主依赖要么打进 bundle、要么完全不依赖

- **共识证据**：
  - injector：`"@deepseek-ai/dsh-tools": ">=0.0.1-rc <2"`、`"cordis": ">=4.0.0-rc <5"`；并用 tsdown host bundle 自包含（[0.3.3]，见 R18）。
  - WeKnora：**零 runtime 依赖**，类型自镜像。
- **要点**：钉死 rc 号会在 DSH 升级后报废（见 R13）；官方 `dsh plugin add <目录>` 对 `link:` 依赖**不装 peers**（见 R18）。
- ⚠️ **`engines.dsh` 是这套「写范围」策略的一个例外**（`dsh-v0.2.1-alpha.4` 起）：一旦声明，**它单独决定兼容性**，`peerDependencies` 的范围**不再**放宽或收窄它 —— 所以「peer 写宽一点以兼容旧版」的做法对 `engines.dsh` 无效。要么给它覆盖全部目标版本的完整范围，要么不写。（判据：`packages/boot/app-boot/src/plugin-compatibility.ts:55-73`。）

## 规范 7：waterfall 事件（`agent/pre-step`、`system-prompt/assemble`、`llm/stream`）必须 `await next()` / `return next()`

- **共识证据**：
  - 官方 `docs/user/develop/framework/events.zh.md:64-81`：waterfall 监听器**必须调用 `next()`**，不调用会短路整条流水线。
  - injector `SCAFFOLD_TOOLKIT` 与 `docs/SPEC.md` 第 6 节：“Waterfall 必须 `await next()`、`agent` 判空、晋升从持久日志推导、只裁剪本插件工具”。
- **要点**：不 `next()` = 吃掉后续所有监听者与真实调用；`{ prepend: true }` 表示“最后说话”，需先 `await next()` 拿最终结果再改。

## 规范 8：存盘/配置路径以 `DSH_HOME` 为准，别硬编码 `~/.dsh`

- **共识证据**：
  - injector [0.3.3]：“DSH_HOME 优先（homedir 错家）”，scaffold 模板同步（见 R5）。
  - injector `SCAFFOLD_DAEMON`：`const dshHome = process.env.DSH_HOME || join(homedir(), '.dsh')`。
  - `graded/src/index.js`：`stateFile` 同规则。
- **要点**：web 进程的 `homedir()` 与 `DSH_HOME` 可能不一致（服务账户/跨用户部署），硬编码会把文件写到错误位置。

## 规范 9（强共识）：工具 = `parameters`（输入 schema）+ `output.schema/render`（输出）+ `execute`（纯数据）

- **共识证据**：WeKnora 全部 4 个工具、modlens（`vision-schema.json` + `render`）、injector 全部 `dev_*` 工具，形态一致。
- **要点**：`execute` 只返回**可序列化的纯数据**；面向模型的文本在 `render` 里生成。

## 规范 10（两家，写法二选一）：配置校验用 schemastery `Config` 或手写 `resolveConfig`

- **共识证据**：
  - 用 schemastery：injector（`import z from 'schemastery'` + `export const Config = z.object({...})`）、injector scaffold。
  - 手写：WeKnora `config.ts` 的 `resolveConfig()`（收集所有错误一次性报）。
- **要点**：两种都行；关键是**在 `apply` 入口就校验**，拼错字段要“加载即失败”，别拖到运行中。

## 明确“**未找到共识**”的项（不要当规范写）

- 插件目录用 `src/`（TS 编译，WeKnora/injector）还是根目录手写 `.mjs` 还是 `dsh/`（modlens）——**并存，无共识**。
- 构建工具：WeKnora 用 `tsc`；injector/modlens 用 `tsdown`/`vite`——**无共识**。
- 是否要 client 面板：WeKnora 无 client，modlens/injector 有——**按需**。

---

# B · 四、新手最容易卡住的 5 个点（每条一句可执行建议）

1. **插件“装上了但没反应 / 工具找不到”** → 先查 `package.json` 有没有 `dsh.bundle.patch` 且 `files` 里带了 `cordis.patch.yml`，再查 patch 顶层是不是**单个数组**、`id` 有没有和别的 entry 重名。（依据：R3、R4、规范 3/4）
2. **`duplicate` / `already registered` / 热重载后跑旧代码** → 把所有注册（工具、路由、服务）**包进 `ctx.effect` 并保存返回值**，卸载时真调用它；不要“裸注册”。（依据：R2、R19、规范 2）
3. **工具一调用就报 schema 错 / 模型看不到工具** → `parameters` 用**对象级 `required` 数组 + `additionalProperties: false`**，别在属性里写 `required: true`；`output.schema` 必须完整描述 `execute` 的返回值。（依据：R1、规范 5/9）
4. **`cannot get property 'X' without inject` / 面板白屏** → 用了哪个服务就在插件里 `export const inject = ['X']`（UI 用 `ctx.slots` 就写 `['slots']`），`register` 记得带 `name` 字段；`settings.section` 的 `component` 必须**返回 React 元素**。（依据：R10、R23、模板四）
5. **本地能跑、发布/换机就崩** → `peerDependencies` 写**范围**不钉 rc 号；宿主依赖要么**打进 bundle**、要么像 WeKnora 一样用**结构化类型镜像做到零依赖**；路径一律以 `process.env.DSH_HOME || ~/.dsh` 派生。（依据：R5、R13、R18、规范 6/8）

---

# B · 五、附录：目录树汇总、坑位统计与来源索引

## 附录 A：四个仓库的完整目录树（实际快照）

### A1. WeKnora · `@wxg-prc-cpg/dsh-weknora`（工具插件，最干净）

```
packages/dsh-weknora/
├── .gitignore
├── README.md / README_CN.md
├── contract/contract_test.go
├── cordis.patch.yml
├── package.json / package-lock.json
├── src/
│   ├── client.ts        # REST + SSE
│   ├── config.ts        # 手写 resolveConfig
│   ├── harness.ts       # 结构化类型镜像（零依赖关键）
│   ├── index.ts         # name / inject / apply
│   ├── render.ts        # 文本渲染辅助
│   └── tools.ts         # 4 个 defineTool
├── test/
│   ├── client.test.mjs / config.test.mjs / contract.test.mjs / tools.test.mjs
│   ├── e2e/fake-model.mjs / e2e/run-in-dsh.mjs
│   ├── fixtures/api-contract.json
│   └── helpers/json-schema.mjs / helpers/mock-weknora.mjs
└── tsconfig.json / tsconfig.build.json
```

### A3. modlens · `@liustack/modlens`（bundle + client 双声明）

```
liustack_modlens/
├── package.json / cordis.patch.yml
├── dsh/
│   ├── index.js            # 后端插件（2199 行）
│   ├── client.js           # 前端 UI（client 入口，51KB）
│   ├── vision-schema.json  # output.schema（纯 JSON）
│   ├── spawnHidden.js / spawnHidden.d.ts
├── dist/                   # CLI 产物（bin）
├── docs/（含 troubleshooting.zh-CN.md 248 行、harness-setup.zh-CN.md、output-schema.md）
├── skills/modlens/...
├── assets/ / evals/ / scripts/
└── CHANGELOG.md / SECURITY.md / AGENTS.md
```

### A4. routing-suite · `@dsh-external/dsh-super-injector`（运行时注入器）

```
yjh051108_dsh-routing-suite/
├── package.json / cordis.patch.yml / install.ps1 / install.sh
├── .gitattributes / README.md / README.en.md / LICENSE
├── docs/FLATTEN-MIGRATION.md
├── test/root-package-prepare.test.mjs
├── scripts/install-injector.ps1
├── injector/            # 插件本体（bundle + client）
│   ├── package.json / cordis.patch.yml / CHANGELOG.md / INSTALL.md / README.md
│   ├── docs/SPEC.md
│   ├── src/index.ts（3323 行）/ src/client/index.ts（181 行）
│   ├── scripts/build.sh / prepare.mjs / fix-patch.mjs
│   └── lib/（构建产物：index.js / client.js / types/）
├── graded/             # 预设/工具示例（bundle 插件）
│   ├── package.json / cordis.patch.yml / dsh.plugin.json
│   ├── src/index.js / src/tools.js（521 行）/ src/inject-text.js / src/mode-state.js
│   └── lib/ / client/ / docs/ / tests/ / scripts/
└── preset/            # agent preset（不是插件！）
    ├── package.json / README.md / AGENTS.md / CHANGELOG.md
    ├── router-react/ / router-spec/ / router-standard/（*.mjs + preset.yml + agent.cordis.yml）
    └── router.test.mjs / router.integration.test.mjs
```

## 附录 B：三仓库坑位统计（本次实际挖到）

| 仓库 | 坑编号 | 数量 | 最主要的 3 个 |
|---|---|---|---|
| WeKnora | W1–W4 | 4 | W1 无 scope 检索不透明 400；W2 `resource://` 渲染 + 403 降级记忆；W3 SSE 截断当完整答案 |
| ~~OpenViking~~ | — | **0（原 10）** | 该来源为 **AGPL-3.0**，已整体移出引用集合；其中 8 条私有实现类坑移除、教训提炼为 8 条自撰建议；坑 **O1/O5 保留**，权威出处已换为官方 `deepseek-harness` 源码（MIT） |
| modlens | M1–M10 | 10 | M1 缺 `dsh.bundle` + pnpm 冷静期；M2 工具名撞 scoped 层被遮蔽；M8 Windows 黑框 |
| routing-suite | R1–R28 | 28 | R1 属性级 `required` 不允许；R4 `duplicate loader entry id` 启动即崩（**0.1.6 起行为已变，见 `05-pitfalls.md` 坑 P3**）；R18 官方装配不装 peers |

**总计 42 条**（WeKnora 4 + modlens 10 + routing-suite 28），另有 **2 条机制类坑（O1 / O5）**，其权威出处为**官方 `deepseek-harness` 源码行号**（MIT）；以及 8 条以「自撰建议」形式保留的通用教训（见 §1.2）。

## 附录 C：本次实际读取的源码/文档文件（去重后清单，供复核）

- **WeKnora**：`package.json`、`src/index.ts`、`src/tools.ts`、`src/client.ts`、`src/config.ts`、`src/harness.ts`、`src/render.ts`、`cordis.patch.yml`、`README.md`、`test/fixtures/api-contract.json`、根 `.github/workflows/dsh-plugin.yml`（约 11 个）
- ~~**OpenViking**~~：该来源已整体移出引用集合，其读取清单不再收录（现存 **0** 个文件计入）。
- **modlens**：`package.json`、`cordis.patch.yml`、`AGENTS.md`、`docs/troubleshooting.zh-CN.md`、`docs/harness-setup.zh-CN.md`、`docs/output-schema.md`、`CHANGELOG.md`、`dsh/index.js`、`dsh/client.js`、`dsh/spawnHidden.js`、`dsh/vision-schema.json`（约 11 个）
- **routing-suite**：`injector/package.json`、`injector/cordis.patch.yml`、`injector/src/index.ts`、`injector/src/client/index.ts`、`injector/docs/SPEC.md`、`injector/CHANGELOG.md`、`graded/package.json`、`graded/cordis.patch.yml`、`graded/dsh.plugin.json`、`graded/src/tools.js`、`graded/src/index.js`、`graded/CHANGELOG.md`、`package.json`、`cordis.patch.yml`（约 14 个）

**三仓库合计约 36 个文件**（另含 git 提交元数据查询若干次）。

## 附录 D：结论来源索引（按坑号反查）

- W1–W4 → `src/Tencent_WeKnora/packages/dsh-weknora/**`（tools.ts / client.ts / .github/workflows）
- O1、O5 → 官方 `deepseek-harness` 源码（MIT）：`packages/preset/persona/src/index.ts`、`packages/llm/llm/src/types.ts:112`、`packages/acp/acp/src/updates.ts:82`（原 AGPL 来源的定位已整体移除）
- M1–M10 → `src/liustack_modlens/**`（package.json / docs/troubleshooting.zh-CN.md / dsh/**）
- R1–R28 → `src/yjh051108_dsh-routing-suite/**`（injector/CHANGELOG.md、graded/CHANGELOG.md、injector/src/index.ts）+ `repos/yjh051108_dsh-routing-suite` git 提交元数据

> 备注：本次另有 git 历史查询（仅 commit 元数据、无 blob，故只用 `git log` 读提交信息，**未使用 `git show`**）。所有“提交信息原文”均来自 `repos/<仓库目录>/` 的 git 元数据。

---

