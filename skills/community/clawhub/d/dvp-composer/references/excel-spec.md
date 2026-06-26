# Excel Output Specification

## Default Format (4 Sheets)

When no user template is provided, generate Excel with these 4 sheets.

### Sheet 1: Check List

| Column | Header | Width | Description |
|--------|--------|-------|-------------|
| A | Check ID | 12 | Unique identifier (e.g., AE-001) |
| B | Module | 10 | Domain/module name |
| C | Category | 15 | Completeness/Consistency/Range/Cross-Module/Timeline |
| D | Check Description | 35 | Clear description of the check |
| E | Logic Rule | 30 | Exact logical condition |
| F | Applicable Scope | 20 | Which subjects/visits/conditions |
| G | Trigger Condition | 20 | When the check fires |
| H | Query Wording | 35 | Exact query text for sites |
| I | Severity | 10 | Critical/Major/Minor |
| J | Execution Method | 15 | System/SAS/Listing/Manual/Reconciliation |
| K | Status | 8 | Active/Inactive |
| L | Notes | 20 | Additional notes or comments |

**Formatting**:
- Header row: bold, white text on blue (#4472C4) background, centered, wrapped
- Module grouping: alternate row colors by module (light blue #D9E2F3 / white)
- Severity coloring: Critical=red (#FF4444) bold white text, Major=orange (#FFA500), Minor=yellow (#FFFF00)
- Freeze top row (A2)
- Auto-filter enabled on all columns
- All cells: thin border, vertical top alignment, text wrap

### Sheet 2: Summary

Layout as key-value pairs:

| Label | Content |
|-------|---------|
| Document Title | Data Validation Plan - [Protocol Number] |
| Protocol Number | [from Phase 1] |
| Study Phase | [from Phase 1] |
| Indication | [from Phase 1] |
| Sponsor | [from Phase 1] |
| Version | 1.0 |
| Date | [generation date] |
| Author | [user name or DM team] |
| Scope | [modules in scope] |
| Key Data | [critical variables list] |
| Risk Summary | [key risk areas] |
| Validation Strategy | [overall approach summary] |

Followed by a Roles & Responsibilities table:

| Role | Responsibility |
|------|---------------|
| [role] | [responsibility] |

**Formatting**:
- Labels in column A: bold, width 25
- Values in column B: wrapped text, width 60
- Roles table has header row with blue background

### Sheet 3: Revision History

| Column | Header | Width |
|--------|--------|-------|
| A | Version | 10 |
| B | Date | 15 |
| C | Author | 15 |
| D | Description of Changes | 40 |
| E | Reviewer | 15 |
| F | Approval Status | 15 |

**Formatting**: Header with blue background, thin borders, text wrap.

### Sheet 4: Ext Data Recon

| Column | Header | Width | Description |
|--------|--------|-------|-------------|
| A | Recon ID | 12 | Unique identifier (e.g., RECON-001) |
| B | Data Source | 15 | Lab/ECG/Imaging/SAE/Randomization/Other |
| C | Provider | 20 | External data provider name |
| D | Key Fields | 25 | Matching fields between internal and external data |
| E | Recon Method | 15 | Automated/Semi-automated/Manual |
| F | Frequency | 15 | Per transfer/Weekly/Monthly/Per milestone |
| G | Discrepancy Handling | 30 | How discrepancies are resolved |
| H | Responsible Party | 15 | Who performs reconciliation |
| I | Notes | 20 | Additional notes |

## Template Mode

When a user-provided template is used:
1. Read the template's existing sheet names and column headers
2. Map DVP content to the template's structure using flexible field name matching
3. Preserve the template's formatting and styles
4. Add data to existing sheets; do not create new sheets unless necessary
5. Respect any validation rules or dropdowns in the template

### Field Name Mapping

When mapping to template columns, recognize these common variations:

| Standard Field | Common Aliases |
|---------------|----------------|
| check_id | Check ID, CheckID, Check Number |
| module | Module, Domain |
| category | Category, Type, Check Category |
| description | Description, Check Description, CheckDesc |
| logic | Logic, Logic Rule, Rule |
| scope | Scope, Applicable Scope |
| trigger | Trigger, Trigger Condition |
| query_wording | Query, Query Wording, Query Text |
| severity | Severity, Priority |
| method | Method, Execution Method |
| status | Status |
| notes | Notes, Comments |
