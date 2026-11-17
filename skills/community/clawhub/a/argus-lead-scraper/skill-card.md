## Description:

Extracts verified B2B leads (name, email, company, LinkedIn, job title) from target sources and exports them as CRM-ready CSV files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and operations teams use this skill to generate filtered B2B lead lists and export deduplicated records for CRM import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a LinkedIn session cookie, which is a live account credential.

Mitigation: Store LI_SESSION only in an approved secrets manager, limit access to authorized operators, rotate or revoke it after use, and avoid sharing it in prompts, logs, or output files.

Risk: Bulk collection of personal lead data can create privacy, contractual, and compliance exposure.

Mitigation: Run the skill only with clear authorization for the target sources, prefer official APIs or approved providers, and define retention, deletion, and CSV-sharing controls before collection.

Risk: The artifact describes throttling to avoid detection and saving raw data before cleaning.

Mitigation: Require review of target-source terms, approved collection limits, and raw-data storage controls before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/argus-lead-scraper)
- [ClawHub publisher profile](https://clawhub.ai/user/neo1307)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated CSV file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces UTF-8 CRM-ready CSV files and a run summary with totals, duplicate removals, and validation pass rate.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
