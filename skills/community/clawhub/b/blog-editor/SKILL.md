---
name: blog-editor
description: >
  Edit, polish, and improve a blog post draft written in Markdown. Use this
  skill whenever the user wants to refine a blog draft — fixing grammar,
  improving clarity, enhancing thin content, checking paragraph structure,
  and preserving the original language (Chinese, English, or mixed). Trigger
  when user mentions "blog", "draft", "post", "article", or uploads/pastes a
  markdown file they want reviewed. Also trigger on phrases like "clean up my
  post", "check my writing", "improve my blog", or "review my draft".
---

# Blog Editor

Polish a blog draft in Markdown — fix grammar, fill in thin spots, flag
structure issues, and keep the original voice and language intact.

---

## Before You Start

This skill needs no external dependencies — it's pure Markdown in, Markdown
out. No Python, no scripts, no packages to install.

**What you need:**
- The blog draft as a `.md` file (or pasted text)
- The `md` skill loaded (you already have it — you said so!)

That's it. You're good to go.

---

## Step 1 — Read the Draft

Ask the user to paste or upload their blog draft if they haven't already.

Once you have it, read it in full before doing anything. Don't start editing
mid-read. Get the full picture first — tone, topic, structure, language(s).

Note these things as you read:
- What language(s) is it written in?
- What's the overall vibe? (casual, technical, personal?)
- Are there sections that feel thin or confusing?
- Are there grammar issues?
- Does the paragraph order make sense?

---

## Step 2 — Grammar & Language Check

Go through the draft and fix grammar issues. Rules:

**Fix silently (no need to ask):**
- Spelling mistakes
- Punctuation errors
- Subject-verb agreement
- Tense consistency
- Run-on sentences or obvious typos

**Language rule — important:**
- Keep the original language as-is. Chinese stays Chinese. English stays
  English. Do NOT translate unless a sentence mixes languages in a way that
  breaks meaning.
- If you do change language in a spot (rare), **highlight it** with a comment
  like: `<!-- ⚠️ Language changed here: [reason] -->`
- If there's genuinely conflicting content between the two languages in a
  bilingual post, flag it to the user before changing anything.

---

## Step 3 — Content Enhancement

For sections that are too thin, vague, or feel incomplete — add a bit more
context or explanation. But keep these rules:

- Keep it as simple as the original. Don't make it fancy if the original
  wasn't.
- Don't add fluff. Only add something if it actually helps the reader
  understand.
- Don't change the author's voice. If they write casually, keep it casual.
  If they write short punchy sentences, don't pad them out.
- If a section is missing a key point that would make it confusing without
  it, add it — but note what you added with a comment:
  `<!-- ✏️ Enhanced: added [brief reason] -->`

---

## Step 4 — Paragraph Structure Check

Read through the structure. Ask yourself:

- Does the intro actually introduce the topic?
- Do the sections flow in a logical order?
- Does the conclusion wrap things up, or does it just stop?
- Are any paragraphs doing too much (should be split)?
- Are any paragraphs doing too little (should be merged or cut)?

**If you spot a structural issue — do NOT just change it.**
Flag it like this and ask the user first:

```
⚠️ Structure suggestion: The section "[X]" feels like it would land better
after "[Y]" because [reason]. Want me to move it?
```

Wait for a yes before touching the order.

---

## Step 5 — Output the Edited Draft

Once grammar is fixed and content is enhanced, output the full edited
Markdown file. Use the `md` skill to write it out properly.

Save it as: `[original-filename]-edited.md`

At the top of your response, give a short summary of what you changed:

```
## What I changed
- Grammar: [brief summary]
- Enhanced: [which sections, and why]
- Flagged for your input: [list any structure questions]
- Language notes: [if any language was changed, explain here]
```

---

## Tone Reminders

- Stay in the author's voice. You're editing, not rewriting.
- Don't over-polish. A blog doesn't need to read like a textbook.
- Spoken and informal language is fine — don't sanitize it into corporate
  speak.
- If something sounds weird but it's intentional style, leave it alone.

---

## Example Flow

**User says:** "here's my blog draft, can you clean it up?"

**You do:**
1. Read the whole thing
2. Fix grammar quietly
3. Enhance thin sections (keep it simple)
4. Flag any structure questions and ask
5. Output the edited `.md` file with a change summary

---

## Dependencies

None. This skill is pure Markdown. No installs needed.

The only requirement is the `md` skill — which you already have set up.
