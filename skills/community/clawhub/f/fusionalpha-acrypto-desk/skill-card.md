## Description: <br>
Generates data-anchored A-share, crypto, and morning-brief market analysis reports with fixed templates, evidence lists, and conservative risk controls. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn provided or helper-script-fetched JSON market data into structured research drafts for A-share, crypto, and morning-brief workflows. Outputs are intended for research and learning, not investment, legal, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-analysis outputs may be mistaken for investment, legal, or financial advice. <br>
Mitigation: Treat outputs as research drafts, verify important claims independently, and avoid acting on them without appropriate professional review. <br>
Risk: Helper scripts install Python dependencies and make outbound calls to market-data providers. <br>
Mitigation: Review dependencies before execution, run scripts in a controlled environment, and expect network access to public data sources. <br>
Risk: Optional CryptoPanic news fetching requires a user-provided token. <br>
Mitigation: Use a low-risk token only when news is needed, pass it through an environment variable or parameter, and do not echo or store it in outputs. <br>
Risk: Upstream market-data sources can fail, return partial data, or become stale. <br>
Mitigation: Check evidence lists and script error metadata before relying on a report; label unavailable or insufficient data instead of filling gaps. <br>


## Reference(s): <br>
- [Data Sources & How to Fetch](references/data_sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/xinyuqinfeng/fusionalpha-acrypto-desk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with evidence lists and optional shell-command guidance for JSON fetch scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can emit JSON for market data; CryptoPanic news is optional and requires a user-supplied token.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
