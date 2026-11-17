## Description:

Experience Manager creates, learns, lists, searches, and publishes OpenClaw experience packages so agents can retain and share reusable practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlx](https://clawhub.ai/user/zlx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to package lessons learned into reusable OpenClaw experience ZIP files, apply experience packages to current or specified agents, and search or publish packages through Experience Hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or arbitrary experience packages can be imported into persistent agent instructions.

Mitigation: Install only in a trusted OpenClaw environment, use dry-run, avoid --yes, and review every package reference before applying it.

Risk: Generated ZIP packages may include or derive local memories and agent configuration.

Mitigation: Review generated ZIP contents before publishing.

Risk: Cross-agent operations can modify another agent workspace.

Mitigation: Avoid cross-agent operations unless you explicitly intend to modify that agent workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zlx/skills/experience-manager)
- [Experience Hub API](https://www.expericehub.com:18080)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and text guidance with shell commands, generated ZIP files, and OpenClaw configuration changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create experience ZIP packages, update local experience indexes, or apply learned content to agent instruction files after user confirmation.]

## Skill Version(s):

1.3.1 (source: server release and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
