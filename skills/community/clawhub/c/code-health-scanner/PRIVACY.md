# 🔒 Privacy & Data Governance — Code Health Scanner

> **Last updated:** 2026-06-18
> **Applies to:** v1.0.1+

---

## 1. What This Skill Does

Code Health Scanner reads your Spring Boot project code and generates a health report:

| Data Category | What | Where | Stored For |
|---------------|------|-------|------------|
| Code analysis | Reads project source files | Your project directory | Duration of scan only |
| Health report | Structured report with findings | `{project}/health-report.md` | Until you delete |

---

## 2. What This Skill NEVER Does

- ❌ Send your code to third-party servers
- ❌ Upload scan results to cloud services
- ❌ Modify your code without explicit confirmation
- ❌ Exfiltrate credentials or environment variables
- ❌ Perform any network calls (100% offline)
