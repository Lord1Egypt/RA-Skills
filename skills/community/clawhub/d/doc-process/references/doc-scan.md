# Doc Scan — Reference Guide

## Purpose
Convert a photo of a document (printed page, form, receipt, whiteboard, handwritten note, book page, ID card, etc.) into a clean, flat, professional-looking scanned image — as if produced by a real flatbed scanner. Works by detecting the document's edges, applying a perspective warp to flatten it, removing shadows, and applying scan-quality enhancement.

---

## Step 1 — Read and Assess the Input Image

Visually examine the uploaded photo and report a pre-scan assessment:

```
## Document Photo Assessment

| Property            | Detected Value |
|---|---|
| Document type       | [Printed letter / handwritten note / receipt / form / ID / whiteboard / book page] |
| Orientation         | Portrait / Landscape / Tilted (~N°) |
| Perspective distortion | None / Mild / Moderate / Severe |
| Lighting            | Even / Uneven (shadow on [region]) / Too dark / Too bright / Flash glare |
| Background          | Plain white / Dark table / Carpet / Complex / Patterned |
| Image quality       | Sharp / Slightly blurred / Blurred |
| Estimated document area | ~N% of frame |
| Multi-page?         | Single page / N pages visible |
| Content description | [e.g., "text-only letter, 2 columns" / "colour form with logos and tables"] |

Recommended settings:
- Mode: bw       ← best for text-only documents
- Mode: color    ← best for forms, diagrams, logos, colour content
- Mode: gray     ← middle ground
- DPI: 300       ← print quality (default)
- DPI: 150       ← screen / preview use only
```

### Non-Document Detection

If the image does **not** contain a document as its primary subject, do not proceed. Respond:

```
⚠ This doesn't appear to be a document photo.
I see: [brief description — "a landscape", "a person's portrait", "a blank wall"]

Doc Scan works with:
- Printed pages, forms, letters, reports
- Handwritten notes and whiteboards
- Receipts, invoices, business cards
- Book and magazine pages
- Any flat document photographed on a surface

Please re-upload with the document clearly visible on a contrasting background.
```

---

## Step 2 — Run the Scanner Script

**Dependencies required:** `pip install opencv-python-headless>=4.9 numpy>=1.24 Pillow>=10.0`
Optional for PDF output: `pip install img2pdf>=0.5`

**Before running**, confirm the user has dependencies installed, or ask if they want to install them.

### Standard commands:

```bash
# Black & white — best for text documents (default)
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png --mode bw

# Colour — best for forms, diagrams, coloured content
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png --mode color

# Grayscale — intermediate option
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png --mode gray

# PDF output (single page)
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.pdf --format pdf

# Multi-page PDF (all pages in one command)
python skills/doc-process/scripts/doc_scanner.py \
  --input page1.jpg page2.jpg page3.jpg \
  --output document.pdf --format pdf

# High-resolution (print quality)
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png --dpi 300

# Skip perspective correction (photo already taken flat overhead)
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png --no-warp

# Manual corner hints (when auto-detection fails)
# Corners: top-left, top-right, bottom-right, bottom-left (pixels or %)
python skills/doc-process/scripts/doc_scanner.py \
  --input photo.jpg --output scanned.png \
  --corners "50,30 800,20 820,1100 40,1120"
```

---

## Step 3 — Understand the Scan Pipeline

The script performs these steps in order:

| Step | What it does |
|---|---|
| **1. Edge detection** | Three strategies tried in order: (A) Canny edge detection on greyscale — best for high-contrast docs; (B) Morphological gradient — handles low contrast and faint edges; (C) Colour/brightness threshold — used when the document is white on a dark background |
| **2. Corner refinement** | Sub-pixel corner accuracy using `cv2.cornerSubPix` for the most precise warp |
| **3. Perspective warp** | Four-point transform to flatten the document to a perfect rectangle using Lanczos interpolation |
| **4. Shadow removal** | Per-channel background estimation + normalisation removes cast shadows and uneven lighting |
| **5. Enhancement** | Mode-specific: BW = adaptive threshold + morphological close + denoise; Gray = auto-levels + CLAHE + unsharp mask; Color = white-balance + CLAHE + sharpening |
| **6. Scanner border** | 8 px clean white border added to simulate scanner bed edges |
| **7. Save with DPI** | Output saved with embedded DPI metadata |

---

## Step 4 — Interpret Script Output

Script outputs a JSON block to stderr:

```json
{
  "status": "success",
  "corners_detected": true,
  "corners": [[50,30],[800,20],[820,1100],[40,1120]],
  "warp_applied": true,
  "enhancement_mode": "bw",
  "input_size": [3024, 4032],
  "output_size": [2480, 3516],
  "output_dpi": 300,
  "pages": 1,
  "output_file": "scanned.png",
  "processing_time_s": 1.4,
  "warnings": []
}
```

### Handling outcomes:

| Field | Value | Action |
|---|---|---|
| `status` | `"success"` | Report completion summary |
| `status` | `"error"` | Report the `error` message to user |
| `corners_detected` | `false` | Warn user, offer manual corners or `--no-warp` |
| `warp_applied` | `false` | Note that perspective correction was skipped |
| `warnings` | non-empty | Report each warning to user |

**When `corners_detected: false`:** offer:
1. Manual corner specification — ask "Please describe roughly where the four corners of the document appear (e.g., top-left at 10% from left and 5% from top)"
2. `--no-warp` fallback — enhancement without perspective correction
3. Photography tips (see Step 6)

---

## Step 5 — Post-Scan Quality Check

After the script finishes, read the output image visually and verify:

| Check | Criteria |
|---|---|
| **Edges are straight** | No barrel distortion, no curved lines |
| **Background is white/clean** | No table surface, carpet, or shadow visible |
| **Text is legible** | Not blurred, not over-thresholded (losing strokes) |
| **Correct aspect ratio** | Not stretched or squished |
| **Lighting is even** | No dark gradient from one side |
| **Colour correct** | B&W for text docs; colour preserved for colour docs |
| **No artefacts** | No severe noise, moire patterns, or streaks |

**If a check fails**, offer:
- Different mode (`bw` ↔ `color` ↔ `gray`)
- Different `--dpi`
- Manual corners if edges were wrong
- Re-photograph tips

---

## Step 6 — Output Report

Present to the user:

```
## Scan Complete

| Property              | Value |
|---|---|
| Output file           | scanned.png |
| Output size           | 2480 × 3516 px |
| Mode                  | Black & White |
| Perspective corrected | Yes — 4 corners detected automatically |
| Shadow removal        | Applied |
| DPI                   | 300 |
| Processing time       | 1.4 s |

Enhancements applied:
- Three-strategy edge detection → four corners found
- Sub-pixel corner refinement
- Four-point perspective warp (Lanczos)
- Shadow and uneven-lighting removal
- Adaptive threshold (block size auto-scaled to resolution)
- Morphological stroke repair + denoising
- Scanner border added
```

---

## Step 7 — Multi-Page Documents

1. Process each page image individually in one command:
```bash
python skills/doc-process/scripts/doc_scanner.py \
  --input page1.jpg page2.jpg page3.jpg \
  --output document.pdf --format pdf --mode bw
```
2. Report: "N pages scanned and saved to document.pdf"
3. For very large batches (20+ pages), process in groups of 10 and combine PDFs.

---

## Step 8 — Photography Tips (poor quality input)

Provide when auto-detection fails or quality is poor:

**Lighting:**
- Use bright, even indoor lighting — avoid direct sunlight creating glare
- Avoid shadows from your hand or body
- Turn on all available lights in the room

**Camera position:**
- Hold camera directly above the document (parallel to the surface)
- The full document should be visible with a small margin around it
- Do not crop the document edges out of frame

**Background:**
- Place the document on a **contrasting background** — dark table for white paper, white surface for dark paper
- Avoid patterned, textured, or busy backgrounds

**Sharpness:**
- Tap to focus on the document before shooting
- Hold steady — wait for autofocus to lock
- Use highest resolution available

---

## Step 9 — After Scanning: Continue Processing

After a successful scan, offer to continue with doc-process modes:

```
Scan complete. Would you also like me to:
- Redact PII / sensitive data from this scanned document?
- Extract text and fill a form?
- Analyze this as a contract, receipt, or medical document?
- Translate this document?
- Extract tables to CSV?

Just let me know which mode to run on the scanned output.
```

Pass the scanned output file path to the appropriate mode if the user confirms.

---

## General Rules

- Never process the image if it does not contain a document — describe what was detected and ask the user to re-upload
- Always report the detected document type in the assessment before running the script
- Default mode: `bw` for text-only; `color` for anything with colour content
- Default DPI: 300 (print quality); use 150 for screen-preview only
- Default format: PNG (lossless); PDF only when explicitly requested or for multi-page
- If `corners_detected: false`, offer manual corners before giving up
- Always confirm dependencies are installed before running the script
