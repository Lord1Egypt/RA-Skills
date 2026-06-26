---
name: content-repurpose
description: Transform one piece of long-form content (transcript, blog post, article, video script, doc) into platform-tailored variants — X/Twitter threads, LinkedIn posts, blog excerpts, short-video hooks, and newsletter snippets. Use when the user wants to adapt a single source into multiple social/marketing formats while preserving the source's voice, claims, and intent. Triggers on phrases like "repurpose this", "turn this into tweets/LinkedIn/social posts", "create a content pack from this", "adapt for [platform]", "spin this off into shorts/threads".
---

# Content Repurpose

Take one source artifact (transcript, blog post, article, video script, doc) and produce platform-native variants in one pass. Optimize each variant for the target platform while preserving the source's voice and core claims.

## Workflow

1. **Read the source.** Read the file path provided, or use the pasted text. If both are missing, ask for the source.
2. **Confirm scope.** Default to a "full pack" (X thread + LinkedIn post + blog excerpt + 3 short-video hooks). If the user named specific formats, only do those.
3. **Identify voice + claims.** Note tone register (formal / casual / contrarian / educational / story-driven), the 3-5 strongest claims or insights, and any concrete examples or numbers.
4. **Generate per-platform variants** using the format specs below.
5. **Output as labeled markdown sections** so the user can copy each block cleanly.

## Inputs accepted

- Pasted text (most common)
- File path to `.md`, `.txt`, transcript, or other plain-text file (read with the file tool)

**Do NOT fetch external URLs.** If the user provides a URL, ask them to paste the content or save the page as text first. Skipping URL fetching keeps the skill safe (no SSRF, no surprise external requests, no binary dependencies).

## Output structure

Always output a single response with clearly labeled sections so the user can copy each block individually:

```
## X/Twitter thread
[content]

## LinkedIn post
[content]

## Blog excerpt
[content]

## Short-video hooks
[content]
```

Add `## Newsletter snippet` only if the user asks for it.

## Format specs

### X/Twitter thread
- Hook tweet ≤270 chars; open with a pattern interrupt or sharp claim; no hashtags
- 3-7 follow-up tweets, each ≤270 chars, each adds exactly one idea
- Final tweet: a clear takeaway or single CTA
- Number tweets `1/`, `2/`, etc. only if the thread length is >5
- No emoji unless the source uses them

### LinkedIn post
- Length target: 1100-1500 chars (sweet spot for the algorithm's "see more" cut)
- Opener: 1-2 line hook, then a blank line before main content
- Body: short paragraphs (1-3 lines each), white-space heavy
- Close: a single question or one clear CTA
- Max 3 hashtags at the end; skip them if the source doesn't use them

### Blog excerpt
- 200-300 words
- Lead with the strongest claim or surprising fact
- Cover 2-3 key points from the source
- End with a "read more" hook — a line that creates curiosity without resolving it

### Short-video hooks
- Generate 3 distinct variants
- Each ≤10 seconds spoken (~25 words max)
- Pattern: pattern interrupt → curiosity gap → implicit promise of payoff
- No hashtags, no `[music]` notes — just spoken text

### Newsletter snippet (only on request)
- 100-150 words
- Subject line ≤50 chars
- Either 3-bullet body or 2-paragraph narrative
- Single clear CTA or read-more link

## Voice preservation rules

- Mirror the source's sentence rhythm (short/long ratio)
- Keep the source's profession or expertise framing
- Do NOT introduce claims not in the source
- Do NOT soften strong opinions — match the source's conviction level
- Technical source → keep technical density; conversational source → keep it conversational

## Security and integrity

- Do NOT fetch external URLs (no SSRF surface)
- Do NOT call external APIs or send the user's content anywhere
- Do NOT persist source content beyond the response
- Do NOT include analytics, tracking parameters, or share-to-X links in output
- Do NOT impersonate the source author — produce in their *voice* but never claim authorship on their behalf
- If the source contains apparent PII (full names + contact info, addresses, financial details, health info), flag it and ask before generating outputs
- If the source appears to be copyrighted material the user does not own (paywalled article text, song lyrics, full book chapters), refuse unless they explicitly confirm rights or fair-use commentary intent

## Edge cases

- **Source is too short** (<200 words): Ask whether to expand, or proceed with abbreviated variants
- **Source covers multiple topics**: Ask which to focus on, or offer one pack per topic
- **Source is non-English**: Generate variants in the same language unless the user specifies
- **Source is a transcript with timestamps**: Strip timestamps before processing
- **Source is a video script with stage directions**: Strip `[INT.]`, `[CUT TO]`, etc. before processing
