## Description:

Automates Adobe After Effects using ExtendScript (.jsx) files and aerender CLI. Supports composition creation, effect application, batch rendering, project templates, and Adobe Media Encoder workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camel-255](https://clawhub.ai/user/camel-255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motion graphics engineers use this skill to automate Adobe After Effects compositions, effects, render queues, and command-line rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch rendering can write outputs outside the intended folder when composition names contain unsafe path components.

Mitigation: Run the batch render script only on trusted projects, avoid composition names containing path separators or '..', choose output folders carefully, and inspect render queue output paths before rendering.

Risk: After Effects automation can modify project structure, compositions, effects, and render queues.

Mitigation: Review generated ExtendScript and run it on backups or disposable project copies before using it on production project files.

## Reference(s):

- [After Effects ExtendScript API Reference](references/extendscript_api.md)
- [ClawHub skill page](https://clawhub.ai/camel-255/skills/after-effects-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/camel-255)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with ExtendScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Adobe After Effects project, render queue, and output path guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
