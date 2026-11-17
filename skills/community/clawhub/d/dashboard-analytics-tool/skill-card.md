## Description:

仪表盘分析工具 wraps dashboard analytics API calls so agents can turn Chinese instructions and request parameters into structured API response data for analytics, reporting, statistical insight, and visualization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams use this skill to call dashboard analytics APIs, convert request parameters into structured responses, and generate analysis or reporting outputs from supported data sources. The artifact says it is not suitable for real-time stream data processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill requests broad file, command, and API authority.

Mitigation: Run it only in trusted workspaces, review file writes and shell commands before execution, and limit available credentials and filesystem access to the minimum needed.

Risk: The skill uses an API key and may call external APIs.

Mitigation: Provide API keys through environment variables or a secrets manager, avoid committing credentials, and restrict keys by scope, service, and rotation policy.

Risk: The security evidence notes inconsistent limits and data-retention statements.

Mitigation: Use non-sensitive data until the publisher clarifies supported real-time behavior, CRUD scope, command and write confirmation, and log or data retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dashboard-analytics-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured success/data/error responses, API configuration guidance, troubleshooting steps, and command examples for environment setup.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.7.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
