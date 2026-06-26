## Description: <br>
ClawFeed 新闻摘要飞书推送，定时抓取全球新闻源，使用 AI 生成中文摘要，并推送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goofyfht-blip](https://clawhub.ai/user/goofyfht-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who monitor global news can use this skill to generate Chinese news digests from BBC, CNBC, Reuters, and Al Jazeera feeds, then send or schedule those digests to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated news summaries to a fixed Feishu recipient. <br>
Mitigation: Confirm the Feishu recipient before running push commands and change the target if it is not yours. <br>
Risk: The workflow depends on local scripts that were not included in the submitted artifact. <br>
Mitigation: Inspect the referenced local scripts before executing digest, push, or daily workflow commands. <br>
Risk: A recurring cron job can continue sending messages after initial setup. <br>
Mitigation: Verify the crontab entry before use and confirm it can be disabled or removed. <br>
Risk: The workflow uses a MiniMax API key. <br>
Mitigation: Check how the API key is stored and avoid exposing it in scripts, logs, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/goofyfht-blip/clawfeed-push) <br>
- [Publisher profile](https://clawhub.ai/user/goofyfht-blip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese news summaries for Feishu delivery and scheduling workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
