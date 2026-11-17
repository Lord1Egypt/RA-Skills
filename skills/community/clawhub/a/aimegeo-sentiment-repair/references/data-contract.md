# 纠正记录合同（schema_version: 1）

供 Agent 完成语义分析和写作后使用。脚本不推断事实，不抓网页，也不验证来源真实性；它检查关联、逐字摘录、证据类型和日期边界。所有对象均拒绝额外或缺失字段，防止把情绪分、未执行的检测结果或错误字段静默导出。最小可用记录见 [资料不足输入](../examples/insufficient-facts/input.json)，完整双语记录见 [成功输入](../examples/success/input.json)。

## 顶层

| 字段 | 约定 |
| --- | --- |
| `schema_version` | 整数 `1` |
| `brand` | 产品/品牌名，非空文本 |
| `as_of` | 本次核对日期，`YYYY-MM-DD` |
| `mode` | `case` 真实输入；`illustrative` 教学资料，导出FAQ会标示 |
| `sources` | 产品事实来源数组，允许空数组 |
| `observations` | 回答/质疑记录，至少一条 |
| `claims` | Agent 拆分、核对并写好的断言，至少一条 |
| `retests` | 待执行的复测/补充问题，至少一条，覆盖所有断言 |

每种数组内 `id` 唯一。未取得的信息用 `null`，不用空文本、“未知”假链接或零值代替。教学资料不能标为真实输入；真实个案不能使用 `illustrative` 证据。

## sources：事实来源

每条恰好有 `id`、`title`、`locator`、`content`、`provenance`、`scope`、`effective_from`、`effective_to`。

- `title` 是文档名，`locator` 是用户提供的文件/段落说明或已取得的真实 URL；不要求存在网站。`content` 保存用于核对的原文。
- `provenance`：`user_provided`、`collected` 或 `illustrative`。用户粘贴的产品政策不自动升级成外部核实资料。
- `scope`：`current` 当前适用、`historical` 历史资料、`uncertain` 时效不明。由 Agent 根据产品、套餐、版本和用户说明判定，程序只检查日期一致性，不能证明这个判断正确。
- `effective_from` / `effective_to`：已知的生效起止日期，均可为 `null`。不知道生效起日但用户明确“这是当前说明”，可以 `current` + 两个 `null`，在答复注明信息来源；不要伪造发布日期。当前资料不得尚未生效或已经失效，历史资料已知的止日须早于 `as_of`。

仅有“现在免费”不能外推永久免费、全部增值功能免费或所有地区适用。历史状态有可靠版本关系但无日期时，可保留空日期并在判定理由写清版本依据；没有历史依据就用 `contradicted`，不能用 `outdated`。

## observations：原始记录

每条恰好有以下字段：

| 字段 | 值与约束 |
| --- | --- |
| `id` | 唯一文本 ID |
| `kind` | `ai_answer` 或 `customer_question` |
| `status` | `provided` 用户提供；`collected` 实际采集；`simulated` 模拟；`not_run` 未运行；`query_failed` 失败 |
| `text` | 原文。真实输入/模拟必须有文本，未运行/失败必须为 `null` |
| `question` | 原始提问，未提供时 `null`，不得自行补造原题 |
| `platform` | 已知平台名，否则 `null` |
| `observed_at` | 已知回答/采集日期，否则 `null`，不能晚于核对日期 |
| `native_citations` | 原生引用对象数组（每个有 `label` 和 http(s) `url`），或 `null` |
| `citation_capture` | `complete` 完整、`partial` 部分、`not_available` 未取得 |
| `error` | 失败原因；仅 `query_failed` 为非空文本，其他状态为 `null` |

`collected` 必须有平台、日期和原始提问；`provided` 可只是一个未注明平台的粘贴片段，不能写成本站已独立查询。客户质疑、模拟、未运行、失败的引用一律为 `null` / `not_available`。真实 AI 回答的部分引用要求非空列表；未取得引用为 `null`，只有完整回读确认无原生引用时才可 `[]` + `complete`。正文链接不自动变成原生引用。

仅分析成功取得的原文。可以同时记录失败/未运行的平台，但断言不得依附无回答的记录。统计只覆盖提供/采集的真实AI原文，不包含客户问题、模拟、失败、未运行；任何真实回答引用不完整时，汇总引用总数保留 `null`，不外推全平台数量。完整引用的总数按各回答的原生引用条目累计，不表示去重网站数。`baseline_summary` 不表示情绪、提及率、收录或发布结果。

## claims：Agent 的核对与答复

| 字段 | 约定 |
| --- | --- |
| `id`、`observation_id` | 断言 ID 和原文记录 ID |
| `quote` | 原话中的连续逐字摘录，可包含更长的上下文 |
| `proposition` | Agent 提炼的单一说法，保留否定、条件、范围；疑问不当作事实 |
| `verdict` | `accurate` / `outdated` / `contradicted` / `unconfirmed` |
| `rationale` | 结合语义、来源、范围解释判定，不能只说“命中了负面词” |
| `evidence` | 证据数组，每项只有 `source_id`、`quote`、`relation`；摘录须逐字存在于来源 |
| `faq_question` | 用户会问的具体问题，每条围绕该断言撰写 |
| `public_answer` | Agent 写好的完整公开答复，导出时原样使用；不得有占位句或虚构事实 |
| `repair` | 只有 `priority`（P1/P2/P3）、`location`（具体位置）、`action`（具体修改动作） |
| `needed_information` | 待补的关键资料数组；`unconfirmed` 至少一项 |

`relation` 是 Agent 的语义判断：`supports` 支持原说法、`contradicts` 反驳原说法、`historical_support` 曾经支持原说法。

- `accurate` 至少关联 `current` + `supports`，保留真实限制。
- `contradicted` 至少关联 `current` + `contradicts`。
- `outdated` 同时关联 `historical` + `historical_support`、`current` + `contradicts`。
- 同时有当前支持和当前反驳且未解开范围冲突时，只能 `unconfirmed`；保留冲突证据和要问的问题。
- `unconfirmed` 允许没有证据，也可记录相互冲突/时效不明的证据；公开答复仍须谨慎，程序不能从文本判断是否强行翻正。

CSV 中保留关系与摘录，FAQ 仅转换已写好的问答，不把内部判定理由硬塞成广告或对用户的解释。以公式起始字符开头的 CSV 单元格会加单引号，避免表格软件执行公式。

## retests：尚未执行的计划

每项恰好有 `id`、`claim_ids`（非空断言ID数组）、`kind`、`baseline_observation_id`、`question`、`expected_checks`（非空检查点数组）。

- `kind: same_question`：必须有基线ID，`question` 逐字等于该记录的原始提问；关联的断言都来自这条基线。
- `kind: follow_up`：原题缺失时写补充验证问题；基线ID可以 `null`，不要冒充同题。
- 检查点描述要观察的事实、限制及引用，不把“必须给出正面推荐”当正确结果。输出自动标记 `status: not_run`、`answer: null`、`native_citations: null`。

实际复测时另外保存日期、平台、可用模型/地区设置、完整回答和原生引用，保留本次基线，不覆盖成新回答。只有采集后的数据才能比较同题变化；只有用户明确给出的提及判断与统计口径才能描述提及，不能从本技能的断言数推算品牌情绪指数或收录率。

## 执行与失败

```sh
python3 scripts/repair_bundle.py check --input examples/success/input.json
python3 scripts/repair_bundle.py export --input examples/success/input.json --output-dir demo-delivery
python3 scripts/repair_bundle.py check --input examples/failure/input.json
```

成功退出 `0`，stdout 为包含断言分类数与基线状态的 JSON；业务/输入错误退出 `2`，stderr 为错误 JSON。输出目录必须不存在，脚本不覆盖既有交付；先验证全部记录，再暂存并一次生成三份文件，错误记录不创建交付目录。缺证据示例应返回 `evidence_required`。导出的复测 JSON 是计划，不能重新作为输入记录直接读取。
