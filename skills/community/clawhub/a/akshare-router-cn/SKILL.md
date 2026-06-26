# akshare-router-cn

面向中文用户的「AKShare 数据路由器」skill：把期货/期权问题按 **频率(实时/分钟/日频)** → **品类(期货/期权)** → **是否需要二次加工(指标/Greeks/RR25)** 三步分流到最合适的数据源与 recipe。

> 一期只覆盖 **免费可用源**：东方财富/新浪等公开页面对应的 AKShare 接口。**不包含奇货可查/付费源**。

---

## 你要做的事（路由协议，必须遵守）

当用户提问时：

### Step 0：抽取意图槽位
- `freq`：realtime | intraday(minute) | daily/历史
- `asset`：futures | options
- `need_compute`：none | indicators | greeks_iv | rr25 | (组合)
- `scope`：单合约 | 品种全合约 | 全市场/列表

### Step 1：先判频率（实时优先）
- 命中【实时/盘面/盘口/最新价/当前/成交量/持仓/分时/分钟/5m/30m】→ `realtime` 或 `intraday`
- 命中【日线/历史/从…到…/近一年/回测】→ `daily/历史`

### Step 2：再判品类（期货 vs 期权）
- 命中【期货/主连/次主连/合约如 IF2403/ RB主连】→ futures
- 命中【期权/看涨/看跌/行权价/隐含波动率/Delta/Gamma】→ options

### Step 3：最后判是否二次加工
- 命中【MA/EMA/MACD/RSI/布林/ATR/5m指标/30m指标】→ indicators
- 命中【隐含波动率/IV/Delta/Gamma/Theta/Vega/Rho】→ greeks_iv
- 命中【RR25/25D 风险逆转/Skew】→ rr25（需要 greeks_iv + 规则）

### Step 4：按需加载（只读需要的文件）
1) 先 `read maps/router.yml`：找到对应 recipe
2) 再 `read recipes/<name>.md`：按步骤执行
3) 如果 recipe 引用 method（例如 RR25/指标计算），再 `read methods/<name>.md`

---

## 入口路由表（文件）
- `maps/router.yml`：意图 → recipe 文件名（**唯一真源**）
- `maps/keywords.yml`：中文关键词归一化（减少误判）
- `references/INDEX.md`：AKShare 可用接口索引（只列一期用到的）

---

## MVP 覆盖的用户高频需求

### 期货
- 实时盘面/成交（某个品种所有合约）：`recipes/futures_realtime_board.md`
- 5m/30m 分钟线 + 技术指标：`recipes/futures_kline_indicators.md`

### 期权
- 隐含波动率 + Greeks（基于上交所 ETF 期权）：`recipes/options_iv_greeks.md`
- RR25（基于 Delta 近似）：`recipes/options_rr25.md`

---

## 运行方式（给会用工具的 agent）
- 数据抓取与计算脚本在 `scripts/`；可用 `exec` 运行，例如：
  - `python3 skills/akshare-router-cn/scripts/futures_realtime.py --symbol PTA`
  - `python3 skills/akshare-router-cn/scripts/futures_indicators.py --contract IF2008 --period 30`
  - `python3 skills/akshare-router-cn/scripts/options_rr25.py --underlying 510050 --trade_date 202603`

> TODO：如果未来要把脚本封装成统一 CLI（如 `akrcn ...`），可以在二期做，不影响本期路由文档结构。
