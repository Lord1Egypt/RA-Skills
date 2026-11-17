---
name: ashareapi
description: 用 ashareapi 获取 A 股数据：行情 / K线 / 财务三表 / 资金流 / 龙虎榜 / 板块 / 可转债 / 因子选股 / 量化回测 / 宏观 / 产业链。当用户要查 A 股现价、K线走势、财报（营收净利毛利率）、主力资金、龙虎榜（机构/游资）、涨停、板块轮动、可转债条款（强赎/双低）、ETF、新股打新、指数估值、产业链上下游，或要写调用 A 股数据的代码、接 REST API / 官方 SDK（Python：pip install ashareapi · Node.js：npm install ashareapi）时使用。含 40 个端点的参数与字段语义、单位换算（volume 是手 / amount 是元 / 比率为百分数）、数据日期语义、常见错误与限流处理（匿名 5 次/分、单次 250 条、每天 10 万条；解一次 PoW 挑战提到 15 次/分，每日条数不变）。
license: MIT
metadata:
  version: "0.2.8"
  updated: "2026-10-08"
  homepage: "https://ashareapi.com"
  docs: "https://ashareapi.com/docs"
  endpoints: "https://ashareapi.com/endpoints"
  changelog: "https://ashareapi.com/changelog"
---

# ashareapi — A 股数据 API

**40 个 HTTP 端点**（`https://api.ashareapi.com/v1/...`），覆盖行情 / K线 / **五档盘口** / 财务 / 资金 / 龙虎榜 / 板块 / 转债 / 选股 / 量化回测 / 宏观 / 产业链。
**5 个端点无需 Key**（装上就能调），其余需要 Key（¥9.9 起）。另有**官方 SDK**：Python `pip install ashareapi` · Node.js / TypeScript `npm install ashareapi`。

---

## 一、先判断：这个任务要不要 Key

| 任务 | 免费端点够不够 |
|---|---|
| 现价 / K线 / 热搜 / 市场总览 / 涨跌分布 | ✅ **够，无需 Key**（先试这个）|
| 财报 / 资金流 / 龙虎榜 / 板块 / 转债 / 选股 / 全历史K线 / **量化回测** / 宏观 … | ❌ 需要 Key（`Authorization: Bearer <key>`）|

**免费 5 个**：`/v1/quote`（行情）· `/v1/kline`（K线）· `/v1/hot`（热搜）· `/v1/market-overview`（大盘画像）· `/v1/changedist`（涨跌分布）
**工具端点**（也免 Key）：`/v1/health`（健康检查）· `/v1/challenge`（PoW 提额）

## 二、免费端点：直接调（无需任何鉴权）

```bash
# 行情：现价 / 开高低 / 成交量 / 换手率
curl "https://api.ashareapi.com/v1/quote?code=sh600667"

# K线（日/周/月）
curl "https://api.ashareapi.com/v1/kline?code=sh600667&period=day&count=5"

# 热搜榜
curl "https://api.ashareapi.com/v1/hot?limit=10"
```

Python：

```python
import requests

r = requests.get("https://api.ashareapi.com/v1/quote",
                 params={"code": "sh600667"}, timeout=10)
body = r.json()
if not body.get("ok"):
    raise RuntimeError(body)          # 上游取数失败（已自动换源，且不扣次数）
bar = body["data"][0]                 # 最新一根（当日实时）
print(bar["date"], bar["last"], bar["turnover"])
```

## 三、带 Key 调用

```bash
curl -H "Authorization: Bearer ct-你的Key" \
     "https://api.ashareapi.com/v1/fund?code=sh600667"
```

Key 从 https://ashareapi.com/pricing 获取。**401 = 没带 Key 调了付费端点**。

## 四、按任务找端点（决策树）

| 用户想要 | 用这个端点 | 备注 |
|---|---|---|
| 现价 / 开高低 / 换手 | `/v1/quote` | 免费 |
| **封单多少 / 买盘卖盘 / 盘口 / 挂单** | **`/v1/orderbook`** | **五档盘口**（买五卖五·秒级快照·**盘中才有意义**·量单位=手）|
| **估值 / PE / PB / 市值 / 股本 / 涨停价** | **`/v1/snapshot`** | **全字段画像**（**仅A股**·付费·**要多项时比分别调更省次数**）|
| 走势 / 历史 K线 | `/v1/kline` | 日/周/月/季/年免费；**分钟线 `m1`~`m120` 付费**（窗口近 1 个月）。复权口径由服务端固定：日线及以上前复权（除权除息日不跳空），分钟线不复权 ——**不要再自己复权**（会二次复权）|
| 分时（盘中每分钟价+累计量）| `/v1/minute` | 付费；`days` 只有 `1`（当日）和 `5`（近 5 日）两档。⚠️ 与上面「分钟 K 线」不是一回事 |
| 什么股票热门 | `/v1/hot` | 免费 |
| 大盘怎么样 / 风格轮动 / 估值分位 | `/v1/market-overview` | 免费；`type` 选 summary/trade/interval/technical/margin/valuation/rotation |
| 涨跌家数 / 涨停家数 / 市场广度 | `/v1/changedist` | 免费；**当期口径**（别用 market-overview?type=updown，那是 T-1）|
| 财报 / 营收 / 净利润 / 毛利率 | `/v1/finance` | 三表 |
| 主力资金 / 资金流 / 龙虎榜 / 大宗 / 两融 | **`/v1/fund`** | **一个接口拿全交易面**（优先用）|
| 龙虎榜分榜（机构 / 游资 / 席位）| `/v1/lhb` | `type=institution/hotmoney/activeseat` |
| 技术面 / MACD / KDJ / RSI / BOLL | `/v1/technical` | |
| 谁在持有 / 股东户数 / 机构持仓 | `/v1/shareholder` | |
| 筹码 / 套牢盘 / 成本分布 | `/v1/chip` | |
| 板块涨幅榜 / 轮动 | `/v1/sector` | |
| 某板块贵不贵 / 估值分位 | `/v1/sector-valuation` | `code=pt01801780` 形式 |
| 可转债 / 强赎 / 双低 / 溢价 | `/v1/bond` | `code=sh113052` 形式 |
| ETF | `/v1/etf` | `code=sh510300` |
| 新股 / 打新 | `/v1/ipo` | |
| 分红送转 | `/v1/dividend` | |
| 个股事件（42 类）/ 解禁 / 回购 | `/v1/events` | |
| 个股事件日历（某日有什么事件）| `/v1/calendar` | **不是宏观日历**（宏观用 `/v1/macro`）|
| 研报 / 机构观点 | `/v1/dehydrated` | `mode=list/detail` |
| 宏观 / LPR / CPI / GDP | `/v1/macro` | `region=cn/us/...` |
| 产业链 / 上下游 / 某公司链上位置 | `/v1/industry-chain` | `mode=list/graph/stock` |
| 筛选股票 / 低估高 ROE | `/v1/screen` | `expr` 多因子交集 或 `preset`（22 个预设）|
| 只知道名字，要代码 | `/v1/search` | **先搜代码再查数据** |
| 公司是做什么的 | `/v1/profile` | |
| 融资融券 | `/v1/margin-trade` | `code` 必填（支持批量）|
| 大宗交易 | `/v1/block-trade` | |
| 我的用量 / 额度 | `/v1/usage` | |
| **回测某策略 / 历史收益 / 最大回撤** | **`/v1/backtest`** | `mode=single` 单标的·实时（配 `code`）· `mode=portfolio` 组合·查预置区间。⚠️ 成本已计入 |
| **多标的 × 多策略对比** | `/v1/backtest-batch` | ≤20 标的 × ≤10 策略 |
| **有哪些策略 / 参数范围** | `/v1/strategies` | **先查再回测**（静态清单，不占额度）|
| 有哪些因子 / 筛股模板 | `/v1/factors` | ⚠️ 要用因子**实际选股**请用 `/v1/screen` |
| 怎么判断市场（方法论）| `/v1/playbooks` | 13 条流程（判据/阶段/实测证据），**不是数据** |

**完整参数与返回字段** → 读 `references/endpoints.md`。

## 五、四个必知语义（最常踩的坑）

1. **单位不统一，先看清**
   - `volume` 是**手**（×100 = 股）· `amount` 是**元**（不是万元）
   - 比率字段是**百分数**：`instBuyRate: 20` 表示 **20%**（不是 0.2）
   - 金额有时以**字符串**返回（`"135160431.2"`）→ **先 `float()` 再算**，否则 `+` 会拼字符串

2. **数据日期语义**：休市日**不会**变成"今天"。看返回里的 `date` 字段判断数据属于哪个交易日（`quote` 的最新一根就是当日实时）。

3. **返回结构：`data` 是主载荷，形状有 4 种**（统一信封 `{ok, endpoint, tier, elapsed_ms, source, data}`）
   - `data` 可能是：**对象数组**（多数端点）/ **表列表**（`finance`）/ **多段结构**（`shareholder`·`calendar`）/ **Markdown 文本**（`bond`·`sector` 等 9 个）
   - ⚠️ **`structured` / `tables` 是【条件字段】—— 不是每个端点都有**：**只有 `data` 是 Markdown 时才附**
     ⇒ 代码里**一律写 `body.get("structured")`**；写 `body["structured"]` 在 `quote`/`kline`/`finance` 上会 **KeyError**
   - ⚠️ `/v1/health` · `/v1/challenge` · `/v1/usage` · `/v1/ip-whitelist` 信封**没有 `data`**
   - 四种形状怎么判别 + 通吃写法 → `references/endpoints.md` §返回形态

4. **`ok:false` 不等于"我们写错了"**：那是**上游取数失败**（我们已自动换源，**不扣调用次数**）→ 重试一次通常就好。**空结果**（如当天没大宗交易）与"失败"是两件事。

## 六、错误与限流

| 现象 | 含义 | 怎么办 |
|---|---|---|
| **401** | 没带 Key 调了付费端点 | 拿 Key，或改用 5 个免费端点 |
| **429** | 超出限额（匿名：**每分钟次数** 或 **当天条数**）| 次数超 → 降频，或**解一次 PoW 挑战提到 15 次/分**（见下）；**条数超 → 解 PoW 无效**，次日恢复，或用 Key |
| **`ok:false`** | 上游取数失败（已自动换源）| **不扣次数**，重试一次 |
| **200 但 data 为空** | 当前确实没有这类数据（如当天无大宗交易）| 换条件 / 稍后再试，**不是故障** |
| **5xx** | 重试耗尽 | 稍后再试 |

**匿名提额（PoW）**：

```bash
# 1) 拿挑战
curl "https://api.ashareapi.com/v1/challenge"
# → {challenge, difficulty, expires_in, how_to}
# 2) 算 nonce（sha256(challenge.nonce) 前 difficulty 位为 0），然后：
curl -H "X-PoW: <challenge>.<nonce>" "https://api.ashareapi.com/v1/quote?code=sh600667"
```

⚠️ PoW 只提升**每分钟次数**，**不提升每日条数** —— 匿名每天仍最多 **10 万条**；批量补历史/回测请用 Key。

详细错误语义 → 读 `references/errors.md`。

## 七、要写代码？用官方 SDK（Python / Node.js）

**Python**：

```bash
pip install ashareapi            # 基础（返回 list[dict]）
pip install "ashareapi[pandas]"  # 加 DataFrame 支持（推荐）
```

```python
from ashareapi import AShareAPI

cli = AShareAPI()                  # 免费端点无需 Key
df = cli.quote("sh600667")         # → DataFrame
print(df[["date", "last", "turnover"]])

cli = AShareAPI("ct-你的Key")      # 付费端点
print(cli.fund("sh600667"))        # 资金流 + 龙虎榜 + 大宗 + 两融
print(cli.screen(preset="low_pe", limit=10))
```

**Node.js / TypeScript**：

```bash
npm install ashareapi            # 零运行时依赖（原生 fetch，需 Node ≥ 18）
```

```ts
import { AShareAPI } from "ashareapi";

const cli = new AShareAPI();                 // 免费端点无需 Key
const bars = await cli.quote("sh600667");    // → 对象数组
console.log(bars[0].last);

const paid = new AShareAPI({ apiKey: "ct-你的Key" });
console.log(await paid.screen("", "low_pe", 10, "ROETTM"));
```

> 两个 SDK **同 40 个方法 / 同 5 类异常 / 同重试策略**；差异只是语言惯例：
> Python 用 `snake_case` 且返回 DataFrame，Node 用 `camelCase`（也认 `snake_case` 别名）且**全部返回 Promise**。

**代码格式随便写**：`sh600667` / `600667.SH` / `600667` 都认（自动归一化）。
**40 个端点 = 40 个方法**（`/v1/margin-trade` → Python `margin_trade()` / Node `marginTrade()`）。

完整用法与 5 类异常 → 读 `references/sdk.md`。

## 八、详细参考（按需读取，不要一次全读）

| 文件 | 什么时候读 |
|---|---|
| [references/endpoints.md](references/endpoints.md) | 要确认某端点的**完整参数 / 返回字段** |
| [references/fields.md](references/fields.md) | 要**算数**（单位换算、字段含义、字符串数字）|
| [references/errors.md](references/errors.md) | 遇到 401/429/ok:false/空结果，或要处理限流 |
| [references/sdk.md](references/sdk.md) | 用户要**写 Python / Node.js 代码**或问 SDK |

---

**边界（诚实）**：
- K 线支持**日/周/月/季/年** + **分钟线 `m1`~`m120`**（分钟线属付费层，窗口近 1 个月）；另有 `/v1/minute` **分时**（当日 / 近 5 日）。⚠️ 期货 / 外汇 / 北交所**无分钟线**
- 新闻/公告**全文**不在 API 范围（有 `dehydrated` 研报摘要、`events` 事件标签、`calendar` 事件日历）
- 数据仅供研究参考，**不构成投资建议** —— 本 skill 只讲怎么取数与计算，不给买卖建议

---

## 九、本 skill 版本

**当前版本：`0.2.8`（2026-10-08）**

**本版更新**：
- **新增 7 个端点**（端点数 **33 → 40**）：量化回测 `/v1/backtest`（单标的实时 / 组合预置区间）· `/v1/backtest-batch`（多标的×多策略矩阵，≤20×≤10）· `/v1/strategies`（策略清单 20+9 条）· `/v1/factors`（因子库 88 因子 + 50 筛选入口 + 22 预设）· `/v1/playbooks`（方法论 13 条）· `/v1/kline-full`（10 年全历史日线，可选复权）· `/v1/ip-whitelist`（IP 白名单，Unlimited 档）。
- **MCP 工具 25 → 31**、**SDK 方法 33 → 40**（`references/` 三份同步）。
- **修正边界说明**：此前写「K 线没有分钟级」与实际不符 —— 分钟线（`m1`~`m120`）与分时 `/v1/minute` 均已提供（属付费层）。
- **补 `/v1/kline-full` 说明**：与 `/v1/kline` 的区别是「全历史 + 复权口径可选」。

### 怎么知道该更新

本 skill 是**随 API 演进的快照** —— 每次新增端点/字段，`references/` 里的清单会同步但**你手上装的可能还是旧版**。判断方法：

| 检查 | 说明 |
|---|---|
| `metadata.version` | 看本文件 frontmatter 的版本号 |
| **端点总数** | 对比现实：**当前 40 个**（`endpoints.md` 标题也是这个数）|
| **MCP 工具数** | 当前 **31 个**（`list_tools` 返回数量）|

**任一项对不上 → 你装的是旧版。**

### 怎么更新

1. 重新下载：**https://ashareapi.com/skill**（页面有 zip 下载）
2. 解压覆盖到你的 skills 目录（`.claude/skills/` · `.agents/skills/` · `.opencode/skills/` 等）
3. 重启客户端

> ⚠️ **API 本身不需要更新** —— 端点永远是最新的（服务端演进）；需要更新的是**这份说明**（否则你可能不知道新端点存在）。

### 版本记录

| 版本 | 日期 | 变化 |
|---|---|---|
| `0.2.8` | 2026-10-08 | **新增 7 个端点**：量化回测 `/v1/backtest`（单标的实时 / 组合预置区间）· `/v1/backtest-batch`（多标的×多策略矩阵）· `/v1/strategies`（策略清单 20+9）· `/v1/factors`（因子库 88+50+22）· `/v1/playbooks`（方法论 13 条）· `/v1/kline-full`（10 年全历史）· `/v1/ip-whitelist`（IP 白名单，Unlimited 档）· 端点数 **33 → 40** · MCP 工具 **25 → 31** · SDK 方法 **33 → 40**（`references/` 三份同步） |
| `0.2.7` | 2026-10-06 | **新增 `/v1/minute` 分时端点**（当日 / 近 5 日盘中走势，`days` 只有 `1`/`5` 两档）· 端点数 **32 → 33** · `/v1/kline` 放开**分钟线**（`m1`~`m120`）与 `start`/`end` 日期范围（均属付费层）· MCP 工具 **24 → 25** |
| `0.2.6` | 2026-10-03 | 匿名 **429 提示口径更准确**（单次最多 250 条 / 每天最多 10 万条；区分「每分钟次数超」与「当天条数超」） |
| `0.2.5` | 2026-10-01 | 文档更新：K 线复权口径表述统一 · 明确 `days` 只有 `1`/`5` 两档 |
| `0.2.4` | 2026-09-30 | **文档表述统一**：全文改为面向使用者的表述；**端点 / 字段 / 口径无任何变化** |
| `0.2.3` | 2026-09-28 | **补 K 线价格口径**：`/v1/kline` 明确「口径**固定为前复权**（除权除息日不跳空）、**无 `adjust` 参数**、**不要再自己复权**（会二次复权）」（`SKILL.md` 速查表 + `references/endpoints.md` 同步）|
| `0.2.2` | 2026-09-26 | 换手率字段统一为 **`turnover`**（%）—— 与 `/v1/snapshot` 同名同值（`references/fields.md` 字段表 · `endpoints.md` · `sdk.md` 示例同步）|
| `0.2.1` | 2026-09-26 | **完善返回结构文档**：明确 `structured`/`tables` 是**条件字段**（仅 `data` 为 Markdown 时才附）· 新增「`data` 四种形状」速查表 + 通吃写法 · `snapshot` 字段数 → **35** · 补 `finance` 表列表 / `shareholder`·`calendar` 多段结构 / `fund` 扁平 dict · 补 `profile` 字段说明 |
| `0.2.0` | 2026-09-23 | 新增 `/v1/snapshot`（全字段画像）· `/v1/orderbook`（五档盘口）· 端点数 30→32 · MCP 工具 22→24 · 补字段单位与"计费=次数"说明 |
| `0.1.0` | 2026-09-20 | 首个版本（30 个端点 · 22 个 MCP 工具）|

**完整更新日志（含字段级变更）→ https://ashareapi.com/changelog**

