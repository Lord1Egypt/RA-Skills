## Description:

Auto Revolution provides structured task templates, review prompts, safety scanning, task state updates, and logging for human supervised multi step workflows without autonomous background execution or arbitrary shell instruction execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and review structured task JSON, manage queued task state, scan instruction text for risky shell patterns, and keep supervised workflow logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can modify task state and workflow logs.

Mitigation: Run the skill only in a restricted workspace with limited filesystem access and review task changes before relying on them.

Risk: Untrusted task IDs, note text, or reference file paths may be abused by helper scripts.

Mitigation: Avoid running unblock or force-unlock helpers with untrusted inputs until task IDs are validated and reference files are constrained to approved project paths.

Risk: Generated instructions may be incorrect or unsafe if treated as executable work.

Mitigation: Keep a human in the loop and review generated instructions before any real execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/auto-revolution)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Task schema](task-schema.json)
- [Model role configuration](config/models.json)
- [Script guide](scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON task structures and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces supervised task workflow artifacts and prompts; does not include autonomous execution.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
