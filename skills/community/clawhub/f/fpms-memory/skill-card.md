## Description:

Cognitive memory engine that gives an AI assistant persistent work tracking, proactive risk alerts, and cross-conversation continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeff0052](https://clawhub.ai/user/jeff0052)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add local project memory, task tracking, decision logs, and risk alerts across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly persist conversation-derived project, task, and decision data.

Mitigation: Use it only in workspaces where automatic project memory is acceptable, and avoid discussing secrets or highly sensitive information while it is active.

Risk: The setup installs an unpinned focalpoint MCP server package.

Mitigation: Verify the focalpoint package source and version before installation, and pin an approved version where operational policy requires reproducible installs.

Risk: Optional GitHub sync may expand the data and permission surface.

Mitigation: Require narrow GitHub permissions if sync is enabled, and review which repositories or issues are allowed to synchronize.

## Reference(s):

- [Project homepage](https://github.com/jeff0052/founderOSclaudecode)
- [Full documentation](https://github.com/jeff0052/founderOSclaudecode/blob/main/docs/USAGE-GUIDE.md)
- [PyPI package](https://pypi.org/project/fpms/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist conversation-derived project, task, and decision data through a local MCP memory service.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
