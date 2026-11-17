<!-- 手工维护文件。与本文件对应的是 scripts/dsh-api-probe.sh 的断言表 —— 改这里也要改那里。 -->

# API 声明登记表（本 skill 依赖的易变事实）

> **用途**：本 skill 的每一条「关于 DSH 的断言」都登记在这里，标注易变性等级、基线写法、源码位置、核验方式。
> **基线**：commit `f3803c9697` / `dsh-v0.2.2-alpha.2`（2026-10-28）。
> **探针**：`scripts/dsh-api-probe.py`（首选，零 coreutils 依赖）与 `scripts/dsh-api-probe.sh`（备选）。
> **两份探针的断言表必须逐条一致**；被核验的断言数 = **56 条（48 正向 S/M/L + 8 反向 N）**。
> **核验结果（2026-09-18 实测，对新基线 tag `dsh-v0.1.6-alpha.2` 的检出）**：`total=56 holds=56 stale=0`，`exit 0`。
> **负向证明（历史实测，对 `dsh-v0.1.6-alpha.1` 的检出）**：`holds=47 stale=7 skipped=2`、`exit 1` —— 那 7 条 STALE 正是 `1.1.0` 新增/改写的断言（`M11`/`M35`/`M36`/`M37`/`N06`/`N07`/`N08`），证明它们**能失败**，不是恒真装饰。
> **第二批断言**：`scripts/verify_absorbed_claims.py`，随 `dsh-v0.1.7-rc.1` 由 **39 条扩到 49 条**（先修 4 条判据缺陷、再加 `P06`/`P07`/`U09`/`U10`/`V01`/`X07`，1.5.0 轮又加 `U11`/`U12`/`X08`/`X09`，**本轮（alpha.4）再加 `E` 组 3 条** `E01`/`E02`/`E03`，口径同时修正为 **54 条**）。**负向自检 `54/54 STALE`、正向 `54/54 HOLDS`（2026-10-16 实测，两个退出码均为 0）**。
> ⚠️ **2026-10-16 修正一处既有文档缺陷**：本条此前一直写 **49 条**，而脚本**实际一直是 51 条**（`H`5 + `T`4 + `B`13 + `U`12 + `P`7 + `V`1 + `X`9）—— 差在 §7.2 的分组表把 `B` 组少记 2 条、`U` 组少记 2 条，又**多列了一个早已不存在的 `G` 组**（其 2 条实为 `U11`/`U12`，随设置机制重做一起并进了 `U`）。复现：`grep -oE "^(  )?(HOLDS|STALE) +[A-Z][0-9]+" <日志> | grep -oE "[A-Z][0-9]+$" | sed -E 's/^([A-Z])[0-9]+/\1/' | sort | uniq -c`。**改检查器后必做可失败性探针**（硬规则 6）：本轮 `--selftest` 仍为 `54/54 STALE`。
> **编号提示**：本表的 `M` 编号是**本表自己的**连续编号，**与探针 `dsh-api-probe.py` 的 `M` 编号不是一套**（例：本表 `M20` = 探针 `M11`）。两套编号各自连续、互不引用，对照时请按「结论文字 + 核验方式」匹配，不要按编号。新增条目会在「核验方式」列标注探针 ID。
> **怎么用**：写代码前按 ID 或等级检索；探针 `scripts/dsh-api-probe.sh` 会逐条核验 S / M / L / N 级。
> **四个维度**：S/M/V（易变性，越高越易变）+ **N（极性，否定性论断）**。N 级是本表唯一一类「语义反向」的条目，见第五节。
> **怎么维护**：探针报 STALE → 改本文件对应行 → 同步改探针断言表 → 重跑探针。见 `00-version-gate.md` 第 7 节。

⚠️ **「源码位置」里的行号只记录基线时刻的位置。行号必然漂移，核验时必须按符号名 grep，不要按行号找。**

---

## 一、S 级 · 结构性公理（可直接用）

| ID | 基线写法 / 结论 | 源码位置（基线时） | 核验方式 |
|---|---|---|---|
| S01 | **服务插件**用 default export 导出服务类；**函数式插件**具名导出 `name`/`inject`/`Config`/`apply`，**不得有 default export**。混用会让 Loader 丢弃函数式插件的命名空间 | `packages/AGENTS.md:5` | `grep -n "default-export" packages/AGENTS.md` |
| S02 | 上述规则的完整事故复盘在档 | `docs/postmortem/0001-acp-default-export-drops-inject.md` | 文件存在性 |
| S03 | 服务类继承形态：`class X extends Service`（`Service` 来自 cordis；也可继承领域基类，如 `export abstract class DirectoryPicker extends Service`） | `packages/host/directory-picker/src/index.ts:103` | `grep -rn "extends Service" packages` |
| S04 | **补丁行的书写顺序不影响加载顺序** —— 激活由「服务可用性」驱动 | `packages/bundle/base/cordis.patch.yml`（注释） | `grep -rn "Row order carries no load semantics" packages` |
| S05 | **纯配置组合包**的 `src/index.ts` 只是占位，不承载任何运行时 API | `packages/bundle/base/src/index.ts`（全文 9 行，仅 `export {}`） | `grep -n "export {}" packages/bundle/base/src/index.ts` |
| S06 | 官方 `base` 补丁是 `!!js` 用法的完整范本；**`!!js` 只在 `config:` 与 `disabled:` 内求值**，写在别处**静默失效**（不报错） | `packages/bundle/base/cordis.patch.yml` | `grep -rn "!!js" packages/bundle/base` |
| S07 | **`config` 是整段替换，不是深合并** —— 覆盖时必须重述整个 config | 同上（注释） | `grep -rn "replaces the targeted row" packages` |

---

## 二、M 级 · 接口名（**每次使用前必须核验**）

### 工具（Tools）

| ID | 基线写法 / 结论 | 源码位置（基线时） | 核验方式 |
|---|---|---|---|
| M01 | `defineTool` 从 `@deepseek-ai/dsh-tools` 具名导出 | `packages/core/tools/src/schema.ts` | `grep -rn "export function defineTool" packages` |
| M02 | **`parameters` 的必填写在属性级**：`ParameterPropertySpec = ValueSchemaSpec & { required?: true }`；参数 schema 的根是**隐式开放对象** | `packages/core/tools/src/schema.ts:97-107` | `grep -rn "ParameterPropertySpec" packages` |
| M03 | 属性级写错（值不是 `true`）时的报错文案：`.required must be true when present` | `packages/core/tools/src/schema.ts:293-296` | `grep -rn "required must be true when present" packages` |
| M04 | **裸 `ctx.tools.register` 走标准 JSON Schema，`required` 写在对象级且必须是字符串数组** —— 与 M02 规则相反，套错必报错 | `packages/core/tools/src/schema.ts` | `grep -rn "required must be an array of strings" packages` |
| M05 | `DefineToolOptions` 接口（`name`/`description`/`parameters`/`output{schema,render}`/`timeoutMs`/`isConcurrencySafe`/`execute`…） | `packages/core/tools/src/schema.ts:483-537` | `grep -rn "interface DefineToolOptions" packages` |
| M06 | 注册入口 `ctx.tools.register(...)`；是副作用，卸载时自动注销 | `packages/core/tools/src/schema.ts:571-572` | `grep -rn "tools.register(" packages` |
| M07 | 保留工具名 `run_code` 不可使用 | `docs/subsystems/tools.zh.md:645` 等 | `grep -rn "run_code" packages` |
| M08 | `timeoutMs` 必须是正有限数，否则报 `timeoutMs must be a positive finite number` | `packages/core/tools/src/schema.ts` | `grep -rn "timeoutMs must be a positive finite number" packages` |

### 命令 / 服务 / 插槽 / 事件

| ID | 基线写法 / 结论 | 源码位置（基线时） | 核验方式 |
|---|---|---|---|
| M09 | 命令注册：`ctx.commands.register({...})` | `packages/interaction/...`（`commands.register(` 全仓命中） | `grep -rn "commands.register(" packages` |
| M10 | 服务插件构造函数首行：`super(ctx, '服务名')` | 例 `packages/host/directory-picker-browse/src/index.ts:187` | `grep -rn "super(ctx, '" packages` |
| M11 | 取可选服务用 `ctx.get('名字')`（拓扑无关）；`ctx.x` 仅限已声明 `inject` 的服务 | 全仓 | `grep -rn "ctx.get(" packages` |
| M12 | 副作用回收：`ctx.effect(setup, label)`，setup 返回 disposer | 例 `packages/acp/acp/src/index.ts` | `grep -rn "ctx.effect(" packages` |
| M13 | waterfall 放行约定：`await next()` | 全仓 | `grep -rn "await next()" packages` |
| M14 | UI 插槽 API：`ctx.slots.inject(name, fn)` / `ctx.slots.register({name,...}, 组件)` | 例 `packages/client/ui-chat/src/client/contract/slots.ts` | `grep -rn "slots.\(inject\|register\)(" packages` |
| M15 | 高频插槽名（**基线枚举，非全集**）：`settings.section`、`conversation.view`、`tool.call.toolview` | `packages/bundle/base/cordis.patch.yml`、`packages/client/ui-chat/src/client/apply.ts`、`packages/client/ui-deliverables/src/client/index.ts` | 逐个 grep |
| M16 | Agent 流程事件（waterfall）：`agent/pre-step`（进入 step 前唯一的监听链）、`agent/request`（替换冻结调用配置，不能改消息）、`agent/turn-stopping` | 例 `packages/compaction/compaction-basic/src/index.ts`、`packages/core/agent/src/model-selection.ts` | 逐个 grep |
| M17 | 其它高频事件：`llm/stream`、`system-prompt/assemble`、`approval/request` | 例 `packages/llm/llm/src/index.ts:75`（`llm/stream`）、`packages/core/system-prompt/src/index.ts:31`（`system-prompt/assemble`）、`packages/interaction/user-approval/src/index.ts:308`（`approval/request`）；⚠️ 旧文引的 `packages/core/agent-loop/src/invariant.ts` 已在 `0.2.1-alpha.1` 随 `dsh-invariants` 包一并删除 | 逐个 grep |

### 清单 / 加载 / CLI / 路径

| ID | 基线写法 / 结论 | 源码位置（基线时） | 核验方式 |
|---|---|---|---|
| M18 | 组合包清单字段：`"dsh": {"bundle": {"patch": "./cordis.patch.yml"}}` | 各包 `package.json` | `grep -rn "dsh\.bundle" packages` |
| M19 | 缺清单字段时的警告：`declares no dsh.bundle` | `packages/boot/app-boot/src/profile.ts` | `grep -rn "declares no dsh.bundle" packages` |
| M20 | **补丁行 `id` 重复不再报错、也不再拦截** —— `EntryGroup.update()` 已删掉重复 id 的 `TypeError` 校验，两个同 id 的行会在 `oldMap`/`newMap` 里互相覆盖（后者胜）。**这是 0.1.6-alpha.1 的行为变化**，旧写法「启动即崩」已不成立 | `vendor/loader/src/config/group.ts`（`update()` 内已无 `seen` 校验） | `grep -rn "duplicate loader entry id" vendor` **应 0 命中**；人工确认见 §5.2 |
| M20b | 加载器**非事务化**：`EntryTree.await()` 只等待、**不再因某个 fiber 失败而拒绝**；`Entry.update()` 失败只写日志。**推论：`Loader.create()` 返回 ≠ 插件已激活**，调用方必须自行审计 | `vendor/loader/src/config/tree.ts`、`group.ts`、`entry.ts` | 探针 `M11`：`grep -rn "Wait until this tree has no pending import" vendor/loader`；决策记录 `.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md` |
| M21 | 补丁内相对路径被**锚定到补丁文件所在目录** | `packages/boot/app-boot/src/index.ts`（`anchorInsertedPluginNames()`） | `grep -rn "anchorInsertedPluginNames" packages` |
| M22 | `dshHomePath()` 路径辅助函数（用于 `!!js` 内） | `packages/boot/app-boot/src/index.ts` | `grep -rn "dshHomePath" packages` |
| M23 | 环境变量 `DSH_HOME` | 全仓 | `grep -rn "DSH_HOME" packages` |
| M24 | 配置树导出开关 `--dump-config` | `apps/cli/README.md`、`packages/boot/app-boot/README.md` | `grep -rn -- "--dump-config" apps` |
| M25 | 插件安装 CLI：`dsh plugin --profile <名字> add <包>`（pnpm 转发器；实现已移入 plugin-manager 包，CLI 只剩转发） | `packages/boot/plugin-manager/src/operations.ts`（入口 `apps/cli/src/plugin.ts`） | `grep -rn "runPluginCommand" apps packages` |
| M26 | 子进程凭据清洗：`SENSITIVE_ENV_PATTERN = /KEY\|PASSWORD\|SECRET\|TOKEN/i`，且删除所有 `DSH_*`。**要传的凭据必须在 `env:` 里显式列出** | `packages/subprocess/subprocess/src/index.ts` | `grep -rn "SENSITIVE_ENV_PATTERN" packages` |

---

## 三、V 级 · 实现细节（**故意不做断言**）

这些事实**变化最快**，写进代码会自己坏掉。探针不断言它们——因为一断言就会天天报假警，最后没人信任探针。

| 事实类型 | 基线时刻的值 | 为什么不断言 / 该怎么用 |
|---|---|---|
| 官方斜杠命令清单 | 基线时约 6 个（含 `/compact`、`/permission`、`/plan`、`/goal` 等） | **枚举会增长**。需要用就现场 `grep -rn "commands.register(" packages` 或看 `dsh` 的 `/help` |
| UI 插槽总数与全清单 | 基线时**只提取到 40 个**（**低估**——`slots.inject/register` 的正则抓不到内建键；2026-09-11 重抽为 75 个声明侧键 / 约 59 个公开可用；**2026-09-16 对 0.1.6-alpha.1 重抽为 77 个声明侧键 / 并集 79 / 约 61 个公开可用**） | 数量会变。要用就用 M14 的方式现场枚举，或跑 `<skill>/scripts/extract_slots.py` |
| `$DSH_HOME` 默认值 | 基线时为 `~/.dsh` | 默认值可被改。要么读 `DSH_HOME` 环境变量，要么运行时确认 |
| profile 目录布局 | `$DSH_HOME/profiles/<名字>/`，已装插件在 `profiles/node_modules/` | 布局可能调整。用 `dsh plugin --profile <名字> ls` 现场确认 |
| 报错文案的细节措辞 | 见 M 级各条 | 只把**关键片段**当断言（如 `required must be true when present`），**不要断言整句**。⚠️ 反面教材：`duplicate loader entry id` 这条文案在 0.1.6-alpha.1 上**整条消失**了（校验被删），见 M20 |
| 源码行号 | 本文件记录的均为基线时刻位置 | **行号必然漂移。** 核验只按符号名 grep |
| 各字段默认值（`timeoutMs` 等） | — | 不要假设默认值，显式写出你要的值 |
| 包的内部文件布局 | 如 `src/index.ts`、`src/client/index.ts` | 新建插件时以官方同级包为参照，不要照抄记忆里的路径 |

---

## 四、L 级 · 仓库布局（探测用）

| ID | 结论 | 核验方式 |
|---|---|---|
| L01 | `packages/AGENTS.md` 是官方插件工程约定的入口 | 文件存在性 |
| L02 | `vendor/loader/src/` 是加载器与配置校验实现 | 文件存在性 |
| L03 | `apps/cli/src/plugin.ts` 是 `dsh plugin` 的 CLI 入口（转发层）；对账实现是 `packages/boot/plugin-manager/src/operations.ts` | 文件存在性 |
| L04 | `packages/bundle/base/cordis.patch.yml` 是官方最完整的补丁范本 | 文件存在性 |
| L05 | 顶层布局：`packages/`、`vendor/`、`native/`、`apps/`、`docs/` | 目录存在性 |
| L06 | `docs/postmortem/` 存放事故复盘（0001~0004 已读） | 目录存在性 |
| L07 | `.agents/notes/` 存放设计决策与 bug 修复笔记（含中文版） | 目录存在性 —— **挖「为什么这么设计」的最佳去处** |

---

## 五、N 级 · 否定性论断（「没有 X」「不用 Y」）

**为什么单列一级**：本 skill 有相当一部分结论是**否定形式**的——「仓库没有 CHANGELOG」「提交不用 `BREAKING CHANGE:` 页脚」「不存在 TUI 前端包」。

它们同样会过时，而且**过时的方向是反的**：

- 正向断言过时的表现是「东西**消失**了」→ 探针搜不到 → STALE。
- 否定断言过时的表现是「东西**出现**了」→ 上面那套机制**完全抓不到**（搜不到反而被判定为成立）。

本 skill 曾因一条**错误的否定论断**（「DSH 不用 `!` 标记破坏性提交」——实际有 21 条）误导过整份文档，所以专门引入反向断言。**这是本表最容易被忽视的一类。**

### 5.1 已纳入探针自动核验（8 条）

> 语义与正向**相反**：**未命中 = HOLDS**（否定成立）；**命中 = STALE**（否定已被推翻）。
> 下表「若被推翻会看到什么」一列，写的就是探针要搜的证据。

| ID | 否定论断 | 若被推翻会看到什么（= 探针搜索的证据） | 探针模式 |
|---|---|---|---|
| N01 | 仓库**没有 CHANGELOG 文件** —— 变更史只在 git 与 `.agents/notes/` | 出现 `CHANGELOG*` 文件 | `nf:CHANGELOG*` |
| N02 | 提交**不使用 `BREAKING CHANGE:` 页脚**（只用 `type(scope)!:` 标题标记） | 任一提交的标题或正文含 `BREAKING CHANGE` | `nl:BREAKING CHANGE` |
| N03 | **不存在 `packages/ui/`**（TUI 前端包已归档） | 该目录重新出现 | `nd:ui`（scope=packages） |
| N04 | **版本号不连续**：不存在 `0.1.4` | 出现含 `0.1.4` 的 tag | `nt:0\.1\.4` |
| N05 | **不采用 changesets 发布流程**（无 `.changeset/`） | 出现 `.changeset/` 目录 | `nf:.changeset` |
| N06 | 旧服务名 **`ctx.codeRuntime` 已无兼容别名**（改名后旧名彻底消失） | `packages/` 下任一文本再出现 `ctx.codeRuntime` | `na:ctx\.codeRuntime`（scope=packages） |
| N07 | 事件 **`agent/session-start` 已被 `agent/created` 取代** —— 后者由 `emit` 改成 **`serial`**（监听器被 `await`，抛错会让创建失败） | 源码里再出现 `agent/session-start` | `na:agent/session-start`（scope=packages） |
| N08 | **E2B 执行后端已整体移除**（`dsh-e2b` / `fs-e2b` / `subprocess-e2b` 三包与 SDK 依赖） | 源码里再出现 `@deepseek-ai/dsh-e2b` 包名 | `na:deepseek-ai/dsh-e2b`（scope=packages） |

新增一条 N 级断言的写法：在探针断言表里加一行，格式同其它行，模式用
`nf:`（文件名）/ `nd:`（目录）/ `nt:`（git tag）/ `nl:`（git log 提交信息）/ **`na:`（文本内容，2026-09-16 新增）**，
**payload 写「否定被推翻时会出现的证据」**。

> **`na:` 为什么必须存在**：前四个模式只能否定「文件 / 目录 / tag / 提交信息」的存在，
> 而本轮三类最重要的否定结论——「旧服务名无别名」「旧事件名被取代」「某后端整体移除」——
> 的过时方向都是**内容里又冒出了旧字符串**。缺了 `na:`，这三条只能落到 §5.2 的人工复核里。

### 5.2 只能人工复核（无法自动核验，附理由）

这些同样是「否定 / 行为」类结论，但**依赖 skill 之外的信息或运行时行为**，探针做不到。
**每次上游新版本时，5.1 由探针核对，5.2 需要人来判断** —— 这是本表唯一需要人工介入的部分。

| 论断 | 为什么不能自动 | 人工复核方式 |
|---|---|---|
| 官方**文档**没有随仓库提交插槽键完整清单 | skill 内没有官方文档副本，且官方文档会更新 | ✅ **2026-09-23 复核：已有更好的权威源，且原前提是错的** —— `pnpm run gen-client-catalog` 的**产物其实早已入库**：`packages/extensions/cordis-client-runner/src/client/slot-catalog.ts`（引入于 `4064198560`，2026-08-13；由 `verify-client-catalog` 守新鲜度），给出**客户端半侧完整清单**（`0.1.7-rc.1` 实测 **86 个**，带 kind/scope/owner props）。`scripts/extract_slots.py` 的 **A2 段现在自动与它交叉核对**，漏抽量应为 0。**仍需人工的只剩**：宿主侧是否也有同类生成产物。⚠️ 另注：上游文档写的 `cordis_inspect what:"client"` 是**旧简写**，实际工具为 `cordis_inspect_list` / `cordis_inspect_query`（`packages/extensions/tool-cordis/src/index.ts:23,42`） |
| ✅ **2026-10-16 复核（结论被收窄，不是推翻）**：生态**仍**没有**官方**插件市场，但**「生态里没有市场机制」已不成立** —— 自 `dsh-v0.2.1-alpha.4` 起官方**随仓库交付**了读取器 / Discover 页 / agent 工具 / 插槽（见下一行）；上游原文两处明写「**目前没有官方市场**，因此 DSH 无法随附默认源；**索引源属于用户数据**」（`.agents/notes/implemented/feature/2026-10-02-plugin-market-discover.zh.md:9`、`…-plugin-market-index-format.zh.md:9`）。**发现机制仍以 GitHub topic `dsh-plugin` 为主** | 生态事实 + 仓库内机制，**两者都要看** | ① 查 GitHub 是否出现官方 marketplace **仓库**；② 查 `packages/boot/plugin-market/` 是否被加进 **base 补丁**（若加进去，「无默认源」也随之失效） |
| 🔴 **官方插件市场机制已在仓库内**（`dsh-v0.2.1-alpha.4` 新增，**本表本轮新登记**） | 可直接对源码核验 | 服务 `pluginMarket`（`packages/extensions/tool-cordis/src/api-catalog.ts:2280`）· 事件 `plugin-market/changed`（`api-catalog.ts:4409-4411`，emit 于 `packages/boot/plugin-market/src/index.ts:167`）· agent 工具 `plugin_market`（`packages/boot/plugin-market/src/tools.ts:72`）· 插槽 `plugins.tab`（`packages/client/ui-plugin-manager/src/client/slot-contract.ts:124`）· 新增 4 个包 · 🔴 **不在 base 补丁里** → 不装 `plugin-market-bundle` 就没有市场面。与上一行是**同一轮、同一事实的两面**：机制存在（本条）／官方市场不存在（上一行）；`E01`~`E03` 覆盖同一轮的插件兼容变更 |
| 官方文档存在**两处内部矛盾** | 需人工阅读理解 | 重读 `11-glossary-and-provenance.md` 记录的矛盾点是否被官方修正 |
| `!!js` 写在 `config:`/`disabled:` 之外**静默失效（不报错）** | 运行时行为，静态搜不出来 | 写一个错位用例实跑一次 |
| 未声明 `inject` 就访问 `ctx.x` 会 **PENDING 或崩** | 同上 | 同上 |
| 补丁行应用失败**不回滚**、失败行留在树上（0.1.6-alpha.1 起） | 加载器行为，静态搜不出来 | 造一个 `apply()` 抛错的插件行：看该行是否仍在 `--dump-config`、日志是否只有一条 error 而无回滚 |

---

## 六、探针自身的可信度（**不是关于 DSH 的断言，而是关于本 skill 的**）

探针报「全部成立」是一种**权力**——它会让使用者放心照抄。因此「不能失败的探针」比「没有探针」更危险。

### 6.1 已修正的三处假通过（本项目实际发生）

| # | 症状 | 根因 | 现状 |
|---|---|---|---|
| 1 | bash 版 `total=0` 却报「✅ 全部断言成立」并 `exit 0` | `CHECKS=$(cat <<'EOF'…)` 在缺 `cat` 的 shell 里静默展开为空 | 已改内联字符串 + 空表哨兵（`exit 3`） |
| 2 | Python 版 2 条假 STALE（样本明明存在） | `scope` 可指目录也可指**文件**，代码只按目录处理 | 遍历函数已支持单文件入口 |
| 3 | 本机 bash 报 37 条假 STALE | 该 bash 缺 `grep`/`head`/`find` | 改用纯 Python 探针；bash 版降为备选并在 SKILL.md 标注「本机勿用」 |

**共同模式**：失败形态不是报错，而是**静默给出一个看起来正常的答案**。三次都发生在「环境能力缺失」或「输入形态超出假设」时。

### 6.2 强制自检（每次改探针后必跑，步骤详见 `00-version-gate.md` 第 9 节）

| # | 场景 | 期望 |
|---|---|---|
| 1 | 正向：真实仓库 | `stale=0`，`exit 0` |
| 2 | 负向-路径：传 `C:\Windows` | `exit 2`，提示「看起来不是 DSH 仓库」 |
| 3 | 负向-断言：临时骨架中塞入 `CHANGELOG.md` + `packages/ui/` | `N01`/`N03` 报 STALE，`exit 1` |
| 4 | 空表：断言表置空 | `exit 3`，**不得**报成功 |

第 3 步是唯一能验证「否定性结论的兜底机制真的接上了」的手段，最容易被跳过。

### 6.3 断言表维护纪律

- `.py` 与 `.sh` 两份断言表**逐条一致**（等级 / 说明 / 模式 / 作用域全同），改一份必须同步另一份。
- 改断言前，**先用已知存在的样本验证正则本身**（`grep` 是 ERE，Python 是 `re`，转义不通用）。
- **V 级事实一律不许进断言表**。判据：这条事实明天变了，会让本 skill 的指引失效吗？不会 → 不进表。

---

## 七、第二批断言：入站 HTTP / 定时器 / 客户端产物 / 插槽（**独立核验器**）

> 追加于 2026-09-11（v1.0.1）。来源：调研同类方案 `dsh-plugin-studio` 时发现它提供的代码大面积不可用，于是把它**自称能做的事**逐条对源码重做核验；能核验的才吸收，核验不过的一律写成反面教材（见 `14-inbound-http-and-timers.md` §17.5）。

### 7.1 为什么单开一个核验器，而不是并进 `dsh-api-probe.py`

| 维度 | `dsh-api-probe.py` | `scripts/verify_absorbed_claims.py` |
|---|---|---|
| 覆盖面 | 本 skill 核心骨架（56 条，全仓级） | 第二批 54 条（指定文件级） |
| 失败信号 | `exit 1` 表示某条 M/S 事实漂移 | 同上 |
| 分开的理由 | 「56 条」这个数字被 SKILL.md、README、发布清单多处引用；并表会让**一个纯增量的动作**引发全库数字同步，制造无关的改动面与风险 | 保持主探针稳定；新事实独立可复跑 |

**代价（如实声明）**：现在有**两个**核验入口，改 DSH 基线时要跑两个。这是有意识的取舍——用「多跑一条命令」换「主探针数字不被动摇」。

### 7.2 本轮核验通过并已写入 `14-*.md` 的断言（54 条）

核验器自带**负向自检**（对空仓库跑同一张表，要求 54/54 全 STALE），因为一张全是「X 不存在」的断言表在空语料上会**全部假通过**——这一点在开发本核验器时**真的发生了**（首版 5 条否定断言在空仓库上 HOLDS），修法是给每条否定断言加**护栏模式**（必须同时命中一个必然存在的样本，证明语料读到了）。

> ⚠️ **2026-10-16 更正**：下面这张分组表此前把 `B` 记作 11、`U` 记作 10，并**多列了一个 `G` 组（2 条）**，合计 49 —— 而脚本**实际一直是 51 条**（`G` 组从未存在；那 2 条是 `U11`/`U12`，随设置机制重做并进了 `U`）。本轮加 `E` 组 3 条后为 **54**。**「文档写 49、脚本跑 51」这种静默漂移，正是硬规则 12「条数必须从唯一真源推导」要防的东西**；本表的条数现已与脚本 `CHECKS` 表逐组对齐。

| 组 | 条数 | 代表断言 | 级别 |
|---|---|---|---|
| H · 入站 HTTP | 5 | `register(route: WebRoute): () => void`；`WebRoute` 三字段；`webServer` 由 Web 组合的 `id: webserver` 行提供 | S/M |
| T · 定时器 | 4 | `ctx.interval(cb, delay)` 返回 disposer；handle 绑 fiber 自动清；`ctx.setInterval` 仅 deprecated 别名 | S/M |
| B · 客户端产物 | 13 | lazy-CJS factory 的 banner（**按 chunk 生成，非入口多带 `chunk` 字段**）/intro/footer；`lib/client.js`；分块名 `client.<name>.js` 与 `require.async`；平台模块种子表 9 项；仓库外无已发布预设；**`dualClient` 的 Node 面产物 `client.node.js`**；**`staticLinked` 通道与 `isStaticLinkedConfig`**（后 2 条为 `B12`/`B13`） | S/M |
| U · 插槽 | 12 | `register(options, component)`；未声明 slot 的报错原文；`root` 是内建键；`ui-layout` 可禁用；**`plugins.item` 为 list、`plugins.bundle.config`/`plugins.row.config` 为 keyed**；组件收 `view` 两态；**`plugins.bundle.activation`（keyed）与 `plugins.detail.section`（list）已声明**；**`settings` 服务改为 `SettingsForms`（`U11`）+ 乐观并发码 `SETTINGS_CONFLICT`（`U12`）—— 后 2 条即此前误记为独立 `G` 组的那两条** | S/M |
| P · 基线推进（`alpha.2` 新增） | 7 | base 补丁 hmr 行改用 `@deepseek-ai/dsh-hmr`；官方 README 明写只换模块名；base 补丁新增 `plugin-manager` / `tool-plugin-manager`；CLI 转发给 `dsh-plugin-manager/operations`；bundle 对账实现与警告文案；**`DefineToolOptions.deferLoading`**；**`projectContent(exec, result)`** | M |
| V · 数据格式版本 | 1 | `SESSION_FORMAT_VERSION = 4`（0.1.7 起；0.1.5～0.1.6 为 3） | M |
| E · 插件兼容（`alpha.4` 新增） | 3 | **`engines.dsh` 命中即单独判定、不再看 peer 范围**（`E01`）；**`IncompatiblePlugin.requirements` 取代 `peers`**（`E02`）；**否定**：`peers` 字段已从该接口体内移除（`E03`，判据收紧到**接口体内**而非裸关键词 —— 测试文件里 `peers:` 是形参名） | M/N |
| X · 否定（防编造） | 9 | 不存在 `ui` 服务；不存在裸 `settings`/`status`/`workspace` 插槽键；`webServer.register` 不收 router 回调；**`settings.plugin.item` 不再被声明为插槽**；**`conversation.session.header.leading` 已移除**；**`installSection` 已整体移除**；**`SettingsScope` 已整体移除** | N |

### 7.3 本批**修正**的既有表述（原文错了，已改）

| # | 位置 | 原表述（错） | 现状（核验后） |
|---|---|---|---|
| 1 | `02b-official-templates.md`（2 处）、`05-pitfalls.md`（1 处） | 浏览器半侧「平台种子表允许的**四个**：`react` / `cordis` / `ui-slots` / `ui-primitives`」 | 种子表实为 **9 个 specifier**，且是**全名**（含 `react-dom`、`react-dom/client`、`@deepseek-ai/dsh-client-store`、`@deepseek-ai/dsh-client-ui-dockkit`）；另有 `dsh.client.external` 可追加请求。以 `packages/client/web/src/platform.ts:8-14` 为准 |
| 2 | `02b-official-templates.md` 插槽清单标题 | 「官方全部 UI 插槽名（**40 个**，实测提取）」 | 实为 **75 个声明侧键**（并集 77；剔除 18 个测试专用键后**约 59 个公开可用** —— 2026-09-16 对 0.1.6-alpha.1 重抽为 **77 / 79 / 约 61**；2026-09-18 对 0.1.6-alpha.2 再抽为 **81 / 84 / 约 66**；**2026-09-23 对 0.1.7-rc.1 重抽为 121 / 123 / 约 86**；**2026-09-25 对 0.1.7-rc.2 再抽为 124 / 126 / 约 89**（+3 / −0）；**2026-09-29 对 0.2.0-rc.1 再抽为 124 / 126 / 约 89**（+0 / −0，客户端权威目录 `slot-catalog.ts` 89 → 89）；**2026-09-30 对 0.2.0-rc.2 再抽为 125 / 127 / 约 90**（+1 / −0，`slot-catalog.ts` 89 → 90；新增键 `sidebar.right.tab.files.actions`）；**2026-10-04 对 0.2.1-alpha.1 再抽为 127 / 129 / 约 92**（+2 / −0，`slot-catalog.ts` **90 → 92**；新增键 `plugins.add.actions` / `shell.bottom`）；**2026-10-09 对 0.2.1-alpha.2 再抽为 129 / 131 / 约 94**（+2 / −0，`slot-catalog.ts` **92 → 94**；新增键 `conversation.chat.flow` / `conversation.chat.reasoning.body`）；**2026-10-15 对 0.2.1-alpha.3 再抽为 139 / 141 / 约 98**（**+5 / −1**，`slot-catalog.ts` **94 → 98**；新增键 `conversation.chat.message.images` / `conversation.chat.user.images` / `conversation.hero.options` / `conversation.user.text.node` / `workspace.toast`，**移除键 `conversation.message.images`**——这是本链上第一次出现「移除」）；**2026-10-16 对 0.2.1-alpha.4 再抽为 140 / 142 / 约 99**（**+1 / −0**，`slot-catalog.ts` **98 → 99**；新增键 `plugins.tab`，`kind: 'list'` / `scope: 'root'`，宿主 `ui-plugin-manager`）；**2026-10-17 对 0.2.1-rc.2 再抽为 141 / 143 / 约 100**（**+1 / −0**，`slot-catalog.ts` **99 → 100**；新增键 `conversation.input.model.label`，`kind: 'single'` / `scope: 'session'`，宿主 `ui-model-selection`）；**2026-10-24 对 0.2.1-rc.3 再抽为 144 / 146 / 约 103**（**+3 / −0**，`slot-catalog.ts` **100 → 103**；新增键 `sidebar.panellist.actions` / `conversation.session.header.views.actions` / `sidebar.right.tab.guide.actions`，三者均为 `list` / `scope: 'root'`，是三个区域的 **More 菜单行**），见 §三）。🔴 **上面这条历史链里 2026-09-23 之前的全部数字（75 / 77 / 79 / 81 / 84 / 96 / 99）都由有缺陷的抽取器产出，是逐轮低估**：该器只扫 `.ts`、键字符类不含连字符、且用**非贪婪正则**截 `SlotMap` 正文（撞上嵌套的 `children: { … }` 即提前截断）。2026-09-23 修好后：0.1.6-alpha.2 重抽为 **104 / 106 / 约 70**、0.1.7-rc.1 为 **121 / 123 / 约 86**；并以随仓库提交的生成产物 `slot-catalog.ts` 交叉核对，**两棵树上漏抽量均为 0**），且**漏了内建的 `root`**。已把 4 处「40 个」的说法改成「节选/低估」并给出可复现命令（`08-cheatsheet.md`、`11-glossary-and-provenance.md`、`api-claims.md` 同批修正） |
| 3 | `04-ui-and-slots.md` 第 10 章（整章） | 整章以 `ctx.settings.installSection(...)` + `SettingsScope.update(patch)` + 手写卡片族为**主路径**教学 | 🔴 **这套机制在 `dsh-v0.1.7-rc.1` 被整体移除**（`settings` 服务换成 `SettingsForms`，表单改由 `Config` schema 派生，持久化改走配置编辑器写 profile 的 Cordis patch；客户端卡片族 −4608/+73 行）。`04` §10 已改写为派生模型并新增 **§10.9** 旧→新对照速查表；`01` / `02` / `05` / `07` / `08` / `10a` / `11` 同步 |

**教训（与 §6 同源）**：「全清单」「四个」这类**完备性措辞**本身就是一种断言，而它往往来自一次不完整的 grep——用 `slots\.(inject|register)\(\s*'` 提取，永远抓不到用 `renderSlot('root')` 渲染的内建键。**凡写「全部/仅/只有 N 个」，都要能给出可复现的抽取命令。**

