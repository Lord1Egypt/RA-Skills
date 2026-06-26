---
name: accounting-finance-system-research
description: Research and solve "how do I do this?" questions inside accounting and finance software systems (ERP, GL, AP/AR, billing, close, and reporting tools). Use when a user needs operational steps, setup guidance, or troubleshooting help in a specific system and wants the result documented as a quick memo or simple Q-and-A DOCX.
---

# Accounting And Finance System Research

## Overview

Follow a fixed process for system-how-to support: collect facts, ask clarifying questions, confirm output format, confirm understanding, research external guidance, analyze the best path, and generate a DOCX deliverable.

## Required Behavior

- Ask clarifying questions before proposing a solution.
- Confirm whether output should be `quick memo` or `simple q-and-a`.
- Restate understanding and wait for confirmation before web research.
- Research the internet after confirmation, prioritizing official vendor guidance.
- Separate source-backed guidance from assumptions or inference.
- Include source links and accessed dates in the deliverable.
- Generate a DOCX report in the user-selected format.

## Workflow

### 1) Intake And Scope

- Capture the user objective in one sentence.
- Confirm system name and version/edition (for example: NetSuite, SAP S/4HANA Cloud, Dynamics 365 Finance, QuickBooks).
- Confirm module or workflow area (for example: AP, AR, close, reconciliations, reporting).
- Confirm role/permission constraints and any deadline pressure.

### 2) Clarification Questions (Mandatory)

- Use [references/clarification-question-bank.md](references/clarification-question-bank.md).
- Ask only missing critical questions; avoid redundant prompts.
- Pause solutioning until enough facts are available.
- If facts remain unknown, continue with explicit assumptions and conditional guidance.

### 3) Output Format Confirmation (Mandatory)

- Ask the user to choose one:
- `quick memo`: concise professional summary with recommendation and steps.
- `simple q-and-a`: direct answer format with numbered actions.
- Default to `quick memo` only when user gives no preference.

### 4) Understanding Confirmation (Mandatory)

- Restate:
- problem statement
- system context
- open questions or assumptions
- chosen output format
- Ask for explicit confirmation before researching.

### 5) Research External Guidance

- Follow source ranking in [references/source-priority.md](references/source-priority.md).
- Gather at least two relevant sources where possible.
- Include at least one official vendor source when available.
- Track per-source metadata: title, publisher, URL, updated/published date if available, accessed date.
- Prefer current version-specific guidance over older generic content.

### 6) Analyze And Build Recommendations

- Translate research into concrete user actions.
- Provide prerequisites and permissions needed for each action.
- Add fallback steps when primary path is blocked.
- Include validation checks to confirm completion.
- Call out risks and unresolved dependencies.

### 7) Generate DOCX Deliverable

- Build JSON input using [references/report-json-schema.md](references/report-json-schema.md).
- Run:

```bash
python scripts/build_system_guidance_docx.py \
  --input-json <analysis.json> \
  --output-docx <system-guidance.docx> \
  --format <memo|q-and-a>
```

- Map `quick memo` to `memo`.
- Map `simple q-and-a` to `q-and-a`.
- Confirm the document includes:
- request summary and system context
- clarifications and assumptions
- guidance sources with URLs
- recommended steps
- validation checks
- risks and open items

### 8) Quality Check

- Verify recommendations are consistent with cited guidance.
- Verify assumptions are explicit and easy to review.
- Verify deliverable format matches user request.
- Verify every source has a URL and accessed date.
- Verify output file is `.docx` and readable.

## Resources

- Clarification checklist: [references/clarification-question-bank.md](references/clarification-question-bank.md)
- Source hierarchy: [references/source-priority.md](references/source-priority.md)
- Report JSON schema: [references/report-json-schema.md](references/report-json-schema.md)
- Example report payload: [references/example_report_input.json](references/example_report_input.json)
- DOCX generator: `scripts/build_system_guidance_docx.py`

## Dependency

Install once if needed:

```bash
python -m pip install --user python-docx
```
