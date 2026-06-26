---
name: datayes-stock-data
slug: datayes-stock-data
description: 通过 Datayes 查询 A 股和港股的行情、分时、K 线、财务、估值、资金流向、股东持仓、分红和公司资料。用户询问个股价格、公司基本面、估值指标、资金流向、排行筛选、技术指标或其他需要实时股票数据的问题时使用。
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["DATAYES_TOKEN"],
        "bins": ["python3"]
      }
    }
  }
---

# Datayes Stock Data

使用 Datayes 接口回答股票与上市公司数据问题。通过仓库内的 Python 脚本发请求。

## 前提条件

### 1. 获取 Datayes Token

访问 https://r.datayes.com/auth/login 登录 Datayes 账号，并在 Datayes 控制台获取可撤销的 API token。

### 2. 配置 Token

先确认环境变量已配置：

macOS / Linux:

```bash
export DATAYES_TOKEN='your-token'
```

Windows PowerShell:

```powershell
$env:DATAYES_TOKEN = "your-token"
```

Windows CMD:

```cmd
set DATAYES_TOKEN=your-token
```

建议只使用最小权限、可随时撤销的 token，不要把 token 写入仓库。

## 使用脚本

脚本位置：`scripts/datayes_api.py`

```bash
python3 scripts/datayes_api.py market_snapshot --param ticker=002594 --param type=stock --result-only --pretty
```

脚本行为：

- 自动从环境变量 `DATAYES_TOKEN` 读取 token。
- 在所有请求头里携带 `Authorization: Bearer <token>`。
- 先请求 API 规格接口，再按返回的 `httpUrl`、`httpMethod` 和参数位置调用真实业务接口。
- 真实业务接口的 `httpUrl` 会先校验主机名，只允许 Datayes 受信任域名，避免把 token 发送到非 Datayes 地址。
- 调用前按规格校验参数名，并自动补齐有默认值的必填参数。
- 支持 `--result-only` 只看业务结果，支持 `--field` 提取嵌套字段。
- 默认输出 JSON，并同时包含规格信息和业务结果。

## 工作流

1. 判断用户要查的是行情、财务、估值、资金流向、股东持仓还是公司资料。
2. 如果只有公司名，没有股票代码，先调用 `stock_search`。
3. 先用 `--spec-only` 拉取最新 API 规格，确认必填参数、参数位置和请求方法。
4. 再执行正式请求，必要时组合多个接口交叉验证。
5. 读取返回字段后，用自然语言总结结果，并明确时间范围、单位和口径。

## 常用命令

只查规格：

```bash
python3 scripts/datayes_api.py market_snapshot --spec-only --pretty
```

查股票代码：

```bash
python3 scripts/datayes_api.py stock_search --param query=比亚迪 --result-only --pretty
python3 scripts/datayes_api.py stock_search --param query=比亚迪 --result-only --field data.hits.0.entity_id
```

说明：`stock_search` 当前规格里的默认参数会自动补齐；常见返回字段是 `entity_id`，A 股场景下可直接作为股票代码使用。

查实时快照：

```bash
python3 scripts/datayes_api.py market_snapshot --param ticker=002594 --param type=stock --result-only --pretty
python3 scripts/datayes_api.py market_snapshot --param ticker=002594 --param type=stock --field result.data.lastPrice
```

查利润表：

```bash
python3 scripts/datayes_api.py fdmt_is_new_lt --param ticker=002594 --param reportType=A --param beginDate=20230101 --param endDate=20241231 --result-only --pretty
```

运行 smoke test：

```bash
python3 scripts/smoke_test.py
```

## 参数约定

- `--param key=value` 可重复传入多个参数。
- `value` 支持普通字符串，也支持 JSON 字面量；数组和布尔值可直接写成 JSON，例如 `--param ids='["000001","000002"]'`。
- 日期优先使用接口要求的格式，常见为 `YYYYMMDD`。
- 当接口要求 `type` 时，不要省略；例如区间涨跌统计通常要显式传 `type=stock`。
- 如果传入旧参数名或无效参数名，脚本会先本地报错，而不是把错误请求直接发到线上。
- `--field` 使用点路径；数组下标直接写数字，例如 `result.data.0.ticker`。

## 输出规则

- 优先引用接口返回的原始数值，不要凭经验补充未经验证的结论。
- 如果多个接口口径可能不同，先说明差异，再给结论。
- 如果接口报错或无数据，先检查股票代码、日期范围、`type`、`reportType` 等关键参数。
- 如果需要更多接口映射和常见参数，读取 `references/api-catalog.md`。
