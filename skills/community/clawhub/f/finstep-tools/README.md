# finstep-mcp

财跃星辰 A 股金融数据服务，覆盖行情、板块、公司、宏观、搜索等全维度数据。

## 配置

首次使用前设置 API 签名（可从财跃星辰平台获取）：

```bash
export FINSTEP_SIGNATURE="AI-ONE-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 快速参考

所有命令格式：`bash scripts/<脚本> <子命令> [参数...]`

### 搜索 `search.sh`

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `news` | 关键词 | 新闻搜索 |
| `report` | 关键词 | 研报搜索 |
| `announcement` | 股票代码/名称 | 公告搜索 |
| `morning` | — | 早参 |

### 行情 `quote.sh`

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `snapshot` | 代码/名称 | 个股实时行情 |
| `snapshot_plate` | 板块名称 | 板块实时行情 |
| `kline` | 代码 [数量] [类型¹] [复权²] | K线 |
| `intraday` | 代码 | 分时数据 |
| `market` | — | 大盘行情 |
| `leader` | [日期] [关键词] | 龙虎榜 |
| `flow` | 代码 [结束日期] [开始日期] | 资金流向 |
| `trending` | — | 热门行业 |
| `calendar` | 开始日期 结束日期 | 投资日历 |
| `hk_kline` | 代码 [数量] | 港股K线 |
| `us_kline` | 代码 [数量] | 美股K线 |

> ¹ 类型：1=日K 2=周K 3=月K　² 复权：1=不复权 2=前复权 3=后复权

### 板块 `plates.sh`

| 子命令 | 参数 | 说明 |
|--------|------|------|
| `list` | [关键词] [concept/industry] | 板块列表 |
| `ranking` | [日期] [数量] | 涨跌排名 |
| `stock` | 代码/名称 | 股票所属板块 |

### 公司 `company.sh`

| 子命令 | 说明 |
|--------|------|
| `base` | 基本信息 |
| `security` | 证券信息 |
| `finance` | 财务信息 |
| `valuation` | 估值指标 |
| `holders` `<01/02>` | 十大股东 / 十大流通股东 |
| `holders_num` | 股东人数 |
| `balance` | 资产负债表 |
| `cashflow` | 现金流量表 |
| `income` | 利润表 |
| `business` | 主营业务 |
| `industry` | 申万行业分类 |

所有公司接口第二个参数为股票代码或名称，支持后接 `[结束日期] [开始日期]`。

### 宏观 `macro.sh`

| 子命令 | 说明 |
|--------|------|
| `lpr` | LPR 利率 |
| `bond` | 中美国债收益率 |
| `pboc` | 央行公开市场操作 |
| `pboc_week` | 央行一周操作汇总 |
| `rrr` | 存款准备金率 |
| `pmi` / `cpi` / `ppi` / `gdp` | 经济指标 |
| `unemployment` | 失业率 |
| `house <城市>` | 主要城市房价 |

### 通用 `common.sh`

| 子命令 | 说明 |
|--------|------|
| `time` | 当前时间 |
| `trade_info` | 今日交易日信息 |
| `trade_date <开始> <结束> [市场³]` | 交易日历 |

> ³ 市场代码：83=上交所 90=深交所 18=北交所 72=港交所 78=纽交所
