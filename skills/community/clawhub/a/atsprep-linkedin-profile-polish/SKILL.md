---
name: linkedin-profile-polish
description: Check and improve a LinkedIn headline and About section with ATSPrep's rules - score what's there, explain the issues, and write keyword-rich headline options from the user's real role and skills. Use when someone asks to improve, rewrite or review their LinkedIn headline, summary, About section or profile.
license: MIT
compatibility: Needs network access to https://atsprep.com. The bundled script needs Node 18+.
metadata:
  author: ATSPrep
  homepage: https://atsprep.com/mcp
  version: "1.0.0"
---

# LinkedIn profile polish

Web versions: https://atsprep.com/tools/linkedin-headline-generator and https://atsprep.com/tools/linkedin-about-checker.

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

1. Ask for the current headline, the About section, and the job title they want to be found for.
2. Call `check_linkedin_headline` with `headline` (references/tools.md lists the optional fields). Explain each issue in a line or two.
3. Call `generate_linkedin_headline` with `role` and whatever the user gave (`years`, skills, `results` with their real numbers). Offer three or four options and say why each works.
4. Call `check_linkedin_about` with `about`. Walk through the findings: the opening lines shown before "see more", keywords, proof and a call to action.
5. Help rewrite the About section in the user's voice, using only facts they've given. Run `check_linkedin_about` again on the new version.
6. If they're also job hunting, suggest the resume-ats-check skill or `check_resume`.

## Honesty rules

- Never add a number, employer, tool, credential or result the user didn't give you. If a line would be stronger with a number, ask for it.
- Only add a missing keyword if the user confirms they really have that skill.
- AI tool results come back already filtered for made-up facts. Hold your own edits to the same standard.
- Keep the headline within LinkedIn's 220 characters and lead with the role they want to be found for.
