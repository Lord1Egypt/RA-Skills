---
name: demo-note-polisher
description: Turn rough notes, bullet lists, chat fragments, meeting takeaways, and mixed-language drafts into polished writing. Use when the user asks to rewrite, polish, clean up, organize, or reframe messy text into a clearer message, email, status update, announcement, summary, or short memo without changing the underlying facts.
---

# Demo Note Polisher

## Goal

Turn incomplete or messy source text into clean, readable output while preserving the user's intent, facts, and level of certainty.

## Workflow

1. Identify the target output.
   Common targets: direct message, email, project update, meeting summary, announcement, short memo.
2. Infer audience and tone from the request.
   Default to concise and professional when the user does not specify tone.
3. Extract the factual content from the raw notes.
   Preserve names, dates, numbers, decisions, blockers, and next steps exactly unless the user explicitly asks for changes.
4. Rewrite for clarity.
   Remove duplication, filler, and private shorthand that would confuse the reader.
5. Mark uncertainty instead of inventing details.
   If key information is missing, surface it as an open question or a neutral placeholder.

## Output Rules

- Keep the same language as the input unless the user requests another language.
- If the input mixes languages, normalize to the dominant language unless the user wants bilingual output.
- Do not fabricate timelines, metrics, owners, or outcomes.
- Keep the output shorter than the source unless the user asks for expansion.
- Preserve the user's stance and confidence level.
- If the notes are extremely rough, provide one polished version and one shorter version.

## Format Heuristics

### Message

- Keep it brief and direct.
- Lead with the main point.
- End with the requested action, if any.

### Email

- Use a clear subject line only when it helps.
- Open and close politely but keep the body compact.
- Group related details into short paragraphs or bullets.

### Status Update

Use this structure when the user wants a weekly update or progress summary:

1. Summary
2. Progress
3. Blockers
4. Next steps

### Meeting Summary

Use this structure when the notes come from a meeting:

1. Purpose
2. Decisions
3. Action items
4. Open questions

## Clarification Rule

Ask at most one clarifying question only if the missing detail would materially change the output, such as the target audience or required language. Otherwise, make a reasonable default choice and proceed.

## Example Requests

- "Polish these meeting notes into a short recap for the team."
- "Turn this rough draft into a professional email."
- "Clean up my weekly update and make it more concise."
- "Rewrite these mixed Chinese and English notes into one clear announcement."
