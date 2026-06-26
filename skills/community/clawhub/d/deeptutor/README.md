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
clawhub install deeptutor@1.0.8
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

## Configuration

If your environment differs, you may need to edit `scripts/save_chapter_deepdive.py` to match your Obsidian vault path.

## What a deepdive includes

- What the chapter is actually trying to do (not just what it says)
- The mechanism or tension holding it together
- Key examples from the text
- What most readers miss or misread
- One-line takeaway
- Comprehension questions (as many as the chapter warrants)

## Philosophy

- **Content drives structure** — don't force a template
- **Interpret, don't summarize** — add insight, not just restate
- **Anti-generic** — if it could fit any book, rewrite it
- **Depth over length** — go as deep as the chapter demands

## Files

```
deeptutor/
├── SKILL.md           # Execution instructions (for subagents)
├── README.md           # This file
├── scripts/
│   ├── epub_chapter_reader.py      # Extract chapters from EPUB
│   └── save_chapter_deepdive.py    # Save deepdive to Obsidian
├── references/
│   └── quiz-templates.md           # Quiz generation templates
└── .clawhub/
    └── origin.json
```

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

## Author

Built for personal book reading workflow. Prioritizes depth, original text, and insight over format.