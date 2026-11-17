## Description:

Monitor competitor websites for changes, analyze updates, generate competitive intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdio-afk](https://clawhub.ai/user/clawdio-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, product managers, and competitive strategists use this skill to monitor selected competitor websites for pricing, product, content, and messaging changes and turn those changes into competitive intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-configured websites, which can reach unintended domains or internal network locations if configuration is not controlled.

Mitigation: Use only trusted competitor configurations, restrict allowed domains, and run monitoring away from internal networks.

Risk: Snapshots and reports may store website content, pricing data, and competitive analysis longer than intended.

Mitigation: Set data-retention expectations before use, cap response and report sizes, and periodically remove stale snapshots and reports.

Risk: Reports sent to Slack, email, or custom webhooks may disclose inaccurate or sensitive competitive intelligence.

Mitigation: Sanitize competitor names where appropriate and review reports before forwarding them to external systems or teams.

Risk: Cron-style continuous monitoring can repeatedly collect external website data without enough legal, privacy, or operational review.

Mitigation: Enable scheduled monitoring only after legal, privacy, and data-retention expectations are clear.

## Reference(s):

- [Competitor Change Monitor API & Configuration Guide](references/api-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include snapshots, detected changes, pricing data, change summaries, competitive implications, and recommended actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
