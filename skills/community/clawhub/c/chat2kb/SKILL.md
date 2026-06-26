---
name: chat2kb
description: Convert chat conversations into structured Markdown knowledge-base files. Use when the user wants to save, capture, export, or document a conversation, including requests like "save this conversation", "export our discussion", "generate KB", "turn this into notes", "保存对话", "生成知识库", "转成KB", or "导出笔记".
license: MIT
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["date", "openssl"],
            "env": ["CHAT2KB_FOLDER", "CHAT2KB_DRY_RUN", "CHAT2KB_LOG_LEVEL"],
            "configPaths": ["~/.chat2kb/config.yml"]
          }
      }
  }
---

# Chat2KB for OpenClaw

Convert chat history into clean, structured Markdown knowledge-base files.

## When To Use

Use this skill when the user wants to:

- save the current conversation as notes or KB
- export part or all of a discussion into Markdown
- turn a design/debug/brainstorming thread into reusable documentation
- update a previously saved KB entry with new discussion content

If the request is ambiguous, ask one short clarification question instead of skipping the export flow.

## OpenClaw Workflow

### Step 1: Detect topics

Read the relevant conversation scope and identify distinct topics.

- If the user specified a time range or topic, honor that first
- If only one topic is present, continue directly
- If multiple topics are present, present a numbered list
- Support `all` to save each topic separately
- Support `combine` to merge selected topics into one KB file

Use this format when multiple topics are found:

```
Detected 3 topics:

1. [Title]
   [One-sentence summary]

2. [Title]
   [One-sentence summary]

3. [Title]
   [One-sentence summary]

Which topics would you like to save?
-> Enter numbers, e.g. 1,3
-> Enter all
-> Enter combine
```

### Step 2: Check for previous export

Before generating a new file, scan the conversation for a previous `conversation_id` for the same topic.

- If no previous export exists, generate a new ID
- If a previous export exists, ask whether to update, append, or create a new KB

Conversation ID format:

```
kb_{YYYYMMDD}_{HHMMSS}_{6hex}
Example: kb_20260410_143052_a7c9e2
```

Generation:

```bash
CONVERSATION_ID="kb_$(date +%Y%m%d_%H%M%S)_$(openssl rand -hex 3)"
```

Use this prompt when a previous export exists:

```
Found a previous KB for this topic (ID: kb_20260410_143052_a7c9e2)

-> A: Update (regenerate the full KB with all content)
-> B: Append (export only content added since last save)
-> C: New (ignore previous KB, create an independent one)
```

### Step 3: Extract content

For each selected topic, extract:

- `summary`: 1-2 paragraph overview
- `key_points`: grouped by theme, not chronology
- `code_examples`: only if code was discussed
- `action_items`: completed and pending items

Extraction rules:

- preserve technical accuracy over elegance
- group related ideas by theme
- prefer decisions, tradeoffs, and takeaways over transcript-like detail
- include code only when it helps future reuse
- omit empty sections instead of leaving placeholders

### Step 4: Generate Markdown

Use this structure:

```markdown
---
conversation_id: kb_20260410_143052_a7c9e2
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
export_type: full
topics: [tag1, tag2]
language: en
participants: [User, Assistant]
platform: openclaw
word_count: 342
---

# [Topic Title]

**Date**: YYYY-MM-DD

## Summary

[1-2 paragraphs]

## Key Points

### [Theme 1]
- insight
- detail

### [Theme 2]
- insight

## Code Examples

```language
// code
```

## Action Items

- [x] Done item
- [ ] Pending item
```

Rules:

- group by theme, not chronology
- use bullet points in `Key Points`
- omit `Code Examples` if no code was discussed
- omit `Action Items` if none exist
- do not include a full transcript
- set `word_count` to the total number of words in the body (excluding frontmatter)

### Step 5: Preview before writing

Always show the generated Markdown before writing the file.

Use this preview structure:

```
Preview (not saved yet)

[full Markdown content]

Will save to: /path/to/YYYY-MM-DD-topic-slug.md

-> Y Save
-> E Edit summary
-> N Cancel
```

If the user chooses `E`, accept the revised summary, regenerate the preview, and ask again.

### Step 6: Resolve save path and write

Resolve the save path in this order:

1. `~/.chat2kb/config.yml`
2. `CHAT2KB_FOLDER`
3. ask the user

Config file example:

```yaml
kb_folder: ~/Documents/KnowledgeBase
dry_run: false
create_backup: true
log_level: info
```

Environment overrides:

| Variable | Purpose |
|---|---|
| `CHAT2KB_FOLDER` | KB save location |
| `CHAT2KB_DRY_RUN` | `true` = preview only |
| `CHAT2KB_LOG_LEVEL` | Logging verbosity |

Write behavior:

- create the directory if needed
- use filename `YYYY-MM-DD-<topic-slug>.md`
- for incremental export use `YYYY-MM-DD-<topic-slug>-part{N}.md`
- if config `dry_run: true` or `CHAT2KB_DRY_RUN=true`, do not write the file; clearly report preview-only mode
- if overwriting and `create_backup: true`, create a backup first

### Slug rules

The `<topic-slug>` in the filename must follow these rules:

- lowercase alphanumeric and hyphens only
- no leading or trailing hyphens
- maximum 50 characters
- derived from the conversation topic

Examples:
- `2026-04-10-react-performance-optimization.md` ✅
- `2026-04-10-react-performance-optimization-and-other-things.md` ❌ too long
- `2026-04-10--react.md` ❌ double hyphen

### Step 7: Confirm success

After writing, report:

- saved file path
- filename
- `conversation_id`

Use this format:

```
Knowledge base saved!

Location: /absolute/path/to/2026-04-10-react-optimization.md
ID: kb_20260410_143052_a7c9e2
```

If running in dry-run mode, say so explicitly:

```
Dry run complete — preview generated, no file written.
```

## Error Handling

### Cannot write to folder

```
Cannot write to folder: /path/to/folder
Reason: directory does not exist or no write permission
```

Suggested fixes:

- create the directory
- check write permissions
- ask the user for an alternate save location

### No content found

```
No content to export.
Reason: no messages found in the selected time range.
```

Suggested fixes:

- export the full conversation
- widen the requested time range

### File conflict

```
File already exists: 2026-04-10-react-optimization.md
-> A: Overwrite
-> B: Rename
-> C: Cancel
```
