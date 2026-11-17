# 证据台账格式与导出

输入为 UTF-8 JSON（可带 BOM），`schema_version: 1`。参照完整可运行的 [成功台账](../examples/success/evidence.json) 编辑，不需要任何第三方 Python 包。所有字段均必填，只有下表标明允许为空的值可留空。脚本拒绝重复 JSON 键。

## 三组记录

根对象含 `schema_version`、`task`、`claims`、`sources`、`evidence`。三组数组非空，ID 在各自组内唯一。

`claims` 每项：

| 字段 | 含义 |
|---|---|
| `id` / `text` | 稳定论点标识与完整论点，不把多个结论混写 |
| `kind` | `industry_context`、`industry_statistic`、`product_fact`、`effectiveness` |
| `subject` | 论点对象；产品事实须与企业来源的 `subject` 一致 |

`sources` 每项：

| 字段 | 含义 |
|---|---|
| `id` / `title` / `publisher` | 材料标识、实际标题、实际发布者 |
| `source_type` | `government`、`research`、`media`、`company`、`other`；不是可信度评分 |
| `subject` | 企业材料必填，指它自己的产品；其他类型可省略 |
| `relationship` | `primary` 或 `reprint`；政府域名也可能刊登转载 |
| `url` | 精确 http(s) 页面；`fetched` 必填，其他状态无 URL 时填空字符串 |
| `input_ref` | `supplied` 必填，定位用户文档或摘录；其他状态可填空字符串 |
| `published_on` | `YYYY-MM-DD` 或 `null`，缺日期不猜测 |
| `publication_date_note` | 无发布日期时必须解释原因；有日期可为空字符串 |
| `period` | 统计/适用时期；没有统计时明确写“非统计材料”及适用时点 |
| `scope` | 地区、对象、方法/样本、单位、版本等适用限制；缺口明确写出 |
| `locator` | 页码、表号、章节、段落或网页区块；失败时说明没有读取位置 |
| `excerpt` | 在有权或获准再分发的前提下记录支撑判断的短原文；可以留空 |
| `summary` | 由整理者独立撰写的材料摘要；可以留空，与 `excerpt` 至少填一项才可标 `fetched` 或 `supplied` |
| `access_status` | 下表中的五种采集状态之一 |
| `accessed_on` | 实际采集/收件/尝试日期；`unrun`、`simulated` 可为 `null` |
| `access_note` | 访问方式、缓存/片段限制或错误原因；不要存凭据、Cookie |
| `trace` | 见下文转载溯源对象 |

| 采集状态 | 准确含义 | 可作为 `cite` |
|---|---|---|
| `fetched` | 实际读到公开页面正文，保留定位及有权分享的摘录或独立摘要；如工具返回缓存需注明 | 可以，由 Agent 判断内容范围 |
| `supplied` | 只读到用户给定材料，未在线核验原页；只在输出/分享权限允许时保存原文，否则记录用户资料定位及独立摘要 | 可以，但段落明确仅据所供材料 |
| `unrun` | 未执行访问或查询 | 不可 |
| `failed` | 实际尝试失败，保留错误 | 不可 |
| `simulated` | 受控测试资料 | 不可用作现实证据 |

`trace` 含 `status`、`original_url`、`attempts`。一手材料用 `status: not_applicable`、空 URL 和空数组。转载用 `not_attempted`、`original_found` 或 `not_found`；后两者至少有一次真实 `attempts`，每项含 `query` 和 `outcome`。`original_found` 还需完整 `original_url`。这是原链接定位状态，原文是否读到还要看独立来源行的采集状态。

`evidence` 每项把一个论点与一份材料配对：

| 字段 | 含义 |
|---|---|
| `claim_id` / `source_id` | 引用已有 ID；同一配对不能重复，每个论点至少出现一次 |
| `support` | `direct`、`background`、`self_statement`、`none`；语义由 Agent 判断 |
| `use` | `cite`、`pending`、`reject` |
| `reason` | 具体支撑范围或不采用原因，不能只写“权威” |
| `citation_text` | Agent 写好的可引用句；仅 `cite` 非空，其他决定必须为空 |
| `next_step` | `pending`/`reject` 必填，指出补证或删改措施；`cite` 可为空 |

企业材料只有 `product_fact`、对象一致且 `support: self_statement` 才能 `cite`。转载需先有实际溯源记录，最多标 `background` 使用。只有转载但无访问条件时保留 `pending`，不要把 `not_attempted` 改成 `not_found` 来通过校验。没有外部来源时，可将实际收到的原稿记为 `supplied`，对应论点标 `none/pending`，而不是虚构来源。

## 命令和产物

从技能根目录运行：

```bash
python3 scripts/evidence_table.py --input examples/success/evidence.json --out-dir /tmp/cn-source-map-result
```

退出码 `0` 表示台账通过一致性校验且导出成功；`2` 表示输入/路径/引用边界错误，stderr 给出原因。无效台账在写入前被拒绝；文件系统写入失败可能已产生部分文件，应修复目标目录后重试。重复运行会覆盖导出目录内同名的三份脚本产物。

导出 UTF-8 BOM CSV，包含论点、精确出处、日期、范围、原文摘录/独立摘要、状态、决定与可引用句；对表格公式前缀加单引号防止执行，原始 JSON 保留原值。`未核实清单.md` 按台账汇总待核实和弃用行，并列出可用材料的限制。`校验汇总.json` 区分有可用背景/自述的论点与有 `direct` 支持的论点，按输入记录计数；这些数字不表示 AI 引用或收录。

`可直接使用的出处段落.md` 由 Agent 撰写，不由脚本拼模板生成。转述不得冒充逐字原文；只在有权分享的场景使用短引语，否则用独立摘要并标明来源和定位。相关限制紧邻结论。仓库中的演示材料仅含独立摘要，不包含第三方原文摘引。
