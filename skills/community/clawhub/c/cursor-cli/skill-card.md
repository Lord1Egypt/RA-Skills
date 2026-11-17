## Description:

Use Cursor editor and Cursor agent for coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyavchik](https://clawhub.ai/user/pyavchik)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to open files in Cursor, ask Cursor Agent coding questions, and compare files with Cursor's diff command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cursor Agent prompts may include or trigger analysis of local project code.

Mitigation: Use the skill only in repositories where Cursor account, workspace, and data-handling policies permit that code to be analyzed.

Risk: The skill depends on local Cursor CLI binaries and may fail where cursor or cursor-agent is unavailable.

Mitigation: Confirm the cursor and cursor-agent binaries are installed before relying on the skill.

## Reference(s):

- [Cursor CLI documentation](https://cursor.com/docs/cli/overview)
- [ClawHub Cursor CLI skill](https://clawhub.ai/pyavchik/skills/cursor-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/pyavchik)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the cursor and cursor-agent binaries to be installed.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
