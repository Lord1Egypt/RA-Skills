## Description: <br>
Generates an interactive local HTML spending report from native Alipay CSV exports and WeChat Pay XLSX exports for expense categorization, trend review, recurring merchant analysis, spending habit diagnosis, and budget optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeyitech](https://clawhub.ai/user/yeyitech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to convert personal Alipay and WeChat Pay bill exports into a local spending dashboard. It helps review expense categories, monthly and daily trends, recurring merchants, spending habits, and budget optimization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment exports and generated reports contain sensitive personal financial data. <br>
Mitigation: Use explicit local file paths or a dedicated bills folder, write the report to a private location, and avoid opening or sharing the HTML where others can view it. <br>
Risk: Directory auto-discovery may select the newest matching bill file rather than the intended export. <br>
Mitigation: Use explicit --alipay and --wechat paths, or run the skill in a dedicated folder containing only the intended bill exports. <br>
Risk: Password-protected WeChat ZIP exports are not parsed directly. <br>
Mitigation: Unzip the WeChat export locally and provide the extracted XLSX file to the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yeyitech/generate-alipay-wechat-report) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a self-contained local HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local Alipay CSV and WeChat XLSX exports; the generated report may contain personal financial details.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
