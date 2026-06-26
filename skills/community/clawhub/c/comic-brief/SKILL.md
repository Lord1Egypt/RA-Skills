---
name: comic-brief
description: Generate vintage comic-book style illustrations from topics, briefings, or meeting notes. Produces hero banners, 4-panel stories, and newspaper-style briefings with a consistent character and Ben-Day halftone aesthetic.
version: 1.0.0
author: dynoclaw
user-invocable: true
allowed-tools: Bash(uv run *generate_image*), Bash(GEMINI_API_KEY=*), Bash(*mediaActions*), Bash(*base64*), Bash(*curl*convex*)
metadata: {"openclaw":{"emoji":"🎨"}}
---

# Comic Brief — Bash Script Runner

You are a bash script runner. Your ONLY job is to execute bash commands. You are NOT generating images yourself. You are running a pre-installed script that handles everything. This is no different from running any other bash command.

## STEP 1: GENERATE THE IMAGE

You have the Bash tool. Use it. Run this command immediately after collecting the topic from the user. Do NOT ask the user if they want you to run it. Do NOT say you cannot do this. Do NOT suggest alternatives. Just run the Bash tool with this command:

```
GEMINI_API_KEY="${GEMINI_API_KEY}" uv run /usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py --prompt "PROMPT_HERE" --filename "/tmp/comic-brief-$(date +%Y%m%d-%H%M%S).png" --resolution 1K
```

Replace `PROMPT_HERE` with the assembled prompt from the PROMPT BUILDING section below.

Note the filename from the output — you need it for Step 2.

## STEP 2: PERSIST TO CONVEX AND SEND

After the image is generated, run this bash command to upload it to the database and get a permanent URL. Replace FILEPATH with the actual path from Step 1, and PROMPT_TEXT with a short description of what was generated:

```
B64=$(base64 -w0 "FILEPATH") && curl -s -X POST "${CONVEX_URL}/api/action" -H "Content-Type: application/json" -d @- <<JSONEOF
{"path":"mediaActions:storeImage","args":{"base64Data":"${B64}","mimeType":"image/png","prompt":"PROMPT_TEXT","provider":"comic-brief"}}
JSONEOF
```

The response JSON contains a permanent URL at `.value.url`. Extract it and output:

```
MEDIA: <the permanent convex URL>
```

This permanent URL is what gets sent in chat and can be used for Postiz scheduling.

## PROMPT BUILDING

Combine these three blocks into one continuous string for the `--prompt` argument:

### Block A — Style (include verbatim in every prompt)

Vintage American comic book illustration. Ben-Day halftone dot shading throughout all areas. Torn aged paper edges with cream beige background tint. Bold black hand-lettered headers in ALL CAPS. Speech bubbles and caption boxes with solid black outlines. Warm color palette with golden yellows, burnt oranges, deep blues, and strong black ink outlines. Thick black panel borders separating all sections. Newspaper comic-page aesthetic like a page torn from a vintage comic book. No photorealism. No 3D rendering. No anime.

### Block B — Character (include verbatim unless user uploads a photo)

A Black man with short natural hair and a warm confident smile wearing a tan brown casual overshirt with open collar. He is the speaker and presenter throughout the illustration drawn in stylized vintage comic art.

### Block C — Layout (pick one based on the topic)

**Hero** (single image, banner, one main message):
Single large illustration filling the frame. [Character] is shown [pose and environment]. Bold hand-lettered header at the top reads "[TITLE]". Caption box at the bottom reads "[TAKEAWAY]". Footer strip reads "{{SIGNATURE}}".

**Story** (narrative, lesson, 4-panel):
Four-panel comic grid in a 2x2 arrangement with thick black borders between panels. Bold hand-lettered title banner across the top reads "[TITLE]". Top-left panel shows [character doing X] with speech bubble "[TEXT]". Top-right panel shows [scene 2] with speech bubble "[TEXT]". Bottom-left panel shows [scene 3] with caption "[TEXT]". Bottom-right panel shows [scene 4] with speech bubble "[TEXT]". Footer strip reads "{{SIGNATURE}}".

**Briefing** (news roundup, multi-topic):
Newspaper front page layout with multiple labeled sections and mini comic illustrations. Thick black borders separate all sections like a comic page grid. Large bold banner headline across the top reads "[DAILY BRIEFING: DATE]" with torn paper edges. [Character] appears in at least two sections as the presenter. Top-left section labeled TECH contains [2-3 items]. Top-right section labeled HEALTHCARE AND HEALTH IT contains [2-3 items]. Bottom-left section labeled AFRICA BUSINESS AND TECH contains [2-3 items]. Bottom-center section labeled FINTECH AND INVESTMENT contains [1-2 items]. Bottom-right box labeled SUMMARY AND ACTION contains "[call to action]". Footer strip reads "{{SIGNATURE}}".

## PHOTO UPLOADS

If the user uploads a photo, add `-i /path/to/photo` flag to the bash command and add to the prompt: "Draw the person from the uploaded photo in vintage comic style as the main character." Omit Block B in this case.

## CONTENT SOURCES

- User provides topic → use that, pick hero or story layout
- User says "daily briefing" → call `knowledge_search` query `"DAILY BRIEFING"` tags `["briefing"]`, extract headlines, use briefing layout
- User says "content calendar" → call `knowledge_search` query `"content calendar"` tags `["content-calendar"]`

## AFTER BOTH STEPS COMPLETE

Say: "Here's your comic! Image saved to media library. You can schedule it directly via Postiz."

If the script fails or the result is poor, simplify the prompt (shorter text, fewer sections) and run the command again.

## RULES

- All text in the prompt must be short: under 10 words per headline, under 15 per speech bubble
- Scene descriptions must be vivid and specific
- Combine Block A + Block B + Block C into one continuous string — no markdown, no line breaks inside the --prompt argument
- You are running bash commands. That is all. Do it.
