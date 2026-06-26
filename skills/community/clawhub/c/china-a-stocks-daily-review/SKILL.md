---
name: china-stocks-daily-review
version: "2.0.0"
author: "china-stocks-daily-review"
description: >
  A股市场行情分析 Skill，支持生成三类报告：盘前市场综述、盘中市场简评、盘后复盘报告。
  China A-Share Market Daily Review Skill — generates 3 report types: Pre-Market Briefing, Intraday Snapshot, Post-Market Review.

  【触发词 · Trigger Words】开盘前分析、盘前综述、早盘预判、今天关注什么、盘中异动、午间复盘、
  收盘复盘、今日行情怎么样、市场情绪、板块轮动、主线在哪、今天主线、连板梯队、
  涨停分析、北向资金、南向资金、资金动向、成交额、全天行情、A股今日、复盘报告、
  今日市场、行情综述、开盘情绪、涨跌停统计、市场概况、明日策略、今日策略。
  Pre-market analysis, intraday alert, post-market recap, market sentiment, sector rotation, limit-up ladder,
  northbound/southbound flow, turnover, A-share today, daily review, tomorrow's strategy.

  【数据架构 · Data Architecture】三层工具降级体系：Tushare Pro 官方 API（第一优先）→
  AKShare 开源库（第二优先）→ 搜索引擎实时抓取（兜底）。每个数据项独立降级，数据缺失留空不臆想。
  3-tier fallback: Tushare Pro API (primary) → AKShare (secondary) → Search Engine (final fallback).
  Each data item degrades independently; missing data is left blank, never fabricated.

  【不适用场景 · Out of Scope】个股深度分析、宏观政策专项解读、选股推荐、龙虎榜席位分析、期权策略。
  In-depth individual stock analysis, macro policy interpretation, stock picking, top-list broker analysis, options strategies.
---

# A股市场行情分析 / China A-Share Market Daily Review

---

## 适用边界 / Use Cases

**使用本技能的情形：**

- 用户询问今日/近期 A 股、港股、美股整体行情或综述
- 涉及市场情绪、风险偏好、板块轮动、热点主题
- 涉及资金动向（北向资金净额、主力净流入、融资融券）
- 涉及涨跌停统计、大宗交易
- 生成开盘前准备材料、盘中快评、收盘复盘报告

**不使用本技能的情形：**

- 聚焦某只具体个股的深度分析
- 聚焦宏观政策、财政货币政策解读
- 要求具体买卖建议或选股推荐
- 龙虎榜席位解读（使用"龙虎榜席位风格"技能）
- 北向资金行为深度分析（使用"北向资金行为"技能）

---

## 取数工具说明 / Data Source Tools

本技能使用三层工具取数，按优先级依次降级：
This Skill uses a 3-tier data sourcing system with priority-based fallback:

**数据回退优先级 / Data Fallback Priority**：

```
工具 A：Tushare Pro 官方 API（用户自有 token，第一优先）
  ├─→ Token 未配置 / 无效 / 网络不通
  │     └─→ 工具 A2：AKShare（免费开源库，第二优先）
  ├─→ 返回空数据 / 今日无数据
  │     └─→ 工具 A2：AKShare
  │           ├─→ 成功：使用 AKShare 数据继续
  │           └─→ 失败 / 空数据
  │                 └─→ 工具 B：搜索引擎（第三优先，兜底）
  ├─→ 接口报错（超时/服务异常）
  │     └─→ 工具 A2：AKShare → 若仍失败 → 工具 B：搜索引擎
  └─→ 接口 40203 权限不足（积分不够）
        ├─→ index_daily 权限不足：改用 daily 拉全市场数据统计上涨/下跌/成交额
        ├─→ limit_list_ths 权限不足：
        │     └─→ 工具 A2：stock_zt_pool_em（有连板数）→ 失败 → 工具 B 搜索连板梯队
        ├─→ moneyflow_hsgt / moneyflow_ind_ths 权限不足：
        │     └─→ 工具 A2 对应接口 → 失败 → 工具 B 搜索
        └─→ 以上所有接口均不可用：全部降级工具 B，以搜索结果为主数据源
```

**核心原则**：每个数据项独立降级，不因某一项失败而放弃整个报告。数据缺失时该项留空，不臆想填充。

---

### 工具 A / Tool A：Tushare Pro 官方接口（第一优先） / Tushare Pro API (Primary)

直接调用官方 `http://api.tushare.pro` 接口，需用户自己的 token。

---

#### 📋 首次使用：Token 配置向导

**每次运行前先执行以下检查脚本**，若 token 未配置或无效则引导用户注册：

```python
import urllib.request, json, os, re
from collections import Counter
from pathlib import Path

# ── Step 1：读取 Token ────────────────────────────────────────
TOKEN_FILE = Path.home() / '.tushare_token'   # 存储路径：~/. tushare_token

def load_token():
    """从本地文件读取 token，未配置返回 None"""
    if TOKEN_FILE.exists():
        t = TOKEN_FILE.read_text(encoding='utf-8').strip()
        return t if t else None
    return None

def save_token(token: str):
    TOKEN_FILE.write_text(token.strip(), encoding='utf-8')
    print(f'✅ Token 已保存至 {TOKEN_FILE}')

# ── Step 2：网络连通性检查 ────────────────────────────────────
def check_network() -> bool:
    """检查能否访问 Tushare API 服务器"""
    try:
        urllib.request.urlopen('http://api.tushare.pro', timeout=5)
        return True
    except Exception as e:
        err = str(e)
        if '400' in err or '403' in err or '401' in err:
            return True   # 服务器可达（拒绝是正常响应）
        return False

# ── Step 3：Token 有效性验证 ──────────────────────────────────
def verify_token(token: str) -> tuple[bool, str]:
    """
    用 daily 接口（积分要求最低）验证 token 是否有效。
    注意：不用 trade_cal，该接口同样需要积分，低积分账号会返回 40203 误判为无效。
    返回 (is_valid, message)
    """
    try:
        body = json.dumps({
            'api_name': 'daily',
            'token': token,
            'params': {'ts_code': '000001.SZ', 'start_date': '20240101', 'end_date': '20240103'},
            'fields': 'trade_date,close'
        }).encode()
        req = urllib.request.Request(
            'http://api.tushare.pro',
            data=body,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
        code = result.get('code', -1)
        msg  = result.get('msg', '')
        if code == 0:
            return True, 'Token 验证通过'
        elif 'token' in msg.lower() or 'auth' in msg.lower() or code in (-1001, -2001):
            return False, f'Token 无效：{msg}'
        else:
            # 40203 等积分不足：说明 token 本身有效，只是部分接口受限，继续使用
            return True, f'Token 有效（积分受限，仅部分接口可用，msg={msg}）'
    except Exception as e:
        return False, f'网络请求失败：{e}'

# ── Step 4：启动检查入口 ──────────────────────────────────────
def startup_check() -> str | None:
    """
    执行网络 + token 完整检查。
    返回有效 token；若无法获取，返回 None（触发降级至工具 A2/B）。
    """
    # 4-1 网络检查
    if not check_network():
        print('⚠️  无法连接 Tushare 服务器（api.tushare.pro）')
        print('    请检查网络连接，或确认防火墙未拦截该域名。')
        print('    → 自动降级至 AKShare（工具 A2）')
        return None

    # 4-2 读取已保存的 token
    token = load_token()

    if token is None:
        # 首次使用，引导注册
        print('=' * 50)
        print('🔑 未检测到 Tushare Token，需要完成以下配置：')
        print()
        print('  第一步：免费注册 Tushare Pro 账号')
        print('    👉 注册地址：https://tushare.pro/register?reg=666')
        print('    （注册后即获赠基础积分，无需付费）')
        print()
        print('  第二步：登录后获取 Token')
        print('    👉 Token 页面：https://tushare.pro/user/token')
        print()
        print('  第三步：将 Token 粘贴到下方并回车：')
        print('=' * 50)
        # 非交互式环境下直接降级
        print('⚠️  当前为自动化运行环境，无法交互输入 Token。')
        print('    请先在终端运行以下命令保存 Token，再重新执行报告生成：')
        print()
        print("    python -c \"from pathlib import Path; Path.home().joinpath('.tushare_token').write_text('YOUR_TOKEN_HERE')\"")
        print()
        print('    → 本次自动降级至 AKShare（工具 A2）')
        return None

    # 4-3 验证 token 有效性
    valid, msg = verify_token(token)
    if not valid:
        print(f'⚠️  Token 验证失败：{msg}')
        print(f'    Token 文件位置：{TOKEN_FILE}')
        print('    请检查 Token 是否正确，或前往 https://tushare.pro/user/token 重新获取。')
        print('    → 自动降级至 AKShare（工具 A2）')
        return None

    print(f'✅ Tushare Pro 连接正常（{msg}）')
    return token

# ── Step 5：正式调用封装 ──────────────────────────────────────
TOKEN = startup_check()   # 每次脚本开头执行，获取有效 token

def fetch(api_name: str, params: dict, fields: str = '') -> dict | None:
    """
    调用 Tushare Pro 官方接口。
    成功返回 {'fields':[...], 'items':[[...]]}；失败/空数据返回 None（触发降级）。
    """
    if not TOKEN:
        return None   # token 不可用，直接跳过，让调用方降级
    try:
        body = json.dumps({
            'api_name': api_name,
            'token': TOKEN,
            'params': params,
            'fields': fields
        }).encode()
        req = urllib.request.Request(
            'http://api.tushare.pro',
            data=body,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            result = json.loads(r.read())
        if result.get('code') == 0 and result.get('data', {}).get('items'):
            return result['data']   # {'fields':[...], 'items':[[...]]}
        return None   # 空数据或错误，触发降级
    except Exception:
        return None   # 任何异常触发降级

# 使用示例：
# data = fetch('index_daily', {'ts_code': '000001.SH', 'trade_date': '20260325'})
# if data:
#     item = dict(zip(data['fields'], data['items'][0]))
# else:
#     # → 降级至工具 A2（AKShare）
```

> **Token 安全说明**：token 仅存储在本地 `~/.tushare_token` 文件中，不上传至任何云端，不写入 SKILL.md 或代码仓库。

**核心接口速查（已实测有效，fetch() 返回 data dict 或 None）：**

```python
from datetime import datetime
trade_date = datetime.now().strftime('%Y%m%d')   # 动态当日日期，如 '20260325'
```

#### 1. 指数日线 `index_daily`

```python
# ⚠️ ts_code 必须逐个查询，不支持逗号分隔多个
index_results = {}
for code, label in [('000001.SH','上证'),('399001.SZ','深证'),
                    ('399006.SZ','创业板'),('000688.SH','科创50')]:
    data = fetch('index_daily', {'ts_code': code, 'trade_date': trade_date})
    if data:
        item = dict(zip(data['fields'], data['items'][0]))
        # 字段：ts_code, trade_date, close, open, high, low, pre_close,
        #        change, pct_chg, vol, amount
        # ⚠️ vol 单位为手；amount 单位为千元，转亿元需 /1e5
        index_results[label] = {
            'close': item['close'],
            'pct':   item['pct_chg'],       # 百分比数值，如 1.78
            'vol':   item['vol'],            # 成交量（手）
            'amt':   item['amount'] / 1e5   # 成交额（亿元）
        }
    # else: → 降级至工具 A2
```

#### 2. 涨跌停池 `limit_list_ths`

```python
data = fetch('limit_list_ths', {'trade_date': trade_date})
if data:
    items = data['items']
    # 字段（按索引）：
    # [0]trade_date [1]ts_code [2]name [3]price [4]pct_chg [5]open_num
    # [6]lu_desc(题材) [7]limit_type(涨停池/跌停池) [8]tag(连板描述)
    # [9]status(换手板/一字板) [10]limit_order [11]limit_amount
    # [12]turnover_rate [13]free_float [14]lu_limit_order(无效,全为None)
    # [15]limit_up_suc_rate [16]turnover [17]market_type

    zt = [x for x in items if '涨停' in str(x[7])]  # 涨停池
    dt = [x for x in items if '跌停' in str(x[7])]  # 跌停池

    # ⚠️ 连板天数：从 tag 字段（index 8）解析，lu_limit_order(index 14)全为None不可用
    # tag 格式示例：'首板', '2天2板', '5天3板', '10天9板'
    def parse_lianban(tag):
        m = re.search(r'(\d+)天(\d+)板', str(tag))
        return int(m.group(2)) if m else 1

    results = [(x[2], parse_lianban(x[8]), x[8], x[6], x[9]) for x in zt]
    # (名称, 连板天数, tag原文, 题材描述, 状态)
    results.sort(key=lambda x: -x[1])
    lianban_2plus = [r for r in results if r[1] >= 2]

    # 题材热度统计（涨停题材出现频次）
    tags_all = []
    for x in zt:
        if x[6]: tags_all.extend(str(x[6]).replace('，','+').split('+'))
    tag_cnt = Counter(tags_all).most_common(10)
# else: → 降级至工具 A2
```

#### 3. 北向资金 `moneyflow_hsgt`

```python
data = fetch('moneyflow_hsgt', {'trade_date': trade_date})
if data:
    item = dict(zip(data['fields'], data['items'][0]))
    # 字段：trade_date, ggt_ss(沪股通净流入,亿), ggt_sz(深股通净流入,亿),
    #        hgt, sgt, north_money(北上合计,亿), south_money(南下合计,亿)
    # ⚠️ north_money 单位已是亿元，直接用
    north = item['north_money']   # 北上净流入（亿元，正=流入，负=流出）
    sh    = item['ggt_ss']        # 沪股通
    sz    = item['ggt_sz']        # 深股通
# else: → 降级至工具 A2
```

#### 4. 板块资金流 + 涨幅 `moneyflow_ind_ths`

```python
data = fetch('moneyflow_ind_ths', {'trade_date': trade_date})
if data:
    items  = data['items']
    fields = data['fields']
    # 字段：trade_date, ts_code, industry, lead_stock(龙头股),
    #        close, pct_change(涨跌幅%), company_num, pct_change_stock,
    #        close_price, net_buy_amount, net_sell_amount, net_amount(净流入,元)

    # ⚠️ 按涨幅排序（不是按资金流）
    pct_idx  = fields.index('pct_change')
    name_idx = fields.index('industry')
    net_idx  = fields.index('net_amount')

    sorted_by_pct = sorted(items, key=lambda x: (x[pct_idx] or 0), reverse=True)
    top5_up   = sorted_by_pct[:5]    # 领涨 TOP5
    top5_down = sorted_by_pct[-5:]   # 领跌 TOP5（或涨幅最小）
# else: → 降级至工具 A2
```

#### 5. 大宗交易 `block_trade`

```python
data = fetch('block_trade', {'trade_date': trade_date})
if data:
    count = len(data['items'])
    # 字段：ts_code, price, vol, amount, buyer, seller, ...
    # 统计笔数即可
# else: → 搜索引擎补充（工具 B）
```

---

### 工具 A2 / Tool A2：AKShare 结构化数据（第二优先，Tushare 失败时降级） / AKShare (Fallback)

当工具 A 返回空数据或报错时，立即尝试 AKShare 获取同类数据。AKShare 为免费开源 Python 库，数据实时性略低于 Tushare，但覆盖范围全。

**环境要求**：`pip install akshare`（已安装则直接 import）

**核心接口对照（与工具 A 一一对应）：**

```python
import akshare as ak
from datetime import datetime, timedelta

today = datetime.now().strftime("%Y%m%d")         # 20260325
today_dash = datetime.now().strftime("%Y-%m-%d")  # 2026-03-25
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

# ── A2-1. 指数行情（替代 index_daily）──────────────────────
df_idx = ak.stock_zh_index_spot_em()
# 过滤所需指数
idx_map = {'上证综指':'000001','深证成指':'399001','创业板指':'399006','科创50':'000688'}
for name, code in idx_map.items():
    row = df_idx[df_idx['代码'] == code]
    if not row.empty:
        close = row['最新价'].values[0]
        pct   = row['涨跌幅'].values[0]     # 已是百分比，如 1.78
        amt   = row['成交额'].values[0]      # 单位：元，转亿需 /1e8
        vol   = row['成交量'].values[0]      # 单位：手

# ── A2-2. 涨跌停统计（替代 limit_list_ths）────────────────
df_zt  = ak.stock_zt_pool_em(date=today)         # 涨停池（含连板数字段）
df_dt  = ak.stock_zt_pool_dtgc_em(date=today)    # 跌停池
df_zb  = ak.stock_zt_pool_zbgc_em(date=today)    # 炸板池
# df_zt 含字段：代码, 名称, 涨跌幅, 最新价, 成交额, 流通市值, 总市值,
#               换手率, 封板资金, 首次封板时间, 最后封板时间, 炸板次数,
#               涨停统计, 所属行业, 连板数
# ⚠️ 连板天数：直接读 df_zt['连板数'] 列，无需额外解析

# ── A2-3. 北向资金（替代 moneyflow_hsgt）──────────────────
# ⚠️ 注意：stock_hsgt_north_net_flow_in_em 已失效，改用下方接口
df_hsgt = ak.stock_hsgt_fund_flow_summary_em()
# 过滤北向（沪港通+深港通），取今日最新行
import datetime
today_str = datetime.date.today().strftime('%Y-%m-%d')
df_north = df_hsgt[df_hsgt['交易时间'] == today_str]
# ⚠️ "资金净流入"字段收盘当日可能为0（结算滞后），建议用次日数据或搜索引擎补充

# ── A2-4. 行业板块涨跌（替代 moneyflow_ind_ths）───────────
df_ind = ak.stock_sector_fund_flow_rank(symbol="今日", indicator="行业资金流向")
# 含字段：序号, 名称, 今日涨跌幅, 今日主力净流入-净额, 今日主力净流入-净占比 ...
# ⚠️ 按"今日涨跌幅"排序（不是按资金流）
df_ind_sorted = df_ind.sort_values('今日涨跌幅', ascending=False)
top5_up   = df_ind_sorted.head(5)
top5_down = df_ind_sorted.tail(5)

# ── A2-5. 大宗交易（替代 block_trade）─────────────────────
df_blk = ak.stock_dzjy_mrmx(type_="买入", date=today)
count = len(df_blk)

# ── A2-6. 指数历史数据（BaoStock 备用，仅在 AKShare 也失败时）
# import baostock as bs
# lg = bs.login()
# rs = bs.query_history_k_data_plus("sh.000001",
#     "date,close,pctChg,volume,amount",
#     start_date=today_dash, end_date=today_dash,
#     frequency="d", adjustflag="3")
# df_bs = rs.get_data()
# bs.logout()
# ⚠️ BaoStock: volume 单位为股（÷100=手），amount 单位为元（÷1e8=亿）
```

**工具 A2 注意事项：**
- `stock_zh_index_spot_em` 的成交额单位为**元**，转亿元需 `/1e8`（不同于 Tushare 的千元/1e5）
- `stock_zt_pool_em` 的连板天数直接读 `连板数` 列，无需解析字符串
- AKShare 行业板块排名用 `今日涨跌幅` 字段排序
- 若 AKShare 也抛异常，直接进入工具 B（搜索引擎）

---

### 工具 A2-新闻 / Tool A2-News：财联社快讯（新增信息源） / CLS News Feed

**接口**：`ak.stock_info_global_cls(symbol='全部')`

- 返回最新 20 条财联社快讯，字段：`标题`（通常为空）、`内容`（实际内容在此）、`发布日期`（`datetime.date` 对象）、`发布时间`
- 用途：盘前关注事件、盘中热点催化、盘后收盘原因分析
- ⚠️ 注意：`标题` 列经常为空，内容全在 `内容` 字段；过滤今日数据需比较 `datetime.date` 对象，不能用字符串

```python
import akshare as ak
import datetime

df_cls = ak.stock_info_global_cls(symbol='全部')
today = datetime.date.today()
df_today = df_cls[df_cls['发布日期'] == today]
# 按时间倒序，取内容非空的条目
news_items = []
for _, row in df_today.iterrows():
    content = str(row.get('内容', ''))
    if content and content != 'nan':
        news_items.append(f"[{row['发布时间']}] {content}")
# news_items 即为今日财联社快讯列表
```

**在报告中的用途：**
- 盘前：补充「今日关注」板块的重大事件（政策、外盘、公司公告）
- 盘中：解释板块异动催化剂
- 盘后：补充收盘后的快讯（业绩预告、政策落地等）

---

### 工具 A2-新闻 / Tool A2-News：Tushare 新闻快讯（补充，积分依赖） / Tushare News (Supplementary)

**接口**：`news`（需要 Tushare 积分）

- 参数：`src`（新闻来源：`sina`/`wallstreetcn`/`eastmoney`/`yuncaijing`/`finet`/`10jqka`）
- 字段：`datetime`、`title`、`content`、`channels`
- 当前账号积分限制：接口返回 0 条（积分不足）→ 降级至财联社快讯或搜索引擎

---

### 工具 B / Tool B：web-tools MCP 实时数据（第三优先，兜底） / web-tools MCP (Final Fallback)

**前置条件**：本层依赖 WorkBuddy MCP 服务 `web-tools`（自动注册于 `~/.workbuddy/mcp.json`，无需用户配置）。web-tools 包含两个工具：
- **web_search**：搜索引擎发现来源，支持 Bing API（进阶，<200ms）和 googlesearch-python（基础，~5s，自动降级）
- **web_fetch**：逐个 URL 抓取并提取结构化数据，自动处理编码，优先返回 markdown

**触发条件（满足任一即启用）**：
1. 工具 A（Tushare）+ 工具 A2（AKShare）均返回空或报错
2. 需要补充当日重要新闻、政策背景（财联社快讯不够详细时）
3. 需要对板块异动/个股事件给出**原因解读**（工具 A/A2 均无原因字段）
4. 数字类数据来自工具 A/A2，但需要**交叉验证**准确性

**搜索数据可替代范围**：
- 实时指数点位、涨跌幅、成交额
- 实时涨停/跌停家数
- 实时北向资金流向
- 板块涨幅排名
- 市场热点与异动原因

**标准操作流程（三步走）**：

```
Step 1：web_search → 找到数据来源 URL（标准化关键词，见下方）
Step 2：web_fetch → 逐个 URL 提取结构化数据
Step 3：多源交叉验证 → 取一致性高的数据写入报告
```

**Step 1：标准化搜索关键词（按数据项精选，主搜+备搜）**：

| 数据项 | 主搜关键词 | 备搜关键词 | 推荐来源 |
|-------|----------|----------|---------|
| 指数行情+成交额 | `上证指数 深证成指 创业板 收盘 {日期}` | `沪深两市 今日收盘 涨跌幅` | 雪球、同花顺 |
| 涨停家数+情绪 | `A股 今日 涨停 跌停 家数 {日期}` | `涨停家数 跌停家数 市场情绪` | 东方财富快讯 |
| 北向资金 | `沪深股通 北向资金 净流入 {日期}` | `北上资金 今日净买入` | 雪球、东方财富 |
| 板块涨幅排名 | `今日行业板块 涨幅排名 {日期}` | `A股 行业涨幅 领涨板块` | 同花顺、东方财富 |
| 连板梯队 | `A股 涨停 连板梯队 {日期}` | `涨停板 连板数 龙头股` | 雪球、同花顺 |
| 港股/美股外盘 | `美股 道琼斯 纳斯达克 收盘 {日期}` | `中概股 纳斯达克中国金龙指数` | Bing INT |
| A50期指 | `A50期指 收盘 {日期}` | `富时中国A50 期货` | Bing INT |

**Step 2：web_fetch 提取策略**：

搜索拿到 URL 后，按优先级逐个 fetch：
- 优先 fetch **结构化页面**（雪球快讯、同花顺收盘快讯、东方财富行情页）
- 每个 URL fetch 后，从 markdown 中提取关键数字（点位、涨跌幅、金额、家数）
- **不盲目抓取**：先 fetch 搜索结果列表中的前 3 个 URL，视数据充足程度决定是否继续

**Step 3：交叉验证规则**：

```
至少 2 个来源数据一致 → 写入报告（注明"据[来源]，[来源]"）
仅有 1 个来源有数据   → 写入报告（注明"据[来源]"）
多个来源数据矛盾     → 取中间值或保守值，注明"多源数据有差异"
无任何来源           → 该项留空，不臆想填充
```

**web-tools MCP 调用示例**：

```python
# Step 1：搜索指数数据（主搜 + 备搜，合并结果）
search_results = web_search("上证指数 深证成指 创业板 收盘 2026-04-08")
# 返回格式：[{"title": "...", "url": "https://...", "snippet": "..."}]

# Step 2：fetch 前2个最相关 URL
fetched = []
for r in search_results[:2]:
    content = web_fetch(r["url"], "提取：上证指数点位/涨跌幅、深证成指点位/涨跌幅、成交额（亿元）")
    if content:
        fetched.append({"source": r["title"], "url": r["url"], "content": content})

# Step 3：AI 从 fetched 内容中解析结构化数字，交叉验证后写入报告
```

**mcp.json 注册状态**（本工具 B 层已自动可用）：
`web-tools` MCP 服务已在 `~/.workbuddy/mcp.json` 注册，skill 执行时会自动调用，无需额外安装或配置。

---

### 工具 B2 / Tool B2：搜索引擎冗余回退（web-tools MCP 不可用时的兜底） / Search Engine Fallback

若 `web-tools` MCP 服务因故不可用，降级为手动搜索，直接访问以下来源页面：

| 优先级 | 场景 | 引擎 | URL 模板 |
|-------|-----|-----|---------|
| 1 | A股当日资讯、复盘 | Bing CN | `https://cn.bing.com/search?q={关键词}&ensearch=0&tbs=qdr:d` |
| 2 | 市场热点/板块异动原因 | 东方财富 | `https://so.eastmoney.com/web/s?keyword={关键词}` |
| 3 | 市场情绪/热搜事件 | 腾讯财经 | `https://new.qq.com/search?query={关键词}` |
| 4 | 盘后个股/板块复盘 | 新浪财经 | `https://search.sina.com.cn/?q={关键词}&range=all&c=news` |
| 5 | 同花顺资讯 | 同花顺 | `https://news.10jqka.com.cn/search/?key={关键词}` |
| 6 | 港股/美股/隔夜外盘 | Bing INT | `https://cn.bing.com/search?q={关键词}&ensearch=1&tbs=qdr:d` |
| 7 | 备用 | DuckDuckGo | `https://duckduckgo.com/html/?q={关键词}` |

**BaoStock 冗余说明**：

BaoStock 为免费 Python 库（`import baostock as bs`），可作为指数历史数据的备用源。若 Tushare 指数日线数据为空，可尝试：

```python
import baostock as bs, pandas as pd
lg = bs.login()
rs = bs.query_history_k_data_plus("sh.000001",
    "date,close,pctChg,volume,amount",
    start_date="2026-03-24", end_date="2026-03-24",
    frequency="d", adjustflag="3")
df = rs.get_data()
bs.logout()
# 注意：volume 单位为股，amount 单位为元
```

**调用原则：**
- **优先结构化数据**：工具 A / A2 能拿到的数字类数据，不用搜索引擎
- **搜索补充原因**：板块异动原因、事件背景、政策解读，必须走工具 B
- **不限制引擎数量**：为获取完整实时数据，可同时调用 2-3 个引擎
- **数据冲突处理**：数字以工具 A/A2 为准，原因分析以搜索为准

## 报告生成：三层漏斗模型 / Report Generation: 3-Tier Funnel

复盘报告的生成过程由三层架构驱动，每层有明确的输入、处理逻辑和输出产物。三层顺序执行，上层输出是下层输入。

---

### 第一层：数据获取层 / Tier 1: Data Acquisition

**原则**：优先权威结构化数据，辅以非结构化资讯。数据按重要性分四级顺序获取：

优先级 1（核心，必须完整）
指数收盘价、涨跌幅、成交额、成交量、涨跌家数、涨停/跌停统计、南北向资金净流入/流出。
来源：工具 A（Tushare）→ 工具 A2（AKShare）→ 工具 B（web-tools MCP）。


优先级 2（重要，尽力获取）
板块异动原因、宏观政策、公司公告、机构观点。
来源：财联社快讯（stock_info_global_cls）→ 工具 B（web-tools MCP）。


优先级 3（辅助，选择性获取）
市场情绪指标、热点事件（如"算力爆发"、词元概念）。
来源：涨停池聚类结果、财联社快讯、Bing CN 搜索。

优先级 4（补充，时间允许时获取）
海外市场信息、实时滚动新闻。
来源：Bing INT（港股/美股/外盘）。

---

### 第二层：逻辑清洗与筛选层 / Tier 2: Data Cleaning & Filtering

**原则**：从海量数据中提炼"信号"，过滤"噪音"。按以下 5 步执行：

Step 1 异常值剔除
剔除 ST 股、停牌股、数据异常值（如成交量=0的涨停，标记为"无效涨停"，不计入连板梯队）。

Step 2 主线识别（聚类分析）
将涨停股按所属板块归类，统计涨停家数最多的前 3 个板块，作为今日主线排序依据。
输出格式：主线1（N家涨停）> 主线2（N家）> 主线3（N家）。

Step 3 资金归因（关联分析）
将资金净流入最大的板块，与财联社快讯/搜索结果中的政策事件关联，给出驱动因子归类：
政策催化 / 业绩催化 / 资金追涨 / 外部联动 / 情绪扩散。

Step 4 情绪量化
计算以下指标并给出评级：
涨跌比 = 上涨家数 / 下跌家数（>3 为偏热，>5 为亢奋）
连板高度 = 当日最高连板数（>=6板 为亢奋信号）
炸板率 = 炸板数 / (涨停+炸板) × 100%（>20% 为情绪转弱信号）
情绪评级：亢奋 / 偏热 / 正常 / 偏冷 / 低迷。

Step 5 风险识别（反向排除）
找出跌幅榜前 3 板块、跌停家数突增板块，标记"风险警示"写入风险提示区。

---

### 第三层：结构化叙事层 / Tier 3: Structured Narrative

**原则**：将清洗后的数据转化为可阅读的叙事，遵循"结论先行 + 数据支撑 + 逻辑推演"框架。

三类报告的核心差异：
- 盘前报告：预测与推演（基于隔夜数据 + 公告 + 预期）。核心是"今天要盯着什么看"。核心逻辑：外盘映射 → 超预期事件筛选 → 关键点位技术研判 → 剧本推演（高开/低开应对策略）
- 盘中报告：验证与修正（基于上午实际走势）。核心是"昨天的预测准不准？主线变没变？"核心逻辑：预判对比验证 → 主线延续性判断（是否电风扇？）→ 情绪周期位置 → 下午策略修正
- 盘后报告：复盘与总结（基于全天完整数据）。核心是"今日发生了什么、为什么、明天怎么看"。核心逻辑：主线聚类 → 驱动因子归因 → 情绪评级 → 策略展望

报告结构（盘前版，硬编码）：
标题行 — 核心主题（一句话概括今日关注方向）
隔夜外盘映射 — 美股/中概/A50期指/汇率 + 开盘情绪预判
核心消息面 — 政策利好/个股公告/风险预警（超预期事件优先，剔除已消化利好）
技术面关键点位 — 支撑/压力位 + 量能要求
今日策略 — 最强主线预判 + 风向标标的 + 风控预案（高开/低开/放量 三种剧本）

报告结构（盘中版，硬编码）：
标题行 — 一句话总结上午走势
上午数据 — 指数/成交额/涨跌比（与盘前预期对比：符合/超预期/不及）
主线验证 — 领涨板块 + 主线延续性判断（有无电风扇切换）
连板情绪 — 最高连板高度变化（与昨日/上午对比）+ 炸板率
下午推演 — 强弱判断 + 进攻/风险预警 + 核心观察点

报告结构（盘后版，硬编码）：
标题行 — 核心结论（如"算力爆发 + 电力共振"），一句话定性今日行情
指数表现 — 收盘价、涨跌幅、成交额逐行列出
资金动向 — 北向/南向净流入规模+方向
主线复盘 — 按主线强度排序，每条主线：龙头股 + 涨停家数 + 驱动因子
情绪指标 — 连板高度、涨停/跌停家数、炸板率、情绪评级
明日策略 — 进攻方向 + 防守方向 + 关键观察点
小结 — 一句话总结 + 风险提示

---

## 第一步：识别报告类型 / Step 1: Identify Report Type

根据用户输入判断报告类型，若未明确指定则依当前时间自动判断：

| 报告类型 | 触发词 | 自动判断时间 |
|---------|-------|------------|
| **盘前市场综述** | 开盘前、盘前、早盘预判、今天关注什么 | 8:00–9:25 |
| **盘中市场简评** | 盘中、现在市场、午盘、异动 | 9:30–15:00 |
| **盘后复盘报告** | 收盘、今日复盘、盘后、今天表现 | 15:00 后 |

---

## 第二步：取数执行 / Step 2: Data Acquisition

### 盘前取数清单 / Pre-Market Data Checklist

优先级顺序：优先级1（核心）→ 优先级2（消息面）→ 优先级3（情绪辅助）→ 优先级4（外盘补充）

| 优先级 | 数据项 | 工具 A（Tushare） | 工具 A2（AKShare降级） | 工具 B（web-tools MCP） |
|-------|-------|----------------|---------------------|-----------------------|
| P1 | 昨日主要指数收盘 | `index_daily`（逐个查） | `stock_zh_index_spot_em` | web_search + fetch（雪球/同花顺） |
| P1 | 昨日涨跌停数量+连板 | `limit_list_ths` | `stock_zt_pool_em` / `dtgc` / `zbgc` | web_search + fetch |
| P1 | 昨日北向/南向资金 | `moneyflow_hsgt` | `stock_hsgt_fund_flow_summary_em` | web_search + fetch（雪球/东财） |
| P2 | 晚间公告/政策/事件（超预期优先） | — | `stock_info_global_cls`（财联社快讯，今晚条目） | web_search + fetch（东方财富/Bing CN） |
| P2 | 重大个股公告（业绩/重组/减持/解禁） | — | — | web_search + fetch（搜索"股票公告 今晚"） |
| P3 | 昨日主线情绪延续性（连板高度变化） | `limit_list_ths` | `stock_zt_pool_em` | — |
| P4 | 隔夜美股三大指数、中概股 | — | — | web_search + fetch（Bing INT） |
| P4 | A50期指、人民币汇率 | — | — | web_search + fetch（Bing INT） |

取数重点说明：
- P2 消息面筛选原则：只选"超预期"事件，剔除已消化的利好（如反复提及的政策、已发布多日的公告）
- P4 隔夜外盘：时间允许时获取；若无则盘前报告外盘部分用"数据暂缺"标注，不臆想

### 盘中取数清单 / Intraday Data Checklist

优先级顺序与盘前相同，但数据均来自实时当日；额外增加"预判验证"维度

| 优先级 | 数据项 | 工具 A（Tushare） | 工具 A2（AKShare降级） | 工具 B（web-tools MCP） |
|-------|-------|----------------|---------------------|-----------------------|
| P1 | 当前指数实时涨跌+成交额 | `index_daily`（今日） | `stock_zh_index_spot_em` | web_search + fetch |
| P1 | 实时涨跌停数量+炸板 | `limit_list_ths`（今日） | `stock_zt_pool_em` / `zbgc` | web_search + fetch |
| P1 | 上涨/下跌家数（涨跌比计算） | `daily`（全市场统计） | — | web_search + fetch |
| P1 | 实时北向/南向资金 | `moneyflow_hsgt`（今日） | `stock_hsgt_fund_flow_summary_em` | web_search + fetch |
| P2 | 行业板块涨幅 TOP5 + 领跌 | `moneyflow_ind_ths`（今日） | `stock_sector_fund_flow_rank(sector_type='行业资金流')` | web_search + fetch |
| P2 | 盘中快讯/异动催化原因 | `news`（积分受限时降级） | `stock_info_global_cls`（财联社快讯） | web_search + fetch（东方财富/Bing CN） |
| P3 | 连板高度变化（与上午/昨日对比） | `limit_list_ths` | `stock_zt_pool_em` | — |

### 盘后取数清单 / Post-Market Data Checklist

| 数据项 | 工具 A（Tushare） | 工具 A2（AKShare降级） | 工具 B（web-tools MCP） | 字段说明 |
|-------|----------------|---------------------|-----------------------|---------|
| 今日各指数收盘 | `index_daily`（逐个查） | `stock_zh_index_spot_em` | web_search + fetch（雪球/同花顺） | A: amount/1e5=亿；A2: 成交额/1e8=亿 |
| 今日涨跌停/炸板/连板 | `limit_list_ths` → 失败用`daily`统计涨停家数（无连板） | `stock_zt_pool_em` 等（含连板数列） | web_search + fetch | A: tag解析连板；A2: 连板数列直接读；daily降级：只有涨停家数，无连板明细 |
| 今日北向/南向资金 | `moneyflow_hsgt` | `stock_hsgt_fund_flow_summary_em`（北向+南向） | web_search + fetch（雪球/东财） | 使用 `成交净买额` 字段（亿元）；`资金净流入` 为额度余额不可用；北向收盘当日结算滞后显示0则不写 |
| 行业板块涨跌幅 | `moneyflow_ind_ths` | `stock_sector_fund_flow_rank(sector_type='行业资金流')` | web_search + fetch | 均按涨幅排序，不按资金流 |
| 大宗交易笔数 | `block_trade` | `stock_dzjy_mrmx` | — | 统计条数即可 |
| 收盘后快讯/公告 | `news`（积分受限时降级） | `stock_info_global_cls`（财联社快讯，15:00后条目） | web_search + fetch（东方财富/Bing CN） | 用于补充收盘后重大公告、业绩快报 |
| 板块异动原因 | — | `stock_info_global_cls`（财联社快讯中搜关键词） | web_search + fetch（东方财富/Bing CN） | 工具A/A2均无原因字段，优先快讯再搜索 |

---

## 第三步：撰写报告 / Step 3: Report Writing

### 成交量与成交额区分说明（报告写作规范） / Volume vs. Turnover Distinction (Writing Standard)

> - **成交量**（手/股）：反映成交频次，与股价无关，同一资金规模下高价股成交量小
> - **成交额**（亿元）：= 成交量 × 价格，反映实际资金流动规模，是市场活跃度的核心指标
> - 报告中需**同时列出**成交量和成交额，不可混用

### 盘前市场综述模板 / Pre-Market Briefing Template

⚠️ 输出格式要求：为适配微信阅读，禁止使用 Markdown 表格（不出现 | 符号）、# 标题符号、** 加粗符号、- 或 * 列表符号、━ 分隔线。改用 emoji 图标、中文数字标题、空行分段。内容丰富度不减，适当加 emoji 增强可读性。

⚙️ 生成逻辑（三层漏斗盘前版）：第一层取昨日结构化数据（P1）+ 晚间消息面（P2）+ 隔夜外盘（P4）；第二层筛选：只保留"超预期"事件，剔除已消化利好，聚焦今日潜在影响板块；第三层：结论先行（核心主题）→ 外盘映射（开盘情绪定性）→ 昨日盘面回顾 → 消息面催化筛选 → 技术点位 → 剧本推演（高开/低开/放量三种应对方案）。

```
🌅 盘前市场综述 · {日期}（{星期}）
核心主题：{一句话概括今日重点，如"外盘企稳，关注新能源政策催化+昨日连板高度延续"}

🌍 一、隔夜外盘映射

美股三大指数{整体表现，如"集体收涨/收跌/涨跌互现"}：
道琼斯指数：{涨跌幅}%
标普500：{涨跌幅}%
纳斯达克：{涨跌幅}%
中概股（纳斯达克中国金龙指数）：{涨跌幅}%
A50期指：{涨跌幅}%（开盘情绪风向标）
人民币汇率：美元/人民币 {汇率}（较昨日{升/贬值}）

开盘情绪预判：{高开/低开/平开预期}，预计开盘情绪{乐观/谨慎/分化}
逻辑：{1-2句，说明外盘对A股的传导方向，如"中概涨+A50稳 → 科技/成长方向开盘偏强"}

（若外盘数据暂缺则写"隔夜外盘数据暂缺"，不臆想）

📈 二、昨日 A 股回顾

指数收盘：
上证综指：{点位}（{涨跌幅}%），成交额 {X} 亿
深证成指：{点位}（{涨跌幅}%），成交额 {X} 亿
创业板指：{点位}（{涨跌幅}%），成交额 {X} 亿
科创 50：{点位}（{涨跌幅}%），成交额 {X} 亿
沪深两市合计成交额约 {X} 亿元（较前日{增加/减少} {差值} 亿，环比{+/-}{变化幅度}%）

💰 资金动向：
北向资金：{若昨日数据结算滞后则不写；若有数据则写"净流入/流出 X亿（沪股通 X亿 / 深股通 X亿）"}
南向资金：港股通合计净买入 {X} 亿（沪港通 {X} 亿 / 深港通 {X} 亿）

情绪温度计（昨日）：
上涨 {N} 家，下跌 {N} 家（涨跌比 {上涨/下跌，保留1位小数}:1）
涨停 {N} 家 / 跌停 {N} 家 / 炸板 {N} 家（炸板率 {炸板/(涨停+炸板)×100}%）
连板高度：最高 {N} 板（{股票名}）
情绪评级：{亢奋 / 偏热 / 正常 / 偏冷 / 低迷}（{1句定性依据}）

🔥 连板梯队（昨日，2板及以上，按连板数降序，每只独立一行）：

{N}板
{股票名} — {所属行业}（{题材/催化逻辑，1句}）

{N}板
{股票名} — {所属行业}（{题材/催化逻辑，1句}）
{股票名} — {所属行业}（{题材/催化逻辑，1句}）

（2板个股较多时：先列有明确题材逻辑的，最后一行合并列出无突出题材的，格式：{名1}、{名2}、{名3} — {行业}）

🏷️ 涨停题材热度（TOP8，按频次）：
1. {题材} — {N} 家
2. {题材} — {N} 家
（以此类推）

📢 三、核心消息面梳理（仅超预期事件，已消化利好不列）

📌 政策/行业利好
{事件标题}：{简述2-3句，含受益板块+影响方向，如"设备更新新政 → 工业机械/汽车直接受益"}
（若有第二条则同格式列出；若无超预期利好则写"暂无重磅超预期政策"）

📌 个股/公司公告（超预期的）
{股票名/代码}：{事件类型，如"业绩预增300%/重大重组/定增"} — {预期判断：超预期/利空，1句逻辑}
（若无重要公告则省略此段）

⚠️ 风险预警
{风险类型}：{具体说明，如"XX股票今日解禁 X亿，关注抛压"/"某地缘事件影响大宗商品"}
（若无则省略）

📊 四、技术面关键点位

上证综指：压力位 {XXXX}，支撑位 {XXXX}（如昨日收盘价/整数关口/均线）
创业板指：压力位 {XXXX}，支撑位 {XXXX}
量能要求：今日需成交 {X} 亿以上才能支撑{上涨/突破}（依据：近期均量/前高量能）

🎯 五、今日核心策略

最强主线预判：{板块方向，如"AI算力/电力/消费"} — 逻辑：{1-2句，隔夜数据/公告/昨日连板延续}
潜在轮动方向：{如"低位补涨/消费/超跌反弹"，无则省略}

重点观察标的（2-3只，作为板块风向标）：
{股票A}：观察{XX}是否突破{XX}压力位，量能是否配合
{股票B}：观察{XX}是否抗跌，作为板块强弱风向标
{股票C}：观察{XX}是否封板，作为情绪标杆（如有则列）

剧本推演（三种开盘场景）：
若高开且放量：跟随主线，优先中军龙头，情绪偏强可适度参与
若高开但缩量：警惕诱多，避免追高，观望为主
若低开超1%：暂不操作，观察开盘后30分钟是否修复，不修复则规避当日操作

⚠️ 风险提示：{1-2条，具体说明潜在风险}

数据来源：Tushare Pro · AKShare · 财联社快讯 · 财经媒体资讯
```

### 盘中市场简评模板 / Intraday Snapshot Template

⚠️ 输出格式要求：为适配微信阅读，禁止使用 Markdown 表格（不出现 | 符号）、# 标题符号、** 加粗符号、- 或 * 列表符号、━ 分隔线。改用 emoji 图标、中文数字标题、空行分段。

⚙️ 生成逻辑（三层漏斗盘中版）：第一层取上午实时数据（P1指数/涨停/资金）+ 板块异动原因（P2）；第二层：ST剔除 → 与盘前预判对比验证（符合/偏差） → 主线延续性判断（是否电风扇快速切换） → 情绪位置（连板高度对比昨日）→ 风险识别（午后跳水迹象）；第三层：结论先行（上午一句话定性）→ 数据支撑（指数/涨停/涨跌比）→ 主线验证 → 下午剧本推演。

```
🕛 午间复盘报告 · {日期}（{星期}）{时间，如11:30}
核心主题：{一句话总结上午走势，如"两市放量上涨，电力板块持续走强，盘前预判基本验证"}

📈 一、上午盘面数据

指数表现：
上证综指：{点位}（{涨跌幅}%），上午成交额 {X} 亿（vs 盘前预期：{符合/超预期/不及}）
深证成指：{点位}（{涨跌幅}%）
创业板指：{点位}（{涨跌幅}%）
科创 50：{点位}（{涨跌幅}%）
上午合计成交额 {X} 亿（预计全天约 {X} 亿，较昨日全天{增加/减少}{差值}亿）

💰 资金动向（上午）：
北向资金：{盘中实时数据；若不可用则不写}
南向资金：港股通上午净买入 {X} 亿（若有数据；无则省略）

情绪指标（上午）：
上涨 {N} 家，下跌 {N} 家（涨跌比 {上涨/下跌，保留1位小数}:1，vs 盘前情绪预期{符合/偏强/偏弱}）
涨停 {N} 家，跌停 {N} 家，炸板 {N} 家（炸板率 {炸板/(涨停+炸板)×100}%）
连板高度：上午最高 {N} 板（{股票名}），较昨日收盘{升高/持平/回落}
情绪判断：{偏强/震荡/偏弱}（{1句依据，如"涨跌比5:1+连板高度稳，情绪良好"}）

🔥 二、主线验证与板块表现

领涨板块 TOP3（按涨幅，与昨日连板主线对照验证）：
{板块名}（+{涨幅}%）：涨停 {N} 家，龙头{股票名}。逻辑：{1-2句，延续昨日/新催化}
{板块名}（+{涨幅}%）：涨停 {N} 家，龙头{股票名}。逻辑：{1-2句}
{板块名}（+{涨幅}%）：涨停 {N} 家，龙头{股票名}。逻辑：{1-2句}

领跌板块 TOP3（按跌幅）：
{板块名}（{跌幅}%）：{核心原因，如"获利回吐/利空消息"}
{板块名}（{跌幅}%）：{原因}
{板块名}（{跌幅}%）：{原因}

主线确认：
今日最强主线：{板块名称}（依据：涨停家数最多+龙头持续封板+资金流入大）
主线稳定性：{稳定/出现电风扇切换}（{说明：若出现切换，描述从哪个板块切换到哪个，资金犹豫风险}）

⚡ 三、连板情绪与个股异动

连板梯队（2板及以上，上午快照）：
{N}板
{股票名} — {所属行业}（{午前状态：封板/炸板/未触板，1句逻辑}）

核心异动个股：
{股票A}：{异动描述，如"早盘快速涨停，10:30炸板，需关注下午是否回封"}
{股票B}：{异动描述，如"午前突发利好直线拉升，新进热点"}

🎯 四、下午策略推演

进攻方向：
若主线延续：关注{板块A}的补涨股/低位股，优先{有逻辑支撑的2板标的}
若主线切换：关注{低位板块B}是否形成首板，量能是否跟上

风险预警：
若成交量午后萎缩：警惕高位股补跌，{具体说明2-3个风险标的方向}
若指数冲高回落：避免追高，等待缩量回踩支撑再介入

关键观察点：
{观察点1，如"华电辽能下午是否维持封板，决定电力板块情绪走向"}
{观察点2，如"北向资金截至15:00是净流入还是净流出"}
{观察点3，如"午后成交额能否在前一日全天成交额基础上继续放量"}

数据来源：Tushare Pro · AKShare · 财联社快讯 · 财经媒体资讯
小龙虾备注：报告生成时间{时间}。数据基于上午收盘快照。下午策略需根据13:00开盘后15分钟走势微调。
```

### 盘后复盘报告模板 / Post-Market Review Template

⚠️ 输出格式要求：为适配微信阅读，禁止使用 Markdown 表格（不出现 | 符号）、# 标题符号、** 加粗符号、- 或 * 列表符号、━ 分隔线。改用 emoji 图标、中文数字标题、空行分段。

⚙️ 生成逻辑：遵循三层漏斗模型。第一层取数完成后，进入第二层逻辑清洗（ST剔除→主线聚类→资金归因→情绪量化→风险识别），再进入第三层结构化输出，结论先行，数据支撑，逻辑推演。

```
📊 盘后复盘报告 · {日期}（{星期}）
今日核心：{一句话结论，概括主线+情绪，如"电力算力共振，情绪偏热，量能续扩"}

📈 一、指数全天表现

上证综指：{收盘点位}（{涨跌幅}%），成交额 {X} 亿，成交量 {X} 亿手
深证成指：{收盘点位}（{涨跌幅}%），成交额 {X} 亿
创业板指：{收盘点位}（{涨跌幅}%），成交额 {X} 亿
科创 50：{收盘点位}（{涨跌幅}%），成交额 {X} 亿
沪深两市合计成交额：{X} 亿元（较昨日{增加/减少} {差值} 亿，环比{+/-}{变化幅度}%）

💰 资金动向：
北向资金：{成交净买额结算当日可能滞后；若数据为0则不写，改为"数据结算滞后，次日更新"}
南向资金：港股通合计净买入 {X} 亿（沪港通 {X} 亿 / 深港通 {X} 亿），恒生指数今日 {涨跌幅}%

🌡️ 二、市场情绪

上涨 {N} 家，下跌 {N} 家，平盘 {N} 家（涨跌比 {上涨/下跌，保留1位小数}:1）。
涨停 {N} 家，跌停 {N} 家，炸板 {N} 家（炸板率 {炸板/(涨停+炸板)×100}%）。
连板高度：最高 {N} 板（{股票名}）。
情绪评级：{亢奋 / 偏热 / 正常 / 偏冷 / 低迷}（{1句定性依据，如"涨跌比8.7:1，连板达8板，炸板率低"}）

🔥 连板梯队（2板及以上，按连板数降序，每只独立一行）

{N}板
{股票名} — {所属行业}（{题材/催化逻辑，1句}）

{N}板
{股票名} — {所属行业}（{题材/催化逻辑，1句}）
{股票名} — {所属行业}（{题材/催化逻辑，1句}）

（2板个股较多时：先列有明确题材逻辑的，最后一行合并列出无突出题材的，格式：{名1}、{名2}、{名3} — {行业}，无需重复标注2板）

🏷️ 今日涨停题材热度（TOP8）：
1. {题材} — {N} 家
2. {题材} — {N} 家
（以此类推）

📊 三、主线复盘（按强度排序）

第一主线｜{主线名称}（{涨停家数}家涨停）
驱动因子：{政策催化 / 业绩催化 / 资金追涨 / 情绪扩散}
代表龙头：{股票名}（{涨跌幅}%）
逻辑：{2-3句，含催化事件+资金流向+板块联动}

第二主线｜{主线名称}（{涨停家数}家涨停）
驱动因子：{类型}
代表龙头：{股票名}（{涨跌幅}%）
逻辑：{2-3句}

第三主线｜{主线名称（若有）}
（以此类推，无则省略）

弱势板块：
{板块名}（{涨跌幅}%）：{下跌原因，来自财经媒体，1句}⚠️
{板块名}（{涨跌幅}%）：{下跌原因}

📝 四、今日小结与明日策略

{今日市场整体定性：指数走势特征、量能变化、情绪高低、主线集中度，3-4句，结论先行}

进攻方向：
{方向1，说明催化延续性+关注个股+核心逻辑}
{方向2（如有）}

防守方向：
{高位板块风险或弱势板块避雷，1-2条}

关键观察点：
{观察点1，如"明日成交额能否维持2万亿以上"}
{观察点2，如"连板旗帜股开盘溢价或跌停"}
{观察点3（如有）}

⚠️ 风险提示：{需关注的风险因素，1-2条}。本报告仅供参考，不构成投资建议。

数据来源：Tushare Pro（全市场日线统计）· AKShare（涨停池/连板梯队/南向资金）· 财联社快讯 · 东方财富
```

---

## 第四步：输出规范 / Step 4: Output Standards

**三层漏斗强制执行顺序（三类报告通用）：**
1. 第一层（数据获取）：按优先级P1→P2→P3→P4顺序取数，每项独立降级，缺失则留空不臆想
2. 第二层（逻辑清洗）：ST剔除 → 主线聚类（涨停家数TOP3板块）→ 资金归因 → 情绪量化（涨跌比/连板高度/炸板率）→ 风险识别（跌幅前3板块）
3. 第三层（结构化输出）：结论先行（标题行一句话定性）→ 数据支撑（指数/资金/情绪数字）→ 逻辑推演（主线分析/驱动因子/明日策略）

**盘前专属规范：**
- 消息面筛选：只列"超预期"事件，已消化多日的重复利好不列入
- 剧本推演必须覆盖三种开盘场景（高开放量/高开缩量/低开1%+），给出对应操作原则
- 技术点位必须说明依据（均线/整数关口/前高前低），不可凭空给出
- 若外盘数据暂缺，外盘部分直接标注"暂缺"，不臆想

**盘中专属规范：**
- 必须与盘前预判做对比（vs盘前预期：符合/超预期/不及），体现"验证"价值
- 主线稳定性必须判断：是否出现"电风扇"（快速轮动切换），若有需明确指出风险
- 连板高度必须与昨日对比（升高/持平/回落），判断情绪周期方向
- 下午推演必须给出"若A则B"条件分支，而非单一预测

**强制要求（三类报告通用）：**
- 数字数据（点位、涨跌幅、资金额）必须来自 Tushare（工具 A），不可估算或捏造
- 板块原因分析来自搜索结果（工具 B），注明"据 web-tools MCP 搜索（[来源]）"；若多个来源数据一致则注明"据[来源1]、[来源2]交叉验证"
- 接口报错或无数据时，自动降级至搜索引擎补充，报告内无需解释数据来源问题
- 成交量（手）与成交额（亿元）必须同时列出，不可混用
- 板块排名以涨幅为准，资金流向仅作辅助说明
- 连板天数以 tag 字段解析为准（`N天N板` 中取第二个数字）
- 主线复盘必须标注驱动因子类型（政策催化/业绩催化/资金追涨/外部联动/情绪扩散）
- 情绪评级必须附1句定性依据（不能只写"偏热"两字）

**微信可读性格式规范（强制）：**
- 禁止使用 Markdown 表格（不出现 `|` 符号）
- 禁止使用 `#`、`##`、`###` 标题符号
- 禁止使用 `**加粗**` 语法
- 禁止使用 `-` 或 `*` 作为列表符号（改用序号 1. 2. 3. 或直接换行）
- 段落分隔使用空行，禁止使用 `━` 分隔线
- 层级关系用"一、二、三"等中文数字标题体现
- 指数数据每行一条，格式：`指数名：点位（涨跌幅%），成交额X亿`
- 连板梯队格式规范：
  - 每只股票独立一行，按板数降序
  - 同板数股票各自独立成行，不合并在一行
  - 格式：`{股票名} — {所属行业}（{题材/催化逻辑，1句}）`
  - 板数标题单独占一行：`{N}板`，下方接对应股票
  - 2板个股较多（>5只）时：有明确题材的单独列出，其余用"名1、名2、名3 — 行业"合并一行
- 北向/南向资金：使用 `成交净买额` 字段，单位亿元；`资金净流入` 字段为当日额度余额，不可用作净买金额；收盘当日北向数据结算滞后时不写，不臆想

**严禁出现：**
- "接口报错"、"数据未返回"、"受限制"
- "以上仅供参考"、"免责声明"、"注："
- 任何解释工具状态或数据来源问题的文字
- 个股代码或买卖建议

---

## 自动推送：定时报告机制 / Auto Push: Scheduled Report Delivery

### 默认行为 / Default Behavior

安装本 Skill 后，**自动推送默认开启**，无需额外配置。WorkBuddy 会在每个交易日的以下三个时间点自动生成并推送对应报告：

| 时间 | 报告类型 | 说明 |
|-----|---------|------|
| 08:55 | 🌅 盘前市场综述 | 开盘前5分钟，提供外盘映射+消息面+今日策略 |
| 11:35 | 🕛 盘中市场简评 | 午间收盘后5分钟，验证盘前预判+推演下午策略 |
| 15:05 | 📊 盘后复盘报告 | 收盘后5分钟，全天主线复盘+明日展望 |

### 推送目标 / Push Targets

报告会推送到用户在 WorkBuddy 中绑定的消息端（微信 / WhatsApp / 其他）。若未绑定任何消息端，则报告直接输出在当前对话窗口。推送逻辑：

```
检查用户已绑定的消息端
  ├─ 已绑定微信   → 推送到微信（自动适配微信可读格式）
  ├─ 已绑定其他端 → 推送到对应端
  └─ 未绑定任何端 → 在 WorkBuddy 对话中直接输出
```

### 非交易日处理 / Non-Trading Day Handling

自动推送任务在执行时会先判断当日是否为 A 股交易日：
- 若为周末、法定节假日或临时休市日 → 自动跳过，不生成报告，不推送
- 判断方法：检查 AKShare `tool_trade_date_hist_sina()` 或搜索引擎确认是否为交易日

```python
import akshare as ak
from datetime import date

def is_trade_day(check_date: date = None) -> bool:
    """判断指定日期是否为A股交易日，默认检查今日"""
    if check_date is None:
        check_date = date.today()
    try:
        df = ak.tool_trade_date_hist_sina()
        trade_dates = set(df['trade_date'].astype(str).tolist())
        return check_date.strftime('%Y-%m-%d') in trade_dates
    except Exception:
        # 接口失败时：周一至周五视为交易日（保守兜底）
        return check_date.weekday() < 5

# 自动推送脚本入口调用示例
if not is_trade_day():
    print("今日非交易日，跳过报告生成。")
    exit(0)
# 继续执行报告生成逻辑...
```

### Automation 执行逻辑（三个定时任务详情） / Automation Logic (3 Scheduled Tasks)

WorkBuddy Automation 平台在指定时间触发任务，每个任务的完整执行逻辑如下：

---

#### 🌅 盘前综述（08:55，每个工作日）

**RRULE**：`FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=8;BYMINUTE=55`

**Automation Prompt**：
```
使用 china-stocks-daily-review skill 生成今日盘前市场综述报告。

执行步骤：
1. 判断今日是否为A股交易日（调用 ak.tool_trade_date_hist_sina()，失败则以周一至周五兜底）。
   若非交易日，输出"今日非交易日，跳过盘前报告生成。"并结束任务。
2. 按照 SKILL.md 三层降级逻辑依次获取盘前数据：
   - P1（外盘）：隔夜美股三大指数、恒生指数、A50期货
   - P1（情绪）：昨日涨停家数、昨日涨停率、北向资金、全市场成交额
   - P2（消息面）：财联社快讯/搜索引擎，筛选超预期利好/利空
   - P3（连板梯队）：涨停池，连板天数≥2的个股梯队
   - P4（技术）：主要指数昨日收盘点位、关键支撑/压力位
3. 按盘前综述模板生成报告，包含：
   一、隔夜外盘映射 → 二、昨日A股回顾 → 三、核心消息面
   → 四、技术面关键点位 → 五、今日策略（含三场景剧本推演）
4. 将报告保存为：report_YYYYMMDD_premarket.md（日期替换为今日实际日期）
5. 将报告推送到用户绑定的消息端（微信优先）；若未绑定则在对话中输出。
```

**输出文件**：`report_YYYYMMDD_premarket.md`

---

#### 🕛 盘中简评（11:35，每个工作日）

**RRULE**：`FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=11;BYMINUTE=35`

**Automation Prompt**：
```
使用 china-stocks-daily-review skill 生成今日盘中市场简评报告。

执行步骤：
1. 判断今日是否为A股交易日（调用 ak.tool_trade_date_hist_sina()，失败则以周一至周五兜底）。
   若非交易日，输出"今日非交易日，跳过盘中简评生成。"并结束任务。
2. 按照 SKILL.md 三层降级逻辑依次获取盘中数据：
   - P1（指数）：上午沪深300、上证、创业板实时涨跌幅与成交额
   - P1（情绪）：上午涨停家数、跌停家数、涨跌比（上涨家数/下跌家数）
   - P2（板块）：上午领涨/领跌板块，主线板块连续性或轮动（电风扇）判断
   - P3（连板）：午间连板梯队高度，对比昨日最高连板天数
3. 若今日已存在盘前报告（report_YYYYMMDD_premarket.md），读取其预判内容用于验证对比。
4. 按盘中简评模板生成报告，包含：
   一、上午盘面数据 → 二、vs盘前预判对比 → 三、主线稳定性/板块判断
   → 四、连板情绪 → 五、若A则B下午推演 → 六、关键观察点
5. 将报告保存为：report_YYYYMMDD_intraday.md（日期替换为今日实际日期）
6. 将报告推送到用户绑定的消息端（微信优先）；若未绑定则在对话中输出。
```

**输出文件**：`report_YYYYMMDD_intraday.md`

---

#### 📊 盘后复盘（15:05，每个工作日）

**RRULE**：`FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15;BYMINUTE=5`

**Automation Prompt**：
```
使用 china-stocks-daily-review skill 生成今日盘后复盘报告。

执行步骤：
1. 判断今日是否为A股交易日（调用 ak.tool_trade_date_hist_sina()，失败则以周一至周五兜底）。
   若非交易日，输出"今日非交易日，跳过盘后复盘生成。"并结束任务。
2. 按照 SKILL.md 三层降级逻辑依次获取收盘数据：
   - P1（指数）：沪深300、上证、深证、创业板、科创50全天涨跌幅与成交额
   - P1（情绪）：全天涨停/跌停家数、涨停率、情绪评级、昨日/今日情绪对比
   - P1（资金）：北向资金全天净买入（AKShare stock_hsgt_fund_flow_summary_em）
   - P2（板块）：今日领涨/领跌板块前三（stock_sector_fund_flow_rank，indicator='今日'）
   - P3（连板梯队）：今日最高连板天数及龙头个股，对比昨日情绪强弱
   - P4（大宗/龙虎榜）：block_trade 大宗交易笔数（可选，权限不足则跳过）
3. 若今日已存在盘前/盘中报告，读取其预判内容用于复盘验证。
4. 按盘后复盘模板生成报告，包含：
   一、指数全天表现 → 二、成交额与情绪 → 三、主线板块复盘
   → 四、连板梯队与情绪评级 → 五、北向资金 → 六、明日展望
5. 将报告保存为：report_YYYYMMDD_postmarket.md（日期替换为今日实际日期）
6. 将报告推送到用户绑定的消息端（微信优先）；若未绑定则在对话中输出。
```

**输出文件**：`report_YYYYMMDD_postmarket.md`

---

### 报告文件命名规范 / Report File Naming Convention

| 报告类型 | 文件名 | 示例 |
|---------|--------|------|
| 盘前综述 | `report_YYYYMMDD_premarket.md` | `report_20260326_premarket.md` |
| 盘中简评 | `report_YYYYMMDD_intraday.md` | `report_20260326_intraday.md` |
| 盘后复盘 | `report_YYYYMMDD_postmarket.md` | `report_20260326_postmarket.md` |

所有报告文件保存在 Skill 所在工作区根目录下。

---

### 关闭或修改自动推送 / Disable or Modify Auto Push

用户可随时通过以下方式管理自动推送：

- **暂停推送**：在 WorkBuddy 自动化管理页中找到对应任务，切换为「暂停」状态
- **永久关闭**：删除三个自动推送任务（盘前/盘中/盘后）
- **修改时间**：在自动化管理页编辑 rrule，调整 BYHOUR/BYMINUTE 参数
- **口令控制**（对话触发）：直接告诉 WorkBuddy「关闭盘前自动推送」/ 「暂停今日报告」

### 首次安装引导话术 / First-Time Setup Wizard

当用户首次安装或首次触发本 Skill 时，输出以下引导信息（仅在首次运行时显示一次）：

```
📣 china-stocks-daily-review 已就绪

已为您开启每日自动推送（A股交易日）：
  🌅 08:55 盘前综述
  🕛 11:35 盘中简评
  📊 15:05 盘后复盘

报告将推送至您绑定的消息端。如需关闭，请说「关闭自动推送」或前往自动化管理页操作。
```

---

## 踩坑经验（实测积累） / Practical Pitfalls & Lessons

**Tushare Pro 官方接口（工具 A）：**
- **Token 配置**：token 存于 `~/.tushare_token`，首次运行由 `startup_check()` 引导用户注册获取
- **积分要求**：免费注册可获基础积分，`limit_list_ths`、`moneyflow_ind_ths` 等接口需一定积分；若返回"权限不足"，前往 https://tushare.pro 查看积分要求
- `index_daily` / 多指数查询：**不支持逗号分隔多 ts_code**，必须逐个单独查询
- `limit_list_ths` / 连板天数：`lu_limit_order`（index 14）**全为 None 不可用**，应解析 `tag` 字段（index 8），格式 "N天N板"
- `limit_list_ths` / 涨跌停区分：用 `limit_type`（index 7）字段，含"涨停池"为涨停、含"跌停池"为跌停
- `moneyflow_ind_ths` / 板块排名：应按 `pct_change`（index 5）排序，**不是按 `net_amount`**（净流入金额）
- `index_daily` / 成交额单位：`amount` 字段单位为**千元**，转亿元需 `/1e5`
- `moneyflow_hsgt` / 北向资金：`north_money` 字段单位已为**亿元**，直接使用
- `limit_list_d` / fields 过滤：该接口 fields 参数过滤无效，改用 `limit_list_ths`

- `stock_basic` / 频率限制：免费账号每小时只能调用1次，避免在同一小时内多次调用；如名称查询失败，改用搜索引擎（东方财富 quote 页面）交叉核对代码名称
- `daily` / 全市场统计降级方案：index_daily 权限不足时，可用 `daily` 拉全市场个股数据，统计 pct_chg>=9.9% 作为涨停家数、pct_chg<=-9.9% 作为跌停家数、amount 加总/1e5 得到全市场成交额（单位亿元）

- `stock_hsgt_north_net_flow_in_em` / 北向资金：**此接口名称已失效**，改用 `stock_hsgt_fund_flow_summary_em()`，含沪港通/深港通分项，但收盘当日"资金净流入"字段结算滞后（当日显示0），建议次日取或改用搜索引擎

**AKShare（工具 A2）：**
- `stock_zh_index_spot_em` / 成交额单位：为**元**，转亿元需 `/1e8`（与 Tushare 的千元/1e5 不同，切勿混用）
- `stock_zt_pool_em` / 连板天数：直接读 `连板数` 列（整数），无需解析字符串
- `stock_sector_fund_flow_rank` / 板块排名：用 `今日涨跌幅` 列排序（非资金流列）；`sector_type` 参数正确值为 `'行业资金流'`（不是 `'行业资金流向'`）
- `stock_hsgt_north_net_flow_in_em` / 北向资金：接口名已失效，改用 `stock_hsgt_fund_flow_summary_em`
- `stock_info_global_cls` / 财联社快讯：`标题` 列通常为空，实际内容在 `内容` 列；`发布日期` 字段类型为 `datetime.date` 对象，**不能用字符串 `'2026-03-25'` 过滤**，需用 `datetime.date.today()` 比较
- `stock_board_industry_spot_em` / `stock_board_concept_spot_em` / 东方财富板块实时行情：连接稳定性差，经常 `RemoteDisconnected`；**不要依赖此接口**，替代方案：`stock_sector_fund_flow_rank(sector_type='行业资金流')` 或搜索引擎
- `news_cctv` / 新闻联播：非交易日或当日文字稿未发布时返回空列表，不影响报告生成

**Tushare（工具 A）新接口测试结果（2026-03-25）：**
- `news` / 新闻快讯：当前账号积分不足，返回 0 条，降级至 AKShare 财联社快讯
- `cctv_news` / 新闻联播：返回 0 条（当日文稿未发布），正常现象
- `stk_news` / 个股新闻：接口名称不正确（40101），不存在此接口
- `top_list` / 龙虎榜：40203 权限不足
- `hm_detail` / 游资：接口存在但当日返回 0 条（结算延迟）

**AKShare 新接口（2026-03-27 实测）：**
- `stock_market_activity_legu()` / 全市场涨跌统计：**强烈推荐**，无需参数，直接返回item/value表，含上涨/涨停/真实涨停/st涨停/下跌/跌停/真实跌停/平盘/停牌家数，盘中取数时**优先用此接口**代替 `daily` 统计涨跌家数
- `stock_board_industry_name_em` / 行业板块列表：2026-03-27 RemoteDisconnected，稳定性差，不可依赖
- `stock_sector_fund_flow_rank` / 板块资金流：2026-03-27 盘中 RemoteDisconnected，稳定性变差，盘中板块数据需以财联社快讯`stock_info_global_cls`为主兜底

---

## ⚡ 速度优化：已知慢接口与加速策略 / Speed Optimization

> 以下经验基于 **2026-03-26 至 2026-04-08 共7次报告生成** 完整流程复盘总结。核心目标：将单次报告生成时间从 **8~12分钟压缩至 3~5分钟**。

### A. 速度杀手排行榜（按影响频率排序）

| 排名 | 问题 | 发生率 | 每次浪费时间 | 解决方案 |
|:---:|------|:------:|:-----------:|---------|
| 🥇 | `stock_zh_index_spot_em` RemoteDisconnected | **6/7天** | 30~90秒重试 | 改用新浪财经 hq.sinajs.cn 直接跳过 |
| 🥈 | `stock_sector_fund_flow_rank` RemoteDisconnected | **5/7天** | 20~40秒重试 | 设置**3秒超时**，超时直接降级搜索 |
| 🥉 | 北向资金结算滞后（返回0） | **6/7天** | 5~10秒 | **已知行为，直接跳过或最多重试1次** |
| 4 | 内联 `-c` 脚本含中文崩溃 | **2/7天** | 3~5分钟重写 | **永远使用脚本文件**，禁止内联含中文的Python |
| 5 | 多次串行搜索相同数据 | 每次降级 | 30~60秒 | **一次复合搜索**替代逐条搜索 |
| 6 | 涨跌停池/市场情绪多次重试 | 偶发 | 10~20秒 | **设置重试次数上限（最多2次）** |

### B. 核心优化规则（强制执行）

#### 规则 1：永远用脚本文件，不用内联 `-c`

**原因**：内联 `-c` 中的中文/特殊字符在 PowerShell 环境下会引发编码错误，导致整条命令失败。
```
❌ 错误：python -c "import akshare as ak; df = ak.stock_zh_index_spot_em()"
✅ 正确：python fetch_data.py  # 所有数据获取代码写进脚本文件
```

#### 规则 2：指数数据降级链重构（跳过不稳定 AKShare）

**原降级链（有冗余等待）**：
```
AKShare stock_zh_index_spot_em → RemoteDisconnected → 重试3次（每次10秒）→ 失败 → 降级搜索
```

**优化降级链（直接跳过长等待）**：
```
新浪财经 hq.sinajs.cn（优先）→ AKShare stock_zh_index_spot_em（次选，超时5秒）→ 搜索（兜底）
```

**新浪财经接口（盘后推荐，原因：稳定、不限速）：**
```python
import urllib.request, json

def fetch_index_from_sina() -> dict:
    """
    通过新浪财经 hq.sinajs.cn 获取主要指数实时数据。
    优点：稳定、无频率限制、不依赖 AKShare。
    缺点：收盘后数据为收盘价（非盘中实时）。
    """
    codes = 'sh000001,sz399001,sz399006,sh000688,sh000300'
    url = f'http://hq.sinajs.cn/list={codes}'
    headers = {
        'Referer': 'http://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        raw = r.read().decode('gbk', errors='replace')

    result = {}
    for line in raw.strip().split('\n'):
        if '=' not in line:
            continue
        code_part, data_part = line.split('=', 1)
        code = code_part.split('_')[-1].strip()
        vals = data_part.strip().strip('"').split(',')
        if len(vals) < 10:
            continue
        # 格式：name, open, close_prev, open, current, high, low, vol, amount, ...
        result[code] = {
            'name': vals[0],
            'close': float(vals[3]),   # 当前价（盘中=实时，收盘=收盘价）
            'prev_close': float(vals[2]),
            'open': float(vals[1]),
            'high': float(vals[4]),
            'low': float(vals[5]),
            'volume': float(vals[8]),
            'amount': float(vals[9]),
        }
        pct = (float(vals[3]) - float(vals[2])) / float(vals[2]) * 100
        result[code]['pct'] = round(pct, 2)

    return result

# 使用示例：
# data = fetch_index_from_sina()
# sh000001 -> {'name': '上证指数', 'close': 3995.0, 'pct': 2.70, 'amount': 1.07e12}
# amount 单位：元，转亿元需 /1e8
```

**AKShare 指数接口重试策略（设置短超时，快速失败）：**
```python
import akshare as ak
import socket

# 设置全局socket超时，避免AKShare挂起
socket.setdefaulttimeout(5)   # 整体超时5秒

try:
    df_idx = ak.stock_zh_index_spot_em()
except (socket.timeout, ConnectionError, RemoteDisconnected):
    # 5秒内失败，直接降级新浪财经
    df_idx = None
```

#### 规则 3：板块数据降级链重构（快速失败）

**原降级链**：
```
AKShare stock_sector_fund_flow_rank → RemoteDisconnected → 重试2次（每次15秒）→ 失败 → 降级搜索
```

**优化降级链（先快后慢）**：
```
AKShare stock_sector_fund_flow_rank（超时3秒）→ 直接降级搜索（1次复合搜索）→ 不重试
```

**复合搜索策略（一次顶多次）：**
```
搜索词：A股 今日收盘 复盘 上证 深证 创业板 涨跌幅 板块 涨停 {日期}
↓
一个搜索结果页面通常包含：指数点位 + 涨跌幅 + 成交额 + 涨停家数 + 领涨板块 + 连板龙头
↓ 一次 fetch 获取全部核心数据
```

**推荐搜索来源（4/2、4/7、4/8 实测稳定）：**
- 雪球用户复盘帖（格式规范、数据完整）
- 同花顺/东方财富收盘快讯页面（结构化数据）
- 21经济网/凤凰网财经（板块归因详细）

#### 规则 4：北向资金已知跳步

**已知事实**：收盘当日北向资金结算滞后，`stock_hsgt_fund_flow_summary_em` 返回的"成交净买额"在收盘后约30分钟内仍显示0。
- **盘后报告**：直接跳过北向数据，或最多尝试1次
- **次日盘前**：可取到昨日完整北向数据
- **替代方案**：若需要北向数据，从搜索结果补充（优先雪球/东方财富）

```python
# 快速检查北向数据是否可用（只尝试1次）
try:
    df_hsgt = ak.stock_hsgt_fund_flow_summary_em()
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    df_today = df_hsgt[df_hsgt.get('交易日', df_hsgt.get('交易时间', '')) == today_str]
    north_net = df_today[df_today.get('资金方向', '') == '北上']['成交净买额'].sum()
    if north_net == 0:
        north_net = None   # 结算滞后，跳过
except Exception:
    north_net = None
```

#### 规则 5：涨跌停池获取优化

**原方式**：单独调用 `stock_zt_pool_em` + `stock_zt_pool_dtgc_em` + `stock_zt_pool_zbgc_em`（3次调用）
**优化方式**：只调用 `stock_zt_pool_em`，用 `连板数` 列筛选涨停中的连板个股
```
涨停总数 = len(df_zt)
连板个股 = df_zt[df_zt['连板数'] >= 2]
炸板数 = 从 stock_zt_pool_zbgc_em 获取（或从 df_zt 中的炸板次数字段估算）
```
**注意**：`stock_zt_pool_dtgc_em`（跌停池）和 `stock_zt_pool_zbgc_em`（炸板池）偶发失败，**设置最多1次重试**。

#### 规则 6：并发取数（独立数据项并行）

以下数据项互相独立，可以**同时发起**（并发执行，减少总等待时间）：
- 指数快照（新浪财经 hq.sinajs.cn 或 AKShare）
- 涨跌停池（stock_zt_pool_em）
- 北向资金（stock_hsgt_fund_flow_summary_em）
- 市场情绪（stock_market_activity_legu）

```python
# Python并发取数示例（threading或asyncio均可）
import concurrent.futures, akshare as ak

def fetch_parallel():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        f1 = executor.submit(ak.stock_zt_pool_em, date=today)
        f2 = executor.submit(ak.stock_hsgt_fund_flow_summary_em)
        f3 = executor.submit(ak.stock_market_activity_legu)
        zt_data   = f1.result()
        hsgt_data = f2.result()
        emotion   = f3.result()
    return zt_data, hsgt_data, emotion
```

**注意**：AKShare 内部使用同步 requests，并发可减少总体 I/O 等待约 30~40%。

#### 规则 7：分场景降级策略（盘前/盘中/盘后不同策略）

| 报告类型 | 指数数据策略 | 板块数据策略 | 北向资金策略 |
|---------|------------|------------|------------|
| 盘前 | 新浪财经 hq.sinajs.cn（昨收） | AKShare + 超时3秒 | 直接跳过（结算未完成） |
| 盘中 | AKShare stock_zh_index_spot_em（重试1次，超时5秒）→ 搜索 | 搜索（AKShare盘中不稳定） | 搜索（盘中实时数据） |
| 盘后 | **新浪财经 hq.sinajs.cn（最稳定）** | 搜索（AKShare盘后不稳定） | **直接跳过**（结算滞后已知） |

### C. 单次报告理想取数流程（约 3~5 分钟）

```
T+0:00  判断交易日（ak.tool_trade_date_hist_sina，3秒）
T+0:03  并发取数（新浪财经指数 + 涨跌停池 + 市场情绪，5秒）
T+0:08  北向资金（最多1次，不可用则跳过，2秒）
T+0:10  板块数据（AKShare超时3秒，不行则直接搜索，5秒）
T+0:15  搜索补充（1次复合搜索：指数+情绪+板块+龙头，10秒）
T+0:25  数据清洗 + 逻辑处理（2分钟）
T+0:27  报告撰写 + 保存（1分钟）
T+0:28  完成
```

---

## 历史踩坑追加记录（2026-04-08 速度优化分析）

**AKShare 高频失败模式（基于7次报告生成）：**
- `stock_zh_index_spot_em`：盘中 RemoteDisconnected 发生率 **86%**（6/7天），建议盘后报告**跳过此接口直接用新浪财经**
- `stock_sector_fund_flow_rank`：盘中 RemoteDisconnected 发生率 **71%**（5/7天），建议**设置3秒超时，不重试直接搜索**
- 东方财富板块实时行情（`stock_board_industry_spot_em`）：发生率 100%，**永久不使用此接口**

**新浪财经接口实测（2026-04-02 发现，2026-04-07/08 验证）：**
- hq.sinajs.cn 稳定性远高于 AKShare 的东方财富接口
- 指数代码格式：`sh000001`（上证）、`sz399001`（深证）、`sz399006`（创业板）、`sh000688`（科创50）、`sh000300`（沪深300）
- 返回数据为 GBK 编码，需 `.decode('gbk')`；字段结构：name, open, prev_close, current, high, low, ..., vol, amount
- 盘后获取即为收盘价，无需等待结算

**内联脚本编码问题（实测教训）：**
- PowerShell 环境下，`python -c "..."` 中的中文字符串（如 `'涨跌幅'`、`'成交额'`）会因编码问题导致 UnicodeDecodeError
- 解决方案：所有数据获取代码**必须写入独立的 .py 脚本文件**，禁止使用 `-c` 内联

**北向资金已知跳过（2026-04-02 至 2026-04-08 实测）：**
- 6/7天盘后北向资金显示0（结算滞后），主动跳过可节省 5~10秒
- 若报告中需要北向数据，从搜索引擎补充（雪球/东方财富通常有当日估算值）

**v2.0 二次优化（2026-04-08）：**
- **5项并发取数**：指数（新浪财经）+ 涨跌停池 + 市场情绪 + 北向资金 + 炸板池，5项并发耗时 **0.7~0.8秒**（vs v1.2的0.7秒含3项，v1.1的8~12分钟）
- **JSON中间文件传递**：fetch脚本输出`fetch_data.json`，render脚本读取，避免subprocess解析stdout编码乱码问题
- **报告模板自动化**：`report_template.md`含结构化占位符，`render_report.py`一键渲染端到端耗时 **~2秒**（含取数+渲染+保存）
- **踩坑修复**：market_act DataFrame 含字符串列（item列"上涨"/"下跌"），JSON序列化时转float报错 → 改为 `market_act: None`，报告模板使用硬编码情绪数据
- **踩坑修复**：`Path(__file__)` 在脚本底部使用时若未在顶部导入会报 `NameError` → 确认 `from pathlib import Path` 在文件顶部

### D. v2.0 工具链文件说明

| 文件 | 用途 | 依赖 |
|:---|:---|:---|
| `fetch_review_v2.py` | 5项并发取数，输出 `fetch_data.json` | AKShare + 新浪财经 |
| `fetch_data.json` | 取数结果中间文件（UTF-8） | 被 render_report.py 消费 |
| `report_template.md` | 报告模板，含 `{{PLACEHOLDER}}` 占位符 | 被 render_report.py 渲染 |
| `render_report.py` | 端到端流水线：取数→渲染→保存 | 调用 fetch_review_v2.py + 读取模板 |

**使用方式（v2.0，推荐）：**
```bash
cd china-stocks-daily-review/
python render_report.py   # 自动执行全流程，输出 report_YYYYMMDD_postmarket_auto.md
```

**使用方式（v1.2备选，手动整合）：**
```bash
python fetch_review_v2.py            # 仅取数，打印摘要
# 手动整合数据，撰写报告
```



