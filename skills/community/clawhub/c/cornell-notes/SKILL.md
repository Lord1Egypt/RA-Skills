---
name: notes
description: >
  Manage Cornell Method notes as Markdown files using the bundled cornell.py CLI script.
  Use this skill whenever the user wants to take notes, create a new note, view, list,
  search, edit, or delete Cornell-style notes. Trigger on phrases like "take a note",
  "create a note", "show my notes", "list notes", "search notes", "open my note on X",
  "delete note", "edit my note", or any request involving personal notes or note-taking.
  Also trigger when the user says things like "save this as a note" 
  or "what did I write about X". Always prefer this skill over ad-hoc solutions
  for anything note-related.
---

# Notes Skill

Manage Cornell Method notes stored as Markdown files in `~/cornell-notes/`.
One `.md` file per note. Uses the bundled `scripts/cornell.py` CLI tool.

## Script location

```
scripts/cornell.py
```

Always run it with:
```bash
python scripts/cornell.py <command> [args]
```

The script path must be relative to the skill root, or use the absolute path once
you know it. Copy the script to `/tmp/cornell.py` for convenience if needed:
```bash
cp <skill_root>/scripts/cornell.py /tmp/cornell.py
```

## Commands

| Command | What it does |
|---|---|
| `new [title]` | Create a new Cornell note (opens in `$EDITOR` / micro) |
| `list` / `ls` | List all notes with title and date |
| `view [note]` | Pretty-print a note in two-column Cornell layout |
| `search [query]` | Search all notes by keyword, highlights matches |
| `edit [note]` | Open a note in `$EDITOR` for editing |
| `delete [note]` / `rm` | Delete a note (asks for confirmation) |

Notes can be referenced by **number**, **title**, or **slug**. If ambiguous, the script
shows an interactive picker.

## Note structure (auto-generated)

Each note has YAML frontmatter + three Cornell sections:

```markdown
---
title: <Title>
date: <YYYY-MM-DD HH:MM>
tags: []
---

## Notes
<!-- Raw lecture / reading notes -->

## Cues
<!-- Keywords, questions, main ideas — filled in after studying -->

## Summary
<!-- 2-3 sentence synthesis in your own words -->
```

## Workflow

### Creating a note
1. Ask the user for the note title if not provided.
2. Run: `python /tmp/cornell.py new "<title>"`
3. Tell the user the file was created at `~/cornell-notes/<slug>.md` and that it
   opened in their editor (micro by default). Remind them to fill in the three sections.

### Viewing / listing
- For a quick overview: `python /tmp/cornell.py list`
- To read a specific note: `python /tmp/cornell.py view "<title or number>"`
- Render the output in the conversation so the user can read it.

### Searching
- Run: `python /tmp/cornell.py search "<keyword>"`
- Present the matching notes and highlighted lines to the user.

### Editing
- Run: `python /tmp/cornell.py edit "<title or number>"`
- Confirm which note was opened.

### Deleting
- Run: `python /tmp/cornell.py delete "<title or number>"`
- The script will ask for confirmation — relay that to the user if running non-interactively.

## Tips

- Notes are stored in `~/cornell-notes/` — the directory is created automatically.
- The script uses `$EDITOR` or `$VISUAL` env var, falling back to `micro`.
- Slugs are auto-generated from titles (lowercased, spaces → hyphens).
- When the user asks to "take a note now", offer to capture their content directly and
  write it into the appropriate Cornell sections yourself, then save the file.
