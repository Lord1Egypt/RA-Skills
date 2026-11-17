## Description:

A-stock-report automates A-share market reports and WeCom delivery for morning, market-close, evening, intraday alert, IPO weekly, and weekend finance workflows, with sentiment scoring and AI outlook sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cookfish1979](https://clawhub.ai/user/cookfish1979)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect A-share market data, generate scheduled finance reports, and deliver them to a controlled WeCom destination. It supports operational reporting and monitoring workflows, not unchecked financial decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically post market reports and investment-related suggestions to WeCom.

Mitigation: Install only on hosts and WeCom destinations you control, review the configured cron jobs before enabling them, and keep the report disclaimer intact.

Risk: Secrets are loaded from environment files and may be exposed if /workspace/.env is broadly readable or sourced into more processes than necessary.

Mitigation: Protect /workspace/.env with restrictive permissions, keep only the required WECOM_WEBHOOK_KEY and IWENCAI_API_KEY values available to this skill, and avoid broad .env sourcing in cron.

Risk: Shared temporary handoff and lock files can create tampering or race-condition exposure on multi-user hosts.

Mitigation: Move handoff and lock files into a private 0700 runtime directory and use atomic creation for lock and state files.

Risk: Webhook sending currently relies on a curl subprocess path.

Mitigation: Replace subprocess-based sending with an in-process HTTPS client before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cookfish1979/skills/a-stock-report)
- [cron_jobs README](cron_jobs/README.md)
- [cron_mirror.json](cron_jobs/cron_mirror.json)
- [fallback-chain-validation](references/fallback-chain-validation.md)
- [weekend-4kb-budget](references/weekend-4kb-budget.md)
- [historical config reference](references/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text reports with JSON configuration and shell-command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automated WeCom text delivery, scheduled cron workflows, and report files with byte-budget constraints for weekend messages.]

## Skill Version(s):

3.5.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
