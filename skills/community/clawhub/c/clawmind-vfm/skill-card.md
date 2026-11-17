## Description:

ClawMind helps an OpenClaw agent track task health, rank improvement proposals with VFM scoring, manage project state, and store or recall experience memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[numuly](https://clawhub.ai/user/numuly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ClawMind to add self-management workflows to OpenClaw agents, including task health tracking, proposal scoring, reflection prompts, state logging, and persistent experience recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist raw conversation or task context in local memory and workspace state.

Mitigation: Use explicit opt-in before storing sensitive context, review stored data regularly, and provide retention, redaction, and deletion procedures.

Risk: The skill can append user profile information and create future skills that may affect later agent behavior.

Mitigation: Require review before activating generated skills or profile updates, scan generated files, and keep rollback steps for changes to agent behavior.

## Reference(s):

- [ClawMind ClawHub skill page](https://clawhub.ai/numuly/skills/clawmind-vfm)
- [state-manager.md](artifact/references/state-manager.md)
- [vfm-design.md](artifact/references/vfm-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent workspace state, SQLite memory records, user profile notes, logs, and generated skill files when its scripts are executed.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
