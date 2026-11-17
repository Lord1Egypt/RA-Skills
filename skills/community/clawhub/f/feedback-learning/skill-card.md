## Description:

Zero-LLM feedback learning system for OpenClaw agents that detects Russian, English, and emoji feedback signals, logs events, discovers recurring patterns, promotes repeated corrections into rules, and generates weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surdeddd](https://clawhub.ai/user/surdeddd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local feedback detection, event logging, pattern analysis, rule promotion, and reporting to OpenClaw agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated feedback can be promoted into persistent active agent rules that influence future behavior.

Mitigation: Require human review before loading or activating promoted rules, and disable automatic activation unless the deployment explicitly approves it.

Risk: Feedback logs and reports may retain sensitive user text or operational context.

Mitigation: Avoid logging sensitive content, restrict access to the learning directory, and define retention and deletion rules before use.

Risk: Scheduled analysis and boot-time loading can make stale or low-quality learned rules persist across agent sessions.

Mitigation: Review genes.json and weekly reports regularly, expire outdated rules, and require approval before adding the learning directory to agent startup workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/surdeddd/skills/feedback-learning)
- [Publisher profile](https://clawhub.ai/user/surdeddd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON event records, JSON rule files, and Markdown weekly reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files such as events.jsonl, patterns.json, genes.json, capsules.json, and reports/WEEKLY_REPORT_YYYY_WNN.md when installed and run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
