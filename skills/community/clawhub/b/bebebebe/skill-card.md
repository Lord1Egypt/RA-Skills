## Description:

Set up Orthogonal for your AI agent - access premium APIs and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and authenticate the Orthogonal CLI, discover skills and APIs, and route external API or OAuth integration tasks through Orthogonal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install skills and use paid APIs or OAuth-connected accounts.

Mitigation: Review installed skills before use, prefer pinned or local installs, and confirm account scope and billing impact before execution.

Risk: The skill includes workflows that can send messages, modify cloud data, create GitHub objects, or delete account content.

Mitigation: Require explicit user approval before any state-changing integration action and verify endpoint parameters with orth api show before running commands.

Risk: Credential handling can expose API keys if users choose manual setup.

Mitigation: Use orth login when possible, protect local credential files and environment variables, and rotate keys if exposure is suspected.

## Reference(s):

- [Orthogonal Homepage](https://orthogonal.com)
- [Orthogonal Documentation](https://docs.orthogonal.com)
- [Orthogonal Skills](https://orthogonal.com/skills)
- [Orthogonal API Discovery](https://orthogonal.com/discover)
- [Orthogonal Integrations](https://orthogonal.com/integrations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI commands, setup steps, API discovery workflow, authentication guidance, billing guidance, and OAuth integration examples.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
