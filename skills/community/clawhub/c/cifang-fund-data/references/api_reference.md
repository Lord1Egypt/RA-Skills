# 次方量化API参考文档

本文档详细说明次方量化数据接口的使用方法。

## 基础信息

### 认证
- **请求头**: `x-api-key: YOUR_API_KEY`
- **获取API Key**: 访问 https://www.cifangquant.com 注册并获取API Key
- **权限**: 仅限VIP会员使用

### 响应格式
所有接口返回统一的JSON格式：

```json
{
  "code": 0,           // 业务码，0表示成功
  "message": "ok",     // 人类可读提示
  "data": {}           // 业务数据，失败时为null
}
```

### 错误码
- `0`: 成功
- `401`: API Key无效或未提供
- `400`: 参数错误
- `404`: 资源未找到
- `429`: 请求频率超限

## 基金行情接口

### 1. 基金列表接口
获取基金清单，支持关键词过滤。

**端点**: `GET /api/fund/list`

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `key_word` | string | 否 | 基金代码或名称关键词 |

**响应示例**:
```json
[
  {
    "fund_code": "510300",
    "fund_name": "华泰柏瑞沪深300ETF",
    "fund_type": "指数型-股票",
    "fund_market": "SH",
    "establish_date": "2012-05-04"
  }
]
```

**字段说明**:
- `fund_code`: 基金代码
- `fund_name`: 基金名称
- `fund_type`: 基金类型
- `fund_market`: 上市市场（SH-上海，SZ-深圳）
- `establish_date`: 成立日期

### 2. 历史行情接口
批量查询基金历史K线数据，支持复权选项。

**端点**: `GET /api/fund/hist_em`

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `symbol` | string | 是 | 基金代码，多个以英文逗号分隔，最多50个 |
| `start_date` | date | 是 | 开始日期，格式YYYY-MM-DD |
| `end_date` | date | 是 | 结束日期，格式YYYY-MM-DD |
| `adjust` | string | 否 | 复权类型：`none`(不复权)/`qfq`(前复权)/`hfq`(后复权)，默认`none` |

**响应格式**:
```json
{
  "510300": [
    ["2024-01-02", 3.45, 3.48, 3.50, 3.44, 1.23, 1000000],
    ["2024-01-03", 3.48, 3.50, 3.52, 3.47, 0.57, 1200000]
  ]
}
```

**数据字段说明**（每个数组元素）:
| 索引 | 类型 | 字段 | 说明 |
|------|------|------|------|
| 0 | string | 日期 | 交易日期，YYYY-MM-DD格式 |
| 1 | number | 开盘价 | 当日开盘价 |
| 2 | number | 收盘价 | 当日收盘价 |
| 3 | number | 最高价 | 当日最高价 |
| 4 | number | 最低价 | 当日最低价 |
| 5 | number | 涨跌幅 | 百分比数值，如1.23表示1.23% |
| 6 | number | 成交量 | 当日成交量 |

### 3. 实时行情接口
获取场内基金实时行情快照，数据延迟通常不超过2分钟。

**端点**: `GET /api/fund/spot`

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `symbol` | string | 否 | 基金代码，多个以英文逗号分隔；不传则返回全量实时行情 |

**响应示例**:
```json
{
  "161226": {
    "code": "161226",
    "name": "国投白银LOF",
    "price": 2.73,
    "change": -4.177,
    "change_amount": -0.119,
    "volume": 133505376,
    "amount": 366382936,
    "open": 2.789,
    "high": 2.792,
    "low": 2.716,
    "close_yesterday": 2.849,
    "fund_type": "LOF",
    "trade_date": "2026-04-23T00:00:00Z",
    "data_time": "13:32:33"
  }
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | string | 基金代码 |
| `name` | string | 基金名称 |
| `price` | number | 最新价 |
| `change` | number | 涨跌幅 (%) |
| `change_amount` | number | 涨跌额 |
| `volume` | number | 成交量 |
| `amount` | number | 成交额 |
| `open` | number | 开盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `close_yesterday` | number | 昨收价 |
| `fund_type` | string | 基金类型（ETF / LOF） |
| `trade_date` | string | 交易日期（ISO 8601） |
| `data_time` | string | 行情时间（HH:MM:SS） |

### 4. 场内基金排行接口
获取场内基金按不同时间区间的收益率排行榜。

**端点**: `GET /api/fund/exchange_rank`

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `sort_by` | string | 否 | 排序字段，见下表，默认 `1yzf` |
| `sort_order` | string | 否 | 排序方向：`desc`(降序) / `asc`(升序)，默认 `desc` |
| `limit` | integer | 否 | 返回数量上限，默认 30000，最大 30000 |

**`sort_by` 可选值**:
| 值 | 含义 |
|----|------|
| `zzf` | 近1周 |
| `1yzf` | 近1月 |
| `3yzf` | 近3月 |
| `6yzf` | 近6月 |
| `1nzf` | 近1年 |
| `2nzf` | 近2年 |
| `3nzf` | 近3年 |
| `jnzf` | 今年来 |
| `lnzf` | 成立以来 |

**响应示例**:
```json
[
  {
    "rank": 1,
    "fund_code": "515880",
    "fund_name": "通信ETF国泰",
    "fund_type": "指数型-股票",
    "date": "2026-04-22",
    "unit_nav": 1.4105,
    "accumulated_nav": 4.2315,
    "week_1": 15.52,
    "month_1": 30.87,
    "month_3": 33.43,
    "month_6": 58.25,
    "year_1": 270.6,
    "year_2": 282.98,
    "year_3": 279.1,
    "ytd": 37.28,
    "since_inception": 323.19,
    "inception_date": "2019-08-16"
  }
]
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `rank` | integer | 排名 |
| `fund_code` | string | 基金代码 |
| `fund_name` | string | 基金名称 |
| `fund_type` | string | 基金类型 |
| `date` | string | 净值日期 |
| `unit_nav` | number | 单位净值 |
| `accumulated_nav` | number | 累计净值 |
| `week_1` | number | 近1周收益率 (%) |
| `month_1` | number | 近1月收益率 (%) |
| `month_3` | number | 近3月收益率 (%) |
| `month_6` | number | 近6月收益率 (%) |
| `year_1` | number | 近1年收益率 (%) |
| `year_2` | number | 近2年收益率 (%) |
| `year_3` | number | 近3年收益率 (%) |
| `ytd` | number | 今年来收益率 (%) |
| `since_inception` | number | 成立以来收益率 (%) |
| `inception_date` | string | 成立日期 |

## 使用示例

### 示例1：获取基金列表
```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "https://www.cifangquant.com/api/fund/list?key_word=沪深300"
```

### 示例2：获取历史数据
```bash
curl -H "x-api-key: YOUR_API_KEY" \
  "https://www.cifangquant.com/api/fund/hist_em?symbol=510300,510500&start_date=2024-01-01&end_date=2024-12-31&adjust=qfq"
```

### 示例3：Python代码示例
```python
import requests

api_key = "YOUR_API_KEY"
headers = {"x-api-key": api_key}

# 获取基金列表
response = requests.get(
    "https://www.cifangquant.com/api/fund/list",
    headers=headers,
    params={"key_word": "510300"}
)

# 获取历史数据
response = requests.get(
    "https://www.cifangquant.com/api/fund/hist_em",
    headers=headers,
    params={
        "symbol": "510300,510500",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "adjust": "qfq"
    }
)
```

## 注意事项

### 1. 数据限制
- 历史行情接口最多支持50个基金代码
- 需要有效的API Key（VIP会员）
- 数据更新频率：交易日收盘后

### 2. 日期处理
- 日期格式必须为YYYY-MM-DD
- 开始日期不能晚于结束日期
- 建议合理设置日期范围，避免数据量过大

### 3. 错误处理
- 401错误：检查API Key是否正确
- 400错误：检查参数格式
- 429错误：降低请求频率

### 4. 复权说明
- `none`: 不复权，原始价格
- `qfq`: 前复权，以当前价格为基准向前调整
- `hfq`: 后复权，以历史价格为基准向后调整

## 常见问题

### Q1: 如何获取API Key？
A: 访问 https://www.cifangquant.com 注册账号，在个人中心获取API Key。

### Q2: 支持实时行情吗？
A: 支持。使用 `/api/fund/spot` 接口获取实时行情快照，数据延迟通常不超过2分钟。

### Q3: 数据来源是什么？
A: 数据来源于东方财富，新浪财经等公开数据源，经过清洗和整理。

### Q4: 请求频率有限制吗？
A: 文档未明确说明，但建议合理控制请求频率，避免被封禁。

### Q5: 支持哪些类型的基金？
A: 主要支持A股场内交易基金，包括ETF、LOF等。

## 更新日志

### V1.0 (2026-04-23)
- 初始版本发布
- 支持基金列表查询
- 支持历史行情数据获取
- 支持复权选项

---

**重要提示**: 使用本API需要遵守次方量化的服务条款，仅限个人或内部使用，不得用于商业用途或大规模数据爬取。