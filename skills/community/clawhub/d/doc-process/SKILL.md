---
name: doc-process
description: >
  Document intelligence: categorize, autofill forms, analyze contracts, scan receipts/invoices,
  analyze bank statements, parse resumes/CVs, scan IDs/passports (MRZ), summarize medical records,
  redact PII (light/standard/full, 50+ rule types, global coverage), extract meeting minutes/action
  items, extract tables to CSV/JSON, translate documents, scan/dewarp document photos (edge detection,
  perspective correction, scan-quality output).
  Trigger: fill this form, autofill, review contract, red flags, scan receipt, log expense, bank
  statement, subscriptions, parse resume, scan passport, read id, lab report, redact, remove pii,
  anonymize, meeting minutes, action items, extract table, table to csv, translate, scan photo,
  make scanned, dewarp, correct perspective, what is this, analyze this.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Doc-Process — Document Intelligence Skill

## Step 0 — Auto-Setup (run once on first use)

Before invoking any script for the first time in a session, check whether the script dependencies are available. If any are missing, run the setup script automatically — no prompting needed:

```bash
bash skills/doc-process/setup.sh
```

This installs all Python packages (`pymupdf`, `Pillow`, `pytesseract`, `opencv-python-headless`, `numpy`, `img2pdf`, `pdfplumber`, `openai-whisper`) and attempts to install system binaries (`tesseract`, `ffmpeg`) via `brew` or `apt` depending on the platform.

**When to run Step 0:**
- First time any script-assisted mode is used in a session
- After a fresh `clawhub install piyush-zinc/doc-process`
- If a script fails with `ModuleNotFoundError` or `ImportError`

To install Python packages only (no system packages):
```bash
bash skills/doc-process/setup.sh --light
```

Or install directly from the skill's requirements file:
```bash
pip install -r skills/doc-process/requirements.txt
```

> **Note:** `openai-whisper` downloads its model (~140 MB) on first audio transcription — not at install time.

---

## Overview

This skill handles all document-related tasks using Claude's native vision/language capabilities for reading and analysis, and Python scripts for file-output operations. Most modes require **no installation** — only the file-output scripts need third-party libraries.

---

## How Features Are Implemented

| Feature | Implementation | External libraries |
|---|---|---|
| OCR / reading images | Claude built-in vision | None |
| MRZ decoding (passport/ID) | Claude reads MRZ visually, applies ICAO algorithm | None |
| PDF reading | Claude reads PDF text layer or visually | None |
| Form autofill | Claude reads form fields, outputs fill table | None |
| Contract analysis | Claude applies reference rule set | None |
| Receipt / invoice scanning | Claude reads image or PDF | None |
| Bank statement (PDF) | Claude reads PDF pages | None |
| Bank statement (CSV) | `statement_parser.py` — pure stdlib | None |
| Expense logging | `expense_logger.py` — pure stdlib | None |
| Bank report generation | `report_generator.py` — pure stdlib | None |
| Resume / CV parsing | Claude reads document | None |
| Medical summarizer | Claude reads document | None |
| Legal redaction (display) | Claude marks up output | None |
| **Legal redaction (file output)** | `redactor.py` | **pymupdf** (PDF); **Pillow + pytesseract** (image) |
| Meeting minutes (text/PDF) | Claude reads document | None |
| Translation | Claude's multilingual capabilities | None |
| Document categorizer | Claude reads first 1–2 pages (with consent gate) | None |
| Timeline logging | `timeline_manager.py` — pure stdlib | None |
| **Table extraction (PDF)** | `table_extractor.py` | **pdfplumber** |
| **Audio transcription** | `audio_transcriber.py` | **openai-whisper + ffmpeg** |
| **Doc scan / perspective correction** | `doc_scanner.py` | **opencv-python-headless, numpy, Pillow**; img2pdf optional |

---

## Dependencies & Installation

### No installation required for core functionality
Reading, analysis, form filling, contract review, receipt scanning, bank statement analysis (PDF), resume parsing, ID scanning, medical summarising, redaction markup, meeting minutes, and translation all run on Claude's built-in capabilities.

### Optional — install only for file-output scripts

```bash
# PII redaction to PDF/image files  (redactor.py)
pip install pymupdf>=1.23          # required for PDF redaction
pip install Pillow>=10.0           # required for image redaction
pip install pytesseract>=0.3       # required for image redaction (also: brew install tesseract)

# Document scanning / perspective correction  (doc_scanner.py)
pip install opencv-python-headless>=4.9 numpy>=1.24 Pillow>=10.0
pip install img2pdf>=0.5           # optional — for PDF output; Pillow fallback used if absent

# Table extraction from PDFs  (table_extractor.py)
pip install pdfplumber>=0.11

# Audio transcription  (audio_transcriber.py)
# Also requires ffmpeg binary: brew install ffmpeg  /  apt install ffmpeg
pip install openai-whisper>=20231117
```

All dependencies are also listed in `requirements.txt` at the repository root.

### Binary dependencies

| Binary | Required by | Install |
|---|---|---|
| `tesseract` | `redactor.py` (image mode) | `brew install tesseract` / `apt install tesseract-ocr` |
| `ffmpeg` | `audio_transcriber.py` | `brew install ffmpeg` / `apt install ffmpeg` |

### Network access

`openai-whisper` downloads model files (~140 MB) from OpenAI/HuggingFace servers **on first run only**. Cached at `~/.cache/whisper/`. All other scripts are fully local after installation.

---

## Script Reference

| Script | Dependencies | Purpose | Example |
|---|---|---|---|
| `redactor.py` | pymupdf; Pillow + pytesseract (image mode) | PII redaction to file (PDF/image/text) | `python scripts/redactor.py --file doc.pdf --mode full --log` |
| `doc_scanner.py` | opencv-python-headless, numpy, Pillow; img2pdf optional | Document scanning: edge detection, perspective correction, scan-quality output | `python scripts/doc_scanner.py --input photo.jpg --output scanned.png --mode bw` |
| `expense_logger.py` | None | Add/list/edit/delete expense entries in CSV | `python scripts/expense_logger.py add --date 2024-03-15 --merchant "Starbucks" --amount 13.12 --file expenses.csv` |
| `statement_parser.py` | None | Parse bank CSV export, categorize transactions | `python scripts/statement_parser.py --file statement.csv --output categorized.json` |
| `report_generator.py` | None | Format categorized JSON into a markdown report | `python scripts/report_generator.py --file categorized.json --type bank` |
| `timeline_manager.py` | None | Manage opt-in document processing timeline | `python scripts/timeline_manager.py show` |
| `audio_transcriber.py` | openai-whisper, ffmpeg | Transcribe audio files to text | `python scripts/audio_transcriber.py --file meeting.mp3 --output transcript.txt` |
| `table_extractor.py` | pdfplumber | Extract tables from PDFs to CSV or JSON | `python scripts/table_extractor.py --file document.pdf --output data.csv` |

All scripts import only what they declare. Scripts with no declared deps use Python stdlib only. You can verify any script: "show me the source of [script name]".

---

## Script Import Verification

| Script | Stdlib imports | Third-party | Network |
|---|---|---|---|
| `timeline_manager.py` | argparse, json, sys, datetime, pathlib, uuid, collections | None | Never |
| `redactor.py` | argparse, re, sys, pathlib, dataclasses | pymupdf (PDF); Pillow + pytesseract (image) | Never |
| `doc_scanner.py` | argparse, json, sys, time, pathlib | opencv-python-headless, numpy, Pillow; img2pdf optional | Never |
| `expense_logger.py` | argparse, csv, json, sys, pathlib | None | Never |
| `statement_parser.py` | argparse, csv, json, re, sys, collections, datetime, pathlib | None | Never |
| `report_generator.py` | argparse, json, sys, collections, pathlib | None | Never |
| `utils.py` | re, unicodedata, datetime, pathlib | None | Never |
| `audio_transcriber.py` | argparse, sys, pathlib | openai-whisper | First-run model download only |
| `table_extractor.py` | argparse, csv, io, json, sys, pathlib | pdfplumber | Never |

---

## Privacy & Data Handling

| Aspect | Policy |
|---|---|
| Document content | Read locally within this session only. Not stored, indexed, or transmitted. |
| Personal data for form autofill | Used only to complete the current form. Not written to any file. Not retained after session. |
| Timeline log | Opt-in only. Confirmed by user before any entry is written. Contains no raw document content — only category-level summaries. |
| Redacted output files | Written only to a path the user explicitly confirms. |
| Audio transcripts | Written to a local file the user specifies. Model download on first Whisper use only. |
| No telemetry | This skill has no analytics, usage reporting, or network calls beyond what is listed above. |

---

## Step 1 — Identify the Mode

### Explicit intent → go directly to the matching mode

| Mode | User intent signals | Typical file types |
|---|---|---|
| **Document Categorizer** | "process this", "what is this?", "analyze this", "help with this", no clear intent | Any |
| Form Autofill | fill, autofill, fill out, complete this form | PDF form, image, screenshot |
| Contract Analyzer | review, summarize, contract, agreement, risks, red flags, NDA, lease | PDF, text |
| Receipt Scanner | receipt, invoice, log expense, scan this bill | Photo, image, PDF |
| Bank Statement Analyzer | bank statement, transactions, subscriptions, categorize spending | PDF, CSV |
| Resume / CV Parser | parse resume, extract cv, what's on this resume, scan resume | PDF, image, text |
| ID & Passport Scanner | scan id, read passport, extract from id card, scan my passport | Photo, image, PDF |
| Medical Summarizer | lab report, blood test, prescription, discharge summary, medical results | PDF, image, text |
| Legal Redactor | redact, remove pii, anonymize, censor sensitive info | PDF, text, image |
| Meeting Minutes | meeting minutes, action items, summarize meeting, transcribe meeting | Text, PDF, image, audio |
| Table Extractor | extract table, table to csv, get data from pdf, table to json | PDF, image, text |
| Document Translator | translate this, translate to [language], document translation | Any |
| Document Timeline | show my timeline, document history, what have I processed, save timeline | — |
| **Doc Scan** | scan this photo, make this look scanned, correct perspective, dewarp, clean this photo, digitize this, straighten this | Photo, image |

### Ambiguous intent → Document Categorizer (with consent gate)

If the user uploads a file without a clear mode signal, **do not read it yet**. Ask:

> "I can classify this document automatically to suggest the best mode — that requires me to read the first 1–2 pages. Or you can choose directly:
>
> | Option | Best for |
> |---|---|
> | Form Autofill | Forms with fill-in fields |
> | Contract Analyzer | Agreements, NDAs, leases |
> | Receipt Scanner | Receipts, invoices |
> | Bank Statement Analyzer | Bank/credit card statements |
> | Resume Parser | CVs, resumes |
> | ID Scanner | Passports, IDs, driver's licenses |
> | Medical Summarizer | Lab reports, prescriptions |
> | Legal Redactor | Any document with PII to remove |
> | Meeting Minutes | Notes or recordings |
> | Table Extractor | Documents with data tables |
> | Translator | Non-English documents |
> | Doc Scan | Document photo needing perspective correction |
>
> Shall I classify it, or which mode would you like?"

Only read the document after the user confirms.

---

## Step 2 — Read the Document

Use the `Read` tool on the uploaded file. For images, read them visually. For PDFs over 10 pages, read in page ranges.

**For audio files (Meeting Minutes mode only):** confirm before running — this requires `openai-whisper` and downloads a model on first run:

> "Transcribing this audio requires the `openai-whisper` library. On first use it downloads a model file (~140 MB). Is that OK?"

If yes:
```bash
python skills/doc-process/scripts/audio_transcriber.py --file <path> --output transcript.txt
```

If no: ask if the user can provide a text transcript.

**For document photos (Doc Scan mode):** read the image visually first to assess quality and detect the document type before running the scanner script.

---

## Step 3 — Execute the Mode

Load and follow the matching reference file in full:

| Mode | Reference file |
|---|---|
| Document Categorizer | `references/document-categorizer.md` |
| Form Autofill | `references/form-autofill.md` |
| Contract Analyzer | `references/contract-analyzer.md` |
| Receipt Scanner | `references/receipt-scanner.md` |
| Bank Statement Analyzer | `references/bank-statement-analyzer.md` |
| Resume / CV Parser | `references/resume-parser.md` |
| ID & Passport Scanner | `references/id-scanner.md` |
| Medical Summarizer | `references/medical-summarizer.md` |
| Legal Redactor | `references/legal-redactor.md` |
| Meeting Minutes | `references/meeting-minutes.md` |
| Table Extractor | `references/table-extractor.md` |
| Document Translator | `references/document-translator.md` |
| Document Timeline | `references/document-timeline.md` |
| **Doc Scan** | `references/doc-scan.md` |

---

## Step 4 — Redactor: PII Rule Coverage

The `redactor.py` script covers the following PII categories across **50+ rule types** for global document types (bank statements, contracts, medical records, invoices, share-purchase agreements, government forms, and more).

**Category 1 — Personal Identifiers** (standard + light mode)

| Rule | Examples |
|---|---|
| SSN (US) | 123-45-6789 |
| SIN (Canada) | 123-456-789 |
| UK National Insurance Number | AB 12 34 56 C |
| Australian TFN | 123 456 789 |
| Australian Medicare number | 1234 56789 1 |
| Indian Aadhaar | 1234 5678 9012 |
| Passport number | A12345678 |
| Driver's license | keyword-anchored |
| UK NHS number | 943 476 5919 |
| National / voter ID | keyword-anchored |
| Vehicle VIN | keyword-anchored 17-char code |
| NRIC (Singapore) | S1234567A |
| Medical record (MRN) | keyword-anchored |
| Indian PAN | AABCW6386P |
| Email address | any@domain.com |
| Phone number | all international formats; date/reference false-positives suppressed |
| Street address | BLK/BLOCK/FLAT/UNIT/APT prefix + number + street name + type (Street, Ave, Rd, Hill, Close, Quay, Park, etc.) |
| Unit / apartment number | #02-01, Unit 3B, Apt 4C, Flat 12 |
| P.O. Box | PO Box 1234 |
| US ZIP / CA postal | 10001, M5V 3A8 |
| UK postcode | SW1A 2AA |
| International 6-digit postal | Singapore 229572, Bangalore 560067 |
| IPv4 address | 192.168.1.1 |
| MAC address | AA:BB:CC:DD:EE:FF |
| Date of birth | keyword + numeric/month-name formats |
| Age | "Age: 34" |
| Labeled name (50+ field keywords) | Bill To, Shipper, Attention, Buyer, Seller, Patient, Employee, Plaintiff, Trustee, Shareholder, Director, Tenant, Lender, Beneficiary, etc. |
| Honorific prefix + name | Mr./Mrs./Ms./Dr./Prof./Rev./Hon./Mx. + name |

**Category 2 — Financial Data** (standard + full mode)

| Rule | Examples |
|---|---|
| Credit / debit card number | 4111 1111 1111 1111 |
| Card CVV | CVV: 123 |
| Card expiry | 03/26 |
| Bank account number | keyword-anchored |
| IBAN | IBAN country-code validated (GB, DE, FR, etc.) |
| ABA / routing number | "Routing No." and "ABA No." |
| UK Sort code | 20-00-00 |
| Australian BSB | 063-000 |
| Indian IFSC code | HDFC0000001 |
| SWIFT / BIC code | allows space in code (e.g. CHAS US33) |
| Salary / compensation | salary, CTC, gross/net pay, take-home, remuneration |
| Credit score | keyword-anchored |
| Loan / mortgage amount | keyword-anchored |
| Tax figures | AGI, taxable income, tax paid |
| Net worth / total assets | keyword-anchored |
| Cryptocurrency wallet | Bitcoin, Ethereum |

**Category 3 — Sensitive / Protected** (full mode only)

HIV/AIDS status, blood type, mental health diagnoses (expanded), reproductive health, substance use history, sexual orientation / gender identity, disability, criminal record, genetic information, immigration status, minor's name, attorney–client privilege, trade secrets.

### Redaction modes

| Flag | Categories | Use case |
|---|---|---|
| `--mode light` | Cat 1 only | Sharing docs where financial details can remain |
| `--mode standard` | Cat 1 + 2 (default) | General privacy protection |
| `--mode full` | Cat 1 + 2 + 3 | Legal filings, healthcare, immigration, HR |
| `--custom REGEX` | Cat 0 + selected mode | Domain-specific or proprietary terms |

### How PDF redaction works

1. Word bounding boxes are extracted from the PDF layout engine
2. PII is detected using a single-pass, non-overlapping regex engine
3. Matched spans are mapped back to word bounding boxes
4. PyMuPDF redaction annotations (solid black fill) are placed on the exact word rects
5. `apply_redactions()` burns the black fills in and removes the underlying text data from the content stream — redacted text cannot be copy-pasted or extracted
6. The file is saved incrementally — every non-redacted element (fonts, images, vector graphics, metadata) is left completely untouched
7. The original file is never modified; output is always a separate copy

---

## Step 5 — Doc Scan: How It Works

The `doc_scanner.py` script converts a document photo into a professional scan in 7 steps:

1. **Multi-strategy edge detection** — tries three approaches in order: (A) Canny on greyscale; (B) Morphological gradient; (C) Colour/brightness threshold. Stops at first success.
2. **Sub-pixel corner refinement** — `cv2.cornerSubPix` makes the four corner points accurate to sub-pixel level for the most precise warp.
3. **Perspective warp** — four-point transform using Lanczos interpolation flattens the document to a perfect rectangle.
4. **Shadow removal** — per-channel background estimation + normalisation removes cast shadows and uneven lighting without affecting text.
5. **Scan-quality enhancement** — mode-specific: BW = adaptive threshold (block size auto-scaled to resolution) + stroke repair + denoising; Gray = auto-levels + CLAHE + unsharp mask; Color = white-balance + CLAHE + sharpening.
6. **Scanner border** — 8 px white border simulates scanner bed edge.
7. **DPI-tagged output** — saved with embedded DPI metadata (default 300 DPI, print quality).

### When auto-detection fails

If the script reports `"corners_detected": false`:
1. Offer manual corner hints: ask the user where the four corners of the document are approximately
2. Use `--no-warp` to at least apply enhancement without perspective correction
3. Provide photography tips (see `references/doc-scan.md` Step 8)

---

## Step 6 — Document Timeline (Opt-In)

Off by default. After completing the first document task in a session, ask once:

> "Would you like me to keep a processing log for this session? It records document type, filename, and a category-level summary (no raw content, no personal data) to `~/.doc-process-timeline.json` on your local machine. Entirely optional — yes or no."

- **Yes** → confirm "Timeline logging is on." Log current and subsequent documents. Announce each with "Logged to your timeline."
- **No** → confirm "No log will be kept." Do not run any timeline script. Do not ask again this session.
- **No response / unsure** → treat as No.

**Summary rules (strictly enforced):** the `--summary` argument must never contain names, ID numbers, dates of birth, addresses, account numbers, card numbers, medical values, or any data that could identify a person. Category-level descriptions only.

---

## Step 7 — Deliver Output

Present output in clean tables with section headers as specified in each reference file. Always end with an action prompt relevant to the mode. For Doc Scan, always offer to continue processing the scanned output.

---

## General Principles

- **Never hallucinate field values.** Unknown values → `[MISSING]` or `[UNREADABLE]`.
- **Flag risks conservatively** — when in doubt, include it.
- **Keep summaries scannable** with tables and bullets.
- **Do not echo sensitive data** beyond what is necessary for the immediate task.
- **Always include relevant disclaimers** (medical, legal, privacy) where required by the reference guide.
- **Timeline is opt-in per session.** Never log without confirmed consent.
- **Personal data for form autofill is session-only.** Never write it to a file.
- **Before running any script with third-party deps**, run `bash skills/doc-process/setup.sh` automatically if deps are not yet installed (see Step 0). No need to ask — the setup script is safe and idempotent.
- **Categorize before asking** — but only after confirming the user wants auto-classification.
- **For Doc Scan:** always assess the image visually first; never process non-document images.
