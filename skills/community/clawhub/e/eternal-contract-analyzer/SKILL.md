---
name: contract-analyzer
description: Analyze contracts, legal documents, and agreements for red flags, key terms, and risks. Use when the user uploads or references a contract, NDA, lease, employment agreement, terms of service, or any legal document and wants: a plain-English summary, risk analysis, key clauses extracted, unfair terms flagged, or comparison between versions. Triggers on "analyze contract", "review this agreement", "check for red flags", "what does this contract say", "NDA review", "lease review", "terms of service analysis".
---

# Contract Analyzer

Analyze legal documents for risks, key terms, and red flags.

## Quick Start

Analyze a contract:
```bash
python3 scripts/contract.py analyze contract.pdf
python3 scripts/contract.py analyze agreement.docx
python3 scripts/contract.py analyze terms.txt
```

Compare two versions:
```bash
python3 scripts/contract.py diff v1.pdf v2.pdf
```

## What It Extracts

- **Parties** — Who is bound by the agreement
- **Term** — Duration and renewal/auto-renewal clauses
- **Payment terms** — Amounts, schedules, penalties
- **Termination** — How to exit, notice periods, penalties for early exit
- **Liability** — Liability caps, indemnification, warranties
- **IP ownership** — Who owns what is created
- **Non-compete** — Restrictions on future work
- **Confidentiality** — NDA scope and duration
- **Dispute resolution** — Arbitration vs litigation, jurisdiction
- **Assignment** — Can the contract be transferred

## Red Flags Detected

- Auto-renewal without clear opt-out
- Unlimited liability or uncapped indemnification
- One-sided termination (only one party can exit)
- Broad non-compete clauses
- Jurisdiction far from user's location
- Vague payment terms
- Missing limitation of liability
- Unilateral modification clauses
- Penalty clauses disproportionate to breach

## Output

Reports include:
1. **Plain English Summary** — 3-5 sentence overview
2. **Risk Score** — Low/Medium/High/Critical
3. **Red Flags** — List with severity and explanation
4. **Key Terms Table** — Extracted terms in structured format
5. **Recommendations** — What to negotiate or clarify

## Supported Formats

- PDF (via pdfplumber)
- DOCX (via python-docx)
- TXT / plain text
- Images (via OCR)

## Note

This is an analysis tool, not legal advice. Always consult a qualified attorney for binding legal decisions.
