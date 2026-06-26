---
name: gh-securitysuite
description: "Comprehensive agent security platform with 7 endpoints. Scan text for injection, audit SKILL.md files for malware and scope issues, generate detailed security reports with severity ratings and recommendations, browse the pattern catalog, or batch-audit multiple skills at once."
metadata: {"openclaw":{"emoji":"🏛️","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml"]}]}}
---

# SecuritySuite

Full security platform for AI agents. Seven endpoints, one server.

## Start the server

```bash
uvicorn securitysuite.app:app --port 8010
```

## Endpoints

### Scan text for prompt injection

```bash
curl -s -X POST http://localhost:8010/v1/scan-text \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the weather?"}' | jq
```

### Audit a SKILL.md (full check)

```bash
curl -s -X POST http://localhost:8010/v1/audit \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat SKILL.md | jq -Rs)}" | jq
```

### Generate a security report with recommendations

```bash
curl -s -X POST http://localhost:8010/v1/report \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat SKILL.md | jq -Rs)}" | jq
```

Returns `overall_rating`, `risk_level` (LOW/MEDIUM/HIGH/CRITICAL), `summary`, `findings_by_severity`, `recommendations`, and `details` (each finding with category, severity, description, and fix).

### List all known attack patterns

```bash
curl -s http://localhost:8010/v1/patterns | jq '.patterns[] | "\(.severity): \(.name) — \(.description)"' -r
```

### Batch audit multiple skills

```bash
curl -s -X POST http://localhost:8010/v1/batch \
  -H "Content-Type: application/json" \
  -d "{\"skills\": [$(cat skill1.md | jq -Rs), $(cat skill2.md | jq -Rs)]}" | jq
```

Returns `results` (verdict per skill), `safe_count`, and `flagged_count`.
