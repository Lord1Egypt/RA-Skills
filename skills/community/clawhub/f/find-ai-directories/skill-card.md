## Description:

Finds, ranks, and shortlists directories where users can submit AI tools, AI apps, AI agents, or agent skills and plugins for backlinks, referral traffic, and discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nostrband](https://clawhub.ai/user/nostrband)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, growth teams, and developers use this skill to identify AI-focused directory and registry sites, rank them by authority signals, and decide which listings to unlock for submission guidance and traffic details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST authentication example sources .env.local from the project directory, which can execute project-controlled shell code.

Mitigation: Prefer the OAuth/MCP path, a trusted secret manager, or an already-exported SERVICEGRAPH_API_KEY; do not run the wrapper that sources .env.local.

Risk: Unlocking directory rows can spend credits.

Mitigation: Confirm paid unlocks with the user before making unlock requests and state the credit cost and 30-day TTL before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nostrband/skills/find-ai-directories)
- [Publisher profile](https://clawhub.ai/user/nostrband)
- [ServiceGraph API](https://api.servicegraph.co)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples and concise ranked recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filters, ranked directory shortlists, unlock cost notes, submission guidance, and credential setup guidance.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
