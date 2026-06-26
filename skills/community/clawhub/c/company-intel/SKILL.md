---
name: company-intel
description: Build structured company intelligence for interview preparation.
---

# Company Intel Skill

## Trigger

Activate when user asks:

- "帮我调研这家公司"
- "这个公司做什么、技术栈是什么？"
- "整理这家公司的面试风格"
- "给我公司情报报告"

## Workflow

1. Collect input:
   - `company` (required)
   - `role_title` (optional)
   - `jd_text` (optional)
2. Call:
   - `POST http://127.0.0.1:8010/api/company/intel`
   - Body example:
     - `{"company":"MiniAgent","role_title":"AI Agent Intern","focus_keywords":["技术栈","面试流程"],"max_results":6,"include_search":true}`
3. Parse response and show:
   - `summary`
   - `business_direction`
   - `tech_stack`
   - `funding_stage` / `team_size_stage`
   - `interview_style`
   - `risks` + `suggestions`
4. If user asks for deeper prep, suggest using `interview-prep` skill next.

## Command templates (exec tool + curl)

- Generate company intel:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/company/intel" -H "Content-Type: application/json" -d '{"company":"MiniAgent","role_title":"AI Agent Intern","focus_keywords":["技术栈","面试流程"],"max_results":6,"include_search":true}'`

## Constraints

- If company name is missing, ask user to provide it first.
- If API call fails, show exact error and ask user whether to retry.
- Never fabricate facts as certainty; indicate confidence and uncertainty explicitly.
