## Description:

AnyGen图表生成-专业版 helps enterprise teams and professional users generate, batch process, template, share, and export diagrams through AnyGen CLI and API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, product teams, and enterprise documentation teams use this skill to produce architecture diagrams, flowcharts, reusable diagram templates, and diagram assets for technical and business documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad CLI/API workflows and team asset write paths that can affect files, repositories, or shared diagram assets.

Mitigation: Review exact commands, input directories, output paths, remote repositories, and team asset targets before execution.

Risk: Diagram prompts and source documents may be sent to an external AnyGen API.

Mitigation: Avoid sending confidential architecture, product, customer, or internal documentation details unless organizational policy permits it.

Risk: API credentials are required and could be exposed through hardcoded examples, shell history, logs, or shared configuration.

Mitigation: Store API keys in approved secret management or environment variables, and avoid committing credentials or generated logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anygen-diagram-tool-pro)
- [AnyGen diagrams API endpoint](https://api.anygen.io/v1/diagrams)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API examples, configuration values, and generated diagram file targets such as PNG, SVG, PDF, and Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AnyGen Pro API access, AnyGen CLI, Python 3.9+, Git, and configured API credentials for execution-oriented workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
