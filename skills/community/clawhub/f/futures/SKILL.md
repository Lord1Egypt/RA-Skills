---
name: "Futures Inquiry - 期货查询"
description: 查询上期所、大商所、郑商所、中金所、广期所期货实时行情及历史 K 线。当用户说：螺纹钢主力什么价？豆粕期货涨了吗？SC 原油最近一周走势？或类似期货行情问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📉", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据期货查询（Jisu Futures）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 提供上海、大连、郑州、中金、广州等交易所期货价格查询。

## 何时使用本技能

- **期货价格**、**主力合约**、**某品种涨跌**（如螺纹钢、豆粕、PTA、工业硅、IF 股指）
- **五大交易所**行情：上期所、大商所、郑商所、中金所、广期所
- **历史走势**：指定合约在某段时间的开高低收、成交量、持仓量

**技术前提：** 脚本 **`skills/futures/futures.py`**，环境变量 **`JISU_API_KEY`**。

**接口与数据范围：**

- **上海期货交易所**（`/futures/shfutures`）
- **大连商品交易所**（`/futures/dlfutures`）
- **郑州商品交易所**（`/futures/zzfutures`）
- **中国金融期货交易所**（`/futures/zgjrfutures`）
- **广州期货交易所**（`/futures/gzfutures`）
- **期货历史查询**（`/futures/history`）

各交易所实时接口返回：品种代号、名称、最新价、涨跌幅、涨跌量、最高/最低价、开盘价、昨收盘价、成交量、持仓量、买卖价量、更新时间等。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [期货查询 API](https://www.jisuapi.com/api/futures/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/futures/futures.py`

## 使用方式

### 1. 上海期货交易所（/futures/shfutures）

```bash
python3 skills/futures/futures.py shfutures

# 指定品种（可选 type）
python3 skills/futures/futures.py shfutures '{"type":"FU2309"}'
```

### 2. 大连商品交易所（/futures/dlfutures）

```bash
python3 skills/futures/futures.py dlfutures
python3 skills/futures/futures.py dlfutures '{"type":"V0"}'
```

### 3. 郑州商品交易所（/futures/zzfutures）

```bash
python3 skills/futures/futures.py zzfutures
python3 skills/futures/futures.py zzfutures '{"type":"TA0"}'
```

### 4. 中国金融期货交易所（/futures/zgjrfutures）

```bash
python3 skills/futures/futures.py zgjrfutures
python3 skills/futures/futures.py zgjrfutures '{"type":"IF2306"}'
```

### 5. 广州期货交易所（/futures/gzfutures）

```bash
python3 skills/futures/futures.py gzfutures
python3 skills/futures/futures.py gzfutures '{"type":"SI0"}'
```

### 6. 期货历史查询（/futures/history）

按交易所、合约代码与日期区间查询历史开高低收、涨跌幅、成交量、持仓量等。

```bash
python3 skills/futures/futures.py history '{"market":"shfutures","type":"SC2703","startdate":"2026-06-01","enddate":"2026-06-10"}'
```

请求 JSON：

```json
{
  "market": "shfutures",
  "type": "SC2703",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10"
}
```

| 字段名    | 类型   | 必填 | 说明                                                                 |
|-----------|--------|------|----------------------------------------------------------------------|
| market    | string | 是   | `shfutures` / `dlfutures` / `zzfutures` / `zgjrfutures` / `gzfutures` |
| type      | string | 是   | 期货类型代码，如 `SC2703`、`TA0`、`IF2306`                           |
| startdate | string | 是   | 开始日期                                                             |
| enddate   | string | 是   | 结束日期                                                             |

### 各交易所实时接口可选参数

| 字段名 | 类型   | 必填 | 说明         |
|--------|--------|------|--------------|
| type   | string | 否   | 期货类型代码 |

实时接口 `result` 按品种名称分组，例如 `{"燃油": [...], "铜": [...]}`。

## 返回结果示例（节选）

### 上海期货交易所（实时）

```json
{
  "燃油": [
    {
      "type": "FU2309",
      "typename": "燃料油2309",
      "price": "2948.00",
      "changepercent": "+6.27%",
      "changequantity": "+174",
      "maxprice": "2975.00",
      "minprice": "2777.00",
      "openingprice": "2782.00",
      "lastclosingprice": "2774.000",
      "tradeamount": "704525",
      "holdamount": "295063",
      "buyamount": "47",
      "buyprice": "2947.000",
      "sellamount": "66",
      "sellprice": "2948.000",
      "updatetime": "2023-04-03 15:46:43"
    }
  ]
}
```

### 期货历史查询

```json
{
  "market": "shfutures",
  "type": "SC2703",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10",
  "count": 8,
  "list": [
    {
      "typename": "上海原油2703",
      "date": "2026-06-10",
      "openingprice": 562,
      "maxprice": 565.6,
      "minprice": 550.8,
      "price": 559.2,
      "changeamount": -5.8,
      "changepercent": "-1.027%",
      "tradeamount": 23,
      "holdamount": 0
    }
  ]
}
```

当无数据时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据期货文档](https://www.jisuapi.com/api/futures/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在     |
| 102  | APPKEY 已过期           |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止               |
| 106  | IP 请求超过限制         |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. **实时行情**：用户问「PTA、燃油今天什么价？」  
   - 调用 `zzfutures`、`shfutures` 等对应交易所  
   - 从返回的分组结果中按品种名（如 `PTA`、`燃油`）筛选合约，汇总 `price`、`changepercent`、`maxprice`、`minprice`

2. **单合约查询**：已知合约代码时加 `type` 参数，减少返回体积：  
   `python3 skills/futures/futures.py zzfutures '{"type":"TA0"}'`

3. **历史走势**：用户问「SC2703 最近一周走势」  
   - 调用 `history`，`market` 与交易所子命令一致（如上期所 → `shfutures`）  
   - 用 `list` 中的开高低收、涨跌幅归纳区间表现，并注明数据时效与免责

4. **交易所对照**

   | 用户说法     | 子命令       | history 的 market |
   |--------------|--------------|-------------------|
   | 上期所、上海 | `shfutures`  | `shfutures`       |
   | 大商所、大连 | `dlfutures`  | `dlfutures`       |
   | 郑商所、郑州 | `zzfutures`  | `zzfutures`       |
   | 中金所、股指 | `zgjrfutures`| `zgjrfutures`     |
   | 广期所、广州 | `gzfutures`  | `gzfutures`       |

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供生活常用、交通出行、工具万能、图像识别、娱乐购物、位置服务等百余类 API。

在官网注册后，按 [期货查询 API](https://www.jisuapi.com/api/futures/) 申请数据，在会员中心获取 **AppKey** 进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。
