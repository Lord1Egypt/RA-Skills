# Document OCR Skill (docr)

[![Go Version](https://img.shields.io/badge/Go-1.21+-00ADD8?style=flat&logo=go)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[中文版](./README_CN.md)

A powerful, single-binary CLI tool for Optical Character Recognition (OCR) on scanned PDFs and images. It supports multiple engines including **Gemini 2.5 Flash**, **PaddleOCR**, and **RapidOCR**.

## ✨ Features

- **Multi-Engine Support**: Choose between cloud-based (Gemini) or local (PaddleOCR, RapidOCR) engines.
- **Single Binary**: Compiled Go binary for easy distribution and installation.
- **Batch Processing**: Process entire directories of documents with a single command.
- **Cross-Platform**: Supports macOS (Darwin), Linux, and Windows.
- **Custom Prompts**: Enhance recognition results with custom prompts when using Gemini.

## 🚀 Quick Start

### Quick Install (Single Command)

```bash
npx skills add scottkiss/doc-ocr-skills
```

### Installation (Binary)

Use our convenient install script to download the latest pre-compiled binary for your system:

```bash
curl -sSL https://raw.githubusercontent.com/scottkiss/doc-ocr-skills/main/scripts/install.sh | bash
```

*Note: The script installs the `docr` binary into a `docr` directory relative to where it's run. Add it to your PATH for global access.*

### Building from Source

If you have Go 1.21+ installed:

```bash
git clone https://github.com/scottkiss/doc-ocr-skills.git
cd doc-ocr-skills/scripts/docr
go build -o docr .
```

## 🛠 Prerequisites

### Local Engines (Optional)
If you plan to use local OCR engines, ensure the corresponding Python packages are installed:

- **RapidOCR** (Default): `pip install rapidocr_onnxruntime`
- **PaddleOCR**: `pip install paddleocr paddlepaddle`

### API Configuration (For Gemini)
To use the Gemini engine, create a configuration file at `~/.ocr/config`:

```bash
mkdir -p ~/.ocr
cat > ~/.ocr/config << EOF
# Google Gemini API Key
gemini_api_key=your_gemini_key_here
EOF
```

## 📖 Usage

### Basic OCR
Recognize text using the default engine (RapidOCR):
```bash
docr document.pdf
docr image.png
```

### Specifying an Engine
```bash
# Use Google Gemini (Requires API Key)
docr -engine gemini document.pdf

# Use PaddleOCR (Local)
docr -engine paddle document.pdf
```

### Batch Processing
Process all supported files in a directory and save results to an output folder:
```bash
docr -batch ./input_docs/ -o ./output_results/
```

### CLI Options

| Flag | Description |
|------|-------------|
| `-engine`, `-e` | OCR engine to use: `rapid` (default), `gemini`, or `paddle`. |
| `-o`, `-output` | Path to the output file or directory (for batch mode). |
| `-batch` | Enable batch processing for a directory. |
| `-prompt` | Custom recognition prompt (only applicable to Gemini). |

## ❗ Troubleshooting

| Issue | Solution |
|-------|----------|
| `config file not found` | Ensure `~/.ocr/config` exists. |
| `gemini_api_key not found` | Check if the key is correctly set in the config file. |
| `pip: command not found` | Ensure Python and pip are installed for local engines. |
| Permission Denied | Run `chmod +x docr` on the binary. |

## 📄 License

This project is licensed under the MIT License.
