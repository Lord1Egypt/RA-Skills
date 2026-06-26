# Converter Execution Examples

## 1. Document export
**Prompt:** "Convert this DOCX to PDF."
**Response:**
### CONVERSION ROUTE ANALYSIS
- **Path**: DOCX → PDF
- **Type**: Structural Export
- **Primary Tool**: soffice

### FIDELITY NOTES
- **Preserved**: Most document structure, text flow, and embedded formatting
- **Lost / At Risk**: Small layout differences depending on fonts and office engine behavior
- **Compatibility**: Suitable for general PDF sharing

### EXECUTION STATUS
- **Status**: Ready to Execute
- **Next Step**: `soffice --headless --convert-to pdf input.docx`

---

## 2. Audio transcoding
**Prompt:** "Turn this WAV recording into a high-quality MP3."
**Response:**
### CONVERSION ROUTE ANALYSIS
- **Path**: WAV → MP3
- **Type**: Lossy
- **Primary Tool**: FFmpeg

### FIDELITY NOTES
- **Preserved**: Core audible range and metadata if mapped
- **Lost / At Risk**: Perceptual compression loss
- **Compatibility**: Broad device compatibility

### EXECUTION STATUS
- **Status**: Ready to Execute
- **Next Step**: `ffmpeg -i input.wav -codec:a libmp3lame -b:a 320k output.mp3`

---

## 3. Batch web images
**Prompt:** "Convert all JPEGs in this folder to WebP."
**Response:**
### CONVERSION ROUTE ANALYSIS
- **Path**: JPEG → WebP
- **Type**: Lossy-to-Lossy Optimization
- **Primary Tool**: ImageMagick

### FIDELITY NOTES
- **Preserved**: Visual quality for web display
- **Lost / At Risk**: Some compression detail
- **Compatibility**: Excellent for modern browsers

### EXECUTION STATUS
- **Status**: Ready to Execute
- **Next Step**: `magick mogrify -format webp *.jpg`

---

## 4. Missing tool fallback
**Prompt:** "Convert this HEIC image to JPEG."
**Response:**
### CONVERSION ROUTE ANALYSIS
- **Path**: HEIC → JPEG
- **Type**: Raster Conversion
- **Primary Tool**: magick / OS-native fallback

### EXECUTION STATUS
- **Status**: Missing Binary
- **Next Step**:
  1. Install ImageMagick locally, or
  2. On macOS use: `sips -s format jpeg input.heic --out output.jpg`

---

## 5. Partial-fidelity warning
**Prompt:** "Convert this PDF into Markdown."
**Response:**
### CONVERSION ROUTE ANALYSIS
- **Path**: PDF → Markdown
- **Type**: Structural Reconstruction
- **Primary Tool**: Fallback / preprocessing pipeline

### FIDELITY NOTES
- **Preserved**: Plain text and some recoverable structure
- **Lost / At Risk**: Exact layout, complex tables, multi-column flow, scanned/OCR content
- **Compatibility**: Requires preprocessing or cleanup

### EXECUTION STATUS
- **Status**: Partial-Fidelity Only
- **Next Step**: Extract text first or use OCR preprocessing before Markdown conversion
