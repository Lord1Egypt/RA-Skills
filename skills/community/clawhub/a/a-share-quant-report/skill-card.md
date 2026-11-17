## Description:

Helps agents reproduce A-share quantitative research reports by decomposing the research question, selecting an appropriately sized stock universe, generating factor or screening logic, running a standardized Python backtest when applicable, and presenting results in a report-style format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x2hacks](https://clawhub.ai/user/0x2hacks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to convert A-share quant or sell-side research reports into executable research plans, factor expressions, backtest scripts, structured Markdown reports, tables, charts, and follow-up guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script writes generated reports to an output path controlled by the runtime environment.

Mitigation: Run it only with a dedicated, trusted output directory and review generated files before sharing or publishing them.

Risk: Generated HTML report metadata can come from environment-controlled text.

Mitigation: Do not run the script with attacker-controlled environment variables, and be cautious opening generated HTML when report metadata is untrusted.

Risk: The workflow may make outbound market-data requests to AkShare and yfinance.

Mitigation: Run the skill only in environments where those network requests are expected, permitted, and monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x2hacks/skills/a-share-quant-report)
- [OpenClaw skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, inline chart references, Python code, shell commands, and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce report.md, report.html, CSV summaries, PNG charts, run summaries, and conversation-ready Markdown when the bundled backtest script is used.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and changelog show 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
