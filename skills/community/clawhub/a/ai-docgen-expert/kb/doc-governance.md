---
subdomain: doc-governance
version: 2
updated: 2026-11-17
---

# 文档治理（doc-governance）：所有权、生命周期、SSOT 与盘点

## 定位与心智模型

本子域把文档当作**资产管理**而非写作副产品，回答四个治理问题：谁负责（所有权）、怎么流转（生命周期）、怎么防漂移（SSOT + 盘点对账）、AI 参与怎么管（责任 + 披露）。

治理体检五问（快速自检面）：

| 问 | 归属法则 |
|---|---|
| 这文档谁负责？ | [DG-1] |
| 它现在什么状态？ | [DG-4] |
| 这个事实的权威来源在哪？ | [DG-8] |
| 全量资产清单在哪、最后何时核验？ | [DG-9] |
| AI 参与了多少、谁放的行？ | [DG-10] / [DG-11] |

两个官方级心智锚：

- **文档如盆景**："alive but frequently trimmed"（Google docguide "Minimum Viable Documentation"）——文档资产不是建成即完事的纪念碑，而是需要频繁修剪的活物；常态维护观是本域一切纪律的前提。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)
- **一致性期望责任**：KaC "Inconsistent Changes"——部分维护的 changelog 与没有一样危险；一旦读者把某载体视为事实来源，不一致即背叛。该原则从 changelog 泛化到一切被当作 SSOT 的文档资产。[官方文档](https://keepachangelog.com/en/1.1.0/)

适用边界：本域为治理实践域，无 SemVer 式规格版本；CODEOWNERS 语法已于第 2 轮锚定 GitHub 官方文档（docs.github.com）；SSG 版本化实现仍以宿主工具文档为准（本库未抓取验证）。

## 法则

**DG-1 [GLOBAL] 每个文档资产有 owner，目录级归口。** 「文档人人有责」= 无人负责；CODEOWNERS 覆盖 docs/；owner 三职责：评审归口、时效性负责、争议裁决；所有权团队化（`@team` 而非个人，防单点）；分级治理（强/中/弱——产品文档全流程+门禁、内部文档轻评审、WIP 明确标注态）——无分级的强治理被绕过。
- 违反后果: 无主文档改坏无人回滚、过时无人更新、owner 离职即所有权真空；「人人有责」的实际产出是责任稀释，文档 PR 挂两周找不到 reviewer；无分级则个人笔记也套全流程，摩擦过度被绕过。
- 溯源: [官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)（CODEOWNERS 官方机制：owner 自动评审请求、write 权限要求、`@org/team` 格式、每分支独立生效）+ [模型经验]（01-ownership-model 萃取；DOCOWNERS 独立惯例未获文档证实，主流形态为 CODEOWNERS 通吃 docs 目录）。GLOBAL 理由：所有权归口可迁移到任何资产治理（配置/依赖/脚本）。

**DG-2 双通道评审：技术准确性归领域专家，结构与语言归文档 owner。** PR 模板分列两个确认区；专家不纠结措辞、文档人按领域确认单核对技术描述。
- 违反后果: 单通道评审使两类审校者都在低置信区作业——专家改语法、文档人不敢质疑技术描述，技术错误与语言问题双双漏网。
- 溯源: [模型经验]（01 萃取）。

**DG-3 文档生命周期四态管理：创建有准入、演进禁大爆炸、归档有标记、删除是正当动作。** 准入四判据（判型明确/owner 认领/有入口/查重不重复）；归档页首声明+从导航与搜索摘除+深链可达；删除前检查入链迁移；VCS 留底——删比留错强。
- 违反后果: 只建不删→站点腐烂，搜索命中过时文档概率随库存膨胀上升；归档无标记→过时内容被当现行引用；死文档误导读者、拖慢工作、诱发「文档都不可信」的绝望——官方点名三宗罪。
- 溯源: [模型经验]（02-lifecycle-states 萃取）+ [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（"Delete Dead Documentation"——删除纪律官方锚：死文档三宗罪（误导/拖慢/诱发绝望）+ 批量清理五步（渐进推进/先删确定错的/全员 Keep-or-delete/默认删/迭代））。

**DG-4 状态即元数据+可视化双层。** WIP→已发布→维护中→已过时（警示横幅）→已归档——状态在 frontmatter 可机读、在页面可视可感知；过时内容静默存在是治理失败。
- 违反后果: 状态只在作者脑中——读者把 WIP 当成品、把过时当现行；元数据无可视化等于对人类读者不可见，可视化无元数据等于对工具不可见。
- 溯源: [模型经验]（02 萃取）。

**DG-5 版本化维护乘数意识：默认无版本段 URL + 最新±1 原则 + 版本退役计划。** 多版本并存只在破坏性升级时启用（每版全量维护 ×N）；默认版本 URL 不含版本段（深链稳定）；非最新版本每页过时横幅；旧版本归档只读+下线日程公告。
- 违反后果: 低估维护乘数→v1 站三年无人管，错误内容+断链+安全漏洞在线；默认版本 URL 含版本段→改默认版本时全站外链齐断；过多版本并存（v1~v5 全在线）→维护乘数爆炸。
- 溯源: [模型经验]（03-versioning-strategy 萃取；「最新±1」为经验原则，无官方标准）。

**DG-6 版本标注纪律：版本敏感内容显式标注（引入/废弃/移除版本），标注进 CI 对账。** 「vX 起」漂移与编造同罪（版本事实无源不写）；文档版本与产品版本两层独立管理。
- 违反后果: 「v2 起」实际 v2.3 起——读者按错误版本边界排障/升级踩空；无源编造的版本标注比不标注更有害（虚假确定性）；文档版本与产品版本混层则版本切换器与内容标注互相污染。
- 溯源: [模型经验]（03 萃取）。

**DG-7 [GLOBAL] 风格指南 = 术语表 + 语态人称 + 格式规范 + 命名规范，可 lint 的进 lint，原则层可迁移、惯例层必须本地化。** 术语表是一致性的锚（每条：标准词+禁用别名+定义）；指南 ≤2 页核心；生搬英文指南到中文是双输；指南自身遵守自己（自指一致）。
- 违反后果: 无风格指南→多人贡献风格漂移；有指南零 enforcement→装饰品；200 条规则无人读完；中文团队直译英文惯例层（半角句号/去敬语）→读者别扭，规则被弃用。
- 溯源: [模型经验]（04-style-guide 萃取；developers.google.com/style 为业界事实参照但未经本库抓取验证）。GLOBAL 理由：原则层/惯例层分解法适用于任何跨语言/跨文化规范移植。

**DG-8 [GLOBAL] SSOT：每个事实只有一个权威存放处，链接优先于复制，事实刚性而表达自由。** 复制的必然漂移（物理规律非纪律问题）；复用三策略排序：链接 > transclusion > 复制（复制必须配同步检查或显式标注复制日期）；判据问句：「改一处另一处必错吗（事实→SSOT）还是同主题不同表达（表达→可多样）」；生成物单向（改源再生成，不手改编译产物）。
- 违反后果: 事实多处手写→改一处漏两处，读者无法判断哪份是权威版；生成物手改→下次生成覆盖/冲突；官方立场 "Duplication is Evil"：不写自有版本指南、用链接替代、take ownership and don't be shy。
- 溯源: [模型经验]（05-ssot-principle 萃取）+ [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（"Duplication is Evil"——SSOT 官方级背书）+ [官方文档](https://keepachangelog.com/en/1.1.0/)（GitHub Releases 评价：非便携、可发现性弱——changelog 双份漂移的官方素材）。GLOBAL 理由：SSOT/DRY 族是全工程领域原则。

**DG-9 盘点是治理基石：资产清单必须机器化（文件系统遍历+frontmatter 读取），CI 对账双向报警（未登记资产/幽灵条目）。** 元数据六字段上限（path/type/owner/status/version_scope/last_verified）；last_verified 是时效维度可操作化（超期进报告）；元数据必须有下游消费者（导航/审计/报告）——无消费者的元数据是装饰品。
- 违反后果: 无清单则 triage 不可能（债管理无分母）、触发链失效、交接不可能；手维护清单三个月必与文件系统漂移；一致性期望一旦建立，部分维护与没有一样危险——官方 "Inconsistent Changes" 警告。
- 溯源: [模型经验]（06-inventory-audit 萃取；本库「配置↔产物对账」实践锚定）+ [官方文档](https://keepachangelog.com/en/1.1.0/)（"Inconsistent Changes"——一致性期望责任的官方同构：用户将 changelog 视为 SSOT 的期望责任）。

**DG-10 [GLOBAL] 发布即担责：AI 参与度是归因线索不是责任转移。** 责任链终点是人（发布者）——「AI 写的」不构成任何免责；AI 参与度影响审校强度（风险分级）不影响责任归属；追溯类资产 AI 修改过人工门；审校记录不可省（谁/何时/抽了什么）。
- 违反后果: 责任真空——「AI 写错了」成为免责叙事，低质量被归因于工具而非流程缺失；审校记录不存则错误复发无追溯；「AI 生成」标签沦为挡箭牌。
- 溯源: [模型经验]（07-ai-era-governance 萃取）。GLOBAL 理由：AI 协作责任原则跨域适用（代码 PR 同理）。

**DG-11 AI 透明度分级：内部元数据优先于外部声明，披露服务于归因优先于告知。** 内部透明（参与度元数据+审校人）为默认；边界透明（高风险内容人工核验标注）按内容风险；对外披露按政策/信任需要——过度披露磨损信任；批量 AI 内容进周期复检计划（参与度标记×抽检密度联动）。
- 违反后果: 每页「本页由 AI 生成」→读者对全部内容疑虑（信任磨损）；内部参与度无人记录→归因不可能、周期复检无分母；批量 AI 内容无周期复检→同模式错误成批长期在位。
- 溯源: [模型经验]（07 萃取；AI 披露政策环境政策敏感，以当地要求为准）。

## 核心概念速览

| 概念 | 一句话定义 |
|---|---|
| SSOT | Single Source of Truth：每个事实只有一个权威存放处，其余位置引用不复制。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| Duplication is Evil | Google docguide 对复制式文档的官方定性：不写自有版本指南、链接替代、take ownership and don't be shy。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| Delete Dead Documentation | Google docguide 删除纪律：死文档三宗罪（误导/拖慢/诱发绝望）+ 批量清理五步（渐进/先删确定错的/全员 Keep-or-delete/默认删/迭代）。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| Minimum Viable Documentation | 盆景隐喻：docs "alive but frequently trimmed"——文档资产常态维护观。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html) |
| Inconsistent Changes | KaC 坏实践：部分维护的 changelog 与没有一样危险——SSOT 一致性期望责任。[官方文档](https://keepachangelog.com/en/1.1.0/) |
| CODEOWNERS / DOCOWNERS | 目录级所有权归口文件（如 `/docs/ @docs-team`）。官方语法事实：位置搜索顺序 `.github/`→仓库根→`docs/` 取首个；**最后匹配模式优先**（非首匹配）；owner 须显式 write 权限（`@user`/`@org/team`）；gitignore 三语法例外（`\#` 转义、`!` 取反、`[ ]` 字符类）不生效；路径大小写敏感；文件 <3MB；无效行跳过。[官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) DOCOWNERS 独立惯例未证实，类指称。[模型经验] |
| 双通道评审 | 技术准确性归领域专家、结构与语言归文档 owner，PR 模板分列两个确认区。[模型经验] |
| 分级治理 | 流程强度三档：强（产品文档全流程+门禁）/ 中（内部文档轻评审）/ 弱（个人笔记 WIP 标注）。[模型经验] |
| 准入四判据 | 新建文档门槛：判型明确 / owner 认领 / 有入口 / 查重不重复——准入不过 = 不建。[模型经验] |
| 维护乘数 | 多版本并存的代价：每版全量维护（链接/安全/内容）×N——版本数是维护成本乘数。[模型经验] |
| 最新±1 | 只维护最新两个大版本、更旧归档的经验原则（无官方标准）。[模型经验] |
| 原则层/惯例层 | 风格指南的可迁移部分（一致性/精确性/可及性）vs 必须本地化部分（标点/语态/敬语）。[模型经验] |
| 事实/表达二分 | SSOT 判据：事实（改一处另一处必错）刚性单一；表达（示例/解释/类比）允许多样。[模型经验] |
| transclusion | 内容内嵌引用（维护单一源）；Markdown include 语法无标准，SSG 各自实现。[模型经验] |
| 生成物单向 | 生成物是只读投影：修改回到源（注释/代码）重新生成，不手改编译产物。[模型经验] |
| last_verified | 最后事实核验时间戳——时效维度可操作化：超期进盘点报告，人工重验回写。[模型经验] |
| 未登记资产 / 幽灵条目 | CI 盘点对账双向报警：系统有清单无 → 未登记资产；清单有系统无 → 幽灵条目。[模型经验] |
| 发布即担责 | 责任链终点是人（发布者）；AI 参与度是归因线索不是责任转移。[模型经验] |

## 最佳实践

### 场景 1：为仓库建立文档治理基线（从零起步）

推荐路径（源于 [DG-1]）：
1. CODEOWNERS 覆盖 docs/：目录级归口（粗粒度——文件级所有权维护成本爆炸），团队化引用防单点。
2. 定分级：强治理（对外产品文档：全流程+门禁）/ 中治理（ADR/设计文档：至少一人审）/ 弱治理（个人笔记：无评审但显式 WIP 标注）。
3. owner 三职责成文：评审归口、时效性负责、争议裁决。
4. 治理规则本身落成文档（治理文档也是文档——递归自指）；owner 离职交接 checklist 进团队流程。

do/don't：

```text
✗ 「文档人人有责，不用指定 owner。」（责任稀释）
✗ CODEOWNERS 只写 /src/（docs/ 无归口）
✗ /docs/ @zhang-san（个人归口，离职即真空）
✗ 个人笔记也要两人评审（弱治理内容套强流程，被绕过）
✓ /docs/api/    @api-team
✓ /docs/guide/  @docs-team
✓ 治理规则落 docs/governance.md 并入新人必读
```

边界条件：小团队（<5 人）可一人兼任多目录 owner，但归口必须显式；人名归属是团队事实，AI 建议只能到角色设计层。

### 场景 2：设计文档 PR 评审流程（双通道）

推荐路径（源于 [DG-2]）：
1. PR 模板分列两个确认区：技术准确性（领域专家 checkbox 确认）/ 结构与语言（文档 owner 确认）。
2. 代码 PR 含文档改动时，文档部分不豁免评审（割裂即漏网）。
3. 技术审用确认单（逐项核对签名/参数/版本号），不做措辞级修改；语言审不质疑技术结论，按确认单核对。

do/don't：

```markdown
✗ Reviewer（领域专家）：「这句改成 we'll 更亲切……」（专家改语法）
✗ Reviewer（文档 owner）：技术描述看不懂，直接跳过。
✓ PR 模板：
   - [ ] 技术准确性已确认（by @domain-expert）
   - [ ] 结构与语言已确认（by @docs-owner）
```

边界条件：小 PR 可一人双签，但两个确认区仍分列（自检分角色）。

### 场景 3：清理死文档（批量清理五步，官方锚）

推荐路径（源于 [DG-3]，官方背书 [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)）：

死文档三宗罪（官方）：误导读者 / 拖慢工作 / 诱发对文档整体的绝望。

批量清理五步（官方策略）：
1. 渐进推进——不要一次大爆炸清理。
2. 先删确定错的。
3. 全员参与 Keep-or-delete 评审（每篇二选一）。
4. 默认删——拿不准按删处理（VCS 留底，删错可恢复）。
5. 迭代多轮——清理是常态动作，不是一次性运动。

删除前检查：入链迁移（谁链到它）；删除后链接检查兜底。

do/don't：

```text
✗ 「这文档可能还有人看，先留着吧。」（默认留 = 只增不减）
✗ 一次 PR 删 300 篇（大爆炸，评审失效）
✓ 拿不准的进 Keep-or-delete 名单，逾期未认领即删（默认删）
✓ 删除 PR 附入链迁移说明，断链检查通过才合并
```

边界条件：合规/法务留存要求的文档不适用「默认删」——按保留政策归档。

### 场景 4：归档一篇文档

推荐路径（源于 [DG-3] [DG-4]）：
1. 触发条件确认：对应版本废弃 / 替代文档在位 / 内容过时但历史有值。
2. 移入 archive 分区 + 页首显式声明（「本文对应 vX（日期），现行文档 → Y」）。
3. 从主导航与站点搜索索引摘除，保留深链可达（搜不到、链得到）。
4. frontmatter 状态改 archived——机读层与可视化层同步。

do/don't：

```markdown
✗ 移入 archive/ 但页首无声明（搜索/外链直达即误导）
✗ 归档声明写「本文对应 v2」但未对账真实版本归属（编造版本对应）
✓ ---
  status: archived
  ---
  > ⚠️ 本文对应 v2（2024-06 冻结），不再维护。现行文档：[/guide/config](/guide/config)
```

边界条件：归档 ≠ 删除——归档内容不再维护但保留可查；归档区需周期复核，防「无人区化」。

### 场景 5：多版本文档站决策（何时分版本、何时退役）

推荐路径（源于 [DG-5] [DG-6]）：
1. 先判升级形态：破坏性升级（v1→v2 迁移成本高）才启用多版本并存；平滑演进用单站+页内标注（多版本维护成本 > 用户价值）。
2. 多版本时：版本段进 URL（/v1/ /v2/）；默认版本无版本段（`/docs/api` = 最新稳定）；版本间 slug 保持一致（切换器跨页不漂移）；非最新版本每页过时横幅。
3. 退役计划：「最新±1」[模型经验]——只维护最新两个大版本，更旧归档只读+下线日程公告。
4. 版本标注进 CI 对账：「自 vX 引入」「vY 起废弃（vZ 移除）」× 真源（package.json/CHANGELOG）核对。

do/don't：

```text
✗ /docs/v2/api 是默认版（默认版本含版本段——v3 发布改默认时全站外链齐断）
✗ /v2/routing 切 v3 落在 /v3/ 首页（slug 不一致，切换器漂移）
✗ v1~v5 全在线（维护乘数 ×5 爆炸）
✗ 旧版每页无「你在看 vX」横幅（用户按 v1 文档排障 v3 问题）
✓ /docs/api（默认，无版本段）+ /docs/v2/api（显式旧版）+ 旧版每页横幅
```

边界条件：「最新±1」为经验原则无官方标准 [模型经验]；SSG 版本切换器实现以工具文档为准（本库未验证）。

### 场景 6：建立风格指南与术语表（中文团队本地化）

推荐路径（源于 [DG-7]）：
1. 四件套齐备：术语表（标准词+禁用别名+定义）/ 语态人称 / 格式规范（一页一 h1、代码块语言标注）/ 命名规范（文件名 kebab-case、导航项统一）。
2. 原则层可迁移（一致性/精确性/可及性），惯例层本地化（中文全角标点、敬语按中文习惯）——生搬英文惯例层是双输。
3. 可 lint 的进 lint（术语表扫描/标题层级/代码块语言），不可 lint 的进评审清单；指南 ≤2 页核心+附录。
4. 中英混杂决策进术语表（每词显式决策不逐篇即兴）：业界通用词保留英文（API/cache）、有主流译法的用中文（组件/路由）、产品自有名词原文；判据是目标读者搜索习惯。
5. 指南自身遵守自己（自指一致）。

do/don't：

```markdown
✗ 中文指南第一条：「句号用半角」（直译英文惯例层）
✗ 风格指南 200 条规则（无人读完）
✗ cache / 缓存 / Cache 三写法并存且无术语表裁决
✓ 术语表条目：标准词 `cache`；禁用别名：`缓存`；定义：一句话；首次出现处链接
```

边界条件：中文技术写作无 Google 级权威单源 [模型经验]——惯例层需团队自建；developers.google.com/style 未经本库抓取验证，不作为 URL 来源。

### 场景 7：SSOT 复用决策（链接 vs transclusion vs 复制）

推荐路径（源于 [DG-8]，官方背书 "Duplication is Evil" [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)）：
1. 先过判据问句：「改一处另一处必错吗？」——是 → 事实（SSOT 刚性）；否 → 表达（可多处多样）。
2. 复用三策略排序：链接（默认）> transclusion（需内联且 SSG 支持）> 复制（最后手段，必须配同步检查或显式标注复制日期）。
3. 已有官方源的内容（安装指南/版本指南）不写自有版——链接替代，take ownership and don't be shy [官方文档](https://google.github.io/styleguide/docguide/best_practices.html)。
4. 生成物单向：改源（注释/代码）再生成，不手改编译产物。
5. changelog 双份治理：CHANGELOG.md 为 SSOT，发布页自动生成——官方评价 GitHub Releases 为非便携 changelog、可发现性弱 [官方文档](https://keepachangelog.com/en/1.1.0/)。

do/don't：

```markdown
✗ 完整配置表复制进 quickstart（README/reference/quickstart 三处手写三版本）
✗ TypeDoc 生成 reference 后直接编辑输出 HTML（下次生成覆盖）
✗ 要求所有示例集中一页统一引用（SSOT 教条化——示例是表达）
✓ quickstart 最小示例 + 「完整配置项 → reference 链接」
✓ 离线文档复制时页首标注「复制自 X，日期 YYYY-MM-DD」
```

边界条件：离线/不可链接场景允许复制（配标注与同步检查）；transclusion 语法无 Markdown 标准（SSG 各自实现）[模型经验]。

### 场景 8：搭建机器化盘点与 CI 对账

推荐路径（源于 [DG-9]）：
1. 盘点 = 脚本：遍历文件系统 + 读 frontmatter 产出清单——不手维护 inventory.md。
2. 元数据六字段上限：path / type / owner / status / version_scope / last_verified；设计 frontmatter 时先设计「谁读它」（下游消费者）。
3. CI 双向对账：系统有清单无 → 「未登记资产」报警；清单有系统无 → 「幽灵条目」报警。
4. last_verified 超期阈值（如 6 个月）→ 超期进盘点报告 → 人工重验回写；事实核查通过即回写。
5. 盘点范围全覆盖：docs 站 + README（根/子包）+ CONTRIBUTING + CHANGELOG + ADR 库 + 示例仓库——判据：读者会接触的每一个信息资产。

do/don't：

```yaml
✗ 手维护的 docs/inventory.md（三个月后必漂移）
✗ frontmatter 15 个字段（无人填）
✓ ---
  type: how-to
  owner: @docs-team
  status: maintained
  version_scope: ">=2.3"
  last_verified: 2026-10-01
  ---
```

边界条件：盘点脚本必须实际运行验证（未运行验证的脚本 = 编造）；AI 参与度字段仅在其有消费者（周期复检计划）时增设。

### 场景 9：AI 起草文档接入治理（责任 + 披露 + 复检）

推荐路径（源于 [DG-10] [DG-11]）：
1. AI 产出生命周期起点强制 WIP 态（`status: draft` / draft PR）——「已发布」态必须人工放行，跳过 WIP 直发是流程违例。
2. 责任锚定：发布即担责——AI 参与度记入元数据（归因线索）；审校记录不可省（谁审/何时/抽了什么）。
3. 披露分级：内部透明（参与度元数据+审校人，默认）→ 边界透明（法律/合规/安全声明标注人工核验在位）→ 对外披露（仅政策/信任需要——过度披露磨损信任）。
4. 批量 AI 内容进盘点（参与度标记）+ 周期抽检计划（抽检密度由反馈回流数据驱动）。

do/don't：

```markdown
✗ AI 生成的 200 页直接 merge 进 docs/（跳过 WIP，游离治理外）
✗ 每页标注「本页由 AI 生成」（过度披露——读者对全部内容疑虑）
✗ 出错后归因「AI 写的」（免责叙事）
✓ frontmatter: ai_assisted: true + review_log: {reviewer, date, sampled}
✓ 高风险页（安全声明）标注「已经人工核验」
```

边界条件：AI 披露政策要求以当地法规与平台现行规定为准（政策敏感、演化快）[模型经验]。

## 高频坑点（速查）

### 深度展开 Top 2

**Top 1：「文档人人有责」——无主文档堆积**（违反 [DG-1]）
- 症状：「这文档谁负责的？」「不知道，原来 X 写的，X 走了」；文档 PR 挂两周找不到 reviewer。
- 根因：「人人有责」是责任稀释——所有权缺位时改坏无人回滚、过时无人更新、离职即真空。
- 代码对照：

```text
✗ CODEOWNERS: /src/ @team-a（docs/ 无归口）
✗ 「文档不用指定 owner，大家随手改。」
✓ /docs/api/ @api-team
✓ /docs/guide/ @docs-team
```

- 修复：目录级 CODEOWNERS 覆盖 docs/、团队化归口、分级治理（场景 1）。

**Top 2：只建不删——死文档堆积**（违反 [DG-3]）
- 症状：5 年 800 篇文档，一半过时——搜索命中过时文档概率 50%。
- 根因：创建有成就感、删除有风险感的不对称心理；无准入 + 无盘点使删除无分母。官方点名死文档三宗罪：误导读者 / 拖慢工作 / 诱发对文档整体的绝望。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)
- 代码对照：

```text
✗ 「先写了再说」——无准入新建，垃圾桶文档逐年累积
✗ 拿不准的一律保留（默认留）
✓ 批量清理五步：渐进 / 先删确定错的 / 全员 Keep-or-delete / 默认删 / 迭代
```

- 修复：按场景 3 执行批量清理；准入四判据前置（判型/owner/入口/查重）。

### 速查表

| 症状 | 根因 | 修复 | 法则 |
|---|---|---|---|
| CODEOWNERS 只覆盖代码不覆盖 docs/ | 所有权盲区 | docs/ 目录级归口，团队化引用 | DG-1 |
| 文档 PR 挂两周无人审 | 评审无归口 | owner 评审归口 + 治理分级 | DG-1, DG-2 |
| owner 离职，其目录 PR 堆积 | 个人归口单点 | `@team` 团队化 + 交接 checklist | DG-1 |
| 个人笔记也要全流程评审，团队绕过流程 | 治理无分级 | 强/中/弱三档，WIP 显式标注 | DG-1 |
| 治理规则只存在于口头惯例 | 规则不成文（新人无从遵循） | 治理规则落 docs/governance.md | DG-1 |
| API 文档 PR：专家改语法、文档人不敢质疑技术 | 双通道混同 | PR 模板分列技术/语言两个确认区 | DG-2 |
| 「先写了再说」，垃圾桶文档泛滥 | 创建无准入 | 准入四判据不过 = 不建 | DG-3 |
| 5 年 800 篇一半过时 | 只建不删（不对称心理） | 批量清理五步，默认删 | DG-3 |
| 搜索/外链直达归档页被当现行 | 归档无标记 | 页首声明 + 导航/搜索摘除 + 深链可达 | DG-3, DG-4 |
| 删除后出现断链 | 删除无入链检查 | 删除前入链迁移检查 + 链接检查兜底 | DG-3 |
| AI 生成文档直接「已发布」态 | 跳过 WIP 人工验收 | AI 产出强制 draft 起步，人工放行 | DG-4 |
| 状态标记只有作者知道 | 元数据无可视化 | frontmatter + 横幅双层同步 | DG-4 |
| v1 站三年无人管、漏洞在线 | 低估维护乘数 | 「最新±1」+ 版本退役计划 | DG-5 |
| `/v2/routing` 切 v3 落首页 | 版本间 slug 不一致 | slug 稳定 + 切换映射表 | DG-5 |
| 改默认版本时全站外链断 | 默认版本 URL 含版本段 | 默认版本无版本段（`/docs/api`） | DG-5 |
| 用户在旧版页面排障新版问题 | 旧版无过时横幅 | 非最新版本每页「你在看 vX」横幅 | DG-5 |
| 「v2 起」实际 v2.3 起 | 版本标注漂移/编造 | 标注进 CI 对账；版本事实无源不写 | DG-6 |
| 文档版本与产品版本混为一谈 | 两层版本未独立管理 | 文档站版本 × 内容对应产品版本分层管理 | DG-6 |
| 风格指南在 Wiki 躺着，PR 无人查 | 零 enforcement | 可 lint 进 lint，不可 lint 进评审清单 | DG-7 |
| 中文文档按英文指南直译规则，读者别扭 | 惯例层未本地化 | 原则层迁移 + 惯例层本地化 | DG-7 |
| 同概念多写法（cache/缓存并存） | 术语表缺失 | 术语表每词显式决策，进 CI 扫描 | DG-7 |
| 指南自身违反自己的规则 | 自指不一致 | 指南即风格样本，评审时对照执行 | DG-7 |
| 同一配置项三处手写三个版本 | 事实多处复制 | 链接替代 + 真源唯一（"Duplication is Evil"） | DG-8 |
| 生成物直接手改，下次生成覆盖 | 生成物当活文档 | 生成物单向：改源再生成 | DG-8 |
| CHANGELOG.md 与 GitHub Releases 一新一旧 | 双份人工维护漂移 | CHANGELOG.md 为 SSOT，发布页自动生成（官方：Releases 非便携、可发现性弱） | DG-8 |
| 要求示例也集中一页统一引用 | SSOT 教条化（事实/表达不分） | 事实刚性单一，表达允许且鼓励多样 | DG-8 |
| 手维护 inventory 三个月即漂移 | 盘点未机器化 | 脚本遍历 + CI 双向对账报警 | DG-9 |
| frontmatter 说 v2、正文说 v3 | 元数据与正文漂移 | 元数据 lint 交叉核对 | DG-9 |
| 「这文档还准吗？」「应该……准吧」 | last_verified 缺失 | 时间戳 + 超期阈值 + 重验回写 | DG-9 |
| 盘点只盘 docs/，漏 README/ADR/changelog | 范围漏资产 | 判据：读者会接触的每一个信息资产 | DG-9 |
| 元数据 15 字段无人填、无流程读它 | 模型过度 + 无消费者 | 六字段上限；先设计「谁读它」 | DG-9 |
| 「AI 写错了」成为免责叙事 | 责任真空 | 发布即担责；参与度影响审校强度不影响责任 | DG-10 |
| AI 改 ADR/changelog 无人工门 | 追溯类资产失守 | 追溯类资产 AI 修改过人工门 | DG-10 |
| 每页「本页由 AI 生成」，读者对全部内容疑虑 | 过度披露 | 内部元数据优先于外部声明 | DG-11 |
| 半年前 AI 批量生成内容错误至今在位 | 无周期复检 | 参与度标记 × 周期抽检计划联动 | DG-11 |

## API 速查表

本域无运行时 API——速查表为治理操作化三表 [模型经验]。

### 表 1：文档漂移根因分类 × 检测手段

| 漂移根因 | 典型症状 | 检测手段 |
|---|---|---|
| 代码变更未同步文档 | 行为已变，文档还在教旧用法 | 触发链映射（PR 触及路径 ↔ 受影响文档清单）+ last_verified 超期报告 |
| 复制粘贴散布 | 同一事实 N 处 N 个版本 | 重复内容/术语一致性扫描；CI 对账（事实字段 × 真源核对） |
| 职责真空 | 过时无人更新、改坏无人回滚 | CODEOWNERS 覆盖检查（docs 目录无归口报警）；盘点 owner 字段空值扫描 |
| 生成器配置漂移 | docgen 配置已改、产物未重建；或生成物被手改 | CI 重新生成对账（仓库产物 vs 重新生成产物 diff） |
| 元数据漂移 | frontmatter 与正文版本/状态不一致 | 元数据 lint（frontmatter × 正文版本引用交叉核对） |
| 版本标注漂移 | 「v2 起」实际 v2.3 起 | 版本号对账 CI（文档标注 × package.json/CHANGELOG 真源） |

### 表 2：文档门禁工具 × 集成位置

| 门禁 | 检查内容 | 集成位置 |
|---|---|---|
| docs lint | markdownlint / 术语表扫描 / 标题层级 / 代码块语言标注 | PR CI（每次文档改动） |
| 链接检查 | 内外链可达性、锚点存在性、{@link} 目标存在 | PR CI（增量）+ 定时任务（全站） |
| 覆盖率门禁 | 新公共 API 无文档报警、覆盖矩阵格子空缺 | PR CI（diff 触及公共接口时） |
| docgen 流水线 | 从源生成 reference + 生成物对账（只读投影检查） | CI 构建步（产物部署前） |
| 盘点对账 | 文件系统 vs 清单双向 diff（未登记资产/幽灵条目） | 每次 CI |
| hook 拦截 | 治理元数据必填校验（status/owner 缺失拦截提交） | 本地 git hook + CI 双层 |

### 表 3：生命周期状态机 × 处置动作

| 状态 | 判定标志 | 处置动作 | 迁移触发 |
|---|---|---|---|
| 新建（WIP/草稿） | `status: draft` / draft PR | 过准入四判据；AI 产出强制从本态起步；人工放行才可发布 | 验收通过 → 维护 |
| 维护（已发布/维护中） | `status: maintained` + last_verified 在阈值内 | 随代码触发链更新；事实核验通过回写 last_verified；增量演进禁大爆炸重写 | 超期未核验 / 内容失准 → 过时 |
| 过时（已过时） | 警示横幅在位 | 进盘点报告 triage：更新 / 归档 / 删除三选一 | triage 结论 → 维护或退役 |
| 退役（归档/删除） | `status: archived` 或已删除 | 归档：页首声明 + 导航/搜索摘除 + 深链可达；删除：入链迁移检查 + VCS 留底 | 归档内容周期复核；删除经 VCS 可恢复 |

## 版本注意

- 实践声明：本域为治理实践域，无 SemVer 式规格版本；以下为来源文档版本与实践状态声明，非本域「版本」。
- **Google docguide**（[google.github.io/styleguide/docguide/best_practices.html](https://google.github.io/styleguide/docguide/best_practices.html)）：风格指南型活文档，非版本化规格；"Duplication is Evil" / "Delete Dead Documentation" / "Minimum Viable Documentation" 以抓取时页面为准。[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)
- **Keep a Changelog**：当前规格 1.1.0；本域引用其 "Inconsistent Changes" 坏实践与 GitHub Releases 评价（非便携、可发现性弱），均以该版为准。[官方文档](https://keepachangelog.com/en/1.1.0/)
- 多版本策略「最新±1」：无官方标准，经验原则，按团队维护容量裁剪。[模型经验]
- AI 披露政策：政策敏感、环境演化快（版本敏感度高）——以当地法规与平台现行要求为准。[模型经验]
- **CODEOWNERS**（第 2 轮补锚，2026-11-17）：GitHub 官方文档已锚定——位置搜索顺序、**最后匹配模式优先**、write 权限要求、分支保护「Require review from Code Owners」下任一 owner 批准即满足（OR 语义）、draft PR 不自动请求、3MB 上限、gitignore 三语法例外以 [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) 为准。[官方文档] SSG 版本切换器实现仍以宿主工具文档为准，未经本库验证。[模型经验]

## 与其他子领域的集成要点

- **adr-changelog**（`kb/adr-changelog.md`）：修订 vs 追加二分的治理面——「活文档（changelog，可诚实修订）vs 追加型历史（ADR，只追加）」是 [DG-3] 生命周期策略的判定输入；KaC "Inconsistent Changes" 为两域共享锚；追溯类资产（ADR/changelog）AI 修改过人工门 = [DG-10] 在该域的落地条款（AC-4/AC-5）。
- **ai-doc-verification**（`kb/ai-doc-verification.md`）：验证即治理手段——[DG-9] 的 last_verified 回写、CI 对账与本域表 2 门禁工具的执行层在该域展开；[DG-10] 的审校强度分级与抽检密度由该域度量体系（风险分级/反馈回流）驱动。
- **ai-docgen-workflow**（`kb/ai-docgen-workflow.md`）：同步机制——[DG-3] 的触发链（代码变更→文档更新）与文档债管理的机制实现层；docgen 流水线（表 2）的触发点设计对接该域工作流。
- **doc-taxonomy**（`kb/doc-taxonomy.md`）：导航与可发现性——DT-10/DT-11（导航/新页入链）的执行机制归本域；[DG-3] 准入判据「判型明确」以该域判型体系为前提；orphan 检测（入度=0）与归档「导航/搜索摘除」共用链接图。
- **api-doc-gen**（`kb/api-doc-gen.md`）：[DG-8] 生成物单向原则与该域 AD-8（手写 reference 反模式）同源；表 2 docgen 流水线行对接该域 TypeDoc/OpenAPI 管线细节。
- **横切文件**：[GLOBAL] 候选（DG-1 所有权归口 / DG-7 原则层惯例层 / DG-8 SSOT / DG-10 发布即担责）汇入 `kb/laws.md` 与全局法则池查重合并；本域 AI 自省层（07 主题）汇入 `kb/ai-mistakes.md`；「无主文档」「死文档堆积」候选 `kb/gotchas.md` Top。

## 来源索引

- https://keepachangelog.com/en/1.1.0/ — KaC 1.1.0 全文（与 adr-changelog 子域共用抓取）："Inconsistent Changes"（部分维护的 changelog 与没有一样危险——SSOT 一致性期望责任）；GitHub Releases 评价（非便携 changelog、可发现性弱）。[官方文档]
- https://google.github.io/styleguide/docguide/best_practices.html — Google docguide best practices（借道抓取，经 doc-quality 子域共享）："Duplication is Evil"（不写自有版本指南/链接替代/take ownership and don't be shy）；"Delete Dead Documentation"（死文档三宗罪：误导/拖慢/诱发绝望 + 批量清理五步：渐进/先删确定错的/全员 Keep-or-delete/默认删/迭代）；"Minimum Viable Documentation"（盆景隐喻 alive but frequently trimmed）。[官方文档]

### 第 2 轮新增（CODEOWNERS 官方文档）

- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners — GitHub 官方 About code owners：CODEOWNERS 位置搜索顺序（`.github/`→根→`docs/` 取首个）、**最后匹配模式优先**、owner 须显式 write 权限、分支保护「Require review from Code Owners」（任一 owner 批准即满足，OR 语义）、draft PR 不自动请求评审、每分支独立生效、3MB 上限、gitignore 三语法例外（`\#` 转义、`!` 取反、`[ ]` 字符类不生效）、路径大小写敏感、无效行跳过。[官方文档]
- [模型经验] — 01~07 号萃取文件：所有权模型、生命周期状态、多版本策略、风格指南、SSOT、盘点、AI 时代治理（07 为本库前瞻贡献层，无上游文档）。
- 未经文档验证声明（更新）：developers.google.com/style 核心规则（04 边界轮待验证项，ingest 未覆盖）；Docusaurus/VitePress 版本切换器实现；Markdown transclusion 语法；「最新±1」业界共识；AI 披露政策要求。
- [推断] 「官方清理五步对应 [DG-3] 删除纪律、盆景隐喻对应生命周期演进态」的映射为蒸馏期综合理解，仅作导航辅助——官方原文未做此映射。

## 冲突消解记录

1. **借道锚处置**：本子域种子为 keepachangelog.com；Google docguide 治理锚（Duplication is Evil / Delete Dead Documentation / Minimum Viable Documentation）非种子直抓，经 doc-quality 子域抓取共享（ingest 登记「借道抓取（治理层官方锚）」）→ 采用结论：作为 [DG-3]/[DG-8] 官方背书与「定位与心智模型」素材引入；URL 限于 ingest 记录两域（google.github.io、keepachangelog.com），未新增编造来源。
2. **SSOT 权威表述**（05 边界轮待验证项）：模型原认知「SSOT 落地策略无官方锚、标实践归纳」→ 文档事实：Google docguide "Duplication is Evil" 提供官方级背书（不写自有版本指南、链接替代、take ownership and don't be shy）→ 采用结论：[DG-8] 溯源升级为「官方锚 + 模型经验」双标。
3. **生命周期处置官方立场**（02 待验证项）：模型原认知「删除纪律为实践归纳」→ 文档事实："Delete Dead Documentation" 官方锚（死文档三宗罪 + 批量清理五步）→ 采用结论：[DG-3] 删除纪律获官方背书；五步策略写入场景 3 与 Top 2 坑点。
4. **多版本策略权威源**（03 待验证项）：未解决（无官方标准）→ 采用结论：「最新±1」维持 [模型经验] 经验原则标注；SSG 切换器实现维持类指称降级（以工具文档为准）。
5. **盘点权威框架**（06 待验证项）：未解决 → 采用结论：维持「实践归纳 + 本库内源锚（配置↔产物对账）」；[DG-9] 溯源不冒充官方。
6. **AI 披露政策**（07 待验证项）：未解决 → 采用结论：维持「政策敏感，以当地要求为准」；[DG-11] 相应标注。
7. **DOCOWNERS 独立惯例**（01 待验证项）：未解决 → 采用结论：类指称降级——主流形态为 CODEOWNERS 通吃 docs 目录；「DOCOWNERS」仅作概念指称保留。
8. **developers.google.com/style 核心规则**（04 待验证项）：ingest 未覆盖 → 采用结论：「原则层/惯例层」分解维持 [模型经验]；该指南未经本库抓取验证，不作 URL 来源引用。
9. **CODEOWNERS 语法官方锚定**（第 2 轮补锚）：模型原认知「CODEOWNERS 平台语法以宿主平台官方文档为准，未经本库验证」→ 文档事实（[官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)）：位置搜索顺序 `.github/`→根→`docs/` 取首个；**最后匹配模式优先**（非首匹配）；gitignore 三语法例外（`\#` 转义、`!` 取反、`[ ]` 字符类）不生效；路径大小写敏感；文件 <3MB；owner 须显式 write 权限；分支保护下任一 owner 批准即满足（OR 语义）；draft PR 不自动请求评审；无效行跳过不阻断 → 采用结论：[DG-1] 溯源升级「官方锚 + 模型经验」；语法事实写入概念表与「版本注意」——「最后匹配优先」与「OR 审批」是 docs/ 归口配置最易踩的两个官方语义。
