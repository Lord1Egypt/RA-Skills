## Description:

Feedback Learning V2 helps OpenClaw agents detect positive and corrective feedback, log events, promote recurring patterns into structured rules, and generate weekly learning reports using local shell and Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surdeddd](https://clawhub.ai/user/surdeddd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture feedback and command failures, review recurring behavior patterns, and maintain suggested rules for future agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores raw feedback, command context, and error snippets in local learning files.

Mitigation: Keep the learning directory private, redact secrets from feedback and error fields, and review captured data before enabling hooks or scheduled jobs.

Risk: Repeated feedback can be promoted into active rules that future agents may follow.

Mitigation: Treat generated genes as suggestions and require human approval before adding them to an agent boot sequence or operational workflow.

Risk: Optional PostToolUse hooks and cron jobs can capture or process data automatically.

Mitigation: Review the hook and schedule configuration first, then enable automation only in environments where persistent local telemetry is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/surdeddd/skills/feedback-learning-v2)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown]

**Output Format:** [Markdown guidance with shell commands and local JSON or Markdown artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files and command-line text; no API keys are required.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
