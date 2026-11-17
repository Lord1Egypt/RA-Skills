## Description:

Fitness & Workout Manager helps an agent create personal fitness plans, log workouts in one-shot or live-session mode, summarize training history, export Markdown reports, and optionally sync plan or log content to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ph13917403910](https://clawhub.ai/user/ph13917403910)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this skill to maintain workout plans, capture exercise logs from natural-language updates, review weekly or monthly fitness status, and generate exportable training reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workout plans, logs, feelings, constraints, and free-form notes are health-adjacent data stored under ~/.openclaw.

Mitigation: Use on a single-user machine where possible, review local filesystem permissions, and avoid recording sensitive medical details unless storage access is tightened.

Risk: When Feishu sync or reminders are enabled, plan and log information can be shared through Feishu documents or bot messages.

Mitigation: Review the Feishu document, bot permissions, and sharing settings before enabling FEISHU_FITNESS_DOC_ID or scheduled reminders.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ph13917403910/skills/fitness-skill)
- [Fitness Data Schemas](references/schemas.json)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown, with JSON files used for local plan, log, and active-session state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can export bounded Markdown workout reports and uses compact status output by default.]

## Skill Version(s):

1.2.2 (source: server release evidence, SKILL.md frontmatter, manifest.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
