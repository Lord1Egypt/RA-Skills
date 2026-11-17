---
name: fec-web-video-presentation
description: Use when turning an article, talk script, lesson, product demo, or narrated explanation into a recordable 16:9 web presentation with step-driven scenes, optional narration alignment, theme tokens, and screen-recording guidance; Chinese triggers include web video, dynamic demonstration, spoken script to video, screen-recordable demonstration, 16:9 demonstration.
---

# Web video demonstration

## Purpose

Convert articles, oral presentations, courses, product explanations or technology sharing into screen-recordable 16:9 web presentations. The product should be like a clickable video stage: each step carries a spoken rhythm, the visual design serves the content rhythm, and can be stably recorded using the browser.

## Procedure

1. Determine the input form
   - When the user submits an article or long text, it is first split into a spoken draft and an outline.
   - When the user broadcasts the manuscript to the ready-made script, the original order is retained and only the outline, chapters and steps are added.
   - When the user only provides a topic but no content, first ask for materials, outlines or key points; do not make up the entire content for the user.

2. Generate a content plan
   - Press [content-plan.md](references/content-plan.md) to output script and outline.
   - The script determines the order of telling and each beat; the outline determines the chapters, steps, time estimates, screen information and material list.
   - The outline only describes the content density and screen tasks, and does not write down the specific animation implementation in advance.

3. Align the demo system
   - Choose a starter theme from [theme-system.md](references/theme-system.md) or [starter-themes.json](data/starter-themes.json), or redefine the token by project brand.
   - Create a minimal Vite + React + TypeScript presentation skeleton using [create-video-presentation.mjs](scripts/create-video-presentation.mjs):
     ```bash
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs ./presentation --theme editorial-slate
     ```
   - If you just want to preview optional themes or plan to write content:
     ```bash
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs --list-themes
     node skills/fec-web-video-presentation/scripts/create-video-presentation.mjs --dry-run ./presentation --theme editorial-slate
     ```

4. Implementation Chapter
   - Each chapter is implemented as [chapter-craft.md](references/chapter-craft.md).
   - Each step occupies the stage exclusively, and the screen only carries the core content that the user needs to understand for the current spoken beat.
   - Chapters must have visible visual presentation, graphics, layout changes, status progression, or data/media presentation; do not deliver text-only slides.
   - The first chapter should be completed and accepted first as the style anchor before continuing with other chapters.

5. Screen recording and audio
   - Use [recording-and-audio.md](references/recording-and-audio.md) to check stage scale, navigation, recording mode and optional audio synchronization.
   - Audio can come from the user's existing files, host tools, or the project's own TTS process; this skill is not bound to a specific TTS provider.

6. Pre-delivery verification
   - Open the demo in a browser to check 16:9 zoom, keyboard/click advancement, step count, text overflow, hidden controls, console errors, and screen recording path.
   - If the number, order or step number of chapters changes, reset the local persistence key or clear the old progress to avoid reverting to a non-existent step.

## Constraints

- Do not turn web videos into ordinary marketing landing pages, static PPT or long scrolling articles.
- Do not copy the reference project's themes, template chapters, long prompts, or scaffolding implementations; generate an original skeleton based on the current project.
- Do not lock each animation name in the outline stage; animations should be driven by chapter content relationships.
- Do not use fake data, fake quotes, fake product screenshots or uncheckable media to fill the screen.
- Do not let controls, page numbers, explanatory text or debugging panels pollute the screen recording; necessary controls are hidden or weakened by default.
- No outside-project vendor conventions are introduced for audio synthesis; TTS is an optional adaptation layer.

## Expected Output

Output script, outline, runnable 16:9 web page demonstration skeleton or chapter implementation, and describe the theme, number of chapters/steps, screen recording method, optional audio path and verification results. The final presentation should be able to be progressed steadily through clicks or keyboards, the visual rhythm should fit the spoken content, and it should be suitable for browser screen recording.
