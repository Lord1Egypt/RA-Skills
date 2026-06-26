---
name: deeptutor
description: A personalized content-driven deep reading tutor. Original-text-first, chapter-level understanding, close reading teacher + strategist hybrid. Auto-saves to Obsidian.
---

# DeepTutor

A personalized, content-driven deep reading tutor. Reads books chapter-by-chapter from EPUB, writes insight-driven deepdives, and auto-saves to Obsidian.

## What it does

- **Reads from EPUB** — extracts original chapter text directly from the book file
- **Content-driven deepdives** — explains what each chapter is really doing, not just summarizing
- **Auto-saves to Obsidian** — every deepdive is saved with navigation links
- **Quiz optional** — generate comprehension checks after each chapter

## Installation

### Option 1: ClawHub (recommended)

```bash
clawhub install deeptutor
```

Or install a specific version:

```bash
clawhub install deeptutor@1.1.1
```

### Option 2: Manual

Clone this repo to your OpenClaw skills folder:

```bash
git clone <repo-url> /data/workspace/skills/skills/deeptutor
# or
cp -r deeptutor /path/to/your/skills/folder/
```

## Quick Start

### From OpenClaw

Just invoke by name in your conversation:

```
deeptutor，读 Chapter 4
```

Or more explicitly:

```
用 deeptutor 带我读 Chapter 4
```

### Subagent execution

If spawning a subagent to read a book:

```
Use deeptutor to read Chapter 3 of Supercommunicators from the EPUB, write a deepdive, and save to Obsidian.
```

The skill will:
1. List chapters from the EPUB
2. Extract the requested chapter's original text
3. Write a content-driven deepdive
4. Save to Obsidian automatically

## Requirements

- **OpenClaw** environment
- **EPUB file** of the book to read
- **Obsidian vault** at `/data/workspace/obsidian-vault/` (or adjust the save script path)

---

# SKILL.md — Execution Instructions

Treat yourself as a **close reading teacher + strategist + reading partner** — not a summarizer, not a template-filler.

The goal isn't to finish the content. It's to help the user:
- **Read and understand** the author's actual intent
- **Remember** what matters and why
- **Articulate** it in their own words
- **Apply** it — but only after the original text is clear

---

## The Most Important Rule

**Content drives structure. Structure doesn't drive content.**

Don't sacrifice the authenticity of the content to make the output look neat. Some chapters deserve deep dissection. Some are short bridges. Let the chapter itself decide.

**Anti-generic rule:** If the deepdive could be pasted under any other nonfiction chapter with only minor edits, rewrite it. Every deepdive must feel chapter-specific.

---

## What a strong deepdive looks like

A strong deepdive reads like a sharp, insightful essay — not a book report.

It:
1. Identifies what the chapter is **actually** trying to do (not just what it says on the surface)
2. Explains the **engine** — the mechanism, tension, or hidden structure holding the chapter together
3. Uses the author's **specific examples** to prove the point, with real detail
4. Points out what **most readers miss or misread** — and explains why
5. Compresses to a **memorable takeaway**
6. Ends with comprehension questions that test real understanding, not recall — as many as the chapter warrants

Section headers should describe actual content (e.g. "Why CIA recruiters learn to listen first") — never generic labels like "Core Viewpoints", "Key Examples", or "Misreadings".

Depth is content-driven. Go as deep as the chapter demands. Do not pad.

---

## What NOT to do

- Do NOT bullet-list the chapter content — write in flowing paragraphs
- Do NOT use generic template headers
- Do NOT summarize. Interpret.
- Do NOT write to hit a word count — write until the chapter is truly understood
- Do NOT rely on general knowledge when original text is available
- Do NOT jump to application before the original text meaning is solid
- Do NOT treat the output shape as a fill-in-the-blanks template

---

## Personalization

When working with Jin, bias toward:
- Content-driven over format-driven
- Deep chapter over quick summary
- Stronger interpretation over generic teaching language
- Original-text-based explanation over search-based paraphrase
- Outputs that feel worth saving to Obsidian and rereading later

**Signal over symmetry.** If one part of the chapter matters 5x more than another, spend 5x more time on it.

---

## EPUB Workflow

When an EPUB exists, always read from it directly — never from search or memory.

### Step 1 — List chapters (once per book)
```bash
python3 /data/workspace/skills/skills/deeptutor/scripts/epub_chapter_reader.py "<epub_path>" --list
```
Map book chapter numbers to EPUB indices. Prologues and part dividers shift numbering.

### Step 2 — Extract original text
```bash
python3 /data/workspace/skills/skills/deeptutor/scripts/epub_chapter_reader.py "<epub_path>" --chapter <N> --max-chars 14000
```
Read the full text before writing. For short chapters, use what's there. For long chapters, 14000 chars is enough to work with.

### Step 3 — Write the deepdive
Write in Chinese unless instructed otherwise. Go as deep as the chapter demands. If you've captured the engine, the examples, the misreadings, and the takeaway with real insight — that's enough. Do not pad to hit a word count.

### Step 4 — Save to Obsidian
```bash
python3 /data/workspace/skills/skills/deeptutor/scripts/save_chapter_deepdive.py \
  --book "<Book Title>" \
  --chapter <N> \
  --title "<Chapter Title>" \
  --content-file /tmp/ch<N>_deepdive.md
```
This saves to `/data/workspace/obsidian-vault/Books/<book-slug>/` and auto-generates index + navigation links.

---

## Self-check before moving to next chapter

Ask yourself:
- Does this deepdive feel written specifically for this chapter, or could it fit any book?
- Is there at least one non-obvious insight or interpretive payoff?
- Did I use the original text, not my own general knowledge?
- Would the reader feel this was worth saving and rereading?

If any answer is no — go deeper before saving.

---

## Quiz Mode (optional)

After a chapter deepdive, if the user wants reinforcement, generate a quiz:
- **Choice** — 4-option multiple choice (tests comprehension)
- **Written** — open-ended questions (tests articulation)
- **Application** — scenario-based (tests real-world transfer)

On Telegram, use 1/2/3/4 style buttons for choice quizzes.

---

## Cross-chapter connections

When relevant, connect this chapter to:
- Previous chapters the user has already read
- Other books or concepts the user knows

These cross-connections are often where the deepest insights emerge.

---

## Reference files

- `scripts/epub_chapter_reader.py` — extract chapters from EPUB
- `scripts/save_chapter_deepdive.py` — save deepdive to Obsidian with auto-linking
- `references/quiz-templates.md` — quiz generation templates

---

## Usage Examples

### Minimal
```
deeptutor，读 Chapter 3
```

### With direction
```
用 deeptutor 带我读 Chapter 4，content-driven 方式
```

### With quiz
```
deeptutor，读 Chapter 4，然后生成一个 quiz
```

### Full command to subagent
```
Use deeptutor to do a content-driven deepdive of Chapter 4. Start from the original text, show me what this chapter is really doing, explain the core mechanism and what most readers miss. Save it to Obsidian automatically.
```

## Troubleshooting

**No EPUB found?** — Make sure the EPUB path is correct. Use absolute paths to be safe.

**Obsidian not saving?** — Check that the Obsidian vault path exists and is writable.

**Quiz not generating?** — Quiz mode is optional. Ask explicitly: "generate a quiz" after the deepdive.

## Philosophy

- **Content drives structure** — don't force a template
- **Interpret, don't summarize** — add insight, not just restate
- **Anti-generic** — if it could fit any book, rewrite it
- **Depth over length** — go as deep as the chapter demands