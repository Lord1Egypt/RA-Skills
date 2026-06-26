---
name: finstep-mcp
description: 财跃星辰金融数据服务。提供实时行情、板块数据、公司信息、宏观经济、研报新闻等全方位金融数据。触发条件：用户查询股票行情、板块涨跌、公司财务、宏观数据、研报公告等金融信息。
---

# FinStep Tool 金融数据服务

财跃星辰提供的专业金融数据 API，覆盖 A 股市场全维度数据。

## Requirements

### Environment variables

| 环境变量 | 必填 | 说明 |
|----------|------|------|
| `FINSTEP_SIGNATURE` | ✅ 必填（机密） | Finstep API 签名令牌，所有脚本调用均需此变量。可从 [财跃星辰](https://product.finstep.cn/) 获取。 |

> **注意**：未设置 `FINSTEP_SIGNATURE` 时，所有脚本调用均会失败（HTTP 401/403 或连接被拒）。请通过 `.env` 文件、密钥管理工具或 shell 配置预先设置，切勿明文写入代码。

### Required binaries

| 工具 | 用途 |
|------|------|
| `bash` | 运行所有脚本（需 bash 3.2+，macOS/Linux 内置） |
| `curl` | 发起 HTTP 请求调用 Finstep API |
| `jq` | 构建请求参数 JSON 及解析响应（需 1.6+） |
| `date` | 生成默认日期参数（macOS/Linux 内置） |

## 服务列表

| 服务 | 脚本 | 功能 |
|------|------|------|
| 搜索 | `search.sh` | 新闻、公告、研报、微信公众号、投资者问答 |
| 行情 | `quote.sh` | 实时行情、K线、龙虎榜、资金流向 |
| 板块 | `plates.sh` | 板块列表、涨跌排名、成分股 |
| 公司 | `company.sh` | 财务报表、估值、股东信息 |
| 宏观 | `macro.sh` | LPR利率、国债收益率、央行操作、CPI/PPI/GDP等 |
| 通用 | `common.sh` | 交易日历、时间信息 |

## 使用方法

脚本位于 skill 目录的 `scripts/` 子目录下，使用 `bash <脚本> <子命令> [参数...]` 格式调用。调用前请确保 `FINSTEP_SIGNATURE` 已通过安全方式预先配置（详见 Requirements）。

### 1. 搜索新闻/研报/公告

```bash
bash scripts/search.sh news "关键词"
bash scripts/search.sh report "关键词"
bash scripts/search.sh announcement "股票代码或名称"
bash scripts/search.sh morning
```

### 2. 查询行情

```bash
# 实时行情快照 (支持代码或名称)
bash scripts/quote.sh snapshot "茅台"
bash scripts/quote.sh snapshot "600519"

# 板块行情快照
bash scripts/quote.sh snapshot_plate "白酒"

# K线数据 (代码 数量 类型 复权)
# 类型: 1=日K, 2=周K, 3=月K  |  复权: 1=不复权, 2=前复权, 3=后复权
bash scripts/quote.sh kline "600519" 30 1 2

# 分时数据
bash scripts/quote.sh intraday "600519"

# 大盘行情
bash scripts/quote.sh market

# 龙虎榜 (日期 [关键词])
bash scripts/quote.sh leader "2026-02-05"

# 资金流向 (关键词 [结束日期] [开始日期])
bash scripts/quote.sh flow "600519"

# 热门行业
bash scripts/quote.sh trending

# 投资日历 (开始日期 结束日期)
bash scripts/quote.sh calendar "2026-02-05" "2026-02-10"

# 港股K线
bash scripts/quote.sh hk_kline "00700" 30

# 美股K线
bash scripts/quote.sh us_kline "AAPL" 30
```

### 3. 板块数据

```bash
# 板块列表 ([关键词] [类型: concept/industry])
bash scripts/plates.sh list "白酒"

# 板块涨跌排名
bash scripts/plates.sh ranking

# 查询股票所属板块
bash scripts/plates.sh stock "茅台"

# 板块成分股
bash scripts/plates.sh stocks "白酒"
```

### 4. 公司信息

```bash
bash scripts/company.sh base "600519"        # 公司基本信息
bash scripts/company.sh security "600519"    # 证券信息
bash scripts/company.sh finance "600519"     # 财务信息 ([结束日期])
bash scripts/company.sh valuation "600519"   # 估值指标 ([结束日期] [开始日期])
bash scripts/company.sh holders "600519" "01"  # 股东信息 (01=十大股东, 02=十大流通股东)
bash scripts/company.sh holders_num "600519" # 股东人数
bash scripts/company.sh balance "600519"     # 资产负债表
bash scripts/company.sh cashflow "600519"    # 现金流量表
bash scripts/company.sh income "600519"      # 利润表
bash scripts/company.sh business "600519"    # 主营业务
bash scripts/company.sh industry "600519"    # 申万行业分类
```

### 5. 宏观数据

```bash
bash scripts/macro.sh lpr          # LPR 利率
bash scripts/macro.sh bond         # 中美国债收益率
bash scripts/macro.sh pboc         # 央行公开市场操作 ([日期])
bash scripts/macro.sh pboc_week    # 央行一周操作汇总 ([周末日期])
bash scripts/macro.sh rrr          # 存款准备金率
bash scripts/macro.sh pmi          # PMI指数 ([结束日期] [开始日期])
bash scripts/macro.sh cpi          # CPI
bash scripts/macro.sh ppi          # PPI
bash scripts/macro.sh gdp          # GDP季度
bash scripts/macro.sh unemployment # 失业率
bash scripts/macro.sh house "北京" # 主要城市房价 (城市 [结束日期] [开始日期])
```

### 6. 通用工具

```bash
bash scripts/common.sh time        # 获取当前时间
bash scripts/common.sh trade_info  # 交易日信息（是否交易日、上下一个交易日）

# 交易日历 (开始日期 结束日期 市场)
# 市场: 18=北交所, 83=上交所, 90=深交所, 72=港交所, 78=纽交所
bash scripts/common.sh trade_date "2026-02-01" "2026-02-28" 83
```

## API 端点

Base URL: `http://fintool-mcp.finstep.cn`

| 端点 | 用途 |
|------|------|
| /common | 通用工具 |
| /market_quote | 行情数据 |
| /plates | 板块数据 |
| /company_info | 公司信息 |
| /macro | 宏观数据 |
| /search | 搜索服务 |

## 已知问题

- `plates.sh stocks` (板块成分股): 接口返回"暂未找到相关股票信息"，可能是后端问题

## 注意事项

- 所有接口返回 JSON 格式
- 股票检索支持代码、名称、拼音等多种方式
- 部分接口有调用频率限制
- K线数据单次最多100条，需要更多数据请分批调用
