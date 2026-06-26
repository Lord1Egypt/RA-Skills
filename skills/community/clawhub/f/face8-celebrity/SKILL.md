---
name: face8-celebrity
description: "Upload a photo to identify celebrities using Face8 Taiwan face recognition engine"
allowed-tools:
  - exec
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Face8 Celebrity Recognition

Use the [Face8 台灣臉霸](https://face8.ai/faceMaster/) face recognition engine to identify celebrities and public figures from photos.

## Usage

```bash
python3 scripts/recognize.py <image_path>
```

Output example:
```
#1 ✅ 簡良益　相似度 97%

🏆 最佳匹配: 簡良益 (97%)
```

Use `--json` for raw API response.

## Register unknown faces

If Face8 doesn't recognize someone, you can register them:

```bash
# Register an unknown face
python3 scripts/recognize.py photo.jpg --register "王小明"

# Confirm a suggested match
python3 scripts/recognize.py photo.jpg --confirm 57298
```

## Notes

- Only works for **celebrities and public figures**, not general face search
- Works best with clear, front-facing photos
- Registering a face adds it to the Face8名人堂 database
- API provided by face8.ai, accuracy not guaranteed
- Requires internet access to reach the face8.ai API
