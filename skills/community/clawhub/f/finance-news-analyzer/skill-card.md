## Description:

Analyzes finance news from multiple sources, classifies sentiment and market impact, extracts key entities and figures, and generates investor-facing briefings, reports, charts, and persisted analysis data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sucriss](https://clawhub.ai/user/sucriss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather finance-related news, assess likely sentiment and market impact, and produce concise briefings or deeper reports for review. The generated material should be treated as decision-support content, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock or randomly labeled analysis may be mistaken for live market intelligence.

Mitigation: Require the publisher to replace mock behavior with verified data-source handling and clearly label any sample output before deployment.

Risk: Installer guidance may encourage piping remote installer output directly into a shell.

Mitigation: Review installation steps before use and avoid executing unaudited network-delivered scripts directly.

Risk: Model-provider data sharing, local storage, scheduling, and export behavior may be unclear to users.

Mitigation: Require explicit disclosure and opt-in configuration for provider calls, local persistence, scheduled runs, and exported files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sucriss/skills/finance-news-analyzer)
- [Supported models](references/supported-models.md)
- [Configuration example](references/config-example.md)
- [Sentiment rules](references/sentiment-rules.md)
- [Ticker map](references/ticker-map.md)
- [Industry map](references/industry-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports, command-line guidance, JSON or CSV exports, SQLite records, and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sentiment labels, confidence levels, related tickers, industry impact summaries, risk notes, scheduled task configuration, and local persistence artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
