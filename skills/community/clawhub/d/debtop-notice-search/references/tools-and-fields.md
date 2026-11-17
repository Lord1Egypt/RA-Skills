# 工具参数与返回字段

> 4 个工具均为**只读**。本 Skill 主用前两个（公告搜索与公告详情），后两个（企业搜索与企业概要）作按主体汇总的辅助手段。调用顺序与降级策略见 SKILL.md §四；错误码与处置见 `@references/errors.md`。

## 通用参数约定

入参统一 **下划线（snake_case）**：`page_size`、`notice_id`、`enterprise_id`。为兼容历史调用，旧的驼峰写法（`pageSize` / `noticeId` / `enterpriseId`）仍可被接受，但**新代码请一律用下划线**（驼峰仅作过渡，后续可能移除）。ID 参数**整数与字符串都可传**（搜索结果里是整数，直接回传即可）；`page_size` 默认 10，**工具接受 1–100，但上游后端按 20 截断**（传更大值只会拿到 20 条，响应里 `page_size` 回显 20）。

## 1. `search_debt_notice` — 债权公告搜索（**本 Skill 主入口**）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | **是** | 企业名、债权人、债务人或事项关键词均可；空值报 `PARAM_INVALID: keyword 不能为空` |
| page | integer | 否 | 页码，默认 1 |
| page_size | integer | 否 | 每页条数，默认 10；工具接受 1–100，**上游按 20 截断** |

返回 `total` / `page` / `page_size` / `items[]`；`items[]` 关键字段：

| 字段 | 说明 |
|------|------|
| `notice_id` | 公告 ID（整数，int64），可直接回传给 `get_debt_notice_detail` |
| `title` | 公告标题 |
| `notice_type` / `notice_type_name` | 公告类型与中文名（枚举见下） |
| `source` | **公告来源**（报纸 / AMC 官网 / 产权交易所 / 资产平台等），与链接上的 `source` 客户端标识无关 |
| `notice_date` | 公告日期 |
| `creditor` | 债权人（出让方） |
| `debtor` / `debtor_num` | 债务人；**多主体串 + 主体个数** |
| `principal_amount_yuan` / `_text` | 本金（精确值 / 展示文本） |
| `total_amount_yuan` / `_text` | 债权总额（精确值 / 展示文本） |
| `original_creditor` | 原债权人——**条件字段**（转让类公告常见，可能整体缺失） |
| `detail_url` | **公告详情页链接，输出时务必附上，并带 `source` 客户端标识——见 SKILL.md §五** |

`notice_type` 枚举（以后台为准）：`transfer` 转让、`deal` 处置、`market` 招商、`collect` 催收、`correct` 更正、`trade` 处置挂牌。

> **`debtor` 是多主体串**：一条公告常含多个债务人，`debtor` 以**逗号分隔**（如 `甲公司,乙公司`），`debtor_num` 即主体个数。做清单统计或关键词延伸时，**先按逗号拆分再逐个使用**，不要把整串当作一个企业名。
> **命中的粒度是「公告」**：同一主体的多条公告会分别出现；`total` 是命中公告数，不是企业数。

## 2. `get_debt_notice_detail` — 债权公告详情（担保线索）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| notice_id | integer \| string | **是** | 取自 `search_debt_notice` 的 `notice_id` |

返回列表项全部字段；下列字段为**条件字段**——仅在公告披露时才出现，**可能整体缺失**（不是 `null`，`key` 不存在）：

| 条件字段 | 说明 |
|---|---|
| `guarantor` | 保证人 |
| `collateral` | 抵押物 |
| `original_creditor` | 原债权人（转让类公告常见） |

> **字段差异（务必判空）**：催收类公告通常有 `guarantor` 而无 `collateral`；转让类公告两者都可能缺失、但常多出 `original_creditor`。**取值前先判断 key 是否存在**，不要假设字段一定存在。

> 详情同样返回 `detail_url`（公告详情页链接）——引用该公告时一并附上。

## 3. `search_debt_enterprise` — 债务企业搜索（辅助：定位主体）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | **是** | **单一**企业名称（一个名称；**不要传逗号分隔的多主体串**）；**过宽的词会被拒**（`PARAM_INVALID: 搜索内容过于宽泛`），请用企业全称或较完整的简称 |
| page / page_size | integer | 否 | 同上 |

返回 `items[]`：`enterprise_id`、`enterprise_name`、`detail_url`（**企业详情页链接，输出时务必附上，并带 `source` 客户端标识——见 SKILL.md §五**）。

> **索引范围（很关键）**：该索引是**债务人（融资方）**维度——`search_debt_notice` 结果里 `debtor` 列出的企业能查到；`creditor`（AMC / 银行等出让方）**通常查不到**，用债权人名会返回 0 命中，属正常现象，不是故障。**要按债权人检索，请直接用 `search_debt_notice`**（公告索引同时覆盖出让方与融资方）。

## 4. `get_debt_enterprise_debt_summary` — 企业债务概要（辅助：按主体汇总）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_id | integer \| string | **是** | 取自上一步的 `enterprise_id` |

关键返回字段：

| 字段 | 说明 |
|------|------|
| transfer_notice_count | 转让公告数量 |
| transfer_principal_total_yuan / _text | 转让类本金合计 |
| transfer_interest_total_yuan / _text | 转让类利息合计 |
| disposal_notice_count | 处置/招商公告数量 |
| disposal_principal_total_yuan / _text | 处置类本金合计 |
| disposal_interest_total_yuan / _text | 处置类利息合计 |
| related_creditors[] / related_creditor_count | 相关债权人（**仅返回前 3**，总数看 count） |
| related_debtors[] / related_debtor_count | 相关债务人（**仅返回前 3**，总数看 count） |
| related_sources | 相关公告来源（最多 2 个，超出以「等」结尾） |
| related_notice_period | 相关公告时段 `yyyy-MM-dd ～ yyyy-MM-dd` |
| detail_url | 企业详情页链接（**输出时务必附上并带 `source`**，见 SKILL.md §五） |

> 上述字段由后台服务定义、本服务仅透传；首次接入或后台升级后，建议用一次真实调用确认字段未变。
