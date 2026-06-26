---
name: gh-skillscan
description: "Scan an OpenClaw SKILL.md file for security threats before installing it. Posts the raw SKILL.md content and gets back a safety score (0-1), detected threat patterns (credential harvesting, data exfiltration, obfuscated commands, permission overreach), and a SAFE/CAUTION/DANGEROUS verdict."
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# SkillScan

Check if a SKILL.md is safe before you install it.

## Start the server

```bash
uvicorn skillscan.app:app --port 8001
```

## Scan a SKILL.md file

```bash
curl -s -X POST http://localhost:8001/v1/scan-skill \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat path/to/SKILL.md | jq -Rs)}" | jq
```

Returns `safety_score` (1.0 = safe, 0.0 = dangerous), `findings` (list of threat names), `verdict` (SAFE/CAUTION/DANGEROUS), and `skill_name`.

## What it detects

- `credential_harvesting` — accessing $API_KEY, $TOKEN, $SECRET, $PASSWORD
- `data_exfiltration` — curl/wget sending data to external URLs
- `obfuscated_command` — base64 decode piped to bash, eval, exec
- `permission_overreach` — accessing /etc/shadow, .ssh/, reverse shells

## Example: scan before install

```bash
clawdhub inspect some-skill > /tmp/skill.md
VERDICT=$(curl -s -X POST http://localhost:8001/v1/scan-skill \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat /tmp/skill.md | jq -Rs)}" | jq -r '.verdict')
echo "Verdict: $VERDICT"
```
