## Description:

Generate standardized experiment templates for Electronic Laboratory Notebooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, lab informatics staff, and research teams use this skill to generate structured Markdown templates for Electronic Laboratory Notebook experiment records across general, molecular biology, chemistry, cell culture, and animal study workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --output option can overwrite writable files, including paths outside the intended workspace.

Mitigation: Prefer stdout or a clearly workspace-relative output path, and do not let untrusted input choose --output until path validation and overwrite protection are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/eln-template-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands]

**Output Format:** [Markdown templates printed to stdout or written to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports template type, title, researcher, date, project, and output path arguments.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
