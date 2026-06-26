# ClawHub Listing — Contract Risk Reviewer

## Basic Info
- **Slug:** contract-risk-reviewer
- **Name (CN):** 合同风险智能审查
- **Name (EN):** Contract Risk Reviewer
- **Category:** Legal & Compliance / Productivity
- **Tags:** contract, risk, legal, PDF, AI, analysis, contract-review

## Description (EN)
Upload any contract PDF and get an instant AI-powered risk report. Automatically detects contract type (labor, procurement, sales, lease, NDA), extracts key terms, and generates a structured risk list graded by severity (🔴 HIGH / 🟠 MEDIUM / 🟡 LOW).

Supports both Chinese and English contracts. Perfect for procurement teams, HR departments, freelancers, and small businesses who need quick contract reviews without hiring a lawyer.

## Features
- **PDF text extraction** — PyMuPDF + pdfplumber (with OCR fallback for scanned documents)
- **Automatic contract type detection** — 6 types: labor, procurement, sales, lease, NDA, other
- **Bilingual** — Chinese + English contracts
- **Structured risk report** — Summary + key terms table + graded risk list
- **Excel export** — For paid tiers
- **Clear disclaimer** — Not legal advice

## Pricing
- **FREE:** 3 contracts/month, summary + risk list
- **STD (¥9.9/mo):** 30 contracts, all 6 types, key terms table, Excel export
- **PRO (¥29/mo):** 200 contracts, batch processing, risk comparison
- **MAX (¥69/mo):** Unlimited, API priority

## Quick Start
```bash
pip install -r scripts/requirements.txt
python scripts/analyze_contract.py --pdf contract.pdf --tier FREE
```

## Requirements
- Python 3.8+
- PyMuPDF, pdfplumber, pytesseract, pdf2image, openai
- For OCR: `tesseract-ocr` + `tesseract-ocr-chi-sim` (language packs)
- OpenAI-compatible API key

## Screenshots / Output Sample
See README.md for full output format example.

## Disclaimer
This skill provides informational analysis only. It does not constitute legal advice. Consult a qualified attorney for legal decisions.
