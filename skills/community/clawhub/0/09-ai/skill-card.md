## Description:

AI-assisted programming guidance that helps Claude learn how to create and use OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to learn how to structure SKILL.md files, organize supporting documentation, and teach an agent when and how to use provided tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad conversational trigger examples could lead users to rely on vague remembered instructions for tool use.

Mitigation: Use specific trigger phrases and require confirmation before sensitive tool calls.

Risk: Example dependency installation commands do not pin package versions.

Mitigation: Install dependencies in a virtual environment with reviewed pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/09-ai)
- [OpenClaw learning guide](guides/OpenClaw如何学习文档说明.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language tutorial content; no executable payload is included.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
