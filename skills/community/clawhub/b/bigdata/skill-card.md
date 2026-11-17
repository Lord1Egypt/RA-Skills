## Description:

Split large files, run parallel processing, and stream batch analysis for dataset sampling, log aggregation, and bulk data transformation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to record, search, summarize, and export local notes about data pipeline steps, schemas, validation checks, profiling results, and related workflow activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may record dataset names, SQL, schemas, file paths, customer information, or secrets in local plaintext history.

Mitigation: Avoid entering secrets or personal data, redact sensitive values before logging, restrict local file permissions, and delete or rotate logs according to the user's retention policy.

Risk: The release summary overstates processing capabilities relative to the local logging behavior described by the security evidence.

Mitigation: Treat the skill as a workflow logging and review helper unless its processing behavior is independently verified before operational use.

## Reference(s):

- [ClawHub Bigdata skill page](https://clawhub.ai/bytesagain3/skills/bigdata)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create or update local plaintext logs under ~/.local/share/bigdata when executed.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
