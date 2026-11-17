## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlist alerts, dividend analysis, stock scoring, trend scanning, and rumor detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylfy-ljl](https://clawhub.ai/user/ylfy-ljl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run stock and cryptocurrency analysis workflows, monitor watchlists and portfolios, evaluate dividends, and identify trending or early market signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanning can involve AUTH_TOKEN and CT0 session tokens.

Mitigation: Prefer hot scans with --no-social; if social scanning is required, keep tokens out of repositories and shared folders.

Risk: Browser-cookie based social scanning can require broad local access.

Mitigation: Avoid browser-cookie extraction where possible and do not grant Terminal Full Disk Access.

Risk: Portfolio and watchlist JSON files may contain private financial data.

Mitigation: Store generated portfolio and watchlist files privately and avoid sharing them with logs, repositories, or public folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylfy-ljl/skills/auto-test-skill)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage Guide](docs/USAGE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)
- [Architecture](docs/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts can emit console text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local portfolio, watchlist, hot scan, and rumor scan JSON files under user skill state or cache paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
