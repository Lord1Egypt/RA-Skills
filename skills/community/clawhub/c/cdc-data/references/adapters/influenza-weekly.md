# Adapter: influenza_weekly

```yaml
id: influenza_weekly
name: 中国流感监测周报
index_url: https://www.chinacdc.cn/jksj/jksj04_14249/
allowed_path_prefix: /jksj/jksj04_14249/
period_type: week
content_mode: html_with_pdf
title_pattern: '^(?<year>\d{4})年第(?<week>\d{1,2})周第(?<issue>\d{1,4})期中国流感监测周报$'
pagination_mode: semantic
transport_preference: browser_first
supports_issue_number: true
index_marker: 流感监测周报
allowed_url_patterns:
  - '^https://www\.chinacdc\.cn/jksj/jksj04_14249/(?:index(?:_\d+)?\.html)?$'
  - '^https://www\.chinacdc\.cn/jksj/jksj04_14249/\d{6}/t\d+_\d+\.html$'
  - '^https://www\.chinacdc\.cn/jksj/jksj04_14249/\d{6}/P\d+\.pdf$'
adapter_version: 2.0.0
```
