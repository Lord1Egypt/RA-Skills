---
name: clawhub-dev-invoice
description: "Generate professional invoices for ClawHub/OpenClaw skill development services. Use when billing for custom AgentSkills: creation, editing, testing, ClawHub publishing. Features: standard rates ($150/hr dev, $500 skill init), Saskatchewan GST 5% auto-calc, multi-item support, PDF/HTML output via templates/scripts."
---

# ClawHub Dev Invoice Generator

## Overview
Specialized tool for Thomas to quickly generate invoices for freelance ClawHub skill dev work. Includes standard rates, Sask tax, professional formatting. Outputs ready-to-send PDF.

## When to Use
- Client requests quote/invoice for skill work
- Monthly billing summary for ongoing dev
- One-off fixed fee for skill publish/package
- Track billable hours on projects

## Standard Rates (CAD)
| Service | Rate |
|---------|------|
| Skill Initialization & Basic SKILL.md | $500 fixed |
| Hourly Development/Editing | $150/hr |
| ClawHub Publishing & Validation | $100 fixed |
| Testing/Debugging | $75/hr |
| Expenses (tools, API credits) | Cost + 15% |
| Rush Fee (<48h) | +50% |

## Quick Start Workflow
1. **Collect Data**:
   - Invoice # (e.g. 2026-001)
   - Date (YYYY-MM-DD), Due (30 days later)
   - Client: name, company, address, email
   - Your details: Thomas [Lastname], Clavet SK, thomas@example.com
   - Line items: desc, hours/qty, rate, amount = qty*rate

2. **Calculate Totals**:
   - Subtotal = sum amounts
   - GST = subtotal * 0.05
   - Total = subtotal + GST

3. **Generate**:
   - Use `scripts/generate_invoice.py client-data.json` for PDF
   - Or manually: copy `assets/invoice-template.html`, edit, exec pandoc to PDF

4. **Send**: Attach PDF, reference invoice #.

## Resources

### scripts/generate_invoice.py
Automates HTML+PDF from JSON input. Run: `python scripts/generate_invoice.py input.json`

Input JSON example:
```json
{
  "invoice_num": "2026-001",
  "date": "2026-03-29",
  "due_date": "2026-04-28",
  "client": {
    "name": "Client Co",
    "address": "123 Street, City SK",
    "email": "client@example.com"
  },
  "items": [
    {"desc": "Skill init: weather-forecast", "hours": 4, "rate": 150},
    {"desc": "ClawHub publish", "fixed": 100}
  ],
  "expenses": 50
}
```

### references/sask_tax_guidelines.md
Sask GST details, terms.

### assets/sample-input.json
HTML template for manual edits. Style: clean, professional (Arial, tables).
