# bid-reader Skill

## Overview
A lightweight skill to extract readable text from bid and tender documents in PDF, Word (`.docx`), and Excel (`.xlsx`/`.xls`) formats. It can be invoked from the OpenClaw UI or other agents to quickly pull the full textual content of a file for analysis, search, or summarisation.

## Usage
```
bid-read <file-path>
```
- `<file-path>` should be an absolute or workspace‑relative path to a document.
- The skill prints the extracted plain‑text to stdout, which OpenClaw captures and returns to the caller.

## Example
```bash
bid-read /home/zhenxing/投标文件/招投标项目1/13.上海联通/投标文件.pdf
```
The command returns the full text of the PDF, ready for further processing (e.g., keyword search, summarisation).

## Installation
Copy the skill folder into your workspace under `skills/bid-reader`. Install required Python packages:
```bash
pip install -r $(pwd)/skills/bid-reader/requirements.txt
```
The skill is then available as an agent command.

## Implementation Details
- **PDF**: Uses `pdfplumber` to extract text page‑by‑page.
- **Word**: Uses `python-docx` to read paragraphs.
- **Excel**: Uses `pandas` (with `openpyxl`/`xlrd`) to read all sheets and concatenate cell values.

## Limitations
- Only `.pdf`, `.docx`, `.xlsx`, and `.xls` are supported. Other formats will be ignored.
- Large files may take a few seconds to process.
- Tables are flattened into whitespace‑separated rows; complex formatting is not preserved.

## Future Enhancements
- Add OCR fallback for scanned PDFs (e.g., via `pytesseract`).
- Support selective page or sheet extraction.
- Provide a JSON output mode with structural metadata.
