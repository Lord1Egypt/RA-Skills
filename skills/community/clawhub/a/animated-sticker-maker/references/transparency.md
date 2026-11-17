# Transparency branch

Use existing alpha when it is clean. Otherwise generate or place the isolated subject on a flat work color that is far from the subject's dominant palette.

Prefer a saturated candidate from magenta, green, blue, cyan, yellow, or red. Reject a candidate when it appears in the subject, highlights, effects, exact text, or semi-transparent material. Keep the work background flat, without texture, lighting, horizon, or cast shadow.

Remove the work color with:

```bash
python <skill-dir>/scripts/chroma_key.py input.png output.png --key auto --despill
```

Use an explicit key when the border does not represent the intended work color:

```bash
python <skill-dir>/scripts/chroma_key.py input.png output.png \
  --key '#FF00FF' \
  --transparent-threshold 12 \
  --opaque-threshold 180 \
  --despill
```

`--key auto` estimates the key from border pixels and automatically raises the transparent threshold enough to clear the observed border variation. With an explicit key, raise `transparent-threshold` when background remnants remain; lower it when valid subject-edge pixels are being removed. Raise `opaque-threshold` when fine translucent edges are being removed. Inspect the result on light and dark backgrounds after every threshold change.
