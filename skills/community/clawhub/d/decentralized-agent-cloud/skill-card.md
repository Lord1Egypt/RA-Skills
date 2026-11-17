## Description:

Decentralized compute and data marketplace for AI agents with spot pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to discover, configure, and route compute or data-processing work through a decentralized marketplace with spot pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned npm package.

Mitigation: Use a pinned package version or lockfile and review the package before installation.

Risk: Prompts, scripts, and datasets may be routed through a decentralized provider marketplace with unclear privacy and trust boundaries.

Mitigation: Run in a least-privileged environment and avoid submitting secrets, private datasets, regulated data, or sensitive prompts until the provider's data handling, retention, and compliance protections are verified.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhenstaff/skills/decentralized-agent-cloud)
- [Project homepage](https://github.com/openclaw/openclaw-decentralized-agent-cloud)
- [Project documentation](https://github.com/openclaw/openclaw-decentralized-agent-cloud#readme)
- [npm package](https://www.npmjs.com/package/openclaw-decentralized-agent-cloud)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation guidance, SDK usage examples, marketplace concepts, and provider-registration examples.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; SKILL.md frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
