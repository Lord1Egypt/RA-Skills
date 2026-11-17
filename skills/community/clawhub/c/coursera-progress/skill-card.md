## Description:

Fetch and display Coursera course enrollment, completion progress, grades, certificates, and upcoming deadlines using the Coursera API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elmoorish](https://clawhub.ai/user/elmoorish)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and agents assisting learners use this skill to check Coursera enrollments, course progress, grades, earned certificates, and upcoming assignment deadlines. It also supports public Coursera course lookup when personal API credentials are not available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coursera credentials and private learning records could be exposed through chat, logs, or overly broad access.

Mitigation: Use least-privilege and short-lived Coursera credentials where possible, avoid pasting secrets into chat, and rotate or revoke tokens after use.

Risk: Shell-based API examples can mishandle user-provided search terms or expose tokens if commands are copied without review.

Mitigation: Review commands before execution, URL-encode search terms, and keep tokens in authorization headers or environment variables instead of logs.

## Reference(s):

- [Coursera API credential setup](https://www.coursera.org/account/api)
- [Coursera API base endpoint](https://api.coursera.com/api)
- [ClawHub skill listing](https://clawhub.ai/elmoorish/skills/coursera-progress)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks, API call examples, and formatted progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; personal progress, grades, certificates, and deadlines require Coursera credentials.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
