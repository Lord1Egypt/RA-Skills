## {企业名称} 公开公告汇总

> 数据来源：智收云公开债权公告（{N} 条）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告原文，非征信报告，不构成信用评估或投资建议

### 1. 主体概览
| 项 | 内容 |
|---|---|
| 企业名称 | [{enterprise_name}]({detail_url}) |
| 企业 ID | {enterprise_id} |
| 企业详情页 | {detail_url} |
| 关联公告时段 | {related_notice_period} |
| 相关债权人 | {related_creditors}（共 {related_creditor_count} 家） |
| 相关债务人 | {related_debtors}（共 {related_debtor_count} 户） |
| 数据来源渠道 | {related_sources} |

### 2. 公告披露金额
| 口径 | 公告数 | 本金合计 | 利息合计 |
|---|---|---|---|
| 转让类 | {transfer_notice_count} | {transfer_principal_total_text} | {transfer_interest_total_text} |
| 处置/招商类 | {disposal_notice_count} | {disposal_principal_total_text} | {disposal_interest_total_text} |

### 3. 公告时间线（按日期倒序，最多 20 条）
| 日期 | 类型 | 标题 | 债权人 | 本金 | 链接 |
|---|---|---|---|---|---|
| {notice_date} | {notice_type_name} | {title} | {creditor} | {principal_amount_text} | {detail_url} |

### 4. 担保与标的（字段可能缺失，缺失时写「公告未披露」）
- 抵押物：{collateral}
- 保证人：{guarantor}
- 公告详情：{detail_url}

### 5. 关联方延伸
- {关联名称}：命中 {X} 条公告，涉及本金 {Y}

### 6. 提示
- 以上为公开公告口径，未包含未披露债务；数据存在滞后与不全的可能
- 本汇总仅为公开公告原文的检索结果，不构成信用评估、风险评级、投资建议或任何交易依据
- 金额汇总仅取公告披露值，`_yuan` 为精确数值、`_text` 为展示文本
- 链接均为接口返回的 `detail_url`，**原样引用、不做任何改写**，可直接点击查看公告/企业原文

---

说明：占位符 `{detail_url}` 一律指**接口原样返回的链接**（不要追加、修改或删除任何查询参数，见 SKILL.md §五）；企业名、标题等应做成可点击链接，展示文本与 href 用同一个 URL。字段为空时按各节的说明处理（如「公告未披露」「暂无链接」），不要编造。
