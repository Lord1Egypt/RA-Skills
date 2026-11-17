---
name: "conversation-visualizer"
description: "Generate visual HTML summaries from OpenClaw session history."
metadata:
  version: 1.1.0
  author: Maximius
  tags: [visualization, summary, html, sessions, codex, markdown, powerpoint]
  homepage: https://github.com/openclaw/skills/conversation-visualizer
  license: MIT
allowed-tools:
  - sessions_history
  - sessions_list
  - write
  - read
  - exec
  - node_inference
  - skill_workshop
user-invocable: true
---

# Conversation Visualizer

Turn an OpenClaw chat session into a clean, tabbed HTML infographic — like a Codex `$visualize` card, but local. Also exports to Markdown and PowerPoint.

## When to use

- The user asks to "summarize this chat", "visualize our discussion", or "make a one-pager from this conversation".
- After a planning or decision session, to create a shareable summary card.
- To produce a quick visual artifact for clawhub, a daily note, a Telegram post, or a slide deck.

## Workflow

1. Pick a session. Use the current session by default; use `sessions_list` if the user names another one.
2. Fetch history with `sessions_history(includeTools=false, limit=200)`.
3. Build a plain-text transcript: `\n\n<role>: <text>` for each message.
4. Send the transcript to a local model via `node_inference` with the summary prompt below. Parse the JSON output.
5. Run `scripts/generate_visual.py --summary <json_file> --output <dir> --png --md --pptx --lang <lang>` to render:
   - self-contained HTML with EN/RU/ZH language switcher and light/dark theme toggle,
   - one PNG per tab,
   - a Markdown summary,
   - a PowerPoint deck.
6. Show the user the output paths. Offer to open the HTML in `canvas` if a node is connected.

## Summary prompt (send via node_inference)

```text
You are a conversation summarizer. Read the OpenClaw transcript below and return ONLY a JSON object with no markdown:

{
  "title": "Short title in the conversation language",
  "subtitle": "One-line context",
  "main_takeaway": "The single most important conclusion",
  "format_takeaway": "How the discussion was structured",
  "next_takeaway": "What the next move should be",
  "flow": [
    {"label": "Step 1", "sub": "what happened"},
    {"label": "→", "sub": ""},
    {"label": "Step 2", "sub": "what happened"}
  ],
  "metrics": [
    {"title": "Goal", "text": "..."},
    {"title": "Approach", "text": "..."},
    {"title": "Output", "text": "..."}
  ],
  "dos": ["good practice 1", "good practice 2"],
  "donts": ["risk 1", "risk 2"],
  "checklist": [
    {"text": "Item name", "status": "ready|pending|blocked"}
  ],
  "next_steps": ["action 1", "action 2"]
}

Transcript:
{{transcript}}
```

## Output rules

- HTML must be self-contained: inline CSS and JS, no external assets.
- Include an EN/RU/ZH language switcher and light/dark theme toggle.
- Match the conversation language in the generated content.
- Default output directory is `workspace/visualized/`; fall back to the user's preferred directory if that path is not writable.
- Never include secrets, passwords, tokens, or private identifiers from the session.

## Safety

- If the history contains sensitive content, summarize it generically or ask the user first.
- Do not call external APIs with the transcript.
