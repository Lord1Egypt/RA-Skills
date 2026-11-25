---
type: cross-cutting
name: patterns
domain: ai-docgen
skill_name: ai-docgen-expert
version: 2
updated: 2026-11-17
subdomains: [doc-taxonomy, api-doc-gen, code-comment, adr-changelog, ai-docgen-workflow, ai-doc-verification, doc-governance, doc-quality]
patterns: 7
---

# 跨子领域最佳实践（patterns）— 场景 → 推荐路径

本文件是 ai-docgen 领域的**跨子领域流程层**：把 8 个子领域 kb 重组为端到端推荐路径。每个 pattern = 场景标题 → 推荐路径（步骤化）→ 来源标注；支撑法则引用子域编号（DT/AD/CC/AC/AW/AV/DG/DQ），深度展开见各 `kb/<subdomain>.md`。

排序：P-1~P-2 建设（工具链/文档体系）；P-3~P-4 联动（AI 流水线/记录体系）；P-5 门禁；P-6~P-7 治理专项（文档债/AI 腔）。「建设 → 联动 → 门禁 → 治理」闭环。

---

## P-1 API 文档工具链选型决策

**场景**：新项目或存量项目要为 API 建文档，在 TypeDoc/TSDoc、JSDoc、OpenAPI 注释路线、手写之间选型。

推荐路径：

1. **判项目形态**（选型分派的第一判据）：TS 库 / TS 应用 / 纯 JS 项目 / REST(HTTP) 服务。
2. **TS 库** → TypeDoc + TSDoc 体系：类型系统是第一文档层，注释只写类型外语义（[AD-1]）。[官方文档](https://tsdoc.org) / [官方文档](https://typedoc.org)
3. **TS 库的治理三项**：覆盖率检查 / `@internal` 过滤 / 生成进 CI——工具链生成 raw、治理出文档，缺一不可（[AD-8]）；站点产物不提交仓库，ApiExtractor 类 `.api.md` API 报告提交（PR diff 即 API 审查面）。
4. **纯 JS 项目** → JSDoc（TSDoc 的前提是类型信息由 TS 承担，JS 项目不适用）。[官方文档](https://jsdoc.app)
5. **REST(HTTP) 服务** → OpenAPI 路线：先定**唯一手写真源**——spec-first（外部契约稳定性要求高、多客户端并行）或 code-first（内部快速迭代）二选一，两边手写必漂移（[AD-13]）；错误响应（非 200）必入 spec（[AD-6]/[AD-13]）；装饰器路线（框架体系成熟时）vs 注释路线（框架无关但 YAML schema 与类型双写是漂移源）按框架现实取舍（[AD-13]）。
6. **无提取工具链的项目**：文档注释只是带格式的普通注释——先确认提取→渲染路径可走通，否则降级（[CC-12]）。
7. **手写 reference** 仅限工具链覆盖不了的场景（概念文档/设计论证），且受「无源不生成」纪律约束（[AD-2]）；文档难写是设计坏味信号，应上报设计问题而非用文字打补丁（[AD-12]）。

边界条件：具体装饰器/注释语法（NestJS/tsoa/swagger-jsdoc）必须锚定对应框架文档，不得凭记忆；ESDoc 维护状态待考，不作为选型事实输出。

来源：[官方文档](https://tsdoc.org)（TSDoc 三设计要求）+ [官方文档](https://typedoc.org)（入口点发现）+ [官方文档](https://jsdoc.app) + [模型经验]。详见 kb/api-doc-gen.md（AD-1/AD-2/AD-8/AD-12/AD-13）、kb/code-comment.md（CC-12）。

## P-2 项目文档体系从零搭建

**场景**：新项目（或文档荒漠项目）要搭建文档体系，从 README 到分层结构到门禁的信息架构路径。

推荐路径：

1. **README 四要素起步**：一句话定位、可复制安装、30 秒最小示例、文档入口链接（[DT-2]）；README 是位置不是类型，膨胀为全知文档（>400 行）即违例；badge 只保留与真实服务对账过的（[DT-12]）。
2. **第一篇 tutorial**：新人 20 分钟走通最小流程——一条主路径无分叉（[DT-4]）、每步附可观察预期结果（[DT-5]）、开头声明环境与版本假设（[DT-9]）。首页即 API 索引是新人流失设计（[DT-7]）。
3. **Diátaxis 分层扩展**：每篇动笔前过判型四问（"Can you teach me to…?" / "How do I…?" / "What is…?" / "Why…?"），落 tutorial/how-to/reference/explanation 之一（[DT-1]）[官方文档](https://diataxis.fr/map/)。
4. **一文档一类型**：混写是 blur 不是省事（[DT-3]）[官方文档](https://diataxis.fr/map/)。
5. **覆盖度数格子不数文档**：按读者-时刻矩阵（评估/上手/日常/排障/贡献 × 读者分层）标注格子，评估格与贡献格缺失是高危信号（[DT-8]）；每新增一页必入链——挂导航树或至少一个相关页（[DT-11]）。
6. **治理收口**：CODEOWNERS 覆盖 docs/、团队化归口（[DG-1]）；新建过准入四判据（判型明确/owner 认领/有入口/查重不重复，[DG-3]）；盘点机器化——脚本遍历 + frontmatter 读取 + CI 双向对账（[DG-9]）。
7. **门禁收口**：按 P-5 成本排序接入，不为从零项目上全量门禁。

边界条件：README 四要素为社区共识无官方标准（[模型经验]）；小团队（<5 人）可一人兼任多目录 owner，但归口必须显式。

来源：[官方文档](https://diataxis.fr/map/)（判型四问、blur）+ [模型经验]。详见 kb/doc-taxonomy.md（DT-1~DT-12）、kb/doc-governance.md（DG-1/DG-3/DG-9）。

## P-3 AI 文档生成-验证-审校流水线设计

**场景**：团队引入 AI 批量起草文档，需要设计「生成 → 验证 → 审校」三段流水线与置信度分层，防幻觉直出也防人工瓶颈。

推荐路径：

1. **生成段——输入契约先行**：事实源（代码/类型/diff/既有文档）、类型与受众约束、风格样例 2-3 篇、边界说明四要素齐备才调用（[AW-3]）。
2. **无源降级**：无源只产出「结构模板 + 待填标注」，不生成事实内容（[AD-2]/[AC-5]）。
3. **生成段——来源分级标记**：草稿态对事实声明标 `[S:源]` / `[I:推断依据]` / `[P:先验未验]`（[AW-6]）；终稿清洗后 `[P]` 类必须已验证或已删除——先验未验即输出是幻觉高发通道。
4. **验证段——机器层自动化**：lint → 示例编译 → 签名比对 → 链接三态检查（内链 blocking、外链 warning+豁免、403/429 反爬族豁免，[AV-3]）逐层拦截；语义层不入自动化（[AV-1]）。
5. **验证段——引用分类验证**：文件/锚点/API 符号/issue/版本各有验证方法，逐类存在性验证而非「合理想象」（[AV-4]）。
6. **审校段——风险分级抽样**：低风险（结构化改写/格式化）5% / 有源中风险 15% / 无源高风险全量或拒生成（[AV-7]）；抽样按幻觉高发位加权（数字/链接/名称 > 断言 > 常识）；发现率超阈值触发整批扩抽——批次内错误自相关（[AV-7]）。
7. **审校段——外部性**：AI 可自查结构层（格式/链接/清单完备性），不可自查事实层；AI 不做最终放行人，验收人不得是生成人（[AV-8]）；AI 产出强制 WIP/draft 态起步，人工放行才发布（[DG-4]/[DG-10]）。
8. **回流段**：验收发现按错误模式归类，回流进后续生成规则（prompt/few-shot/lint），审校是校准不是修补（[AV-9]/[AW-10]）。

边界条件：抽样密度（5%/15%）为经验设计可调参数——幻觉率随模型代际下降则密度可降；批量场景另加四锚（分域分批/风格锚先行/术语表先行/批间 checkpoint，[AW-7]）与长会话疲劳管理（[AW-8]）。

来源：[模型经验]（种子 docs.anthropic.com 区域封锁，降级纯模型模式）。详见 kb/ai-docgen-workflow.md（AW-3/AW-6/AW-7）、kb/ai-doc-verification.md（AV-3/AV-4/AV-7/AV-8/AV-9）、kb/doc-governance.md（DG-4/DG-10）。

## P-4 changelog/ADR/doc 体系的联动设计

**场景**：代码变更后 changelog、ADR、API 文档、迁移指南多产物如何被同一触发链同步，不靠记忆不漏不漂。

推荐路径：

1. **触发分类三态**（触发链的判定核心）：接口变更 → reference 更新 + changelog Unreleased；行为变更 → 全站 grep 旧行为关键词建立「受影响文档清单」再改；纯实现 → 无动作（[AW-1]）。PR 模板含「文档影响」checkbox；hotfix 流程强制文档影响一句话。
2. **changelog 层——写入时机**：合并时即写 `## [Unreleased]` 对应类目，不发版日突击（[AC-7]）。
3. **changelog 层——类目与过滤**：类目用 Keep a Changelog 官方六类（Added/Changed/Deprecated/Removed/Fixed/Security，[AC-6]）[官方文档](https://keepachangelog.com/en/1.1.0/)；每条过「用户可见」过滤——commit 复读是官方点名坏实践。
4. **ADR 层——决策窗口**：决策窗口期建 `Status: proposed`，定稿改 accepted——事后补写的 ADR 是辩护文不是记录（[AC-2]）。
5. **ADR 层——supersede 双向链**：推翻决策走双向链：新建 ADR 指回旧篇 + 旧篇仅改状态行，历史条目保持历史准确（[AC-4]）[官方文档](https://adr.github.io/adr-templates/)。
6. **废弃联动链**：`@deprecated` 标注一次写全（原因/替代/迁移指引/移除版本，[AD-9]）→ 标注当天全站 grep 扫描文档资产（[AD-10]）→ changelog 的 Deprecated 与 Removed 两步走、到期必联动（[AC-9]）→ 迁移指南以旧代码为起点 + 行为差异列（[AD-11]）。
7. **commit 层**：Conventional Commits type/scope/BREAKING 标记驱动 SemVer 推导与 changelog 自动化；规范必须工具强制（commitlint + hook + CI），靠自觉必然溃败（[AC-8]）。
8. **发布节点**：CHANGELOG.md 为 SSOT，release notes 自动从其生成或明确单份维护——双份人工维护必然漂移（[AC-10]/[DG-8]）[官方文档](https://keepachangelog.com/en/1.1.0/)。

边界条件：Conventional Commits 细节已锚定官方规格 1.0.0（[官方文档](https://conventionalcommits.org/en/v1.0.0/)，第 2 轮补抓）；「文档与代码同 PR（小变更）或同里程碑（大变更）」——不允许文档 PR 跨版本悬置（[AW-1]）。

来源：[官方文档](https://keepachangelog.com/en/1.1.0/)（六类目/坏实践/GitHub Releases 评价）+ [官方文档](https://adr.github.io/adr-templates/)（ADR 三模板）+ [模型经验]。详见 kb/adr-changelog.md（AC-2~AC-11）、kb/api-doc-gen.md（AD-9/AD-10/AD-11）、kb/ai-docgen-workflow.md（AW-1）。

## P-5 文档门禁 CI 最小集（按成本升序引入）

**场景**：为文档资产建 CI 门禁，决定先上什么后上什么——一步到位全量门禁必被绕过，渐进接入才能存活。

推荐路径（引入顺序 = 成本升序）：

1. **链接检查**（半天接入，立刻拦最高频错误）：内链 blocking；外链可达性 warning + 缓存（TTL 数天）+ 豁免清单；403/429 反爬族直接豁免——三态分类防误报淹没真断链（[AV-3]/[AW-9]）。
2. **lint + 格式校验**：markdownlint 类 + 术语表扫描（[DG-7]）+ changelog 格式校验；可 lint 的风格规则进 lint，不可 lint 的进评审清单。
3. **示例可运行——分层落地**（成本最高）：示例编译每 CI（全部可执行块）→ reference 示例运行断言 → tutorial 快照关键输出 → 全流程走查每版本发布前（[AV-2]）。
4. **快照纪律**：快照 diff 必须出现在 PR 中被审——快照变化即行为变更信号；断言用关键行/归一化比对，禁全量 stdout 匹配（[AV-2]）。
5. **覆盖率门禁**：分母来自代码侧（类型导出/AST 解析公共接口），文档侧只提供分子——防幸存者偏差；新增 blocking + 存量基线渐进清偿（[AV-5]）。
6. **度量配对抽查**：随机质抽查配对——防 `// the x` 式凑数的 Goodhart 凑数（[AV-5]）。
7. **门禁分级**：blocking（链接 404/changelog 格式/示例编译失败）/ warning（覆盖率阈值/文风，配额制：新 warning 不许增加、旧逐步清零）/ 报告（orphan 扫描/过时文档扫描，定期）（[AW-9]）。
8. **运维纪律**：报错必须可操作（文件/行/修复建议）；每条豁免登记原因 + 定期复核——豁免是资产不是暗门（[AV-3]）；生成物新鲜度检查（TypeDoc 类产物与源码同步校验，[AW-9]）。

边界条件：一次性项目文档可裁剪到「示例编译 + 内链检查」两项；长生命周期文档库全套；门禁失败必须可修复，否则团队绕过门禁。

来源：[模型经验]。详见 kb/ai-docgen-workflow.md（AW-9）、kb/ai-doc-verification.md（AV-2/AV-3/AV-5）、kb/doc-governance.md（DG-7/DG-9）。

## P-6 文档债盘点与增量偿还

**场景**：文档与现实差距已积累（漂移/过时/误导），要系统性清偿而非「想起来修一篇」——也用于拦截「用 AI 一次重写全站」的大爆炸诱惑。

推荐路径：

1. **三维盘点**：漂移度（对照当前代码/行为）× 触达度（流量/入口位置/链接入度）× 误导度（错误导致的代价）（[AW-2]）。
2. **四象限 triage**：高误导×高触达 → 立即修；高误导×低触达 → 修或删（删掉过时文档比留着更负责）；低误导×高触达 → 排期更新；低误导×低触达 → 归档候选（[AW-2]）。
3. **增量偿还**：分目录/分域迁移，每篇迁完即合、新旧并存期短——禁止「文档重构月」式大爆炸（人工版与 AI 版同禁，[AW-2]/[AW-7]）。
4. **死文档清理官方五步**：渐进推进 → 先删确定错的 → 全员 Keep-or-delete 评审 → 默认删（拿不准按删处理，VCS 留底）→ 迭代多轮（[DG-3]）[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)。
5. **止损优先**：修不完的先挂显式警示横幅（版本对应关系 + 正确入口链接）——错误文档+警示 > 静默错误文档（[AW-2]）；横幅中的版本对应关系须对账，编造「本页对应 v2」是新增错误（[DG-6]）。
6. **反馈信号接入**：搜索零结果词 top N（最沉默最贵的内容缺口信号）+ 轻反馈负分页清单周期汇帐进 triage（[AV-6]）。
7. **修复复验**：修复挂信号基线，下周期复验收敛——修复不复验等于没修（[AV-6]）。

边界条件：无真实用户数据时触达度用结构代理（入口位置/入度/版本关联）；合规/法务留存文档不适用「默认删」。

来源：[官方文档](https://google.github.io/styleguide/docguide/best_practices.html)（Delete Dead Documentation 五步、死文档三宗罪）+ [模型经验]。详见 kb/ai-docgen-workflow.md（AW-2）、kb/doc-governance.md（DG-3/DG-6）、kb/ai-doc-verification.md（AV-6）。

## P-7 AI 腔治理流水线

**场景**：团队文档已混入 AI 腔（总结癖/对称癖/免责癖），要系统性治理而非逐句手改——也用于批量生成前的风格约束设计。

推荐路径：

1. **判型先于去腔**：tutorial 的引导句是教学功能不是腔；reference 零叙事零引导——去腔一刀切会删掉教学功能、产生「无菌无味」文档（[DQ-10]）。
2. **删除测试定位**：删掉这段/这句信息量变化吗？不变即腔（低信息密度的高完成感是 AI 腔共同本质）（[DQ-8]）。
3. **大纲层审查**（结构性 AI 腔）：每节等长、每列表恰三点、每节末尾有总结段即警觉——腔在骨架不止在词汇，逐句去腔结构残留则治理无效（[DQ-8]/[DQ-9]）。
4. **词典 lint 自动化**：免责词/元话语/强调词/模板骨架词（「在本节中」「综上所述」）词典扫描进 CI——人审兜不住词典化机会（[DQ-9]）。
5. **风格样例锚**：2-3 篇人工认可样例作 few-shot 输入每批生成——展示风格，不描述风格（「简洁专业」类描述无效）（[DQ-9]/[AW-7]）。
6. **治理边界**：治理低密度（腔），不治理风格偏好（句式/用词习惯）——过治产生 sterilized 文档（[DQ-10]）。

边界条件：AI 腔谱随模型代际演化，清单非穷尽、需代际重内省（[DQ-8] 标注）；中文场景有英文 AI 腔 + 翻译腔双重叠加问题。

来源：[模型经验]（自我内省 + 观察，无权威源）。详见 kb/doc-quality.md（DQ-8/DQ-9/DQ-10）、kb/ai-docgen-workflow.md（AW-7 风格锚）。

---

取舍说明：多语言 docstring 惯例（[CC-12]）、多版本文档站策略（[DG-5]）等为单领域深展主题，不入本文件；工具具体版本事实归 doc-governance 及对应子域 kb（本文件以类指称书写）。

## 来源索引

- 来源主体：8 个子领域 kb「最佳实践」小节的跨域模式汇总；每场景尾部的「来源」行已就地标注，此处汇总本文件引用的全部官方 URL。
- [官方文档](https://tsdoc.org) / [官方文档](https://typedoc.org) / [官方文档](https://jsdoc.app) — 工具链选型（P-1）
- [官方文档](https://diataxis.fr/map/) — 体系搭建判型锚（P-2）
- [官方文档](https://keepachangelog.com/en/1.1.0/) / [官方文档](https://adr.github.io/adr-templates/) — 联动设计规格锚（P-4）
- [官方文档](https://google.github.io/styleguide/docguide/best_practices.html) — 门禁与文档债治理纪律锚（P-5/P-6）
- 未被上述 URL 覆盖的模式内容均标注 [模型经验]（跨域工程实践归纳）。
