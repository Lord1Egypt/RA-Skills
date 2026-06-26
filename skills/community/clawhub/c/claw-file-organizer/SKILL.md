---
name: file-organizer
description: Automated file management — sorts downloads folder by type, renames files with consistent patterns, generates structured folder hierarchy, with undo/restore capability. Use when: (1) Downloads folder is chaotic, (2) Need to organize files by category, (3) Want consistent naming conventions, (4) Need to restore files to original state, (5) Want to batch-rename files
---

# File Organizer Skill

Automatically sort, rename, and organize files into structured folders. Reduces chaos in Downloads and any directory with scattered files.

## Quick Start

```bash
# Install the skill
npx clawhub install file-organizer

# Organize your downloads folder
"Organize my Downloads folder"

# Organize a specific directory
"Organize ~/Documents/projects"

# Undo the last organization
"Undo the last file organization"
```

## Core Features

### 1. Automatic Sorting

Files are categorized into standard folders:

- **Images** (`images/`) — JPG, PNG, GIF, SVG, WEBP, BMP, TIFF, ICO
- **Documents** (`documents/`) — PDF, DOC, DOCX, TXT, RTF, ODT, PPT, PPTX, XLS, XLSX, PPT, ODP
- **Audio** (`audio/`) — MP3, WAV, FLAC, OGG, AAC, M4A
- **Video** (`video/`) — MP4, MKV, AVI, MOV, WEBM, FLV
- **Archives** (`archives/`) — ZIP, TAR, GZ, 7Z, RAR, BZ2, XZ
- **Code** (`code/`) — PY, JS, TS, HTML, CSS, MD, JSON, YAML, SH, BAT
- **Data** (`data/`) — CSV, JSON, XML, SQL, DB, SQLITE, DAT
- **Executables** (`installers/`) — EXE, MSI, DMG, APP, PKG, DEB, RPM, APK
- **Fonts** (`fonts/`) — TTF, OTF, WOFF, WOFF2, FON
- **Other** (`other/`) — uncategorized files

### 2. Smart File Renaming

- Extracts dates from filenames (YYYY-MM-DD patterns) and places them in naming
- Converts spaces to underscores for consistency
- Strips special characters (preserving hyphens in compound names)
- Handles duplicate names by appending `_2`, `_3`, etc.
- Preserves original extension case (lowercased for consistency)

### 3. Undo / Restore

- Generates a `ORGANIZE_LOG.json` after each operation
- Stores original path, new path, and timestamp for every move
- `undo` command restores files to their exact original locations
- Safe: only restores if files haven't been modified since

### 4. Preview Mode

- `--dry-run` shows what would change without moving files
- Reports counts by category and renamed files
- No disk writes in dry-run mode

## Configuration

Edit `config.yaml` to customize:

```yaml
source_dirs:
  - ~/Downloads

target_base: ~/organized-files
auto_sort: true
rename_pattern: "{name}_{date}"  # or "none" to skip renaming
max_file_size_mb: 500  # skip files larger than this
exclude_patterns:
  - "*.tmp"
  - "*.swp"
  - ".DS_Store"
  - "Thumbs.db"
log_file: ORGANIZE_LOG.json
```

## File Type Patterns

Full mapping is in `references/file-patterns.md`. You can add custom mappings:

```yaml
custom_types:
  - name: "Design Assets"
    folders: "design/"
    extensions: [AI, PSD, SKETCH, FIG, INDD]
```

## Safety

- **Dry-run first**: Always review changes before committing
- **Undo-safe**: Every move is logged; full restore possible
- **Size limits**: Skip large files to avoid moving heavy media
- **Exclude patterns**: Configurable file filters to skip unwanted types
- **No data loss**: Only moves files; never deletes

## Integration

- Works with any directory (Downloads, Documents, Desktop, project roots)
- Integrates with cron-manager for periodic auto-organizing
- Compatible with file-sync workflows
- Output is compatible with cloud storage (consistent naming)
