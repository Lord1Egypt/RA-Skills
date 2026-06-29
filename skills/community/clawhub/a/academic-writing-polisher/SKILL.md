---
name: academic-writing-polisher
description: Use when researchers need a Nature-inspired, context-first workflow to polish academic paragraphs, abstracts, reviewer responses, peer-review comments, or editorial feedback. Revises for clarity, coherence, concision, and journal-ready tone while preserving author intent, avoiding invented claims or citations, and flagging ambiguity or meaning risks.
version: 1.0.0
metadata:
  openclaw:
    emoji: "✍️"
    homepage: https://github.com/Figpad/academic-writing-polisher
---

# Academic Writing Polisher

Use this skill to polish academic writing responsibly. The goal is not to write the paper for the user. The goal is to help the user express their own research meaning more clearly, coherently, concisely, and professionally.

This workflow is inspired by context-first academic writing practices discussed in Dritjon Gruda's Nature Career Column, "Three ways ChatGPT helps me in my academic writing" (2024), DOI: `10.1038/d41586-024-01042-3`.

## When To Use

Use this skill when the user asks to:

- Polish, revise, or improve academic writing.
- Improve clarity, coherence, concision, flow, or journal-ready tone.
- Rewrite an abstract, paragraph, introduction, discussion, limitation, or conclusion.
- Draft or refine responses to reviewers.
- Organize peer-review comments or editorial feedback.
- Improve academic English while preserving the user's meaning.

Do not use this skill for literature review, citation discovery, data analysis, journal selection, or generating new scientific claims unless the user separately asks for that workflow.

## Core Rule

Never silently add intellectual content. Do not invent claims, mechanisms, citations, results, limitations, methods, implications, or author intent.

If meaning is unclear, flag the ambiguity and offer a conservative revision.

## Context First

Before revising, collect missing context when it materially affects the edit. Ask only the questions needed for the current passage.

Useful context:

- Field or discipline.
- Document type: paper, thesis, abstract, rebuttal, review, editorial letter.
- Target audience or journal level.
- Section role: introduction, method, results, discussion, limitation, response to reviewer.
- Intended meaning in plain language.
- Desired edit strength: light polish, moderate rewrite, heavy restructure.
- Tone: concise, formal, direct, diplomatic, assertive, cautious.
- Terms, phrases, citations, or claims that must stay unchanged.

If the user already supplied enough context, proceed without asking.

## Revision Modes

Choose the smallest mode that solves the task:

- `Light polish`: grammar, word choice, flow, and academic tone.
- `Clarity rewrite`: restructures sentences to make the intended meaning easier to follow.
- `Concision`: removes repetition, filler, and unnecessary hedging.
- `Coherence`: improves paragraph order, transitions, and logical flow.
- `Reviewer response`: makes responses specific, respectful, and action-oriented.
- `Peer-review feedback`: organizes the user's notes into clear review comments without uploading or exposing confidential manuscript text beyond what the user provided.
- `Editorial feedback`: turns decision notes into direct, respectful, actionable letters.

## Output Format

For most polishing tasks, return:

```markdown
**Polished Version**
[revised text]

**What Changed**
- [brief explanation of major edits]

**Meaning Check**
- Preserved: [key meaning preserved]
- Please verify: [any assumption or ambiguous point]

**Risk Flags**
- [invented-claim/citation/overstatement/ambiguity risks, or "None noticed"]
```

For very short requests, you may omit headings if a concise answer is better, but still preserve meaning and flag risks.

## Style Principles

- Prefer clear academic prose over ornate phrasing.
- Preserve field-specific terminology unless the user asks to simplify jargon.
- Keep claims calibrated: "suggests", "may", "is associated with", and "demonstrates" are not interchangeable.
- Keep citations exactly as provided.
- Keep statistical values, gene/protein names, chemical names, model names, and labels unchanged unless the user asks otherwise.
- Do not make the text sound more certain than the evidence supports.
- Avoid generic filler such as "plays a crucial role" unless the user's field and sentence require it.

## Reviewer Response Rules

When revising responses to reviewers:

- Start by acknowledging the reviewer's point.
- State what was changed, where it was changed, and why.
- If disagreeing, be respectful and evidence-based.
- Do not claim that a change was made unless the user says it was made.
- Separate "response text" from "manuscript revision text" when both are requested.

## Peer Review And Editorial Rules

When helping with peer review or editorial feedback:

- Work from the user's summary, notes, and judgments.
- Do not pretend to have read a manuscript that was not provided.
- Do not create confidential details.
- Organize limitations by importance when asked.
- Make feedback specific, constructive, and professional.

## Reference Templates

If the user needs reusable prompts or examples, read:

- `references/prompt-patterns.md` for reusable task prompts.
- `references/examples.md` for before/after examples and launch copy.
