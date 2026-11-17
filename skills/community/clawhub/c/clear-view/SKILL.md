---
name: clear-view
description: >-
  Use when the user wants to quickly understand a conversation, article, paper,
  tutorial, product brief, long thread, or messy discussion: what is going on,
  who said what, topics, positions, agreements/disagreements, or a clearer
  structural explanation. Always delivers a structured text version plus a
  lightweight self-contained HTML infographic.
---
# clear-view

Turn any material into "what is going on right now": first a structured text version, then a default visual HTML. Never take sides, never invent facts that are not in the source.

## Core principles

- **Two deliverables, always**: every time, give **a text version + a visual version** (unless the user explicitly asks for only one).
- **Shortest that works**: pick sections by material type; skip anything the material does not have.
- **Faithful to the source**: attribute views to their speakers; when unsure, mark "unclear in source"; never add drama.

## When to use / not use

**Use:** muddled conversations, long articles that are hard to skim, tutorials with an unclear outline, scattered product features, multi-party debates where agreements and differences are hard to tell apart, or when the user says "explain this clearly / draw this clearly / sort this out".

**Do not use:** the user only wants a one-line summary; only wants code changes or implementation; only wants a translation; or wants a developer-architecture visualization and explicitly names the original show-me workflow.

## Delivery contract

### 1) Text version (give it directly in chat)

Choose from the sections below to fit the material. **Write a section if it applies, skip it if not**, and keep headings short:

| Section | When it appears |
|---|---|
| Topic | Almost always: one sentence |
| What is going on now | One-sentence status summary (put it near the top) |
| Structure / flow / outline | Tutorials, long articles, documentation |
| Features / capabilities | Product briefs |
| What each party said | Conversations, meetings, multi-person threads (bullets per person) |
| Topic threads | When 2+ topics run at once: one line per topic |
| Common ground | When parties overlap |
| Differences / points of contention | When there is disagreement or something unresolved |
| Open / needs clarification | When the source is vague or references are unclear |
| Summary | At most 3 points; do not repeat "What is going on now" |

Text version rules: conclusion first; lists over long paragraphs; key quotes may be quoted briefly, never paste whole passages.

### 2) Visual version (default: lightweight HTML infographic)

- **Default**: write one self-contained HTML file (single file, opens offline) that uses simple diagrams to explain relationships, flows, and who said what, instead of piling up more prose.
- **People**: for multi-person conversations, distinguish speakers with simple character blocks or small figure markers (fixed colors/labels, with a legend saying who is who).
- **Topic branches**: for multiple topics, use columns or branching lines, and mark shared nodes and fork points.
- **Flow / architecture**: show steps as a horizontal or vertical flow; show system relationships with simple boxes and lines.
- **Add more only when needed**: Mermaid, call trees, file trees, diffs, embedded in the HTML or as a text appendix. They never replace the default HTML.
- **Delivery**: hand the HTML file to the user in a form they can open (attachment or equivalent); file name `clear-view-{short-slug}.html`.
- **Look and feel**: readable font size, sufficient contrast, scannable on mobile; minimal decoration, no irrelevant animation; labels in the source language (if the user writes in Chinese, use Chinese).

## Steps

1. Confirm the scope of the material (pasted text / link / specified passage). If it is very long, split it into parts, but the conclusion must still cover the overall "what is going on now".
2. Classify the type: conversation | article/paper | tutorial | product brief | mixed.
3. Extract topic, speakers, topic threads, agreements/differences, and open items, based only on the source.
4. Output the text version (using the sections above).
5. Generate and deliver the default visual HTML; if the user only wants text or only wants the diagram, follow that choice.
6. If a key point in the source is vague: record it under "Open", and mark it on the diagram with a dashed line or question mark. Do not guess it into a solid-line conclusion.

## Quick reference by material type

- **Conversation / debate**: people → each one's claims → focus of contention → agreements/differences → status summary; HTML uses characters + topic branches.
- **Article / paper**: question → argument/evidence structure → conclusion; HTML uses an argument structure or section map.
- **Tutorial**: goal → steps/modules → what you will learn; HTML uses a step flow.
- **Product brief**: what the product is → feature list → who it is for; HTML uses a feature map.

## Common mistakes

| Mistake | Fix |
|---|---|
| Only a long summary, no structured sections | Produce the text version per the contract |
| Only Mermaid, no HTML | A lightweight HTML must come first by default |
| Writing inferences as facts | Mark "unclear in source" or move it to Open |
| Piling on animation or decorative copy to "look good" | Remove it; keep only labels and relationships that aid understanding |
| Cute figures but you cannot tell who is who | Fixed colors + legend; label with names/roles |
| Several topics squashed into one timeline | Split into topic threads, then mark the crossing points |

## Red flags: stop and correct

- About to deliver only one of the two deliverables (and the user did not ask for just one)
- The diagram contains a conclusion that is not in the source
- Using developer show-me code trees in place of a conversation/article clarification
- Turning "clear presentation" into a rewrite or taking sides
