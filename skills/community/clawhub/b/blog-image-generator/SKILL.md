---
name: Blog Image Generator
description: "DEPRECATED — superseded by memorable-image-gen. This skill has been replaced by the Memorable Image Generator, which uses science-backed memorability scoring (ResMem, Brain Bridge Lab, University of Chicago) to ensure generated images are actually remembered. Install the new skill instead: clawhub install memorable-image-gen"
metadata:
  openclaw:
    homepage: https://github.com/PhantomWorksIO/clawhub-skills
    emoji: "🔄"
    deprecated: true
    superseded_by: "memorable-image-gen"
---

# Blog Image Generator — DEPRECATED

> ⚠️ **This skill has been superseded.** Please install the new version instead.

## Upgrade to Memorable Image Generator

This skill has been replaced by **[memorable-image-gen](https://clawhub.com/skills/memorable-image-gen)** — a science-backed image generation agent that scores images for memorability before returning them.

```bash
clawhub install memorable-image-gen
```

### Why the upgrade?

The old skill generated images and stopped. The new one:

1. **Generates** via Google Gemini
2. **Scores** memorability using ResMem (Brain Bridge Lab, University of Chicago) — a deep learning model trained to predict whether a human will remember the image
3. **Iterates** until the image clears a memorability threshold (default 0.7/1.0)
4. **Returns** the best result, not just the first

Every other image generator stops at "looks good." This one keeps going until the image will actually be remembered.

## Migration

Same interface — just install the new skill and update your command:

```bash
# Old
python scripts/generate_blog_image.py --prompt "..." --output hero.png

# New
python scripts/generate_memorable_image.py --prompt "..." --output hero.png --threshold 0.7 --verbose
```

The `--threshold` and `--verbose` flags are new. Everything else carries over.

## Install

```bash
clawhub install memorable-image-gen
```
