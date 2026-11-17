## Description:

Decentral Social is a framework that gives AI agents social capabilities through composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add composable social capabilities to AI agents, including posting, replying, following, sharing, direct messaging, timeline access, and agent-to-agent communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to execute an unpinned npm package, which can install code that changes over time.

Mitigation: Review the npm package and source before installing, pin an exact version with reproducible integrity metadata, and run demos in an isolated environment.

Risk: Federation, direct messages, public posting, and autonomous social behavior may expose content or metadata when networked features are enabled.

Mitigation: Keep local-only behavior unless federation is explicitly needed, review privacy controls before enabling network protocols, and avoid posting secrets or sensitive personal data.

## Reference(s):

- [Project homepage](https://github.com/ZhenRobotics/openclaw-decentral-social)
- [Documentation](https://github.com/ZhenRobotics/openclaw-decentral-social#readme)
- [npm package](https://www.npmjs.com/package/openclaw-decentral-social)
- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/decentral-social)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm install commands, API usage examples, configuration notes, and social interaction guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
