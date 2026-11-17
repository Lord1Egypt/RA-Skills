## Description:

Helps agents read, create, edit, validate, and visually QA PowerPoint presentations using PPTX workflows, design guidance, and supporting Office document scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, analysts, and presentation authors use this skill to inspect, edit, build, and quality-check PowerPoint decks from templates or from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses local execution patterns while handling Office presentation files.

Mitigation: Review proposed commands before execution and use an isolated workspace or container for untrusted presentations.

Risk: The skill documentation includes mutable global package installation guidance.

Mitigation: Prefer project-local or sandboxed dependency installation and pin versions where practical.

Risk: The trigger is broad for any PPTX-related task, and the bundle includes Office document helpers beyond PPTX.

Mitigation: Limit use to intended presentation workflows and review requested file operations before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/anthropic-pptx)
- [PPTX skill instructions](artifact/SKILL.md)
- [Editing presentations guide](artifact/editing.md)
- [PptxGenJS tutorial](artifact/pptxgenjs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands, plus generated or edited PPTX files when the agent applies the workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Office document artifacts and image or PDF previews during QA workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
