# Unified metric schema

Schema version: `1.0`.

Every metric requires:

```text
metric_id, topic, pathogen, population, region, data_period,
value, unit, denominator, methodology, source_report_type,
source_location, extraction_method, confidence
```

Preserve original strings beside parsed values. `source_location` includes page/table/figure or DOM locator meaningful to a reader. Use `extraction_method` from `dom`, `native_text`, `native_table`, `ocr`, or `chart_digitization`.

Before cross-report comparison, check metric meaning, pathogen, population, geography, data period, value type, unit, denominator, sampling/surveillance design, and methodology. Compare only compatible values. Explain differences or refuse direct aggregation when any material dimension is incompatible.
