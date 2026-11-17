## Description:

Fetches public market quotes from Yahoo Finance for selected global equity indexes, foreign exchange rates, commodities, and cryptocurrency, then produces a Chinese finance report suitable for manual or scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfstylejf](https://clawhub.ai/user/jfstylejf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate market snapshot reports for tracked stocks, indexes, currencies, commodities, and Bitcoin. It can be run manually or scheduled through the documented OpenClaw cron flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires outbound network access to Yahoo Finance, so reports can fail or become stale when the network or upstream data source is unavailable.

Mitigation: Run it only in environments where outbound finance-data access is expected, and treat generated market values as runtime data that should be checked before use.

Risk: The documented dependency installation uses an unpinned requests package, which can change behavior across installs.

Mitigation: Pin Python dependencies in a reviewed requirements file before production deployment.

Risk: The skill can be scheduled through the documented cron workflow.

Mitigation: Enable scheduling only after reviewing the command, runtime environment, and delivery target.

Risk: The generated report and user-facing documentation are Chinese-oriented.

Mitigation: Confirm that the deployment audience can read the output or localize the report text before relying on it operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jfstylejf/skills/finance-reporter)
- [Yahoo Finance](https://finance.yahoo.com)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Chinese plain-text finance report with markdown documentation and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report values depend on outbound Yahoo Finance responses at runtime.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and package.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
