# File Organizer Skill

Automatically sort, rename, and organize files into structured folders.

## Features

- **Auto-sorting** — Files categorized into 10 folder types (images, documents, audio, video, archives, code, data, installers, fonts, other)
- **Smart renaming** — Extracts dates, removes special characters, handles duplicates
- **Undo/restore** — Full rollback capability via `ORGANIZE_LOG.json`
- **Dry-run mode** — Preview changes without touching files
- **Configurable** — Customize categories, patterns, exclusions, file size limits

## Quick Start

```bash
# Organize downloads
python3 scripts/organize.py ~/Downloads

# Preview changes first
python3 scripts/organize.py ~/Downloads --dry-run

# Undo last organization
python3 scripts/organize.py --undo

# Output as JSON
python3 scripts/organize.py ~/Downloads --json
```

## Configuration

Edit `config.yaml`:

```yaml
source_dirs:
  - ~/Downloads
target_base: ~/organized-files
rename_pattern: "{name}_{date}"  # or "none"
max_file_size_mb: 500
exclude_patterns:
  - "*.tmp"
  - ".DS_Store"
```

## File Categories

| Folder | Extensions |
|--------|-----------|
| images | jpg, png, gif, svg, webp, bmp, tiff, ico |
| documents | pdf, doc, docx, txt, rtf, odt, ppt, xls |
| audio | mp3, wav, flac, ogg, aac, m4a |
| video | mp4, mkv, avi, mov, webm, flv |
| archives | zip, tar, gz, 7z, rar, bz2, xz |
| code | py, js, ts, html, css, md, json, yaml |
| data | csv, xml, db, sqlite, dat, log |
| installers | exe, msi, dmg, app, pkg, deb, rpm, apk |
| fonts | ttf, otf, woff, woff2, fon |
| other | uncategorized files |

## License

MIT
