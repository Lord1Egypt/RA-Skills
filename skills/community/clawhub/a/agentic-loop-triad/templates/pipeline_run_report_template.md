# Pipeline Run Report

**Run ID:** `{{pipeline_run_id}}`
**Goal:** {{goal}}
**Cycle:** {{cycle}}
**Generated:** {{generated_at}}

---

## Summary

| Metric | Value |
| :--- | :--- |
| Performance Score | {{summary.performance_score}} |
| Alignment Score | {{summary.alignment_score}} |
| Drift Score | {{summary.drift_score}} ({{summary.drift_severity}}) |
| Suggestions | {{summary.suggestions_count}} |
| Regression Tests Generated | {{summary.regression_tests_generated}} |
| Improvement Chain Length | {{summary.chain_length}} |

**Next Action:** `{{next_action}}`

---

## Paradigm Shifts Activated

### Shift 1: Specification Drift Detection
- **Drift Score:** {{paradigm_shifts.drift_detection.drift_score}}
- **Severity:** {{paradigm_shifts.drift_detection.severity}}
- **Action:** {{paradigm_shifts.drift_detection.action}}
- **Dimensions:**
  - Performance drift: {{paradigm_shifts.drift_detection.dimensions.performance_drift}}
  - Alignment drift: {{paradigm_shifts.drift_detection.dimensions.alignment_drift}}
  - Behavioral drift: {{paradigm_shifts.drift_detection.dimensions.behavioral_drift}}
  - Temporal drift: {{paradigm_shifts.drift_detection.dimensions.temporal_drift}}

### Shift 2: Meta-Learning
- **Applied:** {{paradigm_shifts.meta_learning_applied}}

### Shift 3: Autonomous Re-specification
- **Triggered:** {{paradigm_shifts.auto_revised}}

### Shift 4: Cross-Goal Transfer
- **Applied:** {{paradigm_shifts.transfer_applied}}

### Shift 5: Improvement Chain
- **Chain Link Hash:** `{{paradigm_shifts.chain_link.report_hash}}`
- **Previous Hash:** `{{paradigm_shifts.chain_link.previous_hash}}`
- **Timestamp:** {{paradigm_shifts.chain_link.timestamp}}

---

## Output Files

| File | Path |
| :--- | :--- |
| Specification | `{{outputs.specification}}` |
| Outcome Report | `{{outputs.outcome_report}}` |
| Observation | `{{outputs.observation}}` |
| Analysis | `{{outputs.analysis}}` |
| Improvement Report | `{{outputs.improvement_report}}` |
| Improvement Chain | `{{outputs.improvement_chain}}` |
| Pipeline State | `{{outputs.pipeline_state}}` |

---

## Integrity

**SHA-256:** `{{integrity.sha256}}`
**Signed At:** {{integrity.signed_at}}
