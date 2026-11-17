## 债权标的筛选：{行业词} × {地区} × {金额区间}

> 数据来源：智收云公开债权公告（命中 {total} 条，入筛 {matched} 条）｜查询时间：{yyyy-MM-dd HH:mm}｜口径：公开公告，非征信报告

### 1. 筛选概览
| 项 | 内容 |
|---|---|
| 行业 / 标的类型词 | {keywords}（共 {keyword_count} 个，**每个词单独检索**） |
| 地区 | {area}（公告地区 `area`：{area_field}；兜底：{area_fallback}） |
| 金额区间 | {amount_min_text} ～ {amount_max_text}（按 {amount_field} 口径：本金 `principal_amount_yuan` / 总额 `total_amount_yuan`） |
| 命中公告总数 `total` | {total}（达到 10000 表示可能被上限截断） |
| **已扫描条数** | {scanned}（`page_size` 固定 20，共 {pages} 页，按 `notice_id` 去重后） |
| **扫描覆盖率** | {coverage}（已扫描 / `total`） |
| **已覆盖日期窗口** | {scanned_date_min} ～ {scanned_date_max} |
| **是否全量** | {is_full}（覆盖率 < 100% 时必须写「仅覆盖已扫描窗口，非全量」） |
| 入筛条数 | {matched}（金额区间内，**限已扫描窗口内**） |
| 金额未披露条数 | {undisclosed}（不计入金额档位统计，单列） |
| 数据来源渠道 | {sources} |

### 2. 持有人（出让方）分布（按本金合计倒序，最多 15 家）
| 出让方 | 命中标的数 | 本金合计 | 涉及债务人数 | 最近公告日期 |
|---|---|---|---|---|
| {creditor} | {notice_count} | {principal_total_text} | {debtor_count} | {latest_notice_date} |

> 出让方即公告中的 `creditor`（债权人 / 出让方），**不等于当前实际持有人**（债权可能已再次转让）。

### 3. 标的清单（按本金倒序，最多 20 条）
| 日期 | 类型 | 地区 | 标题 | 出让方 | 债务人 | 本金 | 链接 |
|---|---|---|---|---|---|---|---|
| {notice_date} | {notice_type_name} | {area} | {title} | {creditor} | {debtor} | {principal_amount_text} | {detail_url} |

> 债务人为多主体时按逗号拆开展示（如「甲公司、乙公司」），主体数见 `debtor_num`；排序按 `principal_amount_yuan`（或回落口径 `total_amount_yuan`），展示用 `principal_amount_text`。

### 4. 分布统计
| 维度 | 取值 | 条数 | 本金合计 |
|---|---|---|---|
| 类型 | {notice_type_name} | {count} | {principal_total_text} |
| 地区 | {area} | {count} | {principal_total_text} |
| 金额档位 | {amount_bucket} | {count} | {principal_total_text} |

> 金额未披露的标的**不进档位统计**，单列条数并在提示中说明。

### 5. 提示
- **金额区间仅在已扫描窗口内生效**：检索接口不接受金额条件，结果**不等于全量**。本次覆盖率 {coverage}，已覆盖 {scanned_date_min} ～ {scanned_date_max}；如需提高覆盖率，请按 SKILL.md §四 4.3 收窄关键词后重跑
- 以上为公开公告口径，未包含未披露信息；数据存在滞后与不全的可能，**不构成投资建议**
- 「命中」不等于该债务人的主业：全文检索也会命中**抵押物文本**，输出时请勿把命中缘由写成主业判断
- `area` 为**公告地区（省级、条件字段可能缺失）**，不是抵押物坐落；`area` 缺失的条目按关键词兜底，已在上表标注
- 出让方（`creditor`）是公告中的债权人 / 出让方，**不等于当前实际持有人**
- 命中条数以接口返回的 `total` 为准，**达到 10000 表示可能被上限截断**；已扫描 / 入筛 / 展示条数以本次实际取得为准（分页按 20 截断，同一天可能跨页，已按 `notice_id` 去重）
- 金额 `_yuan` 为精确数值、`_text` 为展示文本，不要自行换算；本金为 0 或缺失时已回落总额口径，并在「金额口径」列标注
- 链接均为接口返回的 `detail_url`，**原样引用、不做任何改写**，可直接点击查看公告/企业原文

---

说明：占位符 `{detail_url}` 一律指**接口原样返回的链接**（不要追加、修改或删除任何查询参数，见 SKILL.md §五）；标题、出让方等应做成可点击链接，展示文本与 href 用同一个 URL。字段为空时按各节的说明处理（如「公告未披露」「暂无链接」），不要编造。
