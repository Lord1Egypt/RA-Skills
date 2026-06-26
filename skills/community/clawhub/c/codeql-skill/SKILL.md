---
name: codeql
description: >
  CodeQL security audit pipeline: static scanning, SARIF triage, and QL query optimization.
  Trigger on: CodeQL, .ql, .sarif, taint tracking, source→sink, LGTM, GitHub Code Scanning,
  "scan this repo", "analyze this vulnerability", "optimize this query".
---

# CodeQL Security Audit Skill

Three independent modes — identify which one the user needs and run the corresponding script.

| User Intent | Mode | Script |
|-------------|------|--------|
| Scan a repo / create a DB / generate SARIF | **[SCAN]** | `scripts/scan.sh` |
| Read SARIF / triage vulns / generate report | **[AUDIT]** | `scripts/audit.py` |
| Optimize or debug a .ql query file | **[TUNE]** | `scripts/tune.py` |

---

## [SCAN]

```bash
bash scripts/scan.sh <repo_path> [language] [output.sarif]
# language: java | javascript | python | cpp | auto (default)
```

The script handles: language detection → build command selection → CodeQL DB creation → security suite scan → SARIF output.

For writing **custom queries**, refer to the relevant language reference:
`references/lang-java.md` / `lang-javascript.md` / `lang-python.md` / `lang-cpp.md`

---

## [AUDIT]

```bash
python3 scripts/audit.py <results.sarif> --output exp.md
```

The script handles: SARIF parsing → attack surface inventory → vuln family grouping → source→sink evidence chain extraction → exp.md output.

**Claude's responsibility** (what the script cannot do):
- Manually assess `[SUSPICIOUS]` entries with no data flow — determine if they are real vulnerabilities
- Write POC requests based on business context
- Provide concrete remediation code

---

## [TUNE]

```bash
python3 scripts/tune.py <query.ql>
```

The script outputs a tuning checklist covering seven checks: coverage, false positives, performance, and metadata completeness.

**Claude's responsibility** (what the script cannot do):
- Rewrite source / sink / sanitizer logic based on checklist findings
- Debug queries with no results or unexpected output — refer to `references/debugging.md`
