---
name: "clawvision"
description: "ClawVision 1.0.13 — honest data-export description, offline-only analytics, explicit permissions table."
metadata:
  version: 1.0.13
  author: Maximius
  tags: [visualization, summary, html, sessions, codex, markdown, powerpoint, aesthetic, presets]
  homepage: https://github.com/monaxamo/clawvision
  license: MIT
  icon: clawvision_demo_en.png
allowed-tools:
  - sessions_history
  - sessions_list
  - write
  - read
  - exec
  - node_inference
user-invocable: true
---

# ClawVision 1.0.13

Turn an OpenClaw chat session into a clean, tabbed HTML infographic — like a Codex `$visualize` card, but local. Also exports to Markdown and a redesigned, visual PowerPoint deck. Now with aesthetic presets and a Summary Design Specification step.

## Permissions and data flow

This skill intentionally operates on **session data** and **local files**. Before invoking it, the user must confirm which session to export and that the session does not contain secrets or private identifiers.

| OpenClaw tool | Why it is used |
|---|---|
| `sessions_history` / `sessions_list` | Read the conversation the user wants to export and summarize. Only the session explicitly chosen by the user is accessed. |
| `node_inference` | Send the transcript to a **local** model to produce a structured JSON summary. No remote APIs receive session content. |
| `exec` | Run local Python scripts (`generate_visual.py`, `session_charts.py`) to render HTML, PNG, Markdown, and PowerPoint. |
| `read` / `write` | Read the generated JSON summary and write export files to the user's local disk. |

## What's new in 1.0.13

- **Honest install-facing description** replaces the previous "security audit" wording so the skill's actual data-export behavior is immediately clear.
- **Offline-only analytics charts**: removed CDN fallback for ECharts. Session analytics now require a locally vendored `scripts/echarts.min.js`; if it is absent, charts are skipped instead of loading from the network.
- Added explicit **Permissions and data flow** section to the skill manifest.

## What's new in 1.0.12

- Published with GitHub source repo metadata to fix ClawHub skill-card generation.

## What's new in 1.0.11

- **i18n fix for export buttons and section titles** — language switcher now updates "Export Markdown", "Export PowerPoint", and the "Do"/"Don't" section titles (EN/RU/ZH) without a page reload.
- Added `skill-card.md` for ClawHub publication.
- ~~Removed bundled `echarts.min.js` so ClawHub security scan passes; session analytics charts fall back to CDN when the local bundle is absent.~~ (Reverted in 1.0.13 — CDN fallback removed for offline-by-default behavior.)

## What's new in 1.0.9

- **Session analytics charts** (smart-charts inspired) — optionally generate ECharts-based analytics from session history: message counts by role, activity timeline, tool usage. Charts are embedded as an **Analytics** tab in the ClawVision HTML/PowerPoint/PNG exports.
- Self-contained ECharts bundle (`scripts/echarts.min.js`) so analytics HTML works offline.
- New CLI flags: `--session <json>` and `--include-charts` for `generate_visual.py`.

## What's new in 1.0.7

- **Even clearer install-facing description** explicitly states that the skill reads session history and writes persistent export files to disk.
- Same permission transparency, CSS-variable fix, Summary Design Specification, and 5 aesthetic presets as 1.0.6.

## What's new in 1.0.6

- **Improved skill description and permission transparency** for ClawHub security review.
- Removed unused `skill_workshop` tool permission.
- Same CSS-variable fix, Summary Design Specification, and 5 aesthetic presets as 1.0.5.

## What's new in 1.0.5

- **CSS variable fix**: the generated HTML now correctly includes `:root` color variables for every preset, so tabs, cards, export buttons, and theme switching render as intended.
- Same **Summary Design Specification** and **5 aesthetic presets** from 1.0.4.

## What's new in 1.0.4

- **Summary Design Specification** — before rendering, lock in language, preset, accent color, font family, layout strategy, and export formats.
- **Aesthetic presets** — `minimal`, `editorial`, `retro`, `luxury`, `playful`. Each preset changes colors, typography, rounding, shadows, and visual density for both HTML and PowerPoint.
- Same reliable exports: self-contained HTML (EN/RU/ZH + light/dark), PNG tabs, Markdown, branded PPTX.

Only run ClawVision when the user explicitly asks for a visual/exportable summary of an OpenClaw session. Acceptable triggers include:

- "Create a ClawVision summary card for this conversation."
- "Export the current OpenClaw session to HTML/PNG/Markdown/PowerPoint."
- "Build a visual one-pager from the chat we just had."
- "Summarize session `<id>` with ClawVision."

If the request is vague, ask the user to confirm intent and scope before proceeding.

## When NOT to use

- Do not activate on generic "summarize" or "make a note" requests.
- Do not run on sessions that may contain secrets, credentials, personal data, or internal identifiers unless the user explicitly confirms it is safe to summarize and export.

## Workflow

1. Confirm the user's intent. If the request is vague or the session may contain sensitive content, ask for explicit confirmation before continuing.
2. Pick a session. Use the current session only when the user explicitly refers to "this conversation" or the current context. Use `sessions_list` if the user names another session by ID or label.
3. Fetch history with `sessions_history(includeTools=false, limit=200)` and save it as a JSON file (array of `{role, content, timestamp, tool_calls?}` objects).
4. Build a plain-text transcript: `\n\n<role>: <text>` for each message.
5. Run the **Summary Design Specification** step (below). Ask the user if any choices should change, otherwise default to: preset `minimal`, accent `#2a9df4`, font `Inter`, layout `card-based`, language from the conversation.
6. Send the transcript to a local model via `node_inference` with the summary prompt below. Parse the JSON output.
7. (Optional) Run `scripts/session_charts.py --session <json> --output <dir> --slug <slug>` to generate standalone analytics HTML/PNG. This step is skipped if `scripts/echarts.min.js` is missing; no CDN is loaded.
8. Run `scripts/generate_visual.py --summary <json_file> --session <session_json> --include-charts --output <dir> --png --md --pptx --lang <lang> --preset <preset>` to render:
   - self-contained HTML with EN/RU/ZH language switcher, light/dark theme toggle, and an **Analytics** tab,
   - one PNG per tab (including analytics),
   - a Markdown summary,
   - a redesigned visual PowerPoint deck using the chosen preset.
9. Show the user the output paths. Offer to open the HTML in `canvas` if a node is connected.

## Summary Design Specification

Before generating, output a compact specification and ask the user to confirm or override. Default to inference from the session language and topic.

```text
SUMMARY SPECIFICATION
====================
1. Session language: [en | ru | zh]
2. Aesthetic preset: [minimal | editorial | retro | luxury | playful]
3. Dominant accent color: #HEX
4. Font family: [Inter | Georgia | Space Grotesk | Playfair Display | Nunito | etc.]
5. Layout strategy: [card-based | editorial-column | retro-grid | luxury-spaced | playful-stacked]
6. Export formats: [html | png | md | pptx | all]
```

### Preset guide

| Preset | Best for | Accent examples | Rounding | Shadow | Font |
|---|---|---|---|---|---|
| `minimal` | Clean technical summaries | blue/grey | medium | subtle | Inter / system |
| `editorial` | Long-form insights, articles | burgundy/navy | small | flat | Georgia / serif |
| `retro` | Nostalgia, games, old-web | orange/brown | large | hard | Space Grotesk |
| `luxury` | Finance, premium products | gold/black | tiny | soft | Playfair Display |
| `playful` | Education, social, onboarding | purple/green | huge | bouncy | Nunito |

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

- HTML must be self-contained: inline CSS and JS, no external assets. Preset font should be requested from a web-safe fallback stack.
- Include an EN/RU/ZH language switcher and light/dark theme toggle.
- Match the conversation language in the generated content.
- PowerPoint export uses the same brand colors, preset, and card layout as the HTML card.
- Default output directory is `workspace/visualized/`; fall back to the user's preferred directory if that path is not writable.
- Never include secrets, passwords, tokens, or private identifiers from the session.

## Safety

- Confirm intent and scope before accessing session history or writing output files.
- If the conversation may contain sensitive content, ask the user first; if they decline, stop or summarize generically without exporting files.
- Do not call external APIs with the transcript.
- Review generated files before sharing them.

## Roadmap

- **ClawVision 1.0.13** — current stable version: explicit disk/export disclosure + permission transparency + offline-only analytics + CSS variable fix + Summary Design Specification + 5 aesthetic presets for HTML/PPTX.
- **ClawVision 2.0** — planned: CSS-only session analytics charts (no external JS dependency).
