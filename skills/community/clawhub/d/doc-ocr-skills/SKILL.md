---
name: doc-ocr-skills
description: OCR documents (PDFs and images) using Gemini 2.5 Flash, PaddleOCR (local), or RapidOCR (local).
---

# Document OCR Skill (docr)

Uses **Gemini 2.5 Flash**, **PaddleOCR**, or **RapidOCR** (local) to recognize text from scanned PDFs and images. Compiled as a single Go binary.

## Prerequisites

- API Key configured in `~/.ocr/config` (not needed for Paddle/Rapid)
- For RapidOCR engine: `pip install rapidocr_onnxruntime`
- For PaddleOCR engine: `pip install paddleocr paddlepaddle`

### API Key Configuration

Create the config file:

```bash
mkdir -p ~/.ocr
cat > ~/.ocr/config << EOF
# Google Gemini API Key
gemini_api_key=your_gemini_key
EOF
```

## Quick Start

> **Path Variable**: All commands below use `$DOCR`. Before running any command, set this variable:
> ```bash
> SKILL_DIR="$(cd "$(dirname "<path-to-this-SKILL.md>")" && pwd)"
> DOCR="$SKILL_DIR/scripts/docr/docr"
> ```

```bash
# OCR a single document using RapidOCR (default)
$DOCR document.pdf
$DOCR image.jpg

# Use Gemini engine
$DOCR -engine gemini document.pdf

# Use PaddleOCR local engine
$DOCR -engine paddle document.pdf

# Specify output file
$DOCR document.pdf -o result.txt

# Batch process all supported files in a directory
$DOCR -batch ./docs/ -o ./outputs/
```

## Engines

| Engine | Flag | API Key Config | Doc Handling |
|--------|------|---------------|--------------|
| **RapidOCR** (default) | `-engine rapid` | None | Local OCR |
| **Gemini** | `-engine gemini` | `gemini_api_key` | Cloud Vision API |
| **PaddleOCR** (local) | `-engine paddle` | None | Local OCR |

## CLI Reference

```
docr [options] <file or directory>

Options:
  -engine string   OCR engine: rapid (default) / gemini / paddle
  -e string        Engine (short flag)
  -o string        Output file path or directory (batch mode)
  -output string   Output path (long flag)
  -batch           Batch mode: process all files in directory
  -prompt string   Custom recognition prompt (gemini)
```

## Installation

We provide pre-compiled binaries to get you started quickly.

```bash
cd doc-ocr-skills/scripts
./install.sh
```
This script will detect your OS (`darwin`/`linux`) and architecture (`amd64`/`arm64`) and download the appropriate version of `docr`.

### Building from Source (Optional)

If you prefer to build from source, ensure you have **Go 1.21+** installed:

```bash
cd doc-ocr-skills/scripts/docr
go build -o docr .
```

## Error Handling

| Error | Solution |
|-------|----------|
| `config file not found` | Create `~/.ocr/config` with API keys |
| `gemini_api_key not found` | Add `gemini_api_key=VALUE` to config |
| `file not found` | Verify the document file path |
| API timeout | Retry; large files may need longer |
