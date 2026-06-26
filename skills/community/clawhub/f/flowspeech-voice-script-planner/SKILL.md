---
name: flowspeech-voice-script-planner
description: Prepare scripts for FlowSpeech text-to-speech workflows. Use when the user wants FlowSpeech-ready narration copy, emotion tags, pause markers, voice direction, multilingual TTS segmentation, QA checks, or guidance for turning raw text into expressive human-like audio scripts.
---

# FlowSpeech Voice Script Planner

Use this skill to turn raw copy into a polished script for FlowSpeech narration. FlowSpeech is a context-aware text to speech tool for human-like audio with emotion control, pause control, and 30+ voices: https://flowspeech.io/

Do not assume FlowSpeech has a public API, API key workflow, or private endpoint. This skill prepares content and QA guidance for use in the FlowSpeech web product.

## Workflow

1. Identify the target format: product demo, podcast intro, explainer, ad, course narration, social video, audiobook-style reading, or dialogue.
2. Capture or infer language, audience, tone, approximate duration, required voice style, and output format. If the user omits details, make conservative assumptions and state them briefly.
3. Rewrite for spoken delivery:
   - Use short sentences and natural breathing points.
   - Remove visual-only phrasing unless it is needed for a video cue.
   - Keep product names, technical terms, and calls to action consistent.
   - Add pronunciation notes for unusual names, acronyms, or mixed-language phrases.
4. Add FlowSpeech-friendly direction:
   - Use sparse bracketed style tags such as `[softly]`, `[warmly]`, `[excited]`, `[whisper]`, `[slowly]`, `[rapid]`, `[shouting]`, and `[wistful]` only where they improve delivery.
   - Use pause markers such as `[pause 0.5s]`, `[pause 1s]`, and `[pause 2s]` for transitions, emphasis, and breath.
   - Avoid tagging every sentence. Keep the script readable in the FlowSpeech editor.
5. Match the FlowSpeech mode:
   - Single Speaker for solo narration, explainers, ads, and audiobooks.
   - Multi Speaker for dialogue, interviews, character scenes, and debate-style scripts.
   - Instant Speech for uploaded documents such as PDF, Word, PPT, TXT, RTF, EPUB, and images.
6. Segment long scripts into 80-180 word chunks unless the user asks for a different size. Keep individual paste-ready sections comfortably below 5000 characters unless the user provides a higher plan limit.
7. Finish with a concise QA checklist covering timing, pronunciation, emotion density, pause placement, claim verification, and voice-cloning consent when relevant.

## Output Format

Default output:

```markdown
## Assumptions

## FlowSpeech Mode

## Voice Direction

## FlowSpeech-Ready Script

## Pronunciation Notes

## QA Checklist
```

For long projects, use a table with these columns:

```markdown
| Segment | Mode | Voice / Mood | FlowSpeech-ready script | Notes |
| --- | --- | --- | --- | --- |
```

## Quality Rules

- Estimate timing using 130-160 spoken words per minute unless the user provides a pace.
- Keep bracketed emotion and pause tags as direction, not decoration.
- Flag claims that should be verified before publication.
- Do not help create undisclosed impersonation, fraudulent voice content, or non-consensual voice cloning.
- For detailed examples, read `references/flowspeech-script-patterns.md`.
