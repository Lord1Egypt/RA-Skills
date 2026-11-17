## Description:

Collect Indeed company records by company-list URL, keyword, industry and state, or company URL, excluding Indeed job listings and Glassdoor company URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and monitor Dataify collection tasks that retrieve Indeed company profile data by list URL, keyword, industry/state, or company URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataify receives collection parameters and uses the configured Dataify API token.

Mitigation: Install and run the skill only when that data sharing is acceptable, and use a proper secret manager or session-scoped environment variable for the token.

Risk: Credential setup guidance could encourage long-lived shell-profile token storage.

Mitigation: Prefer session-scoped environment variables, avoid pasting tokens into chat or command lines, and avoid the Chinese persistent shell-profile setup commands.

Risk: The result-waiting workflow relies on an external local dataify-task-operations dependency.

Mitigation: Review and trust that dependency as part of the runtime before using workflows that wait for final results.

## Reference(s):

- [Dataify Indeed Companies Info API Reference](references/indeed_companies_info_api.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-indeed-companies-info)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown responses with optional shell commands and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit Dataify builder tasks and wait for asynchronous results when a valid DATAIFY_API_TOKEN is available.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
