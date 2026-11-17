## {出让方名称} 债权处置清单

> 数据来源：智收云公开债权公告（命中 {total} 条，本次展示 {count} 条）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

### 1. 处置概览
| 项 | 内容 |
|---|---|
| 出让方（债权人） | {creditor} |
| 命中公告总数 | {total} |
| 本次展示条数 | {count}（按日期倒序） |
| 公告时段 | {notice_date_min} ～ {notice_date_max} |
| 涉及债务人数 | {debtor_total}（去重后；本批可见 {debtor_shown}） |
| 数据来源渠道 | {sources} |

### 2. 公告清单（按日期倒序，最多 20 条）
| 日期 | 类型 | 标题 | 债务人 | 本金 | 链接 |
|---|---|---|---|---|---|
| {notice_date} | {notice_type_name} | {title} | {debtor} | {principal_amount_text} | {detail_url} |

> 债务人为多主体时按逗号拆开展示（如「甲公司、乙公司」），主体数见 `debtor_num`；金额排序按 `principal_amount_yuan`，展示用 `principal_amount_text`。

### 3. 类型与金额分布
| 类型 | 公告数 | 本金合计 | 总额合计 |
|---|---|---|---|
| 转让（transfer） | {transfer_count} | {transfer_principal_text} | {transfer_total_text} |
| 处置（deal） | {deal_count} | {deal_principal_text} | {deal_total_text} |
| 招商 / 挂牌（market / trade） | {market_trade_count} | {market_trade_principal_text} | {market_trade_total_text} |
| 催收 / 其它（collect / correct） | {other_count} | {other_principal_text} | {other_total_text} |

> 金额合计用 `*_yuan` 汇总、展示用 `*_text`；某类型为 0 时可省略该行。

### 4. 重点标的明细（字段可能缺失，缺失时写「公告未披露」）
- 公告标题：{title}（{notice_id}）
- 债务人：{debtor}
- 本金 / 总额：{principal_amount_text} / {total_amount_text}
- 保证人：{guarantor}
- 抵押物：{collateral}
- 原债权人：{original_creditor}
- 公告详情：{detail_url}

### 5. 涉及债务人（可选：清单中出现的主体）
- {债务人名称}：命中 {X} 条公告，涉及本金 {Y}

### 6. 提示
- 以上为公开公告口径，未包含未披露信息；数据存在滞后与不全的可能
- 命中条数以接口返回的 `total` 为准，展示条数以本次实际取得为准（分页按 20 截断）
- 金额 `_yuan` 为精确数值、`_text` 为展示文本，不要自行换算
- 链接均为接口返回的 `detail_url`，**原样引用、不做任何改写**，可直接点击查看公告/企业原文

---

说明：占位符 `{detail_url}` 一律指**接口原样返回的链接**（不要追加、修改或删除任何查询参数，见 SKILL.md §五）；标题、债务人等应做成可点击链接，展示文本与 href 用同一个 URL。字段为空时按各节的说明处理（如「公告未披露」「暂无链接」），不要编造。
