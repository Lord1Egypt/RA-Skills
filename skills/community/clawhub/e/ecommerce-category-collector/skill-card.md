## Description:

Automates Audtools e-commerce category collection by reading CSV collection links, logging in, submitting collection jobs, and optionally selecting and exporting collected items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qirongzhang](https://clawhub.ai/user/qirongzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Operators or developers with authorized Audtools access use this skill to validate CSV files of e-commerce collection URLs, submit category collection tasks, and optionally export collected products in bulk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes hard-coded Audtools login credentials that should be treated as compromised.

Mitigation: Rotate the exposed credential and require credentials from environment variables, a secret manager, or an interactive prompt before use.

Risk: The skill performs bulk export actions by default.

Mitigation: Require explicit confirmation before export, prefer test mode or --no-export first, and run only with an authorized least-privileged Audtools account.

## Reference(s):

- [CSV Format Reference](references/csv-format.md)
- [ClawHub Skill Page](https://clawhub.ai/qirongzhang/skills/ecommerce-category-collector)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, CSV examples, and operational logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts CSV file or directory paths and command options for item count, interval, close delay, test mode, and export suppression.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact package.json and README.md show 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
