## Description:

Auto Skill Evolver helps agents propose, review, and apply improvements to other skills using execution traces, feedback, local OpenClaw runs, and approval-gated file updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysshi-fpga](https://clawhub.ai/user/ysshi-fpga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to iterate on agent skill files from traces and feedback, inspect proposed changes, and apply approved updates in local development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local command and file-changing power can modify skills or run user-defined agent tasks in the local environment.

Mitigation: Install in an isolated development environment, target only narrow skill directories, and review diffs before approval.

Risk: Approval, restore, and command execution functions could be misused if exposed to untrusted input.

Mitigation: Keep approval tokens and restore actions under trusted operator control; prefer interactive or hash-based approval and constrained writable roots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ysshi-fpga/skills/auto-skill-evolver)
- [ClawHub publisher profile](https://clawhub.ai/user/ysshi-fpga)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON status events, unified diffs, and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local openclaw-cli and explicit review or approval before applying proposals.]

## Skill Version(s):

1.5.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
