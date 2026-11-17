## Description:

Greek social security (EFKA) integration — employee records, contribution calculations, APD declarations. Human approval for submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers, payroll operators, and accounting teams use this skill to configure EFKA-oriented workflows for Greek employee records, contribution calculations, APD declaration preparation, deadline monitoring, and human-approved submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: EFKA submission, registration, payment, Slack, or calendar workflows may be live unless dry-run behavior is confirmed.

Mitigation: Confirm dry-run defaults before installation, test in a controlled environment, and require explicit human approval before any regulated submission or payment action.

Risk: EFKA credentials and employee identifiers could be exposed through shell history, shared files, logs, or committed configuration.

Mitigation: Use managed secret injection, avoid plaintext credentials in commands or files, restrict access to payroll data directories, and review logging before using real employee data.

Risk: Four-eyes approval and external-access boundaries are described, but security evidence says they need review.

Mitigation: Verify the technical enforcement of approval status, role separation, audit records, and outbound integrations before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/satoshistackalotto/skills/efka-api-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference file paths under OPENCLAW_DATA_DIR and optional Slack or calendar integration settings.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
