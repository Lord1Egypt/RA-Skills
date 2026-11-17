## Description:

Lint cron entries for schedule validity, bad model names, and missing NO_REPLY discipline markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to lint cron entries before deployment and catch schedule formatting issues, disallowed model names, and missing NO_REPLY markers on announcement-style jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron files may contain sensitive job commands, paths, or operational details.

Mitigation: Review and redact cron file contents before sharing lint outputs or using the skill on sensitive schedules.

Risk: The lint checks are narrow and may not catch every invalid or unsafe cron pattern.

Mitigation: Use the lint result as a guardrail and keep normal code review or deployment checks for cron changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/cron-guardrails-pack)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text lint results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The cron lint script returns exit code 0 when no issues are found, 1 when lint issues are found, and 2 for usage or read errors.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
