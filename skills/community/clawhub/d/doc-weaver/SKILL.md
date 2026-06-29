---
name: doc-weaver
description: "Transform Markdown or outlines into polished Word/PDF documents with professional templates"
version: 1.1.0
---

# Doc Weaver

Convert Markdown documents or structured outlines into publication-ready Word (.docx) or PDF documents using built-in professional templates.

## Quick Start

```bash
# Generate a Word document from Markdown
python3 scripts/weaver.py --input doc.md --template prd --output output.docx

# Generate a PDF
python3 scripts/weaver.py --input doc.md --template report --output output.pdf

# Auto-detect the best template
python3 scripts/weaver.py --input doc.md --output output.docx

# List all available templates
python3 scripts/weaver.py --show-templates

# Check local conversion dependencies
python3 scripts/weaver.py --doctor

# Preview without generating a file
python3 scripts/weaver.py --input doc.md --template proposal --preview

# Run release verification against bundled examples
python3 scripts/verify.py
```

## Workflow

1. **Parse input** — Read headings, lists, code blocks, tables, and blockquotes from Markdown.
2. **Auto-detect type** — Identify document purpose from structure: PRD, proposal, resume, whitepaper, and more (10 types).
3. **Load template** — Apply a matching template with covers, heading fonts, color schemes, and page styles.
4. **Auto-number headings** — Multi-level heading numbering (1, 1.1, 1.1.1) with configurable starting level.
5. **Table of contents** — Generate TOC field from heading hierarchy (clickable in Word, update field to populate).
6. **Format tables** — Apply borders, styled header rows (white text on primary color), alternating row shading.
7. **Special elements** — Code blocks → monospace (Courier New) + grey background; blockquotes → indented + left grey border; inline code → highlighted.
8. **Headers & footers** — Running title in header; page numbers (Page X of Y) + date in footer.
9. **Export** — `.docx` via python-docx (native Word formatting); `.pdf` via pandoc + weasyprint.

## Built-in Templates (10)

| Key              | Name                       | Cover | Heading Font    | Primary |
|------------------|----------------------------|-------|-----------------|---------|
| `prd`            | Product Requirements Doc   | Yes   | Arial           | #1a73e8 |
| `report`         | Report                     | Yes   | Georgia         | #333333 |
| `academic`       | Academic Paper             | Yes   | Times New Roman | #000000 |
| `manual`         | User Manual                | Yes   | Helvetica       | #005a9e |
| `contract`       | Contract                   | Yes   | Times New Roman | #000000 |
| `proposal`       | Business Proposal          | Yes   | Helvetica       | #2d5f8a |
| `resume`         | Resume / CV                | No    | Calibri         | #2c3e50 |
| `newsletter`     | Email Newsletter           | Yes   | Georgia         | #c0392b |
| `meeting-minutes`| Meeting Minutes            | Yes   | Arial            | #27ae60 |
| `whitepaper`     | Technical Whitepaper       | Yes   | Times New Roman | #1a1a2e |

## Real-world Examples

### Example 1: Product Requirements Document

**Scenario:** You have a feature spec written in Markdown and need to share it as a professional Word document with stakeholders.

**Input (`prd.md`):**
```markdown
# Chat Feature PRD

## Overview
Add real-time chat to the dashboard. Supports **1:1** and **group** conversations.

## User Stories
- As a user, I can send messages in real time
- As an admin, I can moderate chat rooms

## API Design

| Endpoint       | Method | Description       |
|----------------|--------|-------------------|
| /chat/send     | POST   | Send a message    |
| /chat/history  | GET    | Get chat history  |

> **Note:** WebSocket connections require authentication tokens.

## Timeline
1. Alpha: Week 1-2
2. Beta: Week 3-4
3. Launch: Week 5
```

**Command:**
```bash
python3 scripts/weaver.py -i prd.md -t prd -o ChatFeaturePRD.docx
```

**Expected output:** A Word document with cover page showing "1 Chat Feature PRD", table of contents, blue-themed headings, numbered structure (1.1 User Stories, 1.2 API Design), styled table with blue header, grey-background code block, and indented blockquote. Header shows "Chat Feature PRD", footer shows "Page X of Y | 2026-06-15".

---

### Example 2: Meeting Minutes → PDF

**Scenario:** You took meeting notes in Markdown and need to distribute a polished PDF.

**Input (`minutes.md`):**
```markdown
# Sprint Planning Meeting

## Attendees
- Alice (Product)
- Bob (Engineering)
- Charlie (Design)

## Agenda
1. Sprint goal review
2. Backlog grooming
3. Capacity planning

## Decisions
- **Sprint goal**: Ship user dashboard v2
- **Scope**: 8 story points for frontend, 5 for backend

## Action Items
- [ ] Alice: Finalize mockups by Wednesday
- [ ] Bob: Set up CI/CD pipeline
- [ ] Charlie: Design system audit

## Next Meeting
Friday, 3:00 PM — Sprint Review
```

**Command:**
```bash
python3 scripts/weaver.py -i minutes.md -t meeting-minutes -o SprintPlanning.pdf
```

**Expected output:** Both `.docx` and `.pdf` files. Green (#27ae60) theme with Arial fonts. Cover page with meeting title and date. Green-styled table headers, proper list formatting. PDF rendered with green headings and professional typography.

---

### Example 3: Technical Whitepaper with Auto-Detection

**Scenario:** You drafted a technical whitepaper and want the system to auto-detect and format it.

**Input (`architecture.md`):**
```markdown
# Cloud-Native Architecture Whitepaper

## Executive Summary
This whitepaper presents a **benchmark analysis** of cloud-native patterns.

## Architecture Overview

The solution architecture consists of three tiers:

```yaml
tiers:
  - presentation: React SPA
  - application: Python microservices
  - data: PostgreSQL + Redis
```

## Performance Benchmarks

| Pattern        | P99 Latency | Throughput | Cost/Month |
|----------------|-------------|------------|------------|
| Monolith       | 450ms       | 1.2K rps   | $1,200     |
| Microservices  | 120ms       | 8.5K rps   | $3,800     |
| Serverless     | 80ms        | 12K rps    | $2,100     |

## Industry Analysis

> Cloud-native adoption grew 47% YoY according to CNCF 2025 survey.

## Conclusion
Serverless offers the best latency/cost ratio for variable workloads.
```

**Command:**
```bash
python3 scripts/weaver.py -i architecture.md -t auto -o Whitepaper.docx
# Output: [doc-weaver] Auto-detected document type: whitepaper (Technical Whitepaper)
```

**Expected output:** System auto-detects `whitepaper` type. Dark navy (#1a1a2e) theme with Times New Roman. Cover page with "1 Cloud-Native Architecture Whitepaper". Properly numbered sections (1.1 Architecture Overview, 1.2 Performance Benchmarks), YAML code block with grey background, styled table with dark header row and alternating row shading.

## Requirements

- **python-docx** (`pip install python-docx`) — for .docx generation
- **pandoc** (`brew install pandoc`) — for .pdf generation
- **weasyprint** (`pip install weasyprint`) — PDF engine for pandoc

Run `python3 scripts/weaver.py --doctor` before using PDF output. If PDF
dependencies are missing, `.docx` generation can still work as long as
`python-docx` is installed.

## Verification

Before publishing or sharing a new package version, run:

```bash
python3 -m py_compile scripts/weaver.py scripts/verify.py
python3 scripts/weaver.py --doctor
python3 scripts/verify.py
```

The verification script renders a preview, generates a sample Word document,
and generates a sample PDF when the optional PDF toolchain is available.

## Safety

- All input stays local; no data is sent to external conversion services.
- Template engine uses built-in dictionaries; no external CSS files required.
- PDF output uses local pandoc + weasyprint pipeline.
