## Description:

创建和管理 OpenClaw 插件使用 before_prompt_build hook。触发词：'create plugin'、'add hook'、'inject context'、'modify gateway'。适用于使用 hook 系统扩展 OpenClaw 功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, register, and manage OpenClaw plugins that add hooks such as before_prompt_build, after_response, and on_error.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: before_prompt_build hooks can change system context or user messages across future OpenClaw runs.

Mitigation: Review hook code carefully before enabling generated or modified plugins.

Risk: Plugin changes can affect prompt construction behavior.

Mitigation: Install only when the intended use is authoring OpenClaw plugins that modify prompt-building behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for plugin directory layout, plugin manifest configuration, hook code, and OpenClaw plugin commands.]

## Skill Version(s):

1.0.0 (source: release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
