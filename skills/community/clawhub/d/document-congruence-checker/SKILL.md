---
name: document-congruence-checker
description: |
  Compare multiple documents for congruency and consistency.
  Use when: User needs to verify that multiple documents (contracts, reports, forms, specs) 
  contain consistent information, identify conflicting data points, or ensure alignment 
  across document sets.
---

# Document Congruence Checker

## Purpose

Compare 2+ documents to identify:
- Conflicting information (dates, names, amounts, terms)
- Missing fields in some documents
- Inconsistent terminology or values
- Version mismatches

## Input

User provides:
- 2 or more documents (PDF, DOCX, TXT, MD, JSON, XML)
- Optional: specific fields to focus on
- Optional: tolerance rules (e.g., date format differences OK)

## Process

### 1. Document Parsing
- Extract text and structured data from each document
- Identify document type and key fields
- Normalize data formats (dates, currencies, names)

### 2. Field Mapping
- Create unified field schema across all documents
- Map equivalent fields (e.g., "Client Name" = "Customer Name" = "Party A")
- Note fields present in some docs but not others

### 3. Congruence Analysis
For each mapped field:
- **Congruent**: Values match exactly (or within tolerance)
- **Incongruent**: Values conflict
- **Missing**: Field absent in one or more documents
- **Ambiguous**: Values unclear or unparseable

### 4. Report Generation
Output a discrepancy table with:
| Field | Doc A | Doc B | Doc C | Status | Notes |
|-------|-------|-------|-------|--------|-------|

## Output Format

```markdown
## 📊 Document Congruence Report

**Documents Compared:** {list}
**Analysis Date:** {date}
**Overall Congruence:** {High/Medium/Low} - {X}% fields aligned

### ✅ Congruent Fields ({count})
| Field | Value | Present In |
|-------|-------|------------|
| {field} | {value} | All docs |

### ⚠️ Incongruent Fields ({count})
| Field | Doc A | Doc B | Doc C | Discrepancy Type |
|-------|-------|-------|-------|------------------|
| Date | 2026-04-01 | 2026-04-10 | 2026-04-01 | Value mismatch |
| Amount | $10,000 | $10,000 | - | Missing in Doc C |

### 📋 Missing Fields ({count})
| Field | Missing In | Impact |
|-------|------------|--------|
| Signature | Doc B | High - legal validity |

### 🔍 Recommendations
1. {action item}
2. {action item}
```

## Congruence Levels

| Level | Criteria |
|-------|----------|
| **High** | 90%+ fields congruent, no critical conflicts |
| **Medium** | 70-89% congruent, minor conflicts only |
| **Low** | <70% congruent, or critical conflicts present |

## Critical vs Non-Critical Fields

**Critical** (incongruence = high risk):
- Dates (effective, expiry, delivery)
- Amounts (prices, fees, penalties)
- Names (parties, signatories)
- Legal terms (liability, termination)
- Identifiers (contract #, account #)

**Non-Critical** (incongruence = low risk):
- Formatting differences
- Typos in non-legal text
- Optional fields
- Descriptive language variations

## Usage Examples

### Example 1: Contract Comparison
```
User: Compare these 3 contract versions for inconsistencies
Agent: [parses docs, outputs congruence table]
```

### Example 2: Financial Report Alignment
```
User: Check if Q1 report matches Q2 report for opening balances
Agent: [compares specific fields, flags mismatches]
```

### Example 3: Form Data Validation
```
User: Verify all application forms have consistent applicant info
Agent: [cross-checks names, IDs, dates across forms]
```

## Tools Used

- `read` - Parse document contents
- `exec` - Run document parsing tools (pdftotext, docx2txt, etc.)
- `write` - Generate congruence report

## Limitations

- Scanned PDFs require OCR (may have accuracy issues)
- Handwritten content not reliably parseable
- Semantic equivalence (same meaning, different words) requires human judgment
- Images/charts not analyzed for data congruence

## Security Notes

- Never send sensitive documents to external APIs
- Process locally when possible
- Redact confidential data from reports if sharing
- Delete temp files after analysis

---

*Skill ready for document congruence analysis*
