---
name: a-stock-individual-analysis
description: A股个股深度分析 — 五模块框架（基本面/趋势量价/紫苏叶逻辑/近期消息/综合总结）。基于a-stock-data工具包的真实数据，覆盖订单可见度、毛利率方向、现金流匹配度、产能扩张动因、PE/PEG/EPS、均线量价、主力资金、技术壁垒、行业卡位、供需研判、近期新闻研报、解禁预警等维度。适用于个股深度研判、估值分析、买卖点判断。涉及"分析个股""深度研判""估值分析""紫苏叶""serenity""个股报告"时激活。
origin: custom
version: 1.1.0
---

# A股个股深度分析 V1.1

五模块分析框架，基于真实数据，参考白毛股神 Serenity 的紫苏叶方法论。

---

## When to Activate

- 用户要求"分析XXX股票""深度研判XXX""给XXX做个分析"
- 用户问"这个股怎么样""值不值得买/持有"
- 用户提到"紫苏叶""serenity""白毛股神"方法论
- 用户要求"估值分析""个股报告"
- 关键词：分析个股、深度研判、估值分析、紫苏叶、个股报告、买卖点

---

## 数据获取策略（优先级递进）

```
第一优先：a-stock-data 工具包（mootdx / 腾讯 / 新浪 / 东财 / 同花顺）
    ↓ 失败
第二优先：联网搜索（web_search）+ 公开 API 自行调用
    ↓ 失败
第三优先：标记「⚠️ 数据不可获取」
```

**成功获取的数据源及调用方式必须沉淀到本 SKILL 的「已知可用端点」章节，未来直接复用。**

### 已知可用端点

| 数据 | 端点 | 方式 |
|------|------|------|
| 实时行情（PE/PB/市值等） | 腾讯财经 `qt.gtimg.cn` | urllib GBK |
| K线 + 均线 + RSI | mootdx TCP 7709 | Python (需重命名 datetime 列) |
| 一致预期 EPS | 同花顺 `basic.10jqka.com.cn` | requests + pd.read_html |
| 研报列表+评级+EPS预测 | 东财 `reportapi.eastmoney.com` | em_get 限流 |
| 板块归属（行业/概念） | 东财 `push2 slist spt=3` | em_get 限流 |
| 限售解禁 | 东财 `datacenter RPT_LIFT_STAGE` | em_get 限流 |
| 龙虎榜 | 东财 `datacenter RPT_DAILYBILLBOARD_DETAILSNEW` | em_get 限流 |
| 资金流向（分钟级） | 东财 `push2 fflow/kline` | em_get 限流（仅交易时间） |
| 股东户数 | 东财 `datacenter RPT_F10_FINANCE_HOLDERINFO` | em_get 限流 |
| 新闻 | web_search 联网搜索 | 当东财 API 不可用时 |
| 财报明细（三表） | web_search 联网补充 | 当新浪 API 不可用时 |
| 行业对比/竞争格局 | web_search 联网搜索 | 补充分析 |

---

## 分析前准备

1. 用户必须提供股票代码（6 位数字），若只提供名称则先确认代码
2. 先读取 `~/.agents/skills/a-stock-data/SKILL.md` 确认端点
3. 运行内置数据采集脚本
4. 任何数据源失败 → 尝试 fallback（联网搜索 / 其他公开 API）
5. 所有尝试失败 → 标注「⚠️ 数据不可获取」，不编造

---

## 数据采集脚本

```python
"""A股个股深度分析 — 数据采集脚本 V1.1"""
import sys, json, time, random, requests, urllib.request, pandas as pd
from datetime import datetime, timedelta
from io import StringIO

CODE = sys.argv[1] if len(sys.argv) > 1 else "600519"
PREFIX_SH = CODE.startswith(("6", "9"))
PREFIX_BJ = CODE.startswith("8")
SECID = f"1.{CODE}" if PREFIX_SH else (f"0.{CODE}" if not PREFIX_BJ else f"2.{CODE}")
TODAY = datetime.now().strftime("%Y-%m-%d")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# 东财防封
EM_SESSION = requests.Session()
EM_SESSION.headers.update({"User-Agent": UA})
EM_MIN_INTERVAL = 1.2
_em_last_call = [0.0]

def em_get(url, params=None, headers=None, timeout=15, **kwargs):
    wait = EM_MIN_INTERVAL - (time.time() - _em_last_call[0])
    if wait > 0: time.sleep(wait + random.uniform(0.1, 0.5))
    try: return EM_SESSION.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
    finally: _em_last_call[0] = time.time()

def eastmoney_datacenter(report_name, columns="ALL", filter_str="", page_size=50, sort_columns="", sort_types="-1"):
    params = {"reportName": report_name, "columns": columns, "filter": filter_str, "pageNumber": "1", "pageSize": str(page_size), "sortColumns": sort_columns, "sortTypes": sort_types, "source": "WEB", "client": "WEB"}
    r = em_get("https://datacenter-web.eastmoney.com/api/data/v1/get", params=params)
    d = r.json()
    return d["result"]["data"] if d.get("result") and d["result"].get("data") else []

result = {"code": CODE, "分析时间": TODAY}

# ======================== 阶段1: 实时行情 ========================
print(">>> [1/7] 实时行情...", file=sys.stderr)
pfx = "sh" if PREFIX_SH else ("bj" if PREFIX_BJ else "sz")
try:
    req = urllib.request.Request(f"https://qt.gtimg.cn/q={pfx}{CODE}")
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = urllib.request.urlopen(req, timeout=10)
    vals = resp.read().decode("gbk").split('"')[1].split("~")
    if len(vals) >= 53:
        result["实时行情"] = {
            "名称": vals[1], "现价": float(vals[3] or 0), "昨收": float(vals[4] or 0),
            "今开": float(vals[5] or 0), "最高": float(vals[33] or 0), "最低": float(vals[34] or 0),
            "涨跌幅%": float(vals[32] or 0), "成交额_万": float(vals[37] or 0),
            "换手率%": float(vals[38] or 0), "PE_TTM": float(vals[39] or 0),
            "总市值_亿": float(vals[44] or 0), "流通市值_亿": float(vals[45] or 0),
            "PB": float(vals[46] or 0), "涨停价": float(vals[47] or 0),
            "跌停价": float(vals[48] or 0), "量比": float(vals[49] or 0), "PE_静": float(vals[52] or 0),
        }
except Exception as e: result["实时行情"] = {"error": str(e)}

# ======================== 阶段2: K线技术（mootdx） ========================
print(">>> [2/7] K线技术...", file=sys.stderr)
try:
    from mootdx.quotes import Quotes
    client = Quotes.factory(market='std')
    klines = client.bars(symbol=CODE, category=4, offset=250)
    if klines is not None and len(klines) > 0:
        df = pd.DataFrame(klines)
        if 'datetime' in df.columns: df = df.rename(columns={'datetime': 'dt'})
        df = df.sort_values("dt")
        for ma in [5, 10, 20, 60, 120, 250]: df[f"MA{ma}"] = df["close"].rolling(ma).mean()
        recent = df.tail(60)
        last = df.iloc[-1]
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + gain / loss))
        vol_ma20 = recent["vol"].rolling(20).mean().iloc[-1] if len(recent) >= 20 else recent["vol"].mean()
        vol_ratio = last["vol"] / vol_ma20 if vol_ma20 > 0 else 0
        mas = []
        price = last["close"]
        for m in [5, 10, 20, 60, 120, 250]:
            v = last[f"MA{m}"]
            if pd.notna(v): mas.append({"均线": f"MA{m}", "价格": round(float(v),2), "偏离%": round(float((price-v)/v*100),2)})
        result["K线技术"] = {
            "最新价": round(float(price), 2),
            "均线": {f"MA{m}": round(float(last[f"MA{m}"]),2) if pd.notna(last[f"MA{m}"]) else None for m in [5,10,20,60,120,250]},
            "RSI14": round(float(rsi.iloc[-1]), 2) if pd.notna(rsi.iloc[-1]) else None,
            "量比": round(float(vol_ratio), 2),
            "60日最高": round(float(recent["high"].max()), 2),
            "60日最低": round(float(recent["low"].min()), 2),
            "从高点回调%": round(float((price-recent["high"].max())/recent["high"].max()*100),2),
            "60日涨跌幅%": round(float((price-recent.iloc[0]["close"])/recent.iloc[0]["close"]*100),2),
        }
except Exception as e: result["K线技术"] = {"error": str(e)}

# ======================== 阶段3: 一致预期EPS ========================
print(">>> [3/7] 一致预期...", file=sys.stderr)
try:
    r = requests.get(f"https://basic.10jqka.com.cn/new/{CODE}/worth.html", headers={"User-Agent": UA, "Referer": "https://basic.10jqka.com.cn/"}, timeout=15)
    r.encoding = "gbk"
    dfs = pd.read_html(StringIO(r.text))
    for df in dfs:
        cols = [str(c) for c in df.columns]
        if any("每股收益" in c or "均值" in c for c in cols):
            result["一致预期EPS"] = df.to_dict(orient="records")
            break
except Exception as e: result["一致预期EPS"] = {"error": str(e)}

# ======================== 阶段4: 东财系（串行限流） ========================
print(">>> [4/7] 研报...", file=sys.stderr)
try:
    reports = []
    for page in range(1, 4):
        params = {"industryCode": "*", "pageSize": "50", "industry": "*", "rating": "*", "ratingChange": "*", "beginTime": (datetime.now()-timedelta(days=180)).strftime("%Y-%m-%d"), "endTime": TODAY, "pageNo": str(page), "qType": "0", "orgCode": "", "code": CODE, "rcode": "", "p": str(page), "pageNum": str(page), "pageNumber": str(page)}
        r = em_get("https://reportapi.eastmoney.com/report/list", params=params, headers={"Referer": "https://data.eastmoney.com/"}, timeout=30)
        rows = (r.json().get("data") or [])
        if not rows: break
        for row in rows:
            reports.append({"日期": (row.get("publishDate") or "")[:10], "机构": row.get("orgSName", ""), "标题": row.get("title", ""), "评级": row.get("emRatingName", ""), "今年EPS": row.get("predictThisYearEps", ""), "明年EPS": row.get("predictNextYearEps", ""), "后年EPS": row.get("predictNextTwoYearEps", "")})
        if page >= (r.json().get("TotalPage", 1) or 1): break
    result["研报"] = reports[:15]
except Exception as e: result["研报"] = {"error": str(e)}

print(">>> [5/7] 解禁+龙虎榜...", file=sys.stderr)
try:
    end_d = (datetime.now()+timedelta(days=90)).strftime("%Y-%m-%d")
    data = eastmoney_datacenter("RPT_LIFT_STAGE", filter_str=f"(SECURITY_CODE=\"{CODE}\")(FREE_DATE>='{TODAY}')(FREE_DATE<='{end_d}')", page_size=10, sort_columns="FREE_DATE", sort_types="1")
    result["解禁"] = [{"日期": str(r.get("FREE_DATE",""))[:10], "类型": r.get("LIMITED_STOCK_TYPE",""), "占比%": r.get("FREE_RATIO",0)} for r in data]
except Exception as e: result["解禁"] = {"error": str(e)}

try:
    start_lh = (datetime.now()-timedelta(days=30)).strftime("%Y-%m-%d")
    data = eastmoney_datacenter("RPT_DAILYBILLBOARD_DETAILSNEW", filter_str=f"(TRADE_DATE>='{start_lh}')(TRADE_DATE<='{TODAY}')(SECURITY_CODE=\"{CODE}\")", page_size=20, sort_columns="TRADE_DATE", sort_types="-1")
    result["龙虎榜"] = [{"日期": str(r.get("TRADE_DATE",""))[:10], "原因": r.get("EXPLANATION",""), "净买_万": round((r.get("BILLBOARD_NET_AMT") or 0)/10000,1)} for r in data]
except Exception as e: result["龙虎榜"] = {"error": str(e)}

print(">>> [6/7] 板块归属...", file=sys.stderr)
try:
    mc = 1 if PREFIX_SH else 0
    params = {"fltt": "2", "invt": "2", "secid": f"{mc}.{CODE}", "spt": "3", "pi": "0", "pz": "200", "po": "1", "fields": "f12,f14,f3,f128"}
    r = em_get("https://push2.eastmoney.com/api/qt/slist/get", params=params, headers={"Referer": "https://quote.eastmoney.com/"}, timeout=15)
    diff = (r.json().get("data") or {}).get("diff") or {}
    items = diff.values() if isinstance(diff, dict) else diff
    result["板块归属"] = [{"板块": it.get("f14",""), "BK码": it.get("f12",""), "涨跌幅%": it.get("f3",""), "龙头": it.get("f128","")} for it in items]
except Exception as e: result["板块归属"] = {"error": str(e)}

# ======================== 阶段7: 资金流向（仅交易时间） ========================
print(">>> [7/7] 资金流向...", file=sys.stderr)
try:
    params = {"secid": SECID, "klt": 1, "fields1": "f1,f2,f3,f7", "fields2": "f51,f52,f53,f54,f55,f56,f57"}
    r = em_get("https://push2.eastmoney.com/api/qt/stock/fflow/kline/get", params=params, headers={"Referer": "https://quote.eastmoney.com/"}, timeout=10)
    rows = [l.split(",") for l in r.json().get("data",{}).get("klines",[])]
    total = sum(float(p[1]) for p in rows if len(p)>=6)
    result["资金流向"] = {"主力累计_万元": round(total/10000,1), "方向": "流入" if total>0 else "流出"}
except Exception as e: result["资金流向"] = {"error": str(e), "note": "非交易时间或接口不可用"}

print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
```

---

## 分析报告模板

数据采集完成后，按以下模板撰写分析报告。

---

### 📊 {股票名称}（{代码}）深度分析报告

> 分析时间：{时间} | 当前价：**{现价}元** | 总市值：**{总市值}亿** | PE(TTM)：{PE} | PB：{PB}

---

### 一、基本面分析

#### 1a. 订单可见度

从预收账款/合同负债趋势、营收增速、公告大单等维度分析：
- 营收增速是否匹配预收/合同负债增长
- 是否有实打实的大单公告（非仅"在手订单"话术）
- 判断：订单是否真实体现在报表中

#### 1b. 毛利率方向

分析毛利率趋势：
- 稳定/提升 → 溢价能力强，技术壁垒牢
- 下滑 → 竞争加剧或成本压力上升
- 结合行业景气度判断方向

#### 1c. 现金流匹配度

- 经营性现金流 vs 净利润的比值（> 0.8 健康）
- 应收占比趋势（持续抬升 = 盈利含水）

#### 1d. 产能扩张动因

- 固定资产 + 在建工程趋势
- 产能扩张是否由真实订单倒逼（营收同步增长）
- 是否有定增/可转债等融资行为

#### 基本面总评

> 综合订单可见度、毛利率方向、现金流质量、产能动因四个维度，基本面整体打分（1-5）：
> **{得分}/5**

---

### 二、趋势量价分析

#### 估值锚

| 指标 | 数值 |
|------|------|
| PE(TTM) | {x} |
| 26/27/28 年一致预期 EPS | {x} / {x} / {x} |
| 26/27 年前向 PE | {x}x / {x}x |
| PEG（27年EPS增速） | {x} |

**估值判断：** （基于前向 PE 和 PEG 的合理区间判断）

#### 量价趋势

> 现价 vs 各均线关系 + RSI 超买超卖 + 量价配合 + 支撑/压力位

#### 主力资金

（仅当数据可获取时纳入。不可获取 → 本小节不出现）

---

### 三、紫苏叶逻辑

> 参考白毛股神 Serenity 的分析框架，从商业模式本质出发，研判该标的是否具备"紫苏叶"属性——即拥有难以复制的竞争壁垒 + 占据产业链不可替代的位置 + 受益于持续紧张的供需格局。

核心研判维度（不限于以下，以 Serenity 框架为准）：

- **护城河深度：** 毛利率反映的定价权、技术路径的独占性、客户转换成本
- **产业链议价权：** 对上下游的议价能力、在产业链中的可替代性
- **增长持续性：** 需求的刚性程度、供给扩张的难度和周期
- **竞争格局：** 行业集中度、新进入者威胁、替代品风险

#### 紫苏叶判定

> 综合研判该标的是否属于紫苏叶——即「好生意 + 好位置 + 好时机」三重共振

---

### 四、近期消息面

> 数据获取优先使用 a-stock-data；失败则通过 web_search 联网搜索补充。仍无法获取 → 标注。

- **近期研报：** 近 6 月研报数量及评级分布
- **关键研报摘要：** 最近 3~5 篇核心观点
- **近期新闻：** 重要公司/行业动态（联网搜索补充）
- **解禁预警：** 未来 90 天有无解禁
- **龙虎榜：** 近 30 日有无异动上榜

---

### 五、综合总结

#### 短期研判（1-3 个月）

基于技术面（均线/RSI/量价）和近期催化剂，给出方向判断和关键价位。

#### 长期研判（6-12 个月）

基于基本面 + 紫苏叶逻辑 + 行业景气度，给出估值目标价区间。

**目标价推算：**

| 情景 | PE | 目标价 | 逻辑 |
|------|:--:|------:|------|
| 保守 | {x}x | **{x}元** | |
| 基准 | {x}x | **{x}元** | |
| 乐观 | {x}x | **{x}元** | |

#### 买卖点参考

| 维度 | 判断 |
|------|------|
| 当前估值 | 偏贵 / 合理 / 低估 |
| 短期支撑/压力 | {x}元 / {x}元 |
| 长期目标区间 | **{x} - {x}元** |

#### 一句话总结

> 🦞 用 2-3 句话概括该标的核心逻辑：它是什么 / 为什么值得关注 / 当前处于什么位置 / 关键催化剂是什么。

---

> ⚠️ **免责声明：** 本报告基于公开数据和量化分析框架，不构成任何投资建议。股市有风险，投资需谨慎。所有估值目标价均为模型测算，实际走势受多重因素影响。

---

## 执行流程总结

1. 读取 `~/.agents/skills/a-stock-data/SKILL.md` 确认端点
2. 运行数据采集脚本：`python3 /tmp/stock_analysis.py <代码>`
3. 检查各模块数据完整性，缺失项尝试联网搜索补充
4. 按上述报告模板撰写分析
5. 不编造数据，获取不到 → 如实标注

## 新闻/数据 fallback 方法

当 a-stock-data 接口不可用时，按以下优先级尝试：

1. **web_search** 搜索 `"{股票名称} 最新消息"`、`"{股票名称} 研报"`、`"{股票名称} 财务数据"`
2. **web_crawl** 抓取东方财富个股页、新浪财经个股页等公开页面
3. 提取关键信息补充到报告中
