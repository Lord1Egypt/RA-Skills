## Description:

Check AI provider credits and balance across 10 services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to check remaining balances, quotas, usage windows, and spend trends across supported AI providers from one CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local AI provider API keys, Codex/Grok CLI auth files, and CodexBar usage data to check balances.

Mitigation: Install only when this credential access is acceptable; review credential sources before running checks.

Risk: Balance snapshots may be written to a local trend log for history and burn-rate estimates.

Mitigation: Use --no-log when local balance history should not be stored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/check-ai-credits)
- [README.md](artifact/README.md)
- [Migration map](artifact/docs/MIGRATION.md)
- [DeepSeek platform](https://platform.deepseek.com)
- [DeepInfra dashboard](https://deepinfra.com/dash)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON snapshots from CLI commands, with Markdown guidance in skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON snapshots include provider, source, timestamp, currency, balance, usedPercent, resetsAt, monthCost, monthPeriod, details, and error fields.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
