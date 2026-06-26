## Description: <br>
Automatically generates and sends a daily AI news report with recent articles, highlighted open-source AI projects, and visual Markdown/SVG/PNG outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fireflywwj](https://clawhub.ai/user/fireflywwj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a daily AI information report on demand or through scheduling, then deliver the generated report image to a Feishu chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload generated reports to Feishu when delivery is enabled. <br>
Mitigation: Verify FEISHU_CHAT_ID and Feishu permissions before enabling scheduled delivery. <br>
Risk: GitHub access may use an environment token for higher-rate searches. <br>
Mitigation: Use a limited-scope GitHub token and rotate it according to local credential policy. <br>
Risk: Project descriptions may be sent to a third-party translation service when translation is available. <br>
Mitigation: Avoid including private project descriptions unless that translation path is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fireflywwj/ai-daily-report) <br>
- [SVG report template](artifact/references/report_template.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report plus SVG and PNG report files, with setup and execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu chat configuration for delivery and may use GitHub and RSS sources while generating reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
