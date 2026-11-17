## Description:

Deploy HTML content to EdgeOne Pages, return the public URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcp](https://clawhub.ai/user/mcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish supplied HTML or text content to EdgeOne Pages and receive a public URL for access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes supplied content to a public URL.

Mitigation: Do not deploy secrets, credentials, private documents, or internal data through this skill.

Risk: The install path relies on the current npm release of mcporter rather than a pinned package version.

Mitigation: Review the npm package before use and prefer pinning a trusted version in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcp/skills/edgeone)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment commands and guidance that result in a public URL for submitted content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
