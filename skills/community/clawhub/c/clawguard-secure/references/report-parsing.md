# Parse and summarize scan reports

Load when the user shares a scan report for analysis.

## Reading the Report

- Accept a JSON file path (use Read tool) or pasted JSON content directly.
- Accept compact website handoffs that begin with `CLAWGUARD_ANALYSIS_V1`.
- If Markdown format, extract score from the header and findings from sections.
- Handle both camelCase (browser export) and snake_case (API export) field names.
- Validate that `findings` is an array and `score` is 0-100 before proceeding.

## Compact Website Handoff

When the input contains `CLAWGUARD_ANALYSIS_V1`:

- Ignore the natural-language prompt above the marker for parsing purposes; use it only as user intent.
- Parse the JSON block after the marker first.
- Treat it as a compact, localized handoff exported from clawguardsecurity.ai.
- Prefer these fields in order:
  1. `focus_findings`
  2. `actionable_rule_ids`
  3. `summary`
  4. `report_meta`
- `focus_findings[].related_rules` already contains OC-to-OC rule chain context. Use it to explain why multiple findings amplify each other and which fixes should be grouped.
- Do not ask for a full JSON export unless the compact handoff is missing details the user explicitly needs.

Expected handoff shape:

```json
{
  "language": "en | zh-CN",
  "report_meta": {
    "report_id": "rpt_xxx",
    "scan_level": "L1 | L2 | L3A | L3B",
    "score": 58,
    "created_at": "2026-04-01T12:00:00Z",
    "platform": "browser | linux | windows | macOS",
    "execution_profile": "browser | quickscan_unix | quickscan_windows | local_client | control_plane",
    "rulepack_version": "2.x",
    "supported_rule_count": 100,
    "fully_checked_count": 62
  },
  "summary": {
    "severity_fail": { "CRITICAL": 1, "HIGH": 3, "MEDIUM": 0, "LOW": 0 },
    "severity_warn": { "CRITICAL": 0, "HIGH": 0, "MEDIUM": 2, "LOW": 1 },
    "best_effort_count": 2,
    "actionable_issue_count": 6,
    "needs_more_evidence_count": 12,
    "not_relevant_count": 20
  },
  "actionable_rule_ids": ["OC-001", "OC-011", "OC-034"],
  "focus_findings": [
    {
      "rule_id": "OC-001",
      "severity": "CRITICAL",
      "status": "fail",
      "coverage_status": "checked_fail",
      "title": "Localized title",
      "risk_summary": "Localized risk summary",
      "fix_summary": "Localized fix summary",
      "related_rules": [
        {
          "rule_id": "OC-011",
          "effect": "amplifies",
          "description": "Localized rule-chain description"
        }
      ]
    }
  ]
}
```

## JSON Schema (Key Fields)

```
ScanReport {
  score: number (0-100)
  scan_level: "L1" | "L2" | "L3A" | "L3B"
  execution_profile: string
  created_at: string (ISO 8601)
  rulepack_version: string
  report_id: string
  schema_version: string
  session_id: string | null
  platform: string
  findings: Finding[]
  coverage: CoverageItem[]
  severity_summary: { CRITICAL: n, HIGH: n, MEDIUM: n, LOW: n }
  category_summary: Record<string, number>  # maps category name to finding count
  coverage_summary: Record<CoverageStatus, number>
  metadata: { execution_profile, rulepack_id, rule_count, browser_profile_opt_in }
}

Finding {
  rule_id: string (e.g. "OC-001")
  title: string
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
  status: "pass" | "fail" | "warn" | "best_effort"
  coverage_status: "checked_pass" | "checked_fail" | "best_effort"
                 | "not_checked" | "not_applicable"
  message: string
  remediation: string
  evidence: EvidenceItem[]
  confidence: number
  compensatingControls: CompensatingControl[]
  attackScenario: string
  fixSuggestion: { action, patches[], description, configBefore?, configAfter? }
  alternativeFix: { action, description }
  aiHint: string
  relatedRuleEffects: RelatedRuleEffect[]
  environmentHint: { environment, signals[], confidence }
}
```

## Summary Generation Template

Output this format after reading:

```
## Scan Summary
- Score: {score}/100 (Grade: A/B/C/D/F based on 90/80/60/40 thresholds)
- Scan Mode: {scan_level}
- Date: {created_at}
- Rules Checked: {checked_pass + checked_fail} / {total coverage items}

### Severity Breakdown
| Severity | Failed | Warned | Passed |
| --- | --- | --- | --- |
| CRITICAL | n | n | n |
| HIGH | n | n | n |
| MEDIUM | n | n | n |
| LOW | n | n | n |

### Immediate Attention ({count})
(List all status=fail AND severity=CRITICAL or HIGH: rule_id - title)

### Next Steps
(1-2 actionable suggestions based on results)
```

Grade thresholds: A >= 90, B >= 80, C >= 60, D >= 40, F < 40.

> Note: `severity_summary` only has totals per severity. Compute the Failed/Warned/Passed columns by iterating `findings[]` and cross-tabulating severity x status, or use `{baseDir}/scripts/parse-report.py` which outputs pre-computed `severity_fail`, `severity_warn`, `severity_pass` breakdowns.

## Sorting Priority

Sort findings for display using this order:
1. Status weight: fail=0, warn=1, best_effort=2, pass=3
2. Severity weight: CRITICAL=0, HIGH=1, MEDIUM=2, LOW=3
3. Confidence: exact > heuristic (higher confidence first)

## Large Report Handling (50+ findings)

- **Pre-processing**: For reports with 50+ findings, run `{baseDir}/scripts/parse-report.py <file>` first. Use its summary JSON (score, severity counts, urgent items) for Layer 1. Only read the full JSON if the user requests details.
- **Layer 1** (always show): Summary above -- score, severity table, top critical/high fails.
- **Layer 2** (on request): Category breakdown table from `category_summary`.
- **Layer 3** (on request): Individual finding details with evidence and remediation.
- Never dump all findings at once.
- Prompt: "Want to drill into a specific category or finding?"

## Report Comparison

When the user provides two reports:
- Show score delta and direction.
- List new fails, resolved fails, and degraded items (pass/warn -> fail).
- Show coverage changes (rules added/removed).
- Warn if `rulepack_version` differs between reports.
- Warn if `scan_level` differs (L1 vs L2 have different coverage scope).

## Field Notes

- `evidence[].redacted === true`: Value is masked. Tell user to check locally.
- `not_checked` does NOT mean safe. Always mention unchecked rule count in summary.
- `best_effort` means incomplete evidence. Flag reliability concern for those findings.
- `compensatingControls`: If present, note them when discussing a fail -- they may reduce effective risk.
- `environmentHint`: Use to contextualize findings (dev vs staging vs prod).
- `category_summary`: A flat map of category name to finding count. Use it to show per-category totals, not per-status breakdowns.
