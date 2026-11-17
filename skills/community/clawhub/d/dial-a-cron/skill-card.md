## Description:

Stateful cron system for OpenClaw with persistent memory, change detection, smart routing, token budget tracking, and self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenthyjack](https://clawhub.ai/user/agenthyjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Dial A Cron to wrap scheduled OpenClaw jobs with persistent state, change detection, severity-based routing, token budget tracking, and retry or pause behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job configs can grant broad command, file, and network access.

Mitigation: Run the skill in a least-privilege, isolated environment and personally review every job config before use.

Risk: Diffs, commands, routes, webhook URLs, file paths, and outputs may expose sensitive data.

Mitigation: Avoid secrets and internal metadata services, restrict file paths and HTTP targets, and route only to trusted recipients.

Risk: Arbitrary shell strings and shell-based delivery paths can be unsafe when influenced by untrusted configuration or output.

Mitigation: Use only trusted job configs, avoid arbitrary shell strings, and ensure OpenClaw and gog CLIs run with limited credentials.

## Reference(s):

- [Dial A Cron ClawHub Skill Page](https://clawhub.ai/agenthyjack/skills/dial-a-cron)
- [Job Config Schema Reference](references/job-config-schema.md)
- [Security Review for dial-a-cron](references/security-review.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with JSON job configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local job state, logs, and routed delivery outputs when used by an agent.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
