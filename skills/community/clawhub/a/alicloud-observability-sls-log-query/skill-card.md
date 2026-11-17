## Description:

Query and troubleshoot logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to compose time-bounded Alibaba Cloud SLS queries, run SDK-backed log searches, and investigate errors or latency patterns across one or more logstores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned SLS logs may contain secrets, personal data, internal tokens, or other sensitive operational data.

Mitigation: Review query scope before execution, avoid broad searches on sensitive logstores, and treat script output as sensitive evidence.

Risk: Alibaba Cloud credentials used by the scripts can grant access beyond the intended project or logstore.

Mitigation: Use read-only credentials scoped to the required SLS projects and logstores, preferably in a dedicated virtual environment.

Risk: A misconfigured endpoint can query the wrong Alibaba Cloud region or environment.

Mitigation: Verify SLS_ENDPOINT, SLS_PROJECT, and SLS_LOGSTORE before running queries or troubleshooting templates.

## Reference(s):

- [SLS Query and Analysis Syntax Notes](references/query-syntax.md)
- [Python SDK Basic Calls](references/python-sdk.md)
- [SLS Troubleshooting Query Templates](references/templates.md)
- [Source List](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python snippets; bundled scripts emit JSON lines for returned log rows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alibaba Cloud SLS endpoint, project, logstore, and access-key environment variables when executing the bundled scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
