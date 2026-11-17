# 1688选品库 MCP 工具 API 参考

本文档为 1688选品库 MCP 服务的完整 API 参考，包含 4 个工具的参数说明和返回字段。

---

## 工具一：product_search_list（1688选品库商品筛选）

### 功能说明
在 1688 平台中根据关键词、类目、价格区间、销量、销售额、上架时间、发货时间、卖家类型、诚信通年限、代发权益、面单支持及商品标识等多维条件，精准筛选符合特定商业条件的商品及供应商。

**适用场景：** 爆品/潜力品筛选、供应商评估、条件化选品（价格、销量、发货时效）、按规则扫描类目或关键词市场、新品挖掘

**消耗点数：** 1点

### 请求参数

#### 必填参数

| 参数名 | 类型 | 描述 | 示例值 |
|--------|------|------|--------|
| pageIndex | Integer | 页码 | 1 |
| pageSize | Integer | 每页条数，默认20，最大100 | 20 |
| sortField | String | 排序字段（见下方枚举值） | orderCount7d |
| sortType | String | 排序类型：desc-降序，asc-升序 | desc |
| cycle | String | 统计周期：1-近1天，3-近3天，7-近7天，30-近30天 | 7 |

**sortField 枚举值：**
- `orderCount1d` - 近1天销售笔数
- `saleCount1d` - 近1天销售件数
- `saleVolume1d` - 近1天预估销售额
- `orderCount3d` - 近3天销售笔数
- `saleCount3d` - 近3天销售件数
- `saleVolume3d` - 近3天预估销售额
- `orderCount7d` - 近7天销售笔数
- `saleCount7d` - 近7天销售件数
- `saleVolume7d` - 近7天预估销售额
- `orderCount30d` - 近30天销售笔数
- `saleCount30d` - 近30天销售件数
- `saleVolume30d` - 近30天预估销售额
- `ordersCount` - 总笔数
- `salesCount` - 总件数
- `offerCreateTime` - 上架时间
- `price` - 批发价
- `consignPrice` - 代发价

> **重要：** sortField 的时间维度（1d/3d/7d/30d）应与 cycle 参数保持一致。例如 cycle=7 时，sortField 应使用 orderCount7d/saleCount7d/saleVolume7d。

#### 可选参数

| 参数名 | 类型 | 描述 | 示例值 |
|--------|------|------|--------|
| keyWord | String | 商品关键字搜索，最多支持50个字符 | 夏季女装 |
| searchType | Integer | 关键词搜索类型：1-模糊匹配，3-精准匹配 | 1 |
| categoryIdList | List\<String\> | 类目ID集合，最多20个 | ["100"] |
| beginOfferCreateTime | String | 起始上架时间 | 2025-06-12 |
| endOfferCreateTime | String | 结束上架时间 | 2025-06-12 |
| beginPrice | Double | 起始批发价 | 10.0 |
| endPrice | Double | 结束批发价 | 50.0 |
| beginStartQuantity | Integer | 起始起批量 | 1 |
| endStartQuantity | Integer | 结束起批量 | 100 |
| beginOrderCount | Integer | 起始销售笔数（按统计周期维度） | 100 |
| endOrderCount | Integer | 结束销售笔数（按统计周期维度） | 5000 |
| beginSaleCount | Integer | 起始销售件数（按统计周期维度） | 100 |
| endSaleCount | Integer | 结束销售件数（按统计周期维度） | 10000 |
| beginSaleVolume | Double | 起始预估销售额（按统计周期维度） | 1000.0 |
| endSaleVolume | Double | 结束预估销售额（按统计周期维度） | 50000.0 |
| beginOrdersCount | Integer | 起始总笔数 | 100 |
| endOrdersCount | Integer | 结束总笔数 | 50000 |
| beginSalesCount | Integer | 起始总件数 | 500 |
| endSalesCount | Integer | 结束总件数 | 100000 |
| location | List\<Object\> | 卖家所属地（多选），province-省份，city-城市 | [{"province":"广东","city":["深圳","珠海"]}] |
| beginTpYear | Integer | 开始诚信通年限 | 1 |
| endTpYear | Integer | 结束诚信通年限 | 10 |
| shiLiType | List\<String\> | 卖家会员类型（多选）：superFactory-超级工厂，Power-实力商家，TrustPass-仅诚信通会员 | ["superFactory","Power"] |
| goodsUrl | String | 商品链接地址 | https://detail.1688.com/... |
| productIds | String | 商品ID，多个用顿号隔开，最多20个 | 123\|456\|789 |
| companyType | Integer | 公司类型：0-不限，1-店铺，2-工厂 | 2 |
| proxyRights | List\<String\> | 代发权益（多选）：4360897-一件代发包邮，449154-先采后付 | ["4360897","449154"] |
| faceToFaceSupport | List\<String\> | 面单支持（多选）：441218-淘宝，386434-抖音，422914-拼多多，422978-小红书，386370-快手 | ["441218","386434"] |
| shopService | List\<String\> | 卖家服务（多选）：4057409-安心购，888777-深度认证报告 | ["4057409"] |
| offerType | Integer | 商品标识：0-不限制，2-新品，3-1688严选，4-跨境Select，5-支持定制，6-镇店之宝 | 2 |
| sendTime | List\<Integer\> | 发货时间（多选）：24-24小时，48-48小时，72-72小时 | [24,48] |

### 返回参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| pageIndex | Integer | 页码 |
| pageSize | Integer | 每页条数 |
| totalCount | Integer | 总条数（最多可翻页查询2000条） |
| totalPages | Integer | 总页码 |
| list | List\<Object\> | 商品集合（见下方字段） |

**list 中每个商品对象的字段：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| offerId | String | 商品ID |
| shopId | String | 店铺ID |
| image | String | 商品图片地址 |
| offerCreateTime | String | 商品上架时间 |
| quantityPrices | String | 价格区间 |
| title | String | 商品标题 |
| price | Double | 批发价 |
| deliveryTime | String | 发货时间 |
| company | String | 店铺名称 |
| saleQuantity | Integer | 销售件数（按统计周期返回） |
| orderCount | Integer | 销售笔数（按统计周期返回） |
| salesVolume | Integer | 预估销售额（按统计周期返回） |
| ordersCount | Integer | 总笔数 |
| salesCount | Integer | 总件数 |
| province | String | 卖家所属地省份 |
| city | String | 卖家所属地城市 |
| tpYear | Integer | 诚信通年限 |
| buyerProtections | String | 商品权益 |
| consignPrice | Double | 代发价 |
| shiLiType | List\<String\> | 卖家会员类型 |
| unit | String | 单位（如：件） |
| quantityBegin | Integer | 起批量 |
| levelName | String | 类目层级名称 |
| companyType | Integer | 公司类型：1-店铺，2-工厂 |
| shopUrl | String | 店铺链接地址 |

---

## 工具二：product_billboard_list（1688商品榜单）

### 功能说明
查询 1688 平台日榜、周榜、月榜热销商品，支持按关键词、类目、价格区间、销量、销售额、卖家类型等条件筛选，可按销售笔数、销售件数或预估销售额排序。

**适用场景：** 爆品趋势追踪、热销商品挖掘、市场竞争分析、按榜单周期监测商品销售表现

**消耗点数：** 1点

### 请求参数

#### 必填参数

| 参数名 | 类型 | 描述 | 示例值 |
|--------|------|------|--------|
| pageIndex | Integer | 页码 | 1 |
| pageSize | Integer | 每页条数，默认20，最大100 | 20 |
| pageType | Integer | 榜单类型：1-日榜，2-周榜，3-月榜 | 1 |
| date | String | 查询时间（见下方格式说明） | 2025-06-12 |
| sortField | String | 排序字段（见下方枚举值） | orderCount |
| sortType | String | 排序类型：desc-降序，asc-升序 | desc |

**date 参数格式说明：**
- 日榜：每天时间，如 `2025-06-12`（可查询近30天）
- 周榜：每周的周日时间，如 `2025-06-15`（可查询近90天）
- 月榜：每月的第一天时间，如 `2025-06-01`（可查询近一年）

**sortField 枚举值：**
- `orderCount` - 销售笔数（按查询榜单类型维度）
- `saleCount` - 销售件数（按查询榜单类型维度）
- `saleVolume` - 预估销售额（按查询榜单类型维度）
- `ordersCount` - 总笔数
- `salesCount` - 总件数
- `offerCreateTime` - 上架时间
- `price` - 批发价
- `consignPrice` - 代发价

#### 可选参数

| 参数名 | 类型 | 描述 | 示例值 |
|--------|------|------|--------|
| keyWord | String | 商品关键字搜索，最多支持50个字符 | 夏季女装 |
| searchType | Integer | 关键词搜索类型：1-模糊匹配，3-精准匹配 | 1 |
| categoryIdList | List\<String\> | 类目ID集合，最多20个 | ["100"] |
| beginOfferCreateTime | String | 起始上架时间 | 2025-06-12 |
| endOfferCreateTime | String | 结束上架时间 | 2025-06-12 |
| beginPrice | Double | 起始批发价 | 10.0 |
| endPrice | Double | 结束批发价 | 50.0 |
| beginStartQuantity | Integer | 起始起批量 | 1 |
| endStartQuantity | Integer | 结束起批量 | 100 |
| beginOrderCount | Integer | 起始销售笔数（按榜单类型维度） | 100 |
| endOrderCount | Integer | 结束销售笔数（按榜单类型维度） | 5000 |
| beginSaleCount | Integer | 起始销售件数（按榜单类型维度） | 100 |
| endSaleCount | Integer | 结束销售件数（按榜单类型维度） | 10000 |
| beginSaleVolume | Double | 起始预估销售额（按榜单类型维度） | 1000.0 |
| endSaleVolume | Double | 结束预估销售额（按榜单类型维度） | 50000.0 |
| beginOrdersCount | Long | 起始总笔数 | 100 |
| endOrdersCount | Long | 结束总笔数 | 50000 |
| beginSalesCount | Long | 起始总件数 | 500 |
| endSalesCount | Long | 结束总件数 | 100000 |
| beginConsignPrice | Double | 起始代发价 | 5.0 |
| endConsignPrice | Double | 结束代发价 | 30.0 |
| buyerProtections | String | 权益保障，多个用逗号隔开 | 商品包邮,7天包退货,支持运费险 |
| location | List\<Object\> | 卖家所属地（多选），province-省份，city-城市 | [{"province":"广东"}] |
| beginTpYear | Integer | 开始诚信通年限 | 1 |
| endTpYear | Integer | 结束诚信通年限 | 10 |
| shiLiType | List\<String\> | 卖家会员类型（多选）：superFactory-超级工厂，Power-实力商家，TrustPass-仅诚信通会员 | ["superFactory"] |
| goodsUrl | String | 商品链接地址 | https://detail.1688.com/... |
| productIds | String | 商品ID，多个用顿号隔开，最多20个 | 123\|456 |
| companyType | Integer | 公司类型：0-不限，1-店铺，2-工厂 | 2 |
| proxyRights | List\<String\> | 代发权益（多选）：4360897-一件代发包邮，449154-先采后付 | ["4360897"] |
| faceToFaceSupport | List\<String\> | 面单支持（多选）：441218-淘宝，386434-抖音，422914-拼多多，422978-小红书，386370-快手 | ["441218","386434"] |
| shopService | List\<String\> | 卖家服务（多选）：4057409-安心购，888777-深度认证报告 | ["4057409"] |
| offerType | Integer | 商品标识：0-不限制，2-新品，3-1688严选，4-跨境Select，5-支持定制，6-镇店之宝 | 3 |
| sendTime | Integer | 发货时间：24-24小时，48-48小时，72-72小时 | 24 |

### 返回参数

返回结构与 product_search_list 完全相同，包含 pageIndex、pageSize、totalCount、totalPages 和 list。list 中每个商品对象的字段也完全一致，请参考 product_search_list 的返回参数说明。

---

## 工具三：product_info（1688商品分析）

### 功能说明
查询指定商品的基础信息及近30天每日销售趋势，包含日笔数、日件数、日预估销售额及批发价变动。

**适用场景：** 单品销售分析、价格监测、竞品追踪及采购决策

**消耗点数：** 1点

### 请求参数

| 参数名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|--------|
| beginTime | String | 是 | 查询开始时间（可查询近30天数据） | 2025-05-13 |
| endTime | String | 是 | 查询结束时间（可查询近30天数据） | 2025-06-11 |
| offerId | String | 是 | 商品ID | 893612428681 |

### 返回参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| image | String | 商品图片地址 |
| offerCreateTime | String | 商品上架时间 |
| offerId | String | 商品ID |
| title | String | 商品标题 |
| price | Double | 批发价 |
| tendencies | List\<Object\> | 每日商品数据集合（见下方字段） |

**tendencies 中每个对象的字段：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| date | String | 日期 |
| orderCount | String | 日笔数 |
| saleQuantity | String | 日件数 |
| salesVolume | String | 日预估销售额 |
| price | String | 当日批发价 |

---

## 工具四：get_category_info（1688商品类目）

### 功能说明
根据类目ID查询类目名称及是否存在子类目，支持逐级展开类目层级结构。

**适用场景：** 类目导航、类目筛选及类目层级分析

**消耗点数：** 1点

### 请求参数

| 参数名 | 类型 | 必填 | 描述 | 示例值 |
|--------|------|------|------|--------|
| categoryId | String | 是 | 类目ID，第一级传 0 | 0 |

### 返回参数

返回类目列表，每个类目对象包含以下字段：

| 参数名 | 类型 | 描述 | 示例值 |
|--------|------|------|--------|
| category_name | String | 类目名称 | 衣服 |
| category_id | String | 类目ID | 10 |
| has_child | Boolean | 是否有子类目 | true |

> **使用方式：** 首次调用传 categoryId=0 获取一级类目列表，若 has_child 为 true，可继续用该 category_id 作为参数查询下一级子类目，逐级展开完整类目树。

---

## 通用注意事项

1. **翻页限制：** product_search_list 和 product_billboard_list 最多可翻页查询2000条数据
2. **时间格式：** 所有时间参数统一使用 `YYYY-MM-DD` 格式
3. **商品链接：** 1688商品链接格式为 `https://detail.1688.com/offer/{offerId}.html`，可通过 offerId 拼接生成
4. **图片展示：** 返回数据中的 image 字段为商品图片URL，可直接用于 Markdown 图片展示
5. **统计周期：** product_search_list 的 cycle 参数决定销售数据的统计维度，sortField 的时间维度需与 cycle 对应
