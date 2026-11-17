## Description:

Helps users find, compare, and select OpenClaw skills from the Clawhub marketplace based on their tasks, output needs, and troubleshooting context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthwalking](https://clawhub.ai/user/earthwalking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and OpenClaw users use this skill to identify suitable marketplace skills, compare options for a task, and get concise usage or troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published artifacts may expose credential-shaped Clawhub and WeChat secrets.

Mitigation: Install only after the publisher removes those artifacts or secrets and rotates any affected credentials.

Risk: Publishing and upload workflows are bundled into a skill-search guide, which can broaden the skill beyond discovery tasks.

Mitigation: Narrow activation to explicit skill-discovery requests and move publishing workflows into a separately scoped publishing skill with confirmation and secret-handling guidance.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the evidence security summary and scan the release before deployment; treat skill recommendations and command examples as guidance that must be checked before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/earthwalking/skills/clawhub-skill-search)
- [Publisher Profile](https://clawhub.ai/user/earthwalking)
- [ClawHub Marketplace](https://clawhub.ai/skills)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Skill Development Guide](https://docs.openclaw.ai/skills/creating)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline command examples and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended skill names, task-to-skill mappings, troubleshooting steps, and command templates.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
