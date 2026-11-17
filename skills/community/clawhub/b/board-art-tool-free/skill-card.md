## Description:

画板艺术工具 helps agents guide users through publishing, viewing, locating, and managing personal pixel art on a shared collaborative canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare pixel-art JSON, choose canvas coordinates, run publish/view/locate/export workflows, and manage personal artwork history on a shared canvas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording could cause the skill to run for requests outside the intended shared-canvas pixel-art workflow.

Mitigation: Review or narrow the trigger text before installation and use the skill only for the intended canvas pixel-art workflow.

Risk: State-changing publish or delete guidance can modify canvas content.

Mitigation: Confirm each publish or delete action before execution and review generated commands before running them.

Risk: Canvas service tokens may grant access beyond the current task.

Mitigation: Provide only a scoped canvas service token through the environment and avoid placing tokens in files or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/board-art-tool-free)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce canvas publish, view, locate, and export commands, plus pixel-art JSON structures.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
