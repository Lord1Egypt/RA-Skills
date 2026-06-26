# Legal Document Redactor — Reference Guide

## Purpose
Identify and redact personally identifiable information (PII), financial data, health information, and other sensitive content from documents before sharing, filing, or publishing. Produce a verifiable redaction log.

---

## Step 1 — Assess the Document

Before redacting, classify the document to determine default redaction scope:

| Document Type | Default Mode | Special Considerations |
|---|---|---|
| Personal letter / email | standard | Focus on contact info and financial data |
| Legal filing (court document) | standard | Keep party names; redact third parties (witnesses, minors) |
| Medical record | full | HIPAA/sensitive health info |
| Employment record | standard | Keep employer/employee names; redact salary, ID numbers |
| Financial statement / tax return | full | Extensive financial data |
| Government form | light → standard | User decides what to remove |
| Business contract | light | Usually shared — redact personal contact info only |
| Research / academic paper | standard | Redact participant data; keep author names |
| Immigration document | full | Highly sensitive — passport, visa, immigration status |

---

## Step 2 — Redaction Modes

| Mode | Categories Covered | Use Case |
|---|---|---|
| `light` | Category 1 only (personal identifiers) | Sharing a document where financial details can remain |
| `standard` | Category 1 + 2 (personal + financial) | General privacy protection before sharing |
| `full` | Category 1 + 2 + 3 (all sensitive) | Legal submissions, healthcare, immigration |
| `custom` | User-specified terms + any of the above | Domain-specific or proprietary term removal |

Ask the user which mode if not stated. Default: **standard**.

---

## Step 3 — Redaction Categories

### Category 1 — Personal Identifiers

| Data Type | Examples | Replacement Token |
|---|---|---|
| Full name (non-party) | Witnesses, third parties, minor adults | [NAME REDACTED] |
| Social Security Number (US) | 123-45-6789 | [SSN REDACTED] |
| Social Insurance Number (Canada) | 123-456-789 | [SIN REDACTED] |
| National Insurance Number (UK) | AB 12 34 56 C | [NIN REDACTED] |
| Tax File Number (Australia) | 123 456 789 | [TFN REDACTED] |
| NRIC / FIN (Singapore) | S1234567A | [NRIC REDACTED] |
| PAN / Aadhaar (India) | ABCDE1234F / 1234 5678 9012 | [ID NUMBER REDACTED] |
| Passport number | A12345678 | [PASSPORT NUMBER REDACTED] |
| Driver's license number | Any state/country format | [LICENSE NUMBER REDACTED] |
| Date of birth | 14/03/1990 | [DATE OF BIRTH REDACTED] |
| Age (when combined with DOB) | "Jane Smith, age 34" | [AGE REDACTED] |
| Home / residential address | 42 Baker St, London; BLK 101 Dalvey Road | [ADDRESS REDACTED] |
| Apartment / unit number | #02-01, Unit 3B, Apt 4C, Flat 12 | [UNIT NUMBER REDACTED] |
| Personal phone number | +1-555-000-1234 | [PHONE REDACTED] |
| Personal email | user@gmail.com | [EMAIL REDACTED] |
| Biometric reference | Fingerprint ID, facial recognition ID | [BIOMETRIC DATA REDACTED] |
| Medical record number | MRN-1234567 | [MEDICAL ID REDACTED] |
| Voter ID / registration | Voter registration number | [VOTER ID REDACTED] |
| Vehicle registration / VIN | ABC-1234 / 1HGCM82633A123456 | [VEHICLE ID REDACTED] |
| GPS coordinates | 37.7749° N, 122.4194° W | [LOCATION REDACTED] |
| IP address | 192.168.1.1 | [IP ADDRESS REDACTED] |
| Device ID / IMEI | 354813060698174 | [DEVICE ID REDACTED] |
| Cookie / session ID | Long alphanumeric string | [SESSION ID REDACTED] |
| Signature | Handwritten signature (if OCR'd) | [SIGNATURE REDACTED] |
| Photo description | "Attached photo of [name]" | [PHOTO REFERENCE REDACTED] |

### Category 2 — Financial Data

| Data Type | Examples | Replacement Token |
|---|---|---|
| Bank account number | Full account string | [ACCOUNT NUMBER REDACTED] |
| Credit / debit card number | 4111 1111 1111 1111 | [CARD NUMBER REDACTED] |
| Card CVV / security code | 3–4 digit code | [CVV REDACTED] |
| Card expiry date (standalone) | 03/26 | [CARD EXPIRY REDACTED] |
| IBAN | GB29 NWBK 6016 1331 9268 19 | [IBAN REDACTED] |
| SWIFT / BIC code | NWBKGB2L | [SWIFT REDACTED] |
| ABA routing number | 021000021 | [ROUTING NUMBER REDACTED] |
| Salary / compensation amount | $85,000 per year | [SALARY REDACTED] |
| Tax return financial figures | AGI, taxable income | [TAX FIGURE REDACTED] |
| Investment holdings | "500 shares of AAPL" | [INVESTMENT DATA REDACTED] |
| Loan amount | Mortgage balance | [LOAN AMOUNT REDACTED] |
| Credit score | 742 | [CREDIT SCORE REDACTED] |
| Net worth | $1.2M | [NET WORTH REDACTED] |
| Cryptocurrency wallet | 1A1zP1eP5QGefi2DMPTfTL... | [WALLET ADDRESS REDACTED] |

### Category 3 — Sensitive / Protected Categories

| Data Type | Replacement Token |
|---|---|
| Minor's full name | [MINOR'S NAME REDACTED] |
| Victim name (crime, abuse, trafficking) | [VICTIM NAME REDACTED] |
| Survivor / complainant name (HR/legal) | [COMPLAINANT REDACTED] |
| Medical diagnosis / condition | [MEDICAL INFORMATION REDACTED] |
| HIV / AIDS status | [HEALTH STATUS REDACTED] |
| Mental health diagnosis | [MENTAL HEALTH INFORMATION REDACTED] |
| Substance use history | [SUBSTANCE HISTORY REDACTED] |
| Sexual orientation / gender identity (self-identified in document) | [PERSONAL INFORMATION REDACTED] |
| Pregnancy / reproductive health | [HEALTH INFORMATION REDACTED] |
| Immigration status / visa details | [IMMIGRATION STATUS REDACTED] |
| Religion / faith details (if sensitive context) | [RELIGIOUS INFORMATION REDACTED] |
| Racial / ethnic origin in sensitive context | [DEMOGRAPHIC INFORMATION REDACTED] |
| Attorney–client privilege marker | [PRIVILEGED — REDACTED] |
| Work product doctrine marker | [WORK PRODUCT — REDACTED] |
| Trade secret / proprietary formula | [PROPRIETARY INFORMATION REDACTED] |
| National security / classified material | [CLASSIFIED — REDACTED] |
| Whistleblower identity | [PROTECTED IDENTITY REDACTED] |

---

## Step 4 — What NOT to Redact (Context Rules)

| Element | Rule |
|---|---|
| Party names in a contract | Keep — these are the principal parties |
| Company names | Keep — business entities are not personal data unless the business is the person (sole trader) |
| Public figures' names in their official capacity | Keep — public role is not private data |
| Author / attorney of record | Keep — professional identity in professional context |
| Dates that are not DOBs | Keep — contract dates, court dates, invoice dates are not personal |
| Generic addresses (court address, company HQ) | Keep — public record |
| Job titles (without linked personal data) | Keep |
| Professional certifications / qualifications | Keep |

---

## Step 5 — Run Script Redaction

Run from the directory where `skills/` is installed (your project root).

### 5a — Read the document first

Before running the script, use the `Read` tool to extract the document's full text. Identify:
- Names in ALL-CAPS (e.g. `SMITH JOHN`) — the engine requires mixed case unless the name follows a keyword label
- Names that appear far from their label in the PDF text extraction order (labels and values on different lines or columns may not be adjacent in extraction)
- Document-specific identifiers: serial numbers, reference codes, custom ID formats
- Any PII not matching standard patterns (e.g. foreign-language names, non-standard ID formats)

These will need `--custom` patterns in step 5c.

### 5b — Dry run (preview, no file written)

```bash
python skills/doc-process/scripts/redactor.py --file document.pdf --mode standard --dry-run
```

Review the printed summary. Note any PII that was NOT detected.

### 5c — Full redaction with custom patterns for gaps

```bash
# PDF — black bars drawn over PII on a copy; original never modified
python skills/doc-process/scripts/redactor.py \
  --file document.pdf \
  --output document_redacted.pdf \
  --mode standard \
  --custom "SMITH\s+JOHN" \
  --custom "REF-[A-Z0-9]+" \
  --log

# Text file — token replacement (e.g. [SSN REDACTED])
python skills/doc-process/scripts/redactor.py \
  --file document.txt --output document_redacted.txt --mode standard --log

# Image — OCR-based detection, black bars painted on a copy
# Requires: pip install Pillow pytesseract && brew install tesseract
python skills/doc-process/scripts/redactor.py \
  --file scan.png --output scan_redacted.png --mode full --log
```

`--custom` is repeatable. Each takes a Python regex. Use it for every gap identified in step 5a. For ALL-CAPS names use `\bFIRSTNAME\s+LASTNAME\b`; for reference codes use `\bPREFIX-[A-Z0-9]+\b`.

### 5d — Verify the output

After redaction, re-extract the text from the output file and confirm the PII is gone:

```bash
# Quick check: search the redacted PDF for any remaining sensitive values
python -c "
import fitz
doc = fitz.open('document_redacted.pdf')
text = '\n'.join(p.get_text() for p in doc)
print(text)
"
```

If any PII is still present in the extracted text, add a `--custom` pattern for it and re-run on the original file (not the already-redacted copy).

**How PDF redaction works:** word bounding boxes are extracted from the PDF layout engine; matched PII spans are covered with solid-black PyMuPDF redaction annotations; `apply_redactions()` burns the fills in and removes the underlying text data — redacted content cannot be copy-pasted or extracted. The file is saved incrementally so every non-redacted element (fonts, images, vector graphics, metadata) is left completely untouched. The original file is never modified.

**Requires:** `pip install pymupdf>=1.23` for PDF; `pip install Pillow>=10.0 pytesseract>=0.3` + `brew install tesseract` for image mode.

For images without OCR support: visually describe which areas to black out and apply manually.

---

## Step 6 — Visual Review Checklist

After script processing, manually scan for:

- [ ] Names in non-standard formats (initials only, nicknames, first-name-only references)
- [ ] Phone numbers in prose: "call me at five five five, oh one two three"
- [ ] Account numbers written as words: "account ending forty-two thirty"
- [ ] Addresses embedded mid-sentence: "at her home in [address]"
- [ ] Relative date references that imply DOB: "on her 40th birthday" with date nearby
- [ ] Social media handles if they could identify the person
- [ ] Medical conditions mentioned colloquially: "her cancer", "his diabetes"
- [ ] Foreign-language PII not caught by English patterns
- [ ] Numbers that look like financial data but lack keywords (regex may miss these)
- [ ] Handwritten text that was OCR'd with errors (partial catch)

---

## Step 7 — Output Report

### Redaction Summary
| Category | Items Redacted | Data Types Removed |
|---|---|---|
| Category 1 — Personal Identifiers | N | Names, phone, email, addresses |
| Category 2 — Financial Data | N | Account numbers, salary figures |
| Category 3 — Sensitive/Protected | N | Medical diagnoses, privilege markers |
| Custom Patterns | N | [User-specified terms] |
| **Total** | **N** | |

### Redaction Log (first 15 items)
| Line | Rule Triggered | Preview | Replacement |
|---|---|---|---|
| 12 | SSN | 12X-XX-X789 | [SSN REDACTED] |
| 34 | Email | jo…om | [EMAIL REDACTED] |

### Redacted Document
Full redacted content displayed in a code block, or saved to file.

---

## Step 8 — Residual Risk Assessment

After redaction, assess the residual re-identification risk:

| Risk Factor | Present? | Notes |
|---|---|---|
| Quasi-identifiers remaining | Yes / No | Age + zip + sex can re-identify 87% of US individuals |
| Unique combination of retained attributes | Yes / No | Rare combination of role + company + location |
| Small dataset | Yes / No | If only 5 people could match, single identifier enough |
| Public record cross-reference risk | Yes / No | Information matchable against public databases |

If quasi-identifiers remain, suggest: "Consider also redacting [age/zip/specific role] to prevent re-identification by combining with public records."

---

## Step 9 — Save Options

Ask: "Would you like me to save the redacted document?"

Output path is auto-named `<original_name>_redacted.<ext>` unless `--output` is specified:
- PDF: `<original_name>_redacted.pdf`
- Text: `<original_name>_redacted.txt`
- Image: `<original_name>_redacted.png` / `.jpg`

The redaction log (printed to stderr with `--log`) can be saved separately if needed.

---

## General Rules
- Truncate sensitive values to first 2 + last 2 characters max in the redaction log — never display the full value.
- Preserve document structure, formatting, paragraph breaks, and numbering exactly.
- Party names in legal documents are NOT redacted by default — confirm with user if they want them removed.
- Never guess at partially obscured values — mark as `[UNREADABLE — possible sensitive data]`.
- In the redacted output, use consistent replacement tokens — don't use `[REDACTED]` generically; use specific tokens so readers know what type of data was removed.

## Action Prompt
End with: "Would you like me to:
- Change the redaction mode (light/standard/full)?
- Add custom terms or patterns to redact?
- Assess re-identification risk from remaining attributes?
- Save the redacted file to disk?"
