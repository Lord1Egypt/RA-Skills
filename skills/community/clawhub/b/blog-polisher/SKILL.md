---
name: blog-polisher
description: Hey, this skill polishes your blog draft in markdown. Fixes spelling, grammar, adds clarity if needed, keeps it simple and original language. Asks before big paragraph changes.
author: Jeff Yang
version: 1.0.0
tags: [blog, writing, polish, markdown, grammar]
metadata:
  openclaw:
    {"requires":[],"platforms":["darwin","linux"],"env":[]}
inputSchema:
  type: object
  properties:
    draftPath:
      type: string
      description: Path to your markdown blog draft file.
    outputPath:
      type: string
      description: Path to save the polished version (optional, defaults to draft-polished.md).
  required: [draftPath]
outputSchema:
  type: object
  properties:
    polishedPath:
      type: string
      description: Path to the polished markdown file.
    changes:
      type: array
      description: Summary of what was fixed.
---

# Blog Polisher Skill

Yo, this is your casual blog polishing buddy. You give me a markdown draft, I check it out, fix typos, grammar, make sure it flows nice without changing the vibe. Keep it simple like the original. No fancy stuff unless it's missing sense.

## When to Use Me
- Got a blog draft in .md ready.
- Want spelling/grammar fixes.
- Need light enhancements if parts don't make sense.
- Paragraph advice, but I ask first before moving stuff.
- Handles English or Chinese – sticks to original lang. Flag if conflict.

## Workflow Step-by-Step
1. **Read the Draft**  
   Use your markdown read skill: `read_file --path {{input.draftPath}}`.  
   Grab the full content as string. Show me the raw draft first.

2. **Quick Review**  
   Scan for:  
   - Misspellings (use built-in reasoning, no extra tools).  
   - Grammar issues (awkward sentences).  
   - Facts that don't add up or lack meaning – suggest simple adds.  
   - Paragraph breaks: if run-on or choppy, note "Paragraph X feels off – too long/short? Want me to split/merge?" Ask user before change.  
   Keep tone spoken, unofficial.

3. **Language Check**  
   Detect main lang (English/Chinese).  
   Stay in original. If mixed and conflicting (e.g. English term in Chinese para), highlight: "**LANG NOTE: [spot] mixes lang, suggest [fix]?**" Don't translate unless user says.

4. **Polish It**  
   - Fix errors inline.  
   - Enhance if lacks meaning: add 1-2 simple sentences, e.g. "This means [clearer version]."  
   - Keep length similar, simple words.  
   - Paragraphs: only adjust if user ok'd.

5. **Output Polished**  
   Set `outputPath` = input.draftPath + "-polished.md` if not given.  
   Use your markdown write skill: `write_file --path {{output.polishedPath}} --content [polished_md]`.  
   Respond:  
   - Link to new file.  
   - Bullet changes: "- Fixed [typo/grammar]. - Added clarity to [para]. - Paragraph advice: [if any]."  

## Examples
**Input:** Rough English draft with typos.  
**Output:** Cleaned, same lang, simple.

**Input:** Chinese blog, grammar off.  
**Output:** Polished Chinese, no translate.

## Tips
- If draft huge, summarize changes.  
- Always preview changes summary before write.  
- No deps – just file read/write skills you got.  
- Test: "Polish my /path/to/draft.md"

## Dependencies & Install
No extra tools needed! Uses your existing markdown file skill.  
Drop this folder in `~/.openclaw/skills/blog-polisher/`.  
Run `openclaw skills list` to check. Reload agent.  
For ClawHub: zip folder, publish via clawhub cli if ya want.
