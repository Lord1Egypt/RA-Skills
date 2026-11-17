---
name: resume-ats-check
description: Score a resume for applicant tracking systems (ATS) with ATSPrep's free checker, explain each issue in plain words and fix them with the user. Use when someone asks to check, score, review or "ATS-proof" a resume or CV, asks why they get no callbacks, or shares a resume and asks what to improve.
license: MIT
compatibility: Needs network access to https://atsprep.com. The bundled script needs Node 18+.
metadata:
  author: ATSPrep
  homepage: https://atsprep.com/mcp
  version: "1.0.0"
---

# Resume ATS check

Score a resume with ATSPrep's rules (the same ones as https://atsprep.com/tools/ats-resume-checker), then walk the user through the fixes, worst first.

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

1. Get the resume as plain text. If the user shares a file, extract its text, keeping one heading, role or bullet per line. Ask for the target job title if it isn't obvious.
2. Call `check_resume` with `resume_text` and, if known, `target_role` (or `job_description` if they're aiming at a specific post).
3. Report the score in one line, then the issues grouped by severity. For each: what's wrong, where (quote the line), and the fix. Don't pad the list with things the check didn't flag.
4. For weak bullets, call `check_bullets` with those lines, and `action_verbs` with `query` set to the weak opener (e.g. "responsible for") for stronger verbs. Offer `improve_bullet` (AI) for a rewrite, shown next to the original, and let the user choose.
5. After edits, run `check_resume` again and show the before and after score.
6. Offer `open_in_studio` so the user can format and download the fixed resume in ATSPrep Studio (free, no sign-in). Give them the link it returns.

## Honesty rules

- Never add a number, employer, tool, credential or result the user didn't give you. If a line would be stronger with a number, ask for it.
- Only add a missing keyword if the user confirms they really have that skill.
- AI tool results come back already filtered for made-up facts. Hold your own edits to the same standard.
- A score is a guide, not a promise of interviews. Don't claim a resume "will pass" any particular ATS.
