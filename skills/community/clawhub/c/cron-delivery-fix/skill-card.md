## Description:

Diagnose and fix OpenClaw cron job delivery failures with scripted checks for silent delivery failures, missing delivery parameters, and invalid session or payload combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimonxin](https://clawhub.ai/user/shimonxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw cron jobs that report delivery success without reaching recipients, fail delivery, or have invalid delivery configuration. It guides agents toward scripted diagnosis, scoped fixes, restoration, and verification of cron delivery settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix scripts can broadly overwrite cron delivery settings with hard-coded channel, recipient, and account values.

Mitigation: Review destination values, make a backup, and prefer manually scoped edits or patched scripts that require explicit channel, recipient, and account inputs.

Risk: Running fix-all.sh in production or multi-user cron environments can unintentionally redirect scheduled delivery behavior.

Mitigation: Avoid fix-all.sh in shared or production cron environments unless each affected job and destination has been reviewed first.

Risk: The security scan reports an input-handling flaw in the bundled scripts.

Mitigation: Review script arguments and OpenClaw command output handling before execution, and run diagnosis again after any change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shimonxin/skills/cron-delivery-fix)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and cron configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw cron diagnostic and edit commands that should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
