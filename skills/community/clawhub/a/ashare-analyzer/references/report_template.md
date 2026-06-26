# 报告模板 v2

此文件定义最终报告的**严格结构**。每个 `{{placeholder}}` 都对应 `data_<code>.json` 里的一个字段。

## 结构要求

1. **两张图先出**（K线图、对比图），顺序固定，紧接着是报告正文
2. 报告正文按以下顺序，不增不减：
   - 一、公司速览
   - 二、K线图（说明）
   - 三、主营业务构成 ← **新增**
   - 四、技术面评分
   - 五、大盘 & 同行业对比
   - 六、核心催化剂 & 风险
   - 七、买卖建议
3. 末尾附免责声明

---

## 模板正文（严格对齐）

```markdown
**【📈 {meta.name} ({meta.code6}) 综合分析】**
**数据截止：{meta.analysis_date}收盘**
---

**一、公司速览**
- 公司：{meta.name}
- 行业：{meta.industry}
- 所属板块/概念：{由 Claude 根据 F10 ssbk 返回结果总结，列出 3-5 个最相关的概念}
- 股价：**{price.close}元**（{price.pct_today 带符号}%，{见涨跌定性规则}）
- 市值：**{price.total_mv_yi:.1f}亿**
- PE(TTM)：**{price.pe_ttm}x**{见 PE 失真标注规则}
- PB：**{price.pb}x**
- ROE：**{financials.roe}%**（{见 ROE 定性规则}）
- 毛利率：**{financials.gross_margin}%**
- 最新财报（{financials.report_name}）：营收{financials.revenue_yi:.2f}亿（{financials.revenue_yoy_pct 带符号}%），归母净利{financials.net_profit_wan:.0f}万（{financials.net_profit_yoy_pct 带符号}%）
- **近期涨跌：** 1周 {technicals.pct_1w:.1f}% | 1月 {technicals.pct_1m:.1f}% | 1年 **{technicals.pct_1y:.1f}%**

> {由 Claude 基于数据写 1-2 句定性描述}

---

**二、K线图**（已发送 ↑）
近252个交易日完整日K线
- 年内最高：{technicals.year_high}元（{technicals.year_high_date}）
- 年内最低：{technicals.year_low}元（{technicals.year_low_date}）
- 当前位置：{Claude 结合 year_high/year_low 给当前价格定位}

---

**三、主营业务构成**（{main_business.report_name}）

| 业务 | 收入（亿元） | 占比 | 毛利率 |
|---|---|---|---|
| {item} | {revenue/1e8:.2f} | {revenue_ratio*100:.1f}% | {gross_margin*100:.2f}% |
| ... | | | |

> 按地区：{main_business.by_region 用一句话概述，如 "境内 92.9%，境外 7.1%"}
> {由 Claude 给 1 句业务结构评价，例如 "收入高度集中在制冷管路，毛利率低，汽车部件毛利率更高但体量小"}

---

**四、技术面评分**
**综合评分：{+X/10}（{偏多/中性/偏空}，{简评}）**

• {✅或⚠️} 均线排列：MA5({technicals.ma5:.2f}) {> 或 <} MA10({technicals.ma10:.2f}) {> 或 <} MA20({technicals.ma20:.2f})，**{多头/空头/纠缠}排列**
• {✅或⚠️} RSI(14)：{technicals.rsi14:.2f} → {根据 >70 / 30-70 / <30 判定}
• {✅或⚠️} MACD：DIF={technicals.macd_dif:.2f}, DEA={technicals.macd_dea:.2f} → {金叉/死叉/粘合}，MACD柱 {technicals.macd_hist:.2f}（{动能强弱}）
• {✅或⚠️} 布林带：价格{突破上轨/处于中轨上/处于中轨下/跌破下轨} {technicals.bb_deviation_pct 带符号}%
• {✅或⚠️} KDJ：K={technicals.kdj_k:.0f}, D={technicals.kdj_d:.0f}, J={technicals.kdj_j:.0f} → {超买/中性/超卖}
• {✅或⚠️} 成交量：{基于近 5 日成交量判断 放量/缩量/正常}
• 关键支撑：{ma5:.2f}（MA5）/ {ma10:.2f}（MA10）/ {ma20:.2f}（MA20）
• 关键阻力：{year_high:.2f}（52周新高）/ {下一整数关口}

---

**五、大盘 & 同行业对比**（对比图已发送 ↑）

**vs 沪深300**
- 近1月：{meta.name} {technicals.pct_1m:.1f}% | 沪深300 {market_compare.csi300_pct_1m:.1f}%
- 近1年：{meta.name} {technicals.pct_1y:.1f}% | 沪深300 {market_compare.csi300_pct_1y:.1f}%
> {由 Claude 一句话点评}

**vs 同行业对比**

| 指标 | **{target_name}** | {peer1.name} | {peer2.name} | {peer3.name} | {peer4.name} |
|---|---|---|---|---|---|
| 来源 | (目标) | {peer1.source} | {peer2.source} | ... | ... |
| 股价 | {price.close} | {peer1.close} | ... | ... | ... |
| 市值(亿) | {price.total_mv_yi:.1f} | {peer1.total_mv_yi:.1f} | ... | ... | ... |
| PE(TTM) | {price.pe_ttm} | {peer1.pe_ttm} | ... | ... | ... |
| ROE | {financials.roe}% | {peer1.roe}% | ... | ... | ... |
| 毛利率 | {financials.gross_margin}% | {peer1.gross_margin}% | ... | ... | ... |
| 营收增速 | {financials.revenue_yoy_pct}% | {peer1.revenue_yoy}% | ... | ... | ... |
| 利润增速 | {financials.net_profit_yoy_pct}% | {peer1.net_profit_yoy}% | ... | ... | ... |
| 1年涨幅 | {technicals.pct_1y:.1f}% | {peer1.pct_1y:.1f}% | ... | ... | ... |

> 📌 关键发现：
> 1. {指标对比中最突出的差距}
> 2. {估值层面}
> 3. {增长层面}
> 4. {1-2 条 Claude 总结}

---

**六、核心催化剂 & 风险**

**催化剂 🚀**
1. **{标题}**（{高/中高/中/低}影响）：{内容}
2. ...（3-5 条，通过 web_search 查近 30 天公告/新闻）

**风险 ⚠️**
1. **{标题}**（{高/中高/中/低}影响）：{内容}
2. ...（3-5 条）

---

**七、买卖建议 💡**
**整体判断：{一句话定性}**

**📌 短线（几天～2周）**
- 技术面：{超买/中性/超卖}、{多头/空头}排列
- **支撑位 {ma5 或 ma10}元 / 阻力位 {year_high}元**
- 操作建议：**{具体建议}**
- **止损参考 {数值}元**

**📌 中线（1～3个月）**
- 核心驱动力：{2-3 个关键变量}
- 估值判断：{高估/合理/低估}
- 中期支撑：**{ma20 或更远的价位}元**
- **建议：{具体操作}，目标看 {数值}元**
- 情景分析：乐观 {价位}（{条件}）/ 中性 {价位}（{条件}）/ 悲观 {价位}（{条件}）

**总结**
- 基本面：⭐{1-5}（{评价}）
- 题材概念：⭐{1-5}（{评价}）
- 技术面：⭐{1-5}（{评价}）
- 时机：⭐{1-5}（{评价}）

**一句话：{punchy 投资结论}**

---
*⚠️ 以上分析仅供参考，不构成投资建议。数据来源：腾讯财经（价量）、东方财富（板块+主营业务）、{meta.data_sources.fundamental_used}（基本面）。*
```

---

## 填写规则

### 涨跌定性
- `pct_today > 9.8%`（创业板/科创板 19.8%）→ "涨停"
- `pct_today < -9.8%` → "跌停"
- `pct_today > 0` → "上涨"
- `pct_today < 0` → "下跌"

### 市值
- 以"亿"为单位，保留 1 位小数
- `total_mv_yi` 字段已经是亿元

### PE 失真标注
- `pe_ttm < 0` → 加 "⚠️亏损股，PE失真"
- `pe_ttm > 200` → 加 "（估值极高）"
- `pe_ttm is None` → 写 "暂缺"

### ROE 定性
- `roe > 15%` → "优秀"
- `10% < roe ≤ 15%` → "良好"
- `5% < roe ≤ 10%` → "一般"
- `1% < roe ≤ 5%` → "较差"
- `roe ≤ 1%` → "极差" / "垫底"
- `roe < 0` → "⚠️亏损"

### 主营业务表
- 只列前 5 条（按收入排序）
- 如果有 "其他(补充)" 且占比 < 1%，可以合并或省略
- 如果 `by_product` 为空，用 `by_industry`
- `by_region` 只用一句话概述，不单独列表

### 同行业对比表
- 目标股放第一列，加粗
- 其余 3-5 列为 peer，按 `peer.source` 顺序排（先 industry 后 concept 后 theme）
- 任何 `None` / null 的单元格显示为 `-`
- 单位：市值亿元，其他按原数据

### 涨跌标记
- 正数增长加 `+` 号
- 负数保持负号

### 数据来源声明（末尾免责声明的一部分）
- 根据 `meta.data_sources.fundamental_used` 动态生成，例如：
  - `tushare` → "tushare pro（基本面）"
  - `akshare` → "akshare（基本面）"
  - `baostock` → "baostock（基本面）"
  - `eastmoney` → "东方财富数据中心（基本面）"
  - `null` (即 needs_websearch) → "网络公开资料（基本面）"

### 催化剂与风险
- 必须通过 `web_search` 查询近 30 天：`<n> 公告`, `<n> 澄清`, `<n> 利好`, `<n> 风险`, `<n> 股东减持`
- 特别关注紧急公告（澄清函、业绩预警、股东变动）
- 每条必须标注影响级别（高/中高/中/低）
- 遇到负面信息或澄清函，在"⚠️特别提醒"段单独突出

### 评分星级
- **基本面**：ROE + 毛利率 + 利润增速 + 债务负担
- **题材概念**：F10 ssbk 中概念板块数量 + 市场关注度
- **技术面**：均线 + 动量 + 量能（参考 technical_scoring.md）
- **时机**：是否超买 + 距支撑/阻力距离 + 波动率
