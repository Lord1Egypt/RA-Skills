## Description: <br>
A Chinese A-share analysis assistant that screens stocks using technical and financial criteria, generates market summaries, and produces Markdown reports with buy ranges, targets, stop-loss levels, and position suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxihyv](https://clawhub.ai/user/dxihyv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and developers can use this skill to run A-share market screening workflows and generate daily Markdown reports for review. Its outputs should be treated as unverified screening material rather than professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate buy ranges, targets, stop-loss levels, and position sizing from default, cached, or simulated financial data. <br>
Mitigation: Review the generated report and underlying data sources before acting on it, and do not rely on the output as professional financial advice. <br>
Risk: Report summaries can be sent to external Feishu or DingTalk webhooks when push delivery is enabled and configured. <br>
Mitigation: Disable push delivery unless needed, review config.json before execution, and configure webhook URLs only for trusted destinations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxihyv/a-stock-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/dxihyv) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and terminal text with optional webhook-delivered summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write timestamped reports under reports/ and use cached or simulated financial data when live data is unavailable.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
