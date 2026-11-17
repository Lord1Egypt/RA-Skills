## 债权公告搜索：{keyword}

> 数据来源：智收云公开债权公告（命中 {total} 条，本次展示 {count} 条）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

### 1. 搜索概览
| 项 | 内容 |
|---|---|
| 搜索关键词 | {keyword} |
| 命中公告总数 | {total} |
| 本次展示条数 | {count}（按日期倒序） |
| 公告时段 | {notice_date_min} ～ {notice_date_max} |
| 类型分布 | 转让 {transfer_count} / 处置·招商 {disposal_count} / 催收 {collect_count} / 其它 {other_count} |
| 数据来源渠道 | {sources} |

### 2. 公告清单（按日期倒序，最多 20 条）
| 日期 | 类型 | 标题 | 债权人 | 债务人 | 本金 | 链接 |
|---|---|---|---|---|---|---|
| {notice_date} | {notice_type_name} | {title} | {creditor} | {debtor} | {principal_amount_text} | {detail_url} |

> 债务人为多主体时按逗号拆开展示（如「甲公司、乙公司」），主体数见 `debtor_num`；金额排序按 `principal_amount_yuan`，展示用 `principal_amount_text`。

### 3. 重点公告明细（字段可能缺失，缺失时写「公告未披露」）
- 公告标题：{title}（{notice_id}）
- 债权人 / 债务人：{creditor} / {debtor}
- 本金 / 总额：{principal_amount_text} / {total_amount_text}
- 保证人：{guarantor}
- 抵押物：{collateral}
- 原债权人：{original_creditor}
- 公告详情：{detail_url}

### 4. 主体延伸（可选：命中公告中的相关主体）
- {关联名称}：命中 {X} 条公告，涉及本金 {Y}

### 5. 提示
- 以上为公开公告口径，未包含未披露信息；数据存在滞后与不全的可能
- 命中条数以接口返回的 `total` 为准，展示条数以本次实际取得为准（分页按 20 截断）
- 金额 `_yuan` 为精确数值、`_text` 为展示文本，不要自行换算
- 链接均为接口返回的 `detail_url`（已按规则附加 `source`），可直接点击查看公告/企业原文

---

说明：占位符 `{detail_url}` 一律指**已附加 `source=<客户端标识>` 的链接**（拼接规则与调用方式见 `@scripts/with_source.py` 与 SKILL.md §五）；标题、债权人等应做成可点击链接，展示文本与 href 都用带 `source` 的完整 URL。字段为空时按各节的说明处理（如「公告未披露」「暂无链接」），不要编造。
