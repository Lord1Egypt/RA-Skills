## Description:

个人进化追踪系统 - 不是冷冰冰的数据，是你的成长伴侣。记录心流、低谷、习惯、情绪，让每一次进化都有温度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexduming](https://clawhub.ai/user/alexduming)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill as a personal growth companion to record flow states, low points, habit check-ins, mood scores, achievements, and weekly reflection letters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive mood, habit, low-point, and reflection data may be retained in local plaintext.

Mitigation: Install only if local plaintext retention is acceptable; tighten file permissions and back up existing data before use.

Risk: Broad triggers and automatic suggestions may record more personal context than intended.

Mitigation: Use explicit consent before saving entries and disable or review automatic recording behavior unless it is desired.

Risk: Weak reset safeguards could affect existing personal tracking data.

Mitigation: Check for an existing local data file before initialization and preserve a backup before overwriting or resetting records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexduming/skills/evolution-diary)
- [Publisher profile](https://clawhub.ai/user/alexduming)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation output with JSON records and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes personal tracking records to local plaintext JSON unless the user changes the workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
