## Description:

Generates modular, configurable global finance daily reports with source-linked market data, external LLM collection, chat delivery, scheduled setup, and module management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyangryr-cyber](https://clawhub.ai/user/xyangryr-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily global finance briefing, configure scheduled delivery, and customize the report modules. It is intended for informational market reporting, not real-time trading, individual stock analysis, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports insecure API key handling in setup.

Mitigation: Use a proper secret store or tightly permissioned environment file, and avoid entering API keys into the setup script as written.

Risk: Scheduled delivery can run automatically through an OpenClaw cron job.

Mitigation: Inspect the cron job, schedule, session, and command before enabling automatic delivery, and run it under a dedicated unprivileged account.

Risk: The scheduled workflow uses shared temporary files for collected report data and logs.

Mitigation: Prefer private per-run temporary directories with restrictive permissions, and clean them after report generation.

Risk: Fetched public content may be sent to DashScope or Volcengine for processing.

Mitigation: Assume external processing occurs, avoid sensitive inputs, and review provider data-handling requirements before use.

Risk: Finance briefings can be mistaken for trading recommendations.

Mitigation: Treat generated reports as informational summaries, verify cited sources, and do not use the skill for real-time trading, stock picks, or investment advice.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/xyangryr-cyber/skills/finance-daily-report)
- [Data source list](references/sources.md)
- [Report generation workflow](references/workflow.md)
- [Fact verification guidance](references/verification.md)
- [Report template](references/template.md)
- [Module configuration schema](references/module-schema.md)
- [Collector prompt templates](references/collector-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with source links, plus shell commands and YAML configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat output may be auto-chunked; scheduled runs can save dated Markdown reports and optional evidence mappings.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
