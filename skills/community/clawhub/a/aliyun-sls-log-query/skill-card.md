## Description:

Use when querying or troubleshooting logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to query and troubleshoot Alibaba Cloud SLS logs for time-bounded search, error investigation, aggregation, and root-cause analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Alibaba Cloud SLS using user-provided Alibaba Cloud credentials and endpoint settings.

Mitigation: Use a dedicated read-only RAM identity, prefer short-lived credentials, and set SLS_ENDPOINT only to a trusted Alibaba Cloud SLS endpoint.

Risk: Returned SLS logs may contain sensitive operational or customer data.

Mitigation: Limit time ranges and result counts, and avoid saving or sharing raw log output when logs contain sensitive data.

Risk: Unpinned SDK dependencies can change behavior over time.

Mitigation: Pin the aliyun-log-python-sdk version before operational use.

## Reference(s):

- [SLS query and analysis syntax notes](references/query-syntax.md)
- [Python SDK basic usage](references/python-sdk.md)
- [SLS troubleshooting query templates](references/templates.md)
- [Reference source list](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python code blocks; bundled scripts emit JSON lines from SLS responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include raw log fields and query summaries; users should avoid saving or sharing sensitive log data.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
