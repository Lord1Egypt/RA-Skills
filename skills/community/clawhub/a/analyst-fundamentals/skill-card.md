## Description: <br>
Provides a Chinese A-share fundamental analysis workflow when a user supplies a stock code or asks for company fundamentals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vbdspd](https://clawhub.ai/user/vbdspd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to gather Eastmoney F10 data for Chinese A-share stocks, run staged fundamental analyses, and assemble a Markdown research report. The output is generated research context and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can be resource-heavy because it opens Eastmoney pages and coordinates many concurrent research tasks. <br>
Mitigation: Run it only in an environment where that load is acceptable, use bounded run-mode workers, and avoid persistent no-timeout workers. <br>
Risk: The skill writes many local research artifacts. <br>
Mitigation: Confirm the output path before execution and review generated files before sharing or relying on them. <br>
Risk: The output may contain investment-style recommendations or position-sizing language even though the skill states it is not investment advice. <br>
Mitigation: Treat outputs as generated research, independently verify financial facts, and remove or review recommendation language before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vbdspd/analyst-fundamentals) <br>
- [Publisher profile](https://clawhub.ai/user/vbdspd) <br>
- [Eastmoney F10 data page template](https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code}&color=b#/{module}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files with concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local data/{stock code}/ Markdown artifacts and a final report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
