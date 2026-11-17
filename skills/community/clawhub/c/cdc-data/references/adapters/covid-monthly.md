# Adapter: covid_monthly

```yaml
id: covid_monthly
name: 全国新型冠状病毒感染疫情情况
index_url: https://www.chinacdc.cn/jksj/xgbdyq/
allowed_path_prefix: /jksj/xgbdyq/
period_type: month
content_mode: html
title_pattern: '^全国新型冠状病毒感染疫情情况[（(](?<year>\d{4})年(?<month>\d{1,2})月[）)]$'
pagination_mode: semantic
transport_preference: browser_first
supports_issue_number: false
index_marker: 全国新型冠状病毒感染疫情情况
allowed_url_patterns:
  - '^https://www\.chinacdc\.cn/jksj/xgbdyq/(?:index(?:_\d+)?\.html)?$'
  - '^https://www\.chinacdc\.cn/jksj/xgbdyq/\d{6}/t\d+_\d+\.html$'
adapter_version: 2.0.0
```
