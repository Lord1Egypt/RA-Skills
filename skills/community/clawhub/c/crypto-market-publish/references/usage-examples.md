# Usage Examples

All examples assume you're in your crypto workspace directory.

## Scenario 1: Daily Economic Report

**Need:** User wants to see upcoming important economic data for the next week.

**From crypto workspace:**
```bash
cd economic
python3 daily_economic_report_v2.py
```

**Output:**
```
📅 **Daily Economic Data Forecast** 📅
🕐 2026-03-13 21:30

📊 **Next 7 Days - High Importance**

📊 CPI Consumer Price Index
🕐 2026-04-14 21:30
📊 Expected: 2.3% | Previous: 2.4%
⏰ 31 days 23 hours remaining
```

## Scenario 2: Update CPI Actual Value

**Need:** CPI data released, actual is 2.1% (lower than expected 2.3%). Update and analyze impact.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py update "CPI 消费者价格指数" "2.1%" --datetime "2026-03-13 21:30"
```

**Output:**
```
📝 Update Economic Data Actual Value
================================================================================
Name: CPI 消费者价格指数
Actual: 2.1%
Release Time: 2026-03-13 21:30

✅ Actual value saved

📊 Impact Analysis:
================================================================================

**🟢 CPI 消费者价格指数**

📊 Actual: **2.1%**
📌 Expected: 2.3%
📌 Previous: 2.4%

**Market Impact**: 🟢 Bullish 🟢
**Impact Strength**: Strong 💪
**Analysis**: Actual 2.10 below expected -8.7%, inflation/unemployment pressure relief

💡 **Suggestion**: 🟢 Bullish data, market sentiment may turn positive
```

## Scenario 3: Quick Analysis (No Save)

**Need:** Quick impact check without saving to database.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py analyze "Non-Farm Payrolls" "+280K" "+200K" "+256K"
```

**Output:**
```
📊 Economic Data Analysis
================================================================================

**🟢 Non-Farm Payrolls**

📊 Actual: **+280K**
📌 Expected: +200K
📌 Previous: +256K

**Market Impact**: 🟢 Bullish 🟢
**Impact Strength**: Strong 💪
**Analysis**: Actual 280,000 above expected +40.0%, strong economy

💡 **Suggestion**: 🟢 Bullish data, market sentiment may turn positive
```

## Scenario 4: View Updated Data

**Need:** Check all economic data with actual values.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py list
```

**Output:**
```
📋 Updated Economic Data:
================================================================================

📊 CPI Consumer Price Index
   Actual: 2.1%
   Updated: 2026-03-13 21:30

👷 Non-Farm Payrolls
   Actual: +280K
   Updated: 2026-03-14 21:30
```

## Scenario 5: Comprehensive Monitoring

**Need:** Get crypto price monitoring and upcoming economic data.

**From crypto workspace:**
```bash
cd scripts
python3 crypto_monitor_telegram.py
```

**Output:**
```
=======================================================
📊 Crypto Market Monitor - 2026-03-13 21:30
=======================================================

🌍 Global Market Overview
-------------------------------------------------------
Total Market Cap: $2.53T (+2.29%)
24h Volume: $120.42B
BTC Dominance: 57.1%

😊 Market Sentiment: 🚀 Extremely Greedy

⚠️ Price Volatility Alerts (±5%):
-------------------------------------------------------
🚀 DOGE: 24h change +5.53%
    Current Price: $0.0999

💰 Major Tokens
-------------------------------------------------------
📈 BTC $72,291.00 +2.54%
...

📅 Economic Data Reminder

📊 CPI Consumer Price Index
🕐 2026-03-13 21:30
📊 Expected: 2.3%
📈 Actual: **2.1%**
🟢 **Bullish** 🟢 (Strong 💪)
💡 Actual 2.10 below expected -8.7%, inflation/unemployment pressure relief

⚠️ Prepare your positions
```

## Scenario 6: Bearish Data Analysis

**Need:** GDP released, actual 1.8% below expected 2.0%. Analyze impact.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py analyze "GDP 季度报告" "1.8%" "2.0%" "1.6%"
```

**Output:**
```
📊 Economic Data Analysis
================================================================================

**🔴 GDP 季度报告**

📊 Actual: **1.8%**
📌 Expected: 2.0%
📌 Previous: 1.6%

**Market Impact**: 🔴 Bearish 🔴
**Impact Strength**: Strong 💪
**Analysis**: Actual 1.80 below expected -10.0%, weak economy

⚠️ **Suggestion**: 🔴 Bearish data, market volatility may increase
```

## Scenario 7: Unemployment Rate Analysis

**Need:** Unemployment rate released, actual 4.0% above expected 3.8%.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py analyze "失业率" "4.0%" "3.8%" "3.7%"
```

**Output:**
```
📊 Economic Data Analysis
================================================================================

**🔴 失业率**

📊 Actual: **4.0%**
📌 Expected: 3.8%
📌 Previous: 3.7%

**Market Impact**: 🔴 Bearish 🔴
**Impact Strength**: Strong 💪
**Analysis**: Actual 4.00 above expected +5.3%, inflation/unemployment pressure increases

⚠️ **Suggestion**: 🔴 Bearish data, market volatility may increase
```

## Scenario 8: Neutral Data Analysis

**Need:** Retail sales released, actual 0.3% close to expected 0.4%.

**From crypto workspace:**
```bash
cd economic
python3 update_economic_data.py analyze "零售销售月率" "0.3%" "0.4%" "0.5%"
```

**Output:**
```
📊 Economic Data Analysis
================================================================================

**🟡 零售销售月率**

📊 Actual: **0.3%**
📌 Expected: 0.4%
📌 Previous: 0.5%

**Market Impact**: 🟡 Neutral 🟡
**Impact Strength**: Weak 📊
**Analysis**: Actual 0.30 close to expected -25.0%, limited impact

📊 **Suggestion**: 🟡 Neutral data, market reaction may be limited
```

## Common Questions

**Q: How to know upcoming data?**
A: Run `python3 daily_economic_report_v2.py` from economic/ to see 7-day forecast.

**Q: How long for updates to take effect?**
A: Immediately. Next run of `daily_economic_report_v2.py` or `crypto_monitor_telegram.py` will show analysis.

**Q: Can I update duplicate data?**
A: Yes. Running update command again will overwrite previous data.

**Q: Does bullish mean I must buy?**
A: No. Bullish means data itself is market-positive, actual reaction may vary. Combine with technicals and risk management.

**Q: How to clear all data?**
A: Delete data file:
```bash
rm data/actual_data.json
```

## Best Practices

1. **Update promptly** - Within 10-15 minutes of data release
2. **Accurate sources** - Reliable news sites, official releases, or trading platforms
3. **Comprehensive analysis** - Don't just look at one indicator, consider overall market
4. **Risk management** - Be cautious before/after major data releases
5. **Observation** - Compare analysis with actual market reaction, build experience
