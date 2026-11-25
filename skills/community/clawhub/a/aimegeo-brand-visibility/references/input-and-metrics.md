# 输入契约与指标

输入是 UTF-8 JSON，`schema_version` 固定为字符串 `1.0`。脚本使用 Python 3.10+ 标准库，无网络调用。Agent 可直接整理用户粘贴的回答，不要求用户手工写 JSON。[完整四回答输入](../examples/success/input.json)可供参考。

## 品牌和范围

| 字段 | 规则 |
| --- | --- |
| brand.name | 非空品牌名，先区分同名实体 |
| brand.aliases | 可省略的非空字符串数组；只是字面搜索候选 |
| brand.facts | 可省略。每项包含唯一 id、statement、source 和可空 as_of |
| facts.source | 事实依据的 URL 或用户资料说明；脚本不会访问或验证来源 |
| facts.as_of | 事实适用时间，含时区的 ISO 8601 时间或 null；未知不能填当前时间 |
| scope.locale / market | 可空的语言/市场描述，缺失保留 null |
| records | 记录数组，允许空数组，空样本不产生百分比 |

`as_of` 表示依据的适用时间，不自动证明来源权威性。证据中的源网址应属于用户提供的材料，不能为了完成表格发明网址。

## 每条记录

以下字符串必填且非空：`id`、`question_id`、`question`、`intent`、`platform`、`run_id`、`source`、`status`。不知道平台名称可写 `未知平台（用户粘贴）`，不猜具体产品。

- `id` 全局唯一；同一 `question_id` 必须对应相同问题原文和意图。
- 同一 `(question_id, platform, model, run_id)` 只能出现一次。重复粘贴不换 run_id 重复统计；确实重新查询才另记运行。内容相同不证明是同一运行，脚本不按答案文本自动合并。
- `model` 可空；`search_mode` 为 `on`、`off` 或默认 `unknown`；`context_note` 可空，写首轮/多轮、登录个性化等已知条件。
- `captured_at` 为含时区的 ISO 8601 时间（例如 `2026-10-18T09:00:00+08:00`）或 null。不知道时保留 null，汇总会列出缺时间的记录 ID。
- `source` 写可回溯的采集说明，例如用户导出记录标识；不要存 Cookie、Token 或凭据路径。

| status | 含义 | answer / reason | 实测分母 |
| --- | --- | --- | --- |
| observed | 实际收到的完整回答 | answer 必须非空；reason 可空 | 可以进入；各项还需审核/采集完整 |
| query_failed | 实际查询报错、超时等 | reason 必填；可保留部分 answer，但不分析 | 排除 |
| missing | 用户说已查询，但没有可用原文 | reason 必填 | 排除 |
| not_run | 未执行查询 | reason 必填 | 排除 |
| simulated | 为讲解构造的回答 | answer 必须非空 | 仅隔离演示 |

不把“模型回答不知道该品牌”记成失败；有完整原文时仍是有效回答，可审核为未提及或仅提及。模型拒答也保留原文并在报告中说明。失败、缺失、未运行记录不能带审核或引用条目，避免误作成功证据。

## 引用采集

`citations_capture`：

- `complete`：确认采到了全部原生来源面板/脚注。没有原生来源时才可用完整的空数组表示已确认零条。
- `partial`：只采到部分来源或没有取得完整脚注 URL。
- `not_captured`（默认）：来源面板未检查或导出未包含它；可以保留已知的 inline 正文链接，不能带 native 条目。

`citations` 每项：

| 字段 | 规则 |
| --- | --- |
| url | 绝对 http(s) URL；拒绝带用户名/密码和空白的 URL |
| kind | `native` 平台原生来源，或 `inline` 普通正文链接 |
| evidence | 必填，实际来源标号、面板摘录或导出定位；不能只凭用户另附参考链接 |
| relation | `brand` 与品牌有关、`other` 无关、`unreviewed` 未审核 |
| relation_evidence | brand/other 必填，说明实体关联依据；未审核可空 |

同一类链接按 URL 去重：协议/主机大小写归一，忽略 fragment，保留 query；相同链接的关联判定冲突则拒绝。原始 URL 保留在输出。不解析重定向、不判断可访问性、不验证原生标记真伪，Agent 需回看采集材料。

没有原生 URL，即使有品牌名、脚注数字、截图或普通官网超链接，也不能算原生链接引用。来源面板没采完时，`native_brand_urls` 可列出已看到的链接，但 `native_brand_citation_count` 和 `brand_native_cited` 为 null，不能把已知下限称为总量。

## Agent 的语义审核

`review` 可省略，但省略表示未审核，脚本不会用关键词冒充判断。

- `mention` / `recommendation`：对象含 `value: true/false/null`、`reason`（非空）和 `quote`。true 必须附回答中的原文连续子串；false 可无 quote，reason 说明全文未见或为什么不构成推荐。null 表示暂不能判断。未提供字段的规范化值为 null。
- 推荐为 true 需提及审核为 true。提及可以是有充分实体依据的间接指代；引用面板中的名字不直接当正文提及。候选检索命中不等于实体审核通过。
- `tone`：`value` 为 `positive/neutral/negative/mixed/unknown`。非 unknown 时须已审核提及，且有原句 quote、理由 reason；不把中性说明当推荐。
- `fact_checks`：每项含 `fact_id`、`verdict`、`quote`、`reason`。`verdict` 为 `match/contradiction/unverified`；确定结论须引用已知 brand.facts 的 id。未核验可以 `fact_id: null`。原句须属于回答正文，同一回答同一事实只能核对一次。必须先审核该回答确实在说品牌。

脚本只检查结构、证据可定位性与逻辑约束；事实是否真的吻合、语句是否真的推荐，由 Agent 根据上下文判断。未知顶层/记录扩展字段不进入输出；这不等于敏感数据脱敏，回答与已知字段会原样保留。

## 透明计算

`measured` 只含 observed。总有效回答数与每项已审核分母分别披露，失败记录不算“未提及”。没有有效分母时，`numerator` 和 `percent` 都为 null，`denominator` 为 0；显示“不可计算”，不能显示 0%。

| 观察面 | 计算 / 输出 | 未知处理 |
| --- | --- | --- |
| 提及 | mention=true 数 / mention 已审核回答数 | null 审核排除；字面候选不参与 |
| 推荐 | recommendation=true 数 / recommendation 已审核回答数 | null 排除；衡量回答中的推荐，不推测用户购买意愿 |
| 原生品牌链接引用 | 有原生品牌 URL 的回答数 / 原生来源已完整采集且全部 native 关联已审核的回答数 | 未采全或 native 关联未审核则排除；其他来源和 inline 不计品牌原生引用 |
| 事实准确性 | match 条数 / (match + contradiction) 条数 | unverified 单列；无核对的回答另计，不能声称全部准确 |
| 语气与一致性 | 四种语气的已审核数量；同事实同时有吻合与冲突的记录 ID | 无语气审核时分布值 null；一致性只给证据，不自算分数 |
| 意图覆盖 | 至少一次提及的意图数 / 所有有效回答均已完成提及审核的意图数 | 没有有效回答的意图不入分母；部分回答未审核的意图排除 |

每项 `unknown` 是当前有效样本中因未审核/采集不足而未纳入的单位数；事实项单位为核对条目，意图项单位为意图。它不包含全局失败数，需同时展示 `status_counts`。有实测分母且确认为零才输出数值 0。

`fact_review_disagreements` 是同一事实出现两种审核结论的线索，不自动推导平台间不一致。`by_platform_model_search` 保留分组，不进行跨条件排名。逐问题 `unmentioned_in_all_valid_answers=true` 仅在至少一个有效回答且该问题全部有效回答完成审核、全部未提及时成立；没有有效回答或审核不全时为 null。

`simulation_preview` 单独复用公式展示合成数据计算，永不进入 measured。演示中的 valid_answers 只表示可用于演算的合成回答数。没有历史同条件实测时不写趋势；重复少、问题偏向品牌或联网条件不明时说明样本偏差。

## CLI 约定

```sh
python3 scripts/analyze.py examples/success/input.json
python3 scripts/analyze.py examples/success/input.json --output evidence.json
```

命令相对技能根目录。实际输出应保存到用户本次工作目录。未给 `--output` 时写 stdout；给定时创建新文件，不建父目录、不覆盖已有文件。成功退出 0；非法 JSON、重复键、非有限数、校验错误、输入/输出读写失败退出 2，并向 stderr 写 JSON 错误。失败时不输出半份成功 JSON。
