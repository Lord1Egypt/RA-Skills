> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：按症状检索的踩坑百科：25 条编号坑点（P1~P24，含 P22b）+ 症状速查表 + 报错信息/界面现象对照表 + 官方 4 篇事故复盘全文摘录与八条红线。插件出问题时第一站。
> **合成来源**：DSH插件开发实战补充-模板与踩坑.md（第三篇，略去与官方复盘重复的红线摘要） + DSH插件开发指导手册.md（附录 E 报错对照表） + F-official-pitfalls.md
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 671 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **上游素材原文**：约 200 行（32%），起点：`F-official-pitfalls.md`（文件末尾）。**不是本技能重写的整理稿**；性质不一——**有的是官方文档逐字摘录（属权威原文），有的是调研期粗笔记（仅备查）**。读某一段前，务必连带读**该段开头的取材说明**。
> - **其余部分 = 面向任务的整理稿**，可直接照做；但它同样是基线快照，写代码前先过版本闸门。
> - 常用检索：`grep -n '^### 坑 P'`（按编号定位单条坑）、`grep -n '^# F\.'`（档案起点）

---

<!-- ↓ 源：DSH插件开发实战补充-模板与踩坑.md 区间 1257-1620 -->

# 第三篇 · 踩坑百科（按症状检索）

> **用法**：先在下表找到你的症状 → 拿到坑号 → 跳到对应小节看「现象 → 根因 → 怎么修」。
> 全部坑来自 **社区真实仓库的 git 提交历史 + 官方 4 篇事故复盘 + 源码实证**（用到的仓库清单见 `11-glossary-and-provenance.md` §A.1），每条都标了来源。
> 每条坑的「来源」行用**素材代号 A~J** 标注证据出处（这些素材已合并进本套 references，**不随 skill 发布**，见 `11-glossary-and-provenance.md` §A.2）；能追到源码的另标 `packages/…` 等上游路径。

## 3.0 症状速查表

| 你看到的症状 | 坑号 | 一句话解法 |
|---|---|---|
| 装完插件毫无反应，`pnpm add` 却成功了 | **P1** | `package.json` 少了 `dsh.bundle.patch` |
| 装上了，界面/工具就是没有 | **P2** | `files` 漏了 `cordis.patch.yml`，或 `exports` 没暴露它 |
| 启动不报错、但生效的是另一行（0.1.6-alpha.1 起） | **P3** | 补丁里两行用了同一个 `id` |
| YAML 解析炸了 | **P4** | 补丁顶层写成了两个值（应该是单个数组） |
| 报 `cannot get property "xxx" without inject` | **P5** | 多写了一行 `export default`，Loader 丢弃了命名空间 |
| 可选服务读取报错，但顶层测试能过 | **P6** | 应该用 `ctx.get('x')`，不是 `ctx.x` |
| 工具注册被拒 / schema 报错 | **P7/P8** | `required` 写错层级（两条路径规则相反） |
| `!!js` 写了但不生效，还不报错 | **P9** | 该字段不被求值（只有 `config` 和 `disabled` 会） |
| 热更新后事件触发多次 / 越来越慢 | **P10** | 副作用没包 `ctx.effect`，清理函数没返回 |
| 热更新后报 `duplicate` / `already registered` | **P11** | 注册时没挂 `ctx.effect` |
| UI 插件改了没生效 | **P12** | 改的是 bundle 层 → **必须重启**，刷新没用 |
| 插槽注册了但界面上什么都没有 | **P13** | 解构丢了 `this` / 插槽名写错 / 注册时机不对 |
| 页面白屏，报 `__DSH_BOOT__ is missing` | **P14** | 只跑了裸 Vite，应用根本没起来 |
| 浏览器控制台报 `missed the module table` | **P15** | 浏览器半侧里用了非 type-only 的 `@deepseek-ai/*` 导入 |
| 卡片整个不渲染 | **P16** | 类实例方法当 React 回调没 `.bind()` |
| waterfall 写了但后续处理消失 | **P17** | 忘了 `await next()` |
| 报 `Cannot find package '@deepseek-ai/dsh-tools'` | **P18** | 官方装配不装 peers，要么镜像依赖要么零依赖 |
| 换台机器 / 换用户就崩 | **P19** | 硬编码了路径（如 Git Bash 路径、本机绝对路径） |
| 外部子进程读不到凭据 | **P20** | 环境被清洗，凭据必须显式列在 `env` 里 |
| 一段时间后整个 harness 挂掉 | **P21** | 一个坏的 client 插件会把整个 HARNESS 拖下水 |
| 卸载后刷新 404 | **P22** | 要在响应完成前先禁掉自己的 entry |
| 工具注册成功但模型看不到，或报 `ToolExecutorUnavailableError` | **P23** | 执行器已成独立插件，自建组合要自己挂；旧配置键 `mode` / `maxParallelSubCalls` 被拒 |
| 靠 `system-prompt/assemble` 筛工具，升级后条件不起作用 | **P24** | 该 waterfall 不再携带工具数组，改用 `register(def, { when })` |

---

## 3.1 安装类

### 坑 P1 · 装完毫无反应，但 `pnpm add` 成功了 ★★★

- **现象**：`dsh plugin --profile web add <你的包>` 返回成功，`node_modules` 里也有你的包，但插件完全不起作用。
- **你会看到这条警告**（逐字，来自源码 `packages/boot/plugin-manager/src/operations.ts:104`）：
  ```
  dsh: warning: <你的包名> declares no dsh.bundle — installed as a plain dependency, not a profile layer
  ```
  > ⚠️ **`dsh-v0.1.6-alpha.2` 起这句话变短了**：旧版结尾还有 `(a later update that gains one activates it automatically)` 一句，新版**已删掉**。你按旧文案去 grep 会一无所获。
- **根因**：`dsh plugin` 是 pnpm 转发器（`apps/cli/src/plugin.ts` 现在只做转发），装完会把 `dsh.profile.bundles` 与**实际安装状态**对账，实现已移到 `packages/boot/plugin-manager/src/operations.ts`。判定逻辑（逐字，`operations.ts:58-62`）：
  ```ts
  export function bundleManifest(name: string, dir: string, anchor: string): ProfileManifest | undefined {
    const packageDir = resolveBundleDir('dsh', name, anchor, dir)
    const manifest = readProfileManifest('dsh', packageDir)
    return manifest.dsh?.bundle?.patch === undefined ? undefined : manifest
  }
  ```
  对账循环（逐字，`operations.ts:82-92`）——**只有 `dsh.bundle.patch` 非 undefined 的包才会成为 profile 层**，其余打上面那条警告后跳过：
  ```ts
  for (const name of dependencies) {
    if (beforeDeps.has(name)) continue
    const metadata = bundleManifest(name, dir, anchor)
    if (metadata?.dsh?.bundle === undefined) {
      options.onOutput?.(`dsh: warning: ${name} declares no dsh.bundle — installed as a plain dependency, not a profile layer\n`, 'stderr')
      continue
    }
    loadOverlayPatches('dsh', join(resolveBundleDir('dsh', name, anchor, dir), metadata.dsh.bundle.patch))
    if (!bundles.includes(name)) {
      bundles.push(name)
    }
  }
  ```
- **怎么修**：`package.json` 加：
  ```json
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
  ```
  且包里**必须真的带**那个文件。
- **来源**：`packages/boot/plugin-manager/src/operations.ts`（`reconcile()` 起于 `:73`）；CLI 入口 `apps/cli/src/plugin.ts`；社区侧印证见素材 B 坑 M1（已拆入 `10b-casebook-tools.md`）。

### 坑 P2 · `files` 漏了补丁文件 ★★

- **现象**：本地开发正常，发布到 npm 后别人装上不生效。
- **根因**：`files` 白名单没包含 `cordis.patch.yml`（以及构建脚本、`lib/client.js`）。
- **怎么修**：
  ```json
  "files": ["lib/index.js", "cordis.patch.yml", "lib/client.js", "lib/types/**/*.d.ts"]
  "exports": {
    "./cordis.patch.yml": "./cordis.patch.yml"
  }
  ```
- **自查命令**：`npx publint`

### 坑 P3 · 补丁行「同 id 互相覆盖」与「应用失败不回滚」（**0.1.6-alpha.1 起语义已变**）★★

> ⚠️ **这一条在 0.1.6-alpha.1 上换了个方向。** 旧版是「重复 id → **启动即崩**，报 `TypeError: duplicate loader entry id`」；
> 新版把加载器改成**非事务化**（决策记录 `.agents/notes/implemented/simplification/2026-09-09-nontransactional-loader.md`），
> 那处校验被**整条删掉**了。于是同一个错误从「响亮地崩」变成了「**静默地错**」——这比原来难查得多。

- **现象（新版）**：`--dump-config` 里能看到你的行，进程也正常起来，但实际生效的是**另一行**（或你的插件行根本没激活）。
- **根因（两条，都要会认）**：
  1. **补丁里两行用了同一个 `id`** → 不再报错，而是在 `oldMap`/`newMap` 里**互相覆盖，后者胜**。
     你以为在「覆盖」，其实是在赌 YAML 里的行序 —— 而**行序本身没有加载语义**（见 S04）。
  2. **该行的 `apply()` 抛错** → 不再回滚，只在日志里写一条 `error`，**失败的行仍留在树上**。
     `Loader.create()` 返回 **≠** 插件已激活。
- **怎么修**：
  - `id` 仍然必须全局唯一（这不是宿主强制的规则了，而是你自己的纪律）。改之前先 `dsh --profile web --dump-config` 看现有 id 有没有撞。
  - **装完插件要两看**：① 看 `--dump-config` 里那行在不在；② **看启动日志有没有 `error`**。只看「进程起来了」会漏掉第 2 类。
  - 启动逻辑若依赖「某插件必须已激活」，**必须自己显式审计**，不能靠 `await` 的结果推断。
  - **双挂载的标准处理姿势**仍适用（来自 `better-sidebar` 的真实修复）：
    ```yaml
    - id: my-sidebar
      name: 'my-sidebar-plugin'
      # 官方层已经挂过时让位；注意 !!js 的可见范围是「同一补丁内它之前的行」
      disabled: !!js <判断条件>
    ```
- **⛔ 顺序敏感提醒**：`disabled: !!js` 里能看到的**只有同一补丁内它之前的行**（官方 `better-sidebar` 补丁注释原文：`only rows before this one are visible`）。所以"退让判断"必须写在被判断的那些行**之后**。
- **还剩下的「真崩」情形**：`duplicate prefix route`、界面上出现两个侧边栏 —— 这类由**注册期**发现，依旧会响亮地失败。
- **来源**：`vendor/loader/src/config/{group,tree,entry}.ts`；素材 D 坑 4.2（better-sidebar）、坑 3.x（anchored-standard）。

### 坑 P4 · 补丁顶层写成了两个值 ★

- **现象**：YAML 解析炸了。
- **根因**：盲目 append 导致文件里出现两个顶层 `- insert:`（YAML 顶层成了两个值）。
- **怎么修**：顶层**只能是一个数组**（一个 `- insert:`），要加内容就加到那个列表里。

### 坑 P5 · `export default` 丢弃命名空间 ★★★（官方复盘 0001）

- **现象**：插件"看起来装上了"，一调用就报
  ```
  Internal error: cannot get property "agents" without inject
  ```
  而且**所有单元测试都是绿的、覆盖率 100%**。
- **根因**：函数式插件多写了一行 `export default apply`。Loader 的规范化逻辑（逐字，`vendor/loader/src/index.ts`）：
  ```ts
  unwrapExports(exports: any) {
    if (isNullable(exports)) return exports
    exports = exports.default ?? exports        // ← prefers `.default`
    if (!exports.__esModule) return exports
    return exports.default ?? exports
  }
  ```
  存在 default 导出时，解析成**裸 `apply` 函数** —— 它没有 `inject`/`name`/`Config`（那些是**同级命名导出**）。Loader 基于空 `inject` 建 fiber，`apply` 拿不到任何服务。
- **怎么修**：**删掉 `export default`**。
- **官方教训原文**：
  > 命名空间插件与 default export 在 Cordis Loader 下互斥。选择命名空间形式（`name`/`inject`/`Config`/`apply`），不要添加 `export default`——`unwrapExports` 会丢弃命名空间。
  > 手动构建插件的测试无法验证插件的加载方式。至少一个测试必须端到端地驱动真实的 Loader/export 路径。
- **来源**：`docs/postmortem/0001-acp-default-export-drops-inject.zh.md`。

### 坑 P6 · 可选服务读取在真实拓扑下失败 ★★★（官方复盘 0001，Bug #2）

- **现象**：`cannot get property "sessionPersistence" without inject` —— 但从**顶层测试**读同一个服务却没问题。
- **根因**：`ctx.<name>` 是**可追踪代理**，解析时**只向祖先方向**遍历 fiber；而该服务在一个**兄弟**分支上。从插件 fiber 内部经 shadow 到达时必崩。测试从顶层调用时走的是提前绕过的全局查找（`if (!ctx.fiber.runtime) return ctx.reflect.get(prop, false)`），所以能过。
- **怎么修**：**读可选服务一律用 `ctx.get('name')`**（拓扑无关，且默认严格模式）。声明过的注入才用 `ctx.name`。
- **来源**：`docs/postmortem/0001-acp-default-export-drops-inject.zh.md` 根因 #2。

---

## 3.2 工具 / Schema 类

### 坑 P7 · `required` 写错层级（**最高频**）★★★

- **现象**：工具注册被拒，或参数校验报错。报错要么是
  ```
  parameters.<x>.required must be true when present
  ```
  要么是
  ```
  parameters.<x>.required must be an array of strings
  ```
- **根因**：DSH 有**两条**注册路径，`required` 位置**正好相反**（详见 **T3 §3.2**）：

  | 路径 | `parameters` 是什么 | 必填怎么写 |
  |---|---|---|
  | `defineTool()` | DSH 作者 DSL | **属性级** `required: true` |
  | 裸 `ctx.tools.register()` | 原始 JSON Schema | **对象级** `required: ['a']` |

- **怎么修**：先确定你走哪条路。**新手一律走 `defineTool`**：
  ```ts
  parameters: {
    query: { type: 'string', required: true, description: '...' },   // ✅ 属性级
  }
  ```
- **来源**：官方 `packages/core/tools/src/schema.ts:97-107, 293-296, 450-459, 571-572`；社区侧 `Tencent_WeKnora/packages/dsh-weknora/src/tools.ts`。

### 坑 P8 · `output.schema` 根节点写了 `required` ★

- **现象**：schema 校验报错。
- **根因**：`defineTool` 编译 `output.schema` 时，**根节点**以 `allowRequired: false` 起步（`schema.ts:427`），所以根上不能有 `required`。
- **怎么修**：`required` 只写在**对象节点的属性级**，不要写在根上。

### 坑 P9 · `!!js` 写了不生效，还不报错 ★★★（官方复盘 0002）

- **现象**：YAML 语法合法、加载无诊断信息，但表达式对象是 truthy，于是该行**永远是禁用的**。
- **根因**（原文逐字）：
  > Cordis Include 将每个 `!!js` 标量解析为一个表达式对象。Loader 递归地对插件的 `config` 进行插值，但直接读取 `disabled` 等配置项元数据。因此每个文件系统配置项看到的都是一个 truthy 对象，在所有模式下均保持禁用。
- **怎么修**：`!!js` **只在 `config:` 内部**（和当前版本的 `disabled:`）被求值；**其它 entry 元数据一律写字面量**。
- **额外教训（对调试极有用）**：这个 bug 被快照测试"掩盖"了 —— 工具不存在产生 `UNKNOWN_TOOL`，测试却把它当成了新的正确输出刷新进 fixture。
  > 快照刷新是 fixture 的生产过程，不是正确性审查。
- **来源**：`docs/postmortem/0002-js-expression-disabled-filesystem-tools.zh.md`。

---

### 坑 P23 · 工具注册成功、模型却调不到；或一调就报 `ToolExecutorUnavailableError` ★★★（**`0.2.2-alpha.2` 起的新形态**）
**现象**：`ctx.tools.register(...)` 不报错，但请求里根本没有这个工具；或者模型一调就抛 `ToolExecutorUnavailableError`；也可能启动直接失败，报 `Config` 校验错误。
**根因**：**`0.2.2-alpha.2` 起，「工具定义」与「工具执行」被拆成两层。** `@deepseek-ai/dsh-tools` 只留注册表与执行器选择，执行本体在独立插件里（`@deepseek-ai/dsh-tool-executor-native` 或 `-ptc`）。三处会咬人：
1. **自建组合没挂执行器** → `ctx.tools` 的 `private selectExecutor()` 找不到执行器即抛 `ToolExecutorUnavailableError`（`packages/core/tools/src/index.ts:357-366`，错误类在 `packages/core/tools/src/executor.ts:97`）。
2. **还在 `dsh-tools` 上写旧的执行配置** → `Config` 只剩两个 `z.never()` 占位：`mode`（`index.ts:102`，`Removed. Mount a native or PTC tool executor instead.`）与 `maxParallelSubCalls`（`:103`，`Moved to the PTC tool executor configuration.`）→ **写了就被拒**。
3. **以为 `DSH_TOOLS_MODE` 还能用** → 该环境变量**已不再被读取**（Web / headless / SDK 一律继承 base 的原生执行）。
**怎么修**：
```yaml
# 官方 base 补丁就是这么写的：原生 + PTC 各一行，PTC 默认关
- id: tool-executor-native
  name: '@deepseek-ai/dsh-tool-executor-native'
- id: tool-executor-ptc
  name: '@deepseek-ai/dsh-tool-executor-ptc'
  disabled: true
```
需要 PTC 时，用 overlay 补丁把两者对调（原生 `disabled: true` / PTC `disabled: false`），并确保 **`ctx.ptcRuntime` 在册** —— PTC 执行器把它声明为必需注入，缺了会阻止启动。
**判据**：`docs/upgrade-guide/v0.2.1-rc.2/tool-executor-plugins/guide.zh.md`（权威迁移指南）+ `packages/core/tools/src/index.ts:99-104` + `packages/bundle/base/cordis.patch.yml` 的 `tool-executor-*` 两行。
**顺带**：`dsh-agent-tool-presentation` 的 `Config.mode` 选择器**仍可用但已 `@deprecated`**（`packages/core/agent-tool-presentation/src/index.ts:23,25`）—— 它内部就是把对应执行器插件挂上去，别再往新代码里写。
---
### 坑 P24 · 在 `system-prompt/assemble` 里筛工具 —— 升级后**彻底失效**，而且不报错 ★★★
**现象**：原来靠 `system-prompt/assemble` waterfall 给工具做「按条件隐藏」的插件，升级后**条件完全不起作用**（工具照样全给模型）；读取 `assembly.tools` 的监听器要么拿到 `undefined`，要么直接在下游抛错。
**根因**：**`0.2.2-alpha.2` 起该 waterfall 不再携带工具数组。** 它只接收段落、上下文与变量（`PromptPresentation`），**返回的 `tools` 字段被忽略** —— 也就是说「在 waterfall 里增删工具声明」这条路被官方关掉了。而这次收窄**没有任何运行时报错**：你在 waterfall 里做的删除不再进入请求。
**怎么修**：把条件挪到**注册时**，用 `ToolRegistrationOptions.when`：
```ts
ctx.tools.register(defineTool({ /* … */ }), {
  when: ({ agent, modelSelection, signal }) => /* 同步或异步布尔 */,
})
```
- 条件在**每个拟议步骤**求值一次（`agent/pre-step` 与提示词组装之前），结果（`ResolvedToolSet`）同时决定**声明 / 原生分发 / PTC 绑定 / 嵌套调用**四处。
- 为假 → 四处一并移除；条件抛错 → 轮次以 `TOOL_ACTIVATION_FAILED` 结束；不属于已准入集合的调用 → `UNKNOWN_TOOL`，**不执行**。
- 若你在做**自定义执行器**，用 `ctx.tools.executable(name, agent, toolSet)` 逐次查找，别自己缓存注册表。
**两个连带坑**：① 步骤中途重新注册工具（热重载 / MCP 重连 / skill 重载）会让该步骤内**尚未开始**的调用失败 —— 已被准入的批次按原集合结算；② `exit_plan_mode` 现在**只在会话首次进入计划模式之后**才声明，所以「从未进过计划模式」的请求里它不会出现，快照测试要相应更新。
**判据**：`docs/upgrade-guide/v0.2.1-rc.2/conditional-tools/guide.zh.md` + `packages/core/tools/src/contracts.ts:105-126`。
## 3.3 生命周期 / 热更新类

### 坑 P10 · 副作用不回收 → 热更新后叠加 ★★★

- **现象**：改一次代码，事件回调就多触发一次；界面越改越慢。
- **根因**：加了监听/订阅却没返回清理函数。
- **怎么修（官方标准写法）**：
  ```ts
  ctx.effect(() => {
    media.addEventListener('change', onChange)
    return () => { media.removeEventListener('change', onChange) }   // ← 必须返回
  }, 'ui-theme: prefers-color-scheme listener')                       // ← 第二参是给人看的标签
  ```
  **凡是在插件里注册了外部资源（监听器、订阅、定时器），一律包进 `ctx.effect`。**
- **注册类 API 一般自带 disposer**，直接用返回值即可，不必再包：
  ```ts
  ctx.slots.register({ name: '...' }, Comp)   // 返回 () => void
  ctx.locale.register(NS, { zh, en })         // 返回 () => void（幂等）
  ```
  > ⚠️ **2026-09-30 更正**：本例第二行原写 `settings.register(ns, Schema)` —— 该 **Host 侧**入口随 `0.1.7-rc.1` 的设置机制重做**已被移除**（新树全树 0 命中），换成同一文件里仍有效的 `ctx.locale.register(...)`
  > （`packages/client/locale/src/client/index.ts:403-404` 的两个重载均返回 `() => void`）。**「注册类 API 自带 disposer」这条通用规则不变。**
- **来源**：官方 `packages/client/ui-theme/src/client/index.ts`。

### 坑 P11 · 裸注册 → 热重载报 `duplicate` ★★

- **现象**：热重载或禁用再启用后报 `duplicate` / `already registered`，功能异常。
- **根因**：`ctx.tools.register(x)` 直接调用、没挂 effect，插件卸载时不注销。
- **怎么修**：挂进 effect，保证 dispose 时注销：
  ```ts
  ctx.effect(() => ctx.tools.register(defineTool({ ... })))
  ```
- **官方硬规则原文**：
  > Registry contributions prove disposal through the HMR-safety test required by testing policy: **dispose the fiber and observe removal.**
- **来源**：`packages/AGENTS.md`；社区侧素材 B 坑 R2（`10b-casebook-tools.md`）、素材 D 坑 4.3（`10d-casebook-host-bundle.md`）。

### 坑 P12 · UI 插件改了没生效 —— 其实需要重启 ★★★

- **现象**：改了一行 UI，刷新页面没变化；或宿主报 `1 client package failed to compose`。
- **根因**：**分层的热更新能力不同**。
- **怎么修**（官方复盘 0003 的官方口径）：
  > 生产指南要求重新构建产物，并在刷新后验证既有 URL。开发指南说明 HMR 接收端始终开启；**同一源码检出目录中的 `pnpm run dev:web` 会重新构建客户端插件 bundle，实现免刷新的重载，而 Web shell 和普通包的改动仍然需要刷新页面**。
  - **改 `cordis.patch.yml` / `package.json` / bundle 层 → 必须重启**
  - 只改被按需服务的 `lib/client.js` → 刷新页面可能够
- **来源**：`docs/postmortem/0003-web-agent-gui-feedback-loop.zh.md`。

---

## 3.4 UI / 插槽类

### 坑 P13 · 插槽注册了但界面上没有 ★★★

- **三步排查**（来自社区 2444 次提交的反复修复）：
  1. **绝不写成 `const { register } = ctx.slots`** —— 解构丢 `this`，报
     `TypeError: Cannot read properties of undefined (reading 'effect')`。
     正确：`ctx.slots.register(...)`。
  2. **用 `ctx.slots.inject` 做延迟注册** —— 别在 `apply()` 一开始就注册（依赖服务可能还没就绪）。
  3. **查 DOM 锚点**：`document.querySelector('[data-slot="<你的插槽全名>"]')` ——
     **不在 = 插槽名错了；在 = 渲染/优先级问题**。
  4. 另外：`catch(e) {}` 空捕获是这类 bug 的头号帮凶 —— 先把异常打出来。
- **来源**：素材 A 坑 C1/C2/C4（已拆入 `10a-casebook-ui.md`）。

### 坑 P14 · 页面白屏，报 `window.__DSH_BOOT__ is missing` ★★

- **现象**：浏览器抛 `client-modules: window.__DSH_BOOT__ is missing or not an object`，白屏。
- **根因**（官方原文）：
  > 裸 Vite 返回 HTTP 200，使错误的启动路径看似合理。`window.__DSH_BOOT__` **只由完整宿主注入**，因此**传输层就绪不代表应用已就绪**。
- **怎么修**：用完整的 `dsh web` 启动，不要只跑裸 Vite；验收必须指向**用户原本打开的那个 URL**。
- **来源**：`docs/postmortem/0003-web-agent-gui-feedback-loop.zh.md`。

### 坑 P15 · `missed the module table`（浏览器半侧引入了非法依赖）★★

- **现象**：
  ```
  client-modules: require("...") missed the module table — not a platform seed word,
  not a materialized module, and no registered package factory
  ```
- **根因**：浏览器半侧里用了**非 type-only** 的 `@deepseek-ai/*` 导入。
- **怎么修**：
  - `@deepseek-ai/*` 只能写 `import type`
  - 要用值只允许平台种子表的 9 个 specifier：`react`、`react/jsx-runtime`、`react-dom`、`react-dom/client`、`@deepseek-ai/cordis`、`@deepseek-ai/dsh-client-store`、`@deepseek-ai/dsh-client-ui-slots`、`@deepseek-ai/dsh-client-ui-primitives`、`@deepseek-ai/dsh-client-ui-dockkit`（权威来源 `packages/client/web/src/platform.ts:8-14`；另可在 `dsh.client.external` 精确追加）
  - 需要别的插件的功能时，**不要 import**，改用 **cordis 服务**（`ctx.slots`/`ctx.sessions`/`ctx.workspaces`）或**插槽**
- **来源**：官方 `packages/AGENTS.md` 的"浏览器 bundle 纯度门" + `packages/client/tsdown.client.ts` 的 `dsh-client-bundle-purity` 插件 + 素材 A §二.5.1。详见 `14-inbound-http-and-timers.md` §17.3。

### 坑 P16 · 卡片整个不渲染（类实例方法当 React 回调）★★

- **现象**：
  ```
  TypeError: Cannot read properties of undefined (reading 'store')
      at getSnapshot (client.js:998)
      ... 
  slot entry crashed in 'settings.section'
  ```
- **根因**：`SettingsScope` 的 `subscribe`/`getSnapshot` 是读 `this.store` 的**原型方法**，React 的 `useSyncExternalStore` 当裸函数调用 → `this` 变 `undefined`。
- **⚠️ 时效说明（2026-09-23）**：`SettingsScope` 本体与手写卡片族已在 `dsh-v0.1.7-rc.1` **被移除** —— 这个具体场景不会再复现，**但下面那条通用规则仍然成立**（同类事故在 `ctx.slots.register` 等处照样发生），故本条按「**通用教训**」保留、不再指向具体 API。
- **怎么修**（社区维护者原话）：
  > `AutoSettingsPanel` now binds both methods to the scope with `useMemo` (`settings.subscribe.bind(settings)`)
- **通用规则**：**凡是把类实例的方法交给 React 当回调，一律 `.bind(instance)`**。闭包 store（`createSnapshotStore` 之类）不用 bind。
- **来源**：素材 A §二.3.3（已拆入 `10a-casebook-ui.md`）。

### 坑 P22 · 卸载后刷新 404 ★

- **现象**：卸载插件提示"热生效，刷新即可"，刷新后 404。
- **根因**：bundle 没了，但 loader entry 还在。
- **怎么修**：要在**响应完成之后、页面刷新之前**先禁掉自己的 entry；并且**明确告诉用户"已生效"还是"待重启"**。

---

## 3.5 Agent 流程 / 事件类

### 坑 P17 · waterfall 忘了 `await next()` → 静默吃掉后续处理 ★★★

- **现象**：写了拦截器之后，后续所有处理"消失"了，**而且不报错**。
- **根因**：waterfall 的语义是链式的 —— 不调 `next()` 就返回，等于**短路**。
- **怎么修**：
  ```ts
  // ✅ 保持原样，只观察
  ctx.on('agent/pre-step', async (payload, next) => {
    doSomething(payload)
    return next()
  })

  // ✅ 修改后继续
  ctx.on('agent/pre-step', async (payload, next) => {
    const decision = await next()
    return modified(decision)
  })
  ```
- **社区共识（多家仓库都踩过）**：`agent/pre-step`、`system-prompt/assemble`、`llm/stream` 这几个 waterfall 必须 `await next()` / `return next()`。

### 坑 P18 · system prompt 注入被 persona 整段丢弃 ★★

- **现象**：往 system prompt 里加内容，完全不生效。
- **根因**：`agent preset` 的 persona 若声明了 `complete: true`，会**丢弃其它插件贡献的 system prompt 段**。
- **怎么修**：加内容前先确认当前 persona 有没有 `complete: true`；有就换注入方式（如走 `agent/pre-step` 改消息）。
- **来源（官方一手源，MIT）**：**DSH 自身机制**，见素材 B 坑 O1（已拆入 `10b-casebook-tools.md`）。官方出处：`packages/preset/persona/src/index.ts:42-43,52,67` + 官方单测 `packages/core/system-prompt/tests/system-prompt.spec.ts:380-385`。**该条的社区来源（AGPL-3.0）已于 2026-09-16 移出本技能的引用集合。**

---

## 3.6 依赖 / 平台 / 构建类

### 坑 P19 · 官方装配不装 peers → `Cannot find package` ★★

- **现象**：本地能跑，换机器/换用户就崩，报
  ```
  Cannot find package '@deepseek-ai/dsh-tools'
  ```
- **根因**：官方装配**不安装 peerDependencies**。
- **怎么修**（二选一）：
  - **镜像**：每个 dsh peer 依赖也在 `devDependencies` 里写一份（官方 monorepo 的做法）；
  - **零依赖**：像 `Tencent/WeKnora` 那样**手写自己用到的接口类型**，完全不 import 宿主包（见 T4 §4.3）。

### 坑 P20 · 硬编码路径 / 平台差异 ★★

- **社区真实坑**（都来自 git 提交）：
  | 现象 | 根因 | 修法 |
  |---|---|---|
  | 换台机器找不到 shell | 硬编码了 Git Bash 安装路径 | 运行时探测，别写死 |
  | Windows 上路径被 Node spawn 解释错，报误导性 ENOENT | Git Bash 路径格式 | 用 `pathToFileURL` / 规范化 |
  | 装了 WSL 的机器上 `bash` 探测抢先命中 WSL，构建必挂 | 探测顺序 | 显式指定，或按 `process.platform` 分支 |
  | 子进程弹黑框 | Windows 默认窗口行为 | 加 `windowsHide` |
  | `.sh` 被 CRLF 检出 → `set: pipefail: invalid option name` | 换行符 | 加 `.gitattributes` 固定 LF |
- **官方跨平台标准写法**（见 T2 §2.3）：
  ```yaml
  disabled: !!js process.platform === 'win32'
  ```

### 坑 P21 · 一个坏的 client 插件把整个 HARNESS 拖下水 ★★

- **现象**：整个 harness 报 `Failed to load plugins`，所有功能都不可用。
- **根因**：客户端半侧的一个坏插件会导致整棵树加载失败。
- **怎么修**：
  - 客户端代码里所有异步都 try/catch，**绝不放走 rejection**；
  - 加错误边界与降级出口；
  - 用 `dsh --profile web --dump-config` 定位是哪一层出的问题。

### 坑 P22b · 外部子进程读不到凭据 ★★

- **现象**：spawn 出来的子进程拿不到 API key。
- **根因**（原文）：
  > @deepseek-ai/dsh-subprocess hands mcp-client a **scrubbed parent env with every credential-shaped name (/KEY|PASSWORD|SECRET|TOKEN/i) and every DSH_\* name removed**, precisely so harness credentials never leak into a spawned process implicitly.
- **怎么修**：`config.env` 里**显式列出**你需要的凭据：
  ```yaml
  env:
    DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY ?? ''
  ```
  `?? ''` 让值的类型保持字符串（该行 schema 是 string dict）。

---


---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 3010-3033 -->

# 附录 E 常见报错 / 现象对照表

| 现象 | 最可能原因 | 怎么办 |
|---|---|---|
| 插件完全没反应，进程静默退出（码 0） | 插件 PENDING（依赖缺失） | 找日志 `pending (waiting for service: ...)` |
| 启动报 `dsh: N entries did not activate` | 有插件一直 PENDING | 同上；检查 `inject` 里的服务名与提供方 |
| `ctx.tools is undefined` | 忘了 `export const inject = ['tools']` | 补上 |
| 插件"随机"读到 undefined 服务 | 用 `ctx.<name>` 读了未声明的服务 | 改成 `ctx.get('name')` |
| `inject` / `name` 全丢了，插件行为异常 | 命名导出插件里混了 `export default` | 删掉 `export default`（postmortem 0001） |
| 下游所有行为被吞掉 | waterfall 观察型监听器忘了 `next()` | 补 `return next()` |
| `ValidationError: invalid config` | 配置不符合 schema | 读报错里的路径（如 `$.targets`），改 `cordis.yml` |
| 装完插件毫无变化 | 包 manifest 缺 `dsh.bundle.patch` | 补字段，重新安装 |
| `dsh plugin add` 报错 | 少了 `--profile` | 写成 `dsh plugin --profile <name> add ...` |
| `--dump-config` 找不到我的层 | 装到了别的 profile | 检查 `--profile` 名字 |
| git 装包失败，提示 `allowBuilds` | pnpm ≥10 默认拒绝跑 `prepare` | 按提示把包键写进 `pnpm-workspace.yaml` |
| git 装完加载失败（找不到 `lib/`） | 作者没提供 `prepare`，拉到的是源码 | 让作者补 `prepare`，或改用 npm/tarball |
| 浏览器里看不到我的 UI | Host 半侧缺失 / 插槽名写错 / 没登记 | 查三个登记点；用 `cordis_inspect_query`（`Slots.*`） |
| 配置表单不显示 | 插件没有 `Config` schema，或该条目不在活动 profile 里 | 补 schemastery `Config`（**表单是它派生的**）；**不要**再写 `installSection` —— 它在 `0.1.7-rc.1` 已移除 |
| 改代码没生效 | HMR 默认关闭；overlay 不热重载 | 开启 `id: hmr` 的 `disabled: false`，或重启 |
| `ctx.logger` 输出看不到 | 交付 profile 未挂 console 导出器 | 改用 `console.log` 或自己挂 logger-console |
| 找不到"完整内置事件清单" | 官方就没有静态清单 | 去查 `docs/subsystems/<服务>.zh.md` 的生成区块 |

---


---

<!-- ↓ 源：F-official-pitfalls.md （全文） -->

# F. 官方事故复盘（postmortem）—— 官方自己踩过的坑（原始素材）

> 来源：`deepseek-harness/docs/postmortem/`（commit `86a402200d`）。共 **4 篇**，全部有中文版。
> 这是**一手的一手材料**：官方自己写的「事故 → 根因 → 防护措施 → 教训」。
> 引用一律逐字，标注来源文件。

| 编号 | 标题 | 一句话 |
|---|---|---|
| 0001 | ACP 服务器在连接时崩溃 —— `export default` 丢弃了插件的 `inject` | **一个多余导出 + 一个可选服务读法，让 178 个绿灯测试全部失效** |
| 0002 | 文件系统快照工具被永久禁用 | **`!!js` 只在插件 `config` 里被求值，写在 entry 的别的字段上等于写了块石头** |
| 0003 | Web agent 验收了替代服务器，而非其当前 GUI | **HTTP 200 ≠ 应用就绪；要验证的是"用户那个页面变了"** |
| 0004 | landlock 部分通知把子进程失败误分类 | （沙箱能力边界相关，对第三方插件作者参考价值较低） |

---

## 0001 · `export default` 丢弃 `inject`（**写插件必读，第一号杀手**）

**来源**：`docs/postmortem/0001-acp-default-export-drops-inject.zh.md`（113 行）

### 现象（逐字）

> ACP 服务器（`dsh --profile acp`、`@deepseek-ai/dsh-acp`）在真实编辑器（Zed）连接的瞬间崩溃：第一个 `session/new` 请求返回 `Internal error: cannot get property "agents" without inject`，`session/load` 对 `sessionPersistence` 返回同样的错误。尽管有 178 个绿色单元测试和 100% 行覆盖率，bridge 在生产环境中完全无法工作。

### 根因 #1：多写了一行 `export default apply`

事故代码（逐字）：

```ts
export const name = 'acp'
export const inject = ['agents', 'sessions', 'sessionPersistence']
export function apply(ctx: Context, config: AcpConfig): void { /* … */ }
// …
export default apply   // ← the bug
```

Loader 的规范化逻辑（逐字，`vendor/loader/src/index.ts`）：

```ts
unwrapExports(exports: any) {
  if (isNullable(exports)) return exports
  exports = exports.default ?? exports        // ← prefers `.default`
  if (!exports.__esModule) return exports
  return exports.default ?? exports
}
```

原文解释：

> 存在默认导出时，`exports.default ?? exports` 解析为**裸 `apply` 函数**。裸函数没有 `inject`、没有 `name`、没有 `Config` 属性——这些作为*同级*命名导出存在于模块命名空间上，而 unwrap 到 `.default` 把整个命名空间丢弃了。Loader 随后基于空的 `inject` 构建了插件的 fiber。

> 因此 `apply` 在一个**没有注入任何服务**的 fiber 中运行。第一行 `const agents = ctx.agents` 遍历 fiber 树（ROOT → Include → Loader → ROOT），在所有 fiber 的 store 中都找不到 `agents`，到达根 fiber（`runtime === null`）后抛出 `cannot get property "agents" without inject`。

> **修复：**删除 `export default apply`。

### 根因 #2：可选服务用 `ctx.x` 而不是 `ctx.get('x')`

> `AgentLoop` 的 `static inject` 故意不包含 `sessionPersistence`——注入它会导致非持久化的演示永远挂起，等待一个永远不会加载的后端。该服务由一个独立的兄弟插件/fiber 提供，以机会性方式读取。

fiber 遍历逻辑（逐字，`vendor/cordis/src/reflect.ts`）：

```ts
let fiber = (ctx[symbols.shadow] as Context ?? ctx).fiber   // ← starts at AgentLoop's fiber
while (true) {
  const impl = fiber.store?.[prop]
  if (impl) return getTraceable(ctx, impl.value)
  if (prop in fiber.inject) { /* inactive-context error */ }
  if (!fiber.runtime) throw error                            // ← reached root, throw
  if (fiber.parent[symbols.isolate][prop] !== key) throw error
  fiber = fiber.parent.fiber                                 // ← ancestor-only
}
```

> 遍历**仅向祖先方向**进行。`sessionPersistence` 既不在 `AgentLoop` 的 fiber store 中（不在其 `static inject` 中），也不在通往 root 的任何祖先上（它位于一个*兄弟*分支），因此遍历到达根 fiber 后抛错。

> **修复：**使用 `ctx.get('sessionPersistence')` 读取可选服务……对于插件声明注入集中的服务，直接属性读取仍然适用。

### 为什么 178 个测试全没抓到（原文核心句）

> 两个 bug 都源于同一个根本流程缺口：**没有任何测试通过插件的真实加载路径或真实调用拓扑来驱动它。**

> 内存 harness 通过手动构建插件对象来挂载 bridge：`ctx.plugin({ name, inject, apply })`。这手动提供了 `inject`，因此永远无法复现 Bug #1——`unwrapExports` 只被 *Loader* 调用，`ctx.plugin` 从不调用它。

> 100% 行覆盖率始终满足。覆盖率证明代码行*被执行过*；它不能说明功能是否*按交付方式正常工作*。

### 教训（逐字）

> - 命名空间插件与 default export 在 Cordis Loader 下互斥。选择命名空间形式（`name`/`inject`/`Config`/`apply`），不要添加 `export default`——`unwrapExports` 会丢弃命名空间。
> - 对于插件机会性读取但未在 `static inject` 中声明的服务，使用 `ctx.get(name)`，绝不使用 `ctx.<name>`。属性代理通过仅向祖先方向的 fiber 遍历解析，经由外部 shadow 时会失败；`ctx.get(name)` 是拓扑无关的查找（且默认采用严格模式——非活跃后端读取为 `undefined`，不会在 teardown 期间仍将该后端返回给调用方）。
> - 手动构建插件的测试无法验证插件的加载方式。至少一个测试必须端到端地驱动真实的 Loader/export 路径。当核心操作不调用模型时，该测试无需 API key——因此它属于 CI，而非 key 门控之后。
> - 相信跟踪结果，不要迷信理论。……

### 对新手的三句人话

1. **插件文件里永远只写具名导出**（`name`/`inject`/`Config`/`apply`），一行 `export default` 都别加 —— 加了之后插件会"看起来装上了"，但一调用就报 `cannot get property "xxx" without inject`。
2. **要读"可能没有"的服务，用 `ctx.get('xxx')`**，别写 `ctx.xxx`。
3. **本地手搓测试全绿 ≠ 插件能用**。你必须真的让 dsh 加载它一次。

---

## 0002 · `!!js` 表达式只在 `plugin config` 里被求值

**来源**：`docs/postmortem/0002-js-expression-disabled-filesystem-tools.zh.md`（47 行）

### 现象（逐字）

> ACP（Agent Client Protocol）示例试图通过 `disabled: !!js ...` 有条件地启用文件系统插件，但 Cordis 仅在插件 `config` 内部对 JavaScript 表达式求值。原始的表达式对象为 truthy，因此文件系统栈始终处于禁用状态。快照刷新随后将 `UNKNOWN_TOOL` 结果接受为新的预期输出。

### 根因（逐字）

> Cordis Include 将每个 `!!js` 标量解析为一个表达式对象。Loader 递归地对插件的 `config` 进行插值，但直接读取 `disabled` 等配置项元数据。因此每个文件系统配置项看到的都是一个 truthy 对象，在所有模式下均保持禁用。

> 实现时假设 `!!js` 适用于整个 Loader 配置项。实际只有 `entry.options.config` 使用它：`Entry._resolveConfig()` 对该字段进行插值，而 `Entry.disabled` 直接测试 `entry.options.disabled`，不经过插值。YAML 标签在语法上合法，因此加载过程不产生任何诊断信息。

### 修复后的官方口径（逐字）

> [`AGENTS.md`](../../AGENTS.md) 与 [Cordis 入门](../cordis-primer.zh.md#loader-configuration)明确说明 `!!js` 在插件 `config` 与配置项 `disabled` 内有效；其他配置项元数据保持字面量，因此条件式组合使用 overlay。

> `verify-cordis-config` 解析仓库中的 Cordis YAML，拒绝 Loader 配置项元数据中的表达式节点（包括 include patch 和插入的配置项）。

> `dsh-session-snapshot` 在全新运行和已提交的会话 fixture 中拒绝结构化的 `UNKNOWN_TOOL` 结果，防止其被提交为预期输出。

### ⚠️ 版本注记（诚实标注）

本复盘记录的**是修复前**的行为（`disabled` 不求值）。修复后，官方文档与 `packages/bundle/base/cordis.patch.yml` 都在用 `disabled: !!js process.platform === 'win32'` —— 说明当前版本**已支持** `disabled` 的表达式求值。

**给新手的可操作规则**：
- `!!js` **可以**写在 `config:` 内部（确定支持）。
- `!!js` **可以**写在 entry 的 `disabled:` 上（当前版本支持，有官方 base 补丁为证）。
- **其它任何 entry 元数据字段**（如 `id`、`name`）一律写**字面量**，不要写表达式。

### 教训（逐字）

> - 语法上被接受的配置值不一定在该位置被求值；应记录并验证具体对哪些字段进行插值。
> - 快照刷新是 fixture 的生产过程，不是正确性审查。诸如已注册工具缺失这类语义上不可能的结果，需要独立于预期输出的断言。
> - 权限控制只应描述其实际管辖的能力。

### 对新手的人话

**"YAML 语法合法" ≠ "这个位置会求值"。** 写 `!!js` 却发现没生效时，先查官方文档里该字段是否在插值范围内，不要在 YAML 语法上找原因（它不报错，是静默失效）。

**额外教训（对调试极有用）**：这个 bug 被快照测试"掩盖"了 —— 工具不存在产生 `UNKNOWN_TOOL`，测试却把 `UNKNOWN_TOOL` 当成了新的正确输出刷新进 fixture。**刷新快照 ≠ 验证正确性。**

---

## 0003 · Web agent 验收了"替代服务器"，而非用户当前页面

**来源**：`docs/postmortem/0003-web-agent-gui-feedback-loop.zh.md`（53 行）

### 现象（逐字）

> Web agent 修改了 GUI 源码，却不知道当前会话对应哪个 URL、由哪个进程承载。它把验收交还给用户，随后在 `window.__DSH_BOOT__` 缺失导致白屏的情况下，仍把裸 Vite 返回的 HTTP 200 当作成功；最后，原页面其实已经加载了重建产物，它却去验收另一个端口上的替代 `dsh web` 服务器。

### 关键根因（逐字）

> 裸 Vite 返回 HTTP 200，使错误的启动路径看似合理。`window.__DSH_BOOT__` 只由完整宿主注入，因此**传输层就绪不代表应用已就绪**。

> agent 还通过 shell `&` 绕过了后台进程语义，因此任务身份、完成通知、结果收集和清理机制均未生效。验证端口 3334 只能证明第二个服务可以工作。

### 教训（逐字）

> - agent 必须先知道隐藏的运行时前置条件，才能指导用户；启动模式属于应用上下文，不应依赖团队口口相传。
> - HTTP 就绪、构建成功和启动 manifest 是不同的事实。验收必须明确指定确切的 origin，并从外部观察所请求的改动是否在该 origin 生效。
> - 替代服务无法证明既有页面已经改变。确实收到启动长时间运行进程的请求时，应使用受管任务生命周期。
> - 回归测试必须能够针对所报告的机制失败。进程超时不等同于快速失败，进程退出后端口可用也不能证明该端口从未被绑定。

### 对新手的人话（**写 UI 插件时最实用**）

1. **"我改了代码" ≠ "用户在用的那个页面变了"**。改完 UI 插件，必须回到**用户原本打开的那个 URL**刷新验证，而不是自己另起一个端口。
2. **HTTP 200 什么都不证明**。DSH Web 的客户端插件 bundle 是靠宿主注入启动清单（`window.__DSH_BOOT__`）才活起来的；只跑裸 Vite 会白屏。
3. **不要用 shell `&` 起后台进程**，用受管的任务机制（否则进程身份、通知、清理全失效）。

---

## 0004 · landlock 部分通知把子进程失败误分类

**来源**：`docs/postmortem/0004-landlock-partial-notice-misclassified-child-failures.zh.md`（55 行）

> 说明：本篇涉及 Linux landlock 沙箱的内核能力探测细节，**对第三方插件作者参考价值低**，此处仅登记存在性与主题。（未逐字摘录；如需请直接读原文。）

**可迁移的一条通用教训**：**"部分成功"的返回值如果被当成"完全成功"，错误会被静默降级。** 当你写一个封装外部能力的服务时，返回值要区分"完全成功 / 部分成功 / 失败"，不要让调用方把部分成功当成功。

---

## 归纳：4 篇复盘提炼出的「插件作者红线」

| # | 红线 | 出处 |
|---|---|---|
| 1 | **绝不写 `export default`**（函数式插件） | 0001 |
| 2 | 可选服务一律 `ctx.get('x')`，不写 `ctx.x` | 0001 |
| 3 | 手搓测试不算数，必须让真 Loader 加载一次 | 0001 |
| 4 | `!!js` 只在 `config` 与 `disabled` 内求值，其它字段写字面量 | 0002 |
| 5 | 快照/绿灯刷新 ≠ 正确性验证 | 0002 |
| 6 | 验收要指向"用户那个 URL / 那个进程"，HTTP 200 不算 | 0003 |
| 7 | 别用 shell `&` 起后台进程，用受管任务机制 | 0003 |
| 8 | 部分成功不能当成功返回 | 0004 |

---

