# Adapter: respiratory_weekly

```yaml
id: respiratory_weekly
name: 全国急性呼吸道传染病哨点监测情况
index_url: https://www.chinacdc.cn/jksj/jksj04_14275/
allowed_path_prefix: /jksj/jksj04_14275/
period_type: week
content_mode: html
title_pattern: '^(?<year>\d{4})年第(?<week>\d{1,2})周全国急性呼吸道传染病哨点监测情况$'
pagination_mode: semantic
transport_preference: browser_first
supports_issue_number: false
index_marker: 全国急性呼吸道传染病哨点监测情况
allowed_url_patterns:
  - '^https://www\.chinacdc\.cn/jksj/jksj04_14275/(?:index(?:_\d+)?\.html)?$'
  - '^https://www\.chinacdc\.cn/jksj/jksj04_14275/\d{6}/t\d+_\d+\.html$'
adapter_version: 2.0.0
```
