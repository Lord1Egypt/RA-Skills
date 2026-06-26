## Description: <br>
Provides A-share stock market data queries through qgdata, including real-time prices, minute K-line data, trade details, fundamentals, and trading calendar information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Listolany](https://clawhub.ai/user/Listolany) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and trading researchers use this skill to query A-share market data for quantitative analysis, intraday monitoring, technical analysis, and automated trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fall back to an embedded shared qgdata API token, which may have quota, pricing, or operational reliability limits. <br>
Mitigation: Configure a dedicated personal QGDATA_TOKEN before production use and review the provider's quota and pricing terms. <br>
Risk: The skill reads QGDATA_TOKEN from the environment and may read ~/.openclaw/.env. <br>
Mitigation: Use a least-privilege token, protect local environment files from disclosure, and rotate the token if it is exposed. <br>
Risk: The artifact includes a hardcoded local Python import path for qgdata dependencies. <br>
Mitigation: Audit or remove the hardcoded import path and install qgdata and pandas in the intended agent runtime. <br>


## Reference(s): <br>
- [Astock Data on ClawHub](https://clawhub.ai/Listolany/astock-data) <br>
- [QuantGo Data Platform](https://data.quantgo.ai) <br>
- [QuantGo Data Documentation](https://data.quantgo.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON data responses with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include qgdata provider fields, token and quota notes, upgrade guidance, and data freshness warnings.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata and SKILL.md changelog, released 2026-03-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
