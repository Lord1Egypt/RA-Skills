---
name: file-organizer
description: "Organize messy folders by moving files into subfolders grouped by extension, date, or category. Use for downloads cleanups and batch file sorting."
version: 1.0.0
slug: file-organizer
homepage: https://clawhub.ai/example/file-organizer
changelog: Initial release of the file organization skill.
user-invocable: true
metadata: {"clawdbot":{"emoji":"🗂️","os":["linux","darwin","win32"]},"openclaw":{"requires":{"anyBins":["python3","python"]}}}
---

## When to Use

Use when the main artifact is an organized folder, for example:

- The user wants a messy downloads, desktop, or project folder sorted into subfolders.
- Files should be grouped by type, extension, or modification date.
- A cleanup should happen safely, with a preview before anything moves.

## Core Rules

### 1. Always preview before moving

- Run `{baseDir}/scripts/organize.py` with `--dry-run` first and show the plan to the user.
- Only run without `--dry-run` after the user confirms the plan.
- Never invent the plan; always read the actual directory first.

### 2. Never lose data

- The script never overwrites existing files: name collisions get a numeric suffix.
- Hidden files, symbolic links, and the script itself are always skipped.
- If a file already sits inside its target group folder, it is left untouched.

### 3. Grouping rules

- `--by type` (default): images, documents, videos, audio, archives, other — based on file extension.
- `--by ext`: one subfolder per extension (for example `pdf/`, `jpg/`).
- `--by date`: one subfolder per `YYYY-MM` based on last-modified time.
- Use `--recursive` to include nested files; without it only the top level is processed.

## Usage

```bash
# Preview only (always do this first)
python {baseDir}/scripts/organize.py "C:\path\to\folder" --by type --dry-run

# Execute after user confirmation
python {baseDir}/scripts/organize.py "C:\path\to\folder" --by type
```

## Common Traps

- Moving files changes paths; anything referencing old paths (shortcuts, scripts, configs) breaks silently.
- The script groups by extension, so files with the wrong or missing extension can land in surprising folders.
- Very large folders are safer to organize in smaller batches by category.

## Output Format

Print one line per planned or executed move plus a summary line at the end. Always report the summary back to the user, and never claim success unless every listed move completed.
