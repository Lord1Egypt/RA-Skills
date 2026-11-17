## Description:

Autonomous bug diagnosis and repair. Use when user reports a bug, error, or unexpected behavior in code or systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars82311111](https://clawhub.ai/user/mars82311111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect bug symptoms, analyze likely root causes, choose a repair strategy, apply a fix workflow, and verify whether the reported problem has been resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent OpenClaw log and repair files.

Mitigation: Review the configured OpenClaw workspace and log paths before use, and run the skill only where persistent repair records are acceptable.

Risk: If a Feishu sender skill exists at the expected path, this skill may automatically execute it to send a repair report.

Mitigation: Disable, remove, or gate the Feishu sender integration unless automatic repair notifications are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars82311111/skills/bug-fixer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples and script-generated text and Markdown repair records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent OpenClaw log and repair files and may send a repair notification through an installed Feishu sender skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
