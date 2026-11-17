## Description:

Create business planning records from the command line by logging, searching, and exporting local entries for planning workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators can use this skill to install and run a Bash-based local logging utility for business planning notes, queries, transformations, searches, status checks, and exports. It should be treated as a local data logger rather than a generator of complete business plans or financial projections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the package behaves as a local business-data logger rather than the advertised business-plan generator.

Mitigation: Present it as a logging utility, validate behavior before relying on it for planning deliverables, and do not expect generated business plans or financial projections.

Risk: The security guidance says user-entered business, investor, customer, or financial data may remain in plaintext logs under ~/.local/share/bizplanner.

Mitigation: Avoid confidential inputs unless storage permissions, retention, deletion, and export controls are hardened for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/bizplanner)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Files, Configuration, Guidance]

**Output Format:** [Markdown and shell command guidance for a Bash CLI that writes local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates plaintext local data under ~/.local/share/bizplanner and can export accumulated entries to JSON, CSV, or text.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
