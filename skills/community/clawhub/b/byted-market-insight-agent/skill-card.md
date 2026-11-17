## Description:

Byted Market Insight Agent lets agents call Volcengine market-insight services to list monitoring tasks, pull AI-filtered public content, and query AI-generated business leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve brand, competitor, topic, and industry monitoring data from Volcengine market-insight services, then use the returned results for market analysis and lead discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Volcengine or Gateway credentials and market-insight data.

Mitigation: Use it only in environments where granting that credential and data access is acceptable, and prefer explicit environment variables or a secure secret store.

Risk: Automatic dependency installation can change the runtime environment.

Mitigation: Disable automatic pip installation unless the dependency source and package version are approved.

Risk: A custom Gateway URL could send requests and credentials to an untrusted destination.

Mitigation: Use a custom Gateway URL only after verifying and trusting the destination.

## Reference(s):

- [Usage and Integration Guide](references/usage.md)
- [API Differences](references/api-diff.md)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON API results and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns monitoring task lists, filtered post records, pagination tokens, and structured lead records.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
