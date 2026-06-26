# Prompt Refiner — Worked Examples

## Example 1: Voice Transcription (Chinese) → Gmail Check

**Raw Input:**
```
"帮我查一下今天有没有重要邮件"
```

**Analysis:**
- Intent: Check Gmail for important emails
- Language: Chinese (voice/text)
- Gaps: Which account? What counts as "important"?
- Clarity: MEDIUM

**Clarification (if needed):**
> "Are we checking your personal Gmail (jamesxu81@gmail.com) or work email?"

**Refined Prompt:**
```
Persona: You are a personal assistant with expertise in email triage and priority filtering.

Task: Check Gmail inbox for important/urgent emails received today.

Context:
  Account: jamesxu81@gmail.com
  Date: [today]
  Timezone: Pacific/Auckland

Requirements:
  Focus on:
  - Financial/bills (bank, payments, invoices)
  - Deadlines (meetings, RSVPs, approvals needed)
  - Action-required items
  Exclude: newsletters, school emails (Pinehurst, Seesaw), automated notifications
  If no important emails found, confirm inbox is clear.

Output:
  Bullet list per email:
  - Sender name
  - Subject
  - 1-line action summary
```

---

## Example 2: Vague Code Review → Structured Debug Prompt

**Raw Input:**
```
"That code looks broken. Can you fix it?"
```

**Analysis:**
- Intent: Fix code bugs
- Gaps: Which file? What's "broken" mean?
- Clarity: LOW — clarification required

**Clarification:**
> "Which file — `src/auth/validate.js` or `src/payment/process.js`?"

**Refined Prompt (after clarification):**
```
Persona: You are a senior Node.js engineer specializing in security and runtime reliability.

Task: Debug and fix src/auth/validate.js for runtime and logic errors.

Context:
  Project: Mission Control backend
  Language: Node.js (CommonJS)
  File: /Users/luckbot/Projects/mission-control/src/auth/validate.js

Requirements:
  Check for:
  - Runtime errors (missing null checks, try/catch gaps)
  - Logic bugs (incorrect conditions, off-by-one errors)
  - Security issues (missing input validation, auth bypasses)
  - Edge cases not handled
  Do NOT refactor style — only fix actual bugs.

Output:
  For each issue:
  - Line number(s)
  - Issue type (bug/security/edge case)
  - Root cause
  - Code fix
  If no issues found, confirm file is production-ready.

Think step by step: identify each issue before proposing fixes.
```

*CoT added because debugging benefits from step-by-step reasoning.*

---

## Example 3: Service Restart (Chinese, Ambiguous Target)

**Raw Input:**
```
"重启那个服务"
```

**Analysis:**
- Intent: Restart a service
- Gap: Which service?
- Clarity: LOW

**Clarification:**
> "Which service — Mission Control backend, frontend, or another?"

**Refined Prompt:**
```
Persona: You are a macOS systems administrator managing launchd services.

Task: Restart the Mission Control backend service gracefully.

Context:
  OS: macOS (ARM64)
  Service: LaunchAgent — ai.openclaw.mission-control.backend
  Logs: ~/.openclaw/logs/mission-control-backend.log

Requirements:
  - Stop with SIGTERM, wait up to 5 seconds before force kill
  - Verify no orphan processes (check lsof port 3001)
  - Start fresh instance
  - Health check: GET http://localhost:3001/health → 200 OK
  - Max wait: 10 seconds for healthy status

Output:
  - Timestamp of stop and start
  - Health check result (pass/fail)
  - Any errors encountered
  If failed: specific error + troubleshooting steps
```

---

## Example 4: Multi-Step Task → Prompt Chaining

**Raw Input:**
```
"Write a weekly report from this data and post it to Slack"
```

**Analysis:**
- This is a 3-phase task: analyze → write → post
- Benefits from chaining — each step is verifiable

**Chain:**

*Prompt 1 — Analysis:*
```
Persona: You are a data analyst summarizing weekly business metrics.

Task: Analyze the attached data and extract the 5 most significant changes vs last week.

Output: Bullet list with metric name, value, % change, and 1-line interpretation.
```

*Prompt 2 — Report Writing (using Prompt 1 output):*
```
Persona: You are a business writer crafting concise executive summaries.

Task: Using these metrics: [Prompt 1 output], write a weekly report for the engineering team.

Requirements:
  - Max 200 words
  - Tone: Professional but friendly
  - Format: Sections for Wins, Blockers, Next Steps

Output: Final report text ready to post.
```

*Prompt 3 — Post (using Prompt 2 output):*
```
Task: Post this report to the #weekly-updates Slack channel: [Prompt 2 output]
```

---

## Example 5: Meta Prompting — When You're Stuck

**Situation:** You know what you want but can't frame the prompt well.

**Use Meta Prompting:**
```
I want to get better at writing SQL queries for our PostgreSQL database.
I learn best through worked examples.

What questions should I ask you, and in what order, to build this skill effectively?
```

The AI will design a learning curriculum — then follow it.

---

## Example 6: Few-Shot Format Consistency

**Raw Input:**
```
"Format these log entries as a table"
```

**Without few-shot:** AI might use any table format.

**With few-shot:**
```
Persona: You are a log analysis expert.

Task: Format these error log entries as a structured table.

References (example format I want):
| Timestamp | Level | Service | Message |
|-----------|-------|---------|---------|
| 2026-03-29 09:12 | ERROR | auth | Token validation failed |
| 2026-03-29 09:13 | WARN | api | Rate limit approaching |

Now apply this exact format to: [log data]

Output: Markdown table only — no explanation.
```
