# 详细参考 - auto-file-organizer-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (yaml)

```yaml
organizer:
  version: "1.0"
  language: zh
  log_file: ~/organizer-pro.log

scan:
  paths:
    - ~/Downloads/
    - ~/Desktop/
    - ~/Documents/
  schedule: "0 9 * * *"
  incremental: true
  exclude: [".DS_Store", "Thumbs.db", "*.tmp", "*.crdownload", ".git/"]

dedup:
  enabled: true
  strategy: keep_latest
  hash_algorithm: sha256
  min_size: 1KB
  scan_paths: [~/Documents/, ~/Downloads/]

smart_classify:
  enabled: true
  rules: rules/smart-rules.yaml
  content_aware: true
  min_confidence: 0.8

watch:
  enabled: true
  paths: [~/Downloads/]
  auto_organize: true
  debounce_seconds: 5
  daemon: true

report:
  format: [html, pdf]
  output: ~/reports/organizer/
  retention_days: 90
  monthly_summary: true

schedule:
  tasks:
    - name: 每日整理
      cron: "0 9 * * *"
      paths: [~/Downloads, ~/Desktop]
      actions: [organize, dedup]
    - name: 每周深度清理
      cron: "0 10 * * 0"
      paths: [~/Documents/]
      actions: [organize, dedup, smart_classify]

team:
  shared_rules: rules/team-rules.yaml
  sync_interval: "0 0 * * 0"
  audit: quarterly
```

## 代码示例 (yaml)

```yaml
organizer:
  version: "1.0"
  language: zh

scan:
  paths:
    - ~/Downloads/
    - ~/Desktop/
    - ~/Documents/
  schedule: "0 9 * * *"
  incremental: true
  exclude: [".DS_Store", "Thumbs.db", "*.tmp", "*.crdownload"]

dedup:
  enabled: true
  strategy: keep_latest
  hash_algorithm: sha256
  scan_paths: [~/Documents/, ~/Downloads/]
  min_size: 1KB

smart_classify:
  enabled: true
  rules: rules/smart-rules.yaml
  content_aware: true

watch:
  enabled: true
  paths: [~/Downloads/]
  auto_organize: true
  debounce_seconds: 5

report:
  format: [html, pdf]
  output: ~/reports/
  retention_days: 90

team:
  shared_rules: rules/team-rules.yaml
  sync_interval: "0 0 * * 0"
```

## 代码示例 (yaml)

```yaml
rules:
  - name: 财务文档识别
    type: content_aware
    match:
      content_keywords: [发票, 收据, 账单, 报销, 财务]
      file_types: [pdf, jpg, png]
    target: 财务文档/

  - name: 合同文档识别
    type: content_aware
    match:
      content_keywords: [合同, 协议, 甲方, 乙方, 签约]
      file_types: [pdf, docx]
    target: 合同文档/

  - name: 身份证件识别
    type: content_aware
    match:
      content_keywords: [身份证, 护照, 驾驶证]
      file_types: [jpg, png]
      min_confidence: 0.8
    target: 证件/ (加密存储)
    encrypt: true

  - name: 项目截图识别
    type: contextual
    match:
      filename_pattern: "Screenshot*|截图*|Screen*"
      recent_days: 7
    target: 项目截图/
```

