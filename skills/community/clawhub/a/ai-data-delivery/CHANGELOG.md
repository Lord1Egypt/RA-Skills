# Changelog

## 0.3.10

- 3D 关系图与 2D 编辑器共用浅色背景和青绿色选中态。原文和标识按需展开，先看业务含义和直接关系。触屏提供双指缩放提示。
- 首次安装可运行 `python scripts/smoke.py` 实测导入、草稿导出和离线读取。中英文入口集中说明常见错误、离线依赖安装及真实输出。分发包包含 `LICENSE.md`。
- Updated the historical guides for public sharing. Maintainers can scan a Git tree, ZIP and release notes with an external private term list using `maintainer/privacy_check.py`.

## 0.3.9

- 同名对象可按领域、范围与身份区分。关系支持搜索和翻页，高连接对象可展开全部直接邻居。缩放和窄屏时会重新排布标签。
- 指标的包含与排除范围可和依据原文对照。填写“无排除条件”而引文明确排除记录时，系统拦截确认和正式交付，并允许保留草稿。

- 从编辑器或 Agent 保存回执打开变更对象及其直接关系的 3D 图。支持按修订离线保存 HTML，也可主动浏览全量图。
- Explore a verified semantic package in an offline HTML file. 2D editing and SVG handoffs keep their existing entry points.

## 0.3.8

- 导入时定位缺逗号、错误主键和重名列，保留扩展字段类型，区分带点的表名和库表限定名。GBK 文件可显式选择编码重试。
- 无外键或少外键的库可用 `relation-hints` 查看字段线索与来源。确认、按范围导出及离线复核都会检查物理连接字段，草稿保留未决问题。
- 在同一画布上建对象、选两端连线，保存前可按一句话核对关系、交换方向。普通对象只填名称就能保存草稿。
- 首次导入表结构先显示表和外键。表内字段可以展开、搜索、逐个定位，参与独立业务关系的字段保留在图上。
- Bring the graph into the first viewport on desktop and narrow screens. Search for an object, inspect its neighbors, and use the same editing controls in full screen. Keyboard users can pick both ends of a relationship and cancel with Escape.

## 0.3.7

- Material tasks accept a temporary question or explicit roots, explain source recommendations across jurisdictions and retain explicit full-model access.
- Show the changed relation in the local editor or generate an immutable, revision-specific graph image from the CLI. Trace a directed path across definitions and relationships in an offline package, with evidence pointers and disclosed gaps.
- Preserve a reviewed same-name distinction when only the locator of the same quoted source changes. Compare an optional independent grain before writing a metric and surface duplicate-counting risks in bound calculations.

- Install the graph editor, selected-catalog reader, offline reader and one transport example. Additional industry exercises, database profiling and online evaluation stay in the source repository.
- Follow DDL parsing progress and open the changed graph or candidate review from a CLI receipt. Nodes distinguish source type and review status. Invalid focus links return to the overview with a message.
- Compare selected materials side by side through the local Agent task. Confirmation checks declared inference and conflicts. Resolving a recorded dispute preserves the original claims and the operator's decision. Same-name assets can keep distinct meanings through the CLI.
- DDL identities repeat across fresh projects. Batch retirement is atomic, retries preserve the original result, TLS failures have actionable diagnostics and rejected imports roll back their attachments.


## 0.3.6 — 2026-11-18

- Follow saved changes in the open local graph without replacing an in-progress form. Share a focused view, create objects or relations directly, and attach exact source passages.
- Plain model exports include all active assets when no roots are selected. An explicitly scoped question still cannot expand to the whole model.
- Keep source quotations and summarize large global inventories and warning lists. The CLI options `--full-scope` (reader) and `--full-output` (authoring) retain verbose access.
- **CLI migration:** updating existing asset IDs now requires `--revision N` from the read used to prepare the edit. New IDs do not. Reconcile changes on conflict.
- An added paragraph in a text/Markdown source that retains the previous paragraphs triggers review of cited definitions. Existing snapshots stay immutable. Read applicability using `decision`; completeness alone is insufficient.
- [Verification and limits](https://github.com/franklinxkk/ai-data-delivery/blob/v0.3.6/references/v0.3.6-release-validation.md).

## 0.3.5 — 2026-11-18

- Why: cross-industry trials exposed incomplete task dependencies, repetitive per-asset edits and avoidable reader retries.
- Authoring: atomic arrays on the existing `edit --file` path; explicit confirmation, evidence, revision conflicts, rollback and operation receipts remain guarded. `state --summary` discovers identities without full history.
- Handoff: read-only `inspect --id` highlights omitted mappings, relations and join keys, unresolved states and changed source evidence. Suggestions do not silently expand scope or confirm meaning.
- Reader: paged multi-asset `sources` with deduplicated evidence and explicit missing targets; paged, scope-filtered term discovery on no match; clear page identity coverage without claiming business completeness.
- Guidance: one short business-modeling path, source-supported aliases, explicit secondary-table dependencies and reuse of existing confirmation authority. CLI and optional editor retain one canonical graph.
- Scope: no embedded model, business-query executor, new service, industry policy defaults or migration. Published 0.3.4 remains unchanged.
- Validation: [actual checks and remaining boundaries](https://github.com/franklinxkk/ai-data-delivery/blob/v0.3.6/references/v0.3.5-release-validation.md).


## 0.3.4 — 2026-11-17

- Why: first use required too many management steps, and question handoffs lacked physical dependencies and a clear execution boundary.
- What: derive snapshot/model/task-bound query_control.json; add the control reader, strict recomputation, explicit metric query bindings and common dependency/impact coverage. Preserve zero-hop single-table queries, typed NULL/false/zero and offline freshness uncertainty.
- Fix: bind equipment fields, rewrite bindings on identity merge, withdraw outdated/in-flight handoff links, disclose known newer source revisions, and avoid treating internal preview packaging as a business draft.
- Tool workflow: CLI-first DDL/catalog draft initialization in an empty graph; model export without a question or server; optional editor opens directly in the right graph view with three primary tools. Existing models and candidate review remain protected.
- UX: shorter bilingual quickstart, compact editor shell, readable optional query bindings and narrow-screen navigation. Questions and acceptance stay optional.
- Reader: `brief` combines saved question/context/control/evidence pointers; ordinary search uses the same Unicode normalization. No implicit execution or evidence-read claims.
- Packaging/security: reproducible ZIP, actual capability declaration, bounded subprocesses, loopback-only editor and exclusive occupied-port protection on Windows.
- Scope: no production executor, general JOIN compiler, MCP server or automatic migration. Old 1.0 packages remain readable; new question packages use 1.1. Metadata and Neo4j adapters remain available.
- Validation: see [actual evidence and limits](https://github.com/franklinxkk/ai-data-delivery/blob/v0.3.6/references/v0.3.4-release-validation.md); [research and expert-advice decisions](https://github.com/franklinxkk/ai-data-delivery/blob/v0.3.6/references/v0.3.4-design-review.md).

Versioning: keep published tags unchanged; continue from `0.3.0` with patch increments (`0.3.1`, `0.3.2`, …). Unreleased previews use `-dev`. / 版本约定：保留已发布标签，后续默认递增补丁号，开发预览加 `-dev`，不重写历史版本。

## 0.3.3 — 2026-11-14

- Add explicit host CLI review/edit with shared revision, provenance and rejection guards. / 新增宿主候选核对与维护命令，复用修订、证据和拒绝守卫。
- Document exact confirmed property keys and local HTTP session discovery. / 补齐确认属性的准确字段与本地接口会话获取方法。
- Distinguish definition applicability from data cutoff in bilingual guidance and the question form. / 在双语说明和问题界面区分定义适用日期与取数截点。
- Recheck the complete dependency scope against the requested definition date on every confirmed question handoff, including after prior publication. / 每次确认问题交付均重检定义日期及完整依赖，修复首次发布后可绕过有效期检查的问题。
- Show catalog column/table names before shared connection prefixes in graph nodes; retain full names in details. / 图谱节点优先显示实际字段与表名，详情仍保留完整身份。
- Preserve directed `mapping` edges in Neo4j alongside relation edges, complete asset JSON and dependencies. / 修复 Neo4j 遗漏 mapping 有向边，继续保留完整资产与依赖。

## 0.3.2 — 2026-11-14

- Add optional SQLite, PostgreSQL and MySQL catalog-only connectors with named environment credentials, explicit table scope and bilingual workbench/CLI controls. / 新增三种数据库只读元数据连接、凭据变量、明确选表及双语入口。
- Reuse evidence-linked candidate review; trace catalog changes to dependent questions, preserve unresolved candidates, and require current regression before confirmed publication. / 复用候选核对，定位问题影响，保留未核对候选，发布前重检结构与回归依据。
- Allow explicitly enabled nonunique-index-only synchronization of untouched physical definitions; keep identity, mapping and business changes under review. / 可授权机械同步非唯一索引，其余身份、映射及业务变化需核对。
- Export verified snapshots as Neo4j CSV and fixed Cypher, retaining directed relations, stable identities, full JSON and evidence in isolated snapshot namespaces. / 新增可导入 Neo4j 的文件包，保留方向、身份、完整语义与证据，隔离不同快照。
- Add a runnable metadata exercise. Pre-1.0 format compatibility is not guaranteed. / 新增可运行元数据练习；1.0 前不承诺旧格式兼容。

## 0.3.1 — 2026-11-13

- Unify question discovery with safe rule/metric/scope search; fix relative cross-domain output paths. / 统一问题入口和规则、指标、范围检索，修复四域样例相对路径。
- Add explicit question criteria, operator observations and stale-evidence checks; trace source/definition changes to affected questions. / 新增问题验收条件、人工记录及过时检查，沿依赖定位来源／定义变化影响。
- Add optional snapshot-bound question handoff and progressive context/evidence reading, with bilingual UI and guides. / 新增绑定快照的问题交付及摘要／完整依据读取，保持双语界面和说明。

The question-driven foundation below was first submitted in `ab4be18` on 2026-11-12. / 以下问题驱动基础于 2026-11-12 首次提交。

- Start from a saved business question, expected examples and selected definitions; inspect task-specific dependencies and gaps without claiming an answer or executing data/actions. / 新增业务问题入口、保存重开、预期线索及只读准备检查。
- Reuse existing transactional candidate review, scope-aware publication and offline packages. Show meaning, conditions and evidence before detailed editing fields. / 复用原候选核对和发布，先展示业务含义，详细配置收起。
- Add scenario-aware host tasks and `semantic_read.py resolve --question`; explicit meaning selection produces required context with evidence and execution boundaries. / 宿主任务可聚焦问题，Agent 可从问题发现候选、明确选择后读取上下文。
- Preserve source dispositions, optimistic concurrency and retry receipts. Restore scoped delivery after reload and refuse accidental empty-to-all expansion. / 保留处置与事务合同，修复范围交接及冲突恢复。
- Fix typed scope matching for zero, false, null and missing keys; shorten bilingual instructions through relevant references. / 修复范围类型匹配并精简双语入口。
- Exercise traffic, agriculture, university and finance semantics with 32 synthetic questions and 54 assets; fix short Chinese business terms missing compound labels. / 新增四域合成问题与反例，修复“批次怎么追溯”漏掉“产品批次”候选。
- Export confirmed objects/relations to OGS 1.1.0 with explicit per-asset coverage and opaque semantic/evidence preservation; audit actual roundtrip losses. No database mapping, import or rule execution is inferred. / 新增有覆盖报告的 OGS 离线投影和往返损失检查。
- No embedded LLM, production query gateway, authorization service or action executor. Existing v0.3.0 assets remain unchanged when scenarios are added. / 不增加嵌入模型或生产执行能力。

## 0.3.0 — 2026-11-09

- Add English and Simplified Chinese skill instructions, README, workbench UI and guides; preserve original knowledge when switching language. / 新增中英文技能、说明和工作台界面，切换不改写领域知识。
- Add an executable equipment-loan semantic exercise: text + DDL, explicit review, graph maintenance and independent Agent consumption. / 新增可直接运行的设备借用建模练习。
- Publish bilingual human-review pages and reader instructions; show real graph screenshots and an input-to-answer example. / 交付阅读页及调用说明双语化，展示真实图谱及完整案例。
- Fix graph double-click editing after selection redraw and improve English node labels. / 修复选中重绘影响双击编辑，改善英文节点换行。
- Do not treat different asset kinds (such as a business object and its physical table) as mergeable duplicate identities; same-kind conflicts still require review. / 不把不同类型的同名对象误判为可合并身份；保留同类型冲突检查。
- Pre-1.0 projects and formats remain incompatible by default. / 1.0 前仍不承诺旧项目与格式兼容。

## 0.2.3-dev — 2026-11-09

- 修复分项适用范围在界面编辑时被转成字符串的问题，按分项维护并保留嵌套值和类型；修正上下文末页仍提示继续取页的诊断。
- 规则条件、要求、指标口径、业务范围及明确待补问题可检索，CLI返回命中字段；图谱搜索同步覆盖。
- 新增独立 Agent 的 describe/context 入口，一次返回必需依赖、业务范围、出处、缺口和只读能力；业务关系与定义引用分开。
- 当前请求与整包完整性分开，身份冲突返回触发词与具体候选；明确业务未知、日期适用和分页，不默认补齐。
- 来源登记范围随证据保留；建模与交付说明明确保留原文范围及禁止条件，共享范围规则参与子图依赖闭合。
- 新增可维护的业务待补问题；不增加数据库连接、HTTP/MCP服务或动作执行器。

## 0.2.2-dev — 2026-11-09

- 图谱自动布局改为基于关系拓扑和画布比例选择分层或紧凑布局，减少交叉；完整保留业务关系与去重后的定义引用。
- 新增正交避障、关系标签换行和碰撞避让，标签不压节点；专注模式充分使用屏幕，详情可收起。
- 手动拖动后重新布线，首次拖动或固定时保存整幅布局；自动布局可撤销，失败保留原坐标，异步计算不会写入已切换的视图。
- 本地随包提供固定版本 ELK 及其许可证，无运行时 CDN 或外网依赖。

## 0.2.1-dev — 2026-11-09

- 修复指标提升截取部分条件、未知字段或枚举仍输出可合并操作的问题；不支持的完整表达式明确阻断。
- 修复金标准缺失期望仍写入、只读结构检查意外创建数据库的问题。
- 修复源码 mock 目录越界和链接路径风险；通用服务重建与进程管理迁入 maintainer，可执行 mocks 同时移出安装包。
- 明确 live 评测发送对象和下游边界，拒绝在线/离线混用及歧义引擎 URL；补齐能力声明并固定运行依赖。
- 修复画像输出覆盖源数据库和指标公式来源表冲突仍可合并的问题。
- 新增展开画布、适应画布和相关连线突出显示；扩大默认节点间距，改善关系箭头落点。
- 1.0 前不保留旧 scripts/rebuild.py 和 scripts/_process.py 调用路径。

## 0.2.0-dev — 2026-11-09

- 新增知识材料、候选核对、语义图谱、交付与调用、项目历史主线；原数值工具保留为可选入口。
- 新增统一语义资产、稳定身份、逐项原文依据、来源内容修订及独立提取记录；支持文本、DDL、CSV/XLSX、DOCX、文本 PDF、JSON/YAML 材料。
- 新增宿主任务与候选 CLI；候选经操作者核对后整组写入，支持增量融合、拒绝重放、来源变更复核、合并与分离、停用和安全撤回。
- 新增图谱拖动、业务连线、详情编辑、搜索与邻域、表格视图；布局与语义分别保存。
- 新增固定语义 ZIP、依赖闭合、草稿缺口、人审页，以及无需原项目的只读 Agent 查询与来源接口。
- 修复本机服务被浏览器空闲连接阻塞、附件下载不稳定、旧依赖候选覆盖人工修正，以及来源原文未删但新增例外未触发复核的问题。
- 提交操作使用持久回执；浏览器恢复时先查询结果，不因回执丢失自动重复提交。
- 1.0 前不承诺旧项目、旧模型或命令兼容；`start --ddl/--model` 现在登记材料与候选，不直接生成已确认图谱。

本版不内置大模型、OCR、实时实例图或通用 SQL/规则执行器。语义确认与原有数值执行准备分别维护。
