# 取数口径与指标映射

## 一、输入 JSON 字段说明

`scripts/negative_screen.py` 接受如下结构（缺失字段一律填 `null`，**不要填 0**）：

```json
{
  "company": "万科企业股份有限公司",
  "entity_type": "企业法人",
  "unit": "亿元",
  "years": [
    {
      "year": 2025,
      "net_profit_parent": -885.56,
      "net_profit_total": null,
      "net_profit_deducted": null,
      "asset_liability_ratio": 76.89,
      "total_assets": null,
      "total_liabilities": null,
      "net_assets": null,
      "net_assets_parent": null,
      "audit_opinion": "标准无保留",
      "source": "MCP·预警通 2025年报"
    }
  ]
}
```

| 字段 | 含义 | 必填 | 说明 |
|---|---|---|---|
| `company` | 客户工商全称 | 是 | 用于报告抬头 |
| `entity_type` | 单位性质 | 是 | 企业法人 / 事业单位 / 其他 |
| `unit` | 金额单位 | 是 | 仅用于展示，需全表统一 |
| `year` | 会计年度 | 是 | 整数年份 |
| `net_profit_parent` | 归母净利润 | C1 口径一 | 与合计**平权**，单独判一次；两者尽量都取 |
| `net_profit_total` | 净利润合计 | C1 口径二 | 与归母**平权**，非回退项；缺失会在信息缺口中声明 |
| `net_profit_deducted` | 扣非归母净利润 | 建议 | 实质性连亏辅助判断 |
| `asset_liability_ratio` | 资产负债率（%） | C2 首选 | 填 `76.89` 表示 76.89%，不要填 0.7689 |
| `total_assets` / `total_liabilities` | 资产总计 / 负债合计 | C2、C3 备选 | 用于反算资产负债率与净资产 |
| `net_assets` | 净资产（所有者权益合计） | C3 首选 | **最近一期必取**——C3 为当期口径，最近年度缺失将直接导致 C3 判"数据缺口" |
| `net_assets_parent` | 归母净资产 | 建议 | 用于母公司资不抵债提示 |
| `audit_opinion` | 审计意见类型 | 建议 | 含"保留/否定/无法表示/持续经营"字样时脚本自动预警 |
| `source` | 来源标签 | 是 | 缺失会被列入信息缺口 |

数组 `years` 可传超过 3 个年度，脚本自动按年份倒序取最近 3 个完整年度。

## 二、财汇MCP（企业预警通）取数映射

调用前先加载 `caihui-mcp-usage` Skill，避免参数试错。

| 判定字段 | 财汇MCP 指标名 | 调用要点 |
|---|---|---|
| `net_profit_parent` | 归母净利润 | `get_company_financial_metrics` |
| `net_profit_total` | 净利润 | 同上 |
| `net_profit_deducted` | 扣非净利润 | 同上 |
| `asset_liability_ratio` | 资产负债率 | 同上，返回值即百分数 |
| `total_assets` | 资产总计 | 同上 |
| `total_liabilities` | 负债合计 | 同上 |
| `net_assets` | 所有者权益合计 | 同上 |
| `net_assets_parent` | 归属母公司所有者权益 | 同上 |
| `audit_opinion` | 审计意见 | 通常需从年报公告正文获取，可用 `search_company_announcements` 取年报后读正文 |
| `pledge_details` | 股票质押明细（**必查**） | `get_stock_pledge_details`：`target_stock`（数组，股票名/代码），返回出质人/质权人/最新质押数量/剩余质押数量/状态/起始截止日/成本价/预警价/平仓价/公告日；覆盖沪深京 A 股，不覆盖港美股 |

### 已知调用坑（来自实测）

- `get_company_financial_metrics` 的 `target_company` 与 `indicator_name` 均为**数组**，`date` 为**自然语言字符串**（如 `"近五年年报"`、`"2023年年报"`）
- **组合查询可能漏字段**：一次性传多个 `indicator_name` 时，个别年度可能返回不全。判定用的关键指标（净利润、资产负债率、净资产）建议**分指标单独查询校验**，尤其是命中/未命中临界的年度
- `search_company_announcements` 的 `title_keywords` 与 `date_range` **同时传会返回 0 条**，需只传 `date_range`（数组，自然语言元素）后自行过滤
- 港股主体 MCP 常返回空，需外网补充并标注「外网·WebSearch」

## 三、来源标签规范

每个年度的 `source` 必须可追溯，格式为「来源 + 期间」：

| 来源类型 | 标签写法 | 可信度 |
|---|---|---|
| 客户提供的审计报告 | `客户提供·审计报告 2024年度` | 高 |
| 财汇MCP / 企业预警通 | `MCP·预警通 2024年报` | 高 |
| 交易所 / 公开年报 | `公开年报 2024` | 高 |
| 外网检索 | `外网·WebSearch 2024` | 中 |
| 客户口头或未审数 | `客户提供·未审数 2024` | 低（不得单独作为判定依据） |

低可信度来源不得单独支撑红线命中判定；若仅有低可信度数据，对应红线应判为「数据缺口」。

## 四、批量筛查

批量场景下，为每户生成一个 JSON，循环调用脚本并收集 `--format json` 输出，再汇总为名单表：

```bash
for f in ./batch/*.json; do
  python scripts/negative_screen.py -i "$f" -f json
done
```

汇总表建议字段：客户名称、判定年度、C1/C2/C3 结果、总体结论、数据缺口数、待补资料。需要 Excel 交付物时调用 `financial-report-generation`。

## 五、loan_demand.py 输入字段与 MCP 映射

`scripts/loan_demand.py` 接受 `working_capital` 与 `rigid_liabilities` 两组字段（缺失填 `null`，**不要填 0**）：

| 输入字段 | 含义 | 财汇MCP 指标 | 备注 |
|---|---|---|---|
| `working_capital.revenue` | 上年度营业收入 | 营业收入 | `get_company_financial_metrics` |
| `working_capital.net_profit` | 上年度净利润 | 净利润 | 同上（算销售利润率） |
| `working_capital.cogs` | 营业成本 | 营业成本 | 同上（算存货/应付周转） |
| `working_capital.inventory` | 存货 | 存货 | 同上 |
| `working_capital.accounts_receivable` | 应收账款 | 应收账款 | 同上 |
| `working_capital.accounts_payable` | 应付账款 | 应付账款 | 同上 |
| `working_capital.prepayments` | 预付账款 | 预付账款 | 同上 |
| `working_capital.advances_received` | 预收账款 | 预收账款 | 同上 |
| `working_capital.growth_rate` | 预计增长率 g | — | 取经营计划/行业 CAGR，缺省 0 |
| `working_capital.own_fund_ratio` | 自有资金比例 f | — | 缺省 0.30 |
| `working_capital.existing_short_term_loan` | 现有流贷 L | 短期借款 | 近似，标注假设 |
| `working_capital.other_operating_funds` | 其他渠道 O | — | 缺省 0 |
| `rigid_liabilities.short_term_borrowing` | 短期借款 | 短期借款 | 同上 |
| `rigid_liabilities.non_current_liab_due_within_1y` | 一年内到期非流动负债 | 一年内到期非流动负债 | 同上 |
| `rigid_liabilities.long_term_borrowing` | 长期借款 | 长期借款 | 同上 |
| `rigid_liabilities.bonds_payable` | 应付债券 | 应付债券 | 同上 |
| `rigid_liabilities.long_term_payable` | 长期应付款 | 长期应付款 | 同上 |
| `rigid_liabilities.notes_payable_financing` | 融资性应付票据 | 应付票据 | 可选计入刚性 |
| `rigid_liabilities.total_liabilities` | 负债合计 | 负债合计 | 同上 |
| `rigid_liabilities.net_assets` | 净资产 | 所有者权益合计 | 同上 |
| `rigid_liabilities.ebit` | 息税前利润 | 利润总额+利息费用 | 推算 |
| `rigid_liabilities.ebitda` | EBITDA | EBITDA | 同上 |
| `rigid_liabilities.interest_expense` | 利息费用 | 利息费用 | 同上 |
| `rigid_liabilities.cash_and_equivalents` | 货币资金 | 货币资金 | 同上 |

> EBIT / EBITDA / 利息费用未必在 `get_company_financial_metrics` 直接返回，可从利润表科目推算（EBIT = 利润总额 + 利息费用；EBITDA = EBIT + 折旧 + 摊销），或取公开年报 / 问询函补位。
> 经营性占款（正常应付账款、预收账款、合同负债）默认**不计入**刚性负债；若将融资性应付票据并入，须在报告中声明口径。
