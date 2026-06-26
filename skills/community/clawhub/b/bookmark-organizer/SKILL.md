
---
name: bookmark-organizer
description: Imports a browser bookmark HTML file and transforms it into a structured, categorized, and time-sorted Markdown knowledge base. Includes features for deduplication, dead-link checking, and customizable classification rules.
---

# Bookmark Organizer Skill (v1.0)

This skill provides a robust, reusable script to turn a standard browser bookmark export file (HTML) into a clean, categorized, and searchable knowledge base in Markdown format.

## Core Features

- **Parses Standard Bookmark Files**: Extracts links, titles, and creation dates.
- **Automatic Deduplication**: Processes each unique URL only once.
- **Customizable Categorization**: Uses an external `rules.json` file, allowing any user to define their own categories and keywords without editing code.
- **Dead Link Checking**: An optional flag (`--check-links`) finds and reports broken or inaccessible links, and excludes them from the final lists.
- **Time-Sorted Output**: All lists are sorted chronologically with the newest bookmarks first.

## How to Use

### 1. (Optional) Customize Rules

To change how links are categorized, edit the `rules.json` file located in the script's directory.

File: `skills/bookmark-organizer/scripts/rules.json`

### 2. Run the Organizer Script

Execute the `organize.py` script, providing the input HTML path and a desired output directory. Use the optional `--check-links` flag to perform a network check on all URLs.

**Command:**
```bash
python3 /path/to/organize.py <input_file> <output_dir> [--check-links]
```

**Example:**
```bash
# Define paths
SKILL_SCRIPT="/root/.openclaw/workspace-aii/skills/bookmark-organizer/scripts/organize.py"
INPUT_FILE="./bookmarks/import/bookmarks.html"
OUTPUT_DIR="./bookmarks/organized_v1"

# Create output directory
mkdir -p $OUTPUT_DIR

# Run the script (with dead link checking)
python3 $SKILL_SCRIPT $INPUT_FILE $OUTPUT_DIR --check-links
```

### 3. Review the Output

The script will generate:
- **Markdown files for each category** (e.g., `ai-art.md`, `games-mods.md`).
- A `_SUMMARY.md` file with statistics.
- If checked, a `_dead_links_report.md` file.

Start by inspecting `_SUMMARY.md` to get an overview.
