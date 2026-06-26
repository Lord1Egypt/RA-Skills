---
name: doc-scan
description: >
  DEPRECATED — this skill has been merged into doc-process (v4.0.0+).
  Use doc-process instead for document scanning, perspective correction, and dewarping.
  doc-process includes an improved scanner with multi-strategy edge detection,
  sub-pixel corner refinement, and scan-quality enhancement.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Doc-Scan — DEPRECATED

> **This skill is deprecated.** All functionality has been merged into **doc-process v4.0.0** with a significantly improved scanner engine. Please use `doc-process` instead.
>
> To scan a document photo: install `doc-process` and say "scan this photo", "correct perspective", "dewarp this document", or any equivalent phrase.

---

# Doc-Scan — Document Scanner Skill (archived)

Converts a photo of a document (whiteboard, printed page, handwritten note, form, receipt, book page, etc.) into a clean scanned-looking image with perspective correction and enhancement.

## Step 1 — Validate the Input

Read the provided image visually. Assess:

| Check | Yes/No | Notes |
|---|---|---|
| Is this an image file? | | .jpg, .jpeg, .png, .heic, .webp, .bmp, .tiff |
| Does the image contain a document? | | Printed page, form, note, receipt, whiteboard, book |
| Is the document the primary subject? | | Centered or dominant in frame |
| Is there a perspective distortion? | | Taken from an angle — not flat/overhead |
| Is the image quality sufficient? | | Not severely blurred or too dark |

### Non-Document Detection
If the image does not appear to contain a document, respond:
```
⚠ This image doesn't appear to contain a document.

I detected: [brief description of what the image contains — e.g., "a landscape photo", "a person's portrait", "a blank wall"]

Doc-Scan works best with:
- Printed documents (forms, letters, reports)
- Handwritten notes or whiteboards
- Receipts, invoices, or business cards
- Book or magazine pages
- Any flat document photographed from above or at an angle

If you intended to upload a document photo, please try again with better lighting and the document clearly visible. If you want to process this image for a different purpose, I can help with that instead.
```

Do not proceed with scanning if this check fails.

---

## Step 2 — Pre-Scan Assessment

Report what you see before scanning:

```
## Document Photo Assessment

| Property | Detected Value |
|---|---|
| Document type | [e.g., Printed letter, handwritten note, receipt, form] |
| Orientation | Portrait / Landscape / Tilted (~N degrees) |
| Perspective distortion | None / Mild / Moderate / Severe |
| Lighting | Even / Uneven (shadow on [region]) / Too dark / Too bright |
| Background | White desk / Dark table / Complex background |
| Image quality | Sharp / Slightly blurred / Blurred |
| Estimated document area | ~N% of total image |
| Multi-page? | Single page / [N] pages detected |
| Content visible | [brief description — e.g., "text document, 3 columns, appears to be a form"] |

Recommended enhancements:
- [x] Perspective correction
- [x] Background removal / edge crop
- [ ] Binarization (black & white) — suitable if text-only
- [x] Contrast enhancement
- [x] Shadow removal
- [ ] Color preservation — suitable for documents with color content
```

---

## Step 3 — Run the Scanner Script

```bash
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png
```

### Common Options
```bash
# Black and white output (best for text documents)
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --mode bw

# Color-preserved output (best for forms, diagrams, colored content)
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --mode color

# Grayscale output (middle ground)
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --mode gray

# Output as PDF
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.pdf --format pdf

# Multiple images into one PDF (multi-page scan)
python skills/doc-scan/scripts/doc_scanner.py --input page1.jpg page2.jpg page3.jpg --output document.pdf --format pdf

# Manual corner specification (if auto-detection fails)
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --corners "50,30 800,20 820,1100 40,1120"

# High-resolution output
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --dpi 300

# Skip perspective correction (if photo is already flat)
python skills/doc-scan/scripts/doc_scanner.py --input photo.jpg --output scanned.png --no-warp
```

---

## Step 4 — Interpret Script Output

The script outputs a JSON status block to stderr. Parse and report to user:

```json
{
  "status": "success",
  "corners_detected": true,
  "corners": [[50,30],[800,20],[820,1100],[40,1120]],
  "warp_applied": true,
  "enhancement_mode": "bw",
  "input_size": [3024, 4032],
  "output_size": [2480, 3508],
  "output_dpi": 300,
  "pages": 1,
  "output_file": "scanned.png",
  "warnings": []
}
```

### Status Handling

**`"status": "success"`**: Report completion with key stats.

**`"corners_detected": false`**: Auto-detection failed. Offer:
- "Auto edge-detection could not find the document corners. I can try with manual corner hints — please describe approximately where the four corners of the document appear in the photo (e.g., top-left at about 10% from left and 5% from top)."
- Or: offer `--no-warp` mode to at least apply enhancement without perspective correction

**`warnings` array**: Report any warnings to user — e.g., "Low contrast image", "Detected significant blur", "Partial document visible"

---

## Step 5 — Post-Scan Quality Check

After the script completes, read the output image visually and assess:

| Quality Check | Pass / Fail | Notes |
|---|---|---|
| Document edges are straight | | No barrel distortion remaining |
| Text is legible | | Not blurred or over-enhanced |
| Shadows removed or reduced | | Even lighting across page |
| Background removed (white/clean) | | No table/desk visible |
| Correct aspect ratio (A4/Letter) | | Not stretched or squished |
| Color / binarization correct | | B&W if text-only, Color if content requires it |

If any check fails, report the issue and offer:
- Re-run with different settings (different mode, manual corners, contrast level)
- Re-photograph tips (see Step 7)

---

## Step 6 — Output Report

```
## Scan Complete ✓

| Property | Value |
|---|---|
| Output file | scanned.png |
| Output size | 2480 × 3508 px (A4 at 300 DPI) |
| Mode | Black & White |
| Perspective correction | Applied |
| Shadow removal | Applied |
| Processing time | ~2.3s |

### Enhancements Applied
- Edge detection and four-corner extraction
- Perspective warp to standard A4 dimensions
- Adaptive thresholding (Sauvola method) for clean B&W text
- Shadow compensation via background normalization
- Border cropped to document edges

### Before → After
[Original photo] → [Scanned output]
(Both are available at their file paths)
```

---

## Step 7 — Multi-Page Documents

If the user provides multiple photos (or a folder of images):

1. Process each image individually
2. Sort by filename or user-specified order
3. Combine into a single PDF:
```bash
python skills/doc-scan/scripts/doc_scanner.py \
  --input page1.jpg page2.jpg page3.jpg \
  --output document.pdf --format pdf
```
4. Report: "3-page document scanned and saved to document.pdf"

For very large batches (10+ pages), process in batches of 10 and combine.

---

## Step 8 — Photography Tips (on poor quality input)

If the input image quality is poor or auto-detection fails, provide tips:

```
### Tips for Better Scans

**Lighting:**
- Scan in bright, even lighting (avoid direct sunlight creating glare)
- Avoid shadows from your hand or body
- A well-lit indoor environment works well

**Camera position:**
- Hold the camera directly above the document when possible
- Keep the camera parallel to the document surface
- The full document should be visible with a small border around it

**Background:**
- Place the document on a contrasting background (dark table for white paper, white surface for dark paper)
- Avoid patterned or busy backgrounds

**Focus & stability:**
- Tap to focus on the document before taking the photo
- Hold steady or use a tripod for sharper results
- Use the highest resolution available on your camera

**Document preparation:**
- Flatten any folds or curves
- If the document is creased, press it flat before photographing
```

---

## Step 9 — Integration with Doc-Process

After a successful scan, offer to process the scanned document with doc-process:

```
Scan complete! Would you also like me to:
- Extract text and fill a form from this scanned document?
- Analyze this as a contract/receipt/medical document?
- Translate this document to another language?
- Extract tables from this document?

Just say what you'd like to do and I'll process the scanned version.
```

If the user confirms, pass the scanned output file to the appropriate doc-process mode.

---

## Step 10 — Timeline Logging

After a successful scan, silently log to the timeline:
```bash
python skills/doc-process/scripts/timeline_manager.py add \
  --type "Doc Scan" \
  --source "<input filename>" \
  --summary "<N> page(s) scanned, perspective corrected, saved as <output filename>"
```

---

## General Rules
- Never process the photo if it does not contain a document — explain what was detected instead
- Always report the detected document type so the user can confirm before scanning
- Auto-detect corners when possible; fall back gracefully to manual or no-warp mode
- Default output mode: `bw` for text documents, `color` for anything with color content
- Default output format: PNG (lossless); PDF only if explicitly requested or for multi-page
- Default DPI: 300 (print quality); 150 for screen-only use
