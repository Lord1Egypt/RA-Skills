# DVP Document Structure Catalog

Standard sections in a Data Validation Plan document.

## Required Sections

### 1. Purpose

State the purpose of the DVP: to define the data validation approach, checks, and procedures for the clinical study.

### 2. Scope

Define what the DVP covers:
- Study identifier and protocol number
- Data modules/domains in scope
- Types of validation covered (edit checks, manual review, SAS programs, listings)
- What is explicitly out of scope

### 3. Roles & Responsibilities

Define who is responsible for each aspect of data validation:

| Role | Responsibility |
|------|---------------|
| Lead DM | Overall DVP ownership, strategy approval |
| DM | Execute validation checks, raise queries |
| DB Programmer | Implement edit checks, SAS programs |
| Biostatistician | Confirm analysis-driven validation needs |
| Medical Monitor | Review clinical logic of checks |
| Project Manager | Milestone alignment |

### 4. Data Review Strategy

Overall approach to data review:
- Frequency of data review
- Review milestones aligned with study timeline
- Prioritization of review activities
- Escalation procedures for critical findings

### 5. Validation Check Details

The core of the DVP — all check rules organized by module. Each check includes:
- Check ID, description, logic, trigger, query wording, priority, method
- Organized by domain/module with clear section headers

### 6. External Data Reconciliation

Plan for reconciling external data sources:
- Lab data
- ECG data
- Imaging data
- SAE reporting (MedWatch/CIMOS)
- Randomization data
- Other third-party data

For each: reconciliation method, frequency, key matching fields, discrepancy handling.

### 7. Query Management Rules

How queries are managed:
- Query generation rules (automatic vs manual)
- Query aging and escalation
- Query resolution expectations
- Query categorization (critical, major, minor)

### 8. Review Frequency & Milestones

Timeline for data review activities:
- Routine review frequency (e.g., weekly, biweekly)
- Milestone-driven reviews (database lock, interim analysis)
- SAE/safety data review frequency
- Special review triggers

### 9. Revision History

Track document changes:

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | YYYY-MM-DD | Name | Initial draft |

### 10. Appendix

Supporting materials:
- Complete check list (cross-reference to Excel)
- Reference documents list
- Domain-to-module mapping
- Abbreviations and definitions
