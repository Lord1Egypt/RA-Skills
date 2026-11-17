## Description:

BigLead helps agents search for B2B customer leads by industry, product, and region, cross-check public sources, extract public contact details, manage a local lead database, and export prospecting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, business-development, and market-research users can use this skill to find target companies, collect public business contact information, score lead credibility, track follow-up status, and export local lead lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists prospect and contact data locally, which may be sensitive in some workflows.

Mitigation: Use the skill only where local storage of lead data is acceptable, and review retention, access, and handling practices for memory/lead-data/.

Risk: Export paths are under-scoped and could overwrite files if chosen carelessly.

Mitigation: Do not allow untrusted prompts to choose export paths; review the CSV output destination before running exports.

Risk: CSV exports from imported or untrusted lead data may be unsafe to open directly in spreadsheet tools.

Mitigation: Inspect or sanitize exported CSV content before opening it in a spreadsheet application.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON and CSV files managed by shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores lead records under memory/lead-data/ and can export CSV files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
