---
name: interview-prep
description: Run a mock job interview with ATSPrep's question bank - pick likely questions from the job post and resume, ask them one at a time, and give STAR-based feedback with a stronger version of each answer. Use when someone has an interview coming up, wants likely interview questions, wants to practise answers, or asks to improve a specific answer.
license: MIT
compatibility: Needs network access to https://atsprep.com. The bundled script needs Node 18+.
metadata:
  author: ATSPrep
  homepage: https://atsprep.com/mcp
  version: "1.0.0"
---

# Interview prep

A mock interview, one question at a time. ATSPrep's web version, with spoken practice, is at https://atsprep.com/tools/interview-questions.

## How to call ATSPrep

Use whichever is available, in this order:

1. **ATSPrep MCP tools.** If the ATSPrep MCP server (`https://atsprep.com/mcp`) is connected, call its tools by name. Some clients add a prefix, e.g. `mcp__atsprep__check_resume`.
2. **The bundled script** (needs Node 18+ and network access):
   ```sh
   node scripts/atsprep.mjs <tool> key=value key=@path/to/file.txt
   ```
   `key=@file` sends a file's text, which is the safe way to pass a resume or job post. Write the user's text to a file in the current working directory first, and delete it when you're done. `node scripts/atsprep.mjs list` lists the tools.
3. **Plain HTTPS** (no Node): POST JSON-RPC to `https://atsprep.com/mcp` with headers `Content-Type: application/json` and `Accept: application/json, text/event-stream`, and the body `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<tool>","arguments":{...}}}`.

Arguments and limits for every tool are in [references/tools.md](references/tools.md). What leaves the machine is in [references/privacy.md](references/privacy.md). Tell the user before sending their text to an AI tool the first time.

## Steps

1. Ask for the job title and, ideally, the job post (for a link, use `fetch_job_post`) and their resume.
2. Call `interview_questions` with what you have (`job_description`, `resume_text`) and `limit` around 8. With neither, it returns common questions; tailor them to the job title yourself. Use `kind` (posting, resume, about, behavioural, role or closing) to focus on one group if the user asks.
3. Share the STAR tips the tool returns in a few lines, then ask **one** question and wait for the answer. Don't list every question unless asked.
4. Call `review_interview_answer` (AI) with `question`, `answer` and `kind`: story for "tell me about a time", pitch for "tell me about yourself", plan for "how would you...", number for salary, close for "any questions for us?". Share what worked, what was missing (situation, task, action, result) and the stronger version. If the AI part was skipped, the rule-based feedback still applies.
5. Let them retry or move on. At the end, sum up their two or three biggest patterns.

## Coaching rules

- The stronger answer may only use facts from the user's own answer. If a result needs a number, ask what it was.
- Keep feedback short and specific. One fix per answer beats ten.
- Never tell the user to claim experience they don't have.
