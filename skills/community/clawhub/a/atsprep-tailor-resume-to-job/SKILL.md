---
name: tailor-resume-to-job
description: Tailor a resume to a specific job posting with ATSPrep - rank the posting's keywords, show which are missing, and rewrite the user's own lines in the posting's wording without inventing anything. Use when someone shares a job link or job description with their resume and asks to tailor, target, match or optimise it for that role.
license: MIT
compatibility: Needs network access to https://atsprep.com. The bundled script needs Node 18+.
metadata:
  author: ATSPrep
  homepage: https://atsprep.com/mcp
  version: "1.0.0"
---

# Tailor a resume to a job

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

1. Get the job post. For a link, call `fetch_job_post` with `url`. If it says the site is blocked or the post wasn't found, ask the user to paste the post's text.
2. Get the resume as plain text (one heading, role or bullet per line).
3. Call `match_job` with `resume_text` and `job_description`. Report coverage (overall, required, preferred) and list the missing keywords, required ones first, each with the posting sentence it came from.
4. Ask which missing keywords the user genuinely has. Never assume.
5. Call `tailor_resume` (AI) with `resume_text` and `job_description`. It suggests rewrites of existing lines. Show each as original → suggestion, and keep only those the user approves. If its AI note says the model was skipped (busy, limit, budget), carry on with the rule-based result and suggest edits yourself under the honesty rules.
6. If useful, call `write_summary` (AI) with `resume_text` and `target_title` for a tailored summary.
7. Run `match_job` again on the edited resume and show the change in coverage.
8. Offer `open_in_studio` with the final text, so the user can format and download it.

## Honesty rules

- Never add a number, employer, tool, credential or result the user didn't give you. If a line would be stronger with a number, ask for it.
- Only add a missing keyword if the user confirms they really have that skill.
- AI tool results come back already filtered for made-up facts. Hold your own edits to the same standard.
- A keyword the user doesn't have stays missing. Help them describe nearby experience truthfully instead.
