# Improvement Report — Cycle {{cycle}}

**Report ID:** {{report_id}}
**Generated:** {{generated_at}}
**Mode:** {{mode}}
**Goal:** {{goal}}

---

## Summary

| Metric | Value |
| :--- | :--- |
| Health | {{health}} |
| Performance Score | {{performance_score}} |
| Alignment Score | {{alignment_score}} |
| Regression Detected | {{regression_detected}} |
| Total Suggestions | {{total_suggestions}} |
| Critical Suggestions | {{critical_suggestions}} |
| Regression Tests Generated | {{regression_tests_generated}} |

---

## Suggestions

{{#each suggestions}}
### [{{priority}}] {{suggestion}}
{{/each}}

---

## Alignment Violations

{{#each alignment.violations}}
- {{this}}
{{/each}}

---

## Auto-Generated Regression Tests

{{#each regression_tests}}
**{{test_id}}:** {{description}}
- Input: `{{input}}`
- Expected: `{{expected_output}}`
{{/each}}

---

## Next Steps

{{#each next_steps}}
{{@index}}. {{this}}
{{/each}}

---

**Integrity SHA-256:** `{{integrity.sha256}}`
