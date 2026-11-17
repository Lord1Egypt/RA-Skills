# 坑与规避（含实测案例）

> 以下坑均来自对 vendor/cordis v4.0.1 源码与教程的实测验证，非推测。

## 坑分类总览

```
┌─ 事件/分发 ────── waterfall 是分发非注册 · next(新值) 被忽略
├─ 依赖/生命周期 ── inject 缺失=静默 PENDING · 可选依赖误用 inject
├─ 装配/HMR ─────── 条目无 id=全量重挂 · HMR 三件套缺一静默
├─ 导出/Config ──── 默认导出丢 Config · Config 导普通对象无效
├─ 作用域/状态 ──── 服务命名冲突 · 全局变量绕过 Context
├─ 子进程/桥接 ──── 相对路径指向 CWD · 常驻进程僵尸 · stderr 吞掉
├─ 路径/构建 ────── Windows file:// 三斜杠 · paths 指向包目录 · .ts emit
└─ 装配/Windows ─── insert: 包裹 · 只改 patch 层 · junction 悬空
```

> 每个坑的完整症状/根因/规避见下文编号条目（31 个）。

## 1. waterfall：`next(新值)` 传参被静默忽略 ⚠️ 实测

- **现象**：监听器写 `next(text + suffix)`，下游收到的是**原始 args**，转换值丢失。
- **根因**：`next` 闭包捕获分发时的 args 数组；你传给 `next()` 的参数不参与 `cb(...args)`。
- **规避**：`const result = next()` 取下游返回值，包装后 `return`。
- **延伸**：`ctx.waterfall(name, fn)` 不是注册！`fn` 会被当成内层 next 立即执行（实测抛 `next is not a function`）。

## 2. 函数插件不能赋 `name` 属性 ⚠️ 实测

- **现象**：`Object.assign(fn, { name: 'x' })` 在 ES 严格模式抛 `TypeError: Cannot assign to read only property 'name'`。
- **规避**：模块级 `export const name = 'x'`；函数自身的 `name` 由声明自动获得。

## 3. `inject` 缺失 = 静默 PENDING，不是报错

- **现象**：插件不输出、进程状态码 0 静默退出，看似"没运行"。
- **根因**：PENDING 是合法状态——提供方可能稍后挂载；PENDING fiber 不保持事件循环活跃。
- **规避**：用 `FiberState.PENDING` 遍历 `ctx.registry` 诊断；确认 `cordis.yml` 里提供方条目存在。

## 4. cordis.yml 条目不带 `id` → HMR 全量重挂

- **现象**：编辑配置文件任意内容，所有插件都被重挂。
- **根因**：loader 按 `id` 对比条目；无 `id` 每次读文件生成新 id，视为删除+新增。
- **规避**：每个条目写稳定 `id`。

## 5. 默认导出插件丢失 Config schema

- **现象**：`export default { apply, Config }` 挂载后 config 校验不生效。
- **根因**：Loader 默认解包丢弃 `Config`（docs/postmortem/0001-acp-default-export-drops-inject.zh.md）。
- **规避**：只导出命名导出：`export const name` / `export function apply` / `export const Config`。

## 6. `Config` 导出普通对象无效

- **现象**：config 不校验，任何值都通过。
- **根因**：Cordis 接受 Standard Schema 验证器；普通对象不是 schema。
- **规避**：用 `@deepseek-ai/schemastery` 的 `Schema.object({...})`；类型与 schema 同名导出。

## 7. HMR 依赖三件套，缺一个就静默

- **现象**：改了文件不热重载。
- **根因**：HMR 插件 `inject` timer 服务（去抖）、经 logger 输出；两者缺失 → 永远 PENDING 且无提示。
- **规避**：同时挂 `cordis-plugin-logger-console` + `cordis-plugin-timer` + `cordis-plugin-hmr`。

## 8. 服务命名冲突

- **现象**：`ctx.myService` 类型/行为异常或覆盖现有服务。
- **根因**：服务名是扁平命名空间，`tools`/`llm`/`agents`/`sessions`/`skills` 等已被 harness 占用。
- **规避**：加辨识前缀；查询 `docs/subsystems/core.md` 的 `cordis-surface` 区块确认未占用。

## 9. 可选依赖误用 `inject`

- **现象**：某个可选能力缺失时插件永远不启动。
- **根因**：`inject` 是硬依赖，缺失即 PENDING。
- **规避**：可选依赖不 inject，用 `ctx.get('name')` 运行时探测（undefined 即无提供方）。

## 10. 忘记 disposer → 卸载泄漏

- **现象**：HMR 重载后旧资源（定时器/监听器/服务）仍在运行，行为叠加。
- **根因**：副作用未走 `ctx.effect()`/`ctx.on()`，fiber 卸载无法回卷。
- **规避**：一切注册走 effect/on 并返回 disposer；teardown 顺序敏感工作放同一 effect。

## 11. 子进程相对路径指向 CWD 而非插件目录

- **现象**：`child_process` 调用 `./script.py`，换个启动目录就 `ENOENT` 找不到文件。
- **根因**：相对路径相对 Node **当前工作目录**解析，不是插件源码目录。
- **规避**：`path.join(__dirname, './script.py')` 转绝对路径。

## 12. 常驻子进程未释放 → 僵尸进程

- **现象**：HMR 重载后旧 WebSocket/常驻进程仍存活，端口占用或行为叠加。
- **根因**：`new` 出来的常驻进程只启动、没在 `ctx.effect()` 里注册释放逻辑。
- **规避**：把底层进程的 kill/close 放进 `ctx.effect()` 的 disposer。

## 13. 子进程 stderr 未包装 → 静默失败

- **现象**：底层 Python 崩了，Harness 表现怪异但看不到原因。
- **根因**：Python 报错不会自动转为 Node 异常，stderr 被吞。
- **规避**：try-catch 包裹调用，stderr 经 `ctx.logger` 格式化输出（最好转 Cordis `Error`）。

---

# 第二部分：Windows 本地开发与装配（⚠️ 实测 2026-08，dsh-memory 构建）

## 14. `tsx -e` 不支持顶层 await

- **现象**：`npx tsx -e "await import(...)"` 报 `Top-level await is currently not supported with the "cjs" output format`，无任何输出。
- **根因**：`-e` 内联脚本按 cjs 处理。
- **规避**：验证脚本写成 `.ts` 文件再 `tsx scripts/xxx.ts`（文件按 package.json `type: module` 走 ESM）。

## 15. tsconfig `paths` 指向 `.d.ts` 文件 → tsx 运行时加载失败

- **现象**：tsc 通过（类型 OK），但 tsx 运行报 `ERR_MODULE_NOT_FOUND .../lib/types/context.ts`（.d.ts 内部相对 `.ts` 导入指向不存在的源码路径）。
- **根因**：paths 指到 `lib/types/index.d.ts`，tsx 按 paths 解析运行时入口，加载了 d.ts 而非可执行模块。
- **规避**：**paths 指向包目录**（`vendor/cordis` 而非 `lib/types/index.d.ts`）——tsc 读其 `types` 字段，tsx 读其 `main` 字段，两者自洽。

## 16. Windows junction 到 pnpm node_modules → SymbolicLink 悬空

- **现象**：`New-Item -ItemType Junction node_modules → <pnpm包>/node_modules` 后，部分 `@deepseek-ai/*` 目录 `Test-Path` 为 True 但内部文件缺失。
- **根因**：pnpm 的包链接是**相对 SymbolicLink**（`..\..\vendor\xxx`），从 junction 新基位置解析错位。
- **规避**：**逐包绝对 junction**：`node_modules/@deepseek-ai/<pkg>` → `D:/.../vendor/<pkg>`（Junction 类型目标绝对，可穿透）。

## 17. 未 start 的 Context 上 `await ctx.service` 永久 pending

- **现象**：`new Context()` + `new FakeTools(ctx)` 后 `await ctx.tools` 卡死无输出（超时）。
- **根因**：Service 需 fiber 启动才 resolve；裸 Context 上 await 服务永不返回。
- **规避**：验证/装配必须用 **`ctx.plugin(plugin, config)`**（cordis 启动 fibers）；`apply()` 直调只用于已就绪服务的单元场景。

## 18. Service 构造即注册（无需 ctx.provide）

- **现象**：按老习惯写 `ctx.provide(service)` 报类型错（provide 参数是 string）。
- **根因**：cordis v4 `Service` 子类 `constructor(ctx, name)` **构造即注册**（内部调 `ctx.reflect.provide`）。
- **规避**：`new XxxService(ctx, 'name')` 即完成注册，fiber 卸载自动反注册。

## 19. 常驻子进程句柄 → 验证脚本"超时"（跑完不退出）

- **现象**：验证脚本打印完所有结果但进程不退出（120s 超时 kill）。
- **根因**：child_process 的 stdin/stdout + readline 引用保持 event loop 存活。
- **规避**：验证脚本结尾显式 `process.exit(0)`（生产插件由 fiber disposer 管理，不受影响）。

## 20. `.ts` 扩展导入与 emit 冲突

- **现象**：源码用 DSH 风格 `import './x.ts'`（`allowImportingTsExtensions: true` 只能配 `noEmit`），构建 emit 报 TS5097。
- **规避**：构建配置开 **`rewriteRelativeImportExtensions: true`**（TS 5.7+），emit 时自动改写 `.ts` → `.js`。

## 21. DSH loader 原生加载 `.ts` 源码，无需构建 lib

- **现象**：tsdown 构建在独立目录失败（pnpm 嵌套链接缺失导致 CLI 依赖解析崩溃）。
- **根因**：独立目录的 node_modules 链接树不完整，构建工具无法解析传递依赖。
- **规避**：**cordis.yml 的 `name` 直接指向 `.ts` 源码文件**（loader 用 tsx 加载，DSH 原生支持）；lib 构建仅为正式 workspace 包选项。

## 22. `ctx.plugin` 不传 config → 默认空 → 运行参数缺失

- **现象**：插件加载成功但 Python 侧 `ModuleNotFoundError`（skillRoot 空）。
- **根因**：`ctx.plugin(plugin)` 未传 config，cordis 用 `{}` 默认 → 路径类配置全空。
- **规避**：`ctx.plugin(plugin, { skillRoot: '...', ... })` 显式传配置。

## 23. 跨语言桥接：snake_case ↔ camelCase 必须显式转换

- **现象**：TS 类型声明 `{ memoryId }` 但 Python 返回 `{ memory_id }`，运行时 `result.memoryId` 为 undefined（类型欺骗，tsc 不报错）。
- **根因**：桥接层直接透传未做字段名转换，类型标注与实际不符。
- **规避**：胶水层（Service 封装）显式做 snake→camel 转换 + 单独的类型转换函数，勿透传裸 RPC 结果。

## 24. DSH profile 装配：patch 插入语义 + file:// URL + HMR

- **现象**：cordis.patch.yml 裸写 `- id: memory` 被当「按 id 覆盖」而非「插入」，插件不加载；`name: 'E:/...'` 报 `ERR_UNSUPPORTED_ESM_URL_SCHEME`。
- **规避**：
  - 插入新条目用 **`- insert:`** 包裹（裸条目是覆盖语义）
  - Windows 绝对路径 name 写 **`file:///E:/...`**（三斜杠）
  - HMR：改 patch 无需重启 DSH，验证信号 = 常驻 python 进程 + 工具列表出现 `memory_*`

# 第三部分：001 笔记蒸馏补充（2026-08）

## 25. 配置补丁是整体替换，不是深度合并

- **现象**：patch 里只为插件写一个新字段，原有配置（如 API Key）直接消失。
- **根因**：Cordis patch 是**整体替换**该条目的配置，不合并已有字段。
- **规避**：patch 中必须带完整配置；或用 `!!js` 表达式从环境变量/上级配置读取缺失字段。

## 26. 全局变量绕过 Context → 幽灵状态 → HMR 失效

- **现象**：插件卸载/热重载后行为残留，系统越跑越乱，只能重启。
- **根因**：插件用了全局变量或未封装的外部 API，绕过 Context 的 Proxy 副作用追踪——卸载时框架无法撤销这些残留。
- **规避**：所有副作用（监听器/定时器/服务注册）一律走 `ctx.on()`/`ctx.effect()`；禁用模块级可变全局状态。

## 27. 异步初始化别写插件主体，放 `ready` 事件

- **现象**：插件加载时异步操作（文件/网络）竞态——依赖服务还没就绪就开始跑。
- **规避**：文件/网络等异步初始化放 **`ready` 事件**（应用完全启动 + 依赖插件加载完成后执行）。

# 第四部分：DSH profile 装配详细版蒸馏（2026-08，插件项目 docs/DSH-装配经验.md）

## 28. loader 验证必须 `ctx.plugin(Loader)`，不是 `new Loader(ctx)`

- **现象**：独立验证脚本 `new Loader(ctx)` 报 `Cyclic __proto__`（循环原型）。
- **根因**：loader 包的正确加载方式是作为插件 `ctx.plugin(Loader)`（cordis fiber 初始化），直接 new 破坏了原型链。
- **规避**：
  ```ts
  await ctx.plugin(Loader)                       // ✅
  await ctx.loader.create({ id, name, config })  // 然后 create + await
  ```
- **loader 包不在插件 node_modules 时的解析**：`createRequire('D:/.../apps/cli/package.json')`（harness 应用包）从依赖树解析。

# 第五部分：DSH-Context-Pro 项目实测沉淀（2026-08，通用 Cordis 插件开发补充）

> 以下内容来自 DSH-Context-Pro 项目全链路开发实测，仅收录与已有条目**不重复**的补充内容。

## 40. TS 工程环境补充

### 40.1 新项目无 TypeScript/tsx

- **现象**：`npx tsc` 装错包 / `Cannot find package 'tsx'`
- **根因**：项目未声明 devDependencies
- **规避**：用 harness 的编译器：`node D:/Git/github/deepseek-harness-master/node_modules/typescript/bin/tsc --noEmit`；tsx 从 harness 根跑 `node --import tsx/esm <脚本>`

### 40.2 `@types/node` 缺失

- **现象**：`Cannot find type definition file for 'node'`
- **根因**：tsconfig `types:["node"]` 找不到
- **规避**：`typeRoots` 指向 harness 的 `node_modules/@types`

### 40.3 tsconfig `paths` 指 junction → 类型分裂

- **现象**：`agent/pre-step` 事件类型与监听器不匹配（`next` 参数变宽）
- **根因**：node_modules junction（lib 构建）与 paths 源包（src）两副本冲突
- **规避**：**paths 指向 harness 源包目录**（`packages/core/agent` 而非 node_modules）；移除 `node_modules/@deepseek-ai` junction，只走 paths

## 41. DSH 运行时补充

### 41.1 `ctx.provide` 非 Service 不可 await

- **现象**：`await ctx.contextPro` 永远 undefined
- **根因**：只有 `Service` 子类注册才是可等待服务；普通对象 provide 走 Proxy 惰性解析
- **规避**：首版**不要服务预留**（聚焦核心）；真要暴露能力用 `Service` 子类（构造即注册）

## 42. e2e 测试假阳性

- **现象**：e2e 测试全绿，但真实 web boot 插件不工作
- **根因**：旧 e2e 的"hook 触发 = true"是**测试自己注册的监听器**被 waterfall 触发，与插件激活无关；且 raw Context 缺 agents 服务时 apply 根本不执行，`ctx.plugin()` 也不报错
- **诚实 e2e 三要素**：
  1. 先 `ctx.plugin(AgentRegistry)` 供服务
  2. 内层 next 返回**真实消息列表**（插件从 decision.messages 取数据，空列表=永远早退）
  3. 断言注入块存在（深展平后找 `source.plugin === 'my-plugin'` 标记）
- **不展平断言**：`decision.messages` 返回前必须保证扁平；断言**不要**用 flatDeep 自我展平（那正是假阳性根源），改为断言"每个消息元素都是含 role/content 的对象 + 无嵌套数组"

## 29. profile 根 `cordis.yml` 启动时被重写为 `[]`

- **现象**：手动改了 `$DSH_HOME/profiles/<name>/cordis.yml`，重启后消失。
- **根因**：profile 根 cordis.yml 每次启动被程序重写为空列表，装配全靠 **patch 层**（`cordis.patch.yml`）。
- **规避**：**只改 patch 层**（`cordis.patch.yml`），不动 profile 根 cordis.yml。生效层序：bundle patch → profile patch → home patch → `--patch` 覆盖（后层优先）。

# 第五部分：技能注册与桥接扩展蒸馏（2026-08，E 系列）

## 30. 技能注册用 `ctx.skills.register()` 直注册，无需完整 provider

- **场景**：把本地 SKILL.md 注册为模型可见技能（非文件系统 provider 场景）。
- **做法**：`ctx.skills.register(SkillRegistration)`——`SkillRegistration = Omit<SkillDefinition, 'invocation'|'provider'> & { invocation?, provider? }`（含 name/description/content/source/resourceBase）。
- **要点**：
  - `ctx.skills` 是**可选依赖**：用 `ctx.get('skills')` 探测，缺失静默跳过（勿进 `inject`）
  - `content` = SKILL.md 全文；`resourceBase: { kind: 'directory', path }` 让模型可解析相对资源
  - 完整 `SkillProvider`（list/get）仅在需要动态目录/远程源时才实现；静态技能直注册更简单
- **生产级补齐**（dsh-memory skill-provider.ts 实测）：
  - **动态读文件**：`content = await readFile(join(skillRoot, 'SKILL.md'))`——比内联占位可配置
  - **补全字段**：`whenToUse`（触发时机）+ `invocation: { modelInvocable, userInvocable }`（双开关）+ `source/provider`（来源标识）——八个字段齐全
  - **降级**：`ctx.get('skills')` + try-catch 返回 boolean——技能注册失败不拖垮插件主体
  - **双通道架构**：工具给能力（执行）、技能给方法（指导）——配套注册形成"指导 + 执行"完整插件
  - **打包副本**：`bundledSkillRoot()` 指向包内副本（离线可用），见 harness-integration.md 3.0

## 31. DSH `Session` 公开面很薄，深度内容提取受限

- **现象**：想从 `agent.session` 读"最近用户消息"做自动存储，发现没有简单的 log/messages 读取方法。
- **根因**：`Session` 类 `private log` + `surface`（事件序号折叠视图），公开只有 `header`/`firstLiveSeq`/`surface`。
- **规避**：跨语言桥接的自动闭环用**可插拔提取回调**（默认占位 + 用户自定义）；深度解析需走 surface 事件模型（SessionEvent 折叠），标注为已知限制而非硬编码。

# 第六部分：DSH 插件开发实测补充（2026-08-17，dsh-context-pro 项目沉淀）

> 以下坑来自 `@kiwifruit/dsh-context-pro` 完整开发周期的实测验证——从零到 npm 发布，涵盖 pre-step waterfall、systemPrompt 契约、Events 声明合并、服务名解析等 DSH 特有的痛点。

## 32. `systemPrompt.section()` 字段名是 `text` 不是 `content` ⚠️ 有崩溃记录

- **现象**：插件加载正常，但每轮 agent 循环都崩溃：`Cannot read properties of undefined (reading 'indexOf')`。日志无 request/header 事件（LLM 调用前就崩了）。
- **根因**：`PromptSection` 接口声明 `{ name, order, text: string | ((ctx) => string) }`，但传了 `content` 字段。`section.text = undefined` → `systemPrompt.assemble()` 中 `interpolate()` 对 `text` 调 `indexOf('{{')` → `undefined.indexOf` 崩溃。
- **类型绕过**：`ctx.get('systemPrompt') as { section: (s: unknown) => ... }` 的 `(s: unknown)` 接受任何对象，tsc 不校验字段名。
- **规避**：
  - 传 **`text`** 而非 `content`
  - 用 `(s: PromptSection)` 替代 `(s: unknown)` 让 tsc 校检
  - 可导入 `@deepseek-ai/dsh-system-prompt` 的 `PromptSection` 接口
- **崩溃时机**：不在注册时（晚绑定），在每轮 `systemPrompt.assemble()` 时——所以插件上线后每个 turn 都崩，难以定位。

## 33. `inject` 服务名 ≠ cordis.yml 条目 id ⚠️ 易混淆

- **现象**：`inject: ['agent-loop']` 但插件永远 PENDING。cordis.yml 里有 `id: agent-loop` 的条目。
- **根因**：cordis.yml 的 `id` 是 loader 寻址用的条目标识；服务名由插件内部 `super(ctx, 'agentLoop')` 决定（camelCase）。条目 id 只是巧合同形，两者无强制约束。
- **规避**：写 inject 前必须 grep `super(ctx, '...')` 确认服务名；同类插件（time-context / tmux-context）用 `inject: ['agents']`（AgentRegistry——dsh-agent 默认导出，更抽象）。

## 34. pre-step `decision.messages` 必须扁平，agent-loop 不展平 ⚠️ 有数据损坏记录

- **现象**：插件开启后注入提示词成功、但模型**无法应答**；e2e 测试全部通过（假阳性）。
- **根因**：`appendContextToMessages()` 返回 `UserMessage[]`，但预判代码写了 `[...messages, injectedMessages]`（把数组当单个元素嵌套）。agent-loop `turn()` 对 `decision.messages` **逐条 `session.append('user/message', m)` 不展平** → 数组整体写入 session，`deriveMessages()` 产出数组"消息"，LLM 请求畸形 → API 校验失败。
- **规避**：
  - 返回 `appendContextToMessages(messages, injected)`（拿整数组），绝不二次包裹
  - e2e 断言**禁止 flatDeep 自我展平**（那是假阳性根源），改为断言"每个消息元素都是含 role/content 的对象 + 无嵌套数组"
- **延伸**：旧笔记误记"协议允许 UserMessage | UserMessage[] 嵌套（agent loop 侧展平）"——**这是错误假设**。实测 agent-loop 不展平。

## 35. Events 声明合并需要副作用导入，`import type` 不够

- **现象**：`import type { PreStepDecision } from '@deepseek-ai/dsh-agent'` 后，`ctx.on('agent/pre-step', ...)` 报 `is not assignable to parameter of type 'keyof Events'`。
- **根因**：`PreStepDecision` 是类型，不触发 `declare module '@deepseek-ai/cordis'` 的 Events 合并。Cordis 的 Events 声明合并依赖**模块的副作用执行**（`import` 值触发，`import type` 只传递类型）。
- **规避**：加一行**副作用导入**：`import '@deepseek-ai/dsh-agent'`（触发其 `declare module '@deepseek-ai/cordis'` 的 Events 合并）。类型导入和副作用导入可以并存。

## 36. `MessageId` 是 branded type，不能直接赋值 `string`

- **现象**：`id: \`ctx-pro-${Date.now()}\`` 报 `Type 'string' is not assignable to type 'MessageId'`。
- **根因**：`@deepseek-ai/dsh-llm` 的 `MessageId` 带 unique symbol 品牌，`string` 不兼容。
- **规避**：`id: \`ctx-pro-${Date.now()}\` as unknown as MessageId` 或 `MessageId(id)` 构造（如果导出构造器）。

## 37. schemastery 没有 `z.literal`，用 `Schema.const` 或 `Schema.union`

- **现象**：`z.literal('value')` 报 `Property 'literal' does not exist`。
- **根因**：schemastery 是 zod 风格但不是 zod。API 命名不同。
- **规避**：用 `Schema.const('value')` 或 `Schema.union([...])` 替代。

## 38. `ctx.effect()` 不能直接传 disposer 函数

- **现象**：`ctx.effect(dispose)` 报 TS2769（类型不匹配）。
- **根因**：effect 回调须返回 disposer/Effect，不能直接传 disposer 函数。
- **规避**：**`ctx.effect(() => dispose)`**——回调包装，返回 disposer。

## 39. `ctx.get('harness')` 无效——harness 不是服务是沙箱全局 ⚠️ 实测（dsh-context-pro）

- **现象**：`ctx.get('harness')` 始终返回 `undefined`，RPC handler 注册静默失败，Client UI 无数据。
- **根因**：`harness` 是 `node:vm` 沙箱全局变量（`cordis-host-runner/src/sandbox.ts` 第 30 行），**不是 Cordis 服务**。只在动态插件沙箱环境中可用，源码加载的插件（`file://` 路径）不在沙箱中运行，无法访问。
- **规避**：
  - 动态插件侧：`harness` 作为 Builtin 直接使用（`harness.handle('method', handler)`），无需 `ctx.get()`
  - 源码加载插件侧：需要持久 Client-Host 通信时，用 **`ctx.get('webServer').register()`** HTTP 端点替代（见 `client-ui.md` 第 5 节）
- **鉴别**：`ctx.get('name')` 返回 `undefined` ≠ 服务未挂载，也可能是该名称根本不是服务。写代码前 `cordis_inspect_query` 查 `Service.listService` 确认目标是否在服务清单中。

## 43. npm `files` 白名单漏运行时资产（发布后缺文件）⚠️ 实测

- **现象**：发布并 `dsh plugin add` 后插件加载报 `Cannot find module` 或运行时找不到 `python/` 等目录。
- **根因**：`package.json` 的 `files` 白名单只列了 `lib`，**漏了运行时资产目录**（如 `python/`、模板包、`cordis.patch.yml`），npm 发布时被排除。
- **规避**：`files` 必须显式包含 `lib` + 全部运行时资产 + `cordis.patch.yml`；发布前跑 **`npm pack --dry-run`** 核对 tarball 清单，再用 `npm pack <pkg>@<ver>` 回拉实测。

## 44. 发布制品漏声明 peer 依赖 → 运行时 Service 基类分裂

- **现象**：用户装插件后 `ctx.memory` 等挂到另一套 Context 原型，行为诡异。
- **根因**：`@deepseek-ai/cordis`、`@deepseek-ai/dsh-tools` 等**宿主已挂载**的服务被写进了 `dependencies`，pnpm/npm 为插件装了独立副本 → Service 基类两份，`ctx.xxx` 注册到不同的 Context 原型。
- **规避**：宿主已有服务一律 `peerDependencies`；真·独立依赖（如 schemastery 仅用于 Config schema）视宿主是否提供而 peer 或 dependency。

## 45. `node_modules` 半损坏：tsc 版本漂移指纹 ⚠️ 实测

- **现象**：`pnpm r build` 报 `x is not a function` / 类型错误像"换了个编译器"。
- **根因**：pnpm 判断依赖未变时**跳过重新构建**（`modules/.pnpm/lock.yaml` 缓存逻辑），但磁盘上的 `node_modules` 已半损坏（如 `@deepseek-ai/genai` 中途 install 被阻断）。
- **规避**：先看各方 `tsc` 版本（`pnpm exec tsc --version`），版本漂移即文件级损坏；整修三步：`rm -rf node_modules` → `pnpm install --force` → `pnpm rebuild <target>`。勿信 HMR 增量，依赖树必须重装验证。
