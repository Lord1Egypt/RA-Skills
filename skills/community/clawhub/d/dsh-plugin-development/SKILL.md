---
name: dsh-plugin-development
slug: dsh-plugin-development
displayName: DSH Plugin Development
summary: Develop DSH (DeepSeek Harness) / Cordis plugins end to end — plugin forms, templates, an API cookbook, catalogued pitfalls, packaging and publishing, plus a mandatory version gate for the pre-stable upstream. Third-party fragments quoted here remain under their own licences (MIT / Apache-2.0 / BSD-3-Clause) — see the bundled LICENSE and NOTICE.
description: A development-time skill for building plugins on DSH (DeepSeek Harness) / Cordis. It is not itself an installable DSH plugin; it is the tooling that guides a developer or AI agent through creating, debugging, packaging, and publishing one. This skill should be used when the user asks to develop a DSH plugin, write or modify a cordis plugin, add a tool, slash command, config schema, service, UI slot or HTTP route to DSH, run a periodic task inside a plugin, fix a plugin that fails to load or stays in PENDING, or package a plugin bundle for installation or distribution. It covers the plugin forms and official conventions, with 12 templates, 25 catalogued pitfalls, and copy-ready prompts for AI-agent pair development. Because DSH is pre-stable and ships breaking changes on a short cadence, it also ships a mandatory pre-coding version gate, a probe that re-verifies its own claims against a live source checkout, and a per-tag history of upstream breaking changes.
version: 1.8.1
license: MIT-0
agent_created: true
metadata:
  openclaw:
    emoji: "🔌"
    homepage: https://github.com/liupengyang-1008/dsh-plugin-development
    requires: { anyBins: [python3, python] }
---

# DSH 插件开发

把「DSH 插件」从选型做到发布：选形态 → 写代码 → 排错 → 打包 → 发布。入口只放**执行时必需**的东西（闸门 / 选型 / 路由 / 工作流 / 红线 / 合同 / 验收），细节一律在 `references/`，按需读取，不要一次全读。

> **定位：这是一个「用来开发 DSH 插件的技能」，它本身不是能装进 DSH 的插件。** 它不会被 `dsh plugin add` 安装，也不进入任何 DSH profile；**本技能产出的那个 `dsh.bundle` 包才是能装进 DSH 的东西**。找现成插件请去社区插件市场（`references/12-community-plugins.md`）。
> 已知边界与维护守则见 `references/15-skill-scope-and-maintenance.md`（此处不重复）。

## 何时使用

- 用户要求开发 / 修改 / 调试 / 打包 / 发布 DSH（DeepSeek Harness）插件
- 出现这些词：DSH 插件、cordis 插件、`cordis.patch.yml`、`dsh.bundle`、`defineTool`、`ctx.slots`、`ctx.tools.register`、PENDING
- 用户要求审查现有 DSH 插件代码、判断该用哪种插件形态
- 用户问「为什么我的插件装上了但没反应」
- 用户报这些症状：**插件不生效 / slot 崩溃 / 服务注入失败 / 改了代码不生效 / 样式被冲掉**

**不适用**：要的是「装进 DSH 就能直接用的现成插件」——本技能不提供任何运行时能力、也不负责插件分发。

## 第 0 步（强制，不可跳过）· 版本闸门

**references 是某一时刻的快照，会腐化。** DSH 处于 rc 阶段（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），tag 间隔中位数约 1.0 天（实测 1.03）、出现过破坏性变更。**所以不要承诺「不过时」，要保证「过时会响」。**

**① 权威顺序（源码永远压过本技能）**

```
1. 当前 DSH 源码                    ← 唯一权威
2. 探针脚本对当前源码的核验结果      ← 可执行的证据
3. 本技能的 references（快照）       ← 脚手架，不是权威
4. 模型记忆 / 常识                   ← 禁止作为唯一依据
```

**② 三问**：① 我在对哪个版本写代码？（拿不到就**先要版本**，不知道版本不得断言 API）② 我要用的 API 属于 S/M/V 哪一级？③ 我能核验吗？（不能 → 走降级规则）

**③ 跑探针**（两个版本，优先 Python 版）

```bash
python <skill>/scripts/dsh-api-probe.py <DSH 仓库路径>    # 推荐：零 coreutils 依赖，Windows 最稳
bash   <skill>/scripts/dsh-api-probe.sh <DSH 仓库路径>    # 备选：仅当 shell 有完整 coreutils
# 0 = 断言全部成立    1 = 有 STALE（不要照抄）
# 2 = 仓库路径不对    3 = 断言表为空（结果无效）
```

> ⚠️ shell 缺 `cat`/`grep`/`dirname` 时，bash 版会报几十条**假 STALE**。拿不准就用 Python 版；两者不一致以 Python 版为准。
> **S/M/V**：问「这条事实明天变了，我的代码会崩吗？」——会崩 → M/V，必须核验；不会崩 → S，可直接用。
> **降级规则**（拿不到源码时）：① 显式声明「以下 API 未对当前版本核验」；② S 级骨架照给，M/V 级符号单列成「需你确认」；③ 禁止把未核验事实写成肯定句。**绝不编造 API 名填补空白。**
> **目标版本高于基线时**不要猜：`dsh-sync.sh` 拉源码（先经确认）→ 探针核验 → `dsh-version-diff.sh` 出差异。
> 完整机制（腐化推导、三级全表、五种核验手段、网络不可达时的降级路径）见 `references/00-version-gate.md`。

**基线 `dsh-v0.2.2-alpha.2` 的硬变化（照抄旧资料前先对照）**

DSH 每次发版的破坏性变更集中在少数几类。**本节只展开基线所属的最新一个区间；更早的 16 个区间（`dsh-v0.1.5-rc.2` → `0.2.1-rc.3`）见 `references/13-version-history.md` §2。**

**`0.2.1-rc.3` → `0.2.2-alpha.2`（2170 个提交、2 个新 tag：`-rc.4` 9 个 / `-0.2.2-alpha.2` 2161 个）—— 🔴 有破坏性变更（第二段进位 → `1.8.0`）**

> 🔴 **判据渠道**：本区间 `!:` 自报破坏性提交仅 **1 条**（`2f01ad549c fix(web)!: …`，第六次近乎空炮），而真破坏面 **5 条里它一条都没标出**。权威渠道 = 上游 `docs/upgrade-guide/` 本区间新增 **38** 个 topic，其中 `v0.2.1-rc.2/tool-executor-plugins` 与 `v0.2.1-rc.2/conditional-tools` 是两条主破坏面。

1. 🔴 **工具执行器从 `dsh-tools` 拆成独立插件**。`dsh-tools` 的 `Config` 只剩两个 `z.never()` 占位：`mode`（`packages/core/tools/src/index.ts:102`，原文 `Removed. Mount a native or PTC tool executor instead.`）与 `maxParallelSubCalls`（`:103`）→ **任何还写 `tools: config: mode:` / `maxParallelSubCalls:` 的 patch 或 profile 在加载时被拒**。原生 / PTC 分别要挂 `@deepseek-ai/dsh-tool-executor-native` / `-ptc`（官方 base 补丁同批新增两行，后者 `disabled: true`；PTC 还需 `ctx.ptcRuntime` 在册）。**没有执行器时 `ctx.tools` 直接抛 `ToolExecutorUnavailableError`**（`:365` / `packages/core/tools/src/executor.ts:97`）—— 自建组合必须自己挂一个。`DSH_TOOLS_MODE` 环境变量**不再被读取**。`dsh-agent-tool-presentation` 的 `Config.mode` 仍在但**已 `@deprecated`**。
2. 🔴 **`system-prompt/assemble` 不再携带工具数组**。该 waterfall 只给段落、上下文与变量，**返回的 `tools` 被忽略**、`assembly.tools` 为 `undefined` → **以前在这里增删工具声明的插件彻底失效**，读该字段的监听器运行时出错。替代方案：`ctx.tools.register(definition, { when })`（`packages/core/tools/src/contracts.ts:115`），以 `{ agent, modelSelection, signal }` 每步骤求值；为假即从声明 / 原生分发 / PTC 绑定 / 嵌套调用**四处**移除，抛错则轮次以 `TOOL_ACTIVATION_FAILED` 结束，集合外调用返回 `UNKNOWN_TOOL`。
3. 🔴 **`ctx.tools` 服务面重排**：`presentAs(mode)` 与 `ToolPresentationMode` **移除**；`execute()` 由单次改为**批次**（`ToolBatchInput` / `ToolBatchResult`）；`register()` 增加第二参数；新增 `setExecutor` / `resolve` / `definitions` / `executable` / `checkGuards`。主入口**不再导出** `ToolExecutionPipeline` / `executeToolBatch` → 改从 **`@deepseek-ai/dsh-tools/pipeline`** 导入，工具测试夹具改从 **`@deepseek-ai/dsh-tool-testkit`** 取。
4. 🔴 **配置键改名**：`tool-subagent` 的 `modelSelectionSettings` → **`modelSelection`**，并新增 `modelDiscovery`（`packages/subagent/tool-subagent/src/index.ts`）→ 旧键写进 patch 会校验失败。
5. ⚠️ **行为面变动（不是失效）**：`web_fetch` 现在可达非公网地址（`2f01ad549c`）—— 依赖「web_fetch 只能取公网」的安全假设需复核。另一处加法：`webServer.register` 形参扩为 `WebRoute \| WebResourceRoute`（`packages/host/webserver/src/index.ts:549`），旧写法不受影响。

**新增面（不改已有契约）**：官方包 **352 → 378（+27 / −1）**，新增含 `dsh-tool-executor-native` / `-ptc` / `dsh-tool-testkit` / `dsh-official-bundles` / `dsh-plugin-detail` / `dsh-action-cards` / `dsh-message-quotes` 等，**移除 `dsh-client-ui-deepseek-model-label-1017`**（原 `conversation.input.model.label` 的官方占用方示例，本技能 `04` / `08` 已改写）；base 补丁 +`tool-executor-native` / +`tool-executor-ptc`(disabled) / −`tool-subagent-list-agents`；插槽 **+3 / −0**（`conversation.chat.text-interaction` / `conversation.chat.user.before` / `sidebar.session.row.trailing`）；服务 +8（**全部在 `experimental/` 或 headless 组合包内**）、事件 +5、类型 +144 / −8（8 项移除中 7 项是主入口改子路径导出，`ToolRuntime` 仍以别名保留）；包内 `Config` 键 **+38 / −1**（416 → 453）。

**未变项逐条实测**：`SESSION_FORMAT_VERSION` 仍 **4**；模型 ID 仍 `deepseek-flash`；CLI **无新增选项**；`defineTool` 的参数 DSL 契约未变（`schema.ts` 仅新增 `projectToolSchema`）。插槽计数由 **144 / 146 / 约 103** 改为 **148 / 150 / 约 106**，`slot-catalog.ts` **103 → 106**。
**更早的 16 个区间（`dsh-v0.1.5-rc.2` → `0.2.1-rc.3`）不在此处重复。** 完整破坏性变更总表（按区间逐行）见 `references/13-version-history.md` §2；作者自报渠道 `!:` 的覆盖率实测与反例见同文件 §2.5。**手上资料早于 `0.2.1-alpha.4` 时，先去读那两节再动手。** 其中紧邻的上一区间（`0.2.1-rc.2 → -rc.3`，6 个提交）**无破坏性变更**，只做了一处行为收紧（New Session 复用空白会话）；再上一区间（`0.2.1-alpha.4 → -rc.2`）的重头是**账号奖励通知字段放宽**，并附「**交付了机制、但没有官方市场与默认索引源**」那条收窄结论 —— 这两点仍在 `13` §2 该行与 `01` / `06` / `12` 的对应条目里，别因为本节换了区间就当成「没这回事」。

**判据**：三条来源都要看 —— 探针（`M33`~`M37` / `N06`~`N08` / `P06`~`P07` / `V01` / `X07` / `U11`~`U12` / `X08`~`X09` / **`E01`~`E03`** 就是这几批）、`dsh-version-diff.sh` 的六维度、以及上游自带的 `docs/upgrade-guide/`。
**⚠️ 别指望 `!:`**：十三个区间里非 merge 提交带 `!:` 的分别是 **0 / 0 / 1 / 0 / 0 / 0 / 0 / 1 / 0 / 0 / 0 / 0 / 1** —— 而最狠的整族改名一条都没标 —— **`!` 既非充分也非必要，判影响只看两端文件内容的集合 diff**（完整实测与反例见 `13-version-history.md` §2.5）。


## 三条基础纪律

1. **引用任何字段名 / 事件名 / 服务名 / 插槽名前，先查 `references/08-cheatsheet.md` 或 `references/api-claims.md`。** 查不到就 grep 源码，**不要凭印象写**。
2. **代码跑通前不要声称完成。**「装上了」不等于「生效了」——必须看到实际输出或界面变化。
3. 每条结论尽量附出处（文件路径 + 行号）。

## 决策流程

### 第 1 步 · 选形态（选错形态 = 后面全部返工）

| 形态 | 何时选 | 必须这样写 | 禁止 |
|---|---|---|---|
| **函数式插件** | 绝大多数情况：加工具 / 命令 / 事件监听 | 具名导出 `name` / `inject` / `Config` / `apply` | **绝对不能有 `export default`**（会被当成服务类解析而失败） |
| **服务插件** | 要给**别的插件**提供能力，让别人 `inject` 你 | `export default class extends Service`，构造函数首行 `super(ctx, '服务名')` | 写成普通函数导出 |
| **组合包 bundle** | 只是把已有插件装到一起，纯配置 | 只需 `package.json` + `cordis.patch.yml`，声明 `"dsh": {"bundle": {"patch": "./cordis.patch.yml"}}` | 不要写 JS / TS，不要有 `src/` |

> **UI 插件是函数式插件的特例**，不是第四种形态——它只是多了一个「浏览器半侧」和若干登记点。判定流程见 `references/01-mental-model.md`。

### 第 2 步 · 按需求路由到模板

用户不会说「T3」或 `defineTool`，他说的是人话。**照抄用户的说法**在左列定位，再往右走：

| 用户这么说 | 模板 | 形态 | 注册在哪 | 怎么算跑通（冒烟判定） |
|---|---|---|---|---|
| 「把某个现成能力 / MCP server 挂进来」 | **T1** | 组合包 | `cordis.patch.yml`（零代码） | `--dump-config` 里出现 insert 行 |
| 「改一下某个现成插件的行为」 | **T2** | 组合包 + 覆盖层 | 同上 + 补丁字段 | 同上，且被改的行为确实变了 |
| 「让模型会用某个能力」「加个工具」 | **T3**（首选）/ **T4** | 函数式插件 | 宿主半侧 `ctx.tools.register(defineTool({...}))` | 真实会话里模型调用它并拿到结果 |
| 「加个 /命令」 | **T5** | 函数式插件 | `ctx.commands.register({...})` | 敲一次 `/命令`，有返回 |
| 「让用户能调参 / 改配置」 | **T6** | 函数式插件 | `export const Config` | 改配置后行为变化；非法配置被拒 |
| 「给别的插件提供能力」「当基础设施」 | **T7** | 服务插件 | `extends Service` / `ctx.provide` | 另一个插件能 `inject` 并调用成功 |
| 「网页界面上加个东西」 | **T8** | 函数式插件 + 浏览器半侧 | `ctx.slots.inject(key, () => ctx.slots.register({...}, 组件))` | 界面出现你的东西，无 slot 崩溃 |
| 「设置界面里加一张卡」 | **T9** | 同上 | 设置命名空间 + `settings.*` 插槽 | 卡片可见、改动生效 |
| 「管住 Agent / 拦消息 / 改请求 / 加提示词」 | **T10** | 函数式插件 | `agent/pre-step`、`agent/request`（waterfall） | 跑一次会话，行为确实被改 |
| 「接一个外部系统（HTTP / CLI / 协议）」 | **T11**（零代码优先 → **T1**） | 函数式插件 或 组合包 | 工具 + 事件钩子 | 真调一次外部系统，拿到真数据 |
| 「暴露一个接口给外面调」「加个健康检查」 | — | 函数式插件 | `ctx.webServer.register({kind, path, handler})` | `curl` 真打一次，看到 200 与预期响应体 |
| 「每天定时跑」「周期任务」 | — | 函数式插件 | `ctx.interval(cb, delay)`（**不是** `ctx.setInterval`） | 等一个周期，看到任务真的跑了 |
| 「建一个规范的完整工程 / 准备发布」 | **T12** | 工程骨架 | 全套约定 | 门禁脚本通过 + 真 profile 安装成功 |
| 「托管静态文件」「发布一个 DSH skill」 | ⚠️ 范围外 | — | — | 见 `references/15-skill-scope-and-maintenance.md` |

**没在表里？** 先按「实现位置」归属——改宿主行为 = 工具/命令/服务/事件；改界面 = 插槽；只是组装 = 补丁。归属清楚后照最近的模板改。
带 `—` 的两行（入站 HTTP / 定时任务）没有独立模板，完整写法见 `references/14-inbound-http-and-timers.md`；更细的路由展开见 `references/01-mental-model.md` §1.1 与 `references/08-cheatsheet.md` A.4，**冲突时以 references 的逐字源码为准**。

### 第 3 步 · 按难度阶梯选模板

**不要从最难的开始。** 先做能跑通的最小闭环，再逐级加复杂度：零代码组合包（T1/T2，低）→ 斜杠命令（T5，低）→ 工具插件（T3/T4，中）→ 可配置插件（T6，中）→ 服务插件（T7，中高）→ UI 与设置卡片（T8/T9，高）→ Agent 流程拦截（T10，高）→ 外部集成 / 完整工程骨架（T11/T12，高）。

12 个模板的完整代码、常用 UI 插槽名速查（**节选，非全清单**）在 `references/02-templates.md`；**官方 7 类模板的逐字源码**在 `references/02b-official-templates.md`。

## 标准工作流

按顺序执行，每一步都能独立验证。**不要跳步**，也不要在上一阶段未确认时抢跑下一阶段。

| # | 阶段 | 做什么 | 完成标志（未达到不得进入下一步） | 读哪个文件 |
|---|---|---|---|---|
| **0** | **版本闸门** | **强制**：答三问 + 跑探针 | 探针退出码 0；或已显式声明哪些 API 未核验 | `00-version-gate.md` |
| 1 | 选型 | 判定三种形态之一 + 路由到模板 | 形态与模板编号都写下来了，且**没有 `export default`** | `01-mental-model.md` → `02-templates.md` |
| 2 | 环境 | 版本对照、`DSH_HOME` 位置、从源码跑起来 | `dsh --profile <名字> --dump-config` 能打出组合树 | `06-workflow.md` ① |
| 3 | 最小闭环 | 先做一个能加载、能看到的空插件 | **装进真 profile 后有可见结果**（哪怕只是一条命令返回） | `02-templates.md`（T1 或 T3） |
| 4 | 冒烟 | 给每个能力面立起冒烟点并跑通 | 对照本文件「冒烟与验收」的判定表，逐项为真 | 本文件「冒烟与验收」 |
| 5 | 写功能 | 按 API 写工具 / 命令 / 配置 / 服务 | `inject` 覆盖全部用到的服务；需清理的副作用在 `ctx.effect()` 内 | `03-api-cookbook.md` |
| 6 | UI（如需） | 两个半侧 + **三个登记点** + 插槽 | 界面出现你的东西，且控制台无 slot 崩溃 | `04-ui-and-slots.md` |
| 7 | 调试 | `--dump-config` 查组合树；PENDING 审计查注入失败；HMR 免重启 | 没有 PENDING 条目、没有静默失败 | `06-workflow.md` ④ |
| 8 | 打包 | 组合包结构、`package.json`、patch 引用、分发方式对比 | **合同不变量 5 条全过** | `06-workflow.md` ③ |
| 9 | 安装验证 | `dsh plugin --profile <名字> add <包>`（`--profile` 必填） | 从**最终分发源**重装后仍通过冒烟 | `06-workflow.md` ② |
| 10 | 工程化 | 命名、README 强制节、测试、门禁、提交规范 | 过 `07-conventions.md` 的门禁清单 | `07-conventions.md` |

**决策门的回退规则**（失败先分类，别一律推倒重来）：

- **合同级 / 形态级错误**（导出形式、`inject`、patch 声明、client 声明、名称三处不一致）→ **回第 1~2 步重新选型**。在错形态上打补丁只会越补越乱。
- **业务级错误**（逻辑、返回值、样式、报错信息）→ 留在第 5~7 步**原地修**。

**环境降级**：本机没有 Node / pnpm 时，仍要产出**等价的完整文件**，并在 `docs/plan.md` 里**显式标注跳过了哪些可执行验证**。不许把「跳过」写成「通过」。

## 冒烟与验收

**原则：每个能力面，先配一个「一眼能看出真假」的冒烟点，再写业务。** 新建插件时先立起三件套：**一条命令**（总能成功、输出可辨认）+ **一个真实调用**（工具/集成类要让模型真调一次，看它拿到真数据）+ **一个可见标记**（UI 类要在界面上一眼能看到）。

| 能力面 | 冒烟通过 = |
|---|---|
| 组合包 / 补丁 | `--dump-config` 里出现你的行，且改配置确实生效 |
| 命令 | 敲一次 `/命令`，有返回 |
| 工具 | 真实会话里模型调用它，拿到预期结果 |
| 服务 | 另一个插件 `inject` 后能调用成功 |
| 事件 / 拦截 | 触发一次事件，行为确实随之改变（不是静默无响应） |
| HTTP 路由 | `curl` 真打一次你注册的 `{kind, path}`，看到 200 与预期响应体 |
| 定时任务 | 等过至少一个周期，看到任务真的执行 |
| UI / 设置卡片 | 组件可见可交互，控制台无 `slot entry crashed`、无重复 React 报错 |
| 配置 | 改配置后行为变化；给非法值能被明确拒绝 |

⚠️ **三条反假通过的纪律**：① 必须在**真实组合**（真 profile、真加载）里验，本地另一份配置跑通不算；② 验收要指向**用户实际访问的那个 URL / 那个 profile**；③ 部分成功不能当成功返回——操作了一半要如实报错。

### 改完代码怎么生效（改错地方 = 白改）

| 改了什么 | 怎么生效 |
|---|---|
| profile / home 下 `cordis.patch.yml` 里的 `config` | **自动热替换**（框架卸载旧实例、加载新实例） |
| `--patch` 指定的 overlay 文件 | **不会**被热重载——改它必须重启进程 |
| 插件代码（`src/`） | 默认**必须重启**；想免重启要先开启 HMR（默认 `disabled: true`，且依赖 timer 插件，缺了会永久 PENDING） |
| 浏览器半侧（client） | 重新构建 → 重新安装 / 更新插件 → 刷新页面（client bundle 按 id 缓存） |

> 任何时候都**只改 `src/`，不要手改 `lib/`**——`lib/` 是构建产物，手改会在下次构建被覆盖。

## 合同不变量（写 `package.json` / patch / client 前必看）

DSH 里最常见的「我明明装了啊」有五种成因，全部落在这 5 条上：

1. `package.json`：`type: "module"`、`main: "lib/index.js"`；`exports["."]` 与 `exports["./package.json"]` **必备**。
2. 组合包形态再加：`dsh.bundle.patch` 指向 `./cordis.patch.yml`，且 `exports["./cordis.patch.yml"]` 与 `files` **都要有**。
   ⚠️ 少了 `dsh.bundle.patch`，`dsh plugin add` 只打一条 `declares no dsh.bundle` 警告然后**什么都不做**——新手第一大坑。
3. UI 形态再加：`dsh.client.platform: "web"` 与 `exports["./client"]` **必须成对存在**，缺一个客户端半侧根本不组装。
4. **名称三处一致（铁律）**：`package.json#name` = patch 的 insert `id` / `name` = 客户端 ModuleLoader `id`。
5. **禁止声明 `@deepseek-ai/*` 依赖**（DSH profile 已提供）；客户端 bundle 里 `react`、`react/jsx-runtime`、`react-dom`、`react-dom/client` **必须 external**（打进第二份 React 会导致 hooks 直接崩）。

逐字对照表、官方不变式原文、各形态 `files` 清单见 `07-conventions.md` 与 `08-cheatsheet.md`；客户端 bundle 的产物格式契约见 `14-inbound-http-and-timers.md` §17.3。

## 写代码前必读的八条红线

每条都来自官方事故复盘或社区真实提交，**违反任何一条都会被用户打回**：

1. **绝不写 `export default`** —— 函数式插件的头号杀手。
2. **可选服务一律用 `ctx.get('x')`，不用 `ctx.x`** —— 后者仅限已声明 `inject` 的服务；未声明就访问会 PENDING 或直接崩。
3. **手搓测试不算数** —— 必须用真实组合（真 profile、真加载）验证，不能只调函数单测。
4. **`!!js` 表达式只在 `config:` 与 `disabled:` 内求值** —— 写错位置会被当普通字符串。
5. **快照刷新 ≠ 正确性验证** —— 更新快照只是让测试通过，不代表行为正确。
6. **验收要指向「用户实际访问的那个 URL / 那个 profile」** —— 本地另一份配置跑通不算。
7. **别用 shell `&` 起后台进程** —— 用工具自己的后台机制，否则进程会随会话退出被杀。
8. **部分成功不能当成功返回** —— 操作了一半要如实报错，不能返回 success。

### 最容易写错的一处（`required` 有两条路径，规则相反）

这是本套手册调研中**发现并纠正的真实错误**：

- **`defineTool` 路径（DSH 自有 DSL）**：`required` 写在**属性级**，值为字面量 `true`。
  ```ts
  parameters: {
    questions: { type: 'array', required: true, description: '...' },  // ← 属性级
  }
  ```
- **裸 `ctx.tools.register` 路径（标准 JSON Schema）**：`required` 写在**对象级**，值为字符串数组 `required: ['a', 'b']`。

**两条路径规则相反，套错就静默失效。** 完整源码证据见 `05-pitfalls.md` 的坑 P7。

## 排查顺序

> **只问局部问题**（如「为什么我的 slot 崩溃」）时**不要重跑全流程**——直接按症状定位，改完只重跑受影响的验证。

1. 插件装上了但**完全没反应** → `06-workflow.md` 第 ④ 部分（`--dump-config` + PENDING 审计）
2. 报错信息看不懂 → `05-pitfalls.md` 的「报错信息 / 现象对照表」
3. 已知症状检索 → `05-pitfalls.md`（25 条坑，按症状编号 P1~P24）
4. 追根究底（原始社区提交、行号级出处）→ `10-community-casebook.md`（**总索引**，再进 `10a`~`10d` 对应方向分册）

## 端到端示例（一次完整的装配）

需求：「做一个插件，能敲一条命令查当前时间，也让模型能调用它。」

| 步 | 做什么 | 结果 |
|---|---|---|
| 0 | 版本闸门：确认目标版本 + 跑探针 | 探针退出码 0 |
| 1 | 选型：要「给人用」又要「给模型用」→ 都是**函数式插件** | 不是服务插件、不是组合包 |
| 2 | 路由：T5（命令）+ T3（工具） | 两者可以并存于同一个 `apply` |
| 3 | 最小闭环：先只写命令，让它能加载、能敲 | `export const inject = ['commands']` + `apply` 内注册 |
| 4 | 冒烟：装进真 profile，敲一次命令 | 有返回 = 链路通了 |
| 5 | 加第二个能力：工具走 `ctx.tools.register(defineTool({...}))`，`inject` 补 `'tools'` | 两个能力共用一个 `apply` |
| 6 | 可选：加 `export const Config`，让用户能调时区 | 改配置后行为变化 |
| 7 | 打包 → 安装 → **从最终分发源重装验收** | `dsh plugin --profile <名字> add <包>` |
| 8 | 留痕：把上述决策与验证结果写进 `docs/plan.md` | 可回放、可交接 |

⚠️ **合并多个模板时只有两条规则**：**`inject` 取并集**；**需要清理的副作用包进 `ctx.effect()` 并返回 disposer**（普通注册本身即 effect、会自动回收——见 `01-mental-model.md` §3.6，但显式 `effect` 更稳）。

## 交付前自检清单

逐项打勾；**打不了勾的项就是还没做完**。

- [ ] 形态选对了（函数式 / 服务 / 组合包），且**没有任何 `export default`**
- [ ] 版本闸门已过：三问答完 + 探针退出码 0（或已按降级规则声明未核验项）
- [ ] `inject` 覆盖所有用到的服务；可选服务走 `ctx.get('x')`
- [ ] 需要清理的副作用在 `ctx.effect()` 内并返回 disposer
- [ ] **合同不变量 5 条**全部满足（含名称三处一致）
- [ ] 每个能力面都有冒烟点，且**在真 profile 里**看到了实际输出 / 界面变化
- [ ] 没有手改 `lib/`（改的是 `src/`，且跑过构建）
- [ ] 打包产物齐全（`files` 含 patch 与 client；有静态资源也含）
- [ ] 失败路径试过：给坏输入 / 缺服务时报错能指向原因，而不是静默成功
- [ ] `docs/plan.md` 已按实际决策勾选完成（模板：`assets/plan-template.md`）

## 与 AI Agent 结对开发

用户常让 Agent 代写插件代码。此时：给 Agent 的提示词模板见 `09-agent-pairing.md`（两套来源共 10 个可直接复制的模板）；要求 Agent **每次附出处**（文件 + 行号），无出处不予采纳；交付后按 `07-conventions.md` 的门禁清单验收。

## 资源索引与加载条件

**默认只读本文件。** 上面 10 个步骤全部可以只靠 `SKILL.md` 完成；`references/` 是**触发才读**的加分项，不是必读项。

### 加载纪律（三条，先读再看表）

1. **不要为「保险」通读 `references/`。** 全量 **1.6 万行 / 24 篇 `.md`**（口径：本 `SKILL.md` ＋ `references/` 下全部 `.md`，实测 **15,994 行 / 24 篇**（复现：`wc -l SKILL.md references/*.md`）；中文字符 **14.9 万** + 英文及数字词 **8.4 万**，后者 = 剥离 CJK 后的 `[^\W_]+` 词数；**整个技能目录**含 README 与 `assets/` 则为 29 篇 / 1.7 万行），通读既装不下也不必要——这是本技能最贵的误用方式。
2. **按「读法」列执行，只有三种**：
   - **整读** —— 文件不大，直接整份读；
   - **定点读** —— 先 `grep -n '<锚点>' <文件>` 拿行号，再只读那一节（`Read` 带 `offset` / `limit`）；
   - **禁止整读** —— 只允许 grep 命中后定点读，整读会挤爆上下文。
3. **`references/` 里有两类内容，别把第二类当第一类读**：
   - **前段 = 面向任务的整理稿**（编号小节，可直接照做）；
   - **后段 = 一手素材档案** —— 标题带「（原始素材）」或紧跟 `<!-- ↓ 源：… -->` 标记，是整理稿的**上游原始记录**，比整理稿更细也更粗糙。**只在你需要追查某条结论的原始出处时才读它**，平时整段跳过。每个大文件头部都插了导航块，标出这段从哪开始。

### `references/`（按主题组织，共 23 篇：编号 `00`~`15` + `api-claims` + 6 个上游素材分册）

> 编号带字母后缀的（`02b`、`02c`、`10a`~`10d`）是**上游素材分册** —— 由超大引用文件按来源拆出，
> 内容为原文的逐行搬迁。它们**不是整理稿**：性质不一（既有官方文档逐字摘录，也有调研期粗笔记）。
> ⚠️ **例外**：`10b-casebook-tools.md` **不是逐行搬迁**（其余各册是）—— 它按**来源政策**定点改写：私有实现类条目不收录，通用教训以「自撰建议」形式保留。读它请连带读该册文件头的**许可警示**。

| 触发条件（满足才读） | 文件 | 读法 | 成本 |
|---|---|---|---|
| **写任何 DSH 代码之前**，回答版本三问；探针报 STALE 后 | `references/00-version-gate.md` | 整读 | 中 |
| 拿不准某条事实属 S/M/V/N 哪一级、该怎么核验 | `references/api-claims.md` | 定点：`grep -n '^### '` | 中 |
| 开始任何插件前；搞不清形态 / profile / 组合包加载机制 / 该选哪个模板 | `references/01-mental-model.md` | 整读 | 中 |
| **要抄代码时** | `references/02-templates.md` | **定点**：`grep -n '^## T[0-9]'` 取 T1~T12（纯整理稿，1.2k 行） | 中 |
| 要**逐字照抄官方 7 类模板**的完整源码 | `references/02b-official-templates.md` | 定点：册内 `grep -n '^## '` | 高 |
| 要一个社区零代码组合包全文范本 | `references/02c-community-bundle.md` | 整读（仅 255 行） | 低 |
| 写工具 / 配置 / 命令 / 事件 / 服务 / 终端功能 | `references/03-api-cookbook.md` | 定点：`grep -n '^## '` | 高 |
| 做 UI 插件或设置卡片 | `references/04-ui-and-slots.md` | 定点：`grep -n '^## '` | 中 |
| **写代码前通读整理稿**；出问题按症状检索 | `references/05-pitfalls.md` | 整读整理稿段；`grep -n '^### 坑 P'` 定位单条 | 中 |
| 环境准备 / 安装与 CLI 机制 / 打包分发 / 调试排错（四部分按需选读） | `references/06-workflow.md` | 定点：`grep -n '^## '` | 中 |
| 需要像官方包一样规范：README 强制节 / 门禁清单 / 命名 / 测试 | `references/07-conventions.md` | 定点：`grep -n '^## '` | 中 |
| **随手查**任何符号名（服务名 / 事件名 / 插槽名 / 命令 / CLI / 路径 / 参数 DSL） | `references/08-cheatsheet.md` | 定点：`grep -n` | 中 |
| 与 AI Agent 结对开发，需要可直接复制的提示词模板 | `references/09-agent-pairing.md` | 整读 | 低 |
| **追查某条结论的原始社区出处**（先在此定位方向） | `references/10-community-casebook.md` | 整读索引（仅 38 行） | 低 |
| 已定位到 **UI 方向**，要读该方向原始素材 | `references/10a-casebook-ui.md` | **定点**：`grep -n '^# [ABCD] · '` 定位小节 | 高 |
| 已定位到**工具 / 外部调用**方向 | `references/10b-casebook-tools.md` | **定点**：同上 | 高 |
| 已定位到**服务 / 状态内核**方向 | `references/10c-casebook-services.md` | **定点**：同上（该册用二级标题） | 高 |
| 已定位到**宿主 / 组合包**方向 | `references/10d-casebook-host-bundle.md` | **定点**：同上 | 高 |
| 查术语 / 素材代号对照（§A.2）/ 已知边界与官方文档矛盾 | `references/11-glossary-and-provenance.md` | 整读 | 低 |
| 选型参考；找可借鉴的社区高星插件 | `references/12-community-plugins.md` | 整读 | 中 |
| **目标 DSH 版本高于本技能基线时**（否则不读）；查 tag 版本史、破坏性变更 | `references/13-version-history.md` | 定点：`grep -n '^## '` | 中 |
| 要暴露 HTTP 接口 / 写定时任务 / 搞清客户端产物格式 | `references/14-inbound-http-and-timers.md` | 整读 | 中 |
| 评估本技能是否适用 / 要修改本技能（已知边界 + 维护守则） | `references/15-skill-scope-and-maintenance.md` | 整读 | 低 |

> 「成本」= 一次装载的上下文代价，粗分低 / 中 / 高 / 极高。**只有标「禁止整读」的那个才真的不能整读**，其余按需选读即可。

### `assets/`（可直接复制 / 改名，**不进上下文**）

| 何时复制 | 目录 | 形态 |
|---|---|---|
| 只是把已有插件装到一起 | `assets/minimal-bundle/` | 零代码组合包（T1），0 行 JS |
| 要加工具 / 命令 / 事件（**绝大多数情况**） | `assets/minimal-tool-plugin/` | 最小工具插件（T3），`defineTool` + 参数 Schema |
| **每次开发都建议做**（决策留痕与交接） | `assets/plan-template.md` | 复制到插件项目的 `docs/plan.md` |

> `assets/` 是**产出物**不是文档：它们会被复制进用户工程，所以**不要改成「说明本技能」的口吻**，要写成「说明这个插件」的口吻。改动后必须过 WSL 真机核验（它们要被真实 DSH 组合器接受）。

### `scripts/`（确定性工具，**跑它而不是读它**）

「必须跑的时机」列是硬要求——跳过对应核验会直接产出坏代码：

| 必须跑的时机 | 脚本 | 用法与退出码 |
|---|---|---|
| **写任何 DSH 代码之前**（强制，与版本闸门是同一件事） | `dsh-api-probe.py <仓库路径>` | 核验 48 正向 + 8 反向断言。`0`=全成立 / `1`=有 STALE（**不要照抄**）/ `2`=路径错 / `3`=断言表空（结果无效）。纯标准库、零外部命令依赖，**首选** |
| 同上，但仅在 shell 有完整 coreutils 时 | `dsh-api-probe.sh <仓库路径>` | 断言表须与 `.py` 版同步；**缺 `grep` 会报几十条假 STALE**，拿不准就用 Python 版 |
| 用到**入站 HTTP / 定时器 / 客户端产物 / 插槽**任一项 | `verify_absorbed_claims.py <仓库路径>` | 54 条第二批断言。**先跑 `--selftest` 证明它能失败**，再跑正向 |
| **要写插槽名之前**（不要凭表抄） | `extract_slots.py <仓库路径> <skill目录>` | 从源码抽**权威插槽清单**并双向 diff |
| **改过本技能的任何文档或资源之后** | `check_refs.py <skill目录>` | 悬空引用 / 生成期素材路径 / 本机绝对路径；`0`=全部可在技能内解析 |
| **改动任何来源标注 / 许可声明 / `NOTICE` / `licenses/` 之后**（发版前必跑） | `check_oss_license.sh`（在技能根目录跑） | 5 项：copyleft 关键词扫描（只对**未声明**的文件判失败）、**五个声明文件齐备**（`LICENSE` · `NOTICE` · `licenses/` 下 Apache-2.0 / MIT / BSD-3-Clause 三份正文）、`LICENSE` 来源表与 `NOTICE` 条目数一致、无「待逐字核取」占位符、`NOTICE` 行尾为 LF。`0`=PASS 可对外分发。**它是「已逐文件核实」这句话的可复现证据** |
| 目标版本高于基线，且需要本地源码 | `dsh-sync.sh` | 把 DSH 源码拉进技能目录（`vendor/dsh-src/`）。首次约 200 MB，**必须先经开发者确认**；**绝不执行 pnpm install** |
| 目标版本高于基线，要看上游到底改了什么 | `dsh-version-diff.sh <仓库路径>` | 六维度差异 + 作者自报的 `!:` 破坏性提交；输出可追加到 `13-version-history.md` |
| 质疑「API 名是否稳定」这类**历史结论**时 | `dsh-tag-matrix.sh <仓库路径> [out.tsv]` | 对全部 tag 逐条核验 API 面 |

### 检索配方（**不要整读，先检索**）

```bash
grep -rn "ctx.slots.inject" references/                    # 某个 API 名出现在哪
grep -n '^## T[0-9]' references/02-templates.md            # 定位某个模板（T1~T12）
grep -n -A 40 "^### 坑 P7" references/05-pitfalls.md       # 某个坑的全文（按编号）
grep -rn '^#\{1,2\} [ABCD] · 一、' references/            # 四个素材方向各有哪一册（档案册）
grep -n '（原始素材）' references/05-pitfalls.md            # 找「整理稿 → 上游素材」的分界
```
