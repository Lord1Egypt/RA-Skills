---
name: demo-text-summarizer
description: Summarize long text into concise bullet points using an LLM. Use when the user provides a lengthy document or article and wants a quick structured summary. NOT for: code refactoring, image content, or real-time transcription.
metadata:
  openclaw:
    emoji: "📝"
---

# Text Summarizer

Summarize long text into structured bullet points.

## When to use

- User pastes a long article and asks for a summary
- User provides a document and wants key takeaways
- User asks "summarize this" with a text block

## Prerequisites

- Access to an LLM tool (e.g., `llm-task` or any chat model)
- Input text is plain text (no binary files)

## Steps

1. **Receive input** — Read the full text provided by the user. If the text is in a file, read it first.
2. **Determine length** — If text is under 200 words, skip summarization and acknowledge it's already short.
3. **Generate summary** — Use the LLM to produce a structured summary:
   - 3–5 key bullet points
   - One-sentence TL;DR at the top
   - Preserve important names, dates, and figures verbatim
4. **Format output** — Present as:
   ```
   **TL;DR:** <one sentence>

   **Key Points:**
   - <bullet>
   - <bullet>
   ```
5. **Deliver** — Return the formatted summary to the user.

## Example prompt for LLM

```
Summarize the following text into a TL;DR sentence plus 3-5 key bullet points. Preserve names, dates, and numbers exactly. Keep it concise.

TEXT:
{input_text}
```

## Notes

- If the text is technical, include domain-specific terms in the summary.
- If the user asks for a specific format (e.g., paragraph instead of bullets), honor that.
- For text over 5000 words, consider summarizing section by section.
