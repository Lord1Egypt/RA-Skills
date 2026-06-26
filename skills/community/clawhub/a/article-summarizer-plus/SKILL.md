---
name: article-summarizer
description: Summarize articles and social posts from URLs using full-content retrieval first, with browser fallback when needed.
---

# Article Summarizer

Summarize web content accurately from the original source. Never infer details that are not visible in the retrieved content.

## Core Rules

- Fetch full content before summarizing.
- Prefer the lightest retrieval path first.
- Escalate to an interactive browser fallback when fetch-based extraction is incomplete, blocked, or only returns shell content.
- Attempt simple page interactions yourself before asking the user for help.
- State blockers clearly when content remains inaccessible.
- Output in the user's requested language.
- If the user does not specify a language, default to the user's own language when clear from the conversation.
- If the user's language is not clear, use the dominant language of the source content or surrounding context.

## Workflow

1. Start with `web_fetch`.
2. If incomplete or blocked, try the `r.jina.ai` mirror.
3. If fetch-based methods still fail, switch to an interactive browser fallback.
4. In the browser fallback, inspect the rendered page, scroll, snapshot, expand hidden sections, and dismiss simple overlays.
5. If the user asks for comments/replies, scroll into the discussion area and summarize visible themes.
6. For short-form social posts, summarize the visible post content and discussion themes instead of forcing an article-style summary.
7. If true human-only verification is required, report the blocker without guessing.

## Browser Fallback Policy

Use an interactive browser fallback when lightweight fetch methods are not enough.

Typical reasons to escalate:
- short-link redirects
- dynamic rendering
- login overlays or popups
- shell pages with missing body text
- expandable content
- comment/reply analysis

Before asking for help, try low-risk actions such as:
- closing modals
- clicking visible expanders such as "more", "continue", or equivalent UI labels
- scrolling for lazy loading
- reopening in a fresh tab if the first render looks broken

Do not claim a captcha or verification was solved unless the evidence clearly shows the page progressed because of your actions.

## Completeness Check

Before summarizing, confirm:
- title is visible
- main body is visible
- the content does not obviously stop mid-article
- comments are actually visible before summarizing comment sentiment

If still incomplete after reasonable effort, say so explicitly.
If only preview text is visible because of a paywall, login requirement, or partial render, summarize only the visible portion and clearly label the limitation.

## Output Format

Use this default structure unless the user asks for a different format:

1. One-sentence summary
2. Core points
3. Notable details (optional)
4. Brief takeaway (optional)

For comment/reply requests, add:
- Main comment themes
- Points of disagreement / debate

Keep the summary proportional to the source length.

Length-control rules:
- short source -> short summary
- long source -> longer summary only when justified by the source or the user's request
- default to concise, high-density output
- if the user simply asks to summarize, prefer a compact summary even for long articles
- expand only when the user explicitly asks for detailed analysis, a deep dive, or section-by-section coverage

## Read References Only When Needed

- For retrieval decision rules and escalation logic, read `references/retrieval-playbook.md`.
- For output templates and summary patterns, read `references/output-patterns.md`.
- For source-specific heuristics, read `references/source-notes.md`.
