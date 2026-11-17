# Adapter: global_infectious_risk_monthly

```yaml
id: global_infectious_risk_monthly
name: 全球传染病事件风险评估报告
index_url: https://www.chinacdc.cn/jksj/jksj03/
allowed_path_prefix: /jksj/jksj03/
period_type: month
content_mode: pdf
title_pattern: '^(?<year>\d{4})\s*年\s*(?<month>\d{1,2})\s*月全球传染病事件风险评估(?:报告)?$'
pagination_mode: semantic
transport_preference: browser_first
supports_issue_number: false
index_marker: 全球传染病事件风险评估报告
allowed_url_patterns:
  - '^https://www\.chinacdc\.cn/jksj/jksj03/(?:index(?:_\d+)?\.html)?$'
  - '^https://www\.chinacdc\.cn/jksj/jksj03/\d{6}/P\d+\.pdf$'
adapter_version: 2.0.0
```
