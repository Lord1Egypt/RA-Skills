---
name: ai-watermark-margin
description: "Drop the in-image watermark/signature that an AI image editor stamps on YOUR OWN ai-generated or ai-edited pictures, deterministically — by adding a blank margin before the edit and cropping it off after. No inpainting, no ML model, no third-party copyright watermark removal. Use when: 'AI edit leaves a watermark', 'remove AI signature', 'AI 修图水印', '去AI生成签名', '图片下方有水印', 'generator watermark'. Two tiny Pillow scripts: add_margin.py pads the canvas with whitespace (or black) so the generator's mark lands outside the content; crop_margin.py detects that uniform border and crops it away. Includes an ethics/compliance note: this only removes the generator's own visual stamp; you still disclose AI use per platform rules."
metadata:
  displayName: "AI Watermark Margin Drop (AI水印留白裁剪)"
  slug: "ai-watermark-margin"
  category: "image-processing"
  agent_created: "true"
  description_zh: "确定性去掉 AI 修图/生成器在你【自己】的 AI 图片上盖的那行水印/签名——做法是修图前先加留白边，修完再把边裁掉。不靠 inpainting、不调模型、不去别人的版权水印。触发：AI 修图带水印、去AI生成签名、图片下方有水印、generator watermark。两个极简 Pillow 脚本：add_margin.py 给画布加留白（或黑边）让生成器把水印盖在边外；crop_margin.py 检测那圈纯色边并裁掉。含合规说明：本技法只去生成器自带的视觉签名，AI 使用声明你照常单独标。"
---

# AI Watermark Margin Drop

## What this solves
AI image editors (image-to-image / inpainting tools, online generators) often stamp a small watermark, signature, or "made with X" text on the output — usually along an edge (most commonly the **bottom**). It looks cheap and you'd rather not have it baked into the file, even though you still disclose AI use separately.

This is a **self-developed, deterministic** technique (no model, no inpainting, no copyright-watermark removal):

> **Pad the canvas with a blank margin before sending the image to the AI; the generator drops its watermark into that margin; crop the margin off after the edit → the watermark is gone with zero reconstruction artifacts.**

## Workflow (3 steps)
1. **Pad.** Run `add_margin.py` on your source image to add a ~10% blank (white) margin, typically at the bottom (where watermarks land). This is the image you hand to the AI.
2. **Edit.** Send the padded image to the AI editor / generator. Its watermark/signature lands in the blank margin instead of on your content.
3. **Crop.** Run `crop_margin.py` on the AI output. It auto-detects the uniform blank border and crops it away, taking the watermark with it.

## Scripts
### add_margin.py  (the "pad" step)
```bash
python scripts/add_margin.py input.png output.png --percent 10 --side bottom --color white
```
- `--percent N` : margin thickness as % of the relevant dimension (default 10).
- `--side`      : `bottom` (default), `top`, `uniform`, `left`, `right`.
- `--color`     : `white` (留白, default) or `black` (黑边). Hex like `#000000` also accepted.

### crop_margin.py  (the "drop" step)
```bash
python scripts/crop_margin.py ai_output.png cleaned.png
# dry-run to see detected margins without writing:
python scripts/crop_margin.py ai_output.png --report
```
- Auto-detects the uniform-color border (the margin you added) and crops all four sides.
- `--tol N`        : color tolerance for "is this border?" (default 12).
- `--min-frac F`   : fraction of a row/column that must be border color (default 0.90).
- `--max-percent P`: safety cap — never crop more than P% per side (default 30).
- `--fallback N`   : if detected border < N% per side, crop a fixed N% bottom margin instead.
- `--report`       : print detected left/top/right/bottom crops, write nothing.

## Ethics & compliance
- ✅ This removes **only the generator's own visual watermark/signature** from images **you** generated or edited with AI.
- ✅ It is **not** a tool for removing third-party **copyright** watermarks from stock/licensed media — don't do that.
- ⚠️ You remain responsible for **disclosing AI use** per each platform's rules. This technique only cleans the in-file stamp for aesthetics; keep your "AI-generated" labeling separate and compliant.

## When NOT to use
- The watermark is baked into the **content** (not in a blank margin) → padding won't help; use a different method.
- You need to keep the margin for composition → don't crop.
- The image is someone else's copyrighted work with a rights watermark → do not use.

## Tested backfires (don't retry)
- Adding too little margin (<5%) lets the watermark overlap content → crop can't remove it cleanly. Use ≥8–10%.
- Some generators recolor or fill the margin with content; if `crop_margin.py` reports ~0 border, bump `--fallback` or re-pad with a larger percent.
