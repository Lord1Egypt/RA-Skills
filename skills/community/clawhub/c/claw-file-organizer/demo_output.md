# File Organizer Demo Output

## Source: ~/Downloads (before)

```
downloads/
├── photo.jpg
├── report 2025-03-15.pdf
├── song.mp3
├── video.mp4
├── archive.zip
├── script.py
├── data.csv
├── installer.exe
├── font.ttf
├── unknown.xyz
├── .DS_Store
├── temp.tmp
└── backup.tar.gz
```

## After Running: `python3 scripts/organize.py ~/Downloads`

### Directory Structure (after)

```
organized-files/
├── images/
│   └── photo.jpg
├── documents/
│   └── report_2025-03-15.pdf
├── audio/
│   └── song.mp3
├── video/
│   └── video.mp4
├── archives/
│   ├── archive.zip
│   └── backup.tar.gz
├── code/
│   └── script.py
├── data/
│   └── data.csv
├── installers/
│   └── installer.exe
├── fonts/
│   └── font.ttf
└── other/
    └── unknown.xyz
```

Excluded (not moved):
- `.DS_Store` — in exclude_patterns
- `temp.tmp` — in exclude_patterns

### Rename Behavior

| Original | Result | Reason |
|----------|--------|--------|
| `report 2025-03-15.pdf` | `report_2025-03-15.pdf` | Date extracted, spaces → underscores |
| `photo.jpg` | `photo.jpg` | No changes needed |

### Undo

Running `python3 scripts/organize.py --undo` restores all files to `~/Downloads`.

### Dry Run

`python3 scripts/organize.py ~/Downloads --dry-run` previews:
```
[DRY RUN] photo.jpg → images/photo.jpg
[DRY RUN] report 2025-03-15.pdf → documents/report_2025-03-15.pdf
[DRY RUN] song.mp3 → audio/song.mp3
[DRY RUN] video.mp4 → video/video.mp4
[DRY RUN] archive.zip → archives/archive.zip
[DRY RUN] script.py → code/script.py
[DRY RUN] data.csv → data/data.csv
[DRY RUN] installer.exe → installers/installer.exe
[DRY RUN] font.ttf → fonts/font.ttf
[DRY RUN] unknown.xyz → other/unknown.xyz
[DRY RUN] backup.tar.gz → archives/backup.tar.gz
```
