## Description: <br>
Alpha Pulse provides China A-share T+1 short-term stock signal scanning and report-generation guidance based on capital-flow, price-volume, technical, news, and sentiment factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[77Spongebob](https://clawhub.ai/user/77Spongebob) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through scanning China A-share market data, filtering candidates, and producing short-term stock signal reports. It should be treated as an incomplete stock-data scanner and not as a ready trading engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release describes a stock-prediction system whose full implementation is not included in the package. <br>
Mitigation: Review the artifact contents before use and verify or supply any missing prediction, factor, report, and notification modules before running workflows that depend on them. <br>
Risk: Financial signal output may be inaccurate or incomplete. <br>
Mitigation: Do not rely on the skill output for trading decisions without independent financial review and validation against trusted market data. <br>
Risk: Runtime behavior depends on Python packages and market-data access. <br>
Mitigation: Run the scanner in an isolated Python environment, pin dependencies, and validate data-provider behavior before regular use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/77Spongebob/alpha-pulse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python code references, and report output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact includes a configuration file and scanner skeleton, while described prediction, factor, report, and notification modules are not included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
