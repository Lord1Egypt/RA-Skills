---
name: general-ocr-struct
description: General-purpose offline OCR and post-processing for Chinese/English screenshots, scanned images, receipts, tables, chat screenshots, statement screenshots, and other text-heavy images. Use when you need to: (1) extract text from an image locally, (2) return raw OCR text before interpretation, (3) clean broken OCR lines into structured content, (4) reorganize recognized text into rows/fields for downstream use, or (5) separate recognition from later table entry, summarization, or document drafting.
---

# General OCR Struct

Use this skill to separate OCR recognition from downstream content整理.

## Workflow

1. Run the local OCR script on the image first.
2. Return the raw OCR text before making business interpretations when accuracy matters.
3. If the image is a transaction-detail screenshot, run structuring mode to group rows into fields.
4. Mark uncertain fields explicitly as `待确认`; do not guess missing content.
5. Only after the user confirms recognition quality, use the result for tables, summaries, or documents.

## Commands

### Raw OCR

```bash
python3 scripts/general_ocr.py raw /path/to/image.jpg
```

### Structured transaction extraction

```bash
python3 scripts/general_ocr.py transactions /path/to/image.jpg
```

### JSON output

```bash
python3 scripts/general_ocr.py transactions /path/to/image.jpg --json
```

## Output rules

- Prefer showing the recognition result first, then the cleaned structure.
- Preserve source wording where possible.
- For uncertain content, use `待确认` instead of inferring.
- Adapt the structure to the source image type. For statement-like screenshots, common fields are: `card_last4`, `date`, `time`, `currency`, `merchant`, `amount`.

## Notes

- This skill uses RapidOCR locally.
- First install may need Python packages; after setup it runs offline.
- If OCR quality is weak, request a higher-resolution original screenshot before doing deeper整理.
