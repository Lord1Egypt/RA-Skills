# Document Categorizer — Reference Guide

## Purpose
When a user uploads a document without specifying what they want done with it, automatically analyze the document and determine the most appropriate processing mode. Then either proceed (if confidence is high) or present the classification result and ask for confirmation.

---

## When This Mode Runs

This mode runs as a pre-step when:
1. The user uploads a file and says something like "what can you do with this?", "process this", "analyze this", "help me with this document", or says nothing at all beyond uploading
2. The user's intent is ambiguous and could match more than one mode
3. No mode-specific trigger phrase is detected

This mode does NOT run when the user clearly states their intent ("fill this form", "translate to Spanish", "scan this receipt", etc.).

---

## Consent Gate — Required Before Reading

Do NOT read the document before confirming the user wants auto-classification. Show the mode menu from SKILL.md Step 1 and ask:

> "I can classify this document automatically to suggest the best processing mode — that requires me to read the first 1–2 pages. Alternatively, you can choose a mode directly from the list above. Shall I classify it automatically, or which mode would you like?"

Only proceed to Step 1 (reading) after the user says "classify it", "figure it out", "auto-detect", "yes", or similar. If the user picks a mode directly, skip to that mode's reference file without reading via the categorizer.

---

## Step 1 — Initial Document Read

Read the first 1–2 pages (or the full document if short). You are looking for structural and content signals — do NOT process the full document yet.

Focus on:
- Title, headers, document type label
- Layout (form fields vs. paragraphs vs. tables vs. grid)
- Key vocabulary and domain signals
- Visual structure (photo, scan, text, mixed)
- Language
- File type (if determinable from content)

---

## Step 2 — Classification Signal Map

Apply this signal map to classify the document:

### Identity Documents
| Signal | Classification |
|---|---|
| Photo + MRZ lines at bottom | Passport → **ID & Passport Scanner** |
| "IDENTITY CARD", national crest, no MRZ or TD1 MRZ | National ID → **ID & Passport Scanner** |
| "DRIVER LICENCE / LICENSE", vehicle class codes | Driver's License → **ID & Passport Scanner** |
| "VISA", sticker format with dates and entry count | Visa → **ID & Passport Scanner** |
| "BIRTH CERTIFICATE", registrar seal, no photo | Birth Certificate → **ID & Passport Scanner** |

### Financial Documents
| Signal | Classification |
|---|---|
| "RECEIPT", merchant name at top, line items with prices, total | Receipt → **Receipt Scanner** |
| "INVOICE", invoice number, bill-to/ship-to, net terms | Invoice → **Receipt Scanner** |
| Bank logo + account number + transactions table + period dates | Bank Statement → **Bank Statement Analyzer** |
| "CREDIT CARD STATEMENT", credit limit, minimum payment | Credit Card Statement → **Bank Statement Analyzer** |
| "EXPENSE REPORT", multiple receipt entries in table | Expense Report → **Receipt Scanner** (batch) |
| "TAX RETURN", "FORM 1040 / T1 / SA100", income/deduction fields | Tax Form → **Form Autofill** or **Document Categorizer ask** |
| "W-2 / T4 / P60", employer, gross wages, withholding boxes | Payroll Document → **Table Extractor** or **Bank Statement Analyzer** |

### Legal & Contractual Documents
| Signal | Classification |
|---|---|
| "AGREEMENT", "CONTRACT", party names, "WHEREAS", "NOW THEREFORE" | Contract → **Contract Analyzer** |
| "NON-DISCLOSURE AGREEMENT", "CONFIDENTIAL INFORMATION" | NDA → **Contract Analyzer** |
| "EMPLOYMENT AGREEMENT", "OFFER LETTER", salary, start date | Employment Contract → **Contract Analyzer** |
| "LEASE AGREEMENT", "TENANT", "LANDLORD", "MONTHLY RENT" | Lease → **Contract Analyzer** |
| "TERMS OF SERVICE", "PRIVACY POLICY", "END USER LICENSE" | ToS/EULA → **Contract Analyzer** |
| "SETTLEMENT AGREEMENT", "RELEASE OF CLAIMS" | Settlement → **Contract Analyzer** |
| PII-heavy content + user wants to share it | Any document → **Legal Redactor** |

### Medical Documents
| Signal | Classification |
|---|---|
| Lab panel names (CBC, BMP, LFT, TSH), reference ranges, result values | Lab Report → **Medical Summarizer** |
| Drug names, "SIG:", "Dispense:", prescriber signature | Prescription → **Medical Summarizer** |
| "ADMISSION DATE", "DISCHARGE DATE", "DIAGNOSIS" | Discharge Summary → **Medical Summarizer** |
| "IMPRESSION", "FINDINGS", imaging modality (CT, MRI, X-ray) | Radiology Report → **Medical Summarizer** |
| Vaccine names, lot numbers, administration dates | Vaccination Record → **Medical Summarizer** |
| "EXPLANATION OF BENEFITS", CPT codes, billed/allowed amounts | EOB → **Medical Summarizer** |

### Professional Documents
| Signal | Classification |
|---|---|
| Name prominently at top + contact info + work history + education | Resume/CV → **Resume / CV Parser** |
| "CURRICULUM VITAE", academic publications list | Academic CV → **Resume / CV Parser** |
| "LINKEDIN" export, profile sections | LinkedIn Export → **Resume / CV Parser** |

### Administrative / Government Forms
| Signal | Classification |
|---|---|
| Blank or partially filled fields with labels, checkbox grids | Form → **Form Autofill** |
| "APPLICATION FORM", "PLEASE COMPLETE IN BLOCK CAPITALS" | Application Form → **Form Autofill** |
| Government logo, form number (e.g., DS-160, Form 14A, I-130) | Government Form → **Form Autofill** |
| "CUSTOMS DECLARATION", "ARRIVAL CARD" | Travel Form → **Form Autofill** |

### Meeting & Communication Documents
| Signal | Classification |
|---|---|
| "MEETING MINUTES", "ACTION ITEMS", attendee list | Meeting Notes → **Meeting Minutes Extractor** |
| Audio file path or transcript with speaker turns | Audio/Transcript → **Meeting Minutes Extractor** |
| Chat/message export (Slack, Teams, WhatsApp) | Chat Log → **Meeting Minutes Extractor** |

### Data Documents
| Signal | Classification |
|---|---|
| Grid of rows/columns with numeric or tabular data, no prose | Table → **Table Extractor** |
| "TABLE 1:", "Figure 3:", data appendix in a report | Embedded Tables → **Table Extractor** |
| CSV or TSV file | Structured Data → **Table Extractor** |
| Annual report, research paper with data tables | Report → **Table Extractor** or **Document Translator** |

### Multi-Language Documents
| Signal | Classification |
|---|---|
| Document not in English and user communicates in English | Any doc → **Document Translator** |
| "TRADUZCA", "ÜBERSETZEN", "TRADUCTION" requested | Any doc → **Document Translator** |

---

## Step 3 — Confidence Assessment

| Confidence | Condition | Action |
|---|---|---|
| **High** (≥85%) | Strong signals, one clear mode | Proceed automatically; state classification at the start |
| **Medium** (60–85%) | Reasonable signals, one primary mode | State classification + brief reasoning; ask for confirmation |
| **Low** (<60%) | Weak or conflicting signals | Present top 2–3 options and ask user to choose |
| **Multi-mode** | Document clearly serves multiple purposes | List all applicable modes; recommend one; let user choose |

---

## Step 4 — Classification Output

### High Confidence (auto-proceed)
```
📄 Document classified as: **[Mode Name]**
Confidence: High
Reason: [1-line reason — e.g., "MRZ lines detected, ICAO TD3 passport format"]

Proceeding with [Mode Name]…
---
[Continue with the matched mode's reference guide]
```

### Medium Confidence (ask confirmation)
```
📄 I believe this is a **[Document Type]** — I'll process it with **[Mode Name]**.
Reason: [2-line reason with specific signals observed]

Is that correct, or would you prefer a different mode?
- [Mode A] — [brief description]
- [Mode B] — [brief description]
- [Mode C] — [brief description]
```

### Low Confidence (present options)
```
📄 I can see this is a [general description — e.g., "formal document with financial data"], but I'm not certain which processing mode would be most useful.

What would you like me to do?
| Option | Best For |
|---|---|
| Receipt Scanner | If this is a receipt or invoice |
| Bank Statement Analyzer | If this is a bank or credit card statement |
| Table Extractor | If you want the financial data extracted as a table |
| Contract Analyzer | If this is an agreement or contract |

Please tell me which mode fits, or type "all" to see all available modes.
```

### Ambiguous / Multi-Mode
```
📄 This document could be processed in multiple ways:
- **Primary recommendation**: [Mode A] — because [reason]
- **Also possible**: [Mode B] — if you want [different outcome]

Which would you like?
```

---

## Step 5 — Presenting All Modes (if user asks)

If user says "show me all modes" or "what can you do":

```
I can help with the following document types:

| Mode | Best For | Example Trigger |
|---|---|---|
| Form Autofill | Visa, government, insurance, rental forms | "Fill this form" |
| Contract Analyzer | Contracts, NDAs, leases, employment agreements | "Review this contract" |
| Receipt Scanner | Receipts, invoices, expense reports | "Scan this receipt" |
| Bank Statement Analyzer | Bank/credit card statements, transactions | "Analyze my bank statement" |
| Resume / CV Parser | Resumes, CVs, LinkedIn exports | "Parse this resume" |
| ID & Passport Scanner | Passports, national IDs, driver's licenses, visas | "Scan my passport" |
| Medical Summarizer | Lab reports, prescriptions, discharge summaries, imaging | "Explain my blood test" |
| Legal Redactor | Any document with PII or sensitive data to remove | "Redact this document" |
| Meeting Minutes Extractor | Meeting notes, transcripts, audio recordings | "Extract action items" |
| Table Extractor | PDFs or images with tables and data | "Extract this table to CSV" |
| Document Translator | Any document in a non-target language | "Translate this to English" |
| Document Timeline | View your processing history | "Show my timeline" |
| Doc Scan | Photos of documents — perspective correction + scan effect | "Scan this photo" |

Upload a document and I'll automatically detect what type it is.
```

---

## Classification Accuracy Rules
- Never misclassify a medical document as a form or receipt
- A document with BOTH a form structure AND contract clauses → **Contract Analyzer** (clauses dominate)
- A document with BOTH financial tables AND medical results → **Medical Summarizer** (medical dominates)
- An image that is clearly NOT a document (e.g., selfie, landscape photo, screenshot of a website with no document) → flag: "This doesn't appear to be a document. Did you mean to upload a different file?"
- Always state what signals led to the classification decision
