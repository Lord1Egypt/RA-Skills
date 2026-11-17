# campaign.json 数据约定（版本 1）

这是可选的结构化交接格式。Agent 负责选题、事实核对与完整写作；`check_campaign.py` 只读取传入 JSON，不打开其来源文件、链接或任何浏览器，不保存、不发布、不调用 AI。Python 3.9+ 标准库即可运行。

最完整的有效输入见 [参展 campaign.json](../examples/qinghe/campaign.json)，无需手工复制空结构。它包含原始示例与后续整批授权，所有数值是策划占用估计，不是现场结果。

## 顶层与字段

| 字段 | 内容与约束 |
|---|---|
| `schema_version` | 整数 `1` |
| `request` | 用户事件原话 |
| `event` | `id`、`brand`、`kind`、`time` 和 `staff` |
| `facts` | 各含 `id`、`key`、`status`、`value`、`source` 的事实列表 |
| `scope` | 所需阶段、渠道、写作模式、选择编号和写作授权 |
| `topics` | 每条含稳定 `id`、阶段、渠道、平台、形式、时间、标题、开场、受众、动作、负责人和关联编号 |
| `shots` | 镜头编号、窗口、起止分钟、参与人员、用途、轻重、状态和替代办法 |
| `faqs` | 问题、答案支持状态、事实编号和待补字段 |
| `drafts` | `topic_id`、完整 `text`、事实、必要事实/镜头和使用状态；仅地图模式可为 `[]` |
| `observations` | 用户提供或实际采集的回答观测；没有运行则 `[]`，不自动生成零引用结果 |

编号均为非空字符串，保留 `01` 的前导零。每类列表内不能重复；不同编号可指向同一事实。脚本校验单个版本内的关联，跨轮编号稳定性仍由 Agent 维护。

## 事实与时间

`facts.status` 可为 `confirmed`、`missing`、`unverified`。确认事实须有非空值和 `source.ref`、`source.excerpt`；来源可以是当前对话、明确的项目文件位置或用户提供的公开材料。来源字段是线索，校验器不会打开它们，也无法独立证明来源真实。未知值不用 0，缺失事实用 `value: null`。未核实资料可以保留值，但不得作为已确认依据。

四个必需确认字段为 `brand`、`event_kind`、`time_raw`、`staff_count`，对应事件的品牌、事件、原始时间和实际人手。`staff_count` 是正整数。画像、行业、营业额都不是运行前置。

`event.time` 包含 `raw`、`anchor_date`、`timezone`、`start_date`、`end_date`。原话必须等于 `time_raw`；未知参考日期、时区和展期用 `null`。脚本不解释相对时间，也不从“下周”推导开展日。若提供确切日期，另有确认的 `event_dates` 事实，其值为完全相同的 `start_date`、`end_date` 对象；日期格式为 `YYYY-MM-DD`，结束日不早于开始日。`anchor_date` 和 `timezone` 仅作背景保留，不会自动使推测日期变成事实。

## 范围、平台包和整批成稿

`scope.stages` 从 `before`、`during`、`after` 中选；`scope.channels` 从 `public`、`moments`、`dm` 中选。覆盖它们的每个组合至少一条；用户只需要某个渠道或只剩展后时就缩小范围，不能为凑全表重新创造已错过的事前。

`scope.mode`：

- `plan`：交地图；`selected_ids: []`，`drafts: []`。
- `selected`：交指定编号全文；`selected_ids` 非空，稿件集合必须完全等于选择集合。
- `all`：交所有选题全文；`selected_ids: []`，稿件集合必须等于所有选题编号。

两个写稿模式都要记录 `scope.authorization` 原话，脚本只能检查非空，Agent 必须核对它确实来自用户，不可替用户造授权。没有三条上限。少稿、多稿、重复稿都失败。

每条 `topic` 还需 `title`、`hook`、`audience`、`action`、`platform`、`format`、`time_label`、`owner`、`publish_conditions`（至少一项），以及 `fact_ids`、`faq_ids`、`shot_ids`。事实引用只能指向已确认事实。平台未知时文本可明确标为建议，不能冒充已连接账号。

`draft.status` 为 `ready_for_review`、`awaiting_facts` 或 `awaiting_capture`。`fact_ids` 指已确认依据，`required_fact_ids` 可指向待补事实；后者未确认时不能标可审阅使用。`ready_for_review` 仍需人工核对接收对象和平台，不是发布回执。校验器会拒绝完全相同的重复正文，但无法证明每篇文案充分、有用或没有改写后的重复，需 Agent 人工复核。

素材依赖分为全需与替代，均只接受本次 `shots` 中的真实编号：

- `required_shot_ids` 保持原含义：其中每项都须为 `captured`，空列表表示没有全需镜头。
- 可选的 `required_shot_any_of` 是列表的列表；每组至少一项须为 `captured`，不同组全部满足才可就绪。省略或 `[]` 表示没有替代组；空组、未知编号、重复编号和非列表的破损组均报错，不用猜测替代关系。
- 两类条件同时存在时都须满足。例如 `required_shot_ids: ["S01"]` 加 `required_shot_any_of: [["S03", "S04"]]` 表示已采集 S01，且 S03/S04 至少一项已采集。仅标 `planned`、`unavailable` 或自造 `available` 状态都不能满足依赖。

样例 05 的朋友圈配图允许匿名问题笔记 S03 **或**可公开实拍 S04，因此使用 `required_shot_ids: []`、`required_shot_any_of: [["S03", "S04"]]`；S05 为可选补充，不列为必需。现场没有提问、S03 不可用时，核对过的 S04 实拍可满足此组；两者都未采集时仍不能标为就绪。具体采用哪份素材及是否符合匿名、授权和内容要求由 Agent 实际回看，JSON 状态不能代替看图。

## 拍摄资源

人员是 `event.staff` 中的 `id` 和 `role`。镜头的 `people` 指向实际人员；`topic_ids` 与对应选题的 `shot_ids` 双向关联，防止交接漏项。

每个 `shot` 还需 `content`、`window`、`start_minute`、`end_minute`、`priority`（`essential`/`optional`）、`status`（`planned`/`captured`/`unavailable`）和 `fallback`。窗口表示不同现场时段，同一窗口内分钟为非负整数，区间左闭右开；前项在 5 结束、后项在 5 开始不冲突。脚本拒绝同人同窗口重叠，无论总人数够不够。不同窗口的现实先后与接待可用性需人工确认。

汇总的 `scheduled_person_minutes` 等于每项占用分钟乘参与人数之和，是拍摄任务预算，不是总工时或实际耗时。把状态改成已采集前，必须实际回看素材；脚本无法代替回看。

## FAQ 与 GEO 观测

FAQ 含 `id`、`question`、`status`、`answer`、`fact_ids`、`missing_keys`。`supported` 有答案、事实且没有缺口；`partial` 有已知部分和待补字段；`missing` 的答案为 `null` 并列出缺口。未知业务不能拿资料标题或别的品牌案例当答案。

GEO 观测的四种状态严格区分：

| 状态 | 必要信息 | 提及 / 原生引用 |
|---|---|---|
| `observed` | `id`、`question`、`platform`、`answer`、带时区的 `captured_at`、`origin`、`evidence` | `brand_mentioned` 为布尔值，`native_citations` 为列表 |
| `simulated` | 编号、问题、平台，可附模拟回答 | 两个实测字段均为 `null`，不入实测分母 |
| `not_run` | 编号、问题、平台 | 两个实测字段均为 `null` |
| `query_failed` | 编号、问题、平台、非空 `error` | 两个实测字段均为 `null` |

`observed.origin` 只接受 `provided_answer` 或 `collected_answer`。`evidence` 定位实际输入/采集的原回答；受控测试数据不能用来声称真实 GEO 结果。`brand_mentioned` 须与回答是否含品牌原名一致；别名或同名歧义需先人工核实，当前脚本不处理这些情况。每个原生引用须含 `url`（HTTP/HTTPS）和 `native_ref`（原生卡片/脚注位置），同一条回答不能重复同一位置与链接。正文出现 URL 不自动变成原生引用。

只统计 `observed` 的回答数、品牌提及回答数和原生引用条目数，不将这三者混成收录率。没有实际回答时两个指标为 `null`；有实际回答且确认无提及/无原生引用时才可为 0。模拟、未运行、失败分别计数，不填成 0 引用。原生引用条目数也不代表其中所有链接都引用本品牌；判断品牌相关引用需要人工读取内容。

## 命令与边界

```sh
python3 scripts/check_campaign.py examples/qinghe/campaign.json
python3 scripts/check_campaign.py examples/failure/campaign.json
python3 scripts/self_test.py
```

校验器向标准输出输出 JSON：成功为 `ok: true` 和汇总，业务失败为 `ok: false` 和带 `code/path/message` 的错误列表。退出码 `0` 有效、`1` 业务或结构不合格、`2` 文件无法读取或 JSON 无法解析。不执行数据里的命令，不读取其来源路径。

self_test 验证样例业务汇总、全批/选稿覆盖、确切日期证据、人物冲突、缺事实/镜头就绪、未知事实引用、FAQ 状态、GEO 状态和隔离目录运行。它不检查图标、根目录 LICENSE、宿主配置或兄弟技能；测试内的受控回答仅验证统计逻辑，不是外部查询证据。
