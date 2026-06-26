# AUDIT LOG SCHEMA / 审计日志结构

Use JSON Lines format: one JSON object per line.

使用 JSON Lines 格式：每行一个 JSON 对象。

```json
{
  "audit_log_id": "AUDIT-YYYYMMDD-001",
  "timestamp": "",
  "operation": "search|receive_file|extract|stage|approve|archive|reject|block|upload|rule_change|synthesize",
  "record_id": "",
  "source_type": "",
  "source": "",
  "trust_level": "",
  "status_before": "",
  "status_after": "",
  "decision_by": "",
  "decision_reason": "",
  "archive_target": "",
  "notes": ""
}
```
