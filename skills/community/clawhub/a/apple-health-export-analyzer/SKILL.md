---
name: health-analyzer-mac-local
description: Use the Health Data AI Analyzer Mac app read-only localhost API on macOS to generate a concise Apple Health daily brief and 3 practical suggestions. Only run when the user explicitly asks to analyze their imported health data. If local fetch is unavailable, ask for one exact curl response and continue from that JSON.
homepage: https://clawhub.ai/
user-invocable: true
metadata:
  openclaw:
    os:
      - darwin
---

# Health Data AI Analyzer
Use this skill only with the Health Data AI Analyzer Mac app.

Use it for:
- daily health briefs
- 3 practical non-medical suggestions
- simple recent step and sleep comparisons

Preferred source of truth:
- `http://127.0.0.1:8765/openclaw/status`
- `http://127.0.0.1:8765/openclaw/daily-brief?date=YYYY-MM-DD`

Rules:
- Use this skill only when the user explicitly asks for a health brief, comparison, or summary from their own imported data.
- Treat the local Health Data AI Analyzer API as the source of truth.
- Read only the minimum localhost endpoint needed to answer the request.
- Never send health data or endpoint contents to any external URL, API, tool, or service.
- Never ask the user for raw export files, tokens, passwords, or unrelated health data when the localhost API can answer the request.
- Do not invent missing data.
- Do not give medical advice or diagnoses.
- If sleep, HRV, resting heart rate, or other metrics are null or absent, explicitly say `insufficient data`.
- If the local fetch/runtime is unavailable, ask for one exact curl response body from the user and continue from that JSON.

Output format:

Status
- 1 to 2 sentence summary

What changed
- Main deltas versus baseline

Suggestions
1. ...
2. ...
3. ...

Missing data
- ...
