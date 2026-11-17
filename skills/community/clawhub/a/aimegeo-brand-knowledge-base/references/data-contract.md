# 整理 JSON 与知识索引约定

输入是 Agent 对真实资料的阅读结果；脚本只做验证、归并和导出。完整可运行输入见 [examples/input.json](../examples/input.json)。所有示例实体均为演示对象。

## 输入顶层

| 字段 | 含义 |
| --- | --- |
| `schema_version` | 整数 `1` |
| `kb` | `id` 与 `name`；增量时必须同时匹配旧库 |
| `as_of` | 本次整理日期，`YYYY-MM-DD`；增量不能倒退 |
| `projects` | 项目的 `id`、`name`；首次至少一个，普通单项目任务可使用业务名建立一个项目 |
| `entities` | 对象，见下表；首次至少一个 |
| `sources` | 本地来源清单；增量可省略已保存的来源 |
| `records` | Agent 完成的原子事实和实际正文；合并旧库后至少有一条 |
| `gaps` | 会影响内容使用的缺口；没有必要缺口可为空 |

未知字段报错，不会静默忽略。数组在增量时可省略，表示保留原记录。ID与 `key` 使用小写字母、数字、短横线或下划线，首字符为字母或数字，最长64字符。日期必须有效，不能以未来采集日期支持较早的整理结果。

## 对象、来源和事实

对象字段：`id`、`name`、`kind`（`company` / `product` / `topic`）、非空 `project_ids`。可选 `parent_id`：产品的父对象是公司，主题的父对象可以是产品或公司。子对象项目范围不能超过父对象。项目和对象元数据同ID不可改变；名称或范围变更应显式建立新对象、迁移使用关系，保留旧对象供追溯。

来源字段：`id`、`title`、`path`、`captured_at`，可选 `url`。`path` 是相对输入 JSON 所在目录的 UTF-8 `.md`、`.txt` 或 `.json` 文件；不接受绝对路径、上级跳转或符号链接。路径用 `/`。原文按字节复制到输出的 `原始资料/`，索引保存 SHA-256、原始相对路径、保存日期和可选来源URL；日期表示输入文件保存记录，不代表第三方核实日期。脚本不会下载URL或访问远程系统。

事实记录字段：

| 字段 | 要求与业务含义 |
| --- | --- |
| `id` | 稳定且不可覆盖；更新正文或证据使用新记录ID |
| `entity_id` | 公司、产品或主题之一，防止把产品参数当成公司事实 |
| `category` | `identity`、`product`、`howto`、`faq`、`trust`、`industry`、`contact` |
| `key` | 对象内稳定属性，如 `delivery_formats`；同属性不得换分类掩盖冲突 |
| `value` | Agent 整理的可比较值，如 `Markdown+JSON`；同义说法先由Agent统一，不依赖脚本猜语义 |
| `text` | Agent 撰写的完整可用正文，保留时间、版本、条件和不确定性 |
| `status` | `supported` 或 `pending`；前者必须有来源，后者可以无来源但不可作为已证实事实 |
| `project_ids` | 非空，且全部属于该对象的项目范围 |
| `sources` | 摘录数组，每项含 `source_id`、`locator`、`quote`；有引用就必须匹配原文 |
| `question` | FAQ 必填，其他分类可选；填写用户实际会问的问题 |
| `supersedes` | 可选旧记录ID数组；仅有来源支持的新记录能替代同对象、同分类、同属性的旧记录。每条新记录的项目范围必须是每条被替代记录范围的子集；替代同一旧记录的全部新记录须合计覆盖其完整项目范围 |

同一条话的不同来源分别建记录；具有相同对象、分类、属性、归一值、项目范围和状态的记录会合并成一个事实。待核实记录与有来源记录分开，避免把未经证实的补充正文升级为可用内容。脚本只对值做 Unicode NFKC 和空白归一，保留大小写；不会做同义词或营销语义判定。不同项目范围不归并；重叠项目中的同属性不同值会标冲突。若一条记录覆盖多个项目，其中一个项目冲突，该条事实整体暂停使用；需要细分时按下文完整拆分，并明确替代旧记录，不能只新增窄范围记录。

原文摘录会检查是否存在，允许空白和 Unicode 兼容形式差异。它无法验证正文是否歪曲摘录、来源是否可信或 `locator` 是否真实，因此 Agent 仍须回读定位与语义。不允许用“文件存在”代替证据核对。

## 缺口与增量

缺口含 `id`、`entity_id`、`project_ids`、`question`、`reason`，可选 `resolved_by`（事实记录ID数组）。每个问题要说明缺失如何影响内容，例如“缺价格，无法写收费比较”，而非要求用户填写无关字段。缺口原问题不可覆盖，后续可用同ID更新 `resolved_by`。每条解决记录须属于同一对象、与缺口项目有交集，全部引用的项目并集须完整覆盖缺口；不要求每条单独覆盖全部项目。例如 A+B 缺口可由 `a-current(A)` 与 `b-current(B)` 联合解决，只引用 A 则因缺 B 而拒绝更新。只有全部引用记录的当前导出状态均为 `supported`、可用项目并集仍完整覆盖时，才显示已解决；旧 `shared-v1(A+B)` 已被替代时不能补足 B。证据转为待核实、冲突或历史时，缺口保留未解决。脚本不判断证据语义是否回答了问题，由Agent核对。

`supersedes` 引用原始记录ID，不能只写归并事实的代表ID而遗漏同组其他来源。脚本不按日期自动替代，也不删除旧材料。循环替代、跨对象或属性替代、扩大或移到旧记录范围以外的替代均失败。单项目完整替代见 [update.json](../examples/update.json) 与 [resolution.json](../examples/resolution.json)。

### 跨项目事实只更新一个项目

旧记录 `shared-v1` 适用 `[project-a, project-b]`，值为 `Markdown+JSON`；只有项目 A 改成 `Markdown+JSON+CSV`，项目 B 保持原值。先核实新约定只适用于 A、B 原值仍适用，再一次导入两条有来源的新记录：

| 新记录 | 项目范围 | 当前值 | `supersedes` |
| --- | --- | --- | --- |
| `a-current` | `[project-a]` | `Markdown+JSON+CSV` | `[shared-v1, a-update]` |
| `b-current` | `[project-b]` | `Markdown+JSON` | `[shared-v1]` |

其中 `a-update` 是已导入但尚未声明替代的 A 新值记录；若尚未导入它，省略该ID并在本次输入中提供第二版来源。每条被替代记录都独立校验覆盖范围。两条新记录合计覆盖 `shared-v1` 的 A、B 范围后，旧记录整体转为 `superseded`；原来的 `project_ids`、正文与来源不变，两条新记录分别为 `supported`。若新记录间仍有同项目不同值，仍标冲突，不因覆盖完整而自动选值。

从本技能目录复现（`split-kb` 使用独立输出目录）：

```sh
python3 scripts/knowledge_base.py build --input examples/project-split-input.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-update.json --output split-kb
python3 scripts/knowledge_base.py build --input examples/project-split-resolution.json --output split-kb
```

中间步骤得到 2 条冲突事实；最后得到 2 条当前可用事实、2 条历史事实、0 条冲突事实。实际输入见[初始跨项目事实](../examples/project-split-input.json)、[局部更新](../examples/project-split-update.json)和[完整拆分](../examples/project-split-resolution.json)。已归并的跨项目事实若有多个 `record_ids`，两条新记录必须显式覆盖全部相关旧记录，遗漏的旧记录仍参与冲突检测。

只有 A 的新记录不足以整体替代尚未拆分的 `[A,B]` 旧记录。以下失败示例在仅导入初始事实后运行，退出码为 `2`，原库不变；错误指出缺少 `project-b`，应补上有来源、保留 B 原值的替代记录。不能通过删改旧记录或改 `key` 绕过它。

```sh
python3 scripts/knowledge_base.py build --input examples/project-split-input.json --output split-rejected-kb
python3 scripts/knowledge_base.py build --input examples/failure-incomplete-project-split.json --output split-rejected-kb
```

同ID的新材料与旧版本不同、引用未知对象或项目、无来源的 `supported`、摘录不存在、路径越界、同ID不同事实、受管正文被手改，均以退出码 `2` 和 JSON 错误返回；业务校验失败不会写入。文件系统中断不具备全库事务回滚，原子替换限单文件，需从保留的资料检查恢复。一个输出目录应顺序更新，不要并发写入。

## 输出索引

`知识索引.json` 保留 `kb`、`projects`、`entities`、`sources`、原始 `records`、`gaps`，另包含：

- `facts`：归并事实；`record_ids` 保留全部原记录，`texts` 保留不同正文，`sources` 保留来源定位。派生状态为 `supported`、`pending`、`conflict`、`superseded`，并有 `document_path`、`conflicts_with`、`superseded_by`。
- `documents`：实际正文路径、对象、分类及事实ID；只生成有记录的类别。
- `gap_results`：缺口及本次是否解决。
- `stats`：输入来源、原记录、归并事实、当前可用事实、冲突、待核实、历史与未解决缺口数量。不是AI可见度指标。
- `managed_files`：受管输出文件的 SHA-256。增量前验证原资料和正文未被改写，避免覆盖人工修改；索引本身不纳入自身哈希。

写作检索顺序为对象 → 适用项目 → 当前状态 `supported` → 原文摘录。`知识库目录.md` 是人读入口，机器索引和正文可分发至任意支持 Markdown/JSON 的工具。交付物中不默认附加任何推广文字。
