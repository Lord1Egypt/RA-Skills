## Description: <br>
Provides Hong Kong stock company profiles, valuation metrics, basic stock views, and historical OHLC candlestick data from market.ft.tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data agents use this skill to answer Hong Kong equity questions about company introductions, valuation ratios, market capitalization, share counts, and historical candlestick data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested stock symbols, dates, and pagination parameters are sent to market.ft.tech. <br>
Mitigation: Use only query parameters that are appropriate to disclose to the external market-data service. <br>
Risk: VirusTotal was pending in the security evidence. <br>
Mitigation: Review and scan the artifact before deployment, even though SkillSpector, static scan, and artifact review reported no issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawn92/ftshare-hk-data) <br>
- [market.ft.tech API base](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON API responses with concise text or command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only lookup behavior; sends selected Hong Kong stock symbols, dates, and pagination parameters to market.ft.tech.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
