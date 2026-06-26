## Description: <br>
FusionAlpha A&Crypto Desk helps an agent produce structured A-share, crypto, and morning-brief market research reports from user-provided or script-fetched market data, with fixed templates, evidence lists, and conservative risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinyuqinfeng](https://clawhub.ai/user/xinyuqinfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to draft research-oriented A-share, crypto, and morning market reports from structured market data. It supports trading-plan style outputs, but the security evidence recommends treating generated reports as research rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading reports may be interpreted as financial advice or may contain incorrect conclusions if input market data is incomplete. <br>
Mitigation: Present outputs as research, require evidence lists for specific conclusions, and review decisions before acting on them. <br>
Risk: Python helper scripts call public market-data services and may install dependencies locally. <br>
Mitigation: Run scripts intentionally in a local virtual environment and review dependencies before installation. <br>
Risk: CryptoPanic news access can require a user token. <br>
Mitigation: Pass the token through an environment variable or parameter and avoid echoing, storing, or placing it in chat logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xinyuqinfeng/a-stock-crypto-fusion) <br>
- [Publisher Profile](https://clawhub.ai/user/xinyuqinfeng) <br>
- [Data Sources Reference](references/data_sources.md) <br>
- [CryptoPanic Developer API](https://cryptopanic.com/api/developer/v2/posts/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with evidence lists and final decision summary lines; helper scripts emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on supplied market data quality; optional CryptoPanic news access requires a user-provided token.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
