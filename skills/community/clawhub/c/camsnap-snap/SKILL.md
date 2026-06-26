---
name: camsnap
description: Take webcam snapshots with path validation, safe resource handling, and flexible output options.
metadata:
  openclaw:
    requires:
      commands: [python3]
      pypi: [opencv-python]
---

# Camsnap

Camera snapshot utility for AI agents.

## Features

- Safe webcam capture with guaranteed resource release
- Path traversal protection and extension validation
- Configurable camera index and output directory
- Structured logging (no print statements)
- Type-annotated API

## Usage

```bash
python3 camsnap.py
python3 camsnap.py --output-dir ./photos
python3 camsnap.py snapshot.png --camera 1
```

### As a module

```python
from camsnap import take_snapshot

path = take_snapshot(output_dir="snapshots", camera_index=0)
```
