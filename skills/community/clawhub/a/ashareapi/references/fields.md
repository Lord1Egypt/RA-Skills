# 字段语义与单位（算数前必读）

**为什么单独一份**：这些是最容易踩的坑 —— **不看会算错**（单位错 100 倍、`+` 拼成字符串）。

---

## 一、单位（最容易错）

| 字段 | 单位 | 示例 |
|---|---|---|
| `volume` | **手**（1 手 = 100 股）| `volume: 12345` = 123.45 万股 |
| `amount` | **元** | `amount: 135160431.2` = 1.35 亿元（**不是万元**！）|
| `turnover` | **百分数**（换手率%）| `turnover: 1.88` = 换手 1.88%（与 `/v1/snapshot` **同名同值**）|
| `instBuyRate` / `netBuyRate` | **百分数** | `20` 表示 **20%**（不是 0.2）|
| `pe` / `pb` / `ps` | 倍数 | `pe: 18.5` = 18.5 倍 |
| `totalMV` / 市值类 | 看字段名后缀 | 一般**元**或**亿元** —— 用前先看一条真实数据对量级 |

**自检方法**：拿一个熟悉的股票对量级。比如茅台现价 ~1300 元、市值 ~1.6 万亿 —— 如果算出来是 1.6 亿，就是单位错了 10000 倍。

## 二、数字常以**字符串**返回

上游很多金额字段是**字符串**：

```python
net = row["netBuyAmt"]        # "135160431.2" ← 字符串！
# ❌ net / 1e8                  → TypeError
# ❌ "100" + net                → 拼字符串 "100135160431.2"
net = float(row["netBuyAmt"]) # ✅ 先转 float 再算
print(round(net / 1e8, 2), "亿元")
```

**通用做法**：拿不准就先 `float()`；用 pandas 时 `df["col"].astype(float)`。

## 三、日期语义（别把昨天当今天）

- **`date` 字段 = 数据所属交易日**（不是查询时间）
- **休市日不会变成"今天"**：周六查 `quote`，返回的是**上一交易日**的数据，`date` 会如实标出
- **`quote` 的最新一根**（`data[0]`）就是当日实时（交易时段内）或当日收盘（收盘后）
- **`ok:false` 时 `data` 可能为空**（无数据），此时**没有** `date` 可读

⚠️ **字段名不一致（实测）—— 换端点会 KeyError**：

| 端点 | 日期字段 | 收盘/价格字段 |
|---|---|---|
| `/v1/quote` · `/v1/kline` | **`date`** | `last` |
| **`/v1/kline-full`** | **`time`** | **`close`** |
| **`/v1/minute`** | **`time`** | `price` |

⇒ 从 `kline` 迁到 `kline-full` 时，`data[0]["date"]` / `["last"]` **都会 KeyError**，要改成 `["time"]` / `["close"]`。

**用法**：要判断"这是不是今天的行情"，看 `date`（或 `time`）**而不是**看"我刚查的"。

## 四、返回结构：`data` 的四种形状（`structured` 是**条件字段**）

统一信封**只有 6 个键**（⚠️ 例外：`health` / `challenge` / `usage` / `ip-whitelist` 这 4 个**没有 `data`**，详见 `endpoints.md` 开头）：

```json
{ "ok": true, "endpoint": "quote", "tier": "free", "elapsed_ms": 42, "source": "multi",
  "data": [ {"date": "2026-09-24", "last": "19.41", "turnover": "0.54"}, ... ] }
```

⚠️ **`structured` / `tables` 不是标配** —— **只有 `data` 是 Markdown 文本时才附**
（`market-overview` / `changedist` / `lhb` / `sector` / `sector-valuation` / `bond` / `etf` / `screen` / `macro`）。
**其余端点没有这两个键** ⇒ **代码写 `body.get("structured")`，不要写 `body["structured"]`**（会 KeyError）。

`data` 本身的形状有 **4 种**（判别 + 通吃写法见 `endpoints.md` §返回形态）：

| `data` 形状 | 哪些端点 | 怎么读 |
|---|---|---|
| 对象数组 `[{"col": val}]` | 多数（`quote` `kline` `hot` `snapshot` `profile` …）| `data[0]["field"]` |
| 表列表 `[[行...], [行...]]` | `finance` | `data[表号][行号]["字段"]`（先按表索引）|
| 多段结构 `{tables:[{title,slug,rows}], data:{slug:rows}}` | `shareholder` · `calendar` | `data["tables"]` / `data["data"]["<slug>"]` |
| Markdown 字符串 | 上述 9 个 + `events` · `dehydrated` | 优先读同响应的 `structured` / `tables`（若存在）|

**纪律**：**程序化处理先判 `data` 形状**；**只有** Markdown 端点才退回 `structured`，**不要正则解析 Markdown**。

## 五、字段命名规律（好记）

| 后缀 / 词 | 含义 |
|---|---|
| `_TTM` | 滚动 12 个月（如 `ROETTM` / `PE_TTM`）|
| `YOY` | 同比（`NPParentCompanyYOY` = 归母净利同比）|
| `MOM` | 环比 |
| `Amt` | 金额（amount）|
| `Cnt` / `count` | 数量 |
| `Rate` / `Ratio` | **比率（多為百分数）**|
| `MV` | 市值（market value）|
| `NAV` / `NAPS` | 净值 / 每股净资产 |

## 六、几个具体端点的字段要点

| 端点 | 要点 |
|---|---|
| `fund` | 主力的**当日/5/10/20 日**净流入是不同字段；龙虎榜营业部明细在子结构里 |
| `lhb` | `activeseat` 的 `code` 与 `stockName` 是**分号分隔的等长列表**（`sh600127;sh600664`）→ `split(";")` 后按下标对应 |
| `changedist` | 是**当期**口径；`market-overview?type=updown` 是 **T-1** 口径，**两者数值会不同**（别混用）|
| `kline` | `period` 支持 day/week/month/season/year + 分钟线 `m1`~`m120`（付费层）；`count` 是根数 |
| `screen` | 返回的是股票列表（含命中因子值），排序用 `orderby` |

## 七、算数前检查清单

1. 单位对不对？（手/股 · 元/万元/亿元 · 百分数/小数）
2. 是不是字符串？（`float()` 了吗）
3. 日期是哪一天？（看 `date`）
4. 读的是 `structured` 还是 `data`？
5. 空结果 ≠ 0 —— 是"没有数据"，不是"值为 0"
