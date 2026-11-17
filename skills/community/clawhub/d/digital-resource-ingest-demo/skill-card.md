## Description:

数字资源入库演示技能演示如何通过 TaskFlow 编排业务流程后，将数字内容发布到 ClawHub 资源中心。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams managing digital resources use this Chinese-language demo to model a TaskFlow-based intake process, prepare required metadata, publish content to ClawHub, and verify that the resource can be found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can change ClawHub resource-center state.

Mitigation: Review the content and metadata before running `clawhub publish`.

Risk: The workflow is written in Chinese, which may make review difficult for users who cannot read the instructions.

Mitigation: Use it only when reviewers are comfortable with the Chinese-language workflow or have translated it accurately.

## Reference(s):

- [metadata-template.yaml](references/metadata-template.yaml)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/digital-resource-ingest-demo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and a YAML metadata template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance for publishing digital resources to ClawHub.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
