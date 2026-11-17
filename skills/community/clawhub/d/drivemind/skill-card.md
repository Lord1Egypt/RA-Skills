## Description:

DriveMind helps AI agents sustain structured follow-through, clear progress updates, explicit safety boundaries, human-in-the-loop escalation, and reusable post-task lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzc-001](https://clawhub.ai/user/yuzc-001)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and developers use DriveMind to guide AI assistants through meaningful work with steadier persistence, clearer status reporting, safer escalation, and concise retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory or note-saving behavior could retain unnecessary task details if an agent has a memory mechanism enabled.

Mitigation: Persist only stable lessons or next-time rules, and review memory-related behavior before installation in environments with persistent notes.

Risk: Broad trigger phrases may activate DriveMind when a lighter response would be enough.

Mitigation: Use the compression rule and mode guide to keep simple responses brief and reserve structured behavior for non-trivial tasks.

Risk: Stronger persistence could be misapplied as pressure to continue through unclear authority or high-impact actions.

Mitigation: Apply decision gates and escalation rules before destructive, production, external, or permission-changing actions.

## Reference(s):

- [DriveMind Skill Page](https://clawhub.ai/yuzc-001/skills/drivemind)
- [DriveMind Skill Definition](artifact/SKILL.md)
- [Decision Gates](artifact/references/decision-gates.md)
- [Escalation Rules](artifact/references/escalation-rules.md)
- [Mode Guide](artifact/references/mode-guide.md)
- [Persistence Protocol](artifact/references/persistence-protocol.md)
- [Review Style Guide](artifact/references/review-style-guide.md)
- [Stuck Resolution](artifact/references/stuck-resolution.md)
- [Task Typing](artifact/references/task-typing.md)
- [Review Template](artifact/templates/review-template.md)
- [Distillation Template](artifact/templates/distill-template.md)
- [Daily Diary Template](artifact/templates/diary-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language responses and structured Markdown reviews or lesson notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts structure to task complexity; no fixed token cap specified.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
