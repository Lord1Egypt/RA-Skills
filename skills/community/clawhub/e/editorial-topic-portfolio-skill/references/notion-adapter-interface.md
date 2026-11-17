# Notion Adapter Interface

## Boundary

The adapter is a private connector layer. The reusable Skill must not contain a real token, database ID, page ID, or private field mapping.

## Inputs

```yaml
NOTION_TOKEN: environment variable or secure credential resolver
NOTION_TOPIC_DATABASE_ID: private database ID
NOTION_TOPIC_MAPPING: private JSON mapping
```

The mapping must define:

```json
{
  "title": "选题标题",
  "lifecycle": "状态",
  "priority": "推荐优先级",
  "date": "日期",
  "competition": "竞争密度",
  "originality": "原创性评估",
  "value": "价值判断",
  "reason": "推荐原因",
  "angle": "建议角度",
  "risk": "风险提醒",
  "fit": "定位匹配度",
  "reviewDate": "评估日期"
}
```

## Read flow

1. Load token and database ID from secure configuration.
2. Query pages with pagination.
3. Convert Notion properties into the standard topic record.
4. Preserve page ID, last edited time and original text fields.
5. Do not infer lifecycle or priority from title text.

## Write flow

1. Accept only an approved change set containing page IDs.
2. Print a diff preview before any write.
3. Update lifecycle, priority, evaluation fields and the idempotent evaluation block.
4. Keep original user material outside the current evaluation block.
5. Record success, failure and skipped pages separately.
6. Query the same page IDs again and compare the expected fields.

## Failure handling

- Missing token or mapping: stop without writing.
- Ambiguous page ID: stop and request a change-set correction.
- API failure: retry once, then use a different HTTP path or report both results.
- Partial batch failure: stop the batch, do not blindly retry successful pages.
- Readback mismatch: mark unresolved and do not report the batch as complete.

## Security

- Never hardcode credentials.
- Never log token values.
- Never send the full database or private notes to an external service except the configured Notion API.
- Dry-run and preview modes must not issue PATCH requests.
