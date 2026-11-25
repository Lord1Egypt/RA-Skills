# 固定语义包与离线调用

> **0.3.4:** question handoffs use semantic-package/1.1 with derived query_control.json; start with semantic_read.py --package PACKAGE brief (which includes control). Knowledge-only/old 1.0 packages remain readable and return NO_CONTROL. 问题包新增快照绑定的控制单；仅供解释或明确阻断，不授予查询权限。[Contract / 调用合同](query-control.md)。

本入口交付对象、术语、属性、关系、指标、规则及其依据。术语和规则可以没有数据库或可执行 SQL。工作台生成 ZIP；消费方只需这份 ZIP 或解包目录，以及本工具的只读 CLI，不需要原项目 SQLite、原工作台会话或模型服务。

`model.json` 是包内唯一语义定义。图形查看、文件导出和 CLI 使用同一资产 ID、方向和来源。包中内容只是知识与执行说明；规则是否执行、数据是否正确，不能由“已确认”或包指纹推出。

## 从文件读取

在本工具目录运行以下命令。把路径替换为实际收到的包；有中文或空格的路径加引号。命令不读取当前目录中未指定的项目，不自动打开来源链接。

```powershell
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" verify
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" describe
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" search --query "营运车"
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" get --id ent_vehicle
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" sources --id rule_maintenance
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" context --id rule_maintenance --intent explain
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" neighbors --id ent_vehicle --direction in --depth 1
```

需要再次交付时，明确选择 ID。输出目录需要已经存在，输出文件不能存在；失败不覆盖已有快照。

```powershell
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" export --id rule_maintenance --out "C:\交付资料\维护规则子图.zip"
```

`--package` 放在命令名前。每次命令标准输出只有一个 JSON 结果；文件损坏、参数错误、未知 ID 等返回退出码 2。正常读取、明确歧义、无匹配或结果截断均返回退出码 0，但调用方必须继续检查 `status`、`complete`、`truncated`，不能只判断进程退出码。

## 包内文件

明确选择“生成本问题的 Agent 包”时，可额外包含 `task.json`：问题、意图、所选身份、范围、日期及验收预期。文件指纹和快照／模型绑定一起核对，私人笔记和人工验收记录不包含。用 `task --detail summary` 读取，再用 `sources` 或 `--detail full` 回查；`resolve/context` 也支持摘要，默认完整。普通语义包仍不带问题。详见[问题交付](question-delivery.md#问题验收变更影响与-agent-交付)。

| 文件 | 内容 |
|---|---|
| `model.json` | `schema_version: "1.0"`、资产列表 `assets`、旧 ID 到存续 ID 的 `redirects`。 |
| `sources.json` | 选中断言使用的来源、具体修订、原文位置和片段。只带这些片段，不能据此声称已带完整来源文档。 |
| `manifest.json` | `format_version: "semantic-package/1.0"`（纯知识）或 `semantic-package/1.1`（问题+控制单）、快照 ID、项目身份、来源项目修订、实际范围、草稿状态、缺口、逐文件 SHA256 及规范化模型 SHA256。 |
| `README.md` | 包内调用及边界说明。 |
| `human-review.html` | 无外部依赖的只读页面，展示同一模型的定义、原始关系方向、范围及来源。 |

包不携带原附件、项目数据库或其他未引用来源片段。源码中的读取器接受上表的知识包清单、加 task.json 的旧问题包，或同时加 task.json 与 query_control.json 的新版问题包；混入文件、重复 ZIP 成员、损坏 JSON、指纹不符或不支持的格式均拒绝消费。指纹验证只证明文件与清单一致，不构成来源认证、电子签名或业务验收。

固定快照不会随工作图谱修改而变化。相同输入产生相同包内容；新内容或新项目修订产生新快照身份。离线始终返回 `is_latest: "unknown_offline"`，不能判断是否已经有更新，更不能撤回已发出的文件。

## 资产及依据

每个资产使用项目内唯一的稳定 `id`。`kind` 支持 `entity/term/attribute/relation/metric/rule/dataset/field/mapping`。资产包含名称、定义、领域、适用范围、别名、知识状态、属性、显式必须引用 `refs`、依据和业务有效期。状态为 `draft/confirmed/needs_review/retired`。

`scope` 描述实际业务范围，例如单一账簿、币种、适用年级、允许的业务形态；“模拟场景”“待用户审阅”只是材料性质，不能代替业务限制。将原文开头、章节和例外中的限制写入适用资产并引用相应片段。共用范围也可建成有依据的规则，通过 `refs` 绑定到消费资产；单资产与子图导出会一起带出。来源的登记 `scope` 随来源元数据保留，`sources` 返回 `source_scope`，但登记信息不自动成为已确认业务规则。

确实尚未明确的业务问题可用 `properties.knowledge_gaps: ["结算完成时点尚未提供"]` 保存，并在资产依据中引用原文。它是已知待补问题，不是默认答案。原文的禁止条件应完整进入规则的 `requirement`；不能仅保留在来源中，或把“不自动决定”弱化为“不自动执行”。工具检查结构、引用和引文有效性，不自动证明 Agent 已理解并覆盖了原文全部限制；仍需对照原文核对。

关系与映射另外保存 `from/to/predicate/relation_type`。反向查看只改变遍历方向，不改原谓词、不生成新业务事实。分类关系不会自动产生继承或推理。按 ID 读取只识别明确 ID 和合并重定向，绝不把同名对象当作 ID 替换。

来源依据使用 `source_id + revision + fragment_id + quote`。确认发布会核对这些身份、原文位置和内容指纹，并检查摘录确实位于指定片段中。人工依据保留 `type: manual`、原话、记录人和记录时间。发布不要求把人工决定假装成外部文档，但缺少依据的声明不能发布为完整确认包。

同一内容修订重新提取时，依据可同时携带 `extraction_id`，指向该次提取的片段。来源修订中的 `extractions` 保留各次结果；包只带实际引用的提取片段。旧依据没有提取 ID 时，可在全部提取中寻找同一片段 ID；若其内容或位置有多种解释，则必须明确提取身份，不能自动换绑到最新结果。

来源更新后仍可保留旧修订依据；是否已复核由资产状态表明。旧原文不会被悄悄换成新片段。读取 `sources` 返回当时的具体修订及摘录，不能声称读取了来源的最新全文。

## 发布范围和依赖

确认包要求范围内每个资产均 `confirmed`，有非空定义、领域、范围及有效依据；未解决冲突、必须引用缺失、需复核或停用依赖都阻止该范围发布。其他无关资产有问题时，仍可单独选择完整资产发布。

共用类型检查还要求：指标明确单位、粒度、包含项、排除项和时间范围；规则明确条件和要求；属性/字段明确值类型。关系检查起终点类型与物理外键字段数量；分类关系不得成环。保存草稿时允许缺少上述内容字段，但结构及明确引用仍需有效。导出草稿会如实保留不完整状态。

草稿可保存候选、缺口和缺失依据，`draft: true`，有缺口时 `complete: false`。读取器会复查包内状态和依据，不仅信任清单上的成功文字。

范围选择规则：

- 在建模项目使用 `knowledge.py export` 时，省略 `--id` 会交付全部在用资产，包括表、字段和物理外键。按业务问题交付时，使用该问题已选的根节点。
- 单独导出物理外键时，工具补齐两端数据表及图中对应的连接字段。字段与完整来源冲突会阻止正式导出，草稿在 `manifest.issues` 中列明原因。来源只覆盖部分字段且无法核实时，包会标明连接键待核实。离线 `verify` 也会根据包内依据检查。
- 顶层 `refs` 以及关系的 `from/to` 永远是必须依赖。递归补齐至引用闭合，循环去重。遇到跨领域或物理资产仍带上定义，不能为了缩图删掉必需内容。
- properties.query_plan 中明确声明的数据集、字段、粒度、规则、映射和所选关系也是必需依赖，始终加入上下文与影响追踪。
- 不自动展开这些依赖的所有邻接关系。因此只选一条规则可以带齐规则所需对象，而不夹带这些对象的无关业务网络。
- `include_execution` 包含已有的 `properties.execution` 块及其 `refs/data_refs` 依赖。默认省略此块，并在 `omitted_execution_ids` 中列明。其他业务属性保留。
- `scope.root_ids/dependency_ids/included_ids` 分别说明根节点、自动补入项和最终范围；`omitted_asset_count` 仅相对于输入模型，不代表整个领域的未知知识数量。

从离线包再导出子图只能使用父包已有内容。父包没有携带执行配置时，不能通过参数凭空恢复它。程序读取这些说明不会执行其中的 SQL、脚本、业务动作或 URL。

## 搜索、日期、关系与完整性

| 调用 | 结果要求 |
|---|---|
| `search --query` | 名称/别名精确匹配优先，再查定义、领域、范围、关系谓词及规则/指标的业务字段（条件、要求、单位、粒度、包含/排除、时间、表达式、值类型、待补问题）。返回 `match_fields` 和候选；不检索执行SQL、审查日志或原文指令。多条匹配返回 `ambiguous`，分页不会隐藏歧义。 |
| `search --domain/--kind/--scope` | 依据调用方明确提供的条件过滤。`scope` 可以是完全匹配的范围文字，或用于匹配范围对象的 JSON 子集。业务范围不是权限。 |
| `search --as-of YYYY-MM-DD` | 未指定日期保留所有有效期。指定日期时排除明确不在区间内的项；缺少任一时间边界的项标 `applicability: unknown` 并保留，不能据此假定唯一答案。日期边界按日包含。 |
| `get --id` | 返回完整定义、状态与依据；提供 `--as-of` 也不隐藏指定资产，只报告是否位于已知区间。 |
| `neighbors --direction in/out/both --depth` | 深度 0–10，只遍历明确声明的关系。返回边原定义、实际正向/反向遍历、节点及其时间适用状态。可重复 `--relation-type` 限定类型。 |
| `sources --id` | 返回具体断言、来源修订、片段及位置。缺失或不匹配标明 `missing/invalid`，不能生成看似有效的引文。 |
| `export --id` | 可重复 ID；递归补齐明确必需依赖，生成新的固定子图包。 |

搜索和邻域支持 `--limit 1..500`、`--offset`；返回 `total/next_offset/truncated`。截断和非首页都不能标记为完整结果。`complete` 只针对本包或本次明确请求范围，并非“整个领域知识完整”。搜索的 `not_found` 只表示包内没有匹配，不能据此断言现实世界不存在该概念。

所有正常结果返回实际 `snapshot_id/source_revision/scope` 和 `package_complete`。`get` 的 `complete/request_complete` 针对该资产及必需依赖，`search` 针对本页命中及其依赖（分页时不完整），`sources` 针对所请求引文；它们不代表整包完整或业务批准。`verify` 仍核对整包；具体未确认状态、身份冲突和触发别名在 `issues` 内返回。包通过完整性校验也不代表规则已执行、观点无争议或本包最新。

## Agent 任务上下文

先用 `describe` 发现工具与只读能力。新增 `resolve --question "业务问题"` 可按名称、别名、定义、范围及规则／指标业务字段推荐候选；即使只匹配一项，也返回 `needs_selection`，不自动认定含义。明确选择身份后，可在同一命令追加可重复的 `--id`，直接取得同源上下文；也可以沿用 `search` 消歧和 `context`：

```powershell
python -X utf8 scripts/semantic_read.py --package "C:\交付资料\交通语义.zip" context --id rule_maintenance --intent explain
```

`resolve` 是词法发现与上下文交接，不是自然语言问答执行器。它返回 `decision`、`next_steps`、`selected_asset_ids`，已选身份时附带 `context`。状态为 `needs_selection`（待选身份）、`no_match`（未匹配）、`context_available`（可读取所选上下文）、`needs_review`（存在含义、日期或分页缺口）或 `requires_execution`（需要实际数据或执行器）。`answer_verified` 始终为 `false`，问题覆盖仍须独立核对。

`resolve` 的候选分页在顶层，已选定义分页在 `context` 内；`request_complete` 只说明上下文结构，不能覆盖业务待决项。`calculate` 需真实输入数据和计算结果，`query`／`act` 需已授权连接或执行器。`domain/scope` 过滤不授予权限；选定根节点不匹配过滤条件会报错，依赖仍保留各自范围。JSON 范围匹配区分零、假、空值和缺失键。完整调用字段与示例见 [Agent 读取指引](agent-reader.md#start-with-a-question)。

`--id` 可重复，输入必须是明确的身份。Python 对应 `package.context(["rule_maintenance"], intent="explain")`。`intent` 可为 `explain/calculate/query/act`；它只描述消费意图，不授予权限或触发业务。默认按整个必需依赖闭包返回，支持 `--as-of`、`--limit 1..500`、`--offset`；不自动扩大成全部邻接网络。

| 返回字段 | 如何使用 |
|---|---|
| `root_ids/required_asset_ids/assets` | 根身份、全部所需身份、本页完整资产。合并重定向只跟随已声明的身份。 |
| `business_scopes` | 每项实际适用范围，与资产定义一致，不仅是ZIP的资产选择范围。 |
| `dependency_edges` | `definition_reference` 为 refs；`relation_endpoint` 为关系端点依赖；`execution_reference` 为随包执行声明的引用。它们不是新推断的业务关系。 |
| `relations` | 本页关系资产保留原始 from/to/predicate，反向查看不改业务事实。 |
| `evidence/source_warnings` | 每项具体断言、修订、片段、位置和提取警告。只带选中的原文，不能宣称已读全文。 |
| `gaps` | 缺依赖、依据、身份复核、有效期未知/不适用、显式待补问题、分页或缺执行能力等原因和下一步。不得把未知补为零或通过。 |
| `package_complete/knowledge_complete/request_complete` | 分别是整包、所需依赖范围、当前实际返回内容的完整性。`request_complete` 也是本方法的 `complete`；分页时为 false。完整返回仍可含已明确记录的业务待补问题，应逐条处理 `gaps`。 |
| `capabilities` | 本读取器能解释知识，给定数据的计算由消费方完成；不附实例数据、不连接数据库、不执行动作，角色定义不授予权限。即使含 execution 声明也不改变这一点。 |

`query/act` 额外返回缺数据连接或缺动作执行器的明确缺口。`calculate` 不声称调用方提供的数据已经核验。日期未知或处于已知有效期外的必需定义保留并给出缺口，不靠删除它们假造完整上下文。分页时根据 `next_offset` 继续并保留之前各页；完整性不等于适用于当前业务、更不等于整个领域已穷尽。

## 程序接入与错误

工作台与 CLI 共用 `workbench.semantic_package`：

```python
content, manifest = build_package(
    assets, sources, project_id="project-id", revision=7,
    asset_ids=["rule_maintenance"], draft=False,
    include_execution=False, redirects={"old-id": "surviving-id"},
)
package = read_package("semantic.zip")
package.verify()
package.search("收入", domain="财务")
package.get("rule_maintenance")
package.context(["rule_maintenance"], intent="explain")
package.sources("rule_maintenance")
package.neighbors("ent_vehicle", direction="in")
subgraph_bytes, subgraph_manifest = package.export(["rule_maintenance"])
```

`build_package` 和 `package_preview` 接受相同输入；后者只返回范围、状态和资产摘要。异常为 `PackageError(ValueError)`，其 `code/details/as_dict()` 可直接用于服务响应，不要只显示泛化“发布失败”。典型错误有 `NOT_PUBLISHABLE`（逐项 issues）、`UNKNOWN_ID`、`HASH_MISMATCH`、`UNSUPPORTED_FORMAT/UNSUPPORTED_SCHEMA`、`PACKAGE_CORRUPT`、`CONTENT_NOT_AVAILABLE`、`OUTPUT_EXISTS` 和 `INVALID_INPUT`。

`validate_semantic_assets(assets, redirects=None)` 是工作台与包共用的结构/类型检查入口，成功返回 `None`，失败抛上述异常；来源依据另由发布与读取共用的依据检查处理。它没有工作台或数据库访问副作用。

当前 CLI 没有编辑、确认、发布项目草稿或执行外部业务的命令。独立消费者不能通过包内角色文字提升权限；对文件的访问依赖操作系统。本期未提供 MCP/HTTP 消费服务。后续适配应复用这些方法，不能再写一套消歧、闭合或状态解释。

针对性验证运行：

```powershell
python -X utf8 -m unittest discover -s tests -p test_semantic_package.py -v
```

测试涵盖独立进程读取、中文/空格路径、来源修订、无数据库术语、同名消歧、时间未知、依赖闭合、关系方向、截断、损坏包、旧快照和只读边界。此类验证是代码与独立进程级证据，不替代工作台真实发布操作或独立 Agent 的业务理解验证。
