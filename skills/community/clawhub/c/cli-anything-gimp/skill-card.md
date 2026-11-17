## Description:

Enables agents to control GIMP through CLI-Anything for image creation, layer editing, canvas changes, filters, drawing, exports, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sly27](https://clawhub.ai/user/sly27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate GIMP image-editing workflows from the command line, including project setup, layer operations, filters, drawing, export, and batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable local dependency installation can execute code from the local CLI-Anything agent-harness source.

Mitigation: Install only in a dedicated virtual environment and verify the local agent-harness source before running the editable install.

Risk: Image export commands can overwrite existing files when output paths collide.

Mitigation: Choose output filenames carefully and review target paths before exporting generated or edited images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sly27/skills/cli-anything-gimp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text, Files]

**Output Format:** [Markdown guidance with shell commands; CLI output may be human-readable text or JSON, and image exports are written as files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local GIMP installation and the documented CLI-Anything GIMP environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
