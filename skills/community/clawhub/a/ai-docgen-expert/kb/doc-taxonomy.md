---
subdomain: doc-taxonomy
version: 2
updated: 2026-11-17
---

# doc-taxonomy：文档分类学（Diátaxis 判型 · 混写崩塌 · README · 信息架构）

## 定位与心智模型

本子域回答三个问题：**这篇文档是什么类型？为谁服务？在什么时刻服务？**——先判型，后写作。

核心模型是 Diátaxis 四类型方法论 [官方文档](https://diataxis.fr)：

- **tutorial**（带练）/ **how-to guide**（具体问题解法）/ **technical reference**（事实字典）/ **explanation**（讲为什么）
- 双轴划分（官方命名 [官方文档](https://diataxis.fr/map/)）：
  - **内容维**：行动引导 guide action（tutorials + how-to）vs 命题知识 propositional knowledge（reference + explanation）
  - **技能维**：技能习得 acquisition of skill（tutorials + explanation）vs 技能应用 application of skill（how-to + reference）

三条心智杠杆：

1. **判型 = 读者状态分析，不是文件模板选择**——先问读者是谁、此刻在哪，再选型 [模型经验]
2. **混写不是省事，是崩塌**——官方术语 blur，分级 partial collapse（部分崩塌）/ total collapse（全部崩塌）[官方文档](https://diataxis.fr/map/)
3. **文档按中途着陆设计**——官方循环四阶段（learning-oriented → goal-oriented → information-oriented → explanation-oriented）明确非强制顺序，用户可从任意阶段进入 [官方文档](https://diataxis.fr/map/)

判型四问与循环四阶段在结构上同构（四问分别对应四类型的朝向）——[推断]，依据：/map/ 页两表并列呈现且问句与朝向一一对应。

适用边界：技术文档（软件/开发者文档）的判型、混写治理、README 结构、文档信息架构。README / FAQ / changelog 是**位置**而非**类型**，其内容仍须逐块判型。Diátaxis 是方法论非 API，无版本编号。本子域另沉淀 AI 生成文档的系统性错误谱（判型失守 / 类型串味 / 虚假完整性 / 补全欲），属本知识库特有贡献层 [模型经验]。

## 法则

> DT-1、DT-12 为 [GLOBAL] 候选，汇入 `kb/laws.md` 时与 react/ui-ux 同源条款查重合并。

<DT-1> **MUST**: 先判型，后写作。任何文档动笔前先过官方判型四问（"Can you teach me to…?" / "How do I…?" / "What is…?" / "Why…?"），落到 tutorial / how-to / reference / explanation 之一；判不出型说明内容该拆分。
- 违反后果: 类型失守向下游传染——写作全程无结构准绳，产出混写文档（blur），任何读者都需跳读大半。
- 溯源: [官方文档](https://diataxis.fr/map/)（四问表）+ [模型经验]（01-diataxis-quad；判型三问为四问的操作化变体）

<DT-2> **MUST**: README 是位置不是类型。README 内容先判型再写；README 本身止于四要素——一句话定位、可复制安装、30 秒示例、文档入口链接。
- 违反后果: README 膨胀为全知文档（>400 行），克隆仓库后滚动疲劳；与 docs/ 双份漂移。
- 溯源: [模型经验]（03-readme-anatomy）

<DT-3> **MUST**: 一份文档只服务一种类型。混写是 blur（崩塌）不是省事。拆分判据：见到参数表挪 reference（原文留链接）；见到「让我们 / 我们先了解」挪 explanation 或删除；见到第二个读者假设（「如果你是新手…如果你有经验…」）就拆文件。
- 违反后果: partial collapse 恶化为 total collapse——文档四不像，走读者与查读者两头被拖累；后续维护两处都要改。
- 溯源: [官方文档](https://diataxis.fr/map/)（Blur 节）+ [模型经验]（02-type-mixing-antipatterns）

<DT-4> **NEVER**: tutorial 只走一条路。不列全量选项、不介绍替代方案（「你也可以用 Y」）、不嵌入 API 全表；分叉留给 how-to 与 explanation。
- 违反后果: 新手在选项海洋中迷路，教程主线走不通，心流被打断。
- 溯源: [模型经验]（02、06 自我质询轮）

<DT-5> **MUST**: 每步可验证。tutorial / how-to 的每个步骤必须带可观察的预期结果（输出/状态/返回值）；前置条件（版本/依赖/权限/前置操作）在开头显式声明。
- 违反后果: 读者走完步骤不确定成功与否；中途失败时报错与文档主题无关，无法定位引入步骤。
- 溯源: [模型经验]（01-diataxis-quad）

<DT-6> **MUST**: reference 词条自包含、零叙事。任意条目可从搜索直达读懂，无「如前所述」；不出现「让我们/接下来」；不夹最佳实践建议（那是 how-to 的事）。
- 违反后果: 查字典变成读文章；直达读者被迫逆向找到「文档第 1 页」顺序阅读。
- 溯源: [模型经验]（01-diataxis-quad；06 类型串味内省）

<DT-7> **MUST**: 现代文档按「中途着陆」设计。每页必须自包含；「先读完 Part 1-5 才能懂本页」是设计失败。
- 违反后果: 报错时刻直达文档页的读者被叙事依赖挡在门外，转向 issue/群聊重复提问。
- 溯源: [官方文档](https://diataxis.fr/map/)（循环四阶段官方明确非强制顺序、可任意进入）+ [模型经验]（04-audience-moment-matrix；「多数流量中途着陆」为经验断言，无单一权威源）

<DT-8> **MUST**: 同一主题按读者-时刻矩阵多次服务。评估 / 上手 / 日常 / 排障 / 贡献 × 读者分层的格子需要不同产出；文档覆盖度数格子覆盖率，不数文档数量。
- 违反后果: 只覆盖中层（上手+日常），评估期与贡献期两类高价值读者无支持。
- 溯源: [模型经验]（04-audience-moment-matrix）

<DT-9> **MUST**: 读者假设必须显式。「本文假设你已了解 X、版本 Y」写在文档开头，或在写作前确认。
- 违反后果: 未声明的假设（新手/专家/版本/OS）迟早变成读者报错；文档在「太浅」与「太深」间反复横跳。
- 溯源: [模型经验]（01、03、04）

<DT-10> **NEVER**: 无处可归即质疑存在必要性。禁建 misc / other / FAQ 垃圾桶目录与「其他」页；判型失败的内容拆分归位，而非集中收容。
- 违反后果: 垃圾桶目录成判型失败的制度化逃避——读者无法预测会找到什么，内容无人检索。
- 溯源: [模型经验]（02、05）

<DT-11> **MUST**: 新页必须入链。新增文档页必须同时挂到导航树或至少一个相关页的链接上；删除页面必须迁移或重定向其入链。
- 违反后果: orphan 页入度=0、访问统计趋零，等于不存在；重构后死链批量 404，外部引用失效。
- 溯源: [模型经验]（05-information-architecture）

<DT-12> **NEVER**: 只写有把握的，编造零容忍。badge / CI 状态 / 配置全表 / 设计动机 / 交叉引用，凡无事实来源的一律不写或显式标注「部分 / 以官方为准」；补全欲（表格凑齐、FAQ 凑三、结构填满）是错误不是质量。
- 违反后果: 真实项与幻觉项混排，读者无法区分；引用 404；状态徽章与仓库实况不符。
- 溯源: [模型经验]（03、06）

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| Diátaxis | 文档四类型方法论：tutorial / how-to guide / technical reference / explanation [官方文档](https://diataxis.fr) |
| 内容维（axis 1） | 行动引导 guide action（tutorials+how-to）vs 命题知识 propositional knowledge（reference+explanation）[官方文档](https://diataxis.fr/map/) |
| 技能维（axis 2） | 技能习得 acquisition of skill（tutorials+explanation）vs 技能应用 application of skill（how-to+reference）[官方文档](https://diataxis.fr/map/) |
| tutorial | 带零基础新手确定性地走通一条路（learning-oriented） |
| how-to guide | 面向带任务读者的特定具体问题解法（goal-oriented） |
| reference | 查证事实的干燥、结构化字典（information-oriented） |
| explanation | 讲为什么、设计取舍与背景的理解型文档（explanation-oriented） |
| blur | 官方对混写崩塌的术语，分级 partial collapse（部分崩塌）/ total collapse（全部崩塌）[官方文档](https://diataxis.fr/map/) |
| 中途着陆 | 读者经搜索/外链直达任意页，而非从首页顺序进入 [模型经验] |
| 读者-时刻矩阵 | 读者分层（评估/上手/日常/排障/贡献）× 使用时刻的覆盖度度量框架 [模型经验] |
| orphan doc | 入度=0、无任何入链的内容页——等于不存在 [模型经验] |
| 入口页（landing） | 按读者/任务分流的位置页，本身不是内容页 [模型经验] |
| quickstart | 非独立类型——四类型封闭，quickstart 只是 tutorial 的变体形态 [官方文档](https://diataxis.fr) + [模型经验] |
| 判型三问 | 官方四问的操作化变体：带任务还是空白？照做还是理解？步骤还是事实？[模型经验] |

## 最佳实践

### 场景 1：动笔前判型（任何新文档）

推荐路径：
1. 过官方四问，落型（速查表见「API 速查表」）
2. 判不出型 → 内容内含多类型，按 DT-3 拆分判据处理
3. 显式声明读者假设与版本前提（DT-9）

do/don't：
```
✗ 按文件模板判型：「复制上一篇的结构改改」
✓ 按读者状态判型：先问「读者是谁、此刻带任务还是空白」，再选类型
```

边界条件：判型对象是「读者状态」而非「内容长度」——短的不一定是 how-to，长也不是任何类型的豁免理由。

来源：[官方文档](https://diataxis.fr/map/) + [模型经验]（01）。本场景源于 [DT-1]。

### 场景 2：写 tutorial（带新手走通一条路）

推荐路径：
1. 锁定一条主路径：删除所有分叉与替代方案（DT-4）
2. 每步附可观察预期结果（DT-5）
3. 开头声明环境与版本假设（DT-9）
4. 文末「下一步」链接 how-to / reference；原理链 explanation「延伸阅读」

do/don't：
```
✗「Step 3：配置数据库。数据库有许多选项，让我们看看每种……」（全量选项展开）
✓「Step 3：配置数据库。保持以下默认值即可：
   db.host=localhost
   db.port=5432
   预期：运行 `npm run db:init` 输出 `schema ready`。
   完整选项见 → reference/config」
```

边界条件：教程不解释设计取舍——「为什么这样设计」链到 explanation，不在步骤中展开。

来源：[模型经验]（01、02）。本场景源于 [DT-4][DT-5]。

### 场景 3：写 how-to（直入步骤）

推荐路径：
1. 标题即任务：「如何 <具体目标>」
2. 开头「前置条件」小节：版本、依赖、权限、已完成操作（链接）
3. 直入步骤，每步可验证（DT-5）
4. 文末链接 explanation「延伸阅读」，不在步骤间插大段背景

do/don't：
```
✗「首先，让我们了解 X 的认证架构。OAuth 2.0 有四种授权模式……」（3 屏原理后才有步骤 1）
✓「背景一句话：本指南用 PKCE 流程接入 OAuth。
   ## 前置条件
   - 版本 ≥ 2.3
   - 已获取 client_id
   ## 步骤 1：……」
```

边界条件：页面标题与内容必须是同一任务；多任务写成多篇 how-to 互链。

来源：[模型经验]（02 反模式 3、8）。本场景源于 [DT-3][DT-5]。

### 场景 4：写 reference（自包含字典）

推荐路径：
1. 条目化、结构化，假设读者从搜索直达任意词条（DT-7）
2. 每条自包含：参数、类型、默认值、返回值就地写全（DT-6）
3. 零叙事、零建议：删「让我们/接下来」；「最佳实践」提示挪 how-to
4. 头部放一行「第一次用？先看教程 →」分流

do/don't：
```
✗「返回值：同上节所述类型。」
✓「返回值：`Promise<QueryResult>`——列结构与入参 `fields` 一一对应。」
```

边界条件：reference 不承担教学；示例最小化，仅用于消歧。

来源：[模型经验]（01 坑点 12、02 自我质询 4）。本场景源于 [DT-6][DT-7]。

### 场景 5：写 explanation（讲为什么）

推荐路径：
1. 围绕「为什么」组织：设计取舍、约束、备选方案的弃用理由
2. 无步骤、无操作指令；安装/使用细节链接到 tutorial / how-to
3. 设计动机只来自事实来源（ADR、issue、真实决策记录），无来源不写（DT-12）

do/don't：
```
✗「之所以选择 X，是为了解决某团队的某问题。」（编造背景）
✓「选择 X 的约束：见 ADR-12（链接）。官方给出的理由：……（引用来源）。」
```

边界条件：explanation 允许议论性语气，但不夹带安装/使用步骤；「为什么选 X」写成「如何用 X」即判型错误，重判重写。

来源：[模型经验]（01 自我质询 3、02 反模式 5）。本场景源于 [DT-1][DT-12]。

### 场景 6：拆分混写文档（blur 治理）

推荐路径：
1. 对照「混写崩塌方向对照表」（API 速查表）识别互渗方向
2. 按拆分判据切分：参数表 → reference；「让我们」段落 → explanation 或删除；第二个读者假设 → 拆两篇
3. 切分后互链：tutorial 末尾「API 细节见 →」；reference 头部「第一次用？先看教程 →」
4. 拆出的新页执行 DT-11：挂导航树或至少一个相关页链接

do/don't：
```
✗ 同文件上半部教程叙事、下半部参数字典：「顺便把 API 也放这。」
✓ 按叙事/字典边界切两文件，原位置留单行链接
```

边界条件：混写从不随机——官方 blur 亲缘表给出四组邻接亲和，混写只发生在坐标相邻的类型间 [官方文档](https://diataxis.fr/map/)；短小的跨类型引用（how-to 中一句「详见 reference」链接）不是混写，混写判据是参数全表、成段原理（>200 字无步骤）与第二读者假设。

来源：[官方文档](https://diataxis.fr/map/) + [模型经验]（02 反模式 7）。本场景源于 [DT-3][DT-11]。

### 场景 7：README 最小完备

推荐路径：
1. 一句话定位：这是什么、给谁用、解决什么问题——首屏可见；营销话术换可验证事实
2. 安装：可复制命令序列 + 版本前提（DT-9）
3. 30 秒最小示例：完整可粘贴运行 + 预期输出
4. 文档入口：tutorial / how-to / reference / explanation 至少三类外链
5. badge 只保留与真实服务对账过的（DT-12）

do/don't：
```
✗ README 含完整配置参考 + 故障排查 + FAQ（>400 行）
✓ README = 定位一句话 + 安装 + 30 秒示例 + 三条文档链接
✗「下一代、革命性的状态管理库」
✓「核心 3KB gzip 的原子化状态管理库，适用于 React 18+」
```

边界条件：README 无官方规范，四要素为社区共识 [模型经验]；「30 秒」为经验阈值非标准。

来源：[模型经验]（03）。本场景源于 [DT-2][DT-12]。

### 场景 8：规划文档集覆盖（矩阵与着陆）

推荐路径：
1. 画读者-时刻矩阵：评估 / 上手 / 日常 / 排障 / 贡献 × 读者分层
2. 每格标注现有文档或空白；覆盖度 = 格子覆盖率（DT-8）
3. 同一主题在多格多次产出（如「认证」：README 提及 → tutorial 小节 → how-to + reference → explanation 架构）
4. 每页自包含 + 「前置阅读」侧栏链接（DT-7）；新增页入链（DT-11）

do/don't：
```
✗ 数文档数量：「docs/ 已有 23 篇，覆盖度够了。」
✓ 数格子：「25 格覆盖 11 格；评估格与贡献格空白——高危。」
```

边界条件：并非每格必须有产出——空格是决策结果；但评估格（要不要用）与贡献格（如何参与）缺失是高危信号。排障时刻的 how-to（「报错 ECONNREFUSED 怎么办」）最易因「主题清单里没有错误主题」而缺位。

来源：[模型经验]（04）。本场景源于 [DT-7][DT-8]。

## 高频坑点（速查）

### Top 1：混写崩塌（blur）——违反 DT-3

- 症状：单文件内教程腔 + 参考腔 + 解释腔混排；"Getting Started" 既是带练又是速查；目录锚点混乱；同一内容两处维护。
- 根因：走读者与查读者的阅读模式互斥，作者以「顺便放这」省事；AI 侧成因——生成时逐段局部合理、整体类型漂移。
- 代码对照：
```
✗ getting-started.md（崩塌样本）
     上半部：Step 1 → Step 2（教程腔：「让我们……」）
     下半部：配置项全表 40 行（参考腔）+ FAQ 三条（收容所）
✓ 拆分：
     docs/tutorial/first-app.md   （一条路，每步可验证 → DT-4/DT-5）
     docs/reference/config.md     （自包含，零叙事 → DT-6）
     互链：tutorial 末尾「API 细节见 →」/ reference 头部「第一次用？先看教程 →」
```
- 官方锚点：/map/ Blur 节——partial collapse / total collapse [官方文档](https://diataxis.fr/map/)

### Top 2：AI 虚假完整性与交叉引用幻觉——违反 DT-12

- 症状：reference「全部选项」表格混有真实项与幻觉项；`详见 §3.2` 指向不存在章节；`docs/api.md` 链接目标未创建；badge「build passing」与仓库实况不符。
- 根因：补全欲（pattern completion）——列了 6 个真配置项就会「编到看起来完整」；引用是「合理想象」而非存在性验证。
- 代码对照：
```
✗ 无来源的全量配置表 + `详见 API 参考 §3.2` + 「build passing」badge（从未对账）
✓ 只列有来源的项 + 显式「部分选项，以官方文档为准」；无法验证的引用改「参见官方文档」
```

### Top 3：onboarding 写成 reference——违反 DT-2 / DT-7

- 症状：项目文档首页即 API 索引，新人需自行拼装 Hello World，首日流失；深度页面要求「先完成 Part 1-5」。
- 根因：作者以自己（熟悉者）的查阅路径为默认读者模型；线性「书式」假设忽视随机着陆。
- 代码对照：
```
✗ 首页 = 「模块 A/B/C 的 API 列表」；页首「请先阅读前文」
✓ 首页 = tutorial（20 分钟走通最小流程）+ 显著分流：「已熟悉？→ how-to / API 参考」
```

### 速查表

| 症状 | 根因 | 修复 | 违反 |
|---|---|---|---|
| how-to 开头 3 屏原理，读者只想动手 | 讲解欲前置 | 背景一句话 + 前置条件 + 直入步骤；原理挪 explanation 文末链接 | DT-3 |
| tutorial 步骤走完不知对错 | 省略检查点 | 每步附可观察预期结果（输出/状态/返回值） | DT-5 |
| how-to 中途失败，报错与主题无关 | 前置条件未落纸 | 开头「前置条件」：版本/依赖/权限/前置操作 | DT-5 |
| 查 reference 被叙事拖慢（「让我们」「接下来」） | 教程腔残留 | 零叙事改写 | DT-6 |
| reference 条目必须读完前文才懂 | 写成书的章节而非字典词条 | 每条自包含，删「如前所述」式依赖 | DT-6、DT-7 |
| 架构/设计问题在 issue 与群聊反复出现 | explanation 整体缺失 | 补 explanation（设计取舍/为什么） | DT-1、DT-8 |
| 「为什么选 X」写成「如何用 X」 | explanation/how-to 判型混淆 | 判型四问重判，重写为议论型 | DT-1 |
| FAQ 四类混放且无人检索 | 判型失败收容所 | 逐条判型归位；真高频疑问才留 | DT-10 |
| 「Guides」「其他」目录成垃圾桶 | 判型摇摆逃避拆分 | 强制归入类型树；无处可归即质疑存在必要性 | DT-10 |
| 文档在「太浅/太深」间横跳，人人跳读大半 | 一份文档服务所有读者 | 按读者-时刻矩阵拆分 + 入口页分流 | DT-8、DT-9 |
| 新增页访问统计趋零 | orphan：新页未入链 | 新页挂导航树或至少一个相关页链接 | DT-11 |
| IA 重构后外部引用批量 404 | 无重定向映射 | 旧→新重定向表，或 URL 不变只改内容 | DT-11 |
| AI：任何请求都产出大而全文档（quickstart 2000 字） | 补全欲压倒适用边界 | 严格按请求类型边界产出（quickstart = 5 步内跑通 + 链接） | DT-12、DT-1 |
| AI：文档结尾必附凑数 FAQ 三条 | 结构幻觉 + 凑三癖 | 删；问题判型后归位 | DT-10、DT-12 |
| AI：长文档前半守型、后半回归默认模板 | 类型意识随长度衰减 | 收尾自检全文类型一致性 | DT-3 |

## API 速查表

本域「API」= Diátaxis 判型工具集。

### 四象限判型速查（官方六行对比表 [官方文档](https://diataxis.fr/map/)）

| 类型 | what they do（做什么） | answers the question（官方判型问句） | oriented to（朝向） | form（形态） | analogy（类比） |
|---|---|---|---|---|---|
| tutorial | 带新手完成一次确保成功的旅程 | "Can you teach me to…?" | learning（习得） | 连续必做步骤，单一路径 | 教孩子做饭 |
| how-to guide | 引导读者解决特定具体问题 | "How do I…?" | goal（达成目标） | 步骤 + 前置条件，可跳读 | 食谱 |
| reference | 干燥地描述机器/系统的事实 | "What is…?" | information（查证） | 干燥、精确、结构化 | 食品包装信息 |
| explanation | 阐明并澄清某主题 | "Why…?" | understanding（理解） | 议论性、无固定结构 | 烹饪社会史文章 |

### 双轴定位（官方轴名 [官方文档](https://diataxis.fr/map/)）

| | 内容维：行动引导 guide action | 内容维：命题知识 propositional knowledge |
|---|---|---|
| **技能维：习得 acquisition of skill** | tutorial | explanation |
| **技能维：应用 application of skill** | how-to | reference |

### 操作化判型三问（官方四问的落地变体 [模型经验]）

1. 读者**带着任务**来还是**空白**来？（任务 → how-to/reference；空白 → tutorial/explanation）
2. 此刻要**照做**还是**理解/查证**？（照做 → tutorial/how-to；理解 → explanation/reference）
3. 内容是**步骤**还是**事实**？（步骤 → tutorial/how-to；事实 → reference；无步骤无事实 → explanation）

### 混写崩塌方向对照表

混写方向非随机——官方 blur 亲缘表给出四组邻接亲和，混写只发生在坐标相邻的类型间 [官方文档](https://diataxis.fr/map/)。

| 互渗方向（邻接亲和） | 典型症状 | 拆分方向 |
|---|---|---|
| tutorial ↔ how-to | "Getting Started" 既是带练又是速查，读者不知自己是新手还是熟手 | 按「空白来 / 带任务」拆两篇，互链 |
| how-to ↔ reference | how-to 内嵌 API 参数全表，带任务读者在表格中迷路 | 参数表挪 reference，原文留单行链接 |
| tutorial ↔ explanation | tutorial 中段大段原理（「让我们先了解……」），步骤心流中断 | 原理挪 explanation，文末「延伸阅读」链接 |
| reference ↔ explanation | reference 夹设计辩护/背景叙事，查词条变读文章 | 叙事段挪 explanation，词条只留事实 |

混写就地判据（[模型经验]，02）：参数表 → 挪 reference；「让我们/我们先了解」→ 挪 explanation 或删；不带步骤的段落 >200 字 → 疑似混入 explanation；第二个读者假设 → 拆两篇。

## 版本注意

- Diátaxis 是方法论非软件，**无版本编号**；规格现状以 https://diataxis.fr/map/ 为准（2026-11-17 抓取核验）[官方文档](https://diataxis.fr/map/)
- 四类型封闭：tutorials / how-to guides / technical reference / explanation——首页与 /map/ 均未见独立 quickstart 类型；quickstart 非独立类型 [官方文档](https://diataxis.fr)
- 循环四阶段 learning-oriented → goal-oriented → information-oriented → explanation-oriented：官方明确**非强制顺序**，用户可任意阶段进入 [官方文档](https://diataxis.fr/map/)
- 轴系命名以 /map/ 官方措辞为准：guide action / propositional knowledge / acquisition of skill / application of skill [官方文档](https://diataxis.fr/map/)
- Divio 历史对应（第 2 轮补抓 colophon 解决）：documentation.divio.com 为作者 Daniele Procida 2014-2021 在 Divio 期间的**早期表述**，作者自述「大部分仍认同，但若干方面现已认为有误」——diataxis.fr 为现行唯一权威版；判型依据一律以 diataxis.fr 为准，Divio 版不作为判型依据 [官方文档](https://diataxis.fr/colophon/)
- 本域 AI 错误谱版本敏感度高：随模型代际变化需定期重内省，本文件 AI 相关条目有保鲜期 [模型经验]（06）

## 与其他子领域的集成要点

- **doc-quality.md**：判型一致性是文档质量的前提检查项——质量审查清单应包含 DT-3 / DT-6 违反项扫描（叙事腔残留词、混写判据信号：参数表、「让我们」、第二读者假设）。
- **doc-governance.md**：DT-10 / DT-11 的执行机制归治理域——导航/URL 稳定性、重定向映射、orphan 链接图审计（入度=0 检测）；文档覆盖度治理以 DT-8 矩阵格子为度量单位。
- **api-doc-gen.md**：自动生成的 API reference 必须满足 DT-6（自包含、零叙事）；生成源的编造风险由 DT-12 约束——只列有来源的项，无法验证的配置项显式标注。
- **kb/laws.md**：DT-1、DT-12 为 [GLOBAL] 候选，汇入全局宪法时与 react/ui-ux 同源条款查重合并。
- **kb/ai-mistakes.md**：本域 06 主题的 AI 系统性错误 15 条（判型失守/类型串味/虚假完整性/交叉引用幻觉等）为该文件 doc-taxonomy 分节的素材源。

## 来源索引

官方文档（diataxis.fr，2026-11-17 抓取）：

- https://diataxis.fr —— 首页：四类型确认（tutorials / how-to guides / technical reference / explanation）
- https://diataxis.fr/map/ —— 轴系命名（guide action / propositional knowledge / acquisition of skill / application of skill）、判型四问、Blur（partial collapse / total collapse）与亲缘表、循环四阶段（非强制顺序）、六行期望/指引对比表

### 第 2 轮新增（Diátaxis colophon）

- https://diataxis.fr/colophon/ — 作者 Daniele Procida 确认：documentation.divio.com 为其 2014-2021 Divio 期间早期表述、部分内容作者已认为有误；diataxis.fr 为现行权威版，引用以本站为准（CITATION.cff）。[官方文档]

[模型经验]（本 skill 萃取产物，6 主题 + 1 法则化）：

- 01-diataxis-quad（四象限判型、坑点 Top 15、判型三问、AI 自我质询）
- 02-type-mixing-antipatterns（混写反模式 Top 12、拆分判据速查）
- 03-readme-anatomy（README 四要素、缺陷 Top 12、badge 纪律）
- 04-audience-moment-matrix（读者-时刻矩阵、中途着陆、格子覆盖率）
- 05-information-architecture（IA 构件、orphan 检测、URL 稳定性）
- 06-ai-taxonomy-mistakes（AI 系统性错误 Top 15、补全欲根因）
- 07-laws.md（法则化 DT-1 ~ DT-12 与 [GLOBAL] 候选标记）

未经文档验证的经验断言声明（使用时不得当作官方结论引用）：

- 「多数流量是中途着陆」「导航 ≤3 层」「30 秒示例」「>200 字无步骤段落判据」均为模型经验值/行业常识，无单一权威源
- README 四要素为社区共识，无官方标准
- 06 主题 AI 错误谱为自我内省 + 行业观察混合，上游文档（Diátaxis）不含 AI 错误章节

## 冲突消解记录

| # | 模型原认知 | 文档事实 | 采用结论 |
|---|---|---|---|
| 1 | 双轴命名「认知维（学习 acquisition vs 应用 application）× 内容维（具体 vs 一般）」 | /map/：轴 1 = 行动引导 guide action（tutorials+how-to）vs 命题知识 propositional knowledge（reference+explanation）；轴 2 = 技能习得 acquisition of skill（tutorials+explanation）vs 技能应用 application of skill（how-to+reference） | 全文改用官方轴名：内容维 = 行动引导/命题知识，技能维 = 习得/应用；模型原标签弃用 |
| 2 | 判型三问为自创权威判据 | /map/ 官方四问："Can you teach me to…?" / "How do I…?" / "What is…?" / "Why…?" | 官方四问为权威判据（DT-1 措辞已对齐）；三问降级为操作化变体，并列保留于速查表 |
| 3 | 混写 = 「结构崩塌」（自创表述） | /map/ Blur 节：官方术语 blur，分级 partial collapse / total collapse | 采用官方术语与分级；混写反模式全部重新锚定到 blur 框架 |
| 4 | 循环四阶段疑似推荐线性顺序 | 官方明确非强制顺序，用户可任意阶段进入 | 采信官方；据此为 DT-7（中途着陆设计）补官方锚点 |
| 5 | quickstart 定位存疑（疑为 tutorial 营销化变体，非独立类型） | 首页与 /map/ 均未见独立 quickstart 类型 | 维持原判：四类型封闭，quickstart 非独立类型（写入版本注意） |
| 6 | Divio 原版与 Diátaxis 的术语对应关系细节 | 未在已抓取页面解决（colophon/起源页未抓） | 保持「待考」标注；不进入正文判据区块。**第 2 轮补抓 colophon 解决**：Divio 版为作者早期表述且部分被作者否定，diataxis.fr 为唯一权威版——判型依据不引用 Divio 版，登记于「版本注意」 |
