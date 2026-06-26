# Documentation Prompt

> Copy and paste this prompt into any AI chat window to generate documentation for the AI Company skill.

---

## Prompt

```
Generate documentation for the AI Company unified skill (v5.0.0).

Structure the documentation as follows:
```

## 1. Overview

- Skill name, version, purpose
- Consolidation history (16 skills → 1)
- Department structure (11 departments)

## 2. Department Reference

For each department, document:
- Name, slug, contained roles
- Core responsibilities (brief)
- Key error codes
- Integration points with other departments
- AIGC labeling requirements

| Department | Roles | Key Error Codes |
|-----------|-------|----------------|
| Governance & Strategy | CEO, COO, HQ | CEO_001-004, COO_001-003, HQ_001-004 |
| Finance & Risk | CFO, CRO | CFO_001-003, CRO_001-003 |
| Technology & Engineering | CTO | CTO_001-005 |
| Platform & Infrastructure | Framework | FW_001-010 |
| Security & Compliance | CISO, CLO | CISO_001-004, CLO_001-005 |
| People & Culture | CHO | CHO_001-004 |
| Marketing & Partnerships | CMO | CMO_001-004 |
| Quality & Operations | CQO, PMGR | CQO_001-004, PMGR_001-004 |
| Intelligence | Intel | INTEL_001-005 |
| Information Services | Info | INFO_001-005 |
| Translation & Localization | Translator | TR_001-004 |

## 3. Shared Code Templates Reference

10 templates with function signatures, security markers, and usage examples.

## 4. Prompt Frameworks

CRISPE, 3WEH, Five-Element — when to use each, variable reference.

## 5. Compliance Guide

- VirusTotal/ClawHub security check matrix
- AIGC labeling requirements (explicit + implicit)
- Progressive disclosure strategy (L1/L2/L3)
- L1-L6 harness compliance checklist

## 6. Migration Guide

From individual skills (v3.x) to unified skill (v5.0):
- Department parameter replaces individual skill slug
- Error codes unchanged (department prefix preserved)
- All triggers consolidated

Format: Markdown. English only.

---

*Copy-paste ready for any AI chat window.*