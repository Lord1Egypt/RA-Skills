# 大虾皮 API 详细参考文档

**Base URL:** `https://daxiapi.com/coze`

**认证方式:** `Authorization: Bearer YOUR_TOKEN`

> 说明：本文档已按当前对外能力重新校对。各接口示例以主要返回内容为主，实际返回结果请以线上接口为准。

---

## GET 接口

### get_index_data

获取市场主流指数数据。

**请求方式:** `GET`

**请求示例:**

```javascript
fetch('/coze/get_index_data', {
    headers: {Authorization: 'Bearer YOUR_TOKEN'}
});
```

**响应格式:**

```json
{
    "date": "04-05",
    "index": [
        {
            "fullDate": "2025-04-05",
            "date": "04-05",
            "name": "沪深300",
            "cs": 3.5,
            "zdf": 1.2,
            "zdf5": 2.3,
            "zdf10": 4.5,
            "zdf20": 6.7,
            "zdf30": 8.9
        }
    ]
}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| date | 当前数据日期（`MM-DD`） |
| index[] | 主流指数列表 |
| index[].fullDate | 完整日期（`YYYY-MM-DD`） |
| index[].date | 简写日期（`MM-DD`） |
| index[].name | 指数名称 |
| index[].cs | 短期动量 CS 值 |
| index[].zdf | 当日涨跌幅(%) |
| index[].zdf5/zdf10/zdf20/zdf30 | 5/10/20/30 日涨跌幅 |

**使用说明:**

- CS 值用于判断短期动量强度，正值表示多头，负值表示空头。
- 涨跌幅字段可用于横向比较指数强弱与市场风格切换。

**CLI 对应命令:** `daxiapi market index`

**监控的指数列表:**

- 159628 创业板
- 159949 创业板50
- 510050 上证50
- 510300 沪深300
- 510500 中证500
- 512100 中证1000
- 515080 新能车
- 159920 恒生
- 588000 科创50
- 588800 科创板50
- 513180 恒生科技

---

### get_market_temp

获取市场温度数据。

**请求方式:** `GET`

**请求示例:**

```javascript
fetch('/coze/get_market_temp', {
    headers: {Authorization: 'Bearer YOUR_TOKEN'}
});
```

**响应格式:**

返回字符串，通常为 Toon 表格或多行文本，包含最近一段时间的市场温度数据。

**常见内容维度:**
| 指标 | 说明 | 使用方法 |
|------|------|----------|
| 估值温度 | 基于估值分位的温度指标 | `<20` 偏低估，`>70` 偏高估 |
| 恐贪指数 | 市场情绪强弱 | `0-10` 极度恐惧，`90-100` 极度贪婪 |
| 趋势温度 | 站上关键均线的股票比例 | `<20` 低迷，`>80` 过热 |
| 动量温度 | 市场整体动量 | 正值偏强，负值偏弱 |

**CLI 对应命令:** `daxiapi market temp`

---

### get_market_style

获取大小盘风格数据。

**请求方式:** `GET`

**请求示例:**

```javascript
fetch('/coze/get_market_style', {
    headers: {Authorization: 'Bearer YOUR_TOKEN'}
});
```

**响应格式:**

返回 Toon 格式表格字符串，包含日期和大小盘波动差值。

**使用说明:**

- 差值 `> 0`：小盘股表现优于大盘股。
- 差值 `< 0`：大盘股表现优于小盘股。
- 差值持续扩大：风格趋势延续。
- 差值由正转负或由负转正：常作为风格切换信号。

**CLI 对应命令:** `daxiapi market style`

---

### get_market_value_data

获取指数估值数据。

**请求方式:** `GET`

**请求示例:**

```javascript
fetch('/coze/get_market_value_data', {
    headers: {Authorization: 'Bearer YOUR_TOKEN'}
});
```

**响应格式:**

```json
{
    "date": "2025-04-05",
    "items": [
        {
            "code": "000300",
            "name": "沪深300",
            "PE": 12.5,
            "PB": 1.4,
            "PEPercentile": 35.2,
            "PBPercentile": 28.6,
            "wendu": 31.9,
            "date": "2025-04-05"
        }
    ]
}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| date | 当前数据日期 |
| items[] | 估值数据列表 |
| items[].code | 指数代码 |
| items[].name | 指数名称 |
| items[].PE | 市盈率 |
| items[].PB | 市净率 |
| items[].PEPercentile | PE 历史分位值(%) |
| items[].PBPercentile | PB 历史分位值(%) |
| items[].wendu | 综合温度值 |
| items[].date | 该条记录对应日期 |

**温度使用方法:**

- `20` 以下：低估区域，可开始定投。
- `10` 以下：明显低估，可加量定投。
- `5` 以下：极度低估，可提升定投额度。
- `60` 以上：高估区域，关注止盈。
- `80` 以上：明显高估，考虑分批止盈。

**CLI 对应命令:** `daxiapi market value`

---

### get_bk_data

获取行业板块数据。

**请求方式:** `GET`

**请求示例:**

```javascript
fetch('/coze/get_bk_data', {
    headers: {Authorization: 'Bearer YOUR_TOKEN'}
});
```

**响应格式:**

返回字符串，通常为 Toon 表格或多行文本，常见字段包括：

- 行业名称
- 今日涨幅
- 5 日涨幅
- 20 日涨幅
- CS 强度
- CS 均线
- QD 指标

**使用说明:**

- 数据通常按今日涨幅降序排列，便于快速识别强势行业。
- CS 强度用于判断行业短期动量。
- QD 指标用于判断行业综合强度。

**CLI 对应命令:** `daxiapi sector bk`

---

## POST 接口

### get_stock_data

获取 A 股个股详细信息。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string / string[] | 是 | 股票代码，支持单个代码或多个代码。 |

**请求示例:**

```javascript
fetch('/coze/get_stock_data', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({code: ['000001', '600031']})
});
```

**响应格式:**

返回数组，包含个股详细信息。CLI 描述中建议单次最多查询 20 只股票。

**常见字段:**
| 字段 | 说明 | 使用方法 |
|------|------|----------|
| stockId | 股票代码 | - |
| name | 股票名称 | - |
| zdf | 当日涨跌幅(%) | - |
| cs | 短期动量 | 可用于观察短线强弱 |
| sm | 中期动量 | `>0` 常表示中期偏强 |
| rps_score | RPS 相对强度 | 高值通常代表相对强势 |
| sctr | 技术排名百分比 | 值越高通常越强势 |
| isVCP | 是否为 VCP 形态 | `1` 表示是 |
| isCrossoverBox | 是否突破箱体 | `1` 表示是 |
| vcs | 成交量动量 | `>0` 常表示放量 |
| pe_ttm | 市盈率 TTM | - |
| hy_name / hy | 所属行业 | - |
| gainian | 所属概念 | - |

**CLI 对应命令:** `daxiapi stock info <codes...>`

---

### get_sector_data

获取行业板块热力图。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| orderBy | string | 否 | `cs` | 排序指标，如 `cs`、`zdf` 等 |
| lmt | integer | 否 | `5` | 返回窗口大小 |

**请求示例:**

```javascript
fetch('/coze/get_sector_data', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({orderBy: 'zdf', lmt: 5})
});
```

**响应格式:**

```json
{
    "crossover": "今日板块内突破箱体股票较多的板块为：xxx,xxx",
    "csHeatmap": "...",
    "zdfHeatmap": "...",
    "zdf5Heatmap": "...",
    "total": 100,
    "cs_gt_ma20_names": ["板块1", "板块2"],
    "cs_gt_5_names": ["板块1", "板块2"]
}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| crossover | 板块内箱体突破情况摘要 |
| csHeatmap | CS 动量热力图字符串 |
| zdfHeatmap | 当日涨跌幅热力图字符串 |
| zdf5Heatmap | 5 日涨跌幅热力图字符串 |
| total | 板块总数 |
| cs_gt_ma20_names | CS 高于 MA20 的板块名称列表 |
| cs_gt_5_names | CS 高于 5 的板块名称列表 |

**CLI 对应命令:** `daxiapi sector heatmap --order <field> --limit <num>`

---

### get_sector_rank_stock

获取指定板块内的股票排名。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sectorCode | string | 是 | - | 板块代码，如 `BK0428`、`0428`、`881155` |
| orderBy | string | 否 | `cs` | 排序字段，CLI 常用 `cs`、`zdf`、`sm`、`cg`、`cr`、`sctr` |

**请求示例:**

```javascript
fetch('/coze/get_sector_rank_stock', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({sectorCode: 'BK0428', orderBy: 'cs'})
});
```

**响应格式:**

返回数组，包含板块内股票的详细数据。

**常见字段:**

- 股票代码、名称
- 涨跌幅与多周期涨跌幅
- CS、SM、SCTR 等强度指标
- 成交额、换手率等排序字段
- 所属行业、概念等补充信息

**CLI 对应命令:** `daxiapi sector stocks --code <bkCode> --order <field>`

---

### get_gn_hot

获取热门概念板块列表。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| type | string | 否 | `ths` | 数据源类型：`ths`（同花顺）或 `dfcf`（东方财富） |

**请求示例:**

```javascript
fetch('/coze/get_gn_hot', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({type: 'ths'})
});
```

**响应格式:**

返回字符串，通常为 Toon 表格或多行文本，常见内容包括：

- 概念名称
- 今日涨幅
- 涨幅 7% 以上股票个数
- 5/10/20 日涨幅
- QD（强度）与 CS（动量）

**CLI 对应命令:** `daxiapi sector gn --type <ths|dfcf>`

---

### get_top_stocks

获取热门股票数据。

**请求方式:** `POST`

**请求参数:** 无

**请求示例:**

```javascript
fetch('/coze/get_top_stocks', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
});
```

**响应格式:**

返回字符串，通常为 Toon 表格或多行文本，常见内容包括：

- 股票名称、代码
- 所属板块
- 当日涨跌幅
- 5/10/20 日涨跌幅
- 相关概念

**CLI 对应命令:** `daxiapi sector top`

---

### get_gainian_stock

根据概念板块获取股票列表。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| gnId | string | 是 | - | 概念板块代码，如 `881155`、`BK0428` |
| type | string | 否 | `ths` | 数据源类型：`ths` 或 `dfcf` |

**请求示例:**

```javascript
fetch('/coze/get_gainian_stock', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({gnId: '881155', type: 'ths'})
});
```

**响应格式:**

返回数组，包含该概念板块下股票的详细数据。

**常见字段:**

- 股票代码、名称
- 涨跌幅
- CS、SCTR、RPS 等强度指标
- 所属行业、概念

**CLI 对应命令:** `daxiapi stock gn <gnId> --type <ths|dfcf>`

---

### get_kline

获取股票、指数或板块的 K 线数据。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 代码 |

**请求示例:**

```javascript
fetch('/coze/get_kline', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({code: '000001'})
});
```

**支持的代码格式:**

- `000001`：6 位股票/指数代码
- `sh000001` / `sz000001`：带交易所前缀代码
- `BK0428`：板块代码，BK开头是东方财富板块代码，8开头的是同花顺
- `1.000300`：标准 secid

**响应格式:**

```json
{
    "code": "000001",
    "name": "上证指数",
    "date": "2025-04-05",
    "klines": [
        {
            "date": "2025-01-01",
            "open": 3100.5,
            "close": 3150.2,
            "high": 3180.0,
            "low": 3090.0,
            "vol": 12345678
        }
    ]
}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| code | 代码 |
| name | 名称 |
| date | 最新日期 |
| klines[] | K 线数据数组 |
| klines[].date | 日期 |
| klines[].open | 开盘价 |
| klines[].close | 收盘价 |
| klines[].high | 最高价 |
| klines[].low | 最低价 |
| klines[].vol | 成交量 |

**CLI 对应命令:** `daxiapi kline <code>`

---

### get_zdt_pool

获取涨停、跌停或炸板股票池。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| type | string | 否 | `zt` | 类型：`zt`（涨停）、`dt`（跌停）、`zb`（炸板） |

**请求示例:**

```javascript
fetch('/coze/get_zdt_pool', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({type: 'zt'})
});
```

**响应格式:**

返回字符串，通常为 Toon 表格或多行文本，常见内容包括：

- 股票代码、名称
- 连板/开板等统计信息
- 所属行业、概念
- CS 强度、SCTR 排名

**CLI 对应命令:** `daxiapi zdt --type <zt|dt|zb>`

---

### get_sec_id

代码转换（获取标准 secid）。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票、指数或板块代码 |

**请求示例:**

```javascript
fetch('/coze/get_sec_id', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({code: '000001'})
});
```

**常见转换结果:**

- `000001` → `0.000001`（深市）
- `600000` → `1.600000`（沪市）
- `BK0428` → `90.BK0428`（板块）

**响应格式:**

返回标准 secid 格式字符串，如 `0.000001`。

---

### query_stock_data

搜索股票或板块代码。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| q | string | 是 | - | 搜索关键词 |
| type | string | 否 | `stock` | 搜索类型，CLI 约定使用 `stock` 或 `bk` |

**请求示例:**

```javascript
fetch('/coze/query_stock_data', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({q: '平安', type: 'stock'})
});
```

**响应格式:**

返回数组，常见字段包括：

- `code`：代码
- `name`：名称
- `type`：类型（如 `stock` / `bk`）
- `pinyin`：拼音缩写

**CLI 对应命令:** `daxiapi search <keyword> --type <stock|bk>`

---

### get_pattern_stocks

根据技术形态筛选股票。

**请求方式:** `POST`

**请求参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | 是 | 技术形态编码 |

**请求示例:**

```javascript
fetch('/coze/get_pattern_stocks', {
    method: 'POST',
    headers: {
        Authorization: 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({pattern: 'vcp'})
});
```

**CLI 当前支持的 pattern 值:**

- `gxl`
- `rps`
- `sctr`
- `trendUp`
- `high_60d`
- `crossMa50`
- `rpsTop3`
- `sos_h1`
- `csTop3`
- `sctrTop3`
- `newHigh`
- `fangliang`
- `shizhiTop3`
- `zdf5dTop3`
- `zdf1dTop3`
- `zdf10dTop3`
- `zdf20dTop3`
- `ibs`
- `vcp`
- `joc`
- `sos`
- `spring`
- `w`
- `fangliangtupo`
- `crossoverBox`
- `lps`
- `cs_crossover_20`

**响应格式:**

返回数组，包含符合指定技术形态的股票列表。

**常见字段:**

- 股票代码、名称
- 当日涨跌幅
- RPS、SCTR、CS 等强度指标
- 所属板块、概念等补充信息

**CLI 对应命令:** `daxiapi stock pattern <pattern>`

---

## 相关能力

### dividend score

用于获取红利类指数最近 60 个交易日的打分结果，可辅助判断超买超卖状态、趋势强弱和阶段位置。

**CLI 对应命令:** `daxiapi dividend score -c <code>`

**参数说明:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 指数代码，如 `2.H30269`、`2.930955`、`1.000922`、`2.932365` |

**响应格式:**

```json
{
    "code": "2.H30269",
    "name": "红利低波",
    "scores": [
        {
            "date": "2025-04-05",
            "score": 63.21,
            "cs": "4.18",
            "rsi": "58.30"
        }
    ]
}
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| code | 指数代码 |
| name | 指数名称 |
| scores[] | 最近 60 个交易日的打分结果 |
| scores[].date | 日期 |
| scores[].score | 综合分数 |
| scores[].cs | CS 值 |
| scores[].rsi | RSI 值 |

---

### news sentiment

用于获取个股舆情列表，适合做消息面异动跟踪。CLI 传入 `code` 后会自动转换为 `secid`。

**CLI 对应命令:** `daxiapi news sentiment -c <code> -p <pageSize>`

**参数说明:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票代码，如 `600031` |
| pageSize | number | 否 | 每页条数，默认 `20` |

**响应字段（核心）:**
| 字段 | 说明 |
|------|------|
| pageIndex | 页码 |
| pageSize | 每页条数 |
| total | 总条数 |
| list[].title | 新闻标题 |
| list[].showTime | 发布时间 |
| list[].artCode | 文章编号 |
| list[].url | 原文链接 |
| list[].originUrl | 原始链接 |

---

### news notice

用于获取个股公告列表，适合跟踪法定披露信息。

**CLI 对应命令:** `daxiapi news notice -c <code> -p <pageSize> -i <pageIndex>`

**参数说明:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票代码，如 `600031` |
| pageSize | number | 否 | 每页条数，默认 `20` |
| pageIndex | number | 否 | 页码，默认 `1` |

**响应字段（核心）:**
| 字段 | 说明 |
|------|------|
| pageIndex | 页码 |
| pageSize | 每页条数 |
| total | 总条数 |
| list[].title | 公告标题 |
| list[].noticeDate | 公告日期 |
| list[].displayTime | 展示时间 |
| list[].artCode | 公告编号 |
| list[].stockCode | 股票代码 |
| list[].url | 公告详情链接 |
| list[].columns[] | 公告分类标签 |

---

### news report

用于获取个股研报列表，支持按时间区间筛选。

**CLI 对应命令:** `daxiapi news report -c <code> -p <pageSize> -i <pageIndex> -b <beginTime> -e <endTime>`

**参数说明:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 股票代码，如 `600031` |
| pageSize | number | 否 | 每页条数，默认 `25` |
| pageIndex | number | 否 | 页码，默认 `1` |
| beginTime | string | 否 | 开始日期，格式 `YYYY-MM-DD` |
| endTime | string | 否 | 结束日期，格式 `YYYY-MM-DD` |

**响应字段（核心）:**
| 字段 | 说明 |
|------|------|
| pageIndex | 页码 |
| pageSize | 每页条数 |
| total | 总条数 |
| list[].title | 研报标题 |
| list[].stockCode | 股票代码 |
| list[].stockName | 股票名称 |
| list[].publishDate | 研报日期 |
| list[].orgName | 机构名称 |
| list[].rating | 评级 |
| list[].infoCode | 研报编号 |
| list[].url | 研报详情链接 |

---

## 错误处理

### 统一响应格式

> 下面的统一响应格式适用于大部分接口；个别能力的返回结构可能有所不同，请以实际返回为准。

```json
{
    "errCode": 0,
    "errMsg": "OK",
    "data": { ... }
}
```

### 错误码说明

| 错误码 | 说明 | 处理建议 |
| ------ | ---- | -------- |
| 0 | 成功 | - |
| 401 | Token 无效或未配置 | 检查 Token 配置 |
| 403 | 无访问权限 | 检查账号权限或套餐能力 |
| 404 | API 不存在 / 资源不存在 | 检查请求路径、方法或代码参数 |
| 429 | 请求频率超限 | 等待后重试，避免短时间内高频请求 |
| 500 | 服务器错误 | 稍后重试或联系管理员 |

---

## 使用场景示例

### 场景1：分析市场整体情况

1. 调用 `get_index_data` 获取主流指数数据。
2. 调用 `get_market_temp` 获取市场温度。
3. 调用 `get_market_style` 判断大小盘风格。

### 场景2：自下向上选股

1. 调用 `get_sector_data` 找出强势行业。
2. 调用 `get_sector_rank_stock` 获取行业内龙头股。
3. 调用 `get_stock_data` 分析个股详细指标。

### 场景3：查询特定股票

1. 调用 `query_stock_data` 搜索股票代码。
2. 调用 `get_stock_data` 获取详细信息。
3. 调用 `get_kline` 获取 K 线数据。

### 场景4：定投决策

1. 调用 `get_market_value_data` 获取指数估值。
2. 结合温度值决定定投节奏与金额。

### 场景5：涨跌停分析

1. 调用 `get_zdt_pool` 获取涨停/跌停/炸板股票池。
2. 调用 `get_top_stocks` 获取热门股票。

### 场景6：技术形态选股

1. 调用 `get_pattern_stocks` 获取符合技术形态的股票列表。
2. 再调用 `get_stock_data` 或 `get_kline` 做二次验证。

### 场景7：红利指数打分

1. 调用 `dividend score` 获取最近 60 个交易日分数。
2. 结合 `score`、`cs`、`rsi` 观察超买超卖与趋势变化。

---

## 第三方API接口

除了大虾皮官方API外，还可以使用以下第三方API获取补充数据。

### 东方财富API

#### 1. 指数行情数据

**接口地址:** `GET https://push2.eastmoney.com/api/qt/ulist/get`

**功能说明:** 获取多个指数的实时行情数据，包括价格、涨跌幅、涨跌家数等信息。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| fields | string | 是 | 返回字段列表，逗号分隔 |
| secids | string | 是 | 证券代码列表，格式: 市场.代码，逗号分隔 |
| ut | string | 是 | 用户token |

**请求示例:**

```bash
curl 'https://push2.eastmoney.com/api/qt/ulist/get?fltt=1&invt=2&fields=f12,f13,f14,f1,f2,f4,f3,f152,f6,f104,f105,f106&secids=1.000001,0.399001&ut=fa5fd1943c7b386f172d6893dbfba10b&pn=1&np=1&pz=20&dect=1&wbp2u=|0|0|0|0|web'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| f12 | 指数代码 |
| f13 | 市场代码(1=上海,0=深圳) |
| f14 | 指数名称 |
| f2 | 当前价格(实际值需除以100) |
| f3 | 涨跌幅百分比(实际值需除以100) |
| f4 | 涨跌额(实际值需除以100) |
| f6 | 成交额 |
| f104 | 上涨家数 |
| f105 | 下跌家数 |
| f106 | 平盘家数 |

---

#### 2. K线数据

**接口地址:** `GET https://push2his.eastmoney.com/api/qt/stock/kline/get`

**功能说明:** 获取股票、指数、ETF的K线历史数据，支持日线、周线、月线等多种周期。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| klt | string | 是 | K线类型: 101=日线,102=周线,103=月线 |
| secid | string | 是 | 证券代码，格式: 市场.代码(如: 1.000300) |
| fqt | string | 否 | 复权类型: 0=不复权,1=前复权,2=后复权 |
| lmt | number | 否 | 返回数据条数 |

**请求示例:**

```bash
curl 'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f61&ut=7eea3edcaed734bea9cbfc24409ed989&end=29991010&klt=101&secid=1.000300&fqt=1&lmt=300'
```

---

#### 3. 涨停股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicZTPool`

**功能说明:** 获取当日涨停股票列表，包括涨停时间、封单金额、连板数等信息。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ut | string | 是 | 用户token |
| dpt | string | 是 | 部门代码，默认 wz.ztzt |
| Pageindex | number | 否 | 页码，从0开始 |
| pagesize | number | 否 | 每页数量，默认200 |
| date | string | 是 | 日期，格式: YYYYMMDD |

**请求示例:**

```bash
curl 'https://push2ex.eastmoney.com/getTopicZTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fbt:asc&date=20240101'
```

---

#### 4. 跌停股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicDTPool`

**功能说明:** 获取当日跌停股票列表，包括跌停时间、封单金额等信息。

**请求示例:**

```bash
curl 'https://push2ex.eastmoney.com/getTopicDTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fund:asc&date=20240101'
```

---

#### 5. 炸板股票池

**接口地址:** `GET https://push2ex.eastmoney.com/getTopicZBPool`

**功能说明:** 获取当日炸板(涨停后打开)股票列表。

**请求示例:**

```bash
curl 'https://push2ex.eastmoney.com/getTopicZBPool?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=200&sort=fbt:asc&date=20240101'
```

---

#### 6. 股指期货数据

**接口地址:** `GET https://futsseapi.eastmoney.com/list/custom/{codes}`

**功能说明:** 获取股指期货实时行情数据，包括IH、IC、IF、IM等合约。

**URL路径参数:**

- `{codes}`: 期货合约代码列表，逗号分隔
    - 格式: `220_IHM0,220_IHS1,220_IHM1,220_IHS2`
    - 220_IH: 上证50期货
    - 220_IC: 中证500期货
    - 220_IF: 沪深300期货
    - 220_IM: 中证1000期货

---

### 集思录API

#### 可转债指数报价

**接口地址:** `GET https://www.jisilu.cn/webapi/cb/index_quote/`

**功能说明:** 获取可转债市场整体数据，包括等权指数、平均价格、溢价率、市场温度等。

**请求示例:**

```bash
curl 'https://www.jisilu.cn/webapi/cb/index_quote/'
```

**响应字段:**
| 字段 | 说明 |
|------|------|
| cur_index | 等权指数 |
| cur_price | 平均价格 |
| avg_premium | 平均溢价率 |
| mid_price | 中位数价格 |

---

### 同花顺API

#### 市场成交额数据

**接口地址:** `GET https://dq.10jqka.com.cn/fuyao/market_analysis_api/chart/v1/get_chart_data`

**功能说明:** 获取市场成交额历史数据，支持日线和分钟线。

**请求参数:**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| chart_key | string | 是 | 图表类型: turnover_day=日线,turnover_minute=分钟线 |

**请求示例:**

```bash
curl 'https://dq.10jqka.com.cn/fuyao/market_analysis_api/chart/v1/get_chart_data?chart_key=turnover_day'
```

---

## 第三方API注意事项

### 数据更新频率

| API | 更新频率 |
| ---------- | ----------- |
| 指数行情 | 实时(3秒) |
| K线数据 | 日终 |
| 涨跌停数据 | 实时(1分钟) |
| 股指期货 | 实时(3秒) |
| 可转债指数 | 实时(1分钟) |
| 市场成交额 | 日终 |

### 市场代码说明

| 代码 | 市场 |
| ---- | -------------- |
| 1 | 上海证券交易所 |
| 0 | 深圳证券交易所 |
| 116 | 上海科创板 |

### 证券代码格式

- **股票**: `市场.代码`，如 `1.600000`(上海)、`0.000001`(深圳)
- **指数**: `市场.代码`，如 `1.000300`(沪深300)
- **ETF**: `市场.代码`，如 `1.510300`(沪深300ETF)

## 注意事项
遇见不懂得术语，查询 [术语表](./field-descriptions.md)