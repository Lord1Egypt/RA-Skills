# Report object schema

Schema version: `2.0`.

```json
{
  "schema_version": "2.0",
  "report_id": "influenza_weekly-2026-W28-I917",
  "report_type": "influenza_weekly",
  "period_type": "week",
  "reporting_period": {"year": 2026, "week": 28, "month": null},
  "data_periods": [],
  "issue_number": 917,
  "publish_date": "2026-07-16",
  "title": "2026年第28周第917期中国流感监测周报",
  "detail_url": "https://www.chinacdc.cn/...html",
  "document_url": "https://www.chinacdc.cn/...pdf",
  "content_mode": "html_with_pdf",
  "source_page_url": "https://www.chinacdc.cn/jksj/jksj04_14249/",
  "attachments": [],
  "verification": {"verified": true, "method": "title_and_carrier", "warnings": []}
}
```

The normalized list record always contains these twelve fields: `report_type`, `period_type`, `period_year`, `period_week`, `period_month`, `issue_number`, `publish_date`, `title`, `detail_url`, `document_url`, `content_mode`, and `source_page_url`.

Use null for inapplicable scalar fields. Keep `data_periods` separate from `reporting_period`. Generate `report_id` deterministically: weekly `{type}-{year}-W{week:02}-I{issue|NA}`; monthly `{type}-{year}-M{month:02}-INA`.

Each attachment has `name`, `url`, `type` (`pdf|word|excel|unknown`), and `language` (`zh|en|bilingual|unknown`).
