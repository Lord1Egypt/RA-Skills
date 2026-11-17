## Description:

Query and analyze Tencent Cloud CLS logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbwang0130](https://clawhub.ai/user/dbwang0130)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to list Tencent Cloud CLS log topics, query logs, and retrieve context around specific log entries with clscli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI.

Mitigation: Review the clscli source and installation path before use, and prefer a pinned, verified release.

Risk: The skill uses Tencent Cloud credentials to access potentially sensitive logs.

Mitigation: Use a dedicated least-privilege Tencent Cloud identity scoped to the required CLS regions, logsets, and topics.

Risk: Exported log query results may contain sensitive data.

Mitigation: Treat exported JSON or CSV files as sensitive data and avoid keeping long-lived credentials globally exported.

## Reference(s):

- [Tencent Cloud CLS API Documentation](https://cloud.tencent.com/document/api/614/56474)
- [ClawHub skill page](https://clawhub.ai/dbwang0130/skills/clscli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON or CSV CLI output from clscli.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
