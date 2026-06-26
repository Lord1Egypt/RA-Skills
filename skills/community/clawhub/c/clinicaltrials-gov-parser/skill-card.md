## Description: <br>
Monitors, searches, and summarizes ClinicalTrials.gov trial records for sponsor, condition, recruitment, status-change, and competitive-intelligence workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and competitive-intelligence teams use this skill to query ClinicalTrials.gov, inspect specific NCT records, monitor recruitment and status changes, and generate trial activity summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical trial queries can disclose sponsor, condition, or trial identifiers to ClinicalTrials.gov. <br>
Mitigation: Avoid confidential competitive-intelligence queries unless those query terms are acceptable to send to ClinicalTrials.gov. <br>
Risk: Python dependencies and network execution introduce normal supply-chain and network risks. <br>
Mitigation: Install in a virtual environment, pin or audit dependencies before use, and keep execution within an approved workspace. <br>
Risk: Trial status summaries depend on upstream ClinicalTrials.gov data and may not reflect every internal business or regulatory development. <br>
Mitigation: Treat generated summaries as monitoring aids and verify material decisions against primary trial records and appropriate domain review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/clinicaltrials-gov-parser) <br>
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api) <br>
- [API docs](references/api-docs.md) <br>
- [Usage examples](references/examples.md) <br>
- [Status codes](references/status-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, CSV/table-style CLI text, and Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses HTTPS requests to ClinicalTrials.gov API v2 and can emit JSON trial records or summary reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
