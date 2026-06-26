---
name: bid-review-lite
description: AI-powered bid/tender document review. Extracts text from .docx/.doc files, cross-references bid requirements vs responses, and generates a detailed audit report with risk ratings.
author: zacjiang
version: 1.0.0
tags: bid, tender, procurement, review, audit, compliance, document
---

# Bid Document Review (Lite)

Review bid/tender documents for errors, contradictions, compliance issues, and fraud indicators using AI analysis.

**What it does:**
- Extracts text + tables from .docx and .doc bid documents
- Cross-references procurement requirements vs bid responses
- Checks pricing consistency, qualification claims, technical parameters
- Identifies contradictions, missing information, expired certificates
- Generates a structured audit report with 🔴/🟡/🟢 risk ratings

**Ideal for:**
- Bid managers reviewing submissions before deadline
- Procurement officers auditing received bids
- Companies reviewing competitor bids (post-award disclosure)
- Quality assurance on your own tender responses

## Quick Start

1. Place your bid documents in a working directory:
   - Procurement/tender document (the requirements)
   - Bid/response document (what was submitted)

2. Tell your agent:
   ```
   Review the bid documents in [directory]. The procurement document is [file1] 
   and the bid response is [file2].
   ```

3. The agent will:
   - Extract all text and tables
   - Analyze against the checklist below
   - Generate a structured report

## Text Extraction

### For .docx files:
```bash
python3 {baseDir}/scripts/extract_text.py input.docx output.txt
```

### For .doc (legacy) files:
```bash
python3 {baseDir}/scripts/extract_doc_text.py input.doc output.txt
```

## Review Checklist

### 1. Pricing & Commercial
- [ ] Total price within maximum limit
- [ ] Unit prices within per-item limits
- [ ] Tax rate calculations correct
- [ ] Amount in words matches figures
- [ ] No abnormally low pricing (dumping risk)
- [ ] Payment terms match requirements

### 2. Mandatory Requirements (★ items)
- [ ] ALL mandatory/starred parameters responded to
- [ ] Responses meet or exceed minimums
- [ ] Supporting evidence provided for each claim
- [ ] No contradictions between different sections

### 3. Qualification & Eligibility
- [ ] Business license valid and matching
- [ ] Required certifications in-date
- [ ] Performance track record meets minimum
- [ ] Credit/reputation checks provided
- [ ] Authorization letters (if agent/distributor)

### 4. Technical Response
- [ ] All technical parameters addressed
- [ ] Claims supported by test reports/certificates
- [ ] Product model matches throughout document
- [ ] Standards referenced are current (not withdrawn)
- [ ] Delivery timeline realistic vs. claimed

### 5. Document Integrity
- [ ] Bidder name consistent throughout
- [ ] Signatures and seals present where required
- [ ] Dates logical (no future dates, no pre-bid dates)
- [ ] Page numbering sequential
- [ ] No template placeholders left unfilled (e.g. [X], [TBD])

### 6. Common Red Flags
- [ ] Identical test results matching nominal values exactly (fabrication indicator)
- [ ] Contracts with missing signatures or blank fields
- [ ] Expired certificates/qualifications submitted as valid
- [ ] Third-party materials without clear authorization
- [ ] Inconsistent company names across documents

## Report Format

Generate the report in Markdown with this structure:

```markdown
# Bid Review Report

## Project Info
- Procurement: [name]
- Bidder: [name]
- Date: [date]

## Summary
| Category | Status | Notes |
|----------|--------|-------|
| Pricing  | ✅/⚠️/❌ | ... |
| Mandatory params | ✅/⚠️/❌ | ... |
| ...      | ...    | ...   |

## 🔴 Critical Issues (may cause disqualification)
### 1. [Issue title]
- Location: [where in document]
- Detail: [what's wrong]
- Impact: [consequence]
- Recommendation: [fix]

## 🟡 Medium Issues (affects scoring)
...

## ✅ Positive Findings
...

## Checklist Summary
[Completed checklist with pass/fail for each item]
```

## Dependencies

- Python 3.6+
- python-docx (`pip3 install python-docx`)
- olefile (`pip3 install olefile`) — for .doc files only

## Limitations (Lite Version)

This lite version covers **text-based review only**. It does not include:
- Image extraction and visual analysis (certificates, contracts, photos)
- Automated image fraud detection (watermarks, stock photos, expired seals)
- PDF report generation
- Image compression/optimization for API cost savings

For full image review capabilities, see the complete bid-review skill.

## Built From Real Experience

This skill was developed from reviewing 3 real bid documents (1,800+ pages, 2,600+ images) in the road maintenance equipment industry. Every checklist item comes from an actual issue found in production reviews.

Issues discovered include: fake test data, stolen web images with visible watermarks, technical parameters contradicting government records by 4 tons, expired certificates submitted as valid, and 30+ pages of copied filler content.
