> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：UI 插件与设置卡片的完整实现：两个半侧结构、三个登记点、slot 插槽机制、React/TSX 技术栈约束、样式打包、开发期调试、三层配置解析模型。
> **合成来源**：DSH插件开发指导手册.md（第 9/10 章）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

> **本文件导航 —— 共 553 行，不要整读。** 先 `grep` 定位小节，再只读需要的那一节。
> - **本文件全是整理稿**（无上游素材混杂），但它仍是基线快照——写代码前先过版本闸门。
> - 常用检索：`grep -n '^## '`、`grep -n '插槽'`（插槽名出现处）

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 1654-2138 -->

# 第 9 章 第七课｜UI 插件：在网页界面里长出你的东西

> **本课目标**：写一个在 DSH 网页界面里显示东西的插件。
> **难度**：这是全书最复杂的一章。核心难点是理解「一个包有两个半侧」。

## 9.1 核心概念：一个插件 = 两个半侧

官方原文（`docs/cookbook/adding-a-settings-card.zh.md`，**0.1.7-rc.1 之前**的版本 `:7`；该文档本区间被**整篇改写**，此句已不在其中 —— 事实与写法仍成立，稳定出处见 `packages/client/AGENTS.md`「One UI feature = one plugin package（`src/client/` browser half）」）：

> 两个半侧住在同一个包里——Host 半侧在 `src/`，浏览器半侧在 `src/client/`，以 `./client` 导出并用 `dsh.client` 声明。

```
你的插件包/
├── package.json          ← 声明 dsh.client + exports["./client"]
├── tsconfig.json         ← extends tsconfig.base.client.json
├── tsdown.config.ts      ← 用共享 preset
└── src/
    ├── index.ts          ← 【Host 半侧】运行在 Node 里（常常是空的）
    └── client/
        └── index.ts      ← 【浏览器半侧】真正跑在网页里的代码
        └── Something.tsx ← 你的 React 组件
```

**为什么要两个半侧？** 因为 DSH 是「后端 host + 前端 web」的架构。你的插件既要在 Node 里被加载（哪怕是空壳），又要在浏览器里运行 UI。

⚠️ **Host 半侧不能省**。官方（`packages/client/AGENTS.md:147-148`）：缺 node half 会让 Loader 无法 import 你的包。

**最小的 Host 半侧可以就这么点**（`packages/client/ui-brand-official/src/index.ts` 全文，逐字）：

```ts
/**
 * Official browser-brand plugin, node half. The empty apply gives Loader a
 * host-side row while the browser half ships through `exports["./client"]`.
 */

/** Host plugin body — this package contributes browser presentation only. */
export function apply(): void {}
```

💡 注意 `apply()` **连 ctx 参数都没有**。这是完全合法的——它只负责"占个位"，让 Loader 认为这个包被加载了。

## 9.2 `package.json` 模板（可直接抄）

来源：`packages/client/ui-brand-official/package.json`（逐字关键字段）

```json
{
  "name": "@deepseek-ai/dsh-client-ui-brand-official",
  "type": "module",
  "main": "lib/index.js",
  "types": "lib/types/index.d.ts",
  "exports": {
    ".": { "types": "./lib/types/index.d.ts", "default": "./lib/index.js" },
    "./client": { "types": "./lib/types/client/index.d.ts", "default": "./lib/client.js" },
    "./src/*": "./src/*",
    "./package.json": "./package.json"
  },
  "dsh": {
    "client": {
      "inject": [
        "@deepseek-ai/dsh-client-ui-renderer",
        "@deepseek-ai/dsh-client-ui-sidebar"
      ],
      "platform": "web"
    }
  },
  "files": [
    "lib/index.js",
    "lib/client.js",
    "lib/types/**/*.d.ts"
  ]
}
```

**三个必知字段**：

| 字段 | 含义 |
|---|---|
| `exports["./client"]` | 浏览器半侧的入口。**声明了 `dsh.client` 就必须有这个导出**（没有会抛错） |
| `dsh.client.platform` | **总是必填**，值为 `"web"` |
| `dsh.client.inject` | **信息性**的包名依赖边——**只用于 preflight 显示与 HMR diff，不决定激活顺序**。激活顺序由 Cordis fiber 等**服务**决定 |

来源：`packages/client/AGENTS.md:149`

`tsdown.config.ts`（`ui-brand-official/tsdown.config.ts`，逐字）：

```ts
import { clientBundle } from '../tsdown.client.ts'

export default clientBundle('@deepseek-ai/dsh-client-ui-brand-official', ['lib/types/index.js'])
```

> ⚠️ **这只在 DSH 仓库内可用**——`clientBundle()` 未对外发布。仓库外的第三方插件要自己复刻产物格式，见 §9.6 的校正块与 `14-inbound-http-and-timers.md` §17.3。

`tsconfig.json`（逐字）：

```json
{
  "extends": "../../../tsconfig.base.client.json",
  "compilerOptions": { "rootDir": "src", "outDir": "lib/types" },
  "include": ["src"],
  "references": [
    { "path": "../../../vendor/cordis" },
    { "path": "../ui-renderer" },
    { "path": "../ui-primitives" },
    { "path": "../ui-sidebar" },
    { "path": "../ui-slots" }
  ]
}
```

## 9.3 ⚠️ 再加 3 个登记点（漏一个就失败）

官方（`packages/client/AGENTS.md:147`）：客户端插件除了正常的包登记，还**必须**：

1. 在 `tsconfig.client.json` 的 `references` 里加你的包
2. 在 `packages/bundle/web-app/cordis.patch.yml` 里加一行
3. 在 `packages/bundle/web-app/package.json` 的依赖里加你的包

官方原文警告：

> 缺任一会在不同的更晚点失败。

**给新手的强烈建议**：直接让你的 Agent 抄一个现成的 client 包（如 `ui-brand-official`，src 总共 49 行），然后**逐项对照检查这 3 个登记点**。这是最容易漏、又最难排查的地方。

## 9.4 slots（插槽）：DSH 的 UI 扩展机制

### 9.4.1 设计原则

官方（`docs/subsystems/slots.zh.md:5`）：

> 功能插件**只**通过 `ctx.slots.register()` 贡献 UI，**绝不导入其他功能插件的组件**。

**唯一的注册 API**（用法见 `packages/client/AGENTS.md:11`；完整选项类型 `packages/client/ui-slots/src/index.ts:879` `interface ErasedOptions`）：

```ts
ctx.slots.register({ name, id?, key?, order?, children?, store?, inject? }, Component)
```

⚠️ 没有别的花哨接口：没有单独的 slot 定义调用、没有白名单对象、没有 helper。

### 9.4.2 两个正交维度：基数与作用域

来源：`docs/subsystems/slots.zh.md:52-64`（逐字表格；旧引 `:48-60`）

| 维度 | 值 | 含义 |
|---|---|---|
| 基数 | `single` | 单个 cell，渲染当前 priority 胜者 |
| 基数 | `list` | cell 由必填 `id` 定址，先按 `order`、再按注册顺序排列 |
| 基数 | `keyed` | owner 传入 `entryKey`；匹配 cell 以该 key 对应的 props 渲染 |
| 基数 | `chain` | 每个 entry 提供纯 `select(owner)` 函数；按 priority 顺序第一个非 null 结果获选 |
| 作用域 | `root` | 一个 root 作用域组件和 store 实例 |
| 作用域 | `session-maybe` | 跟随当前选择，但没有 Session 时仍可渲染 |
| 作用域 | `session` | 要求可解析的 Session binding |

### 9.4.3 可用的插槽树（节选）

完整树见 `docs/subsystems/slots.zh.md:117-183`（旧引 `:113-175`）。以下是**最常用的部分**：

```text
root
├─ sidebar
│  ├─ sidebar.brand.mark
│  ├─ sidebar.brand.name
│  ├─ sidebar.panellist
│  ├─ sidebar.footer.action
│  └─ sidebar.settings
│     ├─ settings.section
│     │  ├─ settings.general.item
│     │  ├─ settings.models.provider-card
│     │  └─ settings.plugins.tab
├─ main
│  ├─ main.plugins                        ← 插件页（key = 'plugins'）；**设置卡片改挂这里**（第 10 章）
│  │  ├─ plugins.item                     ← list：插件自己的配置条目
│  │  ├─ plugins.bundle.config            ← keyed：按 bundle 包名
│  │  └─ plugins.row.config               ← keyed：按 `<包名>#<行 id>`
│  └─ main.conversation
│     ├─ conversation.session
│     │  └─ conversation.view
│     │     └─ conversation.chat.node
│     │        └─ tool.call.toolview       ← 工具卡片（第 8 章提到）
│     ├─ conversation.session.header.actions   ← 标题栏按钮（示例用这个）
│     └─ conversation.composer.bar
│        ├─ conversation.input.attachments
│        ├─ conversation.input.plan
│        └─ conversation.input.model
├─ rightbar
│  └─ rightbar.session
│     └─ sidebar.right.pane.tab
└─ shell.overlay
```

> 🔴 **`dsh-v0.1.7-rc.2` 那轮新增 3 个插槽（+3 / −0）**；**`0.2.0-rc.1` 那轮插槽零变化（+0 / −0）**；**`0.2.0-rc.2` 那轮新增 1 个（+1 / −0）**；**`0.2.1-alpha.1` 那轮新增 2 个（+2 / −0）**；**`0.2.1-alpha.2` 那轮新增 2 个（+2 / −0）**；**`0.2.1-alpha.3` 那轮新增 5 个、移除 1 个（+5 / −1）**；**`0.2.1-alpha.4` 那轮新增 1 个（+1 / −0）**；**`0.2.1-rc.2` 这轮新增 1 个（+1 / −0）**；**`0.2.1-rc.3` 这轮新增 3 个（+3 / −0）** —— 上面这棵树是**节选**（权威全量约 **103** 个公开键，见 `08-cheatsheet.md` §3），这几轮新增的都不在节选里，登记在此免遗漏：
> - **`shell.quota-notice`**（`chain` / `scope: root`）—— 框架级配额提示链。宿主 `ui-chat` 在 `shell.overlay` 里放了唯一的活体 host（`QuotaNoticeHost`），**第一个 selector 命中其 code 的 entry 接管该面**；全部 decline 时回落到 host 自带的通用 warning Toast。因为 host 在 Chat 面板之外，提示**能活过面板的切换/关闭**。声明：`packages/client/ui-chat/src/client/contract/slots.ts:329`（另有 `apply.ts:265`）。
> - **`sidebar.session.row.leading`** 与 **`sidebar.session.row.hover`**（都是 `list`）—— 会话行的**行首区**与**悬停区**。新宿主 `ui-schedule`（定时任务）用它们挂任务标记与悬停卡片：`packages/client/ui-schedule/src/client/index.ts:231`（leading）/ `:238`（hover）。声明：`packages/client/ui-workspace/src/client/contract/slots.ts`。
> - 🆕 **`sidebar.right.tab.files.actions`**（`0.2.0-rc.2` 新增，`list` / `scope: 'session'`）—— **文件树「重新加载」控件之后的目录动作位**，owner 属性给 `absolutePath`（当前展示的目录绝对路径）。声明与宿主同在 `packages/client/ui-sidebar-files/src/client/index.ts:34`（宿主是该包的 `FilesBody`；`sidebar.right.pane.tab` 里的 `FILES_ID` 条目在挂载期间它才存在）。⚠️ 同一版里 `conversation.chat.node` 的**已占用 key 表**多了 `question-reply`（`ui-user-questions` 的 `QuestionReplyView`）—— 那是 **chat-node 的 key**，**不是插槽名**，别照抄成 `ctx.slots.register({ name: 'question-reply' })`。
> - 🆕 **`plugins.add.actions`**（`0.2.1-alpha.1` 新增，`list` / `scope: 'root'`）—— **插件页「添加插件」菜单里追加的动作行**（安装完成后出现；每行 72px 高，含标题与两行内的描述；owner 提供 `onDismiss()`，用于先关菜单再启动动作）。声明在 `packages/client/ui-plugin-manager/src/client/slot-contract.ts:118`（宿主包 `@deepseek-ai/dsh-client-ui-plugin-manager`；`PluginAddActionsProps` 在同文件 `:110`）。
> - 🆕 **`shell.bottom`**（`0.2.1-alpha.1` 新增，`single` / `scope: 'root'`）—— **横跨三列下方的整行底部面板位**（占用方自管高度与显隐；三列按该高度收缩，空内容不预留空间；切换主面板时保留底部组件；列宽拖拽手柄止于其上方，`shell.overlay` 仍覆盖整框）。**声明宿主是 `ui-layout`**：`packages/client/ui-layout/src/client/index.ts:94`（渲染点 `packages/client/ui-layout/src/client/AppFrame.tsx:290`）。首个占用方是 `@deepseek-ai/dsh-experimental-inspector`（`packages/experimental/inspector/src/client/bottom/page.tsx:63,91`，devtools iframe + 快捷键切换，高度走 `--inspector-height`）。
> - 🆕 **`conversation.chat.flow`**（`0.2.1-alpha.2` 新增，`single` / `scope: 'session'`）—— **一次渲染的 Chat 流**（有序行 + 本地回显）；带 `hookContext`（`ChatFlowHookContext`，提供 `motion: FlowMotionRows`）与 `inject.hooks`（`groupAction` / `groupHeaderAction` 两个 viewport 级 hook 工厂）。🔴 **它同时改了上层结构**：`conversation.view` 的 `PropsRenderSlots` 由 `conversation.chat.node` **改成 `conversation.chat.flow`** —— 即 view 不再直接渲染 chat node，而是渲染 flow、由 flow 内部再渲染 `conversation.chat.node`。声明：`packages/client/ui-chat/src/client/contract/slots.ts:392-398`（owner 类型 `ChatFlowOwnerProps` 在同文件 `:335-344`）。
> - 🆕 **`conversation.chat.reasoning.body`**（`0.2.1-alpha.2` 新增，`single` / `scope: 'session'`）—— **展开后的推理正文位**；owner 给 `{ text, running }`（原始模型文本 + 尾部是否仍在流式，`packages/client/ui-chat/src/client/contract/slots.ts:80-86`）。官方 entry 优先级 **100** 并调用 reasoning Content Factory，**更小的优先级值会替换它**；贡献者**必须保留对原始文本的访问**。声明：同文件 `:470`。
>
>   ⚠️ **版本分叉（2026-10-31 登记，别混用两个轴）**：**基线 `dsh-v0.2.2-alpha.2` 上 props 只有 `text` / `running`**（上句即按基线写）。维护旁线 `dsh-v0.2.1-rc.5`（`b830ec950f`）上，`ReasoningBodyOwnerProps` **多一个 `rawText`**（完整模型输出），且 `text` 改为「Chat 处理后的显示文本」（`slots.ts:79-86`，该树内 `ReasoningContentInput` 也不再 `extends` 它）。同一改动**已在主线 tip `ce7073d512` 上存在**，只是**还没进入本技能基线 tag**。→ 读 `text` 的插件在两条线上都能跑；**只有需要原始输出时才用 `rawText`，并且要先确认运行版本的 props**（`grep -n "readonly rawText" packages/client/ui-chat/src/client/contract/slots.ts`）。上游权威说明：`docs/upgrade-guide/v0.2.1-rc.4/reasoning-body-props/guide.zh.md`（该目录名 = 升级**起始**版本，不是发布版本）。
>   ⚠️ 同批还有一个**易混项**：`conversation.chat.reasoning.content` 落在 `SlotFactoryMap`（**不是 `SlotMap`**，同文件 `:381-387`，`scope: 'root'`）—— 那是**内容工厂**，**不是可注册的插槽键**，别照抄成 `ctx.slots.inject('conversation.chat.reasoning.content', …)`。
> - 🆕 **`0.2.1-alpha.3` 那轮 +5 / −1** —— 新增 `conversation.chat.message.images` / `conversation.chat.user.images` / `conversation.hero.options` / `conversation.user.text.node` / `workspace.toast`；**移除 `conversation.message.images`**（本链上**第一次出现「移除」**）。⚠️ **诚实声明：这是上一轮（技能 1.5.0）该登记而漏登记的一处** —— 上一轮只把计数链推进到了 `08` / `11` / `api-claims`，这句「登记在此免遗漏」的承诺没兑现；**本轮补记**。逐键位置仍见 `api-claims.md` §7.3 第 2 行（那里有完整的键名与 `slot-catalog.ts` 步进）。
> - 🆕 **`plugins.tab`**（`0.2.1-alpha.4` 新增，`list` / `scope: 'root'`）—— **插件页在自带的「已安装」标签之后的贡献标签页**（官方首个占用方就是市场页 **Discover**）。条目给 `id` / `order` / `label` / `locale`；选中后在页头与标签行之下渲染该条目自己的内容，而**安装动作不自己画，要调 owner 给的 `install()`**（打开页面的安装对话框并直接停在「校验 / 进度」两屏，跳过规格表单）。owner props `PluginTabProps` = `{ install(target: PluginTabInstall): void; openPackage(packageName: string): void }`，其中 `PluginTabInstall` = `{ spec; registry?; title; version }`（`title` 是**已本地化**的显示名，`registry` 缺省则沿用对话框自己的源）。声明：`packages/client/ui-plugin-manager/src/client/slot-contract.ts:124`（owner 类型 `:95-107`、`PluginTabInstall` `:83-92`）；宿主渲染点 `packages/client/ui-plugin-manager/src/client/PluginManagerPage.tsx:1662`，台账 `.../client/tab-ledger.ts`（`navigation-store.ts:12`：`'installed'` 是页面**自带**页签，其余值即 `plugins.tab` 条目的 id）。官方占用方 = `ui-plugin-market`：`packages/client/ui-plugin-market/src/client/index.ts:55-56` 注册 `{ name: 'plugins.tab', id: 'discover', label: () => t('title'), locale: NS, … }`，组件 `DiscoverSection.tsx`。
>   🔴 **极易与 `settings.plugins.tab` 混淆（同名不同物，选错就注册到另一个页面去了）**：那个是**设置面板 → 插件分区**的标签页（owner `SettingsPluginsTabOwnerProps`，声明 `packages/client/ui-settings/src/client/contract/slots.ts:66`，宿主 `ui-settings-plugins`）。**判据：带 `settings.` 前缀 = 设置面板；无前缀 = 插件页。**
> - 🆕 **`conversation.input.model.label`**（`0.2.1-rc.2` 新增，`single` / `scope: 'session'`）—— **输入区模型选择器里的非交互式行内标签**：owner 给 `{ provider, model, placement, selected }`，`placement` 为 `'trigger'`（输入按钮）/ `'menu'`（根菜单当前值）/ `'option'`（可选模型行）三处之一，`provider` 只含 `{ id, name }`（**不含任何连接配置**）。**没有贡献方时 composer 显示目录名**；**选择控件仍由宿主 `ui-model-selection` 拥有**，贡献方只负责展示（该键还带 `inline: true`）。声明：`packages/client/ui-model-selection/src/client/slots.ts:37-42`（owner 类型 `ModelLabelOwner` 同文件 `:9-18`）；宿主 entry 挂在 `conversation.input.model` 之下，**那个 entry 卸载时本插槽随之消失**。该插槽的「**装饰既有 UI 而不接管它**」写法见声明处的 JSDoc 示例（`packages/client/ui-model-selection/src/client/slots.ts:28-41`）：`ctx.slots.inject(key, () => ctx.slots.register({ name, locale }, Component))`，宿主一换实现，装饰自动跟着走 —— 想改官方某个位置的外观又不想接管整个面时，照这个写法。⚠️ 该插槽原先的官方首个占用方 `@deepseek-ai/dsh-client-ui-deepseek-model-label-1017` **已在 `0.2.2-alpha.2` 移除**（包目录一并消失），别再按那个包名找范例。

> - 🆕 **`0.2.1-rc.3` 那轮 +3 / −0 —— 三个「More 菜单行」同族插槽**：`sidebar.panellist.actions`（左侧面板列表）/`conversation.session.header.views.actions`（Conversation 的 View 标签行）/ `sidebar.right.tab.guide.actions`（右栏 Guide 卡片）。三者的形状**完全一致**：`kind: 'list'` + `scope: 'root'`，owner 都给 `{ entries, onOpen(id), onPinnedChange(id, pinned), onDismiss }`；**各自的区域只在该 list 有登记时才画出 More 按钮与菜单**，所以**不注册就完全不占位**。`entries` 里的每项给 `{ id, label, pinned }`（`pinned` = 用户是否手动钉住；**钉住也可能因宽度预算被折进 More**），面板与 View 两族的项另带可选 **`active`**（当前选中项，**与钉住状态彼此独立**）。🔴 **`pinned` 与 `active` 是两件事**：前者决定「在不在主区域显示」，后者只表示「是不是当前选中的那个」—— 上游在**同一区间内**专门修过一次这件事（`39d2903841 fix(ui): separate navigation pins from selection and show menu icons`），即两者曾被混为一谈；按直觉写很容易把「选中」当成「钉住」。声明：`packages/client/ui-sidebar/src/client/contract/slots.ts:38`（owner 类型 `SidebarPanelActionsOwnerProps` 同文件 `:103`）、`packages/client/ui-conversation/src/client/contract/slots.ts:276`（`ConversationViewActionsOwnerProps` `:458`）、`packages/client/ui-sidebar-right/src/client/contract/slots.ts:91`（`SidebarRightGuideActionsOwnerProps` `:232`）。官方首个占用方是新包 `@deepseek-ai/dsh-client-ui-entry-customization`（在三个区域提供插件浏览与 Creator 草稿入口，由 `packages/bundle/web-app/cordis.patch.yml:427` 装入；它自己**不存任何状态**）。
> - 🆕 **`0.2.2-alpha.2` 那轮 +3 / −0 —— 又一个用户消息与侧栏行的扩展点**：`conversation.chat.user.before`（`chain` / `session`：用户消息**源装饰**，由 user Node entry 拥有并渲染，按「durable source + row kind」选择器选一个组件；**无匹配不渲染**，steering 与 pending 行不渲染，声明 `packages/client/ui-chat/src/client/contract/slots.ts:446`）/ `conversation.chat.text-interaction`（`keyed` / `session`：助手文本段落内的局部交互面，每个消费方自己注册同步准入，`…/contract/slots.ts:417`）/ `sidebar.session.row.trailing`（`list` / `root`，`inline: true`：侧栏会话行时间标签之后、pin 标记之前的**非交互图标**，按 `order` 升序；可 hover 的设备上，行被 hover / 获得键盘焦点 / 菜单展开时**隐藏**；**空白会话不渲染该插槽**；占用方须按 Session id 自取数据，**不得持有 Session**，声明 `packages/client/ui-workspace/src/client/contract/slots.ts:146`）。计数：声明侧 **144 → 148**、并集 **146 → 150**、`slot-catalog.ts` **103 → 106**。

💡 运行中的 DSH 用 `cordis_inspect_query`（先 `cordis_inspect_list` 拿 method）查**实时**插槽树。⚠️ 上游文档写作 `cordis_inspect what:"client"`（`docs/subsystems/slots.zh.md:202`），但**当前工具面没有裸 `cordis_inspect`** —— 实际只有族名 `cordis_inspect_list` / `cordis_inspect_query` / `cordis_inspect_self`（`packages/extensions/tool-cordis/src/index.ts:23,42`）；UI 侧具体查 `Slots.listSubTree`。**客户端插槽的静态权威**是生成产物 `slot-catalog.ts`（见 `scripts/extract_slots.py` 的 A2 段）。

### 9.4.4 最小可用示例：往标题栏加一个按钮

来源：`docs/subsystems/slots.zh.md:25-48`（逐字，原文标注 `tsx ignore-check`；旧引 `:21-44`）

```tsx ignore-check
import type { Context } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'
import type {} from '@deepseek-ai/dsh-client-ui-session/client'
import type { PropsRuntime } from '@deepseek-ai/dsh-client-ui-slots'

type HeaderActionProps = PropsRuntime<'conversation.session.header.actions'>

function HeaderAction({ useSession }: HeaderActionProps) {
  const running = useSession(snapshot => snapshot.running)
  return <button disabled={running}>Review</button>
}

export const inject = ['slots']

export function apply(ctx: Context): void {
  ctx.slots.inject('conversation.session.header.actions', () =>
    ctx.slots.register({
      name: 'conversation.session.header.actions',
      id: 'review',
      order: 100,
    }, HeaderAction))
}
```

**逐点解释**：

| 代码 | 含义 |
|---|---|
| `import type {} from '...'` | 只引入**类型声明**（让插槽名和 props 有类型），**不引入运行时值** |
| `ctx.slots.inject(key, cb)` | 「等这个插槽被声明出来，再执行 cb」。owner 折叠时移除，重新声明后再跑，随你的 fiber 离开 |
| `ctx.slots.register({name, id, order}, Component)` | `id` 用于 `list` 基数；`order` 决定排序 |
| 组件签名 `{ useSession }` | 组件**不收到 `ctx`**！只收到框架给的几组 props |

⚠️ **注册进未声明的 slot 会在激活时报错**（`slots.zh.md:15-19`）。所以务必用 `ctx.slots.inject` 包一层，或者确认目标插槽一定存在。

### 9.4.5 组件能拿到什么（四个 share）

来源：`docs/subsystems/slots.zh.md:66-81`（旧引 `:62-77`）

| props 组 | 内容 |
|---|---|
| `PropsRuntime<K>` | owner 值与标准 scope 值 |
| `PropsRenderSlots<S>` | 获授权的子 slot 渲染器 |
| `PropsStore<H>` | 共享视图状态的 selector hook 与 mutation callback |
| `InjectFace<I>` | 私有数据、callback 与 observable hook |
| `PropsLocale<N>` | 国际化文案 |

**框架提供的 hook**：`useSessions`、`useSession`、`useProjection`、`useConversation`、`useInput`、`inputActions`、`useChat`、`useTrajectory`、`useWorkspaces`、`usePanelInfo`，以及按声明 store 生成的 `useStore` 和按 locale namespace 生成的 `t`。

⚠️ **硬规则**（`slots.zh.md:77`）：**组件绝不会收到 `ctx`**。这是刻意的设计——UI 组件不该直接摸服务，必须走声明的 props。

## 9.5 前端技术栈约束（写错会被门禁拦）

| 事实 | 来源 |
|---|---|
| **React 18**（`react: ^18.2.0`、`react-dom: ^18.2.0`） | `packages/client/ui-theme/package.json`、`apps/web/package.json` |
| **样式：CSS Modules + `clsx`**，用语义 token `--dsw-*` | `docs/web-styling.zh.md:16` |
| ⚠️ **不得添加组件库或 Tailwind** | `packages/client/AGENTS.md:118` |
| 不得写颜色字面量，要用 `--dsw-alias-*` 语义别名 | `docs/web-styling.zh.md:9,17` |
| 业务组件**不得**含订阅机制（无 `useSyncExternalStore`、无手写 subscribe） | `packages/client/AGENTS.md:26` |
| ⚠️ **跨插件的运行时值导入被门禁拒绝**，只能 `import type` | `packages/client/AGENTS.md:40` |

**最后一条最容易踩**：你想用别的插件的组件？**不行。** 只能通过 slots 组合，或者通过注入的 Cordis 服务协作。

## 9.6 样式与资源怎么打包

来源：`packages/client/tsdown.client.ts:1-8`

| 写法 | 打包行为 |
|---|---|
| `x.module.css` | 编译成**哈希类名** + 工厂执行时注入 `<style>` |
| `x.css?inline` | 编译后**文本**作为默认导出，供插件自己的生命周期 effect 使用 |
| `x.css` | 全局内联注入 |
| `?raw` 资源 | 内联成字符串（真实范例：`ui-sidebar-documentpreview` 内联 pdf.js worker） |

**结论**：**CSS 会被编进 `lib/client.js`**，不需要单独发布静态资源文件。`files` 里通常只列 `lib/index.js`、`lib/client.js`、`lib/types/**/*.d.ts`。

⚠️ **反直觉的事实（源码实证）**：动态 plugin bundle 是 **lazy-CJS factory**（`window.__ModuleLoader__.load({id, factory})`），**不是 ESM**。

> 🔧 **校正（2026-09-11）**：本节原先说「这是构建产物格式，你写代码时不用管」——**对仓库内开发成立，对仓库外开发不成立**。
> `clientBundle()` 这个共享 preset **没有对外发布**，官方原文（`adding-a-settings-card.zh.md`，`dsh-v0.1.7-rc.1` 里的新位置 **`:76`**；该文档本区间被整篇改写，旧行号 `:118` 已失效）写明「……`clientBundle` tsdown 预设位于 `packages/client/tsdown.client.ts`，而**不在任何已发布的包里**，因此仓库之外的包要自己复刻这一步构建」。
> 所以第三方 UI 插件作者**必须自己产出**这个格式：esbuild/rolldown 的 `format: 'cjs'` + `platform: 'browser'`，并自己拼那三行 banner/intro/footer。完整契约（含逐字三行与平台种子表 9 项）见 `14-inbound-http-and-timers.md` §17.3。

## 9.7 开发期调试 UI 插件

1. **客户端 HMR 需要单独跑 watcher**：源码实证 `apps/cli/reference/README.zh.md:81` —— 接收器始终挂载，但要单独运行 `pnpm run dev:web` 重建客户端 bundle 才会生效。
2. **不需要重新构建整个 Web 应用**：机制在新版 `adding-a-settings-card.zh.md:58` —— 客户端模块系统**扫描已启用的 Loader 条目**，找出声明了 `dsh.client` 的包并送出各自构建好的 `./client` 导出。（旧版 `:82` 那句逐字「只要 `cordis.yml` 挂载了插件，它就会出现在页面上——无需重新构建 Web 应用」已随该文档在 `0.1.7-rc.1` 被整篇改写而消失，**事实不变**。）
3. 用 `cordis_inspect_query`（`Slots.*`）看实时插槽树（**裸 `cordis_inspect` 不存在**，见第 2 章的说明）。

## 9.8 🤖 让 AI Agent 帮你做这一课

UI 插件最容易出错，**强烈建议先让 Agent 做一次"抄范本 + 登记"的热身**：

> 我要写一个 DSH 客户端（UI）插件，作用是**（描述，例如"在侧边栏底部加一个显示当前时间的按钮"）**。
> 请**分三步**做，每步做完等我确认：
>
> **第 1 步（选型）**：读 `docs/subsystems/slots.zh.md`，从插槽树里选一个合适的插槽，告诉我它的名称、基数（single/list/keyed）、scope，以及为什么选它。
>
> **第 2 步（抄范本）**：以 `packages/client/ui-brand-official/` 为范本，列出我需要的**全部文件清单**，以及**三个登记点**（`tsconfig.client.json` / `packages/bundle/web-app/cordis.patch.yml` / `packages/bundle/web-app/package.json`）分别要改什么。
>
> **第 3 步（写代码）**：写 Host 半侧（可以是空 `apply`）和浏览器半侧，组件用 React 18 + CSS Modules + `--dsw-*` token。
>
> 约束：**不允许**跨插件导入运行时值（只能 `import type`）；**不允许**引入组件库或 Tailwind；每个 API 标注仓库出处。

## 9.9 ✅ 第 9 章验收清单

- [ ] 我知道客户端插件必须有 Host 半侧 + 浏览器半侧
- [ ] `package.json` 里有 `exports["./client"]` 和 `dsh.client.platform = "web"`
- [ ] 三个登记点全部到位（用清单逐项勾）
- [ ] 我用的插槽名在 `slots.zh.md` 的插槽树里能找到
- [ ] 组件里**没有**用 `ctx`
- [ ] 没有跨插件导入运行时值、没有引入第三方 UI 库
- [ ] 在浏览器里真的看到了我的东西

---

# 第 10 章 第八课｜设置卡片：让用户在界面里配置你的插件

> **本课目标**：在 DSH 的「插件配置」页面里，给你的插件显示一张卡片，用户点点鼠标就能改配置。
> **前置**：需要先完成第 5 章（Config）和第 9 章（UI 插件）。

## 10.1 三层配置解析模型（必须先理解）

> 🔴 **`dsh-v0.1.7-rc.1` 起整个设置机制被重做**（本区间最大的破坏性变更）：旧的「插件自选一个 settings 命名空间 + 手写设置卡片」模型**已整体移除**，改为「**从 Config schema 自动派生表单** + 配置编辑器写 Cordis patch 持久化」。`SettingsScope` / `installSection` / `settings.yaml` 在源码里**已不存在**（逐条对照见 §10.9）。

**现在的分层**（来源：`docs/subsystems/settings.zh.md:9`；该句原文列举的三个值：实际值 / 继承值 / 显式 profile 覆盖值，下方为据此展开的分层示意）：

```
① 继承值 inherited      ← schema 默认值 + 注册方 base（cordis.yml 那一行的 config，第 5 章）
        ↓ 被 profile 覆盖
② 显式 profile 覆盖值    ← 配置编辑器写进 profile 的 Cordis patch（用户在界面上改的部分）
        ↓ 合成
③ 实际值 actual         ← 业务消费者对自己 Config 引用调用 .get() 读到的值
```

**核心机制**：`ctx.settings.update(ns, patch, expectedRevision?)` 把稀疏 patch **合并进该条目自己的 Config**；每次写入**先校验完整 Config**，并带**乐观并发栅栏** `expectedRevision` —— 不匹配就抛 `SettingsConflictError`（`code = 'SETTINGS_CONFLICT'`），**不覆盖并发变更**。

来源：`docs/subsystems/settings.zh.md:9-15`（逐字）；实现 `packages/settings/settings/src/index.ts`

## 10.2 Host 半侧：**不写注册代码**，表单从 Config 派生

> 🔴 **本区间最需要改认知的一条**：`0.1.6-alpha.2` 及以前，你必须写一段 Host 半侧代码把插件**注册成设置命名空间**；**`0.1.7-rc.1` 起这条路没了** —— 表单由**你的 `Config` schema + profile 条目**自动派生，**你不写任何注册调用**。

旧写法（**已失效，仅供识别老代码/老教程**；原骨架取自 `docs/cookbook/adding-a-settings-card.zh.md` 的**旧版**（该文档自 `0.1.7-rc.1` 起已整篇改写，**旧行号在新树不可核**））：

```ts
// ⚠️ 已失效：installSection 在 0.1.7-rc.1 的新树源码里已无定义
ctx.inject(['settings'], (settingsCtx) => {
  settingsCtx.settings.installSection(ctx, MY_PLUGIN_NS, Config, config, {
    validate: value => void assertReachable(value.endpoint),
    setSource: (current) => { source = current },
    onChange: () => { rebuildFromSettings(source()) },
  })
})
```

**现在你要做的只有两件事**：

1. 在插件里正常声明 `Config`（schemastery schema，见第 5 章）—— **表单字段就是从它派生的**（依据：`docs/subsystems/settings.zh.md:29` 逐字 —— `Project Config schemas into forms and own optional instance-level UI policy.`；实现侧在 `packages/boot/app-boot/src/config-schema/`，`generateConfigSchema()` 由 `--dump-config-schema` 输出，见 `06-workflow.md` §12.1）；
2. 想让某个实例**不自动出页面**时，才调用一次 `ctx.settings.configure({ auto: false }, owner)`（`owner` 省略即当前 fiber）。

**命名空间是什么**（关键变化）：`ns` 不再是你自选的字符串，而是**当前 profile 里可唯一定位该条目的本地 id**（同一插件的多个实例，条目 id 不同 → 各自独立表单）。普通字段被排除。

**`ctx.settings`（`SettingsForms`）的精确签名**（`docs/subsystems/settings.zh.md:31-71`，逐字）：

```ts
configure(presentation: { auto?: boolean }, owner: Fiber = this.ctx.fiber): () => void
prepareDocument(): Promise<string>
describe(options?: SettingsDescribeOptions): SettingsDescriptor[]
async update(ns: string, patch: object, expectedRevision?: number): Promise<void>
async replace(ns: string, section: object, expectedRevision?: number): Promise<void>
async mutate(ns: string, ops: readonly SettingsPathOp[], expectedRevision?: number): Promise<void>
```

**三个写入 API 的选择**（关键区分）：

| API | 语义 | 何时用 |
|---|---|---|
| `update(ns, patch, expectedRevision?)` | **合并**提交的字段 | 表单改了几个字段，其余保持 |
| `replace(ns, section, expectedRevision?)` | 先把**即时字段重置为继承配置**，再应用提交字段 | 「先恢复默认、再整体设一遍」 |
| `mutate(ns, ops, expectedRevision?)` | 按**独立路径**编辑，**保留客户端响应中未包含的秘密值**；`unset` 某个数组下标即删除该元素 | 精细编辑、要避开脱敏字段 |

## 10.3 浏览器半侧：配置页也从 Config 派生

> 🔴 **手写设置卡片这条路在 `0.1.7-rc.1` 已被移除**：`packages/client/ui-settings-plugins/src/client/` 的卡片族（`BashCard` / `AgentLoopCard` / `SubagentCard` / `WebSearchCard` / `card-form.ts` / `fields.tsx` / 各 `*-card-controller.ts`）**整体删除**（本区间 **−4608 行 / +73 行**），客户端服务 `settingsScope` 也**已移除**。原先挤在一个包里的官方配置页，现在拆成**每个插件一个伴生包**：`ui-settings-shell` / `ui-settings-agent-loop` / `ui-settings-subagent` / `ui-settings-web-search` / `ui-settings-plugin-inventory`。

**默认情况：你不用写任何浏览器半侧代码** —— 你的 `Config` schema 会在**插件页**自动渲染出配置表单（读写与持久化由配置编辑器承担）。

**只有要「自定义一张页面」时才注册插槽**（`plugins.*` 声明见下面 **9 键块**）。注册进 `plugins.item` 的宿主组件收到的是 `PluginConfigViewProps`（**只有 `view: 'summary' | 'page'`**），**不再**是 `SettingsScope` —— 读写配置要走 `ctx.remote.settings`（Host 侧 `ctx.settingsController`）。

> ⚠️ **「内置插件」设置分区现在只是个壳**：`ui-settings-plugins` 只拥有设置导航项与标签行，声明 `settings.plugins.tab`（根级 list slot）—— 它**不再自带任何配置卡片**。要贡献标签页就按 `id` / `order` / `label` 注册进 `settings.plugins.tab`（官方口径：`packages/client/ui-settings-plugins/README.zh.md`）。

> 🔴 **`dsh-v0.1.6-alpha.2` 起：插槽名是 `plugins.item`（`list` 语义），不再是 `settings.plugin.item`（`keyed` 语义）。**
> 两者**不是别名关系**：旧槽以「卡片所编辑的 settings 命名空间」为 `key`，新槽是普通列表项，用 `id` / `order` / `label`，组件额外收 `view: 'summary' | 'page'` 两个态。
> 依据：`packages/client/ui-plugin-manager/src/client/slot-contract.ts:136`（权威声明；`0.1.7-rc.1` 那轮由 `:32` 位移至此，本基线再因文件增行下移至 `:136`）、`packages/client/ui-settings-agent-loop/src/client/index.ts:47-48`（官方自己的注册方 —— 配置页已拆成**每插件一个伴生包**，并用 `ctx.configForms.whileServed([NS], …)` 包住 `slots.inject('plugins.item', …)`，即「Host 正服务该条目期间」才注册）。
> ✅ **上游文档已跟上（2026-09-23 复核，撤销上一轮的警告）**：上一轮（基线 `0.1.6-alpha.2`）曾记录「该 cookbook 零改动、仍在教 `settings.plugin.item`」。**在 `dsh-v0.1.7-rc.1` 里它已被整篇改写**：标题换成「实践指南：即时配置表单」，全文**再无 `settings.plugin.item`**，并改为教 `plugins.item`（`:72`）与新的 `plugins.detail.actions` / `.badge` / `.section`（`:46-53`）。
> ⚠️ **但改写带来另一类风险：行号级引用全线失效**。该文档由 100+ 行缩到 **72 行**，本技能原先指向它的逐字引文（旧 `:50` / `:72` / `:82` / `:94` / `:102` / `:13-44` / `:52-70`）**已不再指向原文** —— 本节与 `14 §17.3` 的引用已就地改为「旧位置 + 新位置」或改引源码。**这正是「完备性/出处措辞会静默腐化」的又一实例**：事实没变，出处漂了。
> 机器判据：`verify_absorbed_claims.py` 的 `U06` / `U07` / `U09` / `U10`（新槽已声明）、`X06`（旧槽不再被声明）、`X07`（`conversation.session.header.leading` 已移除）、`B08`（预设仍未发布，按**新措辞**锚定）。

**这组插槽的声明**（源码 `packages/client/ui-plugin-manager/src/client/slot-contract.ts`，对基线 `dsh-v0.2.2-alpha.2` 逐字（该文件在 `0.2.1-rc.2 → -rc.3` 区间零改动）；**条数勿硬抄** —— 复现：`grep -c "^    'plugins\." <该文件>` → **9**）：

> 📈 **历史计数（勿当现值）**：`dsh-v0.1.7-rc.1` 那轮由 3 个键增至 7 个；`0.2.1-alpha.1` 加 `plugins.add.actions`；**`0.2.1-alpha.4` 加 `plugins.tab`**。⚠️ 该文件**头部的分组散文**（「Three carry… / Three more take…」）只点名了 **7** 个键（未点名 `plugins.add.actions` 与 `plugins.bundle.activation`），**不是全量计数** —— 一律以 `declare module` 块为准。

```ts
declare module '@deepseek-ai/dsh-client-ui-slots' {
  interface SlotMap {
    'plugins.add.actions': { kind: 'list'; scope: 'root'; owner: PluginAddActionsProps }
    'plugins.tab': { kind: 'list'; scope: 'root'; owner: PluginTabProps }
    'plugins.bundle.activation': { kind: 'keyed'; scope: 'root'; owner: PluginActivationOwnerProps }
    'plugins.item': { kind: 'list'; scope: 'root'; owner: PluginConfigViewProps }
    'plugins.bundle.config': { kind: 'keyed'; scope: 'root'; owner: PluginConfigViewProps }
    'plugins.row.config': { kind: 'keyed'; scope: 'root'; owner: PluginConfigViewProps }
    'plugins.detail.actions': { kind: 'list'; scope: 'root'; owner: PluginDetailProps }
    'plugins.detail.badge': { kind: 'list'; scope: 'root'; owner: PluginDetailProps }
    'plugins.detail.section': { kind: 'list'; scope: 'root'; owner: PluginDetailProps }
  }
}
```

> **`plugins.detail.*` 三兄弟怎么选**（官方 cookbook `:46` 原文口径）：对**不属于自己**的组合包 / 行 / 官方插件有话要说的插件 —— 页头控件用 `.actions`、标题旁的标签用 `.badge`、页面自身内容之下的区块用 `.section`。条目按页面的 `subject` 渲染（`{ kind: 'bundle', pkg }` / `{ kind: 'row', pkg, row }` / `{ kind: 'item', id }`），对无话可说的 subject **返回 `null`**。

`PluginConfigViewProps` = `{ readonly view: 'summary' | 'page' }`：`summary` 渲染标题下的一行摘要，`page` 渲染带保存控件的整张表单。`plugins.bundle.config` 以 **bundle 包名**为键、`plugins.row.config` 以 **`<包名>#<行 id>`** 为键——给「一个 bundle 自己的配置」和「bundle 里某一行插件的配置」用，不占 `plugins.item`。

**什么时候用哪个**：

| 你要做的事 | 用哪个插槽 |
|---|---|
| 给一个官方插件做配置页 | `plugins.item`（`id` + `order` + `label`） |
| 给一个 bundle 整体做配置页 | `plugins.bundle.config`（key = 包名） |
| 给 bundle 里某一行做配置页 | `plugins.row.config`（key = `<包名>#<行 id>`） |

## 10.4 浏览器侧读写配置的 API

> 🔴 **`SettingsScope` 与 `settings-contract.ts` 在 `0.1.7-rc.1` 已被删除**（客户端 `ui-settings` 现在给的是 `config-form.ts` / `config-form-types.ts`）。读写契约换成**远程设置控制器**。

来源：`docs/subsystems/settings.zh.md:77-129`（逐字）；实现 `packages/api/settings-controller/src/index.ts`

**`ctx.remote.settings` —— 读写都走它**（Host 侧由 `ctx.settingsController` = `SettingsController` 承载，全部标 `@Remote`）：

```ts
// 读：描述每个条目的表单（脱敏后的分层值 + 页面渲染表单用的序列化 schema）
describe(): SettingsDescribeValue
// 三种写
update(ns: string, patch: Record<string, JsonValue>, expectedRevision: number | undefined): Promise<SettingsNamespaceView>
replace(ns: string, section: Record<string, JsonValue>, expectedRevision: number | undefined): Promise<SettingsNamespaceView>
mutate(ns: string, ops: SettingsPathOpView[], expectedRevision: number | undefined): Promise<SettingsNamespaceView>
// 在原生编辑器里打开 provider 拥有的设置文档
openSettingsDocument(signal: AbortSignal): Promise<SettingsDocumentOpenValue>
```

**三条必须知道的规则**：

1. **命名空间 = profile 条目 id**（不再是插件自选字符串）；描述符里同时带**实际值 / 继承值 / 显式 profile 覆盖值**与乐观修订号（`docs/subsystems/settings.zh.md:9`）。
2. **`update` 合并 / `replace` 先重置为继承配置再应用 / `mutate` 按路径编辑且保留客户端响应里未包含的秘密值**（同文档 `:13`）。
3. **⚠️ 每次写入都要带 `expectedRevision` 作栅栏**：`undefined` = 无条件写；不匹配的写入会被**拒绝**（Host 抛 `SettingsConflictError`，`code = 'SETTINGS_CONFLICT'`；远程面归类为 `settings/conflict` 或 `settings/rejected`），**不覆盖并发变更**。

**对新手的意思**：**读 → 改 → 带 revision 写**，失败就重新读一遍。事件 `settings/document-updated`（emit）在 Loader 配置变化后让表单描述符失效，客户端收到后要**重读 schema、值与修订号**。

## 10.5 配置页什么时候才会显示

来源：`docs/subsystems/settings.zh.md:9`（描述符口径）＋ `packages/client/ui-settings-plugins/README.zh.md`（分区壳口径）

> 表单命名空间是**当前 profile 中可唯一定位条目的本地 id**；多个插件实例在条目 id 不同时拥有独立表单。

**翻译**：配置页的前提改为「**你的插件在活动 profile 里有条目、且声明了 `Config` schema**」。旧机制里「Host 半侧先注册命名空间、浏览器半侧才敢挂卡片」的两段式依赖**已经消失** —— 表单是**派生**出来的，不是注册出来的。

**分区与标签页**：设置导航项由 `ui-settings-plugins` 这个**壳**拥有（注册进 `settings.section` 的 `plugins` 项，子槽 `settings.plugins.tab`）；条目顺序由 `order` 决定、`label` 随当前语言解析。**一个标签页贡献都没有的部署只显示空提示**。

## 10.6 真实范本

| 范本 | 路径 | 教什么 |
|---|---|---|
| **插件页 + 配置插槽宿主** | `packages/client/ui-plugin-manager/` | `plugins.item` / `plugins.bundle.config` / `plugins.row.config` 的声明与两态（`summary` / `page`）渲染；面板注册进 `main`（key = `plugins`） |
| **设置分区壳** | `packages/client/ui-settings-plugins/` | 只拥有设置导航项与 `settings.plugins.tab` 标签行 —— 看「一个壳怎么把内容让给功能插件」 |
| 官方配置页（每插件一个伴生包） | `packages/client/ui-settings-shell` / `-agent-loop` / `-subagent` / `-web-search` / `-plugin-inventory` | 本区间新拆出的**标准形态**：功能插件自带页面，不再挤在一个包里 |
| 设置行 + 主题服务 | `packages/client/ui-theme/` | `settings.general.item` + locale + store + CSS 全套 |
| **Host 侧配置服务** | `packages/settings/settings/src/index.ts`（`SettingsForms`） | `describe` / `update` / `replace` / `mutate` / `configure` 与 `SettingsConflictError` |
| **远程设置面** | `packages/api/settings-controller/src/index.ts` | `ctx.remote.settings` 的 `@Remote` 读写与拒绝分类 |
| Host 侧 schema | `packages/client/ui-theme/src/theme-settings.ts` | "配置项 = Cordis Config = schemastery schema" 同一份声明 |

## 10.7 🤖 让 AI Agent 帮你做这一课

> 我要让用户能在界面里配置「（插件名）」的 **（字段列表）**。
> 请：
> 1. 先讲清楚现在的分层模型（继承值 = schema 默认 + 注册方 base / profile 覆盖值 / 实际值），并说明我的每个字段分别落在哪一层；
> 2. 检查我的 `Config` 是否是 schemastery schema —— **表单是它派生的，不要写任何 Host 半侧「注册命名空间」的代码**（`installSection` 已不存在）；
> 3. 说明默认情况下插件页会**自动**出现配置表单；只有我要自定义页面时才注册 `plugins.item` / `plugins.bundle.config` / `plugins.row.config`（组件按 `view` 渲染 `summary` 与 `page` 两态）；
> 4. 写读写逻辑：走 `ctx.remote.settings`，**必须**带 `expectedRevision` 做栅栏，并处理 `settings/conflict` 失败重读；
> 5. 告诉我怎么验证「用户改动真的落到了 profile 覆盖值」。
> 约束：不跨插件导入运行时值；命名空间就是 profile 条目 id，不要自造字符串。

## 10.8 ✅ 第 10 章验收清单

- [ ] 我能说清现在的分层模型（继承值 / profile 覆盖值 / 实际值）
- [ ] 我知道**不需要**写 Host 半侧注册代码 —— 表单从 `Config` schema 派生
- [ ] 我能说清 `SettingsScope` / `installSection` / `settings.yaml` **已被移除**，不再照抄老教程
- [ ] 写设置时带了 `expectedRevision`，并会处理 `settings/conflict`
- [ ] 我能在界面里改配置，并确认它生效了

## 10.9 🔴 本区间设置机制改动速查（`0.1.6-alpha.2` → `0.1.7-rc.1`）

| 旧（`0.1.6-alpha.2` 及以前） | 新（`dsh-v0.1.7-rc.1`） | 判据 |
|---|---|---|
| Host 半侧 `ctx.settings.installSection(owner, ns, schema, entry, hooks)` | **移除**；表单从 `Config` schema 自动派生 | 新树源码中已无 `installSection` 定义（旧定义在 `packages/settings/settings/src/index.ts`；该文件已随设置机制重写，**旧行号在新树不可核**） |
| `interface SettingsScope<T>`（`getSnapshot` / `subscribe` / `update(patch)`） | **移除**；改 `SettingsForms` 的 `update` / `replace` / `mutate(ns, …, expectedRevision?)` | 旧定义在 `packages/settings/settings/src/index.ts:115`；新树全树仅存在于 `.agents/notes/archived/` |
| 命名空间 = 插件自选字符串 | 命名空间 = **profile 条目本地 id** | `docs/subsystems/settings.zh.md:9` |
| 用户层落在 `$DSH_HOME/settings.yaml`（热重载） | **移除**；改由**配置编辑器写 Cordis patch**；`settings.yaml` 只剩一次性迁移 `importLegacyDocument()`（成功后改名 `.imported`） | 新 `docs/subsystems/settings.zh.md:5`；`packages/settings/settings/src/index.ts` |
| 写入无并发保护 | **乐观并发**：`expectedRevision` 不匹配抛 `SettingsConflictError`（`code = 'SETTINGS_CONFLICT'`） | 新 `SettingsForms` 源码 |
| 客户端手写卡片族（`card-form.ts` / `fields.tsx` / `*-card-controller.ts` / `BashCard` / `SubagentCard` …） | **整体删除**（−4608 / +73 行）；官方配置页拆为**每插件一个伴生包** | `packages/client/ui-settings-plugins/src/client/` 现只剩 4 个文件 |
| 客户端服务 `settingsScope` + `settings-contract.ts` | **移除**；**取表单改 `ctx.configForms.get<T>(entryId)`**（客户端服务名 `configForms`；`ConfigForms extends Service`），`inject` 里写 `'configForms'`；它底下走 `ctx.remote.settings`（Host `ctx.settingsController`）。方法面基本同名：`getSnapshot()` / `subscribe()` 照旧，旧的 `update(patch)` → **`set(field, value)`** / `unset(field)` / `mutate(ops, expectedRevision?)` | `packages/client/ui-settings/src/client/config-form.ts:241,266,293` + `packages/client/ui-settings/src/client/config-form-types.ts:36-74`；`settings-contract.ts` 已删；用法实证 `packages/client/ui-theme/src/client/index.ts:585,599` |
| （无） | **新增事件** `settings/document-updated`（emit） | `docs/subsystems/settings.zh.md:139-151` |
| （无） | **新增包** `@deepseek-ai/dsh-config-editor`（base 补丁新增 `config-editor` 行） | `packages/boot/config-editor/package.json`；`packages/bundle/base/cordis.patch.yml:97-98` |

---


---

