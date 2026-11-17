## Description:

Monitor Costco inventory by ZIP and run it safely with OpenClaw cron. Keep secrets outside the skill directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cweiping](https://clawhub.ai/user/cweiping)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure recurring Costco product availability checks across ZIP codes and produce status reports for downstream notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring proxy-based web checks may be inappropriate if used without authorization or at an excessive polling rate.

Mitigation: Use only for authorized monitoring, keep polling frequency modest, and disable the OpenClaw cron job when monitoring is no longer needed.

Risk: Credential-bearing proxy URLs can be exposed in command output, logs, or configuration files.

Mitigation: Store real secrets outside the skill directory, restrict secret file permissions, and avoid printing or logging proxy URLs that contain credentials.

Risk: Product URLs are accepted from configuration and are not restricted to approved Costco hosts.

Mitigation: Restrict product URLs to approved Costco domains before running checks.

Risk: Access-denied, CAPTCHA, or parser failures can create ambiguous inventory signals.

Mitigation: Treat blocked or ambiguous responses as unknown, preserve diagnostic excerpts, and alert only after repeated failures.

## Reference(s):

- [Costco Inventory Monitoring Standard](references/costco-inventory-standard.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands, environment configuration, JSON/JSONL snapshots, and plain-text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime checks may write latest_report.txt, monitor.log, snapshots.jsonl, and state.json to configured output paths.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
