---
name: cn-hk-dividend-fhpg-api
description: 基于服务端 HTTP API 查询中国A股分红配股与港股分红数据（含股息率）。用户提到A股、港股、分红、派息、股息率、分红配股等需求时使用本技能。
homepage: http://clawhub.ai/FunkyGod/cn-hk-dividend-fhpg-api
---

# 中国A股分红配股与港股分红数据 Skill（基于服务端 API）

## 适用场景

在以下场景下优先使用本 Skill：

- 用户提到 **中国A股或港股** 的公司，例如 “腾讯”、“中国平安”、“600519”、“0700.HK”
- 用户需要 **分红/配股相关数据**：
  - A股分红配股列表与详情
  - 港股分红列表与详情
- 用户需要 **分红/派息相关数据**：
  - 历史分红记录（每股派息、送股、转增）
  - 分红频率（年度/中期/季度）
  - 股息率、近几年分红稳定性
- 用户提到：**“看某只股票的财务情况 / 分红历史 / 分红率 / 分红政策”** 等类似描述

> 重要：本仓库 **已实现分红/配股相关的 HTTP API**，但 **未实现财务报表接口**。因此本 Skill 仅处理分红/配股与股息率相关问题；若用户要求财报数据，应明确当前仓库不支持并建议补充数据源。

---

## 使用总原则

1. **统一入口，清晰步骤**
   - 先把用户自然语言需求转成 **结构化查询条件**（市场、代码/名称、时间区间、报表类型等）
   - 再调用项目中 **已实现的 HTTP API** 获取数据
   - 最后对数据进行 **摘要 + 解释 + 风险提示**

2. **强制说明数据范围与滞后性**
   - 例如：财报通常是 **按季/按年披露**，存在滞后
   - 分红为 **历史行为**，不等同于未来承诺

3. **输出时，先结论、再细节**
   - 第一段先说清：盈利是否稳定、负债情况、高/低分红等
   - 后面再给出关键指标表格或列表

---

## 数据访问约定（以服务端实现为准）

该服务提供 **无需登录** 的 REST API，用于获取港股分红与 A 股分红配股数据。所有接口均为 **只读**。

> Base URL：`http://vi-money.com/`（需确认是否为实际对外地址；如未确认，调用方必须先核验协议/端口）
> 建议通过环境变量 `STOCK_API_BASE_URL` 覆盖该地址，避免硬编码。

### 通用响应格式（所有接口一致）

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

- `code = 0` 表示成功
- `code = 400/404/500` 表示错误（缺参、未找到、服务端错误）
- 错误时 `data` 通常为 `null`

### 港股分红 API（`/api/v1/hk-stock`）

- `GET /api/v1/hk-stock/dividend`
  - 说明：港股分红列表（每只股票仅保留最新一条记录）
  - 查询参数：`page`、`limit`、`keyword`、`sort_by`、`sort_order`
  - 默认排序：`sort_by=announce_date`，`sort_order=desc`
  - 返回：`data.list`、`data.total`
- `GET /api/v1/hk-stock/dividend/detail/:code`
  - 说明：某只港股完整分红历史（按公告日降序）
  - 参数：`:code`（如 `0700`）
  - 返回：`data.code`、`data.list`

**港股分红字段说明（`models/hk_dividend_detail.go`）**

- `code`：股票代码
- `name`：股票名称（由 `hk_stock_code` 关联补充）
- `fiscal_year`：财年
- `announce_date`：公告日期
- `ex_date`：除权除息日
- `dividend_plan`：分红方案文本
- `distribution_type`：派息类型
- `transfer_deadline`：过户截止日
- `payout_date`：派息日

### A 股分红配股 API（`/api/v1/cn-stock`）

- `GET /api/v1/cn-stock/fhpg`
  - 说明：A 股分红配股列表（分页 + 联合搜索）
  - 查询参数：`page`、`limit`、`code`、`name`、`plan_progress`、`bonus_type`、`cash_div`、`share_div`、`allotment`、`dividend_yield_min`、`dividend_yield_max`、`announcement_year`、`sort_by`、`sort_order`
  - 默认排序：`sort_by=dividend_yield`，`sort_order=desc`
  - 返回：`data.list`、`data.total`
- `GET /api/v1/cn-stock/fhpg/detail/:code`
  - 说明：某只 A 股分红配股详情（按最新公告日期降序）
  - 参数：`:code`（如 `600519`）
  - 返回：`data.code`、`data.name`、`data.list`

**A 股分红配股列表字段说明（`models/stock_fhps_em.go`）**

- `code`：股票代码
- `name`：股票名称
- `latest_announcement_date`：最新公告日期（列表每只股票只保留一条）
- `report_date`：报告期
- `plan_progress`：方案进度（如预案/已实施/已通过）
- `bonus_type`：送转类型
- `cash_div`：派息文本
- `share_div`：送股文本
- `allotment`：配股文本
- `dividend_yield`：股息率（小数）
- `ex_dividend_date`：除权除息日
- `net_profit_yoy`：净利润同比（可能为空）
- 其他字段（如 `eps`、`navps`、`transfer_ratio` 等）保留但一般不作为首要摘要

**A 股分红配股详情字段说明（`models/stock_fhps_detail_em.go`）**

- `latest_announcement_date`：最新公告日期（排序与图表横轴）
- `report_date`：报告期末日期
- `plan_progress`：方案进度
- `bonus_type`：送转类型
- `cash_div`：派息
- `share_div`：送股
- `allotment`：配股
- `dividend_yield`：股息率（小数）
- `content`：详情正文（可能较长）
- `analysis`：分析文本（可能较长）
- `images_json`：图片/图表 URL 或 JSON

---

## 操作流程

### 1. 解析用户意图

从用户问题中抽取：

- **市场**：A股 / 港股
  - 若用户说 “600519”“贵州茅台”，默认 A股（CN）
  - 若说 “0700.HK”“腾讯控股”，默认 港股（HK）
- **标的**：股票代码或公司名称
  - 可在项目内实现名称到代码的映射：如 `resolve_symbol(name_or_code)`
- **时间范围**：
  - 若未指定，默认 **近 3~5 年分红记录**
  - A 股列表可用 `announcement_year` 限定公告年
- **数据类型**：
  - 分红：历史分红记录、股息率、分红稳定性等
  - 配股/送转：送股、转增、配股信息

### 2. 调用数据接口

按意图调用对应 HTTP API，例如（伪代码）：

```text
# 港股：分红列表
GET /api/v1/hk-stock/dividend?page=1&limit=20&keyword=腾讯&sort_by=announce_date&sort_order=desc

# 港股：分红详情
GET /api/v1/hk-stock/dividend/detail/0700

# A股：分红配股列表（按股息率过滤）
GET /api/v1/cn-stock/fhpg?page=1&limit=20&dividend_yield_min=0.02&dividend_yield_max=0.08&sort_by=dividend_yield&sort_order=desc

# A股：分红配股详情
GET /api/v1/cn-stock/fhpg/detail/600519
```

> 要求：输出时说明股息率字段是 **小数**（如 `0.04` 表示 4%）。

---

## 进行分析与总结

在生成自然语言回答时，建议按以下结构组织：

1. **总体概览（1 段）**
   - 分红是否连续、是否集中在特定年份
   - 股息率区间是否稳定
   - 是否存在一次性大额分红/送转

2. **关键指标列表**
   - 近 3~5 年的分红/配股记录（按公告日期或年份简表）
   - 指标示例：分红方案、股息率、除权除息日、送股/转增/配股

3. **分红情况**
   - 是否持续分红（几年中有缺分红年份）
   - 近几年平均股息率区间（例如 2%–4%）
   - 特殊一次性大额分红需要单独说明

4. **风险与限制说明（必选）**
   - 数据为历史数据，不代表未来表现
   - 分红政策可能会根据经营情况变化
   - 若数据存在缺失或不完整，需要明确指出
   - 本仓库 **不提供财报口径数据**，如用户请求财报，需提示范围限制

---

## 输出格式建议

回答时优先使用 **中文**，并尽量结构化：

- **文字 + 项目符号列表**
- **简表形式**（可用 Markdown 表格，但要简洁）

示例输出结构（示意）：

```markdown
**结论概览**

- 公司近 5 年收入和净利润整体呈上升趋势，盈利能力较为稳定。
- 净利率保持在 20% 左右，ROE 在 15%–18% 区间，盈利质量较好。
- 资产负债率约 40%–45%，杠杆水平适中。

**近 5 年分红/配股记录（示意）**

| 公告日 | 分红方案 | 股息率 | 除权除息日 | 送股 | 转增 | 配股 |
| ------ | -------- | ------ | ---------- | ---- | ---- | ---- |
| 2024-xx-xx | ... | ... | ... | ... | ... | ... |
| 2023-xx-xx | ... | ... | ... | ... | ... | ... |

**分红情况（近 5 年）**

- 共实施现金分红 X 次，其中 Y 年连续分红。
- 近 5 年平均股息率约 Z%，最高年份约 W%。
- 分红较为稳定 / 存在停牌或暂停分红年份，需要注意。

**风险提示**

- 以上数据均为历史披露数据，不构成投资建议。
- 分红政策可能随公司经营环境和董事会决策调整。
- 本仓库不提供财报与预测，请结合其他数据源单独分析。
```

---

## 示例对话用法

**示例 1：查看港股公司分红历史**

> 用户：
> “帮我看看 0700.HK 这家公司最近几年的分红情况，股息率大概多少？”

- 解析：市场=HK，代码=0700.HK，需求=分红历史 + 股息率
- 调用：`GET /api/v1/hk-stock/dividend/detail/0700`
- 输出：总结近几年是否分红、分红方案、股息率区间、是否稳定

**示例 2：对比A股公司财务与分红**

> 用户：
> “把贵州茅台最近 5 年的盈利情况和分红情况总结一下。”

- 解析：市场=CN，symbol=600519（通过名称解析）
- 调用：`GET /api/v1/cn-stock/fhpg/detail/600519`
- 输出：总结分红/配股频率与股息率

---

## 开发者检查清单

在项目里真正启用本 Skill 前，请确认：

- [ ] 已实现 **分红数据接口**（含分红金额、股息率等关键字段）
- [ ] 函数、结构体、字段均有清晰中文注释，说明 **单位/币种/比例含义**
- [ ] 若使用外部数据源（聚宽、TuShare、券商 API 等），已处理好：
  - [ ] 鉴权/Token 管理
  - [ ] 调用频率限制
  - [ ] 网络错误与数据缺失的容错
- [ ] 本 SKILL.md 内容已根据真实实现的函数名/字段名进行同步调整
