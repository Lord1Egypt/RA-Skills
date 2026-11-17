# Adapter: china_public_health_risk_monthly

```yaml
id: china_public_health_risk_monthly
name: 重点传染病和突发公共卫生事件风险评估报告
index_url: https://www.chinacdc.cn/jksj/jksj02/
allowed_path_prefix: /jksj/jksj02/
period_type: month
content_mode: pdf
title_pattern: '^(?<year>\d{4})\s*年\s*(?<month>\d{1,2})\s*月中国需关注的突发公共卫生事件风险评估(?:报告)?$'
pagination_mode: semantic
transport_preference: browser_first
supports_issue_number: false
index_marker: 重点传染病和突发公共卫生事件风险评估报告
allowed_url_patterns:
  - '^https://www\.chinacdc\.cn/jksj/jksj02/(?:index(?:_\d+)?\.html)?$'
  - '^https://www\.chinacdc\.cn/jksj/jksj02/\d{6}/P\d+\.pdf$'
adapter_version: 2.0.0
```
