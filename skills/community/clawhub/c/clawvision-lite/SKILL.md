---
name: "clawvision-lite"
description: "ClawVision Lite 1.0.0 — lightweight HTML-only export of an OpenClaw session. English-only, no analytics, no PowerPoint, no Markdown. Reads session history and writes one self-contained HTML file to disk."
metadata:
  version: 1.0.0
  author: Maximius
  tags: [visualization, summary, html, sessions, minimal]
  homepage: https://github.com/monaxamo/clawvision
  license: MIT
  icon: clawvision_demo_en.png
allowed-tools:
  - sessions_history
  - sessions_list
  - write
  - read
  - exec
user-invocable: true
---

# ClawVision Lite 1.0.0

A minimal, English-only version of ClawVision. Turns an OpenClaw chat session into a single self-contained HTML file — no analytics, no PowerPoint, no Markdown, no language switcher, no CDN.

## What it does

- Reads one OpenClaw session history.
- Summarizes the conversation with a local LLM.
- Writes one self-contained `.html` file (inline CSS and JS, no external assets).

## Permissions and data flow

| Tool | What is accessed | Why |
|---|---|---|
| `sessions_history` | Messages from the chosen OpenClaw session | To build the transcript for summarization |
| `sessions_list` | Session metadata when you ask about another session | To locate the session you want to visualize |
| `read` | Local summary JSON files produced by this skill | To verify/inspect generated outputs |
| `write` | The generated HTML file on local disk | To save the export for you |
| `exec` | Local Python script that renders HTML | To run the visual generator |

## When to use

Use when you want a clean, simple HTML summary and nothing else:

- "Create a minimal ClawVision HTML summary for this conversation."
- "Export this OpenClaw session to a simple HTML file."
- "Make a lightweight visual summary of session `<id>`."

## When NOT to use

- Do not run on sessions that may contain secrets or private data unless the user explicitly confirms it is safe.
- Do not use if the user wants PNG, Markdown, PowerPoint, analytics charts, or a non-English language — use the full ClawVision skill instead.

## Workflow

1. Confirm the user's intent and the session to export.
2. Fetch history with `sessions_history(includeTools=false, limit=200)`.
3. Save the session as JSON if needed.
4. Build a plain-text transcript.
5. Summarize via `node_inference` with the prompt below.
6. Run `scripts/generate_visual.py --summary <json> --output <dir> --lang en --preset minimal`.
7. Show the generated HTML path.

## Summary prompt (send via node_inference)

```text
You are a conversation summarizer. Read the OpenClaw transcript below and return ONLY a JSON object with no markdown:

{
  "title": "Short title in English",
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

- HTML is self-contained (inline CSS and JS only).
- English UI labels only.
- No external assets, no CDN, no analytics, no PowerPoint, no Markdown.
- Default output directory is `workspace/visualized/`.
- Never include secrets, passwords, tokens, or private identifiers from the session.

## Safety

- Confirm intent before accessing session history or writing files.
- Ask first if the session may contain sensitive content.
- Do not send session data to external APIs.
- Review the generated HTML before sharing it.
