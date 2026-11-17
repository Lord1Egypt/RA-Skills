# Sources and extraction

[简体中文](formats.zh-CN.md)

Python 3.10+ is required. The agent reads the extracted material and generates the mentor; the extractor does not perform those steps itself.

| Format | Dependency | Scope |
| --- | --- | --- |
| TXT, MD, Markdown | Standard library | UTF-8 and BOM-declared encodings; no encoding guesses |
| HTML, HTM | Standard library | Visible text; no screenshot or full table reconstruction |
| EPUB | Standard library | OPF spine reading order; no DRM removal or illustration extraction |
| DOCX | Standard library | Body paragraphs and tables; check complex objects and images |
| PDF / text | `pypdf` or `pdfminer.six` | Text layer; scanned pages need separate OCR |
| PDF / technical | Prefer `docling` | Warns when falling back to text; inspect equations/tables |
| RTF | `striprtf` | Reports a missing parser rather than using a lossy regex fallback |

MOBI/AZW are unsupported. Convert them using an appropriate tool first; renaming the extension does not convert a file.

```bash
python scripts/extract.py --check
python -m pip install pypdf striprtf  # Only for formats you need
python -m pip install docling        # Optional technical PDF parser
python scripts/extract.py /path/to/book.pdf --mode text --workdir /path/to/extraction
```

Output: `full_text.txt` and `metadata.json`. Exit codes: `success` / 0, `partial` / 2, `failed` / 1. Mixed inputs retain successful text and report failed inputs. Disclose partial coverage in the generated mentor.

`total_tokens` is a conservative planning heuristic, not a model tokenizer count, a billing estimate, or a guaranteed upper bound. Extraction success does not prove complete visual or semantic fidelity. Chinese extraction diagnostics currently remain Chinese; JSON field names and status values are stable across languages.
