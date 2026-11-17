# Tool Combination Quick Reference

First use `SKILL.md` to check the input types and requested final artifacts. These combinations cover supported tasks only. There is no PDF file merge or standalone cloud upload command; do not promise PDF merging by rendering and reassembling images.

General processing examples below save both locally and to cloud; adjust for explicit local or cloud preferences using the main guide. Derive `--save-title` from actual context. Keep intermediates local and proceed only after the previous step succeeds with a usable artifact. Cloud folder and document management examples retain their explicit save/management intent.

## Basic Combinations

| User Need | Recommended Command | Notes |
|-----------|---------------------|-------|
| Recognize text in an image | `image ocr photo.jpg` | Prints to terminal |
| Convert one image to a document | `image convert photo.jpg --format word -o "photo_convert.docx" -s` | Saves locally and to cloud |
| Convert multiple images to a document | `image merge-word "page1.jpg" "page2.jpg" "page3.jpg" -o "merged.docx" -s` | Multi-page merge; list files explicitly |
| Convert PDF to editable format | `pdf convert doc.pdf --format word -o "doc_convert.docx" -s` | |
| Improve a photo | `image hd blurry.jpg -o "blurry_hd.jpg" -s` | |
| Protect a document | `pdf watermark file.pdf --text "CONFIDENTIAL" -o "file_watermark.pdf" -s` | |
| Word to PDF | `office convert report.docx -o "report.pdf" -s` | |
| Excel to PDF | `office convert data.xlsx -o "data.pdf" -s` | |
| PPT to PDF | `office convert slides.pptx -o "slides.pdf" -s` | |
| Legacy format upgrade | `office convert old.doc --format docx -o "old_upgraded.docx" -s` | DOC->DOCX, XLS->XLSX, PPT->PPTX |

## Multi-Step Combinations

### Convert Multiple Scan Images into a PDF

```bash
# Step 1: merge scan images into a PDF and save both locally and to cloud.
camscanner-cli image merge-pdf "scan_001.jpg" "scan_002.jpg" "scan_003.jpg" -o "merged.pdf" -s --save-title "Merged scans"
```

### Extract Table Data from Images into Excel

```bash
# Step 1: merge multiple table images into Excel.
camscanner-cli image merge-excel "table_page1.jpg" "table_page2.jpg" -o "merged.xlsx" -s
```

### Add a Watermark and Save the Document

```bash
# Step 1: add a watermark to the PDF.
camscanner-cli pdf watermark contract.pdf --text "INTERNAL USE ONLY" -o "contract_watermark.pdf" -s --save-title "Contract-Watermarked"
```

### Multilingual Document Translation Workflow

```bash
# Step 1: translate text in the image while preserving the original layout.
camscanner-cli image translate document.jpg --lang en -o "document_translate.jpg" -s --save-title "Translation-English"
```

### Convert After OCR Extraction

```bash
# Option 1: convert directly to Markdown. Recommended because it preserves structure.
camscanner-cli image convert document.jpg --format md -o "document_convert.md" -s

# Option 2: extract plain text with OCR, then save as Word.
camscanner-cli image ocr document.jpg > extracted.txt
camscanner-cli txt to-word extracted.txt -o "extracted_to_word.docx" -s --save-title "OCR text"
```

### Split a PDF into Individual Images

```bash
# Render each page and save both locally and to cloud.
camscanner-cli pdf to-images report.pdf -d ./pages -s --save-title "Report pages"

# Or split into a ZIP package.
camscanner-cli pdf to-images-zip report.pdf -o report_pages.zip
```

### Image Authenticity Check

```bash
# Detect Photoshop/tampering.
camscanner-cli image validate suspect.jpg --mode 1

# Detect AI-generated content.
camscanner-cli image validate ai_photo.jpg --mode 2
```

### Image Text Editing: Replace, Delete, or Move

```bash
# Step 1: scan layout structure and character indexes.
camscanner-cli image scan document.jpg

# Step 2: locate start_char_idx and end_char_idx for the target text in the JSON returned by scan.
# Search in result.document_info.sections[].columns[].paragraphs[].lines[].characters.

# Step 3: execute the edit. This example replaces text.
camscanner-cli image edit \
  --input-image "<result.urls.input_image>" \
  --document-info "<result.urls.document_info>" \
  --edit-request '{"edit_type":"update","start_char_idx":39,"end_char_idx":42,"target_text":"West"}' \
  -o edited.jpg -s --save-title "Edited text"
```

### Search and Download Cloud Documents

```bash
# Step 1: search for the target document
camscanner-cli doc search "contract"

# Step 2: Agent presents search results for user confirmation
# Step 3: use the confirmed cs_doc_id to download locally
camscanner-cli doc download <cs_doc_id> -o ~/Downloads/contract.pdf
```

### Process Files and Save to a Specific Folder

```bash
# Convert an image to Word and save directly to a specific folder
camscanner-cli image convert photo.jpg --format word -s --save-dir "Work Documents"
```

### Organize Documents into Folders (requires user confirmation)

```bash
# Step 1: search for documents to organize
camscanner-cli doc search "invoice" -n 20

# Step 2: Agent presents search results; user confirms which document(s) to move
# Step 3: list folders to get dir_id
camscanner-cli doc dirs

# Step 4: match the user's folder name against the folder list
#   - Exact match: use the corresponding dir_id
#   - Similar names exist: present similar folders for user to confirm
#   - No match: inform user the folder doesn't exist (the CLI does not support creating folders), list all available folders

# Step 5: use the confirmed cs_doc_id and matched dir_id to move
camscanner-cli doc move <cs_doc_id> --dir-id <folder_id>
```

## Scenario Mapping

| Scenario | Best Approach |
|----------|---------------|
| Meeting whiteboard photo -> editable document | `image convert whiteboard.jpg --format word -o "whiteboard_convert.docx" -s` |
| Paper scans -> Markdown | `image merge-text "page1.jpg" "page2.jpg" --format md -o paper.md` (multi-image text merge is local only); for one image use `image convert page1.jpg --format md -o page1.md -s` |
| Invoice photo -> structured data extraction | `image receipt invoice.jpg` |
| Invoice photo -> Excel spreadsheet | `image convert invoice.jpg --format excel -o "invoice_convert.xlsx" -s` |
| Contract PDF -> editable Word document | `pdf convert contract.pdf --format word -o "contract_convert.docx" -s` |
| Word report -> PDF | `office convert report.docx -o "report.pdf" -s --save-title "Report PDF"` |
| Legacy DOC -> DOCX upgrade | `office convert old.doc --format docx -o "old_upgraded.docx" -s` |
| Excel data -> PDF | `office convert data.xlsx -o "data.pdf" -s --save-title "Data table PDF"` |
| PPT presentation -> PDF | `office convert slides.pptx -o "slides.pdf" -s --save-title "Presentation PDF"` |
| Business card photo -> text extraction | `image ocr namecard.jpg` |
| Foreign-language menu -> Chinese translation | `image translate menu.jpg --lang zh -o "menu_translate.jpg" -s` |
| Handwritten notes -> electronic document | `image enhance notes.jpg --mode 9 -o clean.jpg`, then `image convert clean.jpg --format word -o "clean_convert.docx" -s` |
| Blurry ID photo -> higher clarity | `image hd id_photo.jpg -o "id_photo_hd.jpg" -s` |
| Old photo restoration | `image restore vintage.jpg -o "vintage_restore.jpg" -s` |
| Multiple exam images -> one PDF | `image merge-pdf "q1.jpg" "q2.jpg" "q3.jpg" -o "merged.pdf" -s` |
| Search cloud documents | `doc search "keyword" -f pdf -n 10` |
| Download cloud documents | `doc download <doc_id> -o ~/Downloads/file.pdf` |
| View cloud folders | `doc dirs` |
| Move documents to a folder | `doc move <doc_id> --dir-id <folder_id>` |
| Save processing results to folder | `image convert photo.jpg --format word -s --save-dir "folder name"` |
