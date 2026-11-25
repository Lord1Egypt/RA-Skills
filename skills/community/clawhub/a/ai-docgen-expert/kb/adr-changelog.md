---
subdomain: adr-changelog
version: 2
updated: 2026-11-17
---

# ADR 与 Changelog：决策记录与变更日志

## 定位与心智模型

本子域覆盖四类「记录性文档」的生成与维护：ADR（为什么这么决定）、changelog（用户可见地变了什么）、commit message（这次提交做了什么）、release notes（这次发布讲什么故事）。四者分工不同，混用任两种都会导致信息错位。

核心二分——**活文档 vs 追加型历史**（本子域最重要的一条心智边界）：

- **changelog 是活文档**：官方 FAQ 明确 "Should you ever rewrite a changelog? **Sure.**"——补漏条目、补 breaking change 记录、改进措辞均为正当操作（补漏 ≠ 篡改，修订须诚实）。[官方文档](https://keepachangelog.com/en/1.1.0/)
- **ADR 是追加型历史**：只追加不改写；推翻决策 = 新 ADR supersede + 旧 ADR 仅改状态行。改写历史条目等于摧毁决策记录的全部价值。[官方文档](https://adr.github.io) / [模型经验]

把 changelog 当不可动的碑文（该补不补），或把 ADR 当可重写的文档站内容（历史失真），是本子域最深的两种心智错误。

记录载体分工 [模型经验]（归纳自业界实践，各团队流程变体大，使用时按团队流程裁剪）：

| 载体 | 职责 | 时间性 |
|---|---|---|
| ADR | 为什么（决策 + 备选 + 后果） | 永久（只追加） |
| issue | 什么还没做 | 会关闭 |
| PR/commit | 做了什么 | 永久（diff） |
| changelog | 用户可见的变化 | 每版本（活文档，可诚实修订） |
| 文档站 | 怎么用 | 演进（可重写） |

适用边界：ADR 与 changelog 格式稳定、版本敏感性低；Conventional Commits 1.0.0 已官方锚定（见「来源索引」第 2 轮新增）；release notes 结构无权威规范（业界惯例归纳）。

## 法则

**AC-1 ADR 四段底线：状态/上下文/决策/后果。** 状态机生命周期显式（proposed → accepted → superseded/deprecated，双向链）；上下文陈述事实不夹预设立场；决策短而确定（第一人称主动语态）；负后果必写（ADR 的诚实度指标）。
- 违反后果: 上下文夹立场→决策预设立场污染记录；负后果缺失→历史记录变宣传材料，未来 superseding 时重踩旧坑。
- 溯源: [官方文档](https://adr.github.io/adr-templates/)（Nygard 模板 title/status/context/decision/consequences 官方确认）；01-adr-structure 萃取。

**AC-2 ADR 在决策窗口期落纸。** 讨论时建 proposed，定稿改 accepted；会后 24h 内落纸；事后补写的 ADR 是辩护文不是记录——上下文（forces）新鲜度是价值的一半。
- 违反后果: 上下文已被结果污染，「为什么」退化为「辩护」，决策记录丧失可追溯性。
- 溯源: [模型经验]（02-decision-timing-granularity 萃取）。

**AC-3 一个 ADR = 一个可独立推翻的决策。** 难撤销/跨模块影响/会被重提/踩坑换来/外部强制的决策才值得 ADR；粒度判据是「能否被独立 supersede」；重大 rejected 备选独立成篇（负知识与正知识同样贵）。
- 违反后果: 粒度过粗→一篇记录无法被单独推翻，维护僵死；粒度过细→信噪比崩塌，团队弃用 ADR 实践。
- 溯源: [模型经验]（02 萃取）。

**AC-4 决策记录是追加型历史，永不在原地改写（适用域：ADR）。** 推翻决策 = 新建 ADR supersede + 旧 ADR 仅改状态行（superseded by NNNN）+ 双向链；历史条目保持历史准确。注意：本条仅限 ADR——changelog 是活文档，可诚实修订（见「定位与心智模型」二分）。
- 违反后果: 原地改写历史决策 = 摧毁决策史，团队失去「当初为什么」的全部证据。
- 溯源: [模型经验]（01、06 萃取）；适用域校准依据 [官方文档](https://keepachangelog.com/en/1.1.0/)（FAQ "Sure." 反向印证 changelog 侧不适用本条），详见「冲突消解记录」#2。

**AC-5 [GLOBAL] AI 生成决策记录的角色是结构师+提问者，不是决策代笔。** 结构（模板/类目/段落）可生成；事实（forces/决策/备选对比/后果）是项目私有，无输入时只能产出模板 + 引导提问（「什么约束驱动这个决策？备选考虑过谁？」）。
- 违反后果: 无输入生成完整 ADR → 上下文、备选、决策全是合理想象，编造的项目「事实」进入仓库即污染决策史。
- 溯源: [模型经验]（06-ai-adr-changelog-mistakes 自省层）。GLOBAL 理由：「结构与事实分离」是蒸馏域共享的生成纪律（与 AD-2/CC-2 同族）。

**AC-6 changelog 面向使用者，过滤「用户可见」。** commit 复读是官方点名的反模式；一条一行、动词开头；类型分类用 Keep a Changelog 官方六类目：Added / Changed / Deprecated / Removed / Fixed / Security；`chore`/内部重构过滤。
- 违反后果: git log 复读→用户无法得知与自己何干；自创类目（如 `Improved`）→偏离官方规范，读者与工具均无法按预期解析。
- 溯源: [官方文档](https://keepachangelog.com/en/1.1.0/)（六类目与 "Commit log diffs" 坏实践官方确认）；03-changelog-format 萃取。原「五类 + Security 惯例」认知已修正，见「冲突消解记录」#1。

**AC-7 changelog 滚动维护：Unreleased 常驻。** 合并时即写、不发版日突击；Unreleased 官方双用途：预告下版本内容 + 发版时整体迁移为新版本节；发版 = Unreleased 清空改名 + ISO 8601 日期 + 新建 Unreleased；Breaking change 显式 `**BREAKING**` 标注 + 迁移指引链接。
- 违反后果: 发版日突击补写→条目遗漏；日期格式混乱→官方点名坏实践 "Confusing Dates"。
- 溯源: [官方文档](https://keepachangelog.com/en/1.1.0/)（Unreleased 双用途、ISO 8601）；03 萃取。

**AC-8 commit 规范的意义是机器可解析，不是审美。** Conventional Commits type/scope/BREAKING 标记驱动 SemVer 推导与 changelog 自动化；subject 祈使句 ≤50 字符、不加句号；原子提交（一次一个逻辑变更）；规范必须工具强制（commitlint + git hook），靠自觉必然溃败。
- 违反后果: BREAKING 不标→下游按 patch 升级爆炸，自动化链全部失真；规范无工具强制→六个月后形同虚设。
- 溯源: [官方文档](https://conventionalcommits.org/en/v1.0.0/)（1.0.0 规格：feat/fix/BREAKING CHANGE 与 SemVer 对应、`!` 标记与 footer 语法、BREAKING CHANGE 全大写为唯一大小写敏感项）+ [模型经验]（04-commit-conventions 萃取；subject 长度、原子提交与工具强制为实践层）。

**AC-9 追溯链完整：commit ↔ issue ↔ changelog ↔ release 不脱钩。** `Closes #N` / `Refs #N` 不省略；Deprecated 宣告的移除版本到期必须出现在 Removed（废弃→移除两步走，官方点名坏实践 "Ignoring Deprecations"）。
- 违反后果: 追溯断链→「为什么否了没人记得」，重评估花一周得出同样结论；升级断裂——用户按废弃承诺升级时踩空。
- 溯源: [官方文档](https://keepachangelog.com/en/1.1.0/)（Ignoring Deprecations）+ [模型经验]（03、04、06 萃取）。

**AC-10 release notes ≠ changelog 复读。** 一句话版本主题 + ≤3 条用户价值语言亮点 + 破坏性变更置顶 + 升级指引；受众更广（含潜在用户）；CHANGELOG.md 为 SSOT，发布页自动从其生成或明确单份维护。
- 违反后果: notes = changelog 搬运→无亮点提炼；双份人工维护→必然漂移（官方对 GitHub Releases 的评价：非便携 changelog，仅 GitHub 上下文显示）。
- 溯源: [官方文档](https://keepachangelog.com/en/1.1.0/)（GitHub Releases 评价）+ [模型经验]（05-release-notes 萃取）。

**AC-11 [GLOBAL] 追溯类元数据零编造。** 版本号/发布日期/issue 号/PR 号/贡献者/性能数字是事实数据，无源不写；时间线纪律：只录已发生，「计划做」不进 changelog。
- 违反后果: 编造的版本号、日期、致谢名单进入正式记录→事实数据被污染，后续所有基于它的自动化与信任坍塌。
- 溯源: [模型经验]（06 自省层）。GLOBAL 理由：与 DT-12/AD-2/CC-2 同族（编造零容忍）——追溯数据版。

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| ADR | Architecture Decision Record：一条架构决策的永久记录（上下文/决策/后果），只追加不改写。[官方文档](https://adr.github.io) |
| decision log | ADR 的集合体；ADR 组织三目标：词汇统一 / 工具强化 / AKM 知识指针。[官方文档](https://adr.github.io) |
| Nygard 模板 | 经典 ADR 格式：title / status / context / decision / consequences。[官方文档](https://adr.github.io/adr-templates/) |
| MADR | Markdown ADR 模板族；核心是 considered options + pros/cons；元数据为 YAML front matter（status/date/decision-makers/consulted/informed 等）。版本：3.0.0（2022-10-09，正负后果合并为 Consequences）→ 4.0.0（2024-09-17 当前最新）。[官方文档](https://adr.github.io/adr-templates/) / [官方文档](https://adr.github.io/madr/) |
| Y-Statement | 单句式 ADR：context / facing / decided / neglected / achieving / accepting / because。[官方文档](https://adr.github.io/adr-templates/) |
| supersede | 推翻决策的正规路径：新 ADR 指回旧 ADR，旧 ADR 状态改 `superseded by NNNN`（双向链）。[模型经验] |
| Keep a Changelog (KaC) | changelog 维护规范，当前 1.1.0；七原则 + 官方六类目 + 坏实践清单。[官方文档](https://keepachangelog.com/en/1.1.0/) |
| Unreleased | changelog 顶部滚动节；官方双用途：预告下版本 + 发版时迁移为新版本节。[官方文档](https://keepachangelog.com/en/1.1.0/) |
| [YANKED] | 撤回发布的版本标记，格式：`## [0.0.5] - 2014-12-13 [YANKED]`——响亮标记 + 程序可解析。[官方文档](https://keepachangelog.com/en/1.1.0/) |
| SemVer | Semantic Versioning 2.0.0；KaC 官方原则要求 changelog 声明是否遵循。[官方文档](https://keepachangelog.com/en/1.1.0/) |
| Conventional Commits | commit message 规范（当前 1.0.0）：`<type>(<scope>): <description>` + 可选 body/footers；feat→MINOR、fix→PATCH、BREAKING CHANGE→MAJOR 驱动版本推导与 changelog 自动化。[官方文档](https://conventionalcommits.org/en/v1.0.0/) |
| breaking change | 破坏性变更：changelog 中 `**BREAKING**` 显式标注 + 迁移指引；commit 中 `!` 后缀或 footer `BREAKING CHANGE:`。[模型经验] |
| release notes | 单次发布快照，受众含潜在用户；可带叙事亮点；无官方结构标准（业界惯例）。[模型经验] |

KaC 官方七原则 [官方文档](https://keepachangelog.com/en/1.1.0/)：

| # | 原则 | 一句话展开 |
|---|---|---|
| 1 | for humans, not tools | changelog 给人读，机器可读是副产品 |
| 2 | 每个版本都有对应条目 | 任何版本不应无记录地溜走 |
| 3 | 同类变更分组 | 官方六类目组织，不平铺时间线 |
| 4 | 每个版本可链接 | 版本节锚链到版本对比 |
| 5 | 最新版本在最前 | 倒序排列 |
| 6 | 显示发布日期 | 且用 ISO 8601 格式 |
| 7 | 声明是否遵循 SemVer | changelog 顶部声明行在位 |

KaC 官方坏实践四则 [官方文档](https://keepachangelog.com/en/1.1.0/)：

| 坏实践 | 官方立场 | 对应法则 |
|---|---|---|
| Commit log diffs | commit 复读是噪音——反 git log 复读 | [AC-6] |
| Ignoring Deprecations | 废弃是移除的前置警告——两步走防升级断裂 | [AC-9] |
| Confusing Dates | 日期格式必须统一 ISO 8601 | [AC-7] |
| Inconsistent Changes | **部分维护的 changelog 与没有一样危险**——SSOT 期望 | [AC-7] |

## 最佳实践

### 场景 1：写一篇新 ADR

推荐路径（源于 [AC-1] [AC-2] [AC-3]）：
1. 判定是否值得 ADR：满足「难撤销/跨模块/会被重提/踩坑换来/外部强制」任一才立项。
2. 决策窗口期内动手：讨论期建 `Status: proposed`，讨论结论直接更新为 `accepted`——ADR 是讨论锚点，不是事后追认。
3. 四段落笔：上下文只写 forces（事实，不夹立场）→ 决策短而确定（第一人称）→ 后果正/负/中性三分类全列 → 列 2~3 个公允备选 + 否决理由。
4. 元数据补全：编号、日期、决策人——全部真实事实。

do/don't：

```markdown
✗ Context: Redis 明显不行，所以我们选 Memcached。
✓ Context: 当前会话存储 QPS 峰值 3k，单实例内存 4GB；团队已有 Memcached 运维经验。

✗ Consequences: 提升性能，架构更优。
✓ Consequences: 获得：会话读写延迟 P99 下降（预期）。
   代价：新增运维组件；冷启动缓存穿透风险——我们接受，因为延迟是当前 P0。

✗ Decision: 可以考虑采用 Memcached。
✓ Decision: 我们采用 Memcached 作为会话存储。
```

边界条件：RFC 先行文化的团队可在 ADR 前走 RFC 提议讨论（ADR 记「已决」，RFC 记「提议中」，流程不得混用）。[模型经验]

### 场景 2：推翻既有决策（supersede 流程）

推荐路径（源于 [AC-4]）：
1. 新建 ADR，编号只增不改，状态行写 `supersedes NNNN`。
2. 旧 ADR 仅改状态行为 `superseded by NNNN`——其余内容一字不动。
3. 旧 ADR 的负后果段是新 ADR 上下文的起点：当初接受了什么代价、现在为什么不再接受。

do/don't：

```markdown
✗ 打开 ADR-0007，把「采用 Memcached」改成「采用 Redis」。
✓ 新建 ADR-0021（supersedes 0007）；ADR-0007 状态行改为：
   Status: superseded by 0021
```

边界条件：changelog 不适用本流程（活文档可修订）；文档站教程更不适用（可整体重写）。二分判据见「定位与心智模型」。

### 场景 3：AI 辅助产出 ADR（结构师 + 提问者）

推荐路径（源于 [AC-5] [AC-11]）：
1. 无事实输入时只产出两样：模板骨架 + 引导式提问清单（forces？备选？决策人？）。
2. 有输入时（会议记录/讨论摘要/diff）做「结构化转译」：把散落信息填入四段，不补全未提及的事实。
3. 显式标注空缺：元数据（决策人/日期）缺失就留 `TODO(需人工确认)`，不编造。
4. 备选公允性检查：备选不得稻草人化（列弱备选衬托主选）。

do/don't：

```markdown
✗ 输入「帮我们写个 ADR：用 Redis」→ 输出完整 accepted ADR（约束/备选全编）。
✓ 输出 MADR 骨架 + 提问：
   - Context: 什么约束驱动这个决策？（QPS？数据量？团队经验？）
   - Considered options: 除 Redis 外考虑过谁？各自为何否决？
   - Status: 这是提议还是已决？
```

边界条件：用户提供了真实决策材料时，AI 可完整成文——但每条事实须可追溯到输入材料。

### 场景 4：滚动维护 CHANGELOG.md（合并 → 发版全流程）

推荐路径（源于 [AC-6] [AC-7] [AC-9]）：
1. 建文件：项目根 `CHANGELOG.md`，顶部声明遵循 Keep a Changelog 1.1.0 与 SemVer。
2. 每次合并过「用户可见」过滤后写入 `## [Unreleased]` 对应类目（合并时即写，不发版日突击）。
3. 发版：Unreleased 整体迁移为新版本节 + ISO 8601 日期 + 新建空 Unreleased；底部补版本对比链接。
4. Breaking change 双保险：`**BREAKING**` 标注 + 迁移指引链接 + 版本号按 SemVer 升 major。

do/don't：

```markdown
✗ - chore: update deps
✗ - refactor: extract hook
✓ ### Changed
   - useKeyboard hook 现在要求 React ≥18（#421）
```

过滤判据：**这条变更改变用户可观察行为/接口吗？** 否 → 不进 changelog。官方七原则之一即「changelog for humans, not tools」。[官方文档](https://keepachangelog.com/en/1.1.0/)

边界条件：纯内部版本（无用户可见变化）允许空 changelog，诚实优于凑条目。

### 场景 5：废弃 → 移除两步走（deprecation 流程）

推荐路径（源于 [AC-9]，官方坏实践 "Ignoring Deprecations" 背书）：
1. 第一步：当版 changelog 记 `Deprecated`，显式宣告移除版本（「将于 v3.0 移除」）。
2. 中间版本保持宣告不动。
3. 第二步：宣告的版本到期，记 `Removed`——Deprecated 与 Removed 必须联动。
4. 同步 API 文档的 deprecation 标记与迁移指引（跨子域联动，见「与其他子领域的集成要点」）。

边界条件：紧急安全移除可一步走，但须在 `Security` 类目说明跳过废弃期的原因。

### 场景 6：Conventional Commits + 工具强制

推荐路径（源于 [AC-8]）：
1. 采用 `feat / fix / refactor / ...`（scope 可选）+ subject 祈使句 ≤50 字符。
2. BREAKING 用 `!` 后缀或 footer `BREAKING CHANGE:` 两种官方写法之一。
3. commitlint + git hook（husky 或原生 hook）拦截 + CI 校验——规范不配工具等于没有。

do/don't：

```text
✗ feat: change config format（breaking 未标）
✓ feat(config)!: switch to flat config format
  BREAKING CHANGE: 配置格式由嵌套改为扁平，迁移见 docs/migrate

✗ update（意义不明）
✓ fix(timer): resolve drift after tab suspend
```

边界条件：原子单位是「逻辑变更」不是「文件」——拆分建议不得过细到每文件一提交。[模型经验]

### 场景 7：撰写 release notes

推荐路径（源于 [AC-10]，结构为业界惯例归纳、无官方标准）：
1. 一句话版本主题（无主题的常规版本允许「例行修复版」定位，诚实优于包装）。
2. 亮点 ≤3 条，用户价值语言（做「价值翻译」：`重构状态层` → `大列表滚动帧率提升约 40%`——数字须有源）。
3. 破坏性变更紧跟标题置顶，不按类目字母序埋底。
4. 升级指引一行命令 + 注意事项。
5. 分发策略：以 CHANGELOG.md 为 SSOT，发布页自动生成或明确只维护一份——官方评价 GitHub Releases 为「非便携 changelog」（仅 GitHub 上下文显示）。[官方文档](https://keepachangelog.com/en/1.1.0/)

## 高频坑点（速查）

### 深度展开 Top 2

**Top 1：changelog = git log 复读**（违反 [AC-6]）
- 症状：条目是 `- chore: update deps` / `- refactor: extract hook`，用户无法得知与自己何干。
- 根因：把 changelog 当「提交记录的人类可读版」而非「用户可见变化日志」；官方坏实践 "Commit log diffs" 点名（"Commit log diffs… are just noise"）。
- 代码对照：

```markdown
✗ ## [1.4.0] - 2026-08-15
   - chore: update deps
   - refactor: extract hook
✓ ## [1.4.0] - 2026-08-15
   ### Changed
   - useKeyboard hook 现在要求 React ≥18（#421）
   ### Fixed
   - 修复 Timer 在后台标签页暂停累计漂移（#435）
```

- 修复：每条过「用户可见」过滤判据；chore/内部重构/格式化一律滤除。

**Top 2：ADR 历史改写**（违反 [AC-4]）
- 症状：「更新 ADR-0007」时把原决策内容改成新决策——历史被摧毁。
- 根因：把 ADR 当「活文档」（文档站思维）而非「追加型历史」（记录思维）。
- 代码对照：

```markdown
✗ ADR-0007 原文「我们采用 Memcached」被改为「我们采用 Redis」
✓ ADR-0021: Status: accepted（supersedes 0007）
   ADR-0007: Status: superseded by 0021（其余一字不动）
```

- 修复：改写冲动出现时强制走 supersede 流程（场景 2）；注意 changelog 不适用此限制（活文档可修订）。

### 速查表

| 症状 | 根因 | 修复 | 法则 |
|---|---|---|---|
| ADR 上下文夹「X 明显不行，所以…」 | 上下文夹决策预设立场 | Context 只写 forces 事实，立场归 Decision | AC-1 |
| ADR 后果段清一色正面 | 面向「证明正确」而非「记录决策」 | 正/负/中性三分类强制，负后果必写 | AC-1 |
| 决策段写墙（3 屏论证） | 论证误入决策段 | 论证归上下文/备选分析；决策短而确定 | AC-1 |
| `Status: accepted` 但项目早已绕开该决策 | 状态机不维护，写完即终 | 推翻即建新 ADR + 旧 ADR 改状态行 | AC-1, AC-4 |
| 备选全是弱者衬托主选 | 备选稻草人化（AI 尤甚） | 备选公允，列 2~3 个真实考虑过的选项 | AC-1, AC-5 |
| 重构完才「补个 ADR」 | 事后补写，上下文已失真 | 决策窗口期建 proposed，24h 内落纸 | AC-2 |
| 状态管理选型+目录结构+错误处理挤一篇 | 粒度过粗 | 一个 ADR = 一个可独立推翻的决策，拆分 | AC-3 |
| 每个小决策都写 ADR，团队弃用 | 粒度过细，信噪比崩塌 | 五判据任一满足才立项；小决策归 commit | AC-3 |
| 无输入生成完整 ADR（forces/备选全编） | AI 决策代笔角色混淆 | 只产出模板 + 引导提问 | AC-5 |
| changelog 条目无类目平铺 | 类型分类缺失 | KaC 官方六类目分组 | AC-6 |
| 自创 `Improved` 类目 | 结构幻觉，偏离官方规范 | 类目以 keepachangelog.com 官方六类为准 | AC-6 |
| 发版日突击补写、条目遗漏 | Unreleased 滚动纪律缺失 | 合并时即写，Unreleased 常驻 | AC-7 |
| Unreleased 出现「计划支持 X」 | 时间线倒置，changelog 变路线图 | 只录已合并；规划归 roadmap | AC-7, AC-11 |
| breaking 藏在 Changed 里无标注 | SemVer 意识薄弱 | `**BREAKING**` + 迁移指引 + 升 major | AC-7 |
| 日期格式混乱（8/15/26 与 2026-08-15 混用） | 官方坏实践 "Confusing Dates" | 统一 ISO 8601 | AC-7, AC-11 |
| commit `feat: change config format`（breaking 未标） | `!` 标记缺失 | `feat(config)!:` 或 footer `BREAKING CHANGE:` | AC-8 |
| 一次提交 5000 行混多事 | 提交巨石，非原子提交 | 按逻辑变更拆分原子序列 | AC-8 |
| 规范写在 CONTRIBUTING 里六个月形同虚设 | 无工具强制，靠自觉衰减 | commitlint + hook + CI 拦截 | AC-8 |
| 废弃时宣告的移除版本到期没记 Removed | Deprecated/Removed 不联动 | 废弃→移除两步走，到期必记 | AC-9 |
| `Closes #123` 但 issue 不存在 | 追溯链幻觉（AI 高发） | issue 号来自真实数据，无源不写 | AC-9, AC-11 |
| CHANGELOG.md 与 GitHub Releases 一新一旧 | 双份人工维护漂移 | CHANGELOG.md 为 SSOT，发布页自动生成 | AC-10 |
| release notes 无亮点提炼、无升级指引 | changelog 复读 | 主题 + ≤3 亮点 + breaking 置顶 + 升级指引 | AC-10 |
| 亮点写「重构了状态层」 | 内部视角，价值未翻译 | 用户价值语言，数字须有源 | AC-10, AC-11 |
| 编造版本号/发布日期/贡献者/性能数字 | 元数据编造（AI 最高危错误族） | 无源不写；元数据留 TODO 待人工确认 | AC-11 |
| 新 ADR 标 supersede 但旧 ADR 状态未更新 | supersede 链断裂 | 双向链：新指回旧，旧改状态行 | AC-4 |

## API 速查表

### KaC 官方六类目 + 适用判定表 [官方文档](https://keepachangelog.com/en/1.1.0/)

| 类目 | 适用判定（这条变更…） | 示例 |
|---|---|---|
| `Added` | 新增用户可见的功能/能力 | 支持嵌套路由配置（#421） |
| `Changed` | 既有行为变更（非修复、非破坏） | 默认主题切换为 dark |
| `Deprecated` | 宣告即将移除（还在，但将删） | legacyAdapter() 将于 v3.0 移除 |
| `Removed` | 移除此前已废弃的能力 | 移除 legacyAdapter()（v2 已宣告废弃） |
| `Fixed` | 缺陷修复（行为回归正确） | 修复 Timer 后台标签页暂停漂移 |
| `Security` | 安全漏洞修复（即使影响行为也单列，不混入 Fixed） | 修复 markdown 渲染 XSS |

### ADR 三模板字段对照表 [官方文档](https://adr.github.io/adr-templates/)

| 字段（行） | MADR | Nygard | Y-Statement |
|---|---|---|---|
| 标题 | `# Title`（决策一句话） | Title | —（单句成文） |
| 状态 | Status（YAML front matter 可选元数据；官方示例枚举 proposed/rejected/accepted/deprecated/superseded by ADR-NNNN，省略号显式——开放集） | Status（proposed/accepted/…） | — |
| 元数据 | Date / decision makers / confirmation（官方元数据三件） | —（无强制元数据） | — |
| 上下文 | Context and Problem Statement + Decision Drivers | Context（forces，事实不夹立场） | "In the context of… facing…" |
| 备选方案 | Considered Options + Pros/Cons（MADR 核心） | （无专段，融入 Context/Decision） | "neglected…"（被放弃项） |
| 决策 | Decision Outcome（chosen option + consequences） | Decision（第一人称，短而确定） | "we decided…" |
| 理由 | Pros/Cons 与 Outcome 表达 | 融入 Context/Decision | "because…" |
| 后果 | positive / negative consequences（正负分列） | Consequences（正/负/中性全列） | "achieving… accepting…" |
| 变体 | full / minimal 双模板 | 经典四段（AC-1 底线即此四段） | 单句式，适合高频轻量决策 |

### changelog 条目格式模板 [官方文档](https://keepachangelog.com/en/1.1.0/)

```markdown
# Changelog

本项目所有重要变更记录于此。
格式基于 Keep a Changelog，版本遵循 Semantic Versioning。

## [Unreleased]
### Added
- 支持嵌套路由配置（#421）

## [1.4.0] - 2026-08-15
### Changed
- **BREAKING**: useKeyboard 现在要求 React ≥18，迁移指南 → /docs/migrate/v15（#402）
### Fixed
- 修复 Timer 在后台标签页的累计漂移（#435）

## [0.0.5] - 2014-12-13 [YANKED]

[Unreleased]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.2...HEAD
[1.1.2]: https://github.com/olivierlacan/keep-a-changelog/compare/v1.1.1...v1.1.2
（链接引用两行为 KaC 官方页脚原文；本项目落地时替换为自身 org/repo 与 tag）
```

格式要点：
- 版本节：`## [版本号] - ISO 8601 日期`；最新版本在最前。
- `[YANKED]`：撤回发布的版本，标记写在日期后——响亮可读 + 程序可解析。
- 底部链接引用：每个版本节锚链到版本对比（GitHub compare 链接），保证「版本可链接」原则——示例引用取官方页脚原文，本项目替换为自身 repo/tag。
- 顶部声明：遵循 Keep a Changelog 与 SemVer（官方原则「Mention whether you follow Semantic Versioning」）。

### Conventional Commits 骨架 [官方文档](https://conventionalcommits.org/en/v1.0.0/)

```text
<type>(<scope>)!: <description>   # ! = BREAKING（type/scope 后、冒号前）；scope 可选
<body>                             # 可选；what + why，自由段落
BREAKING CHANGE: <迁移说明>        # 可选 footer；与 ! 二选一或双写
Acked-by: Z                        # footer token 用 - 代空白；值可含空格换行
Refs: #123                         # git trailer 式引用
```

type → 版本推导（官方）：`feat` → MINOR，`fix` → PATCH，`BREAKING CHANGE`（footer 或 `!`，任意 type 均可携带）→ MAJOR。

语法硬规则（官方 1.0.0）：BREAKING CHANGE 必须**全大写**——唯一大小写敏感项，其余 token 一律大小写不敏感；`BREAKING-CHANGE` 与 `BREAKING CHANGE` 作 footer token 时同义；description 紧跟冒号+空格；body 与 footer 前各空一行。revert 建议：`revert` type + 引用被撤销 commit SHA 的 footer。工作流适配：squash 合并流下 casual committer 可不守规范，由 lead maintainer 在合并时清洗——规范不强制全员负担。[官方文档](https://conventionalcommits.org/en/v1.0.0/)

## 版本注意

- **Keep a Changelog**：当前规格 1.1.0（[keepachangelog.com/en/1.1.0/](https://keepachangelog.com/en/1.1.0/)）。官方六类目、七原则、坏实践四则以该版为准；格式稳定，迁移要点无。[官方文档](https://keepachangelog.com/en/1.1.0/)
- **SemVer**：2.0.0；KaC 官方原则要求 changelog 声明是否遵循（semver.org，经 KaC 1.1.0 官方引用锚定）。[官方文档](https://keepachangelog.com/en/1.1.0/)
- **ADR**：无中央规格；[adr.github.io](https://adr.github.io) 为社区枢纽（定义 / AKM 背景 / Nygard 起源），模板以 [adr.github.io/adr-templates/](https://adr.github.io/adr-templates/) 三族（MADR / Nygard / Y-Statement）为准；MADR 状态枚举第 7 轮由 [adr.github.io/madr/](https://adr.github.io/madr/) 官方 spec 站解决——status 为 YAML front matter 可选元数据，官方示例枚举 proposed/rejected/accepted/deprecated/superseded by ADR-NNNN（省略号显式，开放集）；MADR 当前版本 4.0.0（2024-09-17）。[官方文档](https://adr.github.io/adr-templates/) / [官方文档](https://adr.github.io/madr/)
- **Conventional Commits**：当前规格 1.0.0（[conventionalcommits.org/en/v1.0.0/](https://conventionalcommits.org/en/v1.0.0/)）；RFC 2119 关键词书写；feat/fix/BREAKING CHANGE→SemVer 对应、footer token 语法、`!` 标记、revert 建议以该版为准（CC BY 3.0）。[官方文档](https://conventionalcommits.org/en/v1.0.0/)

## 与其他子领域的集成要点

- **doc-governance**（`kb/doc-governance.md`）：文档生命周期治理——本域「活文档 vs 追加型历史」二分是生命周期策略的判定输入（changelog/文档站可修订，ADR 只追加）；API 废弃→移除两步走与该域 deprecation 生命周期流程联动（萃取中提及的 api-docgen AD-9/10/11 同族约束）。
- **ai-docgen-workflow**（`kb/ai-docgen-workflow.md`）：生成时机——ADR 须在决策窗口期（proposed 先行）介入而非实现后补写；changelog 条目须在合并时机滚动写入；workflow 的触发点设计应内建这两个时机。
- **doc-taxonomy**（`kb/doc-taxonomy.md`）：类型定位——changelog（发版产物、用户可见）、ADR（仓库资产、决策记录）、release notes（发布叙事）、文档站（使用说明）在文档分类体系中各归其位；本域 AC-5/AC-11 的 [GLOBAL] 候选与该域 DT-12、api-docgen AD-2、CC-2 同属「编造零容忍」族，归并进 `kb/laws.md` 全局宪法。
- **横切文件**：AI 典型错误（本域 15 条自省清单）汇入 `kb/ai-mistakes.md`；「AI 无输入编造 ADR/changelog」为跨子域共性坑，候选 `kb/gotchas.md` Top。

## 来源索引

- https://keepachangelog.com/en/1.1.0/ — KaC 1.1.0 官方全文：七原则 / 六类目 / 坏实践四则 / FAQ（rewrite "Sure."）/ Unreleased 双用途 / [YANKED] / GitHub Releases 评价。[官方文档]
- https://adr.github.io — ADR 定义 / AKM 背景 / Nygard 起源 / ADR 组织三目标 / decision log。[官方文档]
- https://adr.github.io/adr-templates/ — MADR（full/minimal）/ Nygard / Y-Statement 三族模板 + ISO 42010 背景。[官方文档]
- [模型经验] — 01~06 号萃取文件：ADR 结构缺陷、决策时机与粒度、changelog 维护纪律、Conventional Commits、release notes 结构、AI 生成错误自省层（06 无上游文档，为本库特有贡献层）。

### 第 2 轮新增（Conventional Commits 官方规格）

- https://conventionalcommits.org/en/v1.0.0/ — Conventional Commits 1.0.0 官方规格全文：结构骨架、feat/fix/BREAKING CHANGE 与 SemVer 对应、footer token 语法（`-` 代空白）、BREAKING CHANGE 全大写为唯一大小写敏感项、`!` 标记、revert 建议、squash 工作流适配、RFC 2119 关键词（CC BY 3.0）。[官方文档]
- 未经文档验证声明（更新）：commitlint/husky 工具链用法（lastReviewed: 2026-11-18，维持降级）；release notes 结构模板（业界惯例归纳，边界轮确认无权威规范，lastReviewed: 2026-11-18，维持降级）。MADR 状态枚举项于第 7 轮补锚解决（adr.github.io/madr/），从本清单移除。
- [推断] 载体分工表的时间性归类（如 changelog 标注「活文档，可诚实修订」中「活文档」一词为对官方 FAQ 的概括转译）——仅作理解辅助，不构成独立事实来源。

### 第 7 轮新增（refresh 补锚：MADR 官方 spec 站）

- https://adr.github.io/madr/ — MADR 官方 spec 站（第 2 轮 github.com/adr/madr 传输错误后的第三路径，本轮抓取成功）：status 为 YAML front matter 可选元数据（ADR-0008/0013），官方模板示例枚举 `proposed | rejected | accepted | deprecated | … | superseded by ADR-0123`（省略号显式——开放集）；版本史 3.0.0（2022-10-09，正负后果合并为 Consequences）→ 4.0.0（2024-09-17 当前最新，bare/minimal 模板变体）；可选元素含 decision-makers/consulted/informed（RACI，ADR-0015）、neutral arguments（ADR-0014）、Confirmation 节；文件名模式 `NNNN-title-with-dashes.md`（ADR-0005/0006）；decisions/ 子目录约定；markdownlint 配置（template/.markdownlint）；「无 MADR 3.0.0 工具支持」官方声明；大项目子目录分类（编号局部唯一）；双许可 MIT OR CC0-1.0。[官方文档]

## 冲突消解记录

1. **KaC 类目数**：模型原认知「官方五类 + Security 惯例，确切名单待验证」（03 萃取边界轮）→ 文档事实：KaC 1.1.0 官方六类目 Added/Changed/Deprecated/Removed/Fixed/Security，Security 为官方正列而非惯例（ingest 解决）→ 采用结论：[AC-6] 修正为官方六类含 Security；速查表中「自创类目」坑点与「Security 不混入 Fixed」判定均按官方名单执行。
2. **changelog 可否修订 vs ADR 不可改写**：模型原认知倾向「历史记录一律不改写」（AC-4 曾隐含泛化到 changelog）→ 文档事实：KaC FAQ "Should you ever rewrite a changelog? **Sure.**"——补漏版、改进、补 breaking change 记录是正当的（ingest 重要 nuance）→ 采用结论：[AC-4] 适用域显式限定 ADR；「活文档（changelog，可诚实修订）vs 追加型历史（ADR，只追加）」二分写入「定位与心智模型」；changelog 修订纪律为「补漏 ≠ 篡改」。
3. **MADR 状态枚举**：模型记忆 proposed/accepted/rejected/deprecated/superseded（01 自我质询轮自标待验证）→ 文档事实：模板页确认 MADR 含 status 元数据但未列枚举全集（ingest 部分解决）→ 采用结论：不落为硬事实，统一表述「以 MADR 官方模板仓库为准」，登记于「版本注意」→ **第 7 轮补锚收口**（[官方文档](https://adr.github.io/madr/)）：status 为 YAML front matter 可选元数据（ADR-0008/0013），官方模板示例枚举 proposed/rejected/accepted/deprecated/superseded by ADR-NNNN，带省略号（开放集、非封闭全集）——第 2 轮「未解决」挂账核销；版本注意、对比表、概念表按官方口径更新。
4. **Conventional Commits 溯源升级**（04 萃取边界轮挂账，第 2 轮补锚解决）：模型原认知「conventionalcommits.org 未在 doc_seeds 内、类型表与 BREAKING 双写法细节未经本库文档验证」→ 文档事实（[官方文档](https://conventionalcommits.org/en/v1.0.0/)，1.0.0 规格全文）：feat→MINOR/fix→PATCH/BREAKING CHANGE→MAJOR 为官方对应；`!` 与 footer 双写法均官方且可并用；BREAKING CHANGE 全大写为唯一大小写敏感项；其余 token 大小写不敏感 → 采用结论：[AC-8] 溯源升级为「官方锚 + 模型经验」；骨架示例按官方规格重写；速查表与概念表解除「未经文档验证」标注。
