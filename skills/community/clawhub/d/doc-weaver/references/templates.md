# Doc Weaver — Template Reference

## Built-in Templates (10 total)

| Key              | Name                       | Cover | Heading Font         | Body Font          | Primary Color | Accent    |
|------------------|----------------------------|-------|----------------------|--------------------|---------------|-----------|
| `prd`            | Product Requirements Doc   | Yes   | Arial                | Calibri            | #1a73e8       | #e8f0fe   |
| `report`         | Report                     | Yes   | Georgia              | Calibri            | #333333       | #f5f5f5   |
| `academic`       | Academic Paper             | Yes   | Times New Roman      | Times New Roman    | #000000       | #ffffff   |
| `manual`         | User Manual                | Yes   | Helvetica             | Helvetica          | #005a9e       | #e6f2ff   |
| `contract`       | Contract                   | Yes   | Times New Roman      | Times New Roman    | #000000       | #ffffff   |
| `proposal`       | Business Proposal          | Yes   | Helvetica             | Arial              | #2d5f8a       | #eaf2f8   |
| `resume`         | Resume / CV                | No    | Calibri              | Calibri            | #2c3e50       | #ecf0f1   |
| `newsletter`     | Email Newsletter           | Yes   | Georgia              | Georgia            | #c0392b       | #fdecea   |
| `meeting-minutes`| Meeting Minutes            | Yes   | Arial                | Arial              | #27ae60       | #eafaf1   |
| `whitepaper`     | Technical Whitepaper       | Yes   | Times New Roman      | Times New Roman    | #1a1a2e       | #f0f0f5   |

## Auto-Detection Keywords

Document type auto-detection uses keyword scoring:

- **prd**: PRD, product requirement, feature, stakeholder, user story, product spec
- **report**: report, analysis, findings, summary, conclusion, quarterly, annual report
- **academic**: abstract, introduction, methodology, literature, reference, bibliography, thesis, dissertation
- **manual**: manual, guide, instructions, steps, how to, getting started, tutorial, setup
- **contract**: contract, agreement, party, clause, terms, hereby, hereinafter, indemnification, warranty
- **proposal**: proposal, proposed solution, scope of work, deliverables, budget, timeline, executive summary, business case
- **resume**: resume, curriculum vitae, work experience, education, skills, certification, contact information
- **newsletter**: newsletter, issue #, weekly digest, subscriber, unsubscribe, featured article, editor's note
- **meeting-minutes**: meeting minutes, attendees, agenda, action items, next meeting, minutes of, discussion, motion
- **whitepaper**: whitepaper, white paper, technical overview, architecture, benchmark, use case, industry analysis

## Template Details

### prd — Product Requirements Document
Ideal for software product specs. Blue color scheme (#1a73e8), Arial headings, Calibri body. Includes cover page with title.

### report — Business Report
Neutral grey/black palette (#333333). Georgia headings for a classic look. Suitable for quarterly reports, analysis documents.

### academic — Academic Paper
Traditional black-on-white with Times New Roman throughout. Includes cover page. Suitable for theses, dissertations, and journal papers.

### manual — User Manual
Clean blue (#005a9e) with Helvetica fonts. Cover page. Optimized for step-by-step instructional content.

### contract — Legal Contract
Classic Times New Roman, black. Cover page. Clean, professional legal document styling.

### proposal — Business Proposal
Professional navy blue (#2d5f8a). Helvetica headings, Arial body. Cover page with executive summary layout.

### resume — Resume / CV
Clean, modern Calibri throughout. No cover page (single-page layout optimized). Dark slate (#2c3e50) accents.

### newsletter — Email Newsletter
Warm red (#c0392b) with Georgia serif fonts. Cover page with featured article layout.

### meeting-minutes — Meeting Minutes
Fresh green (#27ae60). Arial fonts. Cover page with date/attendees header layout.

### whitepaper — Technical Whitepaper
Dark navy (#1a1a2e). Times New Roman. Cover page. Technical document styling with architecture focus.

## Usage

```bash
# Generate with specific template
python3 scripts/weaver.py -i doc.md -t prd -o output.docx

# Auto-detect template
python3 scripts/weaver.py -i doc.md -t auto -o output.docx

# List available templates
python3 scripts/weaver.py --show-templates

# Preview template output (without file conversion)
python3 scripts/weaver.py -i doc.md -t report --preview

# Generate PDF
python3 scripts/weaver.py -i doc.md -t whitepaper -o output.pdf
```
