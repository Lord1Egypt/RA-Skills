## Description:

AnyGen Suite helps agents use the AnyGen CLI to create slides, documents, diagrams, websites, images, research, data visualizations, financial analysis, and related content through AnyGen's server-side service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route content-generation requests to AnyGen for presentations, documents, diagrams, websites, images, research, and data analysis. It is intended for normal ClawHub use with an AnyGen CLI installation and ANYGEN_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and files may be sent to AnyGen's remote service during content generation.

Mitigation: Use a narrowly scoped, revocable ANYGEN_API_KEY and avoid regulated or confidential data unless approved.

Risk: The skill can install the anygen-workflow-generate skill without pinning or review.

Mitigation: Review or pin @anygen/cli and anygen-workflow-generate before allowing secondary skill installation.

Risk: Broad activation for many content-generation requests could route unintended user content to the service.

Mitigation: Confirm user intent and data sensitivity before running AnyGen commands.

## Reference(s):

- [ClawHub Skill: AnyGen Suite](https://clawhub.ai/logictortoise/skills/anygen-skill)
- [ClawHub Publisher: logictortoise](https://clawhub.ai/user/logictortoise)
- [AnyGen service](https://www.anygen.io)
- [AnyGen CLI package](https://www.npmjs.com/package/@anygen/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell-command guidance for invoking AnyGen CLI workflows; generated downstream artifacts may include documents, slides, diagrams, websites, images, reports, and visualizations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AnyGen CLI and ANYGEN_API_KEY; generated content may be created server-side at www.anygen.io.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
