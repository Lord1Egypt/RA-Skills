# ETF信息查询 — 接口字段权威参考（v3）

> 编写脚本前必读：数据路径、字段名、单位均以本文件为准。
>
> 说明：
> - 本文所有路径都是 JSON 路径。
> - `$` 表示返回 JSON 的根节点。
> - 默认按 catalog 中的路径取值；只有路径失败、字段缺失或结构可疑时，才先查看真实响应结构再继续。
> - 如果按 catalog 取值失败，不要跨接口猜路径。必须先请求该接口，检查根节点有哪些 key、`data` 是对象/数组/空值，以及列表真实位于哪一层。

---

## 公共请求头与信封（v3）

所有接口请求均需携带以下请求头：

```
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external
```

**统一约定（v3）**：

- 接口分为两类：**GET 接口**参数走 URL query（键值对，数组用英文逗号拼接的字符串）；**POST 接口**参数走 JSON body。
- 除 `search/all`、`search/etf-advanced` 外，**POST 接口不再有公共 `requestId` 参数**；GET 接口一律无 `requestId`。
- 所有接口响应外层信封统一：`$.success`（boolean）、`$.code`（**string**，`"0000"` 表示成功）、`$.message`（string，成功为"成功"）、`$.data`。**无** `$.requestId`/`$.timestamp` 外层字段（部分接口 `$.data` 内含 `serverTime`）。下文只描述 `$.data` 及以内结构。
- 所有 GET 接口的数组参数均以**英文逗号拼接的字符串**传递（如 `fundCodes=510300,159915`），不要传 JSON 数组。

---

## 回答口径说明模板（输出必守）

回答中涉及**数值/数据时，必须随数据给出完整口径**，否则判为口径说明缺失。逐项必守：

1. **凡涉及区间（收益、涨跌幅、分位、日均成交额、净流入、跟踪误差、回撤等），必须给出区间起止日期**，不得只说"近1年/近3个月"：
   - 正确示例：`近1年（2025-09-17~2026-09-17）收益 +12.3%`、`净流入近1个月（2026-08-17~2026-09-17）`。
   - 区间由查询日回推时，写明"自查询日（2026-09-17）往前推 N 个月/年"。
2. **凡实时/盘中行情（最新价、涨跌幅、最新一笔），必须给出行情时间戳**：
   - 接口返回精确时间（如 `quote/etf/single` 的 `date+timeStamp`）→ 写出具体日期与时分秒；
   - 接口不返回时间戳（如 `discovery/top-etf` 只有 `lastPrice/changeRate`）→ 如实注明"接口返回的最新一笔实时行情，无具体时间戳"，**不得编造日期/时间**。
3. **快照类数据（规模、持仓、权重、估值、报告期指标）必须给出数据截止日/报告期**（如 `fundScaleDate`、`rptDt`、`positionDate`），不得只写"最新""最新报告期"。
4. **口径注与正文数据一一对应**：正文引用的每个数字（如"最新价"）在口径注中都能找到取数口径，正文未出现的数字不要出现在口径注中。
5. **多个相近数字并存时（如两个不同区间的收益），必须说明各自区间起点/口径差异**，避免读者混淆。
6. **单位换算必须标注**：亿元/万元/元、亿股/万手、百分比等，换算关系（如 `元 ÷ 1e8 = 亿`）在首次出现时说明。
7. **排序/筛选说明**：若排序或去重在本地完成（接口无排序参数），须说明"按 X 字段本地排序/去重"；分页接口须说明扫描范围（是否翻页取全）。
8. **行情时间早于/晚于数据日期的矛盾必须解释**（如净值截至 09-04、区间收益却称截至 09-17），不得同时出现冲突口径不解释。
9. **净值口径与场内价格口径必须区分**：`etf/interval-return` 同时返回 `returnRate`（单位净值口径）与 `priceReturnRate`（场内收盘价口径，默认后复权）；两者并列展示时必须注明各自口径与复权方式，只给一个数字时也要说明是"净值收益"还是"场内涨幅"，不得混用。

---

## `POST /skill/v3/search/all` — 统一关键词搜索（searchType=etf）

按关键词模糊搜索，`searchType=etf` 时返回匹配 ETF 列表及随附行情、规模、各周期涨跌幅等比较字段。适用于用户未提供具体代码时的检索。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| searchType | string | 是 | `etf`（本技能用 etf） |
| keyword | string | 否 | 搜索关键词，支持 ETF 产品名称、代码等模糊搜索 |
| page | integer | 否 | 页码，从 1 开始，默认 1 |
| pageSize | integer | 否 | 每页条数，建议 10-100，默认 10 |

**最终数据路径**：`$.data.etfFundList.data[]`（⚠️ 不是 `$.data.etfFundList.list[]`，也不是 `$.data.data[]`）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF交易代码，6位数字 |
| fundName / fundNameSht | string | 产品全称（可能含 HTML 高亮标签，用 `fullName` 或去除标签后展示）/ 简称 |
| chiName / fullName / showFullName | string | 法律全称 / 完整名称 / 展示全称 |
| originalTrdCode | string | 原始交易代码（与 trdCode 相同或别名） |
| fundType | string | 基金类型 |
| fundScale | number | ETF规模（**元**，÷1e8=亿） |
| lastPrice / changeRate | number | 最新价（元）、实时涨跌幅（%）【随附行情，可直接使用】 |
| unitNav | number | 单位净值（元） |
| eodPctChg1Y | number | 近1年涨跌幅（%） |
| indexCode / indexSht / indexType | string | 跟踪指数代码、简称、分类 |
| isEfund | number | 是否易方达产品（0/1） |
| fundManageSht / originalFundManageComp | string | 管理人简称 / 全称 |
| fundManagerCurrent | array | 基金经理信息（psnCode、psnName） |
| score | number | 相关度得分 |

**分页信息路径**：`$.data.etfFundList.pageNum`、`pageSize`、`totalNum`、`serverTime`。

> **分页规则**：`pageSize` 取大值一次取回候选，以 `totalNum` 为界，仅当前几页确实无匹配时才翻页，最多翻页 5 页，仍覆盖不全时在回答中说明筛选条件、覆盖范围与排序口径，不得继续扫库；多产品详情用批量接口一次传入全部代码，禁止逐个单查。
>
> ⚠️ 本接口返回 `$.data` 内含 `etfFundList`、`stockList`、`outIndexFundList`、`indexList` 四组，本技能只读取 `etfFundList`。`fundName`/`fundNameSht` 可能含 `<span style='color: ...'>` 高亮标签，展示时去掉标签或用 `fullName`。

---

## `POST /skill/v3/search/etf-advanced` — ETF 高级搜索（服务端筛选/排序）

> **字段覆盖**：除筛选/排序外，本接口随附行情已含 `lastPrice`/`changeRate`/`premiumRate`（溢折率）/`turnoverRate`（换手率）/`dealBalance`（成交额）/`fundScale`，因此"列出前 N 只 ETF 的最新价、涨跌幅、溢折率、成交额、换手率"类问题**一次调用即可**；只有还需 IOPV/昨收/成交量/精确行情时间（timeStamp）时才补调 `quote/etf/single`。

按关键词 + 服务端筛选（`filters`）+ 排序（`sortField`/`sortOrder`）检索 ETF。适用于需要按规模、估值、表现等条件精确筛选并排序的场景。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 关键词 |
| page / pageSize | number | 否 | 默认 1 / 10 |
| sortField | string | 否 | 排序字段（枚举见下），传 `sortOrder` 时必填 |
| sortOrder | string | 否 | `asc` / `desc` |
| fundCodes | array | 否 | 指定代码集合内筛选 |
| filters | object | 否 | 复杂筛选条件（见下） |
| requestId | number | 否 | 请求唯一标识 |

`sortField` 枚举（常用）：`fundScale`（规模）、`lastPrice`、`changeRate`、`eodPctChg1D/1W/1M/3M/6M/1Y/3Y/5Y/TY`（各周期涨跌幅）、`amount1W~5Y/TY`、`netInflow1W/1M/3M`、`turnoverRate`、`premiumRate`、`PETtm/PBLf/PSTtm`、`PETtm5Y/PBLf5Y/PSTtm5Y`、`ROE`、`dividendYield`、`mgtFee/trstFee`、`unitAccBonus/accBonusCount/currBonusDt`、`trackErrorLst/excessReturnLst`、`establishDt`、`lastYearYield/prevYearYield` 等。

`filters` 常用项（数值均为 `{"min": n, "max": n}`，只传需限制的一侧；数组为多选）：

- `productType[]`：产品类型多选（如 `股票-规模指数（宽基）-中国-市场类型-A股`、`股票-风格因子-红利` 等，枚举见接口文档）；
- 表现：`eodPctChg1D/1W/1M/3M`；
- 估值：`PETtm/PETtm5Y`、`PBLf/PBLf5Y`、`PSTtm/PSTtm5Y`；
- 基本面：`dividendYield`、`ROE`、`operatingRevenueYoy`、`parentComOwnerYoy`；
- 规模与流动性：`fundScale`、`avgAmount1W/1M/3M/1Y/TY`、`netInflow1W/1M/3M`；
- 费率：`mgtFee`、`trstFee`；
- 其他：`indexCode[]`、`currBonusDt[]`、`fundManageComp[]`、`unitAccBonus`、`accBonusCount`、`trackErrorLst`、`excessReturnLst`、`lastYearYield`、`prevYearYield`。

**最终数据路径**：`$.data.data[]`（平铺 ETF 列表）；分页在 `$.data.pageNum`、`pageSize`、`totalNum`、`serverTime`。

`$.data.data[]` 关键字段（与 search/all 类似但更全）：

- 标识：`trdCode`、`fundName`、`extdSecuSht`（扩位简称，对外展示名）、`chiName`、`capitalType`、`exchName`、`lstDt`（上市日）、`establishDt`（成立日）、`fundStatus`、`indexCode/indexName/indexSht/indexType`、`firstClass/secondClass/thirdClass`、`indexTopType/indexBottomType`、`authorizedIndex`；
- 行情：`lastPrice`（元）、`changeRate`（%）、`premiumRate`（折溢价率 %）、`turnoverRate`（换手率 %）、`dealBalance`（成交额，元）；
- 规模/净值：`fundScale`（**元**）、`unitNav/accuUnitNav`（净值，元）、`navPctChg1D`（%）⚠️ 本接口净值涨跌幅**仅 `navPctChg1D`**，各周期净值收益率在 etf/detail 才有；
- 表现：`eodPctChg1D/1W/1M/3M/6M/1Y/3Y/5Y/TY/Bgn`（%）；
- 资金：`netInflow1D/1W/1M/3M/6M/1Y/3Y/5Y/TY`（元）、`netInflows[]`（近5日明细：`trdDt`、`netInflow1D`）；
- 成交：`amount1W~5Y/TY`、`avgAmount1W~5Y/TY`（元）、`avgTurnoverRate1M`（%）；
- 费率/管理人：`mgtFee/trstFee`（%）、`fundManageComp/fundManageSht/fundCustComp`、`fundManagerCurrent[]`（psnCode/psnName）；
- 估值：`PETtm/PBLf/PSTtm`（倍）、`PETtm5Y/PBLf5Y/PSTtm5Y`（近5年分位 %）；
- 跟踪误差：`annTrackError1Y`、`trackErrorLst`、`excessReturn1Y/excessReturnLst`（%）；
- 分红：`unitAccBonus`（元）、`accBonusCount`、`currBonusDt`；
- 关联：`relatedFunds[]`（`trdCode`、`relatedTrdCode`、`relatedFundSht` 联接基金）；
- 补充：`fundNameHighLight`（高亮名，展示用无 HighLight 字段）、`score`（相关度）、`priority`/`selectedPortfolio`/`createTime`（可能为 null）、`fundManagerFormer`（可能为 null）。

> ⚠️ `trdCodeHighLight`、`extdSecuShtHighLight` 含 HTML 高亮标签，对外展示必须用不带 HighLight 的字段。

---

## `POST /skill/v3/search/etf-by-stock` — 按股票反查ETF

根据股票代码列表搜索持有这些股票的 ETF，返回 ETF 列表及持仓占比、规模、跟踪指数等信息。适用于「哪些 ETF 重仓了某只股票」类问题。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stockCodes | array | 是 | 股票代码列表（6位数字，不带交易所后缀），如 ["600519","000858"] |
| onlyIncludeFullMatch | string | 否 | `Y`=仅返回同时持有全部输入股票的ETF，`N`=任意包含（默认） |
| showOnlyMaxIndexScaleMatch | string | 否 | `Y`=仅返回相同跟踪指数中规模最大的ETF（推荐与 maxScaleFlag 配合） |
| pageNum / pageSize | number | 否 | 页码/每页条数，默认 1/10 |

**最终数据路径**：`$.data.list[]`；分页信息在 `$.data.currentPage`、`totalPage`、`totalCount`；`$.data.maxHoldNavRat` 为最大持仓占比。

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode / fundName / extdSecuSht | string | ETF代码、名称、简称 |
| fundType | string | 基金类型（如 "etf"） |
| indexCode / indexName / indexSht / indexType | string | 跟踪指数与分类 |
| firstClass / secondClass / thirdClassMarketType / thirdClassMarketValue / className | string | 指数分类 |
| totalRatio | number | 查询股票的持仓合计比例（%） |
| holdings | array | 该ETF实际持有的输入股票代码列表 |
| holdingsDetail | array | 查询股票在该ETF中的持仓明细（`trdCode`、`endDt`、`stockCode`、`secuSht`、`holdNavRat`、`stockWindcode`、`sinfoWindcode`）；用户要"具体持仓明细"时读取本字段 |
| fundScale | string | 资产规模（**元**，÷1e8=亿） |
| unitNav / navPctChg1D / eodPctChg1M / eodPctChgTM | string | 净值与涨跌幅（%） |
| pubDt / exchName | string | 数据更新日期、上市场所 |
| maxScaleFlag | boolean | 是否相同跟踪指数中规模最大 |
| authorizedIndex | boolean | 跟踪指数是否有权限 |
| sInfoWindcode / indexSInfoWindcode | string | 基金/指数万德代码 |

辅助回显：`$.data.matchedStocks[]`（匹配到的股票 key/label）、`$.data.requestList[]`（请求股票回显，含 stockCode/secuSht/holdNavRat/labelCode/labelName）。

**降级策略**：`onlyIncludeFullMatch:"Y"` 返回空时改 `"N"` 重试，并告知用户条件已放宽。

---

## `GET /skill/v3/etf/detail` — 批量ETF详情

批量查询多只 ETF 的详细信息：基本信息、费率、跟踪指数、净值、各周期涨跌幅、成交额/净流入、跟踪误差与超额、夏普比率、最大回撤、基金经理、联接基金及随附实时行情。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | string | 是 | ETF基金代码，英文逗号分隔，最多 20 个 |

**最终数据路径**：`$.data.data[]`（数组，每个元素对应一只 ETF；`$.data.serverTime` 为服务器时间）

> ⚠️ v3 起响应**去掉** `fundCode`/`availabilityStatus`/`detail` 包装，字段直接平铺在每项上；不再有 `availabilityStatus` 标记，代码类型不匹配或未找到时该项直接缺失或为空。

`$.data.data[]` 内字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode / capitalType | string | 交易代码、基金类型 |
| fundName / chiName / extdSecuSht | string | 基金名称（产品名）/ 全称 / 扩位简称（ETF对外展示名优先使用 extdSecuSht） |
| indexCode / indexName / indexSht / benchMark / indexType | string | 跟踪指数与业绩基准 |
| firstClass / secondClass / thirdClassMarketType / thirdClassMarketValue / className | string | 指数分类 |
| establishDt / lstDt / exchName | string | 成立日、上市日、上市场所 |
| mgtFee / trstFee | number | 管理费、托管费（%） |
| fundManageComp / fundManageSht / fundCustComp / fundCustCompSht | string | 基金管理人全称/简称、托管人全称/简称 |
| fundStatus / pubDt | string | 基金状态、数据更新日期 |
| isHugua | string | 是否沪挂（"0"/"1"） |
| fundScale | number | 产品规模（**万元**，÷1e4=亿 ⚠️ v3 单位） |
| unitNav / accuUnitNav / navPctChg1D | number | 单位净值、累计单位净值（元）、当日净值涨跌幅（%） |
| lastPrice / changeRate / turnoverRate | number | 最新价（元）、实时涨跌幅（%）、换手率（%）【随附行情】 |
| eodPctChg1D/1W/1M/3M/6M/1Y/3Y/5Y/TY/Bgn | number | 各周期收盘涨跌幅（%） |
| navPctChg1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 各周期复权净值收益率（%） |
| amount1W~5Y、avgAmount1W~5Y | number | 各周期成交额、日均成交额（**元**，÷1e8=亿） |
| netInflow1D/1W/1M/3M/6M/TY/1Y/3Y/5Y | number | 各周期净流入（**万元** ⚠️ v3 单位） |
| annTrackError1Y / trackError1Y / trackErrorLst | number | 近1年年化跟踪误差、近1年跟踪误差、上市至今跟踪误差（%） |
| excessReturn1Y / excessReturnLst | number | 近1年、上市至今超额收益（%） |
| sharpRatio1M~Bgn | number | 夏普比率（1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn） |
| maxDown1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 最大回撤（%）⚠️ 无 maxDown1W |
| avgTurnoverRate1M | number | 近1月日均换手率（%） |
| unitAccBonus / accBonusCount / currBonusDt | | 分红信息 |
| netInflows | array | 申赎净流入（近5日）：trdDt、trdCode、netInflow1D（万元 ⚠️） |
| fundManagerCurrent / fundManagerFormer | array | 现任/历任基金经理（trdCode、psnCode、psnName、posiBgnDt、posiEndDt、gender、managementTime、manageStatus 1在职/0离任、performance 任期业绩%、sequence） |
| relatedFunds | array | 联接基金（trdCode、relatedTrdCode、relatedFundSht） |
| lastYearYield / prevYearYield | number | 上年/前年收益率（%） |
| authorizedIndex | boolean | 跟踪指数是否有权限 |
| indexSInfoWindcode / sinfoWindcode / indexRegionType | string | 指数/基金万德代码、指数地区 |

> - `fundNavJson`、`benchmarkReturnJson` 是数据文件路径，不当作内嵌 JSON 解析。
> - 跟踪误差统一使用 `annTrackError1Y`。
> - ⚠️ v3 单位口径：`fundScale`、`netInflow*`、`netInflows[].netInflow1D` 单位为**万元**（÷1e4=亿）；**`amount*`、`avgAmount*` 为元**（÷1e8=亿），两者不同，展示前必须按各自口径换算。

---

## `POST /skill/v3/etf/holdings` — 批量ETF前十大持仓

批量查询多只 ETF 的最新（或指定日期）前十大重仓股。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | ETF代码列表，最多 10 个 |
| date | string | 否 | 持仓日期 yyyy-MM-dd，不传返回最新报告期 |

**最终数据路径**：`$.data.data[]`（⚠️ 实际响应为 `{serverTime, data:[...]}`，列表在 `data.data` 下；v3 起为**平铺列表**，不再按基金分组，也不再有 `fundCode`/`availabilityStatus`/`holdingItems` 包装）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金代码 |
| endDt | string | 报告期截止日期 yyyy-MM-dd |
| stockCode / secuSht | string | 股票代码、股票简称 |
| holdNavRat | number | 占净值比例（%） |
| stockWindcode / sinfoWindcode | string | 股票/基金万德代码 |

> ⚠️ v3 平铺后：多只基金的结果混在一个数组里，回答"每只基金的前十大持仓"时必须按 `trdCode` 分组再展示，不要交叉混排。

---

## `GET /skill/v3/etf/return` — 批量ETF区间收益

批量查询多只 ETF 在预设周期或自定义区间内的收益率（%）。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| codes | string | 是 | ETF代码，英文逗号分隔，最多 10 只 |
| timeMode | string | 是 | `PERIOD`（预设周期）或 `RANGE`（自定义区间） |
| period | string | PERIOD时必填 | `1M/3M/6M/1Y/3Y/5Y/TY/INCE` |
| startDate | string | RANGE时必填 | yyyy-MM-dd |
| endDate | string | RANGE时必填 | yyyy-MM-dd |
| boundaryMatchMode | string | 否 | 仅 RANGE 生效：`FLEXIBLE`（默认，允许边界收缩到最近可交易日）/ `STRICT`（严格） |

> ⚠️ 默认用 FLEXIBLE；STRICT 遇非交易日边界会直接报错（success:false，提示建议前后交易日），应如实转述错误并建议改用 FLEXIBLE 重查，展示实际收缩后的起止日期与收益率。

**最终数据路径**：`$.data.data[]`（⚠️ v3 多包一层 `data`；`$.data.serverTime` 为服务器时间）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF代码 |
| indexCode | string | 与 trdCode 相同的代码本身；RANGE 模式下可能为 null |
| startDate / endDate | string | 实际区间起止日期，yyyy-MM-dd |
| returnRate | number | 区间收益率（%，保留2位小数）⚠️ 见下方说明 |
| availabilityStatus | string | 有数据 / API接口无数据 / 历史查询无数据 / 不支持的期间 / API调用异常 / 系统异常 |

> ⚠️ **returnRate 空值处理**：availabilityStatus≠有数据 时，`returnRate` 为 null，必须用 `.get('returnRate')` 取值，不得把空值当作 0。历史不足时状态为"历史查询无数据"，用自然语言说明，不补造收益率。
>
> ⚠️ 展示时以返回的 `startDate`/`endDate` 为准（FLEXIBLE 模式下边界可能收缩到最近可交易日）。
>
> ⚠️ v3 预设周期枚举变为 `1M/3M/6M/1Y/3Y/5Y/TY/INCE`（**无 1W/1D**，新增 3Y/5Y/INCE）；查"近一周"等周期时改用 RANGE 模式。

---

## `GET /skill/v3/etf/interval-return` — 单只ETF区间收益（v3 新增；v3.2 起含场内价格口径）

查询**单只** ETF 的区间收益，**同时返回两个口径**：
- `returnRate`：**基金单位净值区间收益率**（净值口径）
- `priceReturnRate`：**场内收盘价区间涨跌幅**（价格口径，默认按 **BACKWARD 后复权**计算，含分红除权修正；超出历史深度或 K 线无数据时该字段为空）

与 `etf/return` 的区别：本接口一次只查一只，返回结构更简单，且**多一个场内价格口径字段**。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 单只ETF代码 |
| timeMode | string | 是 | `PERIOD` 或 `RANGE` |
| period | string | PERIOD时必填 | `1M/3M/6M/1Y/3Y/5Y/TY/INCE` |
| startDate / endDate | string | RANGE时必填 | yyyy-MM-dd |
| boundaryMatchMode | string | 否 | `FLEXIBLE`（默认）/ `STRICT` |
| **priceModel** | string | 否 | **v3.2 新增**。场内价格口径的复权方式：`ORIGINAL`（不复权）/ `BACKWARD`（后复权，**默认**）/ `FORWARD`（前复权）。仅影响 `priceReturnRate`，不影响 `returnRate` |

**最终数据路径**：`$.data`（单对象）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode / indexCode | string | ETF代码 / 与 trdCode 相同的代码本身（⚠️ RANGE 模式下 indexCode 可能为 null，同 etf/return） |
| startDate / endDate | string | 实际区间起止日期（⚠️ RANGE 模式按实际交易日边界调整：请求的非交易日会**前移/后移**到最近交易日，如请求 `2026-01-01` 返回 `2025-12-31`，即实际区间可能比请求**略微扩大**而非缩小；表述时以返回值为准，不得说成"收缩"） |
| returnRate | number | **净值口径**区间收益率（%，null 判空处理同 etf/return） |
| **priceReturnRate** | number | **场内价格口径**区间涨跌幅（%），受 `priceModel` 控制；无数据时为空 |
| availabilityStatus | string | 数据可用性状态（同上） |
| serverTime | string | 服务器时间 |

> ⚠️ **实测（2026-10-08 验证，510300 / PERIOD / 1Y）**：`returnRate=-4.0015%`（不随 priceModel 变化）；`priceReturnRate` 随 priceModel 变化——不传=**-3.45%**（等同 BACKWARD）、`ORIGINAL`=-6.60%、`BACKWARD`=-3.45%、`FORWARD`=-4.10%。非法取值（如 `BOGUS`）**静默回退默认值**，不报错。
>
> 📌 **口径使用规则**：用户问"**ETF 涨了多少/场内涨幅**"用 `priceReturnRate`（并注明复权方式）；问"**净值收益**"用 `returnRate`。两者并存时必须说明各自口径，不得只给一个数字而不注明来源口径。

---

## `POST /skill/v3/etf/dividends` — 批量ETF分红明细

批量查询多只 ETF 的历史分红明细，按分红时间倒序。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | ETF代码数组，最多 10 只 |
| startDate | string | 否 | 查询开始日期 yyyy-MM-dd，不传从最早记录 |
| endDate | string | 否 | 查询结束日期 yyyy-MM-dd，不传到最新记录 |

**最终数据路径**：`$.data.data[]`（⚠️ 实际响应为 `{serverTime, data:[...]}`，列表在 `data.data` 下；v3 起为**平铺列表**，不再按基金分组，也无 `fundCode`/`availabilityStatus`/`dividendItems` 包装）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金代码 |
| eqyRecordDt | string | 权益登记日，yyyy-MM-dd |
| dvdBenDt | string | 分红计算基准日，yyyy-MM-dd |
| cashDvdPerShTax | number | 每份分红金额（元） |
| payDt | string | 红利发放日（场内） |
| divPayDt | string | 红利发放日（场外） |

> ⚠️ v3 平铺后需按 `trdCode` 分组回答"每只基金的分红历史"。

---

## `POST /skill/v3/etf/etf-scale` — 批量ETF规模变动

批量查询多只 ETF 的规模与净流入变动（数据 T+1 延迟）。适用于「某 ETF 最新规模」「近一个月净流入情况」类问题。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| trdCodes | array | 是 | 基金代码列表，最多 20 个 |
| beginDate | string | 否 | 查询开始日期 yyyy-MM-dd，不传则返回每只基金最新一天数据 |
| endDate | string | 否 | 查询结束日期 yyyy-MM-dd，与 beginDate 配合使用 |

**最终数据路径**：`$.data[]`（按基金分组）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode / fundName | string | 基金代码、简称 |
| availabilityStatus | string | 有数据 / 未找到该基金 / 查询失败。单只失败不影响其他只 |
| scaleChanges | array | 规模变动列表（按日期倒序） |

`scaleChanges[]` 内字段：`trdCode`、`trdDt`（日期 yyyy-MM-dd）、`nscale`（规模，**万元**，÷1e4=亿）、`nnetInflow`（净流入，**万元**）、`sreferDate`（参考日期）。⚠️ **实际返回字段名为全小写 `nscale`/`nnetInflow`/`sreferDate`**（不要用驼峰 `nScale` 等拼写取值，会取不到）。

> ⚠️ 本接口规模/净流入单位为**万元**，与其他接口的元口径不同；数据存在 T+1 延迟，"今日规模"类问题应答最新可得日期。

---

## `GET /skill/v3/quote/etf/list` — 批量ETF精简行情（v3 改名自 quote/etf）

批量获取多个 ETF 的最新价、涨跌幅、成交额与规模。⚠️ **v3 批量接口不再返回完整盘口**（IOPV、溢折率、成交量、换手率、昨收、精确行情时间 timeStamp 均无），核心字段为 `lastPrice`/`changeRate`/`dealBalance`/`fundScale`，并随附 `date`（行情日期）及 `navPctChg*`/`eodPctChg*` 各周期涨跌幅。

> **调用前检查**：`search/all`、`etf-advanced`、`etf/detail`、`discovery/top-etf` 的响应已随附 `lastPrice`、`changeRate` 等行情字段。已通过它们获得问题所需的最新价或涨跌幅时，**禁止**再调本接口获取相同信息。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | ETF代码，英文逗号分隔，单次最多 50 个 |

**最终数据路径**：`$.data.dataInfo[]`（`$.data.serverTime` 为服务器时间）

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | string | ETF代码 |
| lastPrice | number | 最新价（元） |
| changeRate | number | 涨跌幅（%） |
| dealBalance | number | 成交额（元） |
| fundScale | number | 基金规模（**元**，÷1e8=亿） |
| date | integer | 行情日期，yyyyMMdd |
| navPctChg1M/1W/3M/6M/1Y/3Y/5Y/Bgn | number | 各周期净值收益率（%） |
| eodPctChg1W / eodPctChgTW | number | 近1周 / 本周以来收盘涨跌幅（%） |

> ⚠️ 本接口**无** IOPV/溢折率/换手率/昨收/成交量/精确行情时间（有 `date` 无 `timeStamp`）。用户需要**完整盘口**（IOPV、溢折率、成交量、换手率、昨收、精确行情时间）时，改用 `quote/etf/single`（单只）。

---

## `GET /skill/v3/quote/etf/single` — 单只ETF完整盘口+分钟（v3 新增）

查询**单只** ETF 的完整实时盘口（含 IOPV、溢折率、成交量、换手率、昨收、精确行情时间 `date + timeStamp`）及当日分钟序列。承接原 `quote/etf` 的完整盘口能力，但**仅单只**。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 单只ETF代码 |
| lastTimestamp | number | 否 | 上次最后时间戳：>0 仅返回该时间戳之后的新增分钟，=0/不传返回全量 |

**最终数据路径**：`$.data.latestQuote{}`（最新盘口快照）+ `$.data.list[]`（当日分钟序列）；`$.data.serverTime` 为服务器时间。

`latestQuote{}` 字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | string | ETF代码 |
| lastPrice | number | 最新价（元） |
| changeRate | number | 涨跌幅（%） |
| changeValue | number | 涨跌额（元，=lastPrice−yesterdayClosePrice） |
| yesterdayClosePrice | number | 昨收（元） |
| dealBalance / dealVolume | number | 成交额（元）、成交量（份） |
| turnoverRatio | number | 换手率（%，可能为 null） |
| iopv | number | IOPV 实时估值（元） |
| deviationRate | number | 溢折率（%，可能为 null） |
| date | integer | 行情日期，yyyyMMdd |
| timeStamp | integer | 行情时间，HHmmss |

`list[]` 内字段：`minute`（分钟时间戳，如 930 表示 9:30）、`lastPrice`（元）、`iopv`（元）、`changeRate`（%）。

> `date + timeStamp` 是行情数据时间，`serverTime` 是服务器处理时间。回答"现在/实时/盘中"口径问题必须注明精确行情时间；非交易时段表述为"接口返回的最新一笔行情"。
>
> ⚠️ 实际响应 `$.data` 顶层还会重复返回一个 `yesterdayClosePrice`（与 latestQuote 内一致），读取盘口以 `latestQuote{}` 为准。

---

## `POST /skill/v3/quote/etf/kline` — ETF历史K线

查询 ETF 历史 K 线（日K/周K/月K/分钟K），支持原始/前复权/后复权。适用于「近一年日K线」「周K走势」类问题。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | ETF代码（单只） |
| candlePeriod | string | 是 | `DAY`（日K）/ `WEEK`（周K）/ `MONTH`（月K）/ `MINUTE_1` / `MINUTE_5` / `MINUTE_15` |
| dateRange | string | 是 | 查询日期范围，格式 yyyyMMdd~yyyyMMdd，如 20260101~20260501 |
| candleModel | string | 否 | 复权模式：`ORIGINAL`（原始，默认）/ `FORWARD`（前复权）/ `BACKWARD`（后复权） |
| needFillKLine | integer | 否 | 是否补全K线：0=不补（默认）、1=补全 |

**查询范围限制**：日K 最多 500 天，周K/月K 最多 10 年，分钟K 最多 7 天，超出返回错误提示。

**最终数据路径**：`$.data.candle`（列名数组）+ `$.data.<代码>`（如 `$.data.510300`，与列名逐列对齐的二维数组）。⚠️ 无 `lastUpdateTime` 字段（实际 data 只有 `candle` 与代码两个 key）。

> 列名以返回的 `data.candle` 为准，固定为 `["date", "min_time", "open_px", "high_px", "low_px", "close_px", "deal_volume", "deal_amount"]`：`date` 为交易日（yyyyMMdd 整数）；`min_time` 为分钟时间（HHmm 整数，日K/周K/月K 为 0）；`open_px`/`high_px`/`low_px`/`close_px` 为开高低收（元）；`deal_volume` 成交量（份）、`deal_amount` 成交额（元）。解析时按下标与列名逐列对齐。

---

## `POST /skill/v3/quote/etf/realtime` — 批量ETF分时分钟行情（v3.1 改名自 quote/etf/minite）

批量获取多个 ETF 当日分时分钟行情，支持增量更新。⚠️ **v3 语义收窄为仅 ETF**（指数分钟请用 index-query 的 `quote/index/single`）。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodeList | array | 是 | ETF代码列表，最多 50 个 |
| date | string | 否 | 行情日期 yyyyMMdd，默认当天 |
| lastTimestamp | number | 否 | 0 获取全量；>0 仅获取该时间戳之后的新增分钟 |

**最终数据路径**：`$.data.dataList[]`（`$.data.serverTime` 为服务器时间）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | ETF代码 ⚠️ v3 用 `trdCode`（v2 为 `symbol`） |
| quoteList | array | 分钟序列：`minute`（分钟时间戳，如 930 表示 9:30）、`lastPrice`（元）、`iopv`（元）、`changeRate`（%） |

> ⚠️ v3 的 minite（现名 realtime） **不再返回 `latestQuote` 最新盘口快照**；需要最新快照（含精确行情时间）时改用 `quote/etf/single`。

---

## `GET /skill/v3/discovery/top-etf` — 涨幅前10 ETF

查询当前涨幅排名前 10 的 ETF 榜单（按跟踪指数去重）。适用于「今日涨幅居前的 ETF 有哪些」类问题。

**无请求参数**

**最终数据路径**：`$.data.list[]`

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode / fundName | string | ETF代码、名称 |
| indexCode / indexName | string | 跟踪指数 |
| lastPrice | number | 最新价（元） |
| changeRate | number | 涨跌幅（%） |

> ⚠️ **本接口不返回行情日期/时间戳字段**（只有 trdCode/fundName/indexCode/indexName/lastPrice/changeRate）。回答时口径表述为"接口返回的最新一笔实时行情"即可，**不得编造具体行情日期或时间**（如需日期，说明"榜单数据来自接口实时返回"）。
>
> 该接口为服务端涨幅榜来源，不要用少量行情样本自行重建榜单。

---

## `GET /skill/v3/discovery/hot-search-recommend` — 按类型热搜推荐（v3 结构变化）

返回热搜 ETF、热搜场外基金、热搜指数三组推荐列表。⚠️ v3 起**无 `type` 参数**，一次返回全部三组；响应结构从 `$.data[]` 改为 `$.data.{etfList, otcList, indexList}`。

**无请求参数**

**最终数据路径**：

- `$.data.etfList[]`：热搜ETF → `code`（代码）、`name`（名称）、`navPctChg1Y`（近一年涨跌幅 %，通常为 null）
- `$.data.otcList[]`：热搜场外基金 → `code`、`name`、`navPctChg1Y`（近一年涨跌幅 %，有值）
- `$.data.indexList[]`：热搜指数 → `code`、`name`、`navPctChg1Y`（近一年涨跌幅 %，通常为 null）

> 本技能读 `$.data.etfList[]`（热搜ETF）。⚠️ **口径务必准确：本接口返回的是"热搜推荐"列表（推荐性质的展示），不是按搜索次数统计的关键词热榜**——响应中只有 code/name/navPctChg1Y，**没有任何热度值、搜索次数或排序依据字段**，因此：
> - 不得表述为"按搜索热度从高到低""当日用户搜索次数累计"等，接口无此数据；
> - 应表述为"热搜推荐（指数直通车推荐列表）"，如"共返回 N 只"并全部列出（可能不足 5 只）；
> - 热搜推荐仅为热度展示，不代表收益推荐。

---


## `POST /skill/v3/quote/stock/list` — 批量股票实时行情（补充能力）

按代码批量查询个股最新价、涨跌幅、行情时间。用于回答涉及**个股**行情的补充问题（如 ETF 成分股当日表现）。

**请求参数**（body）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| builders | array | 是 | `[{"symbol":"300750","exchange":"2"}, ...]`；`symbol`=6位股票代码，`exchange`=`1`（上交所）/`2`（深交所）/`HK`（香港） |

**最终数据路径**：`$.data.dataInfo[]`；`$.data.serverTime` 为服务器时间。

| 字段 | 说明 |
|------|------|
| symbol / exchange | 股票代码 / 交易所 |
| lastPrice / changeRate | 最新价（元）/ 涨跌幅（%） |
| date / timeStamp | 行情日期（yyyyMMdd）/ 时间（HHmmss） |

> 本接口为**股票**行情，不是 ETF/指数行情；仅当用户明确询问个股时才使用。

---

## `GET /skill/v3/discovery/fund-manager-list` — 基金管理人列表（补充能力）

按关键字模糊匹配基金管理人全称/简称，返回管理人列表。用于回答"有哪些基金公司/管理人"类问题。

**请求参数**（URL query）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 否 | 管理人全称或简称模糊匹配，如"华夏" |

**最终数据路径**：`$.data[]`（顶层数组，非 $.data.data）。

| 字段 | 说明 |
|------|------|
| label | 管理人简称（用于显示），如"华夏基金" |
| key | 管理人全称（唯一标识），如"华夏基金管理有限公司" |
| pyIndex | 拼音首字母索引 |

---

## 单位速查

| 字段 | 接口 | 单位 | 换算 |
|------|------|------|------|
| fundScale | search/all、etf-advanced、quote/etf/list | 元 | ÷1e8=亿 |
| fundScale | **etf/detail** | **万元** ⚠️ | ÷1e4=亿 |
| fundScale / netInflow* / netInflows[].netInflow1D | **etf/detail** | **万元** ⚠️ | ÷1e4=亿 |
| amount* / avgAmount* | **etf/detail** | **元** ⚠️（非万元） | ÷1e8=亿 |
| nscale / nnetInflow | etf/etf-scale | **万元**（字段名全小写） | ÷1e4=亿 ⚠️ |
| dealBalance / dealVolume | quote/etf/single | 元 / 份 | ÷1e8=亿（dealVolume 仅在 single，list 无） |
| holdNavRat | etf/holdings、etf-by-stock | % | 直接展示 |
| cashDvdPerShTax | etf/dividends | 元/份 | 直接展示 |
| annTrackError1Y / 各涨跌幅 / returnRate | 全部接口 | % | 直接展示 |

## 名称字段使用规则

| 接口 | 对外展示名 | 说明 |
|------|------------|------|
| etf/detail | `extdSecuSht` | `fundName` 是产品名，`extdSecuSht` 是扩位简称 |
| search/all、etf-advanced | `extdSecuSht` 或去掉高亮标签的 `fundName` | 列表简称优先 `extdSecuSht`；`fundName` 可能含 `<span>` 高亮 |
| search/etf-by-stock | `extdSecuSht` | 基金简称 |
| discovery/top-etf | `fundName` | 榜单直接返回展示名 |

## 代码格式速查

| 场景 | 正确格式 | 常见错误 |
|------|----------|----------|
| ETF代码入参 | `510300`（6位数字） | `510300.SH`、`510300.SZ` |
| 批量代码（GET query） | `fundCodes=510300,159915` / `symbol=510300,510500`（逗号分隔字符串） | JSON数组 |
| 批量代码（POST body） | `["510300", "510500"]` | 带交易所后缀 |
| K线日期范围 | `dateRange=20260101~20260501`（yyyyMMdd~yyyyMMdd） | `2026-01-01` 带连字符 |
| 分时/业务日期 | 接口参数为 yyyy-MM-dd 或 yyyyMMdd，逐接口核对本文件 | 两种格式混用 |

## 数据路径速查

| 接口 | 结果路径 | 常见错误 |
|------|---------|---------|
| search/all | `$.data.etfFundList.data[]` | 误用 `$.data.data[]`；分页在 `$.data.etfFundList.totalNum` |
| search/etf-advanced | `$.data.data[]` | 分页在 `$.data.pageNum/totalNum` |
| search/etf-by-stock | `$.data.list[]` | fundScale 单位是元，÷1e8=亿 |
| etf/detail | `$.data.data[]`（平铺） | ⚠️ 无 availabilityStatus/detail 包装；fundScale 万元 |
| etf/holdings | `$.data.data[]`（平铺） | ⚠️ 实际多包一层 data+serverTime；已不再按基金分组，需按 trdCode 自行分组 |
| etf/return | `$.data.data[]` | ⚠️ v3 多包一层 data；status≠有数据时 returnRate 为 null |
| etf/interval-return | `$.data`（单对象） | 单只接口；含 `returnRate`（净值口径）+ `priceReturnRate`（场内价格口径，默认后复权，可选 `priceModel`） |
| etf/dividends | `$.data.data[]`（平铺） | ⚠️ 实际多包一层 data+serverTime；已不再按基金分组 |
| etf/etf-scale | `$.data[].scaleChanges[]` | 单位是万元；字段名全小写 nscale/nnetInflow/sreferDate |
| quote/etf/list | `$.data.dataInfo[]` | ⚠️ 核心 4 字段 + date + navPctChg*/eodPctChg* 各周期涨跌幅；无 IOPV/溢折率/成交量/精确时间 |
| quote/etf/single | `$.data.latestQuote{}` + `$.data.list[]` | 单只完整盘口 + 分钟 |
| quote/etf/kline | `$.data.candle` + `$.data.<代码>` | 二维数组需按 candle 列名对齐解析 |
| quote/etf/realtime | `$.data.dataList[].quoteList[]` | v3 字段是 `trdCode` 不是 `symbol`；无 latestQuote |
| discovery/top-etf | `$.data.list[]` | 误用 `$.data[]` |
| discovery/hot-search-recommend | `$.data.etfList[]` | ⚠️ v3 无 type 参数，返回 etfList/otcList/indexList 三组 |

## 行情字段归一

- 随附行情（search/all、etf-advanced、etf/detail、discovery/top-etf）：`lastPrice`、`changeRate`（etf-advanced 另有 `turnoverRate`、`premiumRate`；etf/detail 另有 `turnoverRate`）——不含精确行情时间。
- 批量精简行情（quote/etf/list）：`lastPrice`、`changeRate`、`dealBalance`、`fundScale` + `date` + `navPctChg*`/`eodPctChg*`——**不含** IOPV/溢折率/成交量/换手率/昨收/精确行情时间（timeStamp）。
- 单只完整盘口（quote/etf/single 的 latestQuote）：完整盘口（含 `iopv`、`deviationRate`、`yesterdayClosePrice`、`dealVolume`、`turnoverRatio`）+ `date + timeStamp` 精确行情时间 + 分钟序列 `list[]`。
- 分时分钟（quote/etf/realtime 的 quoteList）：分钟序列（minute/lastPrice/iopv/changeRate），**无最新快照**。
- 回答"现在/实时/盘中"口径问题且需要 IOPV/溢折率/换手率/精确行情时间时，必须使用 `quote/etf/single`；若只需最新价/涨跌幅/溢折率/成交额/换手率（快照口径、无精确行情时间），`search/etf-advanced` 的 `premiumRate`/`turnoverRate`/`dealBalance` 一次调用即可满足，无需为这些字段叠加 `quote/etf/list` 或 `single`；非交易时段表述为"接口返回的最新一笔行情"。
