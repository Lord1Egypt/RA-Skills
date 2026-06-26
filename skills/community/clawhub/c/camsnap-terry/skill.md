---
name: camsnap
description: Take camera snapshots and save them to disk. Use when the user asks to take a photo, capture an image from webcam, or take a snapshot.
allowed-tools: Bash
argument-hint: "[output_path] [--preview]"
version: 1.0.0
---

Take a snapshot from the default webcam using the camsnap utility.

## Usage

```bash
python {{SKILL_DIR}}/camsnap.py [output_path] [--preview] [--output-dir DIR]
```

- **output_path** — optional path to save the snapshot (must be within cwd; extensions: .jpg/.jpeg/.png/.bmp/.webp)
- **--preview** — show a preview window (GUI environments only)
- **--output-dir** — directory for auto-generated filenames (default: `snapshots`)

If no output path is provided, the snapshot will be saved to `./snapshots/` with a timestamp filename.

## Steps

1. Run the snapshot script:
```bash
python {{SKILL_DIR}}/camsnap.py {{ $ARGUMENTS }}
```
2. Confirm the snapshot was saved successfully and return the file path.

## Security

- Output paths are validated to stay within the working directory (no path traversal).
- Only safe image extensions are accepted.
