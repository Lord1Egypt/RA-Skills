---
name: "Exchange Rate Inquiry & Conversion - 汇率查询"
description: 货币汇率换算、热门汇率、货币列表、银行外汇牌价、实时行情及历史汇率等。当用户说：100 美元换多少人民币？今天中行美元现汇价？美元人民币最近一周走势？美元指数多少？或类似汇率换算问题时，使用本技能。
metadata: { "openclaw": { "emoji": "💱", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据汇率查询（Jisu Exchange）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **汇率换算**：任意两种货币之间的金额换算；
- **单个货币**：某一货币相对热门货币的实时汇率列表；
- **所有货币**：查询所有支持的货币代码及名称；
- **十大银行外汇牌价**：查询银行中间价、买入价、卖出价等；
- **基本/交叉盘实时行情**（`/exchange/realtime`）：查询 USD/CNY 等主要货币对实时汇率及涨跌；
- **银行历史牌价**（`/exchange/bankhistory`）：查询指定银行、指定货币的历史外汇牌价；
- **历史汇率**（`/exchange/history`）：查询两种货币之间的历史汇率；
- **历史行情**（`/exchange/history2`）：按 6 位货币代码（如 USDCNY）查询含开高低收的历史行情。

> 汇率为综合汇率，仅供参考，来源详见极速数据文档 [`https://www.jisuapi.com/api/exchange/`](https://www.jisuapi.com/api/exchange/)。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [汇率查询 API](https://www.jisuapi.com/api/exchange/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/exchange/exchange.py`

## 使用方式

### 1. 汇率换算（/exchange/convert）

```bash
python3 skills/exchange/exchange.py '{"from":"CNY","to":"USD","amount":10}'
```

请求 JSON：

```json
{
  "from": "CNY",
  "to": "USD",
  "amount": 10
}
```

### 2. 单个货币热门汇率（/exchange/single）

```bash
python3 skills/exchange/exchange.py single CNY
```

### 3. 所有货币列表（/exchange/currency）

```bash
python3 skills/exchange/exchange.py currency
```

### 4. 十大银行外汇牌价（/exchange/bank）

```bash
# 默认中国银行 BOC
python3 skills/exchange/exchange.py bank

# 指定银行（示例：工商银行 ICBC）
python3 skills/exchange/exchange.py bank ICBC
```

支持的银行编码示例：

- `ICBC`：工商银行
- `BOC`：中国银行
- `ABCHINA`：农业银行
- `BANKCOMM`：交通银行
- `CCB`：建设银行
- `CMBCHINA`：招商银行
- `CEBBANK`：光大银行
- `SPDB`：浦发银行
- `CIB`：兴业银行
- `ECITIC`：中信银行

### 5. 基本/交叉盘实时行情（/exchange/realtime）

```bash
# 基本汇率（默认）
python3 skills/exchange/exchange.py realtime basic

# 交叉盘
python3 skills/exchange/exchange.py realtime cross
```

| 字段名 | 类型   | 必填 | 说明                               |
|--------|--------|------|------------------------------------|
| type   | string | 是   | `basic` 基本汇率，`cross` 交叉盘   |

### 6. 银行历史外汇牌价（/exchange/bankhistory）

```bash
python3 skills/exchange/exchange.py bankhistory '{"startdate":"2026-06-01","enddate":"2026-06-11","bank":"BOC","code":"USD"}'
```

请求 JSON：

```json
{
  "startdate": "2026-06-01",
  "enddate": "2026-06-11",
  "bank": "BOC",
  "code": "USD"
}
```

| 字段名    | 类型   | 必填 | 说明                                   |
|-----------|--------|------|----------------------------------------|
| startdate | string | 是   | 开始日期                               |
| enddate   | string | 是   | 结束日期                               |
| bank      | string | 是   | 银行编码（同 bank 子命令）             |
| code      | string | 否   | 货币代码，留空返回全部                 |

### 7. 历史汇率（/exchange/history）

```bash
python3 skills/exchange/exchange.py history '{"from":"USD","to":"CNY","startdate":"2026-06-01","enddate":"2026-06-10"}'
```

请求 JSON：

```json
{
  "from": "USD",
  "to": "CNY",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10"
}
```

### 8. 历史行情（/exchange/history2）

按 6 位货币代码查询，返回开高低收、涨跌幅等。

```bash
python3 skills/exchange/exchange.py history2 '{"code":"USDCNY","startdate":"2026-06-01","enddate":"2026-06-10"}'
```

请求 JSON：

```json
{
  "code": "USDCNY",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10"
}
```

## 请求参数

### 汇率换算

| 字段名 | 类型   | 必填 | 说明                            |
|--------|--------|------|---------------------------------|
| from   | string | 是   | 原货币代码（如 CNY、USD）      |
| to     | string | 是   | 目标货币代码                    |
| amount | number | 否   | 数量（默认 1）                  |

### 单个货币

| 字段名   | 类型   | 必填 | 说明     |
|----------|--------|------|----------|
| currency | string | 是   | 货币代码 |

### 所有货币

无需额外参数，仅需 `appkey`。

### 银行外汇牌价

| 字段名 | 类型   | 必填 | 说明                               |
|--------|--------|------|------------------------------------|
| bank   | string | 否   | 银行编码，不传则默认为 BOC（中国银行） |

## 返回结果示例

### 汇率换算（简化）

```json
{
  "from": "CNY",
  "to": "USD",
  "fromname": "人民币",
  "toname": "美元",
  "updatetime": "2015-10-26 16:56:22",
  "rate": "0.1574",
  "camount": "1.574"
}
```

### 单个货币热门汇率（简化）

```json
{
  "currency": "CNY",
  "name": "人民币",
  "list": {
    "USD": {
      "name": "美元",
      "rate": "0.1574",
      "updatetime": "2015-10-26 16:56:22"
    },
    "EUR": {
      "name": "欧元",
      "rate": "0.1426",
      "updatetime": "2015-10-26 16:56:22"
    }
  }
}
```

### 所有货币列表（简化）

```json
[
  { "currency": "USD", "name": "美元" },
  { "currency": "EUR", "name": "欧元" },
  { "currency": "CNY", "name": "人民币" }
]
```

### 银行外汇牌价（简化）

```json
{
  "bank": "BOC",
  "list": [
    {
      "code": "USD",
      "name": "美元",
      "midprice": "717.4100",
      "cashbuyprice": "722.0800",
      "forexbuyprice": "722.0800",
      "cashsellprice": "725.1100",
      "forexsellprice": "725.1100",
      "updatetime": "2025-03-11 18:05:59"
    }
  ]
}
```

### 基本/交叉盘实时行情（简化）

```json
{
  "type": "basic",
  "typename": "基本汇率",
  "updatetime": "2026-06-11 12:30:26",
  "count": 13,
  "list": [
    {
      "code": "USDCNY",
      "name": "美元人民币",
      "price": "6.7784",
      "changepercent": -0.114,
      "changeamount": -0.001,
      "openningprice": "6.7681",
      "closingprice": "6.7784"
    }
  ]
}
```

### 历史汇率（简化）

```json
{
  "from": "USD",
  "to": "CNY",
  "fromname": "美元",
  "toname": "人民币",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10",
  "count": 8,
  "list": [
    { "date": "2026-06-10", "rate": "6.778400", "updatetime": "2026-06-10 18:07:23" }
  ]
}
```

### 历史行情 history2（简化）

```json
{
  "code": "USDCNY",
  "name": "美元人民币",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10",
  "count": 8,
  "list": [
    {
      "date": "2026-06-01",
      "openningprice": "6.7681",
      "closingprice": "6.7660",
      "maxprice": "6.7699",
      "minprice": "6.7640",
      "changepercent": "-0.0044",
      "changeamount": "-0.0003"
    }
  ]
}
```

当出现参数错误（如货币代码有误、数量为空等）时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 204,
  "message": "要兑换的货币有误"
}
```

## 常见错误码

来源于 [极速数据汇率文档](https://www.jisuapi.com/api/exchange/)：

| 代号 | 说明             |
|------|------------------|
| 201  | 要兑换的货币为空 |
| 202  | 兑换后的货币为空 |
| 203  | 兑换数量为空     |
| 204  | 要兑换的货币有误 |
| 205  | 兑换后的货币有误 |
| 206  | 货币为空         |
| 207  | 货币有误         |
| 208  | 没有信息         |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户输入自然语言：「帮我把 1000 人民币换算成美元，大概是多少？」  
2. 代理构造 JSON：`{"from":"CNY","to":"USD","amount":1000}` 并调用：  
   `python3 skills/exchange/exchange.py '{"from":"CNY","to":"USD","amount":1000}'`  
3. 从返回结果中读取 `rate` 和 `camount`，向用户说明当前汇率与折算后的金额；  
4. 若用户询问某货币常见汇率，可使用 `single` 或 `currency` / `bank` 子命令补充汇率表或银行牌价信息。
5. 用户问「美元人民币最近一周走势」「美元指数涨跌」时，优先调用 `realtime basic` 获取实时行情；需要历史走势时调用 `history2`（如 `USDCNY`）或 `history`（如 `from: USD, to: CNY`）。
6. 用户问「中行美元牌价最近几天变化」时，调用 `bankhistory` 并指定 `bank` 与 `code`。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

