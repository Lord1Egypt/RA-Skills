## Description:

Guides agents through Alibaba Cloud CMH/APDS database evaluation with the Rainmeter collector, including read-only collection account setup, collector execution guidance, data package upload steps, and generation of profiling, compatibility, target selection, risk, and migration reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database administrators, and migration engineers use this skill to plan and run Alibaba Cloud CMH/APDS database evaluation workflows for Oracle and other supported source databases. It helps produce collector commands, account setup SQL, operational guidance, and report-oriented summaries for migration assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad activation and mandatory output-control rules that may influence wording and add branding to generated outputs.

Mitigation: Review generated text before use, especially public-facing reports, and confirm that required terminology and footer language are appropriate for the deployment context.

Risk: The workflow can produce database account SQL, collector execution commands, and data package upload steps.

Mitigation: Require explicit user confirmation before running any SQL or collector command, use temporary least-privilege read-only accounts, verify the collector checksum from APDS, inspect data.zip before upload, and upload only through the official APDS console.

## Reference(s):

- [RAM Permission Statement](references/ram-policies.md)
- [Alibaba Cloud APDS database evaluation console](https://apds.console.aliyun.com/<region>/db/db-evaluation/collect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline SQL and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database-specific SQL, collector commands, evaluation report summaries, and mandatory CMH/Rainmeter terminology in generated prose.]

## Skill Version(s):

0.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
