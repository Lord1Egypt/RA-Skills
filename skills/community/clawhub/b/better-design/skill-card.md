## Description:

Guides coding agents to use Better Design's remote design systems, UI and UX principles, icons, and review checks when building interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvkr](https://clawhub.ai/user/marvkr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to choose and install design systems, build app and site interfaces, and review accessibility, copy, and spacing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A React or Next.js install command returned by the remote service could change project files without clear limits or approval.

Mitigation: Before running it, show the exact command, package sources, destination paths, and files to be changed; require user approval after checking that they match the project.

Risk: Using the remote design provider can disclose private source, fixtures, or unreleased product details.

Mitigation: Avoid sending sensitive project material unless the user accepts the provider's account and data terms.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/marvkr/skills/better-design)
- [Better Design homepage](https://better-design.com)
- [Better Design MCP installation guide](https://better-design.com/mcp/install)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include design-system selections and interface review findings.]

## Skill Version(s):

1.0.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
