## Description:

ClawBoss turns an OpenClaw agent into a local productivity coach that guides GROW-model goal setting, progress check-ins, adaptive accountability, and reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paitesanshi](https://clawhub.ai/user/paitesanshi)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to structure goals, break them into actionable plans, receive recurring coaching-style check-ins, and reflect on progress over weekly or monthly periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses a mutable latest npm package.

Mitigation: Install a pinned, reviewed package version instead of using the latest npx command.

Risk: Unchecked task-file paths can escape the intended memory folder when state is manually edited or affected by untrusted plugins.

Mitigation: Avoid untrusted plugins and manually edited state until task-file path containment is fixed.

Risk: Personal coaching data and automatic check-in state are stored locally.

Mitigation: Install only if local storage of personal coaching data and automatic check-in updates is acceptable for the intended use.

## Reference(s):

- [ClawBoss ClawHub listing](https://clawhub.ai/paitesanshi/skills/clawboss)
- [Publisher profile](https://clawhub.ai/user/paitesanshi)
- [ClawBoss GitHub link from artifact documentation](https://github.com/Paitesanshi/ClawBoss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text responses, with local JSON state and Markdown task files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores coaching state and task progress locally in the OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
