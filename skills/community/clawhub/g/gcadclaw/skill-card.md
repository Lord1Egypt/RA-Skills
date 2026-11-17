## Description:

Generate, modify, validate, and repair 2D GstarCAD engineering drawings from natural-language requirements using pygcadwin, with DWG output, screenshot evidence, and entity feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gstarcad](https://clawhub.ai/user/gstarcad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CAD automation users, and engineering teams use this skill to create or modify 2D GstarCAD DWG drawings for mechanical parts, assemblies, and engineering layouts from natural-language prompts. The skill also guides the agent to capture before/after entity evidence, screenshots, and repair notes before reporting completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs or upgrades pygcadwin from PyPI without exact version or hash verification.

Mitigation: Review or pin the pygcadwin dependency before setup, run installation from a non-elevated terminal, and install only inside a project/work directory intended for skill writes.

Risk: Drawing execution depends on a live Windows GstarCAD COM environment, so missing registration or unavailable CAD software can prevent completion.

Mitigation: Validate the environment with scripts/validate_env.py before use and report partial completion if GstarCAD, COM access, save, entity capture, or screenshot validation fails.

## Reference(s):

- [GcadClaw Skill Page](https://clawhub.ai/gstarcad/skills/gcadclaw)
- [pygcadwin PyPI Project](https://pypi.org/project/pygcadwin/)
- [2D pygcadwin workflow](references/2d-pygcadwin-workflow.md)
- [Feedback loop](references/feedback-loop.md)
- [Python package manifest](references/python_package_manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and code-oriented instructions that may produce DWG files, JSON feedback artifacts, PNG screenshots, and shell commands during use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Python, live GstarCAD registered as a COM server, and the pygcadwin package from PyPI for drawing execution.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
