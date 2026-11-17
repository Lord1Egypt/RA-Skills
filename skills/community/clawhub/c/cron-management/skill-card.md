## Description:

Manage OpenClaw cron jobs: list, pause, resume, maintenance mode, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw cron job status, pause or resume jobs, enable maintenance mode, and diagnose recent job failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly pause or resume scheduled jobs.

Mitigation: Prefer exact job IDs or unique exact-name matching, and require confirmation before all-jobs operations.

Risk: Maintenance mode uses shared /tmp files.

Mitigation: Replace /tmp maintenance files with an owner-controlled runtime directory that checks ownership and rejects symlinks.

Risk: Installing the skill in shared or production environments can affect operational job execution.

Mitigation: Review the skill before installation and test pause, resume, and maintenance workflows in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/cron-management)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with command examples and integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw cron access and jq for the bundled cronctl shell script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
