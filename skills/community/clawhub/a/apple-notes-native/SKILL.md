---
name: apple-notes
description: Use this skill when the task involves reading, searching, creating, editing, organizing, or moving Apple Notes on macOS. This includes finding notes, creating folders, moving notes into folders, appending structured content to an existing note, and writing well-formatted content into Apple Notes without re-testing multiple access methods.
homepage: https://github.com/lishix520/apple-notes-skill
metadata: {"openclaw":{"emoji":"📝","homepage":"https://github.com/lishix520/apple-notes-skill","os":["darwin"],"requires":{"bins":["osascript"]}}}
---

# Apple Notes Skill

Use this skill for Apple Notes tasks on macOS.

Typical triggers:

- Read an existing Apple Note
- Search notes by title or content
- Create a note
- Append or update a note
- Create a folder
- Move a note into a folder
- Organize uncategorized notes
- Save project progress into Apple Notes
- Save processed content into a specific note

Do not use this skill for summarizing or translating itself. Do that work first, then use this skill to operate on Apple Notes.

Classification is allowed when it directly supports organization. If the task is to sort uncategorized notes, the agent may infer a practical destination folder and then move the note there. Keep the classification simple and action-oriented. Do not turn this skill into a general taxonomy design exercise.

## Preferred Method

Use the already validated Apple Notes access method first. Do not waste time retrying multiple unrelated approaches.

Default rule:

- Prefer `osascript` with Apple Notes automation
- Reuse the known working command pattern for the current machine
- Only switch approach if the preferred method clearly fails

## Working Style

When operating on Apple Notes:

- Search before creating when there is any chance the note already exists
- Prefer append/update over replacing the whole note
- Keep formatting clean and readable
- Be conservative with move and delete
- If the target note is ambiguous, stop and clarify instead of guessing

## Practical Workflows

### Organize Uncategorized Notes

- Search or list candidate notes first
- Infer a reasonable folder based on title and content
- Create the folder if it does not exist
- Preview the source note and destination folder before moving in bulk
- If classification confidence is low, stop and ask instead of guessing

For large messy folders, do not try to solve everything in one pass.

Preferred sequence:

- First pass: move only high-confidence matches
- Second pass: create a few practical flat folders for recurring themes
- Final pass: move the leftovers into a deliberate catch-all folder instead of leaving them unorganized forever

For Apple Notes specifically, flat folder names are safer than fake hierarchical names.

Prefer:

- `系统结构`
- `觉察与能量`
- `行动与方法`
- `对话摘录`
- `思辨片段`

Avoid creating pseudo-nested names unless you know the current Notes setup supports them well.

### Update Project Progress

- Search for the existing project note first
- If found, append a dated update section
- If not found, create a project note in the best matching folder
- Preserve existing history; do not replace the whole note

### Save Processed Content Into Notes

- Finish the upstream work first, such as extraction, translation, or summary
- Search for the target note or decide whether a new one is needed
- Write the final content in a clean Apple Notes friendly structure

## Core Actions

### Read Notes

Use when the user wants existing content, project history, or note contents.

Default behavior:

- Find the note first by title or nearby keywords
- If multiple results match, narrow before reading
- Read the target note only after identifying it confidently

### Search Notes

Use search when:

- The exact note name is unknown
- The user refers to a topic, not a title
- You need to locate candidate notes before moving or updating

Return the best matching notes first, then act on the chosen note.

### Create Note

Create a new note only when:

- Search shows no existing target note
- The user explicitly wants a new note

Before creating:

- Choose the correct folder if known
- Use a clear title
- Write content in clean structure, not a text block dump

### Edit Or Append

Prefer append/update when a note already exists.

Default rule:

- Append new sections rather than rewriting old content
- Preserve existing structure unless the user asks for cleanup
- Avoid destroying manually written content

### Create Folder

Create folders when:

- The user is organizing notes
- A project needs a stable home
- A clear category does not already exist

Use simple, stable names. Do not create many near-duplicate folders.

### Move Note

Move a note only after confirming the destination is correct.

Default rule:

- Search and identify the note
- Confirm the destination folder is the intended one
- For bulk moves, preview the mapping before executing

### Delete Note

Delete is high risk.

Default rule:

- Do not delete unless the user clearly asks
- If the target is ambiguous, clarify first
- Prefer caution over speed

## Formatting Rules

Never write dense wall-of-text notes if the content is more than a few lines.

Use clean spacing:

- A clear title
- Short intro if needed
- Blank lines between paragraphs
- Bullets for lists
- Headings for sections

Recommended patterns:

### Project Update

Use:

```md
# Project Name

## Update - YYYY-MM-DD

### Status

Short status summary.

### Done

- Item

### In Progress

- Item

### Next

- Item

### Risks / Blockers

- Item
```

### Article Notes

Use:

```md
# Article Title

## Source

- Link:
- Date:

## Summary

Short summary.

## Key Points

- Point

## Notes

- Note
```

## Verified `osascript` Patterns

Use shell-wrapped `osascript` blocks when there is any risk the agent may accidentally paste AppleScript directly into `zsh`.

### List all folders

```bash
osascript -e 'tell application "Notes" to get name of every folder'
```

### Read a note body

```bash
osascript -e 'tell application "Notes" to get body of note "Apple Notes Skill Reference" of first folder'
```

### Search notes in a folder by title

```bash
osascript -e 'tell application "Notes" to get name of every note of folder "输出/学习笔记" whose name contains "Apple Notes"'
```

### Create a new note with multi-line shell input

```bash
osascript <<'EOF'
tell application "Notes"
    activate
    tell folder "Claude 协作"
        make new note with properties {name:"Apple Notes Skill", body:"<h1>Apple Notes Skill</h1><br><div>Structured content goes here.</div>"}
    end tell
end tell
EOF
```

### Append content carefully

Default pattern:

- Read the existing body first
- Preserve structure
- Append a new section instead of overwriting the entire note unless explicitly requested

## Error Handling

When a Notes action fails:

- Check whether Automation permission is blocked
- Check whether the folder exists
- Check whether the note title is ambiguous
- Retry the same validated method before inventing a new one

If a destination folder does not exist:

- Create it first
- Then create or move the note

If multiple notes share the same title:

- Narrow by folder or related keywords before editing or moving

## Limitations

Keep these in mind:

- Apple Notes access depends on macOS Automation permission
- Rich text body may be returned as HTML-like content
- Reading may expose HTML tags such as `<div>` or `<br>`
- Writing should use Apple Notes friendly structure and line breaks
- Apple Notes organization is simpler and flatter than full document systems

When reading note bodies:

- Be aware that the raw body may include HTML-ish markup
- Normalize the content mentally before interpreting structure

When writing note bodies:

- Use headings, paragraphs, and explicit spacing
- Do not dump one giant block of text

## Coordination With Other Skills

This skill handles Apple Notes operations.

Upstream work can be done by other skills or by the agent itself:

- article reading
- paper reading
- summary
- translation
- extraction

Do that work first, then use this skill to save or update the final result in Apple Notes.
