## {企业名称} 合作方债务速查

> 数据来源：智收云公开债权公告｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

**结论速览**：{是否命中公开债务公告}｜规模量级：{本金合计约 X}｜最近公告：{最近日期}｜主要债权人：{前 3}

### 1. 速查结论
| 项 | 内容 |
|---|---|
| 企业名称 | [{enterprise_name}]({detail_url}) |
| 企业 ID | {enterprise_id} |
| 是否命中公开债务公告 | {是 / 否}（命中 {total} 条） |
| 企业维度概要 | {有 / 无} |
| 一句话说明 | 公开公告显示{有 / 未检索到}可查到的债权公告记录（只陈述公开信息，不作信用判断） |

### 2. 债务规模（企业维度概要可得时）
| 口径 | 公告数 | 本金合计 | 利息合计 |
|---|---|---|---|
| 转让类 | {transfer_notice_count} | {transfer_principal_total_text} | {transfer_interest_total_text} |
| 处置/招商类 | {disposal_notice_count} | {disposal_principal_total_text} | {disposal_interest_total_text} |

> 未取得企业维度概要（0 命中或报 `PARAM_INVALID: 搜索内容过于宽泛`）时，本节写「未取得企业维度概要」，并以公告口径给出量级。

### 3. 最近公告（按日期倒序，最多 5 条）
| 日期 | 类型 | 标题 | 债权人 | 本金 | 链接 |
|---|---|---|---|---|---|
| {notice_date} | {notice_type_name} | {title} | {creditor} | {principal_amount_text} | {detail_url} |

### 4. 担保线索（字段可能缺失，缺失时写「公告未披露」）
- 抵押物：{collateral}
- 保证人：{guarantor}
- 公告详情：{detail_url}

### 5. 提示
- 以上为公开公告口径，数据存在滞后与不全的可能
- **未命中不等于无债务**：本数据仅覆盖公开披露的债权公告，不能证明企业无债务或具备偿债能力
- 不代表征信结果，也不构成尽调结论；如需完整画像请使用 `debtop-enterprise-profile`
- 链接均为接口返回的 `detail_url`，**原样引用、不做任何改写**，可直接点击查看公告/企业原文

---

说明：占位符 `{detail_url}` 一律指**接口原样返回的链接**（不要追加、修改或删除任何查询参数，见 SKILL.md §五）；企业名、标题等应做成可点击链接，展示文本与 href 用同一个 URL。字段为空时按各节的说明处理（如「公告未披露」「暂无链接」），不要编造。
