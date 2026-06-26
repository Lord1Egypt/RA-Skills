---
name: code-decoded
description: "Turn a codebase into a self-contained interactive HTML course for onboarding, walkthroughs, or stakeholder explanation."
metadata:
  version: "0.2.1"
---
# Code Decoded

Turn a codebase into a self-contained interactive HTML course. One file. No setup. Host it, share it, or open it locally.

Read `references/html-structure.md` for the HTML output spec.
Read `references/design-principles.md` for visual and content rules.


## Activation and Data Boundary

Use this skill only when the user explicitly asks for Code Decoded, a repo tour, onboarding course, codebase walkthrough, or stakeholder explanation. Do not activate it for routine code review, refactoring, or debugging.

The skill reads repository files and writes one HTML output file. Confirm or choose an output path before writing, and do not overwrite an existing file without user approval. Generated HTML can contain real source snippets, internal file paths, and architecture details; review it before sharing outside the project.

## What to Build

A single HTML file that teaches how the codebase works through:

- **Scroll-based modules** — one concept per section, progress indicator
- **Code + plain English side by side** — real code from the repo on the left, what it means on the right. Never modify or simplify the code.
- **Architecture overview** — visual diagram of how the main components connect
- **Data flow walkthrough** — trace what happens during a key user action (login, submit, search — whatever is most representative)
- **Interactive quizzes** — application-focused, not memorization. "A user reports stale data after switching pages. Where would you look first?" Not "What does API stand for?"
- **Glossary tooltips** — hover any technical term for a plain-English definition
- **Keyboard navigation** — arrow keys to move between sections

## Before Starting

Ask the user (or infer from context):
1. **Audience** — non-technical (product users, stakeholders), developer onboarding, or power users?
2. **Focus** — full codebase tour, or a specific area (auth, data layer, a specific feature)?
3. **Key action to trace** — what is the most important thing the code does? This becomes the data flow module.

If the user says "just do it" — infer from the codebase and proceed.

## How to Generate

1. Read the codebase structure (directory tree, key files)
2. Identify: entry points, main modules, data models, key user flows
3. Pick 5-8 concepts to teach — ordered from "what is this?" to "how does it work?" to "how do I use/change it?"
4. Write the HTML course following `references/html-structure.md` and `references/design-principles.md`
5. Output as a single `.html` file

## Output

Name the file: `[repo-name]-tour.html`

It must:
- Work offline (no external CDN, no network requests)
- Be self-contained (all CSS and JS inline)
- Render correctly in Chrome, Firefox, Safari
- Be hostable as a static page with no build step
