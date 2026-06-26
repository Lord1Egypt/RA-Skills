# Apply (Interactive Diff Review)

Run `chezmoi diff`, parse each changed file, and let the user decide per-file whether to apply (chezmoi), keep local, or skip.

## When to Use

- `/chezmoi apply` — interactive apply with per-file approval
- After modifying `.chezmoi-lib/` or `modify_*.sh.tmpl` scripts
- Periodic chezmoi sync check

## Procedure

### 1. Run diff

```bash
chezmoi diff 2>&1
```

### 2. Parse diff into file list

Extract changed files from `diff --git a/<path>` headers.

### 3. Classify each file

For each changed file, summarize the change in one line:
- What changed (added/removed/modified keys, trailing newline, etc.)
- Flag problems: script errors (`command not found`), duplicate entries, file deletions

### 4. AskUserQuestion per file (questions array)

Present all files in a single `AskUserQuestion(questions: [...])` call (max 4 per call, batch if more):

```
AskUserQuestion({
  questions: [
    {
      question: ".claude/settings.json — sort permissions.allow + add new permissions. Which side?",
      header: "settings",
      options: [
        { label: "chezmoi (apply)", description: "Overwrite with chezmoi result" },
        { label: "Keep local", description: "Keep current file; modify script needs fixing" }
      ]
    },
    ...
  ]
})
```

Options per file:
- **chezmoi (apply)** — `chezmoi apply <target-path>`
- **Keep local** — skip, optionally note that the modify script needs fixing
- If a problem is detected (script error, duplicate), **recommend skip** and explain why

### 5. Apply selected files

```bash
chezmoi apply "$HOME/<path1>"
chezmoi apply "$HOME/<path2>"
```

Only apply files the user approved.

### 6. Verify

```bash
# Confirm remaining diff (should only contain skipped files)
chezmoi diff 2>&1 | grep "^diff"
```

## Problem Detection

| Pattern | Action |
|---------|--------|
| `command not found` in diff | Script dependency missing — recommend skip + install |
| File deleted (`deleted file mode`) | Modify script produced empty output — recommend skip |
| Duplicate entries | Modify script bug — recommend skip + fix script |
| Trailing newline only | Safe to apply (cosmetic) |

### 7. Commit tidy

After all selected files are applied, run `/commit-tidy` to organize chezmoi source changes into clean commits.

```
/commit-tidy
```

## Trigger Keywords

- "chezmoi apply", "review chezmoi diff", "diff one at a time", "per-file apply"
