> **文件来源**：本文件由 DSH 插件开发手册套件整合生成。直接编辑会在下次整合时被覆盖，因此维护性改动记录在工作区源文档中。

> **本文件用途**：术语表、事实来源清单（含「不存在/未证实」的明确清单）、已知的官方文档内部矛盾、以及两套手册各自的诚实边界声明与素材索引。
> **合成来源**：DSH插件开发指导手册.md（附录 D 术语表 + 附录 F 事实来源） + DSH插件开发实战补充-模板与踩坑.md（附录 素材来源与边界）
> **快照警告**：本文件是 DSH 插件知识的**冻结快照**（基线 `dsh-v0.2.2-alpha.2` / commit `f3803c9697`，2026-10-28），其中的**接口名级事实可能已过时**。
> **写代码前先核验**：`bash scripts/dsh-api-probe.sh <DSH 仓库路径>`（退出码 1 = 有 STALE，**不要直接照抄**）。
> **分级与核验规则**：`references/00-version-gate.md`、逐条登记 `references/api-claims.md`。
> **素材名约定**：正文里出现的 `Xxx-yyy.md`（如 `E-official-templates.md`、`B-tools-external.md`）是**生成时的源调研笔记名**，其内容在生成时已合并进本文件——**不是 skill 内的文件**，不必去别处找。

---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 2977-3009 -->

# 附录 D 术语表

> 官方统一译名以 `docs/i18n/terminology.md` 为准。以下是新手最常遇到的。

| 英文 | 中文 | 备注 |
|---|---|---|
| plugin | 插件 | |
| Cordis plugin | Cordis 插件 | 指插件实现 |
| Cordis config entry | Cordis 配置项 | 指 `cordis.yml` 里的一项 |
| fiber | fiber | 保留英文。一个已加载插件实例的运行时句柄 |
| effect | effect | 保留概念。注册的副作用，卸载时自动撤销 |
| dispose | dispose（资源释放） | 卸载并清理 |
| PENDING | PENDING | 已声明但依赖未就绪 |
| capability seam | 能力 seam | **保留英文 seam**，不要译成"接缝" |
| Service Definition | 服务定义 | capability seam 三角色之一 |
| Service Provider | 服务提供方 | 三角色之一 |
| Consumer | 消费方 | 三角色之一，**不要译"消费者"** |
| composition bundle | 组合包 | 你要发布的格式 |
| profile | profile | 用户机器上的具名组装 |
| patch / overlay | patch / overlay | 配置层；`--patch` 指命令行叠加层 |
| hook | 钩子 | |
| HMR | HMR（热模块替换） | 改代码不重启 |
| slot | 插槽 | UI 扩展点 |
| manifest | manifest（元数据清单） | |
| waterfall | waterfall | 保留英文。环绕中间件式事件 |
| regression | 回归 | |
| quality gate | 质量门禁 | |
| artifact | 产物 | **不要译"制品"** |
| stale | 陈旧 | |
| source of truth | 真源 | |

---


---

<!-- ↓ 源：DSH插件开发指导手册.md 区间 3034-3099 -->

# 附录 F 本手册的事实来源

**仓库**：`deepseek-ai/deepseek-harness`
**基线 commit**：`f3803c969748fa190a683e469daa699857e9afe8`（2026-10-28）
**版本**：`dsh-v0.2.2-alpha.2`
**核查日期**：2026-09-11

## F.1 本手册引用的一手来源

| 主题 | 来源文件（相对仓库根） |
|---|---|
| 插件入门 | `docs/user/develop/basic/index.zh.md` |
| 工具开发 | `docs/user/develop/basic/tool.zh.md`、`docs/cookbook/adding-a-tool.zh.md` |
| 插件配置 | `docs/user/develop/basic/config.zh.md`、`docs/cordis-tutorial/05-config.zh.md` |
| 打包发布 | `docs/user/develop/basic/publish.zh.md` |
| Cordis 框架 | `docs/cordis-tutorial/01..07*.zh.md` |
| 生命周期与 effect | `docs/user/develop/framework/index.zh.md`、`docs/cordis-tutorial/02-*.zh.md` |
| 服务与依赖 | `docs/user/develop/framework/service.zh.md`、`docs/cordis-tutorial/03-*.zh.md` |
| 事件 | `docs/user/develop/framework/events.zh.md`、`docs/cordis-tutorial/04-*.zh.md` |
| 工具子系统 | `docs/subsystems/tools.zh.md`、`packages/core/tools/src/schema.ts` |
| 命令子系统 | `docs/subsystems/commands.zh.md`、`packages/interaction/commands/README.zh.md` |
| 终端子系统 | `docs/subsystems/terminal.zh.md`、`packages/terminal/README.zh.md` |
| 插槽与 UI | `docs/subsystems/slots.zh.md`、`client-modules.zh.md`、`docs/cookbook/adding-a-settings-card.zh.md` |
| 设置 | `docs/subsystems/settings.zh.md`、`packages/client/ui-settings/src/client/contract/slots.ts`（⚠️ 旧文常引的 `src/client/settings-contract.ts` 已于 `0.1.7-rc.1` 随整套设置机制重做删除） |
| 架构与 seam | `docs/architecture.zh.md`、`docs/capability-seams.zh.md` |
| CLI 与 profile | `apps/cli/src/args.ts`、`apps/cli/README.zh.md`、`packages/boot/app-boot/src/profile.ts` |
| 环境与路径 | `packages/util/home-paths/src/index.ts` |
| 工程规范 | 根 `AGENTS.md`、`packages/AGENTS.md`、`packages/client/AGENTS.md`、`docs/testing.zh.md` |
| 事故复盘 | `docs/postmortem/0001-*.zh.md`、`0002-*.zh.md` |
| 贡献与分发 | `CONTRIBUTING.zh.md`、`README.zh.md` |
| 术语 | `docs/i18n/terminology.md`、`docs/glossary.zh.md` |

## F.2 已知的文档内部矛盾（本手册已如实标注）

| 矛盾 | 立场 |
|---|---|
| `basic/index.zh.md:56` 说插件路径必须绝对；`basic/config.zh.md:38` 用相对路径 | **以源码为准**：相对路径会被锚定到 patch 文件所在目录（`app-boot/src/index.ts:550-552` + 测试 `user-patches.spec.ts:128`） |
| `docs/cookbook/extension-cookbook.zh.md` 的代码片段 | 文件自述**无法直接复制运行**（省略了 import 与辅助实现） |
| `docs/user/develop/basic/index.zh.md` 展示了对象/类形态用 `export default` | 与 `packages/AGENTS.md:5`「函数插件无 default export」并存；**两形态不要混用** |
| `adding-a-package.zh.md:25` 说 `private: true` 必填 | 源码模板 `packages/core/tools/package.json` **无此字段**（用 `publishConfig.access: public`）；以 `pnpm run constraints` 实际行为为准 |

## F.3 明确「不存在 / 未证实」的清单

- ❌ 官方插件市场 / registry / `dsh plugin search` —— ⚠️ **2026-10-16 收窄**：`dsh-v0.2.1-alpha.4` 起官方确实有了市场**机制**（agent 工具 `plugin_market` / Discover 页 / 插槽 `plugins.tab` / 4 个新包），但**没有官方市场、也没有默认索引源**（索引源属用户数据），`dsh plugin search` 仍不存在
- ❌ `CHANGELOG` / release notes
- ❌ TUI 前端插件（已归档，`packages/ui/` 不存在）
- ❌ `onReady` / `onDispose` 生命周期钩子
- ❌ `--log-level` / `DSH_LOG_LEVEL`
- ❌ 项目级 `cordis.yml` 常量
- ❌ 插件审核 / 白名单
- ❌ 官方仓库接受外部 PR
- ⚠️ `installSection`：**已不适用** —— 该 API 在 `dsh-v0.1.7-rc.1` 被移除（同日移除的还有 `SettingsScope` 与整个手写设置卡片族）。设置机制的权威文档现在是 `docs/subsystems/settings.zh.md`（155 行，本区间被整篇重写；旧版 405 行）
- ⚠️ 面向外部作者的测试脚手架：**未找到**

---

## 结语：给零基础的你的三句话

1. **不要追求"学会写代码"，要追求"学会验证"。** 你的 Agent 会写代码，你要会问「出处呢」「怎么验证」「哪里是猜的」。
2. **小步快跑，每步都要能跑起来。** 第 3 章那 4 行插件就是你全部的信心来源——它跑通了，后面只是加东西。
3. **接受它每周都在变。** 作者官方都说 API pre-stable 了。你基于 `dsh-v0.2.2-alpha.2` 学到的东西，三个月后可能需要微调。**这不是你学得不好，是这个项目就是这个阶段。**

⚛️ 从不可否认的事实出发——你的插件跑起来了，这件事不证自明。




---

<!-- ↓ 源：DSH插件开发实战补充-模板与踩坑.md 区间 1925-2000 -->

# 附录 · 素材来源与边界（**请务必读**）

## A.1 本补充用到的真实仓库（**原列表实为 14 行**，其中 1 个为 AGPL-3.0、已于 2026-09-16 排除 → 现 **13** 个）

| 仓库 | ★ | 本补充用它讲什么 |
|---|---|---|
| `deepseek-ai/deepseek-harness`（官方） | — | **全部官方模板与规范**（完整克隆，70 个插件包） |
| `zhu1090093659/dsh-web` | 7,358 | UI 方向的坑矿（2444 提交 / 1032 次修复 / 245 篇维护者笔记） |
| `omdsh-dev/DSH-better-sidebar` | 3,383 | 侧栏底座与**扩展点设计** |
| `dsh-market/dsh-market` | 3,625 | 设置页可视化插件市场 |
| `Tencent/WeKnora` | 22,166 | **最干净的社区工具插件范本** |
| ~~`volcengine/OpenViking`~~ | — | 🔴 **AGPL-3.0 —— 2026-09-16 起不再引用**（原用途：记忆服务 + 事件钩子） |
| `liustack/modlens` | 1,050 | bundle + client 双声明 |
| `yjh051108/dsh-routing-suite` | 7,162 | 运行时注入 / 事件拦截 |
| `MemTensor/MemOS` | 11,277 | **服务生命周期 + 副作用回收** |
| `huangruiteng/loopx` | 5,785 | 状态内核 / 多方监听 / 生成器清理 |
| `tt-a1i/archify` | 57,636 | 完整包结构 / bundle-only 形态 |
| `Q00/ouroboros` | 5,805 | **零代码组合包黄金范本** |
| `anywhere-labs/dsh-desktop` | 25,403 | 桌面宿主 / 进程与生命周期 |
| `xiaobright/dsh-anchored-standard` | — | 工程规范化 / 构建校验 |

## A.2 原始素材索引（十份，共约 7,400 行）

> ⚠️ **下表是「生成期素材代号」，不是本 skill 的文件，也不随本 skill 发布。**
> 素材 A~J 在生成本套 references 时**已被合并**并落位到下表「已并入」一列；正文各处的「来源：素材 B 坑 M1」只是在标注**该结论的证据来源**，
> 不是让你去打开某个文件——**在技能目录里找不到它们，这是设计如此，不是缺失。**

| 素材 | 内容 | 原行数 | 已并入 |
|---|---|---|---|
| **A** | UI 方向坑点 | 1445 | `10a-casebook-ui.md`（原 `10-community-casebook.md`，2026-09-14 拆册） |
| **B** | 工具 / 外部调用（52 坑 + 4 模板 + 10 规范） | 2273 | `10b-casebook-tools.md`；另经实战补充并入 `02-templates.md`、`05-pitfalls.md` |
| **C** | 服务 / 记忆 / 状态内核（19 坑 + 14 模板） | 1517 | `10c-casebook-services.md` |
| **D** | 宿主 / 桌面 / 组合包（32 坑 + 4 模板） | 1189 | `10d-casebook-host-bundle.md` |
| **E** | 官方 7 类模板 + 插槽名提取（当时 40 个，⚠️ 非全量 —— 对基线重新抽取为**约 106 个公开键**（2026-09-23 修好抽取器漏抽后；**2026-09-25 随 `rc.2` 推进 +3**；**2026-09-30 随 `0.2.0-rc.2` 推进 +1**；**2026-10-04 随 `0.2.1-alpha.1` 推进 +2**；**2026-10-09 随 `0.2.1-alpha.2` 推进 +2**（`slot-catalog.ts` `92 → 94`）；**2026-10-15 随 `0.2.1-alpha.3` 推进 +5 / −1**（`slot-catalog.ts` `94 → 98`）；**2026-10-16 随 `0.2.1-alpha.4` 推进 +1 / −0**（`slot-catalog.ts` **98 → 99**；新增键 `plugins.tab`）；**2026-10-17 随 `0.2.1-rc.2` 推进 +1 / −0**（`slot-catalog.ts` **99 → 100**；新增键 `conversation.input.model.label`）；**2026-10-24 随 `0.2.1-rc.3` 推进 +3 / −0**（`slot-catalog.ts` **100 → 103**；新增键 `sidebar.panellist.actions` / `conversation.session.header.views.actions` / `sidebar.right.tab.guide.actions`，三者均为 `list` / `scope: 'root'`，是左侧面板 / Conversation View 标签行 / 右栏 Guide 的 **More 菜单行**）；**2026-10-29 随 `0.2.2-alpha.2` 推进 +3 / −0**（`slot-catalog.ts` **103 → 106**；新增键 `conversation.chat.text-interaction` / `conversation.chat.user.before` / `sidebar.session.row.trailing`）；旧记 约 81 系低估），见 `api-claims.md` §三） | 1044 | `02b-official-templates.md`（原 `02-templates.md` 附录 E，2026-09-14 拆册） |
| **F** | 官方 4 篇事故复盘 | 195 | `05-pitfalls.md` 附录 |
| **G** | 安装 / CLI 机制逐字实证 | 254 | `06-workflow.md` 第 G 篇 |
| **H** | ouroboros 零代码组合包全文 | 231 | `02c-community-bundle.md`（原 `02-templates.md` 附录 H） |
| **I** | 速查表（服务 / 事件 / 插槽 / 命令） | 187 | `08-cheatsheet.md` |
| **J** | 官方包工程约定 | 143 | `07-conventions.md` 第 J 篇 |

> **2026-09-14 拆册说明**：素材 A~D 原本全部塞在 `10-community-casebook.md`（6.6k 行 / 7.9 万词，
> 单文件远超「<5K 词」实务指引），E/H 原本追加在 `02-templates.md` 尾部。现按**来源**拆成 6 个独立分册
> （`10a`~`10d`、`02b`、`02c`），正文为**逐行搬迁、未改写**（**⚠️ 例外：`10b-casebook-tools.md` 已于 2026-09-15 / 09-16 因许可整改被定点改写两轮，不再是逐行搬迁**）；`10-community-casebook.md` 转为**总索引**，
> `02-templates.md` 只留 T1~T12 整理稿。**原文件名全部保留，零删除。**

另有两份**源手册**（同样不随本 skill 发布）也是本套 references 的合成来源：《DSH 插件开发指导手册》与《DSH 插件开发实战补充：模板库·踩坑百科》。各 reference 文件头的「合成来源」行写明了每一篇由谁合成。

> **坑点总量**：四个方向合计 **约 130 条**有 commit 或源码实证的坑/教训（A 100+ / B 52 / C 19 / D 32，部分重叠）。本套 references 精选了其中 **23 条最高频、最致命**的整理成症状索引（见 `05-pitfalls.md`）。

**社区仓库快照与 git 历史**（13 个仓库，**不随本 skill 发布**）：生成期曾在本地以 `<工作区>/src/<仓库>/`（完整源码）与 `<工作区>/repos/<仓库>/`（提交历史）两处存放。
⚠️ 后者是**部分克隆**，**无文件 blob**：`git log` / `ls-tree` 可用，`git show <hash>:<path>` 会报 bad object。`10a`~`10d` 里的「快照路径」行即指这批素材。

## A.3 ⚠️ 三条诚实声明

**1. 一处主动校正（与原始素材不一致，以本文件为准）**

`A~D` 四份素材中，有多处出现过这样的结论：**「工具 `parameters` 属性级不能写 `required` 键，必须用对象级 `required` 数组」**。

**这个结论只对一半。** 官方源码实证（`packages/core/tools/src/schema.ts`）：
- 走 **`defineTool()`** 时，`parameters` 是 **DSH 作者 DSL**，必填**必须**写**属性级** `required: true`；
- 走 **裸 `ctx.tools.register()`** 时，`parameters` 是**原始 JSON Schema**，必填写**对象级** `required: ['a']`。

本文件 **T3 §3.2** 与 **坑 P7** 已给出源码级证据。素材 B 中相关段落已就地加上校正说明。

**2. 官方文档本身存在矛盾的地方**（已按源码为准处理）

| 争议点 | 官方文档说 | 源码实证 | 本文件立场 |
|---|---|---|---|
| 补丁里插件路径能否用相对路径 | `user/develop/basic/index.zh.md:56` 说「必须是绝对路径」 | `app-boot/src/index.ts` 的 `anchorInsertedPluginNames()` 把相对路径锚到补丁文件旁（有单测固定） | **以源码为准**：可以用相对路径；但第三方插件建议用包名 |
| `!!js` 在 `disabled` 上是否求值 | 复盘 0002 描述的是「不求值」的旧行为 | 当前官方 `bundle/base` 补丁在用 `disabled: !!js ...` | **当前版本支持**；解释见素材 F 的 0002 版本注记（原文已并入 `05-pitfalls.md`） |

**3. 素材的历史边界**

素材 A 的部分章节写于「部分克隆导致源码 blob 不可用」的阶段，因此它对**社区 UI 插件的源码正文**标注了「未找到（blob 不可用）」，只有提交信息、维护者笔记与目录树三类证据。

**该缺口现已闭合**：13 个仓库的**完整源码快照**在生成期已下载并用于复核，且 **T8/T9 两节给出的 UI 模板全部来自官方仓库的逐字源码**（`ui-brand-official`、`ui-theme`），可直接照抄。

---

## A.4 下一步建议

1. **试水**：按 **T1** 做一个零代码组合包（30 分钟内可见成果，且不用配前端工具链）。
2. **进阶**：按 **T3** 做一个工具插件（这是用得最多的形态）。
3. **上界面**：按 **T8/T9** 做 UI 与设置卡片（需要先跑通 `pnpm install`）。
4. **长期**：把本文件的 **第五篇** 提示词存成片段，每次让 AI 写 DSH 代码时先贴上"铁律：要求出处"。

> ⚠️ **最后一条风险提示**：本文件基线是 commit `f3803c9697`（`dsh-v0.2.2-alpha.2`，2026-10-28）。DSH 自称 pre-stable、tag 间隔中位数约 1.1 天且有过破坏性变更。**升级前先跑 `git log --grep='!'` 评估影响**，并把 `package.json` 的 `peerDependencies` 写成**区间**而非钉死某个 rc 号。⚠️ 另注：若你还声明了 **`engines.dsh`**，自 `dsh-v0.2.1-alpha.4` 起**只有它决定兼容性**（DSH peer 范围**不再**放宽或收窄它，写 `workspace:` 即判不兼容）→ 要么给它完整范围，要么**不写**、退回 peer 检查（见 `07-conventions.md` §2）。

---

