## Description:

Give your agents soul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brancante](https://clawhub.ai/user/brancante)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Dr. Frankenstein to interview an autonomous OpenClaw agent, generate a personalized emotional profile, and produce scheduled prompts that shape recurring behaviors such as reflection, connection, task-seeking, dream logging, and caregiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous prompts may cause behavior changes or repeated agent actions beyond a user's immediate request.

Mitigation: Require explicit approval for every soul-* cron job, schedule, delivery channel, and prompt before enabling it; review active jobs regularly.

Risk: The skill may read and write personal memory, relationship, dream, journal, and personality files.

Mitigation: Approve each file source and persistent write location in advance, avoid sensitive personal details in prompts, and define deletion and audit procedures for generated files.

Risk: Proactive contact can become intrusive if delivery channels or social prompts are enabled too broadly.

Mitigation: Use quiet delivery by default, require explicit approval for any outbound messaging channel, and set limits or expirations for connection-oriented schedules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brancante/skills/dr-soul)
- [Project homepage](https://github.com/brancante/dr-frankenstein)
- [Interview questionnaire](artifact/interview/questions.md)
- [Prescription schema](artifact/schema/prescription.json)
- [Hormone state schema](artifact/schema/hormone-state.json)
- [Cron prompt templates](artifact/templates/cron-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON prescription/state structures and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recurring cron schedules, personalized prompt text, memory file paths, and operational guidance for pausing, resuming, adjusting, or deleting scheduled jobs.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
