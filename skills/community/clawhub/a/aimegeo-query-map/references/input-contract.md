# 本地问题地图输入协议

这份协议用于可选的 `scripts/map_queries.py`，语义判断由 Agent 完成。脚本不从业务介绍自动生成问题、不做向量聚类、不读取文章路径或访问来源URL。无需导出时，直接按相同业务字段交付文本即可。

最完整的可运行输入是 [五篇教程样例](../examples/success/input.json)；只给业务介绍时参考 [精简输入](../examples/minimal-input.json)。JSON使用UTF-8；允许文件头BOM，禁止重复键和未支持字段，以免信息被静默覆盖或丢弃。

## 根对象

| 字段 | 含义 |
| --- | --- |
| `business` | `description`、`audience`、`goal` 为非空字符串；`inventory_status` 见下表 |
| `articles` | 文章数组，可为空 |
| `questions` | Agent 标注的问题数组，至少一题；每个原始说法各占一条 |
| `answer_records` | 可选，只保存用户已给的回答记录，不触发查询 |

库存状态：

| `inventory_status` | 何时使用 | 无关联文章的问题 |
| --- | --- | --- |
| `unprovided` | 没有拿到文章材料；即使用户说“已有5篇”也适用，`articles` 为空 | 覆盖未知 |
| `partial` | 只有部分文章、标题或节选，或未确认库存完整 | 覆盖未知 |
| `reviewed` | Agent 已读到当前库存的全部文章全文，包含已确认没有文章的空库存 | 主题缺口 |

`reviewed` 是 Agent 对输入完整性的判断，不是脚本替用户保证完整。全部文章均须有 `full_text` 材料才能使用该状态。不得把漏掉的5篇文章登记成已核对的空库存。

## 文章条目

每条包含 `id`、`title`、`material`、`text`、`source`。

- `id` 唯一；`title`、`source` 非空。来源是用户材料的定位文字或其已提供URL，不是抓取指令。
- `material` 为 `title`、`excerpt` 或 `full_text`。
- 仅标题的 `text` 必须为 `""`，其他两种为所提供原文，不用 Agent 摘要冒充全文。
- 用节选判断单题已覆盖时，应确保该节选足以回答整个答案范围；不能用它判定全站没有其他内容。

## 问题条目

| 字段 | 标注要求 |
| --- | --- |
| `id`、`question` | 唯一原题ID及完整说法，不能只有标点 |
| `merge_key` | Agent 确认同义问题的共同键，使用稳定短名 |
| `audience`、`entity` | 具体受众及产品/类别实体 |
| `intent` | `information`了解、`navigation`导航、`operation`操作、`troubleshooting`排障、`comparison`比较、`decision`决策之一 |
| `theme`、`scope` | 内容主题及这道题真正需要回答的范围 |
| `origin` | `{ "kind": "agent_hypothesis", "source": "Agent依据业务介绍推导，待验证" }`；kind也可为 `user_question` 或 `model_simulation` |
| `facts` | 至少一条 `{ "need": "免费额度及适用日期", "status": "missing", "source": "" }` |
| `format` | 能满足该题的内容形式，如撤权检查清单、决策表、已有教程入口 |
| `next_step` | 一个具体动作，避免仅写“优化内容” |
| `impact`、`impact_reason` | `high`、`medium`、`low` 及业务理由，不是测量或流量评级 |
| `article_links` | 数组，可为空；结构如下 |

来源状态：`user_question` 表示输入中已有原题，不表示真实需求已被研究证实；来源如果是演示资料，要原样说明。Agent生成或推演的提问使用另外两类，不能改成用户调研结果。

事实的 `status` 为 `available` 或 `missing`。`available` 须有非空来源，表示输入中已有可用资料，不代表外部独立核实；`missing` 的来源必须为空。同一归并组里，同一事实不能同时可用和缺失，应先解决冲突。

文章关联示例：

```json
{
  "article_id": "A1",
  "coverage": "partial",
  "evidence": "保存后回到账号列表核对昵称与平台，再创建内容任务。",
  "reason": "已有身份核对步骤，但没有撤权步骤"
}
```

`coverage` 可为 `full`、`partial`、`unknown`。前两者需要非空逐字正文证据，且不能关联只有标题的材料。`unknown` 允许证据为空，但理由仍须明确。脚本能验证逐字出现，不能验证答案是否充分；Agent需审核完整语义。

## 归并与优先级的确定性规则

同一 `merge_key` 内，`audience`、`entity`、`intent`、`scope`、`theme` 必须逐字相同；如确为同义，先统一这些语义标注再分组。脚本保留所有ID、不同说法、来源、事实、形式与下一步，不丢弃重复条目的来源。

每组的 `origins` 按输入顺序逐条保留 `question_id`、`question`、`kind`、`source`。`question_id` 对应输入的 `id`，`question` 保留完整原文（含空白、标点和换行），`kind`、`source` 对应该条输入的 `origin`。例如成功样例中的一条记录为：

```json
{
  "question_id": "Q01",
  "question": "免费版能管理几个账号，有哪些平台和功能限制？",
  "kind": "user_question",
  "source": "演示输入的问题清单第1条"
}
```

`variants` 仅汇总去重后的不同说法；同文不同ID的记录仍各自在 `origins` 中保留。CSV的“问题依据”列同样逐条关联ID、来源类型、来源与原文，完整结构可从 `map-audit.json` 回读。

归并键由 Agent 决定。脚本额外识别Unicode规范化、大小写、空白和标点差异形成的字面重复：相同语义标注却分到不同键时会报 `DUPLICATE_SPLIT`，不会自动猜测该如何归并。不同语义范围的同一字面问题允许分组。

覆盖取所提供证据中的最强等级：`full` → 已覆盖；否则 `partial` → 部分覆盖；否则有未知关联或库存未完整核对 → 覆盖未知；剩余才是主题缺口。每个等级只描述输入文章。

所有必要事实可用才视为资料齐备。先处理事实缺失、再处理覆盖未知、再复用已有覆盖；余下高影响缺口为P0，其他缺口为P1。已覆盖且资料齐备为P2。同级按业务影响、归并键稳定排序；不使用问题重复次数或搜索量参与排序。

## 可选回答记录

仅用于已有资料的状态保留，不属于检测执行器。每条包含下面全部字段；没有现有回答资料时直接省略整个数组。

```json
{
  "id": "V1",
  "merge_key": "free-limits",
  "status": "not_run",
  "platform": "用户希望后续验证的平台",
  "prompt": "免费版能管理几个账号？",
  "answer": null,
  "source": "",
  "captured_at": null,
  "native_citations": null,
  "mentions": null,
  "error": null
}
```

| 状态 | 必需条件 |
| --- | --- |
| `simulated` | 有假设回答，error为null；提及、原生引用为null |
| `not_run` | 回答、提及、引用、错误均为null |
| `query_failed` | 有具体error；回答、提及、引用均为null |
| `observed` | 已提供回答原文、记录来源、带时区的ISO时间；error为null |

`captured_at` 非空时一律使用带时区的ISO 8601时间，如 `2026-10-19T10:00:00+08:00`。`observed` 的提及可为回答中实际出现的字符串数组，原生引用可为 `{ "url": "https://example.org/page", "label": "界面显示的引用标签" }` 数组，也都可为null。URL格式检查不证明引用真实性，必须由输入原生引用记录支持；手工识别到的普通超链接不能登记为原生引用。

空数组仅表示输入记录中已检查且未见提及或引用，null表示未知或未采集。脚本不会把null改成空数组，不计算引用率，不判已收录；输出中的“已提供回答记录”也不宣称本技能运行过模型。回答记录状态保留在 `map-audit.json`，CSV仅显示状态，避免把原文推演混进结果摘要。

## 输出与失败

```bash
python3 scripts/map_queries.py input.json --output-dir result
```

成功退出0，标准输出为含归并与覆盖统计的JSON；结果包括中文CSV（UTF-8 BOM，便于表格软件打开）和保留标注来源的 `map-audit.json`。CSV中可能触发表格公式的文本单元格加前导单引号，JSON保留原文。周计划由Agent撰写，不由脚本套模板。

输入、证据或状态校验失败退出2，标准错误输出 `{ "ok": false, "code": "错误码", "error": "原因" }`；校验阶段不创建输出。已有结果时报 `OUTPUT_EXISTS`，不会覆盖。缺少CLI必需参数由argparse返回退出2及用法。文件写入异常也返回退出2，应检查指定输出目录权限后选择合适目录，不修改宿主配置。
