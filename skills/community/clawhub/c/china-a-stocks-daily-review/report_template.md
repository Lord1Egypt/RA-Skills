# 📊 盘后复盘报告 {{VERSION}} · {{DATE}}（{{REPORT_TIME}}）

> 本报告由 `render_report.py` 自动渲染生成。取数耗时：并发 {{T_CONCURRENT}}s，总耗时 {{T_TOTAL}}s。

---

## 今日核心：{{CORE_THEME}}

---

### 📈 一、指数全天表现

**收盘数据（新浪财经 hq.sinajs.cn）：**

| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|:---:|:---:|:---:|:---:|
{{INDEX_TABLE_ROWS}}

**全市场成交额：约 {{TOTAL_AMOUNT}} 万亿**（较昨日约 {{PREV_AMOUNT}} 万亿 {{AMOUNT_CHANGE}}，资金{{FUND_MOOD}}）

**vs 盘中预判对比：**

| 项目 | 盘中报告 | 实际收盘 | 偏差 |
|:---:|:---:|:---:|:---:|
{{PRE_MARKET_VS}}

---

### 💰 二、资金动向

**北向资金：** {{NORTH_MONEY_STR}}
**南向资金：** {{SOUTH_MONEY}}
**央行流动性：** {{CENTRAL_BANK}}

---

### 🌡️ 三、市场情绪（AKShare stock_market_activity_legu）

| 指标 | 数据 | 解读 |
|:---|:---:|:---|
{{EMOTION_TABLE_ROWS}}

---

### 🔥 四、连板梯队（并发取数 {{T_CONCURRENT}}s 完成）

连板总数：**{{LIANBAN_TOTAL}} 家**（{{LIANBAN_STRUCT}}）

{{LIANBAN_TABLE}}

---

### 🏷️ 五、板块复盘

**领涨板块（按强度排序）：**

{{SECTOR_HOT_ROWS}}

**领跌板块：**

{{SECTOR_WEAK_ROWS}}

---

### 📝 六、今日小结与明日策略

**今日定性：**

{{DAILY_SUMMARY}}

**进攻方向：**

{{OFFENSIVE_STRATEGY}}

**防守方向：**

{{DEFENSIVE_STRATEGY}}

**关键观察点（明日）：**

{{KEY_OBSERVATIONS}}

---

### ⚠️ 风险提示

{{RISK_WARNING}}

---

**数据来源：** 新浪财经（指数）· AKShare（涨停池/市场活动/炸板池）· 财联社快讯
**取数脚本：** `fetch_review_v2.py`（5项并发，{{T_TOTAL}}s）
**渲染脚本：** `render_report.py`
**报告生成时间：** {{RENDER_TIME}}
