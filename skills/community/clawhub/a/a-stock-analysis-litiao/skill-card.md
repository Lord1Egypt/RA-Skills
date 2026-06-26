## Description: <br>
Provides China A-share realtime quote lookup, intraday volume analysis, main-force activity signals, limit-up observations, and local portfolio profit and loss tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A-share market data, inspect intraday volume patterns, and maintain a local portfolio record for profit and loss analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and edits a local portfolio file, and the remove command deletes a holding from that record. <br>
Mitigation: Back up the portfolio JSON when records matter and run remove only when the holding should be deleted. <br>
Risk: Market data and signal labels may be delayed, unavailable outside trading hours, or unsuitable as investment advice. <br>
Mitigation: Use the output as analysis support only and verify trading decisions against authoritative market and financial sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/a-stock-analysis-litiao) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina realtime quote endpoint](https://hq.sinajs.cn/list={codes_str}) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local portfolio JSON file under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
