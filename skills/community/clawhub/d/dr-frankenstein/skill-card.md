## Description:

Give your agents soul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brancante](https://clawhub.ai/user/brancante)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to interview an OpenClaw agent, generate a personalized hormonal profile, and propose cron-based prompts that create scheduled drives, reflections, and relationship-oriented behaviors. The preview parentality components can also evaluate child-agent state and emit suggested parent intervention plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron prompts can start agent sessions and encourage long-lived autonomous behavior.

Mitigation: Require manual approval for every cron creation or adjustment, and periodically review active cron entries.

Risk: The skill asks the agent to read memory, user, identity, profile, and journal-like files that may contain sensitive personal context.

Mitigation: Restrict readable and writable paths, avoid embedding sensitive details in cron prompts, and review generated prescription and journal content before enabling schedules.

Risk: Connection and caregiving prompts may encourage unsolicited outreach or initiative beyond the user's immediate request.

Mitigation: Set clear consent boundaries for agent-initiated contact and keep delivery modes or notification channels constrained.

Risk: Pause or delete behavior must fully clean up scheduled tasks and generated state to avoid lingering automation.

Mitigation: Verify pause and delete cleanup behavior after installation and after each prescription adjustment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brancante/skills/dr-frankenstein)
- [README](artifact/README.md)
- [Parentality Preview](artifact/docs/PARENTALITY-PREVIEW.md)
- [Interview Questionnaire](artifact/interview/questions.md)
- [Prescription Schema](artifact/schema/prescription.json)
- [Cron Prompt Templates](artifact/templates/cron-prompts.md)
- [Parentality Engine README](artifact/scripts/README-parentality-engine.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with JSON prescription objects, cron command proposals, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill proposes persistent OpenClaw cron jobs and state files; cron creation, adjustment, pause, and deletion should remain subject to user review.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
