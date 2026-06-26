# analyze.py 输出字段说明（AnalysisResult）

本文档说明 `scripts/analyze.py` 中 `AnalysisResult` 的结构、各字段含义及大致计算方式，便于人读和下游消费。

---

## 一、整体结构

`AnalysisResult` 是一条单股票的分析结果，字段如下：

- `ts_code: str`  
  股票代码或名称（调用时传入的 symbol）。

- `trend: str`  
  趋势方向：
  - `bullish`：多头趋势（近期整体上涨，均线多头结构且价格在关键均线上方）；
  - `bearish`：空头趋势（近期整体下跌，均线空头结构）；
  - `sideways`：震荡趋势（涨跌幅不大、均线结构混乱）。

- `macd_cross: str`  
  MACD 金叉/死叉状态：
  - `golden`：最近一根 DIF 从 DEA 下方上穿 DEA（出现金叉）；
  - `death`：最近一根 DIF 从 DEA 上方向下穿 DEA（出现死叉）；
  - `none`：最近两日未出现明显金叉/死叉。

- `macd_strength: str`  
  MACD 强弱（基于 0 轴）：
  - `strong`：当前 DIF、DEA 都在 0 轴上方，多头更占优；
  - `weak`：当前 DIF、DEA 都在 0 轴下方，空头更占优；
  - `neutral`：一上一下或都接近 0 轴，方向不明确。

- `macd_momentum: str`  
  MACD 柱动能变化：
  - `increasing`：最新一根 MACD 柱绝对值 ≥ 前一根，动能在增强；
  - `decreasing`：最新一根 MACD 柱绝对值 < 前一根，动能在减弱。

- `weekly_change_pct: float`  
  最近一周（约 5 个交易日）的收盘价涨跌幅，单位为百分比：
  \( (C_{latest} / C_{-5}) - 1 \times 100 \)。

- `today_change_pct: float`  
  今日相对上一交易日收盘价的涨跌幅，单位为百分比：
  \( (C_{latest} / C_{prev}) - 1 \times 100 \)。

- `rsi: float`  
  当前 RSI14 数值，基于 14 日涨跌幅计算。

- `rsi_zone: str`  
  RSI 所在区间（强 / 弱 / 中性）：
  - `strong`：RSI ≥ 55；
  - `weak`：RSI ≤ 45；
  - `neutral`：45 < RSI < 55。

- `rsi_signal: str`  
  RSI 信号（超买 / 超卖 / 正常）：
  - `overbought`：RSI ≥ 70，超买；
  - `oversold`：RSI ≤ 30，超卖；
  - `normal`：介于其间。

- `rsi_trend: str`  
  RSI 方向：
  - `up`：当前 RSI > 前一日 RSI；
  - `down`：当前 RSI < 前一日 RSI；
  - `flat`：基本持平。

- `signal: str`  
  综合交易信号：
  - `buy`：短期状态较好，可以考虑买入或重点关注；
  - `sell`：短期状态较差，可以考虑卖出或回避；
  - `hold`：观望/持有，不建议新增仓位。

- `score: int`  
  0~10 分综合评分，主要基于：
  - 趋势（trend：bullish/sideways/bearish）；
  - MACD 金叉/死叉与强弱；
  - RSI 区间与方向；
  - 价格相对 MA20 的位置。  
  分数越高，短期技术状态越强，大致可理解为：
  - 0~2：很弱；
  - 3~5：一般；
  - 6~8：偏强；
  - 9~10：很强。

- `ma_pattern: str`  
  均线结构模式：
  - `bullish_alignment`：MA7 > MA14 > MA20 > MA60，多头排列；
  - `bearish_alignment`：MA7 < MA14 < MA20 < MA60，空头排列；
  - `mixed`：其余情况，均线交错、结构混乱。

- `ma_bias: str`  
  当前价格相对于 MA20 的位置：
  - `above_ma20`：收盘价在 MA20 上方；
  - `below_ma20`：收盘价在 MA20 下方。

- `ma_values: dict`  
  当前一根 K 线对应的均线与收盘价明细：
  - `MA7`: float
  - `MA14`: float
  - `MA20`: float
  - `MA60`: float
  - `close`: float（当前收盘价 / 盘中模拟收盘价）

- `ma_spread: float`  
  短长均线发散程度：\( (MA7 - MA60) / MA60 \)。
  - 正数：短期均线在长期均线上方，且偏离度越大，多头趋势越强；
  - 负数：短期均线在长期均线下方，且偏离度越大，空头趋势越强；
  - 接近 0：短长均线粘合，趋势较弱或处于震荡收敛阶段。

- `trend_strength: float`  
  趋势强度指标，推荐区间约为 -1 ~ +1，用于细分多空强弱：
  - 建议计算方式（示例）：
    \( trend\_strength = (MA7 - MA20)/MA20 + (MA20 - MA60)/MA60 \)；
  - 经验阈值：
    - `> 0.05`：强多头；
    - `0 ~ 0.05`：弱多头；
    - `≈ 0`：震荡；
    - `< -0.05`：强空头。

- `reversal_hint: str`  
  趋势转折预警信号，结合 `trend` 与 `macd_momentum` 提前一两天给出提示，示例逻辑：
  - 若 `trend == "bullish"` 且 `macd_momentum == "decreasing"`：
    - `reversal_hint = "top_warning"`（多头趋势中动能开始衰减，警惕见顶）；
  - 若 `trend == "bearish"` 且 `macd_momentum == "increasing"`：
    - `reversal_hint = "bottom_warning"`（空头趋势中动能减弱，警惕见底反弹）；
  - 否则可为 `"none"` 或留空，表示暂无明显转折信号。

- `risk_level: str`  
  风险标签，用于避免“追高/杀跌”，结合 RSI 与 ma_spread 给出当前风险档位，示例逻辑：
  - 若 `rsi >= 75`：`risk_level = "high_overbought"`（高位超买，追高风险大）；
  - 若 `rsi <= 25`：`risk_level = "high_oversold"`（极度超卖，短期波动风险加大）；
  - 若 `abs(ma_spread) > 0.1`：`risk_level = "trend_overextended"`（趋势过度发散，随时可能剧烈回调或反弹）；
  - 否则：`risk_level = "normal"`。

---

## 二、与脚本的关系

- 数据来源：`analyze_single(ts_code, df)` 会在内部调用：
  - `_append_intraday_bar_if_needed`（如有需要将 today 的盘中快照拼成一根“今日 K 线”）；
  - `_calc_trend` / `_calc_macd_state` / `_calc_rsi_state`；
  - `_describe_ma_structure`（产出 ma_pattern / ma_bias / ma_values / ma_spread）；
  - `_calc_signal` / `_calc_score`。
- 上述字段最终被打包为 `AnalysisResult` 并可通过 `asdict` 转成字典输出。

---

## 三、使用建议

- 做“机器可读”的打分或筛选时，优先使用：`signal`、`score`、`trend`、`weekly_change_pct`、`today_change_pct`；
- 做“人可读”的走势判断时，重点看：`ma_pattern`、`ma_bias`、`ma_spread`、`trend_strength`，再结合 `macd_*` 和 `rsi_*`；
- 做“拐点预警”和“风险控制”时，可以关注：`reversal_hint` 与 `risk_level`，辅助判断是否要减仓/止盈/观望；
- 对接类似 `analyze_data.md` 里的自然语言解读时，可直接把本文件的字段说明当作 schema 参考。