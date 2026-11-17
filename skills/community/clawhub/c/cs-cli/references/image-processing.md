# Image Processing Reference

> **Saving**: These are parameter examples. `-s` alone saves only to the cloud; `-o`/`-d` specify local output. Apply the save policy in `SKILL.md` to the actual task; final artifacts without a save preference require both destinations and a context-based `--save-title`.

## image enhance - Image Enhancement

There are 10 enhancement modes, selected with `--mode`:

| Mode | Description | Best For |
|------|-------------|----------|
| 1 | Brightness enhancement | Dark photos |
| 2 | Sharpening | Blurry scans |
| 3 | Black and white | Black-and-white output |
| 4 | Grayscale | Grayscale output |
| 5 | Shadow removal | Scans with finger or book shadows |
| 6 | Dot pattern removal | Printed documents with halftone patterns |
| 7 | Super filter | General optimization |
| 8 | Moire removal | Photos taken from screens |
| 9 | Handwriting removal | Removing handwritten annotations |
| 10 | Watermark removal | Removing image watermarks |

```bash
camscanner-cli image enhance input.jpg --mode 5 -o enhanced.jpg
camscanner-cli image enhance input.jpg --mode 5 -s
```

## image hd - Image Upscaling

Improve image resolution and clarity. Use this for blurry photos.

```bash
camscanner-cli image hd blurry.jpg -o hd.jpg
camscanner-cli image hd blurry.jpg -s
```

## image restore - Photo Restoration

Restore scratches, fading, and damage in old photos.

```bash
camscanner-cli image restore old.jpg -o restored.jpg
camscanner-cli image restore old.jpg -s
```

## image convert - Image Format Conversion

Recognize content in an image and convert it to a document format.

| Target Format | `--format` Value | Output Extension | Description |
|---------------|------------------|------------------|-------------|
| Word | `word` | .docx | Preserves layout |
| Excel | `excel` | .xlsx | Good for table images |
| Markdown | `md` | .md | Plain text with structure |
| TXT | `txt` | .txt | Plain text, does not support `-s` |

> Warning: `--format pdf` is **not supported**. To convert images to PDF, use `image to-pdf` for one image or `image merge-pdf` for multiple images.

```bash
camscanner-cli image convert table.png --format excel -s
camscanner-cli image convert doc.jpg --format md -o result.md
```

## image to-pdf - Image to PDF

Convert a single image directly to a PDF file.

```bash
camscanner-cli image to-pdf scan.jpg -s
```

## image watermark - Image Watermark

| Parameter | Description |
|-----------|-------------|
| `--text` | Watermark text. **Required**. |
| `--color` | Color, such as `#FF0000`. |
| `--opacity` | Opacity from 0 to 1. |
| `--size` | Font size. |

```bash
camscanner-cli image watermark photo.jpg --text "CONFIDENTIAL" --opacity 0.3 -s
```

## image translate - Image Translation

Translate text in an image while preserving the original layout.

| Parameter | Description |
|-----------|-------------|
| `--lang` | Target language code. Default: `en`. |

Supported languages: `en` (English), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), `fr` (French), `de` (German), `es` (Spanish), `pt` (Portuguese), `ru` (Russian), `ar` (Arabic).

```bash
camscanner-cli image translate menu.jpg --lang zh -s
```

## image extract-formula - Formula Extraction

Detect and extract mathematical formula regions from an image.

```bash
camscanner-cli image extract-formula equation.png -s
```

## image ocr - OCR Text Recognition

Extract plain text from an image and print it to stdout.

```bash
camscanner-cli image ocr document.jpg
camscanner-cli image ocr document.jpg > result.txt
```

## image validate - Image Authenticity Detection

| Mode | Description |
|------|-------------|
| 1 | Photoshop/tampering detection |
| 2 | AI-generated image detection |

```bash
camscanner-cli image validate photo.jpg --mode 1
camscanner-cli image validate ai_art.jpg --mode 2
```

The output is JSON and includes the `is_tampered` field.

## image merge-pdf / merge-excel / merge-word - Multi-Image Merge

Merge images only into one document; PDF/Word/Excel inputs are not accepted. **Hard limit: one command accepts at most 100 input images. More than 100 images cannot be merged into a single file** because the CLI does not provide document merge commands.

```bash
camscanner-cli image merge-pdf "page1.jpg" "page2.jpg" "page3.jpg" -s
camscanner-cli image merge-excel "table1.jpg" "table2.jpg" -s
camscanner-cli image merge-word "doc1.jpg" "doc2.jpg" -s
```

## image merge-text - Multi-Image OCR Merge

Run OCR on multiple images and merge the result as text. **One command accepts at most 100 input images.**

```bash
# Print to terminal.
camscanner-cli image merge-text page1.jpg page2.jpg

# Write to a file.
camscanner-cli image merge-text page1.jpg page2.jpg -o result.md --format md
```

## image scan + image edit - Image Text Editing

Use a three-step flow, scan -> locate -> edit, to accurately replace, delete, or move text in an image while preserving the original layout and visual style.

### How It Works

The edit engine is based on **character-level OCR indexes**. Always run `scan` first to obtain each character's `index`, then build the edit request with exact `start_char_idx` and `end_char_idx` values. **Do not guess index values.**

### Step 1: Scan Layout and Character Indexes

```bash
camscanner-cli image scan photo.jpg
```

`scan` returns a JSON structure:

```json
{
  "code": 200,
  "result": {
    "document_info": {
      "sections": [{
        "columns": [{
          "paragraphs": [{
            "lines": [{
              "text": "East University",
              "characters": [
                {"char": "E", "index": 39, "position": []},
                {"char": "a", "index": 40, "position": []},
                {"char": "s", "index": 41, "position": []},
                {"char": "t", "index": 42, "position": []}
              ]
            }]
          }]
        }]
      }]
    },
    "urls": {
      "input_image": "t_ie_X_..._1",
      "document_info": "t_ie_X_..._1",
      "background_info": ""
    }
  }
}
```

Key fields:

- `result.urls.input_image`: pass this to `image edit` as `--input-image`.
- `result.urls.document_info`: pass this to `image edit` as `--document-info`.
- `result.document_info.sections[].columns[].paragraphs[].lines[].characters`: each character's `char`, `index`, and `position`.

### Step 2: Locate Target Text in the Scan Result

Iterate through all `lines`, find the line containing the target text, and extract the first and last character `index` values for that target.

**Example**: the user wants to replace "East University" with "West University".

In the scan result, locate:

- "E" -> index: 39
- "t" -> index: 42

Therefore, `start_char_idx = 39` and `end_char_idx = 42`, replacing only "East" with "West".

### Step 3: Execute the Edit

```bash
camscanner-cli image edit \
  --input-image "t_ie_X_..._1" \
  --document-info "t_ie_X_..._1" \
  --edit-request '{"edit_type":"update","start_char_idx":39,"end_char_idx":42,"target_text":"West"}' \
  -o edited.jpg
```

All parameters are required:

- `--input-image`: `result.urls.input_image` returned by `scan`.
- `--document-info`: `result.urls.document_info` returned by `scan`.
- `--edit-request`: JSON edit operation.

### edit-request Format

#### Text Replacement (`update`)

```json
{
  "edit_type": "update",
  "start_char_idx": 39,
  "end_char_idx": 42,
  "target_text": "West"
}
```

#### Area Deletion (`delete`)

```json
{
  "edit_type": "delete",
  "area_type": "text",
  "area_idx": 0
}
```

Allowed `area_type` values: `text`, `table`, `image`, `stamp`.
`area_idx` corresponds to the `area_idx` field of a paragraph in the scan result.

#### Area Move (`move`)

```json
{
  "edit_type": "move",
  "area_type": "text",
  "area_idx": 0,
  "target_position": [100, 100, 300, 100, 300, 160, 100, 160]
}
```

### Multiple Replacements

Multiple replacements must be executed **as a chain**, using the latest `urls` returned by the previous `edit` each time:

1. Changes in replacement text length can shift later character indexes.
2. Strategy: replace from back to front, starting with larger indexes, or run `scan` again after each replacement.
3. Each `edit` output returns new `urls`; the next edit must use the new keys.

### Agent Behavior Requirements

1. Run `image scan` to obtain the complete result.
2. **Automatic location**: search the `characters` arrays in the scan result for the target text provided by the user, and precisely extract `start_char_idx` and `end_char_idx`.
3. **Ambiguity confirmation**: if the target text appears multiple times in the image, show all matches with context/location and ask the user which one to edit.
4. Build the `edit-request` JSON and run `image edit`.
5. **Do not guess indexes**: all `char_idx` values must come from the scan result and must not be manually inferred.

### Common Mistakes

| Mistake | Correct Practice |
|---------|------------------|
| Calling `edit` without running `scan` | Always run `scan` first to obtain OSS keys and character indexes |
| Using a file path as `--input-image` | Use `result.urls.input_image` returned by `scan` |
| Guessing `start_char_idx` | Locate it exactly from `characters[].index` |
| Reusing the same `document_info` for multiple replacements | Use the latest key returned by the previous `edit` each time |
| Choosing arbitrarily when target text has multiple matches | Show all matches and ask the user to confirm |
