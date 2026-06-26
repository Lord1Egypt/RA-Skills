# 📊 LLM 监控日报 - 模板

## 今日概览

| 指标 | 数值 | 环比 |
|------|------|------|
| 会话数 | {{session_count}} | {{session_count_change}} |
| 总Token消耗 | {{total_tokens}} | {{total_tokens_change}} |
| 平均健康分 | {{avg_health_score}} | {{avg_health_score_change}} |
| 首通率 | {{first_try_rate}}% | {{first_try_rate_change}} |
| 总返工次数 | {{total_rework}} | {{total_rework_change}} |

## 健康状态

{{status_emoji}} **{{status_label}}**

```
{{score_bar}}
```

## 问题分析

{{problem_analysis}}

## 优化建议

{{suggestions}}

---
*日报生成时间: {{timestamp}}*
