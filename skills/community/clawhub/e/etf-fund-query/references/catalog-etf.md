# ETF信息查询 — 接口字段权威参考

> 编写脚本前必读：数据路径、字段名、单位均以本文件为准。
>
> 说明：
> - 本文所有路径都是 JSON 路径。
> - `$` 表示返回 JSON 的根节点。
> - 默认按 catalog 中的路径取值；只有路径失败、字段缺失或结构可疑时，才先查看真实响应结构再继续。
> - 如果按 catalog 取值失败，不要跨接口猜路径。必须先请求该接口，检查根节点有哪些 key、`data` 是对象/数组/空值，以及列表真实位于哪一层。
> - 本 skill 不提供实时行情类信息。

---

## 公共请求头

所有接口请求均需携带以下请求头：

```
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external
```

---

## `POST /skill/v1/search/etf` — 关键词搜索ETF

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 支持ETF名称、代码模糊搜索 |
| page | integer | 否 | 页码，从1开始，默认1 |
| pageSize | integer | 否 | 每页条数，建议10-100，默认10 |

**最终数据路径**：`$.data.data[]`（⚠️ 不是 `$.data.list[]`）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF交易代码，6位数字 |
| fundName | string | ETF产品全称 |
| extdSecuSht | string | ETF产品简称 |
| indexCode | string | 跟踪指数代码（不带后缀） |
| indexName | string | 跟踪指数名称 |
| indexType | string | 跟踪指数类型 |
| fundScale | number | ETF规模（**元**，÷1e8=亿） |
| eodPctChg1D/1W/1M/3M/TY/1Y/3Y/5Y | number | 各周期涨跌幅（%） |
| avgAmount1W/1M/3M/TY/1Y | number | 各周期日均成交额（元） |
| netInflow1D/1W/1M/3M/TY/1Y | number | 各周期净流入（元） |
| excessReturn1Y | number | 近1年超额收益（%） |
| unitAccBonus | number | 单位累计分红（元） |
| accBonusCount | integer | 累计分红次数（次） |
| currBonusDt | string | 最近分红权益登记日，yyyy-MM-dd |
| dividendYield | number | 指数股息率（%） |
| PETtm | number | PE-TTM（倍）⚠️ 注意大小写 |
| PETtm5Y | number | PE近5年分位（%） |
| PBLf | number | PB-LF（倍）⚠️ 注意大小写 |
| PBLf5Y | number | PB近5年分位（%） |
| PSTtm | number | PS-TTM（倍）⚠️ 注意大小写 |
| PSTtm5Y | number | PS近5年分位（%） |
| fundManageComp | string | 基金管理人 |
| fundManagerCurrent | array | 基金经理信息 |
| establishDt | string | 成立日，yyyy-MM-dd |
| lstDt | string | 上市日，yyyy-MM-dd |
| mgtFee | number | 管理费（%） |
| trstFee | number | 托管费（%） |
| relatedFunds | array | 联接基金列表 |

**分页信息路径**：`$.data.totalNum`、`$.data.pageNum`、`$.data.pageSize`

---

## `POST /skill/v1/etf/detail` — 批量ETF详情

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | ETF代码列表，最多10个 |

**最终数据路径**：`$.data[]`（数组，每个元素对应一只ETF）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/未找到该基金/代码类型不匹配/查询失败 |
| detail | object | 详情对象，仅 availabilityStatus="有数据" 时存在 |

`detail{}` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 交易代码 |
| fundName | string | 基金名称（产品名，不作为ETF对外展示简称） |
| chiName | string | 基金全称 |
| extdSecuSht | string | 扩位简称（ETF对外展示名优先使用此字段） |
| indexCode | string | 跟踪指数代码 |
| indexName | string | 跟踪指数名称 |
| indexSht | string | 指数简称 |
| firstClass | string | 指数一级分类 |
| secondClass | string | 指数二级分类 |
| establishDt | string | 成立日，yyyy-MM-dd |
| lstDt | string | 上市日，yyyy-MM-dd |
| exchName | string | 上市场所 |
| mgtFee | number | 管理费（%） |
| trstFee | number | 托管费（%） |
| fundManageComp | string | 基金管理人全称 |
| fundManageSht | string | 基金管理人简称 |
| fundStatus | string | 基金状态 |
| pubDt | string | 数据更新日期，yyyy-MM-dd |
| fundScale | number | 产品规模（**元**，÷1e8=亿） |
| unitNav | number | 单位净值（元） |
| navPctChg1D | number | 单位净值当日涨跌幅（%） |
| eodPctChg1D/1W/1M/3M/6M/1Y/3Y/5Y/TY/Bgn | number | 各周期收盘涨跌幅（%） |
| navPctChg1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 各周期复权净值收益率（%） |
| annTrackError1Y | number | 近1年年化跟踪误差（%） |
| avgTurnoverRate1M | number | 近1月平均换手率（%） |
| amount1W/1M/3M/TY/1Y/3Y/5Y | number | 各周期成交额（元） |
| avgAmount1W/1M/3M/TY/1Y/3Y/5Y | number | 各周期日均成交额（元） |
| netInflow1D/1W/1M/3M/6M/1Y/3Y/5Y | number | 各周期净流入（元） |
| sharpRatio1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 夏普比率 |
| maxDown1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 最大回撤（%） |
| unitAccBonus | number | 单位累计分红（元） |
| accBonusCount | number | 累计分红次数（次） |
| currBonusDt | string | 最近分红日期 |
| fundManagerCurrent | array | 现任基金经理 |
| fundManagerFormer | array | 历任基金经理 |
| relatedFunds | array | 联接基金 |


---

## `POST /skill/v1/etf/holdings` — 批量ETF持仓

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | ETF代码列表，最多10个 |
| date | string | 否 | 持仓日期 yyyy-MM-dd，不传返回最新报告期 |

**最终数据路径**：`$.data[]`（数组）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/未找到该基金/代码类型不匹配/无持仓数据/查询失败 |
| holdingItems | array | 持仓明细，仅 availabilityStatus="有数据" 时存在 |

`holdingItems[]` 内字段（来自 ETFStockHoldingItem schema）：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金交易代码 |
| endDt | string | 报告期截止日期，yyyy-MM-dd |
| stockCode | string | 股票代码（6位） |
| secuSht | string | 股票简称 |
| holdNavRat | number | 占净值比例（%） |
| sInfoWindcode | string | 基金Wind代码 |
| stockWindcode | string | 股票Wind代码 |

---

## `POST /skill/v1/etf/return` — 批量ETF区间收益率

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| codes | array | 是 | ETF代码数组，最多10只 |
| timeMode | string | 是 | PERIOD（预设周期）或 RANGE（自定义区间） |
| period | string | PERIOD时必填 | 1D/1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY（今年以来）/INCE（成立以来） |
| startDate | string | RANGE时必填 | yyyy-MM-dd |
| endDate | string | RANGE时必填 | yyyy-MM-dd |
| boundaryMatchMode | string | 否 | STRICT/FLEXIBLE（默认FLEXIBLE，允许边界收缩取有效数据） |

**最终数据路径**：`$.data[]`（数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF代码 |
| indexCode | string | 跟踪指数代码 |
| startDate | string | 实际区间开始日期 |
| endDate | string | 实际区间结束日期 |
| returnRate | number | 区间收益率（%）⚠️ 见下方说明 |
| availabilityStatus | string | 有数据/API接口无数据/历史查询无数据/不支持的期间/API调用异常/系统异常 |

> ⚠️ **returnRate 异常值处理**：
> - status≠有数据时，returnRate 字段**完全缺失**（非 null），必须用 `.get('returnRate')`
> - status=有数据 但 returnRate=-888.89 时，为 API 哨兵值，表示历史不足以计算此周期，需过滤：`if returnRate is not None and returnRate > -100`

---

## `POST /skill/v1/etf/dividends` — 批量ETF历史分红

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | ETF代码数组，最多10只 |
| startDate | string | 否 | 查询开始日期，不传从最早记录 |
| endDate | string | 否 | 查询结束日期，不传到最新记录 |

**最终数据路径**：`$.data[]`（数组）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/无历史分红/未找到该基金/代码类型不匹配/查询失败 |
| dividendItems | array | 分红明细，按时间倒序排列 |

`dividendItems[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金交易代码 |
| eqyRecordDt | string | 权益登记日，yyyy-MM-dd |
| dvdBenDt | string | 分红计算基准日，yyyy-MM-dd |
| cashDvdPerShTax | number | 每份分红金额（元） |
| payDt | string | 红利发放日（场内），yyyy-MM-dd |
| divPayDt | string | 红利发放日（场外），yyyy-MM-dd |

---

## `GET /skill/v1/discovery/top-etf` — 实时涨幅前10 ETF

**无请求参数**

**最终数据路径**：`$.data.list[]`（⚠️ 不是 `$.data[]`，而是 `$.data.list[]`）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF代码 |
| fundName | string | ETF名称 |
| indexCode | string | 跟踪指数代码 |
| indexName | string | 跟踪指数名称 |

> 该接口为实时涨幅榜来源。本 skill 对该接口只使用以上字段，不展示实时行情类数据。

---

## `GET /skill/v1/discovery/hot-search` — 热搜榜单

**无请求参数**

**最终数据路径**：`$.data[]`（数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | string | 热搜关键词 |

> 该接口为当日指数直通车小程序内搜索累计热搜榜。

---

## `POST /skill/v1/search/etf-by-stock` — 按股票反查ETF

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stockCodes | array | 是 | 股票代码列表（6位数字，不带交易所后缀） |
| onlyIncludeFullMatch | string | 否 | Y=只看全包含，N=任意包含，默认先Y后N降级 |
| pageNum | integer | 否 | 页码，默认1 |
| pageSize | integer | 否 | 每页条数，默认10 |
| sortField | string | 否 | 排序字段 |
| sortOrder | string | 否 | desc（降序）/ asc（升序） |

**最终数据路径**：`$.data{}`（对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| list[] | array | ETF列表（⚠️ 不是 `data[]`，位于 `$.data.list[]`） |
| totalCount | integer | 总记录数 |
| totalPage | integer | 总页数 |
| maxHoldNavRat | number | 最大持仓占净值比例（%） |
| matchedStocks[] | array | 匹配股票信息（key=代码, label=名称） |

`$.data.list[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF代码 |
| fundName | string | ETF名称 |
| extdSecuSht | string | ETF简称 |
| indexCode | string | 跟踪指数代码 |
| indexName | string | 指数名称 |
| firstClass | string | 指数一级分类 |
| totalRatio | number | 持仓合计比例（%） |
| fundScale | number | 资产规模（元） |
| holdingsDetail | array | 持仓明细 |

**降级策略**：`onlyIncludeFullMatch:"Y"` 返回空时改 `"N"` 重试，并告知用户条件已放宽。

---

## 单位速查

| 字段 | 接口 | 单位 | 换算 |
|------|------|------|------|
| fundScale | etf/detail.detail | 元 | ÷1e8=亿 |
| fundScale | `$.data.data[]`（search/etf） | 元（可为null） | ÷1e8=亿 |
| fundScale | `$.data.list[]`（etf-by-stock） | 元 | ÷1e8=亿 |
| netInflow* | etf/detail.detail | 元 | ÷1e8=亿 |
| holdNavRat | etf/holdings.holdingItems[] | % | 直接展示 |
| cashDvdPerShTax | etf/dividends.dividendItems[] | 元/份 | 直接展示 |
| annTrackError1Y | etf/detail.detail | % | 直接展示；搜索接口没有该字段时先查 detail |

## 名称字段使用规则

| 接口 | 对外展示名 | 说明 |
|------|------------|------|
| etf/detail | `detail.extdSecuSht` | ETF detail 会同时返回 `fundName`、`chiName`、`extdSecuSht`，面向用户展示时优先使用扩位简称 |
| search/etf | `$.data.data[].extdSecuSht` | 搜索列表同样优先展示 ETF 产品简称 |
| etf-by-stock | `fundName`（无 `extdSecuSht` 时） | 若返回 `extdSecuSht` 则优先，否则使用接口返回的 `fundName` |

## 代码格式速查

| 场景 | 正确格式 | 常见错误 |
|------|----------|----------|
| ETF代码入参 | `510300`（6位数字） | `510300.SH`、`510300.SZ`、`510300.OF` |
| 批量ETF代码 | `["510300", "159915"]` | 带交易所后缀或基金后缀 |

## 数据路径速查

| 接口 | 结果路径 | 常见错误 |
|------|---------|---------|
| search/etf | `$.data.data[]` | 误用 `$.data.list[]` |
| etf/detail | `$.data[]` → `[i].detail{}` | 忘记检查 availabilityStatus |
| etf/holdings | `$.data[]` → `[i].holdingItems[]` | 同上 |
| etf/return | `$.data[]` → `[i].returnRate` | status≠有数据时 returnRate 字段**缺失**（非null），需用 `.get('returnRate')` |
| etf/dividends | `$.data[]` → `[i].dividendItems[]` | 忘检查 availabilityStatus |
| top-etf | `$.data.list[]` | 仅用于涨幅榜；误用 `$.data[]` |
| hot-search | `$.data[]` | 无嵌套 |
| etf-by-stock | `$.data.list[]` | 误用 `$.data.data[]` |
