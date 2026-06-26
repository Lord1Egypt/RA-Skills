## Description: <br>
Sends a daily 15:10 summary of A-share closing data including index changes, volume, hot sectors, and main capital flow via Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrislzg](https://clawhub.ai/user/chrislzg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate an end-of-day A-share market report after the China market close. It can print the report locally or send it through Feishu when send mode is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Send mode posts report text to a fixed Feishu user and uses a shell command to send externally sourced report content. <br>
Mitigation: Review before enabling --send, verify the Feishu recipient is yours or make it configurable, and prefer a non-shell API or argument-array subprocess call. <br>
Risk: The generated report includes market interpretation and operation suggestions based on third-party market data. <br>
Mitigation: Treat the report as informational, verify market figures against trusted sources, and do not rely on generated suggestions as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrislzg/a-stock-evening) <br>
- [Eastmoney index data API](https://push2.eastmoney.com/api/qt/ulist.np/get) <br>
- [Eastmoney industry capital-flow API](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally send the generated report to Feishu when send mode is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
