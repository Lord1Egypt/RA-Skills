## Description:

Runs Cursor Agent CLI for coding tasks such as writing, editing, refactoring, reviewing, and planning code while defaulting to read-only execution until the user approves changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albinati](https://clawhub.ai/user/albinati)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate non-trivial coding work in a selected repository to Cursor Agent CLI. It is intended for coding tasks where the agent should start in read-only ask or plan mode and request confirmation before applying changes, using cloud execution, or committing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved Cursor Agent CLI use can inspect repository contents and may expose project data.

Mitigation: Install and run the skill only in repositories where Cursor Agent access is acceptable, and obtain explicit confirmation before execution.

Risk: Write mode can modify files in the selected repository.

Mitigation: Start in read-only ask or plan mode, review the proposed changes, and switch to write mode only after the user confirms.

Risk: Cloud execution may send repository contents to cursor.com.

Mitigation: Warn the user before using cloud mode and proceed only after explicit approval.

## Reference(s):

- [Cursor CLI Documentation](https://cursor.com/docs/cli/overview)
- [Cursor Agent Available Models](references/models.md)
- [Cursor Agent Slash Commands](references/slash-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to read-only ask mode; write mode, cloud execution, and commits require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
