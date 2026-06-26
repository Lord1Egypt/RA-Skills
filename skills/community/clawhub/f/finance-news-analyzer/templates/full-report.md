# 深度分析报告模板

适用于详细分析，包含数据支撑、趋势分析、投资建议。

---

# 📊 深度分析报告：{{report_title}}

**报告日期**: {{date}}  
**分析周期**: {{period}}  
**新闻来源**: {{sources}}  
**分析新闻数**: {{total_count}} 条

---

## 📌 核心观点

{{core_insights}}

---

## 📈 新闻情感分布

| 情感 | 数量 | 占比 |
|------|------|------|
| 🟢 利好 | {{positive_count}} | {{positive_pct}}% |
| ⚪ 中性 | {{neutral_count}} | {{neutral_pct}}% |
| 🔴 利空 | {{negative_count}} | {{negative_pct}}% |

![情感分布](chart_sentiment.png)

---

## 🔍 关键事件时间线

{% for event in timeline %}
- **{{event.date}}**: {{event.title}} ({{event.impact}})
{% endfor %}

---

## 🏢 行业分析

### {{industry_name}}

**行业情感**: {{industry_sentiment}}  
**主要驱动因素**:
{% for driver in industry_drivers %}
- {{driver}}
{% endfor %}

**重点公司**:
| 公司 | 代码 | 情感 | 影响 |
|------|------|------|------|
{% for company in key_companies %}
| {{company.name}} | {{company.ticker}} | {{company.sentiment_label}} | {{company.impact}} |
{% endfor %}

---

## 📊 数据支撑

### 财务指标影响

| 指标 | 影响方向 | 影响程度 | 置信度 |
|------|----------|----------|--------|
| 营收预期 | {{revenue_impact}} | {{revenue_magnitude}} | {{revenue_confidence}} |
| 利润预期 | {{profit_impact}} | {{profit_magnitude}} | {{profit_confidence}} |
| 估值水平 | {{valuation_impact}} | {{valuation_magnitude}} | {{valuation_confidence}} |

### 市场情绪指标

- **恐慌/贪婪指数**: {{fear_greed_index}}
- **VIX 指数**: {{vix}}
- **成交量变化**: {{volume_change}}

---

## 💼 投资建议

### 短期（1-3 天）

**策略**: {{short_term_strategy}}

**关注标的**:
{% for stock in short_term_stocks %}
- {{stock.ticker}}: {{stock.reason}}
{% endfor %}

### 中期（1-4 周）

**策略**: {{medium_term_strategy}}

**关注标的**:
{% for stock in medium_term_stocks %}
- {{stock.ticker}}: {{stock.reason}}
{% endfor %}

### 长期（3 月+）

**策略**: {{long_term_strategy}}

**关注标的**:
{% for stock in long_term_stocks %}
- {{stock.ticker}}: {{stock.reason}}
{% endfor %}

---

## ⚠️ 风险提示

{% for risk in risks %}
{{loop.index}}. **{{risk.title}}**: {{risk.description}}
{% endfor %}

---

## 📚 参考资料

{% for ref in references %}
- [{{ref.title}}]({{ref.url}})
{% endfor %}

---

**分析师**: AI 财经分析师  
**免责声明**: 本报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。
