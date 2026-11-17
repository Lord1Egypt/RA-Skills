## Description:

AI content platform CLI - create workspaces, manage SEO keywords, generate article suggestions, write articles, and publish to WordPress, Webflow, Wix, GoHighLevel, or webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincenzor](https://clawhub.ai/user/vincenzor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and site operators use this skill to operate the Balzac CLI for workspace setup, SEO keyword management, article generation, Markdown export, and publishing through supported CMS or webhook integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Balzac API key, which could expose account access if pasted into logs, prompts, or shell history.

Mitigation: Provide BALZAC_API_KEY through an environment variable or secret manager, and avoid passing the key as a command argument.

Risk: Generated articles, integration IDs, or webhook targets could publish incorrect content or affect connected sites.

Mitigation: Review generated articles and confirm integration IDs before publishing or triggering webhooks.

Risk: The workflow depends on the external balzac-cli package and the user's Balzac account.

Mitigation: Install only from trusted sources, preferably with a pinned or locally reviewed package version.

## Reference(s):

- [Balzac Developer Documentation](https://developer.hirebalzac.ai)
- [Balzac API Keys](https://app.hirebalzac.ai/api_keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI usage patterns when advising scriptable Balzac commands.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
