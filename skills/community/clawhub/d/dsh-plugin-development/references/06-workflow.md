> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：插件开发的完整工作流，四部分顺序阅读：① 环境准备（版本对照、从源码跑起来、三个环境坑、验收清单）② CLI 与安装机制逐字实证（DSH_HOME 默认值、profile 目录布局、dsh plugin 的 pnpm 转发逻辑、declares no dsh.bundle 警告的判定代码）③ 打包与分发（文件结构、package.json 逐字、patch 引用、三种分发方式对比）④ 调试与排错五招 + 五步排错法。注意：DSH_HOME 与 profile 在 ① 和 ② 都出现，以 ② 的源码实证为准。
> **合成来源**：DSH插件开发指导手册.md（第 2/11/12 章） + G-install-and-cli.md
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 749 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **上游素材原文**：约 259 行（36%），起点：`G-install-and-cli.md`（文件开头）。**不是本技能重写的整理稿**；性质不一——**有的是官方文档逐字摘录（属权威原文），有的是调研期粗笔记（仅备查）**。读某一段前，务必连带读**该段开头的取材说明**。
> - **其余部分 = 面向任务的整理稿**，可直接照做；但它同样是基线快照，写代码前先过版本闸门。
> - 常用检索：`grep -n '^## '`（四部分）、`grep -n '^# G\.'`（档案起点）

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 254-360 -->

# 第 2 章 环境准备

## 2.1 版本对照

| 组件 | 要求 | 检查命令 |
|---|---|---|
| Node.js | `^22.19.0 \|\| >=24.0.0` | `node --version` |
| pnpm | 建议 11.x | `pnpm --version` |
| Git | 较新版本 | `git --version` |

## 2.2 从源码跑起来

官方路径（`README.zh.md:37-43`）：

```sh
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

⚠️ **这一步很重**。本机实测：仓库全量克隆后工作区 10,319 个文件、286 MB；构建会跑 tsc（类型编译）+ tsdown（打包）。第一次请留出充足时间，并且**不要中断**。

**也可以用 npx 跳过源码构建**（`README.zh.md:26`）：

```sh
npx @deepseek-ai/dsh web
```

⚠️ 但手册后续章节要用 `--patch` 加载本地 TypeScript 源码，这需要源码检出（因为要用 tsx 直接跑 `.ts`）。所以**做插件开发，还是老老实实用源码路径**。

## 2.3 DSH_HOME 在哪里

源码实证（`packages/util/home-paths/src/index.ts`）：

```ts
export const DSH_HOME_DIR_NAME = '.dsh'
export const DEFAULT_DSH_HOME_DISPLAY = `~/${DSH_HOME_DIR_NAME}`
export const DSH_HOME_ENV = 'DSH_HOME'
```

**解析优先级**：显式配置 > 环境变量 `$DSH_HOME` > `~/.dsh`

在你的 Windows 机器上就是：

```
C:\Users\<你的用户名>\.dsh
```

⚠️ **新手建议**：前期**不要**去改 `$DSH_HOME`。用默认值，出问题时路径才和文档对得上。

## 2.4 三个环境坑（提前告诉你，省 2 小时）

### 坑 1：默认看不到 Cordis 日志

源码实证：官方交付的组合包里**没有挂载** console 日志导出器 `@deepseek-ai/cordis-plugin-logger-console`（全仓库只有测试 fixture 挂载了它）。

- ✅ `console.log(...)` —— **能看见**
- ⚠️ `ctx.logger('x').info(...)` —— **默认看不见**

所以本手册所有示例都用 `console.log`。等你想用正式日志时，需要自己把 logger-console 插件插进组合。

### 坑 2：HMR 的模块名、默认开关、监听根**三样都变了** ★

源码实证（`packages/bundle/base/cordis.patch.yml`，`dsh-v0.1.6-alpha.2` 起）：

```yaml
# Profile configuration reloads by default; module roots are opt-in.
- id: hmr
  name: '@deepseek-ai/dsh-hmr'
  disabled: !!js "!ctx.get('profileContext')"
  config:
    root: []
```

与旧版（≤ `dsh-v0.1.6-alpha.1`）的三处差异：

| 项 | 旧 | 新（`alpha.2` 起） |
|---|---|---|
| 模块名 | `@deepseek-ai/cordis-plugin-hmr` | **`@deepseek-ai/dsh-hmr`**（工作区仍保留 vendored 包） |
| 默认启用 | `disabled: true`（恒关） | `disabled: !ctx.get('profileContext')` —— **有 profile 上下文就开**（profile 的配置改动会自动重载） |
| 监听根 | `root: ['.']` | `root: []` —— **模块根改为显式 opt-in** |

**官方原话**（`packages/boot/hmr/README.zh.md:36`，逐字）：

> 已有配置将模块名 `@deepseek-ai/cordis-plugin-hmr` 替换为 `@deepseek-ai/dsh-hmr`。继续提供 `hmr` 服务键、`baseDir`、`config`、`getLinked()`、`getOuterStack()`、`hmr/change` 和 `hmr/reload`。工作区保留 vendored 包；DSH profile 使用本包。

→ **迁移动作只有一条：把模块名换掉。** 服务键、配置键、事件名都没动。想恢复监听模块根，在你的 patch 里覆盖这一行（patch 是**替换整行 config**，所以要把想保留的键重述）：

```yaml
- id: hmr
  name: '@deepseek-ai/dsh-hmr'
  config:
    root: ['.']
```

⚠️ HMR 仍依赖 `@deepseek-ai/cordis-plugin-timer`（`packages/boot/hmr/package.json:31` 的 peerDependency），缺了它会永久 PENDING。

### 坑 3：改了 `cordis.yml` 里的 `config` 会自动热替换

`docs/user/develop/basic/config.zh.md:100` 原文：

> 配置变更会触发插件热替换：修改 `cordis.yml` 中某个插件的 `config` 后，框架会卸载旧实例并加载新实例。

**但注意**：`--patch` 指定的 overlay 文件**本身不会被热重载**（源码 `profile-boot.ts:328-333`）。只有 profile 与 home 的 `cordis.patch.yml` 会被 watch。所以开发期改代码要**重启进程**，或者开启 HMR。

## 2.5 ✅ 环境验收清单

- [ ] `node --version` 输出满足 `^22.19 || >=24`
- [ ] `pnpm --version` 有输出
- [ ] 仓库已克隆，`pnpm install` 成功
- [ ] `pnpm run build` 成功（无红字）
- [ ] `pnpm dsh web` 能启动，浏览器打开 `http://127.0.0.1:3080` 能看到界面
- [ ] 能找到 `C:\Users\<你>\.dsh\profiles\web\` 目录

**任何一项不通过，先别往下走。** 把报错原文丢给你的 AI Agent，让它在这一章范围内排查。

---


---

<!-- ↓ 源：G-install-and-cli.md （全文） -->

# G. 安装 / 运行 / CLI 机制 —— 逐字实证（原始素材）

> 来源：`deepseek-harness`（commit `86a402200d`）。全部结论附**源码路径或命令原文**。
> 这份笔记解决新手最容易搞错的三个问题：**插件装到哪、怎么装、装完为什么没生效**。

---

## 1. `$DSH_HOME` 与 profile 目录（**插件装在这里**）

### 1.1 `$DSH_HOME` 默认值

逐字证据（**4 个不同包都这么写**，互为交叉印证）：

> `packages/credentials/credentials-local/src/index.ts:67`
> ```
> /** Harness home used when `path` is omitted; defaults to `$DSH_HOME` or `~/.dsh`. */
> ```

> `packages/shell/shell-env/src/index.ts:31`
> ```
> /** DeepSeek Harness home directory exposed as `DSH_HOME`; defaults to `$DSH_HOME` or `~/.dsh`. */
> ```

> `packages/skill/skill-filesystem/src/index.ts:53`
> ```
> /** DeepSeek Harness config root. Defaults to `$DSH_HOME` or `~/.dsh`. */
> ```

**结论**：`$DSH_HOME` 默认是 **`~/.dsh`**（Windows 即 `C:\Users\<你>\.dsh`）。所有用户级配置、凭据、设置都在这里。

### 1.2 profile 是什么、在哪

逐字证据（`packages/boot/app-boot/src/profile.ts`）：

> 第 5 行：
> ```
> * A profile is a directory under `$DSH_HOME/profiles/<name>` holding a
> ```

> 第 16-20 行：
> ```
> * Module resolution is two-anchor by construction: a bundle name resolves
> first from the dsh installation (the launcher's own package), then from the
> profile directory. Pnpm-managed entries in the profile's `node_modules`
> resolve first. The runtime resolution supplies packages carried by the
> installation and selected bundles to Node's ESM and CommonJS resolvers.
> ```

> 第 37 行：
> ```ts
> export const PROFILES_DIR = 'profiles'
> ```

> 第 226-229 行：
> ```
> // The hoisted linker gives out-of-tree plugins a flat node_modules whose
> // missing peers (cordis and friends) use the runtime resolution, so every plugin shares the
> // installation's single cordis instance instead of a duplicate. pnpm ≥10
> ```

**结论（目录布局）**：

```
~/.dsh/                                   ← $DSH_HOME
└── profiles/
    ├── node_modules/                     ← 已安装插件（所有 profile 共享）
    ├── web/                              ← web profile 目录
    │   ├── package.json                  ← 该 profile 的依赖清单 + dsh.profile.bundles
    │   └── cordis.patch.yml              ← 用户自己的补丁层（写在这里）
    ├── tui/
    ├── headless/
    └── acp/
```

> 💡 **关键理解**：**profile = 一个"插件栈"**。官方原文（`apps/cli/src/args.ts:156`）：
> ```
> 'dsh: boot a DeepSeek Harness profile — an ordered stack of plugin-bundle patch layers under your own overrides.'
> ```
> 翻译：profile 是**「一串有序的 bundle 补丁层，叠在用户自己的覆盖层之下」**。

---

## 2. `dsh plugin` 命令 = pnpm 转发器（**装插件的唯一官方姿势**）

### 2.1 帮助原文（逐字，`apps/cli/src/args.ts:90-99`）

```
Examples:
  dsh --profile web                          boot the web profile (same as: dsh web)
  dsh --profile rescue --from-default-profile web
                                             create rescue from the shipped web template, then boot it
  dsh --profile headless "run the tests"     answer one task, print the result, and exit
  dsh --profile tui --patch ./extra.yml      boot a custom profile with one extra overlay
  dsh --profile tui --resume <session>       arguments after the launcher flags reach the app
  dsh --profile web --help                   the web app's own flags and help
  dsh plugin --profile tui add <package>     install a plugin into the tui profile
```

### 2.2 `--profile` 是**必填**（逐字，`apps/cli/src/args.ts:187-197`）

```ts
  const plugin = program.command('plugin').description('manage a profile\'s plugins by forwarding the remaining arguments to pnpm in the profile directory')
  plugin
    .requiredOption('--profile <name>', 'the profile whose plugins to manage (initialized on first use)')
    ...
      if (args.length === 0) program.error('error: plugin needs pnpm arguments to forward (e.g. add <package>)')
```

> 🔥 `--profile` 用的是 `.requiredOption(...)` —— **省略直接报错**。网上流传的 `dsh plugin add xxx` 是错的。

### 2.3 它到底做了什么（`dsh-v0.1.6-alpha.2` 起是**两层**）

**第一层 · CLI 入口**（`apps/cli/src/plugin.ts`，全文 25 行，逐字 `:1-2` 与 `:12-18`）：

```ts
/** dsh plugin forwards pnpm through the shared profile package operations. */
import { runPluginCommand } from '@deepseek-ai/dsh-plugin-manager/operations'

export async function runPlugin(profile: string, args: readonly string[]): Promise<number> {
  const result = await runPluginCommand({ profile, installAnchor: INSTALL_ANCHOR, cwd: process.cwd() }, args, {
    execution: 'cli',
    outputBytes: 16384,
    lockWaitMs: 120000,
    onOutput: (text, stream) => { process[stream].write(text) },
  })
```

**第二层 · 真正的实现**（`packages/boot/plugin-manager/src/operations.ts`，逐字 `:72-73`）：

```ts
/** Reconcile package removals and newly installed bundles without re-enabling retained dependencies. */
async function reconcile(before: ProfileManifest, dir: string, anchor: string, options: PackageOperationOptions): Promise<void> {
```

**三步**：
1. 首次使用时初始化 profile；
2. 在 profile 目录里跑 `pnpm <你的参数>`；
3. 把 `dsh.profile.bundles` 层列表与**实际安装状态**对账（`reconcile()`：依赖解析到声明了 `dsh.bundle` 的包 → 进层栈；被移除或没声明的 → 出栈）。

> ⚠️ **定位变了**：`apps/cli/src/plugin.ts` 在 `alpha.1 → alpha.2` 之间从 **163 行缩到 25 行**，对账逻辑整体搬进 `@deepseek-ai/dsh-plugin-manager`（新包，`packages/boot/plugin-manager/`）。按旧文档去 CLI 文件里找 `exportsPatch()` 会扑空。
>
> 顺带新增的两条 CLI 诊断（`:19-23`）：`pnpm` 不在 PATH 时打印 `dsh: pnpm was not found`；走 `git+` / `github:` / `.git` 的依赖装失败时，直接提示把 pnpm 打印的键加到 profile 的 `pnpm-workspace.yaml` 的 `allowBuilds` 下（见 §4 的 git 安装一节）。

### 2.4 装插件最常见的那个警告（逐字，`packages/boot/plugin-manager/src/operations.ts:103-106`）

```ts
    if (metadata?.dsh?.bundle === undefined) {
      options.onOutput?.(`dsh: warning: ${name} declares no dsh.bundle — installed as a plain dependency, not a profile layer\n`, 'stderr')
      continue
    }
```

**你实际会看到的完整警告**：

```
dsh: warning: <你的包名> declares no dsh.bundle — installed as a plain dependency, not a profile layer
```

> ⚠️ `dsh-v0.1.6-alpha.2` 起**结尾那句 `(a later update that gains one activates it automatically)` 被删掉了**——按旧文案去 grep 会一无所获。语义没变：先按普通依赖装进去，之后某版补上 `dsh.bundle` 时会被自动激活（对账看的是**安装状态**，不是依赖 diff）。

> ## 🔴 这是新手第一号安装事故
> `pnpm add` 会成功、`node_modules` 里也有你的包，**但插件完全不起作用**——因为你只在 `package.json` 里写了 `dsh.client` 或什么都没写，**没写 `dsh.bundle.patch`**。
> 判定逻辑（逐字，`plugin.ts`）：
> ```ts
> function exportsPatch(packageName: string, profileDir: string): boolean {
>   let dir: string
>   try {
>     dir = resolveBundleDir(NAME, packageName, INSTALL_ANCHOR, profileDir)
>   } catch {
>     return false // pnpm reported success yet the package is unresolvable — treat as plain
>   }
>   const manifest = readProfileManifest(NAME, dir)
>   return manifest.dsh?.bundle?.patch !== undefined
> }
> ```
> **只有 `dsh.bundle.patch !== undefined` 的包才会成为 profile 层。**
> 所以：**你的插件 `package.json` 必须有 `"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }`**，并且**包里必须真的带上那个 `cordis.patch.yml`**（写进 `files` 白名单，写进 `exports`）。

### 2.5 「reconcile by installed state」的深意（原文逐字，`plugin.ts` 注释）

```
 * Reconcile `dsh.profile.bundles` against the installed state: pnpm has
 * already written the real installed names (so a git/path/tarball/alias spec
 * on the command line reconciles by its true package name) and materialized
 * the packages. A dependency that resolves to a `dsh.bundle`-declaring
 * package joins the layer stack (appended in dependency order); a
 * dependency-listed name that no longer does — removed, or the installed
 * version dropped the declaration — leaves it. In-box bundles from the
 * profile template are not dependencies and are never touched.
```

**三个可操作结论**：
1. 命令行里的 `git+https://...` / `file:../x` / `./x.tgz` 各种写法**都能装**，对账用**真实包名**。
2. 你的包**后来才加上** `dsh.bundle` 声明时，`dsh plugin ... update` 会**自动激活**它（不需要额外命令）。
3. **profile 模板自带的 bundle 层不受影响**（它们不是依赖项）。

---

## 3. 启动与常用命令（逐字，`apps/cli/src/args.ts`）

| 命令 | 作用 |
|---|---|
| `dsh --profile web` | 启动 web profile（等价于 `dsh web`） |
| `dsh --profile headless "跑一下测试"` | 单任务模式：回答一次、打印结果、退出 |
| `dsh --profile tui --patch ./extra.yml` | 启动自定义 profile，额外叠一层补丁 |
| `dsh --profile web --dump-config` | **打印组装后的完整配置树**（调试神器） |
| `dsh --profile web --dump-default-config` | 只打印 bundle 层（不含 `--patch`） |
| `dsh --profile web --dump-config-schema` | 🆕 `0.1.7-rc.1`：打印配置的 **JSON Schema**（条目/补丁可用的键与类型；**接受** `--patch`） |
| `dsh --profile <名字> --from-default-profile web` | 从官方 web 模板复制出一个新 profile 再启动 |
| `dsh plugin --profile web add <包>` | 装插件 |
| `dsh plugin --profile web update` | 更新插件（会重新对账 bundle 层） |
| `dsh plugin --profile web remove <包>` | 卸插件 |

**两个约束（逐字）**：
- `web` 是 `--profile web` 的硬编码别名（`args.ts:13`：`\`web\` is a hardcoded alias for \`--profile web\``）
- `desktop` profile 禁止手动操作（`args.ts:70`）：
  ```ts
  program.error('error: profile "desktop" is managed exclusively by the Electron application')
  ```

**`--dump-config` / `--dump-default-config` / `--dump-config-schema` 的用法约束（逐字，`apps/cli/src/args.ts:115-120`）**：
> 🔴 `--dump-config` / `--dump-default-config` / `--dump-config-schema` **三者互斥**（上游把三个布尔量收进 `const dumps = [...]`，`dumps.length > 1` 即报错 —— `apps/cli/src/args.ts:115-120`）。**注意这是 `0.1.7-rc.1` 才从「两者互斥」改成「三者互斥」的**：照抄旧资料同时传两个 dump 开关会直接报错；
> 🆕 `--dump-config-schema`（`0.1.7-rc.1` 新增，源码 `apps/cli/src/dump-config-schema.ts`）：打印**组装后配置的 JSON Schema 2020-12 文档**（「without mounting」）—— 根 schema 描述 `--dump-config` 输出解析后的 entry list，`$defs.patchList` 单独描述 profile/home/CLI overlay（**校验片段时要保留 `$defs`**）。**它接受可重复的 `--patch` 与 `--from-default-profile`**（与 `--dump-default-config` 相反）；收集/投影失败时**保留部分输出并退出 1**，准备或组合失败则非零退出且不输出 schema；诊断走 stderr。权威文档 = `apps/cli/reference/README.zh.md:57-58`（CLI reference **不在** `docs/` 下 —— 用 `grep -rn … docs/` 会误判为「无文档」）；
> dump 是"无启动"的（不跑 app 命令行 provider）；
> `--dump-default-config` **不接受** `--patch`。

> 💡 **调试建议**：插件"装上了但没生效"时，先跑
> `dsh --profile <名字> --dump-config`
> 看你的行**到底有没有进入组装树**。这比翻日志快得多。

---

## 4. 一张图说清「写 → 装 → 生效」

```
① 你写的插件包
   my-plugin/
   ├── package.json     ← 必须声明 "dsh": {"bundle": {"patch": "./cordis.patch.yml"}}
   ├── cordis.patch.yml ← 真正的"装配说明书"
   └── src/index.ts     ← apply()

② 装
   dsh plugin --profile web add ./my-plugin        # 本地目录
   dsh plugin --profile web add my-plugin          # 已发布的 npm 包
   dsh plugin --profile web add github:me/my-plugin

③ dsh 自动做的事
   在 ~/.dsh/profiles/web/ 里跑 pnpm add
   → 读你的 package.json 看有没有 dsh.bundle.patch
   → 有：把你 append 进 dsh.profile.bundles（成为一层）
   → 没有：打那条 "declares no dsh.bundle" 警告，然后**什么都不做**

④ 生效
   重启 dsh（改 bundle 层的任何东西都要重启）
   dsh web
```

> ⚠️ **改 `cordis.patch.yml` / `package.json` / 客户端 bundle → 必须重启**。
> 只改被按需服务的 `lib/client.js`（且宿主已支持）→ 刷新页面可能够。

---

## 5. 用户自己的补丁层写在哪

- 用户补丁：`~/.dsh/profiles/<名字>/cordis.patch.yml`
- 额外叠加：`dsh --profile <名字> --patch ./extra.yml`（可重复）
- 官方原文（`packages/bundle/base/cordis.patch.yml` 注释，逐字）：

> ```
> # The dsh-base bundle patch: the shared core of each base-backed profile, applied as
> # ONE insert over the empty profile root. Later bundle patches and the user's
> # profile cordis.patch.yml address these rows by id, with the last write
> # winning per row.
> ```

**层叠顺序**：官方 bundle 层（按 `dsh.profile.bundles` 顺序）→ 用户 `cordis.patch.yml` → `--patch` 叠加层。**逐行 last-write-wins**。

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 2139-2351 -->

# 第 11 章 打包与分发：从「我能用」到「别人能用」

> **本课目标**：把你的插件打成别人能一键安装的包。
> **好消息**：不需要写 `package.json` 的魔改，也不需要过审。

## 11.1 先分清两个概念

来源：`docs/user/develop/basic/publish.zh.md:13-16`（逐字）

> **组合包（bundle）**：附带一个配置层的 npm 包，manifest 声明 `dsh.bundle`，回答"这个包贡献什么？"——一个插入或覆盖插件行的 patch 文件。
>
> **profile**：`$DSH_HOME/profiles/<name>` 下的目录，manifest 声明 `dsh.profile`，回答"这套配置由哪些组合包按什么顺序组成"。
>
> **没有东西同时是两者。**

**你要发布的是组合包。**

## 11.2 组合包的文件结构

来源：`docs/user/develop/basic/publish.zh.md:26-31`（逐字）

```
hello-plugin/
├── package.json       # declares dsh.bundle
├── cordis.patch.yml   # the layer applied when a profile lists this bundle
└── index.js           # plugin modules the patch rows reference
```

## 11.3 `package.json`（逐字）

来源：`docs/user/develop/basic/publish.zh.md:35-44`

```json
{
  "name": "dsh-hello-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

⚠️ **`dsh.bundle.patch` 是关键**。官方原文（`publish.zh.md:64`）：

> 没有 `dsh.bundle` 声明的包仍然可以安装，但只作为普通依赖：`dsh plugin` 会打印警告，且不激活任何层。

**翻译**：忘了写这个字段，你装上去的包**什么也不会发生**，只会看到一个警告。这是新手最常见的"我明明装了啊"。

## 11.4 patch 文件里怎么引用插件

`cordis.patch.yml`（`publish.zh.md:58-62`，逐字）：

```yaml
- insert:
    - id: hello
      name: dsh-hello-plugin
```

⚠️ **必须按「包名」引用，而不是相对源码路径**。官方原文（`publish.zh.md:56`）：

> patch 行按**包名**（不是相对源码路径）引用插件，Node 才能解析到已安装代码。

**这条正是第 3 章那个"绝对路径 vs 相对路径"讨论的答案**：开发期你用本地文件路径（overlay），交付期你用**包名**。

## 11.5 打包入口的写法

`index.js`（`publish.zh.md:48-54`）——就是导出 `name` 和 `apply`，和第 3 章一模一样：

```js
export const name = 'hello-plugin'

export function apply(ctx) {
  console.log('[hello-plugin] plugin loaded!')
}
```

## 11.6 安装与验证

### 安装（本地路径）

```sh
dsh plugin --profile demo add ./hello-plugin
```

来源：`publish.zh.md:80`

⚠️ **`--profile` 是必填的**。源码实证（`apps/cli/src/args.ts:192,199`）：`--profile` 是 `requiredOption`，省略直接报错。所以**不存在 `dsh plugin add xxx` 这种写法**。

### 安装后发生了什么

`dsh plugin` 本质是**在 profile 目录里把参数转发给 pnpm**，然后在 pnpm 成功后重算 bundles 列表。

**源码实证**（`packages/boot/plugin-manager/src/operations.ts:90-120` 的 `reconcile()`）：
- 凡是解析到的包 manifest 声明了 `"dsh": { "bundle": { "patch": ... } }`，该依赖就**加入层栈**（按依赖顺序追加），并 `loadOverlayPatches()` 载入它的补丁（`:112`）
- 没有 `dsh.bundle` 声明的依赖保留为普通依赖，并向 stderr 打印**一条警告**后 `continue`（`:104-105`）
- 被移除的依赖从层栈删除（`:96-99` 的 `filter`）

安装后 profile manifest 变成（`publish.zh.md:85-100`）：

```json
{
  "name": "dsh-profile-demo",
  "private": true,
  "dependencies": { "dsh-hello-plugin": "link:/path/to/hello-plugin" },
  "dsh": { "profile": { "bundles": ["@deepseek-ai/dsh-base", "dsh-hello-plugin"] } }
}
```

### 验证与卸载

```sh
dsh --profile demo --dump-config   # shows a "# == dsh-hello-plugin" layer
dsh --profile demo
dsh plugin --profile demo remove dsh-hello-plugin
```

来源：`publish.zh.md:106-110`

💡 **`--dump-config` 是你的验收工具**：能在输出里看到 `# == 你的包名` 这一层，就说明装对了。

⚠️ **重要提醒**（`apps/cli/reference/README.zh.md:95`）：pnpm 会改磁盘上的 profile manifest 与 bundles 列表，但**正在运行的 profile 保留本次启动时的组合**。增删/更新组合包后**必须重启 profile**。

## 11.7 三种分发方式对比

来源：`docs/user/develop/basic/publish.zh.md:161-186`（旧引 `:159-184`、更早 `:153-178`）

| 方式 | 命令 | 用户要不要授权 | 适用场景 |
|---|---|---|---|
| **发布到 npm** | `pnpm publish` | ❌ 不需要 | 面向公众发布（**推荐**） |
| **交付 tarball** | `pnpm pack` → 用户 `dsh plugin add ./xxx-0.1.0.tgz` | ❌ 不需要 | 内部分发 / 客户交付 |
| **GitHub 直装** | 用户 `dsh plugin add github:you/repo` | ✅ **需要** | 开源但不想发 npm |

### npm 发布

官方原文（`publish.zh.md:177`）：

> **发布到 npm**，在 `pnpm publish` 时构建好 `lib/`；`dsh plugin add your-package` 安装的就是预构建代码。

**要点**：
- 发布前**必须构建好产物**（`lib/`）——因为 dsh 不会跑你的 build。
- 包名规范：官方示例用的是**非 scope 名**（`dsh-hello-plugin`）。
- **不需要** `publishConfig`（`publish.zh.md` 未提这个要求）。
- **不需要**任何官方审核或白名单。

### tarball 分发

```sh
pnpm pack                              # 产出 dsh-hello-plugin-0.1.0.tgz
dsh plugin --profile <name> add ./dsh-hello-plugin-0.1.0.tgz   # 用户侧
```

### GitHub 直装（⚠️ 有几个坑，务必读完）

```sh
dsh plugin --profile demo add github:you/hello-plugin
```

官方警告（`publish.zh.md:153-173`）：

1. **git 安装拉取的是源码，不是构建产物**，**不会**运行 `build` 脚本。TypeScript 包到手没有 `lib/`，**加载会失败**。
2. **作者**必须提供 `prepare` 脚本（pnpm 在 git 安装后运行），且必须自包含。官方推荐范例是 [`turtle-ui`](https://github.com/deepseek-harness/turtle-ui)——它的 `prepare` 用一份专用 tsdown 配置直接转译 `src/`。
3. **用户**必须授权构建。pnpm ≥10 默认拒绝运行 git 依赖的 `prepare`，第一次 `add` 会失败。要把 pnpm 打印的确切包键复制进 profile 的 `pnpm-workspace.yaml`：

```yaml
allowBuilds:
  dsh-hello-plugin: true
```

然后重新执行 `add`。

4. **建议锁定 commit**：`github:you/hello-plugin#<sha>`

🔒 **安全警告（官方原文，请认真对待）**：

> 请把这项授权视为**允许该包的代码在安装时于你的机器上执行**，且不在 agent 运行的任何沙箱之内。只对源码可信的包授权，并锁定 commit。

## 11.8 让社区找到你

**没有官方插件市场**（⚠️ **2026-10-16 收窄**：`dsh-v0.2.1-alpha.4` 起官方交付了市场**机制** —— agent 工具 `plugin_market`、Discover 页、插槽 `plugins.tab`、4 个新包 —— 但**无官方市场、不随附默认索引源**，索引源属**用户数据**且该组合包不在 base 补丁里）。唯一的官方约定（`README.zh.md:50`、`CONTRIBUTING.zh.md:14-15`）：

> 为你的插件仓库添加 [`dsh-plugin`](https://github.com/topics/dsh-plugin) 话题，让其他人更容易找到你的插件。

⚠️ 同时提醒：**官方仓库不接受外部 PR**（`CONTRIBUTING.zh.md:9`）：

> DeepSeek Harness 仍处于早期阶段，并在积极开发中。很抱歉，我们目前无法接受外部 PR（Pull Request）。

但官方也给了一句很鼓励的话（同文件）：

> DeepSeek Harness 的设计支持深度定制。我们并不认为官方仓库中的包天然就比社区开发的包更重要。你可以将本仓库看作一种理念、一份官方示例以及一处灵感来源，而不是我们要求社区遵循的方向。

## 11.9 🤖 让 AI Agent 帮你做这一课

> 我要把插件「（插件名）」打包分发给**（同事 / 客户 / 公开发布）**。
> 请：
> 1. 先读 `docs/user/develop/basic/publish.zh.md`，告诉我该走 npm / tarball / github 哪条路，以及理由；
> 2. 生成组合包所需的**全部文件**（`package.json`、`cordis.patch.yml`、入口文件），并逐字段解释；
> 3. 给出**完整的用户侧安装命令**（注意 `--profile` 必填）；
> 4. 给出**验证命令**（`--dump-config`）以及"应该看到什么";
> 5. 如果走 git 路线，把 `prepare` 脚本和 `allowBuilds` 授权步骤都写清楚，并明确告诉我安全风险。
> 约束：`cordis.patch.yml` 里必须**按包名**引用插件；`dsh.bundle.patch` 字段不能漏。

## 11.10 ✅ 第 11 章验收清单

- [ ] `package.json` 里有 `dsh.bundle.patch`
- [ ] `cordis.patch.yml` 里按**包名**引用插件
- [ ] 我给出的安装命令带了 `--profile`
- [ ] `dsh --profile xxx --dump-config` 能看到 `# == 我的包名` 那一层
- [ ] 我（或别人）在一台**没装我源码**的机器上装成功了
- [ ] 如果走 git 路线，我知道了 `prepare` + `allowBuilds` + 锁 commit 三件事

---


---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 2352-2454 -->

# 第 12 章 调试与排错手册

> **本章是工具书，不用背。出问题时回来查。**

## 12.1 第一招：`--dump-config`（不启动就检查组合树）

```sh
dsh --profile web --dump-default-config                                  # 只看组合包各层
dsh --profile web --patch ./extra.yml --dump-config                      # 加上用户层与 overlay
```

**输出会带注释标明每行来自哪里**、哪些 overlay 改过它（格式是 `# == <标签>` 分组）。

**约束**（`apps/cli/reference/README.zh.md:49-58`）：
- 🔴 `--dump-config` / `--dump-default-config` / `--dump-config-schema` **三种 dump flag 互斥**（`0.1.7-rc.1` 起由「两种互斥」扩为三种 —— 见 `apps/cli/src/args.ts:115-120`）。**照抄旧资料同时传两个 dump 开关会直接报错**
- `--dump-default-config` 不接受 `--patch`（`--dump-config` 与 `--dump-config-schema` 都接受）
- 三种 dump 都**不接受应用参数**（如 `--port`），也拒绝保留的 `desktop` profile
- 🆕 `--dump-config-schema` 输出 JSON Schema；**收集或投影失败时保留部分输出并退出 1**（`partial` 投影同样适用）

## 12.2 第二招：看 PENDING 审计（插件没反应时第一件事）

DSH 启动时会自动审计。源码实证（`packages/boot/app-boot/src/index.ts:1112` 单条格式串、`:1132` 分组汇总表）：对仍 PENDING 的条目打印

```
<name>: pending (waiting for service: <缺失服务>)
```

然后抛 `dsh: N entries did not activate` 并**非零退出**。

**这行日志直接告诉你缺哪个服务。** 对照你的 `inject` 数组，看是不是写错了服务名，或者忘了在组合里加那个服务的提供方。

## 12.3 第三招：日志

| 手段 | 默认可见？ |
|---|---|
| `console.log(...)` | ✅ 可见 |
| `ctx.logger('name').info(...)` | ⚠️ **默认不可见**（交付的 profile 没挂 console 导出器） |

⚠️ **不存在** `--log-level` / `DSH_LOG_LEVEL` 这类开关（`apps/cli/src/args.ts` 全量核查）。

想用正式日志，要自己把 `@deepseek-ai/cordis-plugin-logger-console` 插进组合。它的配置字段（源码 `vendor/logger-console/src/shared.ts:16-42`）：
`colors`、`maxLength`、`levels`、`showDiff`、`showTime`、`label`。

## 12.4 第四招：开启 HMR（改代码不用重启）

在你的 patch 里覆盖 base 的那一行（`packages/bundle/base/cordis.patch.yml:28-30`）：

```yaml
- id: hmr
  disabled: false
  config:
    root: ['.']
```

**注意**：
- ⚠️ patch **替换整行 config**，所以要把想保留的键（`root`）重述一遍
- ⚠️ HMR 依赖 `@deepseek-ai/cordis-plugin-timer`，缺了它会永久 PENDING（且不报错）
- ⚠️ **`--patch` 指定的 overlay 文件本身不会被热重载**，只有 profile 与 home 的 `cordis.patch.yml` 会被 watch
- 客户端 HMR 还需要单独跑 `pnpm run dev:web`

## 12.5 第五招：自己写个 PENDING 诊断插件

当审计信息不够用时（`docs/cordis-tutorial/06-composition-and-hmr.zh.md`，逐字）：

```ts
import { FiberState, type Context } from '@deepseek-ai/cordis'

export const name = 'diagnose'

export function apply(ctx: Context) {
  setTimeout(() => {
    for (const runtime of ctx.registry.values()) {
      for (const fiber of runtime.fibers) {
        if (fiber.state === FiberState.PENDING) {
          console.log(`${fiber.name} is PENDING — a required service is missing`)
        }
      }
    }
  }, 500)
}
```

## 12.6 五步排错法（照着走）

| 步骤 | 动作 | 看什么 |
|---|---|---|
| 1 | 看启动日志关键字 `pending (waiting for service:` | 缺哪个服务 |
| 2 | `dsh --profile <name> --dump-config` | 我的插件行在不在？在哪个层？ |
| 3 | 检查 `inject` 拼写与服务的提供方是否在组合里 | 服务名大小写、复数 |
| 4 | 检查导出形态 | 命名导出插件里有没有混进 `export default`？ |
| 5 | 加 `console.log` 到 `apply` 第一行 | apply 到底跑了没？PENDING 的话不会跑 |

**如果第 5 步的日志没打印**：插件处于 PENDING 或 FAILED。回到第 1 步。

## 12.7 一个残酷但重要的提醒：**"没输出"可能是正常的**

`docs/cordis-tutorial/03-services.zh.md` 原文（逐字）：

> 处于 PENDING 的 fiber 也不会让 Node 的事件循环保持活跃，因此如果组合中没有其他运行项，进程会静默地以状态码 0 退出。

**所以**：进程静默退出、状态码 0，**不代表没问题**。要学会看审计输出。

---


---

