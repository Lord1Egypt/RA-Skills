## Description:

生成配置拉取代码模板，用于在 Android 项目中接入配置中心、白名单、单独接口或推拉结合的配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hefuwei-95](https://clawhub.ai/user/hefuwei-95)

### License/Terms of Use:

MIT-0

## Use Case:

Android developers use this skill to generate Kotlin/Java templates for configuration fetch workflows, including config-center, whitelist, standalone API, and push-pull integration paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated app code may be written into the workspace without clear safeguards for confirmation or overwrites.

Mitigation: Review generated diffs before keeping changes and only install the skill when workspace modification is expected.

Risk: Untrusted names, keys, URLs, or JSON fields may produce unsafe or invalid generated code.

Mitigation: Validate or escape template values before compiling generated code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hefuwei-95/skills/config-pull-template)
- [api-template.md](references/api-template.md)
- [config-center-template.md](references/config-center-template.md)
- [push-pull-template.md](references/push-pull-template.md)
- [whitelist-template.md](references/whitelist-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Kotlin/Java code templates and generated workspace file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code should be reviewed before it is kept or compiled.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
