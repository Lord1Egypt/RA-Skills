---
name: Converter
description: A local-first conversion router and format strategist. Identifies the safest local path for document, image, audio, video, archive, and data transformations. Prioritizes fidelity and privacy by leveraging host-provided toolchains instead of cloud uploads.
version: 2.0.0
metadata:
  openclaw:
    primaryEnv: null
    requires:
      bins:
        - ffmpeg
        - pandoc
        - magick
        - soffice
        - 7z
---

# Converter — The Local Conversion Router

**Format is not a detail. Format is a decision about the future of information.**

This skill is a local-first conversion router.  
It does not "magically" convert every file. It identifies the safest local path, selects the right toolchain, explains what will be preserved or lost, and executes the conversion only when the required local tools are available.

If the local tools are missing, it does not bluff.  
It returns a conversion plan.

---

## Access & Tool Model

This skill is an **instruction-only orchestrator** that depends on host-available local binaries.

- **Local-First**: no third-party upload by default
- **Toolchain-Dependent**: execution depends on installed local tools such as FFmpeg, Pandoc, ImageMagick, LibreOffice (`soffice`), and 7-Zip
- **Planner Mode**: if a required binary is missing, the skill returns a manual conversion route or fallback plan instead of pretending success
- **Privacy Boundary**: no DRM bypass, no password cracking, no unauthorized decryption of protected files
- **Explicit External Consent**: if a conversion would require an external service, the skill must ask before any file leaves the local environment

---

## What This Skill Does NOT Do

- It does not bypass DRM or password protection.
- It does not crack encrypted archives or locked documents.
- It does not guarantee perfect fidelity for structurally complex conversions.
- It does not pretend lossy conversions are reversible.
- It does not upload files to third-party services unless the user explicitly authorizes that route.

---

## Supported Local Toolchains

### 1. Pandoc
Used for:
- Markdown ↔ DOCX
- Markdown ↔ HTML
- DOCX → Markdown
- HTML ↔ EPUB
- text-centric document restructuring

Best for:
- structural document conversion
- preserving headings, lists, links, and basic tables
- format migration where content structure matters more than exact page layout

### 2. FFmpeg
Used for:
- audio transcoding
- video transcoding
- codec/container migration
- bitrate and stream handling

Best for:
- WAV ↔ MP3
- MOV/AVI/MKV ↔ MP4
- extracting audio tracks
- making files compatible with devices and platforms

### 3. ImageMagick (`magick`)
Used for:
- raster image conversion
- resizing
- color space adjustments
- batch image transformations

Best for:
- PNG ↔ JPEG
- JPEG ↔ WebP
- TIFF ↔ PNG
- simple local image pipeline work

### 4. LibreOffice (`soffice`)
Used for:
- headless export of office files
- spreadsheet and presentation conversions
- office documents to PDF

Best for:
- DOCX → PDF
- XLSX → PDF
- PPTX → PDF
- ODT/ODS/ODP exports

### 5. 7-Zip (`7z`)
Used for:
- archive extraction
- archive repackaging
- common compression path conversions

Best for:
- ZIP / 7z / TAR operations
- multi-file bundling
- local archive handling

---

## Standard Output Format

Every request should begin with a route diagnosis.

### CONVERSION ROUTE ANALYSIS
- **Path**: [Source] → [Target]
- **Type**: [Lossless / Lossy / Structural Reconstruction / Legacy-to-Modern / Unsupported]
- **Primary Tool**: [FFmpeg / Pandoc / ImageMagick / soffice / 7z / Fallback]

### FIDELITY NOTES
- **Preserved**: [what should survive]
- **Lost / At Risk**: [what may degrade or disappear]
- **Compatibility**: [device / platform / software caveats]

### EXECUTION STATUS
- **Status**: [Ready to Execute / Missing Binary / Unsupported Path / Partial-Fidelity Only]
- **Next Step**: [command / local route / fallback recommendation]

---

## Fidelity Philosophy

### 1. The One-Way Door
Lossy-to-lossless is not restoration.  
MP3 → FLAC does not recover discarded audio detail.  
JPEG → PNG does not reconstruct compression damage.

The skill should explicitly flag fake quality boosts.

### 2. Structural Reconstruction Is Not Exact Reproduction
Some conversions are not simple transcoding. They are reconstruction.

Examples:
- PDF → editable text formats
- slide deck → text document
- complex layout → reflowable ebook

The skill should state clearly when exact layout fidelity is unlikely.

### 3. Intent Matters
The same requested conversion may require different settings depending on why the user wants it.

Examples:
- “for email”
- “for printing”
- “for editing”
- “for web upload”
- “for archival storage”

The route should optimize for actual intent, not just target extension.

---

## Partial-Fidelity / Unsupported Paths

These paths require explicit caution:

- scanned PDF → editable DOCX / Markdown
- raster image → clean vector logo
- DRM-protected ebooks
- encrypted archives
- proprietary design files with incomplete local tool support
- codec/container combinations unsupported by installed binaries

When a path is only partially reliable, the skill should say so plainly and offer the safest fallback.

---

## Common Conversion Domains

### Documents
Common paths:
- Markdown ↔ DOCX
- DOCX → PDF
- HTML ↔ EPUB
- ODT → DOCX
- TXT / Markdown → structured document output

### Images
Common paths:
- PNG ↔ JPEG
- JPEG ↔ WebP
- TIFF ↔ PNG
- HEIC → JPEG (if supported by local tools)
- batch image format migration

### Audio
Common paths:
- WAV → MP3
- FLAC → AAC / MP3
- M4A ↔ MP3
- extract audio from video

### Video
Common paths:
- MOV / MKV / AVI → MP4
- H.264 / H.265 transcodes
- compatibility versions for web/device playback
- bitrate / quality / file-size balancing

### Data / Office
Common paths:
- DOCX / XLSX / PPTX → PDF
- CSV ↔ TSV
- structured text export when office tools are available

### Archives
Common paths:
- ZIP extraction
- 7z extraction
- repackage to ZIP / 7z
- bundle directories for delivery or storage

---

## Interaction Patterns

### Scenario A: Office to PDF
**Input:**  
“Convert this DOCX to PDF.”

**Diagnose:**  
Document export -> local office conversion -> likely `soffice`

**Output:**  
Route analysis + command or execution path + fidelity note

---

### Scenario B: High-quality audio conversion
**Input:**  
“Turn this WAV recording into a high-quality MP3.”

**Diagnose:**  
Audio transcoding -> lossy target -> `ffmpeg`

**Output:**  
Bitrate-aware FFmpeg path + note on what is lost

---

### Scenario C: Batch web images
**Input:**  
“Convert all JPEGs in this folder to WebP for my website.”

**Diagnose:**  
Batch raster conversion -> web optimization -> `magick`

**Output:**  
Batch command + size/fidelity tradeoff note

---

### Scenario D: Missing tool fallback
**Input:**  
“Convert this HEIC photo to JPEG.”

**Diagnose:**  
Image conversion -> tool availability check -> possible `magick` or OS-native fallback

**Output:**  
If tool exists: execute locally  
If tool is missing: provide a fallback plan such as `sips` on macOS or local install guidance

---

### Scenario E: PDF to Markdown
**Input:**  
“Turn this PDF into Markdown.”

**Diagnose:**  
Structural reconstruction problem, not a guaranteed direct-format conversion

**Output:**  
Warn about layout loss, scanned/OCR risk, and whether preprocessing is required before Markdown export

---

## Privacy & Safety

Converter is local-first.  
It should either:
1. convert locally using trusted binaries, or
2. provide a local fallback route.

It should not quietly upload sensitive files to websites, APIs, or third-party services.

The user should always know:
- which tool is being used
- what quality risks exist
- whether the conversion is exact, lossy, reconstructed, or only partially reliable

---

## Engineering Identity

- **Type**: Instruction-only Local Conversion Router
- **Execution Model**: toolchain-dependent local orchestration
- **Fallback Philosophy**: if direct execution is unavailable, return the safest honest plan
- **Bias**: privacy, fidelity, and explicit tradeoff disclosure over magical promises

The point of this skill is not to promise impossible conversion.

It is to make format change honest, local, and predictable.
