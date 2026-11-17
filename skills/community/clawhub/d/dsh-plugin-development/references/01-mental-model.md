> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：DSH 与 Cordis 的心智模型、插件三种形态、profile/组合包的加载机制、方向决策树（做什么该用哪个模板），以及第一个最小插件的完整走通过程。写插件前先读这个，选错形态会导致后面全部返工。
> **合成来源**：DSH插件开发指导手册.md（第 0/1/3 章） + DSH插件开发实战补充-模板与踩坑.md（第一篇）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 497 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **本文件全是整理稿**（无上游素材混杂），但它仍是基线快照——写代码前先过版本闸门。
> - 常用检索：`grep -n '^## '`（小节清单）、`grep -n '^### '`（子节）

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 36-253 -->

# 第 0 章 开始之前：你必须知道的 6 件事

## 0.1 DSH 是什么

**DSH = DeepSeek Harness**，是 DeepSeek AI 开源的 **agent harness（智能体框架）**。

- 仓库：`deepseek-ai/deepseek-harness`（MIT 许可，22 万+ stars）
- 架构理念：**Everything is a Plugin（一切皆插件）**
- 底层框架：[Cordis](https://github.com/cordiverse/cordis)——一个插件框架，插件通过共享上下文贡献「服务、类型化事件、可逆的副作用」
- 技术栈：TypeScript + pnpm monorepo，前端 React 18

来源：`README.zh.md`、`docs/architecture.zh.md`

**一句话理解**：DSH 是一个「组装出来的 AI 助手」。它没有特权内核，所有能力（模型适配器、工具、终端、界面）都是一个个插件挂上去的。所以——**你写的插件，和官方写的插件，地位是平等的**。

## 0.2 插件是什么（超简版）

一个插件，就是一个 **TypeScript 文件**，它导出一个 `apply` 函数：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'

export function apply(ctx: Context) {
  // 在这里通过 ctx 注册你的能力
}
```

**这就是全部。** 没有构建配置文件要你手写，没有继承庞大的基类，没有 XML 配置。

来源：`docs/user/develop/basic/index.zh.md:19-27`

## 0.3 本手册的难度梯度

用户需求里说的「从命令行到 UI」，在 DSH 里对应这条真实梯度：

```
① 最小插件（console.log）
   ↓ 加能力
② 工具插件     ctx.tools.register(defineTool(...))   ← 给「模型」用
   ↓ 加参数
③ 可配置插件   export const Config = Schema.object(...)
   ↓ 给人用
④ 命令插件     ctx.commands.register({...})          ← 给「人」用（/命令）
   ↓ 改别人行为
⑤ 事件拦截     ctx.on('tools/pre-execute', ...)      ← 权限、审计、改写
   ↓ 要终端能力
⑥ 终端插件     ctx.terminals（PTY 家族）+ 工具卡片
   ↓ 要界面
⑦ UI 插件      src/client/ + ctx.slots.register(...)  ← 网页里长按钮
   ↓ 要可视化配置
⑧ 配置表单     Config schema 派生表单（要自定义页才用 plugins.item）
```

**重要诚实说明**：很多第三方文章会告诉你 DSH 有「TUI（终端界面）插件」。本手册核查了仓库：**TUI 前端确实曾存在**（包名 `@deepseek-ai/dsh-tui`，路径 `packages/ui/tui/`，基于 `pi-tui`），但已 **2026-08-04 归档**，不再作为应用入口交付，当前仓库里 `packages/ui/` 目录**不存在**。
来源：`.agents/notes/archived/feature/2026-07-17-dedicated-full-screen-tui-front-door.zh.md`

所以本手册第 8 章讲的「终端」，指的是**持久 PTY 会话能力**（让 AI 能在终端里跑交互式命令并保持状态），而不是「自己写一个终端界面」。这条边界必须说清楚，否则你会照着不存在的文档白忙。

## 0.4 你需要准备什么

| 需要 | 版本要求 | 你的机器实测（2026-09-11） | 说明 |
|---|---|---|---|
| 操作系统 | Windows / macOS / Linux | Windows ✅ | 本手册命令用 bash 风格，PowerShell 也能跑（注意引号） |
| Node.js | `^22.19.0 \|\| >=24.0.0` | **v22.22.2 ✅** | 仓库 `package.json` 的 `engines` 字段 |
| pnpm | 仓库声明 `pnpm@11.7.0` | **11.21.0 ✅** | 新版本兼容；若报错再切 11.7.0 |
| Git | 任意较新版本 | 2.55.0 ✅ | 用来克隆仓库 |
| 一个 AI Agent | 任意 | WorkBuddy ✅ | 帮你写代码、查文档、排错 |

来源：仓库根 `package.json`、本机实测

⚠️ **corepack 未安装**（本机实测）。本手册的所有命令**不依赖 corepack**，直接使用已安装的 `pnpm` 即可。

## 0.5 最大的风险：API 每周都在变

这是本手册最重要的一节。**在你投入时间之前，必须先知道这件事。**

用 git 历史实证：

| 事实 | 数据 | 来源 |
|---|---|---|
| 仓库首个提交 | 2026-06-10 | `git log` 首次提交 `b67e81ac97` |
| 已发布 tag 数 | 16 个，全部在 2026-08-17 之后 | `git tag --sort=creatordate` |
| **tag 间隔中位数** | **约 1.1 天**（最长 6.2 天） | 逐个 tag 日期相减 |
| 版本号跳跃 | **没有 `0.1.4`**，0.1.3-alpha.2 → 0.1.5-alpha.1 跨了 563 个提交 | `git tag \| grep 0.1.4` 无输出 |
| CHANGELOG | **不存在**（既无 `CHANGELOG.md` 也无 release notes） | `git ls-files \| grep -i changelog` 无输出 |
| 官方自述 | 根 `AGENTS.md:7`：`Public APIs are pre-stable; update every consumer.` | 原文 |
| README 自述 | 「DeepSeek Harness 处于 _开发者预览_ 阶段，正在快速迭代。**未来将出现破坏兼容性的变更。**」 | `README.zh.md` |

**这意味着什么**（给你的三条行动建议）：

1. **锁版本**：开发时记录下你依据的 commit（本手册是 `86a402200d`）。升级前先读 diff。
2. **只信文档 + 源码**：网上第三方博客（尤其 2026-07 之前的）大概率已过时。**任何 API，都要在仓库里找到出处再用。**
3. **接受返工**：你以为的"稳定 API"可能下周就改名了。实际案例：`code-mode` 被改名为 `ptc`；client 清单字段 `dshClient` 在 2026-08-10 被改成嵌套的 `dsh.client`；插件的 client 机制 2026-07-19 才诞生。

## 0.6 官方「不做」的几件事（诚实清单）

写手册的人容易犯的错，是把「别人生态里有的东西」当成「官方的」。以下是核查结果：

| 你可能以为有 | 实际情况 |
|---|---|
| 官方插件市场 / `dsh plugin search` | ⚠️ **「不存在」自 `dsh-v0.2.1-alpha.4` 起须收窄**：官方**交付了市场·机制**（服务 `pluginMarket` / agent 工具 `plugin_market` / Discover 页 / 插槽 `plugins.tab` / 4 个新包），但**没有官方市场、也不随附默认索引源**（索引源属**用户数据**）→ **`dsh plugin search` 仍不存在**，`dsh plugin` 仍只是 pnpm 转发器，**生态发现主渠道仍是 GitHub topic `dsh-plugin`** |
| 官方仓库接受你提交插件 | ❌ `CONTRIBUTING.zh.md`：「很抱歉，我们目前无法接受外部 PR」 |
| 插件需要审核 / 白名单 | ❌ 没有。发布到 npm 即完成分发 |
| CHANGELOG / release notes | ❌ 不存在。破坏性变更靠提交信息里的 `!` 标记 |
| 插件必须用 `publishConfig` | ❌ `publish.zh.md` 未要求（`publishConfig.access: public` 是 dsh 自己用的） |
| 项目级 `cordis.yml`（放在你项目目录里） | ❌ 不存在这个常量。配置在 `$DSH_HOME/profiles/<name>/`，或用 `--patch` 指定 |
| `dsh plugin add xxx`（不带 profile） | ❌ `--profile` 是必填参数，省略会直接报错 |
| 官方插件测试脚手架 | ❌ 未找到面向外部作者模板 |

来源：`CONTRIBUTING.zh.md`、`apps/cli/src/args.ts`、`docs/glossary.zh.md` 及全仓检索

---

# 第 1 章 心智模型：DSH 的架构（看懂这章，后面全都顺）

## 1.1 「一切皆插件」到底意味着什么

官方原文（`docs/architecture.zh.md`，逐字）：

> [Cordis](cordis-primer.zh.md) 是 dsh 底层的框架：插件向共享上下文贡献服务、类型化事件和可逆的副作用。产品的每一部分都是插件，包括模型适配器、工具注册表、会话日志，以及 agent loop（智能体循环）本身，因此每个都可以从配置替换。
>
> 不存在需要打补丁的特权内核：扩展 dsh 的方式是把插件挂载到其他插件旁边，而各项注册都是副作用，会在其插件卸载时撤销。

**翻译成人话**：
- 你**不需要**「找到源码里那个函数改一下」——那是打补丁，DSH 明确说没有这种地方。
- 你**只需要**把你的插件挂在旁边，告诉框架「我提供什么」。
- 你注册的一切，在你插件卸载时**自动撤销**。关机、热更新、配置改动都不会留下垃圾。

## 1.2 Cordis 的三件套

DSH 的一切交互，都通过这三个东西：

| 机制 | 干什么 | 代码长什么样 |
|---|---|---|
| **服务（Service）** | 提供能力给别人用 | `ctx.tools.register(...)`、`ctx.shell` |
| **事件（Events）** | 广播 / 拦截行为 | `ctx.on('tools/result', ...)` |
| **副作用回收（effect）** | 保证卸载时干净 | `ctx.effect(() => { ... return () => 清理 })` |

**关键区别（新手最容易混）**：
- **服务**：你「加」东西进去（注册工具、注册命令）。
- **事件**：你「听」或「截」别人的流程（拦截工具调用、审计结果）。
- 两者都通过 `ctx` 访问，都自动回收。

## 1.3 capability seam 三角色：写插件前必须做的选型

这是官方架构文档里最关键的一个概念，直接决定你的插件该写什么。

官方原文（`docs/architecture.zh.md:140`，逐字）：

> 一个 **seam** 是一项可替换能力，包含三种角色：声明接口的 **Service Definition**、实现它的 **Service Provider**，以及使用它的 **Consumer**（通常是面向模型的工具）。一个包可以合并承担多个角色，但单一角色本身不是 seam；添加一项能力意味着把三者一并设计。

**用途**：拿到需求后，先判断你要写哪一类：

| 你想做的事 | 你的角色 | 你要写的代码 |
|---|---|---|
| 替换/实现某项能力（如换一个文件系统后端） | **Service Provider** | 实现一个已有服务的接口 |
| 声明一项新能力（如"翻译服务"） | **Service Definition** | 定义接口 + 至少一个 Provider + 至少一个 Consumer |
| 让 AI 模型能做某件事 | **Consumer**（最常见） | `ctx.tools.register(defineTool(...))` |
| 拦截/审计/改行为 | 事件监听者 | `ctx.on('...')` |
| 给人用的交互入口 | 命令 | `ctx.commands.register(...)` |
| 加界面 | 客户端插件 | `ctx.slots.register(...)` |

**硬规则**（`packages/AGENTS.md:10`）：为一个 Consumer 定制服务接口是**反模式**。别让「我的工具需要这样」去扭曲公共服务契约。

## 1.4 profile 与组合包：用户是怎么装上你的插件的

这是 DSH 分发机制的骨架，务必看懂。官方定义（`docs/architecture.zh.md`，逐字）：

> **profile** 是存放在 Harness home 中的具名组装。它列出自己叠放的组合包，存放自己安装的树外插件，并保存用户自己的 `cordis.patch.yml`。`web`、`headless`、`sdk`、`sdk-minimal` 和 `acp` 作为模板随发行版交付。
>
> **组合包**是 Cordis 配置项及其挂载代码的分发格式，因此它插入的内容始终可被其上各层 patch。

**两者都在各自 `package.json` 里用 `dsh` 字段声明自己**：

```jsonc
// 组合包（你要发布的东西）
"dsh": { "bundle": { "patch": "./cordis.patch.yml" } }

// profile（用户的机器上）
"dsh": { "profile": { "bundles": ["@deepseek-ai/dsh-base", "你的包名"] } }
```

**关键结论**：**没有东西同时是两者**。你发布的是**组合包**；用户机器上的 profile 会**列出**你的组合包。

配置的**层叠顺序**（后应用者胜；patch 替换整行 `config`，不做深度合并）：

1. profile 的 `dsh.profile.bundles` 里各组合包的 patch（按列表顺序）
2. profile 自己的 `cordis.patch.yml`
3. home 级 `$DSH_HOME/cordis.patch.yml`
4. 每个 `--patch <path>` overlay（按命令行顺序）

来源：`docs/user/develop/basic/publish.zh.md`、`apps/cli/src/profile-boot.ts:206-244`

## 1.5 一张图：你的代码在哪里生效

```
用户的机器
└── $DSH_HOME  (Windows: C:\Users\<你>\.dsh)
    ├── cordis.patch.yml            ← home 级用户层（所有 profile 共享）
    └── profiles/
        └── web/                     ← 一个 profile（模板来自 dsh-web-app 组合包）
            ├── package.json         ← 声明 bundles 列表 + 装了哪些插件
            ├── cordis.patch.yml     ← 这个 profile 的用户层（可热重载）
            ├── cordis.yml           ← 空根配置，不要编辑（每次启动被重写）
            └── node_modules/        ← 你 dsh plugin add 装进来的包就落在这
```

**你开发时的两种接法**：

| 阶段 | 接法 | 命令 |
|---|---|---|
| 开发调试 | `--patch` overlay，指向你的本地 `.ts` 源码 | `pnpm dsh web --patch ./scratch-plugin/cordis.yml` |
| 交付给用户 | 打成组合包，用户 `dsh plugin add` | `dsh plugin --profile web add ./你的包` |

---


---

<!-- ↓ 源：DSH插件开发实战补充-模板与踩坑.md 区间 35-63 -->

# 第一篇 · 方向决策树（先看这个）

## 1.1 你想做什么 → 用哪个模板

| 你的目标 | 用哪个模板 | 难度 | 需要写代码吗 | 涉及的能力 |
|---|---|---|---|---|
| 把已有的 MCP 工具挂进 DSH | **T1** 零代码组合包 | ★ | **不用** | `cordis.patch.yml` |
| 改一个现成插件的行为 | **T2** 组合包 + 覆盖层 | ★ | 不用 | `cordis.patch.yml` |
| 让模型能调用一个新能力（说人话：加个工具） | **T3/T4** 工具插件 | ★★ | 要 | `tools` 服务 |
| 让人能敲一个 `/命令` | **T5** 命令插件 | ★★ | 要 | `commands` 服务 |
| 让用户能配置我的插件 | **T6** 可配置插件 | ★★ | 要 | `Config` schema |
| 给别的插件提供能力（当"基础设施"） | **T7** 服务插件 | ★★★ | 要 | `ctx.provide` / `extends Service` |
| 在网页界面上加东西 | **T8/T9** UI 插件 / 设置卡片 | ★★★ | 要（React） | `slots` 服务 |
| 改 Agent 的行为（拦消息、改请求、加提示词） | **T10** 流程拦截 | ★★★★ | 要 | `agent/pre-step`、`agent/request` |
| 集成一个外部系统（HTTP/CLI/协议） | **T11** 外部集成 | ★★★ | 看情况 | 工具 + 事件钩子 |
| 建一个规范的完整工程 | **T12** 工程化骨架 | ★★★ | 要 | 全套约定 |

## 1.2 五个方向的一句话避坑要点

| 方向 | 最致命的一件事 |
|---|---|
| **工具 / 外部调用** | `parameters` 有**两套写法**（`defineTool` DSL 用属性级 `required: true`；裸 `register` 用对象级 `required: ['a']`），**混用必报错** |
| **UI / 设置卡片** | `dsh.client` 声明与 `exports["./client"]` **必须成对存在**，缺一个客户端半侧根本不组装 |
| **服务 / 状态** | 副作用不包 `ctx.effect` → 热更新后监听器叠加、注册表报 `duplicate` |
| **Agent 流程** | waterfall 监听器必须 `await next()`，否则**静默吃掉**后续所有处理 |
| **组合包 / 安装** | `package.json` 少了 `dsh.bundle.patch`，或 `files` 漏了 `cordis.patch.yml` → 装上有警告、功能不生效 |

---


---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 361-579 -->

# 第 3 章 第一课｜最小插件：Hello

> **本课目标**：写一个只会打印一行字的插件，并让它真的在 DSH 里跑起来。
> **本课的意义**：先把「写文件 → 挂载 → 启动 → 看到输出」这条最小闭环跑通。**这一步不成功，后面全都是空中楼阁。**

## 3.1 建目录

在**仓库根目录**下创建开发目录（官方教程用的就是这个路径，`docs/user/develop/basic/index.zh.md:9-12`）：

```sh
mkdir -p scratch-plugin/src
```

> ℹ️ 官方教程此处**只有上面那一行**；`cd <你的 DSH 检出目录>` 是本节补的上下文。

## 3.2 写插件文件

创建 `scratch-plugin/src/my-plugin.ts`，内容逐字如下（`docs/user/develop/basic/index.zh.md:36-44`）：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'hello-plugin'

export function apply(ctx: Context) {
  // Required dependencies are ready before apply runs.
  console.log('[hello-plugin] plugin loaded!')
}
```

**逐行解释**：

| 代码 | 含义 |
|---|---|
| `import type { Context } from '@deepseek-ai/cordis'` | 只导入**类型**（`import type`），运行时不产生任何依赖。`Context` 就是那个 `ctx` 的类型。 |
| `export const name = 'hello-plugin'` | 插件显示名。**可选**，用于诊断信息和日志。 |
| `export function apply(ctx: Context) { ... }` | **这就是 apply 函数本体**。Cordis 加载模块时会调用它，把上下文 `ctx` 传进来。 |

⚠️ **血泪教训（官方事后复盘真实事故）**：`docs/postmortem/0001-acp-default-export-drops-inject.zh.md` 记录，有开发者在一个命名导出插件里**多加了一行 `export default apply`**，结果 Cordis 的 `unwrapExports` 优先取 `.default`，把 `inject` / `name` / `Config` 全部丢弃 → 插件在**没有依赖注入**的 fiber 里运行 → 崩溃。**178 个单元测试全绿、100% 行覆盖率都没抓到。**

**规则（`packages/AGENTS.md:5`，逐字）**：

> **Plugin exports:** service packages default-export their service class; function plugins named-export `name` / `inject` / `Config` / `apply` and have no default export. Mixing the forms makes the Loader discard the function plugin's namespace.

翻译：**函数插件用命名导出，绝对不要加 `export default`。** 只有「服务类」才用 default export。

## 3.3 把它挂进去（写 overlay）

创建 `scratch-plugin/cordis.yml`：

```yaml
- insert:
    - id: hello
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
```

**三个字段都要解释清楚**：

| 字段 | 作用 |
|---|---|
| `insert:` | patch 操作符：往配置树里**插入**若干行 |
| `id: hello` | 这一行的**稳定标识**。loader 靠它区分「改了这一行」和「删了再加」。**强烈建议给每一行都写 id**（不写的话每次读取都会生成新 id，任何编辑都会导致它被当成"先删后加"重挂载） |
| `name:` | 模块指定符，可以是**相对路径、绝对路径、或 npm 包名** |

### ⚠️ 关于「绝对路径 vs 相对路径」——官方文档自身有冲突

这是一个必须向你交代清楚的真实矛盾：

| 来源 | 说法 |
|---|---|
| `docs/user/develop/basic/index.zh.md:56` | 「插件路径必须是绝对路径。patch 文件只贡献配置，不会改变 loader 解析模块路径时使用的 profile 目录。」 |
| `docs/user/develop/basic/config.zh.md:36-43` | 示例用的是**相对路径**：`name: './src/my-plugin.ts'` |
| **源码 `packages/boot/app-boot/src/index.ts:548-550`** | 实际行为：若 `name` 是绝对路径，或以 `./` `../` 开头，会被重写为**相对该 patch 文件所在目录**的 file URL |
| **测试 `packages/boot/app-boot/tests/user-patches.spec.ts:128`** | 有单元测试固定了这个「相对路径锚定到 patch 文件旁」的行为 |

**本手册的建议（以源码为准）**：

- ✅ **推荐写绝对路径**：最不容易出错，且与入门教程一致。
- ✅ **也可以用相对路径**：`./src/my-plugin.ts` 表示「相对于**这个 patch 文件**所在的目录」——注意**不是**相对于你执行命令的目录。
- 记住这条推论：`config.zh.md` 里 `name: './src/my-plugin.ts'` 能生效，前提是 `src/` 与那个 patch 文件同级。

## 3.4 启动并验证

```sh
pnpm dsh web --patch ./scratch-plugin/cordis.yml
```

然后打开 `http://127.0.0.1:3080`。启动过程中，**终端会打印**：

```
[hello-plugin] plugin loaded!
```

来源：`docs/user/develop/basic/index.zh.md:61-64`

## 3.5 你刚才做了什么（原理，很重要）

你的插件经历了一个**状态机**。官方状态机（`docs/user/develop/framework/index.zh.md:11-24`）：

```
PENDING → LOADING → ACTIVE
                 ↘ FAILED
ACTIVE → UNLOADING → DISPOSED
```

| 状态 | 含义 |
|---|---|
| PENDING | 已声明，但所需依赖未就绪 |
| LOADING | 依赖就绪，正在执行 `apply` |
| ACTIVE | 插件运行中 |
| FAILED | `apply` 抛出异常 |
| UNLOADING | 正在卸载并释放资源 |
| DISPOSED | 已完全卸载 |

**关键提醒**：插件加载**不是按 `cordis.yml` 里的书写顺序**决定的，而是**由依赖关系（`inject`）决定**。官方原文（`docs/cordis-tutorial/03-services.zh.md`）：

> `cordis.yml` 中的加载顺序无关紧要：决定插件何时启动的是依赖关系，而不是文件顺序。

## 3.6 自动清理（这是 DSH 最优雅的地方）

官方原文（`docs/user/develop/basic/index.zh.md:66-70`）：

> 通过 `ctx` 注册的任何东西——事件监听、工具、定时器——在插件卸载时都会被自动清理。你不需要手动 removeListener 或 clearInterval。

**唯一需要你手动处理的**：那些**不由 Cordis 管理**的资源（网络连接、文件句柄、子进程）。用 `ctx.effect()` 包起来：

```ts
import type { Context } from '@deepseek-ai/cordis'

export function apply(ctx: Context) {
  ctx.effect(() => {
    const timer = setInterval(() => {
      console.log('heartbeat')
    }, 5000)

    // The returned function runs when the plugin unloads.
    return () => clearInterval(timer)
  })
}
```

**记忆口诀**：
> `ctx.effect(() => { 拿资源; return () => 还资源 })`

⚠️ **一个反直觉的坑**（`docs/cordis-tutorial/02-lifecycle-and-effects.zh.md`）：

> disposer 会按注册顺序的逆序**启动**，但多个**异步** disposer 会**并发运行**。如果拆除步骤必须按顺序执行，请把它们放在同一个 disposer 中，并在其中依次等待每步完成。

即：逆序只管"开始顺序"，不管"谁先结束"。有顺序依赖的清理，**写在一个 effect 里串行 await**。

## 3.7 插件的三种形态

官方支持三种写法（`docs/user/develop/basic/index.zh.md:105-138`）：

### 形态 1：函数（默认首选）

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'
export const inject = ['tools']

export function apply(ctx: Context) {
  // ...
}
```

### 形态 2：对象

```ts
export default {
  name: 'my-plugin',
  inject: ['tools'],
  apply(ctx: Context) {
    // ...
  },
}
```

### 形态 3：类（要对外提供服务时才用）

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

export default class MyService extends Service {
  static inject = ['tools']

  constructor(ctx: Context) {
    super(ctx, 'myService')
    // Perform synchronous initialization in the constructor.
  }
}
```

**选型建议（官方结论）**：
> 大多数情况下，函数形式足够了。当插件需要向其他插件提供服务时，可使用类形式。

⚠️ **注意形态混用的陷阱**：形态 2 / 3 用了 `export default`。如果你采用形态 1（命名导出），**不要**再叠一个 `export default`（见 3.2 的血泪教训）。

## 3.8 🤖 让 AI Agent 帮你做这一课

把下面这段直接丢给你的 Agent：

> 我在 `deepseek-harness` 仓库里开发 DSH 插件，当前是第 1 级（最小插件）。
> 请严格按 `docs/user/develop/basic/index.zh.md` 的写法，帮我：
> 1. 创建 `scratch-plugin/src/my-plugin.ts`，导出 `name` 和 `apply`，`apply` 里打印一行日志；
> 2. 创建 `scratch-plugin/cordis.yml`，用 `insert` + `id` + `name` 挂载它；
> 3. 告诉我启动命令。
> 约束：**只使用你在该仓库中能找到出处的 API**，每处写法都标注来源文件路径与行号。不要凭记忆写 `onReady`/`onDispose` 之类的钩子——如果文档里没有，就明确说没有。

## 3.9 ✅ 第 3 章验收清单

- [ ] `scratch-plugin/src/my-plugin.ts` 存在，只有命名导出，**没有 `export default`**
- [ ] `scratch-plugin/cordis.yml` 里那一行有 `id`
- [ ] 启动后终端出现 `[hello-plugin] plugin loaded!`
- [ ] 浏览器能打开 `http://127.0.0.1:3080`
- [ ] 你能说出：插件加载顺序由 **`inject` 依赖**决定，而不是文件顺序

---


---

