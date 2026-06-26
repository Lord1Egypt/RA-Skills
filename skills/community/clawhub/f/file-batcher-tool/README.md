# File Batcher Skill

Batch file operations for efficient file management.

## Features

- ✅ Batch rename with patterns
- ✅ Image format conversion
- ✅ Auto-organize by file type
- ✅ Duplicate detection
- ✅ Large file finder

## Usage

### Rename
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh rename "./photos" "2026-03-10_###"
bash skills/file-batcher-1.0.0/scripts/batcher.sh rename "./docs" "prefix_*"
```

### Convert Images
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh convert "./images" "png"
bash skills/file-batcher-1.0.0/scripts/batcher.sh convert "./photos" "jpg"
```

### Organize
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh organize "~/Downloads"
```

### Find Duplicates
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh duplicates "~/Documents"
```

### Count Files
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh count "./project"
```

### Find Large Files
```bash
bash skills/file-batcher-1.0.0/scripts/batcher.sh large "~" --size 500M
```

## License

MIT
