## Description:

Automatically update OpenClaw and installed skills on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crazyozzy](https://clawhub.ai/user/crazyozzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure scheduled maintenance that updates OpenClaw, updates installed ClawHub skills, and returns concise update summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automatic updates can change OpenClaw or installed skill behavior.

Mitigation: Use dry-run or status commands first, schedule updates during a maintenance window, and review the concise summary after each run.

Risk: An update failure can leave manual follow-up work for configuration, service health, or skill resolution issues.

Mitigation: Run OpenClaw doctor/status checks and targeted ClawHub update repair commands when the update summary reports a failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crazyozzy/skills/crazyozzy-auto-updater)
- [Agent implementation guide](artifact/references/agent-guide.md)
- [Update summary examples](artifact/references/summary-examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and scheduled-task prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise user-facing update summaries; supports dry-run/status guidance before enabling recurring updates.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
