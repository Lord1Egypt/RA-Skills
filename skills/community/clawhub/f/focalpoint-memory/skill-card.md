## Description:

FocalPoint provides local project memory, attention management, workflow orchestration, workbench context preparation, and Three-Province review for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeff0052](https://clawhub.ai/user/jeff0052)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an MCP-compatible assistant persistent local project memory, work tracking, role-filtered context, and review workflows across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create durable local project memory, knowledge, and logs automatically.

Mitigation: Use it only for projects where persistent memory is intended, and avoid storing secrets, credentials, regulated data, or other sensitive information.

Risk: The configured install path uses an unpinned external MCP package.

Mitigation: Review the focalpoint package before installation and prefer a pinned, isolated environment.

Risk: Automatic memory loading and writing can affect every conversation in an enabled agent environment.

Mitigation: Define explicit rules for when memory may be loaded or written, and periodically review saved knowledge and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeff0052/skills/focalpoint-memory)
- [Project homepage](https://github.com/jeff0052/founderOSclaudecode)
- [PyPI package](https://pypi.org/project/focalpoint/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for installing and using a local MCP memory server.]

## Skill Version(s):

0.3.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
