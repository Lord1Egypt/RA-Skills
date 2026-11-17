> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：工程规范，三部分：① 官方包的工程约定（目录结构、package.json 不变式、.ts 后缀规则、角色命名表、README 强制节、官方门禁脚本——这部分是权威原文）② 主手册的命名规范、代码硬规则、测试规范、质量门禁清单、提交规范，以及版本演进时间线与兼容性五条军规 ③ 补充手册的 12 条硬规则、发布前自查清单、8 条代码风格共识。①与②在 README 强制节、package.json 不变式上重叠，以①的官方原文为准。
> **合成来源**：J-official-conventions.md + DSH插件开发指导手册.md（第 14/15 章） + DSH插件开发实战补充-模板与踩坑.md（第四篇）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 478 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **上游素材原文**：约 149 行（31%），起点：`J-official-conventions.md`（文件开头）。**不是本技能重写的整理稿**；性质不一——**有的是官方文档逐字摘录（属权威原文），有的是调研期粗笔记（仅备查）**。读某一段前，务必连带读**该段开头的取材说明**。
> - **其余部分 = 面向任务的整理稿**，可直接照做；但它同样是基线快照，写代码前先过版本闸门。
> - 常用检索：`grep -n '^## '`、`grep -n '^# J\.'`（档案起点，在文件开头）

---

<!-- ↓ 源：J-official-conventions.md （全文） -->

# J. 官方包/插件工程约定（`docs/cookbook/adding-a-package.zh.md` + `packages/AGENTS.md`）

> 来源：`deepseek-harness/docs/cookbook/adding-a-package.zh.md`、`deepseek-harness/packages/AGENTS.md`。
> 逐字摘录 + 结构化。**这些是官方对自己仓库的强制约定**；第三方插件不强制，但**照抄能少踩 90% 的坑**。

---

## 1. 包的标准目录（逐字，`adding-a-package.zh.md §1`）

```
packages/<group>/<pkg>/
  package.json     # copy from packages/core/tools, adjust name/description/deps
  tsconfig.json    # extends ../../../tsconfig.base.json, rootDir src,
                   # outDir lib/types, references: ../../../vendor/cosmokit,
                   # ../../../vendor/cordis (+ ../../../vendor/schemastery if
                   # you use Config, + ../../<group>/<dep> for each dsh dep)
  src/index.ts     # service default export or plugin (name/inject/apply/Config)
  README.md        # service API, events, extension points, design notes,
                   # + gated Model Experience context blocks or short form
                   # + the gated "Known Limitations and Deferred Work" section
```

> 🔑 这一行是全文最重要的一句：
> ```
> src/index.ts     # service default export or plugin (name/inject/apply/Config)
> ```
> **服务 = default export 服务类；插件 = 具名导出 name/inject/apply/Config。二选一，不可混。**

**分组（`<group>`）**：`core`、`llm`、`shell`、`compaction`、`subagent`、`todo`、`session`、`client`/`host`、`util`、`test-support`。
分组只是**纯容器**：没有 `package.json`、没有源文件，包恰好位于其下一层。

---

## 2. `package.json` 不变式（逐字，由 `pnpm run constraints` 强制）

> `private: true`，`version` 与根 `package.json` 一致，`type: module`，`main: "lib/index.js"`，`types: "lib/types/index.d.ts"`，`exports["."].types: "./lib/types/index.d.ts"`，`exports["."].default: "./lib/index.js"`，`@deepseek-ai/cordis` 同时出现在 peerDependencies 和 devDependencies 中（相同范围）。每个 dsh 对等依赖（peer dependency）都要在 devDependencies 中镜像。`@deepseek-ai/schemastery` 放在 `dependencies` 中（它是运行时校验器），与 agent-loop 保持一致。`files` 列表精确包含 `lib/index.js`、`lib/types/**/*.d.ts` 以及门禁认可的包专用运行时产物；发布 `./invariant` 的包还要包含 `lib/invariant.js`。如果包的运行时 export 指向输出树，还要包含 `lib/types/**/*.js`。不要发布 `src`、声明映射、JS map 或陈旧的根声明文件。带有 `bin` 的 CLI 应用包在 `files` 中将 `lib/bin.js` 紧跟在 `lib/index.js` 之后。

**翻译成检查清单**：

| 字段 | 要求 |
|---|---|
| `private` | `true`（官方仓库内；你发布到 npm 时改 `false` 或删掉） |
| `version` | 与根保持一致（官方 monorepo 内） |
| `type` | `"module"` |
| `main` | `"lib/index.js"` |
| `types` | `"lib/types/index.d.ts"` |
| `exports["."]` | `{ types: "./lib/types/index.d.ts", default: "./lib/index.js" }` |
| `@deepseek-ai/cordis` | **同时在** `peerDependencies` **和** `devDependencies`（范围相同） |
| 每个 dsh peer 依赖 | 必须在 `devDependencies` 里**镜像**一份 |
| `@deepseek-ai/schemastery` | 放 `dependencies`（运行时校验器） |
| `files` | 精确列 `lib/index.js` + `lib/types/**/*.d.ts`；**不要**发布 `src` |
| 客户端插件额外 | `files` 要含 `lib/client.js`；`exports` 要含 `"./client"` |
| `engines.dsh`（**可选；⚠️ 本技能补充，不是上面那条逐字不变式**） | 自 `dsh-v0.2.1-alpha.4` 起：**声明了它，就只有它决定兼容性** —— DSH peer 范围**不再**放宽或收窄它；写 `workspace:` 会被判**不兼容**；`engines` 非对象、或 `engines.dsh` 非字符串会让兼容性检查读不出清单、**该包被直接拒绝（装不上）**。→ 要么给它一个覆盖全部目标版本的**完整范围**，要么**不写**、退回 peer 检查。宿主侧记录字段已由 `peers` 改名为 **`requirements`** |

> **为什么不把 `engines.dsh` 写进上面那段逐字不变式**：那段是官方 `pnpm run constraints` 的逐字要求，`engines.dsh` 属**可选**字段、不由 constraints 强制 —— 混进逐字块会让人以为必填。（判据：`docs/upgrade-guide/v0.2.1-alpha.3/plugin-engines-dsh/guide.zh.md`；源码 `packages/boot/app-boot/src/plugin-compatibility.ts:55-73`。）

**相对导入规则（逐字）**：
> 包内的相对导入在源码中使用显式 `.ts` 后缀（例如 `export * from './types.ts'`）。编译器在输出的 JS 中将其重写为 `.js`，在声明文件中保留显式 `.ts` 后缀。

> 🔥 这就是为什么官方代码里全是 `from './types.ts'`、`from './Brand.tsx'` —— **源码里写 `.ts`/`.tsx` 后缀是官方要求**，不是笔误。

---

## 3. 客户端（UI）包的额外要求（逐字）

> `packages/client/*` 包改为 extends `tsconfig.base.client.json`（而非 `tsconfig.base.json`）；client 插件包还需在 package.json 声明 `dsh.client`、导出 `./client`、调用共享 tsdown preset（`packages/client/tsdown.client.ts`）。
> ⚠️ 该 preset **只在 DSH 仓库内可用**（官方明确「没有已发布的预设暴露该包」）。仓库外的第三方插件必须自己复刻 lazy-CJS 产物格式——契约见 `14-inbound-http-and-timers.md` §17.3。

**三件套**：`tsconfig.base.client.json` + `dsh.client` 声明 + `./client` 导出。

---

## 4. 自动发现（不用手改的）（逐字）

> 以下内容由 glob 或包 manifest（元数据清单）发现机制自动覆盖，无需手动编辑：根 `package.json` workspaces、`scripts/publint-all.ts`、`tsdown.config.ts`、`.oxlintrc.json`、`scripts/check-workspace-constraints.ts`。

> 💡 对**第三方插件作者**的启示：官方清单是 **glob 自动发现**的，所以你的插件目录结构只要对，就能被 `pnpm -r` / 构建脚本自动纳入。

---

## 5. 角色命名表（逐字，**这段是"起名困难症"的解药**）

> 名称必须描述当前稳定职责。不要用首个实现、可能的未来扩展或 Cordis 基类命名。接口包使用能力名称。实现包加上能够区分实现的机制、协议、环境或厂商限定词。只有同主机执行属于约定时，才使用 `local`。
>
> 一个 engine、runtime、policy、controller、resolver、store 或当前配置使用单数 `ctx` key。registry 或拥有多个具名成员的服务使用复数 key。类的角色与 key 的单复数必须一致。

| 词 | 适用条件 | **不**适用条件 |
|---|---|---|
| `Controller` | 接受命令或用户意图，并改变一项既有领域状态或展示状态 | 执行任意工作、拥有一组 provider，或只把值转成展示形式 |
| `Store` | 拥有一组数据，主要提供 CRUD / snapshot / subscription | 校验状态机、裁决权限、分派工作或拥有 provider 优先级。**类中有 map ≠ store** |
| `Directory` | 暴露供发现或选择的条目及其元数据 | producer 向其中注册任意实现，或调用方通过它执行工作 |
| `Presenter` | 把领域值或工具参数**纯转换**为渲染意图 | 执行 I/O、订阅、修改状态或拥有生命周期 |
| `Registry` | 拥有一组**动态具名注册**，以及查询、重复项/优先级规则、生命周期与释放 | 主要约定是分派、执行、取消、策略或编排 |
| `Runtime` | 运行实时工作，跨调用拥有分派、取消、provider 协调或操作生命周期 | 只存储记录、返回目录、解析一个值或保存配置 |
| `Resolver` | 根据输入计算/定位一个答案，**但不拥有**该答案的生命周期 | 拥有可变集合或长时间运行的执行过程 |
| `Binder` | 把已声明接口绑定到调用方 context/生命周期并返回绑定值 | 把该值作为集合持有、控制其领域状态，或只转换数据 |
| `Engine` | 实现领域算法或有状态执行模型 | 只选择 provider 或跨协议边界转发请求 |
| `Policy` | 决定**允许/选择/限制/观察**什么 | 执行该决定所允许的机制 |
| `Executor` | 在一项能力中运行一个明确请求或已解析 spec | 拥有广泛应用生命周期或 provider 目录 |
| `Gateway` | 适配进程、网络、RPC 或 API 边界 | 只注册同进程服务或存储元数据 |
| `Provider` | 提供一项能力定义的**一个实现**（多实现时加机制/厂商限定词） | 表示能力定义、provider registry 或消费方 runtime |
| `Backend` | 在已定义接口后实现可替换的底层持久化/传输/执行 | 表示面向用户的服务或已返回的实时资源引用 |
| `Handle` | 引用一个**实时资源**，并控制/观察它 | 创建并管理完整资源池 |
| `Config` | 拥有一个已解析配置值，或一项边界严格的配置记录及其更新约定 | 存储通用集合、执行工作或暴露无关设置 |
| `Service` | 拥有一项无法用以上更精确角色诚实描述的内聚领域服务 | **只因为类继承了 Cordis `Service` 就起这名字** |

**额外逐字规则**：
> 不得让不兼容的 host 与 client 声明复用同一个 Cordis `Context` key。即使二者使用独立的运行时 context，TypeScript 声明合并仍会同时看到两种类型。

---

## 6. 包 README 的强制内容（逐字标题）

```
## Model Experience
### Request context and condition
...
## Known Limitations and Deferred Work
```

> Package READMEs document model, token, and KV-cache effects using the canonical Model Experience format.

即：**README 必须写"这个插件对模型的请求上下文有什么影响（token / KV cache）"，并且必须有一节标题为 `## Known Limitations and Deferred Work` 写清遗留缺口。**（官方用 `scripts/verify-package-readme-limitations.ts` 脚本强制检查。）

**对第三方插件的实用建议**：即使不强求格式，README 至少要有这几节：
1. 这个插件给 dsh 加了什么（一句话 + 工具/命令/界面清单）
2. 前置要求（依赖什么环境、需要什么凭据）
3. 配置项说明（每个字段什么意思、默认值）
4. 已知限制与未做的事（**诚实清单**）

---

## 7. 官方门禁脚本（发布前自查）

| 脚本 | 检查什么 |
|---|---|
| `pnpm run constraints` | `package.json` 不变式（见第 2 节） |
| `hygiene` | 仓库卫生 |
| `doc-sync` | 文档与代码同步 |
| `publint` | 发布产物是否合规（`exports`/`files` 等） |
| `verify-cordis-config` | **拒绝 Loader 配置项元数据里的表达式节点**（复盘 0002 的防护） |
| `verify-package-invariants` | 包不变量 |
| `verify-package-readme-limitations` | README 是否有 `## Known Limitations and Deferred Work` |
| `verify-subsystem-pages` | 分组 README 是否声明子系统归属 |
| `dsh-session-snapshot` | 拒绝结构化的 `UNKNOWN_TOOL` 结果（复盘 0002 的防护） |

> 💡 第三方插件**照抄 `publint` 这一条**就够：`npx publint` 能提前发现 `exports`/`files` 配错——那是"发布后用户装了不生效"的头号原因。

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 2555-2785 -->

# 第 14 章 工程规范（想做得像官方包一样）

> **说明**：这一章的门禁**只对官方仓库内的包生效**。社区插件不受这些约束。但如果你想做出"专业级"的插件，照着做不会错。

## 14.1 命名规范

来源：`packages/AGENTS.md`、`docs/cookbook/adding-a-package.zh.md`

| 对象 | 规范 |
|---|---|
| 普通包 | `@deepseek-ai/dsh-<name>` |
| 客户端包 | `@deepseek-ai/dsh-client-<name>`，**目录前缀即包名前缀** |
| service 名（ctx 键） | 单数用于 engine/runtime/policy；复数用于 registry/多具名成员服务 |
| 角色后缀词表 | `Controller`/`Store`/`Directory`/`Presenter`/`Registry`/`Runtime`/`Resolver`/`Binder`/`Engine`/`Policy`/`Executor`/`Gateway`/`Provider`/`Backend`/`Handle`/`Config`/`Service` |

## 14.2 代码硬规则

| 规则 | 原文出处 |
|---|---|
| ESM everywhere（`"type": "module"`）；**包内相对导入用显式 `.ts` 后缀** | 根 `AGENTS.md:105` |
| **注册即 effect**：每个贡献都走 `ctx.effect()` / `ctx.on()`；注册表的 `register()` 返回 disposer | 根 `AGENTS.md:106` |
| **无硬编码可调参数** | 根 `AGENTS.md:116` |
| **capability seam 三角色必须完整设计**，一个角色本身不是 seam | 根 `AGENTS.md:113` |
| 一切在 `strict: true` 下编译；每个模块与导出要有 JSDoc | 根 `AGENTS.md:143` |
| 导出形态：service 包 default-export 服务类；函数插件命名导出，**无 default export** | `packages/AGENTS.md:5` |
| 可选服务用 `ctx.get(name)` | `packages/AGENTS.md:6` |
| `src/types.ts` 只放类型，不放运行时代码 | `packages/AGENTS.md:24` |
| 测试放包级 `tests/`，**不是** `src/__tests__/` | `packages/AGENTS.md:25` |

## 14.3 README 规范（官方强制）

`docs/cookbook/adding-a-package.zh.md:76-110` 规定包 README 必须有这两个规范结尾章节（旧引 `:74-108`）：

```markdown
## Model Experience

### Request context and condition

#### What the model sees

...

#### Token effect

...

#### KV Cache effect

...

## Known Limitations and Deferred Work

- **Consumer-visible gap** — exact missing operation or case, ...
```

**对社区插件的启示**：就算不强制，写上这两节会让你的插件显得非常专业。特别是 **Known Limitations**——主动承认限制，比假装完美更可信。

## 14.4 测试规范

来源：`docs/testing.zh.md`

| 要求 | 内容 |
|---|---|
| 框架 | **vitest** |
| 运行 | `pnpm run test`；CI 覆盖率门禁是 `pnpm run test:coverage`（`packages/*/*/src` **逐文件 100%**） |
| 位置 | 包级 `tests/**`，与所覆盖代码放一起 |
| **HMR 安全测试** | **每个注册表都要有**：对贡献该注册表的 fiber 执行 dispose，断言清理完成 |
| **真实组合测试** | 产品可见的插件**必须有**一个非单元的真实组合测试：通过 Loader 与 app/process 启动测试专用 `cordis.yml`，断言模型可见/持久/用户可见输出。**手动 `ctx.plugin(...)` 套件不算** |
| 原则 | 优先真实实现而非 mock；只 mock 贵或不确定的边界（LLM、网络、时钟） |

**一句话**：官方对"我测过了"的要求，比你想象的高——**必须端到端跑过真实加载路径**。

## 14.5 质量门禁清单（官方包适用）

| 命令 | 检查什么 |
|---|---|
| `pnpm run constraints` | workspace 包不变式（命名、依赖声明、禁止发布的文件、项目引用面） |
| `pnpm run hygiene` | `publint` + 包依赖 + 入口 + license + 不变量 + NodeNext 类型 + client 包边界 + i18n 等一长串 |
| `pnpm run doc-sync` | 全部文档门禁（含死链、生成的目录、JSDoc、翻译配对、README 规范章节…） |
| `pnpm run typecheck` / `pnpm run lint` | 类型与静态检查 |
| `pnpm run build` | tsc 产出 `lib/types`，tsdown 打包运行时 |
| `pnpm run test:coverage` | CI 覆盖率门禁（**逐文件 100%**） |

**建议（给社区插件作者）**：至少自建 `publint`（检查发布视图干净）与文档完整性检查。

## 14.6 提交规范

源码实证：本仓库用 **Conventional Commits**，破坏性变更在标题里加 `!`：

```
refactor(cli)!: complete app-owned profile startup
refactor(cli)!: one shared base config with per-surface overlays
feat: unify JSON value schema DSL
docs: add tutorial for packaging and installing a plugin bundle
```

⚠️ **没有 CHANGELOG**。想知道改了什么，只能看提交历史。

另有一条对官方贡献者的要求（根 `AGENTS.md:153-155`）：**非平凡变更必须在同一个 PR 里附 Agent Note**。

---

# 第 15 章 版本演进与兼容性策略（git 实证）

> **为什么要有这一章**：因为 DSH 是一个**每周都在变**的项目。不了解演进史，你会照着过时教程白干活。

## 15.1 时间线（全部来自 git 实证）

| 日期 | 事件 | 提交 |
|---|---|---|
| 2026-06-10 | 仓库首个提交 | `b67e81ac97` |
| **2026-06-11** | **`defineTool` 引入**（工具 schema DSL） | `7f024a1a9d` |
| 2026-07-15 | `docs/user/develop/basic/` 插件入门教程出现 | `6af61c6f4e` |
| **2026-07-19** | **`ctx.slots` 与 `dsh.client` 机制诞生**（GUI step1 skeleton） | `a6a3807a07` |
| 2026-07-21 | 工具增加规范类型输出；JSON value schema DSL 统一 | `66c36e7325`、`8500974fd4` |
| 2026-07-22 | `docs/cordis-tutorial/` 七章教程整套加入 | `21456a36ca` |
| 2026-07-23 | client 插件形态统一（`dshClient` manifests、clientBundle preset、纯净度门禁） | `c2e0c16d6a` |
| 2026-07-28 | `ctx.settings`（用户设置 seam）加入 | `ec0786e099` |
| **2026-08-04** | **TUI 前端归档**（不再作为应用入口交付） | 归档笔记 |
| **2026-08-10** | client manifest 元数据**嵌套到 `dsh.client`**（`dshClient` → `dsh.client`） | `717792b631` |
| 2026-08-17 | **最早的 tag** `dsh-v0.1.0-rc.7` | `99f6f02fec` |
| **2026-08-30** | **`installSection` 出现**（设置卡片机制成型） | `f4e49ccf8f` |
| **2026-09-23** | **`installSection` / `SettingsScope` / 手写设置卡片族整体移除**（改为「Config schema 派生表单 + 配置编辑器写 profile 补丁」） | `dsh-v0.1.7-rc.1`（`46a7f68b09`） |
| 2026-09-10 | 最新 tag `dsh-v0.1.5-rc.2` | `fb2c4b9e69` |
| 2026-09-10 | 本手册依据的 HEAD | `c291e7961a` |

**从这张表能看出什么**：

1. **所有 UI 相关机制都很年轻**（2026-07-19 之后）。你在网上看到的 2026-07 之前的 UI 插件教程，**一定过时**。
2. **`dsh.client` 这个字段名只从 2026-08-10 起有效**。之前叫 `dshClient`。
3. **`installSection` 的寿命只有 3 周多**：2026-08-30 出现，**2026-09-23（`dsh-v0.1.7-rc.1`）就被整套移除**（详见 `04` §10.9）。这是本项目「pre-stable 上游会**整族重做机制**」的最强例证 —— **不要把任何一代 API 当成长期约定**；更不要因为「某 API 刚出现、文档还不全」就以为它会稳定下来。

## 15.2 一个真实的新旧 API 对比（工具注册）

**旧写法**（`defineTool` 引入前）：

```ts
import type { Context } from 'cordis'

export const name = 'echo-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register({
    name: 'echo',
    description: 'Echo the given text back, uppercased.',
    parameters: {
      type: 'object',
      properties: { text: { type: 'string' } },
      required: ['text'],
    },
    async execute(args: any) {
      return [{ type: 'text', text: `ECHO: ${String(args?.text ?? '').toUpperCase()}` }]
    },
  })
}
```

**新写法**（引入后）：

```ts
import type { Context } from 'cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'echo-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'echo',
    description: 'Echo the given text back, uppercased.',
    parameters: {
      text: { type: 'string', required: true },
    },
    async execute(args) {
      // args is typed: { text: string }
      return [{ type: 'text', text: `ECHO: ${args.text.toUpperCase()}` }]
    },
  }))
}
```

**差异对照**：

| 维度 | 旧 | 新 |
|---|---|---|
| `parameters` | 原始 JSON Schema（`type:'object'` + `properties` + `required` 数组） | 自有 DSL（每属性内联 `required: true`） |
| `execute(args)` | `args: any`，要手动校验 | 类型级 `InferArgs<S>` 自动推导 |
| 返回值 | 直接返回内容块 | 返回**规范值**，由 `output.render` 转内容块 |

**关键洞察**：**注册方式 `ctx.tools.register(...)` 没有变**，变的是传给它的对象由 `defineTool()` 构造。提交正文明确说"raw JSON Schema still accepted for MCP interop"——原始 JSON Schema **仍作为 MCP 互操作路径保留**。

⚠️ 如果你在网上看到 `parameters: { type: 'object', properties: ... }` 的写法，那是**旧 API**（虽然可能仍能用，但不是当前推荐）。

## 15.3 被正式弃用的东西

`git log --grep="deprecat"` 命中（实证）：

- `5cfc765ff6` `docs(session): deprecate direct event readers`
- `aa491acc29` `docs(session): record synchronous history read deprecation policy`

**结论**：**直接同步读取 session 历史事件**的用法已被正式弃用。插件应改从**投影（projection）或标准服务 API** 读取会话数据。

**对你的影响**：不要写"遍历 session 事件数组"这种代码。

## 15.4 兼容性策略（给你的五条军规）

| # | 策略 | 做法 |
|---|---|---|
| 1 | **记录基线** | 在你的插件 README 里写明：「基于 commit `xxx` / 版本 `0.1.7-rc.1` 开发」（写你**实际**用的那版；本手册基线见 `00-version-gate.md` §1） |
| 2 | **锁依赖** | 若引用官方包，用精确版本或 commit，不要用 `^` 漂移 |
| 3 | **升级前评估** | 用第 13 章模板 4 让 Agent 分析 diff，重点看 `--grep='!'` |
| 4 | **小步快跑** | 先做最小可用版本，跑通全链路，再加功能。别一次写 2000 行再调试 |
| 5 | **警惕教程时效** | 任何第三方教程，先核对它的日期。**2026-08 之前的 UI 教程基本不可用** |

## 15.5 怎么知道「我用的 API 变了没」

三条命令（让 Agent 帮你跑）：

```sh
# 1. 看我引用的这些包，最近改了什么
git log --oneline -30 -- packages/core/tools packages/client

# 2. 看所有破坏性变更（本仓库用标题里的 ! 标记）
git log --oneline --grep='!' --since='2026-09-01'

# 3. 看我关注的文档目录的演变
git log --oneline --follow -- docs/user/develop/basic/
```

---


---

<!-- ↓ 源：DSH插件开发实战补充-模板与踩坑.md 区间 1639-1706 -->

# 第四篇 · 工程规范

## 4.1 官方 12 条插件硬规则（`packages/AGENTS.md` 原意转述）

| # | 规则 |
|---|---|
| 1 | **导出形态不能混**：服务包 default export 服务类；函数式插件具名导出 `name/inject/Config/apply`，**无 default export** |
| 2 | **可选服务用 `ctx.get(name)`**；`ctx.<name>` 只留给声明过的注入 |
| 3 | **面向用户可见的插件必须有真组合测试**（真跑 Loader + 应用），手搓 `ctx.plugin()` 不算 |
| 4 | 一次异步操作由**一个**生命周期控制器/事务表示 |
| 5 | 服务定义要**面向所有当前消费方**设计，别让一个消费方决定服务契约 |
| 6 | 每个抽象、状态机、选项、防御性拷贝都要有**当前所有者与需求** |
| 7 | 公开选择要有**证据**（当前消费方或相关先例），"可配置"不能成为无依据默认值的理由 |
| 8 | **面向模型的契约要用模型视角写**：提示词/工具 schema/结果/诊断只含任务相关概念，不含 UI、传输或实现词汇 |
| 9 | **决定要在执行它的那个操作里强制执行**（schema 省略、prompt 过滤、包装器、监听器顺序都不是强制） |
| 10 | **只在提交点发布状态**；通知与派生状态只在操作成功后发出 |
| 11 | **给完整结果施加边界**（字节/token/项/时间限制要考虑 wrapper 与 metadata） |
| 12 | **注册表贡献必须证明释放**（dispose fiber 并观察移除） |

## 4.2 `package.json` 自查清单

| 字段 | 要求 |
|---|---|
| `type` | `"module"` |
| `main` | `"lib/index.js"` |
| `types` | `"lib/types/index.d.ts"` |
| `exports["."]` | `{ types, default }` 两项都要 |
| `exports["./client"]` | **仅 UI 插件**，指向 `lib/client.js` |
| `exports["./cordis.patch.yml"]` | **仅组合包**（建议加上） |
| `dsh.bundle.patch` | **仅组合包** |
| `dsh.client` | **仅 UI 插件**（`inject` 包名数组 + `platform: "web"`） |
| `@deepseek-ai/cordis` | **同时在** peerDependencies 与 devDependencies |
| 每个 dsh peer | 必须在 devDependencies **镜像**一份 |
| `files` | 精确列表；**别发布 `src`** |
| 相对导入 | 源码里写显式 `.ts`/`.tsx` 后缀 |

## 4.3 发布前自查

```bash
npx publint                 # exports / files 配置合规性（最有用的一条）
```

官方完整门禁：`constraints`、`hygiene`、`doc-sync`、`publint`、`verify-cordis-config`、`verify-package-invariants`、`verify-package-readme-limitations`、`verify-subsystem-pages`。

## 4.4 README 必备四节

```markdown
## 这个插件做了什么        # 一句话 + 工具/命令/界面清单
## 前置要求               # 依赖的环境、需要的凭据
## 配置项                 # 每个字段什么意思、默认值
## Known Limitations and Deferred Work   # 诚实清单（官方强制要求这一节）
```

## 4.5 代码风格：从真实仓库提炼的 8 条共识

| # | 共识 | 证据 |
|---|---|---|
| 1 | 具名导出 `name`/`inject`/`apply`，无 default export | 全部 13 个仓库 |
| 2 | 一切注册包 `ctx.effect` 并保留 disposer | 全部 |
| 3 | 清理函数给**人类可读标签**（`ctx.effect(fn, '包名: 说明')`） | 官方 `ui-theme` |
| 4 | 错误信息要点名对象 + 给下一步 | 官方 `resolveConfig`、`validateOverrides` |
| 5 | 配置校验失败要抛**教学式**错误 | 官方 `plan-mode` |
| 6 | 测试放 `tests/`，不放 `src/__tests__/` | 官方约定 |
| 7 | `src/types.ts` 只放类型，不放运行时代码 | 官方约定 |
| 8 | 行为变化与 README/JSDoc 契约**同一次提交**更新 | 官方 `packages/AGENTS.md` |

---


---

