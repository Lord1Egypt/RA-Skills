## Description:

Queries Alibaba Cloud Log Service (SLS) logs for a specified project and logstore, including time-window filtering and SQL analysis queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunr-tg](https://clawhub.ai/user/yunr-tg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to generate Alibaba Cloud SLS CLI queries for retrieving logs, filtering by time range, and running SQL-style log analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles cloud log access and may include command-line credential parameters.

Mitigation: Use least-privilege Alibaba Cloud credentials, prefer configured profiles or secure credential providers, and avoid placing AccessKey secrets or STS tokens in chat or command history.

Risk: Unsafe command templates can be risky when query parameters or shell metacharacters come from untrusted input.

Mitigation: Review generated commands before execution and ensure parameters are trusted and safely quoted or passed as structured process arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunr-tg/skills/aliyun-sls-query)
- [Publisher profile](https://clawhub.ai/user/yunr-tg)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target aliyunlog log get_log and may return SLS data and meta fields in JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
