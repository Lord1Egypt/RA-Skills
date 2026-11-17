## Description:

Controlled autonomous self-evolution: grants the agent authority to self-improve through a tiered safety system with mandatory audit trails, rollback capabilities, and human oversight checkpoints for critical modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niveroviero](https://clawhub.ai/user/niveroviero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to define bounded self-improvement workflows for an agent, including tiered permissions, audit logs, backups, rollbacks, and human oversight for critical changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to maintain and change its own memory, skills, and tool-use rules, with some changes applied before user approval.

Mitigation: Install only where agent self-maintenance is intended; require explicit approval before edits to memory, SKILLS.md, TOOLS.md, configuration, or newly created skills take effect, and review logs and backups closely.

Risk: Self-modification can introduce incorrect guidance or weaken expected behavior.

Mitigation: Review and scan proposed skill changes before deployment, keep rollback artifacts, and preserve approval checkpoints for critical changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niveroviero/skills/bacon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes audit, backup, rollback, sandboxing, and approval practices; it does not itself execute changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
