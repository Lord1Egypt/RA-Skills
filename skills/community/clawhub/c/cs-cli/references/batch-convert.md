# Batch Document Conversion Workflow

> **Preread**: `references/image-processing.md` for image command parameters, and `references/pdf-processing.md` for PDF command parameters.

## Scenario

The user has multiple files that need to be converted into a common format, such as a batch of scans converted to editable documents.

## Decision Flow

### 1. Confirm Input Files

- Reuse existing attachments and paths and verify the file list. Preserve explicit user order; otherwise use natural sorting. Ask only about unresolved ambiguity that affects the result.
- Confirm each file format and the target format.
- **Hard limit: multi-image merge commands (`merge-*`) accept at most 100 input images per command.**

### 2. Handling More Than 100 Images

When there are more than 100 input images:

- **Do not automatically split into batches**. The CLI has no PDF/Word/Excel document merge command, so batch outputs cannot be recombined into a single file.
- The agent **must** tell the user: "At most 100 images can currently be merged into one document. More than 100 images cannot be merged into a single file."
- If the user accepts multiple volumes, process batches of at most 100 images and clearly label each volume.
- If the user must have one single file, explain that this is not currently supported.

### 3. Select a Conversion Strategy

| Input | Target | Strategy | Command |
|-------|--------|----------|---------|
| Multiple images, <=100 -> one document | Word/PDF/Excel | Merge | `image merge-word/pdf/excel` |
| Multiple PDFs -> one file | Any | Unsupported; tell the user | No PDF merge command |
| One PDF -> editable format | Word/Excel/MD | Convert | `pdf convert --format xx` |
| One Office document -> PDF or format upgrade | PDF/DOCX/XLSX/PPTX | Convert | `office convert` |
| Multiple independent files -> separate outputs | Mixed | Process one by one | Invoke the corresponding command for each file |

### 4. Execute and Confirm

- Apply the final-artifact save policy in `SKILL.md`: without a save preference use `-o path -s` (`-d dir -s` for PDF-to-images), with `--save-title` when saving to cloud.
- Verify artifact count, page count, and order. Report local files and actual returned cloud links by successful stage; a missing link means incomplete results.
- Record failures on independent files. Continue with others only until the main guide's attempt or cumulative failure limit is reached; report successful, failed, and unprocessed items.
