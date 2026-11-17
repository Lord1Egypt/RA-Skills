## Description:

Akshare Stock Temp helps agents use AkShare to retrieve and analyze China A-share quotes, historical K-line data, financial metrics, sector data, fund flow, IPO, and margin trading information.

This skill is for research and development only.

## Publisher:

[liguang00806](https://clawhub.ai/user/liguang00806)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to answer China A-share market-data questions and generate AkShare-based examples or commands for quotes, historical prices, financial analysis, screening, and sector review. Outputs should be treated as research data, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AkShare calls contact external market-data services and may return unavailable, stale, or changed data.

Mitigation: Run in an isolated Python environment, pin AkShare when reproducibility matters, add retries or exception handling, and verify important results against authoritative sources.

Risk: Market-data outputs may be mistaken for investment advice.

Mitigation: Treat outputs as research data only and require independent review before making financial decisions.

Risk: The fund-flow CLI path may fail because the security evidence flags that command as needing correction.

Mitigation: Test the fund-flow action locally and fix or disable it before relying on that command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liguang00806/skills/akshare-stock-temp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query external market-data services through AkShare; the fund-flow command may need correction before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
