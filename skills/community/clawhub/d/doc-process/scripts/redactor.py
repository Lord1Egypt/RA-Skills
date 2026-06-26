#!/usr/bin/env python3
"""
redactor.py — PII redaction that preserves the original file format.

Output is always a **copy** of the input.  The original file is never modified.

PDF mode  — black bars are drawn directly on a copy of the original PDF.
  Word bounding boxes are extracted from the PDF layout engine, matched PII
  spans are covered with solid-black PyMuPDF redaction annotations, the
  underlying text data is removed, and the file is saved incrementally so
  every non-redacted element (fonts, images, vector graphics, metadata) is
  preserved exactly.  Requires: pymupdf>=1.23

Image mode — OCR detects PII, black bars are painted on a copy with Pillow.
  Requires: Pillow>=10.0, pytesseract>=0.3, tesseract binary.

Text mode — regex token replacement in a copy of the file.  Pure stdlib.

Modes:
  light     Category 1 only (personal identifiers)
  standard  Category 1 + 2  (personal + financial)  [default]
  full      Category 1 + 2 + 3 (all sensitive data)

Usage:
  python redactor.py --file report.pdf
  python redactor.py --file scan.png   --mode full
  python redactor.py --file notes.txt  --output notes_redacted.txt
  python redactor.py --file report.pdf --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from dataclasses import dataclass, field

# ═══════════════════════════════════════════════════════════════════════════
# Pattern definitions
# ═══════════════════════════════════════════════════════════════════════════

_PDF_EXTS = {".pdf"}
_IMG_EXTS = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}


@dataclass
class RedactionRule:
    name: str
    pattern: str
    replacement: str       # text-mode token (may use \\g<1> backrefs)
    category: int          # 1 | 2 | 3
    flags: int = re.IGNORECASE
    priority: int = 100    # lower wins on ties
    value_group: int = 0   # 0 = full match; N = group N is the sensitive value


# ── Category 1 — Personal Identifiers ────────────────────────────────────

# Comprehensive keyword list for labeled personal name fields — covers invoice,
# contract, legal, HR, healthcare, financial, and government document types.
_NAME_KW = (
    r"(?:"
    # Invoice / shipping
    r"bill(?:ed)?\s+to|ship(?:ped)?\s+to|shipper|consignee"
    # Correspondence
    r"|attention|attn|dear\s+(?:mr\.?|mrs\.?|ms\.?|dr\.?)?"
    # Contract parties (ordinal, alphabetic, generic)
    r"|(?:first|second|third|1st|2nd|3rd)\s+party"
    r"|party\s+[a-z0-9]{1,2}|party\s+(?:a|b|c|one|two|three)"
    r"|buyer|seller|vendor|purchaser|transferor|transferee"
    r"|grantor|grantee|lessor|lessee|tenant|landlord"
    r"|borrower|lender|mortgagor|mortgagee|pledgor|pledgee"
    r"|assignor|assignee|licensor|licensee|franchisor|franchisee"
    r"|licencee"
    # Legal proceedings
    r"|plaintiff|defendant|claimant|respondent|petitioner|appellant|appellee"
    r"|complainant|accused|witness|deponent|declarant|affiant"
    r"|executor|administrator|trustee|settlor"
    r"|notarized\s+by|attested\s+by|acknowledged\s+by"
    # Corporate / company roles
    r"|(?:authorized|authorised)\s+(?:signatory|representative|person)"
    r"|signed\s+by|executed\s+by|prepared\s+by|submitted\s+by"
    r"|reviewed\s+by|approved\s+by|issued\s+to|issued\s+by"
    r"|guarantor|indemnitor|surety|co-?signer"
    r"|director|officer|secretary|treasurer|president|chairman|chairperson"
    r"|partner|member|shareholder|stockholder|subscriber|investor|depositor"
    # Employment / HR
    r"|employee|employer|worker|staff(?:\s+member)?|candidate|applicant"
    r"|hire(?:e|d\s+by)?|recruiter"
    # Healthcare
    r"|patient|insured(?:\s+person)?|policyholder|named\s+insured"
    r"|subscriber(?:\s+name)?|member(?:\s+name)?"
    # Financial / payment
    r"|payable\s+to|pay\s+to|payee|payer|remit(?:tance)?\s+to"
    r"|beneficiary(?:\s+name)?|account\s+(?:holder|owner|name)"
    r"|client|customer"
    # Generic labeled name fields
    r"|(?:full|legal|given|first|last|middle|preferred)\s+name"
    r"|patient\s+name|member\s+name|insured\s+name|employee\s+name"
    r"|policyholder\s+name|account\s+holder\s+name"
    r"|representative(?:\s+name)?|agent(?:\s+name)?"
    r")"
)

_CAT1 = [
    # ── Government / national IDs ──────────────────────────────────────────
    RedactionRule("SSN",  r"\b\d{3}[-\s]\d{2}[-\s]\d{4}\b", "[SSN REDACTED]", 1),
    RedactionRule("SIN",  r"\b\d{3}-\d{3}-\d{3}\b",         "[SIN REDACTED]", 1),
    # UK National Insurance Number: two letters, 6 digits, one suffix letter
    RedactionRule(
        "UK NIN",
        r"((?:national\s+insurance|NIN|NINO)\s*(?:no\.?|number|#)?\s*:?\s*)"
        r"([A-CEGHJ-PR-TW-Z]{1}[A-CEGHJ-NPR-TW-Z]{1}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D])\b",
        r"\g<1>[NIN REDACTED]", 1, value_group=2,
    ),
    # Australian Tax File Number
    RedactionRule(
        "Australian TFN",
        r"((?:TFN|tax\s+file\s+(?:number|no))\s*:?\s*)(\d{3}\s?\d{3}\s?\d{3})\b",
        r"\g<1>[TFN REDACTED]", 1, value_group=2,
    ),
    # Australian Medicare number
    RedactionRule(
        "Medicare number",
        r"(medicare\s*(?:no\.?|number|card)?\s*:?\s*)(\d{4}\s?\d{5}\s?\d{1}(?:\s?-\s?\d)?)\b",
        r"\g<1>[MEDICARE NUMBER REDACTED]", 1, value_group=2,
    ),
    # Indian Aadhaar: 12-digit number in groups of 4
    RedactionRule(
        "Aadhaar",
        r"((?:aadhaar|aadhar|uid|uidai)\s*(?:no\.?|number|#)?\s*:?\s*)"
        r"(\d{4}\s?\d{4}\s?\d{4})\b",
        r"\g<1>[AADHAAR REDACTED]", 1, value_group=2,
    ),
    RedactionRule("Passport", r"\b[A-Z]{1,2}\d{6,9}\b", "[PASSPORT NUMBER REDACTED]", 1),
    RedactionRule(
        "DL keyword",
        r"(driver'?s?\s+licen[sc]e\s*(?:no\.?|number|#)?\s*:?\s*)([A-Z0-9-]{5,15})",
        r"\g<1>[LICENSE NUMBER REDACTED]", 1, value_group=2,
    ),
    # UK NHS number: 10 digits, shown as three groups
    RedactionRule(
        "UK NHS number",
        r"(NHS\s*(?:no\.?|number)?\s*:?\s*)(\d{3}\s\d{3}\s\d{4}|\d{10})\b",
        r"\g<1>[NHS NUMBER REDACTED]", 1, value_group=2,
    ),
    # Generic national / government ID (keyword-anchored to avoid false positives)
    RedactionRule(
        "National ID keyword",
        r"((?:national\s+(?:id|identity|identification)|citizen\s+id|govt\.?\s+id|government\s+id)"
        r"\s*(?:no\.?|number|card)?\s*:?\s*)([A-Z0-9\-]{6,20})\b",
        r"\g<1>[NATIONAL ID REDACTED]", 1, value_group=2,
    ),
    # Voter / election ID (keyword-anchored)
    RedactionRule(
        "Voter ID keyword",
        r"((?:voter|election|electoral)\s*(?:id|identification|registration|card)"
        r"\s*(?:no\.?|number)?\s*:?\s*)([A-Z0-9\-]{5,20})\b",
        r"\g<1>[VOTER ID REDACTED]", 1, value_group=2,
    ),
    RedactionRule("NRIC", r"\b[STFGM]\d{7}[A-Z]\b", "[NRIC REDACTED]", 1),
    # Indian PAN number: AAAAA9999A
    RedactionRule(
        "PAN number",
        r"(PAN\s*(?:no\.?|number|#)?\s*:?\s*)([A-Z]{5}\d{4}[A-Z])\b",
        r"\g<1>[PAN NUMBER REDACTED]", 1, value_group=2,
    ),
    # MRN / medical record
    RedactionRule(
        "MRN keyword",
        r"((?:mrn|medical\s+record\s+(?:no\.?|number|#)|patient\s+id)\s*:?\s*)([A-Z0-9\-]{4,15})",
        r"\g<1>[MEDICAL ID REDACTED]", 1, value_group=2,
    ),
    # Vehicle Identification Number (keyword-anchored — avoids matching random 17-char strings)
    RedactionRule(
        "VIN keyword",
        r"((?:VIN|vehicle\s+identification(?:\s+number)?)\s*:?\s*)([A-HJ-NPR-Z0-9]{17})\b",
        r"\g<1>[VIN REDACTED]", 1, value_group=2,
    ),

    # ── Contact information ────────────────────────────────────────────────
    RedactionRule("Email", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b", "[EMAIL REDACTED]", 1),
    # Phone: separators restricted to space/tab/hyphen/dot (no newline) to prevent
    # cross-line matches.  Lookbehinds block matching from inside date strings
    # and from alphanumeric reference codes (e.g. "DOC-2024-001").
    # Lookahead blocks matching at DD-MM-YYYY boundary.  Up to 8 trailing digits
    # covers long international numbers (Indian STD format, etc.).
    RedactionRule(
        "Phone",
        r"(?<!\d)(?<!\d-)(?<!\d\.)(?<!\d/)(?<![A-Za-z]-)"
        r"(?!\d{1,2}[-./]\d{1,2}[-./]\d{4}(?!\d))"
        r"(\+?\d{1,3}[\ \t\-.])?(\(?\d{2,4}\)?[\ \t\-.]){1,3}\d{3,8}(?!\d)",
        "[PHONE REDACTED]", 1,
    ),

    # ── Location / address ─────────────────────────────────────────────────
    # Street address: covers US, UK, AU, IN, SG street-type abbreviations.
    # Optional BLK/BLOCK/FLAT/UNIT/APT prefix handles Singapore HDB addresses
    # ("BLK 101 Dalvey Road") and apartment-style addresses.
    RedactionRule(
        "Street address",
        r"(?:(?:BLK|BLOCK|Blk|Block|FLAT|UNIT|APT|APARTMENT|SUITE|LOT)\s+)?"
        r"\b\d{1,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\s+"
        r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln"
        r"|Court|Ct|Way|Place|Pl|Terrace|Ter|Hill|Hl|Hills|Hls|Circle|Cir"
        r"|Parkway|Pkwy|Trail|Trl|Highway|Hwy|Crescent|Cres|Close|Walk"
        r"|Row|Quay|Grove|Park|View|Ridge|Square|Sq|Gardens|Gdns|Mount|Mt"
        r"|Broadway|Expressway|Bypass|Loop|Pass)\b\.?",
        "[ADDRESS REDACTED]", 1,
    ),
    # Apartment / unit number: #02-01, #12-345, Unit 3B, Apt 4C, etc.
    RedactionRule(
        "Unit number",
        r"(?:#\d{2,3}-\d{2,4}|\b(?:Unit|Apt|Apartment|Suite|Flat|Room|Level)\s+[A-Z0-9\-]+)\b",
        "[UNIT NUMBER REDACTED]", 1,
    ),
    # P.O. Box: "PO Box 1234", "P.O. Box 45"
    RedactionRule("PO Box", r"\bP\.?\s*O\.?\s*Box\s+\d+\b", "[PO BOX REDACTED]", 1),
    # US ZIP and ZIP+4
    RedactionRule("ZIP code",  r"\b\d{5}(?:-\d{4})?\b",         "[POSTAL CODE REDACTED]", 1),
    # Canadian postal code: A1A 1A1
    RedactionRule("CA postal", r"\b[A-Z]\d[A-Z]\s?\d[A-Z]\d\b", "[POSTAL CODE REDACTED]", 1),
    # UK postcode: SW1A 2AA, EC1A 1BB, M1 1AE, etc.
    RedactionRule(
        "UK postcode",
        r"\b[A-Z]{1,2}\d[A-Z0-9]?\s*\d[A-Z]{2}\b",
        "[POSTAL CODE REDACTED]", 1,
    ),
    # International 6-digit postal codes (SG, IN) when following a letter+space
    RedactionRule("Intl postal", r"(?<=[A-Za-z] )\d{6}\b", "[POSTAL CODE REDACTED]", 1),
    # IPv4 address: strict octet validation (0-255 each)
    RedactionRule(
        "IPv4 address",
        r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
        "[IP ADDRESS REDACTED]", 1,
    ),
    # MAC address: hardware identifier in colon or hyphen notation
    RedactionRule(
        "MAC address",
        r"\b(?:[0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}\b",
        "[DEVICE ID REDACTED]", 1,
    ),

    # ── Date / demographics ────────────────────────────────────────────────
    # DOB with common label prefixes
    RedactionRule(
        "DOB keyword",
        r"((?:d\.?o\.?b\.?|date\s+of\s+birth|birth\s+date|born(?:\s+on)?)"
        r"\s*:?\s*)(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}|\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}"
        r"|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
        r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
        r"\s+\d{1,2},?\s+\d{4})",
        r"\g<1>[DATE OF BIRTH REDACTED]", 1, value_group=2,
    ),
    # Age when labeled ("Age: 34", "Age : 34 years")
    RedactionRule(
        "Age keyword",
        r"((?:\bage\b|aged)\s*:?\s*)(\d{1,3})(?:\s*(?:years?|yrs?\.?))?\b",
        r"\g<1>[AGE REDACTED]", 1, value_group=2,
    ),

    # ── Name detection ─────────────────────────────────────────────────────
    # Keyword-anchored name: covers the broad set of document label types above.
    # Preserves the keyword label; redacts the 2+ word name that follows.
    RedactionRule(
        "Labeled name",
        rf"({_NAME_KW}\s*:?\s*(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?|Mx\.?)?\s*)"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        r"\g<1>[NAME REDACTED]", 1, value_group=2,
    ),
    # Honorific + name: "Mr. John Smith" → "Mr. [NAME REDACTED]"
    RedactionRule(
        "Title prefix name",
        r"\b(Mr\.?|Mrs\.?|Ms\.?|Miss\.?|Dr\.?|Prof\.?|Rev\.?|Hon\.?|Mx\.?)\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b",
        r"\g<1> [NAME REDACTED]", 1, value_group=2,
    ),
]

# ── Category 2 — Financial Data ──────────────────────────────────────────

# ISO 3166-1 alpha-2 country codes that issue IBANs — prevents matching
# invoice numbers, reference IDs, and other alphanumeric codes that start
# with two letters but are not real IBANs.
_IBAN_CC = (
    r"(?:AD|AE|AL|AT|AZ|BA|BE|BG|BH|BR|BY|CH|CR|CY|CZ|DE|DK|DO|EE|EG|ES"
    r"|FI|FO|FR|GB|GE|GI|GL|GR|GT|HR|HU|IE|IL|IQ|IS|IT|JO|KW|KZ|LB|LC"
    r"|LI|LK|LT|LU|LV|MC|MD|ME|MK|MR|MT|MU|MX|NO|NL|PK|PL|PS|PT|QA|RO"
    r"|RS|SA|SC|SD|SE|SI|SK|SM|ST|SV|TL|TN|TR|UA|VA|VG|XK)"
)

_CAT2 = [
    # ── Card / account numbers ─────────────────────────────────────────────
    RedactionRule("Card number", r"\b(?:\d{4}[\s\-]?){3}\d{1,4}\b", "[CARD NUMBER REDACTED]", 2, priority=10),
    # Card CVV / security code (keyword-anchored — 3-4 digits is too common standalone)
    RedactionRule(
        "Card CVV",
        r"(cvv|cvc|cvv2|cvc2|security\s+code|card\s+security)\s*:?\s*(\d{3,4})\b",
        r"\g<1>[CVV REDACTED]", 2, value_group=2,
    ),
    # Card expiry: MM/YY or MM/YYYY.
    # Lookbehind (?<!\d/) prevents matching the middle segment of DD/MM/YYYY
    # transaction dates (e.g. "05/12" in "05/12/2025").
    # Negative lookahead (?!/) prevents matching when followed by another /
    # (which means it is part of a full date, not a standalone expiry).
    RedactionRule(
        "Card expiry",
        r"(?<!\d/)\b(0[1-9]|1[0-2])\s?/\s?(\d{4}|\d{2}(?!/))\b",
        "[CARD EXPIRY REDACTED]", 2,
    ),
    RedactionRule(
        "Account keyword",
        r"(account\s*(?:no\.?|number|#|num)\s*:?\s*)(\d[\d\s\-]{6,18}\d)",
        r"\g<1>[ACCOUNT NUMBER REDACTED]", 2, value_group=2,
    ),
    # IBAN: country-code-restricted to avoid false positives on invoice/reference numbers.
    RedactionRule("IBAN", rf"\b{_IBAN_CC}\d{{2}}[A-Z0-9]{{11,30}}\b", "[IBAN REDACTED]", 2),
    # ABA / routing number: matches "routing No.", "ABA No.", "ABA routing", etc.
    RedactionRule(
        "ABA routing",
        r"((?:aba|routing)\s*(?:no\.?|number|routing|#)?\s*:?\s*)(\d{9})\b",
        r"\g<1>[ROUTING NUMBER REDACTED]", 2, value_group=2,
    ),
    # UK Sort Code: 6 digits in XX-XX-XX or XX XX XX format
    RedactionRule(
        "UK Sort code",
        r"(sort\s*(?:code|no\.?)?\s*:?\s*)(\d{2}[-\s]\d{2}[-\s]\d{2})\b",
        r"\g<1>[SORT CODE REDACTED]", 2, value_group=2,
    ),
    # Australian BSB number
    RedactionRule(
        "Australian BSB",
        r"(BSB\s*(?:no\.?|number)?\s*:?\s*)(\d{3}[-\s]\d{3})\b",
        r"\g<1>[BSB REDACTED]", 2, value_group=2,
    ),
    # Indian IFSC code: 4 alpha + 0 + 6 alphanumeric (keyword preferred, standalone allowed)
    RedactionRule(
        "IFSC code",
        r"(IFSC\s*(?:code|no\.?)?\s*:?\s*)?([A-Z]{4}0[A-Z0-9]{6})\b",
        r"\g<1>[IFSC CODE REDACTED]", 2, value_group=2,
    ),
    # SWIFT / BIC: allows optional space within the code (e.g. "CHAS US33")
    RedactionRule(
        "SWIFT",
        r"((?:swift|bic)\s*(?:code)?\s*:?\s*)([A-Z]{4}\s?[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?)\b",
        r"\g<1>[SWIFT REDACTED]", 2, value_group=2,
    ),
    # Compensation / salary figures
    RedactionRule(
        "Salary keyword",
        r"((?:salary|compensation|annual\s+(?:pay|income|compensation)|base\s+pay|gross\s+(?:salary|pay)"
        r"|net\s+(?:salary|pay)|take[\-\s]home|ctc|cost\s+to\s+company|remuneration|stipend|wage)\s*:?\s*"
        r"[\$£€¥₹]?\s*)(\d[\d,\.]+)",
        r"\g<1>[COMPENSATION REDACTED]", 2, value_group=2,
    ),
    # Credit score (keyword-anchored — 3-digit numbers are too common standalone)
    RedactionRule(
        "Credit score",
        r"(credit\s+(?:score|rating|report\s+score)\s*:?\s*)(\d{3,4})\b",
        r"\g<1>[CREDIT SCORE REDACTED]", 2, value_group=2,
    ),
    # Loan / mortgage balance
    RedactionRule(
        "Loan amount",
        r"((?:loan|mortgage|outstanding\s+balance|principal\s+(?:balance|amount)|credit\s+limit|credit\s+line)"
        r"\s*(?:amount|balance|value)?\s*:?\s*[\$£€¥₹]?\s*)(\d[\d,\.]+)",
        r"\g<1>[LOAN AMOUNT REDACTED]", 2, value_group=2,
    ),
    # Tax return financial figures
    RedactionRule(
        "Tax figure",
        r"((?:adjusted\s+gross\s+income|AGI|taxable\s+income|total\s+income|gross\s+income"
        r"|net\s+income|income\s+tax(?:\s+paid)?|tax\s+(?:liability|due|refund|paid))\s*:?\s*"
        r"[\$£€¥₹]?\s*)(\d[\d,\.]+)",
        r"\g<1>[TAX FIGURE REDACTED]", 2, value_group=2,
    ),
    # Net worth / total assets
    RedactionRule(
        "Net worth",
        r"((?:net\s+worth|total\s+(?:assets|wealth|holdings)|portfolio\s+value"
        r"|investment\s+value)\s*:?\s*[\$£€¥₹]?\s*)(\d[\d,\.]+)",
        r"\g<1>[NET WORTH REDACTED]", 2, value_group=2,
    ),
    # Cryptocurrency wallet address (Bitcoin, Ethereum, etc.)
    RedactionRule(
        "Crypto wallet",
        r"\b(?:1[A-HJ-NP-Za-km-z1-9]{25,34}|3[A-HJ-NP-Za-km-z1-9]{33}|bc1[ac-hj-np-z02-9]{39,59}"
        r"|0x[0-9a-fA-F]{40})\b",
        "[WALLET ADDRESS REDACTED]", 2,
    ),
]

# ── Category 3 — Legal / Health / Highly Sensitive ────────────────────────

_CAT3 = [
    # ── Health information ─────────────────────────────────────────────────
    RedactionRule("HIV status",
        r"\b(HIV[\-\s]?(?:positive|negative|status)|AIDS\s+(?:diagnosis|status))\b",
        "[HEALTH STATUS REDACTED]", 3),
    # Blood type / group (keyword-anchored)
    RedactionRule(
        "Blood type",
        r"(blood\s+(?:type|group)\s*:?\s*)(A[+-]|B[+-]|AB[+-]|O[+-]"
        r"|A\s+(?:positive|negative)|B\s+(?:positive|negative)"
        r"|AB\s+(?:positive|negative)|O\s+(?:positive|negative))\b",
        r"\g<1>[BLOOD TYPE REDACTED]", 3, value_group=2,
    ),
    # Mental health diagnoses
    RedactionRule(
        "Mental health",
        r"\b(depression|major\s+depressive\s+disorder|anxiety\s+disorder|generalized\s+anxiety"
        r"|bipolar(?:\s+disorder)?|schizophrenia|PTSD|post[\-\s]traumatic\s+stress"
        r"|borderline\s+personality|OCD|obsessive[\-\s]compulsive|eating\s+disorder"
        r"|anorexia|bulimia|ADHD|attention\s+deficit|autism\s+spectrum|ASD"
        r"|panic\s+disorder|social\s+anxiety|phobia)\b",
        "[MENTAL HEALTH INFORMATION REDACTED]", 3),
    # Reproductive / pregnancy
    RedactionRule(
        "Reproductive health",
        r"\b(pregnan(?:t|cy)|maternity|prenatal|postnatal|postpartum|miscarriage"
        r"|abortion|termination\s+of\s+pregnancy|fertility\s+treatment|IVF"
        r"|in\s+vitro\s+fertilization|surrogacy|menopause|menstrual\s+disorder)\b",
        "[HEALTH INFORMATION REDACTED]", 3),
    # Substance use history
    RedactionRule(
        "Substance use",
        r"\b(substance\s+(?:abuse|use\s+disorder)|drug\s+(?:abuse|addiction|dependency)"
        r"|alcohol\s+(?:abuse|dependency|use\s+disorder)|opioid\s+(?:abuse|dependency)"
        r"|heroin|cocaine|methamphetamine|naloxone|methadone\s+treatment"
        r"|rehab(?:ilitation)?\s+(?:for|program))\b",
        "[SUBSTANCE HISTORY REDACTED]", 3),
    # Sexual orientation / gender identity
    RedactionRule(
        "Sexual orientation",
        r"\b(gay|lesbian|bisexual|homosexual|heterosexual|queer|LGBTQ\+?"
        r"|transgender|transsexual|non[\-\s]binary|gender[\-\s](?:fluid|queer|nonconforming)"
        r"|intersex)\b",
        "[PERSONAL INFORMATION REDACTED]", 3),
    # Disability / impairment (keyword-anchored to prevent common word false positives)
    RedactionRule(
        "Disability",
        r"(disability|impairment|handicap|differently[\-\s]abled)\s*:?\s*"
        r"([A-Za-z][a-z]+(?:\s+[a-z]+){0,6})",
        "[DISABILITY INFORMATION REDACTED]", 3),
    # Criminal / arrest record
    RedactionRule(
        "Criminal record",
        r"\b(arrest(?:ed|ed\s+for)?|convicted\s+of|prior\s+conviction|criminal\s+(?:record|history"
        r"|background)|felony\s+(?:charge|conviction)|misdemeanor\s+(?:charge|conviction)"
        r"|sex\s+offender|parole|probation\s+record)\b",
        "[CRIMINAL RECORD REDACTED]", 3),
    # Genetic information
    RedactionRule(
        "Genetic info",
        r"\b(genetic\s+(?:test(?:ing)?|data|information|mutation|profile|marker)"
        r"|BRCA[\-\s]?\d|DNA\s+(?:test|profile|sample|sequence)|genomic\s+data"
        r"|hereditary\s+(?:condition|mutation|risk))\b",
        "[GENETIC INFORMATION REDACTED]", 3),
    # Immigration status
    RedactionRule(
        "Immigration",
        r"\b(undocumented|illegal\s+alien|visa\s+overstay|deportation\s+order"
        r"|asylum\s+seeker|refugee\s+status|illegal\s+immigrant"
        r"|unauthorized\s+(?:immigrant|alien|worker))\b",
        "[IMMIGRATION STATUS REDACTED]", 3),
    # Minor's name
    RedactionRule(
        "Minor name",
        r"((?:minor|juvenile|child)\s+(?:named?|called)?\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
        r"\g<1>[MINOR'S NAME REDACTED]", 3, value_group=2,
    ),
    # Legal privilege markers
    RedactionRule(
        "Privilege",
        r"(attorney[\-\s]client\s+privilege|privileged\s+and\s+confidential"
        r"|work\s+product\s+doctrine|without\s+prejudice|under\s+seal)",
        "[PRIVILEGED — REDACTED]", 3),
    # Trade secret / proprietary
    RedactionRule(
        "Trade secret",
        r"\b(trade\s+secret|proprietary\s+(?:formula|algorithm|process|method)"
        r"|confidential\s+business\s+information|classified\s+information"
        r"|national\s+security\s+information)\b",
        "[PROPRIETARY INFORMATION REDACTED]", 3),
]

ALL_RULES = _CAT1 + _CAT2 + _CAT3


def _rules_for_mode(mode: str) -> list[RedactionRule]:
    if mode == "light":
        return list(_CAT1)
    if mode == "full":
        return list(ALL_RULES)
    return list(_CAT1) + list(_CAT2)   # standard


# ═══════════════════════════════════════════════════════════════════════════
# Detection engine  (shared across all file types)
# ═══════════════════════════════════════════════════════════════════════════

def _compile_rules(mode: str, custom_patterns: list[str] | None = None):
    rules = _rules_for_mode(mode)
    if custom_patterns:
        for i, p in enumerate(custom_patterns):
            rules.append(RedactionRule(f"Custom-{i+1}", p, "[CUSTOM REDACTED]", 0))
    out = []
    for r in rules:
        try:
            out.append((re.compile(r.pattern, r.flags), r))
        except re.error as e:
            print(f"Warning: invalid regex for '{r.name}': {e}", file=sys.stderr)
    return out


def _detect(text, compiled_rules):
    """Return non-overlapping matches sorted by position (longest / highest-priority wins ties)."""
    cands = []
    for pat, rule in compiled_rules:
        for m in pat.finditer(text):
            cands.append((m.start(), m.end(), m, rule))
    cands.sort(key=lambda x: (x[0], -(x[1] - x[0]), x[3].priority))
    sel, pos = [], 0
    for s, e, m, r in cands:
        if s >= pos:
            sel.append((s, e, m, r))
            pos = e
    return sel


def _sensitive_span(m, rule):
    """Return (start, end) of the portion to black-out.  For keyword rules this
    is group N (the value), not the label."""
    g = rule.value_group
    if g and g <= len(m.groups()):
        return m.start(g), m.end(g)
    return m.start(), m.end()


def _preview(m):
    s = m.group(0)
    return (s[:2] + "…" + s[-2:]) if len(s) > 6 else "…"


# ═══════════════════════════════════════════════════════════════════════════
# Result
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class RedactionResult:
    output_path: Path | None = None
    log: list[dict] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    fmt: str = "text"          # "text" | "pdf" | "image"
    redacted_text: str = ""    # only populated for text-mode output


# ═══════════════════════════════════════════════════════════════════════════
# PDF redaction — black bars on a copy  (requires PyMuPDF)
# ═══════════════════════════════════════════════════════════════════════════

def _redact_pdf(input_path, output_path, compiled_rules):
    """Redact PII in a PDF while preserving the original exactly.

    Strategy:
    1. Copy the original file byte-for-byte to output_path.
    2. For each page, extract word bounding boxes from the PDF layout engine
       (no search_for — direct bbox mapping avoids false misses).
    3. Build a position-tracked text string and run PII detection on it.
    4. For each hit, merge the overlapping word rects into one bounding rect
       and add a PyMuPDF redaction annotation (solid black fill).
    5. apply_redactions() burns the black fills in and removes the underlying
       text data from the content stream — redacted text cannot be copy-pasted.
    6. Save incrementally so every non-redacted element (fonts, images, vector
       graphics, metadata) is left completely untouched.
    """
    import fitz

    _PAD = 1   # pt of padding added around each merged word rect

    shutil.copy2(input_path, output_path)
    doc = fitz.open(str(output_path))
    log, counts = [], {}

    for page_idx in range(len(doc)):
        page = doc[page_idx]

        # ── 1. Build position-tracked text from word bboxes ────────────
        words = page.get_text("words")  # (x0, y0, x1, y1, word, blk, ln, wn)
        parts, spans, cp = [], [], 0
        for w in words:
            txt = w[4]
            spans.append((cp, cp + len(txt), fitz.Rect(w[0], w[1], w[2], w[3])))
            parts.append(txt)
            cp += len(txt) + 1
        full_text = " ".join(parts)

        # ── 2. Detect PII ──────────────────────────────────────────────
        hits = _detect(full_text, compiled_rules)
        if not hits:
            continue

        # ── 3. Map each match → merged word rect → redaction annotation ─
        for _, _, m, rule in hits:
            gs, ge = _sensitive_span(m, rule)
            rects = [r for cs, ce, r in spans if cs < ge and ce > gs]
            if not rects:
                continue

            merged = fitz.Rect()
            for r in rects:
                merged |= r
            merged.x0 -= _PAD
            merged.y0 -= _PAD
            merged.x1 += _PAD
            merged.y1 += _PAD

            page.add_redact_annot(merged, fill=(0, 0, 0))

            log.append({"page": page_idx + 1, "rule": rule.name,
                        "category": rule.category, "preview": _preview(m)})
            counts[rule.name] = counts.get(rule.name, 0) + 1

        # ── 4. Burn fills in; remove underlying text in redacted areas ──
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    # Incremental save preserves everything that wasn't redacted
    doc.save(str(output_path), incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    return log, counts


# ═══════════════════════════════════════════════════════════════════════════
# Image redaction — black bars on a copy  (Pillow + tesseract)
# ═══════════════════════════════════════════════════════════════════════════

def _redact_image(input_path, output_path, compiled_rules):
    import pytesseract
    from PIL import Image, ImageDraw

    # Work on a copy
    img = Image.open(str(input_path))
    original_mode = img.mode
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    # Build a reconstructed text with word-bbox mapping
    spans, parts, cp = [], [], 0
    for i in range(len(data["text"])):
        w = data["text"][i]
        if not w.strip() or int(data["conf"][i]) < 0:
            continue
        l, t, wd, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        spans.append((cp, cp + len(w), l, t, l + wd, t + h))
        parts.append(w)
        cp += len(w) + 1
    full_text = " ".join(parts)

    hits = _detect(full_text, compiled_rules)
    log, counts = [], {}
    PAD = 2

    for _, _, m, rule in hits:
        gs, ge = _sensitive_span(m, rule)
        boxes = [(x0, y0, x1, y1)
                 for cs, ce, x0, y0, x1, y1 in spans
                 if cs < ge and ce > gs]
        if boxes:
            draw.rectangle([
                min(b[0] for b in boxes) - PAD,
                min(b[1] for b in boxes) - PAD,
                max(b[2] for b in boxes) + PAD,
                max(b[3] for b in boxes) + PAD,
            ], fill=(0, 0, 0))
        log.append({"rule": rule.name, "category": rule.category, "preview": _preview(m)})
        counts[rule.name] = counts.get(rule.name, 0) + 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path))
    return log, counts


# ═══════════════════════════════════════════════════════════════════════════
# Text redaction — token replacement on a copy
# ═══════════════════════════════════════════════════════════════════════════

def _redact_text(text, compiled_rules):
    """Single-pass token replacement.  Returns (redacted_text, log, counts)."""
    log, counts, result_lines = [], {}, []
    for line_no, line in enumerate(text.split("\n"), 1):
        hits = _detect(line, compiled_rules)
        parts, cur = [], 0
        for s, e, m, rule in hits:
            parts.append(line[cur:s])
            parts.append(m.expand(rule.replacement))
            log.append({"line": line_no, "rule": rule.name,
                        "category": rule.category, "preview": _preview(m)})
            counts[rule.name] = counts.get(rule.name, 0) + 1
            cur = e
        parts.append(line[cur:])
        result_lines.append("".join(parts))
    return "\n".join(result_lines), log, counts


# ═══════════════════════════════════════════════════════════════════════════
# Public API — single entry point
# ═══════════════════════════════════════════════════════════════════════════

def redact_file(
    input_path: Path,
    output_path: Path,
    mode: str = "standard",
    custom_patterns: list[str] | None = None,
) -> RedactionResult:
    """
    Produce a redacted **copy** of *input_path* at *output_path*.

    * PDF  → black rectangles drawn over PII, underlying text removed.
    * Image → black rectangles painted over OCR-detected PII.
    * Text → regex token replacement (format preserved).

    The original file is never modified.
    """
    ext = input_path.suffix.lower()
    compiled_rules = _compile_rules(mode, custom_patterns)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if ext in _PDF_EXTS:
        log, counts = _redact_pdf(input_path, output_path, compiled_rules)
        return RedactionResult(output_path=output_path, log=log, counts=counts, fmt="pdf")

    if ext in _IMG_EXTS:
        log, counts = _redact_image(input_path, output_path, compiled_rules)
        return RedactionResult(output_path=output_path, log=log, counts=counts, fmt="image")

    # Text file
    text = _read_text_file(input_path)
    if text is None:
        raise ValueError(
            f"Cannot read '{input_path}' as text. "
            "If the file is password-protected or encrypted, decrypt it first."
        )
    redacted_text, log, counts = _redact_text(text, compiled_rules)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(redacted_text, encoding="utf-8")
    return RedactionResult(
        output_path=output_path, log=log, counts=counts,
        fmt="text", redacted_text=redacted_text,
    )


# Convenience wrapper kept for backward-compat and direct text use
def redact(text: str, mode: str = "standard", custom_patterns: list[str] | None = None) -> RedactionResult:
    """Redact PII in a text string.  Returns result with .redacted_text populated."""
    compiled_rules = _compile_rules(mode, custom_patterns)
    rt, log, counts = _redact_text(text, compiled_rules)
    return RedactionResult(log=log, counts=counts, fmt="text", redacted_text=rt)


# ═══════════════════════════════════════════════════════════════════════════
# Summary formatter
# ═══════════════════════════════════════════════════════════════════════════

_CAT_LABELS = {
    0: "Custom Patterns",
    1: "Category 1 — Personal Identifiers",
    2: "Category 2 — Financial Data",
    3: "Category 3 — Legal / Sensitive",
}


def format_summary(result: RedactionResult, mode: str, input_path: Path) -> str:
    """Return a human-readable summary string."""
    total = sum(result.counts.values())
    rules_map = {r.name: r.category for r in ALL_RULES}

    by_cat: dict[int, dict[str, int]] = {}
    for name, cnt in result.counts.items():
        cat = rules_map.get(name, 0)
        by_cat.setdefault(cat, {})[name] = cnt

    previews: dict[str, list[str]] = {}
    for e in result.log:
        previews.setdefault(e["rule"], []).append(e["preview"])

    lines = [
        "",
        "═" * 60,
        "  REDACTION SUMMARY",
        f"  Mode: {mode}  |  File: {input_path.name}",
        "═" * 60,
    ]
    if total == 0:
        lines.append("  No sensitive data found.")
    else:
        for cat in sorted(by_cat):
            ct = sum(by_cat[cat].values())
            lines.append(f"\n  {_CAT_LABELS.get(cat, f'Category {cat}')}  ({ct} item(s))")
            for name, cnt in sorted(by_cat[cat].items()):
                snips = previews.get(name, [])
                snip = "  ".join(snips[:3]) + ("  …" if len(snips) > 3 else "")
                lines.append(f"    {name:<22} ×{cnt:<3}  {snip}")
    lines += ["", f"  Total: {total} item(s) redacted."]
    if result.output_path:
        lines.append(f"  Output: {result.output_path}")
    lines.append("═" * 60)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def _read_text_file(path: Path) -> str | None:
    for enc in ("utf-8", "latin-1"):
        try:
            text = path.read_text(encoding=enc)
            sample = text[:1000]
            bad = sum(1 for c in sample if ord(c) < 9 or 13 < ord(c) < 32)
            if bad > len(sample) * 0.1:
                return None
            return text
        except UnicodeDecodeError:
            continue
    return None


def _auto_output(input_path: Path) -> Path:
    return input_path.with_stem(input_path.stem + "_redacted")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def build_parser():
    p = argparse.ArgumentParser(
        prog="redactor",
        description="Redact PII from PDFs, images, and text files.",
    )
    p.add_argument("--file", required=True, help="Input file")
    p.add_argument("--output", help="Output path (default: <name>_redacted.<ext>)")
    p.add_argument("--mode", choices=["light", "standard", "full"], default="standard")
    p.add_argument("--custom", action="append", metavar="REGEX",
                   help="Extra regex(es) to redact (repeatable)")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be redacted; don't write a file")
    p.add_argument("--log", action="store_true",
                   help="Append per-item detail to the summary")
    return p


def main() -> int:
    args = build_parser().parse_args()

    in_path = Path(args.file).expanduser().resolve()
    if not in_path.exists():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        return 1

    out_path = Path(args.output).expanduser().resolve() if args.output else _auto_output(in_path)

    # ── Dry run: detect only ──────────────────────────────────────────────
    if args.dry_run:
        ext = in_path.suffix.lower()
        compiled = _compile_rules(args.mode, args.custom)
        if ext in _PDF_EXTS:
            import fitz
            doc = fitz.open(str(in_path))
            text = "\n".join(p.get_text() for p in doc)
            doc.close()
        elif ext in _IMG_EXTS:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(str(in_path)).convert("RGB"))
        else:
            text = _read_text_file(in_path)
            if text is None:
                print("Error: cannot read file as text.", file=sys.stderr)
                return 1
        _, log, counts = _redact_text(text, compiled)
        result = RedactionResult(log=log, counts=counts)
        summary = format_summary(result, args.mode, in_path)
        print(summary, file=sys.stderr)
        print("  (Dry run — no file written.)", file=sys.stderr)
        return 0

    # ── Full redaction ────────────────────────────────────────────────────
    try:
        result = redact_file(in_path, out_path,
                             mode=args.mode, custom_patterns=args.custom)
    except ImportError as e:
        print(f"Error: missing dependency — {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # ── Always print the summary ──────────────────────────────────────────
    summary = format_summary(result, args.mode, in_path)
    print(summary, file=sys.stderr)

    if args.log and result.log:
        print("\n  Redaction log (first 30):", file=sys.stderr)
        for entry in result.log[:30]:
            loc = f"p.{entry['page']}" if "page" in entry else f"L{entry.get('line', '?')}"
            print(f"    {loc:>6} | {entry['rule']:<22} | {entry['preview']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
