## Description:

数字双生养成系统 v3.0 helps an agent create and maintain a personalized digital companion with bonding, shared memory, value-alignment checks, growth tracking, sensory configuration, and backup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejianjun000](https://clawhub.ai/user/xiejianjun000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill to configure a personalized companion experience that records a covenant, value anchors, shared memories, status checks, and backups. It is intended for companion-style agent customization rather than enterprise system integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores long-lived local records about identity, values, memories, and predicted future needs.

Mitigation: Avoid entering secrets or sensitive personal data, and regularly review and remove unneeded files under .twin.

Risk: Backups duplicate personal memory data and should be treated as unencrypted despite the skill's backup language.

Mitigation: Store .twin_backups only in trusted locations, restrict sharing, and delete backups that are no longer needed.

Risk: Migration or sharing workflows may copy personal memory files.

Mitigation: Inspect the exact source and destination files before running migration or sharing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejianjun000/skills/digital-twin-v3)
- [Publisher profile](https://clawhub.ai/user/xiejianjun000)
- [Skill definition](artifact/SKILL.md)
- [Twin covenant template](artifact/templates/twin-covenant.md)
- [Values anchor template](artifact/templates/values-anchor.md)
- [Heartbeat checklist template](artifact/templates/heartbeat-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON status objects, Python scripts, and generated local Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .twin memory files and .twin_backups archives in the configured workspace when invoked.]

## Skill Version(s):

3.0.0 (source: server release metadata; artifact metadata reports 3.0.0-test)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
