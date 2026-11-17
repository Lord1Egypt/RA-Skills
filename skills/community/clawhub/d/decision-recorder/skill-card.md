## Description:

Record, review, search, and analyze decisions from technical work, product work, team discussions, and personal planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, technical teams, and individual users use this skill to capture structured decision records, search prior rationale, compare options, and review decision patterns over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: View, update, or delete operations may affect JSON files outside the intended storage directory if decision IDs are not contained.

Mitigation: Validate decision IDs against the expected generated format and confirm resolved paths remain inside ~/.decision-recorder/ before reading, writing, or deleting files.

Risk: Decision records may contain sensitive planning rationale and are stored as local JSON files.

Mitigation: Avoid recording secrets or highly sensitive details unless local file permissions are hardened, and document retention and deletion practices before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/decision-recorder)
- [ClawHub Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON files, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime commands emit terminal text and write local JSON decision records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision records are stored locally under ~/.decision-recorder/ as JSON files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
