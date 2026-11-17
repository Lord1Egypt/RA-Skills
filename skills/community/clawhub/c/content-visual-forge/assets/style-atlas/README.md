# Style Atlas Assets

This directory stores local style-atlas metadata snapshots used by `content-visual-forge`.

## Runtime Rule

Runtime should read the local snapshot first and should not query the external atlas site for every generation.

## Current Snapshot

- `qiaomu-style-atlas.snapshot.json`
- Source: `https://style.qiaomu.ai/`
- Contents: metadata only, including artist / style entry names, broad movement labels, cues, and source image paths.
- Excluded: generated image files and external page assets.

## Refresh

Refresh only as a maintenance action:

```bash
python content-visual-forge/scripts/style-atlas/fetch_qiaomu_style_atlas.py \
  --snapshot-date 2026-05-20
```
