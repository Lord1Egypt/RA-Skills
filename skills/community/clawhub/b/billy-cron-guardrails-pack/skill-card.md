## Description:

Lint cron entries for schedule validity, bad model names, and missing NO_REPLY discipline markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highlander89](https://clawhub.ai/user/highlander89)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to lint cron entries for schedule field count, disallowed model names, and NO_REPLY markers before deploying or reviewing scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linter reads cron file contents provided by the agent or user.

Mitigation: Run it only on cron files appropriate for local agent processing and avoid feeding sensitive operational schedules unless policy allows.

Risk: The checks are lightweight heuristics and may miss unsafe jobs or flag benign lines.

Mitigation: Treat findings as review guidance and keep human review before changing scheduled jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/highlander89/skills/billy-cron-guardrails-pack)
- [Publisher profile](https://clawhub.ai/user/highlander89)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local cron-file lint findings with process exit codes for pass, findings, or usage/read errors.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
