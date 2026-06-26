# 快速简报模板

适用于日常快速浏览，3-5 条核心新闻 + 一句话点评。

---

# 📈 财经新闻简报

**日期**: {{date}} | **来源**: {{sources}} | **总数**: {{total_count}} 条

---

## 🟢 利好消息 ({{positive_count}}条)

{% for item in positive[:5] %}
#### {{loop.index}}. [{{item.title}}]({{item.url}})
- **来源**: {{item.source}} | **时间**: {{item.time}}
- **影响**: 🟢 利好 | **置信度**: {{item.confidence|capitalize}}
- **相关股票**: {{item.affected_stocks|join(', ')}}
- **一句话**: {{item.summary}}

{% endfor %}

---

## 🔴 利空消息 ({{negative_count}}条)

{% for item in negative[:5] %}
#### {{loop.index}}. [{{item.title}}]({{item.url}})
- **来源**: {{item.source}} | **时间**: {{item.time}}
- **影响**: 🔴 利空 | **置信度**: {{item.confidence|capitalize}}
- **相关股票**: {{item.affected_stocks|join(', ')}}
- **一句话**: {{item.summary}}

{% endfor %}

---

## ⚪ 中性消息 ({{neutral_count}}条)

{% for item in neutral[:5] %}
#### {{loop.index}}. [{{item.title}}]({{item.url}})
- **来源**: {{item.source}} | **时间**: {{item.time}}

{% endfor %}

---

## 💡 投资提示

1. **重点关注**: {{focus_sectors|join('、')}}
2. **风险提醒**: {{risk_tips|join('、')}}
3. **明日事件**: {{upcoming_events}}

---

**免责声明**: 本简报仅供参考，不构成投资建议。投资有风险，决策需谨慎。
