# 官方 SDK（Python `pip install ashareapi` · Node.js `npm install ashareapi`）

**什么时候用 SDK 而不是直接打 HTTP**：
- ✅ **要写代码**（Python 脚本 / notebook / 回测 · Node 服务 / Next.js / 脚本）→ 用 SDK（省掉重试、异常分类、字段解析）
- ✅ Python 要成 **pandas DataFrame**（直接算 / 画图）→ 用 Python SDK
- ✅ Node 要 **TypeScript 类型**（编辑器补全 40 个方法与参数）→ 用 Node SDK
- ❌ 只是**取一个数看一眼** → 直接 `curl` / `fetch` 更快
- ❌ 用 **Go / Java / C# 等**（暂无官方 SDK）→ 直接调 HTTP（见 `endpoints.md`）

---

## 一、安装

**Python**（要求 3.9+；强依赖只有 `requests`，pandas 可选）：

```bash
pip install ashareapi            # 基础：返回 list[dict]
pip install "ashareapi[pandas]"  # 加 DataFrame 支持（推荐）
```

**Node.js / TypeScript**（要求 Node ≥ 18；**零运行时依赖**，用原生 `fetch`）：

```bash
npm install ashareapi
```

> ⚠️ Node SDK **只在服务端用**（Node / Next.js 服务端 / 云函数）—— 浏览器里会暴露你的 API Key，它刻意不提供浏览器构建。

## 二、快速开始

**Python**：

```python
from ashareapi import AShareAPI

cli = AShareAPI()                       # 免费端点无需 Key
df = cli.quote("sh600667")              # 实时行情 → DataFrame
print(df[["date", "last", "turnover"]])

print(cli.kline("600667.SH", count=5))  # 代码格式随便写（自动归一化）
print(cli.hot(limit=10))
print(cli.changedist())                 # 涨跌分布（市场广度）
```

**Node.js / TypeScript**（ESM 与 CommonJS 都支持）：

```ts
import { AShareAPI } from "ashareapi";   // CJS: const { AShareAPI } = require("ashareapi")

const cli = new AShareAPI();                  // 免费端点无需 Key
const bars = await cli.quote("sh600667");     // → 对象数组
console.log(bars[0]);                         // { date, open, last, high, low, volume, amount, turnover }

console.log(await cli.kline("600667.SH", "day", 5));
console.log(await cli.hot(10));
console.log(await cli.changedist());
```

**付费端点**：

```python
# Python
cli = AShareAPI("ct-你的Key")            # 或环境变量 ASHARE_API_KEY
print(cli.fund("sh600667"))              # 资金流 + 龙虎榜 + 大宗 + 两融
print(cli.finance("sh600667"))           # 三大报表
print(cli.lhb("institution"))            # 龙虎榜机构榜
print(cli.screen(preset="low_pe", orderby="ROETTM", limit=10))
print(cli.industry_chain(mode="stock", code="sh600667"))
```

```ts
// Node.js
const cli = new AShareAPI({ apiKey: "ct-你的Key" });   // 或 process.env.ASHARE_API_KEY
console.log(await cli.fund("sh600667"));
console.log(await cli.finance("sh600667"));
console.log(await cli.lhb("institution"));
console.log(await cli.screen("", "low_pe", 10, "ROETTM"));  // expr, preset, limit, orderby
console.log(await cli.industryChain("stock", "", "sh600667"));
```

**环境变量**（推荐，别把 Key 写死在代码里）：

```bash
export ASHARE_API_KEY=ct-你的Key          # Linux/macOS
set ASHARE_API_KEY=ct-你的Key             # Windows cmd
```

## 三、代码格式：三种写法都认

两个 SDK 内部都会把它们统一成 `sh600667`：

| 你写的 | 结果 |
|---|---|
| `sh600667` | `sh600667` |
| `600667.SH` | `sh600667` |
| `600667` | `sh600667`（按首位推断：5/6→沪 · 0/3→深 · 4/8→北）|

→ **从别处迁过来的代码基本不用改**。

## 四、40 个方法（与 HTTP 端点 1:1）

| 端点 | Python | Node.js |
|---|---|---|
| `/v1/quote` | `quote(code)` | `quote(code)` |
| `/v1/kline` | `kline(code, period, count)` | `kline(code, period, count)` |
| `/v1/hot` | `hot(limit)` | `hot(limit)` |
| `/v1/market-overview` | `market_overview(type)` | `marketOverview(type)` · 别名 `market_overview` |
| `/v1/changedist` | `changedist()` | `changedist()` |
| `/v1/health` · `/v1/challenge` · `/v1/usage` | `health()` `challenge()` `usage()` | 同 |
| `/v1/fund` | `fund(code)` | `fund(code)` |
| `/v1/lhb` | `lhb(type, date)` | `lhb(type, date)` |
| `/v1/margin-trade` | `margin_trade(code, date)` | `marginTrade(code, date)` · 别名 `margin_trade` |
| `/v1/block-trade` | `block_trade(code, date)` | `blockTrade(code, date)` · 别名 `block_trade` |
| `/v1/finance` | `finance(code, num)` | `finance(code, num)` |
| `/v1/dividend` · `/v1/shareholder` | `dividend(code, years)` `shareholder(code)` | 同 |
| `/v1/technical` · `/v1/chip` · `/v1/profile` · `/v1/search` | `technical(code)` `chip(code)` `profile(code)` `search(q)` | 同 |
| **`/v1/orderbook`**｜`orderbook(code)` | 同（五档盘口·**盘中**·量单位=手）|
| **`/v1/snapshot`**｜`snapshot(code)` | 同（全字段画像·**仅 A 股**·付费）|
| `/v1/events` · `/v1/calendar` | `events(code)` `calendar(date, limit)` | 同 |
| `/v1/sector` | `sector()` | `sector()` |
| `/v1/sector-valuation` | `sector_valuation(code)` | `sectorValuation(code)` · 别名 `sector_valuation` |
| `/v1/industry-chain` | `industry_chain(mode, topic, code)` | `industryChain(mode, topic, code)` · 别名 `industry_chain` |
| `/v1/bond` · `/v1/etf` · `/v1/ipo` | `bond(code)` `etf(code)` `ipo(days)` | 同 |
| `/v1/screen` | `screen(expr, preset, limit, orderby, desc, market)` | 同（位置参数）|
| `/v1/macro` | `macro(region, names)` | `macro(region, names)` |
| `/v1/dehydrated` | `dehydrated(mode, symbol, limit)` | `dehydrated(mode, symbol, limit)` |
| **`/v1/kline-full`** | `kline_full(code, fq, start, end)` | `klineFull(code, fq, start, end)` · 别名 `kline_full` |
| **`/v1/backtest`** | `backtest(strategy, mode, code, start, end, initial_cash, weighting, include_equity)` | `backtest({...})`（选项对象）|
| **`/v1/backtest-batch`** | `backtest_batch(codes, strategies, start, end, initial_cash)` | `backtestBatch(codes, strategies, start, end, initialCash)` |
| **`/v1/strategies`** | `strategies()` | `strategies()` |
| **`/v1/factors`** | `factors(category, kind)` | `factors(category, kind)` |
| **`/v1/playbooks`** | `playbooks(category, id)` | `playbooks(category, id)` |
| **`/v1/ip-whitelist`** | `ip_whitelist(action, ips)` | `ipWhitelist(action, ips)` · 别名 `ip_whitelist`（⚠️ **Unlimited 档**）|

> **方法是否与线上一致？** 两个 SDK 都有**覆盖守护测试**：拉 `/openapi.json` 比对方法名，端点增减即测试红灯。

## 五、返回形态（两者不同，注意）

⚠️ **端点返回的不总是"一张表"** —— `data` 有 **4 种形状**（对象数组 / 表列表 / 多段结构 / Markdown 文本，见 `endpoints.md`）。
SDK **只把「对象数组」转成 DataFrame**，其余**原样返回**（不强行套成 DataFrame）：

| 返回形状 | Python | Node.js |
|---|---|---|
| 对象数组（多数端点）| `pandas.DataFrame`（装了 pandas）/ `list[dict]` | **对象数组 `Row[]`** |
| 表列表（`finance`）| **`list[list[dict]]` 原样返回**（不套 DataFrame）| `TableList` = `Row[][]` |
| 多段结构（`shareholder` · `calendar`）| **`dict` 原样返回** | `SectionedResult` = `{tables, data}` |
| 完整信封 | `raw=True` | `new AShareAPI({ raw: true })` |
| 同步性 | **同步** | **全部返回 Promise**（要 `await`）|

**字段语义与单位**（手/元/百分数）见 `fields.md` —— 两个 SDK **都不会**帮你换算单位。

## 六、异常（5 类，各自告诉你做什么）

**Python**：

```python
from ashareapi import (AShareAPI, AShareError, AuthError, RateLimitError,
                       UpstreamError, EmptyResultError, APIError)

try:
    df = cli.fund("sh600667")
except AuthError as e:          # 401/403 → 付费端点缺 Key / IP 维度限制
    print(e)
except RateLimitError as e:     # 429 → 降频 · 解 PoW 提额（只提次数）· 升级档位
    print(e)
except UpstreamError as e:      # ok:false → 上游失败（已换源、不扣次数）→ 重试一次
    print(e)
except EmptyResultError as e:   # 当前无数据（如当天无大宗交易）→ 不计费，换条件
    print(e)
except APIError as e:           # 网络 / 5xx 重试耗尽
    print(e)
```

**Node.js**（同名 5 类，`instanceof` 判定）：

```ts
import { AShareAPI, AuthError, RateLimitError, UpstreamError, EmptyResultError } from "ashareapi";

try {
  const rows = await cli.fund("sh600667");
} catch (e) {
  if (e instanceof AuthError) console.log(e.message);            // 401/403
  else if (e instanceof RateLimitError) console.log(e.message);  // 429
  else if (e instanceof UpstreamError) console.log(e.message);   // ok:false → 重试一次
  else if (e instanceof EmptyResultError) console.log(e.message);// 当前无数据 → 不计费
  else throw e;
}
```

全部继承自 `AShareError`（Python 要一把抓就 `except AShareError`）。

**`EmptyResultError` 是 SDK 相对裸 HTTP 的独有改进**：把"**没有数据**"和"**取数失败**"分开，避免把"今天没大宗交易"当故障反复重试（细节见 `errors.md`）。

## 七、SDK vs 直接 HTTP vs 其他数据源

| | 官方 SDK | 自己 requests / fetch | 其他开源库 |
|---|---|---|---|
| 上手 | **装完即用** | 自己封装重试/异常 | 装完即用 |
| 返回 | **DataFrame**（Python）/ **对象数组**（Node）| 自己解析 | DataFrame |
| 免费试用 | **5 端点免 Key** | 同样免 Key | 视来源 |
| 错误处理 | **5 类异常**（含"无数据≠失败"）| 自己判断 | 自己判断 |
| 维护 | **我们维护**（多源自动切换）| 上游改了你改 | 上游改版常需跟进 |
| 依赖 | Python: `requests`（pandas 可选）/ Node: **零依赖** | 同 | 视库 |

## 八、边界（诚实）

- **K 线**：`period` 支持 `day` / `week` / `month` / `season` / `year` + **分钟线 `m1`~`m120`**（分钟线属付费层）；另有 `/v1/minute` **分时**
- **新闻/公告全文**不在 API 范围（有 `dehydrated` 研报摘要、`events` 事件标签）
- **不含投资建议** —— SDK 只负责取数
- **Node SDK 不要在浏览器里用**（会暴露 Key）
- 版本记录与更新：https://ashareapi.com/changelog
