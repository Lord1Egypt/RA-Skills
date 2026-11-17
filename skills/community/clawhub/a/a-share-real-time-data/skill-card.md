## Description:

Fetch China A-share stock market bars, real-time quotes, and tick-by-tick transactions via the mootdx TDX protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangdinglu](https://clawhub.ai/user/wangdinglu)

### License/Terms of Use:


## Use Case:

Developers and market-data engineers use this skill to integrate mootdx-based China A-share market data retrieval into agent workflows, including candlestick bars, real-time quotes, batch quote retrieval, and tick transaction lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper installs Python packages from the configured pip index.

Mitigation: Install only in a virtual environment or another isolated Python environment, and pin mootdx and dependencies before use.

Risk: Verification and demo flows can make live TDX network requests.

Mitigation: Use the --check mode when only local dependency verification is needed, and run live connectivity tests only from approved environments.

Risk: The documented trading-hour bypass changes tdxpy's time-frame check to avoid empty transaction results on non-Beijing-time servers.

Mitigation: Apply the patch only for this market-data workflow and review returned data against the expected Beijing trading calendar.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangdinglu/skills/a-share-real-time-data)
- [api-reference.md](api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for live TDX network calls, dependency installation, Beijing-time trading-hour handling, and SH/SZ stock-code conversion.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
